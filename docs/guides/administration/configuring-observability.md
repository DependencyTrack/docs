# Configuring observability

Dependency-Track exposes health check and metrics endpoints via a dedicated management server,
running on a separate port independently of the main app server.

!!! tip
    All observability-related configuration properties are documented in the
    [configuration reference](../../reference/configuration/properties.md),
    under the *Observability* category.

## Configuring Kubernetes health probes

The management server exposes health check endpoints that follow the [MicroProfile Health]
specification and map directly to Kubernetes [probe types].

Add the following probes to your Deployment manifest, adjusting the port if you changed
[`dt.management.port`](../../reference/configuration/properties.md#dtmanagementport)
(default: `9000`):

```yaml linenums="1"
containers:
  - name: apiserver
    livenessProbe:
      httpGet:
        path: /health/live
        port: 9000
      initialDelaySeconds: 15
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 9000
      initialDelaySeconds: 15
      periodSeconds: 10
    startupProbe:
      httpGet:
        path: /health/started
        port: 9000
      initialDelaySeconds: 10
      failureThreshold: 30
      periodSeconds: 5
```

The aggregate endpoint `/health` returns the combined status of all checks.

## Enabling Prometheus metrics scraping

Metrics are disabled by default. Enable them via
[`dt.metrics.enabled`](../../reference/configuration/properties.md#dtmetricsenabled):

```ini
dt.metrics.enabled=true
```

Once enabled, metrics are served at `/metrics` on the management port in the
[Prometheus text exposition format].

If you want to protect the endpoint with HTTP Basic authentication, set both
[`dt.metrics.auth.username`](../../reference/configuration/properties.md#dtmetricsauthusername) and
[`dt.metrics.auth.password`](../../reference/configuration/properties.md#dtmetricsauthpassword).

Add a scrape target to your Prometheus configuration:

```yaml linenums="1"
scrape_configs:
  - job_name: dependency-track
    metrics_path: /metrics
    static_configs:
      - targets:
          - "apiserver:9000"
    # Uncomment if you enabled authentication:
    # basic_auth:
    #   username: "metrics"
    #   password: "changeme"
```

## Adjusting log levels

By default, Dependency-Track logs at `INFO` level for application loggers and `WARN` for all others.
To troubleshoot a specific area, raise the log level for the relevant logger:

```properties
dt.logging.level."org.dependencytrack"=DEBUG
```

The special logger name `ROOT` applies to all loggers that are not explicitly configured:

```properties
dt.logging.level."ROOT"=ERROR
```

Refer to the [environment variable mapping](../../reference/configuration/application.md#environment-variable-mapping) documentation
for how to express these properties as environment variables.

[MicroProfile Health]: https://download.eclipse.org/microprofile/microprofile-health-4.0.1/microprofile-health-spec-4.0.1.html
[probe types]: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
[Prometheus text exposition format]: https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format
