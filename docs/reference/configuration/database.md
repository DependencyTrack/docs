# Database

Dependency-Track requires a [PostgreSQL], or PostgreSQL-compatible database to operate.

The lowest supported version is 14. Prefer the [newest available version].

For guidance on choosing a hosting solution, deploying, and tuning PostgreSQL, see the
[database configuration guide](../../guides/administration/configuring-database.md).

## Extensions

Dependency-Track **requires** the following PostgreSQL
[extensions](https://www.postgresql.org/docs/current/external-extensions.html).
When choosing a hosting solution, verify it supports them.

* [`pg_trgm`](https://www.postgresql.org/docs/current/pgtrgm.html): *Support for similarity of text using trigram matching*

!!! note
    Dependency-Track executes the necessary `CREATE EXTENSION IF NOT EXISTS` statements
    during [schema migration](#schema-migrations). You do not need to enable extensions manually.

Dependency-Track limits extension usage to those that:

1. Ship with PostgreSQL [out-of-the-box](https://www.postgresql.org/docs/current/contrib.html)
2. Are [trusted](https://www.postgresql.org/about/featurematrix/detail/347/) by default

## Tuning parameters

Dependency-Track recommends the following PostgreSQL parameters for production
deployments. For context on when and why to apply these, see the
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

## Schema migrations

By default, schema migrations run on startup as an [init task](init-tasks.md), using [Flyway].
Upgrading from an older Dependency-Track version requires no manual action,
unless the [upgrade guides](../../guides/upgrading/index.md) explicitly state
otherwise.

[Flyway]: https://www.red-gate.com/products/flyway/
[PostgreSQL]: https://www.postgresql.org/
[newest available version]: https://www.postgresql.org/support/versioning/
