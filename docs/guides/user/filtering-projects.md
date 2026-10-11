# Filtering projects

The *Projects* view lets you filter the portfolio by project attributes.

Open *Projects* and select *Add filter* to add a filter.

## Available filters

The following filters are available:

- **Project name**: Enter text to find projects whose name contains that text.
- **Version**: Enter text to find projects whose version contains that text.
- **Classifier**: Select one or more classifiers. Dependency-Track returns projects that match any selected classifier.
- **Tags**: Enter one or more tags. Projects must have all entered tags.
- **Teams**: Enter one or more teams. Projects must belong to at least one entered team.
- **Ancestor**: Select a project to show its descendants at any hierarchy level.
- **Last BOM import**: Select a date range for the most recent BOM import.
- **Active**: Show only active or only inactive projects.
- **Latest**: Show only projects marked as latest or non-latest.

You can combine filters to narrow the result set.

## Sharing filtered views

The page URL stores the selected filters.

You can use the URL to:

- bookmark a filtered project view;
- share the view with other users;
- restore the filters after a page reload.

Access control still applies. Users see only projects they can access.

## Project hierarchy

Dependency-Track can show projects as a hierarchy when the active filters allow
a tree view.

Filters for project name, version, classifier, tags, teams, ancestor, and last
BOM import switch the project list to a flat view.

The *Active* and *Latest* filters do not require a flat view.

## Clearing filters

Remove a filter from its filter pill, or select *Clear all filters* to reset all
filters.
