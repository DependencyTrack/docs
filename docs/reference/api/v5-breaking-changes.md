# Breaking changes in v5

This page enumerates the breaking changes to REST API v1 between Dependency-Track v4 and v5. REST API v2 is new in v5
and out of scope.

The current [v1 OpenAPI spec](v1.md) is the authoritative source. The [removed endpoints](#removed-endpoints) table and
cross-cutting sections cover the changes most clients hit. The per-resource sections list everything else for lookup.

## What's most likely to break your client

Quick triage. Each item links to the section with the full detail.

- **Endpoints your client calls may no longer exist.** Check the [removed endpoints](#removed-endpoints) table.
- **List endpoints now cap at 100 results by default.** Pagination applies to team, finding, and per-vulnerability
  project listings. See the [Team](#team-resource), [Finding](#finding-resource), and
  [Vulnerability](#vulnerability-resource) sections.
- **Authentication contract changed on badge endpoints.** v5 accepts unauthenticated requests, `401` no longer signals
  bad credentials. See [Badge resource](#badge-resource).
- **New `403` responses on project-association endpoints.** Strict status-code matching fails. See
  [Policy](#policy-resource) and [Notification rule](#notification-rule-resource).
- **Request body shape and required fields changed** on these resources: [Repository](#repository-resource),
  [Notification publisher](#notification-publisher-resource), [Notification rule](#notification-rule-resource), and
  [Tag](#tag-resource).

## Removed endpoints

v5 removes the `/v1/search/*` and `/v1/integration/osv/*` resources entirely, plus the individual endpoints below.

| Method | Path                                                 | Replacement                                                                           |
|:-------|:-----------------------------------------------------|:--------------------------------------------------------------------------------------|
| GET    | `/v1/search`                                         | None. v5 removes the Lucene-backed search index. v5 has no fuzzy-matching capability. |
| GET    | `/v1/search/component`                               | None.                                                                                 |
| GET    | `/v1/search/license`                                 | None.                                                                                 |
| GET    | `/v1/search/project`                                 | None.                                                                                 |
| POST   | `/v1/search/reindex`                                 | None. The search index no longer needs rebuilding.                                    |
| GET    | `/v1/search/service`                                 | None.                                                                                 |
| GET    | `/v1/search/vulnerability`                           | None.                                                                                 |
| GET    | `/v1/search/vulnerablesoftware`                      | None.                                                                                 |
| GET    | `/v1/integration/osv/ecosystem`                      | None.                                                                                 |
| GET    | `/v1/integration/osv/ecosystem/inactive`             | None.                                                                                 |
| POST   | `/v1/notification/publisher/restoreDefaultTemplates` | None.                                                                                 |
| POST   | `/v1/notification/publisher/test/smtp`               | `POST /v2/extension-points/notification.publisher/extensions/email/test`              |
| POST   | `/v1/policy/{policyUuid}/tag/{tagName}`              | `POST /v1/tag/{name}/policy`                                                          |
| DELETE | `/v1/policy/{policyUuid}/tag/{tagName}`              | `DELETE /v1/tag/{name}/policy`                                                        |
| GET    | `/v1/tag/{policyUuid}`                               | `GET /v1/tag/policy/{uuid}`                                                           |

## Cross-cutting changes

These hit many endpoints. They're documented once here to avoid repetition in the per-resource sections.

- **`propertyType` enum lost `ENCRYPTEDSTRING`.** Applies to `ConfigProperty.propertyType`,
  `ProjectProperty.propertyType`, and `ComponentProperty.propertyType`.
- **`Project.classifier` and `Project.collectionLogic` lost `NONE`.** Applies to every endpoint returning `Project`,
  including nested occurrences.
- **`ProjectMetrics.collectionLogic` and `collectionLogicChanged` removed.** Applies to every endpoint returning
  `ProjectMetrics`.
- **`Permission` enum lost `VIEW_BADGES`.** Affects `GET /v1/permission` and any field carrying a permission value.
- **`AffectedVersionAttribution`** (nested in `Vulnerability.affectedComponents[]`) lost the `uuid` field.
- **`VulnerabilityAlias.uuid` removed** from all vulnerability responses.

### Additive permission changes

v5 introduces per-action permissions (for example, `POLICY_MANAGEMENT_READ`, `SYSTEM_CONFIGURATION_UPDATE`,
`VULNERABILITY_ANALYSIS_READ`) alongside the v4 coarse-grained permission. Existing tokens with the v4 permission still
work, so these additions don't break clients. See [Permissions](../permissions.md) for the full list.

## Per-resource changes

Resource sections appear in alphabetical order. Within each section, endpoint paths appear in bold at the start of each
change group.

### Badge resource

**All four badge endpoints (`/v1/badge/vulns/...`, `/v1/badge/violations/...`)**

- **Auth no longer required**: badge endpoints accept unauthenticated requests in v5. Clients that relied on `401` to
  detect missing or bad credentials no longer receive it. Badge support remains turned off by default, and admins must
  explicitly enable unauthenticated access.
- **Status code change**: `401` no longer returned. `403` means the administrator turned badges off, not that the
  credential is wrong. Do not retry with different credentials on `403`.

!!! note
    v4.12.0 introduced auth for badge access. Because badges typically embed in documents such as `README`s, the
    standard `Authorization` header doesn't work there. To compensate, `/v1/badge` endpoints accepted API keys through
    a URL query parameter, with the expectation that an API key holding only the `VIEW_BADGES` permission made this
    safe. In practice the design exposed API keys in logs and referrer headers, so v5 drops it.

### BOM resource

**`GET /v1/bom/cyclonedx/project/{uuid}`**

- **Permission tightened**: v4 required only `VIEW_PORTFOLIO` for all variants. v5 additionally requires one of
  `VIEW_VULNERABILITY`, `VULNERABILITY_ANALYSIS`, or `VULNERABILITY_ANALYSIS_READ` when `variant=withVulnerabilities`
  or `variant=vdr`.

### Calculator resource

**`GET /v1/calculator/cvss`**

- **Response field omission**: v4 returned all six score fields (`baseScore`, `impactSubScore`,
  `exploitabilitySubScore`, `temporalScore`, `environmentalScore`, `modifiedImpactSubScore`) as primitives, even when
  inapplicable (`NaN`). v5 omits fields that don't apply for the given vector. Clients must handle missing keys rather
  than assume `NaN`.

### Component resource

**`GET /v1/component/project/{uuid}`, `PUT /v1/component/project/{uuid}`, `POST /v1/component`, `GET /v1/component/{uuid}`**

- **Enum value removed**: `Component.classifier.NONE`. `null` or an absent field means what `NONE` meant in v4.
- **Removed field**: nested `RepositoryMetaComponent.published` -> `latestVersionPublishedAt`.
- **Required-field contract loosened**: `RepositoryMetaComponent` no longer declares `lastCheck`, `latestVersion`,
  `name`, or `repositoryType` as required. Clients can no longer assume their presence.

### Component property resource

**All endpoints under `/v1/component/{uuid}/property`**

- **Enum value removed**: `ComponentProperty.propertyType.ENCRYPTEDSTRING`.

### Config property resource

**All endpoints under `/v1/configProperty`**

- **Enum value removed**: `ConfigProperty.propertyType.ENCRYPTEDSTRING`.

### Finding resource

**All endpoints returning `Finding`**

- **`vulnerability.cwes` shape changed**: v4 returned an array of CWE integer IDs (for example `[80, 666]`). v5 returns
  an array of CWE objects with `cweId` and `name` fields (for example `[{"cweId": 80, "name": "..."}, ...]`). The SARIF
  output emitted by these endpoints carries the same change: v4 serialized `cwes` as a quoted string of the underlying
  list, v5 emits a proper JSON array of `{cweId, name}` objects.

**`POST /v1/finding/project/{uuid}/analyze`**

- **Permission tightened**: required permission changed `VIEW_VULNERABILITY` -> `VULNERABILITY_ANALYSIS`.

**`GET /v1/finding/project/{uuid}`**

- **Pagination now honored**: v4 exposed `pageNumber`/`pageSize` but the underlying SQL ignored them, the response
  always contained every matching row. v5 applies the parameters. Callers that relied on receiving the full result set
  in one response now silently truncate at `pageSize=100` by default.

**`GET /v1/finding` and `GET /v1/finding/grouped`**

- **Pagination now honored**: same change as `GET /v1/finding/project/{uuid}`. v4 accepted `pageNumber` and `pageSize`
  but ignored them, v5 applies them.

### Metrics resource

**`GET /v1/metrics/project/{uuid}/current`, `/since/{date}`, `/days/{days}`**

- **Removed response fields**: `ProjectMetrics.collectionLogic`, `collectionLogicChanged`.

### Notification publisher resource

v5 removes `POST /v1/notification/publisher/restoreDefaultTemplates` and `POST /v1/notification/publisher/test/smtp`.
See the [removed-endpoints table](#removed-endpoints).

**`PUT /v1/notification/publisher`**

- **Request body schema changed**: v4 accepted full `NotificationPublisher`. v5 uses
  `CreateNotificationPublisherRequest`.
- **Renamed and required field**: `publisherClass` -> `extensionName` (required). `extensionName` must refer to a name
  listed under `GET /v2/extension-points/notification.publisher/extensions`.
- **Removed request fields**: `defaultPublisher` and `uuid` no longer accepted (v4 never used them). `templateMimeType`
  no longer required on create.

**`POST /v1/notification/publisher`**

- **Request body schema changed**: v4 accepted full `NotificationPublisher`. v5 uses
  `UpdateNotificationPublisherRequest`.
- **Renamed and required field**: `publisherClass` -> `extensionName` (required). `extensionName` must refer to a name
  listed under `GET /v2/extension-points/notification.publisher/extensions`.

**`NotificationPublisher` response schema**

- **Renamed field**: `publisherClass` -> `extensionName`.

### Notification rule resource

**`PUT /v1/notification/rule`**

- **Request body schema changed**: v4 accepted full `NotificationRule`. v5 uses `CreateNotificationRuleRequest`.
- **Renamed field**: `notificationLevel` -> `level`.
- **New mandatory request field**: `publisher` (UUID wrapper) is now required.
- **Removed request fields**: `triggerType` and `uuid` no longer accepted (server-assigned).

**`POST /v1/notification/rule`**

- **Request body schema changed**: v4 accepted full `NotificationRule`. v5 uses `UpdateNotificationRuleRequest`.
- **Renamed field**: `notificationLevel` -> `level`.
- **New mandatory request fields**: `level` and `scope` now required.
- **Removed request fields**: `triggerType`, `projects`, `teams`, `tags`, `publisher`, `publisherConfig`, and schedule
  fields no longer in the update body (managed through dedicated sub-endpoints).

**`NotificationRule` response schema**

- **Enum value removed**: `notifyOn.INDEXING_SERVICE`.

**`POST /v1/notification/rule/{ruleUuid}/project/{projectUuid}`, `DELETE /v1/notification/rule/{ruleUuid}/project/{projectUuid}`**

- **New response status**: `403 Forbidden` (project access denied).

### Permission resource

**`GET /v1/permission`**

- **Enum value removed**: `Permission.VIEW_BADGES`.

### Policy resource

**`POST /v1/policy/{policyUuid}/project/{projectUuid}`, `DELETE /v1/policy/{policyUuid}/project/{projectUuid}`**

- **New response status**: `403 Forbidden` (project access denied). Strict clients that match only v4 codes see
  undocumented errors.

v5 removes the `POST` and `DELETE` variants of `/v1/policy/{policyUuid}/tag/{tagName}`. See the
[removed endpoints](#removed-endpoints) table.

### Project resource

**`PUT /v1/project`, `POST /v1/project`, `GET /v1/project/{uuid}`, `PATCH /v1/project/{uuid}`**

- **Removed response field**: `Project.properties` inline array. Fetch project properties via
  `GET /v1/project/{uuid}/property` instead.
- **Enum values removed**: `Project.classifier.NONE`, `Project.collectionLogic.NONE`. `null` or an absent field means
  what `NONE` meant in v4.

**`GET /v1/project`**

- **Removed response field**: `Project.children` inline array. Fetch project children via
  `GET /v1/project/{uuid}/children` instead.

**`POST /v1/project/batchDelete`**

- **Removed response**: v4 documented a `400` with `ProjectOperationProblemDetails`. v5 documents only `204` and `401`.

### Project property resource

**All endpoints under `/v1/project/{uuid}/property`**

- **Enum value removed**: `ProjectProperty.propertyType.ENCRYPTEDSTRING`.

### Repository resource

**`GET /v1/repository/latest`**

- **Renamed response field**: `RepositoryMetaComponent.published` -> `latestVersionPublishedAt`.
- **Required-field contract loosened**: `lastCheck`, `latestVersion`, `name`, `published`, and `repositoryType`,
  required in v4, are now all optional in the response schema.

**`PUT /v1/repository`, `POST /v1/repository`**

- **New mandatory request field**: `Repository.authenticationRequired`.

### Tag resource

v5 removes `GET /v1/tag/{policyUuid}` in favor of `GET /v1/tag/policy/{uuid}`. See the
[removed-endpoints table](#removed-endpoints).

### Team resource

**`GET /v1/team`**

- **Pagination introduced**: v4 had no pagination parameters. v5 adds `pageNumber`, `pageSize`, `offset`, `limit`,
  `sortName`, and `sortOrder` with default `pageSize=100`. Naive callers silently drop teams beyond the first 100.

### Vulnerability resource

**All endpoints returning `Vulnerability`**

- **Removed response fields**: `findingAttribution` and `normalizedCvssV2Vector` removed without replacement. `cwe`
  (singular) removed, use the `cwes` array instead (a single CWE appears as a one-element array).
- Nested `VulnerabilityAlias.uuid` removed. Nested `AffectedVersionAttribution.uuid` removed.

**`GET /v1/vulnerability/source/{source}/vuln/{vuln}/projects`**

- **Pagination introduced**: v4 returned an unbounded list. v5 caps at `pageSize=100` by default and exposes
  `pageNumber`, `pageSize`, `sortName`, and `sortOrder`. Naive callers silently drop projects beyond the first 100.
- **Response type changed**: v4 returned `Project[]` (full schema). v5 returns `AffectedProject[]`, a slim DTO
  containing only `active`, `affectedComponentUuids`, `dependencyGraphAvailable`, `name`, `uuid`, and `version`. v5
  drops all other `Project` fields.
- **Status code removed**: v4 returned `404` for an unknown vulnerability. v5 returns `200` with an empty list.
