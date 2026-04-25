# Notification groups

A *group* is a granular classification of a notification's subject. Every group
belongs to one of two scopes: `SYSTEM` (platform-level events) or `PORTFOLIO`
(events about projects, components, or findings). Every group also has a single
trigger type: `Event` for ad-hoc notifications emitted in response to a system
event, or `Schedule` for notifications produced periodically by a cron schedule.

Subject schemas for each group are documented in the
[notification schema reference](../schemas/notification.md).

## SYSTEM scope

### `ANALYZER`

- **Trigger:** Event
- **Level:** Any

Generated as a result of interacting with an external source of vulnerability
intelligence.

### `CONFIGURATION`

- **Trigger:** Event
- **Level:** Any

Generated as a result of platform configuration changes or configuration errors.

### `DATASOURCE_MIRRORING`

- **Trigger:** Event
- **Level:** Any

Generated when performing mirroring of one of the supported datasources, such as
the NVD.

### `FILE_SYSTEM`

- **Trigger:** Event
- **Level:** Any

Generated as a result of a file system operation. These are typically only
generated on error conditions.

### `INTEGRATION`

- **Trigger:** Event
- **Level:** Any

Generated as a result of interacting with an external integration.

### `REPOSITORY`

- **Trigger:** Event
- **Level:** Any

Generated as a result of interacting with one of the supported repositories,
such as Maven Central, RubyGems, or npm.

### `USER_CREATED`

- **Trigger:** Event
- **Level:** Informational

Generated as a result of a user creation.

### `USER_DELETED`

- **Trigger:** Event
- **Level:** Informational

Generated as a result of a user deletion.

## PORTFOLIO scope

### `BOM_CONSUMED`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a supported BOM is ingested and identified.

### `BOM_PROCESSED`

- **Trigger:** Event
- **Level:** Informational

Generated after a supported BOM is ingested, identified, and successfully
processed.

### `BOM_PROCESSING_FAILED`

- **Trigger:** Event
- **Level:** Error

Generated whenever a BOM upload process fails.

### `BOM_VALIDATION_FAILED`

- **Trigger:** Event
- **Level:** Error

Generated whenever an invalid BOM is uploaded.

### `NEW_VULNERABILITY`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a new vulnerability is identified.

### `NEW_VULNERABLE_DEPENDENCY`

- **Trigger:** Event
- **Level:** Informational

Generated as a result of a vulnerable component becoming a dependency of a
project.

### `POLICY_VIOLATION`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a policy violation is identified.

### `PROJECT_AUDIT_CHANGE`

- **Trigger:** Event
- **Level:** Informational

Generated whenever an analysis or suppression state has changed on a finding
from a project.

### `PROJECT_CREATED`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a new project is created.

### `PROJECT_VULN_ANALYSIS_COMPLETE`

- **Trigger:** Event
- **Level:** Informational

Generated when vulnerability analysis for a project completes.

### `VEX_CONSUMED`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a VEX document is ingested.

### `VEX_PROCESSED`

- **Trigger:** Event
- **Level:** Informational

Generated after a VEX document is ingested and successfully processed.

### `VULNERABILITY_RETRACTED`

- **Trigger:** Event
- **Level:** Informational

Generated whenever a previously reported vulnerability is retracted.

### `NEW_VULNERABILITIES_SUMMARY`

- **Trigger:** Schedule
- **Level:** Informational

Summaries of new vulnerabilities identified in a set of projects.

### `NEW_POLICY_VIOLATIONS_SUMMARY`

- **Trigger:** Schedule
- **Level:** Informational

Summary of new policy violations identified in a set of projects.
