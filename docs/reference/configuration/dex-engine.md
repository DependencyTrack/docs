# Durable Execution Engine

The [durable execution engine](../../concepts/architecture/design/durable-execution.md) (dex) handles background task
scheduling and execution. This page documents its worker types, task queues, and default configuration.

For tuning guidance, see [Scaling](../../guides/administration/scaling.md#increase-background-throughput).

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
| `activity-worker` | `artifact-import`              | `artifact-imports`              |                   5 |
| `activity-worker` | `package-metadata-resolution`  | `package-metadata-resolutions`  |                   3 |
| `activity-worker` | `notification`                 | `notifications`                 |                   5 |
| `activity-worker` | `vuln-analysis-reconciliation` | `vuln-analysis-reconciliations` |                   5 |
| `activity-worker` | `policy-evaluation`            | `policy-evaluations`            |                   5 |
| `activity-worker` | `metrics-update`               | `metrics-updates`               |                   5 |

## Task queues

Task queue capacity limits how many tasks can be pending across the entire cluster.
When a queue reaches capacity, the scheduler stops creating new tasks for that queue,
providing backpressure.

Three related terms describe a queue's load:

- **Capacity** is the upper limit on pending tasks for a queue, enforced across the cluster.
- **Depth** is the number of tasks currently pending in the queue, from zero to capacity. Each
  cycle, the scheduler creates up to `capacity - depth` new tasks, so depth never exceeds capacity.
- **Backlog** applies to activity queues only. Workflow execution creates activity tasks directly,
  independently of the scheduler, so tasks can pile up in the `CREATED` state faster than the
  [activity task scheduler](../../concepts/architecture/design/durable-execution.md#activity-task-scheduler)
  moves them into the queue. The backlog is this set of ready-to-schedule tasks that the queue's
  capacity has not yet admitted. Workflow queues have no backlog, because the scheduler creates
  their tasks itself and never exceeds capacity.

The `dt_dex_engine_activity_task_queue_backlog` metric reports the backlog for scaling decisions. See
[Scale workers horizontally](../../guides/administration/scaling.md#scale-workers-horizontally).

Queue capacity is modifiable at runtime in the administrator panel under
*Workflows* > *Task Queues*, or via REST API.

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
