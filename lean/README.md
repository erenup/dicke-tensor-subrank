# TR-28: universal finite algebraic and combinatorial core

`TR28.core_theorems : TR28.CoreTheorems` proves ten universal targets used in the
[written proof](../verification/core/proofs/PROOF.md) and [paper](../paper/main.pdf): exact partner counts, a rational
collision-span bound, a finite-field kernel count, full-support isolation and
coordinate extraction, and an abstract invariant-supermodular dimension bound.
The entropy formula and asymptotic subrank theorem additionally require the
handwritten steps listed below.

The exact scope is in [SCOPE.md](SCOPE.md). [Definitions.lean](TR28/Definitions.lean)
defines the literal objects, [Statement.lean](TR28/Statement.lean) gives all ten
target propositions, and [Proofs.lean](TR28/Proofs.lean) assembles their proofs.

| Universal target | Exact result and hypotheses |
| --- | --- |
| `PartnerPositionCount` | For any finite alphabet, word length, relation and first word, the number of all partner words is the product of the actual relation-fiber sizes over positions. |
| `PartnerHistogramCount` | The same full-support count is regrouped by the actual complete histogram of the first word. |
| `BalancedPartnerCount` | If each symbol occurs `c` times in the first word, the count is the product of the fiber sizes raised to `c`. The second word has no histogram restriction. |
| `ExactSpanPartnerSubset` | Partners whose actual rational difference span equals a prescribed subspace lie in the full set of its coset partners. |
| `ExactSpanPartnerBound` | For a balanced first word, that exact-span partner count is bounded by the full coset-fiber product. |
| `FiniteFieldKernelCount` | Over any finite field `K`, an actual map `A : K^N → K^r` has exactly `|K|^(N - finrank(range A))` homogeneous solutions. Rank-nullity justifies the natural subtraction; the rank is computed from `A`. |
| `IsolationCountTheorem` | For candidates contained in an original finite support, `X ≤ isolated + Y`, where ordered collisions compare each surviving candidate against every distinct surviving original edge sharing a coordinate. |
| `ExactCoordinateExtraction` | With a positive number of modes, restricting the original support to the coordinate images of the computed isolated candidates leaves exactly those candidates; every coordinate projection is injective on them. |
| `UniformIsolationExtraction` | For a nonempty finite sample type and sample-dependent filters, one sample gives that exact extraction and injectivity with `sum X ≤ |samples| * isolated + sum Y`. The formula uses no truncated subtraction. |
| `InvariantSupermodularDensity` | On an actual positive finite-dimensional rational vector space `E`, a finite-range real function `F` on submodules, with `F(⊥)=0`, explicit supermodularity, invariance under a family of linear automorphisms and irreducibility of that family, satisfies `F(V)*dim(E) ≤ dim(V)*F(⊤)` for every submodule `V`. |

The propositions quantify over ordinary Lean `Type`, without a maximum support
size, dimension, word length or sample count. Empty alphabets, empty supports,
zero word length and empty products have their ordinary meanings. Kernel counting
allows zero domain and codomain dimensions. Isolation counting allows zero modes;
coordinate extraction and its sampled version require a positive number of modes.
The density theorem assumes neither positivity of `F`, a finite submodule lattice,
a maximizing witness nor the desired density bound. Coordinate types in the
support theorems need not be finite; the supports themselves are finite sets.

The proofs are in [Counting.lean](TR28/Counting.lean),
[LinearCount.lean](TR28/LinearCount.lean), [Isolation.lean](TR28/Isolation.lean) and
[Density.lean](TR28/Density.lean). [TR28.lean](TR28.lean) imports their assembly.

## What remains handwritten

- Shannon entropy and the actual quotient-entropy functional's supermodularity,
  finite range and invariance; irreducibility of the concrete permutation action;
  the conditioning and averaging argument for Lemma 3 of the written proof.
- The balanced multinomial estimate (7), average-free set construction, and
  preservation of rational/integer ranks modulo sufficiently large primes.
- The specific hash maps, pair probabilities and rank of their constraint
  matrices; their combination into the exponential expected-collision bound.
  The abstract kernel count alone establishes none of those identifications.
- Interpreting the extracted support as a diagonal tensor after local coordinate
  relabelling, existence of the subrank limit and the asymptotic lower bound,
  the slice-rank upper bound, and the cited external tools.

This package therefore supplies no Lean theorem of the full Dicke entropy/subrank
formula or of a finite subrank, rank or border-rank formula. Every original tensor
mode remains separate; no regrouping of modes is used. The supporting
[Python checks](../verification/README.md) use exact integer/rational arithmetic
and are not premises of these universal Lean targets.

## Build and audit

Lean `v4.34.0-rc2` and Mathlib
`85e3a25e006c35636f0e53b0e9296caca2685bc0` are pinned. With the toolchain available
through Lake, Python 3.11 or later, Git and GNU time (`/usr/bin/time`), run
from this directory:

```sh
lake exe cache get
./verify
```

The first command obtains the official dependency cache. The verification script
runs the verifier's rejection tests in normal and optimized Python, requires
identical output, and then authenticates its inputs and compiles the eight project modules into a fresh isolated
object directory, checks 22 exact types and eleven transitive-axiom probes, and
runs a positive regression module and four mathematical false-statement controls.
It records the bound inputs, commands, logs and generated objects in a build
receipt under `.lake/`. Existing project objects cannot replace the fresh build;
the dependency cache is neither cleaned nor rebuilt by the audit.

Only `propext`, `Classical.choice` and `Quot.sound` are permitted as transitive
axioms. The audit rejects placeholders, custom axioms, unsafe replacements,
native computation oracles and checking overrides. It builds modules serially
with two Lean workers and `-M6000`, checks measured peak RSS against 7 GiB and
enforces a 90-minute limit. The dependency cache is a build prerequisite; the
project sources and exact-type probes are always rebuilt from scratch.
