# About changes in v5

Dependency-Track v5 extensively refactors the platform. It doesn't rewrite
it. Much of the underlying technology and many subsystems carry over from
v4 untouched. Most changes address where v4's design showed its limits:
scalability and reliability, the policy engine, and operational
complexity. A few sections cover new capabilities v4 lacked entirely.

This page summarizes *what changed and why*. For step-by-step upgrade
instructions, see the [upgrade guides](../guides/upgrading/index.md).
To move data from an existing v4 deployment into v5, see
[Migrating from v4 to v5](../guides/administration/migrating-from-v4.md).

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
in-memory pool. PostgreSQL high availability remains your responsibility. See
[Scaling Dependency-Track](../guides/administration/scaling.md).

Long-running work (BOM processing, vulnerability analysis, notification
delivery) runs on a
[durable execution engine](architecture/design/durable-execution.md).
Tasks resume after a restart or crash from where they stopped, instead of
vanishing with the JVM. Failed steps retry automatically with exponential
backoff, rather than requiring manual re-triggering.

Notifications follow the same model. The runtime writes each notification
to a [transactional outbox](architecture/design/notifications.md) in the
same transaction as the change that triggered it. A relay then dispatches
asynchronously. The contract becomes at-least-once delivery: consumers
must tolerate duplicates, but no event silently disappears mid-flight.
See [About notifications](notifications.md) for the user-facing model.

### A single data plane on PostgreSQL

v5 commits to PostgreSQL and drops H2, MySQL, and Microsoft SQL Server.
Concentrating on one engine lets the project use PostgreSQL-specific
features that the v4 multi-database abstraction couldn't. Schema changes
now flow through an explicit, versioned changelog rather than runtime
object-relational mapper (ORM) diffing, so upgrades stay predictable and
roll back cleanly.

Two subsystems that v4 ran as separate processes now live inside the database:

* **Search** runs directly against PostgreSQL. The on-disk
  `~/.dependency-track/index` directory disappears, along with the
  index-corruption and disk-space failure modes that came with it.
  Lucene's fuzzy matching disappears with it. See [What this breaks](#what-this-breaks).
* **Cache** still lives in PostgreSQL, but in `UNLOGGED` tables: no
  write-ahead log overhead, non-durable by design.
  v4 stored cache rows in normal tables and bounded them only through
  recurring cleanup tasks. v5 enforces per-cache TTLs.

Metrics also move into the database. v4 recomputed point-in-time counters
row-by-row in Java tasks. v5 turns metrics into a proper time series,
computed in PostgreSQL. See
[About time-series metrics](time-series-metrics.md).

The schema tightens constraints that v4 deferred to app code under the
multi-database abstraction. Stricter constraints catch bad data at the
persistence layer rather than letting it propagate silently.

The PostgreSQL commitment also unlocks targeted performance work:
partial indexes on common query shapes, table partitioning for high-volume time-series data,
and batched reads and writes to cut network and I/O overhead.

### Policies and notification filtering in CEL

v4's policy editor provided a list of conditions with a fixed set of
operators. v5 backs the same editor with a new engine that is more
efficient than v4's and uses [Common Expression Language][CEL] for
evaluation. An Expression condition lets operators write CEL directly
when the structured conditions are not enough. The same engine drives
[vulnerability policies](vulnerability-policies.md), letting operators
audit or suppress findings before they reach the frontend or trigger a
notification.

CEL also reaches [notifications](notifications.md). A v4 alert filtered
on project, tag, level, and group. A v5 alert can match on any field of
the notification payload through a
[filter expression](../reference/notifications/filter-expressions.md) the
alert carries. For example, an alert can fire only for vulnerabilities at
or exceeding a given severity.

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

### Retention policies for projects and metrics

v5 expires inactive project versions and time-series metrics on
configurable schedules. v4 left both to grow unbounded, so operators
carried stale portfolio data and ever-growing metric tables. See
[Configuring project retention](../guides/administration/configuring-project-retention.md)
and [time-series metrics retention](time-series-metrics.md#daily-partitions-and-bounded-retention).

### Centralized secrets

Credentials for integrations live in one place instead of spreading across
per-feature settings, behind whichever secret-manager provider the
deployment selects. A single store simplifies auditing and rotation: you rotate a compromised
credential in one place, not across scattered configuration screens. See [Managing secrets](../guides/user/managing-secrets.md).

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
  normalize to a single millisecond-precision format. Templates that
  consumed v4's ad-hoc subject objects need a rewrite.
* **REST API v1.** Few endpoints removed, response schemas
  change, and list endpoints enforce pagination by default. See
  [Breaking changes in v5](../reference/api/v5-breaking-changes.md)
  for the full enumeration.
* **Fuzzy vulnerability analysis.** v4's internal analyzer optionally fell back to
  Lucene-based fuzzy matching against the internal vulnerability database
  when a component lacked a CPE. Dropping Lucene removes this capability.
* **Distribution formats.** v4 shipped separate API server and frontend
  container images, a "bundled" container image combining both, and an
  executable WAR. v5 ships container images only, and drops the bundled
  image. Operators on the bundled image or the WAR must move to the
  separate API server and frontend containers.
* **NVD feed mirror.** v4 exposed downloaded NVD feed files at
  `/mirror/nvd/*` so other tools could use Dependency-Track as a local
  NVD mirror. v5 no longer persists the feed files (it has no internal
  use for them), and its file storage abstracts over backends like S3
  rather than assuming a local filesystem to serve from. Dependency-Track
  no longer serves this endpoint. Fetch feeds directly from NIST or run a dedicated mirror.
  See [Running air-gapped](../guides/administration/running-air-gapped.md) for hosting an internal NVD or OSV mirror.

[CEL]: https://cel.dev/
[Protobuf]: https://protobuf.dev/
