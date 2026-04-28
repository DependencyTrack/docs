# Backing up and restoring

## What to back up

| Component     | What it holds                                                       | Backup approach                                                     |
|---------------|---------------------------------------------------------------------|---------------------------------------------------------------------|
| PostgreSQL    | All product data, durable execution engine state, audit history.    | Logical (`pg_dump`) or physical (PITR) backup.                      |
| File storage  | Short-lived intermediate files (uploaded BOMs, analysis artifacts). | Optional. Loss means in-flight uploads must retry.                  |
| Configuration | Environment variables, secret references.                           | Source-controlled or rendered from templates; not a runtime backup. |

The database is the only component whose loss is unrecoverable.

## Back up the database

For managed PostgreSQL, enable automated backups and point-in-time recovery (PITR) through the provider.
For self-hosted PostgreSQL, follow the standard
[backup and restore](https://www.postgresql.org/docs/current/backup.html) procedures.

When `dt.dex-engine.datasource.name` points at a [separate database](scaling.md#isolate-the-engine-database),
back up both. The two are independent: restoring only one leaves the engine inconsistent with product
state. Use PITR to a common timestamp, or quiesce the API servers before taking coordinated logical
dumps.

## Version considerations

Restore into a Dependency-Track version equal to or newer than the one that produced the backup, and
let schema migrations run on first start. Dependency-Track does not support downgrade restores.

## After restoring

Once you have restored the database and stopped all API servers:

1. Start one instance. Wait for `/health/ready` on port `9000` to return `UP` and confirm schema
   migrations applied cleanly. Then start the rest.
2. Restoring the database rewinds workflow state to the snapshot. The engine resumes in-progress
   runs automatically; runs created after the snapshot no longer exist and clients must re-trigger
   them. See [Durable execution](../../concepts/architecture/design/durable-execution.md) for the
   full model.

If you back up file storage independently, restore it to the same moment as the database. Otherwise,
in-flight uploads at the snapshot fail and clients retry them.
