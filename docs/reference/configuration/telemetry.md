# Telemetry

Dependency-Track periodically submits a small, anonymous data point to
`https://metrics.dependencytrack.org`. This helps the maintainers understand
adoption, plan version support, and decide which database systems to keep
testing against.

The submission does not include information that could tie data back to a
specific organization, such as IP addresses, hostnames, or project content.

## Data collected

Each submission is a single JSON object with four fields:

| Field        | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `system_id`  | Random cluster identifier generated at first startup. Stable across restarts and node replacements. |
| `dt_version` | Dependency-Track release version.                                           |
| `db_type`    | Database product name reported by JDBC (for example, `PostgreSQL`).         |
| `db_version` | Database product version reported by JDBC.                                  |

The `system_id` lets the maintainers correlate submissions from the same
deployment over time without identifying who runs it.

## Submission schedule

The [task scheduler](task-scheduler.md) runs the telemetry submission task
once shortly after startup with a random delay of up to one minute, and then
on the schedule defined by
[`dt.task.telemetry-submission.cron`](properties.md#dttasktelemetry-submissioncron)
(default `0 */1 * * *`, hourly).

The task itself enforces a 24-hour interval between submissions, so the cron
expression controls how often the task checks whether a new submission is
due, not how often data is actually sent.

## Opting out

You can opt out at any time through any of the following methods.

### Administration UI

Navigate to **Administration** > **Configuration** > **Telemetry** and turn
off submission.

### Configuration API

```shell linenums="1"
curl -X POST \
  -H 'X-Api-Key: odt_...' \
  -H 'Content-Type: application/json' \
  -d '{
        "groupName": "telemetry",
        "propertyName": "submission.enabled",
        "propertyValue": "false"
      }' \
  https://dtrack.example.com/api/v1/configProperty
```

### Before first startup

To opt out before the first startup populates the runtime setting, set
[`dt.telemetry.submission.default-enabled`](properties.md#dttelemetrysubmissiondefault-enabled)
to `false`:

```ini
dt.telemetry.submission.default-enabled=false
```

As an environment variable:

```shell
DT_TELEMETRY_SUBMISSION_DEFAULT_ENABLED=false
```

This property only seeds the initial value of the runtime setting. Once the
setting exists in the database, changes via the UI or REST API override the
initial value.
