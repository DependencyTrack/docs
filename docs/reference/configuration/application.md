# Application

Dependency-Track's configuration system is based on [MicroProfile Config],
enabling it to support multiple [sources](#sources).

!!! tip
    The full list of supported config properties can be found in
    the [configuration reference](properties.md).

## Sources

Config properties are loaded, *in order*, from the following sources:

1. JVM system properties
2. Environment variables
3. `${cwd}/.env` file
4. `${cwd}/config/application.properties` file
5. `application.properties` embedded in the application

!!! tip
    `${cwd}` refers to the current working directory.
    When running an official container image, it is `/opt/owasp/dependency-track`.

Once a value is found, later sources will not be checked. For example, when Dependency-Track
attempts to look up the config property `foo.bar`, the environment variable `FOO_BAR=123` is
ignored if the JVM was launched with `-Dfoo.bar=321`.

## Expressions

Configuration values may use expressions, indicated by `${...}`, to reference each other:

```ini linenums="1"
dt.datasource.foo.url=jdbc:postgresql://localhost:5432/dtrack
dt.datasource.bar.url=${dt.datasource.foo.url}
```

This is useful to avoid redundant definition of identical values.

## Loading Values From Files

Configuration values may be loaded from files using the `${file::/path/to/file}` expression. This is
useful when secrets are mounted into the container as files, for example via Docker or Kubernetes
secrets:

```ini linenums="1"
dt.datasource.password=${file::/var/run/secrets/database-password}
dt.ldap.bind.password=${file::/var/run/secrets/ldap-bind-password}
```

The file is read once at startup, decoded as UTF-8, and trailing whitespace is stripped. Files
larger than 64 KiB are rejected.

## Environment Variable Mapping

The canonical representation of properties uses alphanumeric characters,
separated by hyphens (`-`) and periods (`.`). For example:

```ini linenums="1"
foo.BAR-baz=123
```

<!-- vale DependencyTrack.AIBuzzwords = NO -->
Environment variables commonly only support alphanumeric characters and underscores (`_`).
<!-- vale DependencyTrack.AIBuzzwords = YES -->
To bridge this gap, Dependency-Track will use the following matching strategies,
as [defined](https://download.eclipse.org/microprofile/microprofile-config-3.1/microprofile-config-spec-3.1.html#default_configsources.env.mapping)
by [MicroProfile Config]:

> 1. Exact match (that is, `foo.BAR-baz`)
> 2. Replace each character that is neither alphanumeric nor `_` with `_` (that is, `foo_BAR_baz`)
> 3. Replace each character that is neither alphanumeric nor `_` with `_`; then convert the name to upper case (that is, `FOO_BAR_BAZ`)

!!! tip
    The [configuration reference](properties.md) includes the correct
    environment variable names for each listed config property.

## JVM options

The container images launch the API server with the following defaults, set via the `JAVA_OPTIONS`
environment variable:

| Flag                              | Purpose                                                             |
|-----------------------------------|---------------------------------------------------------------------|
| `-XX:+UseG1GC`                    | Garbage collector tuned for predictable pause times.                |
| `-XX:+UseStringDeduplication`     | Reduces heap footprint by deduplicating identical `String` values.  |
| `-XX:+UseCompactObjectHeaders`    | Reduces per-object memory overhead.                                 |
| `-XX:MaxGCPauseMillis=250`        | G1GC target pause time, in milliseconds.                            |
| `-XX:MaxRAMPercentage=80.0`       | Caps the JVM heap at 80% of the container's available memory.       |

The remaining 20% of container memory covers off-heap memory, thread stacks, and the OS.

To extend the defaults without replacing them, set extra flags via the `EXTRA_JAVA_OPTIONS`
environment variable:

```ini
EXTRA_JAVA_OPTIONS="-XX:MaxGCPauseMillis=100"
```

At startup, the container appends `EXTRA_JAVA_OPTIONS` to `JAVA_OPTIONS`; later flags override earlier
values for the same flag.

## Debugging Configuration Resolution

To verify whether config values are properly resolved and from which source, enable debug logging
via [`dt.config.log.values`](properties.md#dtconfiglogvalues) and
[`dt.logging.level."io.smallrye.config"`](properties.md) set to `DEBUG`.

!!! warning
    This will *not* mask or omit any secrets. **Do not use in production environments.**

[MicroProfile Config]: https://microprofile.io/specifications/config/
