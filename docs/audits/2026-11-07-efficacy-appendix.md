# Efficacy benchmark — 2026-11-07, technical appendix

The numbers behind [the report](2026-11-07-efficacy.md). Everything else, trial by
trial, is in [the full record](2026-11-07-efficacy-record.md).

## What produced the results

| | |
|---|---|
| Trials | 105, arms none, short, hybrid, hand, reference, inline, skills, K = 15 |
| Generator | `claude-sonnet-5` |
| Judge | `gpt-6-astra` at effort `high`, codex-cli 0.166.0 |
| Blinding | condition markers stripped, order shuffled at seed 20260912 |
| Judgings per trial | 3, meaned |
| Benchmark revision, per trial | `116e50e`, `12b6d76`, `1baac26`, `495a0ec-dirty`, `5236ede`, `5580e2c`, `5734700`, `5a15eb1-dirty`, `5e1e35b`, `64eecd7`, `70b268e`, `757cc34`, `852906e`, `a3c09fc-dirty`, `a4d8a9d`, `ae23403`, `bda0499`, `c462a80`, `ea8d503`, `edea33c-dirty`, `f161e8e`, `f161e8e-dirty` |
| Hidden suite | `1f07e422b3b5348418a596d36c7a2d582688d49b` |
| Bootstrap | 10000 resamples, 95%, seed 20260912 |
| Arm short's file | generated 2026-10-31T13:22:29 from the templates at `9086e0ff`, 40 lines, leak scan: clean |
| Arm hybrid's file | generated 2026-10-27T07:39:46 from the templates at `9086e0ff`, 511 lines, leak scan: clean |
| Arm reference's file | generated 2026-10-27T07:33:03 from the templates at `9086e0ff`, 19 lines, leak scan: clean |
| Arm inline's file | generated 2026-10-27T07:33:38 from the templates at `9086e0ff`, 552 lines, leak scan: clean |
| Arm skills's file | generated 2026-10-27T08:11:09 from the templates at `9086e0ff`, 1351 lines, leak scan: clean |

## The radar's axes, row by row

Each table is one axis of the radar: every measurement it groups, each approach's mean,
and each approach against `none`. Each cell: the mean difference, its 95 % interval in
brackets, and a mark. ▲ better and ▼ worse: the interval is clear of zero, in the
metric's direction, and under round 5d's rules clear of the row's margin. = held, for a
row read by its margin, and ≈ no difference shown: either way the interval's worse end
stays within the row's margin, so it is no worse than the margin, which is not the same
as equal. ○ no verdict, on purpose: a row reported without one, a pair across rounds, or
two judges that disagree. (not compared): too few complete pairs for an interval. No
mark: no difference shown, on a row with no margin or past the margin it has.

Each interval below is a 95 % bootstrap interval over the paired differences of its
contrast, one per block that measured both arms: K = 15 at most, and a cell that had
fewer names its count. The contrasts whose arms ran in different rounds, short − none,
hand − none, inline − hand, hybrid − hand, reference − hand, skills − hand and short −
inline, are unpaired: each arm's trials stand on their own, and the interval is for the
difference of two independent means.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

### Reliability

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Installs and boots | up | 6.7 pp | 1 | 1 | 1 | 1 | 0.867 | 1 | 1 | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ |
| Task success, hidden suite pass rate | up | 2 pp | 0.992 | 0.991 | 0.991 | 0.991 | 0.976 | 0.992 | 0.992 | -0.001 [-0.003, 0.001] = | -0.001 [-0.003, 0.001] = | -0.001 [-0.003, 0.001] = | -0.016 [-0.087, 0.002] (13 pairs) | -0.000 [-0.004, 0.002] = | -0.000 [-0.003, 0.002] = |

### Security

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Security, 1-5 | up | 0.3 points | 2.378 | 3.089 | 2.711 | 2.600 | 3.511 | 3.267 | 3.556 | +0.711 [-0.178, 1.511] = | +0.333 [-0.489, 1.133] | +0.222 [-0.644, 1.044] | +1.133 [0.578, 1.600] ▲ | +0.889 [-0.022, 1.756] = | +1.178 [0.600, 1.711] ▲ |
| Security probe pass rate, of eleven | up | 2 pp | 0.758 | 0.824 | 0.897 | 0.776 | 0.888 | 0.909 | 0.897 | +0.067 [0.030, 0.109] ▲ | +0.139 [0.091, 0.176] ▲ | +0.018 [-0.036, 0.055] | +0.133 [0.091, 0.161] ▲ (13 pairs) | +0.151 [0.109, 0.200] ▲ | +0.139 [0.085, 0.182] ▲ |
| A post without a token is refused | up | — | 0.200 | 0.267 | 0.867 | 0.267 | 0.400 | 0.733 | 0.667 | +0.067 [-0.267, 0.267] | +0.667 [0.133, 0.867] ▲ | +0.067 [-0.267, 0.267] | +0.200 [-0.133, 0.400] | +0.533 [0.067, 0.733] ▲ | +0.467 [0, 0.667] = |
| Stored payload renders inert | up | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Security findings, high and medium, per KLOC | down | 10 % relative | 0.071 | 0.166 | 0.185 | 0.030 | 0.263 | 0.159 | 0.235 | +0.095 [-0.057, 0.383] | +0.113 [-0.032, 0.224] | -0.041 [-0.183, 0.030] | +0.191 [-0.025, 0.587] | +0.088 [-0.055, 0.231] | +0.163 [-0.003, 0.332] |

### Data protection

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Data protection, 1-5 | up | 0.3 points | 2.867 | 3.022 | 3.111 | 2.978 | 3.089 | 3.044 | 3.089 | +0.156 [0, 0.578] = | +0.244 [0.067, 0.667] = | +0.111 [-0.311, 0.467] | +0.222 [0.044, 0.711] = | +0.178 [0.022, 0.600] = | +0.222 [0.022, 0.756] = |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.689 | 0.667 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 pairs) | +0.022 [0, 0.067] = | 0 [0, 0] ‡ = |

### Design

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 2.978 | 3 | 3 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| SRP, 1-5 | up | — | 2.822 | 3.022 | 3.356 | 3.178 | 2.978 | 3.822 | 3.156 | +0.200 [0.067, 0.400] ▲ | +0.533 [0.289, 0.733] ▲ | +0.356 [0.156, 0.622] ▲ | +0.156 [0.044, 0.311] ▲ | +1 [0.756, 1.156] ▲ | +0.333 [0.133, 0.533] ▲ |
| OCP, 1-5 | up | — | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| LSP, 1-5 | up | — | 2.711 | 2.822 | 2.933 | 2.889 | 2.822 | 3.356 | 2.867 | +0.111 [-0.378, 0.622] | +0.222 [-0.111, 0.556] | +0.178 [-0.267, 0.600] | +0.111 [-0.467, 0.489] | +0.644 [0.267, 1.000] ▲ | +0.156 [-0.467, 0.600] |
| ISP, 1-5 | up | — | 4.067 | 4.244 | 4.133 | 4.022 | 4.067 | 3.933 | 4.200 | +0.178 [-0.044, 0.422] | +0.067 [-0.111, 0.311] | -0.044 [-0.222, 0.022] | 0 [-0.133, 0.200] | -0.133 [-0.333, 0.022] | +0.133 [0, 0.333] = |
| DIP, 1-5 | up | — | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Error design, 1-5 | up | — | 2.111 | 2.044 | 2.422 | 2.689 | 2.400 | 2.578 | 2.289 | -0.067 [-0.267, 0.067] | +0.311 [0.111, 0.489] ▲ | +0.578 [0.289, 0.778] ▲ | +0.289 [-0.044, 0.556] | +0.467 [0.200, 0.667] ▲ | +0.178 [0, 0.400] = |
| Naming and abstraction, 1-5 | up | — | 4 | 3.978 | 4 | 4 | 3.978 | 4 | 4 | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Patterns missed | down | — | 1.467 | 1.444 | 1.511 | 1.489 | 1.467 | 1.289 | 1.489 | -0.022 [-0.289, 0.222] | +0.044 [-0.244, 0.311] | +0.022 [-0.244, 0.244] | 0 [-0.333, 0.311] | -0.178 [-0.444, 0.111] | +0.022 [-0.267, 0.311] |
| Modules import tariff loads that reach Flask or the database | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Mutually importing module pairs | down | — | 0.800 | 1.267 | 0 | 0.867 | 0.400 | 0.467 | 0.533 | +0.467 [-1.200, 2.067] | -0.800 [-3.200, -0.400] ▲ | +0.067 [-1.600, 1.400] | -0.400 [-2.400, 0.400] | -0.333 [-2, 0.867] | -0.267 [-1.933, 0.933] |

### Maintainability

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Maintainability, 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Readability, 1-5 | up | 0.3 points | 2.933 | 3 | 3.067 | 3 | 3 | 3.044 | 3.111 | +0.067 [0, 0.200] = | +0.133 [0.022, 0.333] = | +0.067 [0, 0.200] = | +0.067 [0, 0.200] = | +0.111 [0, 0.311] = | +0.178 [0.022, 0.622] = |
| Type errors under --strict, per KLOC | down | 10 % relative | 99.122 | 5.850 | 3.577 | 13.102 | 63.085 | 3.563 | 3.563 | -93.272 [-121.167, -73.096] ▲ | -95.545 [-124.763, -77.443] ▲ | -86.020 [-115.099, -65.947] ▲ | -36.037 [-61.311, -8.503] = | -95.559 [-122.765, -77.119] ▲ | -95.559 [-125.339, -77.929] ▲ |
| Lint findings per KLOC | down | 10 % relative | 238.933 | 146.964 | 137.248 | 139.602 | 194.367 | 141.366 | 151.198 | -91.969 [-119.671, -68.166] ▲ | -101.685 [-127.942, -79.340] ▲ | -99.331 [-127.208, -76.255] ▲ | -44.567 [-61.823, -20.134] = | -97.567 [-122.055, -71.830] ▲ | -87.735 [-109.987, -66.191] ▲ |
| Highest cognitive complexity | down | — | 72.200 | 40.600 | 19.800 | 29.533 | 35.133 | 18.667 | 28.400 | -31.600 [-63.333, -3.533] ▲ | -52.400 [-85, -30.467] ▲ | -42.667 [-75.200, -19.200] ▲ | -37.067 [-69.467, -14.867] ▲ | -53.533 [-86.867, -32.400] ▲ | -43.800 [-79.467, -18.400] ▲ |
| Functions over complexity 15, per KLOC | down | 10 % relative | 1.439 | 1.080 | 0.401 | 0.809 | 1.156 | 0.399 | 0.681 | -0.359 [-0.637, -0.047] = | -1.039 [-1.315, -0.749] ▲ | -0.630 [-0.981, -0.193] ▲ | -0.283 [-0.729, 0.212] | -1.041 [-1.277, -0.818] ▲ | -0.759 [-1.123, -0.288] ▲ |
| Mean cyclomatic complexity | down | — | 3.305 | 3.007 | 2.786 | 2.877 | 3.053 | 2.761 | 2.854 | -0.298 [-0.451, -0.114] ▲ | -0.519 [-0.635, -0.367] ▲ | -0.427 [-0.575, -0.272] ▲ | -0.251 [-0.370, -0.125] ▲ | -0.544 [-0.677, -0.429] ▲ | -0.451 [-0.591, -0.281] ▲ |
| Unused names per KLOC | down | 10 % relative | 13.317 | 10.201 | 7.840 | 11.749 | 11.686 | 9.677 | 12.766 | -3.116 [-5.221, -0.875] = | -5.477 [-7.284, -3.152] ▲ | -1.567 [-4.043, 0.947] = | -1.631 [-4.167, 1.258] = | -3.640 [-5.768, -1.611] ▲ | -0.551 [-3.097, 2.128] |

### Tests

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Test quality, 1-5 | up | — | 3.089 | 3.222 | 3.533 | 3.400 | 3.622 | 3.911 | 3.267 | +0.133 [-0.111, 0.333] | +0.444 [0.089, 0.667] ▲ | +0.311 [0.022, 0.511] ▲ | +0.533 [0.267, 0.733] ▲ | +0.822 [0.578, 0.933] ▲ | +0.178 [0.044, 0.356] ▲ |
| Line coverage of the trial's own tests, % | up | — | 72.685 | 81.839 | 93.036 | 90.353 | 86.951 | 95.080 | 81.984 | +9.153 [-2.558, 19.951] | +22.231 [10.510, 33.969] ▲ (8 pairs) | +17.668 [6.430, 27.319] ▲ | +15.504 [2.773, 26.389] ▲ (14 pairs) | +23.620 [14.567, 32.337] ▲ (14 pairs) | +9.298 [-5.289, 22.514] |

### Economy

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cost, USD | down | 25 % relative | 4.294 | 8.061 | 11.783 | 8.284 | 7.208 | 14.184 | 9.302 | +3.767 [3.011, 4.445] ▼ | +7.489 [6.550, 8.636] ▼ | +3.990 [3.285, 4.627] ▼ | +2.915 [2.325, 3.736] ▼ | +9.890 [8.326, 12.227] ▼ | +5.009 [4.024, 6.242] ▼ |
| Turns | down | 25 % relative | 93.867 | 154 | 197.667 | 157.267 | 139 | 197.800 | 168 | +60.133 [24.067, 77.933] ▼ | +103.800 [57.267, 122.667] ▼ | +63.400 [26.800, 78.533] ▼ | +45.133 [36, 59.200] ▼ | +103.933 [56.267, 131] ▼ | +74.133 [59.867, 91.733] ▼ |

## The verdict vector

The whole vector, which the summary's scores digest and never replace.

| Metric | short−none | hybrid−none | hand−none | short−hand | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline | inline−hand | hybrid−hand | reference−hand | skills−hand | short−inline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Readability, 1-5 | held | held | held | held | held | held | held | held | held | held | held | held | held | held | no improvement shown |
| Maintainability, 1-5 | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Security, 1-5 | held | no improvement shown | no improvement shown | no improvement shown | better | held | better | held | held | held | held | no improvement shown | held | better | no improvement shown |
| Data protection, 1-5 | held | held | no improvement shown | held | held | held | held | held | held | held | held | held | held | held | held |
| Security probe pass rate, of eleven | better | better | no improvement shown | held | better | better | better | no improvement shown | no improvement shown | no improvement shown | better | better | better | better | worse |
| Data-protection probe pass rate, of three | held | held | held | held | held | held | held | held | held | no improvement shown | held | held | held | held | no improvement shown |
| Task success, hidden suite pass rate | held | held | held | held | no improvement shown | held | held | held | no improvement shown | held | held | held | no improvement shown | held | held |
| Installs in a clean environment | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Installs and boots | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Adherence checklist fraction | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| SRP, 1-5 | better | better | better | worse | better | better | better | no improvement shown | worse | worse | better | no improvement shown | worse | no improvement shown | worse |
| OCP, 1-5 | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| LSP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | worse |
| ISP, 1-5 | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | held | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | better | better |
| DIP, 1-5 | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Naming and abstraction, 1-5 | no improvement shown | held | held | no improvement shown | no improvement shown | held | held | held | no improvement shown | held | held | held | no improvement shown | held | no improvement shown |
| Error design, 1-5 | no improvement shown | better | better | worse | no improvement shown | better | held | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | worse |
| Test quality, 1-5 | no improvement shown | better | better | no improvement shown | better | better | better | no improvement shown | no improvement shown | worse | better | no improvement shown | no improvement shown | no improvement shown | worse |
| Patterns warranted | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns over-engineered | no improvement shown | no improvement shown | held | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Patterns missed | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Line coverage of the trial's own tests, % | no improvement shown | better | better | no improvement shown | better | better | no improvement shown | worse | worse | worse | better | no improvement shown | no improvement shown | no improvement shown | worse |
| Docstring coverage, % | better | better | better | no improvement shown | better | better | better | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | better | no improvement shown | worse |
| Lint findings per KLOC | better | better | better | no improvement shown | held | better | better | no improvement shown | worse | no improvement shown | held | held | worse | no improvement shown | no improvement shown |
| Lint findings | better | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | better | better | no improvement shown | better | worse | worse | worse | no improvement shown | no improvement shown |
| Files the formatter would change | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Files the formatter would change, per KLOC | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Type errors under --strict | better | better | better | no improvement shown | no improvement shown | better | better | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown |
| Type errors under --strict, per KLOC | better | better | better | no improvement shown | held | better | better | no improvement shown | worse | no improvement shown | held | held | worse | held | no improvement shown |
| Security findings, high and medium | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | worse | worse | worse | no improvement shown |
| Security findings, high and medium, per KLOC | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | worse | worse | worse | no improvement shown |
| Highest cognitive complexity | better | better | better | no improvement shown | better | better | better | worse | worse | worse | better | better | no improvement shown | no improvement shown | worse |
| Functions over complexity 15 | no improvement shown | better | better | worse | no improvement shown | better | better | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse |
| Functions over complexity 15, per KLOC | held | better | better | no improvement shown | no improvement shown | better | better | no improvement shown | worse | no improvement shown | better | better | no improvement shown | no improvement shown | worse |
| Mean cyclomatic complexity | better | better | better | worse | better | better | better | no improvement shown | worse | worse | better | better | worse | no improvement shown | worse |
| Lowest maintainability index | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Unused names | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Unused names per KLOC | held | better | held | held | held | better | no improvement shown | worse | worse | worse | held | better | no improvement shown | no improvement shown | no improvement shown |
| Extension axes present, of three | held | held | held | worse | held | held | held | no improvement shown | worse | held | worse | no improvement shown | worse | no improvement shown | held |
| Modules import tariff loads that reach Flask or the database | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Routes doing pricing arithmetic | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Boolean parameters | better | better | no improvement shown | no improvement shown | better | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| Conditional ladders over rule kinds | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Public names beyond the specification | no improvement shown | no improvement shown | worse | better | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| Specified names missing | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Mutually importing module pairs | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown |
| Mean instability of domain modules | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Stored payload renders inert | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| A post without a token is refused | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | better | held | no improvement shown | worse | no improvement shown | held | better | no improvement shown | no improvement shown | worse |
| Accessibility violations | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| HTML validity errors | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Invoice builder response size, bytes | held | held | held | held | held | no improvement shown | held | held | held | held | no improvement shown | held | held | held | held |
| Invoice builder subrequests | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Output tokens | no improvement shown | no improvement shown | no improvement shown | held | no improvement shown | no improvement shown | no improvement shown | held | held | held | no improvement shown | no improvement shown | no improvement shown | no improvement shown | held |
| Turns | worse | worse | worse | held | worse | worse | worse | held | held | held | no improvement shown | no improvement shown | held | no improvement shown | held |
| Wall time, seconds | worse | worse | worse | held | no improvement shown | worse | worse | held | held | held | no improvement shown | no improvement shown | held | held | held |
| Cost, USD | worse | worse | worse | held | worse | worse | worse | held | better | held | worse | worse | held | no improvement shown | better |
| Source lines | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Files | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| App code, lines | held | worse | held | held | held | worse | held | held | held | held | worse | no improvement shown | held | held | held |
| App code, files | held | worse | held | held | held | worse | held | held | held | held | no improvement shown | no improvement shown | held | held | held |
| Test code, lines | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict | reported without a verdict |
| Artifacts nobody asked for | held | held | held | held | held | held | held | held | held | held | held | held | held | held | held |
| Change task, acceptance pass rate | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, build suite pass rate after it | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, files touched | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, lines changed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
| Change task, cost, USD | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed | not computed |
