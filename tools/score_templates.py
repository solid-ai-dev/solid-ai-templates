"""Score template documents against the criteria in
docs/design/template-content-quality.md, "Measured criteria".

Usage:
    py tools/score_templates.py                 # score every template
    py tools/score_templates.py <file>...       # score named files, with detail
    py tools/score_templates.py --sections      # the lowest-scoring sections
    py tools/score_templates.py --calibrate     # each metric's distribution
    py tools/score_templates.py --check         # CI gate: no score below baseline
    py tools/score_templates.py --update        # record today's scores as baseline
    py tools/score_templates.py --self-test     # planted cases only

Every metric reads prose only: fenced code, tables and section directives
are left out, because they are not rules an agent reads as prose. No
dependency beyond the standard library.
"""

import io
import pathlib
import re
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
BASELINE = ROOT / "tests" / "baselines" / "template-quality.txt"

# A fork scores its own templates against a baseline it owns, so recording
# them never edits the upstream file it merges.
FORK_BASELINE = ROOT / "tests" / "baselines" / "fork-template-quality.txt"

# Where each baseline lived before the tests folder was grouped by suite. A
# baseline left there is read by nothing, so a fall in score would pass;
# the ratchet refuses until it is moved rather than reading either place.
MOVED_BASELINES = {
    ROOT / "tests" / "template-quality-baseline.txt": BASELINE,
    ROOT / "tests" / "fork-template-quality-baseline.txt": FORK_BASELINE,
}

# A file with no baseline row starts at this score or above. Below it, the
# file is recorded on purpose with --update, never by accident.
NEW_FILE_FLOOR = 70

# Scores are rounded to one decimal; a drop smaller than this is noise from
# rounding, not a regression.
TOLERANCE = 0.1

RFC_KEYWORDS = re.compile(r"\b(MUST|SHOULD|MAY|SHALL|REQUIRED|RECOMMENDED)\b")

# A lowercase obligation word states a rule as plainly as a key word does;
# lowercase "may" is left out, because prose uses it for possibility.
OBLIGATION = re.compile(r"\b(must|should|never|shall)\b", re.IGNORECASE)

# Imperative verbs the corpus opens rules with, read from the first word of
# every bullet. A rule opening with one of these, or carrying an RFC 2119
# key word, states what to do.
IMPERATIVES = frozenset("""
Use Never Do Don't Prefer Validate Set Define Document Keep Include Run
Return Design Build Alert Avoid Provide Add Write Enforce Distinguish Treat
Generate State Remove Store Separate Check Audit Pin Deploy Fail Propagate
Track Review Wrap Implement Expose Apply Verify Commit Name Record Start
Detect Monitor Gate Restrict Lint Pair Derive Regenerate Read Ask Split Make
Encode Assert Scan Refresh Hash Rotate Invalidate Prove Drop Terminate
Configure Route Emit Pass Parse Support Ensure Move Accept Update Always
Limit Require Reject Mark Measure Give Put Place Report Flag Bind Cap
Cover Count Declare Delete Disable Enable Expect Extract Fix Follow Handle
Log Lock Merge Mock Open Plant Publish Raise Rename Replace Reuse Scope
Select Sign Skip Sort Stage Stub Tag Test Throttle Trim Version Wait Watch
No Not Only
""".split())

# Words that tell the reader to use judgement without saying how, so two
# agents reading the same rule act differently.
HEDGES = re.compile(
    r"\b(appropriate(?:ly)?|as (?:needed|necessary|appropriate)|where possible|"
    r"if (?:needed|necessary|possible)|properly|reasonabl[ey]|sensible|"
    r"generally|typically|usually|various|etc\b|and so on|"
    r"as much as possible|when it makes sense|consider(?:ing)?)\b",
    re.IGNORECASE)

# Signs that a passage records a history rather than states a rule: a date,
# a measurement taken on one occasion, an incident seen once.
NARRATIVE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b|\b(?:measured|observed|seen) (?:in|on|at|"
    r"against|during)\b|\bin practice\b|\bone project\b|"
    r"\bwas (?:caught|found|seen|reported)\b",
    re.IGNORECASE)

# A ticket or decision-record number in template text. The rule against it
# is absolute, so one occurrence caps the file's score.
CITATION = re.compile(r"(?<![\w/&])#\d{2,}\b|\bADR[- ]?\d{2,}\b")

SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*(\"'])")

DIRECTIVE_LINE = re.compile(r"^\[(?:ID|EXTEND|OVERRIDE|DEPENDS ON)\b")
BULLET = re.compile(r"^(\s*)(?:[-*+]|\d+\.)\s+(.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")


class Item:
    """One bullet: its words, sentences, line and nesting depth."""

    def __init__(self, text, line, depth, section):
        self.text = text
        self.line = line
        self.depth = depth
        self.section = section

    @property
    def words(self):
        return len(self.text.split())

    @property
    def sentences(self):
        return len([s for s in SENTENCE_END.split(self.text) if s.strip()])

    def is_directive(self):
        if RFC_KEYWORDS.search(self.text) or OBLIGATION.search(self.text):
            return True

        # A checklist item is an instruction to check what it names.
        if re.match(r"^\[[ xX]\]\s", self.text):
            return True
        lead = re.sub(r"^[*_`]+", "", self.text)
        match = re.match(r"[A-Za-z']+", lead)
        return bool(match) and match.group(0) in IMPERATIVES


class Doc:
    """A template's prose, split into rules, paragraphs and sections."""

    def __init__(self, text):
        self.items = []
        self.paragraphs = []
        self.sections = []
        self.prose = []
        self._parse(text.splitlines())

    def _parse(self, lines):
        fence = False
        section = "(preamble)"
        prose_lines = 0
        item = None
        para = []

        def close_item():
            nonlocal item
            if item is not None:
                self.items.append(item)
                item = None

        def close_para():
            nonlocal para
            if para:
                self.paragraphs.append((section, " ".join(para)))
                para = []

        for number, line in enumerate(lines, 1):
            if FENCE.match(line):
                close_item()
                close_para()
                fence = not fence
                continue
            if fence:
                continue
            stripped = line.strip()
            if line.startswith("## "):
                close_item()
                close_para()
                self.sections.append((section, prose_lines))
                section, prose_lines = stripped[3:], 0
                continue
            if (not stripped or line.startswith("#") or stripped.startswith("|")
                    or DIRECTIVE_LINE.match(stripped) or stripped == "---"):
                close_item()
                close_para()
                continue
            prose_lines += 1
            bullet = BULLET.match(line)
            if bullet:
                close_item()
                close_para()
                depth = len(bullet.group(1)) // 2
                item = Item(bullet.group(2).strip(), number, depth, section)
                self.prose.append(bullet.group(2))
                continue
            if item is not None and line.startswith(" "):
                item.text += " " + stripped
                self.prose.append(stripped)
                continue
            close_item()
            para.append(stripped.lstrip("> "))
            self.prose.append(stripped)
        close_item()
        close_para()
        self.sections.append((section, prose_lines))

    @property
    def text(self):
        return " ".join(self.prose)

    @property
    def words(self):
        return len(self.text.split())


def _without_code(text):
    """Text with inline code spans removed, for the word scans."""
    return re.sub(r"`[^`]*`", " ", text)


def _without_quotes(text):
    """Text with quoted passages removed. A rule quoting the form it forbids
    ("not 'see #123'") is not an instance of it."""

    # A straight single quote is also an apostrophe. It opens a quotation
    # only where no letter precedes it and closes one only where no letter
    # follows it, and an apostrophe inside a word ("don't") stays inside the
    # span. So "team's" and "cache's" pair with nothing, and the text between
    # them is still scanned.
    single = r"(?<!\w)'(?=\S)(?:[^']|'(?=\w))*?(?<=\S)'(?!\w)"
    return re.sub(r"\"[^\"]*\"|“[^”]*”|‘[^’]*’|" + single, " ", text)


def _sentences(unit):
    """The word count of each sentence in one bullet or paragraph."""
    return [len(s.split()) for s in SENTENCE_END.split(unit) if s.split()]


def metrics(doc):
    """The raw measurement behind each criterion."""
    rules = [i for i in doc.items if i.depth == 0]
    rule_words = [i.words for i in doc.items] or [0]
    para_words = [len(p.split()) for _, p in doc.paragraphs] or [0]
    units = [i.text for i in doc.items] + [p for _, p in doc.paragraphs]
    sentence_words = [n for u in units for n in _sentences(u)] or [0]
    prose_words = max(doc.words, 1)
    scan = _without_code(doc.text)
    section_lines = [count for _, count in doc.sections] or [0]
    return {
        "rule_words": statistics.median(rule_words),
        "long_rules": sum(w > 40 for w in rule_words) / max(len(doc.items), 1),
        "paragraph_share": sum(para_words) / prose_words,
        "longest_paragraph": max(para_words),
        "sentence_words": statistics.mean(sentence_words),
        "multi_sentence": (sum(i.sentences >= 3 for i in doc.items)
                           / max(len(doc.items), 1)),
        "directive_share": (sum(i.is_directive() for i in rules)
                            / max(len(rules), 1)),
        "hedges": 1000 * len(HEDGES.findall(scan)) / prose_words,
        "narrative": 1000 * len(NARRATIVE.findall(scan)) / prose_words,
        "section_lines": max(section_lines),
        "citations": len(CITATION.findall(_without_quotes(scan))),
        "longest_rule": max(rule_words),
    }


# Each criterion's band: the raw value scoring 100, the value scoring 0, and
# its weight. Between the two the score falls linearly. The bands were
# calibrated on the corpus on 2026-10-19: "good" sits near the median of the
# templates outside core/, "bad" near the corpus's 90th percentile. Run
# --calibrate to see the distributions they came from.
CRITERIA = {
    "rule_words":        {"good": 15,   "bad": 35,   "weight": 2.0},
    "long_rules":        {"good": 0.02, "bad": 0.30, "weight": 2.0},
    "paragraph_share":   {"good": 0.10, "bad": 0.35, "weight": 1.5},
    "longest_paragraph": {"good": 40,   "bad": 120,  "weight": 1.0},
    "sentence_words":    {"good": 15,   "bad": 22,   "weight": 1.0},
    "multi_sentence":    {"good": 0.02, "bad": 0.20, "weight": 1.5},
    "directive_share":   {"good": 0.75, "bad": 0.40, "weight": 1.0},
    "hedges":            {"good": 1.0,  "bad": 5.0,  "weight": 1.0},
    "narrative":         {"good": 0.0,  "bad": 1.0,  "weight": 0.5},
    "section_lines":     {"good": 40,   "bad": 200,  "weight": 1.0},
}

# A severe failure caps the score, so a weighted mean cannot average it
# away: (metric, threshold the raw value must exceed, cap).
CAPS = (
    ("citations", 0, 50),
    ("longest_rule", 150, 60),
)

# The manifest keys a fork never edits (spec, chapter 8.6). A template filed
# under one is upstream's and its score goes in the upstream baseline; every
# other template is a fork's, whatever directory it sits in.
UPSTREAM_KEYS = ("base", "backend", "frontend")


def upstream_files(manifest_text):
    """The template paths the manifest files under an upstream key."""
    sys.path.insert(0, str(ROOT / "tools"))
    import resolve_chain
    manifest = resolve_chain.parse_manifest(manifest_text)
    return {entry["file"] for key in UPSTREAM_KEYS
            for entry in manifest.get(key) or [] if "file" in entry}


def criterion_score(name, value):
    band = CRITERIA[name]
    good, bad = band["good"], band["bad"]
    if good == bad:
        return 100.0
    position = (value - good) / (bad - good)
    return round(100 * min(max(1 - position, 0.0), 1.0), 1)


def score(doc):
    """(score, subscores, raw metrics, caps applied) for one document."""
    raw = metrics(doc)
    subs = {name: criterion_score(name, raw[name]) for name in CRITERIA}
    total = sum(CRITERIA[n]["weight"] for n in CRITERIA)
    value = sum(subs[n] * CRITERIA[n]["weight"] for n in CRITERIA) / total
    applied = []
    for metric, threshold, cap in CAPS:
        if raw[metric] > threshold:
            value = min(value, cap)
            applied.append(f"{metric}={raw[metric]:g}")
    return round(value, 1), subs, raw, applied


def sections(text):
    """(title, first line, Doc) for each H2 section of a template."""
    lines = text.splitlines()

    # A heading inside a fenced example is part of the example, not a
    # section boundary.
    starts, fence = [], False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fence = not fence
        elif not fence and line.startswith("## "):
            starts.append(i)
    out = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        out.append((lines[start][3:].strip(), start + 1,
                    Doc("\n".join(lines[start:end]))))
    return out


def templates():
    """Every template a project reads, as paths relative to the root."""
    return sorted(p for p in TEMPLATES.rglob("*.md")
                  if "fixture" not in p.relative_to(TEMPLATES).parts)


def rel(path):
    return path.relative_to(ROOT).as_posix()


def split_by_owner(scores, owned):
    """(upstream rows, fork rows) of a score table, by manifest ownership."""
    upstream = {n: v for n, v in scores.items() if n in owned}
    fork = {n: v for n, v in scores.items() if n not in owned}
    return upstream, fork


def read_baseline(path):
    rows = {}
    if path.exists():
        for line in io.open(path, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if line:
                name, value = line.rsplit(None, 1)
                rows[name] = float(value)
    return rows


def write_baseline(path, rows, header):
    with io.open(path, "w", encoding="utf-8", newline="\n") as out:
        out.write(header)
        for name in sorted(rows):
            out.write(f"{name} {rows[name]:.1f}\n")


BASELINE_HEADER = """\
# Template quality scores, recorded by `py tools/score_templates.py --update`.
# `--check` fails a template scoring below its row here, a template with no
# row scoring below the new-file floor, and a row naming no template. Raise
# a row by improving the template and re-recording; never lower one by hand.
"""


def unmoved_baselines():
    """A line per baseline still at its old path, naming where it goes."""
    return [f"{rel(old)} is at its old path; move it to {rel(new)}"
            for old, new in MOVED_BASELINES.items() if old.exists()]


def check(scores, baseline, fork_baseline):
    """Findings for the ratchet: each a line naming the file and why."""
    findings = []
    recorded = {**baseline, **fork_baseline}
    for name, value in sorted(scores.items()):
        if name in recorded:
            if value < recorded[name] - TOLERANCE:
                findings.append(f"{name}: {value:.1f} below its baseline "
                                f"{recorded[name]:.1f}")
        elif value < NEW_FILE_FLOOR:
            findings.append(f"{name}: {value:.1f}, no baseline row, below the "
                            f"new-file floor {NEW_FILE_FLOOR}")
    for name in sorted(set(recorded) - set(scores)):
        findings.append(f"{name}: baseline row names no template")
    return findings


# ---- planted cases -----------------------------------------------------

GOOD = """# Planted
[ID: planted]

## Keys

- Use namespaced keys: `<service>:<entity>:<id>`
- Never build a key from unvalidated input
- Include a version segment when the cached schema changes
- Prefer no cache over a stale one for financial data
- Set a TTL on every entry
"""

ESSAY_RULE = (
    "- A cache SHOULD be considered carefully, because a cache that is added "
    "without thought tends to go stale in ways that are hard to see. This is "
    "a distinct class of failure from a slow query, and more severe, since "
    "the failure is wrong data rather than slow data. It was seen in one "
    "project during an outage, where the reader trusted a value that had "
    "long since changed upstream and nothing reported it. The usual answer "
    "is to invalidate where possible and generally to keep entries short.\n")

ESSAY = ("# Planted\n[ID: planted]\n\n## Caching\n\n"
         + "Caching is a trade between speed and freshness, and every team "
         "meets it sooner or later, usually after an incident that nobody "
         "saw coming and that took a long time to trace back to a value "
         "served from a cache long after the source had changed. The rules "
         "below came out of several such incidents, and each of them "
         "records what went wrong as much as what to do about it, so a "
         "reader can follow the reasoning and apply it where the rule does "
         "not quite reach.\n\n" + ESSAY_RULE * 6)


def self_test():
    cases = []
    good = score(Doc(GOOD))[0]
    cases.append(("short imperative rules score 85 or above", good >= 85, good))
    essay = score(Doc(ESSAY))[0]
    cases.append(("essay-like rules score 40 or below", essay <= 40, essay))
    cited = score(Doc(GOOD + "- Read the cache rules (#1234)\n"))
    cases.append(("a ticket citation caps the score at 50",
                  cited[0] <= 50 and cited[3], cited[0]))
    quoted = score(Doc(GOOD + '- Never write "see #123" in a rule\n'))
    cases.append(("a quoted citation does not cap", not quoted[3], quoted[0]))
    fenced = score(Doc(GOOD + "\n```bash\n" + "echo a very long line\n" * 80
                       + "```\n"))[0]
    cases.append(("fenced code does not move the score", fenced == good,
                  fenced))
    apostrophes = score(Doc(GOOD + "- Follow the team's ADR-123 for the "
                            "cache's keys\n"))
    cases.append(("apostrophes do not hide a citation",
                  apostrophes[0] <= 50 and apostrophes[3], apostrophes[0]))
    for quoted_form in ("- Never write 'see #123' in a rule\n",
                        "- Never write 'don't cite #123' in a rule\n"):
        single = score(Doc(GOOD + quoted_form))
        cases.append((f"a single-quoted citation does not cap: "
                      f"{quoted_form.strip()}", not single[3], single[0]))
    table = "\n| Key | Meaning |\n|---|---|\n" + "| a | b |\n" * 40
    tabled = score(Doc(GOOD + table))[0]
    cases.append(("a table does not move the score", tabled == good, tabled))
    fenced_heading = ("# P\n\n## Rules\n\n- Use X\n\n```markdown\n## Example\n"
                      "- not a rule\n```\n\n- Never do Y\n")
    split = sections(fenced_heading)
    rules = [i.text for i in split[0][2].items] if split else []
    cases.append(("a heading inside a fence is not a section boundary",
                  len(split) == 1 and rules == ["Use X", "Never do Y"],
                  [(t, len(d.items)) for t, _, d in split]))
    manifest = ("core: [base-git]\nbase:\n  - id: base-git\n"
                "    file: templates/core/git.md\n"
                "imbra:\n  - id: imbra-cli\n    file: templates/core/cli.md\n")
    upstream, fork = split_by_owner(
        {"templates/core/git.md": 90.0, "templates/core/cli.md": 50.0},
        upstream_files(manifest))
    cases.append(("ownership follows the manifest key, not the directory",
                  list(upstream) == ["templates/core/git.md"]
                  and list(fork) == ["templates/core/cli.md"],
                  (sorted(upstream), sorted(fork))))
    findings = check({"a": 79.0, "b": 80.05, "c": 60.0},
                     {"a": 80.0, "b": 80.1, "gone": 75.0}, {})
    expect = {"a", "c", "gone"}
    named = {f.split(":")[0] for f in findings}
    cases.append(("the ratchet fails a drop, a new file under the floor and "
                  "a stale row, and passes a rounding drift",
                  named == expect, sorted(named)))
    failed = 0
    for label, ok, value in cases:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}  ({value})")
        failed += not ok
    print(f"planted cases: {len(cases)}, failed: {failed}")
    return failed


# ---- CLI ---------------------------------------------------------------

SHORT = {"rule_words": "rule", "long_rules": "long", "paragraph_share": "para",
         "longest_paragraph": "maxP", "sentence_words": "sent",
         "multi_sentence": "multi", "directive_share": "dir",
         "hedges": "hedge", "narrative": "narr", "section_lines": "sect"}


def score_all():
    out = {}
    for path in templates():
        out[rel(path)] = score(Doc(path.read_text(encoding="utf-8")))
    return out


def print_table(results):
    print(f"{'template':40} {'score':>5}  "
          + " ".join(f"{SHORT[n]:>5}" for n in CRITERIA) + "  caps")
    for name, (value, subs, _, caps) in sorted(results.items(),
                                               key=lambda kv: kv[1][0]):
        print(f"{name:40} {value:5.1f}  "
              + " ".join(f"{subs[n]:5.0f}" for n in CRITERIA)
              + ("  " + ", ".join(caps) if caps else ""))
    values = [r[0] for r in results.values()]
    print(f"\ntemplates scored: {len(values)}, median "
          f"{statistics.median(values):.1f}, below 50: "
          f"{sum(v < 50 for v in values)}")


def print_detail(path):
    text = path.read_text(encoding="utf-8")
    doc = Doc(text)
    value, subs, raw, caps = score(doc)
    print(f"{rel(path)}: {value:.1f}" + (f" (capped: {', '.join(caps)})"
                                          if caps else ""))
    for name in CRITERIA:
        print(f"  {name:18} {raw[name]:8.2f}  -> {subs[name]:5.1f}")
    print("  longest rules:")
    for item in sorted(doc.items, key=lambda i: -i.words)[:5]:
        print(f"    line {item.line}: {item.words} words, "
              f"{item.sentences} sentences")
    print("  lowest sections:")
    ranked = sorted((score(d)[0], title, line)
                    for title, line, d in sections(text) if d.items)
    for value, title, line in ranked[:5]:
        print(f"    {value:5.1f}  line {line}: {title}")


def print_sections(limit=25):
    rows = []
    for path in templates():
        text = path.read_text(encoding="utf-8")
        for title, line, doc in sections(text):
            if len(doc.items) >= 3:
                rows.append((score(doc)[0], rel(path), line, title, doc.words))
    print(f"{'score':>5}  {'words':>5}  section")
    for value, name, line, title, words in sorted(rows)[:limit]:
        print(f"{value:5.1f}  {words:5}  {name}:{line} {title}")
    print(f"\nsections scored: {len(rows)}")


def calibrate():
    rows = {name: metrics(Doc(p.read_text(encoding="utf-8")))
            for name, p in ((rel(p), p) for p in templates())}
    for metric in list(CRITERIA) + [m for m, _, _ in CAPS]:
        values = sorted(r[metric] for r in rows.values())
        deciles = statistics.quantiles(values, n=10)
        print(f"{metric:18} p10 {deciles[0]:7.2f}  p50 "
              f"{statistics.median(values):7.2f}  p90 {deciles[8]:7.2f}")


def main(args):
    if "--self-test" in args:
        return 1 if self_test() else 0
    if "--calibrate" in args:
        calibrate()
        return 0
    if "--sections" in args:
        print_sections()
        return 0
    names = [a for a in args if not a.startswith("--")]
    if names:
        for name in names:
            print_detail((ROOT / name).resolve())
        return 0
    if "--update" in args or "--check" in args:
        unmoved = unmoved_baselines()
        if unmoved:
            for line in unmoved:
                print(f"refusing: {line}")
            return 1
    results = score_all()
    scores = {name: r[0] for name, r in results.items()}
    if "--update" in args:
        manifest = (TEMPLATES / "manifest.yaml").read_text(encoding="utf-8")
        upstream, fork = split_by_owner(scores, upstream_files(manifest))
        write_baseline(BASELINE, upstream, BASELINE_HEADER)
        if fork:
            write_baseline(FORK_BASELINE, fork, BASELINE_HEADER)
        print(f"recorded: {len(upstream)} upstream, {len(fork)} fork")
        return 0
    if "--check" in args:
        if self_test():
            return 1
        if not scores:
            print("templates scored: 0 -- refusing: nothing was measured")
            return 1
        findings = check(scores, read_baseline(BASELINE),
                         read_baseline(FORK_BASELINE))
        print(f"templates scored: {len(scores)}")
        print(f"findings: {len(findings)}")
        for finding in findings:
            print(f"  {finding}")
        return 1 if findings else 0
    print_table(results)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
