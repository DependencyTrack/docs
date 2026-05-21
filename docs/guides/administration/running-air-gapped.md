# Running air-gapped

Dependency-Track can run in environments without outbound internet access, but every integration that normally reaches a
public endpoint needs an alternative. This guide collects the relevant considerations.

!!! warning "Incomplete"
    This guide is a work in progress. It currently covers vulnerability data sources and vulnerability analyzers. Other
    application areas (notifications, repository metadata for outdated-component detection)
    also reach the public internet by default and will be documented here as the content is written. If your air-gapped
    deployment depends on one of those areas, treat this guide as a starting point, not a complete checklist.

If your network only routes outbound traffic through a proxy, you may not need a full air-gapped setup. See [Configuring
an HTTP proxy](configuring-http-proxy.md) and [Configuring internal CA trust](configuring-internal-ca.md) first.

## Vulnerability data sources

For background on the three mirrored sources and how to enable them, see [Configuring vulnerability
sources](configuring-vulnerability-sources.md). Each source has a different air-gapped story.

### NVD

Host files that match the [NVD JSON 2.0 feed layout](https://nvd.nist.gov/vuln/data-feeds#divJson20Feeds) on an internal
HTTP file server. Dependency-Track requires the `META` and `GZ` files. The `ZIP` files are not required.

Point the NVD source's feed URL at the internal mirror, then use the **Test** action in the NVD configuration panel to
confirm the mirror is reachable and serves files in the expected layout.

### OSV

Host the [OSV data dumps](https://google.github.io/osv.dev/data/#data-dumps) on an internal HTTP file server.
Dependency-Track expects per-ecosystem `all.zip` files. Dependency-Track also requires `modified_id.csv` for incremental
mirroring. If you turn off incremental mirroring, Dependency-Track re-downloads the full dumps on every run.

Point the OSV source's base URL at the internal mirror.

### GitHub advisories

The GitHub advisories integration uses GitHub's paginated GraphQL API. A static HTTP mirror cannot serve it. Forwarding
through an HTTP forward proxy may work but is not tested.

In a strict air-gapped environment, turn off the GitHub advisories source. Use OSV for open source coverage instead. OSV
ingests GitHub advisories along with advisories from other curators, so you do not lose GHSA-prefixed records by relying
on OSV alone.

## Vulnerability analyzers

The [internal analyzer](../../reference/analyzers.md#internal) is air-gap safe. It queries only the local vulnerability
database and makes no outbound calls during analysis, so it works as long as you have configured the corresponding
[vulnerability data sources](#vulnerability-data-sources) above.

[Trivy](../../reference/analyzers.md#trivy) is the other practical option. The Trivy server itself supports air-gapped
operation by loading its vulnerability database from internal storage ahead of time. See the [Trivy air-gapped
environment guide](https://trivy.dev/docs/latest/guide/advanced/air-gap/) for setup. Dependency-Track only talks to the
Trivy server you operate, so as long as the Trivy server is reachable from the API server, the analyzer works.

The [OSS Index](../../reference/analyzers.md#oss-index), [Snyk](../../reference/analyzers.md#snyk), and
[VulnDB](../../reference/analyzers.md#vulndb) analyzers call vendor-hosted APIs on every analysis run and require
outbound connectivity to those endpoints. Routing them through a caching proxy may work but is not tested. In a strict
air-gapped environment, turn these analyzers off.

## See also

- [Configuring vulnerability sources](configuring-vulnerability-sources.md)
- [Configuring an HTTP proxy](configuring-http-proxy.md)
- [Configuring internal CA trust](configuring-internal-ca.md)
