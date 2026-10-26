"""Resolve dependency chain for a stack template.

Uses the same minimal YAML parser as sync_docs.py — no external
dependencies required.

Usage:
    py tools/resolve_chain.py <stack-id>            # print resolved file list
    py tools/resolve_chain.py <stack-id> --concat   # print concatenated content
    py tools/resolve_chain.py --generate            # cache all stacks to generated/
    py tools/resolve_chain.py --list                # list available stack IDs
    py tools/resolve_chain.py --roots               # list every root a project picks

The resolution algorithm follows ADR-004:
  1. Add all core tier IDs
  2. Recursively resolve the stack's depends_on tree
  3. Append extras (if any)
"""

import io
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


# ---- minimal YAML parser (shared with sync_docs.py) ----

def parse_manifest(text):
    """Parse manifest.yaml into {section: [entries]}, and each task key into
    {kind: description}."""
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
            sections.setdefault(current_section,
                                {} if key in TASK_KEYS else [])
            current_entry = None
            list_key = None
            continue

        # A task key is a mapping of kind to description, one per line.
        if current_section in TASK_KEYS and raw_line.startswith(" "):
            m = re.match(r'^\s+([a-z][a-z0-9-]*):\s+"?(.+?)"?\s*$', raw_line)
            if m:
                sections[current_section][m.group(1)] = m.group(2)
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

# The top-level keys that hold something other than template entries. Every
# other key is a section of entries, so a fork's templates resolve from a key
# of its own, beside upstream's, without any tool knowing its name.
# The keys that list the kinds of task a load directive may name, each a
# mapping of kind to the description its skill carries: upstream's `tasks`,
# then a fork's `fork_tasks`.
TASK_KEYS = ("tasks", "fork_tasks")

NON_ENTRY_KEYS = ("version", "core", "fork_core") + TASK_KEYS


def entry_sections(manifest):
    """The manifest's sections of template entries, in manifest order."""
    return [key for key, value in manifest.items()
            if key not in NON_ENTRY_KEYS and isinstance(value, list)
            and all(isinstance(entry, dict) for entry in value)]


def core_tier(manifest):
    """Every chain's core tier: upstream's `core`, then a fork's `fork_core`.

    A fork MUST NOT edit `core`, so a template it adds to every chain goes in
    `fork_core`, which is the fork's own.
    """
    return list(manifest.get("core") or []) + list(
        manifest.get("fork_core") or [])


def task_kinds(manifest):
    """Every kind of task a load directive may name, with the description its
    skill carries: upstream's, then a fork's."""
    kinds = {}
    for key in TASK_KEYS:
        kinds.update(manifest.get(key) or {})
    return kinds


# A load directive is one tag line under a heading, naming where the
# heading's rules load: a kind of task, or `check` for rules a check
# enforces. A heading without one loads on every turn (spec, chapter 8.1).
LOAD_CHECK = "check"
LOAD_LINE = re.compile(r"^\[LOAD:\s*([^\]]*?)\s*\]\s*$")
TAG_LINE = re.compile(r"^\[[A-Z][A-Z ]*:[^\]]*\]\s*$")
HEADING_LINE = re.compile(r"^(#{1,6})\s+\S")
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})")


def load_directives(text):
    """Each load directive in a template, in order, as a dict: `line`, its
    `kind`, the `heading` line it governs or None, and the findings about
    its place: `placed` is False after a content line or under no heading,
    `second` is True for a heading's second directive, and `inside` names
    the kind an enclosing heading already loads as."""
    found, stack, in_tags, fence = [], [], False, None
    for number, line in enumerate(text.splitlines(), start=1):
        run = FENCE_LINE.match(line)
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            in_tags = False
            continue
        if fence is not None:
            continue
        heading = HEADING_LINE.match(line)
        if heading:
            level = len(heading.group(1))
            while stack and stack[-1]["level"] >= level:
                stack.pop()
            stack.append({"level": level, "line": number, "kind": None})
            in_tags = True
            continue
        load = LOAD_LINE.match(line.strip())
        if load:
            own = stack[-1] if stack and in_tags else None
            enclosing = [h["kind"] for h in stack[:-1] if h["kind"]]
            found.append({
                "line": number, "kind": load.group(1),
                "heading": own["line"] if own else None,
                "placed": own is not None,
                "second": bool(own and own["kind"]),
                "inside": enclosing[-1] if enclosing and own else None})
            if own and not own["kind"]:
                own["kind"] = load.group(1)
            continue
        if not line.strip() or TAG_LINE.match(line.strip()):
            continue
        in_tags = False
    return found


def load_manifest():
    """Load and parse manifest.yaml.

    Returns (core_ids, entries_by_id, stacks).
    """
    text = io.open(MANIFEST, encoding="utf-8").read()
    manifest = parse_manifest(text)

    entries = {}
    for section in entry_sections(manifest):
        for entry in manifest[section]:
            # A second entry under one ID would replace the first, and the
            # chain would carry whichever file came last with no warning.
            if entry["id"] in entries:
                raise ResolveError(
                    f"Manifest ID '{entry['id']}' is declared twice: "
                    f"{entries[entry['id']].get('file', '?')} and "
                    f"{entry.get('file', '?')} ({section}:)")
            entries[entry["id"]] = entry

    core_ids = core_tier(manifest)

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


# Who names an ID, where no entry does: the core tier itself, or nobody,
# which makes the ID a root the caller asked for.
CORE_TIER = object()


def _check_graph(roots, entries, named_by):
    """Raise ResolveError where the trees under `roots` break.

    An ID with no manifest entry is named with the entry that names it, and
    a dependency cycle is named as a path.
    """
    checked = set()
    path = []

    def visit(eid, by):
        if eid in checked:
            return
        if eid not in entries:
            if by is CORE_TIER:
                raise ResolveError(
                    "Missing dependency: the core tier names %s, which has "
                    "no manifest entry" % eid)
            if by is None:
                raise ResolveError(
                    "Unknown root: %s has no manifest entry" % eid)
            raise ResolveError(
                "Missing dependency: %s depends on %s, which has no manifest "
                "entry" % (by, eid))
        if eid in path:
            cycle = path[path.index(eid):] + [eid]
            raise ResolveError("Dependency cycle: " + " -> ".join(cycle))
        path.append(eid)
        for dep in entries[eid].get("depends_on", []):
            visit(dep, eid)
        path.pop()
        checked.add(eid)

    for root in roots:
        visit(root, named_by)


def _resolve_order(root, core_ids, entries):
    """The IDs a root's chain adds after the core tier, dependencies first.

    Raises ResolveError for an ID with no manifest entry, naming it and the
    entry that names it, and for a dependency cycle, naming it as a path.
    """

    # A fork's stacks depend on upstream IDs the fork does not control, so
    # a broken chain is a message, not a silently shorter chain or a
    # RecursionError with no ID in it. The core tier is checked on its own:
    # its entries are seeded below and never walked, so a fault under one of
    # them would otherwise pass in every chain.
    _check_graph(core_ids, entries, CORE_TIER)
    _check_graph([root], entries, None)

    # Every chain seeds the core tier and walks none of its dependencies,
    # so one outside the tier would be dropped from every chain with the
    # resolve clean. A fork's `fork_core` entry is where this arises.
    core = set(core_ids)
    for cid in core_ids:
        for dep in entries[cid].get("depends_on", []):
            if dep not in core:
                raise ResolveError(
                    "Core-tier entry %s depends on %s, which is outside the "
                    "core tier; add %s to core or fork_core, or drop the "
                    "dependency" % (cid, dep, dep))

    done = set(core_ids)
    order = []

    def visit(eid):
        if eid in done:
            return
        done.add(eid)
        for dep in entries[eid].get("depends_on", []):
            visit(dep)
        order.append(eid)

    visit(root)
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
    "<!-- Generated by `py tools/resolve_chain.py --generate`. Edit the\n"
    "     source templates under templates/, not this file. Run\n"
    "     `py tools/resolve_chain.py --check` to verify the committed\n"
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

    Returns (stale stack IDs, orphaned cache files). An orphan is a file
    under generated/ that no stack in `stacks` produces.
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
    owed = {f"{stack['id']}.md" for stack in stacks}
    cached = sorted(p.name for p in GENERATED.glob("*.md")) \
        if GENERATED.is_dir() else []
    orphans = [name for name in cached if name not in owed]
    return stale, orphans


# ---- CLI ----

KNOWN_FLAGS = {"--help", "--list", "--roots", "--generate", "--check", "--concat"}


def _check(core_ids, offered, catalogue, stacks):
    """--check: compare generated/ with the catalogue; exit with the verdict.

    `stacks` is every stack the manifest holds, fixtures included, and
    `catalogue` the ones a project can pick, which are the ones cached.
    """

    # Upstream offers no stack, so its cache is legitimately empty and a
    # zero count alone proves nothing. The fixture is always there, though,
    # so a manifest that parses to no stack at all is a parse that failed.
    if not stacks:
        print("The manifest parsed to no stack, not even the fixture; "
              "refusing to report an empty cache as up to date.")
        sys.exit(1)

    stale, orphans = check_generated(core_ids, offered, catalogue)
    print(f"stacks in the manifest: {len(stacks)}, of which a project can "
          f"pick {len(catalogue)}; generated files checked: {len(catalogue)}")
    for sid in stale:
        print(f"  stale: {sid}")
    for name in orphans:
        print(f"  orphaned: generated/{name}, which no stack produces")
    if stale or orphans:
        print(f"{len(stale) + len(orphans)} generated file(s) out of date. "
              f"Run py tools/resolve_chain.py --generate for a stale one, and "
              f"delete an orphaned one.")
        sys.exit(1)
    print("All generated files up to date.")
    sys.exit(0)


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

    core_ids, entries, stacks = load_manifest()

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
        _check(core_ids, offered, catalogue, stacks)

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
