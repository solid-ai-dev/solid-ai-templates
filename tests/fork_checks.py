"""A fork's own smoke checks, and the directories and exemptions they add.

`run_smoke.py` takes this module in when the file exists. Everything here
reads content that belongs to a fork rather than to upstream -- stacks,
examples, the interview and the e2e cases -- so it lives beside that
content, and the runner both trees share stays identical.
"""

import os
import re
import types

from cases import ALL_TESTS

# The runner's helpers, bound by `bind` before any check here runs.
smoke = None


def bind(namespace):
    """Give the checks below the runner's helpers."""
    global smoke
    smoke = types.SimpleNamespace(**namespace)


# The template directories only a fork fills, added to the runner's lists:
# every template directory, and the ones TPL-08 requires an [ID:] tag in.
TEMPLATE_DIRS = [
    "templates/workflow",
    "templates/language",
    "templates/platform",
    "templates/stack",
]

CORE_DIRS = [
    "templates/workflow",
    "templates/language",
]

# Stack categories exempt from `base-quality-gates`, each because it is
# recorded at the most constrained context tier. SYS-18 asserts the reason
# against the tier file.
QUALITY_GATES_EXEMPT_LAYERS = {
    "hypermedia": "recorded at the most constrained context tier",
    "embedded": "recorded at the most constrained context tier",
}


# ---------------------------------------------------------------------------
# E2E-01 — all cases.py paths resolve to existing files
# ---------------------------------------------------------------------------

def check_e2e_01():
    failures = []
    seen = smoke.Inspected()

    interview = os.path.join(smoke.ROOT, "templates", "INTERVIEW.md")
    if not os.path.isfile(interview):
        failures.append("  INTERVIEW.md not found: templates/INTERVIEW.md")

    required_fields = ("id", "spec", "stack", "answers", "required")

    seen.count("test cases defined", len(ALL_TESTS))
    validated = 0
    for test in ALL_TESTS:
        if "skip" in test:
            continue

        validated += 1
        tid = test.get("id", "?")

        # Validate required fields
        for field in required_fields:
            if field not in test:
                failures.append(f"  {tid}: missing field: {field!r}")

        if not test.get("required"):
            failures.append(f"  {tid}: required list is empty")

        stack = test.get("stack", "")
        if stack:
            path = os.path.join(smoke.ROOT, stack)
            if not os.path.isfile(path):
                failures.append(f"  {tid}: stack file missing: {stack}")
            elif os.path.getsize(path) == 0:
                failures.append(f"  {tid}: stack file empty: {stack}")

        output_file = test.get("output_file", "templates/core/agents.md")
        path = os.path.join(smoke.ROOT, output_file)
        if not os.path.isfile(path):
            failures.append(f"  {tid}: output_file missing: {output_file}")

        for ef in test.get("extra_files", []):
            path = os.path.join(smoke.ROOT, ef)
            if not os.path.isfile(path):
                failures.append(f"  {tid}: extra_file missing: {ef}")

    seen.count("cases validated", validated)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-05 — end-of-session audit rendered faithfully (inline or delegated)
# ---------------------------------------------------------------------------
# A procedural checklist (the scope.md End of session audit) loses steps and
# its enforcement header when a generator condenses it into bullets. The two
# compliant renderings — inline-verbatim and hard-delegation — both keep the
# load-bearing phrase ("execute each item ... do not summarize"); a paraphrase
# drops it. This check asserts that phrase survives in the output spec
# (agents.md §6.3 directive, every output model) and in every example
# CLAUDE.md that declares a session-protocol section. Examples with no such
# section are out of scope (skipped), not failures.

ENFORCE_RE = re.compile(
    r"execute each item|do not summari[sz]e|do not paraphrase",
    re.IGNORECASE,
)


def _section_block(lines, start_index, stop_pattern):
    """Return text from start_index+1 until a line matching stop_pattern."""
    body = []
    for line in lines[start_index + 1:]:
        if stop_pattern.match(line):
            break
        body.append(line)
    return "\n".join(body)


def check_sys_05():
    failures = []
    seen = smoke.Inspected()

    # 1) Output spec — every §6.3 directive in agents.md carries the rule.
    agents_path = os.path.join(smoke.ROOT, "templates", "core", "agents.md")
    a_lines = smoke.read(agents_path).splitlines()
    h63 = re.compile(r"^###\s+6\.3\b")
    stop_spec = re.compile(r"^(#{1,3}\s|```)")
    found = 0
    for i, line in enumerate(a_lines):
        if h63.match(line):
            found += 1
            block = _section_block(a_lines, i, stop_spec)
            if not ENFORCE_RE.search(block):
                failures.append(
                    f"  agents.md:{i + 1}: §6.3 directive must require "
                    f"inline-verbatim or hard-delegation (missing 'execute "
                    f"each item' / 'do not summarize')"
                )
    seen.count("6.3 directives in agents.md", found)
    if not found:
        failures.append("  agents.md: no '### 6.3' directive found")

    # 2) Examples — any CLAUDE.md with a session-protocol section must render
    #    the audit faithfully; examples without one are out of scope.
    examples_dir = os.path.join(smoke.ROOT, "examples")
    head = re.compile(r"^#{2,3}\s.*([Ss]ession protocol|[Ee]nd of session)")
    stop_top = re.compile(r"^##\s")
    examples_read = 0
    protocols = 0
    if os.path.isdir(examples_dir):
        for name in sorted(os.listdir(examples_dir)):
            cm = os.path.join(examples_dir, name, "CLAUDE.md")
            if not os.path.isfile(cm):
                continue
            examples_read += 1
            e_lines = smoke.read(cm).splitlines()
            start = next((i for i, l in enumerate(e_lines) if head.match(l)),
                         None)
            if start is None:
                continue
            protocols += 1
            block = _section_block(e_lines, start, stop_top)
            if not ENFORCE_RE.search(block):
                failures.append(
                    f"  examples/{name}/CLAUDE.md: session-protocol section "
                    f"neither inlines the audit verbatim nor hard-delegates "
                    f"(missing 'execute each item' / 'do not summarize') — a "
                    f"soft reference or paraphrase drops the wrap-up steps"
                )

    seen.count("example context files read", examples_read)
    seen.count("of those, carrying a session-protocol section", protocols)
    return seen.failures() + failures, seen.notes()



# ---------------------------------------------------------------------------
# SYS-08 — every showcased stack keeps its example CLAUDE.md
# ---------------------------------------------------------------------------
# SYS-05 only validates examples that already exist, so a committed example
# could be removed or renamed without any structural failure. This gate
# locks in the example->stack mapping (per ADR-016 examples are
# agent-generated, regenerated on material change): each required example
# MUST have a non-empty CLAUDE.md, and the stack it demonstrates MUST exist
# in the manifest. Adding a new example registers it here; two examples may
# map to the same stack (e.g. astro-portfolio and hybrid-astro).

REQUIRED_EXAMPLES = {
    "astro-portfolio": "stack-astro",
    "hybrid-astro": "stack-astro",
    "fastapi-service": "stack-fastapi",
    "order-service": "stack-fastapi",
    "flask-api": "stack-flask",
    "go-service": "stack-go-service",
    "metricshub": "stack-go-echo",
}


def check_sys_08():
    if not smoke.HAS_YAML:
        return [smoke.MISSING_YAML]

    _, entries, _ = smoke._load_manifest()
    failures = []
    seen = smoke.Inspected()
    seen.count("required examples checked", len(REQUIRED_EXAMPLES))
    seen.count("stacks they map to", len(set(REQUIRED_EXAMPLES.values())))

    for example, stack_id in sorted(REQUIRED_EXAMPLES.items()):
        cm = os.path.join(smoke.ROOT, "examples", example, "CLAUDE.md")
        if not os.path.isfile(cm):
            failures.append(
                f"  examples/{example}/CLAUDE.md missing — required "
                f"example for stack '{stack_id}' (ADR-016: regenerate, "
                f"do not delete)"
            )
        elif os.path.getsize(cm) == 0:
            failures.append(f"  examples/{example}/CLAUDE.md is empty")
        if stack_id not in entries:
            failures.append(
                f"  {example}: mapped stack '{stack_id}' not in manifest"
            )

    return seen.failures() + failures, seen.notes()


CHECKS = [
    {"id": "SYS-05", "spec": "SAIT-SMK-SYS-05-001A",
     "title": "End-of-session audit inlined verbatim or hard-delegated", "fn": check_sys_05},
    {"id": "SYS-08", "spec": "SAIT-SMK-SYS-08-001A",
     "title": "Every showcased stack keeps its example CLAUDE.md", "fn": check_sys_08},
    {"id": "E2E-01", "spec": "SAIT-SMK-E2E-01-001A",
     "title": "All cases.py paths resolve to existing files", "fn": check_e2e_01},
]
