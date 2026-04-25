# Filter expressions

## Introduction

Alerts can include a filter expression to control which notifications the platform dispatches
based on their content. Filter expressions use
[CEL](../cel-expressions.md) (Common Expression Language).

Without a filter expression, an alert matches every notification that meets its scope, group,
level, and project or tag restrictions. A filter expression adds a further condition: the
platform dispatches the notification only when the expression evaluates to `true`.

See [Notification groups](groups.md) for the full list of selectable groups,
and [How alert filtering works](../../concepts/notifications.md#how-alert-filtering-works)
for the order the platform applies filters and how it handles evaluation failures.

![Filter expression field in the alert editor](../../assets/images/reference/notifications/filter-expressions/filter-expression-editor.png)

## Syntax

Filter expressions use standard [CEL syntax](../cel-expressions.md#syntax). CEL is not
[Turing-complete] and does not support constructs like `if` statements or loops. It compensates
for this with [macros] like `all`, `exists`, `exists_one`, `map`, and `filter`.

Refer to the official [language definition] for a thorough description of the syntax.

## Evaluation context

The expression evaluation context contains the following variables:

| Variable    | Type                                                         | Description                                                                            |
|:------------|:-------------------------------------------------------------|:---------------------------------------------------------------------------------------|
| `level`     | [`Level`](../../reference/schemas/notification.md#level)     | The notification level, as an integer enum value. Use named constants (see below).      |
| `scope`     | [`Scope`](../../reference/schemas/notification.md#scope)     | The notification scope, as an integer enum value. Use named constants (see below).      |
| `group`     | [`Group`](../../reference/schemas/notification.md#group)     | The notification group, as an integer enum value. Use named constants (see below).      |
| `title`     | `string`                                                     | The notification title.                                                                |
| `content`   | `string`                                                     | The notification content.                                                              |
| `timestamp` | [`google.protobuf.Timestamp`][protobuf-ts-docs]              | The notification creation time.                                                        |
| `subject`   | dynamic                                                      | The notification subject, typed according to the notification group (see below).        |

### Enum constants

The `level`, `scope`, and `group` variables hold integer values. To compare them in a readable way,
use the named constants from the [notification schema](../../reference/schemas/notification.md#enums):

```js
level == Level.LEVEL_INFORMATIONAL
```

```js
group == Group.GROUP_NEW_VULNERABILITY
```

```js
scope == Scope.SCOPE_PORTFOLIO
```

### Subject types

The `subject` variable holds the notification's subject. Its type depends on the notification
group; see [Subjects](groups.md#subjects) in the notification groups reference for the
group-to-subject mapping, and the [notification schema reference](../../reference/schemas/notification.md)
for each subject's fields.

### Available functions

Notification filters have access to the variables in the preceding table and the
[standard CEL library](../cel-expressions.md#standard-library). No further custom functions
exist for this context.

## Validation

Saving an alert validates its filter expression. If the expression contains syntax errors
or references types that do not exist, the save fails and the response reports the errors
with their exact location (line and column).

![Validation error for an invalid filter expression](../../assets/images/reference/notifications/filter-expressions/filter-expression-editor-error.png)

A filter expression has a length limit of 2048 characters.

## Examples

### Only critical and high severity vulnerabilities

The following expression matches `NEW_VULNERABILITY` notifications where the vulnerability
severity is `CRITICAL` or `HIGH`:

```js linenums="1"
subject.vulnerability.severity in ["CRITICAL", "HIGH"]
```

### Vulnerabilities with a CVSS v3 score over a threshold

```js linenums="1"
subject.vulnerability.cvss_v3 >= 7.0
```

### Notifications for projects matching a name prefix

The following expression matches notifications whose subject contains a project with a name
starting with `acme-`:

```js linenums="1"
subject.project.name.startsWith("acme-")
```

!!! tip
    For simple project-based filtering, consider using project and tag restrictions on the
    alert instead. Filter expressions are more useful for content-based conditions
    that project or tag restrictions cannot capture alone.

### Vulnerabilities with a specific CWE

The following expression matches `NEW_VULNERABILITY` notifications where the vulnerability
has CWE-79 (Cross-site Scripting) among its CWEs:

```js linenums="1"
subject.vulnerability.cwes.exists(cwe, cwe.cwe_id == 79)
```

### Combining conditions

The following expression matches `NEW_VULNERABILITY` notifications for `CRITICAL` vulnerabilities
with a network attack vector in CVSSv3:

```js linenums="1"
subject.vulnerability.severity == "CRITICAL"
  && subject.vulnerability.cvss_v3_vector.matches(".*/AV:N/.*")
```

### Scheduled alerts: only when critical vulnerabilities exist

For scheduled alerts that produce vulnerability summaries, the subject contains
an overview with vulnerability counts grouped by severity. The following expression matches
only when the reporting period contains at least one `CRITICAL` vulnerability:

```js linenums="1"
"CRITICAL" in subject.overview.new_vulnerabilities_count_by_severity
```

### Optional field checking

Use the `has()` macro to check for field presence before accessing it. See
[Optional field checking](../cel-expressions.md#optional-field-checking) in the general primer
for the rationale.

```js linenums="1"
has(subject.vulnerability.cvss_v3_vector)
  && subject.vulnerability.cvss_v3_vector.matches(".*/AV:N/.*")
```

[Turing-complete]: https://en.wikipedia.org/wiki/Turing_completeness
[language definition]: https://github.com/google/cel-spec/blob/v0.13.0/doc/langdef.md#language-definition
[macros]: https://github.com/google/cel-spec/blob/v0.13.0/doc/langdef.md#macros
[protobuf-ts-docs]: https://protobuf.dev/reference/protobuf/google.protobuf/#timestamp
