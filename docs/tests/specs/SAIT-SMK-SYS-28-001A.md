---
id: SAIT-SMK-SYS-28-001A
title: Section files hold every adopted rule, read on demand from a map
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-11-15
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, composition, delivery, determinism]
---

## Short description

> **Given** a chain of templates and the sections a project declines
> **When** `resolve_chain.py --emit --sections` builds one file per topic
> and the root file's map
> **Then** the section files together hold exactly the rules the inlined
> root file holds, each copy of a rule matches its source, a file carries
> every section it extends or names, and the root file holds only the map,
> read on demand, because a rule no file holds is one the agent never
> reads, and a copy that differs contradicts its source

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The planted placements are right, each planted fault is reported, every root built alone passes, and two runs under different hash seeds write the same bytes |
| FAILED | A planted placement is wrong, or a planted fault goes unreported |
| FAILED | A root's section files miss an adopted rule, hold a line no adopted rule is, hold two different copies of one block, or name a section they do not carry |
| FAILED | A root's root file holds a rule, maps a section file other than once, maps a file not emitted, or does not say to read a file on demand |
| FAILED | The two runs differ, or the emitter exits non-zero |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on planted templates and on every root, built in memory, and
on two roots written to a temporary directory that is removed afterwards)

### Execution

1. Build a planted base template, a planted layer that extends one of its
   sections, overrides another and names the first in its title's rules,
   and a planted template with rules under its title alone, declining one
   base section; add a three-level override chain, each level declaring an
   ID of its own, and a template whose extension runs past its heading to
   the next ID, which names and extends the chain's first ID
2. Build every root `--roots` lists on its own, as section files and with
   skills inlined
3. Cut every section file at its headings, keep one copy of each block,
   and count its lines against the inlined root file's rule lines
4. Plant three faults in the planted output: a file dropped, a copy
   edited, and a carried section removed
5. Run `resolve_chain.py --emit --sections` on `backend-auth` and
   `backend-database` twice, with `PYTHONHASHSEED` 1 and 2, and compare
   the trees byte for byte

### Assertions

1. Assert the planted override replaces its base, the declined section is
   absent, the checked rule is left to its check with its command kept,
   and the procedure is in a section file and not in the root file
2. Assert a section's file carries its extension after it, and the
   extension's file carries the section before it, for every heading the
   extension's section runs over and for none after the next ID
3. Assert a file carries the rules under its template's title and every
   section those name, and the bare title gets a file of its own
4. Assert each replaced level of the override chain is out, and a section
   naming or extending its first ID carries the last override, which
   carries that extension in turn
5. Assert, for the planted chain and every root, that the lines held equal
   the adopted lines, that two copies of a block never differ, and that a
   file naming a section in backticks carries its rules
6. Assert the root file maps each section file once, maps no other, holds
   no rule line, and says not to read the files before the work starts
7. Assert each planted fault is reported
8. Assert the two runs write the same files with the same bytes

### Negative controls

1. **No extension carried.** With the extension relation ignored, the
   planted base section's file lacks its extension and the check fails
2. **No name followed.** With the names in a title's rules ignored, the
   planted layer's files name a section they do not carry and the check
   fails
3. **The planted faults.** A dropped file, an edited copy and a removed
   carried section each fail the counts or the copy comparison; the check
   runs all three on every run
4. **A relationship tied to its heading.** With an extension or an
   override given only to the heading whose tags name it, the extension's
   second heading and the section it extends lack each other's rules, and
   the check fails
5. **An override chain cut short.** With an override's relationship read
   only from the rows that survive, a section naming or extending the
   chain's first ID lacks the last override, and the check fails

## Related

- ADR-060: the emitter builds section files read on demand
- SYS-26: the emitter places each section by its load
- SYS-27: an emitted file names no template file, section files included
