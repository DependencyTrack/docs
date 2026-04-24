# Dependency-Track Documentation

Documentation for [OWASP Dependency-Track](https://dependencytrack.org), built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and organized per the [Diataxis](https://diataxis.fr/) framework.

## Prerequisites

- Docker or Podman
- Make

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
make lint              # Run all linters
make lint-markdown     # Markdown (markdownlint)
make lint-prose        # Prose quality (Vale)
make lint-yaml         # YAML (yamllint)
```

All linters run in Docker. Fix all errors before submitting changes.
