# Verification

The finite algebraic core and exact checks have the scope recorded in
[lean/SCOPE.md](lean/SCOPE.md) and the [result map](paper-lean-mapping/by-section.md).
The full entropy and asymptotic theorem, Theorem 1.1 of the
[paper](paper/main.pdf), is proved in the paper. The Python outputs below
were observed on 2026-11-01 with Python 3.12. All Python programs use only
the standard library.

## Exact supporting computations

From the repository root:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
```

Both commands exited successfully, with empty stderr and byte-identical stdout:

```text
PASS: check_entropy.py (normal, optimized, hash-seed; registered output)
PASS: check_hashing.py (normal, optimized, hash-seed; registered output)
PASS: 16 integrity controls; 3 proof bindings
RESULT: PASS TR-28 finite supporting checks
PASS: core/verification/run.py (normal, optimized, hash-seed)
PASS: 17 files authenticated; 6 integrity controls rejected
RESULT: PASS TR-28 exact verification
```

The entry point authenticates every file in `verification/` against its manifest,
binds the child runner `verification/core/verification/run.py` and its manifest by
digest, runs the child in normal, optimized and alternate hash-seed modes with the
same recorded output, and rejects six altered inventories. The child checks both
exact programs normally, under `-O`, and with a second hash seed. The finite
mathematical checks include five lowered-rank controls and three hashing/isolation
controls, as described in Section 11 of the paper. All eight reject; the child also
rejects 16 integrity mutations and checks three proof bindings. The programs use
integer and rational arithmetic only. The output SHA-256 for either entry-point
command is
`9324946bf2ba5102748aeb001d45f29eb55c7f16587445a265d6d70ab6d2467b`.

## Paper-to-Lean mapping

From the repository root:

```sh
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
```

Both commands exited successfully with empty stderr and byte-identical output:

```text
PASS: paper title, 11 numbered section titles and 10 numbered results in TeX order
PASS: 10 finite Lean targets and their aggregate declaration
PASS: 4 exact-check links and 9 supporting paper anchors
PASS: by-section tables and section headings agree with the map
PASS: 23 mapping negative controls
RESULT: PASS mapping structure; mathematical coverage is stated per entry
```

The output SHA-256 for either command is
`8dd64f73d9d034191a4c8fa3c161056f6615fa7d9912c23e93bc9ddd6d073fbc`.
The checks require the paper title and PDF title metadata, all eleven
numbered section titles, all numbered results with their bracketed names,
paper labels, mapped Lean declarations and their proposition types, and
mapped exact-check functions to exist and agree with the map. Both tables
and all section headings of the result map must equal the versions
generated from the map. Comments cannot supply a missing Lean declaration.
The 23 negative controls exercise omitted results, missing declarations,
wrong types, absent anchors, unsupported numbering, malformed metadata, a
stale paper title, obsolete or extra sections, a reinstated or omitted
section file, a renamed result and stale result-map rows and headings.
The checker validates the correspondence structure; it does not replace
Lean compilation or a proof of the paper-only results.

## Markdown math

From the repository root:

```sh
python3 tools/check_markdown_math.py
```

The command exited successfully with empty stderr:

```text
PASS: 16 tracked Markdown files; controls passed
```

The static guard checks all tracked Markdown files against the documented
GitHub math profile and exercises its own controls. It does not replace a
live rendering check.

## Manuscript

From `paper/`, with LaTeX, BibTeX and `latexmk` installed:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The build produced 13 pages. Its LaTeX log contained no warnings,
undefined references or citations, and no overfull or underfull boxes.
The included `paper/main.pdf` has SHA-256
`d4d5c7958b4822cd1cf758bc57b65e0072ddf291258e5eeda0759f68403029d0`.
The extracted text of the included and rebuilt PDFs is identical; its
SHA-256 under `pdftotext -layout` is
`2fd395ab789e13c946b7fb8b54e30697a133b28503caec4f3016169bf492517e`.
PDF container metadata may differ between builds.

The paper manifest lists every file in `paper/` except itself and the
generated `build/` directory: the README, licence, PDF, bibliography and
all six TeX files.

## Lean finite algebraic core

The Lean sources, audit and targets are unchanged by the present version
of the paper. From `lean/`, with the pinned Lean toolchain, Python 3.11 or
later, Git and GNU time:

```sh
lake exe cache get
./verify
```

The run of these commands on 2026-11-01 reported (excerpt):

```text
PASS 67 pre-build integrity controls; no Lean build performed
PASS: pre-build audit controls agree under Python optimization
PASS: 8 fresh modules; 22 exact-type examples; 11 axiom targets; 1 positive and 4 negative controls.
```

As described in the [Lean guide](lean/README.md), the audit compiles the
eight project modules into a fresh isolated object directory, checks 22
exact types and eleven transitive-axiom probes, and runs a positive
regression module and four false-statement controls. The
four false-statement controls reject incorrect full-partner counting,
incorrect kernel counting, candidate-only isolation, and extraction with
zero modes. Only `propext`, `Classical.choice` and `Quot.sound` are
permitted as transitive axioms for each of the following declarations:

```text
TR28.partner_position_count
TR28.partner_histogram_count
TR28.balanced_partner_count
TR28.exact_span_partner_subset
TR28.exact_span_partner_bound
TR28.finite_field_kernel_count
TR28.isolation_count
TR28.exact_coordinate_extraction
TR28.uniform_isolation_extraction
TR28.invariant_supermodular_density
TR28.core_theorems
```

Axiom report: each of the eleven declarations above depends only on these
three axioms; the audit fails otherwise.

The Lean guide also records the dependency pins and resource limits.

## File integrity

From the repository root:

```sh
sha256sum -c SHA256SUMS
```

The root manifest lists every supplied file except itself. Dependency
caches and auxiliary build files are excluded. The paper and verification
folders have their own manifests.
