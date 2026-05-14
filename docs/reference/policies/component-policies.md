# Component policies

Field-level reference for component policies. See
[About component policies](../../concepts/component-policies.md) for background and
[Managing component policies](../../guides/user/managing-component-policies.md) for procedures.

## Operator

| Operator | Behavior                                                                                   |
|:---------|:-------------------------------------------------------------------------------------------|
| `ANY`    | Raises a violation when at least one condition matches the component. Default.             |
| `ALL`    | Raises a violation only when every condition matches the component.                        |

## Violation states

Every violation the policy raises inherits the policy's state. The state drives badges, project
metrics, notifications, and CI/CD gating.

| State  | Typical use                                                                                |
|:-------|:-------------------------------------------------------------------------------------------|
| `INFO` | Informational. Surfaces the violation without affecting the project's pass/fail status.    |
| `WARN` | Warning. Visible in metrics and notifications.                                             |
| `FAIL` | Failure. Consumed by the project badge and REST API to gate CI/CD checks.                  |

## Condition subjects

Each condition has a `subject`, an `operator`, and a `value`. The subject determines the
[violation type](#violation-types) and which operators apply.

`NUMERIC_*` below covers `NUMERIC_GREATER_THAN`, `NUMERIC_LESS_THAN`, `NUMERIC_EQUAL`,
`NUMERIC_NOT_EQUAL`, `NUMERIC_GREATER_THAN_OR_EQUAL`, and `NUMERIC_LESSER_THAN_OR_EQUAL`.

!!! note "Asynchronously populated data"
    Inputs to [`AGE`](#age), [`VERSION_DISTANCE`](#version_distance), [`EPSS`](#epss), and
    [`EXPRESSION`](#expression) conditions that read the same data may not yet exist on the first
    evaluation after a BOM upload. See
    [About component policies](../../concepts/component-policies.md#lifecycle).

### `AGE`

- **Violation type:** Operational
- **Operators:** `NUMERIC_*`
- **Value:** ISO 8601 duration (for example, `P30D`, `P1Y`).

Compares against the component's publication date.

### `COMPONENT_HASH`

- **Violation type:** Operational
- **Operators:** algorithm selector (the operator field carries the hash algorithm)
- **Value:** JSON `{ "algorithm": "<alg>", "value": "<hash>" }`.

Supported algorithms: `MD5`, `SHA-1`, `SHA-256`/`384`/`512`, `SHA3-256`/`384`/`512`,
`BLAKE2b-256`/`384`/`512`, `BLAKE3`.

### `COORDINATES`

- **Violation type:** Operational
- **Operators:** `MATCHES`, `NO_MATCH`
- **Value:** JSON `{ "group": "<re>", "name": "<re>", "version": "<re>" }`.

Each field is a regular expression over the corresponding component coordinate.

### `CPE`

- **Violation type:** Security
- **Operators:** `MATCHES`, `NO_MATCH`
- **Value:** Regular expression over the component's CPE string.

### `CWE`

- **Violation type:** Security
- **Operators:** `CONTAINS_ANY`, `CONTAINS_ALL`
- **Value:** Comma-separated CWE IDs (for example, `CWE-79, CWE-89`).

Matched against the CWEs of the component's vulnerabilities.

### `EPSS`

- **Violation type:** Security
- **Operators:** `NUMERIC_*`
- **Value:** Numeric value between `0.0` and `1.0`.

Matched against the highest EPSS score among the component's vulnerabilities.

### `EXPRESSION`

- **Violation type:** chosen explicitly on the condition (`LICENSE`, `OPERATIONAL`, or `SECURITY`)
- **Operators:** n/a
- **Value:** A [CEL](../cel-expressions.md) expression evaluated for every component in scope. The
  condition matches when the expression evaluates to `true`.

See [Condition expressions](condition-expressions.md) for the available variables, custom
functions (including [`spdx_expr_allows`](condition-expressions.md#spdx_expr_allows),
[`is_dependency_of`](condition-expressions.md#is_dependency_of),
[`matches_range`](condition-expressions.md#matches_range), and
[`version_distance`](condition-expressions.md#version_distance)), and worked examples.

### `LICENSE`

- **Violation type:** License
- **Operators:** `IS`, `IS_NOT`
- **Value:** License UUID, or the literal `unresolved` to match components without a resolved
  license.

### `LICENSE_GROUP`

- **Violation type:** License
- **Operators:** `IS`, `IS_NOT`
- **Value:** License group UUID.

### `PACKAGE_URL`

- **Violation type:** Operational
- **Operators:** `MATCHES`, `NO_MATCH`
- **Value:** Regular expression over the component's package URL (PURL).

### `SEVERITY`

- **Violation type:** Security
- **Operators:** `IS`, `IS_NOT`
- **Value:** One of `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`, `UNASSIGNED`.

Matched against the severity of the component's vulnerabilities.

### `SWID_TAGID`

- **Violation type:** Operational
- **Operators:** `MATCHES`, `NO_MATCH`
- **Value:** Regular expression over the component's SWID Tag ID.

### `VERSION`

- **Violation type:** Operational
- **Operators:** `NUMERIC_*`
- **Value:** Version string. Compared using ecosystem-aware version semantics.

### `VERSION_DISTANCE`

- **Violation type:** Operational
- **Operators:** `NUMERIC_*`
- **Value:** JSON [`VersionDistance`](../schemas/policy.md#versiondistance):
  `{ "epoch": n, "major": n, "minor": n, "patch": n }`.

### `VULNERABILITY_ID`

- **Violation type:** Security
- **Operators:** `IS`, `IS_NOT`
- **Value:** Vulnerability identifier (for example, `CVE-2021-44228`).

## Violation types

A condition's subject determines the violation type recorded when the condition matches.

| Type          | Subjects                                                                                              |
|:--------------|:------------------------------------------------------------------------------------------------------|
| `LICENSE`     | [`LICENSE`](#license), [`LICENSE_GROUP`](#license_group)                                              |
| `OPERATIONAL` | [`AGE`](#age), [`COMPONENT_HASH`](#component_hash), [`COORDINATES`](#coordinates), [`PACKAGE_URL`](#package_url), [`SWID_TAGID`](#swid_tagid), [`VERSION`](#version), [`VERSION_DISTANCE`](#version_distance) |
| `SECURITY`    | [`CPE`](#cpe), [`CWE`](#cwe), [`EPSS`](#epss), [`SEVERITY`](#severity), [`VULNERABILITY_ID`](#vulnerability_id) |
| (explicit)    | [`EXPRESSION`](#expression) (the condition itself names the violation type).                          |

## Assignment

A policy is in scope for a project when any of the following holds:

- The policy has neither projects nor tags assigned. It applies to the entire portfolio.
- The project appears in the policy's `projects` list, or descends from a listed project that has
  `includeChildren` enabled.
- The project carries a tag listed in the policy's `tags`.

## Evaluation

Project analysis evaluates policies on BOM upload, during the scheduled portfolio analysis, and on
a manual trigger. See [About component policies](../../concepts/component-policies.md#lifecycle)
for the reconciliation model.

## Permissions

The relevant permissions are `POLICY_MANAGEMENT` (and the finer-grained `_CREATE`, `_READ`,
`_UPDATE`, `_DELETE` variants) for editing policies, `VIEW_POLICY_VIOLATION` for reading
violations, and `POLICY_VIOLATION_ANALYSIS` for triaging them. See the
[permissions reference](../permissions.md) for the full list.
