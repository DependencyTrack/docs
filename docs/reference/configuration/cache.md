# Cache

Dependency-Track caches results of expensive operations to reduce load on
external services and speed up repeated lookups. Each cache has a TTL after
which entries expire and the cache provider drops them.

Select the provider via [`dt.cache.provider`](properties.md#dtcacheprovider).

## Providers

### Database

The `database` provider stores cache entries in the `CACHE_ENTRY` table on a
configured data source. This is the only built-in provider.

!!! warning
    The provider does not manage its own schema. The configured data source
    must point at the same schema as the `default` data source, where Dependency-Track's
    schema migrations create the `CACHE_ENTRY` table.

!!! tip
    Pointing the cache at a [secondary data source](datasources.md) that
    targets the same schema can still be useful as a way to isolate cache
    traffic from the main connection pool, so that cache activity doesn't
    compete with the API server for database connections.

A background maintenance worker periodically deletes expired rows and
refreshes the per-cache size counters that feed the cache metrics.

Configuration:

- [`dt.cache.provider.database.datasource.name`](properties.md#dtcacheproviderdatabasedatasourcename)
- [`dt.cache.provider.database.maintenance.initial-delay-ms`](properties.md#dtcacheproviderdatabasemaintenanceinitial-delay-ms)
- [`dt.cache.provider.database.maintenance.interval-ms`](properties.md#dtcacheproviderdatabasemaintenanceinterval-ms)

## Entry TTLs

Each named cache has its own TTL property of the form
`dt.cache."<name>".ttl-ms`.

### Vulnerability analyzer results

Cached results of remote vulnerability analyzer lookups, keyed by component
identifier. Reduces API calls to upstream services across analyses of the same
components.

Configuration:

- [`dt.cache."vuln-analyzer.oss-index.results".ttl-ms`](properties.md#dtcachevuln-analyzeross-indexresultsttl-ms)
- [`dt.cache."vuln-analyzer.snyk.results".ttl-ms`](properties.md#dtcachevuln-analyzersnykresultsttl-ms)

### Package metadata resolver responses

Cached HTTP responses from package registry metadata endpoints, used to detect
outdated components.

!!! tip
    Entries include the response body together with `ETag` and `Last-Modified` validators
    so that refreshes after the freshness window revalidate with a conditional request and
    receive a 304 when the upstream response hasn't changed. The TTL must exceed the 12 h
    freshness window for conditional requests to fire.

Configuration:

- [`dt.cache."package-metadata-resolver.cargo.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvercargoresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.composer.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvercomposerresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.cpan.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvercpanresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.gem.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvergemresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.github.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvergithubresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.gomodules.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvergomodulesresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.hackage.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolverhackageresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.hex.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolverhexresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.maven.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvermavenresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.nixpkgs.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvernixpkgsresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.npm.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvernpmresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.nuget.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolvernugetresponsesttl-ms)
- [`dt.cache."package-metadata-resolver.pypi.responses".ttl-ms`](properties.md#dtcachepackage-metadata-resolverpypiresponsesttl-ms)
