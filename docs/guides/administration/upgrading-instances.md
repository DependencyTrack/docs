# Upgrading running instances

This guide covers upgrading a running Dependency-Track cluster to a new version with no planned
downtime. For breaking changes between specific releases, always consult the
[per-release upgrade guides](../upgrading/index.md) before starting.

## When you can upgrade in place

The durable execution engine, leader election, and
[lock-free task claiming](../../concepts/architecture/deployment.md#task-distribution) make it safe
to replace one API server instance at a time as long as:

- The upgrade guide for every intervening version describes no breaking schema changes and calls
  for no full-stop window.
- More than one instance is running. A single-instance deployment cannot upgrade without downtime.

If any of these conditions fail, plan a full-stop upgrade window instead.

## Before you start

- Back up the database and verify the backup. See [Backing up](backing-up.md).
- Read the release notes for every version between the running and target version. Stop and plan a
  full-stop upgrade if any release calls for one.
- Pick the new image tag. Pin a full `X.Y.Z` release tag rather than a snapshot or `latest`. See
  [Container images](../../reference/container-images.md).
- If you run schema migrations in a dedicated container, plan to run it before any new-version API
  server starts. See [init-only containers](../../reference/configuration/init-tasks.md#init-only-containers).
- If you pool connections through PgBouncer in transaction mode, migrations need a direct
  PostgreSQL connection. See [init task data source](../../reference/configuration/init-tasks.md#data-source).

## Rolling upgrade

1. Run schema migrations, either via the dedicated container or by letting the first new-version
   instance run them on startup.

    !!! warning "Raise the startup probe budget first"
        Migrations block startup. If they run longer than the
        [startup probe](configuring-observability.md#configuring-kubernetes-health-probes) allows
        (`failureThreshold` multiplied by `periodSeconds`), the orchestrator restarts the instance
        mid-migration. Instances that start at the same time
        [wait for the init lock](../../reference/configuration/init-tasks.md#lifecycle), and that
        wait counts against the same budget. Check the per-release upgrade guide for migration
        duration warnings, then raise the budget to cover both. Running migrations in an
        [init-only container](../../reference/configuration/init-tasks.md#init-only-containers)
        avoids the problem, because the long-lived containers then start against an
        already-migrated schema.

2. Replace API server instances one at a time using your platform's rolling-update primitive.

    Allow enough time for each instance to shut down gracefully. An instance that stops gracefully
    hands its in-flight background tasks back to the queue, and another instance claims them within
    seconds. An instance killed outright leaves those tasks locked until their lock expires, which
    delays them for the duration of the task's lock timeout. See
    [task processing](../../concepts/architecture/design/durable-execution.md#task-processing).

Old and new instances run side by side against the migrated schema until the roll-out completes.
Cap the roll-out to a single deploy window. Do not leave the cluster running mixed versions
indefinitely.

## Web/worker split

When the cluster [splits API and worker traffic](scaling.md#separate-api-traffic-from-background-work),
upgrade both groups using the same one-at-a-time pattern. Upgrade workers first. Workers poll only
for the task types they register, so tasks that a new-version API tier enqueues stay in the queue
until a worker that can run them exists.

## Rolling back

Dependency-Track does not reverse schema migrations. Once migrations run, returning to the previous
version means restoring the database backup you took before starting, and starting the previous
version against it. Plan the upgrade window with that in mind. See
[Backing up](backing-up.md#version-considerations).

## When to fall back to a full-stop upgrade

Plan a full-stop maintenance window when:

- The release notes call for one explicitly.
- The migration rewrites or locks tables the running version reads or writes. Long-running work
  against new tables only, such as a back-fill, extends startup but does not require stopping the
  cluster.
- You cannot guarantee at least one instance remains running throughout.
