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

## Notifications

- [Publishers](notifications/publishers.md) --
  email, Jira, Kafka, Webhook, and other publisher options
- [Groups](notifications/groups.md) --
  the catalog of events Dependency-Track emits notifications for
- [Filter Expressions](notifications/filter-expressions.md) --
  CEL-based notification filtering

## Vulnerability Analysis

- [Vulnerability Analyzers](analyzers.md) --
  internal and external analyzers used to identify vulnerabilities

## Policies

- [Policies](policies/index.md) --
  overview of component and vulnerability policies
- [Component Policies](policies/component-policies.md) --
  field definitions, condition subjects, operators, and assignment
- [Vulnerability Policies](policies/vulnerability-policies.md) --
  field definitions, bundle YAML schema, and sync configuration
- [Condition Expressions](policies/condition-expressions.md) --
  inputs and custom functions for policy conditions

## CEL Expressions

- [CEL Expressions](cel-expressions.md) --
  shared CEL syntax primer used by both policies and notification filters

## Access Control

- [Permissions](permissions.md) --
  users, teams, API keys, and the full permissions table

## Integrations

- [Badges](badges.md) --
  SVG badges for embedding vulnerability and policy metrics
- [File Formats](file-formats.md) --
  CycloneDX BOM/VEX/VDR and Finding Packaging Format (FPF)
- [Community Integrations](community-integrations.md) --
  third-party tools and libraries built on the Dependency-Track API

## Schemas

- [Notification Schema](schemas/notification.md) --
  Protobuf definitions for notification subjects
- [Policy Schema](schemas/policy.md) --
  Protobuf definitions for the policy CEL evaluation context
