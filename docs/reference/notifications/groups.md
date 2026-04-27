# Notification groups

A *group* is a granular classification of a notification's subject. Every group
belongs to one of two scopes: `SYSTEM` (platform-level events) or `PORTFOLIO`
(events about projects, components, or findings). Every group also has a single
trigger type: `Event` for ad-hoc notifications that the system emits in response
to a system event, or `Schedule` for notifications that fire periodically on a
cron schedule.

The [notification schema reference](../schemas/notification.md) describes the
subject schema for each group.

## System scope

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

## Portfolio scope

### `BOM_CONSUMED`

- **Trigger:** Event
- **Level:** Informational

Fires when the platform ingests and identifies a supported BOM.

### `BOM_PROCESSED`

- **Trigger:** Event
- **Level:** Informational

Fires after the platform ingests, identifies, and successfully
processes a supported BOM.

### `BOM_PROCESSING_FAILED`

- **Trigger:** Event
- **Level:** Error

Fires when a BOM upload process fails.

### `BOM_VALIDATION_FAILED`

- **Trigger:** Event
- **Level:** Error

Fires on upload of an invalid BOM.

### `NEW_VULNERABILITY`

- **Trigger:** Event
- **Level:** Informational

Fires when the platform finds a new vulnerability.

### `NEW_VULNERABLE_DEPENDENCY`

- **Trigger:** Event
- **Level:** Informational

Fires when a vulnerable component becomes a dependency of a project.

### `POLICY_VIOLATION`

- **Trigger:** Event
- **Level:** Informational

Fires when the platform records a policy violation.

### `PROJECT_AUDIT_CHANGE`

- **Trigger:** Event
- **Level:** Informational

Fires when an analysis or suppression state changes on a project finding.

### `PROJECT_CREATED`

- **Trigger:** Event
- **Level:** Informational

Fires on creation of a new project.

### `PROJECT_VULN_ANALYSIS_COMPLETE`

- **Trigger:** Event
- **Level:** Informational

Fires when vulnerability analysis for a project completes.

### `VEX_CONSUMED`

- **Trigger:** Event
- **Level:** Informational

Fires when the platform ingests a VEX document.

### `VEX_PROCESSED`

- **Trigger:** Event
- **Level:** Informational

Fires after the platform ingests and successfully processes a VEX document.

### `VULNERABILITY_RETRACTED`

- **Trigger:** Event
- **Level:** Informational

Fires when an earlier vulnerability report rolls back.

### `NEW_VULNERABILITIES_SUMMARY`

- **Trigger:** Schedule
- **Level:** Informational

Summarizes new vulnerabilities found in a set of projects.

### `NEW_POLICY_VIOLATIONS_SUMMARY`

- **Trigger:** Schedule
- **Level:** Informational

Summarizes new policy violations found in a set of projects.

## Subjects

The typed subject of a notification depends on its group. The
[notification schema reference](../schemas/notification.md) describes
each subject schema.

| Group                                                   | Subject type                                                                                                                                            |
|:--------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `BOM_CONSUMED`, `BOM_PROCESSED`                         | [BomConsumedOrProcessedSubject](../schemas/notification.md#bomconsumedorprocessedsubject)                                                               |
| `BOM_PROCESSING_FAILED`                                 | [BomProcessingFailedSubject](../schemas/notification.md#bomprocessingfailedsubject)                                                                     |
| `BOM_VALIDATION_FAILED`                                 | [BomValidationFailedSubject](../schemas/notification.md#bomvalidationfailedsubject)                                                                     |
| `NEW_VULNERABILITY`                                     | [NewVulnerabilitySubject](../schemas/notification.md#newvulnerabilitysubject)                                                                           |
| `NEW_VULNERABLE_DEPENDENCY`                             | [NewVulnerableDependencySubject](../schemas/notification.md#newvulnerabledependencysubject)                                                             |
| `POLICY_VIOLATION`                                      | [PolicyViolationSubject](../schemas/notification.md#policyviolationsubject)                                                                             |
| `PROJECT_AUDIT_CHANGE`                                  | [VulnerabilityAnalysisDecisionChangeSubject](../schemas/notification.md#vulnerabilityanalysisdecisionchangesubject) or [PolicyViolationAnalysisDecisionChangeSubject](../schemas/notification.md#policyviolationanalysisdecisionchangesubject) |
| `PROJECT_VULN_ANALYSIS_COMPLETE`                        | [ProjectVulnAnalysisCompleteSubject](../schemas/notification.md#projectvulnanalysiscompletesubject)                                                     |
| `VEX_CONSUMED`, `VEX_PROCESSED`                         | [VexConsumedOrProcessedSubject](../schemas/notification.md#vexconsumedorprocessedsubject)                                                               |
| `USER_CREATED`, `USER_DELETED`                          | [UserSubject](../schemas/notification.md#usersubject)                                                                                                   |
| `NEW_VULNERABILITIES_SUMMARY`                           | [NewVulnerabilitiesSummarySubject](../schemas/notification.md#newvulnerabilitiessummarysubject)                                                         |
| `NEW_POLICY_VIOLATIONS_SUMMARY`                         | [NewPolicyViolationsSummarySubject](../schemas/notification.md#newpolicyviolationssummarysubject)                                                       |
