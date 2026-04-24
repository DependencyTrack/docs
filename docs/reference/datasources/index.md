# Vulnerability Datasources

Vulnerability datasources are the upstream feeds from which Dependency-Track populates
its internal vulnerability database. The [internal analyzer](../analyzers.md#internal)
queries this local database when evaluating components, so no external call is made at
analysis time—only during mirroring.

Mirroring runs on a configurable schedule (daily by default) and on instance startup.
Progress and errors are reported via the `DATASOURCE_MIRRORING`
[notification group](../../concepts/architecture/design/notifications.md).

## Mirrored Sources

These sources are downloaded and stored locally. The internal analyzer queries them
without contacting any external service during vulnerability analysis.

| Source | Identifier prefix | Primary use |
|:-------|:-----------------|:------------|
| [NVD](nvd.md) | `CVE-` | CPE-based matching for all component types |
| [GitHub Advisories](github-advisories.md) | `GHSA-` | PURL-based matching for open source packages |
| [OSV](osv.md) | varies by ecosystem | PURL-based matching for open source packages |

## Other Sources

| Source | Description |
|:-------|:------------|
| [Private Vulnerability Repository](private-vulnerability-repository.md) | Internally managed vulnerabilities for proprietary components or pre-disclosure research |
| [Repositories](repositories.md) | Package registry integrations used for outdated component detection |
| [Internal Components](internal-components.md) | Configuring components that should never be sent to external services |

## Analyzers That Query External Services

OSS Index, Snyk, Trivy, and VulnDB are *analyzers* that call external APIs at analysis
time. They are documented separately in the [Analyzers](../analyzers.md) reference.
