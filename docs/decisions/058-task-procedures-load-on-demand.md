---
id: "058"
status: Proposed
date: 2026-10-26
category: composition
supersedes: []
superseded_by: []
---

# ADR-058: Task procedures load on demand

## Context

A generated context file copies most of its template chain, so an agent
reads most of the library on every turn, whichever model generated the
file (#2376).

What four fresh generators produced from `main` at `ec00c4f3` on
2026-10-26:

| Delivery | Library, chain of 6,491 words | API, chain of 8,025 words |
| -------- | ----------------------------- | ------------------------- |
| Inline | 4,779 words, 74% of the chain | 7,184 words, 90% |
| Hybrid | 4,921 words, 76% | 5,646 words, 70% |

What fills the inline files, classed rule by rule:

| Material | Library | API | Needed on every turn |
| -------- | ------: | --: | -------------------- |
| Project facts: names, paths, commands, approvals | 9% | 6% | Yes |
| Rules that counter an agent habit | 29% | 22% | Yes |
| Agreed conventions and extra practices | 23% | 28% | Mostly |
| Procedures for one kind of task, such as a release | 27% | 34% | Only during that task |
| Practice an agent follows unprompted | 13% | 11% | No |

What is settled:

- No rule is left to a reference alone. Nothing loads a referenced file,
  and a consumer's agent missed a gate that lived only there (#712).
- Hybrid adhered to project conventions best in round 3 and scored
  highest on the judge's security rows in round 4. The rules that carry
  that apply on every task.
- Length costs. In the 2026-10-17 round every file made the app 40–160%
  bigger, and with a weaker model every generated file lowered the share
  of hidden tests passed. The one generated file that raised it had 39
  lines.
- A skill loads from its description when a task matches it. The format is
  an open standard, published in December 2025, that several coding
  agents report reading, most from `.agents/skills/`.
- A hand-written project in daily use keeps 563 words in its root file and
  about 7,650 in nine skills.

## Decision

A generated context file keeps in context every project fact and every
silent, unenforced rule that applies on every task; it delivers each
procedure for one kind of task as a skill the agent loads when that task
starts, and leaves out practice a capable agent follows unprompted.

## Rationale

- Out of every turn: procedures, the largest class in the API file, load
  only for their task. In the trial the root files fell 49% for the
  library, and 61% to 69% for the API.
- Nothing an agent must not miss is optional: rules for every task and
  security rules stay in context, and no rule is left to a reference.
- No dead weight: practice an agent follows anyway costs no context, and
  the templates keep it as the standard a review applies.
- One format for every agent: the open skill format, with the procedures
  inlined where an agent cannot load skills.
- Scored: 68 of 100, two points ahead of today's hybrid file and of a hard
  size budget, both at 66 (Scoring). The margin is why this record waits
  for a benchmark round.

## Design

![Where a generated file puts a rule: a project fact or a guard on data, credentials or auth goes in the root file; a rule a test, linter or CI step enforces is referenced; a rule followed unprompted and never seen broken is left out; a rule for every task goes in the root file, and one for one kind of task goes in that task's skill, listed in the trigger table. The root file is in context every turn, a skill loads when a task matches its description, and an agent without skills gets the procedures inlined](../diagrams/task-skills.png)

Placement:

| # | Rule | In practice |
| - | ---- | ----------- |
| 1 | The floor | No generated file delivers its rules by reference alone (MUST NOT) |
| 2 | Facts and rules for every task | The root file holds the project's facts and every rule that is silent, unenforced and applies on every task (MUST) |
| 3 | Security stays | A rule whose breaking exposes data, credentials or an unauthenticated path stays in the root file, even when it applies to one kind of task (MUST) |
| 4 | Obligation or technique | An obligation for every change, such as testing what changed, goes in the root file. The technique for meeting it, such as isolating a test, goes in the skill for the task that uses it |
| 5 | Unprompted practice | A rule a capable agent follows unprompted is left out of the root file and the skills (SHOULD NOT inline). A rule the project has seen broken is inlined (MUST) |
| 6 | Enforced rules | A rule a test, linter or CI step enforces is referenced (SHOULD). Without the templates in the tree, the reference names the tool and its configuration |
| 7 | One home | A rule sits in the root file or in one skill (MUST). A skill may point to a root-file rule, never restate it |

Skills:

| # | Rule | In practice |
| - | ---- | ----------- |
| 8 | Task procedures | A rule that applies only during one kind of task, such as a release, a migration or verifying a finding, goes in that task's skill (SHOULD) |
| 9 | One kind of task each | A skill covers one kind of task, never a single rule; a one-line procedure joins the skill for its task (MUST) |
| 10 | The trigger table | The root file lists each skill with the task that triggers it (MUST) |
| 11 | One format | The open Agent Skills format: a folder holding `SKILL.md`, whose frontmatter carries `name` and a `description` naming the task that triggers it. The body names no agent-specific mechanism (MUST) |
| 12 | One source, mirrored | Each skill is generated once, under `.agents/skills/<name>/`, and copied unchanged where an agent reads only a folder of its own, such as `.claude/skills/`. A copy is never edited by hand (MUST) |
| 13 | No skill support | Where the project's agent cannot load skills on demand, the procedures are inlined in the root file (MUST) |

The file:

| # | Rule | In practice |
| - | ---- | ----------- |
| 14 | Checks by command | The root file and every skill state a check by its command and pass condition, never by copying a script body (MUST) |
| 15 | The model's name | The overview states `Model: root and skills` |
| 16 | Length reported | The generator reports the root file's line and word count (MUST). This record sets no size limit |

## Alternatives considered

Every option weighed, lettered from A, the chosen one first, with its
score out of 100 (Scoring):

| # | Alternative | Score | Outcome |
| - | ----------- | ----- | ------- |
| A | A root file for facts and rules for every task, a skill per kind of task | 68 | Chosen: procedures leave every turn, and every rule an agent must not miss stays |
| B | Hybrid, as today | 66 | Measured at 70–76% of the chain, and length is a cost in the benchmark |
| C | Inline everything | 63 | Up to 90% of the chain on every turn; the full inline file did worse than no file in the 2026-10-17 round |
| D | A hard size budget, such as 40 lines | 66 | The rules for every task alone exceed it, so a budget drops habit counters and security rules rather than procedures |
| E | Plain references with a trigger table | 57 | A plain reference has no loading mechanism, and the consumer failure shows what that costs |
| F | Rules scoped by file path | 49 | Loads on the files touched, not the task started; a release or a review touches no single path, and the mechanism differs per agent |

## Consequences

| Consequence | Effect |
| ----------- | ------ |
| `agents.md` | States the placement, the trigger table and the skill rules, and its model table shows root and skills (#2376) |
| `agents.md` gaps | Closes what the 2026-10-26 generators filled by invention: a checkable rule with no tool, a missing end-of-session checklist, an override order for a single rule source (#2376) |
| Baseline | The four 2026-10-26 files are regenerated under this record, and their counts recorded beside the baseline (#2376) |
| Forks | The interview applies the placement. A benchmark round compares root and skills with hybrid and with no file; worse than hybrid on adherence or on the judge's security and data-protection rows reopens this record |
| Open | Which rules count as unprompted practice stays a generator's judgement until a round measures it. Two generators given the same rules put 2,437 and 2,198 words in their root files, the larger for the smaller project (#2376) |

## Compatibility

A project's existing file keeps working: nothing it names is removed. Its
next regeneration produces a root file and skills where its agent loads
skills, and a hybrid file otherwise. Skills are files the project may
decline, which leaves today's hybrid file.

## Security

- Protects: every rule whose breaking exposes data, credentials or an
  unauthenticated path stays in the root file, so none depends on a skill
  loading.
- Exposes: a procedure in a skill whose trigger is missed is not read for
  that task. The trigger table and the description guard it.
- Trust boundary: a skill is a file in the project's tree, under the same
  review as the context file.

## Scoring

Each option was scored 1 (poor) to 5 (good) per criterion, by the author's
judgement against the measurements in Context. Its score is the sum of
weight times score, divided by 5, so 100 is the best.

| Criterion | Weight | Why it weighs this much |
| --------- | ------ | ----------------------- |
| Context per turn | 25 | The agent's view: the words it reads before the task, which the benchmark shows cost size and correctness |
| Rules that must not be missed | 25 | The project's view: rules for every task and security rules in context with no cue needed |
| Evidence | 15 | The maintainer's view: how far a measured result supports the option |
| Works with every agent | 15 | The consumer's view: one generated set serves whichever agent a team uses |
| Generator consistency | 10 | The reviewer's view: two generators given the same chain place rules alike |
| Maintenance | 10 | What it costs to keep templates, `agents.md` and generated files in step |

The score matrix, one column per alternative, A being this decision:

| Criterion | Weight | A | B | C | D | E | F |
| --------- | ------ | - | - | - | - | - | - |
| Context per turn | 25 | 4 | 1 | 1 | 5 | 4 | 3 |
| Rules that must not be missed | 25 | 4 | 5 | 5 | 1 | 1 | 3 |
| Evidence | 15 | 2 | 3 | 2 | 3 | 1 | 1 |
| Works with every agent | 15 | 4 | 5 | 5 | 5 | 5 | 2 |
| Generator consistency | 10 | 2 | 2 | 3 | 2 | 3 | 3 |
| Maintenance | 10 | 3 | 4 | 3 | 4 | 4 | 2 |
| Score, of 100 | | 68 | 66 | 63 | 66 | 57 | 49 |

Sensitivity: each row raises one criterion's weight and lowers the other
five in proportion, so the weights still total 100.

| Alternative | Where it beats A | Weight now | It wins above |
| ----------- | ---------------- | ---------- | ------------- |
| B | Rules that must not be missed | 25 | About 32 |
| B | Evidence | 15 | About 23 |
| B | Works with every agent | 15 | About 23 |
| B | Maintenance | 10 | About 18 |
| C | Rules that must not be missed | 25 | About 40 |
| D | Context per turn | 25 | About 32 |
| D | Evidence | 15 | About 23 |
| D | Works with every agent | 15 | About 23 |
| E | Works with every agent | 15 | About 45 |
| F | Generator consistency | 10 | About 54 |

The margin is thin. Hybrid wins if evidence weighs a half more than it
does, and a size budget wins if context per turn weighs about a quarter more.
A benchmark round that measures A raises its evidence score and settles
which.
