# 8. Crosscutting concepts

The concepts that hold across every template, tool and fork. They cover
how sections combine, which rule wins, how far a reference reaches, what a
fork may change, what 3.x freezes, how rules are written, and what a root
costs in context.

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
[LOAD: release]
```

- `[ID:]` names the section and comes first
- `[DEPENDS ON:]` declares file-level dependencies; it is metadata, not
  content, and may be split over several lines to keep the width
- `[EXTEND:]` or `[OVERRIDE:]` declares the relationship to a parent
- `[LOAD:]` says where the heading's rules load, either a kind of task
  the manifest's `tasks:` lists, such as `release`, or `check` for rules a
  check enforces. A heading without one loads on every turn, and a
  heading's subheadings take its load (ADR-058, proposed)
- A heading carries one load at most, among its tags, and none under a
  heading that has one. A template that guards data, credentials or
  authentication carries none. SYS-25 checks each of these
- A section runs from its tags to the next `[ID:]` or the end of the file,
  and is never empty
- Shipped IDs are frozen, never removed, renamed or moved to another
  file inside a major, and a new ID never splits a shipped section (8.7)

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

When two templates in one chain name the same ID, the kind of each
settles which rule applies.

| Situation | Resolution | Source |
|-----------|------------|--------|
| One template extends, another overrides one ID | The override replaces the base, and the extension applies on top | FR-04-03 |
| Two templates override one ID | The chain is refused, and TPL-10 fails it | FR-04-04, ADR-039 |
| Two templates extend one ID | Both apply, in the stack's declared dependency order | FR-04-03 |

To specialise across three levels, each override declares an ID of its own
and the next level overrides that:

```text
frontend/content.md           [ID: static-site-content]
stack/static-site-astro.md    [ID: astro-content]    [OVERRIDE: static-site-content]
stack/static-site-tutorial.md [ID: tutorial-content] [OVERRIDE: astro-content]
```

## 8.4 Chain reach

A rule that names another file's section in running prose is not a
directive, and the resolver does not resolve it. It reads correctly only in
chains that carry both files. Never name a section from a file that is
absent from some chain carrying yours; state the substance inline. SYS-11
checks this per chain (FR-01-03, ADR-028).

An orthogonal template is the sharpest case. Its guaranteed context is the
core tier plus its own `depends_on` tree, so every `[EXTEND]` and prose
reference in it resolves there (ADR-035).

When a rule could live in either of two templates, measure both files' chain
reach and put it in the wider one.

## 8.5 Opt-in tier membership

Two opt-in tiers are not left to what the dependency declarations produce.
Membership is stated by stack category, the `layer` a stack declares, with
a reason for each exempt category, and a smoke check enforces it both
ways. A list of stack IDs would be correct the day it is written and
silently wrong at the next stack.

| Tier | Exempt categories | Reason | Check | Source |
|------|-------------------|--------|-------|--------|
| Security | library, embedded | A library's caller owns the trust boundary; an embedded target has no HTTP surface, sessions or TLS | SYS-15 | FR-02-02, ADR-044 |
| Quality gates | Named by a fork in `tests/fork_checks.py` | A category at the most constrained context tier cannot admit the tier without changing which models can run it | SYS-18 | ADR-044 |

## 8.6 Fork contract

What a fork may change, and how it stays current with upstream.

| Mechanism | Rule | Source |
|-----------|------|--------|
| Sync by merge | A fork stays current with `git merge upstream/main`, never by copying files | FR-08-01, ADR-049 |
| Keys of its own | A fork appends under `stacks:`, `platform:` and keys of its own, never `core:`, `base:`, `backend:` or `frontend:`. SYS-20 checks the upstream keys against `SAIT_UPSTREAM_REF` | FR-08-02 |
| `fork_core` | Joins every chain's core tier after `core:`; an entry there depends only on core-tier IDs. SYS-21 checks it | FR-03-02, FR-08-03 |
| Namespaces | Upstream holds `base-*`, `backend-*`, `frontend-*` and its template directories; forks hold `stack-*`, `platform-*` and `<org>-*`. A duplicate ID fails MNF-01 and stops the resolver | FR-03-01 |
| `Fork-merge: ours` | Marks an upstream commit that removes what forks carry. The fork merges it with `-s ours`, keeping its own files | ADR-049 |
| Fork-owned files | `README.md`, `AGENTS.md`, `CLAUDE.md` and `CHANGELOG.md`; the fork keeps its side on every merge | ADR-050 |
| Fork-owned modules | `tests/fork_checks.py`, `tests/fork_dispositions.py` and `tools/fork_examples.py`, loaded when present. `fork_examples.py` may set `CHAIN_EXAMPLES_DOC`, default `docs/architecture/06-runtime-view.md` | ADR-050 |

## 8.7 Frozen surface

From 3.0.0 no release removes, renames or changes the meaning of an
element below before 4.0.0, except for a security fix. A minor may add
elements, and deprecate one by naming its replacement.

| Element | What is frozen | Source |
|---------|----------------|--------|
| Template paths | The file path of every shipped template | ADR-051 |
| Template IDs | The `id` of every manifest entry | ADR-051 |
| Section IDs | Every `[ID:]`, in the file that holds it, and the headings its section holds. A section does not move to another file, and a minor adds an ID only on new content, never in front of lines a shipped section holds. SYS-24 checks it against the newest 3.x tag | ADR-051 |
| Manifest schema | The fields the header comment of `templates/manifest.yaml` lists, and their meaning; a minor adds only optional fields | ADR-051 |
| Core-tier membership | The IDs under `core:`; a new template is reached by declaring it, never by joining the core | ADR-051 |
| Check exit codes | 0 passes, 1 fails, 3 does not apply | ADR-051 |
| Task kinds | The kinds under the manifest's `tasks:`, which a load directive names | ADR-058, proposed |
| Hooks | A shipped hook ID, its direct exit codes, its `not applicable` line and its violation codes | ADR-055 |
| Hook arguments | The name and default of each argument a consumer writes into its config, such as `--path`, `--forbid` and `--base`; a minor adds only arguments whose default keeps the hook's behaviour | ADR-051, applied to hooks |
| Fork entry points | The fork-owned module names (8.6), and the names upstream reads from them, `bind`, `CHECKS`, `TEMPLATE_DIRS`, `CORE_DIRS` and `QUALITY_GATES_EXEMPT_LAYERS` from `fork_checks.py`; `CHECKS` and `SKIP_BUDGET` from `fork_dispositions.py`; `SPEC_CHAIN_EXAMPLES` and `CHAIN_EXAMPLES_DOC` from `fork_examples.py`. The disposition words `tests/conformance` defines for a fork to import | ADR-051, applied to forks |
| Fork baseline | The `SAIT_UPSTREAM_REF` variable smoke reads | ADR-051, applied to forks |
| Resolver CLI | `tools/resolve_chain.py <id>` and its `--concat`, `--generate`, `--list`, `--roots` and `--check` flags | ADR-051, applied to forks |

These elements are not frozen.

| Element | Why | Source |
|---------|-----|--------|
| The wording inside a section | Prose is free while the section keeps its ID | ADR-051 |
| The declaration block | A target with no producer and no reader | ADR-053 |
| The fixture, `stack-fixture` and `platform-fixture` | Test input; no listing offers it and no project resolves it | - |
| The helpers `bind()` hands `fork_checks.py` | Every name in the smoke modules; a change to one is listed in the changelog | - |

## 8.8 Deprecation

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

A shipped hook that no template prescribes any more is deprecated the same
way. Its `name` in `.pre-commit-hooks.yaml` starts with `Deprecated:`, and
the changelog lists it under `Deprecated`. It keeps its frozen behaviour
(8.7) until the next major removes it.

## 8.9 Rule language and naming

A rule is a plain imperative, read as MUST or MUST NOT, or carries an RFC
2119 keyword where strength matters (`templates/core/docs.md`, "Rule
language"). A mechanically checkable rule names its command in a fence and
its pass condition beside it (FR-01-01, FR-07-01, ADR-031).

```text
templates/<concern>/<name>.md   # cross-cutting: core, security, infra, data
templates/frontend/<concern>.md # frontend layer
templates/backend/<concern>.md  # backend layer
templates/fixture/<name>.md     # test input
```

A fork names its own files.

## 8.10 Context cost

Every rule in a widely resolved file is read on every turn by every project
on that chain. A stack category's context-window tier moves only on
purpose, recorded in `tests/smoke/context-tiers.txt`, and SYS-16 checks it
(QG-02-02). Two design documents go deeper:

- [agent-context-tradeoffs.md](../design/agent-context-tradeoffs.md), on
  how context size and startup design affect latency and quality
- [template-content-quality.md](../design/template-content-quality.md), on
  the measured criteria `tools/score_templates.py` scores

The table shows what each root puts in context, as the emitter builds it.
The root file is read on every turn, and the skills load only when their
task starts. The root file's count includes its fact slots.

<!-- generated:spec-context-cost -->
| Root | Every turn, words | Skills | Skill words |
|------|-------------------|--------|-------------|
| `backend-api` | 5730 | 11 | 2714 |
| `backend-auth` | 7784 | 10 | 2094 |
| `backend-caching` | 5389 | 10 | 2094 |
| `backend-concurrency` | 5236 | 10 | 2094 |
| `backend-database` | 5196 | 11 | 2173 |
| `backend-edge` | 8117 | 10 | 2094 |
| `backend-errors` | 6635 | 10 | 2094 |
| `backend-features` | 5247 | 10 | 2094 |
| `backend-grpc` | 8896 | 11 | 2250 |
| `backend-http` | 5663 | 10 | 2094 |
| `backend-jobs` | 5169 | 10 | 2094 |
| `backend-messaging` | 5455 | 11 | 2188 |
| `backend-microservices` | 6852 | 11 | 2853 |
| `backend-monitoring` | 5528 | 10 | 2094 |
| `backend-observability` | 5275 | 10 | 2094 |
| `backend-webhooks` | 8637 | 11 | 2188 |
| `base-agents` | 4797 | 10 | 3189 |
| `base-cicd` | 5085 | 10 | 2214 |
| `base-config` | 5259 | 10 | 2124 |
| `base-containers` | 5138 | 10 | 2194 |
| `base-data-governance` | 5694 | 10 | 2094 |
| `base-data-migration` | 5367 | 11 | 2466 |
| `base-data-modeling` | 5206 | 10 | 2094 |
| `base-data-quality` | 5961 | 11 | 2143 |
| `base-deployment` | 5075 | 10 | 2153 |
| `base-devsecops` | 5383 | 10 | 2094 |
| `base-docs` | 4781 | 10 | 2094 |
| `base-embedded-checks` | 6035 | 11 | 4377 |
| `base-git` | 4781 | 10 | 2094 |
| `base-measurement` | 5508 | 10 | 2094 |
| `base-oop` | 5323 | 10 | 2094 |
| `base-quality` | 4781 | 10 | 2094 |
| `base-quality-gates` | 6014 | 11 | 4134 |
| `base-review` | 4781 | 10 | 2094 |
| `base-security` | 6312 | 10 | 2094 |
| `base-testing` | 4781 | 10 | 2094 |
| `frontend-content` | 5176 | 10 | 2094 |
| `frontend-quality` | 5201 | 10 | 2169 |
| `frontend-ux` | 5283 | 10 | 2094 |
<!-- /generated:spec-context-cost -->
