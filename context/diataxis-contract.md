# Diataxis Contract

The documentation follows the [Diataxis](https://diataxis.fr/) framework.
Content is organized along two axes:

- **Practical vs. Theoretical**: Is this about doing, or about understanding?
- **Acquisition vs. Application**: Is the reader learning something new, or applying existing knowledge?

This yields four documentation types, each with a distinct purpose and voice.

## Tutorials

Learning-oriented, narrative walkthroughs. The reader is a **student** acquiring
new skills through guided, hands-on activity. The author is a **tutor** who bears
full responsibility for the student's success.

### Principles

- Show direction upfront: state what the reader will accomplish.
- Deliver visible results early and often.
- Maintain narrative flow; confirm progress with expected outputs.
- Minimize explanation — link to Concepts instead.
- Stay concrete: specific actions and results, no abstractions.
- Avoid choices: one path, no alternatives or options.
- Ensure reliability: every step must produce the promised result.
- Use "we" to affirm the tutor-learner partnership.

### What belongs here

- "Getting started with Dependency-Track" — install, first BOM upload, first
  vulnerability review.
- "Your first policy violation" — create a policy, upload a BOM that violates it,
  observe the result.
- "Setting up notifications" — configure an alert destination, trigger a
  notification, verify delivery.

### What does NOT belong here

- Exhaustive configuration options (→ Reference).
- Explanation of *why* a feature exists or how it works internally (→ Concepts).
- Procedures for experienced users solving a specific problem (→ Guides).

---

## Guides

Task-oriented, goal-first procedures. The reader **already knows what they want**
and has baseline competence. The guide helps them accomplish a specific task
correctly and safely.

### Principles

- Focus on the goal; omit everything that doesn't serve it.
- Assume domain competence — don't teach prerequisites.
- Use conditional imperatives: "If you want X, do Y."
- Choose titles that match search intent (verb-first: "Configure...",
  "Integrate...", "Migrate...").
- Sequence steps logically; anticipate the reader's workflow.
- Reference external docs (Reference, Concepts) instead of inlining detail.

### What belongs here

- "Deploying Dependency-Track behind a reverse proxy"
- "Integrating with GitHub Actions / GitLab CI / Jenkins"
- "Configuring OIDC authentication"
- "Tuning the analyzer for air-gapped environments"
- "Upgrading from v4.x to v5.x" (lives in `guides/upgrading/`)

### What does NOT belong here

- Step-by-step beginner introductions (→ Tutorials).
- Exhaustive parameter listings (→ Reference).
- Design rationale or architectural background (→ Concepts).
- REST endpoints or configuration property keys when the procedure is UI-driven (→ Surface language).

---

## Concepts

Understanding-oriented background material. The reader wants to **deepen and
broaden** their mental model. This is documentation you read *away from* the
product.

### Principles

- Take a higher, wider perspective than the other sections.
- Build connections between topics; weave a web of understanding.
- Provide context: design decisions, history, trade-offs, alternatives.
- Opinion and perspective are appropriate — acknowledge alternatives.
- Titles should read naturally prefixed with "About": "About vulnerability
  analysis", "About policy evaluation".
- Keep instructional steps and technical parameter listings out.

### What belongs here

- How Dependency-Track models the software supply chain (components, projects,
  BOMs, services).
- How vulnerability analysis works (data sources, correlation, scoring).
- How policy evaluation works (conditions, operators, evaluation order).
- The role of VEX and vulnerability auditing.
- How BOM processing and ingestion works (deduplication, identity matching).
- Permissions and access control model.

### What does NOT belong here

- Step-by-step instructions (→ Tutorials or Guides).
- Parameter or API field listings (→ Reference).
- Actionable procedures ("do X, then Y") (→ Guides).
- Java field names, REST endpoint paths, or runtime config keys (→ Surface language).

---

## Reference

Information-oriented technical descriptions. The reader needs **truth and
certainty** — a firm platform to stand on while working. Reference is
**consulted**, not read end-to-end.

### Principles

- Describe, and *only* describe. Do not instruct, explain, or opine.
- Structure must mirror the product: API endpoints, configuration properties,
  data model entities.
- Be austere: accurate, precise, complete, unambiguous.
- Use consistent formatting and patterns throughout.
- Provide usage examples to illustrate, not to instruct.
- Auto-generated content (OpenAPI, schema docs) is a starting point, not a
  finished product.

### What belongs here

- REST API endpoint reference.
- Configuration property reference (environment variables, application
  properties).
- Data model / schema reference.
- Permission / ACL matrix.
- Supported ecosystem / package URL type matrix.
- CLI flags and options.

### What does NOT belong here

- Explanations of *why* something is designed a certain way (→ Concepts).
- Guided procedures or workflows (→ Guides).
- Narrative introductions (→ Tutorials).

---

## Upgrading guides

Upgrading guides are a subset of Guides that live in `guides/upgrading/`. They
follow all Guide principles but are scoped to version-specific upgrade
procedures. Each document covers one release (or range) and is titled by the
target version (e.g., "Upgrading to v5.0").

Do not create a separate top-level `migration/` section. Upgrading content
belongs under Guides.

---

## Blog

The blog (`docs/blog/`) is **outside the Diataxis framework**. It holds
time-stamped, dynamic content: release announcements, engineering deep dives,
ecosystem updates, and project news. Blog posts are informal and narrative —
they do not need to conform to any of the four content types above.

Changelog entries should be published as blog posts rather than maintained as a
separate page, so that all time-stamped content lives in a single location.

---

## Cross-referencing

Every document must fit exactly one Diataxis type. When content from another
type is needed to support the reader, **link to it** — do not inline it.

Rules:

- Tutorials and Guides may link to Concepts for background, but must not
  inline more than one sentence of explanation.
- Tutorials and Guides may link to Reference for parameter details, but must
  not reproduce reference tables.
- Concepts may link to Reference for precise definitions, but must not include
  procedural steps.
- Reference must not contain instructional or explanatory prose. Usage examples
  are acceptable to illustrate, not to instruct.

Use relative links between documentation pages. Prefer linking to a specific
section (`concepts/vulnerability-analysis.md#data-sources`) over linking to an
entire page when the relevant information is in a subsection.

---

## Surface language

Each Diataxis type has a default surface vocabulary. Match it to the audience
that consults the page.

- **Concepts**: UI labels and domain terms. Do not use Java field names
  (`isLatest`, `accessTeams`, `inactiveSince`), REST endpoint paths, or
  runtime configuration property keys. Refer to features the way they appear
  in the application. Permission codes and CycloneDX classifier names that
  surface verbatim in the product (BOMs, dropdowns, badges) are fine.
- **Guides**: describe procedures via the UI by default. The user's path is
  the form, the dropdown, the toggle. Inline REST endpoints, request bodies,
  or configuration property keys only when the page is itself a technical
  procedure where the API or config file is the user's entry point (for
  example, "Upload a BOM via REST API", "Configure with environment
  variables"). Otherwise, link to the relevant Reference subsection and keep
  prose UI-first.
- **Reference**: structured tables of UI-visible labels, dropdown values,
  classifier names, and other product-surface vocabulary belong here. The
  dedicated REST API and configuration-property references (the OpenAPI
  specs, the `application.properties` table) are the home for low-level
  identifiers. Other Reference subsections should also stay UI-first.
- **Tutorials**: same default as Guides. The student is using the UI unless
  the tutorial is explicitly an API tutorial.

When a feature has both a UI label and a technical identifier, prefer the UI
label and link out to Reference for the identifier. The reverse breaks for
users who never see the API or the config file.
