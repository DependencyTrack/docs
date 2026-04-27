# About notifications

## Introduction

Dependency-Track includes a configurable notification framework
that alerts users and external systems about events in the platform.

## Alerts

Alerts, or *notification rules*, are configurations that specify which notifications
go to which destinations. An alert defines the scope, groups, and level of notifications
it subscribes to, and optionally restricts matching to specific projects or tags.

A *filter expression*, written in [CEL], can refine an alert further. The expression evaluates
against the content of each notification, which lets you filter by properties such as
vulnerability severity, CVSS score, or component name without dedicated UI controls
for each filter criterion. Refer to [Filter expressions](../reference/notifications/filter-expressions.md)
for details.

## Publishers

Publishers are software components that deliver notifications emitted by the platform
to a destination system. Dependency-Track ships a range of publishers, from
email to Webhook. Refer to [Publishers](../reference/notifications/publishers.md) for details.

## Templates

Templates define how the platform's internal representation of notifications
(see [Notification schema](../reference/schemas/notification.md)) maps
to the format that notification recipients expect.

Each [publisher](#publishers) ships with a default template, and administrators
can configure custom templates. Refer to
[Templating](../reference/notifications/templating.md) for the variables and
filters available to templates.

## Levels

Notifications can have one of three levels:

* Informational
* Warning
* Error

These levels behave like logging levels, letting [alerts](#alerts)
define the verbosity of outbound notifications:

* An alert configured for level *Informational* matches notifications of level *Informational*, *Warning*, and *Error*.
* An alert configured for level *Warning* matches notifications of level *Warning* and *Error*.
* An alert configured for level *Error* matches only notifications of level *Error*.

## Scopes

Notifications carry a *scope*. A scope broadly categorises the *subject*
of a notification.

* **SYSTEM**: Informs about system-level events, such as user creation or integration failures.
* **PORTFOLIO**: Informs about portfolio-level events, such as BOM uploads or newly identified vulnerabilities.

## Groups

A group is a granular classification of notification subjects within a [scope](#scopes).
For example, the `NEW_VULNERABILITY` group within the `PORTFOLIO` scope identifies notifications
that the system emits whenever it finds a new vulnerability.

Refer to [Notification groups](../reference/notifications/groups.md) for the full list
of groups, their scopes, levels, and triggers.

## Triggers

The platform produces notifications via one of two triggers:

| Trigger  | Description                                                |
|:---------|:-----------------------------------------------------------|
| Event    | The system emits an event under certain conditions.        |
| Schedule | The notification fires on a planned schedule.              |

* Event-triggered notifications fit near real-time automation
  and chat-platform integrations.
* Scheduled notifications typically communicate high-level summaries,
  which makes them a better fit for reporting.

Each [group](#groups) supports exactly one trigger type. Most groups use event triggers;
the summary groups (`NEW_VULNERABILITIES_SUMMARY`, `NEW_POLICY_VIOLATIONS_SUMMARY`)
use schedule triggers.

## How alert filtering works

When the platform dispatches a notification, it applies the alert's filters in this order:

1. Scope, group, and level matching.
2. Project and tag restrictions, if the alert limits delivery to specific projects or tags.
3. The [filter expression](../reference/notifications/filter-expressions.md), if the alert has one.

The platform runs the filter expression only after a notification has passed the preceding checks.
Project and tag restrictions thus always apply, regardless of what the expression
contains.

Filter expressions are *fail-open*: if an expression fails to run at dispatch time, for
example because it accesses a field that does not exist on the subject, the alert matches the
notification anyway. This avoids silently suppressing notifications when an expression
breaks. Evaluation failures appear in the logs as warnings; an alert with an expression that
consistently fails behaves as though it has no filter expression at all.

[CEL]: https://cel.dev/
