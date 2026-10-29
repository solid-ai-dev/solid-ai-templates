# Project goal and use cases

Status: proposal for discussion.

A dependable quality floor across agents, projects and teams is a worthwhile
goal. Individually plausible solutions can vary substantially in correctness,
maintainability, verification and operational readiness. Shared guidance can help
teams make these expectations explicit and evaluate whether agent work meets them.

The authoritative business goal and prioritized goals are in
[Introduction and goals](../architecture/01-introduction-and-goals.md).
[Quality requirements](../architecture/10-quality-requirements.md) defines the
instruments, baselines and evaluation scenarios. This proposal explores their
implications and possible applications without changing adopted policy.

## A dependable quality floor

One useful expression of the intended quality floor is:

> Help teams consistently deliver solutions that satisfy their requirements,
> preserve essential guarantees, and remain understandable and economical to
> change.

B+ is a useful shorthand, provided its meaning reflects the consequence of
failure. An internal dashboard and a payment system need different evidence even
when both meet the same organizational quality standard.

Acceptance remains the team's responsibility. The specification, architecture
and test expectations establish the intended behavior; generated code and tests
provide evidence against those expectations.

## Responsibility model

The proposed model places solid-ai-templates at the shared engineering policy
level. Upstream supplies reusable quality expectations and architectural defaults;
forks and projects specialize them, and agents apply the adopted rules to tasks.

```text
+-------------------------------------------------------------+
| 1. PURPOSE AND OUTCOMES                                     |
|    Why does the product exist? What does success mean?      |
|    Owner: business and product leadership                   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 2. REQUIREMENTS AND ACCEPTANCE                              |
|    What must work? Which constraints and tradeoffs apply?   |
|    Owner: product owner and engineering team                |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 3. ARCHITECTURE                                             |
|    What are the system boundaries and major design choices? |
|    Owner: technical leadership                              |
+-------------------------------------------------------------+
                              |
                              v
+=============================================================+
| 4. SHARED ENGINEERING POLICY                                |
|    What standards, safeguards and evidence are required?    |
|                                                             |
|    >>> SOLID-AI-TEMPLATES UPSTREAM <<<                      |
+=============================================================+
                              |
                              v
+-------------------------------------------------------------+
| 5. PROJECT-SPECIFIC CONVENTIONS                             |
|    Which stack, tools, commands and local policies apply?   |
|    Owner: fork and project maintainers                      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 6. TASK EXECUTION                                           |
|    Implement, test, review and explain the change.          |
|    Owner: agents and developers                             |
+-------------------------------------------------------------+
                              |
                              v
                  Evidence and observed outcomes
                              |
                              +----> Feedback to levels 1-5
```

Arrows show intent becoming concrete, not a mandatory sequential process or a
replacement for template precedence. Responsibilities interact. The team at
level 2 retains acceptance authority and uses evidence from execution to decide
whether the result meets its requirements.

Use the model to check where a proposed rule belongs:

- Preserve data during migration: shared engineering policy.
- Use a particular migration tool: project-specific conventions.
- Accept ten minutes of downtime: requirements and acceptance.

This proposal explores level 1 for the template system itself: its purpose,
applications and success measures. Its consumer-facing guidance primarily serves
level 4, with defaults that inform architecture at level 3.

## Broader implications

### Reduce the worst outcomes

Raising average quality helps, but preventing occasional serious failures may
matter more. Missing authorization, destructive cleanup, fabricated evidence and
ineffective tests deserve disproportionate attention. Measure how often outcomes
fall below the acceptable floor, and report severe failures separately.

### Make engineering judgment transferable

A useful template preserves the decision boundary: when to introduce a queue,
when an abstraction earns its cost, or when a migration needs staged deployment.
This can make experienced engineers' judgment available beyond their immediate
team. Concrete conditions and examples are essential to that transfer.

### Create a shared acceptance language

Developers, agents and reviewers can agree on what done, verified, compatible and
safe to retry mean. Common definitions could reduce review disagreement and make
handoffs more reliable. They should describe observable behavior and the evidence
needed to accept it.

### Make organizational policy portable

A team can retain essential expectations while changing languages, frameworks or
agent tools. The existing separation between shared policy and fork-owned stack
choices supports this application. Consistency includes how teams select and
justify exceptions for their projects.

### Treat policy changes as product changes

Every new rule imposes a cost on future work. Rules need evidence, compatibility
decisions, adoption boundaries and, occasionally, retirement. Maintaining those
boundaries can become a defining strength of the project.

## Potential applications

| Use case | Practical application |
|---|---|
| New-project setup | Establish relevant conventions, checks and acceptance criteria before inconsistent patterns accumulate |
| Existing-project onboarding | Help an unfamiliar agent understand established decisions and make a bounded first change |
| Code review | Give reviewers a common priority order and evidence standard |
| Modernization and migration | Preserve contracts while changing frameworks, storage or deployment |
| Incident learning | Convert a demonstrated failure into a reusable prevention rule with clear applicability |
| Agent evaluation | Compare models and configurations on whether they meet the organization's quality floor |
| Human onboarding | Teach new engineers the team's decision rules through concrete examples |
| Cross-team handoffs | Make assumptions, ownership, verification and unresolved risks explicit |

These applications are candidates for evaluation. A plausible benefit is not
evidence that every project should adopt an additional rule or workflow.

## Learning from outcomes

Feedback carries evidence to the owner of the decision that needs correction.
It can change requirements, architecture, shared policy, project conventions or
implementation. The following operating model is proposed for discussion.

```text
Observed result
      |
      v
Compare with acceptance criteria
      |
      v
Diagnose the cause using evidence
      |
      v
Route to the responsible level and owner
      |
      v
Correct the relevant artifact
      |
      v
Verify the correction and observe subsequent outcomes
      |
      +----> Reopen if the expected improvement does not hold
```

### Routing and ownership

| Finding | Destination | Decision owner | Artifact to correct |
|---|---|---|---|
| The product works but does not solve the user's problem | 1. Purpose and outcomes | Business and product leadership | Product goals and success measures |
| Expected behavior is missing or ambiguous | 2. Requirements and acceptance | Product owner and engineering team | Specification and acceptance criteria |
| System boundaries cause recurring failures | 3. Architecture | Technical leadership | Architecture and relevant decision records |
| Shared guidance is misleading or omits a demonstrated reusable safeguard | 4. Shared engineering policy | Upstream maintainer | Template and its verification cases |
| A tool, command or stack convention is unsuitable | 5. Project-specific conventions | Fork or project maintainer | Fork template, configuration or project context |
| Implementation violates an adequate requirement | 6. Task execution | Implementer and designated reviewer | Code and regression tests |

A finding may affect several levels. The project maintainer coordinates routing
and identifies one owner for the feedback record; each affected decision retains
its own approver. An agent can collect evidence, suggest a cause and prepare a
correction within its authorization. The designated owner approves changes to
requirements, architecture or policy.

### Capture and triage

The person or agent observing the result records it in the existing issue,
incident record or review. Reuse a canonical record when one already exists.
Include enough evidence to assess the finding:

- Expected and observed behavior, with the acceptance criterion involved.
- A reproduction or supporting artifact, its revision and relevant environment.
- The adopted rule and template version when guidance may contribute.
- Impact, recurrence and any human repair effort actually measured.
- The suspected cause, uncertainty and proposed decision owner.

Keep sensitive values out of the record. Treat a proposed cause as a hypothesis
until the evidence supports it. The owner decides whether to correct the issue,
request evidence, link it to existing work or decline it with a reason.

Reports about upstream templates use the existing
[triage procedure](../playbook.md#triage-a-report). A reusable downstream lesson
uses the
[downstream-lesson procedure](../playbook.md#drain-a-downstream-lesson-into-a-template)
to assess genericity and placement. A local preference alone creates no shared
obligation.

### Correction and verification

The responsible owner identifies the expected improvement and its acceptance
evidence before the correction. The implementer changes the relevant artifact
and verifies the reported case without weakening the accepted requirement to
obtain a pass.

For a proposed shared rule, add an applicability boundary and an acceptance case.
Use repeated representative tasks to assess benefit and cost before claiming
general effectiveness. Evidence can support keeping, narrowing or retiring a
rule as well as adding one.

Consumer adoption follows the existing
[policy-update procedure](../playbook.md#adopt-a-template-policy-update).
Publishing an upstream correction does not automatically change the rules a
project adopts.

### Closing the loop

The record owner links the correction, verification evidence, reviewer decision
and any remaining limitation. A code fix closes when it meets its declared
acceptance criteria and receives the project's required review.

Where the claimed benefit requires downstream observation, the owner records the
observation window or next representative task, who evaluates it and what reopens
the finding. Publishing a rule establishes delivery; improved consumer outcomes
require their own evidence. Track that evaluation explicitly if implementation
closes before the outcome can be observed.

### Example

A migration loses records. The project first establishes the expected retained
population and reproduces the loss. An implementation error routes to level 6
for a code fix and regression test. Ambiguous retention requirements route to
level 2 for a product decision. A demonstrated omission affecting other projects
may also route to level 4 for a shared template correction and broader evaluation.

The same incident can therefore produce a local repair and a reusable lesson,
each with its own owner and evidence of completion.

## Tensions to manage

- Uniform instructions can produce uniform mistakes. Shared rules need challenge
  and correction.
- A growing rulebook can make straightforward work expensive. Evaluate its cost
  against accepted outcomes.
- Agents may optimize visible compliance while missing the user need. Independent
  acceptance criteria must remain authoritative.
- Different projects need different solutions. Make the process for deciding
  exceptions predictable.
- Good engineering cannot compensate for unclear product requirements. Help the
  team expose consequential uncertainty before implementation.

## Preferred pilot

Start with bounded maintenance work in existing projects: bug fixes, small
features and migrations across a few existing downstream stacks.

These tasks expose whether the templates preserve local conventions, prevent
regressions and avoid unnecessary work. They also represent everyday situations
where dependable B+ output is valuable.

Compare the same tasks under the same model, tools and permissions with and
without the candidate guidance. Repeat trials and report unsuccessful tasks.
Use the existing [efficacy benchmark](efficacy-benchmark.md) as the evaluation
foundation rather than introduce a competing score.

## Success measures

The architecture already identifies human effort per accepted change as the
primary measure of the business goal. Evaluate the proposed applications against it,
including specification, supervision, review, repair and ongoing policy cost.

For the maintenance pilot, examine:

- The proportion of tasks that meet independently defined acceptance criteria.
- Human corrective effort and interruptions needed to obtain an accepted change.
- Severe failures and regressions in the declared follow-up window.
- Unnecessary changes and expansion beyond the requested scope.
- Total delivery cost and variation between runs, projects and teams.

The practical question is whether a team needs less corrective effort to turn an
agent's result into an acceptable change without increasing serious failures or
unnecessary work.

The [agent-perspective audit](../audits/2026-10-24-agent-perspective-review.md)
contains the separate template findings and implementation recommendations.
