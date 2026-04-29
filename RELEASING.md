# Releasing the Dependency-Track documentation

The site is versioned with [mike] and deployed by [`docs.yml`]:

- Push to `main` deploys the `next` alias.
- Push of a `<major>.<minor>.<patch>` tag deploys a versioned snapshot,
  updates the `<major>.<minor>` and `latest` aliases, and sets `latest`
  as default.
- Push of a prerelease tag (e.g. `5.7.0-rc.1`) deploys a snapshot
  under the full version. It does not touch `latest` or the default.

## Prerequisites

1. `make lint` and `make build` pass on the target branch.
2. Generated reference content matches the API server release. Re-run
   `update-config-docs`, `update-proto-docs`, and `update-openapi-docs`
   if needed and merge their PRs first.
3. Any release blog post is merged before the tag is pushed (see
   [Blog posts](#blog-posts)).

## Stable version

To release `5.7.0` or `5.7.1`:

```sh
git tag 5.7.0
git push origin 5.7.0
```

For bugfix releases, tag on the maintenance branch (e.g. `5.6.x`).

Verify `dependencytrack.github.io/docs/latest/` and `/5.7/` both serve
the new build, and the version selector lists the new entry.

## Prerelease version

To release `5.7.0-rc.1` or `5.7.0-beta.1`:

```sh
git tag 5.7.0-rc.1
git push origin 5.7.0-rc.1
```

Verify `dependencytrack.github.io/docs/5.7.0-rc.1/` is reachable and
that `latest` still points at the previous stable release.

## Blog posts

The site uses the MkDocs Material [blog plugin]. Mike freezes the blog
per version, so:

- Author release posts on the target branch before tagging. A post
  merged after the tag will not appear in that version's snapshot.
- Set an absolute `date:` matching the release day and
  `categories: [Release]`.
- Remove `draft: true` before merging. Drafts render in `make serve`
  but are excluded from `make build` and mike.
- Edits to old posts do not backport. A fix on `main` updates `next`
  and future tags but leaves `5.7/` untouched. To correct an archived
  version, redeploy it from a fixup commit on the maintenance branch.
- The RSS feed is per version. Treat `latest/blog/` as the canonical
  blog URL for external links.

[mike]: https://github.com/jimporter/mike
[`docs.yml`]: .github/workflows/docs.yml
[blog plugin]: https://squidfunk.github.io/mkdocs-material/plugins/blog/