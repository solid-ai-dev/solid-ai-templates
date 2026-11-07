# Efficacy benchmark — 2026-11-07, full record

Every number behind [the report](2026-11-07-efficacy.md) and its [technical
appendix](2026-11-07-efficacy-appendix.md), trial by trial.

Does a generated context file improve the result? The question, the verdict rule and the
metric directions were fixed before any trial ran, in the solid-ai-benchmark repository.

Each interval below is a 95 % bootstrap interval over the paired differences of its
contrast, one per block that measured both arms: K = 15 at most, and a cell that had
fewer names its count.

## Executive summary

![Radar per arm](2026-11-07-efficacy-radar-dark.svg#gh-dark-mode-only)
![Radar per arm](2026-11-07-efficacy-radar-light.svg#gh-light-mode-only)

One radar per arm, from the cheapest to the dearest. Each axis is the mean of its rows'
moves against `none`: each row's interval bound nearest zero over the row's full scale,
from -1 at the centre to +1 at the rim, and 0 where the interval crosses zero. A row's
full scale is 1 point for a judge score, 20 pp for a share, 20 points for coverage, and
a factor of 4 for a count or a cost, so a reader can work any axis out from the
intervals below. The dashed ring is `none`, so outside it is better. A hollow point is
an axis with no verdict. The rows behind each axis, and every number, are in the
sections below.

## Arms against `none`

| Axis | `reference` | `short` | `hand` | `skills` | `hybrid` | `inline` | Rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Reliability | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | Installs and boots; Task success, hidden suite pass rate |
| Security | +0.21 | +0.03 | 0.00 | +0.20 | +0.22 | +0.18 | Security, 1-5; Security probe pass rate, of eleven; A post without a token is refused; Stored payload renders inert; Security findings, high and medium, per KLOC |
| Data protection | +0.02 | 0.00 | 0.00 | +0.01 | +0.03 | +0.01 | Data protection, 1-5; Data-protection probe pass rate, of three |
| Design | +0.00 | +0.01 | +0.04 | +0.01 | +0.05 | +0.11 | Design (SOLID and patterns), 1-5; SRP, 1-5; OCP, 1-5; LSP, 1-5; ISP, 1-5; DIP, 1-5; Error design, 1-5; Naming and abstraction, 1-5; Patterns missed; Modules import tariff loads that reach Flask or the database; Mutually importing module pairs |
| Maintainability | +0.04 | +0.16 | +0.17 | +0.20 | +0.28 | +0.27 | Maintainability, 1-5; Readability, 1-5; Type errors under --strict, per KLOC; Lint findings per KLOC; Highest cognitive complexity; Functions over complexity 15, per KLOC; Mean cyclomatic complexity; Unused names per KLOC |
| Tests | +0.20 | 0.00 | +0.17 | +0.02 | +0.31 | +0.65 | Test quality, 1-5; Line coverage of the trial's own tests, % |
| Economy | -0.27 | -0.27 | -0.30 | -0.42 | -0.51 | -0.56 | Cost, USD; Turns |

| Arm | File | Verdict vs `none` | Hidden tests passed | Security, judge 1–5 | Adherence | Cost per trial |
| --- | --- | --- | --- | --- | --- | --- |
| `none` | no file | — | 99 % | 2.4 | 47 % | $4.29 |
| `reference` | 19 lines | Yes | 98 % (1 run low) | 3.5 ▲ | 54 % ○ | $7.21 ▼ |
| `short` | 40 lines | Yes | 99 % = | 3.1 = | 58 % ○ | $8.06 ▼ |
| `hand` | 39 lines | No | 99 % = | 2.6 | 60 % ○ | $8.28 ▼ |
| `skills` | 1,351 lines | Yes | 99 % = | 3.6 ▲ | 60 % ○ | $9.30 ▼ |
| `hybrid` | 511 lines | Yes | 99 % = | 2.7 | 56 % ○ | $11.78 ▼ |
| `inline` | 552 lines | Yes | 99 % = | 3.3 = | 63 % ○ | $14.18 ▼ |

Each mark reads an arm against `none`. ▲ better and ▼ worse: the interval is clear of
zero, in the metric's direction, and under round 5d's rules clear of the row's margin. =
held, for a row read by its margin, and ≈ no difference shown: either way the interval's
worse end stays within the row's margin, so it is no worse than the margin, which is not
the same as equal. ○ no verdict, on purpose: a row reported without one, a pair across
rounds, or two judges that disagree. (not compared): too few complete pairs for an
interval. No mark: no difference shown, on a row with no margin or past the margin it
has.

Runs low on the hidden tests, more than 5 points under `none`'s mean: `reference` 77 %.

**`reference`, Yes.** Two runs of 15 declared its dependencies so that a clean install
left the app unable to boot. A few rules the agent could hold: the judge read its code
as more secure and better tested, and its code grew no more than its size margin allows
— for more turns and cost.

**`short`, Yes.** The judge saw none of it as better design, readability,
maintainability, security or data protection.

**`hand`, No.** It built more than the task asked for: more public names beyond the
spec, and took more turns, time and cost to do it. The judge read its code as better
tested.

**`skills`, Yes.** The judge read its code as more secure and better tested, and its
code grew no more than its size margin allows — for more turns, time and cost.

**`hybrid`, Yes.** It built more than the task asked for: more files and more code, and
took more turns, time and cost to do it. The judge read its code as better tested.

**`inline`, Yes.** It built more than the task asked for: more files, more code and more
public names beyond the spec, and took more turns, time and cost to do it. The judge
read its code as better tested.

Reused from an earlier round: none (15 trials), hybrid (15 trials), reference (15
trials), inline (15 trials) and skills (15 trials). Compared unpaired with this round's
trials, as round 5d registered: short − none, hand − none, inline − hand, hybrid − hand,
reference − hand, skills − hand and short − inline. The model is pinned by exact id; the
day is the residual confound.

Together, reading the longest file beside the shortest (`skills`, `reference`): a
context file adds quality, long or short. K = 15, one project: a signal, not proof.

Between the files, 1 to 10: short − hand 3.6 (2 won, 5 failed); skills − hybrid 2.8 (1
won, 4 failed); reference − hybrid 1.7 (1 won, 12 failed); skills − inline 3.2 (2 won, 6
failed); inline − hand 6.6 (10 won, 6 failed); hybrid − hand 6.7 (7 won, 4 failed);
reference − hand 2.6 (2 won, 9 failed); skills − hand 5.5 (3 won, 3 failed); short −
inline 3.2 (4 won, 12 failed). A win or a fail is a metric whose interval separated the
pair in its declared direction, each counting once; the score is 1 + 9 × wins ÷ (wins +
fails), digests the verdict vector at the end, and decides nothing.

Caveats: 105 trials, 105 judged; reused from an earlier round: none, hybrid, reference,
inline and skills; 15 of the 15 registered blocks complete; withdrawn: nothing; lost and
re-run: hand-5, blocked; hand-5, completed; hand-9, completed; hand-12, completed;
hand-15, completed; reached past their workspace: none; the judge is checked only by its
evidence lines.

## What produced these numbers

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

## Primary dimensions

The report leads with these, declared by the owner before the run: five judge rows and
two probe pass rates. Task success and cost follow.

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | short−hand | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline | inline−hand | hybrid−hand | reference−hand | skills−hand | short−inline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 2.978 | 3 | 3 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Readability, 1-5 | up | 0.3 points | 2.933 | 3 | 3.067 | 3 | 3 | 3.044 | 3.111 | +0.067 [0, 0.200] = | +0.133 [0.022, 0.333] = | +0.067 [0, 0.200] = | 0 [0, 0] ‡ = | +0.067 [0, 0.200] = | +0.111 [0, 0.311] = | +0.178 [0.022, 0.622] = | +0.044 [-0.111, 0.244] = | -0.067 [-0.244, -0.022] = | +0.067 [-0.089, 0.244] = | +0.044 [0, 0.133] = | +0.067 [0, 0.178] = | 0 [0, 0] ‡ = | +0.111 [0.022, 0.311] = | -0.044 [-0.311, 0] |
| Maintainability, 1-5 | up | 0.3 points | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Security, 1-5 | up | 0.3 points | 2.378 | 3.089 | 2.711 | 2.600 | 3.511 | 3.267 | 3.556 | +0.711 [-0.178, 1.511] = | +0.333 [-0.489, 1.133] | +0.222 [-0.644, 1.044] | +0.489 [-0.400, 1.400] | +1.133 [0.578, 1.600] ▲ | +0.889 [-0.022, 1.756] = | +1.178 [0.600, 1.711] ▲ | +0.844 [0.200, 1.533] = | +0.800 [0.178, 1.422] = | +0.289 [-0.156, 0.889] = | +0.667 [-0.156, 1.444] = | +0.111 [-0.733, 0.911] | +0.911 [0.200, 1.578] = | +0.956 [0.311, 1.622] ▲ | -0.178 [-1.022, 0.556] |
| Data protection, 1-5 | up | 0.3 points | 2.867 | 3.022 | 3.111 | 2.978 | 3.089 | 3.044 | 3.089 | +0.156 [0, 0.578] = | +0.244 [0.067, 0.667] = | +0.111 [-0.311, 0.467] | +0.044 [-0.156, 0.511] = | +0.222 [0.044, 0.711] = | +0.178 [0.022, 0.600] = | +0.222 [0.022, 0.756] = | -0.022 [-0.178, 0.067] = | -0.022 [-0.178, 0.089] = | +0.044 [-0.044, 0.156] = | +0.067 [-0.133, 0.533] = | +0.133 [-0.067, 0.622] = | +0.111 [-0.089, 0.622] = | +0.111 [-0.089, 0.622] = | -0.022 [-0.089, 0.044] = |
| Security probe pass rate, of eleven | up | 2 pp | 0.758 | 0.824 | 0.897 | 0.776 | 0.888 | 0.909 | 0.897 | +0.067 [0.030, 0.109] ▲ | +0.139 [0.091, 0.176] ▲ | +0.018 [-0.036, 0.055] | +0.049 [-0.000, 0.103] = | +0.133 [0.091, 0.161] ▲ (13 pairs) | +0.151 [0.109, 0.200] ▲ | +0.139 [0.085, 0.182] ▲ | 0 [-0.036, 0.036] | -0.014 [-0.056, 0.021] (13 pairs) | -0.012 [-0.067, 0.042] | +0.133 [0.091, 0.182] ▲ | +0.121 [0.079, 0.170] ▲ | +0.112 [0.067, 0.158] ▲ (13 against 15 trials) | +0.121 [0.073, 0.176] ▲ | -0.085 [-0.121, -0.048] ▼ |
| Data-protection probe pass rate, of three | up | 10 pp | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.689 | 0.667 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 pairs) | +0.022 [0, 0.067] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 pairs) | -0.022 [-0.133, 0] | +0.022 [0, 0.067] = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = (13 against 15 trials) | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] |

Each cell: the mean paired difference, its 95 % interval in brackets, and a mark. ▲
better and ▼ worse: the interval is clear of zero, in the metric's direction, and under
round 5d's rules clear of the row's margin. = held, for a row read by its margin, and ≈
no difference shown: either way the interval's worse end stays within the row's margin,
so it is no worse than the margin, which is not the same as equal. ○ no verdict, on
purpose: a row reported without one, a pair across rounds, or two judges that disagree.
(not compared): too few complete pairs for an interval. No mark: no difference shown, on
a row with no margin or past the margin it has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## Runs per arm

Fixed before the run: the round runs K = 15 blocks, sized from the noise of the rounds
before it, and adds none once results are seen.

**Complete.** Every registered arm has its trial in all 15 blocks.

## Task success, adherence and cost

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | short−hand | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline | inline−hand | hybrid−hand | reference−hand | skills−hand | short−inline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Task success, hidden suite pass rate | up | 2 pp | 0.992 | 0.991 | 0.991 | 0.991 | 0.976 | 0.992 | 0.992 | -0.001 [-0.003, 0.001] = | -0.001 [-0.003, 0.001] = | -0.001 [-0.003, 0.001] = | -0.000 [-0.002, 0.002] = | -0.016 [-0.087, 0.002] (13 pairs) | -0.000 [-0.004, 0.002] = | -0.000 [-0.003, 0.002] = | +0.001 [-0.002, 0.003] = | -0.016 [-0.086, 0.003] (13 pairs) | -0.000 [-0.002, 0.002] = | +0.001 [-0.002, 0.003] = | -0.000 [-0.002, 0.002] = | -0.015 [-0.085, 0.003] (13 against 15 trials) | +0.001 [-0.002, 0.002] = | -0.001 [-0.004, 0.002] = |
| Installs in a clean environment | up | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Adherence checklist fraction | neutral | 8 pp | 0.472 | 0.578 | 0.561 | 0.600 | 0.537 | 0.628 | 0.603 | +0.105 [0.033, 0.161] ○ | +0.089 [0.029, 0.137] ○ | +0.128 [0.061, 0.183] ○ | -0.022 [-0.117, 0.044] ○ | +0.065 [0.021, 0.097] ○ | +0.156 [0.100, 0.225] ○ | +0.131 [0.070, 0.177] ○ | +0.041 [-0.007, 0.122] ○ | -0.025 [-0.077, 0.027] ○ | -0.025 [-0.076, 0.048] ○ | +0.028 [-0.048, 0.103] ○ | -0.038 [-0.107, 0.025] ○ | -0.063 [-0.124, -0.006] ○ | +0.003 [-0.061, 0.067] ○ | -0.051 [-0.129, 0.021] ○ |
| Output tokens | down | 25 % relative | 122963.7 | 140661.9 | 169072 | 141237.9 | 154568.3 | 174413.5 | 159560.5 | +17698.1 [-18313.1, 30754.0] | +46108.3 [1924.3, 61839.9] | +18274.2 [-15724.4, 32153.7] | -576.067 [-34637.8, 28069.5] = | +31604.5 [21863.9, 41453.1] | +51449.8 [4796.9, 75872.1] | +36596.8 [25594, 47760.1] | -9511.5 [-27232.8, 35968.6] = | -14503.7 [-32657.6, 31463.9] = | -14853 [-40360.1, 34141.9] = | +33175.6 [-13632, 67422.5] | +27834.1 [-8404.7, 56550.9] | +13330.3 [-1818.3, 48614.9] | +18322.6 [2875.7, 53841.5] | -33751.7 [-67293.7, 12723.3] = |
| Turns | down | 25 % relative | 93.867 | 154 | 197.667 | 157.267 | 139 | 197.800 | 168 | +60.133 [24.067, 77.933] ▼ | +103.800 [57.267, 122.667] ▼ | +63.400 [26.800, 78.533] ▼ | -3.267 [-33.267, 35.667] = | +45.133 [36, 59.200] ▼ | +103.933 [56.267, 131] ▼ | +74.133 [59.867, 91.733] ▼ | -29.667 [-56.267, 26.800] = | -58.667 [-78.200, -14.333] = | -29.800 [-59.600, 15.800] = | +40.533 [-10.267, 79.333] | +40.400 [-2.067, 73.067] | -18.267 [-35.133, 19.133] = | +10.733 [-10.200, 48.467] | -43.800 [-83.400, 5.800] = |
| Wall time, seconds | down | 25 % relative | 1358.3 | 2002.9 | 2394.8 | 2062.5 | 1815.1 | 2793.4 | 1906.1 | +644.647 [474.767, 821.893] ▼ | +1036.6 [867, 1225.1] ▼ | +704.207 [535.807, 999.560] ▼ | -59.560 [-300.107, 164.853] = | +456.820 [333.520, 619.213] | +1435.1 [1195.5, 1837.6] ▼ | +547.793 [382.420, 723.820] ▼ | -488.760 [-716.907, -209.180] = | -579.733 [-740.780, -342.327] = | -887.353 [-1248.8, -591.920] = | +730.940 [400.040, 1122.7] | +332.347 [5.007, 569.113] | -247.387 [-556.407, -47.367] = | -156.413 [-470.513, 63.347] = | -790.500 [-1199.5, -501.287] = |
| Cost, USD | down | 25 % relative | 4.294 | 8.061 | 11.783 | 8.284 | 7.208 | 14.184 | 9.302 | +3.767 [3.011, 4.445] ▼ | +7.489 [6.550, 8.636] ▼ | +3.990 [3.285, 4.627] ▼ | -0.223 [-1.249, 0.849] = | +2.915 [2.325, 3.736] ▼ | +9.890 [8.326, 12.227] ▼ | +5.009 [4.024, 6.242] ▼ | -2.480 [-3.775, -0.842] = | -4.574 [-5.804, -3.393] ▲ | -4.881 [-7.301, -2.864] = | +5.900 [4.279, 8.121] ▼ | +3.499 [2.309, 4.826] ▼ | -1.076 [-1.894, -0.149] = | +1.018 [-0.135, 2.317] | -6.123 [-8.420, -4.474] ▲ |

Each cell: the mean paired difference, its 95 % interval in brackets, and a mark. ▲
better and ▼ worse: the interval is clear of zero, in the metric's direction, and under
round 5d's rules clear of the row's margin. = held, for a row read by its margin, and ≈
no difference shown: either way the interval's worse end stays within the row's margin,
so it is no worse than the margin, which is not the same as equal. ○ no verdict, on
purpose: a row reported without one, a pair across rounds, or two judges that disagree.
(not compared): too few complete pairs for an interval. No mark: no difference shown, on
a row with no margin or past the margin it has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## The change task

How far each design had to be disturbed to take a change it was not built for, read
beside whether the change works and whether the build still passes after it.

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | short−hand | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline | inline−hand | hybrid−hand | reference−hand | skills−hand | short−inline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Change task, acceptance pass rate | up | — | — | — | — | — | — | — | — | an arm has no measured trial | no complete pair was measured | an arm has no measured trial | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial |
| Change task, build suite pass rate after it | up | — | — | — | — | — | — | — | — | an arm has no measured trial | no complete pair was measured | an arm has no measured trial | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial |
| Change task, files touched | down | — | — | — | — | — | — | — | — | an arm has no measured trial | no complete pair was measured | an arm has no measured trial | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial |
| Change task, lines changed | down | — | — | — | — | — | — | — | — | an arm has no measured trial | no complete pair was measured | an arm has no measured trial | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial |
| Change task, cost, USD | down | — | — | — | — | — | — | — | — | an arm has no measured trial | no complete pair was measured | an arm has no measured trial | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | no complete pair was measured | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial | an arm has no measured trial |

Each cell: the mean paired difference, its 95 % interval in brackets, and a mark. ▲
better and ▼ worse: the interval is clear of zero, in the metric's direction, and under
round 5d's rules clear of the row's margin. = held, for a row read by its margin, and ≈
no difference shown: either way the interval's worse end stays within the row's margin,
so it is no worse than the margin, which is not the same as equal. ○ no verdict, on
purpose: a row reported without one, a pair across rounds, or two judges that disagree.
(not compared): too few complete pairs for an interval. No mark: no difference shown, on
a row with no margin or past the margin it has.

## Every other metric

| Metric | Direction | Margin | none | short | hybrid | hand | reference | inline | skills | short−none | hybrid−none | hand−none | short−hand | reference−none | inline−none | skills−none | skills−hybrid | reference−hybrid | skills−inline | inline−hand | hybrid−hand | reference−hand | skills−hand | short−inline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Installs and boots | up | 6.7 pp | 1 | 1 | 1 | 1 | 0.867 | 1 | 1 | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ | -0.133 [-0.379, 0.092] ‡ | 0 [-0.204, 0.204] ‡ | 0 [-0.204, 0.204] ‡ |
| SRP, 1-5 | up | — | 2.822 | 3.022 | 3.356 | 3.178 | 2.978 | 3.822 | 3.156 | +0.200 [0.067, 0.400] ▲ | +0.533 [0.289, 0.733] ▲ | +0.356 [0.156, 0.622] ▲ | -0.156 [-0.400, -0.022] ▼ | +0.156 [0.044, 0.311] ▲ | +1 [0.756, 1.156] ▲ | +0.333 [0.133, 0.533] ▲ | -0.200 [-0.511, 0.133] | -0.378 [-0.622, -0.200] ▼ | -0.667 [-0.889, -0.378] ▼ | +0.644 [0.400, 0.844] ▲ | +0.178 [-0.089, 0.467] | -0.200 [-0.444, -0.089] ▼ | -0.022 [-0.222, 0.244] | -0.800 [-0.933, -0.622] ▼ |
| OCP, 1-5 | up | — | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| LSP, 1-5 | up | — | 2.711 | 2.822 | 2.933 | 2.889 | 2.822 | 3.356 | 2.867 | +0.111 [-0.378, 0.622] | +0.222 [-0.111, 0.556] | +0.178 [-0.267, 0.600] | -0.067 [-0.533, 0.422] | +0.111 [-0.467, 0.489] | +0.644 [0.267, 1.000] ▲ | +0.156 [-0.467, 0.600] | -0.067 [-0.778, 0.444] | -0.111 [-0.689, 0.267] | -0.489 [-1.000, 0.022] | +0.467 [0.067, 0.844] ▲ | +0.044 [-0.378, 0.533] | -0.067 [-0.400, 0.200] | -0.022 [-0.444, 0.378] | -0.533 [-0.978, -0.044] ▼ |
| ISP, 1-5 | up | — | 4.067 | 4.244 | 4.133 | 4.022 | 4.067 | 3.933 | 4.200 | +0.178 [-0.044, 0.422] | +0.067 [-0.111, 0.311] | -0.044 [-0.222, 0.022] | +0.222 [0.022, 0.444] ▲ | 0 [-0.133, 0.200] | -0.133 [-0.333, 0.022] | +0.133 [0, 0.333] = | +0.067 [-0.156, 0.267] | -0.067 [-0.311, 0.022] | +0.267 [0.044, 0.489] ▲ | -0.089 [-0.333, 0.044] | +0.111 [-0.044, 0.356] | +0.044 [-0.044, 0.244] | +0.178 [0.022, 0.400] ▲ | +0.311 [0.067, 0.600] ▲ |
| DIP, 1-5 | up | — | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Naming and abstraction, 1-5 | up | — | 4 | 3.978 | 4 | 4 | 3.978 | 4 | 4 | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.022 [-0.111, 0] | 0 [0, 0] ‡ = | -0.022 [-0.133, 0] |
| Error design, 1-5 | up | — | 2.111 | 2.044 | 2.422 | 2.689 | 2.400 | 2.578 | 2.289 | -0.067 [-0.267, 0.067] | +0.311 [0.111, 0.489] ▲ | +0.578 [0.289, 0.778] ▲ | -0.644 [-0.844, -0.422] ▼ | +0.289 [-0.044, 0.556] | +0.467 [0.200, 0.667] ▲ | +0.178 [0, 0.400] = | -0.133 [-0.400, 0.200] | -0.022 [-0.356, 0.289] | -0.289 [-0.600, 0.067] | -0.111 [-0.422, 0.178] | -0.267 [-0.533, 0] | -0.289 [-0.600, 0.022] | -0.400 [-0.689, -0.089] ▼ | -0.533 [-0.756, -0.289] ▼ |
| Test quality, 1-5 | up | — | 3.089 | 3.222 | 3.533 | 3.400 | 3.622 | 3.911 | 3.267 | +0.133 [-0.111, 0.333] | +0.444 [0.089, 0.667] ▲ | +0.311 [0.022, 0.511] ▲ | -0.178 [-0.467, 0.022] | +0.533 [0.267, 0.733] ▲ | +0.822 [0.578, 0.933] ▲ | +0.178 [0.044, 0.356] ▲ | -0.267 [-0.556, 0.022] | +0.089 [-0.244, 0.356] | -0.644 [-0.844, -0.467] ▼ | +0.511 [0.244, 0.711] ▲ | +0.133 [-0.200, 0.422] | +0.222 [-0.089, 0.489] | -0.133 [-0.422, 0.111] | -0.689 [-0.844, -0.422] ▼ |
| Patterns warranted | up | — | 4.822 | 4.778 | 4.489 | 4.533 | 4.622 | 5.111 | 4.733 | -0.044 [-0.578, 0.422] | -0.333 [-0.867, 0.133] | -0.289 [-0.778, 0.133] | +0.244 [-0.200, 0.578] | -0.200 [-0.733, 0.222] | +0.289 [-0.022, 0.644] | -0.089 [-0.578, 0.356] | +0.244 [-0.089, 0.467] | +0.133 [-0.244, 0.556] | -0.378 [-0.800, 0.067] | +0.578 [0.156, 0.956] ▲ | -0.044 [-0.400, 0.311] | +0.089 [-0.311, 0.467] | +0.200 [-0.178, 0.600] | -0.333 [-0.800, 0.111] |
| Patterns over-engineered | down | — | 0 | 0.089 | 0.044 | 0 | 0.067 | 0.044 | 0.022 | +0.089 [0, 0.178] | +0.044 [0, 0.133] | 0 [0, 0] ‡ = | +0.089 [0, 0.222] | +0.067 [0, 0.200] | +0.044 [0, 0.133] | +0.022 [0, 0.067] | -0.022 [-0.222, 0.022] | +0.022 [-0.133, 0.200] | -0.022 [-0.222, 0.022] | +0.044 [0, 0.133] | +0.044 [0, 0.133] | +0.067 [0, 0.200] | +0.022 [0, 0.067] | +0.044 [-0.133, 0.133] |
| Patterns missed | down | — | 1.467 | 1.444 | 1.511 | 1.489 | 1.467 | 1.289 | 1.489 | -0.022 [-0.289, 0.222] | +0.044 [-0.244, 0.311] | +0.022 [-0.244, 0.244] | -0.044 [-0.289, 0.133] | 0 [-0.333, 0.311] | -0.178 [-0.444, 0.111] | +0.022 [-0.267, 0.311] | -0.022 [-0.244, 0.267] | -0.044 [-0.244, 0.178] | +0.200 [-0.044, 0.400] | -0.200 [-0.422, 0.044] | +0.022 [-0.200, 0.267] | -0.022 [-0.289, 0.222] | 0 [-0.289, 0.244] | +0.156 [-0.089, 0.378] |
| Line coverage of the trial's own tests, % | up | — | 72.685 | 81.839 | 93.036 | 90.353 | 86.951 | 95.080 | 81.984 | +9.153 [-2.558, 19.951] | +22.231 [10.510, 33.969] ▲ (8 pairs) | +17.668 [6.430, 27.319] ▲ | -8.514 [-17.350, 1.070] | +15.504 [2.773, 26.389] ▲ (14 pairs) | +23.620 [14.567, 32.337] ▲ (14 pairs) | +9.298 [-5.289, 22.514] | -10.644 [-22.604, -2.969] ▼ (8 pairs) | -6.597 [-19.008, -1.289] ▼ (8 pairs) | -11.508 [-19.597, -6.397] ▼ (14 pairs) | +4.727 [0.278, 13.860] ▲ (14 against 15 trials) | +2.683 [-1.875, 11.817] (8 against 15 trials) | -3.402 [-10.417, 4.828] (14 against 15 trials) | -8.370 [-17.015, 1.333] | -13.242 [-22.064, -7.116] ▼ (15 against 14 trials) |
| Docstring coverage, % | up | — | 7.517 | 12.294 | 15.499 | 14.337 | 18.109 | 19.491 | 16.635 | +4.777 [0.253, 8.839] ▲ | +7.981 [4.481, 11.587] ▲ | +6.820 [3.417, 9.875] ▲ | -2.043 [-5.605, 1.491] | +10.591 [5.981, 14.741] ▲ | +11.974 [6.479, 16.991] ▲ | +9.117 [5.590, 12.740] ▲ | +1.136 [-3.565, 4.534] | +2.610 [-0.832, 6.107] | -2.857 [-8.906, 1.899] | +5.154 [0.785, 10.293] ▲ | +1.161 [-1.557, 3.685] | +3.771 [0.237, 8.137] ▲ | +2.297 [-1.891, 5.522] | -7.197 [-12.980, -2.039] ▼ |
| Lint findings per KLOC | down | 10 % relative | 238.933 | 146.964 | 137.248 | 139.602 | 194.367 | 141.366 | 151.198 | -91.969 [-119.671, -68.166] ▲ | -101.685 [-127.942, -79.340] ▲ | -99.331 [-127.208, -76.255] ▲ | +7.362 [-4.895, 18.856] | -44.567 [-61.823, -20.134] = | -97.567 [-122.055, -71.830] ▲ | -87.735 [-109.987, -66.191] ▲ | +13.950 [1.529, 25.051] | +57.119 [43.276, 76.955] ▼ | +9.832 [-7.860, 24.529] | +1.764 [-10.645, 13.629] = | -2.354 [-14.281, 9.872] = | +54.765 [37.386, 76.337] ▼ | +11.596 [-2.221, 25.045] | +5.598 [-6.323, 19.039] |
| Lint findings | down | — | 511.533 | 397.600 | 470.400 | 363.600 | 470.067 | 461.867 | 337.200 | -113.933 [-179.067, -51.533] ▲ | -41.133 [-113.533, 17.800] | -147.933 [-222.800, -72.200] ▲ | +34 [-39.600, 102] | -41.467 [-135.800, 50.333] | -49.667 [-122.133, 34.133] | -174.333 [-233.267, -132.867] ▲ | -133.200 [-182.533, -79] ▲ | -0.333 [-70.600, 117.933] | -124.667 [-195.533, -63.067] ▲ | +98.267 [13.933, 181.667] ▼ | +106.800 [35.267, 170.733] ▼ | +106.467 [23.533, 199.467] ▼ | -26.400 [-91.267, 32.200] | -64.267 [-140.933, 4.400] |
| Files the formatter would change | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Files the formatter would change, per KLOC | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Type errors under --strict | down | — | 220.533 | 17.600 | 13.800 | 42.200 | 157 | 14 | 10.067 | -202.933 [-285.933, -147.400] ▲ | -206.733 [-296, -154.667] ▲ | -178.333 [-262.667, -120.867] ▲ | -24.600 [-69.733, 5.733] | -63.533 [-162.467, 12] | -206.533 [-283.133, -155.467] ▲ | -210.467 [-301.600, -162.600] ▲ | -3.733 [-30.667, 6.133] | +143.200 [98.533, 233.533] ▼ | -3.933 [-22.133, 21.800] | -28.200 [-73.067, 3] | -28.400 [-72.267, 5.667] | +114.800 [57.733, 197.133] ▼ | -32.133 [-75.733, 0.600] | +3.600 [-17.400, 58] |
| Type errors under --strict, per KLOC | down | 10 % relative | 99.122 | 5.850 | 3.577 | 13.102 | 63.085 | 3.563 | 3.563 | -93.272 [-121.167, -73.096] ▲ | -95.545 [-124.763, -77.443] ▲ | -86.020 [-115.099, -65.947] ▲ | -7.252 [-20.741, 2.659] | -36.037 [-61.311, -8.503] = | -95.559 [-122.765, -77.119] ▲ | -95.559 [-125.339, -77.929] ▲ | -0.015 [-6.119, 2.715] | +59.508 [43.686, 91.907] ▼ | -0.001 [-4.978, 8.936] | -9.539 [-23.249, -0.267] = | -9.525 [-22.851, 0.571] = | +49.983 [30.906, 79.649] ▼ | -9.539 [-22.829, 1.029] = | +2.287 [-4.229, 20.571] |
| Security findings, high and medium | down | — | 0.133 | 0.400 | 0.733 | 0.067 | 0.600 | 0.533 | 0.533 | +0.267 [-0.067, 0.933] | +0.600 [0.133, 1.333] ▼ | -0.067 [-0.333, 0.067] | +0.333 [-0.067, 0.867] | +0.467 [0, 1.200] | +0.400 [0, 0.733] | +0.400 [0, 0.733] | -0.200 [-1.200, 0.267] | -0.133 [-1.267, 0.533] | 0 [-0.600, 0.467] | +0.467 [0.133, 0.733] ▼ | +0.667 [0.200, 1.600] ▼ | +0.533 [0.067, 1.267] ▼ | +0.467 [0.133, 0.733] ▼ | -0.133 [-0.600, 0.467] |
| Security findings, high and medium, per KLOC | down | 10 % relative | 0.071 | 0.166 | 0.185 | 0.030 | 0.263 | 0.159 | 0.235 | +0.095 [-0.057, 0.383] | +0.113 [-0.032, 0.224] | -0.041 [-0.183, 0.030] | +0.136 [-0.008, 0.430] | +0.191 [-0.025, 0.587] | +0.088 [-0.055, 0.231] | +0.163 [-0.003, 0.332] | +0.050 [-0.139, 0.238] | +0.078 [-0.179, 0.413] | +0.075 [-0.131, 0.269] | +0.129 [0.023, 0.267] ▼ | +0.155 [0.041, 0.373] ▼ | +0.233 [0.051, 0.595] ▼ | +0.205 [0.063, 0.360] ▼ | +0.007 [-0.155, 0.291] |
| Highest cognitive complexity | down | — | 72.200 | 40.600 | 19.800 | 29.533 | 35.133 | 18.667 | 28.400 | -31.600 [-63.333, -3.533] ▲ | -52.400 [-85, -30.467] ▲ | -42.667 [-75.200, -19.200] ▲ | +11.067 [-3.467, 36.400] | -37.067 [-69.467, -14.867] ▲ | -53.533 [-86.867, -32.400] ▲ | -43.800 [-79.467, -18.400] ▲ | +8.600 [1.067, 31.600] ▼ | +15.333 [9.933, 24.867] ▼ | +9.733 [2.333, 29.800] ▼ | -10.867 [-23.133, -3.867] ▲ | -9.733 [-22.200, -2.733] ▲ | +5.600 [-6.533, 15.933] | -1.133 [-12.867, 16.400] | +21.933 [11.733, 52] ▼ |
| Functions over complexity 15 | down | — | 3.067 | 2.867 | 1.400 | 1.867 | 2.667 | 1.333 | 1.467 | -0.200 [-0.933, 0.400] | -1.667 [-2.600, -1.067] ▲ | -1.200 [-2.067, -0.467] ▲ | +1 [0.267, 1.600] ▼ | -0.400 [-1.267, 0.533] | -1.733 [-2.533, -1.133] ▲ | -1.600 [-2.467, -0.733] ▲ | +0.067 [-0.800, 0.867] | +1.267 [0.400, 1.867] ▼ | +0.133 [-0.800, 1.067] | -0.533 [-1.400, 0.200] | -0.467 [-1.333, 0.200] | +0.800 [-0.067, 1.533] | -0.400 [-1.333, 0.400] | +1.533 [0.800, 2.200] ▼ |
| Functions over complexity 15, per KLOC | down | 10 % relative | 1.439 | 1.080 | 0.401 | 0.809 | 1.156 | 0.399 | 0.681 | -0.359 [-0.637, -0.047] = | -1.039 [-1.315, -0.749] ▲ | -0.630 [-0.981, -0.193] ▲ | +0.271 [-0.071, 0.598] | -0.283 [-0.729, 0.212] | -1.041 [-1.277, -0.818] ▲ | -0.759 [-1.123, -0.288] ▲ | +0.280 [-0.063, 0.627] | +0.755 [0.451, 1.061] ▼ | +0.282 [-0.065, 0.700] | -0.411 [-0.813, -0.094] ▲ | -0.409 [-0.802, -0.109] ▲ | +0.347 [-0.093, 0.731] | -0.129 [-0.573, 0.272] | +0.681 [0.425, 0.911] ▼ |
| Mean cyclomatic complexity | down | — | 3.305 | 3.007 | 2.786 | 2.877 | 3.053 | 2.761 | 2.854 | -0.298 [-0.451, -0.114] ▲ | -0.519 [-0.635, -0.367] ▲ | -0.427 [-0.575, -0.272] ▲ | +0.129 [0.013, 0.277] ▼ | -0.251 [-0.370, -0.125] ▲ | -0.544 [-0.677, -0.429] ▲ | -0.451 [-0.591, -0.281] ▲ | +0.068 [-0.023, 0.189] | +0.267 [0.154, 0.367] ▼ | +0.093 [0.010, 0.181] ▼ | -0.117 [-0.225, -0.013] ▲ | -0.091 [-0.175, -0.003] ▲ | +0.176 [0.055, 0.287] ▼ | -0.023 [-0.129, 0.095] | +0.246 [0.132, 0.387] ▼ |
| Lowest maintainability index | neutral | — | 17.171 | 20.346 | 21.104 | 22.335 | 20.101 | 23.639 | 23.306 | +3.175 [-0.352, 7.779] ○ | +3.933 [1.457, 6.241] ○ | +5.165 [2.563, 9.132] ○ | -1.989 [-4.464, 0.573] ○ | +2.931 [-4.166, 8.081] ○ | +6.469 [0.473, 11.479] ○ | +6.135 [3.079, 10.683] ○ | +2.202 [-1.015, 7.125] ○ | -1.003 [-7.622, 3.693] ○ | -0.333 [-3.087, 6.710] ○ | +1.304 [-3.414, 4.363] ○ | -1.231 [-5.635, 1.219] ○ | -2.234 [-7.021, 1.629] ○ | +0.971 [-1.289, 3.094] ○ | -3.293 [-7.241, 1.891] ○ |
| Unused names | down | — | 27.800 | 26.867 | 26.600 | 28.333 | 27.400 | 30.467 | 28.267 | -0.933 [-4.200, 2.333] | -1.200 [-5.200, 3.067] | +0.533 [-2.600, 3.600] | -1.467 [-5.600, 1.867] | -0.400 [-4.667, 2.933] | +2.667 [-1.467, 7.533] | +0.467 [-3.200, 4.467] | +1.667 [-2.333, 5.600] | +0.800 [-3.933, 5.133] | -2.200 [-8.800, 2] | +2.133 [-1.867, 6.533] | -1.733 [-5.333, 2.333] | -0.933 [-4.600, 2.400] | -0.067 [-3.600, 3.600] | -3.600 [-8.200, 0.467] |
| Unused names per KLOC | down | 10 % relative | 13.317 | 10.201 | 7.840 | 11.749 | 11.686 | 9.677 | 12.766 | -3.116 [-5.221, -0.875] = | -5.477 [-7.284, -3.152] ▲ | -1.567 [-4.043, 0.947] = | -1.549 [-3.879, 1.109] = | -1.631 [-4.167, 1.258] = | -3.640 [-5.768, -1.611] ▲ | -0.551 [-3.097, 2.128] | +4.926 [3.047, 6.868] ▼ | +3.846 [2.067, 5.727] ▼ | +3.089 [1.134, 4.972] ▼ | -2.073 [-4.178, 0.110] = | -3.909 [-5.800, -1.833] ▲ | -0.063 [-2.231, 2.324] | +1.017 [-1.135, 3.413] | +0.524 [-1.249, 2.364] |
| Extension axes present, of three | up | — | 0 | 0 | 0.267 | 0.267 | 0 | 0 | 0.133 | 0 [0, 0] ‡ = | +0.267 [0, 0.533] = | +0.267 [0, 0.533] = | -0.267 [-0.933, -0.133] ▼ | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | +0.133 [0, 0.400] = | -0.133 [-0.800, 0.133] | -0.267 [-1.067, -0.133] ▼ | +0.133 [0, 0.400] = | -0.267 [-1.200, -0.133] ▼ | 0 [-0.667, 0.400] | -0.267 [-1.200, -0.133] ▼ | -0.133 [-0.667, 0.133] | 0 [0, 0] ‡ = |
| Modules import tariff loads that reach Flask or the database | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Routes doing pricing arithmetic | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Boolean parameters | down | — | 1.733 | 0.600 | 0.800 | 0.800 | 0.800 | 1.533 | 0.600 | -1.133 [-2.733, -0.400] ▲ | -0.933 [-2.733, -0.133] ▲ | -0.933 [-2.400, 0.133] | -0.200 [-1.600, 0.267] | -0.933 [-2.800, -0.067] ▲ | -0.200 [-2.200, 0.733] | -1.133 [-2.400, -0.533] ▲ | -0.200 [-0.933, 0.400] | 0 [-0.933, 0.733] | -0.933 [-2.067, 0.200] | +0.733 [-0.333, 1.733] | 0 [-1.067, 0.667] | 0 [-1.133, 0.733] | -0.200 [-1.267, 0.533] | -0.933 [-1.933, -0.200] ▲ |
| Conditional ladders over rule kinds | down | — | 2.467 | 1.267 | 1.733 | 1.467 | 1.867 | 1.200 | 1.533 | -1.200 [-2.800, -0.133] ▲ | -0.733 [-2.200, 0.267] | -1 [-2.533, 0.067] | -0.200 [-0.867, 0.533] | -0.600 [-2.533, 0.333] | -1.267 [-3, -0.133] ▲ | -0.933 [-2.733, 0.067] | -0.200 [-0.933, 0.533] | +0.133 [-0.800, 0.933] | +0.333 [-0.467, 0.933] | -0.267 [-1.133, 0.667] | +0.267 [-0.467, 1] | +0.400 [-0.400, 1.133] | +0.067 [-0.667, 0.800] | +0.067 [-0.933, 0.867] |
| Public names beyond the specification | down | — | 5.867 | 5.267 | 8.800 | 7.867 | 7.067 | 9 | 6.933 | -0.600 [-2.267, 1.200] | +2.933 [-0.067, 5.467] | +2 [0.067, 3.733] ▼ | -2.600 [-4.267, -0.400] ▲ | +1.200 [-0.800, 2.867] | +3.133 [1.133, 4.733] ▼ | +1.067 [-0.933, 3] | -1.867 [-4.333, 0.933] | -1.733 [-3.533, 0.667] | -2.067 [-3.733, 0.467] | +1.133 [-0.800, 3.067] | +0.933 [-1.400, 3.200] | -0.800 [-2.533, 1] | -0.933 [-2.867, 1.133] | -3.733 [-5.400, -1.800] ▲ |
| Specified names missing | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Mutually importing module pairs | down | — | 0.800 | 1.267 | 0 | 0.867 | 0.400 | 0.467 | 0.533 | +0.467 [-1.200, 2.067] | -0.800 [-3.200, -0.400] ▲ | +0.067 [-1.600, 1.400] | +0.400 [-1.733, 2.067] | -0.400 [-2.400, 0.400] | -0.333 [-2, 0.867] | -0.267 [-1.933, 0.933] | +0.533 [0.067, 1.800] ▼ | +0.400 [0, 1.200] | +0.067 [-1.267, 1.067] | -0.400 [-2.133, 0.733] | -0.867 [-3.067, -0.400] ▲ | -0.467 [-2.267, 0.400] | -0.333 [-2.067, 0.800] | +0.800 [-0.600, 2.333] |
| Mean instability of domain modules | neutral | — | 0.433 | 0.397 | 0.384 | 0.370 | 0.400 | 0.375 | 0.380 | -0.036 [-0.067, -0.004] ○ | -0.049 [-0.088, -0.024] ○ | -0.063 [-0.103, -0.026] ○ | +0.027 [-0.015, 0.070] ○ | -0.033 [-0.068, 0.010] ○ | -0.059 [-0.087, -0.025] ○ | -0.053 [-0.088, -0.005] ○ | -0.004 [-0.050, 0.040] ○ | +0.016 [-0.027, 0.052] ○ | +0.006 [-0.031, 0.043] ○ | +0.005 [-0.031, 0.046] ○ | +0.014 [-0.028, 0.060] ○ | +0.030 [-0.015, 0.081] ○ | +0.010 [-0.032, 0.058] ○ | +0.022 [-0.009, 0.053] ○ |
| Stored payload renders inert | up | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| A post without a token is refused | up | — | 0.200 | 0.267 | 0.867 | 0.267 | 0.400 | 0.733 | 0.667 | +0.067 [-0.267, 0.267] | +0.667 [0.133, 0.867] ▲ | +0.067 [-0.267, 0.267] | 0 [-0.400, 0.267] | +0.200 [-0.133, 0.400] | +0.533 [0.067, 0.733] ▲ | +0.467 [0, 0.667] = | -0.200 [-0.600, 0.067] | -0.467 [-0.800, -0.200] ▼ | -0.067 [-0.467, 0.200] | +0.467 [0, 0.667] = | +0.600 [0.200, 0.800] ▲ | +0.133 [-0.200, 0.467] | +0.400 [-0.067, 0.667] | -0.467 [-0.733, -0.133] ▼ |
| Accessibility violations | down | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| HTML validity errors | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Invoice builder response size, bytes | down | — | 241 | 241 | 241 | 241 | 241 | 241.133 | 241 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | +0.133 [0, 0.400] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.133 [-0.800, 0] = | +0.133 [0, 0.400] | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | -0.133 [-0.800, 0] = |
| Invoice builder subrequests | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |
| Source lines | neutral | — | 2181.2 | 2704.6 | 3459.4 | 2575 | 2411.6 | 3269.5 | 2253.9 | +523.400 [217.467, 804] ○ | +1278.2 [931.333, 1611.1] ○ | +393.800 [20.800, 771.200] ○ | +129.600 [-313.800, 557.267] ○ | +230.400 [-123.267, 577.267] ○ | +1088.3 [642.200, 1511.9] ○ | +72.667 [-217.200, 406.333] ○ | -1205.5 [-1491, -853.867] ○ | -1047.8 [-1410.9, -598.133] ○ | -1015.6 [-1406.9, -694.467] ○ | +694.467 [192.467, 1187.4] ○ | +884.400 [437.533, 1269.3] ○ | -163.400 [-537.667, 241.867] ○ | -321.133 [-666.800, 33.867] ○ | -564.867 [-1023.3, -134.733] ○ |
| Files | neutral | — | 38.800 | 44.533 | 63.333 | 47.867 | 47.400 | 64.400 | 43.667 | +5.733 [2.800, 9] ○ | +24.533 [20.133, 27.267] ○ | +9.067 [5.867, 11.733] ○ | -3.333 [-6.933, 1] ○ | +8.600 [6.200, 12.133] ○ | +25.600 [22, 29.133] ○ | +4.867 [1.467, 8.133] ○ | -19.667 [-24.067, -15.467] ○ | -15.933 [-19.933, -12] ○ | -20.733 [-26, -16.733] ○ | +16.533 [13, 20.600] ○ | +15.467 [11.600, 19.333] ○ | -0.467 [-3.800, 3.467] ○ | -4.200 [-7.600, -0.467] ○ | -19.867 [-23.800, -15.867] ○ |
| App code, lines | down | 20 % relative | 2398.8 | 2688.1 | 3090.8 | 2549.6 | 2745.5 | 3206.3 | 2708.9 | +289.333 [163.067, 406.667] = | +692 [570.800, 783.600] ▼ | +150.800 [29, 264.267] = | +138.533 [14.733, 229.667] = | +346.667 [233.867, 465.133] = | +807.533 [661.333, 907.867] ▼ | +310.133 [193.533, 431] = | -381.867 [-489.467, -256.067] = | -345.333 [-454.200, -234.200] = | -497.400 [-633.067, -330.533] = | +656.733 [546.800, 762.267] ▼ | +541.200 [445.933, 642.667] | +195.867 [87.933, 304.600] = | +159.333 [38.467, 294.933] = | -518.200 [-630.733, -406.533] = |
| App code, files | down | 20 % relative | 30.600 | 33.800 | 41.200 | 33.267 | 34.733 | 42.133 | 33.467 | +3.200 [0.667, 5.400] = | +10.600 [8.200, 12.200] ▼ | +2.667 [0.267, 4.600] = | +0.533 [-2, 3.533] = | +4.133 [2.333, 5.867] = | +11.533 [9.333, 14] ▼ | +2.867 [-0.200, 5.667] = | -7.733 [-11.267, -4.867] = | -6.467 [-8.667, -4.667] = | -8.667 [-12.733, -5.400] = | +8.867 [6.533, 11.733] | +7.933 [5.667, 10.600] | +1.467 [-0.667, 3.667] = | +0.200 [-2.467, 2.800] = | -8.333 [-11.400, -5.867] = |
| Test code, lines | neutral | — | 833.533 | 920.600 | 1257.1 | 1157.3 | 926.333 | 1555.4 | 828.800 | +87.067 [5.267, 168.067] ○ | +423.600 [307.667, 523] ○ | +323.733 [219.400, 429.533] ○ | -236.667 [-350.533, -127.067] ○ | +92.800 [-17.667, 187.800] ○ | +721.867 [589.867, 852.667] ○ | -4.733 [-100.067, 79.267] ○ | -428.333 [-576.867, -297.133] ○ | -330.800 [-456.800, -219.800] ○ | -726.600 [-868.933, -597.067] ○ | +398.133 [260.600, 548] ○ | +99.867 [-28, 254.400] ○ | -230.933 [-344.467, -108.533] ○ | -328.467 [-438.733, -215.533] ○ | -634.800 [-772.733, -515.933] ○ |
| Artifacts nobody asked for | down | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = | 0 [0, 0] ‡ = |

Each cell: the mean paired difference, its 95 % interval in brackets, and a mark. ▲
better and ▼ worse: the interval is clear of zero, in the metric's direction, and under
round 5d's rules clear of the row's margin. = held, for a row read by its margin, and ≈
no difference shown: either way the interval's worse end stays within the row's margin,
so it is no worse than the margin, which is not the same as equal. ○ no verdict, on
purpose: a row reported without one, a pair across rounds, or two judges that disagree.
(not compared): too few complete pairs for an interval. No mark: no difference shown, on
a row with no margin or past the margin it has.

‡ the interval was not computed by BCa: the paired differences were identical, or the
bias correction was undefined. `aggregate.json` carries the method per row.

## Round 5d: a person's file and a 40-line file

A row is better or worse only where its whole interval lies past its margin. Task
success and the probes are read on working builds: those that install and boot.
Reliability can refute a hypothesis and never has to hold for one.

| Arm | Working builds | 95 % exact interval |
| --- | --- | --- |
| none | 15 of 15 | 0.78 to 1.00 |
| short | 15 of 15 | 0.78 to 1.00 |
| hybrid | 15 of 15 | 0.78 to 1.00 |
| hand | 15 of 15 | 0.78 to 1.00 |
| reference | 13 of 15 | 0.60 to 0.98 |
| inline | 15 of 15 | 0.78 to 1.00 |
| skills | 15 of 15 | 0.78 to 1.00 |

- H4, a file at all, hand-none: inconclusive, robust (task success held, security probes
  open, data-protection probes held, security open, data protection open, reliability
  open)
  - profile: Reliability unsettled; Security unsettled; Data protection unsettled;
Design better; Maintainability better; Tests better; Economy worse
- H5, inline against a person's file, inline-hand: supported, fragile (task success
  held, security probes better, data-protection probes held, security held, data
  protection held, reliability open)
  - profile: Reliability unsettled; Security better; Data protection held; Design
better; Maintainability better; Tests better; Economy worse
- H5, hybrid against a person's file, hybrid-hand: inconclusive, robust (task success
  held, security probes better, data-protection probes held, security open, data
  protection held, reliability open)
  - profile: Reliability unsettled; Security better; Data protection held; Design
better; Maintainability better; Tests unsettled; Economy worse
- H5, reference against a person's file, reference-hand: inconclusive, fragile (task
  success open, security probes better, data-protection probes held, security held, data
  protection held, reliability open)
  - profile: Reliability unsettled; Security better; Data protection held; Design worse;
Maintainability worse; Tests unsettled; Economy held
- H5, skills against a person's file, skills-hand: supported, robust (task success held,
  security probes better, data-protection probes held, security better, data protection
  held, reliability open)
  - profile: Reliability unsettled; Security better; Data protection held; Design worse;
Maintainability unsettled; Tests unsettled; Economy unsettled
- H6, the templates' content at a person's length, short-hand: inconclusive, fragile
  (task success held, security probes held, data-protection probes held, security open,
  data protection held, reliability open)
  - profile: Reliability unsettled; Security unsettled; Data protection held; Design
worse; Maintainability worse; Tests unsettled; Economy held

## Raw numbers, per trial

| Metric | none-1 | none-2 | none-3 | none-4 | none-5 | none-6 | none-7 | none-8 | none-9 | none-10 | none-11 | none-12 | none-13 | none-14 | none-15 | short-1 | short-2 | short-3 | short-4 | short-5 | short-6 | short-7 | short-8 | short-9 | short-10 | short-11 | short-12 | short-13 | short-14 | short-15 | hybrid-1 | hybrid-2 | hybrid-3 | hybrid-4 | hybrid-5 | hybrid-6 | hybrid-7 | hybrid-8 | hybrid-9 | hybrid-10 | hybrid-11 | hybrid-12 | hybrid-13 | hybrid-14 | hybrid-15 | hand-1 | hand-2 | hand-3 | hand-4 | hand-5 | hand-6 | hand-7 | hand-8 | hand-9 | hand-10 | hand-11 | hand-12 | hand-13 | hand-14 | hand-15 | reference-1 | reference-2 | reference-3 | reference-4 | reference-5 | reference-6 | reference-7 | reference-8 | reference-9 | reference-10 | reference-11 | reference-12 | reference-13 | reference-14 | reference-15 | inline-1 | inline-2 | inline-3 | inline-4 | inline-5 | inline-6 | inline-7 | inline-8 | inline-9 | inline-10 | inline-11 | inline-12 | inline-13 | inline-14 | inline-15 | skills-1 | skills-2 | skills-3 | skills-4 | skills-5 | skills-6 | skills-7 | skills-8 | skills-9 | skills-10 | skills-11 | skills-12 | skills-13 | skills-14 | skills-15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Design (SOLID and patterns), 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Readability, 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 4 | 3 | 3 | 3 |
| Maintainability, 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Security, 1-5 | 1 | 3 | 4 | 4 | 1.333 | 1 | 2.333 | 3 | 1 | 2 | 1 | 3 | 1.667 | 3.333 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 2 | 4 | 1.333 | 1 | 3 | 4 | 4 | 2 | 1 | 2.667 | 1 | 4 | 3.667 | 3 | 2 | 4 | 1 | 4 | 1 | 3.667 | 2 | 3 | 3.667 | 2 | 1 | 1 | 4 | 4 | 4 | 2.333 | 4 | 1 | 2 | 3.333 | 2.333 | 4 | 1 | 3 | 2 | 4 | 4 | 4 | 4 | 3.333 | 2 | 4 | 4 | 2.333 | 3 | 3.333 | 4 | 4 | 3.667 | 3 | 4 | 1 | 2.333 | 2.667 | 3.667 | 5 | 3.667 | 3.667 | 4 | 4 | 3 | 3.333 | 1.667 | 4 | 3 | 4 | 4 | 3.333 | 3.333 | 3 | 3.667 | 3.333 | 4 | 4 | 3 | 2.667 | 4 | 3 | 4 | 4 |
| Data protection, 1-5 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.667 | 3.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3.667 | 3 | 3.333 | 3 | 3 | 3.333 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3.333 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3.667 | 3 | 3 | 3 |
| Security probe pass rate, of eleven | 0.727 | 0.727 | 0.727 | 0.727 | 0.818 | 0.636 | 0.727 | 0.818 | 0.727 | 0.818 | 0.727 | 0.818 | 0.818 | 0.727 | 0.818 | 0.818 | 0.909 | 0.818 | 0.818 | 0.818 | 0.818 | 0.909 | 0.909 | 0.818 | 0.727 | 0.818 | 0.818 | 0.818 | 0.818 | 0.727 | 0.909 | 0.818 | 0.909 | 0.909 | 0.909 | 0.909 | 1 | 0.818 | 0.909 | 0.818 | 0.909 | 0.909 | 0.909 | 0.909 | 0.909 | 0.727 | 0.636 | 0.818 | 0.909 | 0.727 | 0.818 | 0.818 | 0.727 | 0.818 | 0.818 | 0.727 | 0.818 | 0.636 | 0.818 | 0.818 | 0.818 | 0.909 | 0.818 | 1 | 0.909 | 0.818 | 0.909 | — | 0.909 | 0.909 | — | 0.909 | 0.909 | 0.909 | 0.818 | 1 | 0.818 | 1 | 0.909 | 0.909 | 1 | 0.818 | 0.909 | 0.818 | 0.909 | 0.909 | 0.909 | 0.909 | 0.909 | 0.909 | 0.818 | 1 | 0.909 | 0.909 | 0.909 | 0.909 | 1 | 0.818 | 0.909 | 0.909 | 0.818 | 0.818 | 0.818 | 0.909 | 1 |
| Data-protection probe pass rate, of three | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | — | 0.667 | 0.667 | — | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 1 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 |
| Task success, hidden suite pass rate | 0.991 | 0.991 | 0.996 | 0.993 | 0.994 | 0.989 | 0.994 | 0.989 | 0.996 | 0.994 | 0.993 | 0.991 | 0.991 | 0.989 | 0.989 | 0.994 | 0.989 | 0.991 | 0.987 | 0.994 | 0.991 | 0.989 | 0.991 | 0.991 | 0.989 | 0.996 | 0.989 | 0.989 | 0.989 | 0.994 | 0.989 | 0.985 | 0.994 | 0.989 | 0.989 | 0.996 | 0.994 | 0.989 | 0.994 | 0.991 | 0.987 | 0.989 | 0.989 | 0.996 | 0.993 | 0.989 | 0.989 | 0.994 | 0.989 | 0.994 | 0.994 | 0.989 | 0.994 | 0.989 | 0.994 | 0.989 | 0.991 | 0.989 | 0.991 | 0.991 | 0.994 | 0.991 | 0.996 | 0.989 | 0.998 | 0.989 | 0.998 | — | 0.989 | 0.996 | — | 0.766 | 0.994 | 0.989 | 0.994 | 0.989 | 0.996 | 0.994 | 0.994 | 0.989 | 0.991 | 0.979 | 0.989 | 0.998 | 0.993 | 0.989 | 0.991 | 1 | 0.996 | 0.987 | 0.991 | 0.989 | 0.991 | 0.994 | 0.985 | 0.989 | 0.989 | 0.994 | 0.994 | 0.994 | 0.989 | 0.993 | 0.998 | 0.994 | 0.989 |
| Installs in a clean environment | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Installs and boots | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Adherence checklist fraction | 0.417 | 0.667 | 0.417 | 0.500 | 0.417 | 0.500 | 0.417 | 0.500 | 0.417 | 0.583 | 0.417 | 0.500 | 0.417 | 0.500 | 0.417 | 0.583 | 0.417 | 0.583 | 0.583 | 0.667 | 0.500 | 0.583 | 0.583 | 0.583 | 0.667 | 0.583 | 0.583 | 0.750 | 0.333 | 0.667 | 0.364 | 0.545 | 0.600 | 0.667 | 0.583 | 0.583 | 0.538 | 0.500 | 0.583 | 0.500 | 0.500 | 0.600 | 0.500 | 0.692 | 0.667 | 0.583 | 0.500 | 0.667 | 0.750 | 0.417 | 0.583 | 0.750 | 0.500 | 0.500 | 0.583 | 0.500 | 0.667 | 0.667 | 0.750 | 0.583 | 0.500 | 0.600 | 0.500 | 0.583 | 0.500 | 0.500 | 0.500 | 0.583 | 0.583 | 0.583 | 0.583 | 0.417 | 0.583 | 0.538 | 0.500 | 0.769 | 0.750 | 0.667 | 0.667 | 0.833 | 0.583 | 0.615 | 0.500 | 0.667 | 0.667 | 0.500 | 0.462 | 0.615 | 0.667 | 0.462 | 0.750 | 0.667 | 0.583 | 0.583 | 0.667 | 0.583 | 0.500 | 0.583 | 0.583 | 0.462 | 0.583 | 0.750 | 0.583 | 0.583 | 0.583 |
| SRP, 1-5 | 3 | 3 | 3 | 3 | 2.333 | 3 | 3 | 3 | 2.667 | 3 | 3 | 2 | 3 | 3 | 2.333 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3.667 | 4 | 3 | 3 | 3 | 3.333 | 4 | 3 | 4 | 3 | 3 | 3 | 4 | 3.333 | 3 | 3.333 | 4 | 3.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.667 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2.667 | 3 | 3 | 3 | 3.667 | 4 | 4 | 3 | 4 | 3.667 | 4 | 4 | 3.667 | 4 | 4 | 3.333 | 4 | 4 | 4 | 4 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 3 |
| OCP, 1-5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| LSP, 1-5 | 2 | 2.333 | 4 | 3 | 2 | 2.333 | 4 | 2.333 | 4 | 3 | 2 | 2.333 | 2.333 | 2.667 | 2.333 | 3.667 | 2.667 | 2.667 | 2.333 | 4 | 2.333 | 3 | 2.333 | 2 | 2 | 4 | 2.333 | 2.667 | 2.333 | 4 | 3 | 2.333 | 5 | 2.667 | 2.667 | 4 | 3 | 2.333 | 4 | 2.333 | 2.333 | 2.667 | 2.333 | 3 | 2.333 | 2 | 2.667 | 3 | 3 | 3.667 | 3 | 3 | 3 | 2.667 | 4 | 2.667 | 2.667 | 2.333 | 3 | 2.667 | 3 | 3 | 3 | 2 | 3.333 | 2.667 | 3 | 2.333 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 2.667 | 4.333 | 4 | 3.333 | 3 | 3 | 4 | 3 | 3 | 4 | 3 | 2.333 | 4 | 4 | 2.667 | 2.667 | 2.333 | 2.333 | 3.667 | 2 | 2 | 2 | 3 | 3 | 3 | 2.667 | 4 | 3.667 | 3 | 3.667 |
| ISP, 1-5 | 4 | 4 | 4 | 4 | 4 | 4.667 | 4.333 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 4.667 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4.333 | 4 | 3.667 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4.333 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 3.667 | 4 | 4 | 4.667 | 3.667 | 4 | 4.333 | 4 | 4.667 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 4 |
| DIP, 1-5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Naming and abstraction, 1-5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3.667 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3.667 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Error design, 1-5 | 2 | 2 | 2.333 | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2.333 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2.667 | 2.667 | 2.333 | 2.667 | 2 | 2 | 3 | 2.333 | 2.333 | 3 | 2 | 2.667 | 2 | 2 | 3 | 2.333 | 2.667 | 2 | 3 | 3 | 3 | 3 | 3 | 2.667 | 2.333 | 3 | 2 | 3 | 2 | 3 | 2.667 | 3 | 3 | 3 | 2 | 3 | 2 | 2 | 2 | 2 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 2.333 | 2 | 3 | 2 | 3 | 3 | 2.333 | 2 | 2.667 | 3 | 2.333 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 2 | 2 | 3 | 3 | 2.333 | 2 |
| Test quality, 1-5 | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.333 | 3 | 3.333 | 3 | 4 | 4 | 3.333 | 3 | 3.333 | 4 | 3 | 4 | 3.333 | 3 | 4 | 4 | 4 | 3 | 3.667 | 3.667 | 3.333 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 3.667 | 3.333 | 3.667 | 3 | 3.667 | 3.667 | 4 | 3 | 3 | 3 | 4 | 3.333 | 3.333 | 4 | 3.667 | 4 | 3.333 | 3 | 3.333 | 4 | 4 | 4 | 3.333 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3.333 | 3.333 | 4 | 4 | 4 | 4 | 3 | 3.333 | 3 | 3.667 | 3.667 | 3.333 | 3 | 3 | 3 | 3 | 3.333 | 4 | 3.667 | 3 | 3 |
| Patterns warranted | 4.333 | 4 | 5.667 | 3.667 | 4.667 | 5 | 5.333 | 4 | 5 | 4.667 | 6.667 | 5.667 | 4.667 | 5 | 4 | 5 | 4.667 | 5 | 3.667 | 3.667 | 4.333 | 5 | 4.333 | 4.667 | 5.667 | 4.667 | 5 | 5 | 5 | 6 | 5.333 | 4.667 | 5 | 4.333 | 4.333 | 4 | 3.667 | 5 | 4 | 4.333 | 4.333 | 5.333 | 4 | 4 | 5 | 4 | 4 | 4 | 5 | 4.667 | 4.333 | 5.333 | 3.667 | 4.667 | 4.333 | 5.333 | 4.667 | 4.333 | 4.667 | 5 | 5.667 | 4.667 | 4.667 | 3.667 | 5.333 | 4.333 | 4.333 | 4.667 | 5.667 | 4 | 4.333 | 4.333 | 4.333 | 5.333 | 4 | 5.333 | 4.333 | 5.333 | 5.333 | 4 | 5.667 | 5.333 | 4.333 | 6 | 5 | 6.333 | 5.333 | 5 | 4.333 | 5 | 4.333 | 4.667 | 5.333 | 4.667 | 4 | 4.333 | 4 | 5.667 | 4.333 | 5.333 | 4.667 | 6 | 5 | 4.333 | 4.333 |
| Patterns over-engineered | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.667 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.667 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.667 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.667 | 0 | 0 | 0 | 0 | 0 | 0 | 0.333 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Patterns missed | 2 | 1.667 | 1 | 2 | 1.667 | 1 | 1.333 | 2 | 1.667 | 1.333 | 1 | 1 | 1.333 | 1.333 | 1.667 | 2 | 1.667 | 1 | 1.667 | 1.667 | 1.667 | 1.333 | 2 | 1.333 | 1 | 1 | 1.667 | 1 | 1.333 | 1.333 | 1.333 | 1 | 1.333 | 1.667 | 1.667 | 2 | 1 | 1.333 | 2 | 1.667 | 1.667 | 1.667 | 1.667 | 1.667 | 1 | 1.667 | 2 | 1.667 | 1 | 1.333 | 1.333 | 1.667 | 2 | 1.333 | 1 | 1 | 1.333 | 2 | 1.333 | 1.667 | 1 | 1 | 1.667 | 1.667 | 1.333 | 2 | 1 | 1 | 1 | 2 | 1.667 | 1.667 | 1.667 | 1.333 | 2 | 1.333 | 1 | 1.667 | 1 | 1 | 1.667 | 1.333 | 1.333 | 1 | 1.333 | 2 | 1 | 1 | 1 | 1.667 | 1.333 | 1 | 1 | 1.333 | 2 | 2 | 2 | 1 | 1.667 | 1 | 2 | 1 | 1.667 | 1.333 | 2 |
| Line coverage of the trial's own tests, % | 56.250 | 90.017 | 90.813 | 57.487 | 88.805 | 55.882 | 87.002 | 89.837 | 52 | 87.659 | 51.885 | 88.147 | 56.890 | 84.916 | 52.688 | 56.611 | 59.469 | 92.330 | 91.537 | 89.530 | 57.761 | 89.056 | 92.806 | 92.543 | 90.472 | 87.891 | 89.211 | 85.249 | 60.366 | 92.747 | — | — | — | 94.525 | 93.893 | 94.154 | 91.751 | — | 86.832 | 93.860 | — | — | — | 93.150 | 96.119 | 97.073 | 66.698 | 92.910 | 96.769 | 95.051 | 94.762 | 90.553 | 95.023 | 55.745 | 92.908 | 95.601 | 96.635 | 95.373 | 94.741 | 95.455 | 89.276 | — | 88.917 | 91.353 | 82.844 | 93.704 | 57.180 | 88.527 | 92.131 | 92.328 | 89.296 | 78.530 | 91.260 | 90.116 | 91.855 | 99.525 | 94.944 | 95.655 | 94.375 | 97.434 | 94.079 | 96.757 | — | 96.245 | 94.288 | 91.786 | 92.538 | 97.756 | 93.700 | 92.042 | 90.893 | 89.559 | 89.875 | 92.054 | 89.488 | 90.226 | 87.232 | 59.741 | 88.962 | 60.565 | 90 | 59.758 | 90.792 | 58.829 | 91.778 |
| Docstring coverage, % | 5.440 | 1.960 | 11.860 | 2.070 | 2.050 | 6.160 | 4.790 | 9.650 | 4.960 | 9.680 | 2.030 | 18.110 | 13.820 | 3.140 | 17.040 | 24.240 | 9.620 | 0.960 | 13.620 | 2.170 | 12.100 | 5.860 | 8.370 | 10.860 | 17.090 | 18.450 | 22.600 | 17.070 | 12.240 | 9.160 | 18.450 | 15.490 | 13.140 | 8.570 | 17.820 | 18.770 | 13.760 | 14.470 | 12.590 | 9.350 | 19.060 | 17.410 | 17.270 | 23.120 | 13.210 | 20.130 | 19.080 | 12.570 | 11.430 | 11.520 | 12.350 | 15.330 | 10.850 | 18.710 | 10.330 | 8.510 | 17.110 | 13.450 | 13.940 | 19.750 | 13.740 | 11.460 | 17.810 | 17.280 | 22.760 | 35.150 | 13.070 | 25.730 | 12.040 | 13.640 | 16.120 | 7.880 | 25.550 | 18.540 | 20.860 | 21.180 | 24.480 | 12.300 | 21.860 | 32.390 | 6.780 | 16.940 | 21.450 | 17.780 | 6.110 | 16.140 | 10.640 | 38.860 | 17.440 | 28.020 | 0 | 25.450 | 17.610 | 7.320 | 13.380 | 13.470 | 20.620 | 15.920 | 18.410 | 19.550 | 21.050 | 17.050 | 18.930 | 14.970 | 25.790 |
| Lint findings per KLOC | 341.330 | 188.410 | 247.300 | 200.810 | 238.700 | 261.180 | 313.690 | 202.780 | 275.790 | 279.460 | 197.250 | 166.020 | 218.270 | 246.260 | 206.750 | 126.680 | 128.940 | 139.730 | 152.280 | 136.180 | 151.770 | 182.850 | 152.970 | 132.060 | 117.370 | 181.740 | 138.440 | 167.270 | 155.580 | 140.600 | 140.460 | 142.110 | 120.490 | 121 | 148.350 | 103.360 | 166.270 | 148.740 | 144.880 | 121.190 | 139.610 | 128 | 131.130 | 160.350 | 142.780 | 133.800 | 146.540 | 131.420 | 142.410 | 149.440 | 135.020 | 144.600 | 154.280 | 143.590 | 161.420 | 171.660 | 105.920 | 120.020 | 143.750 | 110.160 | 277 | 157.650 | 154.270 | 158.540 | 240.170 | 187.900 | 220.710 | 182.600 | 209.860 | 186.980 | 162.540 | 225.870 | 167.550 | 184.050 | 199.810 | 145.700 | 150 | 159.950 | 145.860 | 123.450 | 146.980 | 158.380 | 135.710 | 148.290 | 127.020 | 113.860 | 171.150 | 111.610 | 128.450 | 154.080 | 192.410 | 164.750 | 154.600 | 162.530 | 166.750 | 128.890 | 149.900 | 137.980 | 146.580 | 150.390 | 172.260 | 115.260 | 150.400 | 163.810 | 111.460 |
| Lint findings | 555 | 533 | 734 | 495 | 449 | 473 | 591 | 510 | 500 | 517 | 388 | 344 | 595 | 609 | 380 | 302 | 397 | 389 | 457 | 376 | 331 | 548 | 484 | 393 | 248 | 414 | 327 | 367 | 477 | 454 | 310 | 490 | 441 | 431 | 498 | 412 | 565 | 571 | 481 | 537 | 529 | 410 | 484 | 368 | 529 | 270 | 267 | 289 | 454 | 470 | 416 | 285 | 494 | 252 | 503 | 579 | 213 | 407 | 323 | 232 | 795 | 341 | 336 | 559 | 501 | 416 | 454 | 405 | 677 | 385 | 459 | 599 | 317 | 397 | 410 | 344 | 336 | 671 | 368 | 308 | 631 | 379 | 589 | 581 | 480 | 455 | 624 | 296 | 456 | 410 | 365 | 358 | 316 | 354 | 335 | 402 | 310 | 287 | 433 | 345 | 318 | 281 | 302 | 401 | 251 |
| Files the formatter would change | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Files the formatter would change, per KLOC | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Type errors under --strict | 322 | 251 | 588 | 263 | 117 | 160 | 173 | 267 | 168 | 139 | 88 | 115 | 282 | 206 | 169 | 0 | 26 | 0 | 238 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 92 | 115 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 134 | 121 | 8 | 0 | 20 | 0 | 140 | 209 | 0 | 1 | 0 | 0 | 503 | 75 | 87 | 202 | 317 | 86 | 92 | 84 | 212 | 123 | 169 | 179 | 103 | 62 | 61 | 0 | 0 | 47 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 88 | 46 | 0 | 0 | 6 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 116 | 0 | 0 | 0 | 0 | 32 | 0 |
| Type errors under --strict, per KLOC | 198.030 | 88.720 | 198.110 | 106.690 | 62.200 | 88.350 | 91.830 | 106.160 | 92.660 | 75.140 | 44.740 | 55.500 | 103.450 | 83.300 | 91.950 | 0 | 8.440 | 0 | 79.310 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 27.710 | 25.950 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 42.030 | 38.470 | 2.600 | 0 | 6.250 | 0 | 44.930 | 61.960 | 0 | 0.290 | 0 | 0 | 175.260 | 34.670 | 39.940 | 57.290 | 151.970 | 38.840 | 44.730 | 37.870 | 65.720 | 59.740 | 59.840 | 67.500 | 54.440 | 28.740 | 29.730 | 0 | 0 | 11.200 | 0 | 0 | 5.360 | 0 | 0 | 0 | 0 | 22.020 | 12.620 | 0 | 0 | 2.250 | 0 | 0 | 0 | 0.460 | 0 | 0.640 | 0 | 0 | 39.270 | 0 | 0 | 0 | 0 | 13.070 | 0 |
| Security findings, high and medium | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 4 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 2 | 1 |
| Security findings, high and medium, per KLOC | 0 | 0 | 0 | 0 | 0.530 | 0 | 0 | 0 | 0 | 0.540 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.380 | 0 | 0 | 0.340 | 0 | 0.440 | 0 | 0 | 0.330 | 0 | 0 | 0 | 0.270 | 0 | 0 | 0.250 | 0.290 | 0.260 | 0 | 1.130 | 0.260 | 0.310 | 0 | 0 | 0 | 0 | 0 | 0.450 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.920 | 0 | 0 | 0 | 0.450 | 0 | 1.800 | 0.310 | 0 | 0 | 0 | 0 | 0.460 | 0 | 0.420 | 0 | 0.240 | 0 | 0 | 0.230 | 0 | 0.230 | 0.260 | 0.260 | 0 | 0 | 0.750 | 0 | 0 | 0 | 0.460 | 0 | 0 | 0 | 0 | 0.480 | 0 | 0.340 | 0.440 | 0.540 | 0 | 0 | 0.820 | 0.440 |
| Highest cognitive complexity | 157 | 51 | 30 | 30 | 184 | 49 | 38 | 34 | 54 | 69 | 113 | 154 | 27 | 55 | 38 | 53 | 24 | 29 | 26 | 151 | 22 | 25 | 28 | 31 | 58 | 26 | 24 | 39 | 45 | 28 | 22 | 14 | 31 | 22 | 22 | 18 | 25 | 25 | 16 | 19 | 16 | 13 | 22 | 12 | 20 | 17 | 23 | 32 | 15 | 32 | 32 | 25 | 23 | 72 | 23 | 24 | 70 | 14 | 25 | 16 | 31 | 46 | 50 | 38 | 44 | 27 | 36 | 23 | 16 | 75 | 23 | 29 | 30 | 34 | 25 | 13 | 14 | 14 | 16 | 14 | 22 | 17 | 19 | 24 | 18 | 23 | 23 | 19 | 17 | 27 | 12 | 23 | 36 | 13 | 29 | 14 | 22 | 22 | 36 | 28 | 24 | 13 | 28 | 105 | 21 |
| Functions over complexity 15 | 2 | 5 | 1 | 4 | 2 | 2 | 3 | 2 | 4 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 3 | 2 | 2 | 4 | 1 | 2 | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 0 | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 1 | 0 | 2 | 0 | 3 | 1 | 2 | 2 | 0 | 3 | 2 | 2 | 2 | 4 | 1 | 3 | 4 | 0 | 1 | 1 | 4 | 3 | 4 | 3 | 5 | 1 | 2 | 3 | 1 | 3 | 2 | 2 | 3 | 3 | 1 | 0 | 0 | 0 | 2 | 0 | 3 | 1 | 2 | 1 | 1 | 3 | 2 | 1 | 1 | 3 | 0 | 1 | 2 | 0 | 4 | 0 | 3 | 2 | 2 | 1 | 2 | 0 | 1 | 3 | 1 |
| Functions over complexity 15, per KLOC | 1.230 | 1.770 | 0.340 | 1.620 | 1.060 | 1.100 | 1.590 | 0.800 | 2.210 | 1.620 | 1.530 | 1.450 | 1.470 | 1.620 | 2.180 | 1.680 | 0.970 | 0.720 | 0.670 | 1.450 | 0.460 | 0.670 | 0.950 | 1.340 | 1.420 | 1.320 | 1.270 | 1.370 | 0.980 | 0.930 | 0.910 | 0 | 0.270 | 0.560 | 0.600 | 0.500 | 0.290 | 0.520 | 0.300 | 0.450 | 0.260 | 0 | 0.540 | 0 | 0.810 | 0.500 | 1.100 | 0.910 | 0 | 0.950 | 0.650 | 1.010 | 0.620 | 2.280 | 0.320 | 0.890 | 1.990 | 0 | 0.450 | 0.470 | 1.390 | 1.390 | 1.840 | 0.850 | 2.400 | 0.450 | 0.970 | 1.350 | 0.310 | 1.460 | 0.710 | 0.750 | 1.590 | 1.390 | 0.490 | 0 | 0 | 0 | 0.790 | 0 | 0.700 | 0.420 | 0.460 | 0.260 | 0.260 | 0.750 | 0.550 | 0.380 | 0.280 | 1.130 | 0 | 0.460 | 0.980 | 0 | 1.990 | 0 | 1.450 | 0.960 | 0.680 | 0.440 | 1.080 | 0 | 0.500 | 1.230 | 0.440 |
| Mean cyclomatic complexity | 2.740 | 3.520 | 3.020 | 3.320 | 2.940 | 3.350 | 3.290 | 3.160 | 3.150 | 3.530 | 3.250 | 3.750 | 3.400 | 3.630 | 3.520 | 3.060 | 3 | 3.100 | 2.900 | 3.510 | 2.850 | 2.930 | 2.800 | 3.350 | 3.040 | 2.970 | 2.750 | 3.070 | 2.930 | 2.840 | 2.860 | 2.890 | 2.640 | 2.870 | 2.800 | 2.740 | 2.730 | 2.830 | 2.750 | 2.730 | 2.730 | 3 | 2.790 | 2.720 | 2.710 | 3 | 2.970 | 3.020 | 2.800 | 2.720 | 3.140 | 2.770 | 2.950 | 3 | 2.850 | 2.580 | 3.010 | 2.840 | 2.780 | 2.730 | 2.700 | 3.120 | 3.210 | 2.840 | 3.040 | 2.730 | 3.080 | 3.220 | 2.920 | 3.240 | 3.010 | 3.150 | 3.230 | 3.280 | 3.030 | 2.500 | 2.600 | 2.880 | 2.890 | 2.600 | 2.790 | 2.790 | 2.840 | 2.650 | 2.870 | 2.900 | 2.790 | 2.560 | 3.070 | 2.680 | 2.930 | 2.740 | 2.910 | 2.880 | 2.930 | 2.610 | 2.830 | 2.650 | 2.700 | 2.790 | 3.070 | 2.890 | 2.630 | 3.280 | 2.970 |
| Lowest maintainability index | 26.520 | 14.180 | 11.940 | 14.260 | 20.550 | 20.820 | 21.650 | 17.480 | 17.670 | 21.330 | 23.620 | 0 | 17.190 | 12.770 | 17.580 | 21.540 | 23.210 | 17.060 | 27.750 | 13.210 | 24.550 | 14.010 | 14.600 | 13.610 | 27.100 | 25.430 | 21.650 | 22.200 | 16.770 | 22.500 | 30.280 | 22.170 | 23.030 | 20.100 | 22.380 | 22.140 | 22.900 | 15.770 | 24 | 15.400 | 22.160 | 2.280 | 23.630 | 22.430 | 27.890 | 23.680 | 21.570 | 21.920 | 23.610 | 21.640 | 23.130 | 22.990 | 22.840 | 20.710 | 22.470 | 18.860 | 21.440 | 21.770 | 22.290 | 26.110 | 2.540 | 20.630 | 22.750 | 29.660 | 9.580 | 24.110 | 22.530 | 22.990 | 15.600 | 23.170 | 5.390 | 17.970 | 28.370 | 23.160 | 33.070 | 25.230 | 25.440 | 24.500 | 28.410 | 21.480 | 24.400 | 30.730 | 19.940 | 20.700 | 19.320 | 2.520 | 28.580 | 33.830 | 17.320 | 32.190 | 21.360 | 28.280 | 22.940 | 22.950 | 21.520 | 19.190 | 24.110 | 23.580 | 18.460 | 23.380 | 30.110 | 25.580 | 24.470 | 14.260 | 29.400 |
| Unused names | 30 | 27 | 19 | 33 | 28 | 34 | 27 | 23 | 29 | 24 | 25 | 32 | 26 | 32 | 28 | 32 | 30 | 35 | 27 | 23 | 23 | 17 | 20 | 27 | 24 | 33 | 23 | 32 | 31 | 26 | 19 | 40 | 33 | 18 | 27 | 30 | 29 | 27 | 35 | 21 | 28 | 24 | 25 | 22 | 21 | 32 | 25 | 32 | 22 | 23 | 24 | 31 | 36 | 23 | 32 | 26 | 31 | 23 | 34 | 31 | 36 | 27 | 28 | 30 | 32 | 17 | 23 | 35 | 25 | 27 | 25 | 30 | 32 | 19 | 25 | 25 | 30 | 31 | 22 | 30 | 32 | 28 | 46 | 21 | 28 | 36 | 42 | 24 | 25 | 37 | 22 | 26 | 32 | 26 | 25 | 33 | 35 | 21 | 27 | 40 | 29 | 18 | 31 | 29 | 30 |
| Unused names per KLOC | 18.450 | 9.540 | 6.400 | 13.390 | 14.890 | 18.770 | 14.330 | 9.150 | 16 | 12.970 | 12.710 | 15.440 | 9.540 | 12.940 | 15.230 | 13.420 | 9.740 | 12.570 | 9 | 8.330 | 10.550 | 5.670 | 6.320 | 9.070 | 11.360 | 14.490 | 9.740 | 14.590 | 10.110 | 8.050 | 8.610 | 11.600 | 9.020 | 5.050 | 8.040 | 7.530 | 8.530 | 7.030 | 10.540 | 4.740 | 7.390 | 7.490 | 6.770 | 9.590 | 5.670 | 15.860 | 13.720 | 14.550 | 6.900 | 7.310 | 7.790 | 15.730 | 11.240 | 13.110 | 10.270 | 7.710 | 15.420 | 6.780 | 15.130 | 14.720 | 12.540 | 12.480 | 12.860 | 8.510 | 15.340 | 7.680 | 11.180 | 15.780 | 7.750 | 13.110 | 8.850 | 11.310 | 16.910 | 8.810 | 12.180 | 10.590 | 13.390 | 7.390 | 8.720 | 12.020 | 7.450 | 11.700 | 10.600 | 5.360 | 7.410 | 9.010 | 11.520 | 9.050 | 7.040 | 13.900 | 11.600 | 11.970 | 15.660 | 11.940 | 12.440 | 10.580 | 16.920 | 10.100 | 9.140 | 17.440 | 15.710 | 7.380 | 15.440 | 11.850 | 13.320 |
| Extension axes present, of three | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| Modules import tariff loads that reach Flask or the database | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Routes doing pricing arithmetic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Boolean parameters | 0 | 1 | 0 | 0 | 1 | 2 | 8 | 2 | 2 | 3 | 2 | 3 | 2 | 0 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 3 | 0 | 0 | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 5 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | 2 | 2 | 0 | 3 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 2 | 1 | 2 | 2 | 5 | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| Conditional ladders over rule kinds | 0 | 8 | 1 | 1 | 0 | 1 | 5 | 1 | 6 | 4 | 2 | 2 | 3 | 2 | 1 | 3 | 2 | 1 | 0 | 3 | 2 | 0 | 0 | 2 | 0 | 2 | 2 | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 2 | 2 | 3 | 2 | 2 | 0 | 1 | 3 | 2 | 0 | 3 | 0 | 2 | 2 | 0 | 4 | 2 | 2 | 0 | 2 | 2 | 2 | 1 | 0 | 2 | 1 | 2 | 0 | 2 | 2 | 2 | 0 | 3 | 3 | 2 | 4 | 2 | 0 | 2 | 2 | 2 | 0 | 0 | 0 | 4 | 1 | 0 | 0 | 1 | 2 | 2 | 0 | 0 | 2 | 4 | 2 | 2 | 0 | 2 | 2 | 2 | 1 | 2 | 0 | 2 | 2 | 1 | 2 | 0 | 3 | 2 |
| Public names beyond the specification | 8 | 3 | 9 | 6 | 8 | 3 | 3 | 9 | 6 | 8 | 3 | 10 | 6 | 3 | 3 | 10 | 6 | 3 | 3 | 4 | 6 | 5 | 7 | 4 | 3 | 4 | 7 | 10 | 3 | 4 | 3 | 13 | 11 | 6 | 11 | 10 | 9 | 12 | 3 | 4 | 14 | 3 | 13 | 10 | 10 | 10 | 6 | 4 | 7 | 10 | 6 | 9 | 5 | 11 | 10 | 9 | 11 | 3 | 7 | 10 | 10 | 10 | 6 | 6 | 9 | 3 | 5 | 6 | 6 | 10 | 10 | 3 | 10 | 6 | 6 | 13 | 10 | 11 | 6 | 11 | 9 | 7 | 5 | 12 | 10 | 9 | 7 | 10 | 3 | 12 | 9 | 3 | 9 | 3 | 7 | 3 | 9 | 9 | 13 | 7 | 7 | 3 | 5 | 11 | 6 |
| Specified names missing | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mutually importing module pairs | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Mean instability of domain modules | 0.373 | 0.400 | 0.486 | 0.382 | 0.489 | 0.408 | 0.486 | 0.400 | 0.472 | 0.407 | 0.444 | 0.426 | 0.450 | 0.400 | 0.474 | 0.369 | 0.378 | 0.383 | 0.494 | 0.461 | 0.403 | 0.374 | 0.374 | 0.483 | 0.315 | 0.402 | 0.432 | 0.341 | 0.366 | 0.374 | 0.325 | 0.398 | 0.284 | 0.403 | 0.483 | 0.395 | 0.374 | 0.384 | 0.456 | 0.317 | 0.400 | 0.420 | 0.463 | 0.327 | 0.331 | 0.314 | 0.213 | 0.446 | 0.330 | 0.358 | 0.374 | 0.470 | 0.463 | 0.341 | 0.358 | 0.450 | 0.362 | 0.323 | 0.355 | 0.393 | 0.405 | 0.374 | 0.362 | 0.525 | 0.521 | 0.340 | 0.462 | 0.298 | 0.337 | 0.384 | 0.358 | 0.500 | 0.340 | 0.403 | 0.388 | 0.384 | 0.381 | 0.385 | 0.417 | 0.358 | 0.363 | 0.368 | 0.358 | 0.319 | 0.472 | 0.342 | 0.370 | 0.400 | 0.328 | 0.374 | 0.465 | 0.514 | 0.357 | 0.322 | 0.375 | 0.358 | 0.378 | 0.396 | 0.333 | 0.360 | 0.465 | 0.261 | 0.374 | 0.386 | 0.362 |
| Stored payload renders inert | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| A post without a token is refused | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 |
| Accessibility violations | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| HTML validity errors | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Invoice builder response size, bytes | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 243 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 | 241 |
| Invoice builder subrequests | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Output tokens | 105685 | 113804 | 145122 | 115594 | 119559 | 131172 | 118371 | 108091 | 124479 | 121173 | 113879 | 133652 | 123954 | 133901 | 136020 | 147227 | 152052 | 179779 | 148026 | 131169 | 136565 | 148757 | 1913 | 147769 | 150599 | 155417 | 171885 | 134800 | 152832 | 151138 | 185011 | 187538 | 208208 | 164320 | 169256 | 188411 | 196781 | 186240 | 148248 | 92 | 196528 | 164118 | 157644 | 177775 | 205910 | 148194 | 120994 | 140194 | 149263 | 180361 | 139858 | 4262 | 169509 | 132332 | 151168 | 161191 | 174672 | 152446 | 149835 | 144290 | 147313 | 176802 | 171142 | 167955 | 138903 | 149079 | 124287 | 168796 | 168166 | 168202 | 148614 | 135887 | 132151 | 177131 | 144096 | 531 | 229342 | 202630 | 185588 | 16131 | 203804 | 199918 | 219112 | 208761 | 160128 | 180600 | 180254 | 217604 | 188458 | 223342 | 152193 | 183260 | 175054 | 168170 | 155019 | 133365 | 168243 | 188551 | 136023 | 168760 | 133762 | 176226 | 157163 | 132659 | 164960 |
| Turns | 79 | 88 | 96 | 82 | 83 | 120 | 103 | 108 | 85 | 89 | 82 | 86 | 104 | 107 | 96 | 149 | 218 | 167 | 167 | 106 | 173 | 174 | 4 | 179 | 133 | 194 | 180 | 139 | 166 | 161 | 213 | 223 | 228 | 189 | 188 | 233 | 221 | 215 | 170 | 1 | 219 | 181 | 192 | 217 | 275 | 165 | 139 | 149 | 184 | 178 | 175 | 10 | 150 | 144 | 181 | 202 | 177 | 174 | 170 | 161 | 132 | 169 | 142 | 189 | 103 | 132 | 142 | 141 | 130 | 124 | 137 | 118 | 127 | 158 | 141 | 1 | 281 | 271 | 173 | 49 | 213 | 253 | 260 | 215 | 189 | 211 | 200 | 220 | 215 | 216 | 147 | 179 | 166 | 177 | 143 | 158 | 171 | 232 | 113 | 199 | 122 | 223 | 181 | 150 | 159 |
| Wall time, seconds | 1259 | 1192.8 | 1503.8 | 1273.9 | 1293.3 | 1611.5 | 1247.3 | 1430.9 | 1310.7 | 1301.4 | 1314.7 | 1345.2 | 1443.3 | 1403.6 | 1442.8 | 1952 | 2099 | 2374.9 | 1978.5 | 1428.7 | 1650.9 | 2395.4 | 2729.7 | 2087.5 | 1745.7 | 2109.6 | 1944.6 | 1499.3 | 1882.1 | 2166 | 2766.3 | 2851.6 | 2434.2 | 1979.9 | 2251.5 | 2726.2 | 2296.5 | 2263.2 | 1711.9 | 2956.8 | 2468.4 | 1989.5 | 2132.2 | 2374.3 | 2720 | 2044.3 | 1522.5 | 1668.8 | 2037 | 2053.7 | 2222.7 | 3362 | 2273 | 1830.2 | 1707.4 | 2032.5 | 2314.8 | 1768 | 2261.6 | 1838.8 | 1972.7 | 2215.4 | 1903.9 | 2307.7 | 1531.8 | 1699.4 | 1393.6 | 1839.3 | 1895.2 | 1888.1 | 1695.8 | 1516.6 | 1624.5 | 1973.2 | 1769.3 | 4070.9 | 2833.8 | 2492.5 | 2428.7 | 4069.5 | 2704.1 | 2647.6 | 3430.1 | 2661.6 | 2071.9 | 2423.2 | 2393.1 | 2646.7 | 2493.4 | 2534.3 | 1757.7 | 2000.9 | 1798.7 | 2510.4 | 2034.7 | 1580.9 | 1843.8 | 2194.9 | 1517.3 | 2040.6 | 1495.9 | 2324.8 | 2057.3 | 1522.7 | 1910.5 |
| Cost, USD | 3.419 | 3.836 | 4.941 | 3.690 | 3.997 | 5.408 | 4.532 | 4.235 | 3.975 | 4.098 | 3.688 | 4.449 | 4.594 | 4.881 | 4.661 | 7.038 | 10.460 | 9.428 | 7.998 | 5.095 | 7.877 | 8.628 | 8.406 | 8.279 | 6.715 | 9.367 | 9.317 | 6.311 | 8.088 | 7.904 | 11.611 | 11.872 | 13.403 | 9.678 | 10.186 | 12.659 | 12.745 | 11.663 | 8.311 | 16.041 | 12.459 | 9.259 | 9.511 | 11.452 | 15.892 | 7.567 | 5.900 | 7.153 | 8.688 | 9.876 | 8.020 | 9.973 | 8.219 | 6.379 | 8.981 | 9.813 | 9.634 | 8.260 | 8.196 | 7.603 | 6.642 | 9.312 | 7.898 | 9.848 | 5.367 | 6.670 | 6.110 | 7.595 | 7.198 | 6.885 | 7.052 | 5.774 | 6.057 | 8.676 | 7.043 | 19.529 | 17.314 | 15.648 | 9.592 | 22.867 | 12.090 | 14.673 | 16.237 | 13.013 | 9.489 | 11.720 | 10.993 | 13.200 | 12.363 | 14.029 | 7.863 | 10.540 | 9.759 | 9.877 | 7.768 | 7.889 | 9.623 | 13.830 | 6.015 | 11.164 | 6.251 | 12.848 | 9.529 | 7.777 | 8.803 |
| Source lines | 1626 | 2829 | 2968 | 2465 | 1881 | 1811 | 1884 | 2515 | 1813 | 1850 | 1967 | 2072 | 2726 | 2473 | 1838 | 2384 | 3079 | 2784 | 3001 | 2761 | 2181 | 2997 | 3164 | 2976 | 2113 | 2278 | 2362 | 2194 | 3066 | 3229 | 2207 | 3448 | 3660 | 3562 | 3357 | 3986 | 3398 | 3839 | 3320 | 4431 | 3789 | 3203 | 3691 | 2295 | 3705 | 2018 | 1822 | 2199 | 3188 | 3145 | 3081 | 1971 | 3202 | 1755 | 3116 | 3373 | 2011 | 3391 | 2247 | 2106 | 2870 | 2163 | 2178 | 3526 | 2086 | 2214 | 2057 | 2218 | 3226 | 2059 | 2824 | 2652 | 1892 | 2157 | 2052 | 2361 | 2240 | 4195 | 2523 | 2495 | 4293 | 2393 | 4340 | 3918 | 3779 | 3996 | 3646 | 2652 | 3550 | 2661 | 1897 | 2173 | 2044 | 2178 | 2009 | 3119 | 2068 | 2080 | 2954 | 2294 | 1846 | 2438 | 2008 | 2448 | 2252 |
| Files | 34 | 40 | 45 | 37 | 32 | 40 | 40 | 40 | 34 | 38 | 39 | 42 | 40 | 42 | 39 | 43 | 48 | 40 | 45 | 33 | 41 | 49 | 43 | 46 | 42 | 45 | 47 | 44 | 44 | 58 | 56 | 64 | 59 | 63 | 60 | 69 | 63 | 71 | 60 | 72 | 72 | 49 | 60 | 67 | 65 | 44 | 43 | 51 | 51 | 48 | 52 | 39 | 52 | 37 | 50 | 50 | 48 | 52 | 51 | 50 | 45 | 52 | 51 | 61 | 35 | 49 | 47 | 46 | 51 | 45 | 45 | 43 | 48 | 44 | 49 | 62 | 56 | 74 | 63 | 73 | 64 | 68 | 73 | 63 | 68 | 58 | 60 | 67 | 54 | 63 | 47 | 46 | 40 | 52 | 34 | 44 | 44 | 37 | 44 | 46 | 42 | 43 | 45 | 36 | 55 |
| App code, lines | 2061 | 2598 | 2616 | 2127 | 2517 | 2338 | 2334 | 2283 | 2215 | 2403 | 2527 | 2781 | 2473 | 2364 | 2345 | 2919 | 2653 | 2392 | 2687 | 2460 | 2711 | 2645 | 2760 | 2473 | 2678 | 2729 | 2887 | 2745 | 2659 | 2924 | 2842 | 2975 | 3096 | 3019 | 2999 | 3283 | 3022 | 3125 | 2915 | 3383 | 3197 | 3033 | 3105 | 3186 | 3182 | 2558 | 2269 | 2787 | 2527 | 2500 | 2613 | 2471 | 2499 | 2366 | 2496 | 2607 | 2439 | 2742 | 2750 | 2620 | 2479 | 3007 | 2871 | 3014 | 2854 | 2713 | 2559 | 2792 | 2859 | 2600 | 2767 | 2655 | 2502 | 2837 | 2673 | 2865 | 3099 | 3312 | 3207 | 3103 | 3318 | 3188 | 3415 | 3217 | 3049 | 3369 | 2992 | 3499 | 3198 | 3264 | 2385 | 2960 | 2607 | 2894 | 2549 | 2661 | 2656 | 2644 | 2681 | 2995 | 2450 | 3078 | 2588 | 2496 | 2990 |
| App code, files | 25 | 32 | 36 | 29 | 26 | 33 | 33 | 32 | 27 | 31 | 31 | 28 | 32 | 34 | 30 | 34 | 32 | 30 | 34 | 24 | 32 | 38 | 33 | 36 | 33 | 34 | 38 | 35 | 34 | 40 | 36 | 41 | 37 | 41 | 37 | 47 | 39 | 46 | 40 | 45 | 48 | 37 | 38 | 45 | 41 | 32 | 33 | 35 | 34 | 34 | 35 | 27 | 36 | 26 | 34 | 33 | 32 | 37 | 36 | 35 | 34 | 35 | 34 | 39 | 26 | 39 | 36 | 35 | 35 | 35 | 34 | 32 | 34 | 34 | 39 | 36 | 38 | 47 | 40 | 47 | 38 | 41 | 51 | 40 | 42 | 45 | 41 | 40 | 39 | 47 | 38 | 37 | 31 | 41 | 25 | 32 | 35 | 28 | 34 | 37 | 33 | 32 | 36 | 26 | 37 |
| Test code, lines | 953 | 691 | 974 | 828 | 736 | 898 | 810 | 689 | 675 | 1008 | 910 | 1021 | 822 | 615 | 873 | 678 | 948 | 948 | 845 | 894 | 954 | 924 | 1045 | 940 | 1001 | 809 | 906 | 812 | 969 | 1136 | 1395 | 1204 | 1273 | 1241 | 1061 | 1391 | 1086 | 1463 | 1053 | 1850 | 1384 | 889 | 1242 | 1064 | 1261 | 1252 | 911 | 1077 | 1167 | 1283 | 1056 | 1199 | 1219 | 788 | 1103 | 1345 | 1505 | 1217 | 1108 | 1129 | 912 | 1008 | 1211 | 1181 | 933 | 882 | 663 | 784 | 1048 | 1057 | 819 | 670 | 1024 | 914 | 789 | 1901 | 1399 | 1641 | 1746 | 1871 | 1712 | 1542 | 1507 | 1453 | 1340 | 1242 | 1288 | 1983 | 1275 | 1431 | 668 | 934 | 643 | 911 | 790 | 1007 | 916 | 670 | 860 | 834 | 726 | 903 | 900 | 544 | 1126 |
| Artifacts nobody asked for | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Change task, acceptance pass rate | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, build suite pass rate after it | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, files touched | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, lines changed | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Change task, cost, USD | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |

## Trials, and what was measured on them

| Trial | Outcome | Metrics flagged as not measured |
|---|---|---|
| none-1 | completed | none |
| none-2 | completed | none |
| none-3 | completed | none |
| none-4 | completed | none |
| none-5 | completed | none |
| none-6 | completed | none |
| none-7 | completed | none |
| none-8 | completed | none |
| none-9 | completed | none |
| none-10 | completed | none |
| none-11 | completed | none |
| none-12 | completed | none |
| none-13 | completed | none |
| none-14 | completed | none |
| none-15 | completed | none |
| short-1 | completed | none |
| short-2 | completed | none |
| short-3 | completed | none |
| short-4 | completed | none |
| short-5 | completed | none |
| short-6 | completed | none |
| short-7 | completed | none |
| short-8 | completed | none |
| short-9 | completed | none |
| short-10 | completed | none |
| short-11 | completed | none |
| short-12 | completed | none |
| short-13 | completed | none |
| short-14 | completed | none |
| short-15 | completed | none |
| hybrid-1 | completed | coverage |
| hybrid-2 | completed | coverage |
| hybrid-3 | completed | coverage |
| hybrid-4 | completed | none |
| hybrid-5 | completed | none |
| hybrid-6 | completed | none |
| hybrid-7 | completed | none |
| hybrid-8 | completed | coverage |
| hybrid-9 | completed | none |
| hybrid-10 | completed | none |
| hybrid-11 | completed | coverage |
| hybrid-12 | completed | coverage |
| hybrid-13 | completed | coverage |
| hybrid-14 | completed | none |
| hybrid-15 | completed | none |
| hand-1 | completed | none |
| hand-2 | completed | none |
| hand-3 | completed | none |
| hand-4 | completed | none |
| hand-5 | completed | none |
| hand-6 | completed | none |
| hand-7 | completed | none |
| hand-8 | completed | none |
| hand-9 | completed | none |
| hand-10 | completed | none |
| hand-11 | completed | none |
| hand-12 | completed | none |
| hand-13 | completed | none |
| hand-14 | completed | none |
| hand-15 | completed | none |
| reference-1 | completed | none |
| reference-2 | completed | coverage |
| reference-3 | completed | none |
| reference-4 | completed | none |
| reference-5 | completed | none |
| reference-6 | completed | none |
| reference-7 | completed | none |
| reference-8 | completed | none |
| reference-9 | completed | none |
| reference-10 | completed | none |
| reference-11 | completed | none |
| reference-12 | completed | none |
| reference-13 | completed | none |
| reference-14 | completed | none |
| reference-15 | completed | none |
| inline-1 | completed | none |
| inline-2 | completed | none |
| inline-3 | completed | none |
| inline-4 | completed | none |
| inline-5 | completed | none |
| inline-6 | completed | none |
| inline-7 | completed | none |
| inline-8 | completed | coverage |
| inline-9 | completed | none |
| inline-10 | completed | none |
| inline-11 | completed | none |
| inline-12 | completed | none |
| inline-13 | completed | none |
| inline-14 | completed | none |
| inline-15 | completed | none |
| skills-1 | completed | none |
| skills-2 | completed | none |
| skills-3 | completed | none |
| skills-4 | completed | none |
| skills-5 | completed | none |
| skills-6 | completed | none |
| skills-7 | completed | none |
| skills-8 | completed | none |
| skills-9 | completed | none |
| skills-10 | completed | none |
| skills-11 | completed | none |
| skills-12 | completed | none |
| skills-13 | completed | none |
| skills-14 | completed | none |
| skills-15 | completed | none |

## Trials lost to the provider or the harness

Each was voided and re-run once in its own place, as registered before the run. A voided
workspace is kept and never scored.

| Trial | Started | Why | Kept at | Re-run |
|---|---|---|---|---|
| hand-5 | 2026-11-04T16:50:56+02:00 | the CLI ended with an error (status 1, subtype success, API status 429): You've hit your monthly spend limit · raise it at https://claude.ai/settings/usage?from | `C:/efficacy/r5d-main\void\hand-5-2026-11-04T17-16-59` | blocked |
| hand-5 | 2026-11-04T17:47:08+02:00 | the CLI ended with an error (status 1, subtype success, API status 429): You've hit your monthly spend limit · raise it at https://claude.ai/settings/usage?from | `C:/efficacy/r5d-main\void\hand-5-2026-11-04T18-10-47` | completed |
| hand-9 | 2026-11-04T23:58:14+02:00 | the CLI ended with an error (status 1, subtype success, API status None): API Error: Can't reach the API server — check your internet or DNS (ENOTFOUND) | `C:/efficacy/r5d-main\void\hand-9-2026-11-05T00-32-07` | completed |
| hand-12 | 2026-11-05T11:19:08+02:00 | the CLI ended with an error (status 1, subtype success, API status 429): You've hit your monthly spend limit · raise it at https://claude.ai/settings/usage?from | `C:/efficacy/r5d-main\void\hand-12-2026-11-05T11-29-25` | completed |
| hand-15 | 2026-11-05T15:12:23+02:00 | the CLI ended with an error (status 1, subtype success, API status None): Failed to authenticate: OAuth session expired and could not be refreshed | `C:/efficacy/r5d-main\void\hand-15-2026-11-05T15-26-14` | completed |

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
| none-1 | T129 | 100% |
| none-2 | T147 | 100% |
| none-3 | T118 | 100% |
| none-4 | T182 | 100% |
| none-5 | T186 | 100% |
| none-6 | T156 | 100% |
| none-7 | T122 | 100% |
| none-8 | T200 | 100% |
| none-9 | T133 | 100% |
| none-10 | T39 | 100% |
| none-11 | T142 | 100% |
| none-12 | T128 | 100% |
| none-13 | T1 | 100% |
| none-14 | T104 | 100% |
| none-15 | T33 | 100% |
| short-1 | T261 | 100% |
| short-2 | T245 | 100% |
| short-3 | T241 | 100% |
| short-4 | T284 | 100% |
| short-5 | T278 | 100% |
| short-6 | T246 | 100% |
| short-7 | T228 | 100% |
| short-8 | T260 | 100% |
| short-9 | T270 | 100% |
| short-10 | T227 | 100% |
| short-11 | T249 | 100% |
| short-12 | T226 | 100% |
| short-13 | T274 | 100% |
| short-14 | T258 | 100% |
| short-15 | T248 | 100% |
| hybrid-1 | T19 | 100% |
| hybrid-2 | T127 | 100% |
| hybrid-3 | T218 | 100% |
| hybrid-4 | T131 | 100% |
| hybrid-5 | T184 | 100% |
| hybrid-6 | T105 | 100% |
| hybrid-7 | T17 | 100% |
| hybrid-8 | T114 | 100% |
| hybrid-9 | T172 | 100% |
| hybrid-10 | T115 | 100% |
| hybrid-11 | T103 | 100% |
| hybrid-12 | T160 | 100% |
| hybrid-13 | T161 | 100% |
| hybrid-14 | T181 | 100% |
| hybrid-15 | T150 | 100% |
| hand-1 | T235 | 100% |
| hand-2 | T233 | 100% |
| hand-3 | T243 | 100% |
| hand-4 | T259 | 100% |
| hand-5 | T229 | 100% |
| hand-6 | T234 | 100% |
| hand-7 | T238 | 100% |
| hand-8 | T237 | 100% |
| hand-9 | T255 | 100% |
| hand-10 | T287 | 100% |
| hand-11 | T282 | 100% |
| hand-12 | T242 | 100% |
| hand-13 | T239 | 100% |
| hand-14 | T231 | 100% |
| hand-15 | T230 | 100% |
| reference-1 | T125 | 100% |
| reference-2 | T119 | 100% |
| reference-3 | T109 | 100% |
| reference-4 | T126 | 100% |
| reference-5 | T117 | 100% |
| reference-6 | T121 | 100% |
| reference-7 | T100 | 100% |
| reference-8 | T13 | 100% |
| reference-9 | T113 | 100% |
| reference-10 | T166 | 100% |
| reference-11 | T189 | 100% |
| reference-12 | T35 | 100% |
| reference-13 | T106 | 100% |
| reference-14 | T196 | 100% |
| reference-15 | T146 | 100% |
| inline-1 | T152 | 100% |
| inline-2 | T132 | 100% |
| inline-3 | T10 | 100% |
| inline-4 | T163 | 100% |
| inline-5 | T219 | 100% |
| inline-6 | T101 | 100% |
| inline-7 | T23 | 100% |
| inline-8 | T162 | 100% |
| inline-9 | T159 | 100% |
| inline-10 | T120 | 100% |
| inline-11 | T143 | 100% |
| inline-12 | T139 | 100% |
| inline-13 | T116 | 100% |
| inline-14 | T167 | 100% |
| inline-15 | T102 | 100% |
| skills-1 | T169 | 100% |
| skills-2 | T110 | 100% |
| skills-3 | T20 | 100% |
| skills-4 | T217 | 100% |
| skills-5 | T197 | 100% |
| skills-6 | T183 | 100% |
| skills-7 | T138 | 100% |
| skills-8 | T130 | 100% |
| skills-9 | T148 | 100% |
| skills-10 | T202 | 100% |
| skills-11 | T155 | 100% |
| skills-12 | T165 | 100% |
| skills-13 | T123 | 100% |
| skills-14 | T135 | 100% |
| skills-15 | T141 | 100% |

No person scores the judge. Each score it gives quotes an evidence line, and the share
of those lines found in the tree they were quoted from is one check on it; the other
vendor's judge, below, is the second.

## The other vendor's judge

Not run: no other vendor's judging was read for this round, so the judge is checked only
by its evidence lines.

## Verdict vector

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
