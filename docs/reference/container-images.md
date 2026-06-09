# Container Images

Dependency-Track ships as a set of container images. Each component has its own
image. Releases go to GitHub Container Registry first and then mirror to Docker
Hub asynchronously.

## Components

| Component | Description |
|:----------|:------------|
| API server | Backend service. Exposes the REST API and runs analysis. |
| Frontend | Web UI. Serves the static single-page app. |
| v4 migrator | One-shot tool for migrating a v4 database to v5. See [Migrating from v4](../guides/administration/migrating-from-v4.md). |

Dependency-Track v4 published a "bundled" image combining API server and
frontend. v5 does not. Operators must run the two components as separate
containers.

## Registries

Two registries host the images:

| Registry | Role |
|:---------|:-----|
| `ghcr.io` | Primary. Receives new tags first. |
| `docker.io` | Mirror. Updated asynchronously from `ghcr.io`. |

A newly published tag appears on `ghcr.io` immediately and on `docker.io` once
the mirror job completes. If a tag is missing from Docker Hub shortly after a
release, pull it from `ghcr.io` or retry after the mirror catches up.

## Image coordinates

| Component | GHCR | Docker Hub |
|:----------|:-----|:-----------|
| API server | `ghcr.io/dependencytrack/apiserver` | `docker.io/dependencytrack/apiserver` |
| Frontend | `ghcr.io/dependencytrack/frontend` | `docker.io/dependencytrack/frontend` |
| v4 migrator | `ghcr.io/dependencytrack/v4-migrator` | `docker.io/dependencytrack/v4-migrator` |

## Tags

| Tag pattern | Example | Description                                                 |
|:------------|:--------|:------------------------------------------------------------|
| `X.Y.Z` | `5.0.0` | Stable release.                                             |
| `X.Y.Z-rc.N` | `5.1.0-rc.1` | Release candidate.                                          |
| `X-snapshot` | `5-snapshot` | Latest build from the `main` branch. Moves with each merge. |

Always pin deployments to a full `X.Y.Z` tag, or to an image digest. This keeps
rollouts reproducible and avoids accidental upgrades.

!!! warning
    Do not use the `latest` tag. It points to the most recent v4 release and
    keeps pointing there until v4 reaches end of life in December 2026. v5
    users that pull `latest` get a v4 image.

## Immutability

Release tags (`X.Y.Z`, `X.Y.Z-rc.N`) on Docker Hub are
[immutable](https://docs.docker.com/docker-hub/repos/manage/hub-images/immutable-tags/).
Once published, the digest a release tag points to cannot change. This
guarantees that a deployment pinned to `5.0.0` resolves to the same image
forever, regardless of mirror state or registry caches.

Snapshot tags (`5-snapshot`) are mutable by design. They move with each new
build.
