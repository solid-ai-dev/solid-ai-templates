---
id: "054"
status: Accepted
date: 2026-10-19
category: composition
supersedes: []
superseded_by: []
---

# ADR-054: Content rules form a frontend layer of their own

## Context

`frontend-static-site` carried two responsibilities in one layer, and
`frontend-quality` repeated part of one of them.

| Force | What it shows |
| ----- | ------------- |
| Two concerns in one file | Content, asset, SEO and structured-data rules hold for any project that authors content; build output, serving, CSS, fonts and theme hold only for a static site |
| A consumer it fits badly | A project that authors content without building a site, such as a docs pipeline or a Markdown-into-CMS blog, inherits CSS, font and theme rules it cannot use |
| A duplicated rule set | The SEO rules appeared in both `frontend-static-site` and `frontend-quality`, worded apart, so a chain carrying both stated them twice |
| The freeze | From 3.0.0, section IDs are frozen until 4.0.0, so a split that moves sections is cheapest before the tag |

## Decision

The build-agnostic content, asset, SEO and structured-data rules move into a
new `frontend-content` layer, which `frontend-static-site` depends on.

## Rationale

- A layer a project can take on its own matches the content-only consumer
  the static-site layer did not fit.
- One canonical copy of the SEO rules removes the duplicate a chain carried.
- Moving sections keeps their IDs, so the split changes where a rule lives,
  not what a template extending or overriding it names.

## Design

1. **`frontend-content`** — content structure, assets, SEO and structured
   data, depending on `base-docs` and `base-quality`
2. **`frontend-static-site`** — build, serving, CSS, typography, theme,
   performance and the trailing slash; it depends on `frontend-content`
3. **`frontend-quality`** — keeps its analytics rules and drops the SEO
   rules; it does not depend on `frontend-content`, so a non-static frontend
   chain does not gain asset and data-directory rules
4. **IDs** — every moved section keeps its ID; structured data gains
   `frontend-content-structured-data`

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Keep one static-site layer | A content-only project keeps inheriting rules it cannot apply |
| Leave the SEO rules in `frontend-quality` as well | The chain keeps stating them twice, in two wordings |
| Make `frontend-quality` depend on `frontend-content` | Every frontend chain would gain content and asset rules, though only the static-site layer consumes `frontend-quality` today |

## Consequences

- A static-site chain resolves the same rules as before, from one more file.
- A chain that takes `frontend-quality` without `frontend-static-site` loses
  the SEO rules and adds `frontend-content` to keep them.
- A content-only project can take `frontend-content` alone.

## Compatibility

No section ID is renamed or removed. A stack overriding or extending a moved
section still resolves it, because `frontend-static-site` depends on the
layer that now holds it. The change ships in 3.0.0, before the freeze.

## Security

No credentials, secrets or attack surface are involved.

## Related

- ADR-004 - the earlier split of a layer whose consumers needed only part
  of it.
