---
id: "058"
status: Proposed
date: 2026-10-26
category: composition
supersedes: []
superseded_by: []
---

# ADR-058: Templates place each rule, and task procedures load on demand

## Context

The templates exist to even out results across teams and agents: every
project that picks the same templates should get the same grade, rather
than one an A and another a D. A generated context file works against that
twice (#2376).

- It is long: it copies most of its template chain, so an agent reads most
  of the library on every turn.
- It varies: the generating agent decides which rules apply, which to
  inline and which to leave out, and two agents decide differently.

What four fresh generators produced from `main` at `ec00c4f3` on
2026-10-26:

| Delivery | Library, chain of 6,491 words | API, chain of 8,025 words |
| -------- | ----------------------------- | ------------------------- |
| Inline | 4,779 words, 74% of the chain | 7,184 words, 90% |
| Hybrid | 4,921 words, 76% | 5,646 words, 70% |
| Root file and skills, placed by the generator | 2,437 words, plus 9 skills | 2,198 words, plus 14 skills |

The last row varies by generator: the smaller project got the larger root
file, and each generator left out a different set of rules as practice an
agent follows anyway.

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
  of hidden tests passed.
- A skill loads from its description when a task matches it. The format is
  an open standard, published in December 2025, that several coding
  agents report reading, most from `.agents/skills/`.
- A hand-written project in daily use keeps 563 words in its root file and
  about 7,650 in nine skills.

## Decision

Each template section declares where its rules load, on every turn or for
a named kind of task, and a tool builds the root file and one skill per
kind of task from the adopted rules, so the same templates give every
project the same files.

## Rationale

- Same input, same files: placement is decided once, in the templates,
  and a tool applies it. No generating agent judges which rules apply or
  where they go.
- Out of every turn: procedures, the largest class in the API file, load
  only for their task.
- Nothing an agent must not miss is optional: unmarked sections and
  security rules stay in context, and no rule is left to a reference.
- One format for every agent: the open skill format, with the procedures
  inlined where an agent cannot load skills.
- Scored: 77 of 100. The same split decided by each generator scores 62,
  and today's hybrid file 61 (Scoring).

## Design

![Where a generated file puts a rule: a template section declares its load. A section with no mark goes in the root file, in context on every turn; a section marked with a task, such as a release, goes in that task's skill, listed in the root file's trigger table; a section marked as checked is referenced with the check that enforces it. A tool builds the root file and the skills from the adopted rules, and the generating agent fills only the project's facts; an agent without skills gets the skills inlined in the root file](../diagrams/task-skills.png)

In the templates:

| # | Rule | In practice |
| - | ---- | ----------- |
| 1 | The load directive | A section MAY carry a load directive under its heading, naming a kind of task, such as `release`, or `check` for a section a check enforces. A section without one loads on every turn |
| 2 | One vocabulary | The manifest lists the kinds of task, each with the description its skill carries. A load directive names only a listed kind (MUST); a fork MAY add kinds of its own |
| 3 | One load per section | A section that mixes rules for every turn with a procedure for one task is split, so each section has one load (MUST) |
| 4 | Security stays | A section whose breaking exposes data, credentials or an unauthenticated path carries no task directive (MUST NOT) |
| 5 | No unprompted practice | A rule an agent follows unprompted is removed from the template in review, never left out by a generator |

In the generated files:

| # | Rule | In practice |
| - | ---- | ----------- |
| 6 | The floor | No generated file delivers its rules by reference alone (MUST NOT) |
| 7 | Built by a tool | A tool builds the rules of the root file and the skills from the chain and the project's adopted list, copying each rule's text unchanged. The same input gives byte-identical files (MUST) |
| 8 | Adoption is declared | A section the project does not adopt is named in its adopted list. The tool reads the list; no agent judges what applies (MUST) |
| 9 | Facts by the agent | The generating agent or the interview writes only the project's facts into the root file's slots: names, paths, commands, approvals |
| 10 | The trigger table | The root file lists each skill with the task that triggers it (MUST) |
| 11 | One format | The open Agent Skills format: a folder holding `SKILL.md`, whose frontmatter carries `name` and the kind's `description`. The body names no agent-specific mechanism (MUST) |
| 12 | One source, mirrored | Each skill is built once, under `.agents/skills/<kind>/`, and copied unchanged where an agent reads only a folder of its own, such as `.claude/skills/`. A copy is never edited by hand (MUST) |
| 13 | No skill support | Where the project's agent cannot load skills on demand, the tool inlines the skills in the root file (MUST) |
| 14 | Checked sections | A section marked `check` is referenced by its command and pass condition, never by copying a script body (MUST) |
| 15 | The model's name | The overview states `Model: root and skills` |
| 16 | Size published | The root file's and each skill's word count per root is generated into the documentation, so a change to a template shows its cost (MUST) |

## Alternatives considered

Every option weighed, lettered from A, the chosen one first, with its
score out of 100 (Scoring):

| # | Alternative | Score | Outcome |
| - | ----------- | ----- | ------- |
| A | Templates declare each section's load, and a tool builds the root file and skills | 77 | Chosen: the same templates give the same files, and procedures leave every turn |
| B | The same split, decided by each generating agent | 62 | Two generators placed the same rules differently, so results vary by agent and run |
| C | Hybrid, as today | 61 | Measured at 70–76% of the chain, and the generator still judges what to inline |
| D | Inline everything | 61 | Up to 90% of the chain on every turn; the full inline file did worse than no file in the 2026-10-17 round |
| E | A hard size budget, such as 40 lines | 61 | The rules for every task alone exceed it, so what to cut is left to each generator |
| F | Plain references with a trigger table | 56 | A plain reference has no loading mechanism, and the consumer failure shows what that costs |
| G | Rules scoped by file path | 50 | Loads on the files touched, not the task started, and the mechanism differs per agent |

## Consequences

| Consequence | Effect |
| ----------- | ------ |
| Templates | Each section that holds a task procedure gets a load directive, and mixed sections are split. Splitting is cheapest before the 3.0.0 tag freezes the headings a section holds; after it, a procedure moves to a new section at the end of its file |
| Template review | Practice an agent follows unprompted is removed, so no generator has to leave it out |
| Manifest | An optional `tasks:` list: each kind's name and description |
| Tool | The resolver gains a mode that builds the root file's rules and the skills from a chain and an adopted list; a smoke check asserts two runs give identical files |
| `agents.md` | States the load directive, the trigger table and the skill rules, and its model table shows root and skills. It closes the gaps the 2026-10-26 generators filled by invention: a checkable rule with no tool, a missing end-of-session checklist, an override order for a single rule source |
| Documentation | A generated table of root-file and skill words per root |
| Forks | The interview records the adopted list and the facts. A benchmark round compares root and skills with hybrid and with no file, scored by the spread across runs and projects as well as the mean; worse than hybrid on adherence or on the judge's security and data-protection rows reopens this record |

## Compatibility

A project's existing file keeps working: nothing it names is removed. Its
next regeneration produces a root file and skills where its agent loads
skills, and one root file otherwise. A section without a load directive
loads on every turn, so a template or a fork that adds none generates what
inline generates today.

## Security

- Protects: a section that guards data, credentials or authentication
  carries no task directive, so it is in context on every turn and depends
  on no skill loading.
- Exposes: a procedure in a skill whose trigger is missed is not read for
  that task. The trigger table and the kind's description guard it.
- Trust boundary: a skill is a file in the project's tree, built by the
  tool and under the same review as the context file.

## Scoring

Each option was scored 1 (poor) to 5 (good) per criterion, by the author's
judgement against the measurements in Context. Its score is the sum of
weight times score, divided by 5, so 100 is the best.

| Criterion | Weight | Why it weighs this much |
| --------- | ------ | ----------------------- |
| Consistency | 25 | The maintainer's goal: the same templates give the same files and the same grade, whichever team or agent generates them |
| Context per turn | 20 | The agent's view: the words it reads before the task, which the benchmark shows cost size and correctness |
| Rules that must not be missed | 20 | The project's view: rules for every task and security rules in context with no cue needed |
| Evidence | 15 | How far a measured result supports the option |
| Works with every agent | 10 | The consumer's view: one generated set serves whichever agent a team uses |
| Maintenance | 10 | What it costs to keep templates, the tool and generated files in step |

The score matrix, one column per alternative, A being this decision:

| Criterion | Weight | A | B | C | D | E | F | G |
| --------- | ------ | - | - | - | - | - | - | - |
| Consistency | 25 | 5 | 2 | 2 | 3 | 2 | 3 | 3 |
| Context per turn | 20 | 4 | 4 | 1 | 1 | 5 | 4 | 3 |
| Rules that must not be missed | 20 | 4 | 4 | 5 | 5 | 1 | 1 | 3 |
| Evidence | 15 | 2 | 2 | 3 | 2 | 3 | 1 | 1 |
| Works with every agent | 10 | 4 | 4 | 5 | 5 | 5 | 5 | 2 |
| Maintenance | 10 | 3 | 3 | 4 | 3 | 4 | 4 | 2 |
| Score, of 100 | | 77 | 62 | 61 | 61 | 61 | 56 | 50 |

Sensitivity: each row raises one criterion's weight and lowers the other
five in proportion, so the weights still total 100.

| Alternative | Where it beats A | Weight now | It wins above |
| ----------- | ---------------- | ---------- | ------------- |
| B | — | — | Never: it scores no higher than A on any criterion |
| C | Rules that must not be missed | 20 | About 56 |
| C | Evidence | 15 | About 53 |
| C | Works with every agent | 10 | About 50 |
| C | Maintenance | 10 | About 50 |
| D | Rules that must not be missed | 20 | About 56 |
| D | Works with every agent | 10 | About 50 |
| E | Context per turn | 20 | About 56 |
| E | Evidence | 15 | About 53 |
| E | Works with every agent | 10 | About 50 |
| E | Maintenance | 10 | About 50 |
| F | Works with every agent | 10 | About 56 |
| F | Maintenance | 10 | About 56 |
| G | — | — | Never: it scores no higher than A on any criterion |

No alternative is close: each needs one criterion weighed more than twice
what it is. The weakest score of A is its evidence, which a benchmark
round that measures it settles.
