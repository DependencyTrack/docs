# Durable Execution Engine

The durable execution engine (dex) handles background task scheduling and execution.
This page documents its worker types, task queues, and default configuration.

For tuning guidance, see [Scaling](../../guides/administration/scaling.md#concurrency-control).

## Workers

Workers poll task queues and execute tasks. Each worker has a configurable
maximum concurrency that limits how many tasks it processes simultaneously
per instance.

Worker concurrency is configured via:

```ini
dt.dex-engine.<worker-type>.<worker-name>.max-concurrency=<N>
```

Where `<worker-type>` is either `workflow-worker` or `activity-worker`.

| Worker Type       | Worker Name                    | Queue                           | Default Concurrency |
|-------------------|--------------------------------|---------------------------------|--------------------:|
| `workflow-worker` | `default`                      | `default`                       |                 100 |
| `activity-worker` | `default`                      | `default`                       |                  25 |
| `activity-worker` | `vuln-analysis`                | `vuln-analyses`                 |                  10 |
| `activity-worker` | `artifact-import`              | `artifact-imports`              |                  10 |
| `activity-worker` | `package-metadata-resolution`  | `package-metadata-resolutions`  |                  10 |
| `activity-worker` | `notification`                 | `notifications`                 |                   5 |
| `activity-worker` | `vuln-analysis-reconciliation` | `vuln-analysis-reconciliations` |                   5 |
| `activity-worker` | `policy-evaluation`            | `policy-evaluations`            |                   5 |
| `activity-worker` | `metrics-update`               | `metrics-updates`               |                   5 |

## Task queues

Task queue capacity limits how many tasks can be pending across the entire cluster.
When a queue reaches capacity, the scheduler stops creating new tasks for that queue,
providing backpressure.

Queue capacity is modifiable at runtime in the administrator panel under
*Workflows* -> *Task Queues*, or via REST API.

| Type       | Queue                           | Default Capacity |
|------------|---------------------------------|-----------------:|
| `workflow` | `default`                       |             1000 |
| `activity` | `default`                       |             1000 |
| `activity` | `artifact-imports`              |               25 |
| `activity` | `metrics-updates`               |               25 |
| `activity` | `notifications`                 |               25 |
| `activity` | `package-metadata-resolutions`  |               25 |
| `activity` | `policy-evaluations`            |               25 |
| `activity` | `vuln-analyses`                 |               25 |
| `activity` | `vuln-analysis-reconciliations` |               25 |
