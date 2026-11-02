# Efficacy benchmark — 2026-11-02, technical appendix

The numbers behind [the report](2026-11-02-efficacy.md). Everything else, trial by
trial, is in [the full record](2026-11-02-efficacy-record.md).

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
in the metric's direction, and under round 5d's rules clear of the row's margin. = held,
for a row read by its margin, and ≈ no difference shown: either way the interval's worse
end stays within the row's margin, so it is no worse than the margin, which is not the
same as equal. ○ no verdict, on purpose: a row reported without one, a pair across
rounds, or two judges that disagree. (not compared): too few complete pairs for an
interval. No mark: no difference shown, on a row with no margin or past the margin it
has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

### Reliability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 2 pp | 0.992 | 0.972 | 0.882 | 0.992 | 0.953 | -0.020 [-0.097, 0.000] | -0.110 [-0.240, -0.033] ▼ | -0.000 [-0.004, 0.002] ≈ | -0.038 [-0.115, -0.001] ▼ |
| Installs in a clean environment | up | — | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |

### Security

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Security, 1-5 | up | 0.3 points | 2.378 | 2.711 | 3.511 | 3.267 | 3.556 | +0.333 [-0.489, 1.133] | +1.133 [0.578, 1.600] ▲ | +0.889 [-0.022, 1.756] ≈ | +1.178 [0.600, 1.711] ▲ |
| Security probe pass rate, of eleven | up | 2 pp | 0.758 | 0.897 | 0.888 | 0.909 | 0.897 | +0.139 [0.091, 0.176] ▲ | +0.133 [0.091, 0.161] ▲ (13 pairs) | +0.151 [0.109, 0.200] ▲ | +0.139 [0.085, 0.182] ▲ |
| A post without a token is refused | up | — | 0.200 | 0.867 | 0.400 | 0.733 | 0.667 | +0.667 [0.133, 0.867] ▲ | +0.200 [-0.133, 0.400] | +0.533 [0.067, 0.733] ▲ | +0.467 [0, 0.667] |
| Stored payload renders inert | up | — | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| Security findings, high and medium, per KLOC | down | 10 % relative | 0.071 | 0.185 | 0.263 | 0.159 | 0.235 | +0.113 [-0.032, 0.224] | +0.191 [-0.025, 0.587] | +0.088 [-0.055, 0.231] | +0.163 [-0.003, 0.332] |

### Data protection

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Data protection, 1-5 | up | 0.3 points | 2.867 | 3.111 | 3.089 | 3.044 | 3.089 | +0.244 [0.067, 0.667] ▲ | +0.222 [0.044, 0.711] ▲ | +0.178 [0.022, 0.600] ▲ | +0.222 [0.022, 0.756] ▲ |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.667 | 0.578 | 0.689 | 0.667 | 0 [0, 0] ‡ ≈ | -0.089 [-0.356, -0.044] ▼ | +0.022 [0, 0.067] ≈ | 0 [0, 0] ‡ ≈ |

### Design

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 0.3 points | 3 | 3 | 2.978 | 3 | 3 | 0 [0, 0] ‡ ≈ | -0.022 [-0.133, 0] ≈ | 0 [0, 0] ‡ ≈ | 0 [0, 0] ‡ ≈ |
| SRP, 1-5 | up | — | 2.822 | 3.356 | 2.978 | 3.822 | 3.156 | +0.533 [0.289, 0.733] ▲ | +0.156 [0.044, 0.311] ▲ | +1 [0.756, 1.156] ▲ | +0.333 [0.133, 0.533] ▲ |
| OCP, 1-5 | up | — | 2 | 2 | 2 | 2 | 2 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| LSP, 1-5 | up | — | 2.711 | 2.933 | 2.822 | 3.356 | 2.867 | +0.222 [-0.111, 0.556] | +0.111 [-0.467, 0.489] | +0.644 [0.267, 1.000] ▲ | +0.156 [-0.467, 0.600] |
| ISP, 1-5 | up | — | 4.067 | 4.133 | 4.067 | 3.933 | 4.200 | +0.067 [-0.111, 0.311] | 0 [-0.133, 0.200] | -0.133 [-0.333, 0.022] | +0.133 [0, 0.333] |
| DIP, 1-5 | up | — | 5 | 5 | 5 | 5 | 5 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| Error design, 1-5 | up | — | 2.111 | 2.422 | 2.400 | 2.578 | 2.289 | +0.311 [0.111, 0.489] ▲ | +0.289 [-0.044, 0.556] | +0.467 [0.200, 0.667] ▲ | +0.178 [0, 0.400] |
| Naming and abstraction, 1-5 | up | — | 4 | 4 | 3.978 | 4 | 4 | 0 [0, 0] ‡ | -0.022 [-0.133, 0] | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| Patterns missed | down | — | 1.467 | 1.511 | 1.467 | 1.289 | 1.489 | +0.044 [-0.244, 0.311] | 0 [-0.333, 0.311] | -0.178 [-0.444, 0.111] | +0.022 [-0.267, 0.311] |
| Domain modules reaching Flask or the database | down | — | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ | 0 [0, 0] ‡ |
| Mutually importing module pairs | down | — | 0.800 | 0 | 0.400 | 0.467 | 0.533 | -0.800 [-3.200, -0.400] ▲ | -0.400 [-2.400, 0.400] | -0.333 [-2, 0.867] | -0.267 [-1.933, 0.933] |

### Maintainability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Maintainability, 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 3 | 0 [0, 0] ‡ ≈ | 0 [0, 0] ‡ ≈ | 0 [0, 0] ‡ ≈ | 0 [0, 0] ‡ ≈ |
| Readability, 1-5 | up | 0.3 points | 2.933 | 3.067 | 3 | 3.044 | 3.111 | +0.133 [0.022, 0.333] ▲ | +0.067 [0, 0.200] ≈ | +0.111 [0, 0.311] ≈ | +0.178 [0.022, 0.622] ▲ |
| Type errors under --strict, per KLOC | down | 10 % relative | 99.122 | 3.577 | 63.085 | 3.563 | 3.563 | -95.545 [-124.763, -77.443] ▲ | -36.037 [-61.311, -8.503] ▲ | -95.559 [-122.765, -77.119] ▲ | -95.559 [-125.339, -77.929] ▲ |
| Lint findings per KLOC | down | 10 % relative | 238.933 | 137.248 | 194.367 | 141.366 | 151.198 | -101.685 [-127.942, -79.340] ▲ | -44.567 [-61.823, -20.134] ▲ | -97.567 [-122.055, -71.830] ▲ | -87.735 [-109.987, -66.191] ▲ |
| Highest cognitive complexity | down | — | 72.200 | 19.800 | 35.133 | 18.667 | 28.400 | -52.400 [-85, -30.467] ▲ | -37.067 [-69.467, -14.867] ▲ | -53.533 [-86.867, -32.400] ▲ | -43.800 [-79.467, -18.400] ▲ |
| Functions over complexity 15, per KLOC | down | 10 % relative | 1.439 | 0.401 | 1.156 | 0.399 | 0.681 | -1.039 [-1.315, -0.749] ▲ | -0.283 [-0.729, 0.212] | -1.041 [-1.277, -0.818] ▲ | -0.759 [-1.123, -0.288] ▲ |
| Mean cyclomatic complexity | down | — | 3.305 | 2.786 | 3.053 | 2.761 | 2.854 | -0.519 [-0.635, -0.367] ▲ | -0.251 [-0.370, -0.125] ▲ | -0.544 [-0.677, -0.429] ▲ | -0.451 [-0.591, -0.281] ▲ |
| Unused names per KLOC | down | 10 % relative | 13.317 | 7.840 | 11.686 | 9.677 | 12.766 | -5.477 [-7.284, -3.152] ▲ | -1.631 [-4.167, 1.258] ≈ | -3.640 [-5.768, -1.611] ▲ | -0.551 [-3.097, 2.128] |

### Tests

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Test quality, 1-5 | up | — | 3.089 | 3.533 | 3.622 | 3.911 | 3.267 | +0.444 [0.089, 0.667] ▲ | +0.533 [0.267, 0.733] ▲ | +0.822 [0.578, 0.933] ▲ | +0.178 [0.044, 0.356] ▲ |
| Line coverage of the trial's own tests, % | up | — | 72.685 | 93.036 | 86.951 | 95.080 | 81.984 | +22.231 [10.510, 33.969] ▲ (8 pairs) | +15.504 [2.773, 26.389] ▲ (14 pairs) | +23.620 [14.567, 32.337] ▲ (14 pairs) | +9.298 [-5.289, 22.514] |

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
| Readability, 1-5 | better | no improvement shown | no improvement shown | better | no improvement shown | worse | no improvement shown |
| Maintainability, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Security, 1-5 | no improvement shown | better | no improvement shown | better | better | better | no improvement shown |
| Data protection, 1-5 | better | better | better | better | no improvement shown | no improvement shown | no improvement shown |
| Security probe pass rate, of eleven | better | better | better | better | no improvement shown | no improvement shown | no improvement shown |
| Data-protection probe pass rate, of three | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Task success, hidden suite pass rate | no improvement shown | worse | no improvement shown | worse | no improvement shown | no improvement shown | worse |
| Installs in a clean environment | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Installs and boots | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | worse | no improvement shown |
| Adherence checklist fraction | better | better | better | better | no improvement shown | no improvement shown | no improvement shown |
| SRP, 1-5 | better | better | better | better | no improvement shown | worse | worse |
| OCP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| LSP, 1-5 | no improvement shown | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| ISP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | better |
| DIP, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Naming and abstraction, 1-5 | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Error design, 1-5 | better | no improvement shown | better | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
| Test quality, 1-5 | better | better | better | better | no improvement shown | no improvement shown | worse |
| Patterns warranted | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
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
| Public names beyond the specification | no improvement shown | no improvement shown | worse | no improvement shown | no improvement shown | no improvement shown | no improvement shown |
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
