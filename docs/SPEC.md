# Template System Specification

## Goal

A composable, inheritance-based template library that an LLM agent can
use to draft a project's context files (`AGENTS.md` and `CLAUDE.md`) for
any type of project — from a static portfolio to a Python SDK to a
React SPA. Output quality depends on the model and context window.

Designed to be agent-agnostic: works with Claude Code, Codex CLI, Devin,
Cursor, or any agent that reads a Markdown context file.

Inspired by SOLID principles: each template has a single responsibility,
is open for extension, and can be composed without modification.

This repository holds the composition engine and the policy every team
shares. Forks carry the stacks, platforms, process layer and interview, and
stay current by merging this repository (ADR-049, ADR-050). A project uses
a fork, or forks this repository to make its own; upstream alone ships no
stack and no interview.

---

## Core concepts

### 1. Base templates (abstract, cross-cutting)

Reusable building blocks covering one concern each: `core/`, `security/`,
`data/` and `infra/`. Apply to every project regardless of stack. Never
used directly — always composed into a higher layer.

### 2. Frontend templates (abstract, frontend layer)

Concerns that apply to all frontend projects but not to backend or library
projects. Extend base templates. Never used directly by a project.

### 3. Backend templates (abstract, backend layer)

Concerns shared by all backend services but not by frontend or pure libraries.
Extend base templates. Never used directly by a project.

### 4. Stack and platform templates (concrete, fork-owned)

A stack template holds technology-specific rules and declares which layers
it depends on. A platform template maps CI and security tools to one
hosting platform, orthogonal to the stack choice. Both live in forks: a
fork appends them under `stacks:` and `platform:` in its manifest. See
[Forks](#forks).

### Fixtures (test input)

`templates/fixture/` holds upstream's only stack and only platform. They
exist for the checks, not for projects: `stack-fixture` (layer `fixture`)
and `platform-fixture`. Each manifest entry carries `fixture: true`, so
every listing a project reads — upstream's or a fork's — leaves them out,
while the checks that read every stack or platform read them too. They keep
those checks fed in a tree that carries no stack of its own.

### Directory listings

Generated from `templates/manifest.yaml` — run `py tools/sync.py` to refresh.
The `stack/` listing leaves out the fixture, so it is empty upstream; in a
fork it lists the fork's stacks.

<!-- generated:spec-directories -->
```
core/
├── git.md          # Committer identity, branching, pull requests, submodules, off-limits paths, .gitignore
├── docs.md         # Rule language, standard documents, writing style, diagrams, docs-as-code, agent output files
├── quality.md      # Architecture, code style, calibration, tool trust, testing
├── review.md       # Peer review priority, MUST/SHOULD checklists, deviation rules
├── testing.md      # Test pyramid, coverage thresholds, naming conventions
├── agents.md       # Output structure, models (inline/hybrid), formatting rules
├── config.md       # Env vars, secrets, fail-fast validation
├── oop.md          # SOLID, OOP, GoF design patterns, AOP guidance
└── quality-gates.md # How a check is built - retrofitting a gate, pairing a constraint with its check, reading a verdict
```

```
security/
├── devsecops.md    # SAST, SCA, SBOM, secret detection, license compliance
└── security.md     # Application security rules — input, output, injection, auth, sessions, TLS, headers
```

```
infra/
├── cicd.md         # Pipeline stages, triggers, environments, IaC, deployment
├── containers.md   # Dockerfile, runtime security, resource limits, Kubernetes
└── deployment.md   # Deployment targets (cloud/hybrid/offline), certs, LB, registries, secrets
```

```
data/
├── data-quality.md # Data sourcing, completeness, freshness, research, scoring — data-heavy projects
├── data-modeling.md # Schema design, naming, normalization, relationships, data types
├── data-governance.md # Classification, PII handling, retention, ownership, audit trail
└── data-migration.md # Versioned migrations, zero-downtime, rollback strategies
```

```
frontend/
├── ux.md           # UX principles, WCAG 2.1 AA, responsive breakpoints
├── quality.md      # CSS conventions, performance, SEO & analytics
└── static-site.md  # Abstract SSG rules — content, assets, SEO
```

```
backend/
├── http.md         # URI design, methods, headers, HATEOAS, auth, errors
├── api.md          # API-first, OpenAPI, versioning, deprecation, pagination
├── database.md     # Migrations, transactions, no raw SQL, connection pooling
├── caching.md      # Cache-aside, TTL, invalidation, resilience, stampede
├── auth.md         # Authn/authz, JWT, RBAC, sessions, API keys
├── jobs.md         # Background jobs, idempotency, retry, DLQ, scheduling
├── concurrency.md  # Threads vs. processes vs. async, shared state, structured concurrency
├── messaging.md    # Brokers, producers, consumers, schema, DLQ, observability
├── webhooks.md     # Inbound webhook intake, edge signature verification, fast-ack, retry amplification
├── edge.md         # Reverse proxy / edge — TLS termination, forwarded headers, upstream routing, timeouts, edge security
├── grpc.md         # Proto design, status codes, interceptors, health check
├── microservices.md # Service boundaries, inter-service comms, saga, contract testing
├── errors.md       # Classification, propagation, recovery, external failures
├── features.md     # Feature flags, rollout strategy, experimentation
├── observability.md # Log levels, log format, health check, error visibility
├── monitoring.md   # Key metrics, thresholds, alerts, dashboards, incidents
└── quality.md      # Layered architecture, security, performance, API stability
```

```
stack/
```
<!-- /generated:spec-directories -->

### 5. Output format template

Rendering rules for the generated output. Describes structure, model
selection (inline or hybrid), and formatting constraints.
Lives in `templates/core/agents.md` alongside the other core
templates.

### 6. Interview template (orchestrator, fork-owned)

A single file any agent uses to ask the user the required questions before
generating the output context file. Each fork ships its own, usually as
`templates/INTERVIEW.md`, and points it at the fork's stacks; upstream
ships none. See [Interview template structure](#interview-template-structure).

### 7. Profile (generated output)

The context file generated for a specific project by combining interview
answers + base templates + stack template + output format template.
`templates/core/agents.md` asks every project who approves a change, how
work is tracked and what a release is. Upstream answers none of them; the
project or its fork does.

Which file each agent reads is the "Output file by agent" table in
`templates/core/docs.md`; README's agents table is generated from it.

---

## Inheritance model

```
upstream                                           fork
templates/core/git.md ──────────────────────────────┐
templates/core/docs.md ─────────────────────────────┤
templates/core/quality.md ──────────────────────────┤
                                                     ▼
frontend/ux.md ──────────────────────────► frontend/static-site.md
frontend/quality.md ─────────────────────►          │
                                                     ▼
                                          templates/stack/static-site-astro.md
                                                     │
                                          + the fork's interview answers
                                                     │
                                          + templates/core/agents.md rules
                                                     │
                                                     ▼
                                                CLAUDE.md
```

Everything above the stack template is upstream's; the stack and the
interview are the fork's. The fork's own `fork_core:` templates join the
core tier of every chain.

Rules:
- A stack template MUST reference which base templates it depends on
- A stack template MAY override a base rule — overrides must be explicit
- A stack template MAY add new rules not present in the base
- The agent merges base defaults + stack overrides + interview answers,
  then applies the output format template

---

## Composition model

Stacks compose only the modules they need — no transitive surprises.
See ADR-004 for the full rationale.

### Core tier

The core-tier base templates apply to every project. They are declared in
`templates/manifest.yaml` under `core:` and included during
resolution — stacks do not need to list them in `depends_on`:

<!-- generated:spec-core-tier -->
- `templates/core/quality.md`
- `templates/core/git.md`
- `templates/core/docs.md`
- `templates/core/testing.md`
- `templates/core/review.md`
- `templates/core/oop.md`

Measured: 10 `[DEPENDS ON]` tokens across 5 templates name one of these
files, and 5 manifest entries name a core id in `depends_on`. Declaring one
is redundant rather than forbidden — the seeding reaches the file either
way, and the directive documents a dependency a reader would otherwise
infer. Reached by the seeding alone: `base-review`. A chain assembled by
walking the directives does not reach that set and reports nothing about it,
because nothing declares what is absent.
<!-- /generated:spec-core-tier -->

A fork adds its own templates to every chain under `fork_core:`, which the
resolver takes after `core:`. It keeps its templates under a top-level key
of its own: every top-level list of entries except `core` and `fork_core`
is a section the resolver reads, so a fork never edits a key upstream owns.

SYS-13 compares the walk the README documents against the resolver for
every root, in both directions.

### Orthogonal templates

Some templates are project-level choices, not stack-level dependencies.
They are not referenced in any stack's `depends_on` chain — users
opt in via the `Extras` field in the declaration block or during a
fork's interview.

Upstream's orthogonal templates include the advanced data templates
(data-governance, data-migration), opt-in extras no stack pulls
automatically. A fork adds its own: platform choices and workflow
preferences are a fork's.

Orthogonal templates are NOT expected to appear in stack resolution.
They are resolved as their own roots instead: an orthogonal template is
guaranteed the core tier plus its own `depends_on` tree, and nothing
else, because the stack it is paired with is not known when it is
authored. Reachability is checked against that chain — an `[EXTEND: ...]`
or a prose section reference in an orthogonal template MUST resolve
there, not in some stack chain the project may never pick.

### Opt-in tiers

Everything else is explicit. Stacks declare what they need. Upstream's
opt-in modules:

| Tier | Modules |
|------|---------|
| CI | cicd, quality-gates |
| Security (app) | security |
| Security (pipeline) | devsecops |
| Infrastructure | containers, deployment |
| Configuration | config |
| Data | data-modeling, data-quality, data-governance, data-migration |

A fork adds tiers of its own, such as language, platform, release and
session templates, under a manifest key of its own.

### Governed tiers

Two opt-in tiers are not left to whatever the dependency declarations
produce. Their membership is stated by stack category — the `layer` each
stack declares in the manifest — with a reason per exempt category, and a
smoke check enforces it in both directions. A stack in a governed category
resolving no member of the tier fails, and a stack declaring no category
fails rather than passing by omission.

| Tier | Exempt categories | Reason | Check |
|------|-------------------|--------|-------|
| Security | library, embedded | a library is imported by a caller that owns the trust boundary; an embedded target has no HTTP surface, sessions or TLS to rule on | SYS-15 |
| Quality gates | named by a fork in `tests/fork_checks.py` | a category recorded at the most constrained context tier cannot admit the tier without changing which models can run the stack | SYS-18 |

Upstream names no quality-gate exemption, because only a fork carries
stacks; the fixture stack is governed by both tiers. Where an exemption's
reason is a property recorded elsewhere in the tree, the check asserts the
reason still holds. The quality-gate exemptions are read against
`tests/context-tiers.txt`, so a category that later moves off the most
constrained tier stops being exempt rather than staying exempt by
omission. See ADR-044.

Membership stated as a list of stack identifiers is what this replaces: a
list is correct on the day it is written and silently wrong at the next
stack.

### File header policy

`[DEPENDS ON: ...]` headers MUST list direct dependencies only —
matching the manifest's `depends_on` for that entry. Headers MUST NOT
expand transitive dependencies.

**Source of truth:** `templates/manifest.yaml` is authoritative. When
a mismatch exists between a file header and the manifest, the manifest
wins and the file header MUST be updated. Smoke check SYS-04 validates
this contract.

### Wiki

The wiki (`docs/wiki/`) gathers human reference documentation
for *projects that use the templates*. It is NOT part of the
dependency graph or agent context. Parent rules files reference
the relevant wiki pages as one-line conventions.

Current wiki pages: `backend.md`, `cicd.md`, `devsecops.md`,
`frontend.md`, `security.md`, `testing.md`.

### Design documents

Design documents (`docs/design/`) are reference material *about the
template library itself* — not conventions for projects using it.
They cover how the library should be reasoned about, audited, and
maintained.

Current design documents:

- `design-notes.md` — the library's design record: the customer
  objective, the operating model it implies, the measured technical
  debt and the standing risks
- `agent-context-tradeoffs.md` — how CLAUDE.md size and
  startup-block design affect agent latency and quality
- `template-content-quality.md` — operational companion: how to
  keep the template library in shape so it doesn't dilute the
  agent's attention, with implications for code review, smoke
  tests, structure audit, and 360
- `efficacy-benchmark.md` — the experiment, its rules fixed in advance, that
  measures whether a generated context file improves an agent's
  output; its harness lives in the Imbra fork, beside the stacks it
  generates from
- `efficacy-assessment.md` — what the benchmark's evidence lets the
  library claim, what it contradicts, and what stays untested
- `testing-ai-assets.md` — the generic method the benchmark applies:
  paired old-versus-new runs, a layered and calibrated judge, and a
  sealed test set, for measuring any template, skill or prompt change

---

## Forks

A fork is a GitHub fork of this repository that carries the content
upstream leaves out: stacks, platforms, the process layer, the interview,
examples and generated chains. ADR-049 sets the model and ADR-050 the
boundary; the first fork is
[Imbra-Ltd/imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates).

| Mechanism | Rule |
|-----------|------|
| Sync by merge | A fork stays current with `git merge upstream/main`, never by copying files |
| Keys of its own | A fork appends under `stacks:`, `platform:` and top-level manifest keys of its own, and never edits `core:`, `base:`, `backend:` or `frontend:`. The resolver reads every top-level list of entries. SYS-20 checks the upstream keys against the revision named by `SAIT_UPSTREAM_REF` |
| `fork_core` | A fork adds to every chain's core tier under `fork_core:`, which the resolver takes after `core:`. A core-tier entry depends only on core-tier IDs: the tier is seeded and never walked, so the resolver refuses a dependency outside it. SYS-21 checks that a fork's key and its `fork_core` entries resolve, and that refusal |
| ID prefixes | `stack-*`, `platform-*` and `<org>-*` belong to forks; upstream adds no ID under them |
| `Fork-merge: ours` | An upstream commit that removes what forks carry carries this trailer. A fork merges everything before it normally, merges it with `git merge -s ours`, then moves its own templates out of upstream's keys into its own key and `fork_core`, and restores each template the commit modified to upstream's text, moving its own lines into fork-owned files. ADR-049 "Merging the split" gives the commands |
| Fork-owned files | `README.md`, `CLAUDE.md` and `CHANGELOG.md` belong to the fork, which resolves them in its own favour on every merge |
| Fork-owned test modules | `tests/fork_checks.py` adds smoke checks for content only a fork carries, `tests/fork_dispositions.py` adds conformance dispositions for its blocks, and `tools/fork_examples.py` names the chain examples `sync.py` renders and, in `CHAIN_EXAMPLES_DOC`, the document they go to (default `docs/SPEC.md`). `run_smoke.py`, `conformance.py` and `sync.py` load each when present, so the runners stay the same file upstream and in every fork |
| Fork sync | `py tests/run_fork_sync.py` simulates a fork on every pull request: it lands the change on a fork that appends a stack and edits its fork-owned files, keeps the fork's side of a conflict in those files, and asserts the merge is otherwise clean |

---

## Deprecation

From 3.0.0 a template is not removed inside a major (ADR-051). It is
deprecated: its manifest entry carries the ID of the template that
replaces it, and the release that marks it lists it under `Deprecated` in
`CHANGELOG.md` with that replacement.

```yaml
- id: base-old
  file: templates/core/old.md
  description: ...
  deprecated: base-new
```

The resolver and the generators read the entry as before, so a chain that
carries a deprecated template still resolves. SYS-22 fails when the field
names no ID, an ID no entry carries, or an entry that is itself deprecated.
The template is removed at the next major.

---

## Override mechanism

Resolution selects source files; project adoption selects operative rules.
The dependency graph and section overrides remain deterministic discovery
mechanisms. A consumer update does not automatically adopt new rules or create
compliance work. Apply "Adopting shared rules" in
`templates/core/docs.md`, and inline that boundary in hybrid
context files. Existing adopted rules remain effective until deliberately changed.

Each base template section is tagged with a unique ID:

```markdown
## Git conventions [ID: base-git]
...
```

A stack template overrides a section by referencing its ID:

```markdown
## Git conventions [OVERRIDE: base-git]
- Always test with `npm run dev` before committing  ← replaces base rule
```

A stack template extends a section by referencing its ID:

```markdown
## Git conventions [EXTEND: base-git]
- Do not commit `dist/` or `node_modules/`  ← added on top of base rules
```

If no override or extend is declared, the base section is used as-is.

### Section tag grammar

A section header MAY combine multiple tags. The valid patterns:

```markdown
## Heading
[ID: section-id]
```

```markdown
## Heading
[ID: section-id]
[DEPENDS ON: path/to/dep.md, path/to/other.md]
```

```markdown
## Heading
[ID: section-id]
[EXTEND: parent-id]
```

```markdown
## Heading
[ID: section-id]
[OVERRIDE: parent-id]
```

Rules:
- `[ID:]` names the section — MUST appear first when combined
- `[DEPENDS ON:]` declares file-level dependencies — metadata,
  not content
- `[EXTEND:]` / `[OVERRIDE:]` declares the relationship to a parent
- A section's content starts after all tag lines
- A section is bounded by the next `[ID:]` tag or end of file
- A section MUST NOT be empty — at least one content line (heading,
  bullet, paragraph, table, or code block) MUST follow the tags

#### Naming another file's section in prose

A rule that names another section in running prose — "`base-quality-gates`
states which categories a project MUST gate" — is not a directive and is
not resolved. It costs reach instead: the referencing file and the
referenced one sit at different depths in the graph, so the reference
reads correctly in the chains carrying both and dangles in the rest.
`base-git` resolves into every chain and `base-data-migration` only into
the chains that opt in, so a reference from the first to the second is
unreadable in the rest.

State the substance inline instead. Where a cross-file reference is
genuinely wanted, the declaring file MUST be present in every chain that
carries the referencing one — SYS-11 checks this per chain, because the
defect is invisible from either file on its own. See ADR-028 for the full
rationale.

An orthogonal template is the sharpest case. It reaches a reader through
no stack chain at all, so its guaranteed context is the core tier plus
its own `depends_on` tree, and nothing beyond what it declares. A
reference out of that is unreadable for every project that opts in.

---

## Precedence rules

When multiple templates reference the same section ID, the following order
applies — higher numbers win:

1. **Base template** — the default; always the lowest precedence
2. **Layer template** (frontend / backend) — overrides or extends the base
3. **Stack template** — overrides or extends the layer or base
4. **Interview answers** — the highest precedence; always win over any template

Example: `templates/core/testing.md` defines the test naming convention.
A fork's `templates/stack/python-fastapi.md`
extends it with a Python-specific pattern. The interview answer "use BDD-style
names" overrides both. The final output uses the interview answer.

---

## Conflict resolution

A conflict occurs when two templates at the same layer reference the same
section ID with different directives (`OVERRIDE` vs `EXTEND`).

**Rule: the more specific directive wins.**

| Situation | Resolution |
|-----------|------------|
| One template `EXTEND`s, another `OVERRIDE`s the same ID | `OVERRIDE` wins — it replaces the base; the `EXTEND` is applied on top of the overridden content |
| Two templates both `OVERRIDE` the same ID | Error — the agent MUST surface this conflict to the user and ask which override to apply |
| Two templates both `EXTEND` the same ID | Both extensions are applied; order follows the dependency declaration in the stack template |

### Specialising across three levels

A stack that depends on another stack MUST NOT override an ID its
dependency already overrides — that is the error above, and the chain
states no winner. The overriding section declares an `[ID:]` of its own,
and the next level overrides that. In Imbra's fork:

```
frontend/static-site.md   [ID: static-site-content]
stack/static-site-astro.md    [ID: astro-content]    [OVERRIDE: static-site-content]
stack/static-site-tutorial.md [ID: tutorial-content] [OVERRIDE: astro-content]
```

Each ID is overridden once, and every level stays available to a stack
that wants to specialise it. `SAIT-SMK-TPL-10-001A` fails a chain that
overrides one ID twice.

**When a conflict cannot be resolved by the rules above**, the agent must:

1. Show the user both conflicting rules
2. Ask which takes precedence
3. Record the decision in the generated context file

---

## Interview template structure

Upstream ships no interview; each fork writes its own and points it at the
fork's stacks. Imbra's fork runs its interview in four phases: explore the
problem, clarify the open choices, propose a setup, then generate the file.
Whatever the structure, the interview hands the agent two things upstream
fixes:

- The output contract in `templates/core/agents.md`: output file, inline or
  hybrid model, and the quality bar
- The questions `templates/core/agents.md` asks every project, which the
  generated file answers or leaves for the project to fill in

The agent asks all required questions before generating anything. Defaults
come from the selected base and stack templates.

---

## How an agent uses the system

1. User provides a fork's interview and a stack template from that fork
   (e.g. `templates/stack/python-fastapi.md`), or the fork's pre-resolved
   chain for the stack
2. Agent reads the stack template, identifies its base dependencies
3. Agent loads the referenced base templates, upstream's and the fork's
4. Agent runs the interview (required questions only)
5. Agent merges: base defaults + stack overrides + interview answers
6. Agent loads the output format template for the chosen AI tool
7. Agent renders and outputs the final context file

Generation stays an agent reading Markdown: no build step or compiler sits
between the fork and the context file. The interview instructions use
neutral language ("ask the user") so any agent can follow them without
tool-specific interpretation.

---

## Consumption model (target)

The current workflow (above) requires the agent to manually navigate
template files. The target model replaces hand-curated file lists with
a declarative header that the agent resolves at startup.

### Lifecycle

```
┌─────────────────────────────────────────────────┐
│  1. SETUP (once)                                │
│     Agent runs the fork's interview →           │
│     writes CLAUDE.md with a declaration block   │
├─────────────────────────────────────────────────┤
│  2. STARTUP (every session)                     │
│     Agent reads CLAUDE.md → reads the fork's    │
│     templates/manifest.yaml → resolves chain    │
├─────────────────────────────────────────────────┤
│  3. DEVELOPMENT (during session)                │
│     Full context loaded — agent applies the     │
│     resolved rules without prompting            │
├─────────────────────────────────────────────────┤
│  4. UPDATE (on upstream change)                 │
│     The fork merges upstream; the project       │
│     moves its pin of the fork (submodule)       │
│     Next session resolves the same chain →      │
│     picks up new/changed rules on next session  │
└─────────────────────────────────────────────────┘
```

### Declaration block

The generated CLAUDE.md contains a machine-readable header instead of
a hand-curated file list:

```markdown
Stack: static-site-astro
Extras: data-quality, 360, issues, scope, review, readme
Platform: github
```

| Field | Required | Description |
|-------|----------|-------------|
| `Stack` | MUST | Stack ID from the fork's `manifest.yaml` |
| `Extras` | MAY | Comma-separated base template IDs not in the stack's dependency chain |
| `Platform` | MAY | Platform ID from the fork (`github`, `gitlab` in Imbra's) |

### Resolution algorithm

Input: declaration block + the fork's `templates/manifest.yaml`.
Output: ordered list of template files to load.

```
1. Seed the core tier: core:, then fork_core:
2. Look up Stack ID in templates/manifest.yaml
3. Recursively resolve depends_on → collect all
   transitive dependencies (depth-first, deduplicated)
4. Resolve each Extra the same way — its depends_on
   tree first, then itself (skip anything already
   in the resolved set)
5. Resolve the Platform template the same way (if
   declared)
6. Return the ordered file list
```

`templates/core/agents.md` is not appended. It governs how the output
is written — structure, model selection, formatting — so it is an input to
generation, applied by whoever produces the file, not a rule file the chain
loads. The diagram above shows it in that position. A project that wants its
rules in the chain declares it as an Extra, where it resolves as its own root
like any other opt-in template.

Ordering: base → backend/frontend → stack (topological sort of
the dependency graph). Within the same depth level, order follows
the `depends_on` list declaration order.

---

## File naming conventions

```
templates/[concern]/[name].md     # cross-cutting — core, security, infra, data
templates/frontend/[concern].md   # frontend layer — UI projects only
templates/backend/[concern].md    # backend layer — services and APIs only
templates/fixture/[name].md       # test input — one stack, one platform
templates/core/agents.md          # output format — structure, models, formatting rules
docs/SPEC.md                      # this file
```

A fork adds its own directories and names its files by its own convention.
Imbra's fork keeps `templates/stack/`, `templates/platform/`,
`templates/workflow/`, `templates/language/` and `templates/INTERVIEW.md`,
and names a stack `<prefix>-<name>.md` (`python-fastapi.md`, `go-echo.md`),
with a bare name for a stack that has no variant.

---

## Roadmap

See [GitHub milestones](https://github.com/solid-ai-dev/solid-ai-templates/milestones).
