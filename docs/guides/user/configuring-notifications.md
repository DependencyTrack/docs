# Configuring notification alerts

An *alert* subscribes to one or more [notification groups](../../reference/notifications/groups.md)
and forwards matching notifications to a destination through a
[publisher](../../reference/notifications/publishers.md). This guide
covers creating an alert and restricting it to a subset of the portfolio.

## Prerequisites

- The `SYSTEM_CONFIGURATION` permission.
- At least one configured publisher. Built-in publishers (email, Slack,
  Webhook, and so on) ship out of the box, but most still
  require global settings such as an SMTP server or destination URL.
  See the [notification publishers reference](../../reference/notifications/publishers.md).

## Creating an alert

Open **Administration → Notifications → Alerts** and click *Create
Alert*. Provide:

- A unique **name**.
- The [scope](../../concepts/notifications.md#scopes): `SYSTEM` for platform events, `PORTFOLIO`
  for project events.
- The notification [level](../../concepts/notifications.md#levels) the alert listens for.
- The [publisher](../../concepts/notifications.md#publishers) that delivers matching notifications.
- The alert's [trigger](#choosing-a-trigger).

After saving the alert, open it for editing to configure the rest.

## Choosing a trigger

Set the trigger to *Event* (default) for real-time delivery, or to
*Schedule* for a periodic digest. See
[Triggers](../../concepts/notifications.md#triggers) for the distinction.
The summary groups (`NEW_VULNERABILITIES_SUMMARY`,
`NEW_POLICY_VIOLATIONS_SUMMARY`) require a scheduled trigger; the
[notification groups reference](../../reference/notifications/groups.md)
lists the trigger for every group.

To configure a recurring digest, set the trigger to *Schedule* and see
[Scheduling](#scheduling) below. The other steps apply to both triggers:
group selection, destination, scope limits, and filter expressions.

## Selecting groups

Each alert subscribes to one or more notification groups within its
scope. The list of available groups shows only those compatible
with the alert's scope and trigger type. Refer to
[Notification groups](../../reference/notifications/groups.md) for the
full list and what each group represents.

## Setting the destination

The destination format depends on the publisher. Common cases:

| Publisher                                 | Destination                                                                                                          |
|:------------------------------------------|:---------------------------------------------------------------------------------------------------------------------|
| email                                     | One or more recipient addresses, one or more teams, or a combination of both. See [email alert config][email-alert]. |
| Slack, Microsoft Teams, Mattermost, Webex | Incoming-webhook URL issued by the destination platform.                                                             |
| Jira                                      | Project key and issue type. See [Jira alert config][jira-alert].                                                     |
| Webhook                                   | HTTP(S) endpoint that accepts the notification payload.                                                              |
| Kafka                                     | Topic name and serialization format. See [Kafka alert config][kafka-alert].                                          |

For the full set of fields exposed by each publisher, see the
[publishers reference](../../reference/notifications/publishers.md).

## Limiting to projects

By default, a `PORTFOLIO`-scoped alert fires for every project in the
portfolio. To restrict it, expand the *Limit To* section and add one or
more projects.

!!! note
    Scheduled alerts *require* a non-empty project list: the summary groups
    cannot run across the entire portfolio because the payload would be too
    large for most receiving systems and too expensive to compute. You cannot
    save the alert without at least one project.

To also receive notifications for child projects of the selected projects,
enable *Include active children of projects*. The platform only includes
active children; it skips inactive ones.

## Limiting to tags

An alert can also restrict delivery to projects carrying any of a set of
tags. Add the tags to the *Limit To* section.

When the list contains more than one tag, a project matches if it has *at
least one* of them. Tags combine with **OR** semantics.

With both *Limit to projects* and *Limit to tags* set, a
project matches if it meets *either* condition. The two restrictions
also combine with **OR** semantics.

## Scheduling

When the trigger is *Schedule*, the alert delivers on a [cron]
expression instead of per event:

```text
* * * * *
| | | | |
| | | | day of the week (0-6, Sunday to Saturday)
| | | month of the year (1-12)
| | day of the month (1-31)
| hour of the day (0-23)
minute of the hour (0-59)
```

`*` means *any*. For example, `0 8 * * *` triggers at 08:00 every day,
and `0 8 * * 1` triggers at 08:00 every Monday.

A few defaults and constraints apply:

- The default schedule on a newly created alert is *hourly*.
- Cron expressions resolve in **UTC**. `0 8 * * *` means 08:00
  UTC, regardless of the operator's timezone. Tools such as
  [crontab guru] help build expressions.
- Dependency-Track checks for due schedules every minute and processes
  them serially. Notifications can thus arrive a few minutes after
  their scheduled time.
- The configuration panel shows the timestamp of the last successful
  trigger and the next planned trigger.

To suppress a notification when no new findings exist
since the last successful run, enable *Skip if unchanged*. This reduces
noise on schedules that often have nothing new to report.

Scheduled summaries can produce sizeable payloads. The email and Webhook
publishers handle the full content reliably; chat-platform publishers
such as Slack or Microsoft Teams may reject messages exceeding their
per-message size limits. For high-volume schedules, prefer email,
Webhook, or Kafka.

## Filter expressions

For finer control over which notifications match (for example, only
vulnerabilities exceeding a CVSS threshold), attach a filter expression to
the alert. See [Filter expressions](../../reference/notifications/filter-expressions.md).

## See also

- [Notification groups](../../reference/notifications/groups.md)
- [Debugging missing notifications](../administration/debugging-notifications.md)
- [Notification publishers](../../reference/notifications/publishers.md)

[cron]: https://en.wikipedia.org/wiki/Cron
[crontab guru]: https://crontab.guru/
[email-alert]: ../../reference/notifications/publishers.md#email-alert-config
[jira-alert]: ../../reference/notifications/publishers.md#jira-alert-config
[kafka-alert]: ../../reference/notifications/publishers.md#kafka-alert-config
