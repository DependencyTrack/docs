# Community Integrations

The following tools and integrations have been built by the community on top of
Dependency-Track's API-first design. They are maintained independently and are not
officially supported by the Dependency-Track project.

!!! note
    Dependency-Track's [REST API](api/v1.md) provides full programmatic access to
    all platform features. This makes it straightforward to build custom integrations
    for tools and workflows not listed here.

## CI/CD and Build System Plugins

These plugins automate SBOM upload and vulnerability gate evaluation as part of your
build pipeline.

| Tool | Integration | Link |
|:-----|:------------|:-----|
| Jenkins | Dependency-Track Jenkins Plugin | [jenkins.io](https://plugins.jenkins.io/dependency-track/) |
| GitHub | OWASP Dependency-Track Check GitHub Action | [GitHub Marketplace](https://github.com/marketplace/actions/owasp-dependency-track-check) |
| Azure DevOps | Azure DevOps Extension | [Visual Studio Marketplace](https://marketplace.visualstudio.com/) |
| Maven | `dependency-track-maven-plugin` | [GitHub](https://github.com/pmckeown/dependency-track-maven-plugin) |

## Developer Portals

| Tool | Integration | Link |
|:-----|:------------|:-----|
| Backstage | Dependency-Track Backstage Plugin (TRIMM) | [GitHub](https://github.com/TRIMM/plugin-dependency-track) |

## Client Libraries

These libraries provide programmatic access to the Dependency-Track API from your
own tools and automation scripts.

| Language | Library | Link |
|:---------|:--------|:-----|
| Go | Dependency-Track Client | [GitHub](https://github.com/nscuro/dtrack-client-go) |
| Python | Dependency-Track Client | [GitHub](https://github.com/nscuro/dtrack-client-py) |
| Ruby | Dependency-Track Client | [GitHub](https://github.com/nscuro/dtrack-client-rb) |

## Security and Vulnerability Management

| Tool | Integration | Link |
|:-----|:------------|:-----|
| SecObserve | Dependency-Track integration | [GitHub](https://github.com/MaibornWolff/SecObserve) |
| Mixeway Hub | Risk aggregation platform | [mixeway.pl](https://mixeway.pl) |
| SD Elements (Security Compass) | Dependency-Track integration | [securitycompass.com](https://securitycompass.com) |

## Reporting and Auditing

| Tool | Description | Link |
|:-----|:------------|:-----|
| Dependency-Track Reporting Tool | Generates reports from Dependency-Track data (Modus Operandi) | [GitHub](https://github.com/ModusCreateOrg/dependency-track-report-tool) |
| dtrack-audit | CLI tool for auditing findings (OZON.ru) | [GitHub](https://github.com/ozonru/dtrack-audit) |
| dtrack-auditor | Policy-driven finding auditor | [GitHub](https://github.com/jetstack/dtrack-auditor) |
| `dependency-track-exporter` | Prometheus metrics exporter (Jetstack) | [GitHub](https://github.com/jetstack/dependency-track-exporter) |

## Other Utilities

| Tool | Description | Link |
|:-----|:------------|:-----|
| dtapac | Policy-as-code for Dependency-Track via OPA | [GitHub](https://github.com/nscuro/dtapac) |
| sbomify | SBOM enrichment and sharing | [sbomify.com](https://sbomify.com) |

---

*Know of an integration that should be listed here? Open a pull request on the
[documentation repository](https://github.com/DependencyTrack/hyades).*
