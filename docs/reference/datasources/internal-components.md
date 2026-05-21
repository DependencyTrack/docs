# Internal components

Dependency-Track allows organizations to mark certain component namespaces and names as *internal*. Components
identified as internal are excluded from all external services. They are never sent to external vulnerability analyzers
(OSS Index, Snyk, Trivy, VulnDB) and never queried against public package repositories.

This is useful when SBOMs include first-party libraries whose coordinates could coincide with public packages, or when
metadata about internal packages must not leave the network.

## How matching works

Configure internal component identification in **Administration > Internal components** by specifying one or more
namespace and name patterns.

Two matching modes are available:

| Mode | Behavior |
|:-----|:---------|
| OR (default) | A component is internal if its namespace or name matches any configured pattern. |
| AND | A component is internal if its namespace and name both match. |

Patterns are matched against the component's PURL namespace and name fields.

!!! note
    By default, no components are identified as internal. All components are treated as third-party and may be sent to
    configured external analyzers.

## Effects of being marked internal

| Service | Behavior for internal components |
|:--------|:---------------------------------|
| OSS Index | Not queried |
| Snyk | Not queried |
| Trivy | Not queried |
| VulnDB | Not queried |
| Public package repositories | Not queried for version currency checks |
| Internal analyzer | Still evaluated against the local vulnerability database |
| Private repositories | Still queried if configured |

## Use with the private vulnerability repository

Internal components can still be matched against vulnerabilities defined in the [private vulnerability
repository](private-vulnerability-repository.md). This allows organizations to track and triage vulnerabilities in their
own codebases without exposing component identifiers externally.
