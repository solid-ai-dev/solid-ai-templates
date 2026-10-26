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
[LOAD: release]
```

- `[ID:]` names the section and comes first
- `[DEPENDS ON:]` declares file-level dependencies; it is metadata, not
  content, and may be split over several lines to keep the width
- `[EXTEND:]` or `[OVERRIDE:]` declares the relationship to a parent
- `[LOAD:]` says where the heading's rules load: a kind of task the
  manifest's `tasks:` lists, such as `release`, or `check` for rules a
  check enforces. A heading without one loads on every turn, and a
  heading's subheadings take its load (ADR-058)
- A heading carries one load at most, among its tags; a template that
  guards data, credentials or authentication carries none, and SYS-25
  checks all three
- A section runs from its tags to the next `[ID:]` or the end of the file,
  and is never empty
- Shipped IDs are frozen: never removed, renamed or moved to another file
  inside a major, and a new ID never splits a shipped section (8.7)

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
| Fork-owned files | `README.md`, `AGENTS.md`, `CLAUDE.md` and `CHANGELOG.md`; the fork keeps its side on every merge |
| Fork-owned modules | `tests/fork_checks.py`, `tests/fork_dispositions.py` and `tools/fork_examples.py`, loaded when present. `fork_examples.py` may set `CHAIN_EXAMPLES_DOC`, default `docs/architecture/06-runtime-view.md` |

## 8.7 Frozen surface

This is the one list of what 3.x freezes; other documents point here. From
3.0.0 no release removes, renames or changes the meaning of an element below
before 4.0.0, except for a security fix (ADR-051). A minor may add elements
and deprecate one by naming its replacement (8.8).

| Element | What is frozen | Source |
|---------|----------------|--------|
| Template paths | The file path of every shipped template | ADR-051 |
| Template IDs | The `id` of every manifest entry | ADR-051 |
| Section IDs | Every `[ID:]`, in the file that holds it, and the headings its section holds: a section does not move to another file, and a minor adds an ID only on new content, never in front of lines a shipped section holds. SYS-24 checks it against the newest 3.x tag | ADR-051 |
| Manifest schema | The fields the header comment of `templates/manifest.yaml` lists, and their meaning; a minor adds only optional fields | ADR-051 |
| Core-tier membership | The IDs under `core:`; a new template is reached by declaring it, never by joining the core | ADR-051 |
| Check exit codes | 0 passes, 1 fails, 3 does not apply | ADR-051 |
| Task kinds | The kinds under the manifest's `tasks:`, which a load directive names | ADR-058 |
| Hooks | A shipped hook ID, its direct exit codes, its `not applicable` line and its violation codes | ADR-055 |
| Hook arguments | The name and default of each argument a consumer writes into its config, such as `--path`, `--forbid` and `--base`; a minor adds only arguments whose default keeps the hook's behaviour | ADR-051, applied to hooks |
| Fork entry points | The fork-owned module names (8.6), and what upstream reads from them: `bind`, `CHECKS`, `TEMPLATE_DIRS`, `CORE_DIRS` and `QUALITY_GATES_EXEMPT_LAYERS` from `fork_checks.py`; `CHECKS` and `SKIP_BUDGET` from `fork_dispositions.py`; `SPEC_CHAIN_EXAMPLES` and `CHAIN_EXAMPLES_DOC` from `fork_examples.py`. The disposition words `tests/conformance` defines for a fork to import | ADR-051, applied to forks |
| Fork baseline | The `SAIT_UPSTREAM_REF` variable smoke reads | ADR-051, applied to forks |
| Resolver CLI | `tools/resolve_chain.py <id>` and its `--concat`, `--generate`, `--list`, `--roots` and `--check` flags | ADR-051, applied to forks |

What is not frozen:

| Element | Why |
|---------|-----|
| The wording inside a section | Prose is free while the section keeps its ID (ADR-051) |
| The declaration block | A target with no producer and no reader (ADR-053, 6.3) |
| The fixture: `stack-fixture`, `platform-fixture` | Test input; no listing offers it and no project resolves it |
| The helpers `bind()` hands `fork_checks.py` | Every name in the smoke modules; a change to one is listed in the changelog |

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
its pass condition beside it (ADR-031).

```text
templates/<concern>/<name>.md   # cross-cutting: core, security, infra, data
templates/frontend/<concern>.md # frontend layer
templates/backend/<concern>.md  # backend layer
templates/fixture/<name>.md     # test input
```

A fork names its own files; the Imbra fork names a stack
`<prefix>-<name>.md`, such as `python-fastapi.md`.

## 8.10 Context cost

Every rule in a widely resolved file is read on every turn by every project
on that chain. A change that moves a stack category across a context-window
tier must record it in `tests/smoke/context-tiers.txt` in the same change
(SYS-16). Two design documents go deeper:

- [agent-context-tradeoffs.md](../design/agent-context-tradeoffs.md): how
  context size and startup design affect latency and quality
- [template-content-quality.md](../design/template-content-quality.md): the
  measured criteria `tools/score_templates.py` scores

What each root puts in context, as `resolve_chain.py --emit` builds it:
the root file an agent reads on every turn, and the skills that load only
when their task starts (ADR-058). The root file counts its fact slots too.

<!-- generated:spec-context-cost -->
| Root | Every turn, words | Skills | Skill words |
|------|-------------------|--------|-------------|
| `backend-api` | 7967 | 0 | 0 |
| `backend-auth` | 9451 | 0 | 0 |
| `backend-caching` | 7071 | 0 | 0 |
| `backend-concurrency` | 6905 | 0 | 0 |
| `backend-database` | 6898 | 0 | 0 |
| `backend-edge` | 9787 | 0 | 0 |
| `backend-errors` | 8304 | 0 | 0 |
| `backend-features` | 6916 | 0 | 0 |
| `backend-grpc` | 10667 | 0 | 0 |
| `backend-http` | 7332 | 0 | 0 |
| `backend-jobs` | 6860 | 0 | 0 |
| `backend-messaging` | 7184 | 0 | 0 |
| `backend-microservices` | 9239 | 0 | 0 |
| `backend-monitoring` | 7197 | 0 | 0 |
| `backend-observability` | 6944 | 0 | 0 |
| `backend-webhooks` | 10366 | 0 | 0 |
| `base-agents` | 7559 | 0 | 0 |
| `base-cicd` | 6874 | 0 | 0 |
| `base-config` | 6958 | 0 | 0 |
| `base-containers` | 6907 | 0 | 0 |
| `base-data-governance` | 7404 | 0 | 0 |
| `base-data-migration` | 7403 | 0 | 0 |
| `base-data-modeling` | 6916 | 0 | 0 |
| `base-data-quality` | 7669 | 0 | 0 |
| `base-deployment` | 6799 | 0 | 0 |
| `base-devsecops` | 7052 | 0 | 0 |
| `base-docs` | 6450 | 0 | 0 |
| `base-embedded-checks` | 9937 | 0 | 0 |
| `base-git` | 6450 | 0 | 0 |
| `base-measurement` | 7177 | 0 | 0 |
| `base-oop` | 7003 | 0 | 0 |
| `base-quality` | 6450 | 0 | 0 |
| `base-quality-gates` | 9673 | 0 | 0 |
| `base-review` | 6450 | 0 | 0 |
| `base-security` | 7981 | 0 | 0 |
| `base-testing` | 6450 | 0 | 0 |
| `frontend-content` | 6845 | 0 | 0 |
| `frontend-quality` | 6941 | 0 | 0 |
| `frontend-ux` | 6966 | 0 | 0 |
<!-- /generated:spec-context-cost -->
