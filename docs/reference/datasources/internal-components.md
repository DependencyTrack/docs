# Internal Components

Dependency-Track allows organisations to mark certain component namespaces and/or names
as *internal*. Components identified as internal are excluded from all external services:
they are never sent to external vulnerability analyzers (OSS Index, Snyk, Trivy, VulnDB)
and never queried against public package repositories.

This is useful when your SBOMs include first-party libraries with coordinates that could
coincide with public packages, or when you simply do not want metadata about internal
packages to leave your network.

## How Matching Works

Internal component identification is configured in
**Administration → Internal Components** by specifying one or more namespace and/or name
patterns.

Two matching modes are available:

| Mode | Behaviour |
|:-----|:----------|
| OR (default) | A component is internal if its namespace *or* name matches any configured pattern. |
| AND | A component is internal if its namespace *and* name both match. |

Patterns are matched against the component's PURL namespace and name fields.

!!! note
    By default, no components are identified as internal. All components are treated
    as third-party and may be sent to configured external analyzers.

## Effects of Being Marked Internal

| Service | Behaviour for internal components |
|:--------|:----------------------------------|
| OSS Index | Not queried |
| Snyk | Not queried |
| Trivy | Not queried |
| VulnDB | Not queried |
| Public package repositories | Not queried for version currency checks |
| Internal analyzer | Still evaluated against the local vulnerability database |
| Private repositories | Still queried if configured |

## Use with the Private Vulnerability Repository

Internal components can still be matched against vulnerabilities defined in the
[private vulnerability repository](private-vulnerability-repository.md). This allows
organisations to track and triage vulnerabilities in their own codebases without
exposing component identifiers externally.
