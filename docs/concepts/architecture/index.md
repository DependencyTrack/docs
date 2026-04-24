# Architecture

This section covers the internal architecture of Dependency-Track v5,
describing key subsystems, their design rationale, and trade-offs.

## Design documents

- [Durable execution](design/durable-execution.md): The embedded workflow engine
  that provides reliable, scalable execution of background processes.
- [Vulnerability analysis](design/vulnerability-analysis.md): How the system matches components
  against vulnerability databases via a durable workflow.
- [Notifications](design/notifications.md): How the system emits, routes,
  and delivers events to external systems.
- [Package metadata resolution](design/package-metadata-resolution.md): How the system retrieves
  package metadata from upstream registries in a controlled, rate-aware manner.
