# Verification

The finite algebraic core and exact checks have the scope recorded in
[lean/SCOPE.md](lean/SCOPE.md) and the [result map](paper-lean-mapping/by-section.md).
The full entropy and asymptotic theorem is proved in the paper.

## Exact supporting computations

From the repository root, using Python 3.10 or later:

```sh
python3 -I -B verification/run.py
python3 -I -B -O verification/run.py
```

Both commands exited successfully, with empty stderr and byte-identical stdout:

```text
PASS: check_entropy.py (normal, optimized, hash-seed; registered output)
PASS: check_hashing.py (normal, optimized, hash-seed; registered output)
PASS: 16 integrity controls; 3 proof bindings
RESULT: PASS TR-28 finite supporting checks
```

Each entry-point invocation checks both exact programs normally, under `-O`,
and with a second hash seed. The finite mathematical checks include five
lowered-rank controls and three hashing/isolation controls. All eight reject;
the entry point also rejects 16 integrity mutations and checks three proof
bindings. The programs use integer and rational arithmetic only.
The output SHA-256 for either entry-point command is
`37feb8ce1349eaee0e855fc994b1c5034ca3656a24a48897c7d4493cb57caef6`.

## Manuscript

From `paper/`, with LaTeX, BibTeX and `latexmk` installed:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The build produced 17 pages. The final LaTeX log contained no warnings,
undefined references, or overfull/underfull boxes. The supplied `paper/main.pdf`
is the resulting PDF; its metadata author and the manuscript's author and
acknowledgement fields are `TBD`. The example, notation table, theorem, entropy discussion and final bibliography
were visually checked in the built PDF.
PDF SHA-256:
`4091c572d3334e3c4589a2911dafd1567e09a3b53c52dc9bef4641834132af8c`.

The source manifest binds the README, bibliography and all eight TeX files.
The root tree manifest also binds the PDF. Rebuilding a PDF can change its
creation metadata, so the source manifest does not require byte identity of
an independently rebuilt PDF.

## Lean finite algebraic core

From `lean/`, with the pinned Lean toolchain, Python 3.11 or later, Git and GNU time:

```sh
lake exe cache get
./verify
```

The audit used the pinned dependency cache and built all eight project modules
from source into a new isolated object directory. The dependency revisions and
compiler were authenticated. Existing project objects were excluded from the
build search path. The pre-build controls agreed byte for byte under normal
and optimized Python. Summary lines:

```text
PASS 67 pre-build integrity controls; no Lean build performed
PASS: pre-build audit controls agree under Python optimization
PASS: 8 fresh modules; 22 exact-type examples; 11 axiom targets; 1 positive and 4 negative controls.
```

The first line describes the pre-build controls; the fresh Lean build follows
inside the same `./verify` command. The four false-statement controls reject
incorrect full-partner counting, incorrect kernel counting, candidate-only
isolation, and extraction with zero modes.

Every target and their conjunction had precisely these transitive axioms:

```text
'TR28.partner_position_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.partner_histogram_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.balanced_partner_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.exact_span_partner_subset' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.exact_span_partner_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.finite_field_kernel_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.isolation_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.exact_coordinate_extraction' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.uniform_isolation_extraction' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.invariant_supermodular_density' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR28.core_theorems' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The audit used two Lean workers with modules compiled serially. It completed
in 43.955 seconds with a maximum recorded process RSS of 3,316,400 KiB,
using the existing dependency cache. The audit enforces `-M6000`, a measured
7 GiB per-invocation RSS ceiling and a 90-minute total limit. Dependency
installation and cache retrieval are separate from this timing.
The receipt records each command, source hash, result and generated object;
its location is printed after the summary under `lean/.lake/`.

## Paper-to-Lean mapping

From the repository root:

```sh
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
```

Both commands exited successfully with empty stderr and identical output:

```text
PASS: 10 numbered results in 11 paper sections
PASS: 10 finite Lean targets and their aggregate declaration
PASS: 4 exact-check links and 8 supporting paper anchors
PASS: 14 mapping negative controls
RESULT: PASS mapping structure; mathematical coverage is stated per entry
```

The checks require all numbered results, paper labels, mapped Lean declarations
and their proposition types, and mapped exact-check functions to exist.
Comments cannot supply a missing Lean declaration. The 14 negative controls
exercise omitted results, missing declarations, wrong types, absent anchors,
unsupported numbering and malformed metadata. The checker validates the
correspondence structure; it does not replace Lean compilation or a proof
of the paper-only results.

## File integrity

From the repository root:

```sh
sha256sum -c MANIFEST.sha256
```

The manifest lists every supplied file except itself. Dependency caches and
auxiliary build files are excluded. The paper has its own source manifest;
its compiled PDF is included in the root manifest.
