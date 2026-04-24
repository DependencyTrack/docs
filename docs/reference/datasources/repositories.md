# Package Repositories

Dependency-Track integrates with public and private package repositories to fetch
component metadata. This integration is used primarily for
outdated component detection: Dependency-Track
queries the registry for a component's latest available version and compares it to the
version in the SBOM.

## Supported Ecosystems

The following ecosystems are supported out of the box, each with a pre-configured
default repository:

| Ecosystem | Default repository |
|:----------|:------------------|
| Cargo (Rust) | [crates.io](https://crates.io) |
| Composer (PHP) | [Packagist](https://packagist.org) |
| Gem (Ruby) | [RubyGems](https://rubygems.org) |
| GitHub (Actions) | [github.com](https://github.com) |
| Go Modules | [proxy.golang.org](https://proxy.golang.org) |
| Hex (Erlang/Elixir) | [Hex.pm](https://hex.pm) |
| Maven (Java) | [Maven Central](https://central.sonatype.com) |
| npm (Node.js) | [npmjs.com](https://www.npmjs.com) |
| NuGet (.NET) | [nuget.org](https://www.nuget.org) |
| PyPI (Python) | [pypi.org](https://pypi.org) |
| CPAN (Perl) | [CPAN](https://www.cpan.org) |

Additional repositories can be configured for any ecosystem in
**Administration → Repositories**.

## Configuration

Repository settings are managed in **Administration → Repositories**. Each repository
entry has the following properties:

| Property | Description |
|:---------|:------------|
| Enabled | Whether the repository is queried during analysis. Disabled repositories are skipped. |
| Internal | Whether this is an internal (private) registry. Internal repositories are used *only* for components marked as internal. Non-internal repositories are used only for non-internal components. |
| URL | The base URL of the repository. |
| Authentication | Optional credentials (see below). |

## Authentication

Three authentication methods are supported:

| Method | Configuration |
|:-------|:-------------|
| None | No credentials required (default for public repositories). |
| Basic | Enter a username and password. |
| Bearer token | Leave the username blank; enter the token in the password field. |

For GitHub, use your GitHub username and a [personal access token](https://github.com/settings/tokens)
with at least public read access.

For private repositories such as Azure Artifacts or JFrog Artifactory, use the
appropriate service account credentials.

## How Dependency-Track Uses Repositories

Dependency-Track uses the Package URL (PURL) of each component to determine which
ecosystem it belongs to, then queries the matching repositories for the latest published
version. If the component's version is older than the latest, it is flagged as outdated.

!!! note
    Repository queries are used only for version currency checks. They are not part
    of the vulnerability analysis pipeline. Vulnerability data comes from the
    [internal analyzer](../analyzers.md) and the external analyzer integrations.

## Internal Components and Repositories

Components marked as [internal](internal-components.md) are only matched against
repositories that are also marked as internal. This prevents internal package
coordinates from being leaked to external registry APIs.
