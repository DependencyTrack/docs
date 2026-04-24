# Configuring observability

Dependency-Track exposes health check and metrics endpoints via a dedicated management server.
It runs on a separate port, and potentially different bind address, independently of the main app server.

The management server's bind address and port are configurable:

- [`dt.management.host`](../../reference/configuration/properties.md#dtmanagementhost) (default: `0.0.0.0`)
- [`dt.management.port`](../../reference/configuration/properties.md#dtmanagementport) (default: `9000`)

!!! tip
    All observability-related configuration properties are documented in the
    [configuration reference](../../reference/configuration/properties.md),
    under the *Observability* category.

## Health checks

Health check endpoints follow the [MicroProfile Health] specification.
They return JSON responses with an overall `status` (`UP` or `DOWN`)
and individual check results. The HTTP status code is `200` when healthy, `503` otherwise.

The following endpoints are available on the management server:

| Endpoint          | Description                           |
|:------------------|:--------------------------------------|
| `/health`         | Aggregate status of all health checks |
| `/health/live`    | Liveness checks                       |
| `/health/ready`   | Readiness checks                      |
| `/health/started` | Startup checks                        |

These endpoints map directly to Kubernetes [probe types] and can be used as-is
in `livenessProbe`, `readinessProbe`, and `startupProbe` configurations.

## Metrics

When enabled, Prometheus metrics are served at the `/metrics` endpoint of the management server,
using the [Prometheus text exposition format].

Metrics are off by default. Enable them via
[`dt.metrics.enabled`](../../reference/configuration/properties.md#dtmetricsenabled).

Access to the metrics endpoint can optionally be protected with HTTP Basic authentication:

- [`dt.metrics.auth.username`](../../reference/configuration/properties.md#dtmetricsauthusername)
- [`dt.metrics.auth.password`](../../reference/configuration/properties.md#dtmetricsauthpassword)

Both must be set for authentication to take effect.

## Logging

By default, Dependency-Track logs at `INFO` level for app loggers (`alpine`, `org.dependencytrack`,
`org.eclipse.jetty`) and `WARN` for all others.

Log levels can be configured per logger as follows:

```properties
dt.logging.level."org.dependencytrack"=DEBUG
dt.logging.level."org.eclipse.jetty"=WARN
dt.logging.level."ROOT"=ERROR
```

The special logger name `ROOT` applies to all loggers that are not explicitly configured.

Refer to the [environment variable mapping](../../reference/configuration/application.md#environment-variable-mapping) documentation
for how to express these properties as environment variables.

[MicroProfile Health]: https://download.eclipse.org/microprofile/microprofile-health-4.0.1/microprofile-health-spec-4.0.1.html
[probe types]: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
[Prometheus text exposition format]: https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format
