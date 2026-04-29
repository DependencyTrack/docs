# About tags

A **tag** is a short, shared label. You can attach the same tag to
[projects](projects.md), [component](component-policies.md) and
[vulnerability](vulnerability-policies.md) policies, vulnerabilities, and
[alerts](notifications.md), and the rest of the system reads tags to scope behavior.
Tags are deliberately lightweight: a name and nothing else.

## What a tag is

A tag is just a name. Names are unique across the instance, so two attachments of the
same name refer to the same tag. A tag has no value, no type, no namespace, no
description. If you need richer metadata bound to a project, use
[project properties](projects.md#tags-and-properties) instead.

Tags are many-to-many with the things they label. A project can carry many tags, and a
tag can label many projects. Removing a tag from one project does not affect any other.

## What tags do

Tags are a scoping primitive. Different parts of the system look at the same tag set:

- **Project filtering.** The project list can filter by tag.
- **Policy assignment.** A component or vulnerability policy can target only projects
  carrying specific tags. See [About component policies](component-policies.md) and
  [About vulnerability policies](vulnerability-policies.md).
- **Collection projects.** The tag-based collection mode aggregates only the children
  carrying the configured tag. See
  [About projects › Collection projects](projects.md#collection-projects).
- **Alerts.** An [alert](notifications.md) can fire only for projects carrying specific tags.
- **Vulnerability tagging.** You can attach tags to vulnerabilities for triage and
  reporting.

## Tags versus project properties

Both attach metadata to a project, but they answer different questions:

- Reach for a **tag** when the value is a label that may apply to many projects, and you
  expect the policy engine, alerting, or the tag-filtered collection mode to read it.
- Reach for a **project property** when the value is per-project structured data (a
  typed key with a value) that you want to read back later, but no built-in feature
  consumes it.

Properties carry types and group names, while tags do not. If you find yourself encoding two
pieces of information into one tag (`team:platform`, `env=prod`), that is a signal to
reach for a property, or for two separate tags, instead.

## Lifecycle

Tags come into being implicitly on first use. Attaching a name that does not exist
creates the tag. Detaching the last attachment leaves an orphan tag, which the
maintenance task cleans up on its next run. Tags carry no per-tag access control. Any
user who can edit a project can also tag it.
