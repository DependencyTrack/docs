# Badges

Dependency-Track provides SVG badges that display a project's current vulnerability
and policy violation metrics. Badges can be embedded in README files, dashboards, or
internal documentation to give at-a-glance visibility into a project's security posture.

Badge URLs reference a project by UUID, by `(name, version)`, or by name alone. The
name-only form resolves to whichever version carries the latest-version flag. See
[Managing project versions](../guides/user/managing-project-versions.md#mark-a-version-as-latest).

## Badge Types

### Vulnerable Components

Displays a severity breakdown of vulnerable components in the project. The badge shows
the highest severity present, or *no vulns* if no active findings exist.

Suppressed vulnerabilities are excluded from badge counts.

**By project name and version:**

```text
https://dtrack.example.com/api/v1/badge/vulns/project/{name}/{version}
```

**By project UUID:**

```text
https://dtrack.example.com/api/v1/badge/vulns/project/{uuid}
```

### Policy Violations

Displays the current policy violation state. Shows *violations* if any active (non-suppressed)
violations are present, or *no violations* otherwise.

**By project name and version:**

```text
https://dtrack.example.com/api/v1/badge/violations/project/{name}/{version}
```

**By project UUID:**

```text
https://dtrack.example.com/api/v1/badge/violations/project/{uuid}
```

## Embedding Badges

=== "Markdown"

    ```markdown
    ![Vulnerabilities](https://dtrack.example.com/api/v1/badge/vulns/project/my-app/1.0.0)
    ![Policy Violations](https://dtrack.example.com/api/v1/badge/violations/project/my-app/1.0.0)
    ```

=== "HTML"

    ```html
    <img src="https://dtrack.example.com/api/v1/badge/vulns/project/my-app/1.0.0" alt="Vulnerabilities">
    <img src="https://dtrack.example.com/api/v1/badge/violations/project/my-app/1.0.0" alt="Policy Violations">
    ```
