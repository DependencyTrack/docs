# Database

Dependency-Track requires a [PostgreSQL], or PostgreSQL-compatible database to operate.

The lowest supported version is 14. You are encouraged to use the [newest available version].

For guidance on choosing a hosting solution, deploying, and tuning PostgreSQL, see the
[database configuration guide](../../guides/administration/configuring-database.md).

## Extensions

The following PostgreSQL [extensions](https://www.postgresql.org/docs/current/external-extensions.html)
are **required** by Dependency-Track. When choosing a hosting solution, verify that the extensions listed
here are supported.

* [`pg_trgm`](https://www.postgresql.org/docs/current/pgtrgm.html): *Support for similarity of text using trigram matching*

!!! note
    Dependency-Track will execute the necessary `CREATE EXTENSION IF NOT EXISTS` statements
    during [schema migration](#schema-migrations). Enabling extensions manually is not necessary.

Generally, usage of extensions is limited to those that:

1. Ship with PostgreSQL [out-of-the-box](https://www.postgresql.org/docs/current/contrib.html)
2. Are [trusted](https://www.postgresql.org/about/featurematrix/detail/347/) by default

## Tuning Parameters

The following PostgreSQL parameters are recommended for Dependency-Track deployments.
For context on when and why to apply these, see the
[advanced tuning guide](../../guides/administration/configuring-database.md#advanced-tuning).

### `autovacuum_vacuum_scale_factor`

<table>
  <tbody style="border: 0">
    <tr>
      <th style="text-align: right">Default</th>
      <td style="border-width: 0"><code>0.2</code></td>
    </tr>
    <tr>
      <th style="text-align: right">Recommendation</th>
      <td style="border-width: 0"><code>0.02</code></td>
    </tr>
    <tr>
      <th style="text-align: right">Tables</th>
      <td style="border-width: 0">
        <ul>
          <li><code>COMPONENT</code></li>
        </ul>
      </td>
    </tr>
    <tr>
      <th style="text-align: right">References</th>
      <td style="border-width: 0"><a href="https://postgresqlco.nf/doc/en/param/autovacuum_vacuum_scale_factor/">Documentation</a></td>
    </tr>
  </tbody>
</table>

### `default_toast_compression`

<table>
  <tbody style="border: 0">
    <tr>
      <th style="text-align: right">Default</th>
      <td style="border-width: 0"><code>pglz</code></td>
    </tr>
    <tr>
      <th style="text-align: right">Recommendation</th>
      <td style="border-width: 0"><code>lz4</code></td>
    </tr>
    <tr>
      <th style="text-align: right">References</th>
      <td style="border-width: 0">
        <ul>
          <li><a href="https://postgresqlco.nf/doc/en/param/default_toast_compression/">Documentation</a></li>
          <li><a href="https://www.postgresql.fastware.com/blog/what-is-the-new-lz4-toast-compression-in-postgresql-14">Comparison by Fujitsu</a></li>
          <li><a href="https://www.tigerdata.com/blog/optimizing-postgresql-performance-compression-pglz-vs-lz4">Comparison by Tiger Data</a></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### `wal_compression`

<table>
  <tbody style="border: 0">
    <tr>
      <th style="text-align: right">Default</th>
      <td style="border-width: 0"><code>off</code></td>
    </tr>
    <tr>
      <th style="text-align: right">Recommendation</th>
      <td style="border-width: 0"><code>lz4</code> or <code>zstd</code></td>
    </tr>
    <tr>
      <th style="text-align: right">References</th>
      <td style="border-width: 0">
        <ul>
          <li><a href="https://postgresqlco.nf/doc/en/param/wal_compression/">Documentation</a></li>
          <li><a href="https://www.enterprisedb.com/blog/you-can-now-pick-your-favorite-compression-algorithm-your-wals">Comparison by EnterpriseDB</a></li>
          <li><a href="https://www.percona.com/blog/wal-compression-in-postgresql-and-recent-improvements-in-version-15/">Explanation by Percona</a></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Schema Migrations

Schema migrations are performed automatically by the API server upon startup using [Liquibase].
Usually no manual action is required when upgrading from an older Dependency-Track version, unless explicitly
stated otherwise in the release notes.

This behaviour can be turned off by setting [`init.tasks.enabled`](properties.md#dtinittasksenabled)
on the API server container to `false`.

For configuring separate migration credentials, see the
[schema migration credentials guide](../../guides/administration/configuring-database.md#schema-migration-credentials).

[Liquibase]: https://www.liquibase.com/
[PostgreSQL]: https://www.postgresql.org/
[newest available version]: https://www.postgresql.org/support/versioning/
