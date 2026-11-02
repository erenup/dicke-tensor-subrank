# The Entropy Law for the Asymptotic Subrank of Dicke Tensors

Authors: Wenqi Zhu; Chunlin Liu; Kai Zou; Ping Nie.

Wenqi Zhu — Mathematical Institute, Woodstock Road, University of Oxford, Oxford, UK, OX2 6GG — wenqi.zhu@maths.ox.ac.uk

Chunlin Liu — School of Mathematical Sciences, University of Science and Technology of China, Hefei, China

Kai Zou — Mathematical & Engineering Sciences, King's College London, UK — kz@netmind.ai

Ping Nie — David R. Cheriton School of Computer Science, University of Waterloo — ping.nie@uwaterloo.ca

The [paper](main.pdf) proves Theorem 1.1 over the complex numbers: for
every $n\geq2$ and every positive integer tuple $\mathbf d$, with
$`k=\sum_a d_a`$ and $`p=\mathbf d/k`$,

```math
\widetilde Q_{\mathrm M}(D_{\mathbf d})=\widetilde Q(D_{\mathbf d})=\exp H(p)=2^{H_2(p)}.
```

All $k$ original factors remain separate. The first quantity uses coordinate
deletion, independent relabelling and rescaling; the second allows arbitrary
independent complex-linear maps. Tensor powers group corresponding factors
only. For every integer $N\geq1$, the theorem also states

```math
Q(D_{\mathbf d}^{\boxtimes N})\leq k\exp(NH(p)).
```

The limit is pointwise for each fixed tuple. No uniform convergence rate,
algorithmic efficiency, finite-subrank equality, tensor-rank or border-rank
formula, or conclusion after merging original factors is asserted.

Section 1 states the theorem and Section 2 relates it to earlier work.
That section distinguishes coordinate restriction from the monomial
degeneration convention in the cited literature; its comparison uses the
ordinary restriction/degeneration equivalence and this family's matching
bounds, and assumes no general equivalence of the two monomial conventions.
It also credits the hashing, average-free, isolation and slice-rank
precedents with precise source locators. Section 3 proves existence of the
limits and treats the two-factor case. Sections 4 to 9 give the lower
bound: an entropy inequality for laws invariant under an irreducible
linear action, its application to permutation fibers over the full
support, average-free sets, rank-dependent hashing, isolation against the
full original support, and the passage to the asymptotic limit. Section 10
proves the slice-rank upper bound, and Section 11 describes the exact
finite checks. The [statement](../verification/core/proofs/STATEMENT.md) and
[proof](../verification/core/proofs/PROOF.md) give a text version of the same result.

## Build

The source is [main.tex](main.tex), which reads the five files in
`sections/` and the bibliography [refs.bib](refs.bib). From this directory,
with LaTeX, BibTeX and `latexmk`:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The rebuilt PDF is `build/main.pdf`; it has 13 pages, and the included
[main.pdf](main.pdf) has the same extracted text. A LaTeX installation with
the packages named in the source suffices. [SHA256SUMS](SHA256SUMS) lists
every file in this directory except itself and the generated `build/`
directory. Rebuilding can change PDF container metadata, so a rebuilt PDF
need not match the listed hash of the included one byte for byte.

## Exact supporting checks

From this directory:

```sh
python3 -S -s -B ../verification/run.py
```

The [verification guide](../verification/README.md) describes the
finite integer and rational checks, registered outputs and rejection
controls. These reproduce the entropy, fiber and hashing examples of
Section 11. The all-multiplicity theorem rests on the written proof; the
finite checks do not establish it by enumeration. The accompanying
[Lean core](../lean/README.md) proves the universal finite algebraic and
combinatorial targets listed in its [scope document](../lean/SCOPE.md);
the entropy and asymptotic steps remain in the paper. The
[numbered-result map](../paper-lean-mapping/by-section.md) identifies the
exact coverage of each result.

## License

All files in this directory, including the manuscript source and PDF, are
licensed under [CC BY-SA 4.0](LICENSE).
