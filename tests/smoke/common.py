"""Helpers every smoke family shares: the manifest, the template files, and
what a check reports it inspected.
"""

import io
import os
import re

# One definition of what a manifest section is, shared with the resolver,
# so a fork's own key is read here exactly as it is resolved there.
from resolve_chain import core_tier, entry_sections

from testkit import ROOT, template_files


# Bound to None without PyYAML, so a check can import it and guard on
# HAS_YAML rather than on an import of its own.
try:
    import yaml
    HAS_YAML = True
except ImportError:
    yaml = None
    HAS_YAML = False


# The one failure a check returns when the manifest cannot be read at all.
# It is a constant rather than fourteen copies of a string so the runner's
# preflight can recognise it, instead of keeping a second list of which
# checks need the dependency.
MISSING_YAML = "  PyYAML not installed — run: pip install pyyaml"


# ---------------------------------------------------------------------------
# [ID: ...] declaration matching
# ---------------------------------------------------------------------------
# An [ID: foo] tag is a declaration only when it is the entire content of
# its line (whitespace-only surroundings allowed). Inline occurrences in
# prose, code blocks, or table cells are references and MUST NOT count as
# declarations — otherwise referencing another template's ID in prose
# would trip duplicate-detection (SYS-02).

_DECL_LINE = re.compile(r'^\s*\[ID:\s*([^\]]+)\]\s*$')


def iter_id_declarations(content):
    """Yield (section_id, line_number) for each [ID:] declaration line."""
    for i, line in enumerate(content.splitlines(), start=1):
        m = _DECL_LINE.match(line)
        if m:
            yield m.group(1).strip(), i


# ---------------------------------------------------------------------------
# Manifest resolution helpers (shared by MNF-02, MNF-03, MNF-04)
# ---------------------------------------------------------------------------

def _load_manifest():
    """Load manifest.yaml and return (core_ids, entries, file_to_id)."""
    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = {}
    for section in entry_sections(data):
        for entry in data[section]:
            entries[entry["id"]] = entry

    file_to_id = {e["file"]: e["id"] for e in entries.values()}
    return core_tier(data), entries, file_to_id


def _stacks(entries):
    """The entries the manifest files under its stacks: key, in its order.

    Selected by key rather than by directory. The fixture stack lives under
    templates/fixture/, and once the stacks move to forks no stack lives
    under templates/stack/ at all -- a directory selector would then read
    nothing and every check built on it would pass on an empty list.
    """
    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [entries[e["id"]] for e in data.get("stacks", [])
            if e["id"] in entries]


def _resolve_stack(stack_id, core_ids, entries):
    """Resolve full dependency chain for a stack.

    Returns (ordered_files, resolved_ids).
    """
    resolved = set()
    files = []

    def add(eid):
        if eid in resolved:
            return
        resolved.add(eid)
        entry = entries.get(eid)
        if entry:
            files.append(entry["file"])

    def resolve(eid):
        if eid in resolved:
            return
        entry = entries.get(eid)
        if not entry:
            return
        for dep in entry.get("depends_on", []):
            resolve(dep)
        add(eid)

    for cid in core_ids:
        add(cid)

    resolve(stack_id)
    return files, resolved


def _opt_in_roots(core_ids, entries):
    """The manifest IDs a project picks directly, that no stack chain carries.

    A project resolves its stack, then its extras, then its platform, each as
    its own root -- the algorithm ADR-004 states and `tools/resolve_chain.py`
    implements. An opt-in template is therefore guaranteed only the core tier
    plus its own dependency tree, so a directive or a prose reference it
    carries has to resolve there, not in a stack chain it may never be paired
    with. Resolving stacks alone leaves these roots unexamined, and a check
    that examines nothing reports the same result as a clean tree.
    """
    reached = set()
    for entry in _stacks(entries):
        _, ids = _resolve_stack(entry["id"], core_ids, entries)
        reached |= ids
    return sorted(set(entries) - reached)


def _roots_by_kind(core_ids, entries):
    """The two kinds of root a project picks, returned apart.

    A check covering both kinds reports each count rather than their sum.
    One number cannot tell a tree where every root resolved from a
    resolver that stopped enumerating one kind: 37 reads the same whether
    it is 17 and 20 or 37 and 0. Two numbers move independently, so the
    kind that empties takes its own count to zero where a reader sees it.
    """
    stacks = sorted(e["id"] for e in _stacks(entries))
    return stacks, _opt_in_roots(core_ids, entries)


# The directories the template corpus is expected to fill. The corpus itself
# comes from git; this list exists so a renamed or emptied directory is a
# finding rather than a corpus that quietly shrinks.
TEMPLATE_DIRS = [
    "templates/core",
    "templates/security",
    "templates/infra",
    "templates/data",
    "templates/backend",
    "templates/frontend",
    "templates/fixture",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def all_template_files():
    """Absolute paths to every template the manifest governs.

    Sourced from git rather than from a walk of TEMPLATE_DIRS. A hardcoded
    directory list defines what the checks reading it can see: a template
    outside the list is invisible to all of them, and the corpus count they
    print cannot move to say so -- a stale count and a correct one read
    alike when the enumerator never looked.
    """
    return [os.path.join(ROOT, p.replace("/", os.sep))
            for p in template_files()]


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


class Inspected:
    """The inputs a check reached, reported whatever its verdict.

    A check that reports only what it found reads identically when its
    corpus empties and when the tree is clean, so a corpus that quietly
    goes to zero keeps reporting green -- the suite's count of passing
    checks stops meaning what a reader takes it to mean. Every count is
    reported on every run, and a count below its floor is a failure: the
    check answered a question it never asked.
    """

    def __init__(self):
        self._counts = []

    def count(self, label, value, floor=1):
        """Record an input count and return the value it was taken from.

        `value` may be a number or anything with a length, so a call can
        wrap the collection a check is about to iterate.
        """
        n = value if isinstance(value, int) else len(value)
        self._counts.append((label, n, floor))
        return value

    def notes(self):
        return [f"  {label}: {n}" for label, n, _ in self._counts]

    def failures(self):
        return [
            f"  {label}: {n} — below the floor of {floor}; the check reached "
            f"nothing and an empty corpus reports the same result as a clean "
            f"tree"
            for label, n, floor in self._counts if n < floor
        ]


# ---------------------------------------------------------------------------
# DEPENDS ON extraction
# ---------------------------------------------------------------------------
# A DEPENDS ON declaration is only meaningful in the file header, and every
# one in the tree sits on line 2, 3 or 4 -- before the first section heading,
# measured across all template files. Consumer-facing sections legitimately
# quote the directive syntax to explain the composition model, so extracting
# it from the whole file reads that prose as a declaration and fails against
# a file that does not exist, naming a path nobody wrote.

HEADER_END_RE = re.compile(r"^## ")
DEPENDS_RE = re.compile(r"\[DEPENDS ON:\s*([^\]]+)\]")


def depends_on_refs(content):
    """Return the paths declared by the header's DEPENDS ON directive."""
    refs = []
    for line in content.splitlines():
        if HEADER_END_RE.match(line):
            break
        for match in DEPENDS_RE.finditer(line):
            refs.extend(ref.strip() for ref in match.group(1).split(","))
    return refs
