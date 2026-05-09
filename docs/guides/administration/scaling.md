# Scaling

This guide assumes the deployment already follows the baseline in
[Deploying to production](deploying-to-production.md): more than one instance, shared file storage, a tuned
PostgreSQL, and observability in place. It covers tuning that baseline under load.

## Separate API traffic from background work

By default, every instance serves API traffic **and** runs background workers. As the cluster grows,
request-path latency starts to suffer when background spikes (BOM imports, vulnerability mirroring) saturate
worker threads on the same node.

Activate the `web` profile on instances that should serve API traffic only via
[`dt.config.profile`](../../reference/configuration/properties.md#dtconfigprofile):

```ini linenums="1"
dt.config.profile=web
```

Instances without the profile keep their default behavior and run background workers.

!!! note
    At least one worker node must run for scheduling, vulnerability analysis, notifications, and other
    background work to make progress. Run **at least two worker nodes** in production so a single instance
    failure does not stop background processing entirely.

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

Scale the two groups independently: `web` based on request volume, `worker` based on background workload depth.

## Increase background throughput

The durable execution engine exposes three levers for background throughput, each addressing a different
symptom. For the model behind them, see
[Concurrency control](../../concepts/architecture/design/durable-execution.md#concurrency-control).

!!! warning "More concurrency does not necessarily mean more throughput"
    Dependency-Track targets throughput, and the engine leans heavily on (micro-)batching to amortize
    database round-trips. Past a workload-specific sweet spot, more concurrency can hurt throughput:
    threads compete for the same database connections, locks, and CPU, and batches shrink as work spreads
    across them. Raise `max-concurrency` only when metrics show the workload starving for capacity, and
    verify throughput improves after each change.

**Worker concurrency.** When one workload saturates its worker (for example, vulnerability analysis) while
others have headroom, raise that worker's `max-concurrency` on worker nodes:

```ini
dt.dex-engine.activity-worker.vuln-analysis.max-concurrency=20
```

For the full list of workers and their defaults, see the
[durable execution engine reference](../../reference/configuration/dex-engine.md#workers).

**Queue capacity.** When ingestion is outpacing processing across the cluster (queue depths grow unbounded
under sustained load), lower the queue's capacity to apply backpressure. Once a queue hits capacity, the
scheduler pauses task creation, propagating throttling back to BOM upload clients.

Change capacity at runtime from the administrator panel under *Workflows > Task Queues*, or via the REST
API. Defaults live in the [task queues reference](../../reference/configuration/dex-engine.md#task-queues).

**Lower-level engine tuning.** When metrics show write-buffer flush latency, run-history cache misses, or
notification outbox lag, the engine exposes more knobs. See the
[`dt.dex-engine.*`](../../reference/configuration/properties.md#dtdex-enginetask-event-bufferflush-interval-ms)
and
[`notification.outbox-relay.*`](../../reference/configuration/properties.md#dtnotificationoutbox-relaypoll-interval-ms)
properties.

## Scale workers horizontally

After tuning the vertical knobs, if an activity backlog keeps growing, scale worker instances
horizontally on demand signals from the durable execution engine. Do not scale on CPU or memory
alone: activity workers are I/O-bound (database, registry calls, vulnerability sources) and spend
most of their time waiting, so CPU stays low while tasks queue up.

The engine exposes three Prometheus metrics for this. The management server serves them once you
[turn on Prometheus metrics scraping](configuring-observability.md#enabling-prometheus-metrics-scraping).

| Metric | What it tells you | Use as |
|---|---|---|
| `dt_dex_engine_activity_task_queue_backlog{queueName}` | Approximate count of ready-to-schedule activity tasks per queue, capped at 10000. | Primary scale-up trigger. |
| `dt_dex_engine_activity_task_queue_backlog_age_seconds{queueName}` | Age of the oldest ready-to-schedule activity task per queue. | SLO-aligned secondary trigger. |
| `dt_dex_engine_task_worker_concurrency_utilization{workerType,name}` | Fraction (0–1) of a worker's concurrency slots currently in use. | Scale-down guard. |

Scale up when the backlog exceeds a target per instance, or when the oldest task has waited longer
than the SLO. Scale down only when worker slots stay below a low-use threshold across all
instances.

!!! note "Combine across instances and queues"
    Every instance publishes the backlog and age gauges. Most deployments run all activity workers
    together, so the right HPA signal is "any queue needs scale-up." Collapse to a single value
    with `max(...)` (no `by` clause), for example
    `max(dt_dex_engine_activity_task_queue_backlog)`. Add `by (queueName)` only if you split
    worker types across separate Deployments and want per-queue scaling.

!!! note "Backlog count is approximate"
    The engine caps the count at 10000 per queue to bound query cost. Beyond the cap, the value
    saturates at 10000. This is precise enough to drive scaling decisions.

<!-- vale Google.Headings = NO -->
### KEDA example
<!-- vale Google.Headings = YES -->

[KEDA](https://keda.sh) can drive a Deployment from these metrics. The `ScaledObject` below
targets worker nodes (no `web` profile), scaling on the worst-case backlog across all queues,
with the worst-case oldest-task age as a secondary trigger. Each query wraps the metric in
`avg_over_time(...[5m:30s])` so a transient spike (a single large BOM upload) does not trigger
churn.

??? example "`ScaledObject` manifest"
    ```yaml linenums="1"
    apiVersion: keda.sh/v1alpha1
    kind: ScaledObject
    metadata:
      name: dependencytrack-worker
    spec:
      scaleTargetRef:
        name: dependencytrack-worker
      minReplicaCount: 2
      maxReplicaCount: 5
      triggers:
        - type: prometheus
          metadata:
            serverAddress: http://prometheus.monitoring:9090
            query: avg_over_time(max(dt_dex_engine_activity_task_queue_backlog)[5m:30s])
            threshold: "1000"
        - type: prometheus
          metadata:
            serverAddress: http://prometheus.monitoring:9090
            query: avg_over_time(max(dt_dex_engine_activity_task_queue_backlog_age_seconds)[5m:30s])
            threshold: "300"
    ```

## Pool connections centrally

- **Up to roughly 5 instances** at the default pool size of 30: the per-instance pool works.
- **Beyond that:** switch to a centralized pooler such as PgBouncer and turn off local pooling. Many
  instances each maintaining their own pool inflates database connection count past PostgreSQL's
  `max_connections` faster than vertical Postgres scaling can keep up.

[Provision compute and database](deploying-to-production.md#provision-compute-and-database) covers the
`max_connections` math.

For pool properties, see
[Data sources](../../reference/configuration/datasources.md#connection-pool-properties). For the PgBouncer
setup, see [Centralised connection pooling](configuring-database.md#centralised-connection-pooling).

## Scale vertically

Add memory before adding instances when large BOMs push GC pressure up. Add CPU when worker throughput
plateaus despite headroom in concurrency settings.

To override JVM defaults without replacing them, extend `EXTRA_JAVA_OPTIONS`. For example, to tighten the
GC pause target for latency-sensitive frontend traffic:

```ini
EXTRA_JAVA_OPTIONS="-XX:MaxGCPauseMillis=100"
```

For the shipped JVM defaults and their meaning, see
[JVM options](../../reference/configuration/application.md#jvm-options).

## Isolate the engine database

Point the durable execution engine at a separate PostgreSQL server once its queue vacuuming and WAL activity
start competing with the main database for I/O or autovacuum bandwidth. By default the engine shares the
main Dependency-Track database
([`dt.dex-engine.datasource.name`](../../reference/configuration/properties.md#dtdex-enginedatasourcename)`=default`).

```ini
# Configure a separate data source for the engine.
dt.datasource.engine.url=jdbc:postgresql://engine-postgres:5432/engine
dt.datasource.engine.username=engine
dt.datasource.engine.password=engine
dt.datasource.engine.pool.enabled=true
dt.datasource.engine.pool.max-size=10

# Point the engine at the separate data source.
dt.dex-engine.datasource.name=engine
```

The engine manages its own schema and does not need to share the main database cluster. For full data source
configuration, see [Data sources](../../reference/configuration/datasources.md).

## Tune the database

PostgreSQL tuning (autovacuum, WAL compression, `shared_buffers`, and similar settings) often matters more
than tuning Dependency-Track itself at scale. See
[Configuring the database](configuring-database.md#advanced-tuning) for recommendations.
