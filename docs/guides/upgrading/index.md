# Upgrade guides

Breaking and otherwise notable changes for each release, with any manual steps they require.

!!! warning "Upgrade minor versions one at a time"
    Work through the guide for every minor version between the one you run and the one you
    upgrade to, in release order, for example `5.0.x` to `5.1.x` to `5.2.x`. Skipping patch releases within
    a minor version is fine. For example, to get from `5.0.1` to `5.0.5`, read every intervening patch
    release guide, but upgrade in a single step.

## Related guides

- [Upgrading running instances](../administration/upgrading-instances.md): rolling upgrade of a running cluster without planned downtime.
- [Migrating from v4 to v5](../administration/migrating-from-v4.md): one-shot data migration from v4 (PostgreSQL or Microsoft SQL Server) into v5 (PostgreSQL only).

## Release notes

These pages cover only what an upgrade demands your attention for. For the complete list of changes
in a release, including features and bug fixes, see the release notes on GitHub:

- [API server release notes](https://github.com/DependencyTrack/dependency-track/releases)
- [Frontend release notes](https://github.com/DependencyTrack/frontend/releases)

## Version 5 releases

- [Upgrading to v5.1.0](v5.1.0.md)
- [Upgrading to v5.0.5](v5.0.5.md)
- [Upgrading to v5.0.0-rc.2](v5.0.0-rc.2.md)
- [Upgrading to v5.0.0-rc.1](v5.0.0-rc.1.md)

## Version 0.x releases

- [Upgrading to v0.7.0-alpha.9](v0.7.0-alpha.9.md)
- [Upgrading to v0.7.0-alpha.8](v0.7.0-alpha.8.md)
- [Upgrading to v0.7.0-alpha.6](v0.7.0-alpha.6.md)
- [Upgrading to v0.7.0-alpha.5](v0.7.0-alpha.5.md)
- [Upgrading to v0.7.0-alpha.4](v0.7.0-alpha.4.md)
- [Upgrading to v0.7.0-alpha.3](v0.7.0-alpha.3.md)
- [Upgrading to v0.6.0](v0.6.0.md)
