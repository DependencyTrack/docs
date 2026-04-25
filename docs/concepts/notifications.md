# About notifications

## Introduction

Dependency-Track includes a robust and configurable notification framework,
capable of alerting users or systems about the occurrences of various events
in the platform.

## Alerts

Alerts, a.k.a. *notification rules*, are configurations that specify which notifications
are sent to which destinations. An alert defines the scope, groups, and level of notifications
it is interested in, and optionally restricts matching to specific projects or tags.

Alerts can further be refined with a *filter expression*, written in [CEL], that evaluates
against the content of each notification. This allows filtering by properties such as
vulnerability severity, CVSS score, or component name, without requiring dedicated UI controls
for each filter criterion. Refer to [Filter expressions](../reference/notifications/filter-expressions.md)
for details.

## Publishers

Publishers are software components that send notifications emitted by the platform
to a destination system. Dependency-Track supports multiple publishers, ranging from
email to Webhook. Refer to [Publishers](../reference/notifications/publishers.md) for details.

## Templates

Templates define how the platform-internal representation of notifications
(see [Notification schema](../reference/schemas/notification.md)) is transformed
to match the expectation of notification recipients.

While each [publisher](#publishers) ships with a default template, administrators
can also configure custom templates.

## Levels

Notifications can have one of three possible levels:

* Informational
* Warning
* Error

These levels behave similar to logging levels, in that they allow [alerts](#alerts)
to define the verbosity of notifications being sent:

* Configuring an alert for level *Informational* will match notifications of level *Informational*, *Warning*, and *Error*.
* Configuring an alert for level *Warning* will match notifications of level *Warning* and *Error*.
* Configuring an alert for level *Error* will only match notifications of level *Error*.

## Scopes

Notifications are emitted for different *scopes*. A scope broadly categorises the *subject*
of a notification.

* **SYSTEM**: Informs about system-level events, such as users being created, or integrations failing.
* **PORTFOLIO**: Informs about portfolio-level events, such as BOM uploads, or newly identified vulnerabilities.

## Groups

A group is a granular classification of notification subjects within a [scope](#scopes).
For example, the `NEW_VULNERABILITY` group within the `PORTFOLIO` scope identifies notifications
emitted whenever a new vulnerability is found.

Refer to [Notification groups](../reference/notifications/groups.md) for the full list
of groups, their scopes, levels, and triggers.

## Triggers

Notifications are produced via one of two triggers:

| Trigger  | Description                                                 |
|:---------|:------------------------------------------------------------|
| Event    | An event is emitted by the system under certain conditions. |
| Schedule | The notification is sent based on a planned schedule.       |

* Notifications triggered by events are ideal for near real-time automation,
  and integrations into chat platforms.
* Notifications triggered on a schedule are typically used to communicate high-level summaries,
  and are thus a better fit for reporting purposes.

Each [group](#groups) supports exactly one trigger type. Most groups are event-triggered;
the summary groups (`NEW_VULNERABILITIES_SUMMARY`, `NEW_POLICY_VIOLATIONS_SUMMARY`)
are schedule-triggered.

[CEL]: https://cel.dev/
