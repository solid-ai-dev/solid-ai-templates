#!/usr/bin/env python3
"""
Smoke and integration test runner for solid-ai-templates structural checks.

The checks live in tests/smoke/, one module per family (SYS, TPL, MNF,
ADR), and tests/smoke/registry.py lists them in run order. This file runs
them and writes the report.

Implements:
  SAIT-SMK-SYS-01-001A  — all DEPENDS ON paths resolve to existing files
  SAIT-SMK-SYS-02-001A  — all section IDs are unique across all templates
  SAIT-SMK-SYS-03-001A  — every template file has a manifest entry
  SAIT-SMK-SYS-04-001A  — DEPENDS ON headers match manifest depends_on
  SAIT-SMK-TPL-04-001A  — all EXTEND/OVERRIDE directives reference existing IDs
  SAIT-SMK-TPL-08-001A  — every base template has at least one [ID:] tag
  SAIT-SMK-TPL-09-001A  — no empty [ID:] sections
  SAIT-SMK-TPL-10-001A  — at most one OVERRIDE of an ID per chain
  SAIT-SMK-ADR-01-001A  — ADR frontmatter matches the ADR-010 schema
  SAIT-INT-TPL-06-001A  — EXTEND/OVERRIDE targets reachable in resolved chain
  SAIT-INT-MNF-01-001A  — all manifest entries reference valid paths and IDs

Usage:
  py tests/run_smoke.py              # run all checks
  py tests/run_smoke.py SYS-01       # run one check by short ID
  py tests/run_smoke.py SYS-01 MNF-01
"""

import datetime
import sys

from lib import PASS, FAIL, ERR, write_report, print_verdict
from smoke import adr, common, manifest, system, templates
from smoke.common import HAS_YAML, MISSING_YAML, TEMPLATE_DIRS
from smoke.registry import CHECKS
from smoke.system import QUALITY_GATES_EXEMPT_LAYERS
from smoke.templates import CORE_DIRS

# Set the output encoding and the line ending at the boundary rather
# than inheriting the console defaults. The encoding mangles any
# non-ASCII this program prints; the line ending is what another
# program reads, and on Windows a bare `print` emits CRLF, so every
# line reaches a consumer with a trailing carriage return.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass


def _helpers():
    """Every name this runner held before its checks moved to smoke/."""
    names = {}
    for module in (common, system, templates, manifest, adr):
        names.update(vars(module))
    names.update(globals())
    return names


# A fork's own checks read what only a fork carries: stacks, examples, the
# interview and the e2e cases. They live in fork_checks.py, which extends
# the registry and the lists imported above when the file exists, so this runner is
# the same file in every tree and a fork's merge of it is clean.
try:
    import fork_checks
except ModuleNotFoundError as exc:
    if exc.name != "fork_checks":
        raise
else:
    fork_checks.bind(_helpers())
    CHECKS += fork_checks.CHECKS
    TEMPLATE_DIRS += fork_checks.TEMPLATE_DIRS
    CORE_DIRS += fork_checks.CORE_DIRS
    QUALITY_GATES_EXEMPT_LAYERS.update(fork_checks.QUALITY_GATES_EXEMPT_LAYERS)


# ---------------------------------------------------------------------------
# Report renderers
# ---------------------------------------------------------------------------

def _inspected(r):
    """Render what a check reported inspecting, when it reported anything."""
    if not r.get("notes"):
        return []
    return ["**Inspected**:", "", "```"] + r["notes"] + ["```", ""]


def render_pass(r):
    return ([f"### {r['status']}  {r['id']} — {r['title']}", ""]
            + _inspected(r))


def render_fail(r):
    lines = [f"### {r['status']}  {r['id']} — {r['title']}", ""]
    lines.extend(_inspected(r))
    lines.extend(["**Expected**: all assertions pass with no violations", "",
                  "**Observed**:", "", "```"])
    lines.extend(r["failures"])
    lines.extend(["```", ""])
    return lines


def render_err(r):
    return [f"### {r['status']}  {r['id']} — {r['title']}", "",
            f"**Error**: {r['error']}", ""]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

# PyYAML is a precondition of this suite, not a property of the tree the
# suite checks. Many checks read `templates/manifest.yaml` through it,
# and each reports the missing dependency itself -- so an incomplete
# environment reads as that many defects in a clean tree, which is what
# an external contributor sees on their first command. The count is not
# stated here: it moves with every check that reads the manifest, and
# the runner computes it at refusal time.
#
# Which checks need it is asked of the checks rather than listed here. A
# hand-kept list duplicates the guards and drifts from them; a guarded
# check returns its one failure before touching the filesystem, so asking
# costs nothing.
def _blocked_on_yaml(checks):
    """Return the IDs of `checks` whose only failure is the missing dependency."""
    blocked = []
    for check in checks:
        try:
            result = check["fn"]()
        except Exception:
            continue
        failures = result[0] if isinstance(result, tuple) else result
        if failures == [MISSING_YAML]:
            blocked.append(check["id"])
    return blocked


def main():
    started_at = datetime.datetime.now()

    args = sys.argv[1:]
    filter_ids = [a for a in args if not a.startswith("--")]

    checks = CHECKS
    if filter_ids:
        checks = [c for c in CHECKS if c["id"] in filter_ids]
        if not checks:
            print(f"No checks matched: {filter_ids}")
            sys.exit(1)

    # Refuse the run rather than reporting the environment as findings.
    # Nothing about the tree has been read at this point, so there is no
    # partial verdict worth printing alongside the refusal.
    if not HAS_YAML:
        blocked = _blocked_on_yaml(checks)
        if blocked:
            print(
                f"PyYAML is not installed, and {len(blocked)} of the "
                f"{len(checks)} selected check(s) read "
                f"templates/manifest.yaml through it:"
            )
            print(f"  {', '.join(blocked)}")
            print("")
            print("  pip install pyyaml")
            print("")
            print(
                "No check has run. This is an incomplete environment, not a "
                "finding about the tree."
            )
            sys.exit(1)

    results = {PASS: 0, FAIL: 0, ERR: 0}
    run_results = []

    print(f"Running {len(checks)} check(s)...\n")

    for check in checks:
        try:
            # A check returns its failures, or (failures, notes) when it
            # reports what it inspected. Both shapes are accepted so a check
            # gains the report without every other one changing.
            result = check["fn"]()
            failures, notes = result if isinstance(result, tuple) else (result, [])

            # A check that would pass while reporting no inputs is the thing
            # this suite is guarding against, so the runner refuses it rather
            # than trusting each check to remember. A failing check has
            # already said something; only a silent pass is rejected here.
            if not failures and not notes:
                failures = [
                    "  the check passed without reporting what it inspected — "
                    "a corpus that empties is indistinguishable from a clean "
                    "tree until the inputs are counted"
                ]
        except Exception as e:
            print(f"  {ERR}  {check['id']}  — {e}")
            results[ERR] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": ERR, "failures": [], "error": str(e),
            })
            continue

        if failures:
            print(f"  {FAIL}  {check['id']}")
            for line in notes:
                print(line)
            for line in failures:
                print(line)
            results[FAIL] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": FAIL, "failures": failures, "notes": notes,
                "error": None,
            })
        else:
            print(f"  {PASS}  {check['id']}")
            for line in notes:
                print(line)
            results[PASS] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": PASS, "failures": [], "notes": notes,
                "error": None,
            })

    elapsed = (datetime.datetime.now() - started_at).total_seconds()
    total = sum(results.values())
    print(
        f"\n{total} checks — "
        f"{results[PASS]} passed  "
        f"{results[FAIL]} failed  "
        f"{results[ERR]} errors"
        f"  ({elapsed:.1f}s)"
    )

    write_report(run_results, started_at, "smoke", {
        PASS: render_pass,
        FAIL: render_fail,
        ERR: render_err,
    })

    ok = results[FAIL] == 0 and results[ERR] == 0
    print_verdict(ok, "%d checks, %d failed, %d errors"
                  % (total, results[FAIL], results[ERR]))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
