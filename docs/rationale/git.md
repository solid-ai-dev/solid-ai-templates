# Rationale: git

Why the rules in `templates/core/git.md` say what they say. The template
states each rule as one instruction; the reasoning is here, one heading per
section.

## Commits

Git history and tooling depend on consistent authorship. An editor
allowlist versions the shared project setup that mirrors the gates, while
per-user editor state stays ignored.

## CI evidence

Where development and CI differ in operating system, interpreter or locale,
a green local suite and a green pipeline are different claims, and only the
second covers what the project ships on. A pipeline check at session start
is a different moment: it catches a break that predates the work, not one
the work introduced.

The host builds the subject of a check that reads the change under review:
a pull-request event checks out a merge commit, HEAD is detached, the clone
may be shallow, and the branch name survives only in an environment
variable. A check that counts commits or diffs against the base reads a
different tree there, and every control on the author's machine still
passes. A decline hides in a green pipeline because it summons no reader.

Run straight after a push, before the host registers the workflow,
`gh pr checks <N> --watch` prints `no checks reported` and exits at once, so
a merge chained after it goes through with no check run.

Evidence in a pull request body is scoped to the base it was produced
against. A later commit can falsify it with a clean merge and passing
checks, and the body still reads as verified. A proof of absence (a deleted
file, a removed reference) is the most exposed: the later commit
reintroduces what the body proved gone.

## Updating a branch

Force-pushing rewrites shared history and can clobber commits collaborators,
agents or bots have not fetched. Merging the base in brings the other
branch's sources and re-derives nothing, so a branch holding regenerated
artifacts now carries one built from a tree that lacked them. Git reports it
mergeable throughout, because the two changes touch different regions. This
happens on every release carrying more than one pull request.

## Regenerated artifacts

A test suite that does not read an artifact passes on a stale one, so local
green is not evidence it is current; the first signal is the CI comparison,
after the author has moved on. Naming the trigger beside the sources lets an
author meet the obligation without knowing the build graph. Run before the
edit or the merge, the comparison reports the previous state and reads as a
pass. `--exit-code` is what makes the absence of output a verdict.

A stale artifact is indistinguishable from a regression to the next
reviewer, which is why regeneration belongs in the fixing change. Silent
staleness is the failure mode when it is deferred. Regenerating a
bidirectional artifact from the pipeline it feeds overwrites values a person
verified.

Whitespace-only diffs reappear as fake regressions on another OS. A binary
artifact diffs as "Binary files differ", opaque to git and often to the
tests. A zero diff on a known-current control proves the generator is
deterministic here; a non-zero one means a mass rewrite would ship disguised
as the intended change. A clean masked remainder proves the data and prose
are untouched. A spot-check catches broken regeneration; a population
metric catches drift.

## Ordered documents

A clean merge proves the edits did not overlap, nothing about whether the
result is coherent. One branch appends 3.9; another inserts 3.5 and
renumbers, so its last section also becomes 3.9. Git merges both without a
conflict and the document carries two sections 3.9. Each diff is correct;
the defect exists only in the combination, and a conflict would have been
the better outcome. Merging the base in and re-running the checks produces
exactly this clean, wrong merge, which is why the check runs after the
merge. A document with no ordinal is a finding because a pattern calibrated
against the wrong convention reports zero either way.

## Submodules

A merged pin bump moves the recorded pointer and nothing else. `git pull`
fast-forwards the superproject and leaves the submodule at the revision the
bump replaced, so the clone reads old content while the pin names new. It
fails silently at the worst moment: reconciling against the vendored
content is the step after a bump. A clean status is evidence the tree was
moved, not that the pull moved it.

## Off-limits paths

Some paths carry consequences a diff does not show; a small diff and a
green suite say nothing about them. A restriction that lives only in a
reviewer's head is not one.

The vendored pointer earns its place differently from the rest. The others
are dangerous for what they execute or hold; a pointer executes nothing, so
no linter, suite or gate reads it, and the diff is a pair of hashes. One
line replaces every rule the project binds, a wider blast radius than a
workflow file, and a malformed workflow at least fails loudly.

The approval is for the plan, not the area. A prose-only diff's rollback is
`git revert` and its regression coverage is that nothing executes, so a
proposal for it is a form, and a form teaches the next author the proposal
step is one. The reviewer's attention is the control, allocated only if the
summary spends it.

The hook reads path names, so it cannot see whether a change is executable
or prose; an executable hit is discharged by the proposal, a prose-only one
by the summary naming the path. Its subject is committed history: a run
against uncommitted work reports what a compliant branch reports, and
`git rev-parse` echoes a base it cannot resolve, so a mistyped base would
look resolved if the hook did not check the exit status.
