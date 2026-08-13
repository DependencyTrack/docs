# Deploying to Kubernetes

The community maintains the `dependency-track` Helm chart for running Dependency-Track on Kubernetes.
The [helm-charts repository] documents installation, the values reference, and OpenShift compatibility.

Chart 2.x targets Dependency-Track 5.0.0 and later. Chart 1.x targets Dependency-Track 4.x.

The sizing, database, and operational guidance in [Deploying to production] applies regardless of platform.

## Upgrading an existing release

Chart 2.x is not a drop-in upgrade from chart 1.x or from the `hyades` chart. Both paths require a
reinstall. The chart's [upgrade guide] describes the full procedure, including database backup,
the Secrets that chart 2.x expects, file storage, values translation, and cutover.

!!! warning "Do not use the `hyades` chart"
    The separate `hyades` chart served as the preview chart for Dependency-Track v5. The maintainers
    deprecated it in favor of the `dependency-track` chart, and it receives no further updates. Do not
    use it for new deployments. If you already run it, follow the chart's [upgrade guide] to move to the
    `dependency-track` chart.

[Deploying to production]: deploying-to-production.md
[helm-charts repository]: https://github.com/DependencyTrack/helm-charts/tree/main/charts/dependency-track
[upgrade guide]: https://github.com/DependencyTrack/helm-charts/blob/main/charts/dependency-track/UPGRADING.md
