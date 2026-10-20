"""Smoke checks of the MNF family: manifest entries and the chains they
resolve to.
"""

import io
import os
import sys

from testkit import ROOT
from .common import (
    _load_manifest, _resolve_stack, _stacks, HAS_YAML, Inspected, MISSING_YAML,
    read, yaml)


# ---------------------------------------------------------------------------
# MNF-01 — manifest entries reference valid paths and IDs
# ---------------------------------------------------------------------------

def check_mnf_01():
    if not HAS_YAML:
        return [MISSING_YAML]

    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    if not os.path.isfile(manifest_path):
        return ["  manifest.yaml not found"]

    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    failures = []
    seen = Inspected()
    declared_ids = set()
    entries = []

    # Every declaration of each ID, as (section, file). The resolver keys
    # entries by ID, so a second declaration would silently replace the
    # first; a fork adding an ID upstream later adds too must fail here.
    declarations = {}
    for key, section in manifest.items():
        if isinstance(section, list):
            for entry in section:
                if isinstance(entry, dict):
                    entries.append(entry)
                    if "id" in entry:
                        declared_ids.add(entry["id"])
                        declarations.setdefault(entry["id"], []).append(
                            (key, entry.get("file", "?")))

    seen.count("manifest entries read", len(entries))
    seen.count("IDs declared in the manifest", len(declared_ids))

    for eid, places in declarations.items():
        if len(places) > 1:
            where = ", ".join(f"{key}: {path}" for key, path in places)
            failures.append(
                f"  ID '{eid}' declared {len(places)} times — {where}")

    for entry in entries:
        path = entry.get("file", "")
        if path and not os.path.isfile(os.path.join(ROOT, path)):
            failures.append(f"  file not found: '{path}' (id: {entry.get('id', '?')})")

    deps_checked = 0
    for entry in entries:
        for dep in entry.get("depends_on", []):
            deps_checked += 1
            if dep not in declared_ids:
                failures.append(
                    f"  depends_on '{dep}' in '{entry.get('id', '?')}' "
                    f"— ID not declared in manifest"
                )

    seen.count("depends_on references checked", deps_checked)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# MNF-02 — all stacks resolve to valid, non-empty file lists
# ---------------------------------------------------------------------------

def check_mnf_02():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []
    seen = Inspected()

    stacks = seen.count("stacks resolved", _stacks(entries))

    resolved = 0
    for stack in stacks:
        sid = stack["id"]
        files, _ = _resolve_stack(sid, core_ids, entries)

        if not files:
            failures.append(f"  {sid}: resolution produced empty file list")
            continue

        for f in files:
            resolved += 1
            path = os.path.join(ROOT, f)
            if not os.path.isfile(path):
                failures.append(f"  {sid}: resolved file missing: {f}")
            elif os.path.getsize(path) == 0:
                failures.append(f"  {sid}: resolved file empty: {f}")

    seen.count("resolved files inspected", resolved)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# MNF-03 — all resolved chains include core tier files
# ---------------------------------------------------------------------------

def check_mnf_03():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []
    seen = Inspected()

    stacks = seen.count("stacks resolved", _stacks(entries))
    seen.count("core tier IDs required of each", len(core_ids))

    for stack in stacks:
        sid = stack["id"]
        _, resolved_ids = _resolve_stack(sid, core_ids, entries)

        for cid in core_ids:
            if cid not in resolved_ids:
                failures.append(
                    f"  {sid}: core ID '{cid}' missing from "
                    f"resolved chain"
                )

    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# MNF-04 — prompt builds for all stacks
# ---------------------------------------------------------------------------

def check_mnf_04():
    if not HAS_YAML:
        return [MISSING_YAML]

    core_ids, entries, _ = _load_manifest()
    failures = []

    output_file = "templates/core/agents.md"
    output_path = os.path.join(ROOT, output_file)
    if not os.path.isfile(output_path):
        return [f"  output format missing: {output_file}"]

    output_fmt = read(output_path)
    seen = Inspected()

    stacks = seen.count("stacks resolved", _stacks(entries))

    built = 0
    for stack in stacks:
        sid = stack["id"]
        files, _ = _resolve_stack(sid, core_ids, entries)

        try:
            parts = []
            for f in files:
                parts.append(read(os.path.join(ROOT, f)))
            prompt = "\n\n".join(parts) + "\n\n" + output_fmt
        except Exception as e:
            failures.append(f"  {sid}: prompt build failed: {e}")
            continue

        if len(prompt) < 500:
            failures.append(
                f"  {sid}: prompt suspiciously short "
                f"({len(prompt)} chars)"
            )
        built += 1

    seen.count("prompts built", built)
    return seen.failures() + failures, seen.notes()


# ---------------------------------------------------------------------------
# MNF-05 — resolve_chain.py resolution matches the PyYAML resolution
# ---------------------------------------------------------------------------
# The user-facing tools/resolve_chain.py uses a stdlib-only hand-rolled manifest
# parser; smoke (and the manifest's own semantics) use PyYAML. A divergence
# between the two — e.g. the multi-line depends_on bug, #654 — ships a wrong
# generated/ chain that `resolve_chain.py --check` cannot catch, since it only
# verifies self-consistency against the same parser. This gate resolves every
# stack with BOTH parsers and fails on any mismatch, so the two can never
# silently drift again regardless of which parser is edited next.

def check_mnf_05():
    if not HAS_YAML:
        return [MISSING_YAML]

    tools_dir = os.path.join(ROOT, "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    try:
        import resolve_chain as resolve_tool
    except Exception as e:
        return [f"  cannot import tools/resolve_chain.py: {e}"]

    core_h, entries_h, stacks = resolve_tool.load_manifest()
    core_y, entries_y, _ = _load_manifest()

    failures = []
    seen = Inspected()
    stacks = seen.count("stacks resolved with both parsers", stacks)
    for stack in stacks:
        sid = stack["id"]
        hand = resolve_tool.resolve_chain(sid, core_h, entries_h)
        ref, _ = _resolve_stack(sid, core_y, entries_y)
        if hand == ref:
            continue
        missing = [f for f in ref if f not in hand]
        extra = [f for f in hand if f not in ref]
        parts = []
        if missing:
            parts.append(f"missing from resolve_chain.py: {', '.join(missing)}")
        if extra:
            parts.append(f"extra in resolve_chain.py: {', '.join(extra)}")
        if not parts:
            parts.append("same files, different order")
        failures.append(
            f"  {sid}: resolve_chain.py chain != PyYAML chain — "
            f"{'; '.join(parts)}"
        )

    return seen.failures() + failures, seen.notes()
