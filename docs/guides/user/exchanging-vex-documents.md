# Exchanging VEX documents

Export a VEX to share your triage decisions with someone outside your Dependency-Track instance, or
import one to apply decisions to a project's findings in bulk. Both actions work from a project's
**Audit Vulnerabilities** tab.

Exporting requires one of the `VIEW_VULNERABILITY`, `VULNERABILITY_ANALYSIS`, or
`VULNERABILITY_ANALYSIS_READ` [permissions](../../reference/permissions.md). Importing requires
`VULNERABILITY_ANALYSIS` or `VULNERABILITY_ANALYSIS_UPDATE`.

For what a VEX asserts and how it differs from a VDR, see [About VEX](../../concepts/vex.md).

## Export decisions for a third party

1. Open the project and switch to the **Audit Vulnerabilities** tab.
2. Select **Export VEX** for a document that carries the analyses alone, or **Export VDR** for one
   that also carries the services and the dependency graph.

The file downloads as CycloneDX JSON. To automate the export, call the endpoints listed in
[VEX and VDR documents](../../reference/vex-and-vdr.md#export), which also records what each
document carries.

Before you send it, check what the recipient expects:

* If they need a document that resolves against an SBOM they already hold, no Dependency-Track
  export does that. Send yours as a standalone document, or produce a cross-linked one with another
  tool.
* If they need the composition of the product as well as the decisions, send the VDR. A VEX omits
  the services and the dependency graph, and describes each component only well enough to identify
  it.
* Suppressed findings are part of both documents, carrying the analysis that led to the
  suppression. Review those analyses before the file leaves your organization.

## Apply decisions from a VEX

Use this to accept a supplier's assessment, to replay decisions onto a new version of a project, or
to apply decisions your team recorded elsewhere.

1. Open the target project and switch to the **Audit Vulnerabilities** tab.
2. Select **Apply VEX**.
3. Choose the CycloneDX VEX file, then select **Upload**.

Dependency-Track applies each decision to findings that already exist, matching components by
identity rather than by the identifiers in the document, so a document exported from another project
applies here too. [About VEX](../../concepts/vex.md#what-an-import-changes) covers what an import
can and cannot change, and [VEX and VDR documents](../../reference/vex-and-vdr.md#import) records
the rules it follows.

Confirm the outcome on the **Audit Vulnerabilities** tab. Importing the analysis states
*False Positive*, *Not Affected*, or *Resolved* suppresses the findings it lands on, so toggle
**Show Suppressed** to see those. When a decision did not land,
[If nothing changed](#if-nothing-changed) lists the reasons.

## Author a VEX that takes effect

A hand-written VEX has to line up with the project in two places: the vulnerability it names, and
the components it points at. The examples that follow apply to a project created from this BOM:

```json linenums="1"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "metadata": {
    "component": {
      "bom-ref": "acme-app@1.0.0",
      "type": "application",
      "name": "acme-app",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "bom-ref": "jackson-databind@2.13.4",
      "type": "library",
      "group": "com.fasterxml.jackson.core",
      "name": "jackson-databind",
      "version": "2.13.4",
      "purl": "pkg:maven/com.fasterxml.jackson.core/jackson-databind@2.13.4"
    }
  ]
}
```

Vulnerability analysis has produced a finding for `CVE-2022-42003` on that component, and your team
has concluded that the vulnerable code is unreachable.

### Target one component

```json linenums="1"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "metadata": {
    "component": {
      "bom-ref": "product",
      "type": "application",
      "name": "acme-app",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "bom-ref": "affected-library",
      "type": "library",
      "group": "com.fasterxml.jackson.core",
      "name": "jackson-databind",
      "version": "2.13.4",
      "purl": "pkg:maven/com.fasterxml.jackson.core/jackson-databind@2.13.4"
    }
  ],
  "vulnerabilities": [
    {
      "id": "CVE-2022-42003",
      "source": { "name": "NVD" },
      "analysis": {
        "state": "not_affected",
        "justification": "code_not_reachable",
        "response": ["will_not_fix"],
        "detail": "The vulnerable deserialization path is unreachable from our entry points."
      },
      "affects": [{ "ref": "affected-library" }]
    }
  ]
}
```

Uploading that document to the project sets the finding on `jackson-databind` to *Not Affected*,
records the justification, response, and detail, and suppresses the finding. Four things made it
land:

1. **The upload chose the project.** The `metadata.component` in the document does not select it,
   and it does not have to describe your project. It matters only when a statement points at it.
2. **`affects[].ref` names an entry in the same document.** The value `affected-library` matches
   that entry's `bom-ref`. These names are local to the document. They need not match the BOM you
   uploaded, and Dependency-Track keeps no record of that BOM's names.
3. **The named entry matches a component in the project by identity.** The PURL matches, so the
   entry resolves to the project's `jackson-databind`. A CPE, a SWID tag ID, or group, name, and
   version together work as well, and a match on any one of them is enough. Version is part of the
   identity: `2.13.5` in the document matches nothing in a project that ships `2.13.4`.
4. **`id` names a vulnerability the project already has a finding for.** `source` is a hint, not a
   filter. When it names a source Dependency-Track knows, resolution starts there. Otherwise the ID
   alone has to identify the vulnerability. Name the source when Dependency-Track holds that ID from
   more than one source, because the name decides which of the resulting findings the decision
   reaches. An import never creates a finding, so Dependency-Track drops a statement about a
   vulnerability the project does not have.

### Broadcast one decision to every affected component

Keep the rest of the document unchanged, and point `affects[].ref` at the `bom-ref` of
`metadata.component` instead of at a component entry:

```json linenums="1"
  "vulnerabilities": [
    {
      "id": "CVE-2022-42003",
      "source": { "name": "NVD" },
      "analysis": {
        "state": "false_positive",
        "detail": "Reported against a component we repackage under a different name."
      },
      "affects": [{ "ref": "product" }]
    }
  ]
```

Every component in the project affected by `CVE-2022-42003` receives that decision, including
components the document does not list. Use this when the statement is about the product as a whole.

### If nothing changed

Dependency-Track logs the reason it skipped an entry. Unresolved vulnerabilities and unresolvable
references appear as warnings in the API server log. Entries without an analysis appear at debug
level. Check the log first, then this list:

* The project has no finding for that ID. Confirm it on the **Audit Vulnerabilities** tab.
* The ID exists in Dependency-Track under more than one source, and the entry names no source it
  recognizes. Name the source.
* The entry has no `analysis` object and no rating with `method: OWASP`. The importer drops those
  entries.
* `affects` is missing, empty, or names a `bom-ref` that no entry in the document declares.
* The component entry and the project's component share no identity. A PURL that differs in version
  or a partial set of group, name, and version matches nothing.

For the full set of matching rules and skip conditions, see
[VEX and VDR documents](../../reference/vex-and-vdr.md#import).
