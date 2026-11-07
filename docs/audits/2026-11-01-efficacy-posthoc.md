# Efficacy benchmark — 2026-11-01, a post-hoc reading

**Post-hoc.** These rules were registered for round 5d, after this round ran. The
round's registered verdicts stand; this page shows how its trials read under the later
rules, and decides nothing.

![Radar per arm, post-hoc](2026-11-01-efficacy-posthoc-radar-dark.svg#gh-dark-mode-only)
![Radar per arm,
post-hoc](2026-11-01-efficacy-posthoc-radar-light.svg#gh-light-mode-only)

One radar per arm, from the cheapest to the dearest. Each axis is the mean of its rows'
moves against `none`: each row's interval bound nearest zero over the row's full scale,
from -1 at the centre to +1 at the rim, and 0 where the interval crosses zero. A row's
full scale is 1 point for a judge score, 20 pp for a share, 20 points for coverage, and
a factor of 4 for a count or a cost, so a reader can work any axis out from the
intervals below. The dashed ring is `none`, so outside it is better. A hollow point is
an axis with no verdict. The rows behind each axis, and every number, are in the
sections below.

| Axis | `reference` | `skills` | `hybrid` | `inline` | Rows |
| --- | --- | --- | --- | --- | --- |
| Reliability | 0.00 | 0.00 | 0.00 | 0.00 | Installs and boots; Task success, hidden suite pass rate |
| Security | +0.21 | +0.20 | +0.22 | +0.18 | Security, 1-5; Security probe pass rate, of eleven; A post without a token is refused; Stored payload renders inert; Security findings, high and medium, per KLOC |
| Data protection | +0.02 | +0.01 | +0.03 | +0.01 | Data protection, 1-5; Data-protection probe pass rate, of three |
| Design | +0.00 | +0.01 | +0.05 | +0.11 | Design (SOLID and patterns), 1-5; SRP, 1-5; OCP, 1-5; LSP, 1-5; ISP, 1-5; DIP, 1-5; Error design, 1-5; Naming and abstraction, 1-5; Patterns missed; Domain modules reaching Flask or the database; Mutually importing module pairs |
| Maintainability | +0.04 | +0.20 | +0.28 | +0.27 | Maintainability, 1-5; Readability, 1-5; Type errors under --strict, per KLOC; Lint findings per KLOC; Highest cognitive complexity; Functions over complexity 15, per KLOC; Mean cyclomatic complexity; Unused names per KLOC |
| Tests | +0.20 | +0.02 | +0.31 | +0.65 | Test quality, 1-5; Line coverage of the trial's own tests, % |
| Economy | -0.27 | -0.42 | -0.51 | -0.56 | Cost, USD; Turns |

## Each arm against `none`, post-hoc

- `reference`: Reliability unsettled; Security better; Data protection held; Design
  better; Maintainability better; Tests better; Economy worse
- `skills`: Reliability unsettled; Security better; Data protection held; Design better;
  Maintainability better; Tests better; Economy worse
- `hybrid`: Reliability unsettled; Security better; Data protection held; Design better;
  Maintainability better; Tests better; Economy worse
- `inline`: Reliability unsettled; Security better; Data protection held; Design better;
  Maintainability better; Tests better; Economy worse

## The round's questions, read post-hoc

A row is better or worse only where its whole interval lies past its margin. Task
success and the probes are read on working builds: those that install and boot.
Reliability can refute a hypothesis and never has to hold for one.

| Arm | Working builds | 95 % exact interval |
| --- | --- | --- |
| none | 15 of 15 | 0.78 to 1.00 |
| hybrid | 15 of 15 | 0.78 to 1.00 |
| reference | 13 of 15 | 0.60 to 0.98 |
| inline | 15 of 15 | 0.78 to 1.00 |
| skills | 15 of 15 | 0.78 to 1.00 |

- H1, skills deliver what hybrid does, skills-hybrid: inconclusive, robust (task success
  held, security probes open, data-protection probes held, security held, data
  protection held, reliability open)
  - profile: Reliability unsettled; Security unsettled; Data protection held; Design
worse; Maintainability worse; Tests worse; Economy held
- H3, a reference alone delivers less, reference-hybrid: inconclusive, robust (task
  success open, security probes open, data-protection probes held, security held, data
  protection held, reliability open)
  - profile: Reliability unsettled; Security worse; Data protection held; Design worse;
Maintainability worse; Tests worse; Economy better

## The numbers behind it, post-hoc

Each cell reads by the later rules, on working builds where the row says so. Each cell:
the mean paired difference, its 95 % interval in brackets, and a mark. ▲ better and ▼
worse: the interval is clear of zero, in the metric's direction, and under round 5d's
rules clear of the row's margin. = held, for a row read by its margin, and ≈ no
difference shown: either way the interval's worse end stays within the row's margin, so
it is no worse than the margin, which is not the same as equal. ○ no verdict, on
purpose: a row reported without one, a pair across rounds, or two judges that disagree.
(not compared): too few complete pairs for an interval. No mark: no difference shown, on
a row with no margin or past the margin it has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate-posthoc.json` carries the method per row.

### The rows the questions decide on

| Metric | Direction | Margin | hybrid | reference | skills | skills−hybrid | reference−hybrid |
|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 2 pp | 0.991 | 0.976 | 0.992 | +0.001 [-0.002, 0.003] = | -0.016 [-0.086, 0.003] (13 pairs) |
| Security probe pass rate, of eleven | up | 2 pp | 0.897 | 0.888 | 0.897 | 0 [-0.036, 0.036] | -0.014 [-0.056, 0.021] (13 pairs) |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.667 | 0.667 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 pairs) |
| Security, 1-5 | up | 0.3 points | 2.711 | 3.511 | 3.556 | +0.844 [0.200, 1.533] = | +0.800 [0.178, 1.422] = |
| Data protection, 1-5 | up | 0.3 points | 3.111 | 3.089 | 3.089 | -0.022 [-0.178, 0.067] = | -0.022 [-0.178, 0.089] = |
| Installs and boots | up | 6.7 pp | 1 | 0.867 | 1 | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ |

### Reliability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Installs and boots | up | 6.7 pp | 1 | 1 | 0.867 | 1 | 1 | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ |
| Task success, hidden suite pass rate | up | 2 pp | 0.992 | 0.991 | 0.976 | 0.992 | 0.992 | -0.001 [-0.003, 0.001] = | -0.016 [-0.087, 0.002] (13 pairs) | -0.000 [-0.004, 0.002] = | -0.000 [-0.003, 0.002] = |

### Security

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Security, 1-5 | up | 0.3 points | 2.378 | 2.711 | 3.511 | 3.267 | 3.556 | +0.333 [-0.489, 1.133] | +1.133 [0.578, 1.600] ▲ | +0.889 [-0.022, 1.756] = | +1.178 [0.600, 1.711] ▲ |
| Security probe pass rate, of eleven | up | 2 pp | 0.758 | 0.897 | 0.888 | 0.909 | 0.897 | +0.139 [0.091, 0.176] ▲ | +0.133 [0.091, 0.161] ▲ (13 pairs) | +0.151 [0.109, 0.200] ▲ | +0.139 [0.085, 0.182] ▲ |
| A post without a token is refused | up | — | 0.200 | 0.867 | 0.400 | 0.733 | 0.667 | +0.667 [0.133, 0.867] ▲ | +0.200 [-0.133, 0.400] | +0.533 [0.067, 0.733] ▲ | +0.467 [0, 0.667] = |
| Stored payload renders inert | up | — | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Security findings, high and medium, per KLOC | down | 10 % relative | 0.071 | 0.185 | 0.263 | 0.159 | 0.235 | +0.113 [-0.032, 0.224] | +0.191 [-0.025, 0.587] | +0.088 [-0.055, 0.231] | +0.163 [-0.003, 0.332] |

### Data protection

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Data protection, 1-5 | up | 0.3 points | 2.867 | 3.111 | 3.089 | 3.044 | 3.089 | +0.244 [0.067, 0.667] = | +0.222 [0.044, 0.711] = | +0.178 [0.022, 0.600] = | +0.222 [0.022, 0.756] = |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.667 | 0.667 | 0.689 | 0.667 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 pairs) | +0.022 [0, 0.067] = | 0 [0, 0] ‡ = |

### Design

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 0.3 points | 3 | 3 | 2.978 | 3 | 3 | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| SRP, 1-5 | up | — | 2.822 | 3.356 | 2.978 | 3.822 | 3.156 | +0.533 [0.289, 0.733] ▲ | +0.156 [0.044, 0.311] ▲ | +1 [0.756, 1.156] ▲ | +0.333 [0.133, 0.533] ▲ |
| OCP, 1-5 | up | — | 2 | 2 | 2 | 2 | 2 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| LSP, 1-5 | up | — | 2.711 | 2.933 | 2.822 | 3.356 | 2.867 | +0.222 [-0.111, 0.556] | +0.111 [-0.467, 0.489] | +0.644 [0.267, 1.000] ▲ | +0.156 [-0.467, 0.600] |
| ISP, 1-5 | up | — | 4.067 | 4.133 | 4.067 | 3.933 | 4.200 | +0.067 [-0.111, 0.311] | 0 [-0.133, 0.200] | -0.133 [-0.333, 0.022] | +0.133 [0, 0.333] = |
| DIP, 1-5 | up | — | 5 | 5 | 5 | 5 | 5 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Error design, 1-5 | up | — | 2.111 | 2.422 | 2.400 | 2.578 | 2.289 | +0.311 [0.111, 0.489] ▲ | +0.289 [-0.044, 0.556] | +0.467 [0.200, 0.667] ▲ | +0.178 [0, 0.400] = |
| Naming and abstraction, 1-5 | up | — | 4 | 4 | 3.978 | 4 | 4 | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Patterns missed | down | — | 1.467 | 1.511 | 1.467 | 1.289 | 1.489 | +0.044 [-0.244, 0.311] | 0 [-0.333, 0.311] | -0.178 [-0.444, 0.111] | +0.022 [-0.267, 0.311] |
| Domain modules reaching Flask or the database | down | — | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Mutually importing module pairs | down | — | 0.800 | 0 | 0.400 | 0.467 | 0.533 | -0.800 [-3.200, -0.400] ▲ | -0.400 [-2.400, 0.400] | -0.333 [-2, 0.867] | -0.267 [-1.933, 0.933] |

### Maintainability

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Maintainability, 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 3 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Readability, 1-5 | up | 0.3 points | 2.933 | 3.067 | 3 | 3.044 | 3.111 | +0.133 [0.022, 0.333] = | +0.067 [0, 0.200] = | +0.111 [0, 0.311] = | +0.178 [0.022, 0.622] = |
| Type errors under --strict, per KLOC | down | 10 % relative | 99.122 | 3.577 | 63.085 | 3.563 | 3.563 | -95.545 [-124.763, -77.443] ▲ | -36.037 [-61.311, -8.503] = | -95.559 [-122.765, -77.119] ▲ | -95.559 [-125.339, -77.929] ▲ |
| Lint findings per KLOC | down | 10 % relative | 238.933 | 137.248 | 194.367 | 141.366 | 151.198 | -101.685 [-127.942, -79.340] ▲ | -44.567 [-61.823, -20.134] = | -97.567 [-122.055, -71.830] ▲ | -87.735 [-109.987, -66.191] ▲ |
| Highest cognitive complexity | down | — | 72.200 | 19.800 | 35.133 | 18.667 | 28.400 | -52.400 [-85, -30.467] ▲ | -37.067 [-69.467, -14.867] ▲ | -53.533 [-86.867, -32.400] ▲ | -43.800 [-79.467, -18.400] ▲ |
| Functions over complexity 15, per KLOC | down | 10 % relative | 1.439 | 0.401 | 1.156 | 0.399 | 0.681 | -1.039 [-1.315, -0.749] ▲ | -0.283 [-0.729, 0.212] | -1.041 [-1.277, -0.818] ▲ | -0.759 [-1.123, -0.288] ▲ |
| Mean cyclomatic complexity | down | — | 3.305 | 2.786 | 3.053 | 2.761 | 2.854 | -0.519 [-0.635, -0.367] ▲ | -0.251 [-0.370, -0.125] ▲ | -0.544 [-0.677, -0.429] ▲ | -0.451 [-0.591, -0.281] ▲ |
| Unused names per KLOC | down | 10 % relative | 13.317 | 7.840 | 11.686 | 9.677 | 12.766 | -5.477 [-7.284, -3.152] ▲ | -1.631 [-4.167, 1.258] = | -3.640 [-5.768, -1.611] ▲ | -0.551 [-3.097, 2.128] |

### Tests

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Test quality, 1-5 | up | — | 3.089 | 3.533 | 3.622 | 3.911 | 3.267 | +0.444 [0.089, 0.667] ▲ | +0.533 [0.267, 0.733] ▲ | +0.822 [0.578, 0.933] ▲ | +0.178 [0.044, 0.356] ▲ |
| Line coverage of the trial's own tests, % | up | — | 72.685 | 93.036 | 86.951 | 95.080 | 81.984 | +22.231 [10.510, 33.969] ▲ (8 pairs) | +15.504 [2.773, 26.389] ▲ (14 pairs) | +23.620 [14.567, 32.337] ▲ (14 pairs) | +9.298 [-5.289, 22.514] |

### Economy

| Metric | Direction | Margin | none | hybrid | reference | inline | skills | hybrid−none | reference−none | inline−none | skills−none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cost, USD | down | 25 % relative | 4.294 | 11.783 | 7.208 | 14.184 | 9.302 | +7.489 [6.550, 8.636] ▼ | +2.915 [2.325, 3.736] ▼ | +9.890 [8.326, 12.227] ▼ | +5.009 [4.024, 6.242] ▼ |
| Turns | down | 25 % relative | 93.867 | 197.667 | 139 | 197.800 | 168 | +103.800 [57.267, 122.667] ▼ | +45.133 [36, 59.200] ▼ | +103.933 [56.267, 131] ▼ | +74.133 [59.867, 91.733] ▼ |
