# Data Sources

Data sources are logical objects through which database connections can be acquired.

## Property Format

Data sources are configured using properties in the following format:

```ini
dt.datasource.<name>.<property>=<value>
```

For available properties, and their environment variable equivalents, refer to the [configuration reference].

!!! tip
    When `<name>` is omitted, `default` is assumed, so
    `dt.datasource.url` and `dt.datasource.default.url` are treated equally.

The `default` data source is *required*. It serves the REST API
and the vast majority of background processing.

Certain features accept a *data source name* instead of database connection details,
allowing them to use a dedicated connection pool. For example, the
[*database* secret management provider](../../guides/administration/configuring-secret-management.md#database)
via [`dt.secret-management.database.datasource.name`](properties.md#dtsecret-managementdatabasedatasourcename).

??? example "Multiple data sources"

    ```ini linenums="1"
    # Configure the default data source
    dt.datasource.url=jdbc:postgresql://localhost:5432/dtrack
    dt.datasource.username=dtrack
    dt.datasource.password=dtrack
    dt.datasource.pool.enabled=true
    dt.datasource.pool.max-size=20

    # Configure the secret management data source
    dt.datasource.secretmgt.url=jdbc:postgresql://localhost:5432/dtrack
    dt.datasource.secretmgt.username=secrets
    dt.datasource.secretmgt.password=secrets
    dt.datasource.secretmgt.pool.enabled=true
    dt.datasource.secretmgt.pool.max-size=5

    # Configure secret management to use separate data source
    dt.secret-management.provider=database
    dt.secret-management.database.datasource.name=secretmgt
    ```

!!! note
    Data sources are instantiated on first use. You can configure as many
    data sources as you like, but unless they're being used by a feature,
    they will not be created.

## Connection Pool Properties

The following properties control local connection pooling per data source:

* [`dt.datasource.<name>.pool.enabled`](properties.md#dtdatasourcepoolenabled)
* [`dt.datasource.<name>.url`](properties.md#dtdatasourceurl)
* [`dt.datasource.<name>.username`](properties.md#dtdatasourceusername)
* [`dt.datasource.<name>.password`](properties.md#dtdatasourcepassword)
* [`dt.datasource.<name>.password-file`](properties.md#dtdatasourcepassword-file)
* [`dt.datasource.<name>.pool.max-size`](properties.md#dtdatasourcepoolmax-size)
* [`dt.datasource.<name>.pool.min-idle`](properties.md#dtdatasourcepoolmin-idle)
* [`dt.datasource.<name>.pool.max-lifetime-ms`](properties.md#dtdatasourcepoolmax-lifetime-ms)
* [`dt.datasource.<name>.pool.idle-timeout-ms`](properties.md#dtdatasourcepoolidle-timeout-ms)

When deploying multiple instances, the total number of connections across all pools
must not exceed the PostgreSQL [`max_connections`](https://postgresqlco.nf/doc/en/param/max_connections/) limit
(default: 100).

For centralised connection pooling with PgBouncer, see the
[database configuration guide](../../guides/administration/configuring-database.md#centralised-connection-pooling).

[configuration reference]: database.md
