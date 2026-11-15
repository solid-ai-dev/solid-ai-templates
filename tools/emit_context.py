"""Build a project's root context file and its task skills from a chain.

Each template section declares its load (spec, chapter 8.1; ADR-058): no
directive loads on every turn, a kind of task loads in that kind's skill,
and `check` loads as the check that enforces it. This module resolves the
chain's overrides, places every section by its load, and copies rule text
unchanged, so the same chain and the same declined list always give
byte-identical files. The project's facts are slots the agent or the
interview fills, and a regeneration keeps what was filled.

With `--sections` it builds one file per topic instead, each a heading of
a template with every rule it needs, and a root file that maps each topic
to its file, to be read when the work first touches it.

Run it through the resolver:

    py tools/resolve_chain.py --emit <out-dir> <root> [<root> ...]
        [--declined <file>] [--inline-skills | --sections] [--mirror <dir>]
"""

from __future__ import annotations

import hashlib
import io
import os
import re
from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import NamedTuple, TypedDict, cast

from resolve_chain import (
    FENCE_LINE,
    HEADING_LINE,
    LOAD_CHECK,
    TAG_LINE,
    load_directives,
)

SKILLS_DIR = ".agents/skills"

# Where the section files go: one folder per template, named by its manifest
# ID, so no emitted path names a template file.
SECTIONS_DIR = ".agents/sections"

ROOT_FILE = "AGENTS.md"
RULES_HEADING = "## Rules"

# Every file the emitter wrote last time, with the hash of what it wrote,
# so a rerun removes a skill it no longer emits and nothing else: not a
# file it never wrote, and not one edited since.
RECORD = ".agents/emitted.txt"

# The first line under `## Rules`, which only the emitter writes. With the
# record listing the root file, it is what shows a root file is the
# emitter's to rebuild.
BUILT_LINE = (
    "Built by `resolve_chain.py --emit`; change the templates, not the rules below."
)

BULLET_LINE = re.compile(r"^(\s*)(?:[-*+]|\d+\.)\s")
ID_TAG = re.compile(r"^\[ID:\s*([^\]]+?)\s*\]$")
OVERRIDE_TAG = re.compile(r"^\[OVERRIDE:\s*([^\]]+?)\s*\]$")
EXTEND_TAG = re.compile(r"^\[EXTEND:\s*([^\]]+?)\s*\]$")

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


# The facts' model line, which names how the rules are delivered.
MODEL_LINE = "- Model: root and skills"
SECTIONS_MODEL_LINE = "- Model: root and sections"

# What the root file says of the section files. The map is read on demand:
# an agent told to read every file at the start loads the whole chain, and
# the section files would save nothing.
SECTIONS_LEAD = [
    "The adopted rules are in the section files below, one topic each. Do not",
    "read them before the work starts. The first time the work touches a",
    "section's topic, read its file; then apply every rule it holds.",
]

# The map's header rows, one table per template.
MAP_HEADER = ["| When the work first touches | Read first |", "| --- | --- |"]

# A section ID named in a rule's prose, in backticks.
NAMED_ID = re.compile(r"`([a-z0-9][a-z0-9-]*)`")


class EmitError(Exception):
    """An emission refused rather than written."""


class Row(TypedDict):
    """One line of a template and where it sits; `_blocks` says each key."""

    line: str
    path: list[tuple[int, str]]
    load: str | None
    anchor: int | None
    section: str | None
    tag: bool
    heading: bool
    fence: bool


class Unit(TypedDict):
    """Rows that stay together: a heading, a block, a paragraph or a bullet."""

    kind: str
    rows: list[Row]
    closed: bool


def _blocks(text: str) -> list[Row]:
    """The file's lines, each a dict describing where it sits.

    Keys: `line`; the `path` of (level, text) headings above it; its `load`
    (the nearest on that path, or None for every turn) and the `anchor`
    level of the heading that set it; the `section` ID it belongs to, a
    section running from its `[ID:]` to the next; and whether it is a tag
    line, a heading, or a fence line or inside one.
    """
    loads = {d["heading"]: d["kind"] for d in load_directives(text) if d["placed"]}
    out: list[Row] = []
    stack: list[tuple[int, str, str | None]] = []
    fence: str | None = None
    section: str | None = None
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
        tag = (
            not in_fence
            and not run
            and not heading
            and TAG_LINE.match(line.strip()) is not None
        )
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
        out.append(
            {
                "line": line,
                "path": [(h[0], h[1]) for h in stack],
                "load": next((h[2] for h in reversed(stack) if h[2]), None),
                "anchor": next((h[0] for h in stack if h[2]), None),
                "section": section,
                "tag": tag,
                "heading": bool(heading),
                "fence": in_fence or bool(run),
            }
        )
    return out


def _overridden(parsed: Iterable[Iterable[Row]]) -> set[str]:
    """The section IDs an adopted override replaces.

    Only a tag line counts, so an example in a fence overrides nothing, and
    an override the project declined leaves its base section in place.
    """
    return {
        match.group(1)
        for rows in parsed
        for row in rows
        if row["tag"]
        for match in [OVERRIDE_TAG.match(row["line"].strip())]
        if match
    }


def _declined(row: Row, path: str, declined: Collection[str]) -> bool:
    """True when the row sits under a heading the project declined."""
    return any(f"{path}#{text}" in declined for _, text in row["path"])


def _demote(line: str, by: int) -> str:
    heading = HEADING_LINE.match(line)
    if not heading:
        return line
    level = max(1, min(len(heading.group(1)) + by, 6))
    return "#" * level + line[len(heading.group(1)) :]


def _fenced(lines: Iterable[str]) -> list[bool]:
    """For each line, True when it is a fence delimiter or inside one."""
    marks: list[bool] = []
    fence: str | None = None
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


def _units(rows: Iterable[Row]) -> list[Unit]:
    """Group a section's rows into units: a heading, a fenced block, a
    paragraph, a bullet with its continuation lines, or a blank line."""
    units: list[Unit] = []
    for row in rows:
        line = row["line"]
        kind = (
            "heading"
            if row["heading"]
            else "fence"
            if row["fence"]
            else "blank"
            if not line.strip()
            else "bullet"
            if BULLET_LINE.match(line)
            else "text"
        )
        last = units[-1] if units else None
        if last and kind == "fence" and last["kind"] == "fence" and not last["closed"]:
            last["rows"].append(row)
            if FENCE_LINE.match(line) and len(last["rows"]) > 1:
                last["closed"] = True
            continue
        bullet = BULLET_LINE.match(line) if kind == "bullet" else None
        nested = bullet is not None and bullet.group(1)
        if (
            last
            and last["kind"] in ("bullet", "text")
            and (kind == "text" or (nested and last["kind"] == "bullet"))
        ):
            # A wrapped line or a nested bullet continues the unit above.
            last["rows"].append(row)
            continue
        units.append({"kind": kind, "rows": [row], "closed": False})
    return units


def _checked(rows: Iterable[Row]) -> list[Row]:
    """What a checked section keeps: its headings, its fenced commands, its
    prose, the bullet that introduces a command, and the whole list that
    follows one, which states its pass condition. The other bullets are
    the rules the check enforces, and the check reports them.

    A list after a command is kept whole, rules and all: dropping a rule
    costs nothing the check does not report, and dropping half a pass
    condition loses what the check means."""
    units = _units(rows)
    near: set[int] = set()
    for i, unit in enumerate(units):
        if unit["kind"] != "fence":
            continue
        j = i - 1
        while j >= 0 and units[j]["kind"] == "blank":
            j -= 1
        if j >= 0 and units[j]["kind"] == "bullet":
            near.add(j)
        j = i + 1
        while j < len(units) and units[j]["kind"] in ("blank", "bullet"):
            if units[j]["kind"] == "bullet":
                near.add(j)
            j += 1
    keep: list[Row] = []
    for i, unit in enumerate(units):
        if unit["kind"] != "bullet" or i in near:
            keep.extend(unit["rows"])
    return keep


def _tidy(lines: Sequence[str]) -> list[str]:
    """Drop headings left with no content and collapse blank runs outside
    fences, so a `#` comment in a code block is never read as a heading."""
    fenced = _fenced(lines)
    kept: list[str] = []
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
        if not fenced[i] and not line.strip() and (not kept or not kept[-1].strip()):
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


class Adopted(NamedTuple):
    """One file of the chain as the project adopts it: its `path`, every
    parsed row in `rows`, tag lines and declined ones included, the
    `declined` rows by identity, and its `runs`, each a load with the rows
    it keeps, a declined or overridden section dropped and a checked run cut
    to its command."""

    path: str
    rows: list[Row]
    declined: set[int]
    runs: list[tuple[str | None, list[Row]]]


def _adopt(
    files: Iterable[tuple[str, str]], declined: Collection[str]
) -> list[Adopted]:
    """Each file of the chain as the project adopts it, in chain order."""
    files = list(files)
    every = [_blocks(text) for _, text in files]
    parsed = [
        [row for row in rows if not _declined(row, path, declined)]
        for (path, _), rows in zip(files, every)
    ]
    overridden = _overridden(parsed)
    adopted: list[Adopted] = []
    for (path, _), all_rows, parsed_rows in zip(files, every, parsed):
        rows = [
            row
            for row in parsed_rows
            if not row["tag"] and row["section"] not in overridden
        ]
        runs: list[tuple[str | None, list[Row]]] = []
        i = 0
        while i < len(rows):
            load = rows[i]["load"]
            j = i
            while j < len(rows) and rows[j]["load"] == load:
                j += 1
            run = rows[i:j]
            if load == LOAD_CHECK:
                run = _checked(run)
            runs.append((load, run))
            i = j
        gone = {id(row) for row in all_rows} - {id(row) for row in parsed_rows}
        adopted.append(Adopted(path, all_rows, gone, runs))
    return adopted


def _place(
    files: Iterable[tuple[str, str]], declined: Collection[str]
) -> tuple[list[str], dict[str, list[str]]]:
    """Split the chain into the root file's rows and each kind's rows."""
    root: list[str] = []
    skills: dict[str, list[str]] = {}
    for adopted in _adopt(files, declined):
        for load, run in adopted.runs:
            if load is None or load == LOAD_CHECK:
                # A template's title sits under the root file's `## Rules`.
                root += [
                    _demote(r["line"], 2) if r["heading"] else r["line"] for r in run
                ]
            else:
                # A skill's sections start at level two, whatever level the
                # loaded heading had in its template. A row with a load has
                # the anchor of the heading that set it.
                skills.setdefault(load, []).extend(
                    _demote(r["line"], 2 - cast(int, r["anchor"]))
                    if r["heading"]
                    else r["line"]
                    for r in run
                )
        root.append("")
    return root, skills


def build(
    files: Iterable[tuple[str, str]],
    kinds: Mapping[str, str],
    declined: Iterable[str] = (),
    inline_skills: bool = False,
) -> dict[str, str]:
    """Every file the chain emits, as {relative path: text}.

    `files` is the chain as (path, text) pairs in resolution order, `kinds`
    the manifest's task kinds, and `declined` the `path#Heading` entries
    the project does not adopt.
    """
    root, skills = _place(files, set(declined))
    used = [kind for kind in kinds if kind in skills]

    head = [FACTS.rstrip("\n"), ""]
    rules = [
        RULES_HEADING,
        "",
        BUILT_LINE,
        "",
        "The adopted rules that apply on every task.",
        "",
    ] + root
    table: list[str] = []
    if used and not inline_skills:
        table = [
            "## Skills",
            "",
            "Load a skill when its task starts; each holds that task's procedures.",
            "",
            "| Skill | Load it when |",
            "|-------|--------------|",
        ]
        table += [f"| {kind} | {kinds[kind]} |" for kind in used]
    procedures: list[str] = []
    if inline_skills and used:
        procedures = [
            "## Procedures",
            "",
            "This agent loads no skills, so each task's procedures are here.",
            "",
        ]
        for kind in used:
            procedures += [f"### {kind}", "", kinds[kind], ""]
            fenced = _fenced(skills[kind])
            procedures += [
                line if fenced[i] else _demote(line, 2)
                for i, line in enumerate(skills[kind])
            ]
            procedures.append("")
    out = {
        ROOT_FILE: "\n".join(_tidy(head + rules + [""] + table + [""] + procedures))
        + "\n"
    }
    if not inline_skills:
        for kind in used:
            skill = [
                "---",
                f"name: {kind}",
                f"description: {kinds[kind]}",
                "---",
                "",
                f"# {kinds[kind]}",
                "",
            ] + skills[kind]
            out[f"{SKILLS_DIR}/{kind}/SKILL.md"] = "\n".join(_tidy(skill)) + "\n"
    return out


# A topic's place in its template: the headings down to its own, the
# template's title alone for the rules under the title.
Key = tuple[tuple[int, str], ...]


@dataclass
class Topic:
    """One heading under a template's title, with its subheadings, or the
    rules under the title itself: the unit a section file is built around.

    `order` is its place in the chain, `ids` the section IDs its rows sit
    in, `extends` and `overrides` the IDs its tags name, `names` the
    adopted IDs its prose names, and `governed` the IDs of its template's
    title that an override replaces.
    """

    order: int
    path: str
    key: Key
    rows: list[Row] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)
    extends: set[str] = field(default_factory=set)
    overrides: set[str] = field(default_factory=set)
    names: set[str] = field(default_factory=set)
    governed: set[str] = field(default_factory=set)

    def content(self) -> bool:
        return any(r["line"].strip() and not r["heading"] for r in self.rows)


def _relate(
    one: Adopted,
    by_key: Mapping[tuple[str, Key], Topic],
    replaced: dict[str, set[str]],
) -> None:
    """Give every topic of one file the IDs its section extends and
    overrides, and record in `replaced` each overridden ID with the IDs the
    overrides that replace it declare.

    A section runs from its tags to the next `[ID:]`, not to the next
    heading, so a heading with no tags of its own stays in the section
    above it. Where a section runs is read from every row, declined and
    replaced ones too, and which rules it reaches from the delivered ones:
    only a surviving rule line takes a relationship, since a blank line
    under a heading comes before its tags, and a replaced subsection's rows
    are not its heading's. A declined override replaces nothing, so it
    relates nothing.
    """
    kept = {id(row) for _, run in one.runs for row in run}
    extends: set[str] = set()
    overrides: set[str] = set()
    fresh = False
    for row in one.rows:
        if row["heading"]:
            fresh = True
            continue
        line = row["line"].strip()
        if row["tag"]:
            for pattern in (ID_TAG, EXTEND_TAG, OVERRIDE_TAG):
                match = pattern.match(line)
                if not match:
                    continue

                # The first relationship under a heading opens a section.
                if fresh:
                    extends, overrides, fresh = set(), set(), False
                if pattern is EXTEND_TAG:
                    extends.add(match.group(1))
                elif pattern is OVERRIDE_TAG and id(row) not in one.declined:
                    overrides.add(match.group(1))

                    # An override replaces with the section it sits in,
                    # whether its heading declares that ID or inherits it
                    # from a heading above.
                    if row["section"]:
                        replaced.setdefault(match.group(1), set()).add(row["section"])
            continue
        if not line:
            continue
        fresh = False
        topic = by_key.get((one.path, tuple(row["path"][:2])))
        if topic is not None and id(row) in kept:
            topic.extends |= extends
            topic.overrides |= overrides


def _topics(adopted: Sequence[Adopted]) -> list[Topic]:
    """The adopted chain's topics, in chain order. One that holds no rule
    gets no file, and a title with none still heads the files below it."""
    topics: list[Topic] = []
    by_key: dict[tuple[str, Key], Topic] = {}
    for one in adopted:
        for _, run in one.runs:
            for row in run:
                at = (one.path, tuple(row["path"][:2]))
                if at not in by_key:
                    by_key[at] = Topic(len(topics), one.path, at[1])
                    topics.append(by_key[at])
                by_key[at].rows.append(row)

                # A topic sits in the sections its rules do. The blank line
                # between a heading and its `[ID:]` still belongs to the
                # section before, and holds no rule of it.
                if row["section"] and row["line"].strip() and not row["heading"]:
                    by_key[at].ids.add(row["section"])
    replaced: dict[str, set[str]] = {}
    for one in adopted:
        _relate(one, by_key, replaced)

    # The rules under a title govern every heading beneath it, read from the
    # unfiltered rows: where a later template overrides the title's ID, the
    # override's rules govern the headings that keep IDs of their own.
    gone = _overridden(
        [row for row in one.rows if id(row) not in one.declined] for one in adopted
    )
    for one in adopted:
        title = {
            row["section"]
            for row in one.rows
            if len(row["path"]) == 1
            and row["section"]
            and not row["tag"]
            and row["line"].strip()
        }
        for topic in topics:
            if topic.path == one.path and len(topic.key) == 2:
                topic.governed = title & gone

    # An override that declares an ID of its own may be overridden in turn,
    # and then none of its rows survive to hold the ID it replaced. The last
    # surviving replacement stands for every ID down the chain, so a rule
    # that names or extends the first still finds it.
    for topic in topics:
        stands = topic.ids | topic.overrides
        grown = True
        while grown:
            grown = False
            for old, new in replaced.items():
                if old not in stands and new & stands:
                    stands.add(old)
                    grown = True
        topic.overrides |= stands - topic.ids
    known = {i for topic in topics if topic.content() for i in topic.ids}
    known |= {i for topic in topics for i in topic.overrides}
    for topic in topics:
        for row in topic.rows:
            if not row["fence"]:
                topic.names.update(NAMED_ID.findall(row["line"]))

        # An ID can run over several headings, so a heading that names its
        # own section's ID still needs the others; the topic itself is
        # already carried.
        topic.names &= known
    return topics


def _carried(topics: Sequence[Topic]) -> dict[int, list[Topic]]:
    """Each topic's order mapped to what its section file carries, in chain
    order: the topic, the rules under its template's title, the sections it
    extends or names, the extensions of its own, and theirs in turn."""
    holding: dict[str, list[Topic]] = {}
    extending: dict[str, list[Topic]] = {}
    for topic in topics:
        for i in topic.ids | topic.overrides:
            holding.setdefault(i, []).append(topic)
        for i in topic.extends:
            extending.setdefault(i, []).append(topic)

    def needs(topic: Topic, whole: bool) -> list[tuple[Topic, bool]]:
        # The rules under a title govern every heading beneath it.
        found = [
            (other, False)
            for other in topics
            if other.path == topic.path
            and len(other.key) < len(topic.key)
            and topic.key[: len(other.key)] == other.key
        ]
        for i in sorted(topic.governed):
            found += [(other, False) for other in holding.get(i, [])]

        # A section is read with the one it extends or names, since a rule
        # left to a reference is one the agent never reads.
        for i in sorted(topic.extends | topic.names):
            found += [(other, True) for other in holding.get(i, [])]

        # An extension applies on top of the section it extends, so it goes
        # with that section's rules. Rules carried only because they govern
        # a heading do not bring theirs: a title's ID runs to the next ID,
        # and its extensions extend that run, not every heading below it.
        if whole:
            for i in sorted(topic.ids | topic.overrides):
                found += [(other, True) for other in extending.get(i, [])]
        return found

    carried: dict[int, list[Topic]] = {}
    for topic in topics:
        seen = {topic.order: topic}
        done: set[tuple[int, bool]] = set()
        todo = [(topic, True)]
        while todo:
            current, whole = todo.pop()
            if (current.order, whole) in done:
                continue
            done.add((current.order, whole))
            for other, other_whole in needs(current, whole):
                seen[other.order] = other
                todo.append((other, other_whole))
        carried[topic.order] = [seen[order] for order in sorted(seen)]
    return carried


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def build_sections(
    files: Iterable[tuple[str, str]],
    templates: Mapping[str, tuple[str, str]],
    declined: Iterable[str] = (),
) -> dict[str, str]:
    """The root file and one section file per topic, as {relative path:
    text}.

    `files` is the chain as (path, text) pairs in resolution order,
    `templates` maps each path to its manifest ID and description, and
    `declined` holds the `path#Heading` entries the project does not adopt.
    Every adopted rule is in a section file and none in the root file, which
    maps each topic to its file.
    """
    topics = _topics(_adopt(files, set(declined)))
    carried = _carried(topics)
    headings = [topic for topic in topics if len(topic.key) == 2 and topic.content()]
    governing = {
        other.order
        for topic in headings
        for other in carried[topic.order]
        if other.path == topic.path and len(other.key) < len(topic.key)
    }

    # A heading that holds a rule gets a file of its own. The rules under a
    # title get one only where no such heading's file carries them.
    owners = [
        topic
        for topic in topics
        if topic.content() and (len(topic.key) == 2 or topic.order not in governing)
    ]
    out: dict[str, str] = {}
    groups: dict[str, list[str]] = {}
    for topic in owners:
        if topic.path not in templates:
            raise EmitError(f"{topic.path} has no manifest entry to name it by")
        folder = f"{SECTIONS_DIR}/{templates[topic.path][0]}"
        name = topic.key[-1][1] if topic.key else templates[topic.path][0]
        rel = f"{folder}/{_slug(name)}.md"
        suffix = 2
        while rel in out:
            rel = f"{folder}/{_slug(name)}-{suffix}.md"
            suffix += 1
        lines: list[str] = []
        for other in carried[topic.order]:
            lines += [r["line"] for r in other.rows] + [""]
        out[rel] = "\n".join(_tidy(lines)) + "\n"
        topic_cell = name.replace("|", "\\|")
        groups.setdefault(topic.path, []).append(f"| {topic_cell} | `{rel}` |")

    table: list[str] = []
    for path, rows in groups.items():
        first = next(t for t in topics if t.path == path)
        title = first.key[0][1] if first.key else templates[path][0]
        table += [f"### {title}", "", templates[path][1], ""] + MAP_HEADER + rows + [""]
    head = [FACTS.replace(MODEL_LINE, SECTIONS_MODEL_LINE).rstrip("\n"), ""]
    rules = [RULES_HEADING, "", BUILT_LINE, ""] + SECTIONS_LEAD + [""] + table
    return {ROOT_FILE: "\n".join(_tidy(head + rules)) + "\n", **out}


def section_rules(
    files: Iterable[tuple[str, str]], declined: Iterable[str] = ()
) -> dict[str, list[str]]:
    """Each adopted section ID with its rule lines, the non-blank lines that
    are not headings, in chain order."""
    rules: dict[str, list[str]] = {}
    for adopted in _adopt(files, set(declined)):
        for _, run in adopted.runs:
            for row in run:
                if row["section"] and row["line"].strip() and not row["heading"]:
                    rules.setdefault(row["section"], []).append(row["line"])
    return rules


def read_declined(path: str | None) -> list[str]:
    """The `path#Heading` entries of a declined list, one per line."""
    if not path:
        return []
    with io.open(path, encoding="utf-8") as handle:
        return [
            line.strip() for line in handle if line.strip() and not line.startswith("#")
        ]


def _read(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_record(out_dir: str) -> dict[str, str]:
    """The previous run's {path: hash}, one tab-separated entry a line."""
    entries: dict[str, str] = {}
    for line in (_read(os.path.join(out_dir, RECORD)) or "").splitlines():
        digest, sep, rel = line.partition("\t")
        if sep and rel:
            entries[rel] = digest
    return entries


def _keep_facts(previous: str, emitted: str, recorded: Collection[str]) -> str:
    """The emitted root file with the facts a previous one filled in.

    The facts are everything above `## Rules`. A previous file is the
    emitter's only when the record lists it and its rules open on the line
    only the emitter writes; any other file is the project's, and
    overwriting it would lose it.
    """
    marker = "\n" + RULES_HEADING + "\n"
    owned = (
        ROOT_FILE in recorded and marker + "\n" + BUILT_LINE + "\n" in "\n" + previous
    )
    if not owned:
        raise EmitError(
            f"{ROOT_FILE} exists and was not built by --emit; "
            f"move it aside, or merge its facts into a fresh "
            f"build"
        )
    facts = ("\n" + previous).split(marker, 1)[0][1:]
    rules = ("\n" + emitted).split(marker, 1)[1]

    # The model line is the emitter's, not a fact: a project that moves to
    # section files, or back, gets the line that names what it now holds.
    model, other = MODEL_LINE, SECTIONS_MODEL_LINE
    if "\n" + other + "\n" in "\n" + emitted.split(marker, 1)[0]:
        model, other = other, model
    facts = ("\n" + facts).replace("\n" + other + "\n", "\n" + model + "\n")[1:]
    return facts + marker[1:] + rules


def _owned_stale(out_dir: str, rel: str, digest: str) -> str | None:
    """The full path of a recorded file to remove, or None to keep it: it
    must stay inside the output directory and still hold what was written.
    """
    # Absolute on both sides, so `.` contains `./x` as any folder contains
    # its files.
    full = os.path.abspath(os.path.join(out_dir, rel))
    base = os.path.abspath(out_dir)
    if os.path.isabs(rel) or not full.startswith(base.rstrip(os.sep) + os.sep):
        return None
    current = _read(full) if os.path.isfile(full) else None
    if current is None or _hash(current) != digest:
        return None
    return full


def write(
    out_dir: str, emitted: Mapping[str, str], mirrors: Sequence[str] = ()
) -> list[str]:
    """Write the emitted files, copy the skills into each mirror, keep the
    facts a previous root file filled in, and remove what a previous run
    wrote that this one does not."""
    files = dict(emitted)
    recorded = _read_record(out_dir)
    previous = _read(os.path.join(out_dir, ROOT_FILE))
    if previous is not None:
        files[ROOT_FILE] = _keep_facts(previous, files[ROOT_FILE], recorded)
    targets: dict[str, str] = {}
    for rel, text in files.items():
        targets[rel] = text
        if rel.startswith(SKILLS_DIR + "/"):
            for mirror in mirrors:
                copy = mirror.rstrip("/") + rel[len(SKILLS_DIR) :]
                targets[copy] = text

    record = os.path.join(out_dir, RECORD)
    for rel in sorted(set(recorded) - set(targets)):
        full = _owned_stale(out_dir, rel, recorded[rel])
        if full is None:
            continue
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
        handle.write(
            "".join(f"{_hash(targets[rel])}\t{rel}\n" for rel in sorted(targets))
        )
    return sorted(files)
