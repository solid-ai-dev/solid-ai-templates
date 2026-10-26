"""Build a project's root context file and its task skills from a chain.

Each template section declares its load (spec, chapter 8.1; ADR-058): no
directive loads on every turn, a kind of task loads in that kind's skill,
and `check` loads as the check that enforces it. This module resolves the
chain's overrides, places every section by its load, and copies rule text
unchanged, so the same chain and the same declined list always give
byte-identical files. The project's facts are slots the agent or the
interview fills, and a regeneration keeps what was filled.

Run it through the resolver:

    py tools/resolve_chain.py --emit <out-dir> <root> [<root> ...]
        [--declined <file>] [--inline-skills] [--mirror <dir>]
"""

import io
import os
import re

from resolve_chain import (
    FENCE_LINE, HEADING_LINE, LOAD_CHECK, TAG_LINE, load_directives)

SKILLS_DIR = ".agents/skills"
ROOT_FILE = "AGENTS.md"
RULES_HEADING = "## Rules"

# Every file the emitter wrote last time, so a rerun can remove a skill it
# no longer emits without touching a file it never wrote.
RECORD = ".agents/emitted.txt"

BULLET_LINE = re.compile(r"^(\s*)(?:[-*+]|\d+\.)\s")
ID_TAG = re.compile(r"^\[ID:\s*([^\]]+?)\s*\]$")
OVERRIDE_TAG = re.compile(r"^\[OVERRIDE:\s*([^\]]+?)\s*\]$")

# The facts no template knows: the agent or the interview replaces each
# slot, and nothing else in the file.
FACTS = """# {{project-name}}

{{one-sentence description}}

- Model: root and skills
- Owner: {{owner}}
- Repository: {{repository}}

## Commands

{{the commands to build, test and run the project}}

## Answers

- Who approves a change: {{approver}}
- How work is tracked: {{tracker}}
- What a release is: {{release}}
"""


class EmitError(Exception):
    """An emission refused rather than written."""


def _blocks(text):
    """The file's lines, each a dict describing where it sits.

    Keys: `line`; the `path` of (level, text) headings above it; its `load`
    (the nearest on that path, or None for every turn) and the `anchor`
    level of the heading that set it; the `section` ID it belongs to, a
    section running from its `[ID:]` to the next; and whether it is a tag
    line, a heading, or a fence line or inside one.
    """
    loads = {d["heading"]: d["kind"] for d in load_directives(text)
             if d["placed"]}
    out, stack, fence, section = [], [], None, None
    for number, line in enumerate(text.splitlines(), start=1):
        run = FENCE_LINE.match(line)
        in_fence = fence is not None
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
        heading = None if (in_fence or run) else HEADING_LINE.match(line)
        if heading:
            level = len(heading.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, line[level:].strip(), loads.get(number)))
        tag = (not in_fence and not run and not heading
               and TAG_LINE.match(line.strip()) is not None)
        declared = ID_TAG.match(line.strip()) if tag else None
        if declared:
            section = declared.group(1)
            # The heading the tag sits under opens the section it names.
            for row in reversed(out):
                if row["heading"]:
                    row["section"] = section
                    break
                if row["line"].strip() and not row["tag"]:
                    break
        out.append({
            "line": line, "path": [(h[0], h[1]) for h in stack],
            "load": next((h[2] for h in reversed(stack) if h[2]), None),
            "anchor": next((h[0] for h in stack if h[2]), None),
            "section": section, "tag": tag, "heading": bool(heading),
            "fence": in_fence or bool(run)})
    return out


def _overridden(files):
    """The section IDs some template in the chain overrides."""
    ids = set()
    for _, text in files:
        for line in text.splitlines():
            match = OVERRIDE_TAG.match(line.strip())
            if match:
                ids.add(match.group(1))
    return ids


def _declined(row, path, declined):
    """True when the row sits under a heading the project declined."""
    return any(f"{path}#{text}" in declined for _, text in row["path"])


def _demote(line, by):
    heading = HEADING_LINE.match(line)
    if not heading:
        return line
    level = max(1, min(len(heading.group(1)) + by, 6))
    return "#" * level + line[len(heading.group(1)):]


def _fenced(lines):
    """For each line, True when it is a fence delimiter or inside one."""
    marks, fence = [], None
    for line in lines:
        run = FENCE_LINE.match(line)
        marks.append(fence is not None or bool(run))
        if run:
            mark = run.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
    return marks


def _units(rows):
    """Group a section's rows into units: a heading, a fenced block, a
    paragraph, a bullet with its continuation lines, or a blank line."""
    units = []
    for row in rows:
        line = row["line"]
        kind = ("heading" if row["heading"] else "fence" if row["fence"]
                else "blank" if not line.strip()
                else "bullet" if BULLET_LINE.match(line) else "text")
        last = units[-1] if units else None
        if last and kind == "fence" and last["kind"] == "fence" \
                and not last["closed"]:
            last["rows"].append(row)
            if FENCE_LINE.match(line) and len(last["rows"]) > 1:
                last["closed"] = True
            continue
        nested = kind == "bullet" and BULLET_LINE.match(line).group(1)
        if last and last["kind"] in ("bullet", "text") and (
                kind == "text" or (nested and last["kind"] == "bullet")):
            # A wrapped line or a nested bullet continues the unit above.
            last["rows"].append(row)
            continue
        units.append({"kind": kind, "rows": [row], "closed": False})
    return units


def _checked(rows):
    """What a checked section keeps: its headings, its fenced commands, its
    prose, and every bullet next to a command, which states the command
    or its pass condition. The other bullets are the rules the check
    enforces, and the check reports them."""
    units = _units(rows)
    keep = []
    for i, unit in enumerate(units):
        if unit["kind"] == "bullet":
            near = False
            for step in (-1, 1):
                j = i + step
                while 0 <= j < len(units) and units[j]["kind"] == "blank":
                    j += step
                if 0 <= j < len(units) and units[j]["kind"] == "fence":
                    near = True
            if not near:
                continue
        keep.extend(unit["rows"])
    return keep


def _tidy(lines):
    """Drop headings left with no content and collapse blank runs outside
    fences, so a `#` comment in a code block is never read as a heading."""
    fenced = _fenced(lines)
    kept = []
    for i, line in enumerate(lines):
        heading = None if fenced[i] else HEADING_LINE.match(line)
        if heading:
            level = len(heading.group(1))
            body = False
            for j in range(i + 1, len(lines)):
                after = lines[j]
                deeper = None if fenced[j] else HEADING_LINE.match(after)
                if deeper and len(deeper.group(1)) <= level:
                    break
                if after.strip() and not deeper:
                    body = True
                    break
            if not body:
                continue
        if (not fenced[i] and not line.strip()
                and (not kept or not kept[-1].strip())):
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


def _place(files, declined):
    """Split the chain into the root file's rows and each kind's rows."""
    overridden = _overridden(files)
    root, skills = [], {}
    for path, text in files:
        rows = [row for row in _blocks(text)
                if not row["tag"] and row["section"] not in overridden
                and not _declined(row, path, declined)]
        i = 0
        while i < len(rows):
            load = rows[i]["load"]
            j = i
            while j < len(rows) and rows[j]["load"] == load:
                j += 1
            run = rows[i:j]
            if load == LOAD_CHECK:
                run = _checked(run)
            if load is None or load == LOAD_CHECK:
                # A template's title sits under the root file's `## Rules`.
                root += [_demote(r["line"], 2) if r["heading"]
                         else r["line"] for r in run]
            else:
                # A skill's sections start at level two, whatever level the
                # loaded heading had in its template.
                skills.setdefault(load, []).extend(
                    _demote(r["line"], 2 - r["anchor"]) if r["heading"]
                    else r["line"] for r in run)
            i = j
        root.append("")
    return root, skills


def build(files, kinds, declined=(), inline_skills=False):
    """Every file the chain emits, as {relative path: text}.

    `files` is the chain as (path, text) pairs in resolution order, `kinds`
    the manifest's task kinds, and `declined` the `path#Heading` entries
    the project does not adopt.
    """
    root, skills = _place(files, set(declined))
    used = [kind for kind in kinds if kind in skills]

    head = [FACTS.rstrip("\n"), ""]
    rules = [RULES_HEADING, "", "The adopted rules that apply on every task.",
             ""] + root
    table = []
    if used and not inline_skills:
        table = ["## Skills", "",
                 "Load a skill when its task starts; each holds that task's "
                 "procedures.", "", "| Skill | Load it when |",
                 "|-------|--------------|"]
        table += [f"| {kind} | {kinds[kind]} |" for kind in used]
    procedures = []
    if inline_skills and used:
        procedures = ["## Procedures", "",
                      "This agent loads no skills, so each task's "
                      "procedures are here.", ""]
        for kind in used:
            procedures += [f"### {kind}", "", kinds[kind], ""]
            fenced = _fenced(skills[kind])
            procedures += [line if fenced[i] else _demote(line, 2)
                           for i, line in enumerate(skills[kind])]
            procedures.append("")
    out = {ROOT_FILE: "\n".join(_tidy(
        head + rules + [""] + table + [""] + procedures)) + "\n"}
    if not inline_skills:
        for kind in used:
            skill = ["---", f"name: {kind}",
                     f"description: {kinds[kind]}", "---", "",
                     f"# {kinds[kind]}", ""] + skills[kind]
            out[f"{SKILLS_DIR}/{kind}/SKILL.md"] = "\n".join(
                _tidy(skill)) + "\n"
    return out


def read_declined(path):
    """The `path#Heading` entries of a declined list, one per line."""
    if not path:
        return []
    with io.open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle
                if line.strip() and not line.startswith("#")]


def _read(path):
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def _keep_facts(previous, emitted):
    """The emitted root file with the facts a previous one filled in.

    The facts are everything above `## Rules`. A previous file without that
    heading was not built here, and overwriting it would lose it.
    """
    marker = "\n" + RULES_HEADING + "\n"
    if marker not in "\n" + previous:
        raise EmitError(f"{ROOT_FILE} exists and has no `{RULES_HEADING}` "
                        f"heading, so it was not built by --emit; move it "
                        f"aside, or merge its facts into a fresh build")
    facts = ("\n" + previous).split(marker, 1)[0][1:]
    rules = ("\n" + emitted).split(marker, 1)[1]
    return facts + marker[1:] + rules


def write(out_dir, emitted, mirrors=()):
    """Write the emitted files, copy the skills into each mirror, keep the
    facts a previous root file filled in, and remove what a previous run
    wrote that this one does not."""
    files = dict(emitted)
    previous = _read(os.path.join(out_dir, ROOT_FILE))
    if previous is not None:
        files[ROOT_FILE] = _keep_facts(previous, files[ROOT_FILE])
    targets = {}
    for rel, text in files.items():
        targets[rel] = text
        if rel.startswith(SKILLS_DIR + "/"):
            for mirror in mirrors:
                copy = mirror.rstrip("/") + rel[len(SKILLS_DIR):]
                targets[copy] = text

    record = os.path.join(out_dir, RECORD)
    stale = set((_read(record) or "").split()) - set(targets)
    for rel in sorted(stale):
        full = os.path.join(out_dir, rel)
        if os.path.isfile(full):
            os.remove(full)
        folder = os.path.dirname(full)
        while folder and os.path.abspath(folder) != os.path.abspath(out_dir):
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)
            folder = os.path.dirname(folder)

    for rel, text in sorted(targets.items()):
        full = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
        with io.open(full, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    os.makedirs(os.path.dirname(record), exist_ok=True)
    with io.open(record, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(sorted(targets)) + "\n")
    return sorted(files)
