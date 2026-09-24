# Rating a finding in context

In this tutorial, we will give one vulnerability two different OWASP risk ratings in two projects,
and watch each rating land on its finding.

Severity comes from the vulnerability and says nothing about where we run the affected component.
A VEX can carry an [OWASP risk rating](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
instead of an analysis decision, so the same component can be risky in one deployment and harmless
in another. We will write one document for an internet-facing service and one for a nightly batch
job.

## What we need

- A running Dependency-Track stack from the [Quick start](quickstart.md), version 5.1.0 or later.
- The `PORTFOLIO_MANAGEMENT`, `BOM_UPLOAD`, `VULNERABILITY_MANAGEMENT`, `VULNERABILITY_ANALYSIS`,
  `VIEW_PORTFOLIO`, and `VIEW_VULNERABILITY` [permissions](../reference/permissions.md).
  The `admin` account has all six.

We will build everything else as we go, so we do not have to wait for a vulnerability mirror.

## Creating the two projects

We open **Projects**, select **Create Project**, and create `checkout-api` with version `1.0.0`.
We repeat this for `nightly-report`, also version `1.0.0`.

Both projects will hold the same component, and only the risk we record differs.

## Uploading the same BOM to both projects

```json title="billing.cdx.json" linenums="1"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "components": [
    {
      "bom-ref": "billing-lib@1.4.2",
      "type": "library",
      "group": "com.example",
      "name": "billing-lib",
      "version": "1.4.2",
      "purl": "pkg:maven/com.example/billing-lib@1.4.2"
    }
  ]
}
```

We open `checkout-api`, switch to the **Components** tab, select **Upload BOM**, and choose the
file. We do the same for `nightly-report`. Each project now holds one component and no findings.

## Creating a vulnerability that affects the component

We need a finding to rate, and we write the vulnerability ourselves so that this tutorial produces
the same result on every instance.

We open **Vulnerabilities** and select **Create Vulnerability**:

| Field            | Value                                       |
|------------------|---------------------------------------------|
| Vulnerability ID | `INT-BILLING-0001`                          |
| Title            | `Incorrect pattern matching in billing-lib` |
| Severity         | `Medium`                                    |

On the **Affected Components** tab, we select the **+** icon and enter:

| Field           | Value                                       |
|-----------------|---------------------------------------------|
| Identifier Type | `Package URL (PURL)`                        |
| Identifier      | `pkg:maven/com.example/billing-lib@1.4.2`   |
| Version Type    | `Exact`                                     |

The version travels inside the PURL. Dependency-Track drops a PURL it cannot parse without
reporting an error, so the identifier has to match what the BOM declares.

After saving, we return to each project and select **Reanalyze** on the **Audit Vulnerabilities**
tab. Within a few seconds both projects show one finding for `INT-BILLING-0001`, each with severity
*Medium*. We refresh the tab if the finding has not appeared yet.

Both projects carry the same severity, which our two documents will now qualify.

## Writing the two VEX documents

Each document names the vulnerability and points at the product as a whole, so `affects[].ref`
carries the `bom-ref` of `metadata.component`. See
[About VEX](../concepts/vex.md#what-an-import-changes) for what an import can and cannot change.

```json title="vex-checkout-api.json" linenums="1"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "metadata": {
    "component": {
      "bom-ref": "product",
      "type": "application",
      "name": "checkout-api",
      "version": "1.0.0"
    }
  },
  "vulnerabilities": [
    {
      "id": "INT-BILLING-0001",
      "source": { "name": "INTERNAL" },
      "ratings": [
        {
          "method": "OWASP",
          "vector": "OWASP/SL:9/M:9/O:9/S:9/ED:9/EE:9/A:9/ID:9/LC:7/LI:7/LAV:7/LAC:7/FD:7/RD:7/NC:7/PV:7",
          "score": 63.0
        }
      ],
      "affects": [{ "ref": "product" }]
    }
  ]
}
```

The first eight factors describe how likely an attack is and the last eight what it costs us, and
the score is those two averages multiplied, out of 81. `checkout-api` takes traffic from the
internet and handles payments, so both halves run high.

Only the rating changes in the second document. The product name follows the project it describes,
but `metadata.component` never selects the target: the upload does.

```json title="vex-nightly-report.json" linenums="1"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "metadata": {
    "component": {
      "bom-ref": "product",
      "type": "application",
      "name": "nightly-report",
      "version": "1.0.0"
    }
  },
  "vulnerabilities": [
    {
      "id": "INT-BILLING-0001",
      "source": { "name": "INTERNAL" },
      "ratings": [
        {
          "method": "OWASP",
          "vector": "OWASP/SL:1/M:1/O:0/S:2/ED:1/EE:1/A:1/ID:1/LC:2/LI:1/LAV:1/LAC:1/FD:1/RD:1/NC:2/PV:3",
          "score": 1.5
        }
      ],
      "affects": [{ "ref": "product" }]
    }
  ]
}
```

Neither document carries an `analysis` object, and a rating with `method: OWASP` is enough on its
own.

## Applying each document to its project

We open `checkout-api`, select **Apply VEX**, choose `vex-checkout-api.json`, and select
**Upload**. We repeat this on `nightly-report` with `vex-nightly-report.json`.

## Comparing the results

We open the finding for `INT-BILLING-0001` in `checkout-api` and expand it. A field labeled
**OWASP RR Vector** now holds the vector we sent. The **Audit Trail** records both values:

```text linenums="1"
OWASP Vector: (None) → OWASP/SL:9/M:9/O:9/S:9/ED:9/EE:9/A:9/ID:9/LC:7/LI:7/LAV:7/LAC:7/FD:7/RD:7/NC:7/PV:7
OWASP Score: (None) → 63.0
```

The same finding in `nightly-report` carries the other vector, and a score of `1.5`.

One vulnerability, one component, two deployments, two ratings. The severity stayed *Medium* in
both projects: an imported rating sits beside the severity rather than replacing it.

## What's next

- [Exchanging VEX documents](../guides/user/exchanging-vex-documents.md): export decisions, and
  target individual components rather than the product.
- [VEX and VDR documents](../reference/vex-and-vdr.md#import): the rules an import follows, and why
  it skips an entry.
- [Community integrations](../reference/community-integrations.md): tools that produce these
  documents for you.
