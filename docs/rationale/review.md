# Rationale: review

Why the rules in `templates/core/review.md` say what they say. The template
states each rule as one instruction; the reasoning is here, one heading per
section.

## Priority order

A security exposure costs more than a wrong result, and a wrong result more
than an unclear name, so a review that runs out of time should have spent it
in that order.

Area and weight are separate. A clarity finding can be a demonstrated
defect, and a security note can be a suggestion. A review that blocks on
every suggestion makes the author redo work the task never needed, which
is the calibration gap the 2026-10-24 agent-perspective review named.

## MUST checklist

A sentence is correct only in relation to its neighbours, and each one reads
fine alone, so a review of the changed line cannot catch a contradiction the
change created. A refactor that extracts a helper can silently change an
edge case (null handling, sort direction, a boundary) on one of the paths it
serves, which is why every path is checked, not the one that motivated it.

Every project takes input from outside its process: a URL parameter, a
command-line argument, a file, a message. Destructuring or indexing it
before validation turns a malformed value into a crash or an injection.

## CI signals

An infrastructure failure (a network error, a missing release, broken
pinning, a runner out of memory) is a signal about the workflow, not the
pull request. Retrying until green masks it, and bypassing it hides it from
the next person who meets it.

## Structure audit

A code review checks the files that changed; nothing checks the files that
were never created. A rule with two MUST clauses passed as a whole lets one
clause go unchecked.

## Picking up an issue

An issue is evidence that a gap existed on its filing date, not that it
exists now. The tree moves, decisions relocate rules, and another session
may already be implementing it; work done from the text alone is coherent,
tested, and aimed at something that is no longer the problem. A closed
classification in acceptance criteria reads as a checklist, and a checklist
invites completion, so a member outside every branch is forced into the
nearest one. The full procedure, the shapes and their checks are this
repository's practice and live in `docs/playbook.md`, "Pick up an issue".

## Planning

A plan is the cheapest artifact to review: reading one costs minutes and can
still change the design, while reading the implementation costs hours and
mostly changes details. An agent makes code cheap to produce, which by
default moves the expensive review later. The assumptions are the part
worth reading; a plan stating none is the request restated. Re-planning
silently mid-implementation spends an approval that covered a different
plan.

## Verifying a finding

A finding is a hypothesis until demonstrated, and reporting one as a defect
costs the author more than missing it, because each has to be disproved by
hand.

A tool that runs cleanly and returns a plausible number is the most
convincing way to be wrong, and zero is the most convincing number: a silent
failure and a real absence print the same thing. Many tools narrow silently
to a diff, a sample or a partition in a pull-request context, and an
incremental run reporting zero on a tree nobody has scanned is evidence that
no baseline exists.

Extraction tools are silently partial: a parser walks the node types it
knows, so "X is missing" often means the extractor does not reach where X
lives.

A probe's result depends on the conditions it ran under: who ran it, with
what credential, in which environment. An endpoint honouring cookie
sessions commonly ignores a bearer token, so adding a token reproduces the
anonymous result and reads like confirmation.

Agents share blind spots and can agree on the same wrong answer. An agent
told only to verify a claim surfaces a different source; one told what was
found before, and where, surfaces a genuine change.

## Deviations

A SHOULD admits a justified exception, and the pull request is where the
justification is read. A MUST or MUST NOT does not, so lifting one is a
decision for an approver, not the author, and an agent meeting one it
cannot satisfy stops and asks rather than writing its own rationale. The
recorded reason lets the next reader see why the rule did not hold.
