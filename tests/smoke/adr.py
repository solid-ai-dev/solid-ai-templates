"""Smoke checks of the ADR family: decision-record frontmatter.
"""

import os
import re

from testkit import ROOT
from .common import HAS_YAML, Inspected, MISSING_YAML, read, yaml


# ---------------------------------------------------------------------------
# ADR-01 — ADR frontmatter schema enforcement
# ---------------------------------------------------------------------------
# Enforces the schema docs/decisions/010-adr-governance.md introduced,
# with the two statuses added since:
# - frontmatter present and parses as YAML
# - id is 3-digit string matching filename leading digits
# - status in closed set: Proposed | Accepted | Superseded | Rejected |
#   Withdrawn
# - date present in YYYY-MM-DD form
# - category in closed set
# - supersedes / superseded_by present (empty list allowed)
# - reciprocal-link consistency
# - status=Superseded iff superseded_by non-empty

ADR_STATUSES = {"Proposed", "Accepted", "Superseded", "Rejected", "Withdrawn"}
ADR_CATEGORIES = {"composition", "templates", "tooling", "process", "release"}
ADR_FILENAME = re.compile(r"^(\d{3})-[a-z0-9-]+\.md$")
ADR_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ADR_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def _parse_adr(filepath, content):
    """Return (frontmatter dict, list of failures) for a single ADR file."""
    rel = os.path.relpath(filepath, ROOT).replace(os.sep, "/")
    fm_match = ADR_FRONTMATTER.match(content)
    if not fm_match:
        return None, [f"  {rel}: missing YAML frontmatter block"]
    try:
        data = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        return None, [f"  {rel}: frontmatter is not valid YAML ({e})"]
    if not isinstance(data, dict):
        return None, [f"  {rel}: frontmatter did not parse as a mapping"]
    return data, []


def check_adr_01():
    if not HAS_YAML:
        return [MISSING_YAML]

    failures = []
    seen = Inspected()
    decisions_dir = os.path.join(ROOT, "docs", "decisions")
    if not os.path.isdir(decisions_dir):
        return ["  docs/decisions/ does not exist — the check inspects nothing"]

    # id (str) -> (rel_path, frontmatter dict)
    parsed = {}

    numbered = 0
    for name in sorted(os.listdir(decisions_dir)):
        m = ADR_FILENAME.match(name)
        if not m:
            # template.md and any non-numbered files are skipped
            continue
        numbered += 1
        filepath = os.path.join(decisions_dir, name)
        rel = os.path.relpath(filepath, ROOT).replace(os.sep, "/")
        content = read(filepath)

        data, errs = _parse_adr(filepath, content)
        failures.extend(errs)
        if data is None:
            continue

        expected_id = m.group(1)
        adr_id = data.get("id")

        # id MUST be a quoted string in the YAML — otherwise leading-zero
        # values (010) are parsed by YAML 1.1 as octal integers (010 -> 8).
        # Detect this case explicitly so the error message points at the
        # quoting fix, not a confusing numeric mismatch.
        if not isinstance(adr_id, str):
            failures.append(
                f"  {rel}: id {adr_id!r} is not a string — quote it as "
                f"\"{expected_id}\" to avoid YAML octal parsing"
            )
        elif adr_id != expected_id:
            failures.append(
                f"  {rel}: id {adr_id!r} does not match filename leading "
                f"digits ({expected_id})"
            )

        status = data.get("status")
        if status not in ADR_STATUSES:
            failures.append(
                f"  {rel}: status {status!r} not in {sorted(ADR_STATUSES)}"
            )

        date = str(data.get("date") or "")
        if not ADR_DATE.match(date):
            failures.append(
                f"  {rel}: date {data.get('date')!r} is not YYYY-MM-DD"
            )

        category = data.get("category")
        if category not in ADR_CATEGORIES:
            failures.append(
                f"  {rel}: category {category!r} not in {sorted(ADR_CATEGORIES)}"
            )

        for field in ("supersedes", "superseded_by"):
            if field not in data:
                failures.append(f"  {rel}: missing field {field!r}")
            elif not isinstance(data[field], list):
                failures.append(
                    f"  {rel}: {field} must be a list "
                    f"(got {type(data[field]).__name__})"
                )

        supersedes = data.get("superseded_by") or []
        if supersedes and status != "Superseded":
            failures.append(
                f"  {rel}: superseded_by is non-empty but status is "
                f"{status!r} — must be 'Superseded'"
            )

        # Index by expected_id (filename digits) — falls back gracefully if
        # the frontmatter id is wrong, so reciprocal-link checks still run.
        parsed[expected_id] = (rel, data)

    # Reciprocal-link consistency — pass 2 once every ADR is parsed.
    # Supersedes/superseded_by entries MUST also be quoted strings.
    def _normalize_ids(values):
        return [str(v) for v in (values or [])]

    for adr_id, (rel, data) in parsed.items():
        for other_id in _normalize_ids(data.get("supersedes")):
            other = parsed.get(other_id)
            if other is None:
                failures.append(
                    f"  {rel}: supersedes references unknown ADR {other_id!r}"
                )
                continue
            other_rel, other_data = other
            back = _normalize_ids(other_data.get("superseded_by"))
            if adr_id not in back:
                failures.append(
                    f"  {rel}: supersedes {other_id!r} but {other_rel} "
                    f"does not list {adr_id!r} in superseded_by"
                )

        for other_id in _normalize_ids(data.get("superseded_by")):
            other = parsed.get(other_id)
            if other is None:
                failures.append(
                    f"  {rel}: superseded_by references unknown ADR {other_id!r}"
                )
                continue
            other_rel, other_data = other
            forward = _normalize_ids(other_data.get("supersedes"))
            if adr_id not in forward:
                failures.append(
                    f"  {rel}: superseded_by {other_id!r} but {other_rel} "
                    f"does not list {adr_id!r} in supersedes"
                )

    seen.count("decision records with a numbered filename", numbered)
    seen.count("records whose frontmatter parsed", len(parsed))
    return seen.failures() + failures, seen.notes()
