# Briefing

What the software does, who uses it, and what problems it solves.

## What is Dependency-Track?

Dependency-Track is an open-source platform for software supply chain risk management. It ingests Bills of Materials (BOMs) in CycloneDX format, continuously monitors components for known vulnerabilities, and enforces organizational policies across an application portfolio.

It is API-first, designed for CI/CD integration, and language/ecosystem-agnostic. Rather than scanning source code or binaries directly, it operates on BOMs — making it complementary to, not a replacement for, traditional SCA tools.

## What problems does it solve?

- **Component visibility**: organizations lack a centralized inventory of what software components are in use across their portfolio.
- **Vulnerability tracking at scale**: identifying which projects are affected when a new vulnerability is disclosed (impact analysis).
- **Policy enforcement**: automating compliance checks for license risk, security severity thresholds, and operational rules (e.g., outdated components, component integrity).
- **Supply chain transparency**: meeting regulatory requirements (e.g., U.S. Executive Order 14028) for BOM production, consumption, and risk assessment.
- **Vendor risk assessment**: evaluating third-party software by ingesting vendor-provided BOMs.
- **Audit and triage workflow**: tracking analysis decisions (exploitable, false positive, mitigated, etc.) with full audit history.

## Who uses it?

- **Security teams** — vulnerability management, risk scoring, portfolio-wide impact analysis.
- **DevOps / platform engineers** — CI/CD integration, BOM upload automation, notification routing.
- **Development teams** — reviewing findings, triaging vulnerabilities, understanding dependency risk.
- **Compliance / governance teams** — license compliance, policy enforcement, regulatory reporting.
- **Procurement teams** — vendor risk assessment via SBOM analysis.

## Key capabilities

- **BOM ingestion and management**: consumes CycloneDX BOMs; tracks components, dependencies, and provenance across the entire portfolio.
- **Multi-source vulnerability intelligence**: aggregates data from NVD, GitHub Advisories, OSV, Sonatype OSS Index, Snyk, Trivy, VulnDB, and an internal vulnerability database.
- **Policy engine**: CEL-based rules for security, license, and operational policies. Supports auto-triage of findings via vulnerability policies.
- **VEX support**: consumes and produces CycloneDX Vulnerability Exploitability Exchange documents.
- **Notifications**: Slack, Teams, Mattermost, email, Jira, webhooks. Supports CEL-based filter expressions for fine-grained routing.
- **Integrations**: Jenkins plugin, GitHub Actions, DefectDojo, Fortify SSC, Kenna Security, and others. REST API with OpenAPI spec for custom integrations.
- **Portfolio metrics**: weighted risk scoring, inherited risk via project hierarchies, trending over time.

## Architecture (v5)

Version 5 (codename "Hyades") is a ground-up rearchitecture of the backend:

- **PostgreSQL-only**: single database dependency, no external message brokers.
- **Durable execution engine ("dex")**: PostgreSQL-backed workflow orchestration replacing the v4 in-memory event system. All background work (BOM processing, vulnerability analysis, notifications) survives restarts and crashes.
- **Horizontally scalable**: multiple instances coordinate via database. Supports web/worker separation for independent scaling of API traffic and background processing.
- **API server + frontend**: the API server (Java/Jetty) exposes the REST API and runs background workflows. The frontend is a separate Vue.js SPA.

### Tech stack

- Java 21, Jetty, Jakarta REST (Jersey), DataNucleus (JDO), Flyway, Protocol Buffers.
- PostgreSQL as the sole external dependency.
- Google CEL for policy evaluation and notification filtering.
