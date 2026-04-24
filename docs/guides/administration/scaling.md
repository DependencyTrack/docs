# Scaling

Dependency-Track requires only PostgreSQL for coordination. Scaling involves
adding instances, splitting workloads, and tuning concurrency.

## Horizontal scaling

Deploy multiple instances pointing at the same database. No additional
infrastructure (message brokers, caches, etc.) is needed.

Work distribution is handled by the embedded [durable execution engine](../../concepts/architecture/design/durable-execution.md).
Lease-based leader election ensures single-instance operations (scheduling, maintenance)
run on exactly one node. All other work is distributed across the cluster automatically.

### File storage

When running multiple instances, all nodes must have access to the same
[file storage](../../reference/configuration/file-storage.md). The `local` provider works well
with a shared persistent volume (for example, NFS). For environments where shared volumes
are impractical, the `s3` provider is available.

## Web and worker separation

By default, every instance serves API traffic **and** runs background workers.
The `web` config profile disables all background processing, turning an instance
into an API-only node. Activate it via [`dt.config.profile`](../../reference/configuration/properties.md#dtconfigprofile):

```ini linenums="1"
dt.config.profile=web
```

This results in two logical node types:

- **Web**: API only. Lightweight. Scale based on request volume.
- **Worker**: Background processing. Scale based on demand.

!!! note
    At least one worker node must be running at all times.
    Workers handle scheduling, vulnerability analysis, notifications, and other
    background tasks that the system depends on.

### Example

```yaml linenums="1"
services:
  web:
    image: ghcr.io/dependencytrack/hyades-apiserver
    environment:
      DT_CONFIG_PROFILE: "web"
      DT_DATASOURCE_URL: "jdbc:postgresql://postgres:5432/dtrack"
      DT_DATASOURCE_USERNAME: "dtrack"
      DT_DATASOURCE_PASSWORD: "dtrack"

  worker:
    image: ghcr.io/dependencytrack/hyades-apiserver
    environment:
      DT_DATASOURCE_URL: "jdbc:postgresql://postgres:5432/dtrack"
      DT_DATASOURCE_USERNAME: "dtrack"
      DT_DATASOURCE_PASSWORD: "dtrack"
```

## Concurrency control

Task execution concurrency can be controlled at two levels:
local (per-instance) and global (cluster-wide). Both complement each other:
queue capacity controls how much work is queued, while worker concurrency
controls how fast that work is processed.

For a detailed explanation, refer to the
[durable execution design doc](../../concepts/architecture/design/durable-execution.md#concurrency-control).

### Local (worker concurrency)

Each worker limits how many tasks it processes concurrently, per instance.
Isolated task queues prevent one workload from starving others.

Workers are configured via:

```ini
dt.dex-engine.<worker-type>.<worker-name>.max-concurrency=<N>
```

Where `<worker-type>` is either `workflow-worker` or `activity-worker`.

| Worker Type       | Worker Name                    | Queue                           | Default Concurrency |
|-------------------|--------------------------------|---------------------------------|--------------------:|
| `workflow-worker` | `default`                      | `default`                       |                 100 |
| `activity-worker` | `default`                      | `default`                       |                  25 |
| `activity-worker` | `vuln-analysis`                | `vuln-analyses`                 |                  10 |
| `activity-worker` | `artifact-import`              | `artifact-imports`              |                  10 |
| `activity-worker` | `package-metadata-resolution`  | `package-metadata-resolutions`  |                  10 |
| `activity-worker` | `notification`                 | `notifications`                 |                   5 |
| `activity-worker` | `vuln-analysis-reconciliation` | `vuln-analysis-reconciliations` |                   5 |
| `activity-worker` | `policy-evaluation`            | `policy-evaluations`            |                   5 |
| `activity-worker` | `metrics-update`               | `metrics-updates`               |                   5 |

For example, to increase vulnerability analysis concurrency to 20:

```ini
dt.dex-engine.activity-worker.vuln-analysis.max-concurrency=20
```

### Global (queue capacity)

Task queue capacity limits how many tasks can be pending across the entire cluster.
When a queue reaches capacity, the scheduler stops creating new tasks for that queue,
providing backpressure. Workflow runs remain in their current state until capacity
becomes available.

The default capacities are:

| Type       | Queue                           | Default Capacity |
|------------|---------------------------------|-----------------:|
| `workflow` | `default`                       |             1000 |
| `activity` | `default`                       |             1000 |
| `activity` | `artifact-imports`              |               25 |
| `activity` | `metrics-updates`               |               25 |
| `activity` | `notifications`                 |               25 |
| `activity` | `package-metadata-resolutions`  |               25 |
| `activity` | `policy-evaluations`            |               25 |
| `activity` | `vuln-analyses`                 |               25 |
| `activity` | `vuln-analysis-reconciliations` |               25 |

Queue capacity is modifiable at runtime in the administrator panel under *Workflows* -> *Task Queues*,
or via REST API. As last resort, it can be controlled by directly modifying the
`dex_workflow_task_queue` and `dex_activity_task_queue` database tables.

## Vertical scaling

Allocate more CPU and memory to containers. The default JVM options are set
via the `JAVA_OPTIONS` environment variable:

```text linenums="1"
-XX:+UseG1GC
-XX:+UseStringDeduplication
-XX:+UseCompactObjectHeaders
-XX:MaxGCPauseMillis=250
-XX:MaxRAMPercentage=80.0
```

`-XX:MaxRAMPercentage=80.0` allows the JVM heap to use up to 80% of the container's
available memory. The remaining 20% covers off-heap memory, thread stacks, and the OS.

Additional flags can be passed via `EXTRA_JAVA_OPTIONS` without overriding the defaults:

```ini
EXTRA_JAVA_OPTIONS="-XX:MaxGCPauseMillis=100"
```

More CPU benefits worker throughput; more memory benefits caching and large BOM processing.

## dex engine tuning

### Buffers

The durable execution engine batches certain write operations to reduce database
round-trips. Each buffer has a configurable flush interval and max batch size.

Increasing flush intervals and batch sizes improves throughput at the cost of
higher end-to-end latency. Decreasing them reduces latency but increases
database load. Should generally not be modified unless evidence suggests
that the defaults are problematic.

Configuration:

- [`dt.dex-engine.task-event-buffer.flush-interval-ms`](../../reference/configuration/properties.md#dtdex-enginetask-event-bufferflush-interval-ms)
- [`dt.dex-engine.task-event-buffer.max-batch-size`](../../reference/configuration/properties.md#dtdex-enginetask-event-buffermax-batch-size)
- [`dt.dex-engine.external-event-buffer.flush-interval-ms`](../../reference/configuration/properties.md#dtdex-engineexternal-event-bufferflush-interval-ms)
- [`dt.dex-engine.external-event-buffer.max-batch-size`](../../reference/configuration/properties.md#dtdex-engineexternal-event-buffermax-batch-size)
- [`dt.dex-engine.activity-task-heartbeat-buffer.flush-interval-ms`](../../reference/configuration/properties.md#dtdex-engineactivity-task-heartbeat-bufferflush-interval-ms)
- [`dt.dex-engine.activity-task-heartbeat-buffer.max-batch-size`](../../reference/configuration/properties.md#dtdex-engineactivity-task-heartbeat-buffermax-batch-size)

### Run history cache

Workflow run event histories are cached in memory to avoid redundant database reads
during replay. Increase `max-size` on worker nodes with high workflow concurrency.
This trades memory for reduced database load.

Configuration:

- [`dt.dex-engine.run-history-cache.max-size`](../../reference/configuration/properties.md#dtdex-enginerun-history-cachemax-size)
- [`dt.dex-engine.run-history-cache.evict-after-access-ms`](../../reference/configuration/properties.md#dtdex-enginerun-history-cacheevict-after-access-ms)

### Maintenance

The maintenance worker periodically deletes completed workflow runs.
At high volume, completed runs accumulate and can increase vacuum and WAL pressure.
Shortening retention or increasing batch size can help keep the database lean,
but larger deletion batches cause more I/O per maintenance cycle.

Configuration:

- [`dt.dex-engine.maintenance.run-retention-duration`](../../reference/configuration/properties.md#dtdex-enginemaintenancerun-retention-duration)
- [`dt.dex-engine.maintenance.run-deletion-batch-size`](../../reference/configuration/properties.md#dtdex-enginemaintenancerun-deletion-batch-size)

### Notification outbox relay

The outbox relay polls for pending notifications and submits them for publishing.
Increase `batch-size` for environments with high notification volume.
Decrease `poll-interval-ms` for lower notification latency.

Configuration:

- [`notification.outbox-relay.poll-interval-ms`](../../reference/configuration/properties.md#dtnotificationoutbox-relaypoll-interval-ms)
- [`notification.outbox-relay.batch-size`](../../reference/configuration/properties.md#dtnotificationoutbox-relaybatch-size)

## Separate database for dex

By default, the durable execution engine uses the app database
([`dt.dex-engine.datasource.name`](../../reference/configuration/properties.md#dtdex-enginedatasourcename)`=default`). For larger deployments, pointing dex
at a separate PostgreSQL instance isolates its queue vacuuming and WAL activity
from the main app database.

```ini
# Configure a separate data source for dex
dt.datasource.dex.url=jdbc:postgresql://dex-postgres:5432/dex
dt.datasource.dex.username=dex
dt.datasource.dex.password=dex
dt.datasource.dex.pool.enabled=true
dt.datasource.dex.pool.max-size=10

# Point dex at the separate data source
dt.dex-engine.datasource.name=dex
```

Refer to [Data Sources](../../reference/configuration/datasources.md) for full data source configuration.

!!! note
    The durable execution engine manages its own schema.
    It does not need to share the main database cluster.

## Connection pooling

Each instance maintains a local connection pool. The default maximum pool size
is **20** ([`dt.datasource.pool.max-size`](../../reference/configuration/properties.md#dtdatasourcepoolmax-size)). When increasing worker concurrency,
ensure the pool is large enough to support the combined load of API requests
and background processing.

- **1-5 instances**: Local connection pooling (the default) is sufficient.
- **5+ instances**: Consider centralised pooling (for example, PgBouncer) and turn off local pooling.
- Ensure PostgreSQL's `max_connections` accounts for the sum of all pools.

Refer to [Data Sources - Connection Pooling](../../reference/configuration/datasources.md#connection-pooling) for details.

## Database tuning

PostgreSQL tuning (autovacuum, WAL compression, `shared_buffers`, etc.) can
impact performance at scale. Refer to [Database](../../reference/configuration/database.md)
for recommendations.
