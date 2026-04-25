# Vulnerability Policies

For background on what vulnerability policies are and how evaluation works, see
[Concepts: Vulnerability Policies](../../concepts/vulnerability-policies.md).
For step-by-step procedures, see
[Managing Vulnerability Policies](../../guides/user/managing-vulnerability-policies.md).

## Policy Sources

| Source | How it is managed                                    | Editable |
|:-------|:-----------------------------------------------------|:---------|
| User   | Created and edited directly in Dependency-Track      | Yes      |
| Bundle | Synchronised from a remote ZIP archive of YAML files | No       |

Policy names are globally unique across user-managed and bundle-managed policies.

## Operation Modes

| Mode     | Behaviour                                                                                            |
|:---------|:-----------------------------------------------------------------------------------------------------|
| Apply    | Apply the analysis and ratings to the finding. This is the default.                                  |
| Log      | Record that the policy matched, but do not modify the finding. Useful for validating a new policy.   |
| Disabled | The policy is not evaluated at all.                                                                  |

## Condition Variables

Conditions are written in [CEL](../cel-expressions.md). A vulnerability policy is scoped to a
single vulnerability, exposed as the `vuln` variable. Standard component policies, in contrast,
expose a list of vulnerabilities as `vulns`, so constructs like `vulns.exists(...)` become direct
field accesses such as `vuln.id == "CVE-2022-41852"`. The `component`, `project`, `now` variables
and all custom functions are identical across both policy types.

See [Condition expressions](./condition-expressions.md) for the complete list of variables,
custom functions, and worked examples.

## Analysis Fields

When a policy matches in *Apply* mode, the following analysis fields are applied to the finding:

* **State** (required). One of `EXPLOITABLE`, `IN_TRIAGE`, `FALSE_POSITIVE`, `NOT_AFFECTED`, `RESOLVED`.
* **Justification**. Only applicable when the state is `NOT_AFFECTED`. Follows the CycloneDX VEX values
  (for example `CODE_NOT_REACHABLE`, `PROTECTED_BY_MITIGATING_CONTROL`).
* **Vendor response**. The response communicated to consumers (`CAN_NOT_FIX`, `WILL_NOT_FIX`, `UPDATE`,
  `ROLLBACK`, `WORKAROUND_AVAILABLE`).
* **Details**. Free-form text explaining the analysis.
* **Suppress**. Whether to suppress the finding.

## Ratings

Up to three ratings may be attached to a policy. Each rating specifies a method (`CVSSv2`, `CVSSv3`,
`CVSSv4`, `OWASP`), a severity, and optionally a score and vector.

## Bundle Configuration

| Property                                                                                                                                     | Description                                         |
|:---------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------|
| [`dt.vulnerability.policy.bundle.url`](../configuration/properties.md#dtvulnerabilitypolicybundleurl)                           | HTTP(S) URL of the bundle ZIP                       |
| [`dt.vulnerability.policy.bundle.auth.username`](../configuration/properties.md#dtvulnerabilitypolicybundleauthusername)        | Basic-auth username                                 |
| [`dt.vulnerability.policy.bundle.auth.password`](../configuration/properties.md#dtvulnerabilitypolicybundleauthpassword)        | Basic-auth password                                 |
| [`dt.vulnerability.policy.bundle.auth.bearer.token`](../configuration/properties.md#dtvulnerabilitypolicybundleauthbearertoken) | Bearer token, used when no basic-auth is configured |
| [`dt.task.vulnerability-policy-bundle-sync.cron`](../configuration/properties.md#dttaskvulnerability-policy-bundle-synccron)    | Cron expression for the scheduled sync              |

## Bundle Layout

A bundle is a plain ZIP archive of YAML files at the root. File names must end in `.yaml` or `.yml` and
must not start with `.` or `_`. Non-YAML files are ignored.

```text
bundle.zip
├── cve-2022-41852.yaml
└── spring-cloud-suppressions.yaml
```

The following size limits apply:

* The bundle ZIP must not exceed 10 MiB.
* It may contain at most 1000 entries.
* Each individual YAML file must not exceed 1 MiB.

## Policy File Format

Each YAML file contains a single policy. The schema is validated on every sync. If any policy in the bundle
fails to validate, the entire bundle is rejected and the database is left untouched.

??? example "Example policy file: `cve-2022-41852.yaml`"

    ```yaml linenums="1"
    apiVersion: v1.0
    type: Vulnerability Policy
    name: Spring Cloud CVE-2022-41852 Suppression
    description: |-
      Suppresses occurrences of CVE-2022-41852 in commons-jxpath,
      when commons-jxpath is introduced through Spring Cloud.
    operationMode: APPLY
    author: Jane Doe
    condition: |-
      vuln.id == "CVE-2022-41852"
        && component.name == "commons-jxpath"
        && component.is_dependency_of(v1.Component{
             group: "org.springframework.cloud",
             version: "vers:maven/>3.1|<3.3"
           })
    analysis:
      state: NOT_AFFECTED
      justification: CODE_NOT_REACHABLE
      details: |-
        It was determined that CVE-2022-41852 is not exploitable in Spring Cloud
        components, because the vulnerable code is not used.
      suppress: true
    ```

| Field           | Required | Description                                                                  |
|:----------------|:---------|:-----------------------------------------------------------------------------|
| `apiVersion`    | Yes      | Schema version. Currently `v1.0`.                                            |
| `type`          | Yes      | Must be the literal string `Vulnerability Policy`.                           |
| `name`          | Yes      | Globally unique policy name.                                                 |
| `description`   | No       | Short description, up to 512 characters.                                     |
| `author`        | No       | Free-form author identifier.                                                 |
| `validFrom`     | No       | RFC 3339 timestamp. The policy is inactive before this instant.              |
| `validUntil`    | No       | RFC 3339 timestamp. The policy is inactive after this instant.               |
| `condition`     | Yes      | CEL expression.                                                              |
| `analysis`      | Yes      | Analysis to apply on match. See [Analysis Fields](#analysis-fields).         |
| `ratings`       | No       | Up to 3 rating overrides. See [Ratings](#ratings).                           |
| `operationMode` | No       | `APPLY` (default), `LOG`, or `DISABLED`. See [Operation Modes](#operation-modes). |
| `priority`      | No       | Integer between 0 and 100. Higher values are evaluated first. Defaults to 0. |

## Sync Behaviour

Each sync reconciles the bundle with the database:

* Policies present in the bundle but absent from the database are *created*.
* Policies present in both are *updated* in place.
* Policies previously synced from the bundle but no longer present are *deleted*. Any analyses applied
  by those policies are reset and an audit trail entry is recorded.
* User-managed policies are never touched, regardless of whether they appear in the bundle.

A sync is aborted without any database changes when:

* The bundle exceeds the size or entry limits.
* The ZIP is malformed, or the bundle file is not reachable.
* Any policy file fails schema validation or its CEL condition fails to compile.
* The bundle contains two policies with the same `name`.
* The bundle introduces a policy whose `name` already exists as a user-managed policy.

The last failure reason is surfaced in the *Bundles* view so that operators can diagnose sync issues
without needing access to the server logs.
