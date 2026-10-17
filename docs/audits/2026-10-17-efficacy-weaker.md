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
| Improves the code? | **Worse** | **Worse** | **Worse** | **Yes** |
| Readability, design, maintainability | security +1.2, security probes -13.6 pp | did not move | data protection +1 | security probes +18.2 pp |
| Hidden tests passed, against 33 % without a file | 0 %, three run of three at 0 % | 24 %, two run of three at 0 % | 21 %, one run of two at 0 % | 47 % |
| Code size | lines +156 %, files +142 % | lines +99 %, files +119 % | files +188 % | lines +77 % |
| Cost | -10 % | -15 % | no change shown | +17 % |
| Reads as | bulk, worse quality | bulk, worse quality | bulk, worse quality | quality, with bulk |

**Templates' inline file, Worse.** Three run of three left the app unable to boot (`no
error recorded`). It built more than the task asked for: more files and more code. The
judge read its code as more secure and better tested.

**Templates' short inline file, Worse.** One run of three declared its dependencies so
that a clean install left the app unable to boot. It built more than the task asked for:
more files and more code. The judge saw none of it as better design, readability,
maintainability, security or data protection; every win is something a tool counts.

**Templates' hybrid file, Worse.** Two run of three left the app unable to boot
(`AttributeError("module 'tariff' has no attribute 'create_app'")`). It built more than
the task asked for: more files. The judge read its code as more careful with personal
data.

**Hand-written file, Yes.** It built more than the task asked for: more code, and took
more turns, tokens and cost to do it; the follow-up change had to move through that
structure too. The judge saw none of it as better design, readability, maintainability,
security or data protection; every win is something a tool counts.

Together, reading the longest file beside the shortest (templates' hybrid file,
templates' short inline file): neither file added quality. K = 3, one project: a signal,
not proof.

Between the files, 1 to 10: full − hand 4.5 (7 won, 11 failed); short − hand 4.0 (6 won,
12 failed); hybrid − full 7.2 (11 won, 5 failed); short − full 5.8 (7 won, 6 failed). A
win or a fail is a metric whose interval separated the pair in its declared direction,
each counting once; the score is 1 + 9 × wins ÷ (wins + fails), digests the verdict
vector at the end, and decides nothing.

Caveats: 15 trials, 15 judged; escalation to K = 5 owed and not yet run; withdrawn:
nothing; lost and re-run: hand-1 (change task), completed; full-2 (change task),
completed; hybrid-2 (change task), completed; reached past their workspace: none; the
judge is checked only by its evidence lines.

## What produced these numbers

| | |
|---|---|
| Trials | 15, arms none, full, short, hybrid, hand, K = 3 |
| Generator | `claude-haiku-4-5-20251001` |
| Judge | `claude-opus-5-5` at effort `high`, claude |
| Blinding | condition markers stripped, order shuffled at seed 20260912 |
| Judgings per trial | 3, meaned |
| Templates revision | `3c6af54` |
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
| Design (SOLID and patterns), 1-5 | up | 2.222 | 3 | 2.889 | 3 | 2.778 | 0.778 (0, 1.444) — no improvement shown, preserved within 0.3 points | 0.667 (0, 1.222) — no improvement shown, preserved within 0.3 points | 0.778 (0, 1.444) — no improvement shown, preserved within 0.3 points | 0.556 (-0.333, 1.333) — no improvement shown, not preserved within 0.3 points | 0.222 (0, 0.444) — no improvement shown, preserved within 0.3 points | 0.111 (-0.333, 0.444) — no improvement shown, not preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | -0.111 (-0.333, 0) — no improvement shown, not preserved within 0.3 points |
| Readability, 1-5 | up | 1.667 | 2 | 2.222 | 2 | 2 | 0.333 (0, 0.667) — no improvement shown, preserved within 0.3 points | 0.556 (0, 0.889) — no improvement shown, preserved within 0.3 points | 0.333 (0, 0.667) — no improvement shown, preserved within 0.3 points | 0.333 (-0.333, 0.778) — no improvement shown, not preserved within 0.3 points | 0 (-0.333, 0.222) — no improvement shown, not preserved within 0.3 points | 0.222 (-0.333, 0.667) — no improvement shown, not preserved within 0.3 points | 0 (0, 0) ‡ — no improvement shown, preserved within 0.3 points | 0.222 (0, 0.444) — no improvement shown, preserved within 0.3 points |
| Maintainability, 1-5 | up | 2.111 | 2.778 | 2.778 | 3 | 2.889 | 0.667 (-0.333, 1.444) — no improvement shown, not preserved within 0.3 points | 0.667 (-0.333, 1.333) — no improvement shown, not preserved within 0.3 points | 0.889 (0, 1.556) — no improvement shown, preserved within 0.3 points | 0.778 (0, 1.444) — no improvement shown, preserved within 0.3 points | -0.111 (-0.333, 0) — no improvement shown, not preserved within 0.3 points | -0.111 (-0.333, 0.111) — no improvement shown, not preserved within 0.3 points | 0.222 (0, 0.333) — no improvement shown, preserved within 0.3 points | 0 (-0.333, 0.222) — no improvement shown, not preserved within 0.3 points |
| Security, 1-5 | up | 1.111 | 2.333 | 1.111 | 2 | 1 | 1.222 (0.667, 1.667) — better | 0 (-0.333, 0.222) — no improvement shown, not preserved within 0.3 points | 0.889 (0, 1.444) — no improvement shown, preserved within 0.3 points | -0.111 (-0.333, 0) — no improvement shown, not preserved within 0.3 points | 1.333 (1, 1.667) — better | 0.111 (0, 0.222) — no improvement shown, preserved within 0.3 points | -0.333 (-0.667, -0.111) — worse | -1.222 (-2, -0.778) — worse |
| Data protection, 1-5 | up | 1.333 | 1.667 | 1.778 | 2.333 | 1.556 | 0.333 (0, 0.667) — no improvement shown, preserved within 0.3 points | 0.444 (-1, 1.222) — no improvement shown, not preserved within 0.3 points | 1 (0.667, 1.333) — better | 0.222 (-0.667, 0.667) — no improvement shown, not preserved within 0.3 points | 0.111 (-0.667, 0.556) — no improvement shown, not preserved within 0.3 points | 0.222 (-0.333, 0.556) — no improvement shown, not preserved within 0.3 points | 0.667 (-0.333, 1.333) — no improvement shown, not preserved within 0.3 points | 0.111 (-1, 0.778) — no improvement shown, not preserved within 0.3 points |
| Security probe pass rate, of eleven | up | 0.409 | 0.273 | 0.333 | 0.545 | 0.606 | -0.136 (-0.273, -0.136) — worse | 0 (0, 0) ‡ — no improvement shown, preserved within 2 pp | not computed: fewer than two paired differences | 0.182 (0.091, 0.182) — better | -0.333 (-0.364, -0.303) — worse | -0.273 (-0.455, -0.152) — worse | 0.273 (0.091, 0.273) — better | 0.061 (-0.091, 0.182) — no improvement shown, not preserved within 2 pp |
| Data-protection probe pass rate, of three | up | 0.111 | 0 | 0.111 | 0.222 | 0.333 | -0.111 (-0.333, 0) — no improvement shown, not preserved within 10 pp | 0 (0, 0) ‡ — no improvement shown, preserved within 10 pp | 0.111 (0, 0.222) — no improvement shown, preserved within 10 pp | 0.222 (0, 0.333) — no improvement shown, preserved within 10 pp | -0.333 (-0.333, -0.333) ‡ — worse | -0.222 (-0.333, -0.111) — worse | 0.222 (0, 0.444) — no improvement shown, preserved within 10 pp | 0.111 (0, 0.222) — no improvement shown, preserved within 10 pp |

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
| Design (SOLID and patterns), 1-5 | full−none | 0.778 | (0, 1.444) | 0.5 points |
| Design (SOLID and patterns), 1-5 | short−none | 0.667 | (0, 1.222) | 0.5 points |
| Design (SOLID and patterns), 1-5 | hybrid−none | 0.778 | (0, 1.444) | 0.5 points |
| Design (SOLID and patterns), 1-5 | hand−none | 0.556 | (-0.333, 1.333) | 0.5 points |
| Readability, 1-5 | short−none | 0.556 | (0, 0.889) | 0.5 points |
| Maintainability, 1-5 | full−none | 0.667 | (-0.333, 1.444) | 0.5 points |
| Maintainability, 1-5 | short−none | 0.667 | (-0.333, 1.333) | 0.5 points |
| Maintainability, 1-5 | hybrid−none | 0.889 | (0, 1.556) | 0.5 points |
| Maintainability, 1-5 | hand−none | 0.778 | (0, 1.444) | 0.5 points |
| Security, 1-5 | hybrid−none | 0.889 | (0, 1.444) | 0.5 points |
| Data protection, 1-5 | hybrid−full | 0.667 | (-0.333, 1.333) | 0.5 points |

## Task success, adherence and cost

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 0.331 | 0.002 | 0.236 | 0.212 | 0.474 | -0.330 (-0.507, -0.159) — worse | -0.095 (-0.269, -0.006) — worse | -0.042 (-0.503, -0.042) — worse | 0.143 (-0.036, 0.313) — no improvement shown, not preserved within 2 pp | -0.472 (-0.477, -0.470) — worse | -0.238 (-0.475, -0.081) — worse | 0.209 (0.004, 0.209) — better | 0.234 (-0.006, 0.393) — no improvement shown, preserved within 2 pp |
| Installs in a clean environment | up | 1 | 0.333 | 0.667 | 1 | 1 | -0.667 (-1, -0.333) — worse | -0.333 (-1, 0) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -0.667 (-1, -0.333) — worse | -0.333 (-1, 0) — no improvement shown | 0.667 (0, 1) — no improvement shown | 0.333 (-1, 1) — no improvement shown |
| Adherence checklist fraction | up | 0.682 | 0.604 | 0.534 | 0.564 | 0.646 | -0.078 (-0.300, 0.063) — no improvement shown, not preserved within 5 pp | -0.148 (-0.444, 0.015) — no improvement shown, not preserved within 5 pp | -0.118 (-0.364, 0.022) — no improvement shown, not preserved within 5 pp | -0.035 (-0.364, 0.142) — no improvement shown, not preserved within 5 pp | -0.043 (-0.223, 0.053) — no improvement shown, not preserved within 5 pp | -0.113 (-0.136, -0.094) — worse | -0.040 (-0.167, 0.053) — no improvement shown, not preserved within 5 pp | -0.070 (-0.167, 0.019) — no improvement shown, not preserved within 5 pp |
| Output tokens | down | 60001.5 | 58659.7 | 58687.3 | 36349.7 | 64548.7 | -3242 (-5416, -3242) — better | -2290 (-9621, -2290) — better | -34908.5 (-56295, -34908.5) — better | 7365.5 (1157, 7365.5) — worse | -5889 (-14642, 174.333) — no improvement shown | -5861.3 (-23195, 3165) — no improvement shown | -22310 (-55227, -5100) — better | 27.667 (-8553, 6364.3) — no improvement shown |
| Turns | down | 108 | 84.333 | 86.667 | 59.333 | 113.667 | -27.500 (-34, -27.500) — better | -22 (-24, -22) — better | -64 (-97, -64) — better | 11 (7, 11) — worse | -29.333 (-49, -16.667) — better | -27 (-35, -20.333) — better | -25 (-63, -4.667) — better | 2.333 (-4, 8.333) — no improvement shown |
| Wall time, seconds | down | 756.050 | 615.867 | 608.500 | 722.067 | 698.267 | -186.850 (-194.200, -186.850) — better | -83 (-105.800, -83.000) — better | -69.450 (-95.800, -69.450) — better | -73.750 (-226.400, -73.750) — better | -82.400 (-258.400, 14.467) — no improvement shown | -89.767 (-250.800, 34.033) — no improvement shown | 106.200 (83.700, 128.667) — worse | -7.367 (-229.800, 109.000) — no improvement shown |
| Cost, USD | down | 1.427 | 1.289 | 1.197 | 1.479 | 1.575 | -0.146 (-0.341, -0.146) — better | -0.210 (-0.333, -0.210) — better | 0.133 (-0.409, 0.132) — no improvement shown | 0.243 (0.084, 0.243) — worse | -0.286 (-0.743, -0.050) — better | -0.378 (-0.735, -0.190) — better | 0.190 (-0.459, 0.681) — no improvement shown | -0.092 (-0.147, -0.040) — better |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## The change task

How far each design had to be disturbed to take a change it was not built for, read
beside whether the change works and whether the build still passes after it.

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Change task, acceptance pass rate | up | 0.685 | 0 | 0.716 | 0.464 | 0.640 | -0.685 (-0.757, -0.635) — worse | 0.032 (-0.041, 0.081) — no improvement shown | -0.221 (-0.757, 0.054) — no improvement shown | -0.045 (-0.243, 0.072) — no improvement shown | -0.640 (-0.716, -0.572) — worse | 0.077 (0, 0.144) — no improvement shown | 0.464 (0, 0.703) — no improvement shown | 0.716 (0.716, 0.716) ‡ — better |
| Change task, build suite pass rate after it | up | 0.490 | 0.002 | 0.376 | 0.212 | 0.475 | -0.488 (-0.507, -0.477) — worse | -0.114 (-0.269, -0.030) — worse | -0.280 (-0.503, -0.280) — worse | -0.016 (-0.036, -0.004) — worse | -0.473 (-0.477, -0.471) — worse | -0.099 (-0.233, -0.023) — worse | 0.209 (0.004, 0.209) — better | 0.374 (0.238, 0.452) — better |
| Change task, files touched | down | 15.333 | 11.667 | 11.333 | 11.333 | 7.333 | -3.667 (-15, 2.333) — no improvement shown, not preserved within 15 % relative | -4 (-14, 1.667) — no improvement shown, preserved within 15 % relative | -4 (-15, 2) — no improvement shown, preserved within 15 % relative | -8 (-17, -3.333) — better | 4.333 (2, 5.667) — worse | 4 (3, 5) — worse | -0.333 (-3, 1.333) — no improvement shown, preserved within 15 % relative | -0.333 (-2, 0.667) — no improvement shown, preserved within 15 % relative |
| Change task, lines changed | down | 1400 | 327 | 561 | 418.333 | 298.333 | -1073 (-3029, -77) — better | -839 (-2812, 254.667) — no improvement shown, not preserved within 15 % relative | -981.667 (-2868, 22) — no improvement shown, preserved within 15 % relative | -1101.7 (-2709, -256) — better | 28.667 (-320, 227) — no improvement shown, not preserved within 15 % relative | 262.667 (-103, 594.667) — no improvement shown, not preserved within 15 % relative | 91.333 (-179, 248.333) — no improvement shown, not preserved within 15 % relative | 234 (-133, 484.333) — no improvement shown, not preserved within 15 % relative |
| Change task, cost, USD | down | 0.777 | 0.797 | 0.755 | 0.820 | 1.010 | 0.021 (-0.347, 0.238) — no improvement shown | -0.021 (-0.250, 0.142) — no improvement shown | 0.044 (-0.065, 0.144) — no improvement shown | 0.233 (0.176, 0.278) — worse | -0.213 (-0.656, 0.049) — no improvement shown | -0.255 (-0.559, -0.047) — better | 0.023 (-0.143, 0.165) — no improvement shown | -0.042 (-0.159, 0.044) — no improvement shown |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## Every other metric

| Metric | Direction | none | full | short | hybrid | hand | full−none | short−none | hybrid−none | hand−none | full−hand | short−hand | hybrid−full | short−full |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SRP, 1-5 | up | 1.667 | 2 | 2 | 2 | 2 | 0.333 (0, 0.667) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| OCP, 1-5 | up | 1.667 | 2 | 1.889 | 2 | 1.889 | 0.333 (0, 0.667) — no improvement shown | 0.222 (0, 0.444) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.222 (-0.333, 0.667) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0 (-0.333, 0.222) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -0.111 (-0.333, 0) — no improvement shown |
| LSP, 1-5 | up | 2.222 | 2.556 | 2.556 | 2.667 | 2.444 | 0.333 (-0.667, 1.111) — no improvement shown | 0.333 (-0.333, 1.667) — no improvement shown | 0.444 (-0.667, 1.333) — no improvement shown | 0.222 (-0.667, 1) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.111 (-0.667, 0.556) — no improvement shown | 0 (-0.333, 0.222) — no improvement shown |
| ISP, 1-5 | up | 3 | 3.111 | 3.667 | 3.333 | 3.889 | 0.111 (-1.333, 1.222) — no improvement shown | 0.667 (-0.667, 1.778) — no improvement shown | 0.333 (-1, 1.333) — no improvement shown | 0.889 (-0.333, 2) — no improvement shown | -0.778 (-1, -0.556) — worse | -0.222 (-0.333, -0.111) — worse | 0.222 (0, 0.333) — no improvement shown | 0.556 (0.333, 0.667) — better |
| DIP, 1-5 | up | 2.778 | 3.333 | 3.667 | 3.333 | 3.667 | 0.556 (-0.333, 1.444) — no improvement shown | 0.889 (0, 1.667) — no improvement shown | 0.556 (-0.333, 1.444) — no improvement shown | 0.889 (-0.667, 2.111) — no improvement shown | -0.333 (-0.667, 0.000) — no improvement shown | 0 (-0.667, 0.444) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.333 (0, 0.556) — no improvement shown |
| Naming and abstraction, 1-5 | up | 2.333 | 3 | 3 | 3 | 3 | 0.667 (0, 1.333) — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0.667 (0, 1.333) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Error design, 1-5 | up | 1.889 | 2.111 | 2.333 | 2.556 | 2.222 | 0.222 (-0.333, 0.667) — no improvement shown | 0.444 (-0.667, 1.111) — no improvement shown | 0.667 (-0.667, 1.444) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | -0.111 (-0.333, 0) — no improvement shown | 0.111 (-0.667, 0.556) — no improvement shown | 0.444 (-0.333, 0.889) — no improvement shown | 0.222 (-0.333, 0.556) — no improvement shown |
| Test quality, 1-5 | up | 1.556 | 2.333 | 2 | 2 | 2.222 | 0.778 (0.333, 1.222) — better | 0.444 (-0.667, 1.111) — no improvement shown | 0.444 (0, 0.778) — no improvement shown | 0.667 (-0.667, 1.444) — no improvement shown | 0.111 (-0.667, 0.667) — no improvement shown | -0.222 (-1.667, 0.778) — no improvement shown | -0.333 (-0.667, -0.111) — worse | -0.333 (-1, 0.111) — no improvement shown |
| Patterns warranted | up | 1.556 | 2 | 2.556 | 3.222 | 2.111 | 0.444 (-1, 1.444) — no improvement shown | 1 (-0.333, 1.667) — no improvement shown | 1.667 (-0.333, 2.778) — no improvement shown | 0.556 (-1, 1.889) — no improvement shown | -0.111 (-1, 0.444) — no improvement shown | 0.444 (-1.333, 1.556) — no improvement shown | 1.222 (0.667, 1.667) — better | 0.556 (-0.333, 1.111) — no improvement shown |
| Patterns over-engineered | down | 0 | 0.444 | 0.111 | 0.111 | 0.333 | 0.444 (0, 0.667) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.111 (0, 0.222) — no improvement shown | 0.333 (0, 0.667) — no improvement shown | 0.111 (-1, 0.667) — no improvement shown | -0.222 (-1, 0.222) — no improvement shown | -0.333 (-0.667, 0) — no improvement shown | -0.333 (-0.667, -0.111) — better |
| Patterns missed | down | 2.222 | 2.889 | 3.222 | 2.778 | 3 | 0.667 (-0.333, 1.556) — no improvement shown | 1 (-0.333, 2.222) — no improvement shown | 0.556 (-0.667, 1.778) — no improvement shown | 0.778 (-0.333, 1.778) — no improvement shown | -0.111 (-0.333, 0) — no improvement shown | 0.222 (-0.333, 0.556) — no improvement shown | -0.111 (-0.667, 0.333) — no improvement shown | 0.333 (-0.333, 0.778) — no improvement shown |
| Line coverage of the trial's own tests, % | up | 73.469 | — | 26.906 | 24.714 | 30.317 | no complete pair was measured | not computed: fewer than two paired differences | no complete pair was measured | not computed: fewer than two paired differences | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured |
| Docstring coverage, % | up | 29.115 | 95.073 | 49.010 | 91.610 | 11.390 | 70.580 (41.770, 70.580) — better | 44.400 (-10.020, 44.400) — no improvement shown | not computed: fewer than two paired differences | -20.705 (-58.230, -20.705) — worse | 83.683 (68.480, 94.190) — better | 37.620 (-17.350, 70.737) — no improvement shown | -1.305 (-4.280, -1.305) — worse | -46.063 (-85.830, -17.643) — worse |
| Lint findings per KLOC | down | 540.445 | 90.770 | 128.177 | 58.095 | 119.467 | -457.145 (-475.510, -457.145) — better | -424.225 (-457.760, -424.225) — better | not computed: fewer than two paired differences | -434.500 (-468.210, -434.500) — better | -28.697 (-40.800, -17.530) — better | 8.710 (5.580, 10.333) — worse | -34.670 (-53.950, -34.670) — better | 37.407 (17.750, 47.520) — worse |
| Lint findings | down | 859 | 244 | 269 | 229.500 | 224 | -612.500 (-659, -612.500) — better | -619 (-661, -619) — better | not computed: fewer than two paired differences | -660.500 (-681, -660.500) — better | 20 (-36, 56.667) — no improvement shown | 45 (20, 59.333) — worse | -6.500 (-43, -6.500) — better | 25 (-11, 58) — no improvement shown |
| Files the formatter would change | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Files the formatter would change, per KLOC | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Type errors under --strict | down | 191.500 | 121 | 98 | 160 | 37.667 | -43.500 (-93, -43.500) — better | -105.500 (-132, -105.500) — better | not computed: fewer than two paired differences | -171.500 (-177, -171.500) — better | 83.333 (-6, 142.667) — no improvement shown | 60.333 (45, 74.333) — worse | 27 (-12, 27) — no improvement shown | -23 (-85, 23.667) — no improvement shown |
| Type errors under --strict, per KLOC | down | 120.775 | 43.393 | 48.070 | 40.465 | 20.183 | -70.500 (-96.960, -70.500) — better | -77.040 (-104.990, -77.040) — better | not computed: fewer than two paired differences | -109.945 (-122.760, -109.945) — better | 23.210 (-9.260, 43.993) — no improvement shown, not preserved within 10 % relative | 27.887 (17.770, 37.977) — worse | -8.435 (-22.360, -8.435) — better | 4.677 (-8.030, 16.390) — no improvement shown, not preserved within 10 % relative |
| Security findings, high and medium | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Security findings, high and medium, per KLOC | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Highest cognitive complexity | down | 164.500 | 68 | 155.667 | 66 | 207.667 | -95 (-139, -95) — better | 17.500 (-10, 17.500) — no improvement shown | not computed: fewer than two paired differences | 47 (-2, 47) — no improvement shown | -139.667 (-235, -77.667) — better | -52 (-97, -22.333) — better | -3 (-3, -3) ‡ — better | 87.667 (38, 136.333) — worse |
| Functions over complexity 15 | down | 5.500 | 3.333 | 4.667 | 5 | 3.333 | -1 (-3, -1) — better | -1.500 (-7, -1.500) — better | not computed: fewer than two paired differences | -2.500 (-6, -2.500) — better | 0 (-3, 2) — no improvement shown | 1.333 (-1, 2.667) — no improvement shown | 1.500 (0, 1.500) — no improvement shown | 1.333 (-4, 4.333) — no improvement shown |
| Functions over complexity 15, per KLOC | down | 3.295 | 1.167 | 2.140 | 1.265 | 1.777 | -1.765 (-3.170, -1.765) — better | -1.480 (-4.120, -1.480) — better | not computed: fewer than two paired differences | -1.695 (-3.550, -1.695) — better | -0.610 (-1.690, 0.080) — no improvement shown, preserved within 10 % relative | 0.363 (-0.570, 0.887) — no improvement shown, not preserved within 10 % relative | 0.015 (-0.590, 0.015) — no improvement shown, preserved within 10 % relative | 0.973 (-0.950, 2.073) — no improvement shown, not preserved within 10 % relative |
| Mean cyclomatic complexity | down | 5.505 | 3.820 | 4.365 | 3.395 | 3.760 | not computed: fewer than two paired differences | -1.140 (-4.360, -1.140) — better | not computed: fewer than two paired differences | -1.665 (-3.120, -1.665) — better | 0.360 (0.150, 0.360) — worse | 0.525 (-1.240, 0.525) — no improvement shown | not computed: fewer than two paired differences | not computed: fewer than two paired differences |
| Lowest maintainability index | neutral | 23.195 | 28.240 | 31.810 | 36.720 | 14.337 | not computed: fewer than two paired differences | 8.615 (7.320, 8.615) — reported without a verdict | not computed: fewer than two paired differences | -14.040 (-14.180, -14.040) — reported without a verdict | 9.245 (3.590, 9.245) — reported without a verdict | 22.655 (21.500, 22.655) — reported without a verdict | not computed: fewer than two paired differences | not computed: fewer than two paired differences |
| Unused names | down | 23.500 | 24.667 | 14.667 | 42 | 23.667 | -4.500 (-28, -4.500) — better | -1.500 (-11, -1.500) — better | not computed: fewer than two paired differences | 3 (0, 3) — no improvement shown | 1 (-28, 16.333) — no improvement shown | -9 (-18, -2.333) — better | 24 (-5, 24) — no improvement shown | -10 (-36, 7.667) — no improvement shown |
| Unused names per KLOC | down | 14.605 | 9.533 | 6.917 | 10.585 | 12.623 | -8.265 (-16.280, -8.265) — better | -4.230 (-6.870, -4.230) — better | not computed: fewer than two paired differences | -0.465 (-0.650, -0.465) — better | -3.090 (-15.630, 4.230) — no improvement shown, not preserved within 10 % relative | -5.707 (-9.590, -2.947) — better | 2.625 (-7.730, 2.625) — no improvement shown, not preserved within 10 % relative | -2.617 (-15.920, 5.827) — no improvement shown, not preserved within 10 % relative |
| Extension axes present, of three | up | 0 | 1.333 | 0 | 1.500 | 0 | 1.500 (0, 1.500) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 1.333 (0, 2.333) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 1 (0, 1) — no improvement shown | -1.333 (-3, -0.333) — worse |
| Domain modules reaching Flask or the database | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Routes doing pricing arithmetic | down | 0 | 0 | 0.667 | 0 | 0.667 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 1 (0, 1) — no improvement shown | -0.667 (-2, 0) — no improvement shown | 0 (-2, 1.333) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0.667 (0, 1.333) — no improvement shown |
| Boolean parameters | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |
| Conditional ladders over rule kinds | down | 7 | 5 | 5.667 | 8 | 6.667 | -2.500 (-4, -2.500) — better | -2 (-5, -2) — better | not computed: fewer than two paired differences | -1 (-7, -1) — better | -1.667 (-6, 1.333) — no improvement shown | -1 (-4, 1) — no improvement shown | 3 (2, 3) — worse | 0.667 (-1, 1.667) — no improvement shown |
| Public names beyond the specification | down | 2 | 0.333 | 1.667 | 1 | 1 | -2 (-3, -2) — better | -0.500 (-1, -0.500) — better | not computed: fewer than two paired differences | -1.500 (-2, -1.500) — better | -0.667 (-1, -0.333) — better | 0.667 (0, 1) — no improvement shown | 0.500 (0, 0.500) — no improvement shown | 1.333 (1, 1.667) — worse |
| Specified names missing | down | 0 | 3.667 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | 3.667 (0, 7.333) — no improvement shown | 0 (0, 0) ‡ — no improvement shown | -5.500 (-11, -5.500) — better | -3.667 (-11, 0) — no improvement shown |
| Mutually importing module pairs | down | 0 | 0 | 0 | 0 | 0 | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | not computed: fewer than two paired differences |
| Mean instability of domain modules | neutral | 0.408 | 0.430 | 0.466 | 0.450 | 0.430 | no complete pair was measured | 0.078 (0.048, 0.078) — reported without a verdict | not computed: fewer than two paired differences | 0.008 (-0.134, 0.008) — reported without a verdict | not computed: fewer than two paired differences | 0.036 (-0.042, 0.111) — reported without a verdict | not computed: fewer than two paired differences | not computed: fewer than two paired differences |
| Stored payload renders inert | up | 1 | — | 1 | 1 | 1 | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | no complete pair was measured |
| A post without a token is refused | up | 0.500 | — | 0 | 0 | 0 | no complete pair was measured | -0.500 (-1, -0.500) — worse | not computed: fewer than two paired differences | -0.500 (-1, -0.500) — worse | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | no complete pair was measured |
| Accessibility violations | down | 10 | — | 10 | 10 | 10 | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | no complete pair was measured |
| HTML validity errors | down | 0 | — | 0 | 0 | 0 | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | no complete pair was measured |
| Invoice builder response size, bytes | down | 273 | — | 251.667 | 273 | 262.333 | no complete pair was measured | -32 (-32, -32) ‡ — better | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | -10.667 (-32, 10.667) — no improvement shown | no complete pair was measured | no complete pair was measured |
| Invoice builder subrequests | down | 0 | — | 0 | 0 | 0 | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | not computed: fewer than two paired differences | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | 0 (0, 0) ‡ — no improvement shown | no complete pair was measured | no complete pair was measured |
| Source lines | down | 1063 | 2725.3 | 2112.7 | 2623 | 1881.7 | 1662.3 (1199, 2016.3) — worse | 1049.7 (86, 1737.7) — worse | 1560 (-1469, 3312) — no improvement shown | 818.667 (71, 1420.7) — worse | 843.667 (384, 1091.7) — worse | 231 (15, 361) — worse | -102.333 (-2996, 1405) — no improvement shown | -612.667 (-1113, -278.667) — better |
| Files | down | 17.333 | 42 | 38 | 50 | 32.667 | 24.667 (16, 32) — worse | 20.667 (9, 30) — worse | 32.667 (12, 49.333) — worse | 15.333 (-2, 28) — no improvement shown | 9.333 (2, 16) — worse | 5.333 (-3, 12.333) — no improvement shown | 8 (-8, 18.667) — no improvement shown | -4 (-7, -2) — better |
| Artifacts nobody asked for | down | 0 | 0 | 0 | 0 | 0 | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown | 0 (0, 0) ‡ — no improvement shown |

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## Raw numbers, per trial

| Metric | none-1 | none-2 | none-3 | full-1 | full-2 | full-3 | short-1 | short-2 | short-3 | hybrid-1 | hybrid-2 | hybrid-3 | hand-1 | hand-2 | hand-3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | 2.667 | 3 | 1 | 3 | 3 | 3 | 3 | 3 | 2.667 | 3 | 3 | 3 | 2.333 | 3 | 3 |
| Readability, 1-5 | 2 | 2 | 1 | 2 | 2 | 2 | 2.667 | 2 | 2 | 2 | 2 | 2 | 1.667 | 2.333 | 2 |
| Maintainability, 1-5 | 2.333 | 3 | 1 | 2.667 | 2.667 | 3 | 3 | 2.667 | 2.667 | 3 | 3 | 3 | 2.667 | 3 | 3 |
| Security, 1-5 | 1 | 1.333 | 1 | 3 | 2 | 2 | 1 | 1 | 1.333 | 2.667 | 1.333 | 2 | 1 | 1 | 1 |
| Data protection, 1-5 | 1 | 2 | 1 | 2 | 2 | 1 | 2.333 | 1 | 2 | 1.667 | 2.667 | 2.667 | 1.667 | 1.333 | 1.667 |
| Security probe pass rate, of eleven | 0.545 | 0.273 | — | 0.273 | 0.273 | 0.273 | 0.545 | 0.273 | 0.182 | 0.727 | — | 0.364 | 0.636 | 0.545 | 0.636 |
| Data-protection probe pass rate, of three | 0.333 | 0 | 0 | 0 | 0 | 0 | 0.333 | 0 | 0 | 0.667 | 0 | 0 | 0.333 | 0.333 | 0.333 |
| Task success, hidden suite pass rate | 0.488 | 0.507 | 0 | 0 | 0 | 0.006 | 0.471 | 0.238 | 0 | — | 0.004 | 0.420 | 0.477 | 0.471 | 0.475 |
| Installs in a clean environment | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| Adherence checklist fraction | 0.500 | 0.545 | 1 | 0.444 | 0.667 | 0.700 | 0.545 | 0.500 | 0.556 | 0.556 | 0.500 | 0.636 | 0.667 | 0.636 | 0.636 |
| SRP, 1-5 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| OCP, 1-5 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 1.667 | 2 | 2 | 2 | 1.667 | 2 | 2 |
| LSP, 1-5 | 3 | 2.667 | 1 | 2.333 | 2.667 | 2.667 | 2.667 | 2.333 | 2.667 | 3 | 2 | 3 | 2.333 | 2.333 | 2.667 |
| ISP, 1-5 | 4 | 4 | 1 | 3.667 | 2.667 | 3 | 4 | 3.333 | 3.667 | 4 | 3 | 3 | 4 | 3.667 | 4 |
| DIP, 1-5 | 3.667 | 3.667 | 1 | 3.333 | 3.333 | 3.333 | 4 | 3.667 | 3.333 | 3.333 | 3.333 | 3.333 | 4 | 3 | 4 |
| Naming and abstraction, 1-5 | 3 | 3 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Error design, 1-5 | 2 | 2.667 | 1 | 2 | 2.333 | 2 | 2.667 | 2 | 2.333 | 3 | 2 | 2.667 | 2 | 2.667 | 2 |
| Test quality, 1-5 | 2 | 1.667 | 1 | 2.333 | 2 | 2.667 | 2.667 | 1 | 2.333 | 2 | 2 | 2 | 1.333 | 2.667 | 2.667 |
| Patterns warranted | 1.667 | 3 | 0 | 2 | 2 | 2 | 3.333 | 2.667 | 1.667 | 4 | 2.667 | 3 | 1.333 | 2 | 3 |
| Patterns over-engineered | 0 | 0 | 0 | 0 | 0.667 | 0.667 | 0 | 0 | 0.333 | 0.333 | 0 | 0 | 1 | 0 | 0 |
| Patterns missed | 3.333 | 3.333 | 0 | 3.333 | 3 | 2.333 | 3 | 3.333 | 3.333 | 2.667 | 2.667 | 3 | 3.333 | 3 | 2.667 |
| Line coverage of the trial's own tests, % | 72.634 | 74.305 | — | — | — | — | 26.906 | — | — | — | — | 24.714 | — | 34.620 | 26.015 |
| Docstring coverage, % | 58.230 | 0 | — | 100 | 99.390 | 85.830 | 48.210 | 98.820 | 0 | 95.720 | — | 87.500 | 0 | 16.820 | 17.350 |
| Lint findings per KLOC | 518.600 | 562.290 | — | 79.820 | 86.780 | 105.710 | 127.910 | 104.530 | 152.090 | 64.430 | — | 51.760 | 117.810 | 94.080 | 146.510 |
| Lint findings | 892 | 826 | — | 233 | 260 | 239 | 231 | 249 | 327 | 263 | — | 196 | 211 | 186 | 275 |
| Files the formatter would change | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Files the formatter would change, per KLOC | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Type errors under --strict | 193 | 190 | — | 199 | 97 | 67 | 114 | 58 | 122 | 187 | — | 133 | 27 | 13 | 73 |
| Type errors under --strict, per KLOC | 112.210 | 129.340 | — | 68.170 | 32.380 | 29.630 | 63.120 | 24.350 | 56.740 | 45.810 | — | 35.120 | 15.080 | 6.580 | 38.890 |
| Security findings, high and medium | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Security findings, high and medium, per KLOC | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Highest cognitive complexity | 212 | 117 | — | 73 | 66 | 65 | 257 | 107 | 103 | 70 | — | 62 | 308 | 115 | 200 |
| Functions over complexity 15 | 9 | 2 | — | 6 | 3 | 1 | 2 | 6 | 6 | 6 | — | 4 | 3 | 3 | 4 |
| Functions over complexity 15, per KLOC | 5.230 | 1.360 | — | 2.060 | 1 | 0.440 | 1.110 | 2.520 | 2.790 | 1.470 | — | 1.060 | 1.680 | 1.520 | 2.130 |
| Mean cyclomatic complexity | 7.480 | 3.530 | — | — | 3.890 | 3.750 | 3.120 | 5.610 | — | 3.150 | — | 3.640 | 4.360 | 3.320 | 3.600 |
| Lowest maintainability index | 19.200 | 27.190 | — | — | 28.190 | 28.290 | 26.520 | 37.100 | — | 45.730 | — | 27.710 | 5.020 | 13.290 | 24.700 |
| Unused names | 28 | 19 | — | 0 | 38 | 36 | 17 | 27 | 0 | 53 | — | 31 | 28 | 25 | 18 |
| Unused names per KLOC | 16.280 | 12.930 | — | 0 | 12.680 | 15.920 | 9.410 | 11.340 | 0 | 12.980 | — | 8.190 | 15.630 | 12.650 | 9.590 |
| Extension axes present, of three | 0 | 0 | — | 0 | 3 | 1 | 0 | 0 | 0 | 2 | — | 1 | 0 | 0 | 0 |
| Domain modules reaching Flask or the database | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Routes doing pricing arithmetic | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | 0 | 2 | 0 | 0 |
| Boolean parameters | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Conditional ladders over rule kinds | 5 | 9 | — | 4 | 5 | 6 | 6 | 4 | 7 | 8 | — | 8 | 10 | 2 | 8 |
| Public names beyond the specification | 1 | 3 | — | 0 | 0 | 1 | 1 | 2 | 2 | 1 | — | 1 | 0 | 1 | 2 |
| Specified names missing | 0 | 0 | — | 0 | 0 | 11 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Mutually importing module pairs | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| Mean instability of domain modules | 0.350 | 0.467 | — | — | — | 0.430 | 0.458 | 0.515 | 0.426 | 0.504 | — | 0.396 | 0.500 | 0.333 | 0.458 |
| Stored payload renders inert | 1 | 1 | — | — | — | — | 1 | 1 | 1 | 1 | — | — | 1 | 1 | 1 |
| A post without a token is refused | 0 | 1 | — | — | — | — | 0 | 0 | 0 | 0 | — | — | 0 | 0 | 0 |
| Accessibility violations | 10 | 10 | — | — | — | — | 10 | 10 | 10 | 10 | — | — | 10 | 10 | 10 |
| HTML validity errors | 0 | 0 | — | — | — | — | 0 | 0 | 0 | 0 | — | — | 0 | 0 | 0 |
| Invoice builder response size, bytes | 273 | 273 | — | — | — | — | 241 | 241 | 273 | 273 | — | — | 273 | 273 | 241 |
| Invoice builder subrequests | 0 | 0 | — | — | — | — | 0 | 0 | 0 | 0 | — | — | 0 | 0 | 0 |
| Output tokens | 56876 | 63127 | — | 55808 | 57711 | 62460 | 47255 | 68168 | 60639 | 581 | 49605 | 58863 | 70450 | 64284 | 58912 |
| Turns | 98 | 118 | — | 64 | 97 | 92 | 78 | 94 | 88 | 1 | 87 | 90 | 113 | 125 | 103 |
| Wall time, seconds | 654.500 | 857.600 | — | 475 | 663.400 | 709.200 | 594.300 | 751.800 | 479.400 | 558.700 | 814.500 | 793 | 733.400 | 631.200 | 730.200 |
| Cost, USD | 1.279 | 1.574 | — | 0.938 | 1.624 | 1.304 | 0.946 | 1.488 | 1.157 | 1.953 | 1.165 | 1.318 | 1.681 | 1.659 | 1.386 |
| Source lines | 1720 | 1469 | 0 | 2919 | 2996 | 2261 | 1806 | 2382 | 2150 | 4082 | 0 | 3787 | 1791 | 1977 | 1877 |
| Files | 26 | 25 | 1 | 42 | 45 | 39 | 35 | 41 | 38 | 50 | 37 | 63 | 38 | 23 | 37 |
| Artifacts nobody asked for | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Change task, acceptance pass rate | 0.608 | 0.757 | 0.689 | 0 | 0 | 0 | 0.716 | 0.716 | 0.716 | 0.676 | 0 | 0.716 | 0.716 | 0.514 | 0.689 |
| Change task, build suite pass rate after it | 0.488 | 0.507 | 0.477 | 0 | 0 | 0.006 | 0.471 | 0.238 | 0.419 | — | 0.004 | 0.420 | 0.477 | 0.471 | 0.477 |
| Change task, files touched | 10 | 10 | 26 | 11 | 13 | 11 | 9 | 13 | 12 | 13 | 10 | 11 | 6 | 7 | 9 |
| Change task, lines changed | 575 | 429 | 3196 | 426 | 388 | 167 | 1044 | 255 | 384 | 718 | 209 | 328 | 151 | 257 | 487 |
| Change task, cost, USD | 1.063 | 0.555 | 0.712 | 0.715 | 0.861 | 0.816 | 0.813 | 0.797 | 0.657 | 0.998 | 0.791 | 0.673 | 1.371 | 0.731 | 0.927 |

## Trials, and what was measured on them

| Trial | Outcome | Metrics flagged as not measured |
|---|---|---|
| none-1 | completed | hidden_suite |
| none-2 | completed | hidden_suite |
| none-3 | no cost record | bandit, complexity, cost, coverage, docstrings, hidden_suite, mypy, radon, ruff, ruff_format, structure, unused, web |
| full-1 | completed | coverage, hidden_suite, radon, web |
| full-2 | completed | coverage, hidden_suite, web |
| full-3 | completed | coverage, web |
| short-1 | completed | hidden_suite |
| short-2 | completed | coverage |
| short-3 | completed | coverage, hidden_suite, radon |
| hybrid-1 | completed | coverage, hidden_suite |
| hybrid-2 | completed | bandit, complexity, coverage, docstrings, hidden_suite, mypy, radon, ruff, ruff_format, structure, unused, web |
| hybrid-3 | completed | hidden_suite, web |
| hand-1 | completed | coverage, hidden_suite |
| hand-2 | completed | hidden_suite |
| hand-3 | completed | hidden_suite |

## Trials lost to the provider or the harness

Each was voided and re-run once in its own place, as the design's failure handling
fixes. A voided workspace is kept and never scored.

| Trial | Started | Why | Kept at | Re-run |
|---|---|---|---|---|
| hand-1 (change task) | 2026-10-16T11:08:52 | a tool call reached past the workspace: /c/efficacy/r4-weaker/ | `C:/efficacy/r4-weaker\void\change-hand-1-2026-10-16T11-24-08` | completed |
| full-2 (change task) | 2026-10-16T11:39:14 | a tool call reached past the workspace: c:/efficacy/r4-weaker/home | `C:/efficacy/r4-weaker\void\change-full-2-2026-10-16T11-44-10` | completed |
| hybrid-2 (change task) | — | no run record holds it: the run stopped before recording the trial | `C:/efficacy/r4-weaker\void\change-hybrid-2-2026-10-16T12-05-37` | completed |

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
| hybrid-2 | T109 | 100% |
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
| Readability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Maintainability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security, 1-5 | better | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | worse | worse |
| Data protection, 1-5 | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security probe pass rate, of eleven | worse | no improvement shown | not computed | better | worse | worse | better | no improvement shown |
| Data-protection probe pass rate, of three | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | worse | no improvement shown | no improvement shown |
| Task success, hidden suite pass rate | worse | worse | worse | no improvement shown | worse | worse | better | no improvement shown |
| Installs in a clean environment | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown |
| Adherence checklist fraction | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown |
| SRP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| OCP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| LSP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| ISP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | worse | no improvement shown | better |
| DIP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Naming and abstraction, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Error design, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Test quality, 1-5 | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Patterns warranted | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown |
| Patterns over-engineered | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| Patterns missed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Line coverage of the trial's own tests, % | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Docstring coverage, % | better | no improvement shown | not computed | worse | better | no improvement shown | worse | worse |
| Lint findings per KLOC | better | better | not computed | better | better | worse | better | worse |
| Lint findings | better | better | not computed | better | no improvement shown | worse | better | no improvement shown |
| Files the formatter would change | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Files the formatter would change, per KLOC | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Type errors under --strict | better | better | not computed | better | no improvement shown | worse | no improvement shown | no improvement shown |
| Type errors under --strict, per KLOC | better | better | not computed | better | no improvement shown | worse | better | no improvement shown |
| Security findings, high and medium | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security findings, high and medium, per KLOC | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Highest cognitive complexity | better | no improvement shown | not computed | no improvement shown | better | better | better | worse |
| Functions over complexity 15 | better | better | not computed | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Functions over complexity 15, per KLOC | better | better | not computed | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Mean cyclomatic complexity | not computed | better | not computed | better | worse | no improvement shown | not computed | not computed |
| Lowest maintainability index | not computed | reported without a verdict | not computed | reported without a verdict | reported without a verdict | reported without a verdict | not computed | not computed |
| Unused names | better | better | not computed | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown |
| Unused names per KLOC | better | better | not computed | better | no improvement shown | better | no improvement shown | no improvement shown |
| Extension axes present, of three | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse |
| Domain modules reaching Flask or the database | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Routes doing pricing arithmetic | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Boolean parameters | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Conditional ladders over rule kinds | better | better | not computed | better | no improvement shown | no improvement shown | worse | no improvement shown |
| Public names beyond the specification | better | better | not computed | better | better | no improvement shown | no improvement shown | worse |
| Specified names missing | no improvement shown | no improvement shown | not computed | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown |
| Mutually importing module pairs | not computed | no improvement shown | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| Mean instability of domain modules | not computed | reported without a verdict | not computed | reported without a verdict | not computed | reported without a verdict | not computed | not computed |
| Stored payload renders inert | not computed | no improvement shown | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| A post without a token is refused | not computed | worse | not computed | worse | not computed | no improvement shown | not computed | not computed |
| Accessibility violations | not computed | no improvement shown | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| HTML validity errors | not computed | no improvement shown | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| Invoice builder response size, bytes | not computed | better | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| Invoice builder subrequests | not computed | no improvement shown | not computed | no improvement shown | not computed | no improvement shown | not computed | not computed |
| Output tokens | better | better | better | worse | no improvement shown | no improvement shown | better | no improvement shown |
| Turns | better | better | better | worse | better | better | better | no improvement shown |
| Wall time, seconds | better | better | better | better | no improvement shown | no improvement shown | worse | no improvement shown |
| Cost, USD | better | better | no improvement shown | worse | better | better | no improvement shown | better |
| Source lines | worse | worse | no improvement shown | worse | worse | worse | no improvement shown | better |
| Files | worse | worse | worse | no improvement shown | worse | no improvement shown | no improvement shown | better |
| Artifacts nobody asked for | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Change task, acceptance pass rate | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | better |
| Change task, build suite pass rate after it | worse | worse | worse | worse | worse | worse | better | better |
| Change task, files touched | no improvement shown | no improvement shown | no improvement shown | better | worse | worse | no improvement shown | no improvement shown |
| Change task, lines changed | better | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Change task, cost, USD | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | better | no improvement shown | no improvement shown |

