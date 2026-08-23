# VEX and VDR documents

Dependency-Track exports a project's findings as a CycloneDX VEX or VDR, and imports CycloneDX VEX
documents to apply analysis decisions to existing findings. For the model behind these documents,
see [About VEX](../concepts/vex.md). For the CycloneDX documents Dependency-Track produces that
carry no analysis, see [File formats](file-formats.md#cyclonedx).

## Export

| | VEX | VDR |
|:-----------------------|:-------------------------------------------|:-------------------------------------------------------|
| Endpoint               | `GET /api/v1/vex/cyclonedx/project/{uuid}` | `GET /api/v1/bom/cyclonedx/project/{uuid}?variant=vdr` |
| `components`           | Only those with findings                   | Only those with findings                               |
| Component detail       | Identifying fields only                    | Full                                                   |
| `services`             | No                                         | Yes                                                    |
| `dependencies`         | No                                         | Yes                                                    |
| `vulnerabilities`      | Yes                                        | Yes                                                    |
| `analysis`             | Yes                                        | Yes                                                    |
| Serializations         | JSON                                       | JSON, or XML with `format=XML`                         |

Both endpoints accept a `version` query parameter that selects the CycloneDX specification version
of the output, and a `download` query parameter that returns the document as a file attachment.

The VEX endpoint requires one of the `VIEW_VULNERABILITY`, `VULNERABILITY_ANALYSIS`, or
`VULNERABILITY_ANALYSIS_READ` [permissions](permissions.md). The VDR variant requires one of those
three and `VIEW_PORTFOLIO`.

## Export contents

### Findings included

Both exports include suppressed findings. They exclude inactive findings, which no analyzer
reports anymore.

### Component entries

A VEX describes each component only well enough to identify it. Its entries in `components` carry
`type`, `group`, `name`, `version`, `purl`, `cpe`, `swid`, and `hashes`, and no other fields. The
VEX specifications count each of these as an identification method, hashes included.

A VEX omits the fields that describe rather than identify a component: `description`, `copyright`,
`scope`, `author`, `supplier`, `properties`, `licenses`, `externalReferences`, and `evidence`. A VDR
carries them.

### Vulnerability entries

Dependency-Track produces the entries in `vulnerabilities` as follows:

1. Group the findings by vulnerability and analysis, comparing the analysis on state,
   justification, response, and details.
2. Emit one entry in `vulnerabilities` per group.
3. Set the entry's `affects` node to the sorted, deduplicated references of the components in the
   group.
4. Add an `analysis` node to the entry.

### Identifiers

| Element                     | Value                                                             |
|:----------------------------|:------------------------------------------------------------------|
| `metadata.component.bom-ref` | The project UUID                                                  |
| `components[].bom-ref`      | The component UUID                                                 |
| `vulnerabilities[].affects[].ref` | A component UUID, resolvable within the same document        |

Entries in `vulnerabilities` carry no `bom-ref`, and exports do not use
[BOM-Link](https://cyclonedx.org/capabilities/bomlink/).

The UUIDs are Dependency-Track identifiers. They are stable across exports of the same project, and
they do not correspond to the `bom-ref` values of any BOM uploaded to the project.

### Analysis mapping

| Dependency-Track    | CycloneDX                                                    |
|:--------------------|:--------------------------------------------------------------|
| Analysis state      | `analysis.state`                                              |
| Justification       | `analysis.justification`                                      |
| Vendor response     | `analysis.responses`, as a single-element array               |
| Details             | `analysis.detail`                                             |
| Suppression         | Not emitted                                                   |

## Import

Two endpoints accept VEX uploads. `POST /api/v1/vex` takes a multipart form.
`PUT /api/v1/vex` takes a JSON body with the document Base64-encoded in a `vex` field, limited to
20,000,000 characters. Both identify the target project by UUID, or by name and version, and both
require the `VULNERABILITY_ANALYSIS` or `VULNERABILITY_ANALYSIS_UPDATE`
[permission](permissions.md).

Dependency-Track validates the document against the CycloneDX schema. Schema violations produce a
`400` response with problem details in RFC 9457 format.

An import applies analysis decisions to existing findings. It creates no components,
vulnerabilities, or findings.

### Skip conditions

Dependency-Track skips the entire upload when the document contains no `vulnerabilities`, or when
the target project has no vulnerabilities.

Dependency-Track skips an individual entry in `vulnerabilities` when any of the following applies:

| Condition                                                                  | Result                        |
|:---------------------------------------------------------------------------|:------------------------------|
| `id` is blank                                                              | Entry skipped, warning logged |
| `affects` is absent or empty                                               | Entry skipped                 |
| The entry has neither an `analysis` node nor a rating with `method: OWASP` | Entry skipped                 |
| The entry's vulnerability does not resolve                                 | Entry skipped, warning logged |

### Vulnerability resolution

The source of an entry acts as a hint rather than as a filter:

1. When `source.name` names a vulnerability source Dependency-Track knows, it looks for a
   vulnerability with that source and `id`. A match ends the resolution.
2. Otherwise, or when the first step finds nothing, `id` alone has to identify the vulnerability.
   Exactly one match resolves. More than one match means the ID does not identify a vulnerability
   on its own, and Dependency-Track skips the entry with a warning naming the competing sources.
   No match means the project is not affected, and Dependency-Track skips the entry with a warning.

The known vulnerability sources are `NVD`, `GITHUB`, `OSSINDEX`, `VULNDB`, `INTERNAL`, `OSV`,
`SNYK`, `CX`, and `JVN`.

The source decides only between vulnerabilities that share an ID. Dependency-Track can hold
`CVE-2020-1234` from both the NVD and OSV, which produces one finding per source on an affected
component. An entry naming one of those sources resolves to that vulnerability alone, and the
finding belonging to the other source keeps the analysis it had. An entry naming neither resolves to
nothing.

### Reference resolution

The importer indexes the metadata component and every entry in `components`, including nested
components, by `bom-ref`. Each value in `affects[].ref` resolves as follows:

| The reference resolves to           | Scope             | Applied to                                                        |
|:------------------------------------|:------------------|:-------------------------------------------------------------------|
| An entry in `components`            | Component-scoped  | Every component in the project matching that entry's identity      |
| The metadata component              | Project-scoped    | Every component in the project affected by the vulnerability       |
| Nothing, and the reference is a BOM-Link | Project-scoped | Every component in the project affected by the vulnerability      |
| Nothing else                        | Unresolvable      | Nothing. Dependency-Track logs a warning naming the reference      |

### Component identity matching

A component entry resolved from `affects[].ref` matches a component in the target project when any
of the following holds:

* The PURL matches in canonical form.
* The PURL coordinates match, meaning the PURL compared without qualifiers and subpath.
* The CPE matches.
* The SWID tag ID matches.
* Group, name, and version all match.

Matching covers the target project only, and can return more than one component. Every match
receives the analysis.

### Applied fields

| Source in the document      | Applied to the finding                    |
|:----------------------------|:-------------------------------------------|
| `analysis.state`            | Analysis state                             |
| `analysis.justification`    | Justification                              |
| `analysis.responses`        | Vendor response. The last entry wins        |
| `analysis.detail`           | Analysis details                           |
| Rating with `method: OWASP` | OWASP risk rating vector and score          |

CycloneDX states that Dependency-Track does not model, such as `resolved_with_pedigree`, arrive as
the analysis state *Not Set*.

Importing the analysis states *False Positive*, *Not Affected*, or *Resolved* also suppresses the
finding. No other state changes suppression.

Each applied decision appends an entry to the finding's audit history with the commenter
`CycloneDX VEX`.
