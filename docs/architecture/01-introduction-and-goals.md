# 1. Introduction and goals

solid-ai-templates is a library of composable rule templates. An LLM agent
reads them to write a project's context files, `AGENTS.md` and `CLAUDE.md`.
Each template covers one concern, extends others without editing them, and
composes into a chain for one stack.

The templates are one of three parts of the solid-ai-dev group, which aims
at autonomous development with little technical supervision.

| Part | Repository | Role |
|------|------------|------|
| Templates | solid-ai-templates | Rules that get an agent to good enough code on the first attempt |
| Orchestrator | solid-ai-dirigent | Runs one agent that develops and a second that reviews |
| Skills | solid-ai-skills | Procedures an agent loads for one kind of task |

This repository is upstream. It holds the composition engine and the policy
every team shares. Forks carry the stacks, platforms, process rules and the
interview, and stay current by merging upstream (chapter 3).

What it does:

- Gives agents shared engineering rules.
- Resolves the templates a project picks into one ordered chain.
- Builds the context file an agent reads on every turn and the skills it loads
  for one task.
- Ships checks for its rules, run as pre-commit hooks in a project's CI.
- Lets a fork add and override rules without editing upstream's files.

How it is built:

- Markdown templates, one concern each, registered in
  `templates/manifest.yaml`.
- Directives in the templates declare dependencies, extensions and
  overrides.
- Python tools resolve chains, regenerate derived docs and check releases.
- Test runners check the templates' structure and run their shipped checks.

Who is responsible:

- The team owns the high-level design, the specifications, the test
  expectations, acceptance and dogfooding.
- Agents implement and review. Their code and tests never redefine the
  intended behaviour.
- Upstream owns the shared policy.
- A fork owns its stacks, platforms, process rules and interview.

## 1.1 Business goals

> Agents produce good enough (B grade) code on the first attempt, at a
> bounded cost, readable by people and fit for production.

| # | Goal | Outcome | Measure |
| - | ---- | ------- | ------- |
| 1 | Good enough first time | Changes accepted with little or no rework | Rework per accepted change, in human time and tokens |
| 2 | Bounded cost | Each change fits a time limit on the chosen model | Time, tokens and cost per accepted change |
| 3 | Readable by people | A person follows a change without asking the agent | Readability findings per accepted change |
| 4 | Fit for production | No severe failure, such as lost data or missing authorization | Severe failures and regressions in a follow-up window |
| 5 | Cheap adoption | Releases adopted without rework | Adoption effort per release |
| 6 | Portable policy | The same rules survive a change of stack or agent | Shared rules a project keeps after changing stack or agent |

## 1.2 Requirements overview

What upstream provides to a fork and, through the fork, to a project. Terms
are defined in the [glossary](12-glossary.md).

| # | Capability | What the system does |
| - | ---------- | -------------------- |
| 01 | Shared rules | Supplies the rules every project needs, for quality, Git, documentation, testing and review, one concern per template. |
| 02 | Layers | Adds rules shared by one kind of project, such as HTTP and databases for a backend, or UX and static sites for a frontend. |
| 03 | Manifest | Registers every template once, with its dependencies and its tier, so every tool reads the same graph. |
| 04 | Composition | Resolves a project's chosen roots into one ordered chain and applies each template's extensions and overrides in a defined precedence. |
| 05 | Context generation | Gives an agent the chain and the output format, from which it writes the project's context file with the answers to the fork's interview. |
| 06 | Context file and task skills | Splits a chain into a context file read on every turn and skills loaded only when their task starts. |
| 07 | Shipped checks | States each mechanically checkable rule with a command and a pass condition, and ships the longer checks as pre-commit hooks. |
| 08 | Fork extension | Lets a fork add stacks, platforms, process rules and its interview under keys of its own, and take upstream's changes by merge. |
| 09 | Versioned releases | Releases with a changelog and semantic versions, keeps section and hook IDs stable, and changes no project's rules until it adopts a release. |
| 10 | Self-checks | Checks every change for broken references, invalid chains, failing shipped checks, duplicate rules and lower template scores, and merges it into a simulated fork. |

## 1.3 Quality goals

The prioritized goals. Chapter 10 names each one's instrument, baseline and
scenarios.

| Priority | Goal | Meaning here |
|----------|------|--------------|
| 1 | Correctness | Composition and precedence resolve as specified, with no conflicting instruction and no lost user work |
| 2 | Effectiveness | An agent given a generated file completes representative tasks at least as well as without one |
| 3 | Efficiency | Context, time and cost stay proportionate to the outcome. A smaller file is better only if outcomes hold |
| 4 | Predictability | A version change has an explainable effect and a manageable migration |
| 5 | Maintainability | Few recurring defects and little policy-induced work for maintainers and consumers |

A change is admitted when it improves a demonstrated outcome enough to
justify the cost every affected consumer carries. One team's preference does
not justify a shared rule.

## 1.4 Stakeholders

| Stakeholder | Expectation |
|-------------|-------------|
| Small engineering team already using coding agents, through a fork | Hand implementation and review to agents with little technical supervision, apply its own standards on top of the shared ones, and adopt releases without rework each time |
| Fork maintainer, with Imbra's private fork the first | Add stacks, platforms and process rules without editing upstream's files, against a stable contract, and take upstream's changes by merge without conflict |
| Upstream contributor | Change a shared rule with evidence that it helps, at a cost every chain carrying it can afford |
| Coding agents reading a generated file | Rules they can apply without guessing, at a context cost proportionate to the task |
| Imbra Ltd, Branimir Georgiev (owner and maintainer) | A library that is cheap to keep correct |
