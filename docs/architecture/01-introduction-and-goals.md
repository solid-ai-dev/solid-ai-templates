# 1. Introduction and goals

solid-ai-templates is a library of composable rule templates. An LLM agent
reads them to draft a project's context files, `AGENTS.md` and `CLAUDE.md`,
for any kind of project, from a static site to a Python SDK. Each template
covers one concern, extends others without editing them, and composes into
a chain for one stack.

This repository is upstream: it holds the composition engine and the policy
every team shares. Forks carry the stacks, platforms, process rules and the
interview, and stay current by merging upstream (chapter 3).

## 1.1 Customer outcome

> Enable small teams to delegate coding and routine code review to agents
> while concentrating on specifications, architecture, tests, and acceptance
> of behaviour.

The primary measure is human effort per accepted change: specification,
supervision, review and repair time, plus a share of setup and maintenance.
An accepted change meets independently defined acceptance criteria, not an
agent's claim that it is finished. Total delivery cost, regressions in a
follow-up window, and failed or unfinished tasks are reported beside it.

## 1.2 Users

| User | Needs |
|------|-------|
| Small engineering team already using coding agents | Delegate routine implementation and review without continuous supervision, and apply its own standards on top of the shared ones |
| Fork maintainer | Add stacks, platforms and process rules without editing upstream's files, and take upstream's changes by merge |
| Upstream contributor | Change a shared rule with evidence that it helps, at a cost every chain carrying it can afford |

The team owns the specification, the architecture, the test expectations
and acceptance. Agents assist; agent-written code and tests do not redefine
the intended behaviour.

## 1.3 Quality goals

The prioritized goals. Chapter 10 names each one's instrument, baseline and
scenarios.

| Priority | Goal | Meaning here |
|----------|------|--------------|
| 1 | Correctness | Composition and precedence resolve as specified; no conflicting instruction and no lost user work |
| 2 | Effectiveness | An agent given a generated file completes representative tasks at least as well as without one |
| 3 | Efficiency | Context, time and cost stay proportionate to the outcome; a smaller file is better only if outcomes hold |
| 4 | Predictability | A version change has an explainable effect and a manageable migration |
| 5 | Maintainability | Few recurring defects and little policy-induced work for maintainers and consumers |

A change is admitted when it improves a demonstrated outcome enough to
justify the cost every affected consumer carries. One team's preference does
not justify a shared rule.

## 1.4 Stakeholders

| Role | Who | Expectation |
|------|-----|-------------|
| Owner and maintainer | Imbra Ltd, Branimir Georgiev | A library that is cheap to keep correct |
| First fork | [Imbra-Ltd/imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates) | Stable contract, merges without conflict |
| Consumer projects | Teams generating from a fork | Rules that fit the project and do not create adoption work on every release |
