# Rationale: agents

Why the rules in `templates/core/agents.md` say what they say. The template
states each rule as one instruction; the reasoning is here, one heading per
section, named by ID where the section has one.

## Output files

A project changes agents, and its contributors use different ones, so both
files are carried whichever agent the project starts with. Two files that
can disagree leave the agent no signal which one wins; an import keeps one
source.

## Choosing a model

Nothing loads a referenced template, so a file that delivers its rules by
reference alone depends on the agent deciding to open each one. Inline keeps
every rule in context; hybrid keeps the rules a missed read would break
silently, and references the rest.

## Placing a rule

A rule whose breaking shows an error, or that a tool enforces, is caught if
the agent never reads it. A rule that breaks silently with nothing to catch
it is not, so it has to be in context.

## Quality bar

Every line of a context file is read on every turn, so a line that is not a
rule the agent applies dilutes the ones that are. Compression has a floor:
a qualifier that scopes a rule is part of the rule, and the clarity it buys
is worth its bytes. A restated rule drifts from its source, and the agent
gets no signal which copy wins.

## agents-project-questions

The templates answer none of the three questions, because each answer is
one team's way of working. A part dropped silently reads as one the project
never needed; stated as not applicable, it reads as decided. A checklist
paraphrased into a shorter list silently drops steps, and with them the
order to execute each in sequence.

## Hybrid model

Git conventions, placement rules, language safety rules, content rules and
the session protocol are the rules most often broken with nothing to catch
them: a wrong branch name pollutes history, a misplaced file breaks a build
quietly, and a condensed checklist is skipped. The adoption boundary is
inlined because a hybrid file reads upstream live, so without it a new
upstream MUST would widen what the project follows. A vendored submodule
puts untracked files on disk, and every tool that walks the tree rather than
the index scans them.

The procedures for reading and bumping a vendored pin, and the gate for a
chain list written into a context file, are in `docs/playbook.md`, "Vendor
the templates in a project".
