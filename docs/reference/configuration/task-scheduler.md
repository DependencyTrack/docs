# Task scheduler

The task scheduler triggers recurring background activities like vulnerability
data source mirroring, integration uploads, metric updates, and maintenance
sweeps. Many tasks enqueue work for the [durable execution engine](dex-engine.md),
which executes workflows and other asynchronous processing.

Nodes with the scheduler enabled coexist safely. The scheduler coordinates
execution through the database, so each due task runs on exactly one node
without requiring leader election.

## Configuration

You can turn the scheduler off on a per-node basis, for example to dedicate
specific nodes to serving web traffic. The `threads` setting caps how many
scheduled tasks may run concurrently on a single node. Because the
[durable execution engine](dex-engine.md) performs most asynchronous work,
this is rarely the right knob to tune.

Configuration:

- [`dt.task-scheduler.enabled`](properties.md#dttask-schedulerenabled)
- [`dt.task-scheduler.threads`](properties.md#dttask-schedulerthreads)
- [`dt.task-scheduler.poll-interval-ms`](properties.md#dttask-schedulerpoll-interval-ms)
- [`dt.task-scheduler.shutdown-max-wait-ms`](properties.md#dttask-schedulershutdown-max-wait-ms)

## Cron expressions

Each scheduled task takes its schedule from a `dt.task.<name>.cron` property,
which holds a five-field UNIX cron expression:

```text
minute  hour  day-of-month  month  day-of-week
```

All expressions use **UTC**.

Example, run every day at 03:30 UTC:

```ini
dt.task.nvd-vuln-data-source-mirror.cron=30 3 * * *
```

## Scheduled tasks

The scheduler ships with the following recurring tasks. Tasks marked with
[^1] also run once shortly after startup, with a random delay of up to one
minute.

| Task                              | Property                                                                                                                | Default cron     | Purpose                                                                                       |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------|
| Portfolio metrics update          | [`dt.task.portfolio-metrics-update.cron`](properties.md#dttaskportfolio-metrics-updatecron)                             | `10 * * * *`     | Refreshes per-project and portfolio time series metrics.                                      |
| Vulnerability metrics update      | [`dt.task.vuln-metrics-update.cron`](properties.md#dttaskvuln-metrics-updatecron)                                       | `0 */6 * * *`    | Refreshes counters used by the vulnerability dashboard.                                       |
| Portfolio vulnerability analysis  | [`dt.task.portfolio-analysis.cron`](properties.md#dttaskportfolio-analysiscron)                                         | `0 6 * * *`      | Re-analyzes every component in the portfolio against current vulnerability data.              |
| NVD mirror[^1]                    | [`dt.task.nvd-vuln-data-source-mirror.cron`](properties.md#dttasknvd-vuln-data-source-mirrorcron)                       | `0 4 * * *`      | Mirrors the NIST National Vulnerability Database.                                             |
| GitHub Advisories mirror[^1]      | [`dt.task.github-advisory-vuln-data-source-mirror.cron`](properties.md#dttaskgithub-advisory-vuln-data-source-mirrorcron) | `0 2 * * *`    | Mirrors the GitHub Advisory Database.                                                         |
| OSV mirror[^1]                    | [`dt.task.osv-vuln-data-source-mirror.cron`](properties.md#dttaskosv-vuln-data-source-mirrorcron)                       | `0 3 * * *`      | Mirrors the OSV vulnerability database.                                                       |
| EPSS mirror[^1]                   | [`dt.task.epss-mirror.cron`](properties.md#dttaskepss-mirrorcron)                                                       | `0 1 * * *`      | Mirrors the FIRST EPSS scores feed.                                                           |
| Vulnerability database maintenance | [`dt.task.vuln-database-maintenance.cron`](properties.md#dttaskvuln-database-maintenancecron)                          | `0 0 * * *`      | Removes orphaned vulnerability records and reconciles indexes.                                |
| Vulnerability policy bundle sync[^1] | [`dt.task.vuln-policy-bundle-sync.cron`](properties.md#dttaskvuln-policy-bundle-synccron)                            | `*/15 * * * *`   | Pulls the configured vulnerability policy bundle. No-op when `dt.vuln-policy-bundle.url` is empty. |
| Package metadata resolution       | [`dt.task.package-metadata-resolution.cron`](properties.md#dttaskpackage-metadata-resolutioncron)                       | `0 1 * * *`      | Refreshes outdated-component status for portfolio components.                                 |
| Package metadata maintenance      | [`dt.task.package-metadata-maintenance.cron`](properties.md#dttaskpackage-metadata-maintenancecron)                     | `0 */12 * * *`   | Removes stale and orphaned package metadata records.                                          |
| Metrics maintenance               | [`dt.task.metrics-maintenance.cron`](properties.md#dttaskmetrics-maintenancecron)                                       | `1 * * * *`      | Compacts time series metric history.                                                          |
| Tag maintenance                   | [`dt.task.tag-maintenance.cron`](properties.md#dttasktag-maintenancecron)                                               | `0 */12 * * *`   | Removes unused tags.                                                                          |
| Project maintenance               | [`dt.task.project-maintenance.cron`](properties.md#dttaskproject-maintenancecron)                                       | `0 */4 * * *`    | Applies project retention and cleanup rules.                                                  |
| Fortify SSC upload                | [`dt.task.fortify-ssc-upload.cron`](properties.md#dttaskfortify-ssc-uploadcron)                                         | `0 2 * * *`      | Uploads finding reports to Fortify SSC.                                                       |
| DefectDojo upload                 | [`dt.task.defect-dojo-upload.cron`](properties.md#dttaskdefect-dojo-uploadcron)                                         | `0 2 * * *`      | Uploads finding reports to DefectDojo.                                                        |
| Kenna Security upload             | [`dt.task.kenna-security-upload.cron`](properties.md#dttaskkenna-security-uploadcron)                                   | `0 2 * * *`      | Uploads finding reports to Kenna Security.                                                    |
| Expired session cleanup           | [`dt.task.expired-session-cleanup.cron`](properties.md#dttaskexpired-session-cleanupcron)                               | `0 * * * *`      | Deletes expired user session tokens.                                                          |
| Scheduled notification dispatch   | [`dt.task.scheduled-notification-dispatch.cron`](properties.md#dttaskscheduled-notification-dispatchcron)               | `* * * * *`      | Polls for due scheduled notification rules and dispatches them.                               |
| Telemetry submission[^1]          | [`dt.task.telemetry-submission.cron`](properties.md#dttasktelemetry-submissioncron)                                     | `0 */1 * * *`    | Submits anonymous usage data. See [Telemetry](telemetry.md).                                  |

[^1]: Triggered once on startup with a random delay of up to one minute, then on the configured schedule.
