# Notification groups

A *group* is a granular classification of a notification's subject. Every group
belongs to one of two scopes: `SYSTEM` (platform-level events) or `PORTFOLIO`
(events about projects, components, or findings). Every group also has a single
trigger type: `Event` for ad-hoc notifications that the system emits in response
to a system event, or `Schedule` for notifications that fire periodically on a
cron schedule.

The [notification schema reference](schema.md) describes the
subject schema for each group.

!!! note "Unreleased policy update groups"

    `POLICY_VIOLATION_UPDATED` and `POLICY_VIOLATION_UPDATED_REVIEWED` are proposed in
    [API server PR #7908](https://github.com/DependencyTrack/dependency-track/pull/7908).
    No released version currently includes these groups.

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

Fires when the platform first records a policy violation. Message changes to an existing violation do not emit this group.

### `POLICY_VIOLATION_UPDATED`

- **Trigger:** Event
- **Level:** Informational

Fires when the stored message of an existing component policy violation changes.
This includes changes between a text message and no message. This group excludes approved or suppressed violations.
The violation keeps its UUID.

### `POLICY_VIOLATION_UPDATED_REVIEWED`

- **Trigger:** Event
- **Level:** Informational

Fires when the stored message of an approved or suppressed component policy violation changes.
An alert receives this group only through an explicit subscription. The review decision and violation UUID stay unchanged.
A rejected, unsuppressed violation belongs to `POLICY_VIOLATION_UPDATED` instead.

### `PROJECT_AUDIT_CHANGE`

- **Trigger:** Event
- **Level:** Informational

Fires when an analysis or suppression state changes on a project finding.

### `PROJECT_CREATED`

- **Trigger:** Event
- **Level:** Informational

Fires on creation of a new project.

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
[notification schema reference](schema.md) describes
each subject schema.

| Group                                                   | Subject type                                                                                                                                            |
|:--------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `BOM_CONSUMED`, `BOM_PROCESSED`                         | [BomConsumedOrProcessedSubject](schema.md#bomconsumedorprocessedsubject)                                                               |
| `BOM_PROCESSING_FAILED`                                 | [BomProcessingFailedSubject](schema.md#bomprocessingfailedsubject)                                                                     |
| `BOM_VALIDATION_FAILED`                                 | [BomValidationFailedSubject](schema.md#bomvalidationfailedsubject)                                                                     |
| `NEW_VULNERABILITY`                                     | [NewVulnerabilitySubject](schema.md#newvulnerabilitysubject)                                                                           |
| `NEW_VULNERABLE_DEPENDENCY`                             | [NewVulnerableDependencySubject](schema.md#newvulnerabledependencysubject)                                                             |
| `POLICY_VIOLATION`                                      | [PolicyViolationSubject](schema.md#policyviolationsubject)                                                                             |
| `POLICY_VIOLATION_UPDATED`, `POLICY_VIOLATION_UPDATED_REVIEWED` | [PolicyViolationUpdatedSubject](schema.md#policyviolationupdatedsubject) |
| `PROJECT_AUDIT_CHANGE`                                  | [VulnerabilityAnalysisDecisionChangeSubject](schema.md#vulnerabilityanalysisdecisionchangesubject) or [PolicyViolationAnalysisDecisionChangeSubject](schema.md#policyviolationanalysisdecisionchangesubject) |
| `VEX_CONSUMED`, `VEX_PROCESSED`                         | [VexConsumedOrProcessedSubject](schema.md#vexconsumedorprocessedsubject)                                                               |
| `USER_CREATED`, `USER_DELETED`                          | [UserSubject](schema.md#usersubject)                                                                                                   |
| `NEW_VULNERABILITIES_SUMMARY`                           | [NewVulnerabilitiesSummarySubject](schema.md#newvulnerabilitiessummarysubject)                                                         |
| `NEW_POLICY_VIOLATIONS_SUMMARY`                         | [NewPolicyViolationsSummarySubject](schema.md#newpolicyviolationssummarysubject)                                                       |

## Policy violation updates

Both update groups have portfolio scope, use event triggers, and have informational level.
Existing alerts gain neither subscription automatically. Scheduled summaries keep their existing behavior.
Project, tag, level, and [filter expression](filter-expressions.md) restrictions still apply.
One message change belongs to exactly one update group, even when an alert subscribes to both.

### Message change behavior

| Change | Result |
|:-------|:-------|
| A condition first matches | A new violation and a `POLICY_VIOLATION` event |
| Stored message stays the same | No update event |
| Stored message changes, with no approval or suppression | `POLICY_VIOLATION_UPDATED` |
| Stored message changes while approved or suppressed | `POLICY_VIOLATION_UPDATED_REVIEWED`, with the decision retained |
| Approval, suppression, or subscriptions change without a message change | No update event or replay of past changes |
| A condition stops matching | The existing violation disappears, without an update event |
| A violation disappears and later returns | A new UUID and a creation event |

Update events describe text changes, including removals, replacements, and wording changes while the violation still matches. They do not classify increases in risk or identify new KEV matches from arbitrary text.
A Boolean condition has no message that can change when another vulnerability starts matching. Different matches that produce equal stored messages are indistinguishable, including text truncated by the existing 1024-character limit.

### Subject fields

Both groups use [PolicyViolationUpdatedSubject](schema.md#policyviolationupdatedsubject).
The Protobuf and CEL field names differ from the lower camel case names in Protobuf JSON and Pebble templates.

| Protobuf / CEL field | JSON / Pebble field | Content |
|:---------------------|:--------------------|:--------|
| `project` | `project` | Project details |
| `component` | `component` | Component details |
| `policy_violation` | `policyViolation` | Original UUID, policy, condition, and current message when present |
| `previous_message` | `previousMessage` | Optional previous stored message |
| `current_message` | `currentMessage` | Optional current stored message |
| `changed_at` | `changedAt` | Time of the reconciliation statement on the database server |
| `analysis_state` | `analysisState` | Optional analysis state captured for a reviewed update |
| `suppressed` | `suppressed` | Optional suppression value captured for a reviewed update |

An absent message field means no message. A present empty string means empty text.
Ordinary updates omit review metadata. Reviewed updates capture both review values while assembling the event.
An absent review field means no captured value. A present `suppressed: false` means explicitly unsuppressed.
Later review decisions do not change the captured event.

### Delivery and compatibility

The message change and notification creation commit together. Delivery uses the existing notification workflow after that commit.
Retries can deliver the same notification ID more than once. Recipients can deduplicate by `notification.id`.
Permanent delivery failures keep [notification diagnostics](../../guides/administration/debugging-notifications.md). Repeating analysis with unchanged text does not create a replacement event for a failed delivery.

The new groups use Protobuf values 25 and 26 without changing existing values or subscriptions.
Consumers that subscribe to either group need support for [PolicyViolationUpdatedSubject](schema.md#policyviolationupdatedsubject).
Custom templates that only handle `GROUP_POLICY_VIOLATION` do not match update groups. See [Update notification templates](templating.md#policy-violation-updates).
