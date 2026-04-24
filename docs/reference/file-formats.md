# File Formats

## CycloneDX

Dependency-Track's primary file format is [CycloneDX](https://cyclonedx.org/), a
lightweight, security-focused Bill of Materials specification. CycloneDX is the only
format supported for **uploading** SBOMs to Dependency-Track.

Supported CycloneDX serialisations:

| Format | Content-Type |
|:-------|:-------------|
| JSON | `application/vnd.cyclonedx+json` |
| XML | `application/vnd.cyclonedx+xml` |

All versions of the CycloneDX BOM specification are supported for upload.

Dependency-Track also **generates** CycloneDX documents in several forms:

| Document type | Description |
|:-------------|:------------|
| BOM | A full software bill of materials reflecting the current component inventory of a project. |
| VEX | A Vulnerability Exploitability Exchange document containing analysis decisions (states, justifications) for a project's findings. |
| VDR | A Vulnerability Disclosure Report containing full vulnerability data for a project's components. |

## Finding Packaging Format (FPF)

The Finding Packaging Format (FPF) is a Dependency-Track-native JSON format for
exporting findings. It is used primarily to integrate with platforms that cannot
consume the REST API directly.

### Structure

An FPF document contains four top-level fields:

| Field | Description |
|:------|:------------|
| `version` | The FPF format version. |
| `meta` | Information about the Dependency-Track instance that generated the file. |
| `project` | Project metadata (name, version, UUID). |
| `findings` | Array of finding records, each linking a component to a vulnerability and including the current analysis state. |

Each finding record includes the affected component's coordinates, the vulnerability
details (ID, source, severity, CVSS vectors, CWEs), the current analysis state and
justification, and a matrix identifier that uniquely identifies the (project, component,
vulnerability) triple.

### API Endpoint

```text
GET /api/v1/finding/project/{uuid}/export
```

Requires the `VIEW_VULNERABILITY` permission.

### Version History

| FPF Version | Dependency-Track Version | Changes |
|:------------|:------------------------|:--------|
| v1.0 | Initial | Baseline format. |
| v1.1 | v4.5 | Added `cwes` array to support multiple CWEs per vulnerability. |
| v1.2 | v4.8.0 | Removed `allBySource` and internal `id` fields from aliases. |
| v1.3 | v4.14.0 | Added optional CVSS vectors (`cvssV2Vector`, `cvssV3Vector`, `cvssV4Vector`) and OWASP Risk Rating vector fields. |
