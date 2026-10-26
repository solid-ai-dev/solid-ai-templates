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

A generated context file copies most of its template chain, so the file an
agent reads on every turn is long under either delivery model. The rubric
that places each rule inlines every rule whose breaking is silent and that
no tool enforces, and almost every template rule is both.

| Force | What it shows |
| ----- | ------------- |
| Size | Measured on 2026-10-26 from `main` at `ec00c4f3` (#2376): four files generated from the current templates ran to 70–90% of their chain's words, 681 to 980 lines. A hybrid file was 76% of its chain for a library and 70% for an API |
| Why hybrid saves little | The generators referenced only the sections a tool enforces; two of the four said the rubric forced the rest inline |
| What fills a file | Each rule of the two inline files was classed (#2376). Procedures that matter in one kind of task, such as verifying a finding, a release or regenerating artifacts, are 27% of the library file's words and 34% of the API's. Practice a capable agent follows unprompted is 13% and 11% |
| A cost of length | In the 2026-10-17 benchmark round, every context file made the app 40–160% bigger, and with a weaker model every generated file lowered the share of hidden tests passed. The one generated file that raised it was cut to 39 lines |
| A hand-written shape | A private project in daily use keeps a 563-word root file and nine skills of about 7,650 words, each loaded only when its task starts: about 8% of its material is in context per turn |
| No loading mechanism | A referenced file is read only when the agent decides to open it. Under a reference-only file a consumer's agent never opened its deferred templates in a whole session, and a gate that lived only there was missed (#712) |
| A loading mechanism | A skill is loaded from its description when a task matches it. That is the mechanism a plain reference lacks; no benchmark round has tested it |
| Several agents | The skill format was published as an open standard in December 2025, and several coding agents report reading it, most from `.agents/skills/`. That folder is a convention, not part of the standard |
| Adherence and security | Hybrid adhered to project conventions best of every arm in round 3, and scored highest on the judge's security rows in round 4. Rules that apply on every task are what carry that, and they stay in context |

## Decision

A generated context file keeps in context every project fact and every
silent, unenforced rule that applies on every task; it delivers each
procedure that applies to one kind of task as a skill the agent loads when
that task starts, and leaves out practice a capable agent follows unprompted.

## Rationale

- The procedures are the largest class in the measured files, and a skill
  takes them out of every turn without leaving them to a reference nothing
  loads.
- Rules that apply on every task, the habit counters and conventions, stay
  in context, which keeps what the adherence and security results rest on.
- Leaving out unprompted practice spends no context on a rule that changes
  nothing; the templates still hold it as the standard a review applies.
- The floor stays: no rule an agent must not miss is left to a file it may
  never open.

## Design

![Where a generated file puts a rule: a project fact or a guard on data, credentials or auth goes in the root file; a rule a test, linter or CI step enforces is referenced; a rule followed unprompted and never seen broken is left out; a rule for every task goes in the root file, and one for one kind of task goes in that task's skill, listed in the trigger table. The root file is in context every turn, a skill loads when a task matches its description, and an agent without skills gets the procedures inlined](../diagrams/task-skills.png)

1. **The floor** — Generation MUST NOT produce a file that delivers its
   rules by reference alone.
2. **Always in context** — The root file MUST hold the project's facts and
   every rule that is silent, unenforced and applies on every task.
3. **Task procedures as skills** — A rule that applies only during one kind
   of task, such as a release, a migration or verifying a finding, SHOULD be
   delivered in a skill for that kind of task. Its description MUST name the
   task that triggers it.
4. **The trigger table** — The root file MUST list each skill with the task
   that triggers it.
5. **No skill support** — Where the project's agent cannot load skills on
   demand, the procedures MUST be inlined in the root file.
6. **Security stays** — A rule whose breaking exposes data, credentials or
   an unauthenticated path MUST stay in the root file, even when it applies
   to one kind of task.
7. **Unprompted practice** — A rule a capable agent follows unprompted
   SHOULD NOT be inlined. A rule the project has seen broken MUST be.
8. **Enforced rules** — A rule a test, linter or CI step enforces SHOULD be
   referenced rather than inlined.
9. **Length** — The generator MUST report the root file's line and word
   count. This record sets no size limit.
10. **Every task or one kind** — An obligation that holds for every change,
    such as testing what changed, goes in the root file. The technique for
    meeting it, such as how to isolate a test, goes in the skill for the
    task that uses it.
11. **One home** — A rule MUST sit in one place: the root file or one skill.
    A skill MAY point to a root-file rule, never restate it.
12. **Group procedures** — A skill MUST cover one kind of task, never a
    single rule; a one-line procedure joins the skill for its task.
13. **Left out means left out** — A rule rule 7 leaves out goes in no skill
    either.
14. **Checks by command** — The root file and every skill MUST state a
    check by its command and pass condition, never by copying a script
    body.
15. **No templates in the tree** — Where the project does not vendor the
    templates, a referenced rule points to the tool and the configuration
    that enforce it.
16. **The model's name** — The overview states `Model: root and skills`.
17. **One skill format** — A skill MUST follow the open Agent Skills format:
    a folder holding `SKILL.md`, whose frontmatter carries `name` and a
    `description` naming the task that triggers it. Its body MUST name no
    agent-specific mechanism.
18. **One source, mirrored** — Each skill MUST be generated once, under
    `.agents/skills/<name>/`. Where an agent reads only a folder of its
    own, such as `.claude/skills/`, the skill is copied there unchanged;
    a copy MUST NOT be edited by hand, and a change to one is a change to
    both.

| A rule that... | Goes |
| -------------- | ---- |
| is a project fact | in the root file |
| applies on every task, breaks silently, no tool enforces it | in the root file |
| applies to one kind of task | in that task's skill, named in the trigger table |
| guards data, credentials or authentication | in the root file |
| a capable agent follows unprompted, never seen broken here | out; the templates keep it |
| a tool enforces | referenced |

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Keep the current rubric | Measured at 70–90% of the chain, with length a cost in the benchmark |
| A hard size budget, such as 40 lines | The rules that apply on every task alone exceed it in both measured files, so a budget drops habit counters rather than procedures |
| Plain references with a trigger table | A plain reference has no loading mechanism, and the consumer failure shows what that costs |
| Rules scoped by file path | Loads on the files touched, not the task started; a release or a review touches no single path. A fork may add it as a delivery mechanism |
| Move task procedures out of the core templates | Changes what every chain carries, not what the generated file loads; the templates stay whole as the standard |

## Consequences

| Consequence | Where |
| ----------- | ----- |
| `agents.md` states the placement table, the trigger table and the skill rules, and its model table shows skills | #2376 |
| `agents.md` closes the gaps the 2026-10-26 generators filled by invention: a checkable rule with no tool, a missing end-of-session checklist, and an override order for a single rule source | #2376 |
| The four 2026-10-26 files are regenerated under this record and their counts recorded beside the baseline | #2376 |
| The interview in the forks applies the placement table | fork |
| A benchmark round compares root file plus skills with hybrid and with no file. If it is worse than hybrid on adherence or on the judge's security and data-protection rows, this record is reopened | fork |
| Which rules count as unprompted practice is a generator's judgement until a round measures it. Two generators given the same rules on 2026-10-26 put 2,437 and 2,198 words in their root files, the larger for the smaller project | #2376 |

## Compatibility

A project's existing file keeps working: nothing it names is removed. Its
next regeneration produces a root file and skills where its agent loads
skills, and a hybrid file otherwise. Skills are additive files the project
may decline, which yields today's hybrid file.

## Security

Protects: a security rule stays in the root file even when it applies to one
kind of task, so no data, credential or authentication rule depends on a
skill loading. Exposes: a procedure in a skill whose trigger is missed is
not read for that task; the trigger table and the description are what
guard it.
