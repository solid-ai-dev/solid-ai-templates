# 8. Crosscutting concepts

## 8.1 Sections, IDs and directives

A section that something references carries a unique ID. A later template
extends or replaces it by naming that ID; with neither, the section is used
as written.

```markdown
## Git conventions [ID: base-git]
- Base rules

## Git conventions [EXTEND: base-git]
- Do not commit `dist/`            <- added on top of the base rules

## Git conventions [OVERRIDE: base-git]
- Always run `npm run dev` first   <- replaces the base rules
```

A heading may carry several tag lines:

```markdown
## Heading
[ID: section-id]
[DEPENDS ON: path/to/dep.md, path/to/other.md]
[EXTEND: parent-id]
```

- `[ID:]` names the section and comes first
- `[DEPENDS ON:]` declares file-level dependencies; it is metadata, not
  content, and may be split over several lines to keep the width
- `[EXTEND:]` or `[OVERRIDE:]` declares the relationship to a parent
- A section runs from its tags to the next `[ID:]` or the end of the file,
  and is never empty
- Shipped IDs are frozen: never removed or renamed inside a major (ADR-051)

`[DEPENDS ON]` lists direct dependencies only, matching the manifest's
`depends_on` for the entry. The manifest wins a mismatch, and SYS-04 checks
it.

## 8.2 Precedence

When several templates name one section ID, the higher level wins:

1. Base template, the default
2. Layer template, frontend or backend
3. Stack template
4. Interview answers, which always win

`core/testing.md` sets a test naming convention, a fork's Python stack
extends it, and the interview answer "use BDD-style names" overrides both.

## 8.3 Conflicts

| Situation | Resolution |
|-----------|------------|
| One template extends, another overrides one ID | The override replaces the base; the extension applies on top |
| Two templates override one ID | Error: the agent shows both and asks which applies |
| Two templates extend one ID | Both apply, in the stack's declared dependency order |

A chain never overrides one ID twice, and `SAIT-SMK-TPL-10-001A` fails one
that does (ADR-039). To specialise across three levels, each override
declares an ID of its own and the next level overrides that:

```text
frontend/content.md           [ID: static-site-content]
stack/static-site-astro.md    [ID: astro-content]    [OVERRIDE: static-site-content]
stack/static-site-tutorial.md [ID: tutorial-content] [OVERRIDE: astro-content]
```

A conflict the rules cannot settle goes to the user: show both rules, ask
which wins, and record the answer in the generated file.

## 8.4 Reach

A rule that names another file's section in running prose is not a
directive and is not resolved. It reads correctly only in chains that carry
both files. Never name a section from a file that is absent from some chain
carrying yours; state the substance inline. SYS-11 checks this per chain
(ADR-028).

An orthogonal template is the sharpest case: its guaranteed context is the
core tier plus its own `depends_on` tree, so every `[EXTEND]` and prose
reference in it resolves there (ADR-035).

When a rule could live in either of two templates, measure both files' chain
reach and put it in the wider one.

## 8.5 Governed tiers

Two opt-in tiers are not left to what the dependency declarations produce.
Membership is stated by stack category, the `layer` a stack declares, with
a reason per exempt category, and a smoke check enforces it both ways
(ADR-044).

| Tier | Exempt categories | Reason | Check |
|------|-------------------|--------|-------|
| Security | library, embedded | A library's caller owns the trust boundary; an embedded target has no HTTP surface, sessions or TLS | SYS-15 |
| Quality gates | Named by a fork in `tests/fork_checks.py` | A category at the most constrained context tier cannot admit the tier without changing which models can run it | SYS-18 |

A list of stack IDs is what this replaces: correct the day it is written,
silently wrong at the next stack.

## 8.6 Fork contract

| Mechanism | Rule |
|-----------|------|
| Sync by merge | A fork stays current with `git merge upstream/main`, never by copying files |
| Keys of its own | A fork appends under `stacks:`, `platform:` and keys of its own, never `core:`, `base:`, `backend:` or `frontend:`. SYS-20 checks the upstream keys against `SAIT_UPSTREAM_REF` |
| `fork_core` | Joins every chain's core tier after `core:`; an entry there depends only on core-tier IDs. SYS-21 checks it |
| Namespaces | Upstream holds `base-*`, `backend-*`, `frontend-*` and its template directories; forks hold `stack-*`, `platform-*` and `<org>-*`. A duplicate ID fails MNF-01 and stops the resolver |
| `Fork-merge: ours` | Marks an upstream commit that removes what forks carry; ADR-049, "Merging the split", gives the commands |
| Fork-owned files | `README.md`, `CLAUDE.md` and `CHANGELOG.md`; the fork keeps its side on every merge |
| Fork-owned modules | `tests/fork_checks.py`, `tests/fork_dispositions.py` and `tools/fork_examples.py`, loaded when present. `fork_examples.py` may set `CHAIN_EXAMPLES_DOC`, default `docs/architecture/06-runtime-view.md` |

## 8.7 Deprecation

From 3.0.0 a template is not removed inside a major (ADR-051). Its manifest
entry names the template that replaces it, and the release that marks it
lists it under `Deprecated` in the changelog.

```yaml
- id: base-old
  file: templates/core/old.md
  description: ...
  deprecated: base-new
```

The entry still resolves. SYS-22 fails a `deprecated` that names no entry,
or one that is itself deprecated. Removal waits for the next major.

## 8.8 Rule language and naming

A rule is a plain imperative, read as MUST or MUST NOT, or carries an RFC
2119 keyword where strength matters (`templates/core/docs.md`, "Rule
language"). A mechanically checkable rule names its command in a fence and
its pass condition beside it (ADR-031).

```text
templates/<concern>/<name>.md   # cross-cutting: core, security, infra, data
templates/frontend/<concern>.md # frontend layer
templates/backend/<concern>.md  # backend layer
templates/fixture/<name>.md     # test input
```

A fork names its own files; the Imbra fork names a stack
`<prefix>-<name>.md`, such as `python-fastapi.md`.

## 8.9 Context cost

Every rule in a widely resolved file is read on every turn by every project
on that chain. A change that moves a stack category across a context-window
tier must record it in `tests/context-tiers.txt` in the same change
(SYS-16). Two design documents go deeper:

- [agent-context-tradeoffs.md](../design/agent-context-tradeoffs.md): how
  context size and startup design affect latency and quality
- [template-content-quality.md](../design/template-content-quality.md): the
  measured criteria `tools/template_quality.py` scores
