---
title: Home
hide:
- navigation
---

# Dependency-Track

Dependency-Track is an intelligent component analysis platform
that allows organizations to identify and reduce risk in the software supply chain.

Built around the Bill of Materials (BOM) concept,
it tracks component usage across every version of every project in your portfolio
and surfaces known vulnerabilities, policy violations, and licensing risk as they emerge.
An API-first design makes it a natural fit for CI/CD pipelines.

!!! info "Documentation version"
    This documentation covers Dependency-Track v5.
    For v4, see the [v4 documentation](../4.x/).

## Features

### Find and rank vulnerabilities

- **Continuous monitoring**: Dependency-Track re-analyzes your portfolio on a schedule,
  so newly disclosed [vulnerabilities](concepts/vulnerability-findings.md) surface without a new upload.
- **Multiple data sources**: combine [mirrored data sources](concepts/about-vulnerability-data-sources.md)
  such as NVD, GitHub Advisories, and OSV
  with [analyzers](reference/analyzers.md) such as Sonatype OSS Index, Snyk, Trivy, and VulnDB.
- **Risk-based prioritization**: rank findings by CVSS severity, EPSS exploit prediction,
  and [known exploited vulnerability catalogs](concepts/about-kev-data-sources.md) from CISA, ENISA, and VulnCheck.
- **Dashboards and trends**: follow risk scores for the portfolio, each project, and each component
  [over time](concepts/time-series-metrics.md).
- **Private vulnerabilities**: track
  [issues your organization discovers](guides/user/managing-private-vulnerabilities.md)
  alongside public ones.

### Know what's in your software

- **BOM import**: upload [CycloneDX](reference/file-formats.md) BOMs from any ecosystem or build tool,
  including services and the dependency graph.
- **Portfolio inventory**: [organize projects](guides/user/organizing-projects.md)
  with versions, hierarchies, and tags.
- **Portfolio-wide search**: find every project that uses a component, or that a vulnerability affects.
- **Outdated component detection**: check [package repositories](reference/datasources/repositories.md)
  such as Maven Central, npm, and PyPI for newer versions,
  and [verify component integrity](concepts/component-integrity-verification.md).

### Enforce policies

- **License compliance**: flag components with licenses your organization doesn't allow,
  using [component policies](concepts/component-policies.md) and license groups.
- **Security and operational rules**: catch high-severity vulnerabilities, outdated or old components,
  and banned packages.
- **Custom conditions**: write [condition expressions](reference/policies/condition-expressions.md) in CEL
  when the built-in conditions don't fit.
- **Violation review**: [triage policy violations](guides/user/triaging-policy-violations.md)
  and approve, reject, or suppress them with a recorded reason.

### Triage and share decisions

- **Audit trail**: record an analysis state, justification, and comments for each finding, and keep their history.
- **Automated triage**: apply decisions across the portfolio
  with [vulnerability policies](concepts/vulnerability-policies.md),
  optionally distributed from a central bundle.
- **VEX and VDR**: [exchange VEX documents](guides/user/exchanging-vex-documents.md) with customers and suppliers,
  and export vulnerability disclosure reports.

### Integrate and automate

- **API-first**: automate every task available in the UI
  through the [v1](reference/api/v1.md) and [v2](reference/api/v2.md) REST APIs.
- **CI/CD**: [upload SBOMs](guides/user/uploading-boms.md) from any pipeline with a single API call,
  and let Dependency-Track create the project and version on first upload.
- **Notifications**: send real-time alerts or scheduled summaries
  to [Slack, Microsoft Teams, Mattermost, Webex, email, Jira, webhooks, and Kafka](reference/notifications/publishers.md).
- **Vulnerability management platforms**: forward findings to DefectDojo, Fortify SSC, and Kenna Security.
- **Badges**: embed [vulnerability and policy badges](reference/badges.md) in README files and internal pages,
  once an administrator turns on badge access.
- **Community integrations**: [plugins and tools](reference/community-integrations.md)
  for Jenkins, GitHub Actions, Azure DevOps, Maven, Backstage, and more.

### Control access

- **Identity providers**: sign in through [OIDC](guides/administration/configuring-oidc.md)
  or [LDAP](guides/administration/configuring-ldap.md), with optional team synchronization.
- **Teams and permissions**: grant fine-grained permissions to teams,
  and limit which projects each team can see with [portfolio access control](concepts/access-control.md).
- **Machine identities**: give pipelines, scanners, and scripts their own
  [service accounts](concepts/access-control.md#service-accounts), with permissions separate from any person's account.
- **Keyless authentication**: let GitHub Actions, GitLab CI, Kubernetes, or SPIFFE workloads sign in
  with their platform's short-lived tokens through [workload identity federation](concepts/workload-identity-federation.md),
  with no API keys to store or rotate.
- **Centralized secrets**: store integration credentials encrypted in one place
  with [managed secrets](guides/user/managing-secrets.md).

### Deploy and operate

- **Open source and self-hosted**: free under the Apache 2.0 license, running on your own infrastructure.
- **Minimal infrastructure**: run the [container images](reference/container-images.md)
  with PostgreSQL as the only external service.
- **Horizontal scaling**: [add instances](guides/administration/scaling.md) as your portfolio grows,
  for example [on Kubernetes](guides/administration/deploying-to-kubernetes.md),
  with health checks and Prometheus metrics.
- **Restricted networks**: run behind an [HTTP proxy](guides/administration/configuring-http-proxy.md),
  or with an [internal certificate authority](guides/administration/configuring-internal-ca.md).
- **Localized interface**: use the web interface in 15 languages.

## Getting started

Get Dependency-Track running locally in minutes with the [quick start tutorial](tutorials/quickstart.md).

Explore the documentation using the navigation tabs:

- [Tutorials](tutorials/index.md): step-by-step walkthroughs for common workflows.
- [Guides](guides/index.md): task-oriented procedures for specific goals.
- [Concepts](concepts/index.md): background material on how Dependency-Track works.
- [Reference](reference/index.md): technical descriptions of APIs, configuration, and internals.

## Key concepts

- [Projects](concepts/projects.md): how Dependency-Track models the software you track.
- [Vulnerability findings](concepts/vulnerability-findings.md): how known vulnerabilities are surfaced and triaged.
- [Component policies](concepts/component-policies.md): codify what's acceptable in your portfolio.
- [Access control](concepts/access-control.md): teams, permissions, and project hierarchy.

## Coming from v4?

See [About changes in v5](concepts/changes-in-v5.md) for what changed and why,
and [Migrating from v4 to v5](guides/administration/migrating-from-v4.md) for the one-shot data migration procedure.

## Community

Dependency-Track is an open source project maintained by a community of contributors.
Join the [monthly community meeting](https://github.com/DependencyTrack/community#community-meetings)
to hear project updates, ask questions, and meet other users and maintainers.
