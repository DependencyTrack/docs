# Scaling

Dependency-Track requires only PostgreSQL for coordination. Scaling involves
adding instances, splitting workloads, and tuning concurrency.

## Horizontal scaling

Deploy multiple instances pointing at the same database. No additional
infrastructure (message brokers, caches, etc.) is needed.

Work distribution is handled by the embedded
[durable execution engine](../../concepts/architecture/design/durable-execution.md).
All work is distributed across the cluster automatically; single-instance
operations (scheduling, maintenance) are handled via leader election.

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
local (per-instance) and global (cluster-wide).

For a detailed explanation, refer to the
[durable execution design doc](../../concepts/architecture/design/durable-execution.md#concurrency-control).

### Local (worker concurrency)

Each worker limits how many tasks it processes concurrently per instance.
Isolated task queues prevent one workload from starving others.

For example, to increase vulnerability analysis concurrency to 20:

```ini
dt.dex-engine.activity-worker.vuln-analysis.max-concurrency=20
```

For all available workers, queues, and their defaults, see the
[dex engine reference](../../reference/configuration/dex-engine.md#workers).

### Global (queue capacity)

Task queue capacity limits how many tasks can be pending across the entire cluster.
When a queue reaches capacity, the scheduler provides backpressure by pausing
new task creation.

Queue capacity is modifiable at runtime in the administrator panel under *Workflows* -> *Task Queues*,
or via REST API. For default capacities, see the
[dex engine reference](../../reference/configuration/dex-engine.md#task-queues).

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

The durable execution engine batches write operations to reduce database round-trips.
Increasing flush intervals and batch sizes improves throughput at the cost of
higher end-to-end latency. Should generally not be modified unless evidence suggests
that the defaults are problematic.

Refer to the buffer properties in the
[configuration reference](../../reference/configuration/properties.md#dtdex-enginetask-event-bufferflush-interval-ms).

### Run history cache

Workflow run event histories are cached in memory to avoid redundant database reads
during replay. Increase `max-size` on worker nodes with high workflow concurrency
to trade memory for reduced database load.

Refer to [`dt.dex-engine.run-history-cache.*`](../../reference/configuration/properties.md#dtdex-enginerun-history-cachemax-size).

### Maintenance

The maintenance worker periodically deletes completed workflow runs.
At high volume, completed runs accumulate and can increase vacuum and WAL pressure.
Shortening retention or increasing batch size can help keep the database lean.

Refer to [`dt.dex-engine.maintenance.*`](../../reference/configuration/properties.md#dtdex-enginemaintenancerun-retention-duration).

### Notification outbox relay

The outbox relay polls for pending notifications and submits them for publishing.
Increase `batch-size` for high notification volume, or decrease `poll-interval-ms`
for lower latency.

Refer to [`notification.outbox-relay.*`](../../reference/configuration/properties.md#dtnotificationoutbox-relaypoll-interval-ms).

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

Refer to [Data Sources](../../reference/configuration/datasources.md#connection-pool-properties) for pool properties,
and [Centralised connection pooling](configuring-database.md#centralised-connection-pooling) for PgBouncer setup.

## Database tuning

PostgreSQL tuning (autovacuum, WAL compression, `shared_buffers`, etc.) can
impact performance at scale. Refer to [Configuring the database](configuring-database.md)
for tuning recommendations.
