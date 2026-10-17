"""Resolve dependency chain for a stack template.

Uses the same minimal YAML parser as sync.py — no external
dependencies required.

Usage:
    py tools/resolve.py <stack-id>            # print resolved file list
    py tools/resolve.py <stack-id> --concat   # print concatenated content
    py tools/resolve.py --generate            # cache all stacks to generated/
    py tools/resolve.py --list                # list available stack IDs
    py tools/resolve.py --roots               # list every root a project picks

The resolution algorithm follows ADR-004:
  1. Add all core tier IDs
  2. Recursively resolve the stack's depends_on tree
  3. Append extras (if any)
"""

import io
import os
import re
import sys
from pathlib import Path

# Set the output encoding and line ending at the boundary rather than
# inheriting the console defaults. The encoding mangles any non-ASCII this
# program prints; the line ending is why the IDs this program lists are
# consumed by a shell loop. On Windows a bare `print` emits CRLF, so each
# ID reaches the loop with a trailing carriage return, every lookup misses,
# and a reach measurement reports zero for a file that is in the chain.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass


# Ensure UTF-8 stdout on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", newline="\n"
    )

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "templates" / "manifest.yaml"
GENERATED = ROOT / "generated"


# ---- minimal YAML parser (shared with sync.py) ----

def parse_manifest(text):
    """Parse manifest.yaml into {section: [entries]}."""
    sections = {}
    current_section = None
    current_entry = None
    list_key = None

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        m = re.match(r"^(\w[\w-]*):\s*$", raw_line)
        if m and not raw_line.startswith(" "):
            key = m.group(1)
            if key == "version":
                continue
            current_section = key
            sections.setdefault(current_section, [])
            current_entry = None
            list_key = None
            continue

        # top-level inline list: core: [a, b, c]
        m = re.match(r"^(\w[\w-]*):\s+\[(.+)\]$", raw_line)
        if m and not raw_line.startswith(" "):
            key = m.group(1)
            sections[key] = [v.strip() for v in m.group(2).split(",")]
            continue

        m = re.match(r'^(\w[\w-]*):\s+"?([^"]+)"?\s*$', raw_line)
        if m and not raw_line.startswith(" "):
            continue

        if current_section is None:
            continue

        if stripped.startswith("- id:"):
            current_entry = {"id": stripped.split(":", 1)[1].strip()}
            sections[current_section].append(current_entry)
            list_key = None
            continue

        if current_entry is None:
            continue

        m = re.match(r"^(\w[\w_]*):\s+\[(.+)\]$", stripped)
        if m:
            key = m.group(1)
            vals = [v.strip() for v in m.group(2).split(",")]
            current_entry[key] = vals
            list_key = None
            continue

        m = re.match(r"^(\w[\w_]*):\s*(.*)$", stripped)
        if m and not stripped.startswith("-"):
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                list_key = key
                current_entry[key] = []
            else:
                current_entry[key] = val
                list_key = None
            continue

        # bracketed continuation after an empty "key:" line:
        #   depends_on:
        #     [a, b, c]
        if (
            list_key
            and stripped.startswith("[")
            and stripped.endswith("]")
        ):
            inner = stripped[1:-1]
            current_entry[list_key] = [
                v.strip() for v in inner.split(",") if v.strip()
            ]
            list_key = None
            continue

        if stripped.startswith("- ") and list_key:
            current_entry[list_key].append(stripped[2:].strip())
            continue

    return sections


# ---- resolution engine ----

def load_manifest():
    """Load and parse manifest.yaml.

    Returns (core_ids, entries_by_id, stacks).
    """
    text = io.open(MANIFEST, encoding="utf-8").read()
    manifest = parse_manifest(text)

    entries = {}
    for section in ("base", "platform", "frontend", "backend", "stacks"):
        for entry in manifest.get(section, []):
            entries[entry["id"]] = entry

    core_ids = manifest.get("core", [])

    stacks = manifest.get("stacks", [])
    return core_ids, entries, stacks


def is_fixture(entry):
    """True for an entry that is test input rather than a template to pick."""

    # This parser reads the flag as the string "true"; PyYAML reads a bool.
    return entry.get("fixture") in (True, "true")


def load_catalogue():
    """load_manifest() without the fixture entries.

    Returns (core_ids, entries_by_id, stacks), as load_manifest() does.
    """
    core_ids, entries, stacks = load_manifest()

    # A fixture is a root nothing depends on, so leaving it out changes no
    # other chain. Every listing, table and cached file describes what a
    # project can pick, and a fixture is not among those.
    entries = {eid: e for eid, e in entries.items() if not is_fixture(e)}
    stacks = [s for s in stacks if not is_fixture(s)]
    return core_ids, entries, stacks


class ResolveError(Exception):
    """A chain that cannot be resolved; the message names what broke."""


def _resolve_order(root, core_ids, entries):
    """The IDs a root's chain adds after the core tier, dependencies first.

    Raises ResolveError for an ID with no manifest entry, naming it and the
    entry that names it, and for a dependency cycle, naming it as a path.
    """

    # A fork's stacks depend on upstream IDs the fork does not control, so
    # a broken chain is a message, not a silently shorter chain or a
    # RecursionError with no ID in it.
    for cid in core_ids:
        if cid not in entries:
            raise ResolveError(
                "Missing dependency: the core tier names %s, which has no "
                "manifest entry" % cid)

    done = set(core_ids)
    order = []
    path = []

    def visit(eid, named_by):
        if eid in done:
            return
        if eid not in entries and named_by is None:
            raise ResolveError("Unknown root: %s has no manifest entry" % eid)
        if eid not in entries:
            raise ResolveError(
                "Missing dependency: %s depends on %s, which has no manifest "
                "entry" % (named_by, eid))
        if eid in path:
            cycle = path[path.index(eid):] + [eid]
            raise ResolveError("Dependency cycle: " + " -> ".join(cycle))
        path.append(eid)
        for dep in entries[eid].get("depends_on", []):
            visit(dep, eid)
        path.pop()
        done.add(eid)
        order.append(eid)

    visit(root, None)
    return order


def resolve_chain(stack_id, core_ids, entries):
    """Resolve full dependency chain for a stack.

    Returns ordered list of file paths (relative to repo root). Raises
    ResolveError when the chain names a missing ID or holds a cycle.
    """
    order = list(core_ids) + _resolve_order(stack_id, core_ids, entries)
    return [entries[eid]["file"] for eid in order if "file" in entries[eid]]


def opt_in_roots(core_ids, entries, stacks):
    """The IDs a project picks directly that no stack chain carries.

    A project resolves its stack, then its extras, then its platform, each
    as its own root. An entry reachable only by the second and third steps
    is guaranteed the core tier plus its own dependency tree and nothing
    more, so measuring reach over stacks alone leaves it out of the count.
    """
    reached = set()
    for stack in stacks:
        for eid in resolve_ids(stack["id"], core_ids, entries):
            reached.add(eid)
    return sorted(set(entries) - reached)


def resolve_ids(stack_id, core_ids, entries):
    """Resolve a chain and return the IDs in it rather than the files."""
    return set(core_ids) | set(_resolve_order(stack_id, core_ids, entries))


def read_file(rel_path):
    """Read a file relative to the repo root."""
    return io.open(ROOT / rel_path, encoding="utf-8").read()


BANNER = (
    "<!-- Generated by `py tools/resolve.py --generate`. Edit the\n"
    "     source templates under templates/, not this file. Run\n"
    "     `py tools/resolve.py --check` to verify the committed\n"
    "     files are up to date. -->\n"
)


def concat_chain(files):
    """Read and concatenate all files in the chain."""
    parts = []
    for f in files:
        content = read_file(f)
        parts.append(f"<!-- {f} -->\n{content}")
    return BANNER + "\n" + "\n\n".join(parts)


def generate_all(core_ids, entries, stacks):
    """Generate cached resolved files for all stacks."""
    GENERATED.mkdir(exist_ok=True)
    count = 0
    for stack in stacks:
        sid = stack["id"]
        files = resolve_chain(sid, core_ids, entries)
        content = concat_chain(files)
        out = GENERATED / f"{sid}.md"

        # Pin the line ending as well as the encoding. This artifact is
        # committed, and Python translates every newline on a platform
        # whose default is CRLF, so the file the repository holds would
        # depend on the machine that regenerated it.
        io.open(out, "w", encoding="utf-8",
                newline="\n").write(content)
        print(f"  {sid} -> {out.relative_to(ROOT)}  ({len(files)} files)")
        count += 1
    print(f"\n{count} file(s) generated.")


def check_generated(core_ids, entries, stacks):
    """Check that generated/ files match current resolution.

    Returns list of stale stack IDs.
    """
    stale = []
    for stack in stacks:
        sid = stack["id"]
        out = GENERATED / f"{sid}.md"
        if not out.exists():
            stale.append(sid)
            continue
        files = resolve_chain(sid, core_ids, entries)
        expected = concat_chain(files)
        actual = io.open(out, encoding="utf-8").read()
        if expected != actual:
            stale.append(sid)
    return stale


# ---- CLI ----

KNOWN_FLAGS = {"--help", "--list", "--roots", "--generate", "--check", "--concat"}


def main():
    try:
        _cli(sys.argv[1:])
    except ResolveError as error:
        print(error)
        sys.exit(1)


def _cli(args):

    if not args or args == ["--help"]:
        print(__doc__)
        sys.exit(0)

    core_ids, entries, _ = load_manifest()

    # The listings and the cache offer what a project can pick. A fixture
    # still resolves when named, which is how the checks reach it.
    _, offered, catalogue = load_catalogue()

    if "--list" in args:
        for s in catalogue:
            label = s.get("label", "")
            print(f"  {s['id']:<30s} {label}")
        sys.exit(0)

    if "--roots" in args:
        for s in catalogue:
            print(s["id"])
        for rid in opt_in_roots(core_ids, offered, catalogue):
            print(rid)
        sys.exit(0)

    if "--generate" in args:
        generate_all(core_ids, offered, catalogue)
        sys.exit(0)

    if "--check" in args:
        stale = check_generated(core_ids, offered, catalogue)
        if stale:
            print(f"{len(stale)} stale file(s):")
            for sid in stale:
                print(f"  {sid}")
            sys.exit(1)
        else:
            print("All generated files up to date.")
            sys.exit(0)

    do_concat = "--concat" in args

    # A flag this program does not implement is a mistake, not a root. Left
    # to fall through it was reported as an unknown stack id, which named the
    # wrong thing, and after roots became a validated list it would have been
    # reported as no root at all.
    unknown = [a for a in args if a.startswith("--") and a not in KNOWN_FLAGS]
    if unknown:
        print("Unknown flag: " + ", ".join(unknown))
        print(f"Known flags: {', '.join(sorted(KNOWN_FLAGS))}")
        sys.exit(1)

    # Every argument is accounted for. Taking args[0] and ignoring the rest
    # let a root that does not exist pass silently whenever it followed a
    # valid one, so a typo in a scripted invocation resolved the wrong chain
    # and exited 0.
    roots = [a for a in args if not a.startswith("--")]

    if not roots:
        print("No root given. Run with --roots to see what a project can pick.")
        sys.exit(1)

    # Roots do not compose. Under ADR-035 a stack and an orthogonal template
    # each resolve as their own root, so concatenating two of them would
    # report a chain no project ever loads.
    if len(roots) > 1:
        print("More than one root given: " + ", ".join(roots))
        print("Roots resolve independently -- run this once per root.")
        sys.exit(1)

    stack_id = roots[0]

    if stack_id not in entries:
        print(f"Unknown stack ID: {stack_id}")
        print("Run with --list to see available IDs.")
        sys.exit(1)

    files = resolve_chain(stack_id, core_ids, entries)

    if do_concat:
        print(concat_chain(files))
    else:
        for f in files:
            print(f)


if __name__ == "__main__":
    main()
