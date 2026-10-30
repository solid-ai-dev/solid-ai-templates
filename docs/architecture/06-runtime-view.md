# 6. Runtime view

How the building blocks of chapter 5 work together in the scenarios that
shape the architecture. A project generates its context, a task skill
loads, a shipped hook runs in a project's CI, a fork takes an upstream
change, and a project adopts a release.

The diagrams are UML sequence diagrams. Each block has a lifeline. A solid
line with a filled head is a call that waits for its answer, a dashed line
is the answer, and a solid line with an open head is a message that does
not wait. A frame marks a choice (`alt`) or a repeat (`loop`), with its
condition in brackets. The numbers on the messages are the steps of each
table.

## 6.1 Context generation

The agent writes the project's context files from the chain the resolver
orders, placing each rule where the output contract says.

![Context generation. The team asks the coding agent to generate the context for a root. The agent reads the fork's interview questions and asks the team each one, getting the answers and the adopted rules. It runs the resolver, which seeds the core tier and walks depends_on, and gets the ordered file list. For an inline or hybrid file, it reads each template in order, applies overrides then extensions, places each rule, writes AGENTS.md and CLAUDE.md, and runs the self-check. For a root file with skills, it runs the emitter with the declined list, which places each section by its load and returns the root file and task skills with fact slots, and the agent fills the facts. The agent hands the files to the team for review](../diagrams/runtime-generate.png)

| Step | What happens | Source |
|------|--------------|--------|
| 1 | The team names a root, such as a stack, and the agent generates its context by reading Markdown | FR-05-01 |
| 2-3 | The questions live in the fork's interview. A conflict the rules cannot settle goes to the team, and the answer is recorded in the file | ADR-049, FR-05-03 |
| 4 | The resolver seeds the core tier, then walks `depends_on` depth-first, without duplicates, base before layer before stack | FR-03-02, FR-04-01 |
| 5-6 | An override replaces a section, and each extension of the same ID adds to it. An inline file copies in every adopted rule. A hybrid file copies in every rule whose breach is silent and which no tool enforces, and any other rule may stay a reference | FR-04-02, FR-04-03, ADR-052 |
| 7-8 | The agent writes both files to the output contract, then runs the contract's self-check against them | FR-05-02, FR-05-04 |
| 9 | The emitter leaves out overridden rules and the sections the project declines, places each remaining section by its load, copies each rule's text unchanged, and builds the same files from the same input | ADR-058, proposed; FR-06-03, FR-06-06 |
| 10 | The agent fills only the project's facts, such as names, paths and commands; a regeneration keeps them | ADR-058, proposed |
| 11 | The team reviews the files like any other change | - |

Without Python, the agent walks the chain by hand. It loads every file in
the manifest's `core:` list, then every file in a fork's `fork_core:`
list, then the root's file and every file its dependency lines name,
transitively. Skipping either list loses rules with no error, because no
template declares those files.

## 6.2 Task skill loading

The root file holds the rules for every turn; a procedure for one kind of
task loads only when that task starts.

![Task skill loading. At the start of the session the coding agent reads the root file and gets the rules for every turn and the trigger table. The team gives it a task, such as a release, and the agent matches the task to a trigger. If one matches, it loads that skill's SKILL.md and gets the task's procedures; otherwise it works from the root file alone. It applies the rules, does the task, and returns the change with its evidence](../diagrams/runtime-skill.png)

| Step | What happens | Source |
|------|--------------|--------|
| 1 | A section with no load directive, and every rule guarding data, credentials or authentication, is in the root file | FR-06-01, FR-06-02 |
| 3 | The root file lists each skill with the task that triggers it | FR-06-04 |
| 4 | A skill is one folder under `.agents/skills/`, copied where an agent reads only its own folder | ADR-058, proposed |
| 5 | An agent that cannot load skills gets them inlined in the root file | ADR-058, proposed |

## 6.3 Hook execution in CI

A check too long for a fence ships as a hook, which pre-commit runs at the
revision the project pinned.

![Hook execution in CI. The project's CI runs pre-commit for a hook. pre-commit fetches upstream at the pinned revision and installs the solid-ai-checks command, then runs it with the hook ID. The hook reads the project's tracked files. If the check passes, it exits 0 with the inspected counts; if it finds a breach, it exits 1 with the findings; if it does not apply, it prints a line and exits 0. pre-commit reports pass or fail to CI](../diagrams/runtime-hook.png)

| Step | What happens | Source |
|------|--------------|--------|
| 1-2 | The project's pre-commit configuration names upstream, a revision and the hook IDs, which `.pre-commit-hooks.yaml` lists | FR-07-02, ADR-055 |
| 3-4 | Every hook reads the tracked tree itself, so pre-commit passes it no file names | ADR-055 |
| 5-7 | A check exits 0 on a pass, 1 on a breach and 3 when it does not apply. Under pre-commit, 3 becomes a printed line and exit 0 | FR-07-03 |

## 6.4 Upstream synchronisation

A fork stays current by merging upstream, never by copying files. A commit
that removes what forks carry is marked `Fork-merge: ours`.

![Upstream synchronisation. The fork maintainer fetches upstream and lists the commits carrying Fork-merge: ours, oldest first. For each, the maintainer merges its parent, merges the commit with -s ours, keeping the fork's files, then moves the fork's templates to its own keys and restores upstream's text. The maintainer then merges upstream/main and pushes, and the fork's CI runs smoke against upstream/main](../diagrams/runtime-fork-sync.png)

| Step | What happens | Source |
|------|--------------|--------|
| 1 | The fork fetches upstream from GitHub | FR-08-01, ADR-049 |
| 2-5 | An ordinary merge of a marked commit would delete every file the fork left unchanged and upstream removed | ADR-049 |
| 5 | The fork's templates move out of upstream's keys, into keys of its own, and the core IDs upstream dropped move into `fork_core:` | FR-08-02, FR-08-03 |
| 6-8 | The fork's smoke reads upstream through `SAIT_UPSTREAM_REF` | FR-08-01 |

`py tests/run.py fork_sync` runs the same merge on every pull request
upstream, in a simulated fork that appends a stack and edits its own files
(FR-10-02).

## 6.5 Release adoption

A newer tag adopts nothing by itself. The team decides what the project
takes, and only a regeneration or an edit changes its context files.

![Release adoption. The team asks the coding agent to assess the release. The agent reads the changelog between the pin and the tag and returns the candidates, with what each addresses. The team names the ones to adopt, and the agent moves the pin to the tag, then regenerates or adopts each rule by hand, and returns the change for review](../diagrams/runtime-adopt.png)

| Step | What happens | Source |
|------|--------------|--------|
| 2 | Within 3.x, a release removes or renames nothing frozen, except for a security fix | FR-09-01 |
| 3-4 | Each template rule is a candidate, which the project adopts only for a named defect, requirement or risk | - |
| 5 | The project pins a released tag, by submodule or clone | FR-08-04 |
| 6 | Moving the pin changes nothing in an existing context file. A regeneration does not widen the adopted set | FR-09-03 |

## 6.6 Other scenarios

| Scenario | What happens | Source |
|----------|--------------|--------|
| A pull request upstream | CI runs smoke, conformance and fork sync, and the maintainer approves the merge | FR-10-01, FR-10-02 |
| Cutting a release | The changelog's `Unreleased` section is cut into the version, and `tools/check_release.py` checks the section and the SemVer step before the tag | QG-03-02 |
| Deprecating a template | It keeps resolving until the next major, naming a live replacement | FR-09-02 |
