# The asymptotic subrank of every Dicke tensor

The manuscript [main.tex](main.tex) proves, over the complex numbers, that
for every `n >= 2` and every positive integer tuple `d`, with
`k = sum d_a` and `p = d/k`,

```math
\widetilde Q_{\mathrm M}(D_d)=\widetilde Q(D_d)=\exp H(p)=2^{H_2(p)}.
```

All `k` original factors remain separate. The first quantity uses coordinate
deletion, independent relabelling and rescaling; the second allows arbitrary
independent complex-linear maps. Tensor powers group corresponding factors
only. For every integer `N >= 1`, the manuscript also proves

```math
Q(D_d^{\boxtimes N})\leq k\exp(NH(p)).
```

The lower bound combines an invariant-distribution entropy inequality,
rank-dependent hashing and isolation against the full support. The upper
bound uses a finite slice cover. The two-factor endpoint and the passage
from an unbounded subsequence to the asymptotic limit are included.

The limit is pointwise for each fixed tuple. No uniform convergence rate,
algorithmic efficiency, finite-subrank equality, tensor-rank or border-rank
formula, or conclusion after merging original factors is asserted.

The [statement](../proofs/STATEMENT.md) and [proof](../proofs/PROOF.md)
give the corresponding result in the repository. The manuscript's
[history section](sections/history.tex) distinguishes coordinate restriction
from the monomial degeneration convention in the cited literature. Its
comparison uses ordinary restriction/degeneration equivalence and this
family's matching bounds; it assumes no general equivalence of the two
monomial conventions. The hashing, average-free, isolation and slice-rank
precedents are credited with precise source locators.

## Build

From this directory:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The introduction starts with the three-mode example, a notation table and the
meaning of the entropy growth rate. The proof roadmap centres on the
invariant conditional-entropy lemma. The discussion relates its finite
setting to dynamical-entropy topics without invoking a theorem from them.

The main file reads seven files in `sections/` and the bibliography `refs.bib`.
A LaTeX installation with the packages named in the source, BibTeX and
`latexmk` is sufficient. The built PDF is [main.pdf](main.pdf). Auxiliary files are kept in `build/`.
Authorship and acknowledgements are TBD; the paper license is TBD.

## Exact supporting checks

From this directory:

```sh
python3 -S -s -B ../verification/run.py
```

The existing [verification guide](../verification/README.md) describes the
finite integer and rational checks, registered outputs and rejection
controls. These reproduce the displayed entropy, fiber and hashing examples.
The all-multiplicity theorem rests on the written proof; the finite checks
do not establish it by enumeration. The accompanying [Lean core](../lean/README.md)
proves the universal finite algebraic and combinatorial targets listed in
its [scope document](../lean/SCOPE.md); the entropy and asymptotic steps
remain in the paper. The [numbered-result map](../paper-lean-mapping/by-section.md)
identifies the exact coverage of each result.
