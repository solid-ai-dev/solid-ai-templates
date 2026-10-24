"""Ask several models, through the Claude Code and Codex CLIs, to review the
templates against the project goal and score them from 1 to 10.

Usage:
    py tools/ask_reviewers.py                       # every default model
    py tools/ask_reviewers.py --models a,b          # the named models only
    py tools/ask_reviewers.py --effort medium       # reasoning effort, default high
    py tools/ask_reviewers.py --timeout 1800        # seconds per model
    py tools/ask_reviewers.py --dry-run             # print the commands only

A model named `claude-*` runs through `claude`, any other through `codex`.
Every reviewer reads the same bundle on standard input and answers in one
JSON shape. The script writes a timestamped Markdown report and the raw
answers to tests/reports/. It exits 0 when every reviewer answered and 1
otherwise. Both CLIs bill subscription quota; no API key is read.
"""

import concurrent.futures
import datetime
import json
import pathlib
import shutil
import statistics
import subprocess
import sys
import tempfile

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
REPORTS = ROOT / "tests" / "reports"

DEFAULT_MODELS = ("claude-opus-5-5", "claude-sonnet-5-5",
                  "gpt-6.1-sol", "gpt-6-astra")

# What a consuming project adopts: the README and spec say what the
# templates are for, the manifest how they compose. The fixture is test
# input, not a template anyone adopts.
CONTEXT_FILES = ("README.md", "docs/spec.md", "templates/manifest.yaml")
EXCLUDED = ("fixture",)

CRITERIA = {
    "consistency": "Agents following these templates produce the same "
                   "conventions across teams, sessions and models",
    "quality_lift": "The policies move typical agent output from average "
                    "to good enough",
    "human_effort": "Adopting and following them takes little effort from "
                    "the human developers",
    "focus": "They leave the humans free to concentrate on architecture "
             "and design",
}

SCORE = {"type": "integer", "minimum": 1, "maximum": 10}
FINDING = {
    "type": "object",
    "properties": {"file": {"type": "string"}, "point": {"type": "string"}},
    "required": ["file", "point"],
    "additionalProperties": False,
}
RECOMMENDATION = {
    "type": "object",
    "properties": {
        "file": {"type": "string"},
        "change": {"type": "string"},
        "effect": {"type": "string"},
    },
    "required": ["file", "change", "effect"],
    "additionalProperties": False,
}

# Every property is required and none is open, because Codex's structured
# output refuses a schema that leaves either unstated.
SCHEMA = {
    "type": "object",
    "properties": {
        "score": SCORE,
        "criteria": {
            "type": "object",
            "properties": {name: SCORE for name in CRITERIA},
            "required": list(CRITERIA),
            "additionalProperties": False,
        },
        "summary": {"type": "string"},
        "strengths": {"type": "array", "items": FINDING},
        "weaknesses": {"type": "array", "items": FINDING},
        "drift_risks": {"type": "array", "items": FINDING},
        "recommendations": {"type": "array", "items": RECOMMENDATION},
    },
    "required": ["score", "criteria", "summary", "strengths", "weaknesses",
                 "drift_risks", "recommendations"],
    "additionalProperties": False,
}

PROMPT = """\
You are reviewing solid-ai-templates, a set of Markdown templates a project
composes into the instruction file (AGENTS.md, CLAUDE.md) its AI coding
agents read. Everything you need is in this message; do not use tools.

The goal of the templates:

- Keep AI agents consistent across teams, projects and sessions.
- Supply useful policies that move generated output from average to good
  enough.
- Ask minimal effort from the human developers, so that they can focus on
  architecture and design.

Judge the templates as an engineering lead deciding whether to adopt them.
Score each criterion from 1 (fails it) to 10 (could not be better), then
give one overall score from 1 to 10 for how well the templates meet the
goal. Be specific and critical; a generous score helps no one.

Criteria:
{criteria}

Then report:

- summary: three to five sentences on your verdict.
- strengths: what works, each with the file it is in.
- weaknesses: what fails the goal, each with its file.
- drift_risks: rules an agent is likely to ignore, misread or apply
  inconsistently, each with its file.
- recommendations: at most seven changes, most valuable first, each with
  the file, the change and its expected effect on the goal.

Name files by their path as given in the headers below.

{bundle}
"""


def bundle():
    """Return the files a reviewer reads, each under its path."""
    paths = [ROOT / name for name in CONTEXT_FILES]
    paths += sorted(path for path in TEMPLATES.rglob("*.md")
                    if path.relative_to(TEMPLATES).parts[0] not in EXCLUDED)
    parts = []

    for path in paths:
        text = path.read_text(encoding="utf-8")
        parts.append("===== %s =====\n%s" % (path.relative_to(ROOT).as_posix(),
                                              text.rstrip()))
    return "\n\n".join(parts)


def prompt():
    """Return the review prompt with the criteria and the bundle filled in."""
    criteria = "\n".join("- %s: %s." % item for item in CRITERIA.items())
    return PROMPT.format(criteria=criteria, bundle=bundle())


def claude_argv(executable, model, effort):
    """Return the command for one review through Claude Code.

    No tools, no MCP servers, no session file, and no setting source, so
    neither the user's global CLAUDE.md nor this repository's reaches the
    reviewer.
    """
    return [executable, "--print",
            "--model", model,
            "--effort", effort,
            "--tools", "",
            "--strict-mcp-config",
            "--setting-sources", "",
            "--no-session-persistence",
            "--output-format", "json",
            "--json-schema", json.dumps(SCHEMA)]


def codex_argv(executable, model, effort, workdir, schema, last):
    """Return the command for one review through Codex.

    The user's config.toml is skipped, because it pins a low reasoning
    effort, and the effort is set on the command instead. The reviewer
    runs read-only in an empty directory, so no AGENTS.md reaches it.
    """
    return [executable, "exec",
            "--model", model,
            "--ignore-user-config",
            "--ignore-rules",
            "-c", 'model_reasoning_effort="%s"' % effort,
            "--sandbox", "read-only",
            "--ephemeral",
            "--skip-git-repo-check",
            "-C", str(workdir),
            "--output-schema", str(schema),
            "--output-last-message", str(last),
            "-"]


def review(model, effort, text, timeout, dry_run):
    """Run one reviewer and return its record: the answer or the error."""
    cli = "claude" if model.startswith("claude-") else "codex"
    executable = shutil.which(cli)
    record = {"model": model, "cli": cli, "effort": effort}
    if executable is None:
        record["error"] = "%s is not on PATH" % cli
        return record

    with tempfile.TemporaryDirectory(prefix="ask-reviewers-") as scratch:
        workdir = pathlib.Path(scratch)
        schema = workdir / "schema.json"
        last = workdir / "last-message.json"
        schema.write_text(json.dumps(SCHEMA), encoding="utf-8")
        if cli == "claude":
            argv = claude_argv(executable, model, effort)
        else:
            argv = codex_argv(executable, model, effort, workdir, schema, last)

        # The schema argument is long and quoted; the record keeps its name.
        record["argv"] = [part if part != json.dumps(SCHEMA) else "<schema>"
                          for part in argv]
        if dry_run:
            return record

        # The prompt goes on standard input: the Codex shim runs through
        # cmd.exe, which ends a command at a newline inside an argument.
        started = datetime.datetime.now()
        try:
            outcome = subprocess.run(argv, input=text, cwd=workdir,
                                     capture_output=True, encoding="utf-8",
                                     errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            record["error"] = "no answer within %d seconds" % timeout
            return record
        record["seconds"] = round((datetime.datetime.now()
                                   - started).total_seconds())
        said = (outcome.stderr or outcome.stdout or "").strip()[-600:]

        if cli == "claude":
            answer, error = claude_answer(outcome.stdout)
        else:
            answer, error = codex_answer(last)
        if error:
            record["error"] = "%s; the CLI said: %s" % (error, said)
        else:
            record["answer"] = answer
    return record


def claude_answer(stdout):
    """Return (answer, error) from Claude Code's JSON result."""
    try:
        result = json.loads(stdout)
    except ValueError:
        return None, "the output was not JSON"
    if result.get("is_error") or "structured_output" not in result:
        return None, "no structured output (%s)" % result.get("subtype")
    return result["structured_output"], None


def codex_answer(last):
    """Return (answer, error) from the final message Codex wrote."""
    if not last.exists():
        return None, "no final message was written"
    text = last.read_text(encoding="utf-8").strip()
    try:
        return json.loads(text), None
    except ValueError:
        return None, "the final message was not JSON: %s" % text[:300]


def report(records, started):
    """Return the Markdown report over every reviewer's record."""
    answered = [r for r in records if "answer" in r]
    names = list(CRITERIA)
    lines = ["# Template review by models", "",
             "Run %s. Each reviewer read the same bundle and scored the "
             "templates from 1 to 10." % started.strftime("%Y-%m-%d %H:%M"),
             "", "| Model | CLI | Score | %s |" % " | ".join(names),
             "|---|---|---|" + "---|" * len(names)]

    for record in records:
        if "answer" in record:
            answer = record["answer"]
            cells = [str(answer["score"])]
            cells += [str(answer["criteria"][name]) for name in names]
        else:
            cells = ["failed"] + ["-"] * len(names)
        lines.append("| %s | %s | %s |" % (record["model"], record["cli"],
                                            " | ".join(cells)))

    # Each model is its own instrument, so the median and range describe
    # the spread of their verdicts rather than averaging them into one.
    if answered:
        scores = [r["answer"]["score"] for r in answered]
        lines += ["", "Median score %s, range %d to %d, across %d reviewers."
                  % (statistics.median(scores), min(scores), max(scores),
                     len(scores))]

    for record in records:
        lines += ["", "## %s" % record["model"], ""]
        if "answer" not in record:
            lines.append("Failed: %s" % record.get("error", "dry run"))
            continue
        answer = record["answer"]
        lines += [answer["summary"].strip(), ""]

        for key, title in (("strengths", "Strengths"),
                           ("weaknesses", "Weaknesses"),
                           ("drift_risks", "Drift risks")):
            lines += ["### %s" % title, ""]
            lines += ["- `%s`: %s" % (item["file"], item["point"])
                      for item in answer[key]] or ["- none"]
            lines.append("")
        lines += ["### Recommendations", ""]
        lines += ["%d. `%s`: %s Effect: %s" % (number, item["file"],
                                                item["change"], item["effect"])
                  for number, item in enumerate(answer["recommendations"], 1)]
    return "\n".join(lines).rstrip() + "\n"


def options(args):
    """Return the parsed command line, or exit 2 on an unknown argument."""
    parsed = {"models": list(DEFAULT_MODELS), "effort": "high",
              "timeout": 1800, "dry_run": False}
    args = list(args)

    while args:
        arg = args.pop(0)
        if arg == "--dry-run":
            parsed["dry_run"] = True
        elif arg == "--models" and args:
            parsed["models"] = [m.strip() for m in args.pop(0).split(",")
                                if m.strip()]
        elif arg == "--effort" and args:
            parsed["effort"] = args.pop(0)
        elif arg == "--timeout" and args and args[0].isdigit():
            parsed["timeout"] = int(args.pop(0))
        else:
            print("unknown or incomplete argument: %s" % arg, file=sys.stderr)
            print(__doc__, file=sys.stderr)
            sys.exit(2)
    return parsed


def main(args):
    parsed = options(args)
    text = prompt()
    started = datetime.datetime.now()
    print("bundle: %d characters, reviewers: %s"
          % (len(text), ", ".join(parsed["models"])))

    # The reviewers run at once: each waits on its own model, not on the
    # machine, and a full run would otherwise take one review per model.
    with concurrent.futures.ThreadPoolExecutor(len(parsed["models"])) as pool:
        records = list(pool.map(
            lambda model: review(model, parsed["effort"], text,
                                 parsed["timeout"], parsed["dry_run"]),
            parsed["models"]))

    if parsed["dry_run"]:
        for record in records:
            print(" ".join(record.get("argv") or [record.get("error", "")]))
        return 0

    REPORTS.mkdir(parents=True, exist_ok=True)
    stem = REPORTS / ("%s-ask_reviewers" % started.strftime("%Y%m%d-%H%M%S"))
    markdown = stem.with_suffix(".md")
    markdown.write_text(report(records, started), encoding="utf-8")
    stem.with_suffix(".json").write_text(json.dumps(records, indent=2),
                                         encoding="utf-8")

    for record in records:
        state = (record["answer"]["score"] if "answer" in record
                 else "failed: %s" % record["error"][:200])
        print("%-20s %s" % (record["model"], state))
    print("report: %s" % markdown.relative_to(ROOT).as_posix())
    return 0 if all("answer" in r for r in records) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
