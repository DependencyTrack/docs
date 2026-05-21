# Vulnerability datasources

Vulnerability datasources are the upstream feeds from which Dependency-Track populates its internal vulnerability
database. The [internal analyzer](../analyzers.md#internal) queries this local database during vulnerability analysis,
so no external call is made at analysis time, only during mirroring.

For background on what each source provides and the trade-offs between them, see [About vulnerability data
sources](../../concepts/about-vulnerability-data-sources.md). For the procedure to enable and schedule mirrors, see
[Configuring vulnerability sources](../../guides/administration/configuring-vulnerability-sources.md).

## Mirrored sources

Dependency-Track can mirror three public sources into its local database. Mirroring runs on a configurable schedule
(daily by default) and on instance startup. Progress and errors are written to the API server logs.

| Source | Identifier prefix | Matches on |
|:-------|:------------------|:-----------|
| NVD | `CVE-` | CPE |
| GitHub advisories | `GHSA-` | PURL |
| OSV | varies by ecosystem | PURL |

## Other sources

| Source | Description |
|:-------|:------------|
| [Private vulnerability repository](private-vulnerability-repository.md) | Internally managed vulnerabilities for proprietary components or pre-disclosure research. |
| [Repositories](repositories.md) | Package registry integrations used for outdated component detection. Not a vulnerability source. |
| [Internal components](internal-components.md) | Marks components that must never be sent to external services. |

## Analyzers that query external services

OSS Index, Snyk, Trivy, and VulnDB are *analyzers* that call external APIs at analysis time. They are documented
separately in the [Analyzers](../analyzers.md) reference.
