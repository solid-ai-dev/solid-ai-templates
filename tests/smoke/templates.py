"""Smoke checks of the TPL family: section IDs and the EXTEND and OVERRIDE
directives that name them.
"""

import os
import re

from testkit import ROOT, template_files
from .common import (
    _load_manifest, _opt_in_roots, _resolve_stack, _roots_by_kind, _stacks,
    all_template_files, depends_on_refs, HAS_YAML, Inspected,
    iter_id_declarations, MISSING_YAML, read)


# ---------------------------------------------------------------------------
# TPL-04 — all EXTEND/OVERRIDE refs point to existing IDs
# ---------------------------------------------------------------------------

def check_tpl_04():
    failures = []
    seen = Inspected()
    ref_pattern = re.compile(r'\[(EXTEND|OVERRIDE):\s*([^\]]+)\]')

    declared = set()
    files = seen.count("template files scanned", all_template_files())
    for filepath in files:
        content = read(filepath)
        for sid, _ in iter_id_declarations(content):
            declared.add(sid)
    seen.count("section IDs declared", len(declared))

    directives = 0
    for filepath in files:
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT)
        for match in ref_pattern.finditer(content):
            directives += 1
            directive = match.group(1)
            ref_id = match.group(2).strip()
            if ref_id not in declared:
                failures.append(
                    f"  {rel}: [{directive}: {ref_id}] — ID not declared"
                )

    seen.count("EXTEND/OVERRIDE directives checked", directives)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-01 — DEPENDS ON chain from the fixture stack is complete
# ---------------------------------------------------------------------------

def _collect_chain(rel_path, visited=None):
    if visited is None:
        visited = set()
    if rel_path in visited:
        return visited
    visited.add(rel_path)
    abs_path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(abs_path):
        return visited
    for dep in depends_on_refs(read(abs_path)):
        _collect_chain(dep, visited)
    return visited


def check_tpl_01():
    failures = []

    # The fixture, not a real stack: it is the one stack upstream keeps, so
    # the check keeps its input in a tree that ships no stack of its own.
    chain = _collect_chain("templates/fixture/stack.md")
    required = [
        "templates/core/quality.md",
        "templates/core/git.md",
        "templates/core/testing.md",
        "templates/core/config.md",
        "templates/core/quality-gates.md",
        "templates/security/security.md",
    ]
    seen = Inspected()
    seen.count("files in the fixture chain", len(chain))
    seen.count("files required to be in it", len(required))

    for req in required:
        if req not in chain:
            failures.append(f"  fixture/stack.md chain missing: '{req}'")
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-02 — EXTEND adds rules without removing base rules
# ---------------------------------------------------------------------------

def _extract_section(filepath, section_id):
    content = read(filepath)
    lines = content.splitlines()
    result = []
    in_section = False
    tag = f"[ID: {section_id}]"
    extend_tag = f"[EXTEND: {section_id}]"
    override_tag = f"[OVERRIDE: {section_id}]"

    for i, line in enumerate(lines):
        if tag in line or extend_tag in line or override_tag in line:
            in_section = True
            continue
        if in_section:
            has_content = any(l.strip() for l in result)
            if re.match(r'^#{1,4} ', line) and has_content:
                break
            if re.match(r'^\[(ID|EXTEND|OVERRIDE|DEPENDS):', line) and has_content:
                break
            result.append(line)

    return [l for l in result if l.strip()]


def check_tpl_02():
    failures = []
    seen = Inspected()

    base_content = _extract_section(
        os.path.join(ROOT, "templates", "core", "testing.md"), "base-testing"
    )
    if not base_content:
        failures.append("  core/testing.md [ID: base-testing] section is empty")

    extension = _extract_section(
        os.path.join(ROOT, "templates", "fixture", "stack.md"),
        "base-testing-general"
    )
    if not extension:
        failures.append(
            "  fixture/stack.md [EXTEND: base-testing-general] section is "
            "empty — base rules may have been lost"
        )

    seen.count("sections extracted", 2)
    seen.count("lines read from base-testing", len(base_content), floor=0)
    seen.count("lines read from the fixture's extension",
               len(extension), floor=0)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-03 — OVERRIDE replaces parent section entirely
# ---------------------------------------------------------------------------

def check_tpl_03():
    failures = []
    seen = Inspected()

    original = _extract_section(
        os.path.join(ROOT, "templates", "core", "testing.md"),
        "testing-container-e2e"
    )
    override = _extract_section(
        os.path.join(ROOT, "templates", "fixture", "stack.md"),
        "testing-container-e2e"
    )

    if not original:
        failures.append(
            "  core/testing.md [ID: testing-container-e2e] section is empty")
    if not override:
        failures.append(
            "  fixture/stack.md [OVERRIDE: testing-container-e2e] section is "
            "empty"
        )
    if original and override and original == override:
        failures.append(
            "  [OVERRIDE: testing-container-e2e] content is identical to the "
            "original [ID: testing-container-e2e] — override has no effect"
        )

    seen.count("sections extracted", 2)
    seen.count("lines read from the original", len(original), floor=0)
    seen.count("lines read from the override", len(override), floor=0)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-06 — EXTEND/OVERRIDE targets reachable in resolved chain
# ---------------------------------------------------------------------------

def check_tpl_06():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    ref_pattern = re.compile(r'\[(EXTEND|OVERRIDE):\s*([^\]]+)\]')
    failures = []
    seen = Inspected()

    stacks = seen.count("stacks resolved", [e["id"] for e in _stacks(entries)])

    # A stack is not the only root a project resolves. Extras and the platform
    # are chosen independently of the stack, so what guarantees their EXTEND
    # target is their own chain -- the core tier plus their dependency tree --
    # and not whichever stack they are paired with. Resolving stacks alone
    # left every opt-in template unexamined, which is how two platform files
    # came to extend a section carried by one chain in seventeen.
    opt_in = seen.count("opt-in roots resolved",
                        _opt_in_roots(core_ids, entries))

    directives = 0
    for sid in list(stacks) + list(opt_in):
        chain_files, _ = _resolve_stack(sid, core_ids, entries)

        # Collect all IDs declared in chain files
        chain_ids = set()
        for f in chain_files:
            content = read(os.path.join(ROOT, f))
            for chain_sid, _ in iter_id_declarations(content):
                chain_ids.add(chain_sid)

        # Check EXTEND/OVERRIDE targets in chain files
        for f in chain_files:
            content = read(os.path.join(ROOT, f))
            rel = f.replace("\\", "/")
            for match in ref_pattern.finditer(content):
                directives += 1
                directive = match.group(1)
                ref_id = match.group(2).strip()
                if ref_id not in chain_ids:
                    failures.append(
                        f"  {sid}: {rel} [{directive}: {ref_id}]"
                        f" — target not in resolved chain"
                    )

    seen.count("directives checked in a resolved chain", directives)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-07 — EXTEND sections do not duplicate parent rules
# ---------------------------------------------------------------------------

def _extract_bullets(filepath, section_id):
    """Return list of bullet-point texts from the section tagged with ID."""
    content = read(filepath)
    lines = content.splitlines()
    bullets = []
    in_section = False
    tag = f"[ID: {section_id}]"

    for line in lines:
        if tag in line:
            in_section = True
            continue
        if in_section:
            if re.match(r'^#{1,4} ', line) and bullets:
                break
            if re.match(r'^\[(ID|EXTEND|OVERRIDE|DEPENDS):', line) and bullets:
                break
            stripped = line.strip()
            if stripped.startswith('- '):
                bullets.append(stripped[2:].strip())

    return bullets


def _word_set(text):
    """Return set of lowercase words (3+ chars) from text."""
    return {w.lower() for w in re.findall(r'[a-zA-Z]{3,}', text)}


def check_tpl_07():
    if not HAS_YAML:
        return [MISSING_YAML]

    extend_pattern = re.compile(r'^\[EXTEND:\s*([^\]]+)\]', re.MULTILINE)
    failures = []
    seen = Inspected()

    # Build ID → file map
    id_to_file = {}
    files = seen.count("template files scanned", all_template_files())
    for filepath in files:
        content = read(filepath)
        for sid, _ in iter_id_declarations(content):
            id_to_file[sid] = filepath

    # For each EXTEND, compare child bullets against parent bullets
    compared = 0
    for filepath in files:
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
        for match in extend_pattern.finditer(content):
            parent_id = match.group(1).strip()
            parent_file = id_to_file.get(parent_id)
            if not parent_file:
                continue

            parent_bullets = _extract_bullets(parent_file, parent_id)
            if not parent_bullets:
                continue
            compared += 1

            # Find the child section that contains this EXTEND
            child_lines = content.splitlines()
            extend_line = match.start()
            char_count = 0
            extend_lineno = 0
            for i, line in enumerate(child_lines):
                char_count += len(line) + 1
                if char_count > extend_line:
                    extend_lineno = i
                    break

            # Collect child bullets after the EXTEND line
            child_bullets = []
            for line in child_lines[extend_lineno + 1:]:
                if re.match(r'^#{1,4} ', line) and child_bullets:
                    break
                if re.match(r'^\[(ID|EXTEND|OVERRIDE|DEPENDS):', line):
                    break
                stripped = line.strip()
                if stripped.startswith('- '):
                    child_bullets.append(stripped[2:].strip())

            # Compare each child bullet against parent bullets
            for cb in child_bullets:
                cb_words = _word_set(cb)
                if len(cb_words) < 3:
                    continue
                for pb in parent_bullets:
                    pb_words = _word_set(pb)
                    if len(pb_words) < 3:
                        continue
                    intersection = cb_words & pb_words
                    union = cb_words | pb_words
                    if union and len(intersection) / len(union) >= 0.7:
                        failures.append(
                            f"  {rel} [EXTEND: {parent_id}]: "
                            f"possible duplicate — \"{cb[:60]}...\""
                        )
                        break

    seen.count("EXTEND sections compared against a parent", compared)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-10 -- at most one OVERRIDE of a given ID per resolved chain
# ---------------------------------------------------------------------------

# The spec's conflict table calls two templates overriding one ID an error the
# agent MUST surface. TPL-03, TPL-04 and TPL-06 check that an EXTEND or
# OVERRIDE target exists and is reachable; none checks multiplicity, so the
# error the spec names is one no tool reports. A chain that carries two
# replacements of one section leaves the agent to pick, and the resolved
# file states both.
#
# The way a three-level chain specialises without colliding is the pattern
# go-lib -> go-service -> go-echo already uses: a section that overrides
# declares an [ID:] of its own, and the next level overrides that.

def check_tpl_10():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    override_pattern = re.compile(r'\[OVERRIDE:\s*([^\]]+)\]')
    failures = []
    seen = Inspected()

    stack_roots, opt_in_roots = _roots_by_kind(core_ids, entries)
    seen.count("stacks resolved", stack_roots)

    # An opt-in root resolves its own chain, so a collision inside one is
    # invisible to a scan of stacks alone.
    seen.count("opt-in roots resolved", opt_in_roots)

    overrides = 0
    for sid in list(stack_roots) + list(opt_in_roots):
        chain_files, _ = _resolve_stack(sid, core_ids, entries)

        # rel path -> the IDs it overrides, in chain order
        overridden = {}
        for f in chain_files:
            rel = f.replace("\\", "/")
            content = read(os.path.join(ROOT, f))
            for match in override_pattern.finditer(content):
                target = match.group(1).strip()
                overrides += 1
                overridden.setdefault(target, []).append(rel)

        for target, homes in sorted(overridden.items()):
            if len(homes) > 1:
                failures.append(
                    f"  {sid}: `{target}` is overridden by "
                    f"{len(homes)} templates ({', '.join(homes)}) — spec "
                    f"calls this an error and states no winner. Give the "
                    f"earlier override an [ID:] of its own and have the "
                    f"later one override that"
                )

    seen.count("OVERRIDE directives read in a resolved chain", overrides)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-08 — every core template has at least one [ID:] tag
# ---------------------------------------------------------------------------

# The concern directories the check is pointed at. Their files come from
# git, so a template added to one is inspected without this list being
# edited; the list survives to make an emptied directory a finding.
CORE_DIRS = [
    "templates/core",
    "templates/security",
    "templates/infra",
    "templates/data",
]


def check_tpl_08():
    failures = []
    seen = Inspected()
    seen.count("directories the check is pointed at", len(CORE_DIRS))

    base_files = seen.count("files inspected for an [ID:] tag",
                            [path for d in CORE_DIRS
                             for path in template_files(d + "/")])

    # A directory that is not there is a finding, not a skip. Skipping it
    # makes a rename silent: every listed directory disappears and the
    # check reports the same pass as a clean tree.
    for d in CORE_DIRS:
        if not any(rel.startswith(d + "/") for rel in base_files):
            failures.append(
                f"  {d}: listed directory holds no template — the check "
                f"inspects nothing in it"
            )

    for rel in base_files:
        content = read(os.path.join(ROOT, rel.replace("/", os.sep)))
        if not any(True for _ in iter_id_declarations(content)):
            failures.append(f"  {rel}: missing [ID:] tag")

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# TPL-09 — no empty [ID:] sections
# ---------------------------------------------------------------------------

def check_tpl_09():
    failures = []
    seen = Inspected()
    meta_pattern = re.compile(r'^\[(DEPENDS ON|EXTEND|OVERRIDE):')
    next_id_pattern = re.compile(r'^\s*\[ID:')

    sections = 0
    for filepath in seen.count("template files scanned",
                               all_template_files()):
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT).replace(os.sep, "/")
        lines = content.splitlines()

        # Map declaration line numbers → section IDs (sole-line only).
        decls = {lineno: sid for sid, lineno in iter_id_declarations(content)}

        for i, line in enumerate(lines):
            section_id = decls.get(i + 1)
            if not section_id:
                continue
            sections += 1

            # Check for any non-blank content before the next [ID:]
            # tag. Skip metadata lines ([DEPENDS ON:], [EXTEND:],
            # [OVERRIDE:]) that accompany this section's [ID:].
            # Sub-headings count as content.
            has_content = False
            for subsequent in lines[i + 1:]:
                stripped = subsequent.strip()
                if not stripped:
                    continue
                if next_id_pattern.match(stripped):
                    break
                if meta_pattern.match(stripped):
                    continue
                has_content = True
                break

            if not has_content:
                failures.append(
                    f"  {rel}: [ID: {section_id}] section is empty"
                )

    seen.count("[ID:] sections inspected", sections)
    return seen.failures() + failures, seen.notes()
