# About component policies

Component policies let organizations encode the standards that third-party components must meet,
and surface a *violation* every time a component falls short. Typical use cases include banning
copyleft licenses, requiring components to be no more than a few years old, blocking specific
package coordinates, or asserting that nothing is more than a major version behind its upstream.

Whereas a [vulnerability policy](vulnerability-policies.md) acts on a single vulnerability finding
and applies an analysis to it, a component policy acts on the component itself. The two are
complementary: use component policies to express what an acceptable component looks like; use
vulnerability policies to centralize triage decisions for individual findings. Both share the same
expression language, evaluation context, and custom function library. See
[Condition expressions](../reference/policies/condition-expressions.md) for details.

## What a violation means

A violation is a fact recorded against a `(component, project, condition)` triple. Every violation
inherits the policy's *violation state*: `INFO`, `WARN`, or `FAIL`. The state propagates into project
metrics, project badges, and the [`POLICY_VIOLATION` notification group](../reference/notifications/groups.md).
Organizations typically use a `FAIL` violation to break a CI/CD pipeline.

Violations are open to audit. Each one supports suppression, comments, and an analysis state, just
like a vulnerability finding. The audit trail lives with the violation and persists across
re-evaluations.

The available analysis states are `APPROVED`, `REJECTED`, and `NOT_SET`. Dependency-Track does not
attach a fixed meaning to `APPROVED` or `REJECTED`; the convention is for the team to settle. Two
common ones are *risk-acceptance* (`APPROVED` records that the team accepts the violation, paired
with suppression) and *workflow* (`APPROVED` records an actionable violation and `REJECTED` a
non-actionable one). Pick one and document it.
[Triaging policy violations](../guides/user/triaging-policy-violations.md) explains how to set an
analysis state.

## How a policy decides

A policy carries one or more *conditions* and an operator that combines them. With operator `ANY`,
a single matching condition raises a violation; with `ALL`, every condition must match.

Conditions describe what to look at. The built-in subjects fall into three families:

- **License** subjects (`LICENSE`, `LICENSE_GROUP`) match on the component's resolved license or its
  membership in a license group.
- **Operational** subjects (coordinates, package URL, hash, age, version, version-distance, SWID tag)
  match on the component's identity and lifecycle.
- **Security** subjects (severity, CPE, CWE, EPSS score, vulnerability identifier) match on the
  component's vulnerabilities.

For anything that the built-in subjects cannot express, a policy can use the *Expression* subject:
a [CEL](../reference/cel-expressions.md) expression evaluated against the component, the project,
the component's vulnerabilities, and the current time. This is the same expression language used by
vulnerability policies, with the same custom functions
([`spdx_expr_allows`](../reference/policies/condition-expressions.md#spdx_expr_allows),
[`is_dependency_of`](../reference/policies/condition-expressions.md#is_dependency_of),
[`matches_range`](../reference/policies/condition-expressions.md#matches_range),
[`version_distance`](../reference/policies/condition-expressions.md#version_distance), and others).
Expression conditions let an organization encode rules that combine component fields, traverse the
dependency graph, or operate on SPDX license expressions directly.

## Where a policy applies

By default, a policy applies to every project in the portfolio. Narrow it to specific projects, to
descendants of those projects, or to projects carrying specific
[tags](tags.md). Scoping is flat: a policy
either applies to a project or does not. See
[Component policies › Assignment](../reference/policies/component-policies.md#assignment) for the
exact rules.

## Lifecycle

Project analysis evaluates policies whenever a BOM lands, during the recurring scheduled portfolio
analysis, and on a manual trigger. Each run reconciles violations against the current state of the
project: new matches become violations and emit notifications; the engine deletes prior violations
that no longer match. This makes a policy safe to author incrementally: tightening a license
allow-list adds violations, loosening it removes them, and the audit trail reflects both.

!!! warning "Policy edits do not take effect immediately"
    Saving or editing a policy does not re-run analysis in the moment. Existing violations stay
    until the next project analysis on each project, which runs on the next BOM upload, on the
    next scheduled portfolio analysis, or on a manual trigger.

!!! note "Asynchronously populated data"
    Some condition inputs come from data that Dependency-Track resolves from external sources after
    analysis starts: the component's publication date, its latest known version, EPSS scores, and
    vulnerability metadata. On the first evaluation of a freshly uploaded BOM, these fields may
    still be empty, and conditions that read them (`AGE`, `VERSION_DISTANCE`, `EPSS`, and
    expressions referencing the same data) do not match. They begin to match on the next
    evaluation, once the background tasks complete. Plan release-gating policies accordingly.

## License groups

A license group names a collection of licenses (for example, *Copyleft* or *Permissive*); the
platform seeds the common ones, and operators can extend them. Groups make license policies
readable (*"License is in Copyleft"* rather than enumerating dozens of identifiers). Richer rules,
such as SPDX expressions with `OR` and `WITH` operators or version-aware matching, use `Expression`
conditions with
[`spdx_expr_allows`](../reference/policies/condition-expressions.md#spdx_expr_allows).

## Further reading

- [Managing component policies](../guides/user/managing-component-policies.md) for the procedures.
- [Component policies reference](../reference/policies/component-policies.md) for field definitions
  and the full subject/operator matrix.
- [Condition expressions](../reference/policies/condition-expressions.md) for CEL variables,
  custom functions, and worked examples.
- [Creating a component policy](../tutorials/creating-a-component-policy.md) for a guided walkthrough.
- [About vulnerability policies](vulnerability-policies.md) for the complementary policy type.
