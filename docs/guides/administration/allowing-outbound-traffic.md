# Allowing outbound traffic

The API server makes outbound HTTPS calls to mirror [vulnerability data
sources](configuring-vulnerability-sources.md), query analyzers, and fetch package
metadata from repositories. If a firewall or proxy restricts egress, allow the API
server to reach the hosts in this guide.

All default endpoints use HTTPS on TCP port 443. The frontend is a static app served
to the browser and does not originate these calls.

The in-repo [`services.bom.json`](https://github.com/DependencyTrack/dependency-track/blob/main/apiserver/src/main/resources/services.bom.json)
file is the source of truth for default service URLs. Release SBOMs merge that file
into the published `bom.json`. Repository URLs, analyzer base URLs, and notification
destinations that you set in **Administration** are extra hosts. They are not in
`services.bom.json`.

If outbound traffic must go through a proxy, see [Configuring an HTTP
proxy](configuring-http-proxy.md). If the proxy intercepts TLS, see [Configuring
internal CA trust](configuring-internal-ca.md). If the API server has no outbound
internet access, see [Running air-gapped](running-air-gapped.md).

## Vulnerability data sources and analyzers

| Service | Host | Default URL |
|:--------|:-----|:------------|
| NVD | `nvd.nist.gov` | `https://nvd.nist.gov/feeds` |
| GitHub Advisories | `api.github.com` | `https://api.github.com/graphql` |
| OSV | `osv-vulnerabilities.storage.googleapis.com` | `https://osv-vulnerabilities.storage.googleapis.com` |
| OSS Index | `ossindex.sonatype.org` | `https://ossindex.sonatype.org/api/v3/component-report` |
| Snyk | `api.snyk.io` | `https://api.snyk.io` |
| VulnDB | `vulndb.cyberriskanalytics.com` | `https://vulndb.cyberriskanalytics.com/api/v1/` |
| EPSS | `epss.empiricalsecurity.com` | `https://epss.empiricalsecurity.com/epss_scores-current.csv.gz` |

OSS Index, Snyk, and VulnDB are analyzers. They call the vendor API during
vulnerability analysis when you enable them. NVD, GitHub Advisories, OSV, and EPSS
are mirrored on a schedule.

## Package repositories

Dependency-Track queries these default registries for latest-version metadata. You
can add, replace, or disable repositories in **Administration > Repositories**.

| Ecosystem | Host | Default URL |
|:----------|:-----|:------------|
| Cargo (Rust) | `index.crates.io` | `https://index.crates.io` |
| Composer (PHP) | `repo.packagist.org` | `https://repo.packagist.org/p/` |
| Gem (Ruby) | `rubygems.org` | `https://rubygems.org/api/v1/versions` |
| GitHub (Actions) | `api.github.com` | `https://api.github.com/repos/` |
| Go Modules | `proxy.golang.org` | `https://proxy.golang.org/` |
| Hex (Erlang/Elixir) | `hex.pm` | `https://hex.pm/api/packages` |
| Maven Central | `repo1.maven.org` | `https://repo1.maven.org/maven2` |
| Atlassian Maven | `packages.atlassian.com` | `https://packages.atlassian.com/content/repositories/atlassian-public/` |
| JBoss Maven | `repository.jboss.org` | `https://repository.jboss.org/nexus/content/repositories/releases/` |
| Clojars | `repo.clojars.org` | `https://repo.clojars.org/` |
| Google Maven | `maven.google.com` | `https://maven.google.com/` |
| npm | `registry.npmjs.org` | `https://registry.npmjs.org/-/package/` |
| NuGet | `api.nuget.org` | `https://api.nuget.org/v3-flatcontainer/` |
| PyPI | `pypi.org` | `https://pypi.org/pypi/` |
| CPAN (Perl) | `fastapi.metacpan.org` | `https://fastapi.metacpan.org/v1/` |
| Hackage (Haskell) | `hackage.haskell.org` | `https://hackage.haskell.org/` |
| Nixpkgs | `channels.nixos.org` | `https://channels.nixos.org/nixpkgs-unstable/packages.json.br` |

## Telemetry

When you enable anonymous usage telemetry, the API server posts to
`https://metrics.dependencytrack.org`.

## Other destinations you configure

These hosts are not defaults in `services.bom.json`. Allow them only for the
integrations you turn on.

| Integration | Hosts |
|:------------|:------|
| [KEV catalogs](configuring-kev-sources.md) | `www.cisa.gov`, `raw.githubusercontent.com`, `api.vulncheck.com`, plus the storage host VulnCheck returns for the catalog download |
| [Trivy](../../reference/analyzers.md#trivy) | The Trivy server you operate |
| [OIDC](configuring-oidc.md) | Your identity provider |
| [LDAP](configuring-ldap.md) | Your directory server (TCP 389 or 636, not 443) |
| Notification publishers | Slack, Teams, email, Jira, webhooks, or other destinations you configure |
| Private package registries | Any repository URL you add in **Administration > Repositories** |

## See also

- [Configuring an HTTP proxy](configuring-http-proxy.md)
- [Configuring internal CA trust](configuring-internal-ca.md)
- [Configuring vulnerability sources](configuring-vulnerability-sources.md)
- [Configuring KEV sources](configuring-kev-sources.md)
- [Running air-gapped](running-air-gapped.md)
- [Package repositories](../../reference/datasources/repositories.md)
