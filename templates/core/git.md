# Base — Git Conventions

[ID: base-git]

How changes are committed, reviewed, verified and merged.

## Commits

- Commit under your full name and one consistent email; never change
  identity mid-project
- Use a work email in a work repository, never a personal one
- Work on a branch; never commit directly to `main`
- Never commit build output, dependency directories or secrets
- Commit a generated file only when the project tracks it on purpose, under
  the regeneration rules below
- Treat every repository as public: no secret, credential or sensitive
  value in source or history
- Keep a `.gitignore` (MUST) covering dependencies, build output, secrets,
  editor state, OS files and coverage output
- Track the shared editor settings that mirror the CI gates; ignore the
  rest of the editor's state
- Commit lockfiles (MUST)

## Pull requests

- Keep a pull request to one concern (SHOULD)
- Test locally before committing
- Review the diff against the base before merging, in the order security,
  correctness, clarity, conventions
- Merge only after the review passes and CI is green

## CI evidence

- Read the CI run for the push before describing a change as good; a local
  run is evidence about one platform
- Treat a pull request with no registered check as not passed: wait until
  one registers, then watch every check to completion

```bash
PR=<N>
count=0
for _ in $(seq 1 60); do
  count=$(gh pr checks "$PR" --json name --jq 'length' 2>/dev/null)
  [ "${count:-0}" -gt 0 ] && break
  sleep 5
done
echo "checks registered: ${count:-0}"
[ "${count:-0}" -gt 0 ] || exit 1
gh pr checks "$PR" --watch > /dev/null
watched=$?
failing=$(gh pr checks "$PR" --json bucket --jq '[.[] | select(.bucket != "pass" and .bucket != "skipping")] | length')
echo "checks not passing: $failing"
[ "$watched" -eq 0 ] && [ "$failing" -eq 0 ]
```

- Require `checks registered` above zero, `checks not passing` zero and a
  zero exit
- Never merge on a non-zero exit: no check registered within five minutes,
  or a failing or cancelled check
- Re-run a verification a pull request body claims once the base has moved
  since it was written; above all a proof of absence
- Read a new or changed workflow's first run in its real environment, and
  require a verdict from it before trusting the workflow

## Updating a branch

- Never force-push, including with `--force-with-lease` (MUST NOT)
- Bring a branch up to date by merging the base into it, or with
  `gh pr update-branch <N>`; never rebase and force-push
- Regenerate derived artifacts and re-run the staleness comparison after
  every such merge, and stage what they produce
- Run `git submodule update --init --recursive` after pulling a change that
  moves a submodule pointer; the checkout keeps the old revision otherwise

## Numbered documents

- Check an ordered document's numbering after merging the base in,
  whenever two open pull requests edit it
- Read an indexed table's rows yourself; the hook below checks numbered
  headings and ordered list items only

```bash
pre-commit run check-heading-numbers --all-files --verbose
```

- Require the documents-inspected and ordinals-inspected counts above zero
  and `numbering problems` zero
- Pass each numbered document as a `--path` argument

## Regenerated artifacts

- Apply these rules to a one-directional artifact, one never read back
  into its source; a bidirectional one follows its own two rules below
- Regenerate a derived artifact in the change that edits its source, and
  stage both together (MUST)
- Name the regeneration trigger beside the sources it derives from (MUST)
- Run the staleness comparison after the edit, and again after any merge
  that brings another branch's sources in (MUST)

```bash
<regenerate-command> || exit 1
git ls-files --error-unmatch -- <artifact-path> > /dev/null || exit 1
git diff --exit-code --stat -- <artifact-path>
```

- Require a zero status; a failed regenerator, an artifact that is not
  committed and any diff each fail it
- Treat any diff as a committed artifact that does not match its sources
- Treat a regenerator that fails this on a current artifact as defective:
  it is not idempotent
- Summarise the visible impact before and after in the pull request body:
  a verdict matrix, a delta table, a screenshot diff
- Open a tracked follow-up naming the stale files, by name or glob, where
  regeneration is too expensive to bundle (MUST)
- Never regenerate a bidirectional artifact, one an ingest or `--apply`
  step reads back into its source, from the pipeline it feeds
- Refresh such an artifact through the step a person owns, and flag it
  stale
- Drop a regenerated file whose diff is line endings only:

```bash
git diff --ignore-cr-at-eol <file>
```

- Read an empty diff as noise, and drop the file with
  `git checkout -- <file>`
- Never drop a file on `--ignore-all-space`; it hides `"a b"` becoming
  `"ab"`
- Read any other whitespace-only diff before dropping it
- Open every regenerated binary artifact in a viewer or an image-read tool,
  and confirm it tracks its source
- Regenerate a known-current control artifact first; a non-zero diff there
  means the environment disagrees with the committed files
- Reconcile a non-zero control diff before committing anything regenerated
- Pair a spot-check of three to five representative artifacts with one
  population metric when a change regenerates many

## Off-limits paths

- Declare an Off-limits section in the project's context file, listing the
  paths that MUST NOT change without explicit approval (MUST)
- Offer this default set for the project to cut down: auth and session
  code, payment code, migrations, `.env*` and secrets, CI/CD workflows,
  and a vendored rules submodule's pointer
- Propose a change inside an off-limits path before making it, with a
  rollback strategy and the tests that would catch a regression (MUST)
- Treat an approval as covering the proposed plan, never the whole path
- Apply the restriction to executable content: steps, commands, flags,
  permissions, triggers, pins, a vendored pointer's revision
- Treat a diff confined to prose as ordinary work
- Treat a comment a tool reads as executable: `# noqa`, `# nosec`, a
  linter disable, a coverage pragma
- Classify by the diff: it is prose only when removing every comment line
  leaves nothing
- Name an off-limits path at the top of the change's summary whenever the
  diff touches one, proposal or not (MUST)

```bash
pre-commit run report-off-limits-paths --hook-stage manual --all-files --verbose
```

- Require the paths-declared and files-changed counts above zero
- Pass each path as a `--path` argument, kept beside the declared list;
  `--base` defaults to `origin/main`
- State every off-limits line in the summary as an escalation; it is not
  a failure
- Run it after committing: on the base with a clean tree it prints
  `not applicable`, and a base that does not resolve fails it
