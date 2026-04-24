# National Vulnerability Database (NVD)

The [National Vulnerability Database](https://nvd.nist.gov/) (NVD) is the largest
publicly available source of vulnerability intelligence, maintained by NIST and building
on CVE identifiers from MITRE. It contains over 200,000 CVE records spanning from the
early nineties to the present day.

!!! note
    This product uses the NVD API but is not endorsed or certified by the NVD.

## What It Provides

The NVD mirror populates Dependency-Track's internal database with CVE records including
descriptions, CVSS scores, CWE classifications, and affected product configurations
expressed as CPE. The [internal analyzer](../analyzers.md#internal) uses this data
to match components with valid CPEs against known vulnerabilities.

## Mirroring

Dependency-Track mirrors the NVD via the NVD REST API. The mirror refreshes daily and
on instance startup. The initial mirror may take significantly longer than subsequent
incremental updates.

The mirroring schedule is controlled by
[`dt.task.nist.mirror.cron`](../configuration/properties.md#dttasknistmirrorcron).

## Configuration

NVD mirroring is configured through the administration UI under
**Administration → Datasources → NVD**.

| Setting | Description |
|:--------|:------------|
| Enabled | Whether NVD mirroring is active. Enabled by default. |
| NVD API Key | Optional but strongly recommended. Unauthenticated requests are rate-limited aggressively, which can cause the initial mirror to take hours or fail. |

Obtain a free NVD API key at [nvd.nist.gov/developers/request-an-api-key](https://nvd.nist.gov/developers/request-an-api-key).

!!! tip
    Configuring an API key is especially important for new installations, where
    the entire NVD dataset must be downloaded on the first mirror run.

## CPE Matching

NVD records describe affected products using CPE (Common Platform Enumeration).
Dependency-Track follows the NIST CPE name matching specification with adjustments
to reduce false positives: matches are rejected when the vendor comparison yields
*SUBSET* and the product comparison yields *SUPERSET*, or vice versa.

Components without a valid CPE are not evaluated by the internal analyzer against
NVD data. Ensure your SBOMs include CPEs for non-open-source components.
