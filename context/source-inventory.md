# Source Inventory

Map of app repo paths and accuracy status of existing-docs/ files.

## Symlinks (source/)

- **apiserver**: Refers to the main application repository. Also referred to as "API server", "apiserver", "backend".
  Contains REST API definitions in OpenAPI format, configuration (application.properties), and database migrations.
- **frontend**: Refers to the repository of the frontend, a SPA built with Vue.js.
  Contains route definitions and UI component structure.

## Existing Docs Accuracy

- **v4**: Refers to documentation of the previous major version of Dependency-Track.
  Most of it is outdated and incomplete. General documentation such as description of the project,
  use-cases, and integrations still apply. Built with Jekyll.
- **v5**: Refers to the initial state of the documentation for this major version of Dependency-Track.
  It is most thorough around the topics of operations and administration, but is missing most of the
  truly user-facing documentation (tutorials, workflows, concepts).
