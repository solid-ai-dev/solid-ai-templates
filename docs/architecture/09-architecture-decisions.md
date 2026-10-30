# 9. Architecture decisions

The decisions recorded for solid-ai-templates, grouped by the part of the
system each one shapes. From 3.0 a record is written only when a decision
changes something a consuming project can observe, the composition model
above all. Earlier records also cover this repository's own process. Each
row gives a record's decision in one line, and the record holds its
context, the alternatives it beat and its consequences.

- Status "Accepted" means the decision holds. "Proposed" means the record
  is drafted and waits for its first implementation. "Superseded" names the
  record that replaced it, and "Withdrawn" means it was dropped before it
  took effect.
- Where a record and the templates disagree, the templates govern and the
  record stands as history.
- Each record sits in one group. The rows run in record order.

## 9.1 Composition model

How templates combine into one chain, which rule wins, and how far a
reference reaches.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-001](../decisions/001-inheritance-model.md) | Templates compose in three layers, base, layer and stack, with the platform orthogonal, through the dependency, extend and override directives | Accepted |
| [ADR-004](../decisions/004-composition-over-inheritance.md) | A stack composes only the modules it needs, with no transitive surprises | Accepted |
| [ADR-027](../decisions/027-language-layer-owns-tool-selection.md) | The language layer selects each language's tools, the abstract gate names none, and a stack binds only the tools its own shape adds | Accepted |
| [ADR-028](../decisions/028-prose-references-bounded-by-chain-reach.md) | A template names another file's section in prose only where that file is in every chain carrying it, and a check verifies this per chain | Accepted |
| [ADR-035](../decisions/035-orthogonal-templates-are-resolution-roots.md) | An orthogonal template no stack reaches is a root of its own, and its references resolve within that root's chain | Accepted |
| [ADR-039](../decisions/039-one-override-per-id-per-chain.md) | A chain overrides each section ID once, and a section that expects further specialisation declares an ID of its own | Accepted |
| [ADR-043](../decisions/043-declaring-a-core-file-is-redundant-not-forbidden.md) | A template may declare a core-tier file, but no chain relies on that declaration to resolve it | Accepted |
| [ADR-044](../decisions/044-rule-family-membership-is-declared-by-category.md) | An opt-in rule family's membership is declared by stack category, with a reason for each exempt category, and checked both ways | Accepted |

## 9.2 Context files and skills

What a project's generated files hold, and how the rules reach them.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-007](../decisions/007-generation-out-of-scope.md) | The product is the template library, not a generation tool, and a local agent generates a project's files | Accepted |
| [ADR-016](../decisions/016-examples-generated.md) | Example context files are generated through the documented path and regenerated, never patched by hand | Accepted |
| [ADR-022](../decisions/022-skill-authoring-in-scope.md) | A skill is an in-scope artifact, governed by a template of its own, and holds an on-demand procedure that never restates the context file | Accepted |
| [ADR-052](../decisions/052-hybrid-is-the-delivery-floor.md) | A context file delivers rules inline or hybrid, never by reference alone, and inlines every rule whose breach is silent and which no tool enforces | Accepted |
| [ADR-053](../decisions/053-declaration-block-is-a-target.md) | The declaration block leaves the frozen surface until a release ships a tool that writes it and one that reads it | Accepted |
| [ADR-058](../decisions/058-task-procedures-load-on-demand.md) | Each section declares where its rules load, and a tool builds the root file and one skill per kind of task from the adopted rules | Proposed |

## 9.3 Template content

Which template holds a rule, and how a template is structured.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-003](../decisions/003-360-analysis.md) | A four-category assessment, Value, Quality, Viability and Discovery, ships as a template with a role prompt for each | Accepted |
| [ADR-005](../decisions/005-base-reorganization.md) | The template source nests under `templates/`, and `base/` splits into subfolders by concern | Superseded by ADR-050 |
| [ADR-009](../decisions/009-stack-scope-cap.md) | The library holds a curated set of stacks, and company and team stacks live in their own repositories | Superseded by ADR-049 |
| [ADR-012](../decisions/012-data-quality-wiring.md) | Only `stack-python-service` depends on `base-data-quality` | Superseded by ADR-013 |
| [ADR-013](../decisions/013-split-data-quality.md) | The calibration and tool-trust rules move into the core tier, and the data research and schema rules stay opt-in | Accepted |
| [ADR-017](../decisions/017-stack-section-structure.md) | Stack templates follow one section structure, in RFC 2119 tiers, with the MUST tier checked | Accepted |
| [ADR-020](../decisions/020-structure-section-ownership.md) | The README holds a project's only directory map, and the context file points to it | Accepted |
| [ADR-025](../decisions/025-examples-get-their-own-template.md) | The rules for an `examples/` directory move to a template of their own, reached by declaring it | Accepted |
| [ADR-029](../decisions/029-changelog-adopted-by-reference.md) | A project that publishes versions keeps a changelog, and one adopting it late records earlier versions by naming where they are published | Accepted |
| [ADR-046](../decisions/046-object-oriented-design-guidance-is-core.md) | `base-oop` joins the core tier | Superseded by ADR-057 |
| [ADR-047](../decisions/047-guide-docs-under-docs-are-kebab-case.md) | Every file under `docs/` takes a lower kebab-case name | Withdrawn |
| [ADR-048](../decisions/048-a-lessons-log-replaces-the-development-journal.md) | A lessons log replaces the development journal | Withdrawn |
| [ADR-054](../decisions/054-frontend-content-layer.md) | The content, asset, SEO and structured-data rules form a frontend layer of their own | Accepted |
| [ADR-056](../decisions/056-measurement-rules-are-opt-in.md) | The expensive-computation, calibration and source-silence rules move into the opt-in `base-measurement` | Accepted |
| [ADR-057](../decisions/057-object-oriented-design-guidance-is-opt-in.md) | `base-oop` leaves the core tier and becomes opt-in | Accepted |

## 9.4 Upstream and forks

What upstream keeps, and what a fork carries.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-049](../decisions/049-forks-carry-stacks-and-process.md) | Forks carry the stacks, platforms, process layer, interview and examples, and stay current by merging upstream | Accepted |
| [ADR-050](../decisions/050-what-stays-upstream.md) | Upstream keeps the rules that hold for any stack, platform or way of working, and every answer about how a team works moves to forks | Accepted |

## 9.5 Releases and compatibility

How a release is versioned and gated, and what it may change.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-006](../decisions/006-release-versioning.md) | Releases follow three-digit SemVer, a minor per milestone | Accepted |
| [ADR-033](../decisions/033-periodic-review-scoped-to-minor-and-major.md) | A periodic review is owed by minor and major releases only | Superseded by ADR-045 |
| [ADR-037](../decisions/037-release-proposal-names-every-pre-release-step.md) | The release proposal names every pre-release step and the result it produced | Accepted |
| [ADR-042](../decisions/042-a-tag-push-runs-the-release-gates.md) | A tag push runs the release gates, each reading its baseline from the commit under release | Accepted |
| [ADR-045](../decisions/045-periodic-review-paced-by-record-age.md) | A periodic review is owed when the newest record is older than the declared interval | Accepted |
| [ADR-051](../decisions/051-compatibility-from-3-0.md) | From 3.0.0 a release only adds or deprecates until 4.0.0, except for a security fix, and 2.x receives nothing after v2.90.0 | Accepted |

## 9.6 Shipped checks

How a template states a check, how it reports, and how this repository
runs its own.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-019](../decisions/019-redundancy-detection.md) | Redundancy is detected on each resolved chain, and CI fails only on an exact duplicate outside the baseline | Accepted |
| [ADR-030](../decisions/030-repository-runs-its-own-shipped-checks.md) | This repository runs every check its templates ship, and each one carries a written disposition | Accepted |
| [ADR-031](../decisions/031-shipped-check-states-command-in-fence.md) | A shipped check states its command in a fence, with its pass condition beside it | Accepted |
| [ADR-032](../decisions/032-check-reports-inapplicability-with-status.md) | A check that does not apply exits 3, which a runner counts apart from a pass or a failure | Accepted |
| [ADR-034](../decisions/034-runner-rejects-a-pass-reporting-no-input.md) | The runner fails a check that passes while reporting no input | Accepted |
| [ADR-036](../decisions/036-chain-size-is-capped-by-a-frozen-ceiling.md) | Every root's chain size is capped at a frozen ceiling | Superseded by ADR-041 |
| [ADR-038](../decisions/038-redundancy-gate-tiers.md) | The redundancy gate fails on exact duplicates and reports near ones | Accepted |
| [ADR-040](../decisions/040-a-reading-is-budgeted-not-scored.md) | Each check allowed to await a person's reading is named in a budget file, and the runner fails on any other | Accepted |
| [ADR-041](../decisions/041-chain-size-is-reported-not-capped.md) | Chain size is reported, not capped | Accepted |
| [ADR-055](../decisions/055-long-checks-become-hooks.md) | A check script over 15 lines ships as a pre-commit hook, and its template states the hook's command | Accepted |

## 9.7 Process and records

How this repository tracks work and keeps its records.

| Record | Decision | Status |
| ------ | -------- | ------ |
| [ADR-002](../decisions/002-label-standardization.md) | Every repository uses one label set, and every issue carries one type and one priority | Accepted |
| [ADR-008](../decisions/008-naming-conventions.md) | Issue titles are imperative in sentence case, and PR titles take the Conventional Commits form ending with the issue numbers | Accepted |
| [ADR-010](../decisions/010-adr-governance.md) | A record carries front matter with its ID, status, date, category and two-way supersession links | Accepted |
| [ADR-011](../decisions/011-provenance-principle.md) | A new rule cites the incident that surfaced it, in the issue proposing it, not in the template | Accepted |
| [ADR-014](../decisions/014-one-concern-per-adr.md) | Each record addresses one concern | Accepted |
| [ADR-015](../decisions/015-dev-journal-ordering.md) | Development journal entries run oldest first | Accepted |
| [ADR-018](../decisions/018-audit-storage-convention.md) | Each assessment is stored as a dated report under `docs/audits/` | Accepted |
| [ADR-021](../decisions/021-priority-scale-four-severities.md) | Four severities, with `P4` marking deferral | Superseded by ADR-024 |
| [ADR-023](../decisions/023-no-named-milestone-lanes.md) | No named holding milestone, with deferral and urgency carried on labels | Accepted |
| [ADR-024](../decisions/024-priority-severity-only.md) | Priority is severity only, and an empty milestone field marks deferral | Accepted |
| [ADR-026](../decisions/026-stale-claim-corrected-by-new-record.md) | A merged record's claim that a later decision falsifies is corrected by a new record, never by editing it | Accepted |
