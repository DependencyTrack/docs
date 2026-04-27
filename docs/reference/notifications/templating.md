# Templating

Publishers render notifications into their destination format using
[Pebble](https://pebbletemplates.io/) templates. Each built-in publisher
ships with a default template; administrators can replace it with a
custom template that draws on the variables and filters described here.

## Template context

The following variables are available in every template.

| Variable                | Type                                                                                                         | Description                                                                                                                                |
|:------------------------|:-------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| `baseUrl`               | string                                                                                                       | Base URL of the Dependency-Track frontend, as configured by the operator. Empty string when unset.                                         |
| `timestampEpochSeconds` | long                                                                                                         | Notification timestamp expressed as seconds since the Unix epoch.                                                                          |
| `timestamp`             | string                                                                                                       | Notification timestamp formatted as an [ISO 8601] local date-time (`uuuu-MM-dd'T'HH:mm:ss.SSSSSSSSS`).                                     |
| `notification`          | [`Notification`](../schemas/notification.md#notification) message                                            | The full notification, with fields `level`, `scope`, `group`, `title`, `content`, `timestamp`, and `subject`.                              |
| `subject`               | message                                                                                                      | Typed subject of the notification, present only for groups that emit one. The concrete message type depends on the notification's `group`. |
| `subjectJson`           | string                                                                                                       | JSON representation of `subject`, present only when the notification has a `subject`.                                                      |

The shape of `subject` varies by notification group. Refer to the
[notification schema reference](../schemas/notification.md) for the
message type emitted for each group.

!!! note
    The variable is `timestampEpochSeconds` (plural). Templates carried
    over from Dependency-Track v4 referenced `timestampEpochSecond`
    (singular) and require an update.

## Custom filters

Beyond the [built-in Pebble filters], Dependency-Track registers
two filters specific to notifications.

### `formatTimestamp`

Formats a `google.protobuf.Timestamp` value (such as
`notification.timestamp`) as an ISO 8601 local date-time string.

```pebble
{{ notification.timestamp | formatTimestamp }}
```

### `summarize`

Produces a short, human-readable identifier for a `Project` or
`Component` value.

For projects, the result is `name` optionally followed by
`` ` : ` `` and `version`. For components, the result is the `purl`
when set; otherwise `name` optionally prefixed with `` `group : ` ``
and suffixed with `` ` : ` `` and `version`. Inputs of any other
type are returned as their string representation.

```pebble
{{ notification.subject.component | summarize }}
```

## Template restrictions

For security reasons, the following Pebble features are **not** available
in notification templates:

- The `include` tag. Templates cannot pull in other files from the
  filesystem.
- Any tag or function that would read from the filesystem or execute
  arbitrary code.

The default output escaping strategy is `json`, which is appropriate for
JSON-bodied destinations such as webhooks and chat platforms. Templates
that produce other formats (for example, plain-text email) should
override the escaping strategy with the relevant Pebble construct.

[ISO 8601]: https://en.wikipedia.org/wiki/ISO_8601
[built-in Pebble filters]: https://pebbletemplates.io/wiki/guide/basic-usage/#filters
