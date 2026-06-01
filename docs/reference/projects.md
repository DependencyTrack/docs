# Projects

UI reference for the project form, the project detail page, and the project-related
administration panels. See [About projects](../concepts/projects.md) for background and
the user guides for procedures:

- [Organizing projects into hierarchies](../guides/user/organizing-projects.md)
- [Managing project versions](../guides/user/managing-project-versions.md)
- [Configuring project retention](../guides/administration/configuring-project-retention.md)

For request and response schemas, see the [v1](api/v1.md) and [v2](api/v2.md) OpenAPI
specifications.

## Classifiers

Project classifiers mirror the CycloneDX `metadata.component.type` enumeration. The
values appear verbatim in the *Classifier* dropdown of the project form.

| Classifier               | Description                       |
|:-------------------------|:----------------------------------|
| `APPLICATION`            | A software app.                   |
| `FRAMEWORK`              | A software framework.             |
| `LIBRARY`                | A software library.               |
| `CONTAINER`              | A container image.                |
| `PLATFORM`               | A computing platform.             |
| `OPERATING_SYSTEM`       | An operating system.              |
| `DEVICE`                 | A physical device.                |
| `DEVICE_DRIVER`          | A driver for a physical device.   |
| `FIRMWARE`               | Device firmware.                  |
| `FILE`                   | A standalone file.                |
| `MACHINE_LEARNING_MODEL` | A machine-learning model.         |
| `DATA`                   | A dataset.                        |

A collection project has no classifier. Switching a project to collection mode hides the
*Classifier* field.

## Collection logic

The *Project Collection Logic* dropdown configures aggregation on a collection project.
While set, the project cannot have its own components, services, or dependency graph,
and it does not accept BOM uploads.

| Value                                | Aggregation                                                                                              |
|:-------------------------------------|:---------------------------------------------------------------------------------------------------------|
| `AGGREGATE_DIRECT_CHILDREN`          | All direct children contribute to the parent's metrics.                                                  |
| `AGGREGATE_DIRECT_CHILDREN_WITH_TAG` | Only direct children carrying the configured *Collection Tag* contribute. The *Collection Tag* is mandatory. |
| `AGGREGATE_LATEST_VERSION_CHILDREN`  | Only direct children marked as the latest version contribute.                                            |

## Identity

| Field   | Required | Limit                                                                       |
|:--------|:--------:|:----------------------------------------------------------------------------|
| Name    | Yes      | Up to 255 characters.                                                       |
| Version | No       | Up to 255 characters. Treated as opaque text, not parsed or sorted.         |

The pair of name and version is unique across the instance, independent of where the
project sits in the hierarchy.

## Identifiers

The project form exposes ecosystem identifiers used for vulnerability matching.

| Field       | Limit      | Purpose                                                            |
|:------------|-----------:|:-------------------------------------------------------------------|
| PURL        | 1024 chars | Package URL. Primary identifier for vulnerability matching.        |
| CPE         |  255 chars | CPE 2.2 or 2.3 identifier. Used for NVD-style matching.            |
| SWID Tag ID |  255 chars | SWID tag identifier. Rarely used in practice.                      |

## Tags and properties

A project may carry any number of tags and any number of project properties.

| Entity           | Limits                                                                                                            | Notes                                                                  |
|:-----------------|:------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------|
| Tag              | Name up to 255 printable characters. Unique across the instance.                                                  | Many-to-many with projects. See [About tags](../concepts/tags.md).     |
| Project property | Group and name 1 to 255 characters, no control characters. Value up to 1024 characters. Type is mandatory.        | Per-project key-value metadata, scoped to the project.                 |

## Retention configuration

Configured at *Administration > Configuration > Maintenance > Projects Retention*. See
[Configuring project retention](../guides/administration/configuring-project-retention.md)
for the setup procedure.

| Control                              | Default      | Purpose                                                                                                                |
|:-------------------------------------|:-------------|:-----------------------------------------------------------------------------------------------------------------------|
| *Enable Inactive Project Deletion*   | Off          | Master switch. While off, the maintenance task does nothing.                                                           |
| *Project Retention Type*             | Unset        | *AGE* deletes by retirement age. *VERSIONS* keeps the most recent inactive versions per project name.                  |
| *AGE* slider                         | 30 days      | Cutoff for the *AGE* mode. The next task run deletes inactive projects older than this.                                |
| *VERSIONS* slider                    | 2 versions   | Number of most recent inactive versions kept per project name in *VERSIONS* mode. The task removes older versions.     |
