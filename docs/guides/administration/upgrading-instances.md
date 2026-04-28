# Upgrading running instances

This guide covers upgrading a running Dependency-Track cluster to a new version with no planned
downtime. For breaking changes between specific releases, always consult the
[per-release upgrade guides](../upgrading/index.md) before starting.

## When you can upgrade in place

The durable execution engine, leader election, and
[lock-free task claiming](../../concepts/architecture/deployment.md#task-distribution) make it safe
to replace one API server instance at a time as long as:

- The release notes describe no breaking schema changes that require all instances to stop.
- The destination version's Liquibase migrations are additive against the running schema.
- More than one instance is running. A single-instance deployment cannot upgrade without downtime.

If any of these conditions fail, plan a full-stop upgrade window instead.

## Before you start

- Back up the database and verify the backup. See [Backing up](backing-up.md).
- Read the release notes for every version between the running and target version. Stop and plan a
  full-stop upgrade if any release calls for one.
- If you run schema migrations in a dedicated container (recommended for large deployments and
  PgBouncer in transaction mode), plan to run it before any new-version API server starts. See
  [Schema migration credentials](configuring-database.md#schema-migration-credentials).

## Rolling upgrade

1. Run schema migrations, either via the dedicated container or by letting the first new-version
   instance run them on startup.
2. Replace API server instances one at a time using your platform's rolling-update primitive.
   Background tasks claimed by an instance that stops mid-flight return to the queue when the
   database transaction ends; another instance picks them up on its next poll.

Old and new instances run side by side until the roll-out completes. The "additive migrations"
condition listed earlier is what makes that safe: the old version must keep working against the
migrated schema for the duration of the roll-out. Cap the roll-out to a single deploy window. Do
not leave the cluster running mixed versions indefinitely.

If a migration fails partway and leaves the Liquibase change-log lock held, clear the lock in
PostgreSQL before retrying the upgrade.

## Web/worker split

When the cluster [splits API and worker traffic](scaling.md#separate-api-traffic-from-background-work),
upgrade both groups using the same one-at-a-time pattern. Upgrade workers first so the API tier
always talks to a database whose schema the workers already understand.

## When to fall back to a full-stop upgrade

Plan a full-stop maintenance window when:

- The release notes call for one explicitly.
- The migration involves long-running data back-fills or partition rewrites.
- You cannot guarantee at least one instance remains running throughout.
