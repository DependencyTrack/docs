# Configuring the time zone

!!! note
    Running the API server with a non-UTC time zone requires Dependency-Track **5.0.1 or newer**.
    Version 5.0.0 implicitly assumes UTC and misbehaves under any other zone.

Dependency-Track does all internal date and time work in UTC, and the official container images set `TZ=Etc/UTC` to
match. `TZ` is the standard POSIX environment variable for the system time zone. Setting it to a non-UTC value only
changes how log timestamps render in the API server's `stdout` and `stderr`. Stored data, dashboards, policies, and REST
responses stay UTC.

!!! tip
    Run the API server in UTC where you can. Log lines, partition names, and dashboard buckets correlate more easily
    when they share a single zone.

## Setting `TZ`

Set `TZ` as an environment variable on the API server container:

```yaml linenums="1" title="docker-compose.yaml"
services:
  apiserver:
    image: dependencytrack/apiserver
    environment:
      TZ: "Europe/Paris"
```

Use any [IANA time zone identifier][iana-tz]. The container image ships with `tzdata`, so all identifiers resolve.

## Database session time zone

The API server's PostgreSQL sessions inherit `TZ`. This does not affect stored data. Writes go in as absolute instants,
and partition maintenance and materialised view refreshes pin the session to UTC for their transactions.

!!! warning
    When connecting to the database directly, match your session zone to the API server's `TZ`. PostgreSQL renders
    `timestamptz` in the session zone, interprets unqualified date and timestamp literals in it, and casts comparisons
    through it. A mismatch makes the same row appear to shift by hours when reading, and silently inserts the wrong
    instant when writing. Issue `SET TimeZone TO '<zone>'` before running ad-hoc updates.

[iana-tz]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
