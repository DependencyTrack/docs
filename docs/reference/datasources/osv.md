# OSV

[OSV](https://osv.dev/) (Open Source Vulnerabilities) is a vulnerability database
focused on open source packages, maintained by Google. It aggregates advisories from
multiple upstream sources including GitHub Advisories, PyPA, RustSec, and many others,
providing a unified PURL-keyed dataset.

## What It Provides

OSV advisories are natively keyed by package ecosystem and version, making them
well-suited for PURL-based matching across a wide range of languages and package managers.

OSV supports alias linking, so vulnerabilities tracked under different IDs (CVE, GHSA,
OSV-specific IDs) across databases are correlated automatically.

## Supported Ecosystems

OSV data can be selectively enabled per ecosystem. Available ecosystems include:
Go, npm, PyPI, RubyGems, crates.io (Rust), Maven, NuGet, Packagist (PHP), Hex (Erlang),
pub (Dart), Alpine, Debian, Ubuntu, Android, and others.

!!! tip
    For Debian, enable **Debian** rather than individual Debian version ecosystems.
    The Debian ecosystem package is a superset of all individual versions.

## Mirroring

Dependency-Track mirrors OSV data from Google Cloud Storage (`gs://osv-vulnerabilities`).
No authentication token is required. The mirror refreshes daily and on instance startup.

The mirroring schedule is controlled by
[`dt.task.osv.mirror.cron`](../configuration/properties.md#dttaskosvmirrorcron).

## Configuration

OSV mirroring is configured in the administration UI under
**Administration → Datasources → OSV**.

| Setting | Description |
|:--------|:------------|
| Enabled | Whether OSV mirroring is active. |
| Ecosystems | The specific ecosystems to mirror. Only selected ecosystems are downloaded. |

!!! warning
    Disabling OSV removes ecosystem selections from the UI but preserves previously
    mirrored vulnerability records in the database. Previously matched findings are
    not automatically removed.

## Alias Synchronisation

OSV supports alias synchronisation with other vulnerability databases. This is
configured on the [internal analyzer](../analyzers.md#internal) rather than on
the OSV datasource directly.
