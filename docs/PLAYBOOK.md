# Playbook

Operational reference for common tasks. Each section is a self-contained
procedure. See `CLAUDE.md` for authoring rules and `SPEC.md` for the
composition model.

---

## Add a new base or layer template

Stacks, platforms, workflow and language templates live in forks
(ADR-049); a fork's own playbook covers adding one. Upstream takes base
and layer templates only.

1. Create the file in the correct layer directory:
   - `<concern>/<name>.md` — cross-cutting, applies to all projects; the
     concern is one of `core`, `security`, `infra`, `data`
   - `backend/<name>.md` — backend services only
   - `frontend/<name>.md` — frontend/UI projects only
2. Tag the file root with `[ID: <layer>-<name>]`
3. Tag every section with a unique `[ID: <layer>-<name>-<section>]`
4. Register in `manifest.yaml` under the correct layer key:
   ```yaml
   - id: <layer>-<name>
     file: <layer>/<name>.md
   ```
5. Update `docs/SPEC.md` — add to the directory listing for the relevant layer
6. Upstream carries no stack to reference the new file. A fork's stacks
   name it in their `[DEPENDS ON: ...]` headers once the fork merges it

---

## Drain a downstream lesson into a template

A lesson sourced from one downstream project (a bug write-up, a session
retro) carries that project's domain in its framing. Vet it for
genericity before it becomes template content:

1. Extract the generic kernel — the rule that holds regardless of stack
   or domain. Strip project-specific nouns (entity, tool, and metric
   names)
2. Pick the target by **measured chain reach**, not by the home the
   issue suggests — and know which kind of template you are measuring:

   ```bash
   # how many roots resolve a candidate file?
   for s in $(py tools/resolve.py --roots); do
     py tools/resolve.py "$s" | grep -q 'core/review.md' && echo "$s"
   done | wc -l
   ```

   `--roots` and not `--list`: a project resolves its stack, then its
   extras, then its platform, each as its own root, so the stacks are
   only part of what carries a file. Measuring over `--list` counts the
   stack chains and silently omits every opt-in root.

   A **chain template** carries rules the generated project follows.
   Reach is the criterion for it, and a rule in one that no root
   resolves reaches no generated context file.

   An **opt-in template** is a root of its own. Its reach is 1 — itself —
   and that is the point rather than a low score: what it may rely on is
   the core tier plus its own `depends_on` tree, because the stack it is
   paired with is unknown when it is authored. A fork's `platform/`
   templates are the clearest case, since a project picks one regardless
   of stack.

   A **pipeline template** carries rules about generating or consuming a
   context file, and a fork's interview reads it directly rather than any
   root resolving it into a project. Reach says nothing about whether the
   rule lands: `core/agents.md` is carried by a single root — its own —
   and shapes every file the pipeline generates. Recognise one by asking
   what reads it: a stack, an opt-in root, or the interview.

   A filed issue's suggested home is a hypothesis — it is usually
   written from the downstream project, without running this. Where a
   rule needs universal reach but applies only sometimes, put it in a
   high-reach template behind an `(if applicable)` heading rather than
   in a low-reach one. Where a rule is one case of a contrast whose
   other cases live in a low-reach file, it stays with them: a case that
   cannot be read without the ones it is defined against is not made
   more useful by moving it somewhere better resolved
3. If the kernel is genuinely cross-cutting, add it to the relevant
   concern or layer template per "Add a new base or layer template"
4. If a fragment only applies to one stack or domain, fold it as an
   *example* inside a generic rule — do not add it as standalone base
   content. Standalone one-stack content in a core-tier template loads
   into every chain and dilutes attention
5. Prefer extending an existing related rule over adding a parallel
   section — duplicate rules restated across templates are the same
   attention-dilution failure
6. Validate per "Validate a template change"

---

## Rename a template file

1. `git mv <old-path> <new-path>`
2. Update every `[DEPENDS ON: ...]` header that references the old path
3. Update `manifest.yaml` — change the `file:` field for the entry
4. Update `SPEC.md` and `README.md` — search for the old filename and
   replace
5. Verify with `git status` that no old references remain

---

## Rename a section ID

1. Change `[ID: <old>]` to `[ID: <new>]` in the source template
2. Search all template files for `[EXTEND: <old>]` and `[OVERRIDE: <old>]`
   — update every occurrence
3. Update `manifest.yaml` if the ID is referenced in `depends_on` lists
4. Update `manifest.yaml` if the concept maps to a template entry

---

## Author a new ADR

Use this workflow only after applying the decision threshold in
`CLAUDE.md` "Decision logs": a record is owed when the decision changes
what a consuming project observes without reading this repository — the
composition model. Prose style, tool choice, release procedure, naming and
file layout need no ADR, however consequential they are. One coherent
architectural decision may cover related work across several issues or PRs.
ADRs live in `docs/decisions/`; ADR-010 records the frontmatter schema.

1. Copy the template:
   ```bash
   NNN=$(printf "%03d" $(($(ls docs/decisions/[0-9]*.md | wc -l) + 1)))
   cp docs/decisions/TEMPLATE.md docs/decisions/${NNN}-<slug>.md
   ```
   Slug is kebab-case, sentence-meaningful (e.g. `011-provenance-principle`).
2. Fill in the frontmatter — `id` (quoted string matching `NNN`),
   `status: Proposed` (or `Accepted` if the decision is already
   ratified), `date` (today, `YYYY-MM-DD`), `category` from the
   closed set in ADR-010, and `supersedes` / `superseded_by` lists.
3. Replace `# ADR-NNN: Title in sentence case` with the real title
   (colon form, sentence case).
4. Write the sections in the template's order — **Context** (the
   forces), **Decision** (one sentence), **Rationale** (two to four
   bullets, each tied to a force), **Design** (optional: the
   numbered rules, with RFC 2119 keywords), **Alternatives
   considered**, **Consequences**, **Compatibility** and
   **Security** (each "None" when nothing applies). Non-trivial
   decisions SHOULD include a diagram in Design: a draw.io source in
   `docs/diagrams/` beside the PNG the record shows, styled like the
   existing files there and ending in a legend. Export it at twice the
   size with a 10 px border, and give the image alt text that states
   what it shows:
   ```bash
   draw.io -x -f png -s 2 -b 10 -o docs/diagrams/NAME.png \
     docs/diagrams/NAME.drawio
   ```
5. If this ADR supersedes an existing one: update the old ADR's
   frontmatter in the same PR — set its `status: Superseded`,
   refresh `date`, and add this ADR's id to its `superseded_by`
   list. Preserve historical claims; format-only changes are also allowed
   under the decision-log rules in `CLAUDE.md`.
6. Run `py tests/run_smoke.py ADR-01` to validate the frontmatter
   schema before opening the PR.
7. If the ADR **removes** a concept, sweep for prose that still
   assumes it — in `templates/` and in open issue bodies:
   ```bash
   grep -rn "<concept>" templates/ docs/
   gh issue list --state open --limit 100 --json number,title,body \
     --jq '.[] | select(.body | test("<concept>")) | "#\(.number) \(.title)"'
   ```
   A queued issue proposing template text that reintroduces the
   removed concept passes review on its own terms and undoes the
   ADR when implemented. Fix the issue body, do not rely on
   catching it at implementation time.
8. Open the PR. Preserve the merged decision as history. Routine later
   refinements update current docs and the PR; only a material architectural
   replacement needs a superseding ADR.

## Adopt a template policy update

A newer tag alone creates no work. Review a template update for a named project
need or material risk, applying "Adopting shared rules" in
`templates/core/docs.md`. Keep existing adopted conventions until the
project deliberately changes them; declining a candidate needs no ADR or ticket.

For consumers adopting the selective-adoption and ADR-threshold update:

- Inline the adoption boundary in the root context file before applying newly
  read template rules. Update copied inline rules as well as the submodule pin.
- Replace old directory-move, paragraph-length, and per-issue ADR triggers in
  the local context, wrap-up checklist, and authoring instructions, along with
  any threshold phrased as a judgement about how consequential a decision is.
  The test is what a user of the thing observes without reading the
  repository's internals.
- Keep existing ADRs as history. Put routine refinements in current docs and
  the PR; do not create a consolidation project or a decline register.
- Reconcile the reference list if a chosen update changes dependencies, and
  run the project's relevant existing checks. Select a released tag when the
  policy ships; until then the current pin remains usable.

---

## Generate a context file for a project

Upstream ships no stacks, no interview and no pre-resolved chains
(ADR-049). A project generates its context file from a fork: the Imbra
fork, [`Imbra-Ltd/imbra-ai-templates`](https://github.com/Imbra-Ltd/imbra-ai-templates),
for Imbra's stacks, or a fork of its own kept current per "Sync with
upstream as a fork".

1. Open your agent
2. Attach the fork's interview and the resolved chain for the stack
3. Answer the interview, review the file the agent proposes, and place it
   at the project root

The fork's own documents own the generation paths, its pre-resolved
chains and the model limits of its stacks.

---

## Validate a template change

1. **Smoke check**: run the automated structural checks — no agent required:
   ```bash
   py tests/run_smoke.py
   ```
   This verifies all `[DEPENDS ON: ...]` paths, unique IDs, `[EXTEND: ...]` /
   `[OVERRIDE: ...]` references, and `manifest.yaml` consistency in one pass.

   A rule added to a widely resolved file is read by every project on
   every chain carrying it, on every turn, and nothing refuses that
   size. Say in the pull request what the addition is worth. Upstream
   carries no stacks, so the size shows in the forks that resolve the
   file: a fork's `README.md` model-limits table reports it per stack
   category beside the smallest context window that still holds it, and
   `py tools/sync.py --check` fails there when the table drifts from the
   tree.

   In a fork, a category crossing to a larger window is a change to what
   a consumer needs to run the stack at all, and that is refused rather
   than reported: SYS-16 fails until the new tier is recorded in
   `tests/context-tiers.txt` in the same change.

   Before adding a paragraph, try stating the rule inside the one that
   already carries the narrow version of it. A widened rule folded in
   place is often shorter than the text it replaces: the
   release-proposal record went from +472 characters as its own
   paragraph to 98 characters shorter than the narrow rule it replaced.
   Measured 2026-09-03 on `core/git.md`.

2. **Agent check**: attach a fork's interview and a resolved chain
   carrying the changed template to an agent, and review the output for
   coherence. The e2e suite that automates this reading lives in the
   forks (ADR-049).

Reports are written to `tests/reports/` after every run, named for the
time and the tree — `<timestamp>-<runner>-<short-hash>.md`, with `-dirty`
where the working tree was not that commit, and no suffix where there is
no repository to read.

---

## Audit redundancy

A rule stated in two active sections of the same resolved chain dilutes
the agent's attention (see `docs/design/template-content-quality.md`). The
audit scans every root a project can pick -- in a fork, the stacks and the
orthogonal templates alike -- and reports duplicates, excluding those the
override model legitimately produces (one section `[OVERRIDE]`s the
other):

```bash
py tools/audit_redundancy.py           # exact in-chain duplicates
py tools/audit_redundancy.py --near    # also paraphrase near-duplicates
py tools/audit_redundancy.py --check   # exit 1 if any exact duplicate
py tools/audit_redundancy.py --self-test  # the planted cases only
```

Every run prints how many rules it read and refuses a chain it read none
from. `--check` first runs planted chains that owe a known number of
findings, so a detector that stops matching fails instead of reporting a
clean corpus.

`--check` gates the exact tier only and prints the near count beside
its verdict, so a passing run states what it did not gate (ADR-038).
A near pair cannot fail CI; the count is what makes it visible.

Run it before opening a template PR and when consolidating rules. A
finding is not automatically a defect — a duplicate may be intentional
(e.g. a rule a base template needs when used standalone). Judge each
against the single-source principle, then either trim the restatement
(prefer the parent/owner template) or accept it with a reason.

`--check` runs in CI as a ratchet: it fails on any exact duplicate not
in the tool's `BASELINE` allowlist, so new redundancy is blocked while
the known duplicates clear through their owning issues (currently the
frontend pair, #624). When you resolve a baselined duplicate, remove
its `BASELINE` entry in `tools/audit_redundancy.py` — `--check` reports
any entry that no longer applies.

---

## Run the test suite

```bash
py tests/run_smoke.py              # structural checks — seconds
py tests/run_conformance.py        # the templates' own checks, run here
py tests/run_conformance.py --list # dispositions only, run nothing
py tests/run_fork_sync.py         # a fork that only appends merges HEAD
py -m pyflakes tools tests        # the tooling's own lint
npx markdownlint-cli2              # Markdown, outside the recorded files
```

CI pins both linters' versions in `.github/workflows/smoke.yml`.
`.markdownlint-cli2.jsonc` lists the files that carried findings when the
Markdown lint first ran. Every other file is held to the rules in full; fix
a listed file and remove its line, never add one.

A change that removes what forks carry, such as the split, carries the
commit trailer `Fork-merge: ours`. Fork sync then merges it the way a fork
must, with `git merge -s ours`, moves the fork's templates out of
upstream's manifest keys into its own, and runs smoke on the result.

The e2e suite and the efficacy benchmark read what the templates generate,
so they live in the forks with the stacks and the interview (ADR-049).
Smoke and conformance read the templates themselves.

See `tests/CODIFICATION.md` for the ID scheme and `tests/INDEX.md` for the
full list of specs. Requires `py -m pip install pyyaml` for the manifest
check.

In a fork, set `SAIT_UPSTREAM_REF` before running smoke; "Sync with
upstream as a fork" gives the command.

In CI, a fork sets the repository variable `UPSTREAM_REPO` to its
upstream (`solid-ai-dev/solid-ai-templates`). Smoke and the release gates
then fetch upstream's `main` and export `SAIT_UPSTREAM_REF` and
`UPSTREAM_REF` as `upstream/main`; unset, they skip the fetch.

`run_smoke.py` prints what each check inspected under its verdict — the
files scanned, the chains resolved, the directives compared. Those lines are
not findings; read them when a count moves without the tree moving, which is
how a check that silently stopped reaching its corpus shows up. A count of
zero fails the check, and a check that passes while reporting nothing is
failed by the runner itself.

`run_smoke.py` checks that the templates COMPOSE. `run_conformance.py`
checks that this repository OBEYS them — it extracts every fenced check in
`templates/` and either runs it here or records why it does not apply.
Adding a fenced check to a template without a disposition in
`tests/conformance.py` fails the run, which is what stops a new check from
arriving unexamined. A block in fork-owned content (stacks, platforms,
workflow, the process sections) takes its entry in
`tests/fork_dispositions.py` instead, and a smoke check reading such
content goes in `tests/fork_checks.py`, so both runners stay the same file
upstream and in every fork. Checks reaching GitHub need `gh` authenticated.

A check whose verdict is a judgement reports `REVIEW` rather than `PASS`,
and the summary counts it as awaiting a reading. It does not fail the run
— the exit status answers whether a verdict was reached and was negative —
so a run ending `0 failed  2 not applicable  6 awaiting a reading` is not
a clean run until someone has read those six. The middle count is not
among them: a check whose moment is not in progress exits 3 and has
answered, which is why it is counted apart. That is different from a
`SKIP`, which a person decided in advance about this repository and which
runs nothing at all. Recording them as passes is what let four
over-long changelog entries sit inside a green report for two sessions.

A `SKIP` carries a `reason`, and the runner refuses one that does not —
the skips are the largest population in the registry, and each is a check
that does not run, justified by prose. Where the only obstacle is a
placeholder the template left for its consumer to fill in, the entry takes
a `substitute` map instead and the check runs. That distinction is not
cosmetic: the release-pipeline check was skipped for naming
`<release-workflow>.yml` while `.github/workflows/release-gates.yml` had
been shipping for weeks, and nothing re-read the reason.

A check only earns that status where nothing in its output can be decided.
The changelog bound declares a limit and counts against it, so it is a
scored verdict now, and each check that stays a judgement carries a
`reason` in `tests/conformance.py` naming what about it takes a person.
The runner refuses a judgement disposition that states none.

Which checks may reach that status is fixed in `tests/reading-budget.txt`,
one title per line above the reason it cannot reach a verdict. A reading
the file does not name fails the run, so the set grows only in a diff that
says why; a named check that reaches a verdict or reports it does not apply
passes freely, which is what keeps the release moment from failing the run
— the ordering check answers "does not apply" while HEAD is the tag. An
empty budget is refused rather than obeyed. On a hosted runner the summary
is written to the run summary as well as the log.

Adding a judgement disposition therefore means two edits in the same
change: the `reason` beside the disposition, and the title in the budget.
Renaming a check means moving its budget line too — the runner reports the
stale entry as an unbudgeted reading rather than ignoring it.

---

## Sync with upstream as a fork

A fork stays current by merging upstream, never by copying files
(ADR-049). It appends under `stacks:`, `platform:` and keys of its own,
adds to every chain's core tier under `fork_core:`, and never edits
`core:`, `base:`, `backend:` or `frontend:`.

1. Fetch upstream and list the commits carrying `Fork-merge: ours` that
   the fork has not merged yet:
   ```bash
   git fetch upstream
   git log --reverse --format='%h %s' --grep='^Fork-merge: ours' HEAD..upstream/main
   ```
2. For each such commit, oldest first: merge its parent normally, then
   the commit itself with `-s ours`, so the files upstream removed stay in
   the fork:
   ```bash
   git merge <commit>^
   git merge -s ours <commit>
   ```
   An ordinary merge of that commit deletes every file the fork left
   unchanged and upstream removed
3. Move the fork's templates out of `base:`, `backend:` and `frontend:`
   into a manifest key of its own, and the core IDs upstream dropped from
   `core:` into `fork_core:`. Commit the move
4. Restore each template the commit modified rather than deleted. `-s ours`
   kept the fork's version of every file the commit touched, so each still
   holds the text upstream replaced, and nothing reports it:
   ```bash
   git diff --name-only --diff-filter=M <commit>^ <commit> -- templates
   ```
   For each file other than the manifest, move the fork's own lines into a
   fork-owned file that reaches the same chains: under `fork_core:` for a
   core-tier file, otherwise depended on by the fork templates that depend
   on the upstream one. A line upstream rewrote takes upstream's text
   unless the fork's states a rule of its own. Then take upstream's text and
   commit:
   ```bash
   git checkout <commit> -- <path>
   ```
5. Merge the rest: `git merge upstream/main`. Resolve `README.md`,
   `CLAUDE.md` and `CHANGELOG.md` in the fork's favour; they are
   fork-owned files. Then confirm no upstream template differs from
   upstream's; the command lists `templates/manifest.yaml` alone:
   ```bash
   git diff --name-only upstream/main -- $(git ls-tree -r --name-only upstream/main -- templates)
   ```
6. Run smoke with `SAIT_UPSTREAM_REF` set to a ref holding upstream's
   history, so SYS-20 compares the manifest's upstream keys with the
   revision the fork last merged:
   ```bash
   SAIT_UPSTREAM_REF=upstream/main py tests/run_smoke.py
   ```
   Unset, SYS-20 treats the checkout as upstream and compares the manifest
   with itself

`py tests/run_fork_sync.py` simulates a fork merging upstream's `HEAD`
this way on every upstream pull request.

---

## Control-test a check you are changing

A check that stopped reporting a finding and a check that can no longer
report one produce the same clean result. Before believing a narrowed or
newly-forked check, drive it through a fixture that MUST be reported and
one that must not.

Where the fixture can live outside `templates/`, write it, run the single
check by a string from its body, and delete it:

```bash
py tests/run_conformance.py "<string from the check body>"
```

Where the fixture must live UNDER `templates/` — anything the check scans
by walking that tree — the runner refuses to execute: an unregistered
fenced block in the fixture is a missing disposition, which it reports
before running anything. Call its extraction directly instead, which skips
the registry reconciliation:

```bash
py - <<'EOF'
import sys, tempfile
sys.path.insert(0, "tests")
from run_conformance import iter_blocks, run_block

body = next(b[3] for b in iter_blocks()
            if b[0] == "core/docs.md" and any("<find>" in l for l in b[3]))
code, out = run_block(body, "bash", tempfile.mkdtemp())
print("exit %d" % code)
for line in out:
    print("  " + line)
EOF
```

Pass condition: the fixture that must be reported is reported, the one
that must not is not, and the check's own corpus counts move between the
two runs. `testing-control-corpus-moves` in
`templates/core/testing.md` is the rule, and says why the third is
what makes the first two readable.

For a check that takes an argument — a milestone, a module, a field —
replace the placeholder line in `body` before calling `run_block`. The
placeholder is not always what the issue or the prose calls it:
`MILESTONE = None` rather than an empty string cost a first attempt here.

Mutate the check's INPUT, never the string its disposition uses to find
it. The two are the same text more often than it looks: the CRLF check is
located by the extension list it filters on, so emptying its corpus by
editing that list stops the registry from finding the block at all. The
run then reports drift between the registry and the templates — a
different defect, in a different file, that says nothing about the check.
Empty the corpus from the other end instead, with a pathspec or a glob
the `find` string does not overlap.

Changing what a check **exempts** is a documentation edit as well as a
code edit. Sweep the documents for the check's name before merging and
re-read every hit against the new exemption set: the check's own tests
exercise the exemptions rather than the sentence describing them, so a
document's account of them decays with nothing reporting it.
`quality-exemption-doc-duty` in `templates/core/quality.md` is the
rule, and ships the sweep.

Adding a constraint owes a sweep of its own. Run the new rule or check
against the corpus that already exists before merging, and record in the
pull request where it looked, what it found and what it left out. Where the
corpus does not comply, say whether the instances were fixed or frozen, or,
for a corpus that cannot be edited, the boundary the rule binds forward
from. `quality-constraint-corpus-sweep` in `templates/core/quality.md`
is the rule.

---

## Run a 360-degree audit

The 360 procedure is process, so a fork carries it in
`templates/workflow/360.md` (ADR-049), the Imbra fork among them. A 360
assesses the whole project from independent
stakeholder perspectives as parallel, context-isolated subagents (the
headless adaptation re-projects Quality into engineering dimensions). Run
one on demand — before a launch, after a milestone or a major feature, or
when a stakeholder needs the whole picture.

- Store each audit as a dated report at `docs/audits/YYYY-MM-DD-360.md` —
  this is the only audit location; never use a single-file
  `docs/360-audit.md` history. All audit history lives in the folder.
- Each report carries a scores table, the issues created, the current
  bottleneck, and per-dimension findings tables with a grade rationale.
- File a labelled issue for every actionable finding (CLAUDE.md §2.2)
  and reference it from the report.

---

## Submit a pull request

1. Ensure you are on a feature branch — never commit to `main` directly
2. Run the validation steps above for every changed template
3. Update all affected documents (`SPEC.md`, `README.md`, `manifest.yaml`) before
   committing
4. Commit with a conventional message:
   ```
   feat(security): add supply-chain template
   docs(spec): update backend layer listing
   ```
5. Push and open a PR — one concern per PR
6. Merge with the default squash subject — `gh pr merge <number>
   --squash`, with no `--subject`. GitHub composes that subject from
   the title and appends the pull request number; supplying one
   replaces both. A release's milestone-coverage check, which a fork
   carries in a template of its own, reads those numbers back out of the log, so a
   hand-typed subject removes the reference it resolves
7. After merge: delete the branch and pull `main`

Where a cut carries more than one pull request, every branch after the
first goes `BEHIND`. A merge that changes the manifest changes what
`tools/sync.py` generates into `README.md` and `docs/SPEC.md`, so the
second branch carries generated sections built from a tree that lacks the
first one's change. Git reports the branch `MERGEABLE` — the edits fall
in different regions of the same files — so nothing warns that the
sections are stale. CI is the first signal.

Recover it with `gh pr update-branch`, never a rebase and force-push.
Then re-run the staleness gate on the updated branch, because
mergeable is not the same claim as current:

```bash
gh pr update-branch <number>
git pull
py tools/sync.py --check
```

Pass condition: the gate prints `All files in sync` **after** the
update, having listed every document it compared. Run it before the
update instead and it reports the previous state, which reads as a pass.

---

## Groom the backlog

Run this before scoping a cut. The procedure and the reasons behind its
order are process, so a fork carries them in `templates/workflow/issues.md`
(ADR-049); what follows is only what is particular here.

List the backlog — an unmilestoned issue is triaged, not untriaged, so no
view reports it:

```bash
gh issue list --state open --limit 200 --json number,title,milestone --jq '.[] | select(.milestone == null) | [.number, .title] | @tsv'
```

- Verify a claim with the tool the claim is about: `py tests/run_smoke.py`
  for a structural claim, `py tools/resolve.py` for a reach or chain claim,
  `py tools/audit_redundancy.py` for a duplication claim. Where the claim
  counts fenced blocks, use `tests/conformance.py`'s own extractor rather
  than a grep over `templates/` — a grep counts occurrences no runner reads
- Measure reach in roots, with `py tools/resolve.py --roots`, before siting
  a rule that could go in either of two templates
- Title the milestone `vA.B.C — <theme>`. The annotated tag message quotes
  the theme, so a bare version leaves the tag with nothing to quote
- The merged-work sweep belongs to the release sequence a fork carries
  in a template of its own, and upstream's conformance run no longer
  includes it. Where a fork's copy is at hand, run it at the groom, where
  a hit is cheapest to act on

Where a milestone already exists but its theme describes work that has not
happened, renumber it rather than dissolving it. A scoped milestone carries
an ordering and a rationale that took a groom to produce, and emptying it to
reuse the version number discards both. Move it to the next version, create
the version being cut under a theme matching what actually shipped, and
assign the closed issues to that. Met on 2026-09-03: `v2.73` was themed for
six unstarted issues while five unrelated ones had already merged, and one
issue had been put in it solely to satisfy the release gate.

---

## Survey the consuming repositories

Run this before proposing to rename or restructure a document other
repositories carry — the three `core/docs.md` requires (`README.md`,
`AGENTS.md`, `CLAUDE.md`) and any a fork's process prescribes, such as
`docs/PLAYBOOK.md` or `CHANGELOG.md`. `tools/sync.py` reaches this
repository and nothing else, so the cost sits downstream, in repositories
no gate here can see.

1. Enumerate every account that generates from these templates. Both are the
   same owner, so no third party is affected, but each repository still needs
   its own pull request under its own branch protection:
   ```bash
   { gh repo list braboj --limit 100 --json nameWithOwner --jq '.[].nameWithOwner'
     gh repo list Imbra-Ltd --limit 100 --json nameWithOwner --jq '.[].nameWithOwner'; } | sort
   ```
2. Fetch each default branch's tree once and test exact paths against it.
   Fetching the tree is one call per repository and answers every path
   question; probing paths one at a time is both slower and wrong, for the
   reason in step 3:
   ```bash
   br=$(gh api "repos/$full" --jq '.default_branch')
   gh api "repos/$full/git/trees/$br?recursive=1" --jq '.tree[].path' \
     | grep -c '^docs/PLAYBOOK\.md$'
   ```
3. Carry a control path through the same probe — one that MUST be absent
   everywhere, such as `docs/THIS-MUST-NOT-EXIST.md`. A probe reporting a hit
   for every repository has usually failed rather than succeeded. The earlier
   form of this survey did exactly that:

   ```bash
   gh api "repos/$full/contents/docs/PLAYBOOK.md" --jq '.name' 2>/dev/null
   ```

   It prints the 404 body to stdout, where the redirect cannot suppress it,
   and `--jq '.name'` reads that body as a non-empty string. Sixteen of
   sixteen repositories reported a hit, including ones with no `docs/`
   directory at all. Measured 2026-09-08 with the tree form: 31 repositories
   probed, 14 carry `docs/PLAYBOOK.md`, 13 carry `docs/ONBOARDING.md`, 0 were
   unreadable, and the control path is found in **0**
4. Count mentions over tracked files, and count occurrences rather than
   matching lines. Reconcile the per-area sum against the total, so an area
   the enumeration missed shows up as a gap rather than as a smaller number
   nobody questions:
   ```bash
   git ls-files -z | xargs -0 grep -io 'PLAYBOOK\.md' | wc -l
   ```
   Measured here on 2026-09-08, the four forms disagree: occurrences over
   tracked files **137**, matching lines over tracked files 133, occurrences
   over the working tree 491, matching lines over the working tree 215. The
   working-tree walk reads `.git/` and inflates by three and a half times;
   `grep -c` counts a line carrying two mentions once. Only the first figure
   is the number of places a rename has to edit
5. Record the result in the issue proposing the change, with the date it was
   taken, before the decision is made. A survey quoted later without its date
   asserts about today's tree what was true on the day it ran

---

## Release a new version

This repo has no version manifest (plain Markdown), so it follows the
no-build release variant from ADR-006. What that variant removes is the
version-bump commit and the `chore: release` branch carrying it — there is
no manifest to bump, so nothing needs one. It does not remove every pull
request: the changelog cut at step 2 is its own, and it is the release
commit the tag names.

The release sequence and its pre-release checks — milestone coverage,
release ordering, changelog completeness, the merged-work sweep — are
process, so a fork carries them in a template of its own (ADR-049; the
Imbra fork's is `templates/imbra/git.md`), and upstream's conformance run
includes none of them. The steps below are what this
repository still does. The `Release gates` workflow runs
`py tools/release_check.py` and `py tests/run_conformance.py` on every tag
push, and can be dispatched with the version as an input to run them at
the release commit. The first checks step 2's cut:
```bash
py tools/release_check.py vA.B.C
```
Pass condition: it names the release, the previous tag and the ref the
changelog was read from, prints `findings: 0`, and exits zero. A finding
is a section missing or undated, entries left under `Unreleased`, or a
version that is not the SemVer step its section owes. Exit 2 means no
release was named or no previous tag was found, so nothing was compared.

1. Confirm the milestone's issues are all closed and `main` is green
   (`py tests/run_smoke.py` passes) and up to date (`git pull`)
2. Cut `CHANGELOG.md` — reconcile the `Unreleased` section against the
   commits since the previous tag:
   ```bash
   git log --oneline "$(git describe --tags --abbrev=0)"..HEAD
   ```
   A commit touching no template carries no entry, so a journal or
   tooling change is expected in that list with nothing answering it.
   Choose the version from the section before naming it, per ADR-006's
   SemVer: a patch when every entry sits under `### Fixed` or
   `### Security`, a major when the section carries
   `### Breaking changes`, a minor otherwise. A patch's milestone is
   retitled `vA.B.C — <theme>`. Then rename that section to
   `## [A.B.C] - YYYY-MM-DD` and open an empty `Unreleased` above it.
   This repo has no version manifest to carry the cut, so it is its own
   pull request, and it MUST merge before the tag below — a tag placed
   first names a tree whose changelog does not mention the release. That
   pull request's body is this repository's release proposal: it names
   every step here and the result it produced
3. Tag and push. The tag is annotated and names a commit, and that commit
   is step 2's changelog cut, not `main`. The theme in the tag message is
   the milestone's, which is where this repository keeps it:
   ```bash
   git tag -a vA.B.C <cut-commit> -m "vA.B.C — <theme>"
   git push origin vA.B.C
   ```
4. Publish the release from that tag, titled with the bare version.
   `tag-guard.yml` fails a lightweight tag, so the annotated tag is
   enforced here rather than merely advised:
   ```bash
   gh release create vA.B.C --title vA.B.C --generate-notes
   ```
5. Close the release's milestone once the release is published — titled
   `vA.B — <theme>` for a minor and `vA.B.C — <theme>` for a patch
6. Record that the session owes a `docs/dev-journal.md` entry — do not
   write it here. The entry is written at the end-of-session audit item
   that owns it, which is the last item for a reason: it is the only one
   whose output is a record of the others, and items above it file
   issues and open pull requests. Written at this point instead, the
   entry names none of them, and its account is fixed once written, so
   the repair is a second entry for one session. When the entry is
   written it is still **separate** — its own `docs(journal): ...` PR
   with **no milestone**, not part of the release. A release cut without
   a wrap-up still owes the entry; publishing the release does not
   discharge it
7. Verify the release exists before closing the session. This is last
   rather than part of step 4 on purpose: a check inside a step is
   skipped whenever the step is:
   ```bash
   gh release view vA.B.C --json tagName,name,isDraft --jq '.tagName, .name, .isDraft'
   ```
   Pass condition: prints the tag, the bare-version title, and `false`.
   `release not found` means step 4 did not happen — and every other
   artifact of the release, the tag and the closed milestone and the
   journal entry, is present either way, so nothing else surfaces it

Which of those steps are actually enforced, audited per step as
`quality-gates-procedure-steps` requires:

| Step | Enforced by |
| --- | --- |
| 1 | `py tests/run_smoke.py`, plus the milestone's own issue list |
| 2 | `tools/release_check.py`, for the cut and the version; the reconciliation against the commits is read by hand |
| 3 | `tag-guard.yml`, which fails a pushed lightweight `v*` tag |
| 4 | step 7, and nothing before it |
| 5 | nothing — an open milestone after a published release is silent |
| 6 | nothing — a missing entry surfaces at the next wrap-up, or never. The entry itself is gated by the audit item that writes it |
| 7 | nothing; it is the closing check, so it is the one to run by hand |

Step 4 is the one to protect first, because its omission cannot be
repaired afterwards: publishing the release later dates it after the
release that followed it, and a mis-ordered release list is worse than a
visibly absent entry. `v2.57.0` is the instance — tagged, milestoned and
journalled, never published, and deliberately left absent for that
reason.

Projects with a version manifest (`package.json`, `pyproject.toml`,
etc.) instead follow the branch → bump → PR → merge → tag flow; see
ADR-006.
