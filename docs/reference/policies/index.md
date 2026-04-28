# Policies

Dependency-Track has two distinct policy types. Both check conditions written in
[CEL](../cel-expressions.md) against components and projects, but they act on different
subjects and produce different outputs.

* **[Component policies](component-policies.md)** raise *violations* against components that
  match a condition. Use them to encode acceptable licenses, banned components, age limits,
  and other organisational standards.
* **[Vulnerability policies](vulnerability-policies.md)** apply triage *analyses* to
  individual vulnerability findings. Use them to centralise suppression and rating overrides
  across the portfolio.

The two policy types share their CEL evaluation context and custom function library. See
[Condition expressions](condition-expressions.md) for variables, custom functions, and worked
examples that apply to both.

For background, see
[About component policies](../../concepts/component-policies.md) and
[About vulnerability policies](../../concepts/vulnerability-policies.md).
