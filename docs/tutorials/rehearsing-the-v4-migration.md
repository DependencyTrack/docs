# Rehearsing the v4 to v5 migration

In this tutorial, we will rehearse a v4 to v5 migration against a throwaway v5 stack,
using our existing v4 deployment as a read-only source.
By the end, we will have a working v5 instance populated with our real data,
safely isolated from production.

The real cutover lives in the [v4 to v5 migration guide](../guides/administration/migrating-from-v4.md).
This tutorial walks the same workflow so we can shake out connectivity, data quirks,
and lossy transformations before the production run.

!!! warning "v4 should not take writes during the rehearsal"

    The migrator does not write to v4, but it also does not take locks on the source.
    Concurrent v4 writers during extraction produce inconsistent extracts, which means
    rows that reference each other can land in disagreeing states in the sandbox.
    For the rehearsal we have three options, in decreasing order of fidelity:

    1. **Stop the v4 API server** for the duration of extraction, the same as the production cutover.
    2. **Run the migrator against a snapshot or restored copy** of the v4 database rather than the live instance.
    3. **Accept inconsistent results.** Useful for shaking out connectivity and lossy-transform behavior,
       but not for trusting row counts or referential integrity.

## What we need

- [Docker](https://docs.docker.com/get-docker/) and [Compose v2](https://docs.docker.com/compose/install/).
- A reachable v4 instance on version **4.14.2 or later**, backed by either:
    - **PostgreSQL**, or
    - **Microsoft SQL Server**.
- The JDBC URL, username, and password for that v4 database.

!!! note

    If v4 runs on the host, use `host.docker.internal` instead of `localhost` in the v4 JDBC URL.
    The migrator runs inside a container and cannot reach the host's `localhost`.

## Downloading the compose file

We reuse the quickstart compose file for the v5 destination:

```shell
curl -O https://raw.githubusercontent.com/DependencyTrack/docs/main/docs/tutorials/docker-compose.quickstart.yml
```

??? note "Compose file contents"
    ```yaml linenums="1"
    --8<-- "docs/tutorials/docker-compose.quickstart.yml"
    ```

!!! warning "Running on the same host as v4"

    The compose file declares the Compose project name `Dependency-Track`,
    which Docker normalizes to `dependency-track`.
    If we also run our v4 stack on this host via Docker Compose under a project name
    that normalizes to the same value, the tutorial's commands target the v4 project
    and stop or remove v4 services.
    In that case, we edit the `name:` field at the top of the downloaded compose file
    to a unique value, for example `dtrack-v5-sandbox`, before continuing.
    We also adjust the network name in the migrator alias to match, for example
    `--network=dtrack-v5-sandbox_default`.

## Starting only Postgres

We bring up the database service on its own:

```shell
docker compose -f docker-compose.quickstart.yml up -d postgres
```

We do **not** start `apiserver` yet.
The v5 apiserver seeds tables on first boot that the migrator must populate from v4,
so starting it before the migration would corrupt the destination.

We wait for the container to report healthy:

```shell
docker compose -f docker-compose.quickstart.yml ps postgres
```

The output looks like this:

```text linenums="1"
NAME                       IMAGE                STATUS                   PORTS
dependency-track-postgres-1   postgres:18-alpine   Up 12 seconds (healthy)  5432/tcp
```

## Aliasing the migrator

The migrator ships as a container image.
We define a shell alias that attaches the container to the compose network
so it can reach Postgres at `postgres:5432`.
We substitute `<version>` with the migrator image tag matching our target v5 release.

```shell linenums="1"
alias v4-migrator='docker run --rm -it --network=dependency-track_default ghcr.io/dependencytrack/v4-migrator:<version>'
```

After this, the rest of the tutorial uses `v4-migrator <subcommand>`.

!!! note ":material-powershell: PowerShell users"

    PowerShell has no shell alias that forwards arguments, so we define a function instead:

    ```powershell linenums="1"
    function v4-migrator { docker run --rm -it --network=dependency-track_default ghcr.io/dependencytrack/v4-migrator:<version> @args }
    ```

    Subsequent `v4-migrator` commands span multiple lines using `\` for line continuation,
    which is bash and zsh syntax.
    In PowerShell, we replace each trailing `\` with a backtick (`` ` ``),
    or paste each command on a single line.

The network name comes from the compose project name (`Dependency-Track`),
which Docker normalizes to lowercase and suffixes with `_default`.
We can confirm with `docker network ls`:

```shell
docker network ls
```

Expected output:

```text linenums="1"
NETWORK ID     NAME                         DRIVER    SCOPE
2f9b1c4d5e6a   bridge                       bridge    local
8a7b6c5d4e3f   dependency-track_default     bridge    local
1a2b3c4d5e6f   host                         host      local
0f9e8d7c6b5a   none                         null      local
```

## Bootstrapping the v5 schema

We apply the v5 schema to the empty target:

```shell linenums="1"
v4-migrator bootstrap \
  --target-url 'jdbc:postgresql://postgres:5432/dtrack' \
  --target-user dtrack \
  --target-pass dtrack
```

Expected output:

```text linenums="1"
Applying v5 Flyway schema up to 202605111028
...
Bootstrap complete. Flyway head = 202605111028. Run 'extract' or 'run' next.
```

After this, the target has the v5 schema but no rows.

## Verifying the empty target

We run preflight against the freshly bootstrapped target:

```shell linenums="1"
v4-migrator verify \
  --target-url 'jdbc:postgresql://postgres:5432/dtrack' \
  --target-user dtrack \
  --target-pass dtrack
```

Expected output:

```text linenums="1"
[Schema]
  OK    Schema version = 202605111028

[Row counts]
  Table                       Source      Staging           v5
  (no source configured)
  LICENSE                          -            0            0
  TEAM                             -            0            0
  ...

[Probes]
  Staging schema "dt_v4_migration" not present — run extract first.

[Constraints]
  13 CHECK constraint(s) hold across 55 loaded table(s)
```

If the schema version is anything else or any row count is non-zero,
the rest of the rehearsal will not work.

## Dry-running the migration

Before writing anything, we ask the migrator to print its plan.
We substitute our v4 connection details into the source flags.
The only difference between a PostgreSQL and a Microsoft SQL Server v4 source is the JDBC URL:

!!! tip "Password prompts"

    The commands below pass `--source-pass` without an argument.
    The migrator then prompts for the password interactively, keeping the secret out of shell history and `ps` output.
    To supply it inline, write `--source-pass <v4-pass>` instead.

=== ":simple-postgresql: PostgreSQL v4 source"

    ```shell linenums="1"
    v4-migrator run \
      --target-url 'jdbc:postgresql://postgres:5432/dtrack' --target-user dtrack --target-pass dtrack \
      --source-url 'jdbc:postgresql://<v4-host>:5432/<v4-db>' --source-user <v4-user> --source-pass \
      --metrics-retention-days 30 \
      --dry-run
    ```

=== ":material-microsoft: Microsoft SQL Server v4 source"

    ```shell linenums="1"
    v4-migrator run \
      --target-url 'jdbc:postgresql://postgres:5432/dtrack' --target-user dtrack --target-pass dtrack \
      --source-url 'jdbc:sqlserver://<v4-host>:1433;databaseName=<v4-db>' --source-user <v4-user> --source-pass \
      --metrics-retention-days 30 \
      --dry-run
    ```

The migrator requires `--metrics-retention-days`.
v5 trims time-series metrics on a retention window that v4 does not have,
so the migrator forces an explicit choice.
We pass `30` to keep this walkthrough fast, since longer windows extend the load phase noticeably.
For the production run we revisit this value, see the
[migration guide](../guides/administration/migrating-from-v4.md#4-extract-transform-load) for the trade-offs.

`--dry-run` writes nothing to either database.
The migrator prints the plan and exits.

## Running the migration

We drop `--dry-run` and run the real extract, transform, and load:

=== ":simple-postgresql: PostgreSQL v4 source"

    ```shell linenums="1"
    v4-migrator run \
      --target-url 'jdbc:postgresql://postgres:5432/dtrack' --target-user dtrack --target-pass dtrack \
      --source-url 'jdbc:postgresql://<v4-host>:5432/<v4-db>' --source-user <v4-user> --source-pass \
      --metrics-retention-days 30
    ```

=== ":material-microsoft: Microsoft SQL Server v4 source"

    ```shell linenums="1"
    v4-migrator run \
      --target-url 'jdbc:postgresql://postgres:5432/dtrack' --target-user dtrack --target-pass dtrack \
      --source-url 'jdbc:sqlserver://<v4-host>:1433;databaseName=<v4-db>' --source-user <v4-user> --source-pass \
      --metrics-retention-days 30
    ```

Runtime depends on the size of our v4 dataset.
The migrator prints per-table progress and a heartbeat every five seconds for long-running tables:

```text linenums="1"
MetricsRetention - Metrics retention set to 30 days (cutoff = 2026-04-15T11:38:10.636499285Z)
ExtractPhase - Extracting LICENSE
ExtractPhase -   -> 811 rows in 395 ms
...
TransformPhase - Transforming LICENSE
TransformPhase -   -> 811 rows in 60 ms
...
LoadPhase - Pre-creating metrics partitions for 32 day(s) from 2026-04-15 to 2026-05-16
LoadPhase - Loading LICENSE into v5
LoadProgressReporter -   -> LICENSE: 811 rows in 56 ms (14482 rows/s)
...
LoadPhase - Loading VULNERABLESOFTWARE_VULNERABILITIES into v5
LoadProgressReporter -   .. VULNERABLESOFTWARE_VULNERABILITIES: still loading after 5s (expected 2740322 rows)
LoadProgressReporter -   .. VULNERABLESOFTWARE_VULNERABILITIES: still loading after 10s (expected 2740322 rows)
LoadProgressReporter -   .. VULNERABLESOFTWARE_VULNERABILITIES: still loading after 15s (expected 2740322 rows)
...
```

## Verifying the result

We run `verify` again.
This time it reports source, staging, and v5 row counts per table, and surfaces every probe:

```shell linenums="1"
v4-migrator verify \
  --target-url 'jdbc:postgresql://postgres:5432/dtrack' \
  --target-user dtrack \
  --target-pass dtrack
```

Expected output:

```text linenums="1"
== v4-migrator verify ==

[Schema]
  OK    Flyway head = 202605111028

[Row counts]
  Table                          Source      Staging           v5
  LICENSE                           811          811          811
  LICENSEGROUP                        4            4            4
  LICENSEGROUP_LICENSE              131          131          131
...

[Probes]
  No probe entries.

[Constraints]
  13 CHECK constraint(s) hold across 55 loaded table(s)
```

We expect mismatches between source and v5 row counts wherever the migrator
deduplicates, drops, or rewrites rows.
The migration guide's [lossy and non-obvious changes](../guides/administration/migrating-from-v4.md#lossy-and-non-obvious-changes)
section catalogs every case.
We read it now and confirm that the mismatches we see match the cases the guide describes.

## Dropping the staging schema

With verify clean, we drop the staging schema:

```shell linenums="1"
v4-migrator cleanup \
  --target-url 'jdbc:postgresql://postgres:5432/dtrack' \
  --target-user dtrack \
  --target-pass dtrack
```

## Starting the v5 stack

Now we start the apiserver and frontend against the migrated database:

```shell
docker compose -f docker-compose.quickstart.yml up -d apiserver frontend
```

We watch the apiserver come up:

```shell
docker compose -f docker-compose.quickstart.yml logs --follow apiserver
```

Once the log settles, we open the frontend at **<http://localhost:8081>** and log in.

!!! warning "Use your v4 credentials, not the quickstart defaults"

    The migrated database carries our v4 user accounts, so the `admin` / `admin`
    credentials from the [Quick start](quickstart.md) do not apply here.
    We log in with the same credentials we used in v4.
    The same applies to LDAP, OIDC, and API key authentication.
    The migration guide's [lossy and non-obvious changes](../guides/administration/migrating-from-v4.md#lossy-and-non-obvious-changes)
    section lists the username rewrites the migrator applies on collisions,
    for example the `-CONFLICT-LDAP` and `-CONFLICT-OIDC` suffixes.

Our v4 projects, components, and findings are there.
We spot-check a project we know well and confirm that its BOM, dependencies, and vulnerabilities
look right.

## What we just did

We migrated a real v4 dataset into a sandbox v5 instance without touching v4.
The rehearsal proves three things specific to our deployment:

- **Connectivity.** JDBC reaches v4 from a container.
- **Data shape.** The migrator's transformations complete against our v4 row mix.
- **Lossy impact.** We have seen which of our users, teams, projects, or properties
  the migrator deduplicates, renames, or drops.

It does not prove production cutover timing, what happens when we take v4 offline,
or the post-migration credential re-entry that the production guide covers.
We work through those in the [migration guide](../guides/administration/migrating-from-v4.md).

The rehearsal is safe to repeat.
Because v4 was never modified, we can tear the sandbox down and run it again whenever we like.

## Tearing down

After the rehearsal, we remove the sandbox and its volumes:

```shell
docker compose -f docker-compose.quickstart.yml down -v
```

The compose file uses named volumes, so `-v` wipes the sandbox cleanly.

## What's next

- [Migrating from v4 to v5](../guides/administration/migrating-from-v4.md): the production cutover.
- [Lossy and non-obvious changes](../guides/administration/migrating-from-v4.md#lossy-and-non-obvious-changes): required reading before the real run.
- [Running v4 and v5 in parallel](../guides/administration/running-v4-and-v5-in-parallel.md): try v5 against live traffic without committing.
