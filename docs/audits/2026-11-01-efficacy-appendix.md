# Efficacy benchmark — 2026-11-01, technical appendix

The numbers behind [the report](2026-11-01-efficacy.md). Everything else, trial by
trial, is in [the full record](2026-11-01-efficacy-record.md).

## What produced the results

| | |
|---|---|
| Trials | 75, arms none, hybrid, reference, inline, skills, K = 15 |
| Generator | `claude-sonnet-5` |
| Judge | `gpt-6-astra` at effort `high`, codex-cli 0.165.0 |
| Blinding | condition markers stripped, order shuffled at seed 20260912 |
| Judgings per trial | 3, meaned |
| Benchmark revision, per trial | `116e50e`, `12b6d76`, `495a0ec-dirty`, `5734700`, `64eecd7`, `70b268e`, `757cc34`, `a4d8a9d`, `ae23403`, `bda0499` |
| Hidden suite | `c987eff4c100c24f070eb1ff2f2e488539b391f5` |
| Bootstrap | 10000 resamples, 95%, seed 20260912 |
| Arm hybrid's file | generated 2026-10-27T07:39:46 from the templates at `9086e0ff`, 511 lines, leak scan: clean |
| Arm reference's file | generated 2026-10-27T07:33:03 from the templates at `9086e0ff`, 19 lines, leak scan: clean |
| Arm inline's file | generated 2026-10-27T07:33:38 from the templates at `9086e0ff`, 552 lines, leak scan: clean |
| Arm skills's file | generated 2026-10-27T08:11:09 from the templates at `9086e0ff`, 1351 lines, leak scan: clean |

## The radar's axes, row by row

Each table is one axis of the radar: every measurement it groups, each approach's mean,
and each approach against `none`. Each cell: the mean paired difference, its 95 %
interval in brackets, and a mark. ▲ better and ▼ worse: the interval is clear of zero,
in the metric's direction. = held, for a row read by its margin, and ≈ no difference
shown: either way the interval's worse end stays within the row's margin, so it is no
worse than the margin, which is not the same as equal. ○ no verdict, on purpose: a row
reported without one, a pair across rounds, or two judges that disagree. (not compared):
too few complete pairs for an interval. No mark: no difference shown, on a row with no
margin or past the margin it has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

### Reliability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 2 pp | 0.992 | 0.906 | 0.882 | 0.926 | 0.906 | -0.086 [-0.352, -0.002] ▼ | -0.110 [-0.240, -0.033] ▼ | -0.066 [-0.333, 0.001] | -0.085 [-0.349, -0.002] ▼ |
| Installs in a clean environment | up | — | 1 | 0.933 | 1 | 0.933 | 0.933 | -0.067 [-0.400, 0] | 0 [0, 0] ‡ | -0.067 [-0.400, 0] | -0.067 [-0.400, 0] |

### Security

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Security, 1-5 | up | 0.3 points | 2.378 | 2.619 | 3.511 | 3.238 | 3.571 | +0.357 [-0.571, 1.214] (14 pairs) | +1.133 [0.578, 1.600] ▲ | +0.786 [-0.143, 1.738] ≈ (14 pairs) | +1.310 [0.762, 1.833] ▲ (14 pairs) |
| Security probe pass rate, of eleven | up | 2 pp | 0.758 | 0.848 | 0.888 | 0.861 | 0.848 | +0.091 [-0.085, 0.152] | +0.133 [0.091, 0.161] ▲ (13 pairs) | +0.103 [-0.097, 0.170] | +0.091 [-0.073, 0.158] |
| A post without a token is refused | up | — | 0.200 | 0.857 | 0.400 | 0.714 | 0.643 | +0.643 [0.143, 0.857] ▲ (14 pairs) | +0.200 [-0.133, 0.400] | +0.500 [0.071, 0.714] ▲ (14 pairs) | +0.500 [0, 0.714] (14 pairs) |
| Stored payload renders inert | up | — | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ (14 pairs) |
| Security findings, high and medium, per KLOC | down | 10 % relative | 0.071 | 0.185 | 0.263 | 0.159 | 0.235 | +0.113 [-0.032, 0.224] | +0.191 [-0.025, 0.587] | +0.088 [-0.055, 0.231] | +0.163 [-0.003, 0.332] |

### Data protection

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Data protection, 1-5 | up | 0.3 points | 2.867 | 3.095 | 3.089 | 3.024 | 3.095 | +0.238 [0.048, 0.667] ▲ (14 pairs) | +0.222 [0.044, 0.711] ▲ | +0.167 [0, 0.619] ≈ (14 pairs) | +0.238 [0.024, 0.833] ▲ (14 pairs) |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.622 | 0.578 | 0.644 | 0.622 | -0.044 [-0.267, 0] | -0.089 [-0.356, -0.044] ▼ | -0.022 [-0.200, 0.022] | -0.044 [-0.267, 0] |

### Design

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 0.3 points | 3 | 3 | 2.978 | 3 | 3 | 0 [0, 0] ‡ ≈ (14 pairs) | -0.022 [-0.133, 0] ≈ | 0 [0, 0] ‡ ≈ (14 pairs) | 0 [0, 0] ‡ ≈ (14 pairs) |
| SRP, 1-5 | up | — | 2.822 | 3.310 | 2.978 | 3.810 | 3.143 | +0.500 [0.238, 0.714] ▲ (14 pairs) | +0.156 [0.044, 0.311] ▲ | +0.952 [0.714, 1.095] ▲ (14 pairs) | +0.333 [0.119, 0.548] ▲ (14 pairs) |
| OCP, 1-5 | up | — | 2 | 2 | 2 | 2 | 2 | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ (14 pairs) |
| LSP, 1-5 | up | — | 2.711 | 2.786 | 2.822 | 3.381 | 2.810 | +0.167 [-0.143, 0.524] (14 pairs) | +0.111 [-0.467, 0.489] | +0.619 [0.214, 1.000] ▲ (14 pairs) | +0.119 [-0.500, 0.595] (14 pairs) |
| ISP, 1-5 | up | — | 4.067 | 4.143 | 4.067 | 3.929 | 4.167 | +0.071 [-0.119, 0.333] (14 pairs) | 0 [-0.133, 0.200] | -0.143 [-0.357, 0.024] (14 pairs) | +0.095 [-0.024, 0.310] (14 pairs) |
| DIP, 1-5 | up | — | 5 | 5 | 5 | 5 | 5 | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ (14 pairs) |
| Error design, 1-5 | up | — | 2.111 | 2.405 | 2.400 | 2.595 | 2.310 | +0.309 [0.119, 0.524] ▲ (14 pairs) | +0.289 [-0.044, 0.556] | +0.476 [0.214, 0.690] ▲ (14 pairs) | +0.191 [0.024, 0.429] ▲ (14 pairs) |
| Naming and abstraction, 1-5 | up | — | 4 | 4 | 3.978 | 4 | 4 | 0 [0, 0] ‡ (14 pairs) | -0.022 [-0.133, 0] | 0 [0, 0] ‡ (14 pairs) | 0 [0, 0] ‡ (14 pairs) |
| Patterns missed | down | — | 1.467 | 1.524 | 1.467 | 1.310 | 1.500 | +0.024 [-0.262, 0.310] (14 pairs) | 0 [-0.333, 0.311] | -0.143 [-0.429, 0.167] (14 pairs) | +0.071 [-0.238, 0.357] (14 pairs) |
| Domain modules reaching Flask or the database | down | — | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| Mutually importing module pairs | down | — | 0.800 | 0 | 0.400 | 0.500 | 0.571 | -0.857 [-3, -0.429] ▲ (14 pairs) | -0.400 [-2.400, 0.400] | -0.357 [-2.071, 0.929] (14 pairs) | -0.286 [-2, 1] (14 pairs) |

### Maintainability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Maintainability, 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 3 | 0 [0, 0] ‡ ≈ (14 pairs) | 0 [0, 0] ‡ ≈ | 0 [0, 0] ‡ ≈ (14 pairs) | 0 [0, 0] ‡ ≈ (14 pairs) |
| Readability, 1-5 | up | 0.3 points | 2.933 | 3.071 | 3 | 3 | 3.095 | +0.143 [0.024, 0.333] ▲ (14 pairs) | +0.067 [0, 0.200] ≈ | +0.071 [0, 0.214] ≈ (14 pairs) | +0.167 [0, 0.595] ≈ (14 pairs) |
| Type errors under --strict, per KLOC | down | 10 % relative | 99.122 | 3.614 | 63.085 | 3.563 | 3.563 | -95.508 [-124.679, -77.433] ▲ | -36.037 [-61.311, -8.503] ▲ | -95.559 [-122.765, -77.119] ▲ | -95.559 [-125.339, -77.929] ▲ |
| Lint findings per KLOC | down | 10 % relative | 238.933 | 137.248 | 194.367 | 141.366 | 151.198 | -101.685 [-127.942, -79.340] ▲ | -44.567 [-61.823, -20.134] ▲ | -97.567 [-122.055, -71.830] ▲ | -87.735 [-109.987, -66.191] ▲ |
| Highest cognitive complexity | down | — | 72.200 | 19.800 | 35.133 | 18.667 | 28.400 | -52.400 [-85, -30.467] ▲ | -37.067 [-69.467, -14.867] ▲ | -53.533 [-86.867, -32.400] ▲ | -43.800 [-79.467, -18.400] ▲ |
| Functions over complexity 15, per KLOC | down | 10 % relative | 1.439 | 0.401 | 1.156 | 0.399 | 0.681 | -1.039 [-1.315, -0.749] ▲ | -0.283 [-0.729, 0.212] | -1.041 [-1.277, -0.818] ▲ | -0.759 [-1.123, -0.288] ▲ |
| Mean cyclomatic complexity | down | — | 3.305 | 2.786 | 3.053 | 2.761 | 2.854 | -0.519 [-0.635, -0.367] ▲ | -0.251 [-0.370, -0.125] ▲ | -0.544 [-0.677, -0.429] ▲ | -0.451 [-0.591, -0.281] ▲ |
| Unused names per KLOC | down | 10 % relative | 13.317 | 7.840 | 11.686 | 9.677 | 12.766 | -5.477 [-7.284, -3.152] ▲ | -1.631 [-4.167, 1.258] ≈ | -3.640 [-5.768, -1.611] ▲ | -0.551 [-3.097, 2.128] |

### Tests

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Test quality, 1-5 | up | — | 3.089 | 3.500 | 3.622 | 3.905 | 3.238 | +0.405 [0.024, 0.619] ▲ (14 pairs) | +0.533 [0.267, 0.733] ▲ | +0.881 [0.667, 0.952] ▲ (14 pairs) | +0.143 [0.024, 0.333] ▲ (14 pairs) |
| Line coverage of the trial's own tests, % | up | — | 72.665 | 93.036 | 86.864 | 94.899 | 81.264 | +22.231 [10.510, 33.969] ▲ (8 pairs) | +15.439 [2.699, 26.284] ▲ (14 pairs) | +24.804 [14.944, 33.538] ▲ (13 pairs) | +7.515 [-7.117, 21.382] (14 pairs) |

### Economy

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cost, USD | down | — | 4.294 | 11.783 | 7.208 | 14.184 | 9.302 | +7.489 [6.550, 8.636] ▼ | +2.915 [2.325, 3.736] ▼ | +9.890 [8.326, 12.227] ▼ | +5.009 [4.024, 6.242] ▼ |
| Output tokens | down | — | 122963.7 | 169072 | 154568.3 | 174413.5 | 159560.5 | +46108.3 [1924.3, 61839.9] ▼ | +31604.5 [21863.9, 41453.1] ▼ | +51449.8 [4796.9, 75872.1] ▼ | +36596.8 [25594, 47760.1] ▼ |
| Turns | down | — | 93.867 | 197.667 | 139 | 197.800 | 168 | +103.800 [57.267, 122.667] ▼ | +45.133 [36, 59.200] ▼ | +103.933 [56.267, 131] ▼ | +74.133 [59.867, 91.733] ▼ |
| Wall time, seconds | down | — | 1358.3 | 2394.8 | 1815.1 | 2793.4 | 1906.1 | +1036.6 [867, 1225.1] ▼ | +456.820 [333.520, 619.213] ▼ | +1435.1 [1195.5, 1837.6] ▼ | +547.793 [382.420, 723.820] ▼ |

## The verdict vector

The whole vector, which the summary's scores digest and never replace.

| Metric | hybrid−none | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline |
|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Readability, 1-5 | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Maintainability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security, 1-5 | no improvement shown | better | no improvement shown | better | better | better | no improvement shown |
| Data protection, 1-5 | better | better | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown |
| Security probe pass rate, of eleven | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Data-protection probe pass rate, of three | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Task success, hidden suite pass rate | worse | worse | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown |
| Installs in a clean environment | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Adherence checklist fraction | better | better | better | better | no improvement shown | no improvement shown | no improvement shown |
| SRP, 1-5 | better | better | better | better | no improvement shown | worse | worse |
| OCP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| LSP, 1-5 | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| ISP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| DIP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Naming and abstraction, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Error design, 1-5 | better | no improvement shown | better | better | no improvement shown | no improvement shown | no improvement shown |
| Test quality, 1-5 | better | better | better | better | no improvement shown | no improvement shown | worse |
| Patterns warranted | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns over-engineered | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns missed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Line coverage of the trial's own tests, % | better | better | better | no improvement shown | worse | worse | worse |
| Docstring coverage, % | better | better | better | better | no improvement shown | no improvement shown | no improvement shown |
| Lint findings per KLOC | better | better | better | better | worse | worse | no improvement shown |
| Lint findings | no improvement shown | no improvement shown | no improvement shown | better | better | no improvement shown | better |
| Files the formatter would change | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Files the formatter would change, per KLOC | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Type errors under --strict | better | no improvement shown | better | better | no improvement shown | worse | no improvement shown |
| Type errors under --strict, per KLOC | better | better | better | better | no improvement shown | worse | no improvement shown |
| Security findings, high and medium | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security findings, high and medium, per KLOC | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Highest cognitive complexity | better | better | better | better | worse | worse | worse |
| Functions over complexity 15 | better | no improvement shown | better | better | no improvement shown | worse | no improvement shown |
| Functions over complexity 15, per KLOC | better | no improvement shown | better | better | no improvement shown | worse | no improvement shown |
| Mean cyclomatic complexity | better | better | better | better | no improvement shown | worse | worse |
| Lowest maintainability index | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Unused names | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Unused names per KLOC | better | no improvement shown | better | no improvement shown | worse | worse | worse |
| Extension axes present, of three | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Domain modules reaching Flask or the database | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Routes doing pricing arithmetic | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Boolean parameters | better | better | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown |
| Conditional ladders over rule kinds | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Public names beyond the specification | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Specified names missing | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Mutually importing module pairs | better | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown |
| Mean instability of domain modules | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Stored payload renders inert | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| A post without a token is refused | better | no improvement shown | better | no improvement shown | no improvement shown | worse | no improvement shown |
| Accessibility violations | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| HTML validity errors | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Invoice builder response size, bytes | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Invoice builder subrequests | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Output tokens | worse | worse | worse | worse | no improvement shown | no improvement shown | no improvement shown |
| Turns | worse | worse | worse | worse | no improvement shown | better | no improvement shown |
| Wall time, seconds | worse | worse | worse | worse | better | better | better |
| Cost, USD | worse | worse | worse | worse | better | better | better |
| Source lines | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Files | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| App code, lines | worse | held | worse | held | better | better | better |
| App code, files | worse | held | worse | held | better | better | better |
| Test code, lines | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Artifacts nobody asked for | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Change task, acceptance pass rate | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, build suite pass rate after it | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, files touched | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, lines changed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, cost, USD | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
