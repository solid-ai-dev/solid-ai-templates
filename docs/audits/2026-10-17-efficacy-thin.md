# Efficacy benchmark — 2026-10-17

Does a generated context file improve the result? The question, the verdict rule and the
metric directions were fixed before any trial ran, in
`docs/design/efficacy-benchmark.md`.

**Every interval below is descriptive.** At K = 3 no arrangement of paired differences
reaches conventional significance, which the design states and this report repeats
rather than footnotes.

## Executive summary

| | Templates' inline file, 391 lines | Templates' short inline file, 39 lines | Templates' hybrid file, 516 lines | Hand-written file, 39 lines |
|---|---|---|---|---|
| Improves the code? | **Worse** | **Yes** | **Worse** | **Yes** |
| Readability, design, maintainability | security probes +27.3 pp | did not move | security +1.9, security probes -31.8 pp, data-protection probes -66.7 pp | security probes +31.8 pp |
| Hidden tests passed, against 92 % without a file | 77 %, two run of three at 69 % | 95 % | 42 %, three run of three at 42 % | 63 %, one run of three at 0 % |
| Code size | lines +84 %, files +137 % | lines +57 %, files +98 % | lines +70 % | no change shown |
| Cost | +80 % | +57 % | +99 % | +141 % |
| Reads as | bulk and cost, worse quality | quality, with bulk | bulk and cost, worse quality | quality, no bulk |

**Templates' inline file, Worse.** It built more than the task asked for: more files and
more code, and took more turns and cost to do it. The judge saw none of it as better
design, readability, maintainability, security or data protection; every win is
something a tool counts.

**Templates' short inline file, Yes.** It built more than the task asked for: more files
and more code, and took more turns, tokens and cost to do it. The judge saw none of it
as better design, readability, maintainability, security or data protection; every win
is something a tool counts.

**Templates' hybrid file, Worse.** Three run of three left the app unable to boot
(`RuntimeError('TARIFF_SECRET_KEY must be set to a non-empty value')`). It built more
than the task asked for: more code and more public names beyond the spec, and took more
turns, tokens and cost to do it. The judge read its code as more secure.

**Hand-written file, Yes.** One run of three left the app unable to boot (`no error
recorded`). It built more than the task asked for: more public names beyond the spec,
and took more time and cost to do it. The judge saw none of it as better design,
readability, maintainability, security or data protection; every win is something a tool
counts.

Together, reading the longest file beside the shortest (templates' hybrid file,
templates' short inline file): length is not quality — the long file spent the agent's
attention on conventions, the short one on the code. K = 3, one project: a signal, not
proof.

Between the files, 1 to 10: full − hand 7.2 (9 won, 4 failed); short − hand 5.5 (8 won,
8 failed); hybrid − full 6.5 (8 won, 5 failed); short − full 6.0 (5 won, 4 failed). A
win or a fail is a metric whose interval separated the pair in its declared direction,
each counting once; the score is 1 + 9 × wins ÷ (wins + fails), digests the verdict
vector at the end, and decides nothing.

Caveats: 15 trials, 15 judged; escalation to K = 5 owed and not yet run; withdrawn:
nothing; lost and re-run: hand-1, completed; none-3, completed; reached past their
workspace: none; the judge is checked only by its evidence lines.

## What produced these numbers

| | |
|---|---|
| Trials | 15, arms none, full, short, hybrid, hand, K = 3 |
| Generator | `claude-sonnet-5` |
| Judge | `claude-opus-5-5` at effort `high`, claude |
| Blinding | condition markers stripped, order shuffled at seed 20260912 |
| Judgings per trial | 3, meaned |
| Templates revision | `73ee7e6` |
| Hidden suite | `65bfb9a8590bfcd0096fdb6c0c6ae7be4d8ed5c6` |
| Bootstrap | 10000 resamples, 95%, seed 20260912 |
| Arm full's file | generated 2026-09-26T12:16:08, 391 lines, leak scan: clean |
| Arm short's file | generated 2026-09-26T14:28:59, 39 lines, leak scan: clean |
| Arm hybrid's file | generated 2026-09-26T12:18:26, 516 lines, leak scan: clean |

## Primary dimensions

The report leads with these, owner-declared in the design: five judge rows and two probe
pass rates. Task success and cost follow.

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 3 | 3 | 3 | 3 | 2.333 | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | -0.667 (-2, 0) — no improvement shown, not preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points |
| Readability, 1-5 | up | 2.667 | 3.333 | 3 | 3.556 | 2.556 | 0.667 (0, 1.111) — no improvement shown, preserved within 0.3 points | 0.333 (0, 0.667) — no improvement shown, preserved within 0.3 points | 0.889 (0, 1.444) — no improvement shown, preserved within 0.3 points | -0.111 (-2, 1.000) — no improvement shown, not preserved within 0.3 points | 0.778 (-0.333, 1.778) — no improvement shown, not preserved within 0.3 points | 0.444 (-0.333, 1.222) — no improvement shown, not preserved within 0.3 points | 0.222 (0, 0.333) — no improvement shown, preserved within 0.3 points | -0.333 (-0.667, -0.111) — worse |
| Maintainability, 1-5 | up | 3 | 3 | 3 | 3 | 2.333 | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | -0.667 (-2, 0) — no improvement shown, not preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points |
| Security, 1-5 | up | 1.444 | 1.889 | 2 | 3.333 | 2.444 | 0.444 (-0.333, 0.889) — no improvement shown, not preserved within 0.3 points | 0.556 (0, 0.889) — no improvement shown, preserved within 0.3 points | 1.889 (1, 2.333) — better | 1 (0, 1.556) — no improvement shown, preserved within 0.3 points | -0.556 (-1.667, 0.333) — no improvement shown, not preserved within 0.3 points | -0.444 (-1.333, 0.333) — no improvement shown, not preserved within 0.3 points | 1.444 (0, 2.333) — no improvement shown, preserved within 0.3 points | 0.111 (0, 0.222) — no improvement shown, preserved within 0.3 points |
| Data protection, 1-5 | up | 2.333 | 2.333 | 3 | 3.111 | 2 | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points | 0.778 (0, 1.556) — no improvement shown, preserved within 0.3 points | -0.333 (-2, 0.667) — no improvement shown, not preserved within 0.3 points | 0.333 (-1, 1.333) — no improvement shown, not preserved within 0.3 points | 1 (0, 1.667) — no improvement shown, preserved within 0.3 points | 0.778 (0, 1.556) — no improvement shown, preserved within 0.3 points | 0.667 (0, 1.333) — no improvement shown, preserved within 0.3 points |
| Security probe pass rate, of eleven | up | 0.606 | 0.879 | 0.697 | 0.318 | 0.909 | 0.273 (0.182, 0.333) — better | 0.091 (0, 0.151) — no improvement shown, preserved within 2 pp | -0.318 (-0.364, -0.318) — worse | 0.318 (0.273, 0.318) — better | -0.045 (-0.091, -0.045) — worse | -0.227 (-0.273, -0.227) — worse | -0.545 (-0.636, -0.546) — worse | -0.182 (-0.182, -0.182) ‡ — worse |
| Data-protection probe pass rate, of three | up | 0.667 | 0.778 | 0.667 | 0 | 0.444 | 0.111 (0, 0.222) — no improvement shown, preserved within 10 pp | 0 (0, 0) ‡ — no improvement shown, preserved within 10 pp | -0.667 (-0.667, -0.667) ‡ — worse | -0.222 (-0.667, 0) — no improvement shown, not preserved within 10 pp | 0.333 (0, 0.667) — no improvement shown, preserved within 10 pp | 0.222 (0, 0.444) — no improvement shown, preserved within 10 pp | -0.778 (-1, -0.667) — worse | -0.111 (-0.333, 0) — no improvement shown, not preserved within 10 pp |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## The escalation to K = 5

Fixed before the run: one escalation is owed where a primary dimension's interval
contains zero while its mean paired difference exceeds 0.5 points, 9 pp for the security
probes or 30 pp for the data-protection probes in either direction, on any contrast. K
never exceeds 5.

**Owed.** Run blocks 4 to 5 with `--k 5 --from none-4`, then report again. A row still
containing zero at K = 5 is reported as no improvement shown.

| Metric | Contrast | Mean difference | Interval | Threshold |
|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | hand−none | -0.667 | (-2, 0) | 0.5 points |
| Design (SOLID and patterns), 1-5 | full−hand | 0.667 | (0, 1.333) | 0.5 points |
| Design (SOLID and patterns), 1-5 | short−hand | 0.667 | (0, 1.333) | 0.5 points |
| Readability, 1-5 | full−none | 0.667 | (0, 1.111) | 0.5 points |
| Readability, 1-5 | hybrid−none | 0.889 | (0, 1.444) | 0.5 points |
| Readability, 1-5 | full−hand | 0.778 | (-0.333, 1.778) | 0.5 points |
| Maintainability, 1-5 | hand−none | -0.667 | (-2, 0) | 0.5 points |
| Maintainability, 1-5 | full−hand | 0.667 | (0, 1.333) | 0.5 points |
| Maintainability, 1-5 | short−hand | 0.667 | (0, 1.333) | 0.5 points |
| Security, 1-5 | short−none | 0.556 | (0, 0.889) | 0.5 points |
| Security, 1-5 | hand−none | 1 | (0, 1.556) | 0.5 points |
| Security, 1-5 | full−hand | -0.556 | (-1.667, 0.333) | 0.5 points |
| Security, 1-5 | hybrid−full | 1.444 | (0, 2.333) | 0.5 points |
| Data protection, 1-5 | short−none | 0.667 | (0, 1.333) | 0.5 points |
| Data protection, 1-5 | hybrid−none | 0.778 | (0, 1.556) | 0.5 points |
| Data protection, 1-5 | short−hand | 1 | (0, 1.667) | 0.5 points |
| Data protection, 1-5 | hybrid−full | 0.778 | (0, 1.556) | 0.5 points |
| Data protection, 1-5 | short−full | 0.667 | (0, 1.333) | 0.5 points |
| Security probe pass rate, of eleven | short−none | 0.091 | (0, 0.151) | 9 pp |
| Data-protection probe pass rate, of three | full−hand | 0.333 | (0, 0.667) | 30 pp |

## Task success, adherence and cost

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 0.915 | 0.769 | 0.946 | 0.418 | 0.631 | -0.146 (-0.235, -0.068) — worse | 0.031 (0.002, 0.051) — better | -0.497 (-0.509, -0.485) — worse | -0.284 (-0.891, 0.027) — no improvement shown, not preserved within 2 pp | 0.138 (-0.276, 0.460) — no improvement shown, not preserved within 2 pp | 0.315 (-0.009, 0.635) — no improvement shown, preserved within 2 pp | -0.351 (-0.506, -0.273) — worse | 0.177 (0.004, 0.265) — better |
| Installs in a clean environment | up | 1 | 1 | 1 | 1 | 0.667 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -0.333 (-1, 0) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Adherence checklist fraction | up | 0.515 | 0.656 | 0.583 | 0.583 | 0.583 | 0.141 (0.109, 0.160) — better | 0.068 (0.038, 0.084) — better | 0.068 (0, 0.123) — no improvement shown, preserved within 5 pp | 0.102 (0.038, 0.102) — better | 0.054 (0, 0.054) — no improvement shown, preserved within 5 pp | -0.042 (-0.083, -0.041) — worse | -0.073 (-0.109, -0.036) — worse | -0.072 (-0.109, -0.044) — worse |
| Output tokens | down | 87099.3 | 113195.3 | 112777.3 | 134165.7 | 66226 | 26096 (-13266, 46411) — no improvement shown | 25678 (2894, 40008) — worse | 47066.3 (9356, 73349) — worse | -24015 (-105327, -24015) — better | 39319.5 (-13422, 39319.5) — no improvement shown | 48404 (-11413, 48404) — no improvement shown | 20970.3 (-4040, 37093.3) — no improvement shown | -418 (-19423, 11443) — no improvement shown |
| Turns | down | 72.333 | 118 | 107 | 123.667 | 72.500 | 45.667 (11, 66.333) — worse | 34.667 (16, 49) — worse | 51.333 (13, 75.667) — worse | -6 (-91, -6) — better | 38 (-26, 38) — no improvement shown | 43.500 (-20, 43.500) — no improvement shown | 5.667 (-18, 22.667) — no improvement shown | -11 (-44, 5.667) — no improvement shown |
| Wall time, seconds | down | 1377.6 | 3387.6 | 1399.1 | 2393.8 | 2108.9 | 2010.0 (-352.400, 4043.9) — no improvement shown | 21.533 (-428.700, 288.100) — no improvement shown | 1016.2 (-31.100, 1787.5) — no improvement shown | 543.950 (532.900, 543.950) — worse | -403.750 (-907.400, -403.750) — better | -572.800 (-983.700, -572.800) — better | -993.800 (-3466.6, 268.833) — no improvement shown | -1988.4 (-5627.2, -138.133) — better |
| Cost, USD | down | 2.910 | 5.224 | 4.569 | 5.797 | 7.249 | 2.314 (0.115, 3.640) — worse | 1.659 (0.530, 2.514) — worse | 2.887 (0.697, 4.413) — worse | 4.089 (4.029, 4.089) — worse | -2.665 (-4.034, -2.665) — better | -2.276 (-3.618, -2.276) — better | 0.574 (-1.402, 1.888) — no improvement shown | -0.655 (-2.743, 0.398) — no improvement shown |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## The change task

How far each design had to be disturbed to take a change it was not built for, read
beside whether the change works and whether the build still passes after it.

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Change task, acceptance pass rate | up | — | — | — | — | — | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |
| Change task, build suite pass rate after it | up | — | — | — | — | — | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |
| Change task, files touched | down | — | — | — | — | — | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |
| Change task, lines changed | down | — | — | — | — | — | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |
| Change task, cost, USD | down | — | — | — | — | — | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |

## Every other metric

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SRP, 1-5 | up | 3 | 3.333 | 3 | 3.778 | 2.444 | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.778 (0.667, 0.889) — better | -0.556 (-2, 0.222) — no improvement shown | 0.889 (-0.333, 1.667) — no improvement shown | 0.556 (-0.333, 1.333) — no improvement shown | 0.444 (0, 0.667) — no improvement shown | -0.333 (-1, 0) — no improvement shown |
| OCP, 1-5 | up | 2 | 2 | 2 | 2 | 1.667 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -0.333 (-1, 0) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| LSP, 1-5 | up | 2.889 | 3 | 3 | 3.333 | 2.333 | 0.111 (0, 0.222) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.444 (0, 0.778) — no improvement shown | -0.556 (-2, 0.222) — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0.333 (-0.333, 0.778) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| ISP, 1-5 | up | 4 | 4 | 4 | 4 | 3 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -1 (-3, 0) — no improvement shown | 1 (0, 2) — no improvement shown | 1 (0, 2) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| DIP, 1-5 | up | 4 | 3.778 | 4.111 | 4.222 | 3 | -0.222 (-0.667, 0) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.222 (0, 0.333) — no improvement shown | -1 (-3, 0) — no improvement shown | 0.778 (-0.667, 2) — no improvement shown | 1.111 (0, 2.111) — no improvement shown | 0.444 (0.333, 0.556) — better | 0.333 (0, 0.667) — no improvement shown |
| Naming and abstraction, 1-5 | up | 3.556 | 4 | 4 | 3.667 | 3 | 0.444 (0, 0.778) — no improvement shown | 0.444 (0, 0.778) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | -0.556 (-3, 0.778) — no improvement shown | 1 (0, 2) — no improvement shown | 1 (0, 2) — no improvement shown | -0.333 (-1, 0) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Error design, 1-5 | up | 3.111 | 3 | 3.444 | 3.444 | 2.667 | -0.111 (-0.333, 0) — no improvement shown | 0.333 (0, 0.556) — no improvement shown | 0.333 (-0.333, 0.778) — no improvement shown | -0.444 (-2, 0.556) — no improvement shown | 0.333 (-1, 1.333) — no improvement shown | 0.778 (-0.667, 1.889) — no improvement shown | 0.444 (0, 0.778) — no improvement shown | 0.444 (0.333, 0.556) — better |
| Test quality, 1-5 | up | 4 | 3.667 | 3.889 | 4 | 2.889 | -0.333 (-1, 0) — no improvement shown | -0.111 (-0.333, 0) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -1.111 (-3, -0.111) — worse | 0.778 (-0.667, 2) — no improvement shown | 1 (-0.333, 2.111) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.222 (-0.333, 0.667) — no improvement shown |
| Patterns warranted | up | 3.111 | 3.222 | 3.111 | 4.667 | 2.111 | 0.111 (-0.333, 0.333) — no improvement shown | 0 (-1.333, 0.667) — no improvement shown | 1.556 (0, 2.333) — no improvement shown | -1 (-2.667, 0.000) — no improvement shown | 1.111 (0, 2.111) — no improvement shown | 1 (-0.667, 2.333) — no improvement shown | 1.444 (0.333, 2) — better | -0.111 (-1, 0.333) — no improvement shown |
| Patterns over-engineered | down | 0.111 | 0.222 | 0 | 0.667 | 0 | 0.111 (-0.333, 0.444) — no improvement shown | -0.111 (-0.333, 0) — no improvement shown | 0.556 (-0.333, 1) — no improvement shown | -0.111 (-0.333, 0) — no improvement shown | 0.222 (0, 0.444) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.444 (0, 0.778) — no improvement shown | -0.222 (-0.667, 0) — no improvement shown |
| Patterns missed | down | 2.333 | 2.333 | 2.778 | 2.222 | 1.444 | 0 (-0.333, 0.222) — no improvement shown | 0.444 (-0.333, 0.889) — no improvement shown | -0.111 (-1.000, 0.556) — no improvement shown | -0.889 (-2.333, 0.000) — no improvement shown | 0.889 (0, 1.556) — no improvement shown | 1.333 (0.333, 2.222) — worse | -0.111 (-1.000, 0.444) — no improvement shown | 0.444 (-0.333, 0.889) — no improvement shown |
| Line coverage of the trial's own tests, % | up | 87.817 | 92.378 | 83.198 | 89.594 | 98.351 | 4.560 (0.111, 7.504) — better | -4.619 (-23.182, 5.192) — no improvement shown | 1.776 (-1.068, 3.648) — no improvement shown | 11.510 (9.556, 11.510) — better | -4.725 (-8.835, -4.725) — worse | -21.565 (-36.646, -21.565) — worse | -2.784 (-10.008, 1.133) — no improvement shown | -9.179 (-27.812, 2.138) — no improvement shown |
| Docstring coverage, % | up | 11.923 | 39.783 | 56.210 | 69.327 | 13.050 | 27.860 (13.630, 38.070) — better | 44.287 (26.760, 56.213) — better | 57.403 (46.830, 64.510) — better | -3.540 (-3.910, -3.540) — worse | 23.200 (16.800, 23.200) — better | 48.190 (30.670, 48.190) — better | 29.543 (2.570, 43.220) — better | 16.427 (-0.700, 32.963) — no improvement shown |
| Lint findings per KLOC | down | 318.217 | 114.283 | 95.833 | 86.980 | 146.415 | -203.933 (-232.920, -182.330) — better | -222.383 (-252.470, -199.990) — better | -231.237 (-249.980, -220.427) — better | -160.765 (-170.140, -160.765) — better | -28.675 (-40.630, -28.675) — better | -46.575 (-78, -46.575) — better | -27.303 (-49.440, -8.577) — better | -18.450 (-61.280, 10.470) — no improvement shown, preserved within 10 % relative |
| Lint findings | down | 489.667 | 315.333 | 226.667 | 219.333 | 476 | -174.333 (-229, -144) — better | -263 (-321, -225.667) — better | -270.333 (-303, -241) — better | -22 (-46, -22) — better | -170.500 (-231, -170.500) — better | -268 (-323, -268) — better | -96 (-147, -68.333) — better | -88.667 (-103, -78) — better |
| Files the formatter would change | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Files the formatter would change, per KLOC | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Type errors under --strict | down | 198.333 | 37.667 | 19 | 24.333 | 54.500 | -160.667 (-181, -150) — better | -179.333 (-202, -158) — better | -174 (-209, -151.333) — better | -134.500 (-174, -134.500) — better | -16 (-57, -16) — better | -33.500 (-103, -33.500) — better | -13.333 (-28, -0.333) — better | -18.667 (-46, 0.333) — no improvement shown |
| Type errors under --strict, per KLOC | down | 129.813 | 14.963 | 8.693 | 10.410 | 16.840 | -114.850 (-144.580, -99.767) — better | -121.120 (-151.130, -100.320) — better | -119.403 (-152.580, -101.373) — better | -99.820 (-107.720, -99.820) — better | -0.165 (-7.410, -0.165) — better | -6.295 (-31.580, -6.295) — better | -4.553 (-8.000, -1.607) — better | -6.270 (-24.170, 5.757) — no improvement shown, not preserved within 10 % relative |
| Security findings, high and medium | down | 0.333 | 0 | 0 | 0.333 | 0 | -0.333 (-1, 0) — no improvement shown | -0.333 (-1, 0) — no improvement shown | 0 (-1, 0.667) — no improvement shown | -0.500 (-1, -0.500) — better | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Security findings, high and medium, per KLOC | down | 0.207 | 0 | 0 | 0.100 | 0 | -0.207 (-0.620, 0) — no improvement shown, preserved within 10 % relative | -0.207 (-0.620, 0) — no improvement shown, preserved within 10 % relative | -0.107 (-0.620, 0.200) — no improvement shown, not preserved within 10 % relative | -0.310 (-0.620, -0.310) — better | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.100 (0, 0.200) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Highest cognitive complexity | down | 56.333 | 20 | 24 | 24.667 | 18.500 | -36.333 (-69, -14) — better | -32.333 (-80, -4.333) — better | -31.667 (-67, -9.667) — better | -58.500 (-80, -58.500) — better | 5 (-1, 5) — no improvement shown | 8 (0, 8) — no improvement shown | 4.667 (1, 8) — worse | 4 (-11, 13.333) — no improvement shown |
| Functions over complexity 15 | down | 1 | 1 | 1.667 | 1.333 | 1.500 | 0 (0, 0) ‡ — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0.333 (-1, 1.333) — no improvement shown | 0 (-1, 0) — no improvement shown | 0 (-1, 0) — no improvement shown | 0 (-1, 0) — no improvement shown | 0.333 (-1, 1.333) — no improvement shown | 0.667 (0, 1.333) — no improvement shown |
| Functions over complexity 15, per KLOC | down | 0.617 | 0.443 | 0.687 | 0.447 | 0.460 | -0.173 (-0.320, -0.067) — better | 0.070 (-0.360, 0.413) — no improvement shown, not preserved within 10 % relative | -0.170 (-0.800, 0.193) — no improvement shown, not preserved within 10 % relative | -0.465 (-0.930, -0.465) — better | 0.205 (-0.320, 0.205) — no improvement shown, not preserved within 10 % relative | 0.235 (-0.100, 0.235) — no improvement shown, not preserved within 10 % relative | 0.003 (-0.600, 0.407) — no improvement shown, not preserved within 10 % relative | 0.243 (-0.160, 0.520) — no improvement shown, not preserved within 10 % relative |
| Mean cyclomatic complexity | down | 2.910 | 2.667 | 2.870 | 2.487 | 2.635 | -0.243 (-0.280, -0.217) — better | -0.040 (-0.390, 0.183) — no improvement shown | -0.423 (-0.450, -0.403) — better | -0.335 (-0.460, -0.335) — better | 0.095 (-0.070, 0.095) — no improvement shown | 0.135 (0.070, 0.135) — worse | -0.180 (-0.250, -0.143) — better | 0.203 (-0.190, 0.443) — no improvement shown |
| Lowest maintainability index | neutral | 28.877 | 19.870 | 23.620 | 38.100 | 13.790 | -9.007 (-16.850, -4.413) — reported without a verdict | -5.257 (-18.840, 4.303) — reported without a verdict | 9.223 (-4.350, 18.277) — reported without a verdict | -15.610 (-25.890, -15.610) — reported without a verdict | 5.650 (-11.520, 5.650) — reported without a verdict | 17.145 (15.170, 17.145) — reported without a verdict | 18.230 (-1.280, 31.877) — reported without a verdict | 3.750 (-11.740, 16.560) — reported without a verdict |
| Unused names | down | 30.667 | 29 | 29 | 30 | 18.500 | -1.667 (-4, 0) — no improvement shown | -1.667 (-8, 1.667) — no improvement shown | -0.667 (-6, 3) — no improvement shown | -12 (-13, -12) — better | 9 (9, 9) ‡ — worse | 9 (5, 9) — worse | 1 (-7, 6.333) — no improvement shown | 0 (-4, 2.667) — no improvement shown |
| Unused names per KLOC | down | 19.977 | 10.867 | 12.133 | 11.530 | 5.690 | -9.110 (-12.040, -6.447) — better | -7.843 (-11.650, -5.470) — better | -8.447 (-11.240, -6.680) — better | -13.125 (-13.460, -13.125) — better | 5.480 (2.220, 5.480) — worse | 7.185 (6.110, 7.185) — worse | 0.663 (-1.890, 2.320) — no improvement shown, not preserved within 10 % relative | 1.267 (-0.480, 2.723) — no improvement shown, not preserved within 10 % relative |
| Extension axes present, of three | up | 0 | 0 | 0 | 0.667 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.667 (0, 1) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.667 (0, 1) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Domain modules reaching Flask or the database | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Routes doing pricing arithmetic | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Boolean parameters | down | 0.333 | 0 | 0 | 0.333 | 0 | -0.333 (-1, 0) — no improvement shown | -0.333 (-1, 0) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Conditional ladders over rule kinds | down | 1.333 | 1 | 1.333 | 0.667 | 2 | -0.333 (-1, 0) — no improvement shown | 0 (-2, 1.333) — no improvement shown | -0.667 (-2, 0) — no improvement shown | 1 (0, 1) — no improvement shown | -1 (-2, -1) — better | 0 (0, 0) ‡ — no improvement shown | -0.333 (-2, 0.667) — no improvement shown | 0.333 (-1, 1.333) — no improvement shown |
| Public names beyond the specification | down | 3.667 | 7.667 | 5.667 | 9 | 10 | 4 (-1, 7.667) — no improvement shown | 2 (0, 3.333) — no improvement shown | 5.333 (1, 7.667) — worse | 6 (5, 6) — worse | -1.500 (-6, -1.500) — better | -3 (-3, -3) ‡ — better | 1.333 (-3, 4) — no improvement shown | -2 (-6, 1) — no improvement shown |
| Specified names missing | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Mutually importing module pairs | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Mean instability of domain modules | neutral | 0.495 | 0.393 | 0.450 | 0.390 | 0.327 | -0.102 (-0.178, -0.062) — reported without a verdict | -0.045 (-0.068, -0.027) — reported without a verdict | -0.105 (-0.189, -0.058) — reported without a verdict | -0.194 (-0.233, -0.194) — reported without a verdict | 0.070 (0.055, 0.070) — reported without a verdict | 0.153 (0.141, 0.153) — reported without a verdict | -0.003 (-0.011, 0.004) — reported without a verdict | 0.057 (0.003, 0.092) — reported without a verdict |
| Stored payload renders inert | up | 1 | 1 | 1 | — | 1 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown |
| A post without a token is refused | up | 0 | 0.667 | 0 | — | 0.500 | 0.667 (0, 1) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0.500 (0, 0.500) — no improvement shown | 0 (-1, 0) — no improvement shown | -0.500 (-1, -0.500) — worse | no complete pair was measured | -0.667 (-1, -0.333) — worse |
| Accessibility violations | down | 10 | 10 | 10 | — | 10 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown |
| HTML validity errors | down | 0 | 0 | 0 | — | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown |
| Invoice builder response size, bytes | down | 241.667 | 241 | 241 | — | 241 | -0.667 (-2, 0) — no improvement shown | -0.667 (-2, 0) — no improvement shown | no complete pair was measured | -1 (-2, -1) — better | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown |
| Invoice builder subrequests | down | 0 | 0 | 0 | — | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown |
| Source lines | down | 1544 | 2843 | 2416.7 | 2623.7 | 2167.7 | 1299 (308, 1816) — worse | 872.667 (345, 1296.3) — worse | 1079.7 (671, 1421.7) — worse | 623.667 (-1390, 1631.7) — no improvement shown | 675.333 (-1319, 2155) — no improvement shown | 249 (-1289, 1680.7) — no improvement shown | -219.333 (-859, 188) — no improvement shown | -426.333 (-1514, 194.667) — no improvement shown |
| Files | down | 20.667 | 49 | 41 | 38 | 32 | 28.333 (5, 45) — worse | 20.333 (4, 33) — worse | 17.333 (-30, 46.667) — no improvement shown | 11.333 (-27, 35.667) — no improvement shown | 17 (-10, 37.667) — no improvement shown | 9 (-11, 26.667) — no improvement shown | -11 (-35, 1.667) — no improvement shown | -8 (-13, -4) — better |
| Artifacts nobody asked for | down | 0 | 0.333 | 0 | 0 | 0 | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -0.333 (-1, 0) — no improvement shown | -0.333 (-1, 0) — no improvement shown |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## Raw numbers, per trial

| Metric | none-1 | none-2 | none-3 | full-1 | full-2 | full-3 | short-1 | short-2 | short-3 | hybrid-1 | hybrid-2 | hybrid-3 | hand-1 | hand-2 | hand-3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 |
| Readability, 1-5 | 3 | 2 | 3 | 3 | 3.333 | 3.667 | 3 | 3 | 3 | 3 | 3.667 | 4 | 3.333 | 3.333 | 1 |
| Maintainability, 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 |
| Security, 1-5 | 2 | 1.333 | 1 | 1.667 | 2 | 2 | 2 | 2 | 2 | 4.333 | 3.667 | 2 | 3.333 | 3 | 1 |
| Data protection, 1-5 | 1 | 3 | 3 | 1 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 2 | 3 | 1 |
| Security probe pass rate, of eleven | 0.636 | 0.545 | 0.636 | 0.818 | 0.909 | 0.909 | 0.636 | 0.727 | 0.727 | 0.364 | — | 0.273 | 0.909 | 0.909 | — |
| Data-protection probe pass rate, of three | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 1 | 0.667 | 0.667 | 0.667 | 0 | 0 | 0 | 0.667 | 0.667 | 0 |
| Task success, hidden suite pass rate | 0.929 | 0.925 | 0.891 | 0.927 | 0.690 | 0.690 | 0.931 | 0.957 | 0.951 | 0.421 | 0.416 | 0.418 | 0.927 | 0.966 | 0 |
| Installs in a clean environment | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| Adherence checklist fraction | 0.417 | 0.545 | 0.583 | 0.583 | 0.692 | 0.692 | 0.500 | 0.583 | 0.667 | 0.583 | 0.583 | 0.583 | 0.583 | 0.583 | — |
| SRP, 1-5 | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 3.667 | 4 | 3.667 | 3.333 | 3 | 1 |
| OCP, 1-5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 |
| LSP, 1-5 | 3 | 2.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 2.667 | 3.333 | 3 | 3 | 1 |
| ISP, 1-5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 1 |
| DIP, 1-5 | 4 | 4 | 4 | 3.333 | 4 | 4 | 4.333 | 4 | 4 | 4 | 4.333 | 4.333 | 4 | 4 | 1 |
| Naming and abstraction, 1-5 | 3.667 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 1 |
| Error design, 1-5 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3.333 | 3.333 | 3.667 | 4 | 3 | 3.333 | 4 | 3 | 1 |
| Test quality, 1-5 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 3.667 | 4 | 4 | 4 | 4 | 3.667 | 4 | 1 |
| Patterns warranted | 4 | 2.667 | 2.667 | 3.667 | 3 | 3 | 2.667 | 3.333 | 3.333 | 4 | 5 | 5 | 3.333 | 3 | 0 |
| Patterns over-engineered | 0 | 0.333 | 0 | 0 | 0 | 0.667 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| Patterns missed | 2 | 2.667 | 2.333 | 2.333 | 2.667 | 2 | 3 | 2.333 | 3 | 3 | 1.667 | 2 | 2.333 | 2 | 0 |
| Line coverage of the trial's own tests, % | 85.143 | 88.539 | 89.770 | 89.773 | 97.480 | 89.880 | 61.961 | 91.611 | 96.022 | 89.689 | 87.471 | 91.621 | 98.607 | 98.095 | — |
| Docstring coverage, % | 17.910 | 15.270 | 2.590 | 31.540 | 40.960 | 46.850 | 80.450 | 42.030 | 46.150 | 75.140 | 83.420 | 49.420 | 14.740 | 11.360 | — |
| Lint findings per KLOC | 302.240 | 312.120 | 340.290 | 134.130 | 101.350 | 107.370 | 72.850 | 126.830 | 87.820 | 84.690 | 62.140 | 114.110 | 150.850 | 141.980 | — |
| Lint findings | 486 | 510 | 473 | 257 | 354 | 335 | 165 | 251 | 264 | 193 | 207 | 258 | 488 | 464 | — |
| Files the formatter would change | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Files the formatter would change, per KLOC | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Type errors under --strict | 200 | 178 | 217 | 48 | 29 | 36 | 2 | 40 | 15 | 59 | 6 | 8 | 105 | 4 | — |
| Type errors under --strict, per KLOC | 124.380 | 108.940 | 156.120 | 25.050 | 8.300 | 11.540 | 0.880 | 20.210 | 4.990 | 25.890 | 1.800 | 3.540 | 32.460 | 1.220 | — |
| Security findings, high and medium | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | — |
| Security findings, high and medium, per KLOC | 0.620 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.300 | 0 | 0 | 0 | — |
| Highest cognitive complexity | 98 | 56 | 15 | 29 | 18 | 13 | 18 | 35 | 19 | 31 | 29 | 14 | 18 | 19 | — |
| Functions over complexity 15 | 2 | 1 | 0 | 2 | 1 | 0 | 2 | 1 | 2 | 1 | 3 | 0 | 1 | 2 | — |
| Functions over complexity 15, per KLOC | 1.240 | 0.610 | 0 | 1.040 | 0.290 | 0 | 0.880 | 0.510 | 0.670 | 0.440 | 0.900 | 0 | 0.310 | 0.610 | — |
| Mean cyclomatic complexity | 2.850 | 3.090 | 2.790 | 2.570 | 2.890 | 2.540 | 2.840 | 2.700 | 3.070 | 2.420 | 2.640 | 2.400 | 2.640 | 2.630 | — |
| Lowest maintainability index | 31.180 | 27.620 | 27.830 | 28.110 | 10.770 | 20.730 | 24.410 | 37.460 | 8.990 | 26.830 | 50.430 | 37.040 | 5.290 | 22.290 | — |
| Unused names | 30 | 31 | 31 | 28 | 27 | 32 | 32 | 23 | 32 | 29 | 36 | 25 | 19 | 18 | — |
| Unused names per KLOC | 18.660 | 18.970 | 22.300 | 14.610 | 7.730 | 10.260 | 14.130 | 11.620 | 10.650 | 12.720 | 10.810 | 11.060 | 5.870 | 5.510 | — |
| Extension axes present, of three | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | — |
| Domain modules reaching Flask or the database | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Routes doing pricing arithmetic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Boolean parameters | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | — |
| Conditional ladders over rule kinds | 2 | 0 | 2 | 2 | 0 | 1 | 2 | 2 | 0 | 0 | 0 | 2 | 2 | 2 | — |
| Public names beyond the specification | 5 | 3 | 3 | 4 | 13 | 6 | 7 | 7 | 3 | 6 | 10 | 11 | 10 | 10 | — |
| Specified names missing | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Mutually importing module pairs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| Mean instability of domain modules | 0.509 | 0.533 | 0.443 | 0.438 | 0.355 | 0.386 | 0.495 | 0.465 | 0.389 | 0.428 | 0.344 | 0.397 | 0.354 | 0.300 | — |
| Stored payload renders inert | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | — | — | — | 1 | 1 | — |
| A post without a token is refused | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | — | — | — | 1 | 0 | — |
| Accessibility violations | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | — | — | — | 10 | 10 | — |
| HTML validity errors | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | — |
| Invoice builder response size, bytes | 241 | 243 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | — | — | — | 241 | 241 | — |
| Invoice builder subrequests | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | — |
| Output tokens | 105373 | 75109 | 80816 | 92107 | 118984 | 128495 | 108267 | 120993 | 109072 | 114729 | 163313 | 124455 | 46 | 132406 | — |
| Turns | 92 | 65 | 60 | 103 | 118 | 133 | 108 | 124 | 89 | 105 | 151 | 115 | 1 | 144 | — |
| Wall time, seconds | 2040.2 | 1089.8 | 1002.8 | 1687.8 | 1722.6 | 6752.3 | 1611.5 | 1460.8 | 1125.1 | 2009.1 | 1886.5 | 3285.7 | 2595.2 | 1622.7 | — |
| Cost, USD | 3.984 | 2.337 | 2.409 | 4.099 | 5.070 | 6.502 | 4.515 | 5.432 | 3.759 | 4.681 | 7.611 | 5.100 | 8.133 | 6.366 | — |
| Source lines | 1608 | 1634 | 1390 | 1916 | 3493 | 3120 | 2265 | 1979 | 3006 | 2279 | 3331 | 2261 | 3235 | 3268 | 0 |
| Files | 32 | 1 | 29 | 37 | 56 | 54 | 36 | 43 | 44 | 2 | 59 | 53 | 47 | 47 | 2 |
| Artifacts nobody asked for | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Change task, acceptance pass rate | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, build suite pass rate after it | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, files touched | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, lines changed | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, cost, USD | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |

## Trials, and what was measured on them

| Trial | Outcome | Metrics flagged as not measured |
|---|---|---|
| none-1 | completed | none |
| none-2 | completed | none |
| none-3 | completed | none |
| full-1 | completed | none |
| full-2 | completed | hidden_suite |
| full-3 | completed | hidden_suite |
| short-1 | completed | none |
| short-2 | completed | none |
| short-3 | completed | none |
| hybrid-1 | completed | web |
| hybrid-2 | completed | web |
| hybrid-3 | completed | web |
| hand-1 | completed | none |
| hand-2 | completed | none |
| hand-3 | no cost record | adherence, bandit, complexity, cost, coverage, docstrings, hidden_suite, mypy, radon, ruff, ruff_format, structure, unused, web |

## Trials lost to the provider or the harness

Each was voided and re-run once in its own place, as the design's failure handling
fixes. A voided workspace is kept and never scored.

| Trial | Started | Why | Kept at | Re-run |
|---|---|---|---|---|
| hand-1 | 2026-10-16T15:27:07 | a tool call reached past the workspace: a process stopped by name | `C:/efficacy/r4-thin\void\hand-1-2026-10-16T16-09-17` | completed |
| none-3 | 2026-10-16T19:04:05 | a tool call reached past the workspace: c:/efficacy/r4-thin/scratch-test | `C:/efficacy/r4-thin\void\none-3-2026-10-16T19-22-41` | completed |

## Trials that reached past their own workspace

The shell keeps its network, and a trial's deny rules fence only the file tools, so a
trial could still fetch this repository or read the hidden suite, the scoring area, or
another trial's workspace, tarball or transcript through the shell. Every transcript is
scanned for a tool call naming any of them. The harness voids a trial whose scan finds
one and re-runs it; a trial this re-scan flags is left out of every figure above.

None: no scanned transcript names any of them.

## The judge, and how it is checked

| Trial | Blind id | Evidence lines found in the tree |
|---|---|---|
| none-1 | T123 | 100% |
| none-2 | T107 | 100% |
| none-3 | T110 | 100% |
| full-1 | T119 | 100% |
| full-2 | T106 | 100% |
| full-3 | T131 | 100% |
| short-1 | T108 | 100% |
| short-2 | T113 | 100% |
| short-3 | T100 | 100% |
| hybrid-1 | T104 | 100% |
| hybrid-2 | T136 | 100% |
| hybrid-3 | T101 | 100% |
| hand-1 | T103 | 100% |
| hand-2 | T112 | 100% |
| hand-3 | T111 | 100% |

No person scores the judge. Each score it gives quotes an evidence line, and the share
of those lines found in the tree they were quoted from is one check on it; the other
vendor's judge, below, is the second.

## The other vendor's judge

Not run: no other vendor's judging was read for this round, so the judge shares a vendor
with the generator unchecked.

## Verdict vector

The whole vector, which the summary's scores digest and never replace.

| Metric | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Readability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse |
| Maintainability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security, 1-5 | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Data protection, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security probe pass rate, of eleven | better | no improvement shown | worse | better | worse | worse | worse | worse |
| Data-protection probe pass rate, of three | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Task success, hidden suite pass rate | worse | better | worse | no improvement shown | no improvement shown | no improvement shown | worse | better |
| Installs in a clean environment | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Adherence checklist fraction | better | better | no improvement shown | better | no improvement shown | worse | worse | worse |
| SRP, 1-5 | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| OCP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| LSP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| ISP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| DIP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown |
| Naming and abstraction, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Error design, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| Test quality, 1-5 | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns warranted | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown |
| Patterns over-engineered | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns missed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown |
| Line coverage of the trial's own tests, % | better | no improvement shown | no improvement shown | better | worse | worse | no improvement shown | no improvement shown |
| Docstring coverage, % | better | better | better | worse | better | better | better | no improvement shown |
| Lint findings per KLOC | better | better | better | better | better | better | better | no improvement shown |
| Lint findings | better | better | better | better | better | better | better | better |
| Files the formatter would change | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Files the formatter would change, per KLOC | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Type errors under --strict | better | better | better | better | better | better | better | no improvement shown |
| Type errors under --strict, per KLOC | better | better | better | better | better | better | better | no improvement shown |
| Security findings, high and medium | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security findings, high and medium, per KLOC | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Highest cognitive complexity | better | better | better | better | no improvement shown | no improvement shown | worse | no improvement shown |
| Functions over complexity 15 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Functions over complexity 15, per KLOC | better | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Mean cyclomatic complexity | better | no improvement shown | better | better | no improvement shown | worse | better | no improvement shown |
| Lowest maintainability index | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Unused names | no improvement shown | no improvement shown | no improvement shown | better | worse | worse | no improvement shown | no improvement shown |
| Unused names per KLOC | better | better | better | better | worse | worse | no improvement shown | no improvement shown |
| Extension axes present, of three | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Domain modules reaching Flask or the database | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Routes doing pricing arithmetic | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Boolean parameters | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Conditional ladders over rule kinds | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown |
| Public names beyond the specification | no improvement shown | no improvement shown | worse | worse | better | better | no improvement shown | no improvement shown |
| Specified names missing | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Mutually importing module pairs | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Mean instability of domain modules | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Stored payload renders inert | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | not computed | no improvement shown |
| A post without a token is refused | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | worse | not computed | worse |
| Accessibility violations | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | not computed | no improvement shown |
| HTML validity errors | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | not computed | no improvement shown |
| Invoice builder response size, bytes | no improvement shown | no improvement shown | not computed | better | no improvement shown | no improvement shown | not computed | no improvement shown |
| Invoice builder subrequests | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | not computed | no improvement shown |
| Output tokens | no improvement shown | worse | worse | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Turns | worse | worse | worse | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Wall time, seconds | no improvement shown | no improvement shown | no improvement shown | worse | better | better | no improvement shown | better |
| Cost, USD | worse | worse | worse | worse | better | better | no improvement shown | no improvement shown |
| Source lines | worse | worse | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Files | worse | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| Artifacts nobody asked for | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Change task, acceptance pass rate | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, build suite pass rate after it | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, files touched | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, lines changed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, cost, USD | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
