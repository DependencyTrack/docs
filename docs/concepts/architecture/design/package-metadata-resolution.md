# Package metadata resolution

## Overview

The package metadata resolution system retrieves metadata for packages from upstream
repositories. This includes latest available versions, artifact hashes, and publish timestamps.
Dependency-Track uses this data for latest version checks, component age policies, and integrity verification.

A singleton [durable workflow](durable-execution.md) orchestrates resolution and
processes packages in controlled batches. ADR-015 documents the data model.

## Responsible consumption of public infrastructure

Public registries like Maven Central, npm, and PyPI share a finite pool of bandwidth across all consumers.
Sonatype has documented that [1% of IP addresses account for 83% of Maven Central's total bandwidth][maven-overconsumption],
and that registries have begun enforcing [organization-level throttling][maven-tragedy] in response,
returning HTTP 429 errors to excessive consumers.

For a system like Dependency-Track, which may track hundreds of thousands of components across many
projects, this has direct architectural implications. Making an HTTP request per component on every
BOM upload or scheduled analysis cycle is not viable. Neither is spawning hundreds of concurrent
requests against upstream registries. Both patterns would quickly exhaust rate limits, especially
in larger deployments where many API server instances run concurrently.

The resolution system thus favors scheduled, controlled processing over
ad-hoc lookups. The system identifies components needing metadata resolution in batches, resolves
them sequentially per resolver, and persists results with enough provenance to avoid redundant upstream requests.

Resolvers also issue [conditional HTTP requests][rfc-conditional] when refreshing
data. A small shared cache stores each upstream response body together with its `ETag` and
`Last-Modified` validators. Refreshes after the in-process freshness window send `If-None-Match`
(or `If-Modified-Since`) and most often exchange a small `304 Not Modified` rather than a full
metadata document. This cuts upstream bandwidth without changing how often the system contacts the
registry, and on registries that exempt `304` responses from rate limiting (notably the GitHub API)
it also conserves quota. Sonatype's
[*Open is not costless: reclaiming sustainable infrastructure*][open-not-costless] post explains the motivation.

## Data model

Two tables form a two-level hierarchy, both keyed by PURL:

* `PACKAGE_METADATA`: Keyed by PURL *without version, qualifiers, or subpath*
  (for example, `pkg:maven/com.acme/acme-lib`). Stores the latest available version and resolution provenance.
  One record per package.
* `PACKAGE_ARTIFACT_METADATA`: Keyed by full PURL *including qualifiers and subpath*
  (for example, `pkg:maven/com.acme/acme-lib@1.2.3?type=jar`). Stores artifact hashes, publish timestamp,
  and resolution provenance. One record per distinct artifact. Has a foreign key to `PACKAGE_METADATA`.

This separates package-level information (latest version) from artifact-level information
(hashes, publish timestamp). The FK constraint enforces that artifact metadata cannot exist
without corresponding package metadata, and the orchestration logic respects the resulting
write-order dependency.

Refer to ADR-015 for the full rationale.

### Persistence

Both tables use `COALESCE`-based upserts that preserve existing non-null values.
A temporal guard (`WHERE "RESOLVED_AT" < EXCLUDED."RESOLVED_AT"`) prevents older results
from overwriting newer ones. Writes use PostgreSQL `UNNEST` to batch many rows
per statement, reducing round trips.

## Workflow

Package metadata resolution is a singleton [durable workflow](durable-execution.md).

### Singleton constraint

The workflow uses a fixed instance ID (`resolve-package-metadata`). The durable execution engine enforces
that only a single execution of a given workflow instance in non-terminal state can exist at
any moment. Attempts to create a run while one is already active are silently deduplicated.

This guarantees that at most one resolution workflow is active across the entire cluster,
regardless of how many API server instances are running. Concurrent resolution attempts are
structurally impossible, which prevents redundant upstream requests and data races during
persistence.

### Triggers

Three situations trigger the workflow:

| Trigger         | When                                                               |
|:----------------|:-------------------------------------------------------------------|
| Scheduled       | Configurable cron schedule                                         |
| BOM upload      | After importing a BOM that contains components                     |
| Manual analysis | When a user manually triggers vulnerability analysis for a project |

All triggers create a run with the same singleton instance ID. If a run is already active,
the creation request is a no-op. This makes triggers cheap to invoke, as the singleton constraint
handles deduplication.

### Structure

```mermaid
sequenceDiagram
    participant W as resolve-package-metadata<br/><<Workflow>>
    participant F as fetch-candidates<br/><<Activity>>
    participant R as resolve-purl-metadata<br/><<Activity>>

    activate W
    W ->> F: Fetch resolution candidates
    activate F
    F -->> W: Candidate groups (by resolver)
    deactivate F
    alt No candidates
        Note over W: Complete
    else Has candidates
        par for each resolver
            W ->> R: Resolve batch
            activate R
            R -->> W: Done (or failure)
            deactivate R
        end
        Note over W: Continue-as-new
    end
    deactivate W
```

### Candidate fetching

| Activity                                        | Task Queue |
|:------------------------------------------------|:-----------|
| `fetch-package-metadata-resolution-candidates`  | `default`  |

A PURL is eligible for resolution if:

* No `PACKAGE_ARTIFACT_METADATA` record exists for it, or
* no `PACKAGE_METADATA` record exists for it, or
* the corresponding `PACKAGE_METADATA` was last resolved over 24 hours ago.

The activity fetches candidates in batches of 250 and groups them by resolver. Each PURL maps
to the first resolver whose `normalize` method returns a non-null result. The activity groups PURLs with no
matching resolver under an empty resolver name. The resolve activity persists
empty results for these so they don't re-appear as candidates in later batches.

### Resolution

| Activity                 | Task Queue                     |
|:-------------------------|:-------------------------------|
| `resolve-purl-metadata`  | `package-metadata-resolutions` |

One activity per resolver processes its assigned PURLs sequentially. Different resolver
activities run concurrently.

For each PURL, the activity:

1. Checks if the resolver already produced a result within the last 5 minutes (idempotency guard for retries).
2. Normalizes the PURL via the resolver factory.
3. Looks up configured repositories for the PURL type, ordered by resolution priority.
4. Iterates repositories, respecting internal/external classification, invoking the resolver
   until one succeeds or none remain.
5. Buffers results and flushes to the database in batches of 25.

If a resolver signals a retryable error (for example, HTTP 429), the activity flushes any buffered
results and propagates the error. The durable execution engine then retries the activity with backoff.
The activity catches non-retryable errors for individual PURLs and persists an empty result,
preventing the PURL from becoming a candidate again immediately.

#### Retry policy

| Parameter            | Value |
|:---------------------|:------|
| Initial delay        | 5&nbsp;s  |
| Delay multiplier     | 2x    |
| Randomization factor | 0.3   |
| Max delay            | 1&nbsp;m  |
| Max attempts         | 3     |

### Continue-as-new

After processing a batch, the workflow uses `continueAsNew` to start a fresh run that
picks up the next batch. This prevents unbounded history growth: each run's event history
covers only one batch. Without this, a single run resolving thousands of packages would
accumulate a large history that degrades replay performance.

It also creates a natural checkpoint. If the process stops between batches,
the next run starts with a fresh candidate query, skipping already-resolved PURLs
based on the `RESOLVED_AT` timestamps in the database.

The cycle continues until no candidates remain, at which point the workflow
completes normally.

## Concurrency control

Concurrency control operates at four levels:

| Level    | Mechanism                                     | Effect                                             |
|:---------|:----------------------------------------------|:---------------------------------------------------|
| Cluster  | Singleton instance ID                         | At most one resolution workflow across the cluster |
| Engine   | `package-metadata-resolutions` queue capacity | Limits pending resolve activities (default: 25)    |
| Node     | Activity worker max concurrency               | Limits parallel activity execution per node        |
| Resolver | Sequential processing within each activity    | Each resolver processes one PURL at a time         |

Refer to [durable execution](durable-execution.md) for how queue capacity and worker
concurrency interact.

## Resolver extension point

Resolvers are pluggable via the plugin system. The API surface consists of two interfaces:

* **`PackageMetadataResolverFactory`**: Creates resolver instances. Declares whether the resolver
  needs a repository, normalizes PURLs (returning `null` to signal non-support), and exposes the
  extension name.
* **`PackageMetadataResolver`**: Given a normalized PURL and an optional repository,
  returns `PackageMetadata` or `null`.

A single resolver handles a given PURL (first match wins based on factory ordering).
Within that resolver, a single repository provides the result (first success wins based
on the configured resolution order).

Resolvers route their upstream fetches through a shared HTTP-resource cache that
handles ETag and Last-Modified revalidation transparently. While an entry stays fresh the
cache serves the body without contacting the upstream; once stale but still cached,
the cache sends validators and a `304 Not Modified` replays the body, while a `200 OK` replaces
the entry. The cache negatively caches `404` and `410` responses so absent packages do not re-issue
requests within the freshness window. The cache uses a separate namespace per resolver and pluggable
between in-memory and database providers via the existing cache provider mechanism.

The candidate query marks a PURL as eligible after 24 hours, but the resolver-side cache
typically prevents that from translating to a full upstream transfer.

## Maintenance

A scheduled task cleans up orphaned metadata:

1. Deletes `PACKAGE_ARTIFACT_METADATA` rows where no `COMPONENT` with a matching PURL exists.
2. Deletes `PACKAGE_METADATA` rows where no `PACKAGE_ARTIFACT_METADATA` references them.

The two-step cascade prevents unbounded table growth as components leave the portfolio.
Distributed locking ensures only one node executes cleanup at a time.

## Resiliency

The [durable execution](durable-execution.md) engine handles crash recovery and retries
transparently:

* If a node crashes mid-resolution, the workflow resumes from the last completed step on restart.
  Results already flushed to the database are not re-processed, because the 5-minute idempotency
  window in the activity causes the activity to skip recently resolved PURLs.
* When resolution fails for a specific resolver even after exhausting retries, the workflow
  catches the `ActivityFailureException`, logs the failure, and continues. The workflow persists
  results from other resolvers normally.
* On graceful shutdown, the activity checks for thread interruption before each PURL,
  flushes buffered results, and propagates the interruption.

[maven-overconsumption]: https://www.sonatype.com/blog/beyond-ips-addressing-organizational-overconsumption-in-maven-central
[maven-tragedy]: https://www.sonatype.com/blog/maven-central-and-the-tragedy-of-the-commons
[open-not-costless]: https://www.sonatype.com/blog/open-is-not-costless-reclaiming-sustainable-infrastructure
[rfc-conditional]: https://www.rfc-editor.org/rfc/rfc7232
