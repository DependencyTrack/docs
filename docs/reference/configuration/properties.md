<!--
  GENERATED. DO NOT EDIT.

  Generated with: --template scripts/templates/config-docs.md.j2 --output docs/reference/configuration/properties.md dependency-track/apiserver/src/main/resources/application.properties
-->

# Configuration Properties

## Glossary

### Required Properties

Properties marked with <strong style="color: red">*</strong> are required. A required property must never be unset.

### Property Types

Configuration properties may use the following types:

| Type | Description |
|:-----|:------------|
| `boolean` | `true` or `false` |
| `cron` | A [cron expression](https://en.wikipedia.org/wiki/Cron#Cron_expression) (e.g. `0 0 * * *`) |
| `double` | A decimal number (e.g. `3.14`) |
| `duration` | An [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) (e.g. `PT30S`, `PT5M`, `PT1H`) |
| `enum` | One of a fixed set of values, refer to *Valid Values* |
| `integer` | A whole number (e.g. `42`) |
| `string` | A text value |


## CORS

<span id="dtcorsallow-credentials">**`dt.cors.allow-credentials`** [¶](#dtcorsallow-credentials){ .headerlink }</span>

Controls the content of the `Access-Control-Allow-Credentials` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_ALLOW_CREDENTIALS</code></td></tr>
</table>

<span id="dtcorsallowed-headers">**`dt.cors.allowed-headers`** [¶](#dtcorsallowed-headers){ .headerlink }</span>

Controls the content of the `Access-Control-Allow-Headers` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>Origin,Content-Type,Authorization,X-Requested-With,Content-Length,Accept,Origin,X-Api-Key,X-Total-Count,*</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_ALLOWED_HEADERS</code></td></tr>
</table>

<span id="dtcorsallowed-methods">**`dt.cors.allowed-methods`** [¶](#dtcorsallowed-methods){ .headerlink }</span>

Controls the content of the `Access-Control-Allow-Methods` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>GET,POST,PUT,PATCH,DELETE,OPTIONS</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_ALLOWED_METHODS</code></td></tr>
</table>

<span id="dtcorsallowed-origins">**`dt.cors.allowed-origins`** [¶](#dtcorsallowed-origins){ .headerlink }</span>

Controls the content of the `Access-Control-Allow-Origin` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>*</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_ALLOWED_ORIGINS</code></td></tr>
</table>

<span id="dtcorsenabled">**`dt.cors.enabled`** [¶](#dtcorsenabled){ .headerlink }</span>

Defines whether [Cross Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)  (CORS) headers shall be included in REST API responses.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_ENABLED</code></td></tr>
</table>

<span id="dtcorsexposed-headers">**`dt.cors.exposed-headers`** [¶](#dtcorsexposed-headers){ .headerlink }</span>

Controls the content of the `Access-Control-Expose-Headers` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>Origin,Content-Type,Authorization,X-Requested-With,Content-Length,Accept,Origin,X-Api-Key,X-Total-Count</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_EXPOSED_HEADERS</code></td></tr>
</table>

<span id="dtcorsmax-age">**`dt.cors.max-age`** [¶](#dtcorsmax-age){ .headerlink }</span>

Controls the content of the `Access-Control-Max-Age` response header.  <br/>  Has no effect when [`dt.cors.enabled`](#dtcorsenabled) is `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>3600</code></td></tr>
<tr><th>ENV</th><td><code>DT_CORS_MAX_AGE</code></td></tr>
</table>



## Cache

<span id="dtcachepackage-metadata-resolvercargoresponsesttl-ms">**`dt.cache."package-metadata-resolver.cargo.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvercargoresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Cargo package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_CARGO_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvercomposerresponsesttl-ms">**`dt.cache."package-metadata-resolver.composer.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvercomposerresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Composer package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_COMPOSER_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvercpanresponsesttl-ms">**`dt.cache."package-metadata-resolver.cpan.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvercpanresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the CPAN package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_CPAN_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvergemresponsesttl-ms">**`dt.cache."package-metadata-resolver.gem.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvergemresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the RubyGems package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_GEM_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvergithubresponsesttl-ms">**`dt.cache."package-metadata-resolver.github.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvergithubresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the GitHub package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_GITHUB_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvergomodulesresponsesttl-ms">**`dt.cache."package-metadata-resolver.gomodules.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvergomodulesresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Go modules package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_GOMODULES_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolverhackageresponsesttl-ms">**`dt.cache."package-metadata-resolver.hackage.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolverhackageresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Hackage package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_HACKAGE_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolverhexresponsesttl-ms">**`dt.cache."package-metadata-resolver.hex.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolverhexresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Hex package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_HEX_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvermavenresponsesttl-ms">**`dt.cache."package-metadata-resolver.maven.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvermavenresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the Maven package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_MAVEN_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvernixpkgsresponsesttl-ms">**`dt.cache."package-metadata-resolver.nixpkgs.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvernixpkgsresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for Nixpkgs package metadata resolver response cache entries.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>14400000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_NIXPKGS_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvernpmresponsesttl-ms">**`dt.cache."package-metadata-resolver.npm.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvernpmresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the npm package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_NPM_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolvernugetresponsesttl-ms">**`dt.cache."package-metadata-resolver.nuget.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolvernugetresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the NuGet package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_NUGET_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachepackage-metadata-resolverpypiresponsesttl-ms">**`dt.cache."package-metadata-resolver.pypi.responses".ttl-ms`** [¶](#dtcachepackage-metadata-resolverpypiresponsesttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for the PyPI package metadata resolver's HTTP response cache.  Entries hold response bodies along with their ETag and Last-Modified validators  so that refreshes after the freshness window can revalidate via 304.  Must exceed the freshness window (12h) for conditional requests to fire.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>604800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__PACKAGE_METADATA_RESOLVER_PYPI_RESPONSES__TTL_MS</code></td></tr>
</table>

<span id="dtcachevuln-analyzeross-indexresultsttl-ms">**`dt.cache."vuln-analyzer.oss-index.results".ttl-ms`** [¶](#dtcachevuln-analyzeross-indexresultsttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for OSS Index result cache entries.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>86400000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__VULN_ANALYZER_OSS_INDEX_RESULTS__TTL_MS</code></td></tr>
</table>

<span id="dtcachevuln-analyzersnykresultsttl-ms">**`dt.cache."vuln-analyzer.snyk.results".ttl-ms`** [¶](#dtcachevuln-analyzersnykresultsttl-ms){ .headerlink }</span>

Defines the TTL in milliseconds for Snyk result cache entries.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>43200000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE__VULN_ANALYZER_SNYK_RESULTS__TTL_MS</code></td></tr>
</table>

<span id="dtcacheprovider">**`dt.cache.provider`** <strong style="color: red">*</strong> [¶](#dtcacheprovider){ .headerlink }</span>

Defines the cache provider to use.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>enum</code></td></tr>
<tr><th>Default</th><td><code>database</code></td></tr>
<tr><th>Valid Values</th><td><code>[database]</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE_PROVIDER</code></td></tr>
</table>

<span id="dtcacheproviderdatabasedatasourcename">**`dt.cache.provider.database.datasource.name`** [¶](#dtcacheproviderdatabasedatasourcename){ .headerlink }</span>

Defines the name of the data source to be used by the database cache provider.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>default</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE_PROVIDER_DATABASE_DATASOURCE_NAME</code></td></tr>
</table>

<span id="dtcacheproviderdatabasemaintenanceinitial-delay-ms">**`dt.cache.provider.database.maintenance.initial-delay-ms`** [¶](#dtcacheproviderdatabasemaintenanceinitial-delay-ms){ .headerlink }</span>

Defines the initial delay in milliseconds after which the  database cache provider first performs its maintenance activities,  e.g. entry expiration.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>60000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE_PROVIDER_DATABASE_MAINTENANCE_INITIAL_DELAY_MS</code></td></tr>
</table>

<span id="dtcacheproviderdatabasemaintenanceinterval-ms">**`dt.cache.provider.database.maintenance.interval-ms`** [¶](#dtcacheproviderdatabasemaintenanceinterval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the database  cache provider performs its maintenance activities,  e.g. entry expiration.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>300000</code></td></tr>
<tr><th>ENV</th><td><code>DT_CACHE_PROVIDER_DATABASE_MAINTENANCE_INTERVAL_MS</code></td></tr>
</table>



## Database

<span id="dtdatasourcepassword">**`dt.datasource.password`** [¶](#dtdatasourcepassword){ .headerlink }</span>

Defines the password to use for the default data source.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>dtrack</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_PASSWORD</code></td></tr>
</table>

<span id="dtdatasourcepoolenabled">**`dt.datasource.pool.enabled`** <strong style="color: red">*</strong> [¶](#dtdatasourcepoolenabled){ .headerlink }</span>

Defines whether connection pooling is enabled for the default data source.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_POOL_ENABLED</code></td></tr>
</table>

<span id="dtdatasourcepoolidle-timeout-ms">**`dt.datasource.pool.idle-timeout-ms`** [¶](#dtdatasourcepoolidle-timeout-ms){ .headerlink }</span>

Defines the maximum time in milliseconds that a connection is allowed to sit idle in the pool.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>300000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_POOL_IDLE_TIMEOUT_MS</code></td></tr>
</table>

<span id="dtdatasourcepoolmax-lifetime-ms">**`dt.datasource.pool.max-lifetime-ms`** [¶](#dtdatasourcepoolmax-lifetime-ms){ .headerlink }</span>

Defines the maximum time in milliseconds for which connections should be kept in the pool for the default data source.  Required when [`dt.datasource.pool.enabled`](#dtdatasourcepoolenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>600000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_POOL_MAX_LIFETIME_MS</code></td></tr>
</table>

<span id="dtdatasourcepoolmax-size">**`dt.datasource.pool.max-size`** [¶](#dtdatasourcepoolmax-size){ .headerlink }</span>

Defines the maximum size of the connection pool for the default data source.  Required when [`dt.datasource.pool.enabled`](#dtdatasourcepoolenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>30</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_POOL_MAX_SIZE</code></td></tr>
</table>

<span id="dtdatasourcepoolmin-idle">**`dt.datasource.pool.min-idle`** [¶](#dtdatasourcepoolmin-idle){ .headerlink }</span>

Defines the minimum number of idle connections in the pool for the default data source.  Required when [`dt.datasource.pool.enabled`](#dtdatasourcepoolenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>15</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_POOL_MIN_IDLE</code></td></tr>
</table>

<span id="dtdatasourceurl">**`dt.datasource.url`** <strong style="color: red">*</strong> [¶](#dtdatasourceurl){ .headerlink }</span>

Defines the JDBC URL to use for the default data source.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>jdbc:postgresql://localhost:5432/dtrack?reWriteBatchedInserts=true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_URL</code></td></tr>
</table>

<span id="dtdatasourceusername">**`dt.datasource.username`** [¶](#dtdatasourceusername){ .headerlink }</span>

Defines the username to use for the default data source.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>dtrack</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATASOURCE_USERNAME</code></td></tr>
</table>

<span id="dtdex-enginedatasourcename">**`dt.dex-engine.datasource.name`** [¶](#dtdex-enginedatasourcename){ .headerlink }</span>

Defines the name of the data source to be used by the durable execution engine.  For larger deployments, it is recommended to use a separate,  non-default data source.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>default</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_DATASOURCE_NAME</code></td></tr>
</table>

<span id="dtdex-enginemigrationdatasourcename">**`dt.dex-engine.migration.datasource.name`** [¶](#dtdex-enginemigrationdatasourcename){ .headerlink }</span>

Defines the name of the data source to use for executing database  migrations of the durable execution engine.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_MIGRATION_DATASOURCE_NAME</code></td></tr>
</table>

<span id="dtinit-tasksdatasourceclose-after-completion">**`dt.init-tasks.datasource.close-after-completion`** <strong style="color: red">*</strong> [¶](#dtinit-tasksdatasourceclose-after-completion){ .headerlink }</span>

Defines whether the data source used by init tasks should be closed  after all tasks completed. This is useful when a non-default data source  was configured, that is not used anywhere else.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASKS_DATASOURCE_CLOSE_AFTER_COMPLETION</code></td></tr>
</table>

<span id="dtinit-tasksdatasourcename">**`dt.init-tasks.datasource.name`** <strong style="color: red">*</strong> [¶](#dtinit-tasksdatasourcename){ .headerlink }</span>

Defines the name of the data source to be used by init tasks.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>default</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASKS_DATASOURCE_NAME</code></td></tr>
</table>



## Development

<span id="dtdev-servicescontainer-reuseenabled">**`dt.dev-services.container-reuse.enabled`** [¶](#dtdev-servicescontainer-reuseenabled){ .headerlink }</span>

Whether dev services containers shall be reused across restarts.  <br/><br/>  When enabled, containers are kept running when Dependency-Track stops, and  re-attached to on the next start. This preserves PostgreSQL state (schema and data)  across restarts and avoids the cost of re-provisioning on every run.  <br/><br/>  This additionally requires Testcontainers reuse to be opted into on the  developer's machine, either via testcontainers.reuse.enable=true in the  `~/.testcontainers.properties` file, or the `TESTCONTAINERS_REUSE_ENABLE=true`  environment variable. Without it, this option has no effect and containers  are disposed on shutdown as usual.  See <https://java.testcontainers.org/features/reuse/#how-to-use-it>.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEV_SERVICES_CONTAINER_REUSE_ENABLED</code></td></tr>
</table>

<span id="dtdev-servicesenabled">**`dt.dev-services.enabled`** [¶](#dtdev-servicesenabled){ .headerlink }</span>

Whether dev services shall be enabled.  <br/><br/>  When enabled, Dependency-Track will automatically launch containers for:  <ul>  <li>Frontend</li>  <li>PostgreSQL</li>  </ul>  at startup, and configures itself to use them. They are disposed when  Dependency-Track stops.  <br/><br/>  The port on which the frontend will be exposed is configurable via  [`dt.dev-services.frontend-port`](#dtdev-servicesfrontend-port). The port of the postgres container  is automatically inferred from dt.datasource.default.url.  <br/><br/>  Trying to enable dev services in a production build will prevent  the application from starting.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEV_SERVICES_ENABLED</code></td></tr>
</table>

<span id="dtdev-servicesfrontend-image">**`dt.dev-services.frontend-image`** [¶](#dtdev-servicesfrontend-image){ .headerlink }</span>

The image to use for the frontend dev services container.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>ghcr.io/dependencytrack/frontend:5-snapshot</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEV_SERVICES_FRONTEND_IMAGE</code></td></tr>
</table>

<span id="dtdev-servicesfrontend-port">**`dt.dev-services.frontend-port`** [¶](#dtdev-servicesfrontend-port){ .headerlink }</span>

The port on which the frontend dev services container shall be exposed on the host.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>8081</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEV_SERVICES_FRONTEND_PORT</code></td></tr>
</table>

<span id="dtdev-servicespostgres-image">**`dt.dev-services.postgres-image`** [¶](#dtdev-servicespostgres-image){ .headerlink }</span>

The image to use for the PostgreSQL dev services container.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>postgres:14-alpine</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEV_SERVICES_POSTGRES_IMAGE</code></td></tr>
</table>



## Durable Execution

<span id="dtdex-engineactivity-task-heartbeat-bufferflush-interval-ms">**`dt.dex-engine.activity-task-heartbeat-buffer.flush-interval-ms`** [¶](#dtdex-engineactivity-task-heartbeat-bufferflush-interval-ms){ .headerlink }</span>

Defines the time in milliseconds between flushes of the activity task heartbeat buffer.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_TASK_HEARTBEAT_BUFFER_FLUSH_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-engineactivity-task-heartbeat-buffermax-batch-size">**`dt.dex-engine.activity-task-heartbeat-buffer.max-batch-size`** [¶](#dtdex-engineactivity-task-heartbeat-buffermax-batch-size){ .headerlink }</span>

Defines the maximum number of items of the activity task heartbeat buffer.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_TASK_HEARTBEAT_BUFFER_MAX_BATCH_SIZE</code></td></tr>
</table>

<span id="dtdex-engineactivity-task-schedulerpoll-interval-ms">**`dt.dex-engine.activity-task-scheduler.poll-interval-ms`** [¶](#dtdex-engineactivity-task-schedulerpoll-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the activity task scheduler polls  for tasks to enqueue for execution.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_TASK_SCHEDULER_POLL_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerartifact-importenabled">**`dt.dex-engine.activity-worker.artifact-import.enabled`** [¶](#dtdex-engineactivity-workerartifact-importenabled){ .headerlink }</span>

Defines whether the artifact import activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_ARTIFACT_IMPORT_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerartifact-importmax-concurrency">**`dt.dex-engine.activity-worker.artifact-import.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workerartifact-importmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the artifact import activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_ARTIFACT_IMPORT_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerdefaultenabled">**`dt.dex-engine.activity-worker.default.enabled`** [¶](#dtdex-engineactivity-workerdefaultenabled){ .headerlink }</span>

Defines whether the default activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_DEFAULT_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerdefaultmax-concurrency">**`dt.dex-engine.activity-worker.default.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workerdefaultmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the default activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>25</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_DEFAULT_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workermetrics-updateenabled">**`dt.dex-engine.activity-worker.metrics-update.enabled`** [¶](#dtdex-engineactivity-workermetrics-updateenabled){ .headerlink }</span>

Defines whether the metrics update activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_METRICS_UPDATE_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workermetrics-updatemax-concurrency">**`dt.dex-engine.activity-worker.metrics-update.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workermetrics-updatemax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the metrics update activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_METRICS_UPDATE_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationenabled">**`dt.dex-engine.activity-worker.notification.enabled`** [¶](#dtdex-engineactivity-workernotificationenabled){ .headerlink }</span>

Defines whether the notification activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationmax-concurrency">**`dt.dex-engine.activity-worker.notification.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workernotificationmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationpoll-backoffinitial-delay-ms">**`dt.dex-engine.activity-worker.notification.poll-backoff.initial-delay-ms`** [¶](#dtdex-engineactivity-workernotificationpoll-backoffinitial-delay-ms){ .headerlink }</span>

Defines the initial poll backoff delay in milliseconds of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>200</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_POLL_BACKOFF_INITIAL_DELAY_MS</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationpoll-backoffmax-delay-ms">**`dt.dex-engine.activity-worker.notification.poll-backoff.max-delay-ms`** [¶](#dtdex-engineactivity-workernotificationpoll-backoffmax-delay-ms){ .headerlink }</span>

Defines the max poll backoff delay in milliseconds of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>10000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_POLL_BACKOFF_MAX_DELAY_MS</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationpoll-backoffmultiplier">**`dt.dex-engine.activity-worker.notification.poll-backoff.multiplier`** [¶](#dtdex-engineactivity-workernotificationpoll-backoffmultiplier){ .headerlink }</span>

Defines the poll backoff delay multiplier of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>double</code></td></tr>
<tr><th>Default</th><td><code>2.0</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_POLL_BACKOFF_MULTIPLIER</code></td></tr>
</table>

<span id="dtdex-engineactivity-workernotificationpoll-backoffrandomization-factor">**`dt.dex-engine.activity-worker.notification.poll-backoff.randomization-factor`** [¶](#dtdex-engineactivity-workernotificationpoll-backoffrandomization-factor){ .headerlink }</span>

Defines the poll backoff randomization factor of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>double</code></td></tr>
<tr><th>Default</th><td><code>0.2</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_NOTIFICATION_POLL_BACKOFF_RANDOMIZATION_FACTOR</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerpackage-metadata-resolutionenabled">**`dt.dex-engine.activity-worker.package-metadata-resolution.enabled`** [¶](#dtdex-engineactivity-workerpackage-metadata-resolutionenabled){ .headerlink }</span>

Defines whether the package metadata activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_PACKAGE_METADATA_RESOLUTION_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerpackage-metadata-resolutionmax-concurrency">**`dt.dex-engine.activity-worker.package-metadata-resolution.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workerpackage-metadata-resolutionmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the package metadata activity worker.  <br/><br/>  Note that a concurrency of N means that at most N PURLs batches will be resolved  concurrently. Each batch performs HTTP requests against package registries.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>3</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_PACKAGE_METADATA_RESOLUTION_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerpolicy-evaluationenabled">**`dt.dex-engine.activity-worker.policy-evaluation.enabled`** [¶](#dtdex-engineactivity-workerpolicy-evaluationenabled){ .headerlink }</span>

Defines whether the policy evaluation activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_POLICY_EVALUATION_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workerpolicy-evaluationmax-concurrency">**`dt.dex-engine.activity-worker.policy-evaluation.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workerpolicy-evaluationmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the policy evaluation activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_POLICY_EVALUATION_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workervuln-analysis-reconciliationenabled">**`dt.dex-engine.activity-worker.vuln-analysis-reconciliation.enabled`** [¶](#dtdex-engineactivity-workervuln-analysis-reconciliationenabled){ .headerlink }</span>

Defines whether the vulnerability analysis reconciliation activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_VULN_ANALYSIS_RECONCILIATION_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workervuln-analysis-reconciliationmax-concurrency">**`dt.dex-engine.activity-worker.vuln-analysis-reconciliation.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workervuln-analysis-reconciliationmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the vulnerability analysis reconciliation activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_VULN_ANALYSIS_RECONCILIATION_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineactivity-workervuln-analysisenabled">**`dt.dex-engine.activity-worker.vuln-analysis.enabled`** [¶](#dtdex-engineactivity-workervuln-analysisenabled){ .headerlink }</span>

Defines whether the notification activity worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_VULN_ANALYSIS_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineactivity-workervuln-analysismax-concurrency">**`dt.dex-engine.activity-worker.vuln-analysis.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineactivity-workervuln-analysismax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the notification activity worker.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>10</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_ACTIVITY_WORKER_VULN_ANALYSIS_MAX_CONCURRENCY</code></td></tr>
</table>

<span id="dtdex-engineexternal-event-bufferflush-interval-ms">**`dt.dex-engine.external-event-buffer.flush-interval-ms`** [¶](#dtdex-engineexternal-event-bufferflush-interval-ms){ .headerlink }</span>

Defines the time in milliseconds between flushes of the external event buffer.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_EXTERNAL_EVENT_BUFFER_FLUSH_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-engineexternal-event-buffermax-batch-size">**`dt.dex-engine.external-event-buffer.max-batch-size`** [¶](#dtdex-engineexternal-event-buffermax-batch-size){ .headerlink }</span>

Defines the maximum number of items of the external event buffer.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_EXTERNAL_EVENT_BUFFER_MAX_BATCH_SIZE</code></td></tr>
</table>

<span id="dtdex-engineleader-electionenabled">**`dt.dex-engine.leader-election.enabled`** [¶](#dtdex-engineleader-electionenabled){ .headerlink }</span>

Whether leader election in the durable execution engine should be enabled.  <br/><br/>  Disabling leader election also disables the workflow task scheduler,  activity task scheduler, and maintenance worker, as only the leader  node is meant to handle those responsibilities.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_LEADER_ELECTION_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineleader-electionlease-check-interval-ms">**`dt.dex-engine.leader-election.lease-check-interval-ms`** [¶](#dtdex-engineleader-electionlease-check-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which leadership lease acquisition or extension is attempted.  <br/><br/>  Must be smaller than [`dt.dex-engine.leader-election.lease-duration-ms`](#dtdex-engineleader-electionlease-duration-ms) to avoid  frequent leadership changes.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>15000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_LEADER_ELECTION_LEASE_CHECK_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-engineleader-electionlease-duration-ms">**`dt.dex-engine.leader-election.lease-duration-ms`** [¶](#dtdex-engineleader-electionlease-duration-ms){ .headerlink }</span>

Defines the duration in milliseconds for which leadership leases are acquired.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>30000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_LEADER_ELECTION_LEASE_DURATION_MS</code></td></tr>
</table>

<span id="dtdex-enginemaintenancerun-deletion-batch-size">**`dt.dex-engine.maintenance.run-deletion-batch-size`** [¶](#dtdex-enginemaintenancerun-deletion-batch-size){ .headerlink }</span>

Defines the maximum number of completed workflow runs to delete during a single execution  of the maintenance worker. Deletion of large volumes of runs in one pass can lead to I/O  spikes and increased table bloat.  <br/><br/>  If retention is not able to keep up with the volumes of  runs, consider increasing the interval of the maintenance worker first.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>1000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_MAINTENANCE_RUN_DELETION_BATCH_SIZE</code></td></tr>
</table>

<span id="dtdex-enginemaintenancerun-retention-ms">**`dt.dex-engine.maintenance.run-retention-ms`** [¶](#dtdex-enginemaintenancerun-retention-ms){ .headerlink }</span>

Defines the duration in milliseconds after which completed workflow runs become  eligible for deletion.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>86400000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_MAINTENANCE_RUN_RETENTION_MS</code></td></tr>
</table>

<span id="dtdex-enginemaintenanceworker-initial-delay-ms">**`dt.dex-engine.maintenance.worker-initial-delay-ms`** [¶](#dtdex-enginemaintenanceworker-initial-delay-ms){ .headerlink }</span>

Defines the initial delay in milliseconds after which the maintenance worker will execute for the first time.  <br/><br/>  Note that only the leader node in the cluster will actually perform maintenance work.  For nodes that are not leaders, maintenance is a no-op.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>60000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_MAINTENANCE_WORKER_INITIAL_DELAY_MS</code></td></tr>
</table>

<span id="dtdex-enginemaintenanceworker-interval-ms">**`dt.dex-engine.maintenance.worker-interval-ms`** [¶](#dtdex-enginemaintenanceworker-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds at which the maintenance worker will execute.  <br/><br/>  Note that only the leader node in the cluster will actually perform maintenance work.  For nodes that are not leaders, maintenance is a no-op.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>1800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_MAINTENANCE_WORKER_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-enginemetrics-collectorenabled">**`dt.dex-engine.metrics-collector.enabled`** [¶](#dtdex-enginemetrics-collectorenabled){ .headerlink }</span>

Defines whether the metrics collector should be enabled.  <br/><br/>  The collector is responsible for collecting metrics from  the database, such as the distribution of workflow run statuses,  task queue capacities and depths, and more.  <br/><br/>  It is recommended to keep it enabled for monitoring purposes,  but may be disabled in case it generates undesired load.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_METRICS_COLLECTOR_ENABLED</code></td></tr>
</table>

<span id="dtdex-enginemetrics-collectorinitial-delay-ms">**`dt.dex-engine.metrics-collector.initial-delay-ms`** [¶](#dtdex-enginemetrics-collectorinitial-delay-ms){ .headerlink }</span>

Defines the initial delay in milliseconds after which the metrics collector will first run.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>15000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_METRICS_COLLECTOR_INITIAL_DELAY_MS</code></td></tr>
</table>

<span id="dtdex-enginemetrics-collectorinterval-ms">**`dt.dex-engine.metrics-collector.interval-ms`** [¶](#dtdex-enginemetrics-collectorinterval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the metrics collector runs.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>30000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_METRICS_COLLECTOR_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-enginerun-history-cacheevict-after-access-ms">**`dt.dex-engine.run-history-cache.evict-after-access-ms`** [¶](#dtdex-enginerun-history-cacheevict-after-access-ms){ .headerlink }</span>

Defines the time in milliseconds for which workflow run event histories are cached.  <br/><br/>  Histories are only cached for non-terminal runs, to improve performance of replay.  Cached histories are automatically evicted when the corresponding run terminates.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>300000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_RUN_HISTORY_CACHE_EVICT_AFTER_ACCESS_MS</code></td></tr>
</table>

<span id="dtdex-enginerun-history-cachemax-size">**`dt.dex-engine.run-history-cache.max-size`** [¶](#dtdex-enginerun-history-cachemax-size){ .headerlink }</span>

Defines the maximum number of workflow runs for which histories may be cached.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>1000</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_RUN_HISTORY_CACHE_MAX_SIZE</code></td></tr>
</table>

<span id="dtdex-enginetask-event-bufferflush-interval-ms">**`dt.dex-engine.task-event-buffer.flush-interval-ms`** [¶](#dtdex-enginetask-event-bufferflush-interval-ms){ .headerlink }</span>

Defines the time in milliseconds between flushes of the task event buffer.  <br/><br/>  Increasing this interval may yield better throughput while reducing the  database load, but also increases end-to-end latency of workflow and  activity executions.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_TASK_EVENT_BUFFER_FLUSH_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-enginetask-event-buffermax-batch-size">**`dt.dex-engine.task-event-buffer.max-batch-size`** [¶](#dtdex-enginetask-event-buffermax-batch-size){ .headerlink }</span>

Defines the maximum number of items that will be flushed at once.  <br/><br/>  Increasing this value may yield better throughput,  at the expense of higher latency and potentially larger  blast radius in case a task event causes failures during the flush.  <br/><br/>  Since flushes are atomic, a single event failing to be flushed impacts  the entire batch.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_TASK_EVENT_BUFFER_MAX_BATCH_SIZE</code></td></tr>
</table>

<span id="dtdex-engineworkersenabled">**`dt.dex-engine.workers.enabled`** [¶](#dtdex-engineworkersenabled){ .headerlink }</span>

Whether all durable execution task workers should be enabled.  <br/><br/>  Acts as a global kill switch that takes precedence over individual worker settings.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_WORKERS_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineworkflow-task-schedulerpoll-interval-ms">**`dt.dex-engine.workflow-task-scheduler.poll-interval-ms`** [¶](#dtdex-engineworkflow-task-schedulerpoll-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the workflow task scheduler polls  for tasks to enqueue for execution.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_WORKFLOW_TASK_SCHEDULER_POLL_INTERVAL_MS</code></td></tr>
</table>

<span id="dtdex-engineworkflow-workerdefaultenabled">**`dt.dex-engine.workflow-worker.default.enabled`** [¶](#dtdex-engineworkflow-workerdefaultenabled){ .headerlink }</span>

Defines whether the default workflow worker should be enabled.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_WORKFLOW_WORKER_DEFAULT_ENABLED</code></td></tr>
</table>

<span id="dtdex-engineworkflow-workerdefaultmax-concurrency">**`dt.dex-engine.workflow-worker.default.max-concurrency`** <strong style="color: red">*</strong> [¶](#dtdex-engineworkflow-workerdefaultmax-concurrency){ .headerlink }</span>

Defines the maximum concurrency of the default workflow worker.  <br/><br/>  Note that workflow workers do not perform any I/O (although they  may block while waiting for semaphores and buffer flushes),  and are executed with virtual threads. This means that it's  usually perfectly fine to have a high degree of concurrency,  without risking excessive resource usage or I/O thrashing.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_DEX_ENGINE_WORKFLOW_WORKER_DEFAULT_MAX_CONCURRENCY</code></td></tr>
</table>



## General

<span id="dtapi-keyprefix">**`dt.api-key.prefix`** [¶](#dtapi-keyprefix){ .headerlink }</span>

Defines the prefix to be used for API keys. A maximum prefix length of 251  characters is supported. The prefix may also be left empty.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>odt_</code></td></tr>
<tr><th>ENV</th><td><code>DT_API_KEY_PREFIX</code></td></tr>
</table>

<span id="dtauthsession-timeout-ms">**`dt.auth.session-timeout-ms`** [¶](#dtauthsession-timeout-ms){ .headerlink }</span>

Defines the user session timeout in milliseconds.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>28800000</code></td></tr>
<tr><th>ENV</th><td><code>DT_AUTH_SESSION_TIMEOUT_MS</code></td></tr>
</table>

<span id="dtbcryptrounds">**`dt.bcrypt.rounds`** <strong style="color: red">*</strong> [¶](#dtbcryptrounds){ .headerlink }</span>

Specifies the number of bcrypt rounds to use when hashing a user's password.  The higher the number the more secure the password, at the expense of  hardware resources and additional time to generate the hash.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>14</code></td></tr>
<tr><th>ENV</th><td><code>DT_BCRYPT_ROUNDS</code></td></tr>
</table>

<span id="dtconfiglog-values">**`dt.config.log-values`** [¶](#dtconfiglog-values){ .headerlink }</span>

Defines whether config value lookups should be logged.  <br/><br/>  Logging happens at DEBUG level. To make the logs visible, you must configure  `dt.logging.level."io.smallrye.config"=DEBUG`.  <br/><br/>  Note that this will not mask or omit any secrets.  **Do not use in production environments!**  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_CONFIG_LOG_VALUES</code></td></tr>
</table>

<span id="dtconfigprofile">**`dt.config.profile`** [¶](#dtconfigprofile){ .headerlink }</span>

Defines the configuration profile to apply.  <br/><br/>  For example, the `web` profile may be used to disable any background processing,  effectively turning the node into a web-only instance.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_CONFIG_PROFILE</code></td></tr>
</table>

<span id="dtdata-directory">**`dt.data-directory`** <strong style="color: red">*</strong> [¶](#dtdata-directory){ .headerlink }</span>

Defines the path to the data directory. This directory will hold logs,  keys, and any database or index files along with application-specific  files or directories.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>${user.home}/.dependency-track</code></td></tr>
<tr><th>ENV</th><td><code>DT_DATA_DIRECTORY</code></td></tr>
</table>

<span id="dtinit-taskdatabase-migrationenabled">**`dt.init-task.database-migration.enabled`** [¶](#dtinit-taskdatabase-migrationenabled){ .headerlink }</span>

Whether to enable the database migration init task.  Has no effect unless [`dt.init-tasks.enabled`](#dtinit-tasksenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASK_DATABASE_MIGRATION_ENABLED</code></td></tr>
</table>

<span id="dtinit-taskdatabase-partition-maintenanceenabled">**`dt.init-task.database-partition-maintenance.enabled`** [¶](#dtinit-taskdatabase-partition-maintenanceenabled){ .headerlink }</span>

Whether to enable the database partition maintenance init task.  Has no effect unless [`dt.init-tasks.enabled`](#dtinit-tasksenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASK_DATABASE_PARTITION_MAINTENANCE_ENABLED</code></td></tr>
</table>

<span id="dtinit-taskdatabase-seedingenabled">**`dt.init-task.database-seeding.enabled`** [¶](#dtinit-taskdatabase-seedingenabled){ .headerlink }</span>

Whether to enable the database seeding init task.  Seeding involves populating the database with default objects,  such as permissions, users, licenses, etc.  Has no effect unless [`dt.init-tasks.enabled`](#dtinit-tasksenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASK_DATABASE_SEEDING_ENABLED</code></td></tr>
</table>

<span id="dtinit-taskdex-engine-database-migrationenabled">**`dt.init-task.dex-engine-database-migration.enabled`** [¶](#dtinit-taskdex-engine-database-migrationenabled){ .headerlink }</span>

Whether to enable the durable execution engine database migration init task.  Has no effect unless [`dt.init-tasks.enabled`](#dtinit-tasksenabled) is `true`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASK_DEX_ENGINE_DATABASE_MIGRATION_ENABLED</code></td></tr>
</table>

<span id="dtinit-tasksenabled">**`dt.init-tasks.enabled`** [¶](#dtinit-tasksenabled){ .headerlink }</span>

Whether to execute initialization tasks on startup.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASKS_ENABLED</code></td></tr>
</table>

<span id="dtinit-tasksexit-after-completion">**`dt.init-tasks.exit-after-completion`** [¶](#dtinit-tasksexit-after-completion){ .headerlink }</span>

Whether to only execute initialization tasks and exit.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_INIT_TASKS_EXIT_AFTER_COMPLETION</code></td></tr>
</table>

<span id="dttelemetrysubmissiondefault-enabled">**`dt.telemetry.submission.default-enabled`** [¶](#dttelemetrysubmissiondefault-enabled){ .headerlink }</span>

Defines the default value for the telemetry submission enabled setting.  <br/><br/>  This is only used during initial database seeding. Once the setting exists in the  database, it can be toggled via the REST API or the admin UI.  <br/><br/>  To opt out of telemetry before first startup, set this to `false`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_TELEMETRY_SUBMISSION_DEFAULT_ENABLED</code></td></tr>
</table>

<span id="dttmpdelay-bom-processed-notification">**`dt.tmp.delay-bom-processed-notification`** [¶](#dttmpdelay-bom-processed-notification){ .headerlink }</span>

Delays the BOM_PROCESSED notification until the vulnerability analysis associated with a given BOM upload  is completed. The intention being that it is then "safe" to query the API for any identified vulnerabilities.  This is specifically for cases where polling the /api/v1/bom/token/<TOKEN> endpoint is not feasible.  THIS IS A TEMPORARY FUNCTIONALITY AND MAY BE REMOVED IN FUTURE RELEASES WITHOUT FURTHER NOTICE.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_TMP_DELAY_BOM_PROCESSED_NOTIFICATION</code></td></tr>
</table>

<span id="dtvuln-policy-bundleauthbearer-token">**`dt.vuln-policy-bundle.auth.bearer-token`** [¶](#dtvuln-policy-bundleauthbearer-token){ .headerlink }</span>

Defines the bearer token to be used for authentication against the service hosting the vulnerability policy bundle.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_POLICY_BUNDLE_AUTH_BEARER_TOKEN</code></td></tr>
</table>

<span id="dtvuln-policy-bundleauthpassword">**`dt.vuln-policy-bundle.auth.password`** [¶](#dtvuln-policy-bundleauthpassword){ .headerlink }</span>

Defines the password to be used for basic authentication against the service hosting the vulnerability policy bundle.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_POLICY_BUNDLE_AUTH_PASSWORD</code></td></tr>
</table>

<span id="dtvuln-policy-bundleauthusername">**`dt.vuln-policy-bundle.auth.username`** [¶](#dtvuln-policy-bundleauthusername){ .headerlink }</span>

Defines the username to be used for basic authentication against the service hosting the vulnerability policy bundle.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_POLICY_BUNDLE_AUTH_USERNAME</code></td></tr>
</table>

<span id="dtvuln-policy-bundleurl">**`dt.vuln-policy-bundle.url`** [¶](#dtvuln-policy-bundleurl){ .headerlink }</span>

Defines where to fetch the vulnerability policy bundle from.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>https://example.com/bundles/bundle.zip</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_POLICY_BUNDLE_URL</code></td></tr>
</table>



## HTTP

<span id="dthttpconnect-timeout-ms">**`dt.http.connect-timeout-ms`** [¶](#dthttpconnect-timeout-ms){ .headerlink }</span>

Defines the connection timeout in milliseconds for outbound HTTP connections.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>30000</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_CONNECT_TIMEOUT_MS</code></td></tr>
</table>

<span id="dthttpproxyauthpassword">**`dt.http.proxy.auth.password`** [¶](#dthttpproxyauthpassword){ .headerlink }</span>



<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_PROXY_AUTH_PASSWORD</code></td></tr>
</table>

<span id="dthttpproxyauthusername">**`dt.http.proxy.auth.username`** [¶](#dthttpproxyauthusername){ .headerlink }</span>



<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_PROXY_AUTH_USERNAME</code></td></tr>
</table>

<span id="dthttpproxyexclusions">**`dt.http.proxy.exclusions`** [¶](#dthttpproxyexclusions){ .headerlink }</span>



<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>localhost,127.0.0.1</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_PROXY_EXCLUSIONS</code></td></tr>
</table>

<span id="dthttpproxyhost">**`dt.http.proxy.host`** [¶](#dthttpproxyhost){ .headerlink }</span>

HTTP proxy address. If set, then [`dt.http.proxy.port`](#dthttpproxyport) must be set too.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>proxy.example.com</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_PROXY_HOST</code></td></tr>
</table>

<span id="dthttpproxyport">**`dt.http.proxy.port`** [¶](#dthttpproxyport){ .headerlink }</span>



<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>8888</code></td></tr>
<tr><th>ENV</th><td><code>DT_HTTP_PROXY_PORT</code></td></tr>
</table>



## LDAP

<span id="dtldapbase-dn">**`dt.ldap.base-dn`** [¶](#dtldapbase-dn){ .headerlink }</span>

Specifies the base DN that all queries should search from  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>dc=example,dc=com</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_BASE_DN</code></td></tr>
</table>

<span id="dtldapbind-password">**`dt.ldap.bind-password`** [¶](#dtldapbind-password){ .headerlink }</span>

If anonymous access is not permitted, specify a password for the username  used to bind.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_BIND_PASSWORD</code></td></tr>
</table>

<span id="dtldapbind-username">**`dt.ldap.bind-username`** [¶](#dtldapbind-username){ .headerlink }</span>

If anonymous access is not permitted, specify a username with limited access  to the directory, just enough to perform searches. This should be the fully  qualified DN of the user.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_BIND_USERNAME</code></td></tr>
</table>

<span id="dtldapenabled">**`dt.ldap.enabled`** [¶](#dtldapenabled){ .headerlink }</span>

Defines if LDAP will be used for user authentication. If enabled,  `dt.ldap.*` properties should be set accordingly.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_ENABLED</code></td></tr>
</table>

<span id="dtldapgroup-filter">**`dt.ldap.group-filter`** [¶](#dtldapgroup-filter){ .headerlink }</span>

Specifies the LDAP search filter used to retrieve all groups from the directory.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>(&(objectClass=group)(objectCategory=Group))</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>(&(objectClass=groupOfUniqueNames))</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>(&(objectClass=group)(objectCategory=Group))</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_GROUP_FILTER</code></td></tr>
</table>

<span id="dtldapgroup-search-filter">**`dt.ldap.group-search-filter`** [¶](#dtldapgroup-search-filter){ .headerlink }</span>

Specifies the LDAP search filter used to search for groups by their name.  The `{SEARCH_TERM}` variable will be substituted at runtime.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>(&(objectClass=group)(objectCategory=Group)(cn=*{SEARCH_TERM}*))</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>(&(objectClass=group)(objectCategory=Group)(cn=*{SEARCH_TERM}*))</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_GROUP_SEARCH_FILTER</code></td></tr>
</table>

<span id="dtldapmail-attribute">**`dt.ldap.mail-attribute`** [¶](#dtldapmail-attribute){ .headerlink }</span>

Specifies the LDAP attribute used to store a users email address  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>mail</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_MAIL_ATTRIBUTE</code></td></tr>
</table>

<span id="dtldapname-attribute">**`dt.ldap.name-attribute`** [¶](#dtldapname-attribute){ .headerlink }</span>

Specifies the Attribute that identifies a users ID.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>userPrincipalName</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>uid</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>userPrincipalName</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_NAME_ATTRIBUTE</code></td></tr>
</table>

<span id="dtldapsecurity-auth">**`dt.ldap.security-auth`** [¶](#dtldapsecurity-auth){ .headerlink }</span>

Specifies the LDAP security authentication level to use. Its value is one of  the following strings: "none", "simple", "strong". If this property is empty  or unspecified, the behaviour is determined by the service provider.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>enum</code></td></tr>
<tr><th>Default</th><td><code>simple</code></td></tr>
<tr><th>Valid Values</th><td><code>[none, simple, strong]</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_SECURITY_AUTH</code></td></tr>
</table>

<span id="dtldapserver-url">**`dt.ldap.server-url`** [¶](#dtldapserver-url){ .headerlink }</span>

Specifies the LDAP server URL.  <br/><br/>  Examples (Microsoft Active Directory):  <ul>  <li><code>ldap://ldap.example.com:3268</code></li>  <li><code>ldaps://ldap.example.com:3269</code></li>  </ul>  Examples (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul>  <li><code>ldap://ldap.example.com:389</code></li>  <li><code>ldaps://ldap.example.com:636</code></li>  </ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_SERVER_URL</code></td></tr>
</table>

<span id="dtldapteam-synchronization">**`dt.ldap.team-synchronization`** [¶](#dtldapteam-synchronization){ .headerlink }</span>

This option will ensure that team memberships for LDAP users are dynamic and  synchronized with membership of LDAP groups. When a team is mapped to an LDAP  group, all local LDAP users will automatically be assigned to the team if  they are a member of the group the team is mapped to. If the user is later  removed from the LDAP group, they will also be removed from the team. This  option provides the ability to dynamically control user permissions via an  external directory.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_TEAM_SYNCHRONIZATION</code></td></tr>
</table>

<span id="dtldapuser-groups-filter">**`dt.ldap.user-groups-filter`** [¶](#dtldapuser-groups-filter){ .headerlink }</span>

Specifies the LDAP search filter to use to query a user and retrieve a list  of groups the user is a member of. The `{USER_DN}` variable will be substituted  with the actual value of the users DN at runtime.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>(&(objectClass=group)(objectCategory=Group)(member={USER_DN}))</code></li></ul>  Example (Microsoft Active Directory - with nested group support):  <ul><li><code>(member:1.2.840.113556.1.4.1941:={USER_DN})</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>(member:1.2.840.113556.1.4.1941:={USER_DN})</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_USER_GROUPS_FILTER</code></td></tr>
</table>

<span id="dtldapuser-provisioning">**`dt.ldap.user-provisioning`** [¶](#dtldapuser-provisioning){ .headerlink }</span>

Specifies if mapped LDAP accounts are automatically created upon successful  authentication. When a user logs in with valid credentials but an account has  not been previously provisioned, an authentication failure will be returned.  This allows admins to control specifically which ldap users can access the  system and which users cannot. When this value is set to true, a local ldap  user will be created and mapped to the ldap account automatically. This  automatic provisioning only affects authentication, not authorization.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_USER_PROVISIONING</code></td></tr>
</table>

<span id="dtldapuser-search-filter">**`dt.ldap.user-search-filter`** [¶](#dtldapuser-search-filter){ .headerlink }</span>

Specifies the LDAP search filter used to search for users by their name.  The <code>{SEARCH_TERM}</code> variable will be substituted at runtime.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>(&(objectClass=group)(objectCategory=Group)(cn=*{SEARCH_TERM}*))</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>(&(objectClass=inetOrgPerson)(cn=*{SEARCH_TERM}*))</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>(&(objectClass=user)(objectCategory=Person)(cn=*{SEARCH_TERM}*))</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_USER_SEARCH_FILTER</code></td></tr>
</table>

<span id="dtldapusername-format">**`dt.ldap.username-format`** [¶](#dtldapusername-format){ .headerlink }</span>

Specifies if the username entered during login needs to be formatted prior  to asserting credentials against the directory. For Active Directory, the  userPrincipal attribute typically ends with the domain, whereas the  samAccountName attribute and other directory server implementations do not.  The %s variable will be substituted with the username asserted during login.  <br/><br/>  Example (Microsoft Active Directory):  <ul><li><code>%s@example.com</code></li></ul>  Example (ApacheDS, Fedora 389 Directory, NetIQ/Novell eDirectory, etc):  <ul><li><code>%s</code></li></ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>Example</th><td><code>%s@example.com</code></td></tr>
<tr><th>ENV</th><td><code>DT_LDAP_USERNAME_FORMAT</code></td></tr>
</table>



## Notification

<span id="dtnotification-publisheremailallow-local-connections">**`dt.notification-publisher.email.allow-local-connections`** [¶](#dtnotification-publisheremailallow-local-connections){ .headerlink }</span>

Defines whether the email notification publisher is allowed to connect to local hosts.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_PUBLISHER_EMAIL_ALLOW_LOCAL_CONNECTIONS</code></td></tr>
</table>

<span id="dtnotification-publisherkafkaallow-local-connections">**`dt.notification-publisher.kafka.allow-local-connections`** [¶](#dtnotification-publisherkafkaallow-local-connections){ .headerlink }</span>

Defines whether the Kafka notification publisher is allowed to connect to local hosts.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_PUBLISHER_KAFKA_ALLOW_LOCAL_CONNECTIONS</code></td></tr>
</table>

<span id="dtnotificationoutbox-relaybatch-size">**`dt.notification.outbox-relay.batch-size`** <strong style="color: red">*</strong> [¶](#dtnotificationoutbox-relaybatch-size){ .headerlink }</span>

Defines the number of notifications that the outbox relay will process in a batch.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>100</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_OUTBOX_RELAY_BATCH_SIZE</code></td></tr>
</table>

<span id="dtnotificationoutbox-relayenabled">**`dt.notification.outbox-relay.enabled`** <strong style="color: red">*</strong> [¶](#dtnotificationoutbox-relayenabled){ .headerlink }</span>

Defines whether the notification outbox relay should be enabled.  When disabled, notifications will still be emitted to the outbox  table, but not be delivered. Should generally stay enabled, unless:  <ul>  <li>The relay has a critical issue that impacts the rest of the system</li>  <li>You run a multi-node cluster and want more granular control over which nodes run the relay</li>  </ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_OUTBOX_RELAY_ENABLED</code></td></tr>
</table>

<span id="dtnotificationoutbox-relaylarge-notification-threshold-bytes">**`dt.notification.outbox-relay.large-notification-threshold-bytes`** <strong style="color: red">*</strong> [¶](#dtnotificationoutbox-relaylarge-notification-threshold-bytes){ .headerlink }</span>

Defines the size in bytes at which notifications are considered "large".  <br/><br/>  Large notifications will be offloaded to file storage before  being sent to the dex engine for publishing.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>65536</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_OUTBOX_RELAY_LARGE_NOTIFICATION_THRESHOLD_BYTES</code></td></tr>
</table>

<span id="dtnotificationoutbox-relaypoll-interval-ms">**`dt.notification.outbox-relay.poll-interval-ms`** <strong style="color: red">*</strong> [¶](#dtnotificationoutbox-relaypoll-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the notification outbox relay will poll  for records in the notification outbox table. Increasing this value will cause higher  notification latencies, but incurs a lesser load on the database.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>1000</code></td></tr>
<tr><th>ENV</th><td><code>DT_NOTIFICATION_OUTBOX_RELAY_POLL_INTERVAL_MS</code></td></tr>
</table>



## Observability

<span id="dtmanagementhost">**`dt.management.host`** [¶](#dtmanagementhost){ .headerlink }</span>

Defines the host for the management server, which exposes  health and metrics endpoints independently of the main server.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>0.0.0.0</code></td></tr>
<tr><th>ENV</th><td><code>DT_MANAGEMENT_HOST</code></td></tr>
</table>

<span id="dtmanagementport">**`dt.management.port`** [¶](#dtmanagementport){ .headerlink }</span>

Defines the port for the management server, which exposes  health and metrics endpoints independently of the main server.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>9000</code></td></tr>
<tr><th>ENV</th><td><code>DT_MANAGEMENT_PORT</code></td></tr>
</table>

<span id="dtmetricsauthpassword">**`dt.metrics.auth.password`** [¶](#dtmetricsauthpassword){ .headerlink }</span>

Defines the password required to access metrics.  Has no effect when [`dt.metrics.auth.username`](#dtmetricsauthusername) is not set.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_METRICS_AUTH_PASSWORD</code></td></tr>
</table>

<span id="dtmetricsauthusername">**`dt.metrics.auth.username`** [¶](#dtmetricsauthusername){ .headerlink }</span>

Defines the username required to access metrics.  Has no effect when [`dt.metrics.auth.password`](#dtmetricsauthpassword) is not set.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_METRICS_AUTH_USERNAME</code></td></tr>
</table>

<span id="dtmetricsenabled">**`dt.metrics.enabled`** [¶](#dtmetricsenabled){ .headerlink }</span>

Defines whether Prometheus metrics will be exposed.  If enabled, metrics will be available via the /metrics endpoint  of the management server.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_METRICS_ENABLED</code></td></tr>
</table>



## OpenID Connect

<span id="dtoidcclient-id">**`dt.oidc.client-id`** [¶](#dtoidcclient-id){ .headerlink }</span>

Defines the client ID to be used for OpenID Connect.  The client ID should be the same as the one configured for the frontend,  and will only be used to validate ID tokens.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_CLIENT_ID</code></td></tr>
</table>

<span id="dtoidcenabled">**`dt.oidc.enabled`** [¶](#dtoidcenabled){ .headerlink }</span>

Defines if OpenID Connect will be used for user authentication.  If enabled, `dt.oidc.*` properties should be set accordingly.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_ENABLED</code></td></tr>
</table>

<span id="dtoidcissuer">**`dt.oidc.issuer`** [¶](#dtoidcissuer){ .headerlink }</span>

Defines the issuer URL to be used for OpenID Connect.  This issuer MUST support provider configuration via the `/.well-known/openid-configuration` endpoint.  See also:  <ul>  <li>https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata</li>  <li>https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig</li>  </ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_ISSUER</code></td></tr>
</table>

<span id="dtoidcteam-synchronization">**`dt.oidc.team-synchronization`** [¶](#dtoidcteam-synchronization){ .headerlink }</span>

This option will ensure that team memberships for OpenID Connect users are dynamic and  synchronized with membership of OpenID Connect groups or assigned roles. When a team is  mapped to an OpenID Connect group, all local OpenID Connect users will automatically be  assigned to the team if they are a member of the group the team is mapped to. If the user  is later removed from the OpenID Connect group, they will also be removed from the team. This  option provides the ability to dynamically control user permissions via the identity provider.  Note that team synchronization is only performed during user provisioning and after successful  authentication.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_TEAM_SYNCHRONIZATION</code></td></tr>
</table>

<span id="dtoidcteams-claim">**`dt.oidc.teams-claim`** [¶](#dtoidcteams-claim){ .headerlink }</span>

Defines the name of the claim that contains group memberships or role assignments in the provider's userinfo endpoint.  The claim must be an array of strings, or a comma-delimited string. Most public identity providers do not support group or role management.  When using a customizable / on-demand hosted identity provider, name, content, and inclusion in the userinfo endpoint  will most likely need to be configured.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>groups</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_TEAMS_CLAIM</code></td></tr>
</table>

<span id="dtoidcuser-provisioning">**`dt.oidc.user-provisioning`** [¶](#dtoidcuser-provisioning){ .headerlink }</span>

Specifies if mapped OpenID Connect accounts are automatically created upon successful  authentication. When a user logs in with a valid access token but an account has  not been previously provisioned, an authentication failure will be returned.  This allows admins to control specifically which OpenID Connect users can access the  system and which users cannot. When this value is set to true, a local OpenID Connect  user will be created and mapped to the OpenID Connect account automatically. This  automatic provisioning only affects authentication, not authorization.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_USER_PROVISIONING</code></td></tr>
</table>

<span id="dtoidcusername-claim">**`dt.oidc.username-claim`** [¶](#dtoidcusername-claim){ .headerlink }</span>

Defines the name of the claim that contains the username in the provider's userinfo endpoint.  Common claims are `name`, `username`, `preferred_username` or `nickname`.  See also:  <ul>  <li>https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse</li>  </ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>name</code></td></tr>
<tr><th>ENV</th><td><code>DT_OIDC_USERNAME_CLAIM</code></td></tr>
</table>



## Secrets

<span id="dtsecret-managementdatabasedatasourcename">**`dt.secret-management.database.datasource.name`** [¶](#dtsecret-managementdatabasedatasourcename){ .headerlink }</span>

Defines the name of the data source to be used by the database secret manager.  <br/><br/>  Required when [`dt.secret-management.provider`](#dtsecret-managementprovider) is `database`.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>default</code></td></tr>
<tr><th>ENV</th><td><code>DT_SECRET_MANAGEMENT_DATABASE_DATASOURCE_NAME</code></td></tr>
</table>

<span id="dtsecret-managementdatabasekek">**`dt.secret-management.database.kek`** [¶](#dtsecret-managementdatabasekek){ .headerlink }</span>

Defines a base64-encoded AES-256 key (32 bytes) to use as the key encryption key (KEK)  for the database secret manager.  <br/><br/>  A secure key may be generated using OpenSSL like this: `openssl rand -base64 32`  <br/><br/>  When set, takes precedence over [`dt.secret-management.database.kek`](#dtsecret-managementdatabasekek)-keyset.path.  Unlike the keyset file approach, this option does not support KEK rotation.  <br/><br/>  Must be the same for all nodes in the cluster. When different keys are detected,  the application will fail to start.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_SECRET_MANAGEMENT_DATABASE_KEK</code></td></tr>
</table>

<span id="dtsecret-managementdatabasekek-keysetcreate-if-missing">**`dt.secret-management.database.kek-keyset.create-if-missing`** [¶](#dtsecret-managementdatabasekek-keysetcreate-if-missing){ .headerlink }</span>

Defines whether a key encryption keyset should be created if it doesn't already exist.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_SECRET_MANAGEMENT_DATABASE_KEK_KEYSET_CREATE_IF_MISSING</code></td></tr>
</table>

<span id="dtsecret-managementdatabasekek-keysetpath">**`dt.secret-management.database.kek-keyset.path`** [¶](#dtsecret-managementdatabasekek-keysetpath){ .headerlink }</span>

Defines the path to the key encryption keyset to use for the database secret manager.  <br/><br/>  Must point to the same file for all nodes in the cluster, e.g. using a shared volume  or mounted k8s secret. When different keysets are detected, the application will fail  to start.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>${dt.data-directory}/keys/secret-management-kek.json</code></td></tr>
<tr><th>ENV</th><td><code>DT_SECRET_MANAGEMENT_DATABASE_KEK_KEYSET_PATH</code></td></tr>
</table>

<span id="dtsecret-managementprovider">**`dt.secret-management.provider`** <strong style="color: red">*</strong> [¶](#dtsecret-managementprovider){ .headerlink }</span>

Defines the secret management type to use.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>enum</code></td></tr>
<tr><th>Default</th><td><code>database</code></td></tr>
<tr><th>Valid Values</th><td><code>[database, env]</code></td></tr>
<tr><th>ENV</th><td><code>DT_SECRET_MANAGEMENT_PROVIDER</code></td></tr>
</table>



## Storage

<span id="dtfile-storagelocalcompression-level">**`dt.file-storage.local.compression-level`** [¶](#dtfile-storagelocalcompression-level){ .headerlink }</span>

Defines the zstd compression level to use for local file storage.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>Valid Values</th><td><code>[-7..22]</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_LOCAL_COMPRESSION_LEVEL</code></td></tr>
</table>

<span id="dtfile-storagelocaldirectory">**`dt.file-storage.local.directory`** [¶](#dtfile-storagelocaldirectory){ .headerlink }</span>

Defines the local directory where files shall be stored.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>${dt.data-directory}/storage</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_LOCAL_DIRECTORY</code></td></tr>
</table>

<span id="dtfile-storageprovider">**`dt.file-storage.provider`** [¶](#dtfile-storageprovider){ .headerlink }</span>

Defines the file storage provider to use.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>enum</code></td></tr>
<tr><th>Default</th><td><code>local</code></td></tr>
<tr><th>Valid Values</th><td><code>[local, memory, s3]</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_PROVIDER</code></td></tr>
</table>

<span id="dtfile-storages3access-key">**`dt.file-storage.s3.access-key`** [¶](#dtfile-storages3access-key){ .headerlink }</span>

Defines the S3 access key / username.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_ACCESS_KEY</code></td></tr>
</table>

<span id="dtfile-storages3bucket">**`dt.file-storage.s3.bucket`** [¶](#dtfile-storages3bucket){ .headerlink }</span>

Defines the name of the S3 bucket.  The existence of the bucket will be verified during startup.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_BUCKET</code></td></tr>
</table>

<span id="dtfile-storages3compression-level">**`dt.file-storage.s3.compression-level`** [¶](#dtfile-storages3compression-level){ .headerlink }</span>

Defines the zstd compression level to use for S3 file storage.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5</code></td></tr>
<tr><th>Valid Values</th><td><code>[-7..22]</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_COMPRESSION_LEVEL</code></td></tr>
</table>

<span id="dtfile-storages3connect-timeout-ms">**`dt.file-storage.s3.connect-timeout-ms`** [¶](#dtfile-storages3connect-timeout-ms){ .headerlink }</span>

Defines the HTTP connect timeout for S3 requests in milliseconds.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_CONNECT_TIMEOUT_MS</code></td></tr>
</table>

<span id="dtfile-storages3endpoint">**`dt.file-storage.s3.endpoint`** [¶](#dtfile-storages3endpoint){ .headerlink }</span>

Defines the S3 endpoint URL.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_ENDPOINT</code></td></tr>
</table>

<span id="dtfile-storages3read-timeout-ms">**`dt.file-storage.s3.read-timeout-ms`** [¶](#dtfile-storages3read-timeout-ms){ .headerlink }</span>

Defines the HTTP read timeout for S3 requests in milliseconds.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_READ_TIMEOUT_MS</code></td></tr>
</table>

<span id="dtfile-storages3region">**`dt.file-storage.s3.region`** [¶](#dtfile-storages3region){ .headerlink }</span>

Defines the region of the S3 bucket.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_REGION</code></td></tr>
</table>

<span id="dtfile-storages3secret-key">**`dt.file-storage.s3.secret-key`** [¶](#dtfile-storages3secret-key){ .headerlink }</span>

Defines the S3 secret key / password.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_SECRET_KEY</code></td></tr>
</table>

<span id="dtfile-storages3write-timeout-ms">**`dt.file-storage.s3.write-timeout-ms`** [¶](#dtfile-storages3write-timeout-ms){ .headerlink }</span>

Defines the HTTP write timeout for S3 requests in milliseconds.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>null</code></td></tr>
<tr><th>ENV</th><td><code>DT_FILE_STORAGE_S3_WRITE_TIMEOUT_MS</code></td></tr>
</table>



## Task Scheduling

<span id="dttask-schedulerenabled">**`dt.task-scheduler.enabled`** [¶](#dttask-schedulerenabled){ .headerlink }</span>

Defines whether the task scheduler should be enabled.  <br/><br/>  May be disabled on specific nodes in the cluster to limit the amount of  background processing they're doing. Can help with dedicating nodes to  only serve web traffic.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>true</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_SCHEDULER_ENABLED</code></td></tr>
</table>

<span id="dttask-schedulerpoll-interval-ms">**`dt.task-scheduler.poll-interval-ms`** [¶](#dttask-schedulerpoll-interval-ms){ .headerlink }</span>

Defines the interval in milliseconds in which the task scheduler polls the  database for due tasks.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>30000</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_SCHEDULER_POLL_INTERVAL_MS</code></td></tr>
</table>

<span id="dttask-schedulershutdown-max-wait-ms">**`dt.task-scheduler.shutdown-max-wait-ms`** [¶](#dttask-schedulershutdown-max-wait-ms){ .headerlink }</span>

Defines how long, in milliseconds, the task scheduler waits for running tasks  to complete during shutdown. Tasks still running when this elapses are left in  place and picked up by another node once their heartbeat expires.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>5000</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_SCHEDULER_SHUTDOWN_MAX_WAIT_MS</code></td></tr>
</table>

<span id="dttask-schedulerthreads">**`dt.task-scheduler.threads`** [¶](#dttask-schedulerthreads){ .headerlink }</span>

Defines the number of threads the task scheduler uses to execute due tasks.  This is the maximum number of scheduled tasks that may run concurrently on  a single node.  <br/><br/>  The scheduled task volume is low, but a few tasks can be long-running,  so the value should be large enough to keep one slow task from blocking others.  <br/><br/>  Note that the grunt of asynchronous work is performed by the dex engine,  not by the task scheduler. This is the wrong knob to tweak in most cases.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>integer</code></td></tr>
<tr><th>Default</th><td><code>3</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_SCHEDULER_THREADS</code></td></tr>
</table>

<span id="dttaskdefect-dojo-uploadcron">**`dt.task.defect-dojo-upload.cron`** <strong style="color: red">*</strong> [¶](#dttaskdefect-dojo-uploadcron){ .headerlink }</span>

Cron expression of the DefectDojo upload task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 2 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_DEFECT_DOJO_UPLOAD_CRON</code></td></tr>
</table>

<span id="dttaskepss-mirrorcron">**`dt.task.epss-mirror.cron`** <strong style="color: red">*</strong> [¶](#dttaskepss-mirrorcron){ .headerlink }</span>

Cron expression of the EPSS mirroring task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 1 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_EPSS_MIRROR_CRON</code></td></tr>
</table>

<span id="dttaskexpired-session-cleanupcron">**`dt.task.expired-session-cleanup.cron`** <strong style="color: red">*</strong> [¶](#dttaskexpired-session-cleanupcron){ .headerlink }</span>

Cron expression of the expired session cleanup task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 * * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_EXPIRED_SESSION_CLEANUP_CRON</code></td></tr>
</table>

<span id="dttaskfortify-ssc-uploadcron">**`dt.task.fortify-ssc-upload.cron`** <strong style="color: red">*</strong> [¶](#dttaskfortify-ssc-uploadcron){ .headerlink }</span>

Cron expression of the Fortify SSC upload task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 2 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_FORTIFY_SSC_UPLOAD_CRON</code></td></tr>
</table>

<span id="dttaskgithub-advisory-vuln-data-source-mirrorcron">**`dt.task.github-advisory-vuln-data-source-mirror.cron`** <strong style="color: red">*</strong> [¶](#dttaskgithub-advisory-vuln-data-source-mirrorcron){ .headerlink }</span>

Cron expression of the vulnerability GitHub Advisories mirroring task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 2 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_GITHUB_ADVISORY_VULN_DATA_SOURCE_MIRROR_CRON</code></td></tr>
</table>

<span id="dttaskkenna-security-uploadcron">**`dt.task.kenna-security-upload.cron`** <strong style="color: red">*</strong> [¶](#dttaskkenna-security-uploadcron){ .headerlink }</span>

Cron expression of the Kenna Security upload task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 2 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_KENNA_SECURITY_UPLOAD_CRON</code></td></tr>
</table>

<span id="dttaskkev-mirrorcron">**`dt.task.kev-mirror.cron`** <strong style="color: red">*</strong> [¶](#dttaskkev-mirrorcron){ .headerlink }</span>

Cron expression of the KEV (Known Exploited Vulnerabilities) mirroring task.  Triggers mirroring of all enabled KEV data sources.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 2 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_KEV_MIRROR_CRON</code></td></tr>
</table>

<span id="dttaskmetrics-maintenancecron">**`dt.task.metrics-maintenance.cron`** <strong style="color: red">*</strong> [¶](#dttaskmetrics-maintenancecron){ .headerlink }</span>

Cron expression of the metrics maintenance task.  <br/><br/>  The task creates new partitions for the day for the following tables  And deletes records older than the configured metrics retention duration from the following tables:  <ul>  <li><code>DEPENDENCYMETRICS</code></li>  <li><code>PROJECTMETRICS</code></li>  </ul>  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>1 * * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_METRICS_MAINTENANCE_CRON</code></td></tr>
</table>

<span id="dttasknvd-vuln-data-source-mirrorcron">**`dt.task.nvd-vuln-data-source-mirror.cron`** <strong style="color: red">*</strong> [¶](#dttasknvd-vuln-data-source-mirrorcron){ .headerlink }</span>

Cron expression of the NIST / NVD mirroring task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 4 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_NVD_VULN_DATA_SOURCE_MIRROR_CRON</code></td></tr>
</table>

<span id="dttaskosv-vuln-data-source-mirrorcron">**`dt.task.osv-vuln-data-source-mirror.cron`** <strong style="color: red">*</strong> [¶](#dttaskosv-vuln-data-source-mirrorcron){ .headerlink }</span>

Cron expression of the OSV mirroring task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 3 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_OSV_VULN_DATA_SOURCE_MIRROR_CRON</code></td></tr>
</table>

<span id="dttaskpackage-metadata-maintenancecron">**`dt.task.package-metadata-maintenance.cron`** <strong style="color: red">*</strong> [¶](#dttaskpackage-metadata-maintenancecron){ .headerlink }</span>

Cron expression of the package metadata maintenance task.  <br/><br/>  The task deletes orphaned records from the `PACKAGE_ARTIFACT_METADATA` and  `PACKAGE_METADATA` tables.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 */12 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_PACKAGE_METADATA_MAINTENANCE_CRON</code></td></tr>
</table>

<span id="dttaskpackage-metadata-resolutioncron">**`dt.task.package-metadata-resolution.cron`** <strong style="color: red">*</strong> [¶](#dttaskpackage-metadata-resolutioncron){ .headerlink }</span>

Cron expression of the package metadata resolution task.  <br/><br/>  Note that package metadata resolution is also triggered by other  actions, such as BOM uploads. The scheduled execution is mostly  relevant for deployments that may sit idle for a long time.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 1 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_PACKAGE_METADATA_RESOLUTION_CRON</code></td></tr>
</table>

<span id="dttaskportfolio-analysiscron">**`dt.task.portfolio-analysis.cron`** <strong style="color: red">*</strong> [¶](#dttaskportfolio-analysiscron){ .headerlink }</span>

Cron expression of the portfolio vulnerability analysis task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 6 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_PORTFOLIO_ANALYSIS_CRON</code></td></tr>
</table>

<span id="dttaskportfolio-metrics-updatecron">**`dt.task.portfolio-metrics-update.cron`** <strong style="color: red">*</strong> [¶](#dttaskportfolio-metrics-updatecron){ .headerlink }</span>

Cron expression of the portfolio metrics update task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>10 * * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_PORTFOLIO_METRICS_UPDATE_CRON</code></td></tr>
</table>

<span id="dttaskproject-maintenancecron">**`dt.task.project-maintenance.cron`** <strong style="color: red">*</strong> [¶](#dttaskproject-maintenancecron){ .headerlink }</span>

Cron expression of the project maintenance task.  <br/><br/>  The task deletes inactive projects based on retention policy.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 */4 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_PROJECT_MAINTENANCE_CRON</code></td></tr>
</table>

<span id="dttaskscheduled-notification-dispatchcron">**`dt.task.scheduled-notification-dispatch.cron`** <strong style="color: red">*</strong> [¶](#dttaskscheduled-notification-dispatchcron){ .headerlink }</span>

Cron expression for polling scheduled notification rules that are due for dispatch.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>* * * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_SCHEDULED_NOTIFICATION_DISPATCH_CRON</code></td></tr>
</table>

<span id="dttasktag-maintenancecron">**`dt.task.tag-maintenance.cron`** <strong style="color: red">*</strong> [¶](#dttasktag-maintenancecron){ .headerlink }</span>

Cron expression of the tag maintenance task.  <br/><br/>  The task deletes orphaned tags that are not used anymore.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 */12 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_TAG_MAINTENANCE_CRON</code></td></tr>
</table>

<span id="dttasktelemetry-submissioncron">**`dt.task.telemetry-submission.cron`** <strong style="color: red">*</strong> [¶](#dttasktelemetry-submissioncron){ .headerlink }</span>

Cron expression of the telemetry submission task.  <br/><br/>  The task enforces a 24-hour minimum interval between submissions,  so the cron expression controls how often the task checks  whether a submission is due.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 */1 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_TELEMETRY_SUBMISSION_CRON</code></td></tr>
</table>

<span id="dttaskvuln-database-maintenancecron">**`dt.task.vuln-database-maintenance.cron`** <strong style="color: red">*</strong> [¶](#dttaskvuln-database-maintenancecron){ .headerlink }</span>

Cron expression of the vulnerability database maintenance task.  <br/><br/>  The task deletes orphaned records from the `VULNERABLESOFTWARE` table.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 0 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_VULN_DATABASE_MAINTENANCE_CRON</code></td></tr>
</table>

<span id="dttaskvuln-metrics-updatecron">**`dt.task.vuln-metrics-update.cron`** <strong style="color: red">*</strong> [¶](#dttaskvuln-metrics-updatecron){ .headerlink }</span>

Cron expression of the vulnerability metrics update task.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>0 */6 * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_VULN_METRICS_UPDATE_CRON</code></td></tr>
</table>

<span id="dttaskvuln-policy-bundle-synccron">**`dt.task.vuln-policy-bundle-sync.cron`** <strong style="color: red">*</strong> [¶](#dttaskvuln-policy-bundle-synccron){ .headerlink }</span>

Cron expression of the vulnerability policy bundle synchronization task.  <br/><br/>  Has no effect unless [`dt.vuln-policy-bundle.url`](#dtvuln-policy-bundleurl) is also configured.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>cron</code></td></tr>
<tr><th>Default</th><td><code>*/15 * * * *</code></td></tr>
<tr><th>ENV</th><td><code>DT_TASK_VULN_POLICY_BUNDLE_SYNC_CRON</code></td></tr>
</table>



## Vulnerability Analysis

<span id="dtvuln-analyzerinternaldatasourcename">**`dt.vuln-analyzer.internal.datasource.name`** [¶](#dtvuln-analyzerinternaldatasourcename){ .headerlink }</span>

Defines the name of the data source to be used by the internal vulnerability analyzer.  <br/><br/>  The internal analyzer performs no database writes, so this data source  *could* point to a read replica if needed.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>default</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_ANALYZER_INTERNAL_DATASOURCE_NAME</code></td></tr>
</table>

<span id="dtvuln-analyzeross-indexallow-local-connections">**`dt.vuln-analyzer.oss-index.allow-local-connections`** [¶](#dtvuln-analyzeross-indexallow-local-connections){ .headerlink }</span>

Defines whether the OSS Index vulnerability analyzer is allowed to connect to local hosts.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>boolean</code></td></tr>
<tr><th>Default</th><td><code>false</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_ANALYZER_OSS_INDEX_ALLOW_LOCAL_CONNECTIONS</code></td></tr>
</table>

<span id="dtvuln-analyzersnykapi-version">**`dt.vuln-analyzer.snyk.api-version`** [¶](#dtvuln-analyzersnykapi-version){ .headerlink }</span>

Defines the Snyk REST API version to use.  <br/><br/>  Should only be changed if the default version is discontinued by Snyk  and an upgrade of Dependency-Track is not immediately possible.  

<table>
<tr><th>Type</th><td style="border-width: 0"><code>string</code></td></tr>
<tr><th>Default</th><td><code>2025-11-05</code></td></tr>
<tr><th>ENV</th><td><code>DT_VULN_ANALYZER_SNYK_API_VERSION</code></td></tr>
</table>


