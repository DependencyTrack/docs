# Reference

Reference documentation describes Dependency-Track's technical interfaces,
configuration properties, and data schemas. It is designed to be consulted
rather than read from start to finish.

For step-by-step instructions, see [Guides](../guides/index.md).
For background and explanations, see [Concepts](../concepts/index.md).

## API

- [REST API v1](api/v1.md)
- [REST API v2](api/v2.md)

## Configuration

- [Application](configuration/application.md) --
  general application settings and MicroProfile Config sources
- [Data Sources](configuration/datasources.md) --
  database connection and pool configuration
- [File Storage](configuration/file-storage.md) --
  local and S3-compatible storage providers
- [Database](configuration/database.md) --
  PostgreSQL requirements, extensions, and tuning parameters
- [All Properties](configuration/properties.md) --
  complete generated registry of all application properties

## Notifications

- [Publishers](notifications/publishers.md) --
  email, Jira, Kafka, Webhook, and other publisher options
- [Filter Expressions](notifications/filter-expressions.md) --
  CEL-based notification filtering

## Datasources

- [NVD](datasources/nvd.md) --
  National Vulnerability Database mirroring and CPE matching
- [GitHub Advisories](datasources/github-advisories.md) --
  GHSA mirroring via GitHub's GraphQL API
- [OSV](datasources/osv.md) --
  Open Source Vulnerabilities mirroring, selectable by ecosystem
- [Private Vulnerability Repository](datasources/private-vulnerability-repository.md) --
  internally managed vulnerabilities for proprietary components
- [Repositories](datasources/repositories.md) --
  package registries for outdated component detection
- [Internal Components](datasources/internal-components.md) --
  excluding first-party components from external analysis

## Expressions and Schemas

- [CEL Expressions](cel-expressions.md) --
  syntax reference for CEL used in policies and notifications
- [Vulnerability Analyzers](analyzers.md)
- [Vulnerability Policies](vulnerability-policies.md)
- [Notification Schema](schemas/notification.md)
- [Policy Schema](schemas/policy.md)

## Access Control and Integrations

- [Permissions](permissions.md) --
  users, teams, API keys, and the full permissions table
- [Badges](badges.md) --
  SVG badges for embedding vulnerability and policy metrics
- [File Formats](file-formats.md) --
  CycloneDX BOM/VEX/VDR and Finding Packaging Format (FPF)
- [Community Integrations](community-integrations.md) --
  third-party tools and libraries built on the Dependency-Track API
