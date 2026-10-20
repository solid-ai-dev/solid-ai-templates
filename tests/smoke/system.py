"""Smoke checks of the SYS family: properties of the repository as a whole.
"""

import io
import os
import re
import subprocess
import sys

# One definition of what a manifest section is, shared with the resolver,
# so a fork's own key is read here exactly as it is resolved there.
from resolve_chain import entry_sections

from runner import ROOT, repository_files, template_files
from .common import (
    _load_manifest, _resolve_stack, _roots_by_kind, _stacks,
    all_template_files, depends_on_refs, HAS_YAML, Inspected,
    iter_id_declarations, MISSING_YAML, read, TEMPLATE_DIRS, yaml)


def missing_template_dirs():
    """Expected directories that contribute no file to the corpus.

    A directory that is not there is a finding, not a skip. Skipping it
    makes a rename silent: every listed directory disappears and the check
    reports the same pass as a clean tree.
    """
    present = template_files()
    return [d for d in TEMPLATE_DIRS
            if not any(p.startswith(d + "/") for p in present)]


# ---------------------------------------------------------------------------
# SYS-01 — DEPENDS ON paths resolve to existing files
# ---------------------------------------------------------------------------

def check_sys_01():
    failures = []
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

def check_sys_02():
    failures = []
    seen = {}
    inspected = Inspected()

    files = inspected.count("template files scanned", all_template_files())
    for filepath in files:
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT)
        for sid, _ in iter_id_declarations(content):
            if sid in seen:
                failures.append(
                    f"  Duplicate ID '{sid}': "
                    f"{seen[sid]} and {rel}"
                )
            else:
                seen[sid] = rel

    inspected.count("section IDs collected", len(seen))
    return inspected.failures() + failures, inspected.notes()


# ---------------------------------------------------------------------------
# SYS-03 — every template file has a manifest entry
# ---------------------------------------------------------------------------

def check_sys_03():
    if not HAS_YAML:
        return [MISSING_YAML]

    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    manifest_files = set()
    for section in entry_sections(manifest):
        for entry in manifest[section]:
            if isinstance(entry, dict) and "file" in entry:
                manifest_files.add(
                    entry["file"].replace("/", os.sep)
                )

    failures = []
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

def check_sys_04():
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

    failures = []
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


def check_sys_06():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []
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
            heading = re.compile(
                r"^##\s+" + re.escape(section) + r"\s*$", re.MULTILINE)
            if not heading.search(blob):
                failures.append(
                    f"  {sid}: resolved chain missing MUST section "
                    f"'## {section}' (ADR-017)"
                )

    seen.count("MUST sections asserted across those chains", asserted)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-07 — 360 audit reports live only under docs/audits/
# ---------------------------------------------------------------------------
# templates/workflow/360.md [ID: 360-tracking] mandates one audit-storage
# convention: each audit is a dated report at docs/audits/YYYY-MM-DD-360.md,
# and the single-file docs/360-audit.md form is prohibited. This guards the
# rule mechanically — no audit report may live outside docs/audits/, and a
# file inside it MUST use the dated YYYY-MM-DD-360.md name.

_AUDIT_DIR = "docs/audits"

# An audit report file: the prohibited single-file form (360-audit*.md) or a
# dated report (*-360.md). The 360.md template itself matches neither.
_AUDIT_NAME = re.compile(r"(?:360-audit.*|.*-360)\.md$")
_DATED_AUDIT_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-360\.md$")
def check_sys_07():
    failures = []
    seen = Inspected()
    reports = 0
    walked = repository_files()
    for rel in walked:
        name = rel.rsplit("/", 1)[-1]
        if _AUDIT_NAME.match(name):
            reports += 1
            if not rel.startswith(_AUDIT_DIR + "/"):
                failures.append(
                    f"  {rel}: 360 audit report outside {_AUDIT_DIR}/ — move "
                    f"it to {_AUDIT_DIR}/YYYY-MM-DD-360.md "
                    f"(360.md [ID: 360-tracking])"
                )
            elif not _DATED_AUDIT_NAME.match(name):
                failures.append(
                    f"  {rel}: audit file must use the YYYY-MM-DD-360.md "
                    f"dated-report name (360.md [ID: 360-tracking])"
                )

    seen.count("repository files read", walked)
    seen.count("audit reports found", reports)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# SYS-09 — sync_docs.py --check inspects without writing
# ---------------------------------------------------------------------------
# A gate that repairs what it inspects reports clean on its second run, so
# only its first invocation carries information. This runs against a
# temporary copy and asserts both directions: check mode reports the
# difference and leaves the bytes alone, plain mode writes. Without the
# second assertion a function that did nothing at all would pass.


def check_sys_09():
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
    failures = []
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


def check_sys_10():
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
    failures = []
    seen = Inspected()
    seen.count("synthetic documents inspected", 1)
    seen.count("directive occurrences in the document",
               document.count("[DEPENDS ON:"), floor=3)
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


def check_sys_11():
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
    def rel_of(path):
        return os.path.relpath(path, ROOT).replace(os.sep, "/")

    defined_in = {}
    for path in all_template_files():
        for section_id, _line in iter_id_declarations(read(path)):
            defined_in.setdefault(section_id, set()).add(rel_of(path))

    references = 0
    cited = set()
    failures = []

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
        failures.append("  resolved no stack chains — the check reached "
                        "nothing")
    if not opt_in_roots:
        failures.append("  resolved no opt-in roots — every extra and "
                        "platform file went unread, and a reference "
                        "dangling only there passes unseen")
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

def _measure_chains():
    """Sizes per root, with the two root kinds returned alongside them.

    Both kinds of root: a stack, and an orthogonal template picked
    independently of the stack, which resolves as its own root. Measuring
    stacks alone leaves every opt-in root uncapped, and a fifth of the
    corpus reaches a consumer only that way. The kinds come back separate
    so a caller reports a count per kind rather than their sum.
    """
    core_ids, entries, _ = _load_manifest()
    stacks, opt_in = _roots_by_kind(core_ids, entries)

    sizes = {}
    for root in list(stacks) + list(opt_in):
        files, _ = _resolve_stack(root, core_ids, entries)
        sizes[root] = sum(len(read(os.path.join(ROOT, f))) for f in files)
    return sizes, stacks, opt_in


def _core_tier_files(core_ids, entries):
    """The files the resolver seeds into every chain regardless of what
    any template declares."""
    return [entries[cid]["file"] for cid in core_ids if cid in entries]


def _declared_closure(start_file):
    """Files reachable from `start_file` by following DEPENDS ON alone.

    This is the walk README instructs an adopter to perform by hand, so it
    reads the directives out of the files rather than the manifest's
    depends_on -- a reader following the README has only the files.
    """
    seen, pending = set(), [start_file]
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


def check_sys_13():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    seen = Inspected()
    core_files = seen.count("core-tier files seeded",
                            _core_tier_files(core_ids, entries))
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

        resolved, _ = _resolve_stack(root, core_ids, entries)
        resolved = set(resolved)
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


def check_sys_14():
    seen = Inspected()
    resolver = os.path.join(ROOT, "tools", "resolve_chain.py")
    seen.count("resolve_chain.py argument cases", RESOLVE_CASES)
    failures = []

    for args, want_code, want_phrase in RESOLVE_CASES:
        proc = subprocess.run(
            [sys.executable, resolver] + args,
            capture_output=True, text=True,
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


def check_sys_15():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []
    seen = Inspected()

    stacks = _stacks(entries)
    seen.count("stacks classified by layer", stacks)
    seen.count("exempt layers named with a reason",
               SECURITY_EXEMPT_LAYERS)

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


def _tier_sort_key(label):
    """Order tier labels by the window they name, not by their text.

    `1M` sorts before `200K` lexically and after it numerically, and the
    exemption is about which window is smallest.
    """
    if label.endswith("M"):
        return float(label[:-1]) * 1000
    return float(label.rstrip("K"))


def _recorded_tiers():
    """The tier recorded per stack category, as {layer: window label}."""
    out = {}
    path = os.path.join(ROOT, CONTEXT_TIERS)
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            layer, window = line.split()
            out[layer] = window
    return out


def check_sys_16():
    if not HAS_YAML:
        return [MISSING_YAML]

    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from sync_docs import (CHARS_PER_TOKEN, OVERHEAD_TOKENS, CONTEXT_WINDOWS,
                           _window_label)
    from resolve_chain import load_manifest, resolve_chain, concat_chain

    failures = []
    seen = Inspected()

    core_ids, entries, stacks = load_manifest()
    seen.count("stacks measured", stacks)

    largest = {}
    for stack in stacks:
        size = len(concat_chain(resolve_chain(stack['id'], core_ids,
                                              entries)))
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


def _runner_text():
    """The text of every runner in tests/ other than run_smoke.py.

    That file's registry is read as data; its prose names specs it does not
    run, so it is not searched as text.
    """
    tests = os.path.join(ROOT, "tests")
    texts = []
    for name in sorted(os.listdir(tests)):
        if name.endswith(".py") and name != "run_smoke.py":
            with io.open(os.path.join(tests, name), encoding="utf-8") as f:
                texts.append(f.read())
    return "\n".join(texts)


def check_sys_17():
    # Imported here: the registry imports this module.
    from .registry import CHECKS

    failures = []
    seen = Inspected()

    spec_dir = os.path.join(ROOT, "docs", "tests", "specs")
    on_disk = {}
    for name in os.listdir(spec_dir):
        if name.endswith(".md"):
            with io.open(os.path.join(spec_dir, name),
                         encoding="utf-8") as handle:
                on_disk[os.path.splitext(name)[0]] = handle.read()

    with io.open(os.path.join(ROOT, "docs", "tests", "index.md"),
                 encoding="utf-8") as handle:
        index = handle.read()

    seen.count("checks registered", CHECKS)
    seen.count("spec documents on disk", on_disk)
    indexed = set(SPEC_ID.findall(index))
    seen.count("specs the index names", indexed)

    cited = {check.get("spec") for check in CHECKS}
    runners = _runner_text()
    for spec in sorted(on_disk):
        if spec not in index:
            failures.append(f"  {spec}: on disk with no row in "
                            f"docs/tests/index.md")
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
        failures.append(f"  {spec}: named in docs/tests/index.md with no "
                        f"document under docs/tests/specs/")

    for check in CHECKS:
        spec = check.get("spec")
        if not spec:
            failures.append(
                f"  {check['id']}: registered with no spec field"
            )
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

QUALITY_GATES_EXEMPT_LAYERS = {}

QUALITY_GATES_ID = "base-quality-gates"


def check_sys_18():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []
    seen = Inspected()

    recorded = _recorded_tiers()
    constrained = min(recorded.values(), key=_tier_sort_key) if recorded else None
    seen.count("categories recorded", recorded)

    # Zero exemptions is a real answer: a tree whose only stack is the
    # fixture has no constrained category to exempt.
    seen.count("exempt layers named with a reason",
               QUALITY_GATES_EXEMPT_LAYERS, floor=0)

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
        layer = stack.get("layer")
        if not layer:
            failures.append(
                f"  {stack['id']}: no 'layer' in the manifest, so this "
                f"check cannot tell whether {QUALITY_GATES_ID} is "
                f"required of it"
            )
            continue
        if layer not in QUALITY_GATES_EXEMPT_LAYERS:
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


def core_fault(depends_on):
    """A manifest whose one core entry depends on `depends_on`.

    A fault under the core tier breaks every root, so each is planted in a
    manifest of its own, and the valid stack is the root asked for.
    """
    return """core: [base-a]

base:
  - id: base-a
    file: templates/core/quality.md
    depends_on: [%s]

stacks:
  - id: stack-valid
    file: templates/fixture/stack.md
    depends_on: [base-a]
""" % depends_on


# The core tier's entries are seeded before any root is walked, so their own
# dependencies are a separate path to each fault, and each gets a case.
MANIFESTS = {
    "stacks": BROKEN_MANIFEST,
    "core-missing": core_fault("base-nowhere"),
    "core-self": core_fault("base-a"),
    "core-through-stack": core_fault("stack-valid"),
}

BROKEN_CASES = [
    ("stacks", "stack-valid", 0, "templates/fixture/stack.md"),
    ("stacks", "stack-missing", 1,
     "Missing dependency: stack-missing depends on base-nowhere"),
    ("stacks", "stack-cycle", 1,
     "Dependency cycle: base-b -> base-c -> base-b"),
    ("core-missing", "stack-valid", 1,
     "Missing dependency: base-a depends on base-nowhere"),
    ("core-self", "stack-valid", 1, "Dependency cycle: base-a -> base-a"),
    ("core-through-stack", "stack-valid", 1,
     "Dependency cycle: base-a -> stack-valid -> base-a"),
]

RESOLVE_WITH = (
    "import sys; sys.path.insert(0, sys.argv[1]); import resolve_chain; "
    "resolve_chain.MANIFEST = sys.argv[2]; "
    "sys.argv = ['resolve_chain.py', sys.argv[3]]; "
    "resolve_chain.main()"
)


def _resolve_cases(manifests, cases):
    """Resolve each case's root in its planted manifest; return the misses.

    A case is (manifest name, root, owed exit status, phrase the output owes),
    optionally followed by a phrase the output MUST NOT carry.
    """
    import tempfile

    failures = []
    with tempfile.TemporaryDirectory() as scratch:
        for name, text in manifests.items():
            with io.open(os.path.join(scratch, name + ".yaml"), "w",
                         encoding="utf-8", newline="\n") as handle:
                handle.write(text)

        for name, root, want_code, want_phrase, *absent in cases:
            manifest = os.path.join(scratch, name + ".yaml")
            case = f"{root} in {name}"
            proc = subprocess.run(
                [sys.executable, "-c", RESOLVE_WITH,
                 os.path.join(ROOT, "tools"), manifest, root],
                capture_output=True, text=True, encoding="utf-8",
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


def check_sys_19():
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
    "    depends_on: [fork-lib]\n")

FORK_CHAIN = "\n".join([
    "templates/core/quality.md", "templates/core/docs.md",
    "templates/core/git.md", "templates/fixture/stack.md"])

FORK_CASES = [
    ("fork", "stack-fork", 0, "templates/core/quality.md"),
    ("fork", "stack-fork", 0, "templates/core/git.md"),
    ("fork", "stack-fork", 0, "templates/core/docs.md"),
    ("fork", "stack-fork", 0, FORK_CHAIN, "templates/core/testing.md"),
    ("fork-outside", "stack-fork", 1,
     "Core-tier entry fork-readme depends on fork-lib, which is outside the "
     "core tier"),
]


def check_sys_21():
    seen = Inspected()
    seen.count("fork-manifest cases", FORK_CASES)
    failures = _resolve_cases({"fork": FORK_MANIFEST,
                               "fork-outside": FORK_OUTSIDE_MANIFEST},
                              FORK_CASES)
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


def upstream_key_edits(was, now):
    """Each edit to an upstream-owned manifest key, as one finding."""
    found = []
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
            fields = sorted(k for k in set(old[eid]) | set(new[eid])
                            if old[eid].get(k) != new[eid].get(k))
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
    ("a stack and a platform appended, and a key of the fork's own",
     OWNED_BASE + """  - id: stack-b
    file: templates/stack/b.md
platform:
  - id: platform-b
    file: templates/platform/b.md
fork:
  - id: fork-note
""", []),
    ("the core tier edited",
     OWNED_BASE.replace("core: [base-a]", "core: [base-a, backend-a]"),
     ["core: ['base-a'] became ['base-a', 'backend-a']"]),
    ("an upstream entry changed",
     OWNED_BASE.replace("depends_on: [base-a]", "depends_on: []"),
     ["backend: backend-a changed (depends_on)"]),
    ("an entry added under an upstream key",
     OWNED_BASE.replace("frontend: []", """frontend:
  - id: frontend-b
    file: templates/frontend/b.md"""),
     ["frontend: frontend-b added"]),
    ("an upstream entry removed",
     OWNED_BASE.replace("""  - id: backend-a
    file: templates/backend/http.md
    depends_on: [base-a]
""", ""),
     ["backend: backend-a removed"]),
]


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, encoding="utf-8")


def fork_baseline(repo, ref):
    """The manifest the fork in `repo` last merged from `ref`.

    Returns (text, basis, refusal): the manifest text and a line naming
    where it came from, or a refusal naming why no baseline exists.
    """

    # A ref that does not resolve and a ref with no shared history are
    # different faults with different remedies -- fetch upstream, or point
    # at the right one -- so each is named as itself.
    resolved = _git(repo, "rev-parse", "--verify", "--quiet",
                    f"{ref}^{{commit}}")
    if resolved.returncode != 0:
        return None, None, (
            f"{UPSTREAM_REF_ENV}={ref} names no commit in this repository, "
            f"so there is no upstream to compare with; fetch it first")
    merged = _git(repo, "merge-base", "HEAD", ref)
    if merged.returncode != 0:
        return None, None, (
            f"{UPSTREAM_REF_ENV}={ref} shares no history with HEAD, so the "
            f"revision the fork last merged is unknown")
    revision = merged.stdout.strip()
    shown = _git(repo, "show", f"{revision}:templates/manifest.yaml")
    if shown.returncode != 0:
        return None, None, (f"the manifest at {revision[:12]} could not be "
                            f"read: {shown.stderr.strip()}")
    return shown.stdout, (f"  baseline: the merge base {revision[:12]} of "
                          f"HEAD and {ref}"), None


# The git path, planted. Upstream sets no ref, so its own run never reaches
# that path, and a fork's run reaches it only in the passing direction. Each
# case is (label, the ref the fork names, the findings or the refusal owed),
# run in order against one throwaway repository whose `upstream` branch is
# OWNED_BASE and whose HEAD is the fork.
GIT_CASES = [
    ("a fork that only appended since its last merge", "upstream", []),
    ("a fork that edited the core tier since its last merge", "upstream",
     ["core: ['base-a'] became ['base-a', 'backend-a']"]),
    ("a ref that names no commit", "upstream/missing", "names no commit"),
    ("a ref with no history in common", "unrelated", "shares no history"),
]


def _git_cases():
    """Run GIT_CASES; return a failure line per case that missed."""
    import tempfile

    manifest = os.path.join("templates", "manifest.yaml")
    edits = {
        GIT_CASES[0][0]: OWNED_BASE + "  - id: stack-b\n"
                                      "    file: templates/stack/b.md\n",
        GIT_CASES[1][0]: OWNED_BASE.replace(
            "core: [base-a]", "core: [base-a, backend-a]") +
            "  - id: stack-b\n    file: templates/stack/b.md\n",
    }
    failures = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as repo:

        def commit(text, message):
            # Each commit MUST change the manifest, or the case after it
            # reads the state before it and passes for the wrong reason.
            path = os.path.join(repo, manifest)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            _git(repo, "add", manifest)
            done = _git(repo, "commit", "-q", "-m", message)
            if done.returncode != 0:
                raise RuntimeError(f"planted commit {message!r} failed: "
                                   f"{done.stderr.strip()}")

        _git(repo, "init", "-q")
        for key, value in (("core.autocrlf", "false"),
                           ("user.name", "smoke"),
                           ("user.email", "smoke@localhost")):
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
                    failures.append(f"  planted git, {label}: refused "
                                    f"{refused!r}, owed {owed!r}")
                continue
            if refused:
                failures.append(f"  planted git, {label}: refused {refused!r}")
                continue
            with io.open(os.path.join(repo, manifest),
                         encoding="utf-8") as f:
                now = f.read()
            got = upstream_key_edits(yaml.safe_load(was), yaml.safe_load(now))
            if got != owed:
                failures.append(f"  planted git, {label}: found {got}, "
                                f"owed {owed}")
    return failures


def check_sys_20():
    if not HAS_YAML:
        return [MISSING_YAML]

    seen = Inspected()
    failures = []

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
        was_text, basis, refused = fork_baseline(ROOT, ref)
        if refused:
            failures.append(f"  {refused}")
            return seen.failures() + failures, seen.notes()
    else:
        was_text = now_text
        basis = (f"  baseline: {UPSTREAM_REF_ENV} is unset, so this is "
                 f"upstream and the manifest is compared with itself")

    was, now = yaml.safe_load(was_text), yaml.safe_load(now_text)
    seen.count("upstream keys compared",
               [k for k in UPSTREAM_KEYS if k in was])
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
    ("a live replacement", """base:
  - {id: base-old, file: a.md, deprecated: base-new}
  - {id: base-new, file: b.md}
""", []),
    ("a replacement that does not exist", """base:
  - {id: base-old, file: a.md, deprecated: base-gone}
""", ["base-old names base-gone, which no entry carries"]),
    ("a replacement that is deprecated too", """base:
  - {id: base-old, file: a.md, deprecated: base-mid}
  - {id: base-mid, file: b.md, deprecated: base-new}
  - {id: base-new, file: c.md}
""", ["base-old names base-mid, which is deprecated too"]),
    ("a field that names no ID", """base:
  - {id: base-old, file: a.md, deprecated: true}
""", ["base-old carries deprecated: True, which names no ID"]),
]


def deprecation_findings(manifest):
    """Each deprecation that names no live replacement, as one finding."""
    entries = [e for v in manifest.values() if isinstance(v, list)
               for e in v if isinstance(e, dict) and "id" in e]
    by_id = {e["id"]: e for e in entries}
    found = []
    for entry in entries:
        if "deprecated" not in entry:
            continue
        target = entry["deprecated"]
        if not isinstance(target, str):
            found.append(f"{entry['id']} carries deprecated: {target}, "
                         f"which names no ID")
        elif target not in by_id:
            found.append(f"{entry['id']} names {target}, which no entry "
                         f"carries")
        elif "deprecated" in by_id[target]:
            found.append(f"{entry['id']} names {target}, which is "
                         f"deprecated too")
    return found


def check_sys_22():
    if not HAS_YAML:
        return [MISSING_YAML]

    seen = Inspected()
    failures = []
    seen.count("planted manifests", DEPRECATION_CASES)
    for label, text, want in DEPRECATION_CASES:
        got = deprecation_findings(yaml.safe_load(text))
        if got != want:
            failures.append(f"  planted, {label}: found {got}, owed {want}")

    manifest = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    marked = [e for v in data.values() if isinstance(v, list)
              for e in v if isinstance(e, dict) and "deprecated" in e]
    seen.count("deprecated entries in the manifest", marked, floor=0)
    for finding in deprecation_findings(data):
        failures.append(f"  {finding}")
    return seen.failures() + failures, seen.notes()
