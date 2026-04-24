# Badges

Dependency-Track provides SVG badges that display a project's current vulnerability
and policy violation metrics. Badges can be embedded in README files, dashboards, or
internal documentation to give at-a-glance visibility into a project's security posture.

## Badge Types

### Vulnerable Components

Displays a severity breakdown of vulnerable components in the project. The badge shows
the highest severity present, or *no vulns* if no active findings exist.

Suppressed vulnerabilities are excluded from badge counts.

**By project name and version:**

```text
https://dtrack.example.com/api/v1/badge/vulns/project/{name}/{version}?apiKey={apiKey}
```

**By project UUID:**

```text
https://dtrack.example.com/api/v1/badge/vulns/project/{uuid}?apiKey={apiKey}
```

### Policy Violations

Displays the current policy violation state. Shows *violations* if any active (non-suppressed)
violations are present, or *no violations* otherwise.

**By project name and version:**

```text
https://dtrack.example.com/api/v1/badge/violations/project/{name}/{version}?apiKey={apiKey}
```

**By project UUID:**

```text
https://dtrack.example.com/api/v1/badge/violations/project/{uuid}?apiKey={apiKey}
```

## Embedding Badges

=== "Markdown"

    ```markdown
    ![Vulnerabilities](https://dtrack.example.com/api/v1/badge/vulns/project/my-app/1.0.0?apiKey=odt_...)
    ![Policy Violations](https://dtrack.example.com/api/v1/badge/violations/project/my-app/1.0.0?apiKey=odt_...)
    ```

=== "HTML"

    ```html
    <img src="https://dtrack.example.com/api/v1/badge/vulns/project/my-app/1.0.0?apiKey=odt_..." alt="Vulnerabilities">
    <img src="https://dtrack.example.com/api/v1/badge/violations/project/my-app/1.0.0?apiKey=odt_..." alt="Policy Violations">
    ```

## Access Configuration

Badge requests require authentication. Two approaches are available:

### API Key in URL

Pass the API key as a query parameter (`?apiKey={apiKey}`). This is the simplest
approach for static badge URLs embedded in documentation.

```text
https://dtrack.example.com/api/v1/badge/vulns/project/{uuid}?apiKey=odt_...
```

### API Key in Header

Pass the API key in the `X-Api-Key` request header. This is appropriate for server-side
badge proxies where the key should not appear in URLs.

```shell
curl -H "X-Api-Key: odt_..." \
  "https://dtrack.example.com/api/v1/badge/vulns/project/{uuid}"
```

## Required Permission

The API key (or the team it belongs to) must have the `VIEW_BADGES` permission.

Dependency-Track creates a default **Badge Viewers** team with this permission and a
pre-generated API key on first startup. You may use this key for badge access, but
rotate it before going to production.

!!! warning
    API keys in badge URLs are visible to anyone who can view the source of the page
    embedding them. Use a dedicated, low-privilege API key with only the `VIEW_BADGES`
    permission for this purpose, and avoid reusing keys from more privileged teams.
