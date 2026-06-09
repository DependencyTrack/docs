# Deploying to Kubernetes

The community maintains Helm charts for running Dependency-Track on Kubernetes at the
[helm-charts repository](https://github.com/DependencyTrack/helm-charts). The sizing, database, and
operational guidance in [Deploying to production](deploying-to-production.md) applies regardless of
platform, and you should read it alongside the chart documentation.

!!! warning "v5 Helm chart not yet available"
    The `dependency-track` chart is not yet compatible with v5. As a safety mechanism against silent
    misconfiguration, the chart fails during rendering when it detects a v5 image tag. A v5-compatible
    release is in progress and ships soon. Until then, you can either wait for the chart, or roll your
    own manifests based on the v5 container images. See
    [Container images](../../reference/container-images.md) for image coordinates and tag conventions.

!!! warning "The `hyades` chart goes away soon"
    A separate `hyades` chart exists from the period when the project developed v5 under the Hyades
    name. The maintainers archive it once the v5-compatible `dependency-track` chart ships. New users
    should not adopt it. If you already run the `hyades` chart, plan to migrate to the
    `dependency-track` chart once it becomes available.
