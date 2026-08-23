# About VEX

A VEX document states whether a vulnerability that exists in a product is exploitable in that
product. Dependency-Track both produces and consumes VEX documents in
[CycloneDX](https://cyclonedx.org/capabilities/vex/) format. Exporting one turns the analyses on a
project's [findings](vulnerability-findings.md) into a document you can hand to a third party, such
as a consumer of your software, an auditor, or another team, without giving them access to your
instance. Importing one applies analysis decisions to your own findings in bulk.

## The product and the component

VEX has two levels. The [CISA requirements for VEX](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf)
call them the *product*, which the status is about, and the *subcomponent*, the thing inside the
product where the vulnerability originates.

<!-- vale off -->
!!! quote "CISA Minimum Requirements for VEX, §2.5.2"
    A VEX statement asserts the [status] of [product_id] with respect to [vul_id]. A VEX statement MAY
    also convey that [subcomponent_id] is included in [product_id]. A common VEX use case is to convey
    that [subcomponent_id] is "affected" by [vul_id] while [product_id] is "not_affected" by [vul_id].
<!-- vale on -->

Dependency-Track records both levels already. An analysis belongs to exactly one project, one
component, and one vulnerability. A finding with the analysis state *Not Affected* says that the
project is not affected by the vulnerability, and that the vulnerability originates in the component
the finding names.

CycloneDX expresses the two levels through the structure of the document rather than through named
fields:

| VEX element  | CycloneDX                                                         | Dependency-Track   |
|:-------------|:------------------------------------------------------------------|:-------------------|
| Product      | The component described in the document metadata                  | The project        |
| Subcomponent | A component entry that a vulnerability's `affects` node points at | The component      |
| Status       | The `analysis` node of a vulnerability entry                      | The analysis state |

*Subcomponent* is a specification term. Dependency-Track calls it a component, and so does the rest
of this page.

## VEX and VDR

Dependency-Track builds both document types from the same findings, and they answer different
questions.

A **VEX** reports what your team concluded about a set of vulnerabilities. It contains the
components that have findings, the vulnerabilities affecting them, and the analysis recorded for
each. It leaves out services and the dependency graph, because a reader of a VEX cares about the
decisions rather than about the composition of the product.

A VEX also describes each component more sparsely than the other exports do. It carries the fields
that identify a component, such as the name, version, PURL, CPE, and hashes, and leaves out the
fields that only describe it, such as licenses, supplier, and evidence. A VEX travels
further than the SBOM it came from, and its recipient needs enough to match each component rather
than a full account of it.

A **VDR** reports everything you know about a product's vulnerabilities. It contains the same
findings and analyses, plus the services and the dependency graph, so the reader can see where an
affected component sits in the product. The document follows the vulnerability disclosure report
defined in NIST SP 800-161.

An inventory export that carries vulnerabilities is neither of the two. It lists every component and
the vulnerabilities affecting it, without any analysis, reporting what the analyzers found rather
than what your team concluded. The
[VEX and VDR documents reference](../reference/vex-and-vdr.md#export) records exactly what a VEX and
a VDR contain.

Both formats capture a decision as it stood on the day of the export.
[Vulnerability policies](vulnerability-policies.md) solve the adjacent problem of applying a
decision continuously as the portfolio changes.

## One statement per decision

An exported document does not emit one entry per finding. Findings that share a vulnerability and
carry the same analysis collapse into a single entry whose `affects` node lists every component
concerned. The specifications require this shape:

<!-- vale off -->
!!! quote "CISA Minimum Requirements for VEX, §3.1.2"
    A VEX statement MAY reference more than one product as long as [status], [vul_id], and other VEX
    information are correct for the complete set of products. If status or other VEX information
    changes for a subset of products, additional VEX statements MUST be created for the respective
    subset.
<!-- vale on -->

One vulnerability affecting five components that share an analysis produces one entry with five
references. If two of those components carry a different analysis, the export produces two entries,
one for each decision.

## Identifiers travel with the document

The references inside an exported document are Dependency-Track's own component identifiers. They
resolve to component entries in the same document, and they stay the same across exports of the
same project.

They are not the identifiers from any BOM you uploaded. Dependency-Track keeps no record of the
references a BOM used, so a consumer cannot correlate an exported VEX with the BOM that created the
project by identifier alone.

Nor does an export use [BOM-Link](https://cyclonedx.org/capabilities/bomlink/), the CycloneDX
mechanism for pointing at a component in a separate document. A Dependency-Track VEX is
self-contained: every reference it makes resolves inside itself. Consumers that expect a VEX to
link to an SBOM they already hold, which is how some third-party scanners match the two documents,
cannot resolve it that way.

## What an import changes

An imported VEX applies analysis decisions to findings that already exist. It never creates
components, vulnerabilities, or findings. A statement about a vulnerability the project is not
affected by has nothing to apply to, and Dependency-Track skips it.

A statement reaches a finding on the strength of the vulnerability ID. The source a statement names
narrows the search when Dependency-Track recognizes it, and otherwise steps aside, because the same
vulnerability reaches different organizations through different sources. An assessment written
against one source applies to your record of the same vulnerability from another.

The source earns its keep when the same ID arrives from more than one source, which leaves the
component with one finding per source. A statement that names a source lands on that source's
finding and leaves its sibling untouched, and a statement that names none lands nowhere, because
Dependency-Track does not choose between them on your behalf.

Components resolve by identity rather than by identifier. A VEX exported from one project applies to
another project that ships the same components, and a document authored by a supplier applies to
your project without either side agreeing on identifiers first.

A statement that targets the product rather than an individual component is a bulk operation. It
carries one decision to every component in the project affected by that vulnerability.

Three analysis states carry a side effect. Importing *False Positive*, *Not Affected*, or
*Resolved* also [suppresses](vulnerability-findings.md#suppression) the finding, which removes it
from the project's metrics until someone clears the suppression.

## Further reading

* [Exchanging VEX documents](../guides/user/exchanging-vex-documents.md): how to export a document
  and how to apply one.
* [VEX and VDR documents](../reference/vex-and-vdr.md): the exact contents of each document and
  the rules an import follows.
