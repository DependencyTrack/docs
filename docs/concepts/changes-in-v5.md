# About changes in v5

Dependency-Track v5 extensively refactors the platform. It does not rewrite
it. Much of the underlying technology and many subsystems carry over from
v4 untouched. The changes concentrate on three areas where v4's pain
points lived: the runtime, the policy engine, and the operational model.

This page summarises *what changed and why*. For step-by-step upgrade
instructions, see the [upgrade guides](../guides/upgrading/index.md).

## Why v5

v4 ran as a single API server that owned an in-memory queue and a local
Lucene index, on a database of the operator's choice. That shape suited
small deployments but constrained anyone who needed high availability,
predictable resource usage, or recovery from partial failures.

v5 targets those constraints directly. The platform now scales
horizontally, survives crashes, and commits to a single mature database
engine. Smaller deployments still work, and gain the same guarantees.

## What changed and why

### High availability and durable background work

v5 removes v4's in-process single point of failure (the in-memory queue
and local index). Web and worker nodes now scale independently, and
background work distributes through PostgreSQL-backed queues instead of an
in-memory pool. PostgreSQL itself stays a tier you must operate in HA if
you need full availability. See
[Scaling Dependency-Track](../guides/administration/scaling.md).

Long-running work (BOM processing, vulnerability analysis, notification
delivery) runs on a
[durable execution engine](architecture/design/durable-execution.md).
Tasks resume after a restart or crash from where they stopped, instead of
vanishing with the JVM.

Notifications follow the same model. The runtime writes each notification
to a [transactional outbox](architecture/design/notifications.md) in the
same transaction as the change that triggered it. A relay then dispatches
asynchronously. The contract becomes at-least-once delivery: consumers
must tolerate duplicates, but no event silently disappears mid-flight.
See [About notifications](notifications.md) for the user-facing model.

### A single data plane on PostgreSQL

v5 commits to PostgreSQL and drops H2, MySQL, and Microsoft SQL Server.
Concentrating on one engine lets the project use Postgres-specific
features that the v4 multi-database abstraction could not. Schema changes
now flow through an explicit, versioned changelog rather than runtime ORM
diffing, so upgrades stay predictable and roll back cleanly.

Two subsystems v4 ran out-of-process now live inside the database:

* **Search** runs directly against PostgreSQL. The on-disk
  `~/.dependency-track/index` directory disappears, along with the
  index-corruption and disk-space failure modes that came with it.
  Lucene's fuzzy matching disappears with it. See *What this breaks*.
* **Cache** still lives in PostgreSQL, but in `UNLOGGED` tables: no
  write-ahead log overhead, non-durable by design, which suits a cache.
  v4 stored cache rows in normal tables and bounded them only through
  recurring cleanup tasks. v5 enforces per-cache TTLs and size limits.

Metrics also move into the database. v4 recomputed point-in-time counters
row-by-row in Java tasks. v5 turns metrics into a proper time series,
computed in PostgreSQL. See
[About time-series metrics](time-series-metrics.md).

### Policies and notification filtering in CEL

A policy in v4 lived in the UI as a tree of click-built clauses, capped by
what the editor could express. v5 evaluates policies in
[Common Expression Language][CEL], so a complex rule collapses to a single
readable expression. The same engine drives
[vulnerability policies](vulnerability-policies.md), letting operators
audit or suppress findings before they reach the UI or trigger a
notification.

CEL also reaches [notifications](notifications.md). A v4 alert filtered
on project, tag, level, and group. A v5 alert can match on any field of
the notification payload through a
[filter expression](../reference/notifications/filter-expressions.md) the
alert carries.

### A provider model for replaceable subsystems

Subsystems an operator might reasonably want to swap now sit behind
provider interfaces. File storage ships with local and S3 backends, secret
managers with database and environment-variable backends, and cache with
in-memory and database backends. Vulnerability data sources (NVD, GitHub
Advisories, OSV) and analyzers (internal, OSS Index, Snyk, Trivy, VulnDB)
load through the same model. Choosing a provider becomes a configuration
decision, not a fork. See the
[file storage reference](../reference/configuration/file-storage.md) for
the storage end of the model.

### Component integrity verification

Dependency-Track flags components whose hashes diverge from what the
upstream package repository publishes. The check catches typosquatting and
registry-side tampering, classes of supply chain attack that v4 left to
scanners further down the chain.

### Portfolio access control out of beta

[Portfolio access control](access-control.md#portfolio-access-control)
shipped as a beta feature in v4 with known gaps and noticeable overhead on
larger portfolios. v5 closes those gaps and reworks the implementation so
the cost stays bounded as the project count grows.

### Centralised secrets

Credentials for integrations live in one place instead of spreading across
per-feature settings, behind whichever secret-manager provider the
deployment selects. See [Managing secrets](../guides/user/managing-secrets.md).

### A spec-first REST API v2

v4 generated its OpenAPI specification from server-side annotations. v5
inverts that for a new [v2 API](../reference/api/v2.md): the spec becomes
the contract, and handlers plug into the interfaces it generates. The
[legacy v1 surface](../reference/api/v1.md) stays in place for backward
compatibility.

### A separate management surface

v4 exposed framework-internal counters on the same surface as the REST
API. v5 runs a dedicated management server on a distinct port, with
Prometheus metrics and Kubernetes-style liveness and readiness probes,
putting scrape and probe targets on a lifecycle separate from user-facing
traffic. See
[Configuring observability](../guides/administration/configuring-observability.md).

### Reduced resource footprint

The runtime targets lower baseline memory and CPU than v4 under comparable
workloads. Much of that comes from removing the in-memory queue, the
Lucene index, and v4's metrics rebuild loop.

## What this breaks

These shifts carry breaking changes for clients, integrations, and
notification consumers. The full list, with field-level details and
remediation steps, lives in the
[upgrade guides](../guides/upgrading/index.md). Headline items:

* **Notification schema.** Subjects now use [Protobuf][Protobuf] (see the
  [notification schema reference](../reference/schemas/notification.md)).
  List fields gain a `List` suffix, enum-like values gain a type prefix
  (`INFORMATIONAL` → `LEVEL_INFORMATIONAL`, `SYSTEM` → `SCOPE_SYSTEM`,
  `NEW_VULNERABILITY` → `GROUP_NEW_VULNERABILITY`), and timestamps
  normalise to a single millisecond-precision format. Templates that
  consumed v4's ad-hoc subject objects need a rewrite.
* **Search.** Endpoints under `/api/v1/search` go away, and fuzzy matching
  goes with them.
* **Fuzzy vulnerability analysis.** v4's internal analyzer optionally fell back to
  Lucene-based fuzzy matching against the internal vulnerability database
  when a component lacked a CPE. Dropping Lucene removes this capability.
* **Findings and SARIF.** Findings and SARIF responses change shape, and
  the per-project findings endpoint now paginates by default. See the
  upgrade guide.
* **Removed deprecated endpoints.** Three v4-deprecated paths under
  `/api/v1/policy` and `/api/v1/tag` go away.
* **NVD feed mirror.** v4 exposed downloaded NVD feed files at
  `/mirror/nvd/*` so other tools could use Dependency-Track as a local
  NVD mirror. v5 no longer persists the feed files (it has no internal
  use for them), and its file storage abstracts over backends like S3
  rather than assuming a local filesystem to serve from. The endpoint is
  removed. Consumers should fetch feeds directly from NIST or run a
  dedicated mirror.

[CEL]: https://cel.dev/
[Protobuf]: https://protobuf.dev/
