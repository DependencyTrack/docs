# AGENTS.md

## Project

Dependency-Track documentation site. Built with MkDocs Material, organized per the Diataxis framework.

## Context files

Before writing or modifying documentation, read the relevant context files in `context/`:

- `context/diataxis-contract.md` — mandatory. Defines the four content types (tutorials, guides, concepts, reference) and what belongs where. Every doc must fit exactly one type.
- `context/vocabulary.md` — canonical terminology. Use these terms consistently.
- `context/briefing.md` — product overview and audience.
- `context/source-inventory.md` — describes source repo symlinks and existing docs accuracy status.

## Documentation structure

```
docs/
  tutorials/      # Learning-oriented walkthroughs (student perspective)
  guides/         # Task-oriented procedures (experienced user)
    upgrading/    # Version-specific upgrade procedures
  concepts/       # Understanding-oriented background
  reference/      # Information-oriented technical descriptions
  blog/           # Release notes, changelog, engineering posts (non-Diataxis)
```

Navigation order is defined in `docs/.pages` and section-level `.pages` files. Update these when adding new pages.

## Commands

Always use `make` targets for building, serving, and linting. Do not run `docker`, `mkdocs`, `markdownlint-cli2`, `yamllint`, or `vale` directly. The Makefile is the single source of truth for how these tools are invoked.

### Linting

Run the relevant linter after modifying files:

- **Markdown files** (`docs/**/*.md`, `context/**/*.md`): `make lint-markdown`
- **Prose quality** (`docs/**/*.md`): `make lint-prose`
- **YAML files** (`mkdocs.yml`, `.github/**/*.yml`, etc.): `make lint-yaml`
- **All at once**: `make lint`

Fix all lint errors before considering work complete.

### Build and preview

- `make serve` — live-reload dev server on port 8000.
- `make build` — strict production build (fails on warnings).

Always verify new or modified pages render correctly with `make build`.

## Writing conventions

- Do not modify files in `existing-docs/`.
- Do not add files to `source/` without instruction.
- Use ATX-style headings (`# Heading`), not setext.
- Inline HTML is allowed (admonitions, tabs).
- No line length limit for Markdown prose.
- YAML indentation: 2 spaces, no document-start markers.
- Vale enforces Google developer style and write-good rules. Accepted/rejected terms are in `.vale/styles/config/vocabularies/DependencyTrack/`.
