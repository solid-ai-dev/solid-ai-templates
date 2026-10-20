---
id: "055"
status: Accepted
date: 2026-10-20
category: composition
supersedes: []
superseded_by: []
---

# ADR-055: Long checks become pre-commit hooks

## Context

The templates carry their checks as fenced scripts, so every chain that
loads a template pays for its code in context. A consumer that wants the
check running in its gate copies the script, and the copy drifts.

| Force | What it shows |
| ----- | ------------- |
| Context cost | Measured on `main` on 2026-10-20: 5,478 words of fenced code across the templates, 9% of the corpus. 21 blocks run over 15 lines, 943 lines in all |
| Where it sits | The longest blocks are in `core/quality-gates.md` (33% of the file), `core/docs.md` (22%), `core/agents.md` (22%) and `core/git.md` (19%). The last three are in the core tier, which every chain loads |
| What an agent needs | The command and its pass condition. The script body is read only by the interpreter |
| Unenforced rules | Some rules prescribe a check a consumer must write itself, such as the ban on ticket citations in code. Most consumers adopt the rule and never enforce it |
| Drift | A script copied into a consumer's tree no longer follows the rule it was copied from when the rule changes upstream |
| One maintainer | One release line serves forks and projects. A second line halves the attention each gets |
| The freeze | From 3.0.0, what forks and projects refer to is frozen until 4.0.0, so a change to what a chain carries is cheapest before the tag |

## Decision

A check script longer than 15 lines ships from this repository as a
pre-commit hook, and its template states the hook's command in a fenced
block, with the pass condition beside it.

## Rationale

- The command alone answers what an agent needs, so the context cost falls
  by the script bodies, without losing any rule.
- One repository keeps a rule, its check and the conformance run that tests
  them in one change and one tag, which fits a single maintainer and the
  fork model.
- A pinned hook replaces the copied script, so a consumer runs the check
  the rule names rather than a drifting copy.
- pre-commit provisions the interpreter, which covers the Windows `py`
  launcher, where `PATH` has no `python`.

## Design

1. **Threshold**: a check of 15 lines or fewer stays inline in its
   template. A longer one MUST move to a hook.
2. **Location**: hook code lives under `checks/`, and
   `.pre-commit-hooks.yaml` and `pyproject.toml` sit at the repository root,
   where pre-commit requires them.
3. **Language**: Python standard library only, `language: python`, so the
   hook environment installs nothing from a third party.
4. **Template form**: the template keeps the rule, then a fenced
   `pre-commit run <hook-id> --all-files --verbose`, with the pass condition
   in prose beside it. pre-commit hides a passing hook's output, so the
   command asks for it, and each hook also sets `verbose: true` in
   `.pre-commit-hooks.yaml`.
5. **Output contract**: a hook prints what it inspected, then one line per
   violation (`path:line: CODE message`). Run directly, the check exits 0
   on a pass, 1 on a failure and 3 when it does not apply.
6. **Not applicable under pre-commit**: pre-commit fails a hook on any
   nonzero exit, so the hook entry point prints `not applicable: <reason>`
   and exits 0 where the check would exit 3. The printed line, not the exit
   status, carries the verdict there.
7. **Frozen surface**: a shipped hook ID, its direct exit codes, its
   `not applicable` line and its violation codes are frozen like a section
   ID. A minor adds hooks, and a hook is
   retired only at a major.
8. **Embedded-check authoring**: the rules for writing a script inside
   Markdown (fence indentation, quoted heredocs, escape-free patterns) move
   from `base-quality-gates` to a new opt-in template, `base-embedded-checks`.
   A project whose own docs carry scripts reaches it through `Extras`.
9. **Conformance**: this repository runs every hook against itself, and a
   template block naming a hook resolves to a hook that exists.

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| A separate checks repository | It needs a second release line and a cross-repo pin between each rule and its check, and gives a fork a second upstream. Independent versioning is its only gain, and a patch release here covers it |
| Keep the scripts inline | Every chain keeps paying for the code, and consumers keep copying it |
| Silent on success, as first proposed | A run that reached no files and a run that found nothing print the same thing, which the gate rules forbid |
| Invoke the scripts through the vendored submodule path | A clone without its submodules loses the gate as a missing file, which reads as a broken checkout |

## Consequences

| Area | Change |
| ---- | ------ |
| Stack | The repository ships Python that runs in consumers' CI, beyond `tools/` and `tests/`. `AGENTS.md`, `README.md` and the building-block view say so |
| Root | `.pre-commit-hooks.yaml` and `pyproject.toml` are added |
| Templates | Each block over 15 lines becomes a hook command. The core templates are rewritten together with this change |
| Manifest | Adds `base-embedded-checks`, outside the core tier |
| Tests | Conformance runs the hooks, and a smoke check matches each hook command in a template to a hook ID |
| Release | A checker fix ships as a patch release |
| Migration guide | Gains the hook pin and the `Extras` entry for embedded checks |

## Compatibility

No template path or section ID is renamed or removed. A section that loses
its script keeps its ID and its rule. A project that relied on the
extraction rules declares `base-embedded-checks` in `Extras`. The change
ships in 3.0.0, before the freeze, and the CHANGELOG lists it under
`Changed`.

## Security

A hook is trusted executable code: it runs with the permissions of the
consumer's runner and could write files, start processes or reach the
network. Nothing in pre-commit confines it. The design narrows the trust a
consumer extends, without bounding it:

- A hook is written to read the tree and write nothing, with no network
  access, and review holds it to that. These are conventions, not
  enforcement
- Standard-library-only removes third-party packages from the supply chain
- A consumer pins a tag, which this repository never moves, or a commit
  SHA where it wants the pin to be immutable

## Related

- ADR-031: the fenced-command rule this decision keeps.
- ADR-051: the frozen surface that hook IDs join.
- Issue #1006, the request this answers.
