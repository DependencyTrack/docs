# GitHub Advisories

The [GitHub Advisory Database](https://github.com/advisories) (GHSA) contains
security advisories for open source packages hosted on GitHub and other ecosystems.
Advisories may or may not overlap with NVD CVE records—GitHub often publishes
advisories for vulnerabilities that are not yet in the NVD, or with more ecosystem-
specific detail.

## What It Provides

GitHub Advisories are keyed by PURL and map directly to package ecosystems such as
npm, Maven, PyPI, Go, NuGet, and others. This makes them highly effective for
open source component matching without requiring a CPE.

Dependency-Track automatically synchronises vulnerability aliases between GHSA and
CVE identifiers where GitHub has made the link explicit. This means a component can
be matched by either its GHSA or CVE identifier, and the finding will not be
duplicated.

## Mirroring

Dependency-Track mirrors GitHub Advisories via GitHub's public GraphQL API. The mirror
refreshes daily and on instance startup.

The mirroring schedule is controlled by
[`dt.task.git.hub.advisory.mirror.cron`](../configuration/properties.md#dttaskgithubadvisorymirrorcron).

## Configuration

GitHub Advisory mirroring is configured in the administration UI under
**Administration → Datasources → GitHub Advisories**.

| Setting | Description |
|:--------|:------------|
| Enabled | Whether GitHub Advisory mirroring is active. Enabled by default. |
| GitHub Personal Access Token | Required. A GitHub PAT with no scopes assigned is sufficient. Without a token, the GraphQL API rejects requests. |

To create a token, visit [github.com/settings/tokens](https://github.com/settings/tokens)
and generate a classic or fine-grained token. No scopes are required—the public
advisory data is accessible to any authenticated user.
