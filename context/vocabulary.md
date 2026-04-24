# Vocabulary

Precise definitions of domain terms used in the software and its documentation.
Use these terms consistently. Avoid synonyms not listed here.

## Core domain model

- **project** — A tracked software deliverable (application, service, library, container image, firmware). Identified by name, version, and classifier. Projects can form hierarchies via parent-child relationships.
- **component** — A software or hardware unit described in a BOM. Component types include: *application*, *framework*, *library*, *container*, *platform*, *operating-system*, *device*, *device-driver*, *firmware*, *file*, *machine-learning-model*, *data*, and *cryptographic-asset*.
- **service** — A network or intra-process service described in a BOM. Includes microservices, function-as-a-service, and other service types. Characterized by endpoints, trust boundaries, and data flows. Distinct from component.
- **portfolio** — The set of all projects in a Dependency-Track instance. Used as a collective noun, not a discrete entity.
- **finding** — The association between a component and a vulnerability. Carries analysis state, suppression status, and audit trail.

## Vulnerability and analysis

- **vulnerability** — A known security defect, identified by CVE, GHSA, or internal ID. Sourced from one or more data sources.
- **vulnerability analysis** — The automated process of matching components against vulnerability databases. Runs on BOM upload and on mirror updates. Not to be confused with manual triage.
- **analyzer** — A pluggable module that matches components against a specific vulnerability data source (e.g., NVD, OSV, Snyk, Trivy).
- **data source** — An upstream vulnerability feed (NVD, GitHub Advisories, OSV, Sonatype OSS Index, Snyk, Trivy, VulnDB). Prefer "data source" over "feed" or "database" when referring to these.
- **mirroring** — Scheduled download and local storage of a vulnerability data source.
- **alias** — A cross-database identifier mapping (e.g., CVE-2021-44228 = GHSA-jfh8-c2jp-5v3q). Enables deduplication across data sources.
- **analysis state** — Triage status of a finding: *Not Set*, *Exploitable*, *In Triage*, *False Positive*, *Not Affected*, *Resolved*.
- **justification** — Required when analysis state is *Not Affected*. Values: *Code Not Present*, *Code Not Reachable*, *Requires Configuration*, *Requires Dependency*, *Requires Environment*, *Protected by Compiler*, *Protected by Mitigating Control*.
- **suppression** — Hides a finding from metrics while preserving its audit trail. Persists until explicitly removed.
- **impact analysis** — Portfolio-wide query: "which projects are affected by this vulnerability or component?"

## Scoring

- **CVSS** (Common Vulnerability Scoring System) — Base score and vector for vulnerability severity.
- **EPSS** (Exploit Prediction Scoring System) — Probability and percentile of real-world exploitation.
- **severity** — Classification derived from CVSS or other scoring: *Critical*, *High*, *Medium*, *Low*, *Unassigned*.
- **risk score** — Weighted calculation combining vulnerability counts by severity across a project or portfolio.
- **inherited risk** — Risk metrics aggregated from child projects to their parent.

## Bill of Materials

- **BOM** (Bill of Materials) — Structured inventory of components, services, and dependencies. Dependency-Track consumes CycloneDX format exclusively.
- **SBOM** (Software Bill of Materials) — A BOM specifically describing software composition. Use "BOM" when the context is generic; use "SBOM" when emphasizing the software supply chain context.
- **CycloneDX** — Lightweight, security-focused BOM specification (ECMA-424). The only BOM format Dependency-Track supports.
- **VEX** (Vulnerability Exploitability eXchange) — CycloneDX document conveying analysis decisions about whether vulnerabilities are exploitable in a given context.
- **VDR** (Vulnerability Disclosure Report) — CycloneDX document listing all known vulnerabilities for a project's components.
- **BOV** (Bill of Vulnerabilities) — CycloneDX export containing vulnerability data.
- **BOM processing** — The pipeline triggered on BOM upload: parsing, component reconciliation, vulnerability analysis, policy evaluation, and notification dispatch.

## Identifiers

- **PURL** (Package URL) — Ecosystem-specific package identifier (e.g., `pkg:maven/org.apache/commons-lang3@3.12.0`). Primary identifier for vulnerability matching.
- **CPE** (Common Platform Enumeration) — Structured naming scheme for products. Used primarily for NVD matching.
- **SWID** (Software Identification) — Tag-based identifier. Rarely used in practice.

## Policy engine

- **policy** — A declarative rule evaluated against components, findings, or projects. Enforces license, security, or operational standards.
- **policy condition** — A single predicate within a policy (e.g., "severity >= HIGH", "license in Copyleft group").
- **policy violation** — Raised when a component matches a policy condition.
- **violation state** — *Inform* (visible, non-blocking) or *Fail* (blocks CI/CD gates).
- **vulnerability policy** — A rule that automatically applies triage decisions (analysis state, suppression, severity override) to findings matching a CEL condition. Distinct from standard policies.
- **license group** — A named collection of licenses (e.g., Copyleft, Permissive) used in policy conditions.
- **CEL** (Common Expression Language) — Expression language used for vulnerability policies and notification filter expressions. Safe, non-Turing-complete.

## Notifications

- **notification** — An event emitted by the system, classified by scope, group, and level.
- **notification scope** — *System* (infrastructure events) or *Portfolio* (project/component events).
- **notification group** — Event type classification (e.g., NEW_VULNERABILITY, POLICY_VIOLATION, BOM_PROCESSED, BOM_PROCESSING_FAILED).
- **notification level** — *Informational*, *Warning*, or *Error*. Higher levels include lower.
- **alert** — A routing rule that subscribes to notification groups and delivers to a publisher. Called "notification rule" in the API; prefer "alert" in docs.
- **publisher** — Delivery mechanism: email, Slack, Teams, Mattermost, Jira, webhook.

## Access control

- **team** — A grouping of users and API keys that share permissions.
- **permission** — A granular access control attribute (e.g., VIEW_PORTFOLIO, VULNERABILITY_ANALYSIS, POLICY_MANAGEMENT).
- **API key** — A long-lived authentication token scoped to a team.
- **managed user** — A user account managed within Dependency-Track.
- **LDAP/OIDC user** — A user account managed by an external identity provider.
- **portfolio access control** — Restricts a team's visibility to a subset of projects.

## Architecture (v5)

- **Hyades** — Codename for the Dependency-Track v5 platform.
- **API server** — The Java backend exposing the REST API and running background workflows. Do not abbreviate to "apiserver" in docs (code references excepted).
- **frontend** — The Vue.js single-page application. Not "UI" or "web interface" — use "frontend" consistently.
- **durable execution engine** — PostgreSQL-backed workflow orchestration replacing v4's in-memory event system. Abbreviated "dex" in code only, not in docs.
- **workflow** — A defined sequence of steps executed by the durable execution engine (e.g., BOM processing, vulnerability analysis, notification delivery).
- **activity** — A single non-deterministic step within a workflow where I/O occurs.

## Integrations

- **repository** — A package registry (Maven Central, npm, PyPI, etc.) used for component currency checks. Not to be confused with git repositories.
- **component currency** — Detection of outdated components by comparing the version in the BOM to the latest version in the upstream repository.
- **internal component** — A component marked as internal, ensuring it is never sent to external vulnerability data sources or repositories.
- **private vulnerability repository** — Internally managed vulnerability data for proprietary components or pre-disclosure tracking.
