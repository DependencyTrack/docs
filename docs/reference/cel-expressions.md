# CEL Expressions

Dependency-Track uses the [Common Expression Language] (CEL) in two places:

* **Policy conditions**, evaluated against components or vulnerabilities to drive
  policy violations and analyses. See
  [Condition expressions](policies/condition-expressions.md).
* **Notification filters**, evaluated against notification subjects to control
  which notifications are dispatched. See
  [Filter expressions](notifications/filter-expressions.md).

The two contexts share the syntax described on this page, but expose **different
variables, types, and custom functions**. The custom functions documented for
policies (for example `depends_on`, `spdx_expr_allows`) are not available to
notification filters, and the variables differ entirely. Refer to the
context-specific page for the available inputs and functions.

## Syntax

The CEL syntax is similar to other [C-style languages] like Java and JavaScript.
However, CEL is not [Turing-complete]. As such, it does *not* support constructs like `if` statements or loops (that is, `for`, `while`).

As a compensation for missing loops, CEL offers [macros] like `all`, `exists`, `exists_one`, `map`, and `filter`.
Refer to the [macros] documentation for more details.

CEL syntax is described thoroughly in the official [language definition].

## Standard library

Both contexts have access to the [standard definitions] of the CEL specification and the
[CEL strings extension], which adds functions like `charAt`, `indexOf`, `join`, `lowerAscii`,
`replace`, `split`, `substring`, `trim`, and `upperAscii`.

The policy context registers additional custom functions (`depends_on`, `spdx_expr_allows`,
and so on); see [Condition expressions](policies/condition-expressions.md#function-reference).
Notification filters do not register any custom functions.

## Optional field checking

CEL does not have a concept of `null`. Accessing a field that is not set
returns its default value (for example, `""` for strings, `0` for numbers, `false` for booleans),
which can lead to misleading matches. Use the `has()` macro to check for field presence
before accessing it:

```js linenums="1"
has(obj.field) && obj.field == "value"
```

The pattern applies in both contexts. The exact root variables (`component`, `subject`,
and so on) are documented on the context-specific reference pages linked above.

[C-style languages]: https://en.wikipedia.org/wiki/List_of_C-family_programming_languages
[CEL strings extension]: https://github.com/google/cel-spec/blob/master/doc/extensions/strings.md
[Common Expression Language]: https://cel.dev/
[Turing-complete]: https://en.wikipedia.org/wiki/Turing_completeness
[language definition]: https://github.com/google/cel-spec/blob/v0.13.0/doc/langdef.md#language-definition
[macros]: https://github.com/google/cel-spec/blob/v0.13.0/doc/langdef.md#macros
[standard definitions]: https://github.com/google/cel-spec/blob/v0.13.0/doc/langdef.md#list-of-standard-definitions
