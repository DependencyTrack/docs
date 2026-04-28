# Deploying to production

This guide covers the baseline posture for running Dependency-Track against real workloads. For an overview
of how the components fit together, see
[Deployment topology](../../concepts/architecture/deployment.md). For tuning a deployment under load, see
[Scaling](scaling.md).

## Provision compute and database

### API server instances

A reasonable starting point per instance is **2 GB of memory and 4 CPU cores**. From there, scale up based
on observed load.

Two floors are worth knowing:

- **Below 1 GB of memory**, an instance is unlikely to sustain any meaningful load.
- **Below 2 CPU cores**, the system cannot exploit the high degree of concurrency it relies on (background
  workers, the durable execution engine, and request handling all compete for the same threads).

Accurate sizing depends on workload shape: concurrent frontend users, number of projects in the portfolio,
and BOM upload frequency. Usage patterns vary widely between procurement-only, CI/CD-driven, and mixed
deployments, so observe before scaling. See [Configuring observability](configuring-observability.md) for
the metrics that surface real load.

!!! warning "JVM heap scales with container memory"
    Adding memory raises the JVM heap cap (default 80% of container memory). Confirm via Prometheus heap
    metrics, not `top` or `docker stats`, that the larger heap pays off before over-provisioning. See
    [JVM options](../../reference/configuration/application.md#jvm-options) for the underlying behavior.

### Database

Dependency-Track runs on PostgreSQL, and PostgreSQL becomes the bottleneck before the API server does. Run
a managed offering or a self-hosted instance with monitoring and automated backups, and pin a major version.

A reasonable starting point is **8 GB of memory and 4 CPU cores**; do not go below 4 GB and 2 cores even
for evaluation workloads. The dominant memory consumers are `shared_buffers` (typically ~25% of RAM) and
per-connection working memory (`work_mem` × the sum of pool sizes), so memory pressure rises with both
data volume and cluster size.

Run the database on a dedicated host. Co-locating PostgreSQL with API server instances forces them to
compete for the same CPU, memory, and I/O, and that contention surfaces as unpredictable latency under
load.

When sizing the database host, account for the per-instance connection pool. PostgreSQL's `max_connections`
must cover the sum of all pools across the cluster, plus headroom for migrations, backups, and
administrator sessions:

```text
max_connections >= (instance_count × dt.datasource.pool.max-size) + headroom
```

[`dt.datasource.pool.max-size`](../../reference/configuration/properties.md#dtdatasourcepoolmax-size)
defaults to 30.

For hosting choices, tuning, and upgrade guidance, see [Configuring the database](configuring-database.md).
For supported versions and required extensions, see the
[database reference](../../reference/configuration/database.md).

## Run more than one instance

Run at least two instances against the same database to avoid a single point of failure and to enable rolling
restarts. Instances coordinate only through PostgreSQL; no clustering protocol or peer-to-peer networking
joins the deployment. See [Coordination](../../concepts/architecture/deployment.md#coordination)
for the model and [Recovery from instance failure](../../concepts/architecture/deployment.md#recovery-from-instance-failure)
for what happens when an instance dies.

All instances must share file storage. The default `local` provider works with a shared persistent volume
(for example, NFS); the `s3` provider works in environments where shared volumes are impractical. See
[File storage](../../reference/configuration/file-storage.md).

## Manage secrets outside the container

Manage two classes of secrets separately:

- **Infrastructure secrets** (database password, LDAP bind password) load at startup.
  Mount them as files and reference them via `${file::/path/to/file}` rather than passing them as clear-text
  environment variables. See
  [Loading values from files](../../reference/configuration/application.md#loading-values-from-files).
- **Integration secrets** (API tokens for Jira, Snyk, Trivy, OSS Index, and similar) live in
  Dependency-Track's runtime secret store. See
  [Configuring secret management](configuring-secret-management.md) for the supported backends.

## Configure authentication

Wire Dependency-Track to your identity provider. Local managed users are for evaluation only:

- For OIDC providers (Keycloak, Entra ID, Google, and similar), see [Configuring OIDC](configuring-oidc.md).
- For LDAP and Active Directory, see [Configuring LDAP](configuring-ldap.md).

## Front the API server with TLS

Handle TLS at a reverse proxy or ingress controller rather than in the API server itself. Forward
`X-Forwarded-Proto` and `X-Forwarded-For` so that audit logs and notification links resolve to the public URL.

Each instance listens on two ports: `8080` for the public REST API and `9000` for health checks and
metrics. Direct user-facing traffic to `8080`; direct probes and metric scrapers to `9000`. See
[Configuring observability](configuring-observability.md#configuring-kubernetes-health-probes) for
the health-endpoint contract.

## Set up observability

Scrape Prometheus metrics from `/metrics` on port `9000` and configure liveness, readiness, and startup
probes against `/health/live`, `/health/ready`, and `/health/started` on the same port. Wire both before the
first real workload lands; capacity decisions are guesses without them. See
[Configuring observability](configuring-observability.md) for the full setup.

## Plan for backup and upgrade

Decide and rehearse two procedures before going live.

- **Backup and restore.** A standard PostgreSQL backup covers everything Dependency-Track persists. See
  [Backing up](backing-up.md) for what to back up, how restores affect in-flight workflows, and how to run
  a restore drill.
- **Upgrades.** New versions can roll out without downtime when the release notes permit it. See
  [Upgrading running instances](upgrading-instances.md) for the procedure and the conditions that call for
  a full-stop maintenance window instead.

## Verify the deployment

Before exposing the deployment to users:

1. Confirm `/health/ready` returns `UP` on every instance.
2. Sign in via your configured identity provider.
3. Upload a sample BOM and confirm vulnerability analysis completes. The
   [Quickstart](../../tutorials/quickstart.md) covers the end-to-end flow.
4. Verify metrics arrive in your scraper and health probes pass through the load balancer.
