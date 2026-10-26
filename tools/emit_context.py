"""Build a project's root context file and its task skills from a chain.

Each template section declares its load (spec, chapter 8.1; ADR-058): no
directive loads on every turn, a kind of task loads in that kind's skill,
and `check` loads as the check that enforces it. This module places every
section by its load, copying rule text unchanged, so the same chain and the
same adopted list always give byte-identical files. The project's facts
are left as named slots for the agent or the interview to fill.

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
BULLET_LINE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")

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


def _blocks(path, text):
    """The file's lines, each tagged with its heading path and load.

    Each row is a dict: the `line`, the `path` of (level, text) headings
    above it, its `load` (the nearest on that path, or None for every
    turn), the `anchor` level of the heading that set the load, and
    whether it is a tag line, inside a fence, or a heading.
    """
    loads = {d["heading"]: d["kind"] for d in load_directives(text)
             if d["placed"]}
    out, stack, fence = [], [], None
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
        load = next((h[2] for h in reversed(stack) if h[2]), None)
        anchor = next((h[0] for h in stack if h[2]), None)
        tag = (not in_fence and not run and not heading
               and TAG_LINE.match(line.strip()) is not None)
        out.append({"line": line, "path": [(h[0], h[1]) for h in stack],
                    "load": load, "anchor": anchor, "tag": tag,
                    "fence": in_fence or bool(run),
                    "heading": bool(heading)})
    return out


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


def build(files, kinds, declined=(), inline_skills=False):
    """Every file the chain emits, as {relative path: text}.

    `files` is the chain as (path, text) pairs in resolution order, `kinds`
    the manifest's task kinds, and `declined` the `path#Heading` entries
    the project does not adopt.
    """
    declined = set(declined)
    root, skills = [], {}
    for path, text in files:
        for row in _blocks(path, text):
            if row["tag"] or _declined(row, path, declined):
                continue
            # A template's title sits under the root file's `## Rules`.
            line = _demote(row["line"], 2) if row["heading"] else row["line"]
            load = row["load"]
            if load is None:
                root.append(line)
            elif load == LOAD_CHECK:
                # A checked section keeps its prose and its fenced command,
                # which state the check and its pass condition; its rules
                # are what the check enforces.
                if row["fence"] or row["heading"] or not BULLET_LINE.match(
                        row["line"]):
                    root.append(line)
            else:
                # A skill's sections start at level two, whatever level the
                # loaded heading had in its template.
                by = 2 - row["anchor"]
                skills.setdefault(load, []).append(
                    _demote(row["line"], by) if row["heading"]
                    else row["line"])
        root.append("")
    used = [kind for kind in kinds if kind in skills]

    out = {}
    head = [FACTS.rstrip("\n"), ""]
    rules = ["## Rules", "", "The adopted rules that apply on every task.", ""]
    rules += root
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
    text = "\n".join(_tidy(head + rules + [""] + table + [""] + procedures))
    out["AGENTS.md"] = text + "\n"
    if not inline_skills:
        for kind in used:
            skill = ["---", f"name: {kind}",
                     f"description: {kinds[kind]}", "---", "",
                     f"# {kinds[kind]}", ""]
            skill += skills[kind]
            out[f"{SKILLS_DIR}/{kind}/SKILL.md"] = "\n".join(
                _tidy(skill)) + "\n"
    return out


def read_declined(path):
    """The `path#Heading` entries of an adopted list, one per line."""
    if not path:
        return []
    with io.open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle
                if line.strip() and not line.startswith("#")]


def write(out_dir, emitted, mirrors=()):
    """Write the emitted files, and copy the skills into each mirror."""
    for rel, text in sorted(emitted.items()):
        targets = [rel]
        if rel.startswith(SKILLS_DIR + "/"):
            targets += [os.path.join(m, rel[len(SKILLS_DIR) + 1:])
                        for m in mirrors]
        for target in targets:
            full = os.path.join(out_dir, target)
            os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
            with io.open(full, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
    return sorted(emitted)
