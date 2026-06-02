# Init tasks

Init tasks are one-time operations the API server performs at startup, before
the main server begins serving traffic. They prepare the database schema, seed
default objects, and bring the durable execution engine to a consistent state.

## Lifecycle

Init tasks run before the HTTP listener starts and before background workers
initialize. They block startup. If any task fails, the JVM exits and the
container does not begin serving traffic.

The management server starts before init tasks run and exposes the
[startup health endpoint](../../guides/administration/configuring-observability.md#configuring-kubernetes-health-probes)
at `/health/started`, which reports per-task status (`STARTED`, `COMPLETED`,
`FAILED`) during execution.

By default, init tasks run in every API server container. To coordinate across
instances, the executor acquires a session-level PostgreSQL [advisory lock],
so only one container performs each task at a time. Remaining containers wait
for the lock, then confirm there is nothing left to do.

!!! warning
    Session-level advisory locks are incompatible with PgBouncer in
    `transaction` pooling mode. When using a transaction-mode connection
    pooler, configure a separate [init data source](#data-source) that
    connects directly to PostgreSQL.

## Tasks

| Task | Purpose | Enable property |
|------|---------|-----------------|
| Database migration | Runs [Flyway](database.md#schema-migrations) migrations against the Dependency-Track schema. Creates required [extensions](database.md#extensions). | [`dt.init-task.database-migration.enabled`](properties.md#dtinit-taskdatabase-migrationenabled) |
| Database partition maintenance | Creates [table partitions] required for [time series metrics](../../concepts/time-series-metrics.md). | [`dt.init-task.database-partition-maintenance.enabled`](properties.md#dtinit-taskdatabase-partition-maintenanceenabled) |
| Database seeding | Populates default permissions, teams, users, licenses, license groups, repositories, and configuration properties. Idempotent. Skips on later startups when the build identifier has not changed. | [`dt.init-task.database-seeding.enabled`](properties.md#dtinit-taskdatabase-seedingenabled) |
| Dex engine database migration | Runs schema migrations for the [durable execution engine](dex-engine.md). | [`dt.init-task.dex-engine-database-migration.enabled`](properties.md#dtinit-taskdex-engine-database-migrationenabled) |

Per-task enable properties take effect only when
[`dt.init-tasks.enabled`](properties.md#dtinit-tasksenabled) is `true`.

## Data source

By default, init tasks use the `default` [data source](datasources.md).
Override this with
[`dt.init-tasks.datasource.name`](properties.md#dtinit-tasksdatasourcename)
to route them through a separate connection pool.

The most common reason: centralized connection pooling with PgBouncer in
`transaction` mode, which requires init tasks to bypass the pooler and
connect to PostgreSQL directly. The default data source connects through
PgBouncer, while the init data source connects to PostgreSQL directly so
session-level advisory locks remain usable. See
[centralized connection pooling](../../guides/administration/configuring-database.md#centralised-connection-pooling)
for an example.

When the init data source exists solely to serve init tasks, set
[`dt.init-tasks.datasource.close-after-completion`](properties.md#dtinit-tasksdatasourceclose-after-completion)
to `true`. The API server closes the connection pool once tasks finish,
freeing its connections.

## Init-only containers

Setting
[`dt.init-tasks.exit-after-completion`](properties.md#dtinit-tasksexit-after-completion)
to `true` causes the JVM to exit with status `0` once init tasks succeed,
without starting the main server. This supports a dedicated init container
pattern, where a short-lived container runs init tasks and exits before
long-lived API server containers start.

In this pattern, the long-lived containers set
[`dt.init-tasks.enabled`](properties.md#dtinit-tasksenabled) to `false` to
skip init tasks on startup.

## Configuration

* [`dt.init-tasks.enabled`](properties.md#dtinit-tasksenabled)
* [`dt.init-tasks.datasource.name`](properties.md#dtinit-tasksdatasourcename)
* [`dt.init-tasks.datasource.close-after-completion`](properties.md#dtinit-tasksdatasourceclose-after-completion)
* [`dt.init-tasks.exit-after-completion`](properties.md#dtinit-tasksexit-after-completion)
* [`dt.init-task.database-migration.enabled`](properties.md#dtinit-taskdatabase-migrationenabled)
* [`dt.init-task.database-partition-maintenance.enabled`](properties.md#dtinit-taskdatabase-partition-maintenanceenabled)
* [`dt.init-task.database-seeding.enabled`](properties.md#dtinit-taskdatabase-seedingenabled)
* [`dt.init-task.dex-engine-database-migration.enabled`](properties.md#dtinit-taskdex-engine-database-migrationenabled)

[advisory lock]: https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS
[table partitions]: https://www.postgresql.org/docs/current/ddl-partitioning.html
