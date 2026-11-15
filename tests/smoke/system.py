"""Smoke checks of the SYS family: properties of the repository as a whole."""

import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from collections.abc import Collection, Iterable, Mapping, Sequence

# One definition of what a manifest section is, shared with the resolver,
# so a fork's own key is read here exactly as it is resolved there.
from emit_context import EmitError
from emit_context import BUILT_LINE, MAP_HEADER, SECTIONS_DIR, section_rules
from emit_context import EXTEND_TAG, ID_TAG, OVERRIDE_TAG

# The emitter's line parser, which only reads a template; the reference
# reading of a chain's relationships in SYS-28 is the check's own.
from emit_context import _blocks as parse_rows
from emit_context import build as emit_build
from emit_context import build_sections as emit_sections
from emit_context import write as emit_write
from resolve_chain import (
    FENCE_LINE,
    HEADING_LINE as LEVEL_HEADING,
    LOAD_CHECK,
    Entry,
    Manifest,
    entry_sections,
    is_fixture,
    load_catalogue,
    load_directives,
    load_manifest,
    opt_in_roots,
    parse_manifest,
    read_file,
    resolve_chain,
    task_kinds,
    template_names,
)

from testkit import ROOT, template_files
from .common import (
    CheckResult,
    _load_manifest,
    _resolve_stack,
    _roots_by_kind,
    _stacks,
    all_template_files,
    depends_on_refs,
    HAS_YAML,
    Inspected,
    iter_id_declarations,
    MISSING_YAML,
    read,
    TEMPLATE_DIRS,
    yaml,
)


def missing_template_dirs() -> list[str]:
    """Expected directories that contribute no file to the corpus.

    A directory that is not there is a finding, not a skip. Skipping it
    makes a rename silent: every listed directory disappears and the check
    reports the same pass as a clean tree.
    """
    present = template_files()
    return [d for d in TEMPLATE_DIRS if not any(p.startswith(d + "/") for p in present)]


# ---------------------------------------------------------------------------
# SYS-01 — DEPENDS ON paths resolve to existing files
# ---------------------------------------------------------------------------


def check_sys_01() -> CheckResult:
    failures: list[str] = []
    seen = Inspected()
    refs_checked = 0

    files = seen.count("template files scanned", all_template_files())
    for filepath in files:
        for ref in depends_on_refs(read(filepath)):
            refs_checked += 1
            ref_path = os.path.join(ROOT, ref)
            if not os.path.isfile(ref_path):
                rel = os.path.relpath(filepath, ROOT)
                failures.append(f"  {rel}: DEPENDS ON '{ref}' — file not found")

    seen.count("DEPENDS ON references resolved", refs_checked)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-02 — all section IDs unique across all templates
# ---------------------------------------------------------------------------


def check_sys_02() -> CheckResult:
    failures: list[str] = []
    seen: dict[str, str] = {}
    inspected = Inspected()

    files = inspected.count("template files scanned", all_template_files())
    for filepath in files:
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT)
        for sid, _ in iter_id_declarations(content):
            if sid in seen:
                failures.append(f"  Duplicate ID '{sid}': {seen[sid]} and {rel}")
            else:
                seen[sid] = rel

    inspected.count("section IDs collected", len(seen))
    return inspected.failures() + failures, inspected.notes()


# ---------------------------------------------------------------------------
# SYS-03 — every template file has a manifest entry
# ---------------------------------------------------------------------------


def check_sys_03() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    manifest_files = set()
    for section in entry_sections(manifest):
        for entry in manifest[section]:
            if isinstance(entry, dict) and "file" in entry:
                manifest_files.add(entry["file"].replace("/", os.sep))

    failures: list[str] = []
    seen = Inspected()
    seen.count("files named in the manifest", len(manifest_files))

    files = seen.count("template files scanned", all_template_files())

    # The corpus comes from git, so an emptied or renamed directory shrinks
    # it silently. Naming the expected directories makes that a finding.
    for d in missing_template_dirs():
        failures.append(
            f"  {d}: expected template directory holds no tracked "
            f"template — the corpus lost a directory it is built to cover"
        )

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        rel_fwd = rel.replace(os.sep, "/")
        if rel_fwd not in {f.replace(os.sep, "/") for f in manifest_files}:
            failures.append(f"  {rel_fwd}: no manifest entry")

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-04 — DEPENDS ON headers match manifest depends_on
# ---------------------------------------------------------------------------


def check_sys_04() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    # Build id→file and file→depends_on(as files) maps
    id_to_file = {}
    for section in entry_sections(manifest):
        for entry in manifest[section]:
            if isinstance(entry, dict):
                id_to_file[entry["id"]] = entry["file"]

    file_manifest_deps = {}
    for section in entry_sections(manifest):
        for entry in manifest[section]:
            if isinstance(entry, dict):
                dep_files = set()
                for dep_id in entry.get("depends_on", []):
                    dep_file = id_to_file.get(dep_id)
                    if dep_file:
                        dep_files.add(dep_file)
                file_manifest_deps[entry["file"]] = dep_files

    failures: list[str] = []
    seen = Inspected()
    seen.count("manifest entries carrying depends_on", len(file_manifest_deps))

    files = seen.count("template files compared", all_template_files())
    for filepath in files:
        rel = os.path.relpath(filepath, ROOT).replace(os.sep, "/")
        content = read(filepath)

        # Collect file paths from DEPENDS ON headers
        header_files = set(depends_on_refs(content))

        manifest_deps = file_manifest_deps.get(rel, set())

        # Only flag if at least one side is non-empty
        if header_files == manifest_deps:
            continue

        only_header = sorted(header_files - manifest_deps)
        only_manifest = sorted(manifest_deps - header_files)

        parts = []
        if only_header:
            parts.append(f"header only: {', '.join(only_header)}")
        if only_manifest:
            parts.append(f"manifest only: {', '.join(only_manifest)}")
        if parts:
            failures.append(f"  {rel}: {'; '.join(parts)}")

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-06 — every usable stack's resolved chain carries the MUST sections
# ---------------------------------------------------------------------------
# ADR-017 defines the canonical stack-template section structure. The MUST
# tier — Stack, Commands, Project structure — is the stack-unique
# contribution the core tier cannot supply. Membership is judged on the
# resolved chain, so a derived stack may inherit a MUST section from its
# parent. Pure-library stacks (manifest layer: library) prescribe no
# directory tree and are exempt from Project structure.

_MUST_SECTIONS = ("Stack", "Commands", "Project structure")


def check_sys_06() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures: list[str] = []
    seen = Inspected()

    stacks = seen.count("stacks resolved", _stacks(entries))

    asserted = 0
    for stack in sorted(stacks, key=lambda e: e["id"]):
        sid = stack["id"]
        is_lib = stack.get("layer") == "library"
        files, _ = _resolve_stack(sid, core_ids, entries)

        blob = "\n".join(
            read(os.path.join(ROOT, f))
            for f in files
            if os.path.isfile(os.path.join(ROOT, f))
        )

        for section in _MUST_SECTIONS:
            if section == "Project structure" and is_lib:
                continue
            asserted += 1
            heading = re.compile(r"^##\s+" + re.escape(section) + r"\s*$", re.MULTILINE)
            if not heading.search(blob):
                failures.append(
                    f"  {sid}: resolved chain missing MUST section "
                    f"'## {section}' (ADR-017)"
                )

    seen.count("MUST sections asserted across those chains", asserted)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-09 — sync_docs.py --check inspects without writing
# ---------------------------------------------------------------------------
# A gate that repairs what it inspects reports clean on its second run, so
# only its first invocation carries information. This runs against a
# temporary copy and asserts both directions: check mode reports the
# difference and leaves the bytes alone, plain mode writes. Without the
# second assertion a function that did nothing at all would pass.


def check_sys_09() -> CheckResult:
    import tempfile

    tools_dir = os.path.join(ROOT, "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    try:
        import sync_docs as sync_tool
    except ImportError as error:
        return [f"  tools/sync_docs.py could not be imported: {error}"]

    marker = "demo"
    stale = (
        "before\n"
        f"<!-- generated:{marker} -->\n"
        "STALE CONTENT\n"
        f"<!-- /generated:{marker} -->\n"
        "after\n"
    )
    failures: list[str] = []
    seen = Inspected()
    assertions = 0

    with tempfile.TemporaryDirectory() as tmp:
        target = os.path.join(tmp, "target.md")

        io.open(target, "w", encoding="utf-8").write(stale)
        changed = sync_tool._update_file(target, {marker: "FRESH"}, True)
        after = io.open(target, encoding="utf-8").read()
        assertions += 2
        if not changed:
            failures.append(
                "  sync_docs.py --check did not report a difference it should see"
            )
        if after != stale:
            failures.append(
                "  sync_docs.py --check wrote to the file it was inspecting — the "
                "first invocation repairs the tree and the second reports "
                "clean"
            )

        io.open(target, "w", encoding="utf-8").write(stale)
        sync_tool._update_file(target, {marker: "FRESH"})
        written = io.open(target, encoding="utf-8").read()
        assertions += 1
        if "FRESH" not in written:
            failures.append(
                "  sync_docs.py without --check did not write; the read-only "
                "assertion above would pass on a no-op"
            )

    # The corpus is a fixture this check builds, so what it reports reaching
    # is the assertions it ran against it. A refactor that returns before
    # them leaves the count short rather than reporting a pass.
    seen.count("fixtures written", 2)
    seen.count("assertions run against them", assertions, floor=3)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-10 — a quoted DEPENDS ON directive in prose is not a declaration
# ---------------------------------------------------------------------------
# Consumer-facing sections quote the directive syntax to explain the
# composition model, and reading that prose as a declaration fails the tree
# against a file nobody wrote. The extraction is restricted to the header,
# which is where every real declaration in the tree sits. This asserts both
# directions on a synthetic document: the header is read, and a backticked or
# fenced occurrence in the body is not. Without the positive case, an
# extractor that returned nothing at all would pass.


def check_sys_10() -> CheckResult:
    document = (
        "# Base — Example\n"
        "[ID: base-example]\n"
        "[DEPENDS ON: templates/core/git.md]\n"
        "\n"
        "## Composition\n"
        "\n"
        "Governance resolves through `[DEPENDS ON: ...]` in each file.\n"
        "\n"
        "```\n"
        "[DEPENDS ON: templates/does-not-exist.md]\n"
        "```\n"
    )

    refs = depends_on_refs(document)
    failures: list[str] = []
    seen = Inspected()
    seen.count("synthetic documents inspected", 1)
    seen.count(
        "directive occurrences in the document", document.count("[DEPENDS ON:"), floor=3
    )
    seen.count("occurrences read as a declaration", len(refs))

    if refs != ["templates/core/git.md"]:
        failures.append(
            f"  header declaration not read as the only one: {refs!r} — a "
            f"backticked or fenced directive in body prose is documentation, "
            f"not a declaration, and reading it names a file nobody wrote"
        )

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-11 — a prose reference to another file's section ID resolves in every
# chain that carries the referencing file
# ---------------------------------------------------------------------------
# TPL-04 and TPL-06 cover EXTEND/OVERRIDE directives. A rule that names
# another section in running prose -- "`base-quality-gates` states which
# categories a project MUST gate" -- is checked by neither, and it costs
# reach: the referencing file and the referenced one sit at different depths
# in the graph, so the reference resolves in the chains that carry both and
# dangles in the rest. A reader of a dangling one is sent to a section their
# context file does not contain.
#
# The failure is invisible from either file. It appears only per chain, which
# is why this check resolves every root a project can pick rather than reading
# the two files.

# What counts as a reference is decided by the IDs the tree declares, not by
# a list of layer prefixes. A prefix list matches file-level IDs, where a
# reference is least likely to dangle -- the section-level IDs the rule is
# actually about are named `quality-gates-layers`, `security-authn`,
# `testing-shared-path-breadth`, and a prefix list is blind to all of them.
# So any backticked token is a candidate and membership in the declared set
# decides, which cannot narrow again as IDs are added.
_BACKTICKED_TOKEN = re.compile(r"`([a-z0-9][a-z0-9-]*)`")

# A token no template declares is a finding only when it is shaped like an
# ID -- `eslint` and `main` are backticked tokens too, and reading every one
# of them as a broken reference makes the check unusable.
_LAYER_SHAPED_ID = re.compile(r"^(?:base|backend|frontend|platform|stack)-[a-z0-9-]+$")


def check_sys_11() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()

    # The third value from _load_manifest is file_to_id, not the stack list.
    # A stack is an entry under the manifest's stacks: key, the same selector
    # MNF-02 uses -- reading the whole entry table instead resolves layer templates
    # as though they were stacks and inflates every count.
    # A stack is one of two kinds of root. Extras and the platform are picked
    # independently of it, and a file reaching a consumer only that way sits
    # in no stack chain at all -- so restricting the corpus to stacks makes
    # the scan of that file vacuous: it is carried by zero chains, nothing
    # can be missing from zero chains, and the reference passes unread.
    stack_roots, opt_in_roots = _roots_by_kind(core_ids, entries)

    chains = {}
    for root in list(stack_roots) + list(opt_in_roots):
        files, _ = _resolve_stack(root, core_ids, entries)
        chains[root] = set(f.replace(os.sep, "/") for f in files)

    # all_template_files() returns absolute paths; the manifest names files
    # repo-relative, and the chains are built from the manifest. Normalise to
    # the manifest's form or nothing matches and every chain looks empty.
    def rel_of(path: str) -> str:
        return os.path.relpath(path, ROOT).replace(os.sep, "/")

    defined_in: dict[str, set[str]] = {}
    for path in all_template_files():
        for section_id, _line in iter_id_declarations(read(path)):
            defined_in.setdefault(section_id, set()).add(rel_of(path))

    references = 0
    cited = set()
    failures: list[str] = []

    for path in all_template_files():
        rel = rel_of(path)
        content = read(path)
        own = set(sid for sid, _line in iter_id_declarations(content))
        for match in sorted(set(_BACKTICKED_TOKEN.findall(content))):
            if match in own:
                continue
            homes = defined_in.get(match)
            if not homes:
                if _LAYER_SHAPED_ID.match(match):
                    failures.append(
                        f"  {rel}: names `{match}`, which no template declares"
                    )
                continue
            references += 1
            cited.add(match)
            carrying = [s for s, f in chains.items() if rel in f]
            missing = [s for s in carrying if not (homes & chains[s])]
            if missing:
                failures.append(
                    f"  {rel}: names `{match}`, declared in "
                    f"{'/'.join(sorted(homes))}, which is absent from "
                    f"{len(missing)} of the {len(carrying)} chains carrying "
                    f"this file ({', '.join(sorted(missing)[:3])}"
                    f"{', ...' if len(missing) > 3 else ''}) — state the "
                    f"substance inline instead of naming a section the "
                    f"reader's context file does not have"
                )

    # An empty result and a check that reached nothing look identical, so the
    # inputs are counted. Zero chains or zero references is a failure.
    # Each kind is asserted on its own. A combined test passes on 17 stacks
    # and no opt-in root, which is the corpus half-empty and reading full.
    if not stack_roots:
        failures.append("  resolved no stack chains — the check reached nothing")
    if not opt_in_roots:
        failures.append(
            "  resolved no opt-in roots — every extra and "
            "platform file went unread, and a reference "
            "dangling only there passes unseen"
        )
    if references == 0:
        failures.append(
            "  found no cross-file prose ID references — either the pattern "
            "stopped matching or every reference was removed; both need "
            "looking at rather than reading as a pass"
        )

    # The count of IDs the check can see is reported on every run, pass or
    # fail. A pattern that narrows takes this number down with it, and
    # without it in the output the narrowing is silent -- which is how a
    # prefix list stayed blind to two thirds of the declared IDs while the
    # check reported green.
    notes = [
        f"  section IDs declared: {len(defined_in)}",
        f"  named in another file's prose: {len(cited)}",
        f"  cross-file references checked: {references}",
        f"  stacks resolved: {len(stack_roots)}",
        f"  opt-in roots resolved: {len(opt_in_roots)}",
    ]

    return failures, notes


# ---------------------------------------------------------------------------
# Chain measurement, shared by the checks that enumerate roots
# ---------------------------------------------------------------------------
# Sizes count decoded characters, not bytes on disk: read() opens in text
# mode, so a CRLF working copy and an LF one measure the same tree the
# same. Nothing gates the size -- `sync_docs.py` writes it into the README's
# model-limits table, which is where a reader meets it.


def _measure_chains() -> tuple[dict[str, int], list[str], list[str]]:
    """Sizes per root, with the two root kinds returned alongside them.

    Both kinds of root: a stack, and an orthogonal template picked
    independently of the stack, which resolves as its own root. Measuring
    stacks alone leaves every opt-in root uncapped, and a fifth of the
    corpus reaches a consumer only that way. The kinds come back separate
    so a caller reports a count per kind rather than their sum.
    """
    core_ids, entries, _ = _load_manifest()
    stacks, opt_in = _roots_by_kind(core_ids, entries)

    sizes: dict[str, int] = {}
    for root in list(stacks) + list(opt_in):
        files, _ = _resolve_stack(root, core_ids, entries)
        sizes[root] = sum(len(read(os.path.join(ROOT, f))) for f in files)
    return sizes, stacks, opt_in


def _core_tier_files(core_ids: list[str], entries: dict[str, Entry]) -> list[str]:
    """The files the resolver seeds into every chain regardless of what
    any template declares."""
    return [entries[cid]["file"] for cid in core_ids if cid in entries]


def _declared_closure(start_file: str) -> set[str]:
    """Files reachable from `start_file` by following DEPENDS ON alone.

    This is the walk README instructs an adopter to perform by hand, so it
    reads the directives out of the files rather than the manifest's
    depends_on -- a reader following the README has only the files.
    """
    seen: set[str] = set()
    pending = [start_file]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        path = os.path.join(ROOT, current)
        if not os.path.isfile(path):
            continue
        seen.add(current)
        pending.extend(depends_on_refs(read(path)))
    return seen


# ---------------------------------------------------------------------------
# SYS-13 - the instructed manual walk reaches what the resolver carries
# ---------------------------------------------------------------------------
# The runtime chapter tells an adopter without Python to build a chain by
# reading the manifest and walking DEPENDS ON. That walk is not the
# resolver: the resolver seeds a core tier unconditionally, and no
# DEPENDS ON directive in the tree declares those files. An adopter
# following an instruction that omits them loses whole rules and gets no
# error, because nothing declares what is absent.
#
# So the instruction and the resolver are compared here rather than
# trusted to agree. The comparison runs in both directions: a file the
# resolver carries and the walk cannot reach is a rule the adopter
# silently loses, and a file the walk reaches that the resolver drops is
# an instruction that overshoots.

MANUAL_WALK_DOC = "docs/architecture/06-runtime-view.md"


def check_sys_13() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    seen = Inspected()
    core_files = seen.count(
        "core-tier files seeded", _core_tier_files(core_ids, entries)
    )
    sizes, stacks, opt_in = _measure_chains()
    seen.count("stacks compared", stacks)
    seen.count("opt-in roots compared", opt_in)
    roots = sorted(sizes)
    failures = list(seen.failures())

    # The instruction is half the pair, so a document that stops naming the
    # core tier has to fail here too -- otherwise this check keeps passing
    # against a document that no longer tells anyone to seed it. The phrase
    # is the prose instruction's; the algorithm block's bare `core:` would
    # pass with the instruction gone.
    if "`core:` list" not in read(os.path.join(ROOT, MANUAL_WALK_DOC)):
        failures.append(
            f"  {MANUAL_WALK_DOC} no longer tells the manual path to load "
            "the manifest's `core:` list, so the walk it instructs misses "
            "every file the resolver seeds"
        )

    missed_without_core = 0
    for root in roots:
        entry = entries.get(root)
        if entry is None:
            failures.append(
                f"  {root}: resolves as a root and has no manifest entry, "
                f"so the walk has no file to start from"
            )
            continue

        chain_files, _ = _resolve_stack(root, core_ids, entries)
        resolved = set(chain_files)
        walk = _declared_closure(entry["file"])
        missed_without_core += len(resolved - walk)
        instructed = walk | set(core_files)

        for path in sorted(resolved - instructed):
            failures.append(
                f"  {root}: the resolver carries {path} and the instructed "
                f"walk cannot reach it — an adopter following the chapter loses "
                f"it with no error, because nothing declares what is absent"
            )
        for path in sorted(instructed - resolved):
            failures.append(
                f"  {root}: the instructed walk reaches {path} and the "
                f"resolver does not carry it — the instruction sends an "
                f"adopter to a file their chain does not include"
            )

    notes = seen.notes()
    notes.append(
        f"  files the DEPENDS ON walk alone would miss, summed over roots: "
        f"{missed_without_core}"
    )
    return failures, notes


# ---------------------------------------------------------------------------
# Test registry
# ---------------------------------------------------------------------------

# SYS-14 -- resolve_chain.py accounts for every argument it is given
#
# The resolver took args[0] and ignored the rest, so a root that does not
# exist passed silently whenever it followed a valid one and the wrong chain
# resolved at exit 0. Roots do not compose -- ADR-035 has a stack and an
# orthogonal template each resolving as their own root -- so more than one
# root is refused rather than concatenated.
#
# Each case asserts the exit status AND a phrase from the message, because a
# program that exits 1 for the wrong reason reads identical to one that
# exits 1 for the right one.

RESOLVE_CASES = [
    (["stack-fixture"], 0, ""),
    (["bogus-root"], 1, "Unknown stack ID"),
    (["stack-fixture", "bogus-root"], 1, "Roots resolve independently"),
    (["stack-fixture", "platform-fixture"], 1, "Roots resolve independently"),
    (["--bogus-flag"], 1, "Unknown flag"),
    # Bare invocation is the usage path, not an error -- same as --help.
    ([], 0, "resolve_chain.py"),
]


def check_sys_14() -> CheckResult:
    seen = Inspected()
    resolver = os.path.join(ROOT, "tools", "resolve_chain.py")
    seen.count("resolve_chain.py argument cases", RESOLVE_CASES)
    failures: list[str] = []

    for args, want_code, want_phrase in RESOLVE_CASES:
        proc = subprocess.run(
            [sys.executable, resolver] + args,
            capture_output=True,
            text=True,
        )
        shown = " ".join(args) or "(no arguments)"
        if proc.returncode != want_code:
            failures.append(
                f"  resolve_chain.py {shown}: exit {proc.returncode}, expected "
                f"{want_code}"
            )
            continue
        if want_phrase and want_phrase not in (proc.stdout + proc.stderr):
            failures.append(
                f"  resolve_chain.py {shown}: exit {want_code} as expected, but the "
                f"message does not carry {want_phrase!r}, so the status may "
                f"be right for the wrong reason"
            )
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-15 -- a stack outside the exempt layers resolves the security tier
# ---------------------------------------------------------------------------
# A stack that serves traffic and carries no security rules is the one shape
# the chain cannot recover from downstream: the consumer's context file is
# silent on input handling, auth and headers, and nothing in the generated
# output says a tier is missing. `stack-htmx` shipped nine files and no
# security template, and every other check passed.
#
# The manifest already classifies every stack by `layer`, so the exemption
# is a property the tree states rather than a list of stack IDs that goes
# stale as stacks are added.

# A library is imported into a caller that owns the trust boundary, and an
# embedded target has no HTTP surface, sessions or TLS to rule on. Both
# would resolve a file whose rules are addressed to somebody else.
SECURITY_EXEMPT_LAYERS = {
    "library": "imported by a caller that owns the trust boundary",
    "embedded": "no HTTP surface, sessions or TLS to rule on",
}

SECURITY_TIER_ID = "base-security"


def check_sys_15() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures: list[str] = []
    seen = Inspected()

    stacks = _stacks(entries)
    seen.count("stacks classified by layer", stacks)
    seen.count("exempt layers named with a reason", SECURITY_EXEMPT_LAYERS)

    # The exemption is read off the manifest, so a stack that declares no
    # layer would be classified by omission. Fail rather than guess: an
    # unclassified stack is the case this check exists to notice.
    governed = []
    for stack in stacks:
        layer = stack.get("layer")
        if not layer:
            failures.append(
                f"  {stack['id']}: no 'layer' in the manifest, so this "
                f"check cannot tell whether the security tier is "
                f"required of it"
            )
            continue
        if layer not in SECURITY_EXEMPT_LAYERS:
            governed.append(stack)

    seen.count("stacks required to resolve the security tier", governed)

    for stack in governed:
        sid = stack["id"]
        _, resolved_ids = _resolve_stack(sid, core_ids, entries)
        if SECURITY_TIER_ID not in resolved_ids:
            failures.append(
                f"  {sid}: layer '{stack['layer']}' resolves no "
                f"{SECURITY_TIER_ID}; only "
                f"{', '.join(sorted(SECURITY_EXEMPT_LAYERS))} are "
                f"exempt, and this layer is not among them"
            )

    return seen.failures() + failures, seen.notes()


# -----------------------------------------------------------------------
# SYS-16 -- a stack category's context tier moves only on purpose
# -----------------------------------------------------------------------
# The README's model-limits table states, per stack category, the
# smallest context window that still holds the largest chain plus the
# interview. sync_docs.py regenerates it, so a change that crosses a tier
# updates the cell and passes sync --check: the crossing arrives as one
# changed word in a generated table, in a diff whose author is reading
# something else.
#
# Chain size is reported rather than capped (ADR-041), and that stands.
# A tier is a different quantity: not what a rule costs the chain, but
# which models can still run the stack at all. Crossing one changes the
# category's stated requirements, and it is rare -- so it is recorded
# where a diff shows it, and raised in the change that causes it.

CONTEXT_TIERS = os.path.join("tests", "smoke", "context-tiers.txt")


def _tier_sort_key(label: str) -> float:
    """Order tier labels by the window they name, not by their text.

    `1M` sorts before `200K` lexically and after it numerically, and the
    exemption is about which window is smallest.
    """
    if label.endswith("M"):
        return float(label[:-1]) * 1000
    return float(label.rstrip("K"))


def _recorded_tiers() -> dict[str, str]:
    """The tier recorded per stack category, as {layer: window label}."""
    out: dict[str, str] = {}
    path = os.path.join(ROOT, CONTEXT_TIERS)
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            layer, window = line.split()
            out[layer] = window
    return out


def check_sys_16() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from sync_docs import (
        CHARS_PER_TOKEN,
        OVERHEAD_TOKENS,
        CONTEXT_WINDOWS,
        _window_label,
    )
    from resolve_chain import load_manifest, resolve_chain, concat_chain

    failures: list[str] = []
    seen = Inspected()

    core_ids, entries, stacks = load_manifest()
    seen.count("stacks measured", stacks)

    largest: dict[str, tuple[int, str]] = {}
    for stack in stacks:
        size = len(concat_chain(resolve_chain(stack["id"], core_ids, entries)))
        layer = stack.get("layer", "unclassified")
        if size > largest.get(layer, (0, None))[0]:
            largest[layer] = (size, stack["id"])

    recorded = _recorded_tiers()
    seen.count("categories measured", largest)
    seen.count("categories recorded", recorded)

    for layer in sorted(largest):
        size, stack_id = largest[layer]
        needed = size / CHARS_PER_TOKEN + OVERHEAD_TOKENS
        window = next((w for w in CONTEXT_WINDOWS if w >= needed), None)

        # A category beyond every window a model sells is a finding
        # about the chain, not a tier to record.
        if window is None:
            failures.append(
                f"  {layer}: {stack_id} needs ~{round(needed / 1000)}K "
                f"tokens, beyond every context window a model sells"
            )
            continue

        now = _window_label(window)
        was = recorded.get(layer)
        if was is None:
            failures.append(
                f"  {layer}: measured at {now} and not recorded in "
                f"{CONTEXT_TIERS}; a category the record does not name "
                f"cannot cross a tier the check would notice"
            )
        elif was != now:
            failures.append(
                f"  {layer}: recorded {was}, now {now} — {stack_id} is "
                f"the largest chain at {size} characters. A crossing "
                f"changes what the category requires of a model. If it is "
                f"intended, record {now} in {CONTEXT_TIERS} in this same "
                f"change so the diff carries it"
            )

    for layer in sorted(set(recorded) - set(largest)):
        failures.append(
            f"  {layer}: recorded in {CONTEXT_TIERS} and measured "
            f"nowhere; a record for a category that no longer exists "
            f"reports nothing on every run"
        )

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-17 -- every registered check names a spec document that exists
# ---------------------------------------------------------------------------

# The templates gate this class of reference for the things they ship: a
# manifest entry pointing at a missing file fails, and so does a DEPENDS ON.
# The suite's own references had no equivalent, so the registry could name a
# document nobody wrote and the run stayed green. The information needed to
# catch it was already in the registry, beside the function the runner does
# resolve.

#
# The reverse direction holds too. A document no check cites and no runner
# names is a procedure nothing runs, and an index row naming no document
# sends a reader to nothing; either survived a repointed registry entry with
# every gate green. A spec declaring `automatable: manual` has no runner by
# design and is exempt from the first.

SPEC_ID = re.compile(r"SAIT-[A-Z0-9]+-[A-Z0-9]+-\d+-\d+[A-Z]")
MANUAL_SPEC = re.compile(r"^automatable:\s*manual\s*$", re.M)


def _runner_text() -> str:
    """The text of the modules at tests/ and every suite's run.py but smoke's.

    The smoke registry is read as data; its runner's prose names specs it
    does not run, so it is not searched as text.
    """
    tests = os.path.join(ROOT, "tests")
    paths: list[str] = []
    for name in sorted(os.listdir(tests)):
        path = os.path.join(tests, name)
        if name.endswith(".py"):
            paths.append(path)
        elif name != "smoke" and os.path.isfile(os.path.join(path, "run.py")):
            paths.append(os.path.join(path, "run.py"))
    texts: list[str] = []
    for path in paths:
        with io.open(path, encoding="utf-8") as f:
            texts.append(f.read())
    return "\n".join(texts)


def check_sys_17() -> CheckResult:
    # Imported here: the registry imports this module.
    from .registry import CHECKS

    failures: list[str] = []
    seen = Inspected()

    spec_dir = os.path.join(ROOT, "docs", "tests", "specs")
    on_disk: dict[str, str] = {}
    for name in os.listdir(spec_dir):
        if name.endswith(".md"):
            with io.open(os.path.join(spec_dir, name), encoding="utf-8") as handle:
                on_disk[os.path.splitext(name)[0]] = handle.read()

    with io.open(
        os.path.join(ROOT, "docs", "tests", "index.md"), encoding="utf-8"
    ) as handle:
        index = handle.read()

    seen.count("checks registered", CHECKS)
    seen.count("spec documents on disk", on_disk)
    indexed = set(SPEC_ID.findall(index))
    seen.count("specs the index names", indexed)

    cited = {check.get("spec") for check in CHECKS}
    runners = _runner_text()
    for spec in sorted(on_disk):
        if spec not in index:
            failures.append(f"  {spec}: on disk with no row in docs/tests/index.md")
        if spec in cited or spec in runners:
            continue
        if MANUAL_SPEC.search(on_disk[spec]):
            continue
        failures.append(
            f"  {spec}: no registered check cites it, no runner in tests/ "
            f"names it, and it does not declare automatable: manual -- a "
            f"procedure nothing runs"
        )
    for spec in sorted(indexed - set(on_disk)):
        failures.append(
            f"  {spec}: named in docs/tests/index.md with no "
            f"document under docs/tests/specs/"
        )

    for check in CHECKS:
        spec = check.get("spec")
        if not spec:
            failures.append(f"  {check['id']}: registered with no spec field")
            continue
        if spec not in on_disk:
            failures.append(
                f"  {check['id']}: spec {spec} names no document under "
                f"docs/tests/specs/ -- a registry entry can cite a document "
                f"nobody wrote and the run stays green"
            )
        if spec not in index:
            failures.append(
                f"  {check['id']}: spec {spec} has no row in "
                f"docs/tests/index.md, which is where a reader goes for the "
                f"list of what the suite checks"
            )

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-18 -- a stack outside the constrained categories resolves the gate tier
# ---------------------------------------------------------------------------

# `base-quality-gates` answers how a gate is retrofitted, ratcheted and
# retired, which is as relevant to an eslint migration as to a ruff one.
# Membership in it used to be whatever three `depends_on` declarations
# produced: a Node library sat outside a family both its library-layer
# siblings carry, and no check had an opinion in either direction.
#
# The line is the recorded context tier, not the language. A category whose
# largest chain sits at the smallest tier a stack category is recorded at
# cannot take the file without moving what the category requires of a
# model, so it is exempt and the tier file is where the reason lives. The
# exemption is asserted against that file rather than trusted, so a
# category that later moves off the tier stops being exempt by omission.
# The exempt categories are a fork's, since only a fork carries stacks; it
# names them in fork_checks.py.

QUALITY_GATES_EXEMPT_LAYERS: dict[str, str] = {}

QUALITY_GATES_ID = "base-quality-gates"


def check_sys_18() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures: list[str] = []
    seen = Inspected()

    recorded = _recorded_tiers()
    constrained = min(recorded.values(), key=_tier_sort_key) if recorded else None
    seen.count("categories recorded", recorded)

    # Zero exemptions is a real answer: a tree whose only stack is the
    # fixture has no constrained category to exempt.
    seen.count(
        "exempt layers named with a reason", QUALITY_GATES_EXEMPT_LAYERS, floor=0
    )

    # An exemption whose stated reason has expired is worse than none: it
    # reads as a decision and behaves as an omission.
    for layer in sorted(QUALITY_GATES_EXEMPT_LAYERS):
        was = recorded.get(layer)
        if was is None:
            failures.append(
                f"  {layer}: exempt from {QUALITY_GATES_ID} for its "
                f"context tier, and no tier is recorded for it in "
                f"{CONTEXT_TIERS}"
            )
        elif was != constrained:
            failures.append(
                f"  {layer}: exempt from {QUALITY_GATES_ID} because it "
                f"sits at the most constrained tier, and it is recorded "
                f"at {was} while the most constrained is {constrained}. "
                f"The reason has expired -- either the exemption goes or "
                f"the reason changes"
            )

    stacks = _stacks(entries)
    seen.count("stacks classified by layer", stacks)

    governed = []
    for stack in stacks:
        stack_layer = stack.get("layer")
        if not stack_layer:
            failures.append(
                f"  {stack['id']}: no 'layer' in the manifest, so this "
                f"check cannot tell whether {QUALITY_GATES_ID} is "
                f"required of it"
            )
            continue
        if stack_layer not in QUALITY_GATES_EXEMPT_LAYERS:
            governed.append(stack)

    seen.count("stacks required to resolve the gate tier", governed)

    for stack in governed:
        sid = stack["id"]
        _, resolved_ids = _resolve_stack(sid, core_ids, entries)
        if QUALITY_GATES_ID not in resolved_ids:
            failures.append(
                f"  {sid}: layer '{stack['layer']}' resolves no "
                f"{QUALITY_GATES_ID}; only "
                f"{', '.join(sorted(QUALITY_GATES_EXEMPT_LAYERS))} are "
                f"exempt, and this layer is not among them"
            )

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-19 -- resolve_chain.py names a missing dependency and a dependency cycle
# ---------------------------------------------------------------------------

# A fork's stacks depend on upstream IDs the fork does not control, so a
# broken chain has to say what broke. The resolver used to drop a missing
# ID and resolve a shorter chain at exit 0, and to recurse on a cycle until
# Python stopped it with no ID in the message.
#
# Each case resolves a root of a planted manifest through the resolver's own
# entry point, so the exit status and the printed message are the CLI's.
# The valid root is the control: it proves a failure comes from the broken
# entry and not from the planted manifest or the way it is loaded.

BROKEN_MANIFEST = """core: [base-a]

base:
  - id: base-a
    file: templates/core/quality.md
  - id: base-b
    file: templates/core/git.md
    depends_on: [base-c]
  - id: base-c
    file: templates/core/docs.md
    depends_on: [base-b]

stacks:
  - id: stack-valid
    file: templates/fixture/stack.md
    depends_on: [base-a]
  - id: stack-missing
    file: templates/fixture/stack.md
    depends_on: [base-a, base-nowhere]
  - id: stack-cycle
    file: templates/fixture/stack.md
    depends_on: [base-b]
"""


def core_fault(depends_on: str) -> str:
    """A manifest whose one core entry depends on `depends_on`.

    A fault under the core tier breaks every root, so each is planted in a
    manifest of its own, and the valid stack is the root asked for.
    """
    return (
        """core: [base-a]

base:
  - id: base-a
    file: templates/core/quality.md
    depends_on: [%s]

stacks:
  - id: stack-valid
    file: templates/fixture/stack.md
    depends_on: [base-a]
"""
        % depends_on
    )


# The core tier's entries are seeded before any root is walked, so their own
# dependencies are a separate path to each fault, and each gets a case.
MANIFESTS = {
    "stacks": BROKEN_MANIFEST,
    "core-missing": core_fault("base-nowhere"),
    "core-self": core_fault("base-a"),
    "core-through-stack": core_fault("stack-valid"),
}

# A resolve case: the manifest's name, the root, the exit status owed and a
# phrase the output owes, optionally followed by one it MUST NOT carry.
ResolveCase = tuple[str, str, int, str] | tuple[str, str, int, str, str]

BROKEN_CASES: list[ResolveCase] = [
    ("stacks", "stack-valid", 0, "templates/fixture/stack.md"),
    (
        "stacks",
        "stack-missing",
        1,
        "Missing dependency: stack-missing depends on base-nowhere",
    ),
    ("stacks", "stack-cycle", 1, "Dependency cycle: base-b -> base-c -> base-b"),
    (
        "core-missing",
        "stack-valid",
        1,
        "Missing dependency: base-a depends on base-nowhere",
    ),
    ("core-self", "stack-valid", 1, "Dependency cycle: base-a -> base-a"),
    (
        "core-through-stack",
        "stack-valid",
        1,
        "Dependency cycle: base-a -> stack-valid -> base-a",
    ),
]

RESOLVE_WITH = (
    "import sys; sys.path.insert(0, sys.argv[1]); import resolve_chain; "
    "resolve_chain.MANIFEST = sys.argv[2]; "
    "sys.argv = ['resolve_chain.py', sys.argv[3]]; "
    "resolve_chain.main()"
)


def _resolve_cases(
    manifests: Mapping[str, str], cases: Sequence[ResolveCase]
) -> list[str]:
    """Resolve each case's root in its planted manifest; return the misses.

    A case is (manifest name, root, owed exit status, phrase the output owes),
    optionally followed by a phrase the output MUST NOT carry.
    """
    import tempfile

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as scratch:
        for name, text in manifests.items():
            with io.open(
                os.path.join(scratch, name + ".yaml"),
                "w",
                encoding="utf-8",
                newline="\n",
            ) as handle:
                handle.write(text)

        for name, root, want_code, want_phrase, *absent in cases:
            manifest = os.path.join(scratch, name + ".yaml")
            case = f"{root} in {name}"
            proc = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    RESOLVE_WITH,
                    os.path.join(ROOT, "tools"),
                    manifest,
                    root,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            said = proc.stdout + proc.stderr
            if proc.returncode != want_code:
                failures.append(
                    f"  {case}: exit {proc.returncode}, expected {want_code}: "
                    f"{said.strip()[-200:]}"
                )
            elif want_phrase not in said:
                failures.append(
                    f"  {case}: exit {want_code} as expected, but the message "
                    f"does not carry {want_phrase!r}, so the status may be "
                    f"right for the wrong reason"
                )
            elif absent and absent[0] in said:
                failures.append(
                    f"  {case}: the output carries {absent[0]!r}, which the "
                    f"case owes it not to"
                )
            elif "Traceback" in said:
                failures.append(
                    f"  {case}: the message is right but arrives inside a "
                    f"traceback, which a fork's maintainer reads as a crash"
                )
    return failures


def check_sys_19() -> CheckResult:
    seen = Inspected()
    seen.count("broken-manifest cases", BROKEN_CASES)
    failures = _resolve_cases(MANIFESTS, BROKEN_CASES)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-21 -- a fork's own key and its core-tier additions resolve
# ---------------------------------------------------------------------------

# A fork MUST NOT edit the keys upstream owns, so its templates live under a
# key of its own and its additions to every chain under `fork_core`. The
# resolver used to read five fixed keys, which left a fork nowhere legal to
# put a template once the split moved it out of upstream.
#
# The planted manifest uses a key no tool names. Its stack depends on an
# entry there, and `fork_core` adds a second; each case asserts one of them
# reaches the chain. The upstream file is the control that the chain
# resolved at all.
#
# Inclusion alone passes a resolver that returns every entry it can see, so
# a third entry under the fork's key, which nothing names, MUST stay out,
# and the whole chain is asserted in its order.

FORK_MANIFEST = """core: [base-a]
fork_core: [fork-readme]

base:
  - id: base-a
    file: templates/core/quality.md

acme:
  - id: fork-readme
    file: templates/core/docs.md
  - id: fork-lib
    file: templates/core/git.md
  - id: fork-unused
    file: templates/core/testing.md

stacks:
  - id: stack-fork
    file: templates/fixture/stack.md
    depends_on: [fork-lib]
"""

# A `fork_core` entry depending on an ID outside the core tier: the tier is
# seeded and never walked, so the dependency would vanish from every chain.
FORK_OUTSIDE_MANIFEST = FORK_MANIFEST.replace(
    "  - id: fork-readme\n    file: templates/core/docs.md\n",
    "  - id: fork-readme\n    file: templates/core/docs.md\n"
    "    depends_on: [fork-lib]\n",
)

FORK_CHAIN = "\n".join(
    [
        "templates/core/quality.md",
        "templates/core/docs.md",
        "templates/core/git.md",
        "templates/fixture/stack.md",
    ]
)

FORK_CASES: list[ResolveCase] = [
    ("fork", "stack-fork", 0, "templates/core/quality.md"),
    ("fork", "stack-fork", 0, "templates/core/git.md"),
    ("fork", "stack-fork", 0, "templates/core/docs.md"),
    ("fork", "stack-fork", 0, FORK_CHAIN, "templates/core/testing.md"),
    (
        "fork-outside",
        "stack-fork",
        1,
        "Core-tier entry fork-readme depends on fork-lib, which is outside the "
        "core tier",
    ),
]


def check_sys_21() -> CheckResult:
    seen = Inspected()
    seen.count("fork-manifest cases", FORK_CASES)
    failures = _resolve_cases(
        {"fork": FORK_MANIFEST, "fork-outside": FORK_OUTSIDE_MANIFEST}, FORK_CASES
    )
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-20 -- a fork leaves upstream's manifest keys as it last merged them
# ---------------------------------------------------------------------------

# A fork appends under `stacks:`, `platform:` and keys of its own, and never
# edits the keys upstream owns. An edit there is what turns the fork's next
# upstream merge into a conflict, and nothing else notices it until then.
#
# In a fork, SAIT_UPSTREAM_REF names a ref holding upstream's history, and
# the baseline is the revision the fork last merged: the merge base of HEAD
# and that ref. Upstream sets no ref, so the manifest is compared with
# itself and the check passes trivially. Because that run reads no edit,
# planted manifest pairs exercise the failing path on every run.

UPSTREAM_KEYS = ("core", "base", "backend", "frontend")
UPSTREAM_REF_ENV = "SAIT_UPSTREAM_REF"


def upstream_key_edits(was: Manifest, now: Manifest) -> list[str]:
    """Each edit to an upstream-owned manifest key, as one finding."""
    found: list[str] = []
    for key in UPSTREAM_KEYS:
        before, after = was.get(key) or [], now.get(key) or []
        if key == "core":
            if before != after:
                found.append(f"core: {before} became {after}")
            continue
        old = {e["id"]: e for e in before}
        new = {e["id"]: e for e in after}
        for eid in sorted(set(old) - set(new)):
            found.append(f"{key}: {eid} removed")
        for eid in sorted(set(new) - set(old)):
            found.append(f"{key}: {eid} added")
        for eid in sorted(set(old) & set(new)):
            fields = sorted(
                k
                for k in set(old[eid]) | set(new[eid])
                if old[eid].get(k) != new[eid].get(k)
            )
            if fields:
                found.append(f"{key}: {eid} changed ({', '.join(fields)})")
    return found


OWNED_BASE = """core: [base-a]
base:
  - id: base-a
    file: templates/core/quality.md
backend:
  - id: backend-a
    file: templates/backend/http.md
    depends_on: [base-a]
frontend: []
stacks:
  - id: stack-a
    file: templates/stack/a.md
    depends_on: [backend-a]
"""

# Each case is a fork's manifest against OWNED_BASE, and the findings the
# check owes it. The appends are the control: a check that flagged them
# would fail every fork that did what the contract allows.
OWNERSHIP_CASES = [
    (
        "a stack and a platform appended, and a key of the fork's own",
        OWNED_BASE
        + """  - id: stack-b
    file: templates/stack/b.md
platform:
  - id: platform-b
    file: templates/platform/b.md
fork:
  - id: fork-note
""",
        [],
    ),
    (
        "the core tier edited",
        OWNED_BASE.replace("core: [base-a]", "core: [base-a, backend-a]"),
        ["core: ['base-a'] became ['base-a', 'backend-a']"],
    ),
    (
        "an upstream entry changed",
        OWNED_BASE.replace("depends_on: [base-a]", "depends_on: []"),
        ["backend: backend-a changed (depends_on)"],
    ),
    (
        "an entry added under an upstream key",
        OWNED_BASE.replace(
            "frontend: []",
            """frontend:
  - id: frontend-b
    file: templates/frontend/b.md""",
        ),
        ["frontend: frontend-b added"],
    ),
    (
        "an upstream entry removed",
        OWNED_BASE.replace(
            """  - id: backend-a
    file: templates/backend/http.md
    depends_on: [base-a]
""",
            "",
        ),
        ["backend: backend-a removed"],
    ),
]


def _git(repo: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", repo] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def fork_baseline(
    repo: str, ref: str
) -> tuple[None, None, str] | tuple[str, str, None]:
    """The manifest the fork in `repo` last merged from `ref`.

    Returns (text, basis, refusal): the manifest text and a line naming
    where it came from, or a refusal naming why no baseline exists.
    """

    # A ref that does not resolve and a ref with no shared history are
    # different faults with different remedies -- fetch upstream, or point
    # at the right one -- so each is named as itself.
    resolved = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if resolved.returncode != 0:
        return (
            None,
            None,
            (
                f"{UPSTREAM_REF_ENV}={ref} names no commit in this repository, "
                f"so there is no upstream to compare with; fetch it first"
            ),
        )
    merged = _git(repo, "merge-base", "HEAD", ref)
    if merged.returncode != 0:
        return (
            None,
            None,
            (
                f"{UPSTREAM_REF_ENV}={ref} shares no history with HEAD, so the "
                f"revision the fork last merged is unknown"
            ),
        )
    revision = merged.stdout.strip()
    shown = _git(repo, "show", f"{revision}:templates/manifest.yaml")
    if shown.returncode != 0:
        return (
            None,
            None,
            (
                f"the manifest at {revision[:12]} could not be "
                f"read: {shown.stderr.strip()}"
            ),
        )
    return (
        shown.stdout,
        (f"  baseline: the merge base {revision[:12]} of HEAD and {ref}"),
        None,
    )


# The git path, planted. Upstream sets no ref, so its own run never reaches
# that path, and a fork's run reaches it only in the passing direction. Each
# case is (label, the ref the fork names, the findings or the refusal owed),
# run in order against one throwaway repository whose `upstream` branch is
# OWNED_BASE and whose HEAD is the fork.
GIT_CASES: list[tuple[str, str, list[str] | str]] = [
    ("a fork that only appended since its last merge", "upstream", []),
    (
        "a fork that edited the core tier since its last merge",
        "upstream",
        ["core: ['base-a'] became ['base-a', 'backend-a']"],
    ),
    ("a ref that names no commit", "upstream/missing", "names no commit"),
    ("a ref with no history in common", "unrelated", "shares no history"),
]


def _git_cases() -> list[str]:
    """Run GIT_CASES; return a failure line per case that missed."""
    import tempfile

    manifest = os.path.join("templates", "manifest.yaml")
    edits = {
        GIT_CASES[0][0]: OWNED_BASE + "  - id: stack-b\n"
        "    file: templates/stack/b.md\n",
        GIT_CASES[1][0]: OWNED_BASE.replace(
            "core: [base-a]", "core: [base-a, backend-a]"
        )
        + "  - id: stack-b\n    file: templates/stack/b.md\n",
    }
    failures: list[str] = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as repo:

        def commit(text: str, message: str) -> None:
            # Each commit MUST change the manifest, or the case after it
            # reads the state before it and passes for the wrong reason.
            path = os.path.join(repo, manifest)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            _git(repo, "add", manifest)
            done = _git(repo, "commit", "-q", "-m", message)
            if done.returncode != 0:
                raise RuntimeError(
                    f"planted commit {message!r} failed: {done.stderr.strip()}"
                )

        _git(repo, "init", "-q")
        for key, value in (
            ("core.autocrlf", "false"),
            ("user.name", "smoke"),
            ("user.email", "smoke@localhost"),
        ):
            _git(repo, "config", key, value)
        commit(OWNED_BASE, "upstream")
        _git(repo, "branch", "upstream")
        _git(repo, "checkout", "-q", "--orphan", "unrelated")
        commit(OWNED_BASE, "unrelated root")
        _git(repo, "checkout", "-q", "upstream")
        _git(repo, "checkout", "-q", "-b", "fork")

        for label, ref, owed in GIT_CASES:
            if label in edits:
                commit(edits[label], label)
            was, _, refused = fork_baseline(repo, ref)
            if isinstance(owed, str):
                if not refused or owed not in refused:
                    failures.append(
                        f"  planted git, {label}: refused {refused!r}, owed {owed!r}"
                    )
                continue
            if refused or was is None:
                failures.append(f"  planted git, {label}: refused {refused!r}")
                continue
            with io.open(os.path.join(repo, manifest), encoding="utf-8") as f:
                now = f.read()
            got = upstream_key_edits(yaml.safe_load(was), yaml.safe_load(now))
            if got != owed:
                failures.append(f"  planted git, {label}: found {got}, owed {owed}")
    return failures


def check_sys_20() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    seen = Inspected()
    failures: list[str] = []

    seen.count("planted fork manifests", OWNERSHIP_CASES)
    base = yaml.safe_load(OWNED_BASE)
    for label, text, want in OWNERSHIP_CASES:
        got = upstream_key_edits(base, yaml.safe_load(text))
        if got != want:
            failures.append(f"  planted, {label}: found {got}, owed {want}")

    seen.count("planted fork repositories", GIT_CASES)
    failures += _git_cases()

    manifest = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest, encoding="utf-8") as handle:
        now_text = handle.read()

    ref = os.environ.get(UPSTREAM_REF_ENV)
    if ref:
        baseline = fork_baseline(ROOT, ref)
        if baseline[2] is not None:
            failures.append(f"  {baseline[2]}")
            return seen.failures() + failures, seen.notes()
        was_text, basis, _ = baseline
    else:
        was_text = now_text
        basis = (
            f"  baseline: {UPSTREAM_REF_ENV} is unset, so this is "
            f"upstream and the manifest is compared with itself"
        )

    was, now = yaml.safe_load(was_text), yaml.safe_load(now_text)
    seen.count("upstream keys compared", [k for k in UPSTREAM_KEYS if k in was])
    for finding in upstream_key_edits(was, now):
        failures.append(
            f"  {finding}: a fork appends under stacks:, platform: and its "
            f"own keys, and leaves upstream's as it last merged them"
        )

    return seen.failures() + failures, seen.notes() + [basis]


# ---------------------------------------------------------------------------
# SYS-22 -- a deprecation names a live replacement
# ---------------------------------------------------------------------------

# From 3.0 a template is never removed inside a major; it is deprecated, its
# manifest entry naming the template that replaces it. A name that resolves
# to nothing sends every project reading the field nowhere, and a name that
# is itself deprecated sends it to a second retirement. Upstream deprecates
# nothing yet, so planted manifests exercise both failing paths on every
# run.

DEPRECATION_CASES = [
    (
        "a live replacement",
        """base:
  - {id: base-old, file: a.md, deprecated: base-new}
  - {id: base-new, file: b.md}
""",
        [],
    ),
    (
        "a replacement that does not exist",
        """base:
  - {id: base-old, file: a.md, deprecated: base-gone}
""",
        ["base-old names base-gone, which no entry carries"],
    ),
    (
        "a replacement that is deprecated too",
        """base:
  - {id: base-old, file: a.md, deprecated: base-mid}
  - {id: base-mid, file: b.md, deprecated: base-new}
  - {id: base-new, file: c.md}
""",
        ["base-old names base-mid, which is deprecated too"],
    ),
    (
        "a field that names no ID",
        """base:
  - {id: base-old, file: a.md, deprecated: true}
""",
        ["base-old carries deprecated: True, which names no ID"],
    ),
]


def deprecation_findings(manifest: Manifest) -> list[str]:
    """Each deprecation that names no live replacement, as one finding."""
    entries = [
        e
        for v in manifest.values()
        if isinstance(v, list)
        for e in v
        if isinstance(e, dict) and "id" in e
    ]
    by_id = {e["id"]: e for e in entries}
    found: list[str] = []
    for entry in entries:
        if "deprecated" not in entry:
            continue
        target = entry["deprecated"]
        if not isinstance(target, str):
            found.append(
                f"{entry['id']} carries deprecated: {target}, which names no ID"
            )
        elif target not in by_id:
            found.append(f"{entry['id']} names {target}, which no entry carries")
        elif "deprecated" in by_id[target]:
            found.append(f"{entry['id']} names {target}, which is deprecated too")
    return found


def check_sys_22() -> CheckResult:
    if not HAS_YAML:
        return [MISSING_YAML]

    seen = Inspected()
    failures: list[str] = []
    seen.count("planted manifests", DEPRECATION_CASES)
    for label, text, want in DEPRECATION_CASES:
        got = deprecation_findings(yaml.safe_load(text))
        if got != want:
            failures.append(f"  planted, {label}: found {got}, owed {want}")

    manifest = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    marked = [
        e
        for v in data.values()
        if isinstance(v, list)
        for e in v
        if isinstance(e, dict) and "deprecated" in e
    ]
    seen.count("deprecated entries in the manifest", marked, floor=0)
    for finding in deprecation_findings(data):
        failures.append(f"  {finding}")
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-24 -- a new section ID never splits a frozen section
# ---------------------------------------------------------------------------

# A section runs from its tags to the next `[ID:]`, so an ID inserted inside
# a shipped section shrinks it, and a fork's OVERRIDE of that section stops
# covering the lines split off -- silently, since every ID still resolves.
# A minor adds a section ID only on new content (spec, chapter 8.7).
#
# The baseline is the newest release tag of the frozen major reachable from
# HEAD. Each line a frozen section held there -- a heading, a rule, a line
# of an example -- that the tree still carries must still sit in that
# section. A line deleted or reworded is prose, which is free, so only one
# present on both sides is compared. The fixture is test input, outside the
# frozen surface, and is not compared. Until the first release of the major
# is tagged nothing is frozen, so planted texts and planted repositories
# exercise the failing path on every run.

FROZEN_MAJOR = 3
FROZEN_TAG = re.compile(rf"v{FROZEN_MAJOR}\.\d+\.\d+")
HEADING_LINE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
DIRECTIVE_LINE = re.compile(r"^\s*\[[A-Z][A-Z ]*:")
FENCE_RUN = re.compile(r"^\s*(`{3,}|~{3,})")
CONTENT = re.compile(r"\w")


def line_owners(text: str) -> dict[str, list[str | None]]:
    """Map each content line's text to the IDs of the sections holding it.

    A content line is any line with a letter or digit other than a
    directive or a fence delimiter. A heading followed by nothing but blank
    and directive lines before an `[ID:]` belongs to that ID's section; a
    line above the first ID belongs to none.
    """
    declared = {n: sid for sid, n in iter_id_declarations(text)}
    owners: dict[str, list[str | None]] = {}
    current: str | None = None
    pending: str | None = None
    fence: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        if number in declared:
            current = declared[number]
            if pending:
                owners[pending][-1] = current
            pending = None
            continue

        # A `#` line inside a fence is a shell comment, not a heading.
        # The delimiters repeat in every section, so they say nothing about
        # which one a line belongs to.
        run = FENCE_RUN.match(line)
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            pending = None
            continue
        if fence is not None:
            if CONTENT.search(line):
                owners.setdefault(line.strip(), []).append(current)
            continue

        if DIRECTIVE_LINE.match(line) or not line.strip():
            continue
        heading = HEADING_LINE.match(line)
        key = heading.group(1) if heading else line.strip()
        if CONTENT.search(key):
            owners.setdefault(key, []).append(current)
        pending = key if heading else None
    return owners


def section_splits(was: str, now: str) -> list[str]:
    """Each section that lost lines to another, as one finding.

    A finding names the two sections, the count of lines moved and the
    first of them, so one inserted ID reads as one split.
    """
    before, after = line_owners(was), line_owners(now)
    moved: dict[tuple[str, str], list[str]] = {}
    for line, held in before.items():
        if line not in after:
            continue

        # Counted, not compared in order: a line repeated across sections
        # is a split only when one section loses it while another gains it.
        # Only a section that held the line can lose it, so the unowned
        # entries are left out of both sides, which subtracting them would
        # not change.
        lost = Counter(o for o in held if o) - Counter(o for o in after[line] if o)
        gained = Counter(after[line]) - Counter(held)
        if not gained:
            continue
        taker = ", ".join(sorted(str(o) for o in gained))
        for owner in sorted(lost):
            moved.setdefault((owner, taker), []).append(line)
    found: list[str] = []
    for (owner, taker), lines in moved.items():
        first = lines[0] if len(lines[0]) <= 60 else lines[0][:57] + "..."
        found.append(f"{len(lines)} line(s) left {owner} for {taker}, from '{first}'")
    return found


SPLIT_BASE = """# Base

[ID: base-a]

## Rules

- Rule one

## Checks

- Check one
"""

# Each case is a later text of SPLIT_BASE and the findings it owes. The
# append, the rewording and the fence are the controls: a check that flagged
# them would fail every minor that does what chapter 8.7 allows. The split
# between two rules is the one a heading-only comparison passed.
SPLIT_CASES = [
    (
        "a section appended after the last frozen line",
        SPLIT_BASE + "\n## Extra\n\n[ID: base-b]\n\n- New rule\n",
        [],
    ),
    (
        "a heading reworded and a rule added",
        SPLIT_BASE.replace("## Checks", "## Gates") + "- Rule two\n",
        [],
    ),
    (
        "a heading-like line inside a fence after a new ID",
        SPLIT_BASE + "\n## Extra\n\n[ID: base-b]\n\n```bash\n# Checks\n```\n",
        [],
    ),
    (
        "an ID inserted above a frozen heading",
        SPLIT_BASE.replace("## Checks", "## Checks\n\n[ID: base-b]"),
        ["2 line(s) left base-a for base-b, from 'Checks'"],
    ),
    (
        "an ID inserted between a frozen heading and its rule",
        SPLIT_BASE.replace("- Check one\n", "## Late\n\n[ID: base-b]\n\n- Check one\n"),
        ["1 line(s) left base-a for base-b, from '- Check one'"],
    ),
    (
        "a frozen heading moved under a later ID",
        SPLIT_BASE.replace("## Checks\n\n- Check one\n", "")
        + "\n## Extra\n\n[ID: base-b]\n\n## Checks\n\n- Check one\n",
        ["2 line(s) left base-a for base-b, from 'Checks'"],
    ),
]

# The text the planted repositories commit over SPLIT_BASE: a split.
SPLIT_TEXT = SPLIT_CASES[3][1]


def frozen_baseline(repo: str) -> tuple[str | None, str | None]:
    """The newest frozen release tag reachable from HEAD in `repo`.

    Returns (tag, refusal). Both are None when no release of the frozen
    major is reachable yet, so nothing is frozen.
    """

    # A shallow or tagless clone reads as "nothing released", which would
    # pass every split, so each is refused rather than read as no baseline.
    shallow = _git(repo, "rev-parse", "--is-shallow-repository")
    if shallow.stdout.strip() == "true":
        return None, (
            "the clone is shallow, so its release tags may not "
            "be reachable; fetch the full history"
        )
    listed = _git(repo, "tag", "--merged", "HEAD", "--sort=-v:refname")
    tags = listed.stdout.split()
    if listed.returncode != 0 or not tags:
        return None, (
            "no release tag is reachable from HEAD, so the tags "
            "were not fetched; fetch them"
        )
    frozen = [t for t in tags if FROZEN_TAG.fullmatch(t)]
    return (frozen[0] if frozen else None), None


def frozen_splits(
    repo: str, files: Iterable[str]
) -> tuple[list[str], None, str, int] | tuple[list[str], str, None, int]:
    """Compare `files` in the working tree of `repo` with the baseline.

    Returns (findings, basis, refusal, compared): each split as
    "path: finding", a line naming the baseline, a refusal naming why none
    exists, and the count of files present on both sides.
    """
    tag, refused = frozen_baseline(repo)
    if refused:
        return [], None, refused, 0
    if tag is None:
        return (
            [],
            (
                f"  baseline: no v{FROZEN_MAJOR}.x release is reachable "
                f"from HEAD, so no section is frozen yet"
            ),
            None,
            0,
        )
    found: list[str] = []
    compared = 0
    for rel in files:
        shown = _git(repo, "show", f"{tag}:{rel}")
        if shown.returncode != 0:
            continue
        compared += 1
        with io.open(os.path.join(repo, rel), encoding="utf-8") as handle:
            now = handle.read()
        found += [f"{rel}: {f}" for f in section_splits(shown.stdout, now)]
    return found, f"  baseline: the release tag {tag}", None, compared


# The tag path, planted. Each case is (label, the tags on the base commit,
# the findings or the refusal owed), run against a throwaway repository
# whose base commit holds SPLIT_BASE and whose HEAD holds SPLIT_TEXT.
TAG_CASES: list[tuple[str, list[str], list[str] | str]] = [
    (
        "a frozen release behind HEAD",
        ["v2.9.0", f"v{FROZEN_MAJOR}.0.0"],
        SPLIT_CASES[3][2],
    ),
    ("only an earlier major's release", ["v2.9.0"], []),
    ("no tag at all", [], "were not fetched"),
]


def frozen_files(files: Iterable[str], entries: Iterable[Entry]) -> list[str]:
    """`files` less those a fixture entry holds, which are test input."""
    exempt = {e["file"] for e in entries if is_fixture(e)}
    return [f for f in files if f not in exempt]


# The exemption, planted: a fixture entry's file is dropped and a template's
# kept, so an exemption that dropped nothing or everything fails here.
FIXTURE_ENTRIES: list[Entry] = [
    {"id": "base-a", "file": "templates/core/a.md"},
    {"id": "stack-fixture", "file": "templates/stack/fixture.md", "fixture": True},
]


def _tag_cases() -> list[str]:
    """Run TAG_CASES; return a failure line per case that missed."""
    import tempfile

    rel = "templates/core/a.md"
    failures: list[str] = []
    for label, tags, owed in TAG_CASES:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as repo:
            _git(repo, "init", "-q")
            for key, value in (
                ("core.autocrlf", "false"),
                ("user.name", "smoke"),
                ("user.email", "smoke@localhost"),
            ):
                _git(repo, "config", key, value)
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path))
            for text, message in ((SPLIT_BASE, "base"), (SPLIT_TEXT, "split")):
                with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
                _git(repo, "add", rel)
                done = _git(repo, "commit", "-q", "-m", message)
                if done.returncode != 0:
                    raise RuntimeError(
                        f"planted commit {message!r} failed: {done.stderr.strip()}"
                    )
                if message == "base":
                    for tag in tags:
                        _git(repo, "tag", tag)

            found, _, refused, _ = frozen_splits(repo, [rel])
            if isinstance(owed, str):
                if not refused or owed not in refused:
                    failures.append(
                        f"  planted tags, {label}: refused {refused!r}, owed {owed!r}"
                    )
            elif refused or found != [f"{rel}: {f}" for f in owed]:
                failures.append(
                    f"  planted tags, {label}: found {found}, "
                    f"refused {refused!r}, owed {owed}"
                )
    return failures


def check_sys_24() -> CheckResult:
    seen = Inspected()
    failures: list[str] = []

    seen.count("planted texts", SPLIT_CASES)
    for label, text, want in SPLIT_CASES:
        got = section_splits(SPLIT_BASE, text)
        if got != want:
            failures.append(f"  planted, {label}: found {got}, owed {want}")

    seen.count("planted repositories", TAG_CASES)
    failures += _tag_cases()

    planted = ["templates/core/a.md", "templates/stack/fixture.md"]
    kept = frozen_files(planted, FIXTURE_ENTRIES)
    if kept != planted[:1]:
        failures.append(f"  planted fixture exemption: kept {kept}, owed {planted[:1]}")

    if not HAS_YAML:
        return seen.failures() + failures + [MISSING_YAML], seen.notes()
    _, entries, _ = _load_manifest()
    files = template_files()
    frozen = frozen_files(files, entries.values())
    seen.count("fixture templates exempt", len(files) - len(frozen), floor=0)

    splits = frozen_splits(ROOT, frozen)
    if splits[2] is not None:
        failures.append(f"  {splits[2]}")
        return seen.failures() + failures, seen.notes()
    found, basis, _, compared = splits
    seen.count("templates compared with the baseline", compared, floor=0)
    for finding in found:
        failures.append(
            f"  {finding}: a minor adds a section ID only on new content, "
            f"never in front of lines a frozen section holds"
        )
    return seen.failures() + failures, seen.notes() + [basis]


# ---------------------------------------------------------------------------
# SYS-25 -- a load directive names a listed task, in its heading's tags
# ---------------------------------------------------------------------------

# A section's load directive decides whether its rules are in context on
# every turn or only during one kind of task. A kind no task lists gives the
# section to no skill, a directive after a rule governs nothing a reader can
# see, and a second directive or one under a loaded heading leaves the load
# ambiguous. A template that guards data, credentials or authentication
# carries none, so none of its rules depends on a skill loading. Templates
# carry few directives, so planted texts exercise every failing path on
# every run.

GUARDED_TEMPLATES = ("templates/security/", "templates/backend/auth.md")
PLANTED_KINDS = {"release": "Cutting a release"}
LOAD_CASES = [
    (
        "a listed kind",
        "templates/core/x.md",
        "# T\n## A\n[ID: a]\n[LOAD: release]\n- rule\n",
        [],
    ),
    ("the check load", "templates/core/x.md", "# T\n## A\n[LOAD: check]\n- rule\n", []),
    (
        "a kind no task lists",
        "templates/core/x.md",
        "# T\n## A\n[LOAD: nowhere]\n- rule\n",
        ["templates/core/x.md:3: names nowhere, which no task lists"],
    ),
    (
        "a directive after a rule",
        "templates/core/x.md",
        "# T\n## A\n- rule\n[LOAD: release]\n",
        ["templates/core/x.md:4: sits outside its heading's tags"],
    ),
    (
        "two directives under one heading",
        "templates/core/x.md",
        "# T\n## A\n[LOAD: release]\n[LOAD: check]\n- rule\n",
        ["templates/core/x.md:4: a second load for one heading"],
    ),
    (
        "a directive under a loaded heading",
        "templates/core/x.md",
        "# T\n## A\n[LOAD: release]\n### B\n[LOAD: check]\n- rule\n",
        ["templates/core/x.md:5: under a heading that loads as release"],
    ),
    (
        "a directive in a fence",
        "templates/core/x.md",
        "# T\n## A\n```\n[LOAD: nowhere]\n```\n",
        [],
    ),
    (
        "a guarded template",
        "templates/security/x.md",
        "# T\n## A\n[LOAD: check]\n- rule\n",
        [
            "templates/security/x.md:3: a template that guards data, credentials "
            "or authentication carries no load directive"
        ],
    ),
]


def load_findings(rel: str, text: str, kinds: Mapping[str, str]) -> list[str]:
    """Each misplaced or unknown load directive in one template."""
    found: list[str] = []
    for d in load_directives(text):
        where = f"{rel}:{d['line']}"
        if rel.startswith(GUARDED_TEMPLATES) or rel in GUARDED_TEMPLATES:
            found.append(
                f"{where}: a template that guards data, credentials "
                f"or authentication carries no load directive"
            )
        elif not d["placed"]:
            found.append(f"{where}: sits outside its heading's tags")
        elif d["second"]:
            found.append(f"{where}: a second load for one heading")
        elif d["inside"]:
            found.append(f"{where}: under a heading that loads as {d['inside']}")
        elif d["kind"] != LOAD_CHECK and d["kind"] not in kinds:
            found.append(f"{where}: names {d['kind']}, which no task lists")
    return found


def check_sys_25() -> CheckResult:
    seen = Inspected()
    failures: list[str] = []
    seen.count("planted templates", LOAD_CASES)
    for label, rel, text, want in LOAD_CASES:
        got = load_findings(rel, text, PLANTED_KINDS)
        if got != want:
            failures.append(f"  planted, {label}: found {got}, owed {want}")

    manifest = os.path.join(ROOT, "templates", "manifest.yaml")
    kinds = task_kinds(parse_manifest(read(manifest)))
    seen.count("kinds of task in the manifest", kinds)
    directives = 0
    for path in all_template_files():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        text = read(path)
        directives += len(load_directives(text))
        failures.extend(f"  {f}" for f in load_findings(rel, text, kinds))
    seen.count("load directives in the templates", directives, floor=0)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-26 -- the emitter places each section by its load, the same every run
# ---------------------------------------------------------------------------

# The emitter builds a project's root file and skills from its chain, so two
# projects on the same templates get the same files. A procedure left in the
# root file costs every turn; a rule moved out of it is one an agent may
# never read; an overridden rule kept beside its override contradicts it; a
# rerun that drops filled-in facts or keeps a declined skill undoes the
# project's own choices; and output that changes between runs is the
# variance the emitter exists to remove. Planted templates exercise each of
# these, and two runs of the real chain under different hash seeds agree.

EMIT_TEMPLATE = (
    "# Base — Demo\n[ID: base-demo]\n\n## Naming\n[ID: demo-naming]\n\n"
    "- Name every turn\n\nAn override reads:\n\n```markdown\n"
    "[OVERRIDE: demo-naming]\n```\n\n"
    "## Releases\n[LOAD: release]\n\n- Tag in the skill\n\n"
    "## Lint\n[LOAD: check]\n\n- Rule the check enforces, wrapped\n"
    "  onto a second line\n\n- Run the linter:\n\n```bash\nruff check .\n"
    "```\n\n- It passes on exit 0; a warning\n  counts as a failure\n"
    "- Require violations zero\n\n"
    "## Optional\n\n- Declined rule\n\n"
    "## Render\n[ID: demo-render]\n\n- Overridden rule\n"
)
EMIT_STACK = (
    "# Stack — Demo\n\n## Render\n[OVERRIDE: demo-render]\n\n- Overriding rule\n"
)
EMIT_KINDS = {"release": "Preparing a release"}
EMIT_DECLINED = ["templates/core/demo.md#Optional"]
EMIT_FILES = [
    ("templates/core/demo.md", EMIT_TEMPLATE),
    ("templates/fixture/stack.md", EMIT_STACK),
]


def emit_findings(emitted: Mapping[str, str], inline: bool) -> list[str]:
    """What the planted templates' emitted files get wrong, one per line."""
    root = emitted.get("AGENTS.md", "")
    skill = emitted.get(".agents/skills/release/SKILL.md")
    owed = [
        ("the every-turn rule is in the root file", "Name every turn" in root),
        ("the checked section keeps its command", "ruff check ." in root),
        (
            "the checked section keeps its whole pass condition",
            "It passes on exit 0; a warning\n  counts as a failure" in root
            and "Require violations zero" in root,
        ),
        ("a fenced override example overrides nothing", "Name every turn" in root),
        (
            "the checked section's rule is left to its check, whole",
            "Rule the check enforces" not in root and "onto a second line" not in root,
        ),
        (
            "the overridden rule is replaced",
            "Overridden rule" not in root and "Overriding rule" in root,
        ),
        ("the declined section is out", "Declined rule" not in root),
    ]
    if inline:
        owed += [
            ("the procedure is inlined", "Tag in the skill" in root),
            ("no skill file is written", skill is None),
        ]
    else:
        owed += [
            ("the procedure is out of the root file", "Tag in the skill" not in root),
            (
                "the procedure is in its skill",
                skill is not None and "Tag in the skill" in skill,
            ),
            (
                "the trigger table names the skill",
                "| release | Preparing a release |" in root,
            ),
        ]
    return [label for label, ok in owed if not ok]


def rewrite_findings(work: str) -> list[str]:
    """What a rerun of the emitter gets wrong about what a project kept."""
    out = os.path.join(work, "rerun")
    mirror = "my skills"
    emit_write(out, emit_build(EMIT_FILES, EMIT_KINDS), [mirror])
    unrelated = os.path.join(out, "my")
    with io.open(unrelated, "w", encoding="utf-8") as handle:
        handle.write("not the emitter's\n")
    root = os.path.join(out, "AGENTS.md")
    with io.open(root, encoding="utf-8") as handle:
        filled = handle.read().replace("{{owner}}", "Example Org")
    with io.open(root, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(filled)
    declined = ["templates/core/demo.md#Releases"]
    emit_write(out, emit_build(EMIT_FILES, EMIT_KINDS, declined), [mirror])
    with io.open(root, encoding="utf-8") as handle:
        rerun = handle.read()
    hand = os.path.join(work, "hand")
    os.makedirs(hand)
    with io.open(os.path.join(hand, "AGENTS.md"), "w", encoding="utf-8") as handle:
        handle.write("# Hand-written\n\n## Rules\n\n- A project policy\n")
    try:
        emit_write(hand, emit_build(EMIT_FILES, EMIT_KINDS))
        refused = False
    except EmitError:
        refused = True

    # The output directory a project passes most often is `.`.
    here, dot = os.getcwd(), os.path.join(work, "dot")
    os.makedirs(dot)
    try:
        os.chdir(dot)
        emit_write(".", emit_build(EMIT_FILES, EMIT_KINDS), [mirror])
        emit_write(".", emit_build(EMIT_FILES, EMIT_KINDS, declined), [mirror])
    finally:
        os.chdir(here)
    dot_cleaned = not any(
        os.path.exists(os.path.join(dot, *parts))
        for parts in ((".agents", "skills", "release"), (mirror, "release"))
    )
    owed = [
        ("a filled-in fact survives a rerun", "Example Org" in rerun),
        (
            "a declined skill is removed",
            not os.path.exists(os.path.join(out, ".agents", "skills", "release")),
        ),
        (
            "its mirror is removed too",
            not os.path.exists(os.path.join(out, mirror, "release")),
        ),
        ("a file the emitter never wrote survives", os.path.exists(unrelated)),
        ("a declined skill and its mirror are removed from `.`", dot_cleaned),
        ("a root file the emitter did not build is not overwritten", refused),
    ]
    return [label for label, ok in owed if not ok]


def emitted_tree(out: str) -> dict[str, bytes]:
    """Every emitted file's bytes, keyed by its path under `out`."""
    tree: dict[str, bytes] = {}
    for folder, _, names in os.walk(out):
        for name in names:
            path = os.path.join(folder, name)
            with io.open(path, "rb") as handle:
                tree[os.path.relpath(path, out)] = handle.read()
    return tree


def check_sys_26() -> CheckResult:
    seen = Inspected()
    failures: list[str] = []
    for inline in (False, True):
        got = emit_findings(
            emit_build(EMIT_FILES, EMIT_KINDS, EMIT_DECLINED, inline), inline
        )
        mode = "inline" if inline else "with skills"
        failures.extend(f"  planted, {mode}: {label} fails" for label in got)
    seen.count("planted placements", 2)

    # An override the project declines leaves the section it replaced.
    root = emit_build(EMIT_FILES, EMIT_KINDS, ["templates/fixture/stack.md#Render"])[
        "AGENTS.md"
    ]
    if "Overridden rule" not in root or "Overriding rule" in root:
        failures.append(
            "  planted: a declined override still replaces its base section"
        )

    trees: list[dict[str, bytes]] = []
    work = tempfile.mkdtemp(prefix="sait-emit-")
    try:
        failures.extend(
            f"  planted rerun: {label} fails" for label in rewrite_findings(work)
        )
        for seed in ("1", "2"):
            out = os.path.join(work, seed)
            env = dict(os.environ, PYTHONHASHSEED=seed)
            proc = subprocess.run(
                [
                    sys.executable,
                    os.path.join(ROOT, "tools", "resolve_chain.py"),
                    "--emit",
                    out,
                    "base-quality",
                    "--mirror",
                    ".claude/skills",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
            )
            if proc.returncode != 0:
                failures.append(
                    f"  emit exited {proc.returncode}: "
                    f"{(proc.stdout + proc.stderr).strip()}"
                )
                return seen.failures() + failures, seen.notes()
            trees.append(emitted_tree(out))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    seen.count("files emitted for the core chain", trees[0])
    if trees[0] != trees[1]:
        differ = sorted(
            set(trees[0]) ^ set(trees[1])
            | {k for k in set(trees[0]) & set(trees[1]) if trees[0][k] != trees[1][k]}
        )
        failures.append(f"  two runs differ in: {', '.join(differ)}")
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-27 -- an emitted file names no template file
# ---------------------------------------------------------------------------

# An emitted project carries the rules, not the templates they came from, so
# a template's path in an emitted file sends the agent to a file it cannot
# open, and the rules that line calls the standard never reach it. Every
# root is emitted on its own, with skills and inlined, and no line may name a
# template file, with or without its `templates/` prefix. Each root gets its
# own build because a project may pick one root alone: an override another
# root carries could drop the section that names the path, and a build of
# every root together would then hide it. A planted template naming itself
# both ways proves the scan finds each form, and a planted second root that
# overrides one of those sections proves each root is scanned on its own.

PATH_TEMPLATE = (
    "# Base — Demo\n[ID: base-demo]\n\n## Review\n[LOAD: release]\n\n"
    "- `templates/core/demo.md` is the standard\n\n"
    "## Naming\n[ID: demo-naming]\n\n"
    '- See `core/demo.md`, "Naming"\n'
)
PATH_STACK = "# Stack — Demo\n\n## Naming\n[OVERRIDE: demo-naming]\n\n- Name by role\n"
PATH_KINDS = {"release": "Preparing a release"}
PATH_TEMPLATES = {
    "templates/core/demo.md": ("base-demo", "Demo rules"),
    "templates/fixture/stack.md": ("stack-demo", "Demo stack"),
}
PATH_CHAINS = {
    "demo": [("templates/core/demo.md", PATH_TEMPLATE)],
    "stack": [
        ("templates/core/demo.md", PATH_TEMPLATE),
        ("templates/fixture/stack.md", PATH_STACK),
    ],
}


def path_findings(
    emitted: Mapping[str, str | bytes], paths: Iterable[str]
) -> list[str]:
    """Each emitted file and line that names one of `paths`, a template's
    path under the repository."""
    patterns = [
        (
            path,
            re.compile(
                r"(?<![\w/.-])(?:templates/)?"
                + re.escape(path[len("templates/") :])
                + r"(?![\w/-])"
            ),
        )
        for path in sorted(paths)
    ]
    findings: list[str] = []
    for rel in sorted(emitted):
        text = emitted[rel]
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            findings.extend(
                f"{rel}:{number} names {path}"
                for path, pattern in patterns
                if pattern.search(line)
            )
    return findings


def root_path_findings(
    chains: Mapping[str, Sequence[tuple[str, str]]],
    kinds: Mapping[str, str],
    paths: Collection[str],
    templates: Mapping[str, tuple[str, str]],
    emitted_counts: Counter[str] | None = None,
) -> list[str]:
    """Each root's emitted lines that name one of `paths`, the root built
    alone with skills, inlined and as section files. `chains` maps a root to
    its (path, text) pairs in resolution order, `templates` each path to its
    manifest ID and description; `emitted_counts`, a Counter, takes the
    files emitted per mode."""
    findings: list[str] = []
    for root in sorted(chains):
        for mode in ("skills", "inline", "sections"):
            emitted = (
                emit_sections(chains[root], templates)
                if mode == "sections"
                else emit_build(chains[root], kinds, inline_skills=mode == "inline")
            )
            if emitted_counts is not None:
                emitted_counts[mode] += len(emitted)
            findings.extend(
                f"{root}, {mode}: {finding}"
                for finding in path_findings(emitted, paths)
            )
    return findings


def check_sys_27() -> CheckResult:
    seen = Inspected()
    failures: list[str] = []
    planted = ["templates/core/demo.md"]
    alone = root_path_findings(
        {"demo": PATH_CHAINS["demo"]}, PATH_KINDS, planted, PATH_TEMPLATES
    )
    if len(alone) != 6:
        failures.append(
            f"  planted: {len(alone)} of the 6 named paths found, 2 per mode"
        )
    seen.count("planted paths found", len(alone))

    # Built together, the stack's override drops the Naming line and only
    # the Review line is left; built per root, the demo root still has both.
    together = path_findings(emit_build(PATH_CHAINS["stack"], PATH_KINDS), planted)
    split = root_path_findings(PATH_CHAINS, PATH_KINDS, planted, PATH_TEMPLATES)
    if len(together) != 1 or len(split) != 9:
        failures.append(
            f"  planted override: {len(together)} found built "
            f"together, owed 1; {len(split)} per root, owed 9"
        )

    core_ids, entries, _ = load_manifest()
    _, offered, catalogue = load_catalogue()
    roots = [stack["id"] for stack in catalogue] + list(
        opt_in_roots(core_ids, offered, catalogue)
    )
    seen.count("roots emitted", len(roots))
    paths = template_files()
    seen.count("template paths scanned for", len(paths))
    chains = {
        root: [
            (path, read_file(path)) for path in resolve_chain(root, core_ids, entries)
        ]
        for root in roots
    }
    kinds = task_kinds(
        parse_manifest(read(os.path.join(ROOT, "templates", "manifest.yaml")))
    )
    emitted: Counter[str] = Counter()
    failures.extend(
        f"  {finding}"
        for finding in root_path_findings(
            chains, kinds, paths, template_names(entries), emitted
        )
    )
    for mode in ("skills", "inline", "sections"):
        seen.count(f"files emitted, {mode}", emitted[mode])
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-28 -- section files hold every adopted rule, and the map reads them
# on demand
# ---------------------------------------------------------------------------

# With `--sections` the emitter builds one file per topic and a root file
# that maps each topic to its file. The files must hold exactly the rules
# the other modes deliver: a rule no file holds is one the agent never
# reads, and a copy that differs from its source contradicts it. A section
# that extends or names another carries it, since a rule left to a
# reference is one the agent never reads, and the root file holds only the
# map, read on demand. Planted templates exercise each of these, every root
# is built alone, and two runs under different hash seeds agree.

SECTION_BASE = (
    "# Base — Demo\n[ID: base-demo]\n\nTitle rule for every heading.\n\n"
    "## Naming\n[ID: demo-naming]\n\n- Name by role\n\n"
    "## Releases\n[LOAD: release]\n\n- Tag the release\n\n"
    "## Lint\n[LOAD: check]\n\n- Rule the check enforces\n\n- Run the linter:\n\n"
    "```bash\nruff check .\n```\n\n"
    "## Optional\n\n- Declined rule\n\n"
    "## Render\n[ID: demo-render]\n\n- Overridden rule\n\n"
    "## Target\n[ID: demo-target]\n\n- Target rule\n\n"
    "## Content\n[ID: demo-content]\n\n- Base content rule\n\n"
    "## Theme\n[ID: demo-theme]\n\n- Base theme rule\n\n"
    "## Shared\n[ID: demo-shared]\n\n- Shared first rule\n\n"
    "## Follow\n\n- Follow the rules of `demo-shared`\n\n"
    "## Parent\n[ID: demo-parent]\n\n- Parent rule\n\n"
    "### Child\n[ID: demo-child]\n[EXTEND: demo-naming]\n\n- Child rule\n"
)
SECTION_LAYER = (
    "# Layer — Demo\n[ID: layer-demo]\n\n"
    "The layer adds to the naming rules (`demo-naming`).\n\n"
    "## Naming\n[EXTEND: demo-naming]\n\n- Prefix a layer name\n\n"
    "## Render\n[OVERRIDE: demo-render]\n\n- Overriding rule\n\n"
    "## Paging\n\n- Page every list\n\n"
    "## Child\n[ID: layer-child]\n[OVERRIDE: demo-child]\n\n- Child replaced\n"
)
SECTION_TITLE_ONLY = "# Other — Demo\n[ID: other-demo]\n\n- Rule under a bare title\n"

# Three levels of override, each declaring an ID of its own, as a section
# that expects further specialisation does.
SECTION_MID = (
    "# Mid — Demo\n[ID: mid-demo]\n\n"
    "## Content\n[ID: mid-content]\n[OVERRIDE: demo-content]\n\n- Mid content rule\n"
)
SECTION_TOP = (
    "# Top — Demo\n[ID: top-demo]\n\n"
    "## Content\n[ID: top-content]\n[OVERRIDE: mid-content]\n\n- Top content rule\n"
)

# An extension whose section runs past its heading to the next ID, a section
# naming the base of the override chain, and an extension of that base.
SECTION_MORE = (
    "# More — Demo\n[ID: more-demo]\n\n"
    "## First\n[EXTEND: demo-target]\n\n- First extension rule\n\n"
    "## Second\n\n- Second extension rule\n\n"
    "## Fresh\n\n[ID: more-fresh]\n\n- Fresh rule\n\n"
    "## Gone\n[EXTEND: demo-naming]\n\n- Gone rule\n\n"
    "## Kept\n\n- Kept rule\n\n"
    "## Later\n[ID: more-later]\n\n- Follow the content rules (`demo-content`)\n"
    "- Follow the theme rules (`demo-theme`)\n\n"
    "## Extra\n[EXTEND: demo-content]\n\n- Extra content rule\n"
)
# Two levels of override where the first sits under a heading with no ID
# of its own, inside its title's section, which the second overrides.
SECTION_SKIN = (
    "# Skin — Demo\n[ID: skin-demo]\n\n"
    "## Theme\n[OVERRIDE: demo-theme]\n\n- Skin theme rule\n"
)
SECTION_BRAND = (
    "# Brand — Demo\n[ID: brand-demo]\n\n"
    "## Skin\n[OVERRIDE: skin-demo]\n\n- Brand theme rule\n"
)
# A title whose ID a later template overrides, while its headings keep
# IDs of their own and stay.
SECTION_FACADE = (
    "# Facade — Demo\n[ID: facade-demo]\n\nFacade title rule.\n\n"
    "## Door\n[ID: facade-door]\n\n- Door rule\n"
)
SECTION_FRONT = (
    "# Front — Demo\n[ID: front-demo]\n[OVERRIDE: facade-demo]\n\nFront title rule.\n"
)
SECTION_FILES = [
    ("templates/core/demo.md", SECTION_BASE),
    ("templates/backend/layer.md", SECTION_LAYER),
    ("templates/backend/mid.md", SECTION_MID),
    ("templates/fixture/top.md", SECTION_TOP),
    ("templates/backend/facade.md", SECTION_FACADE),
    ("templates/backend/skin.md", SECTION_SKIN),
    ("templates/fixture/brand.md", SECTION_BRAND),
    ("templates/fixture/front.md", SECTION_FRONT),
    ("templates/fixture/more.md", SECTION_MORE),
    ("templates/data/other.md", SECTION_TITLE_ONLY),
]
SECTION_TEMPLATES = {
    "templates/core/demo.md": ("base-demo", "Demo rules"),
    "templates/backend/layer.md": ("backend-layer", "Layer rules"),
    "templates/backend/mid.md": ("backend-mid", "Mid rules"),
    "templates/fixture/top.md": ("stack-top", "Top rules"),
    "templates/backend/facade.md": ("backend-facade", "Facade rules"),
    "templates/backend/skin.md": ("backend-skin", "Skin rules"),
    "templates/fixture/front.md": ("stack-front", "Front rules"),
    "templates/fixture/brand.md": ("stack-brand", "Brand rules"),
    "templates/fixture/more.md": ("stack-more", "More rules"),
    "templates/data/other.md": ("base-other", "Other rules"),
}
SECTION_KINDS = {"release": "Preparing a release"}
SECTION_DECLINED = ["templates/core/demo.md#Optional", "templates/fixture/more.md#Gone"]
SECTION_LEAD = "read them before the work starts"
SECTION_PATH = re.compile(r"`(" + re.escape(SECTIONS_DIR) + r"/[^`]+)`")

# The inline root file's own lines, which carry no rule.
INLINE_OWN = (
    BUILT_LINE,
    "The adopted rules that apply on every task.",
    "This agent loads no skills, so each task's procedures are here.",
)


def unfenced(text: str) -> list[str]:
    """A Markdown text's lines outside its fences."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        run = FENCE_LINE.match(line)
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            continue
        if fence is None:
            kept.append(line)
    return kept


def heading_blocks(text: str) -> list[tuple[tuple[str, ...], tuple[str, ...]]]:
    """A Markdown text cut at each heading outside a fence: each block's
    heading path and its non-blank lines that are not headings."""
    blocks: list[tuple[tuple[str, ...], list[str]]] = [((), [])]
    stack: list[tuple[int, str]] = []
    fence: str | None = None
    for line in text.splitlines():
        run = FENCE_LINE.match(line)
        heading = None if (fence or run) else LEVEL_HEADING.match(line)
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
        if heading:
            level = len(heading.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, line))
            blocks.append((tuple(h for _, h in stack), []))
        elif line.strip():
            blocks[-1][1].append(line)
    return [(path, tuple(body)) for path, body in blocks]


def adopted_lines(
    files: Sequence[tuple[str, str]],
    kinds: Mapping[str, str],
    declined: Iterable[str] = (),
) -> Counter[str]:
    """Every rule line the inlined root file delivers, counted: the adopted
    rule set the other modes carry."""
    root = emit_build(files, kinds, declined, inline_skills=True)["AGENTS.md"]
    rules = root.split("\n## Rules\n", 1)[1]
    lines: Counter[str] = Counter()
    for path, body in heading_blocks(rules):
        lines.update(body)
        # A procedure's heading names its kind, and its first line is the
        # kind's description, which the emitter writes and no template does.
        kind = path[-1][len("### ") :] if path and path[-1].startswith("### ") else ""
        if len(path) == 2 and path[0] == "## Procedures" and kind in kinds:
            lines[kinds[kind]] -= 1
    for own in INLINE_OWN:
        lines[own] -= 1 if lines[own] else 0
    return +lines


class _Run:
    """One override's section: the IDs it replaces, the sections its rows
    sit in, and the rule lines it delivers."""

    def __init__(self) -> None:
        self.targets: set[str] = set()
        self.sections: set[str] = set()
        self.lines: set[str] = set()


def relation_findings(
    files: Sequence[tuple[str, str]],
    declined: Iterable[str],
    owed: Counter[str],
    sections: Mapping[str, str],
) -> list[str]:
    """Each section file that lacks rules a relationship owes it.

    A reference reading, apart from the emitter's: every relationship is
    read from the unfiltered chain, the rules under a title, each section a
    heading's section extends, and each ID its prose names, and each owes
    the rules that survive for it, the ID's own or, where it is replaced,
    those of the override that replaces it, followed down the chain. A file
    carries a heading when it holds every rule the heading delivers.
    """
    gone_list = set(declined)
    topics: dict[tuple[str, tuple[tuple[int, str], ...]], set[str]] = {}
    extends_of: dict[tuple[str, tuple[tuple[int, str], ...]], set[str]] = {}
    names_of: dict[tuple[str, tuple[tuple[int, str], ...]], set[str]] = {}
    titles: dict[str, set[str]] = {}
    span: dict[str, set[str]] = {}
    runs: list[_Run] = []
    for path, text in files:
        extends: set[str] = set()
        run: _Run | None = None
        fresh = False
        for row in parse_rows(text):
            gone = any(f"{path}#{h}" in gone_list for _, h in row["path"])
            line = row["line"].strip()
            if row["heading"]:
                fresh = True
                if len(row["path"]) == 1 and row["section"]:
                    titles.setdefault(path, set()).add(row["section"])
                continue
            if row["tag"]:
                for pattern in (ID_TAG, EXTEND_TAG, OVERRIDE_TAG):
                    match = pattern.match(line)
                    if not match:
                        continue
                    if fresh:
                        extends, run, fresh = set(), None, False
                    if pattern is EXTEND_TAG:
                        extends.add(match.group(1))
                    elif pattern is OVERRIDE_TAG and not gone:
                        if run is None:
                            run = _Run()
                            runs.append(run)
                        run.targets.add(match.group(1))
                        if row["section"]:
                            run.sections.add(row["section"])
                continue
            if not line:
                continue
            fresh = False
            if len(row["path"]) == 1 and row["section"]:
                titles.setdefault(path, set()).add(row["section"])
            if run is not None and row["section"]:
                run.sections.add(row["section"])
            if gone or not owed[row["line"]]:
                continue
            key = (path, tuple(row["path"][:2]))
            topics.setdefault(key, set()).add(row["line"])
            extends_of.setdefault(key, set()).update(extends)
            if not row["fence"]:
                names_of.setdefault(key, set()).update(
                    re.findall(r"`([a-z0-9][a-z0-9-]*)`", row["line"])
                )
            if row["section"]:
                span.setdefault(row["section"], set()).add(row["line"])
            if run is not None:
                run.lines.add(row["line"])

    def survives(section: str, seen: set[str]) -> set[str]:
        if section in seen:
            return set()
        seen.add(section)
        found = set(span.get(section, ()))
        for one in runs:
            if section in one.targets:
                found |= one.lines
                for inner in sorted(one.sections):
                    found |= survives(inner, seen)
        return found

    findings: list[str] = []
    for rel in sorted(sections):
        lines = set(sections[rel].splitlines())
        for key, held in topics.items():
            if not held <= lines:
                continue
            path, place = key
            heading = place[-1][1] if place else path
            owes: dict[str, set[str]] = {}
            if len(place) == 2:
                owes["the rules under its title"] = topics.get((path, place[:1]), set())
                for title in sorted(titles.get(path, ())):
                    if not span.get(title):
                        owes[f"the replacement of `{title}`"] = survives(title, set())
            for target in sorted(extends_of.get(key, ())):
                owes[f"`{target}`, which it extends"] = survives(target, set())
            for target in sorted(names_of.get(key, ())):
                owes[f"`{target}`, which it names"] = survives(target, set())
            findings += [
                f"{rel} carries {heading} and lacks {what}"
                for what, needed in owes.items()
                if not needed <= lines
            ]
    return findings


def section_findings(
    files: Sequence[tuple[str, str]],
    kinds: Mapping[str, str],
    emitted: Mapping[str, str],
    declined: Iterable[str] = (),
) -> list[str]:
    """What the section files emitted from `files` get wrong: a rule no file
    holds, a line no adopted rule is, two copies of one block that differ, a
    named section a file does not carry, and a root file that holds a rule
    or maps a file other than once."""
    declined = list(declined)
    findings: list[str] = []
    owed = adopted_lines(files, kinds, declined)
    sections = {rel: text for rel, text in emitted.items() if rel != "AGENTS.md"}
    seen: dict[tuple[str, ...], tuple[str, ...]] = {}
    held: Counter[str] = Counter()
    for rel in sorted(sections):
        for path, body in heading_blocks(sections[rel]):
            if path in seen and seen[path] != body:
                findings.append(f"{rel}: its copy of {' > '.join(path)} differs")
            elif path not in seen:
                seen[path] = body
                held.update(body)
    findings += [f"no section file holds: {line}" for line in owed - held]
    findings += [f"no adopted rule is: {line}" for line in held - owed]

    findings += relation_findings(files, declined, owed, sections)

    rules = section_rules(files, declined)
    for rel in sorted(sections):
        lines = set(sections[rel].splitlines())
        prose = "\n".join(unfenced(sections[rel]))
        for name in sorted(set(re.findall(r"`([a-z0-9][a-z0-9-]*)`", prose))):
            if name in rules and not set(rules[name]) <= lines:
                findings.append(f"{rel} names `{name}` and does not carry it")

    root = emitted.get("AGENTS.md", "")
    mapped = Counter(SECTION_PATH.findall(root))
    findings += [
        f"the root file maps {rel} {mapped[rel]} times, owed once"
        for rel in sorted(sections)
        if mapped[rel] != 1
    ]
    findings += [
        f"the root file maps {rel}, which is not emitted"
        for rel in sorted(set(mapped) - set(sections))
    ]
    # The map's own header rows are the emitter's, and a template's table
    # may share them.
    in_root = [
        line
        for line in root.split("\n## Rules\n", 1)[-1].splitlines()
        if owed[line] and line not in MAP_HEADER
    ]
    findings += [f"the root file holds a rule: {line}" for line in in_root]
    if SECTION_LEAD not in " ".join(root.split()):
        findings.append("the root file does not say to read a file on demand")
    return findings


def planted_section_findings() -> list[str]:
    """What the planted templates' section files get wrong, beyond the
    general findings: where each rule lands and what each file carries."""
    emitted = emit_sections(SECTION_FILES, SECTION_TEMPLATES, SECTION_DECLINED)
    root = emitted.get("AGENTS.md", "")
    base = emitted.get(f"{SECTIONS_DIR}/base-demo/naming.md", "")
    layer = emitted.get(f"{SECTIONS_DIR}/backend-layer/naming.md", "")
    paging = emitted.get(f"{SECTIONS_DIR}/backend-layer/paging.md", "")
    other = emitted.get(f"{SECTIONS_DIR}/base-other/other-demo.md", "")
    target = emitted.get(f"{SECTIONS_DIR}/base-demo/target.md", "")
    second = emitted.get(f"{SECTIONS_DIR}/stack-more/second.md", "")
    later = emitted.get(f"{SECTIONS_DIR}/stack-more/later.md", "")
    fresh = emitted.get(f"{SECTIONS_DIR}/stack-more/fresh.md", "")
    kept = emitted.get(f"{SECTIONS_DIR}/stack-more/kept.md", "")
    door = emitted.get(f"{SECTIONS_DIR}/backend-facade/door.md", "")
    follow = emitted.get(f"{SECTIONS_DIR}/base-demo/follow.md", "")
    extra = emitted.get(f"{SECTIONS_DIR}/stack-more/extra.md", "")
    top = emitted.get(f"{SECTIONS_DIR}/stack-top/content.md", "")
    everything = "\n".join(emitted.values())
    owed = [
        ("the overridden rule is replaced", "Overridden rule" not in everything),
        ("the override is delivered", "Overriding rule" in everything),
        ("the declined section is out", "Declined rule" not in everything),
        ("the checked rule is left to its check", "check enforces" not in everything),
        ("the check's command is kept", "ruff check ." in everything),
        ("the procedure is out of the root file", "Tag the release" not in root),
        ("the procedure has a file", "Tag the release" in everything),
        (
            "a section carries its extension, after it",
            0 <= base.find("Name by role") < base.find("Prefix a layer name"),
        ),
        (
            "an extension carries the section it extends, before it",
            0 <= layer.find("Name by role") < layer.find("Prefix a layer name"),
        ),
        ("a section carries the rules under its title", "Title rule" in base),
        ("a section carries what its title names", "Name by role" in paging),
        ("a bare title gets a file", "Rule under a bare title" in other),
        ("the map names a template's topic", "| Paging |" in root),
        ("the map gives a template's description", "Layer rules" in root),
        ("the model line names section files", "Model: root and sections" in root),
        (
            "a section carries an extension's heading up to the next ID",
            "Second extension rule" in target,
        ),
        (
            "an extension's later heading carries the section it extends",
            "Target rule" in second,
        ),
        ("an extension ends at the next ID", "Target rule" not in later),
        (
            "a declined heading's relationship reaches its adopted siblings",
            "Name by role" in kept
            and "Kept rule" in base
            and "Gone rule" not in everything,
        ),
        (
            "an override under an untagged heading is replaced through its section",
            "Brand theme rule" in later
            and "Skin theme rule" not in everything
            and "Base theme rule" not in everything,
        ),
        (
            "a heading under an overridden title carries the title's replacement",
            "Front title rule." in door and "Facade title rule." not in everything,
        ),
        (
            "a heading whose ID follows a blank line extends nothing",
            "Target rule" not in fresh and "Fresh rule" not in target,
        ),
        (
            "a heading naming its own section's ID carries its other headings",
            "Shared first rule" in follow,
        ),
        (
            "a replaced subsection's relationship stays out of its heading",
            "Parent rule" not in base and "Child rule" not in everything,
        ),
        (
            "each replaced level of an override chain is out",
            "Base content rule" not in everything
            and "Mid content rule" not in everything,
        ),
        (
            "a section naming an overridden ID carries its last override",
            "Top content rule" in later,
        ),
        (
            "an extension of an overridden ID carries its last override, before it",
            0 <= extra.find("Top content rule") < extra.find("Extra content rule"),
        ),
        (
            "the last override carries the extension of the ID it replaces",
            0 <= top.find("Top content rule") < top.find("Extra content rule"),
        ),
    ]
    findings = [label for label, ok in owed if not ok]
    findings += section_findings(
        SECTION_FILES, SECTION_KINDS, emitted, SECTION_DECLINED
    )

    # Each finding the check owes, planted: a file dropped, a copy edited,
    # and a carried section left out.
    controls = {
        "a dropped file": {
            rel: text for rel, text in emitted.items() if not rel.endswith("/paging.md")
        },
        "an edited copy": dict(
            emitted,
            **{
                f"{SECTIONS_DIR}/backend-layer/paging.md": paging.replace(
                    "Title rule", "Edited rule"
                )
            },
        ),
        "a reference left alone": dict(
            emitted,
            **{
                f"{SECTIONS_DIR}/backend-layer/paging.md": paging.replace(
                    "- Name by role\n", ""
                )
            },
        ),
    }
    for label, mutated in controls.items():
        if not section_findings(
            SECTION_FILES, SECTION_KINDS, mutated, SECTION_DECLINED
        ):
            findings.append(f"{label} goes unreported")
    return findings


def check_sys_28() -> CheckResult:
    seen = Inspected()
    failures = [f"  planted: {label}" for label in planted_section_findings()]
    seen.count("planted section files", 1)

    core_ids, entries, _ = load_manifest()
    _, offered, catalogue = load_catalogue()
    roots = [stack["id"] for stack in catalogue] + list(
        opt_in_roots(core_ids, offered, catalogue)
    )
    seen.count("roots built as section files", len(roots))
    kinds = task_kinds(
        parse_manifest(read(os.path.join(ROOT, "templates", "manifest.yaml")))
    )
    names = template_names(entries)
    files = 0
    for root in roots:
        chain = [
            (path, read_file(path)) for path in resolve_chain(root, core_ids, entries)
        ]
        emitted = emit_sections(chain, names)
        files += len(emitted)
        failures += [
            f"  {root}: {finding}"
            for finding in section_findings(chain, kinds, emitted)
        ]
    seen.count("section files emitted", files)

    # Two runs of the real tool, under different hash seeds, over roots
    # whose chains extend and name sections in another template.
    trees: list[dict[str, bytes]] = []
    work = tempfile.mkdtemp(prefix="sait-sections-")
    try:
        for seed in ("1", "2"):
            out = os.path.join(work, seed)
            proc = subprocess.run(
                [
                    sys.executable,
                    os.path.join(ROOT, "tools", "resolve_chain.py"),
                    "--emit",
                    out,
                    "--sections",
                    "backend-auth",
                    "backend-database",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=dict(os.environ, PYTHONHASHSEED=seed),
            )
            if proc.returncode != 0:
                failures.append(
                    f"  emit exited {proc.returncode}: "
                    f"{(proc.stdout + proc.stderr).strip()}"
                )
                return seen.failures() + failures, seen.notes()
            trees.append(emitted_tree(out))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    seen.count("files emitted by the tool", trees[0])
    if trees[0] != trees[1]:
        differ = sorted(
            set(trees[0]) ^ set(trees[1])
            | {k for k in set(trees[0]) & set(trees[1]) if trees[0][k] != trees[1][k]}
        )
        failures.append(f"  two runs differ in: {', '.join(differ)}")
    return seen.failures() + failures, seen.notes()
