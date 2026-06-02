# Dependency-Track Documentation

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![Build status](https://github.com/DependencyTrack/docs/actions/workflows/build.yml/badge.svg)](https://github.com/DependencyTrack/docs/actions/workflows/build.yml)
[![Deploy status](https://github.com/DependencyTrack/docs/actions/workflows/deploy.yml/badge.svg)](https://github.com/DependencyTrack/docs/actions/workflows/deploy.yml)

Documentation for [OWASP Dependency-Track](https://dependencytrack.org), built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and organized per the [Diataxis](https://diataxis.fr/) framework.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Make
- Docker or Podman (linters only)

## Getting started

```sh
# Live-reload dev server on http://localhost:8000
make serve

# Production build
make build
```

## Documentation structure

```
docs/
  tutorials/   # Learning-oriented walkthroughs
  guides/      # Task-oriented procedures
  concepts/    # Understanding-oriented background
  reference/   # Information-oriented technical descriptions
  blog/        # Release notes, changelog, engineering posts
```

Navigation is managed via `.pages` files in each section directory.

## Linting

```sh
make lint                  # Run all linters
make lint-markdown         # Markdown (markdownlint)
make lint-prose            # Prose quality (Vale, full docs/ tree)
make lint-prose-changed    # Vale, only files changed vs. the upstream branch
make lint-yaml             # YAML (yamllint)
make lint-python           # Python (Ruff)
```

Linters run in Docker, except for Python which uses [Ruff](https://docs.astral.sh/ruff/) via `uvx`. Fix all errors before submitting changes.

## Generated documentation

Some reference pages are generated from upstream source repositories and should not be edited directly. GitHub Actions workflows are provided to automate regeneration.

| Content | Source                                                                                              | Workflow | Local command |
|:--------|:----------------------------------------------------------------------------------------------------|:---------|:--------------|
| Configuration properties | `application.properties` in [dependency-track](https://github.com/DependencyTrack/dependency-track) | `update-config-docs` | `make generate-config-docs APISERVER_PROPERTIES=<path>` |
| Protobuf schemas | `.proto` files in [dependency-track](https://github.com/DependencyTrack/dependency-track)           | `update-proto-docs` | `make generate-proto-docs APISERVER_DIR=<path>` |
| OpenAPI specs | CI artifacts from [dependency-track](https://github.com/DependencyTrack/dependency-track)           | `update-openapi-docs` | n/a |

## See also

- [dependency-track](https://github.com/DependencyTrack/dependency-track): Main repository
- [frontend](https://github.com/DependencyTrack/frontend): Frontend repository
- [helm-charts](https://github.com/DependencyTrack/helm-charts): [Helm](https://helm.sh/) charts
- [community](https://github.com/DependencyTrack/community): Community resources

