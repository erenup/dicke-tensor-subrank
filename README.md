# The Entropy Law for the Asymptotic Subrank of Dicke Tensors

Authors: Wenqi Zhu; Chunlin Liu; Kai Zou; Ping Nie.

Wenqi Zhu — Mathematical Institute, Woodstock Road, University of Oxford, Oxford, UK, OX2 6GG — wenqi.zhu@maths.ox.ac.uk

Chunlin Liu — School of Mathematical Sciences, University of Science and Technology of China, Hefei, China

Kai Zou — Mathematical & Engineering Sciences, King's College London, UK — kz@netmind.ai

Ping Nie — David R. Cheriton School of Computer Science, University of Waterloo — ping.nie@uwaterloo.ca

Read the [paper](paper/main.pdf) and its [LaTeX source](paper/main.tex).
The theorem answers the [catalogue question](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/eb7c9d64f91757a82fbe9167e80ab9c1b7f36c22/tensor-computations/TR-28/README.md).

## Main theorem

For every integer $n\geq2$ and every positive integer tuple
$`\mathbf d=(d_1,\ldots,d_n)`$, put $`k=\sum_a d_a`$ and $`p_a=d_a/k`$.
Over $\mathbb C$, let $`D_{\mathbf d}\in(\mathbb C^n)^{\otimes k}`$ be the sum of
all basis tensors $`e_{a_1}\otimes\cdots\otimes e_{a_k}`$ whose words
contain the symbol $a$ exactly $`d_a`$ times. Then

```math
\widetilde Q_{\mathrm M}(D_{\mathbf d})
 =\widetilde Q(D_{\mathbf d})
 =\exp H(p)=2^{H_2(p)}.
```

Here $`H(p)=-\sum_a p_a\log p_a`$ uses natural logarithms and $`H_2`$ uses base two.
The subrank $Q(T)$ is the largest $q$ for which independent complex-linear
maps on the $k$ factors take $T$ to the diagonal
$`\Delta_q=\sum_{j=1}^q e_j^{\otimes k}`$. The coordinate-restriction
subrank $`Q_{\mathrm M}(T)`$ instead uses deletion of local basis vectors
followed by independent relabelling and nonzero rescaling in each factor.
The quantities $\widetilde Q$ and $`\widetilde Q_{\mathrm M}`$ are the
limits of the corresponding subranks of $N$th tensor powers, raised to $1/N$.
All $k$ original modes remain separate; powers group corresponding modes only.
The lower bound is obtained by coordinate restrictions. The upper bound allows
arbitrary linear restrictions and holds at every positive integer power:

```math
Q(D_{\mathbf d}^{\boxtimes N})\leq k\exp(NH(p))\qquad(N\geq1).
```

This is Theorem 1.1 of the paper. The limit is pointwise for each fixed
multiplicity tuple. The theorem makes no claim about a convergence rate
uniform in $\mathbf d$, an efficient algorithm for finding the
restrictions, finite-subrank equality, tensor rank, border rank, or
tensors formed by merging original modes.

When all $`d_a`$ are equal, both asymptotic subranks equal $n$. For
$`\mathbf d=(k-1,1)`$ the value is $`k/(k-1)^{(k-1)/k}`$. For $k=3$
this is the three-mode tensor

```math
D_{(2,1)}=e_1\otimes e_1\otimes e_2
          +e_1\otimes e_2\otimes e_1
          +e_2\otimes e_1\otimes e_1,
```

with $`H_2(2/3,1/3)\approx0.9183`$ and growth base
$`2^{H_2(2/3,1/3)}=3/2^{2/3}\approx1.8899`$. Writing $`q_N`$ for the
subrank of the $N$th grouped power, this means
$`\log_2 q_N=NH_2(p)+o(N)`$ for this fixed tuple; it does not give an
exact finite-power value $`q_N=(1.8899)^N`$.

### Source conventions

This is the ordinary asymptotic-subrank formula in Oneto and Ventura, *Ranks of tensors: geometry and applications*, Bollettino dell'Unione Matematica Italiana 18 (2025), 751–778, [Conjecture 4.26](https://doi.org/10.1007/s40574-025-00472-9). It is equivalently the conversion cost in Vrana and Christandl, *Asymptotic entanglement transformation between W and GHZ states*, Journal of Mathematical Physics 56 (2015), 022204, [equation (40)](https://doi.org/10.1063/1.4908106): input copies per two-level GHZ output have cost $`1/H_2(p)`$.

Christandl, Vrana and Zuiddam, *Asymptotic tensor rank of graph tensors: beyond matrix multiplication*, Computational Complexity 28 (2019), 57–111, [Question 1.58](https://doi.org/10.1007/s00037-019-0172-8), uses a different monomial convention: its $`q_{\mathrm M}`$ is defined via monomial degeneration and monomial border subrank. It is not defined by the coordinate-restriction limit used here. The present lower bound is stronger; the ordinary upper bound then gives, as in equation (2.1) of the paper,

```math
\begin{aligned}
H_2(p)&=\log_2\widetilde Q_{\mathrm M}(D_{\mathbf d})
 \leq q_{\mathrm M}^{\mathrm{CVZ}}(D_{\mathbf d})
 \leq q^{\mathrm{CVZ}}(D_{\mathbf d})\\
 &=\log_2\widetilde Q(D_{\mathbf d})=H_2(p).
\end{aligned}
```

The last comparison uses their Theorem 1.11 for ordinary restriction and degeneration. Their Remark 1.12 explicitly distinguishes monomial restriction from monomial degeneration in general. No general equivalence of those two monomial notions is assumed. Section 2 of the paper also credits the published hashing, average-free, weighted-isolation and slice-rank precedents.

## Evidence status

- **Formally proved in Lean:** ten universal finite algebraic and combinatorial
  targets: three partner-count identities, exact-span partner containment and
  its count bound, finite-field kernel cardinality, the isolation count,
  exact coordinate extraction, finite uniform isolation, and the abstract
  invariant-supermodular dimension bound. The aggregate declaration is
  `TR28.core_theorems`. Only `propext`, `Classical.choice`, and `Quot.sound`
  are permitted axioms. See the [precise scope](lean/SCOPE.md). No complete
  numbered result of the paper is a Lean theorem; Lemma 4.2 has partial
  Lean coverage through its abstract density argument.
- **Exact computation:** standard-library Python checks integer and rational
  identities for the displayed small collision supports, 405 rank-one fibre
  cases, and all 161,051 assignments in the three-mode hashing example
  (Section 11 of the paper). Mathematical and integrity negative controls
  are required to reject.
- **Proved in the paper only:** Theorem 1.1 and the limits of Lemma 3.1;
  supermodularity of the quotient-entropy function (Lemma 4.1) and the
  identification of the abstract functional with quotient entropy;
  concrete irreducibility and conditional entropy (Lemma 5.1); the
  multinomial estimate of Section 5 and the average-free estimate
  (Lemma 6.1); rational-to-modular rank transfer (Lemma 7.1); the
  particular hashing probabilities and the tensor bridge of Sections 7
  and 8; the asymptotic lower bound of Section 9; and the slice-rank upper
  bound of Section 10 (Lemmas 10.1 and 10.2, Proposition 10.3). Finite
  checks do not establish the all-multiplicity theorem by enumeration.
- **Open:** exact finite-power subranks, quantitative convergence uniform
  across multiplicities, and efficient construction of the restrictions are
  not resolved here. A formal proof of the complete entropy and asymptotic
  argument is also outside the supplied Lean core.
- **Review:** the [review record](verification/reviews/README.md) contains
  the independent informal AI-agent audits of the written statement, proof
  and exact checks; the one requested source-convention correction is
  incorporated. Wenqi Zhu checked the complete argument, and Chunlin Liu, a
  co-author working on entropy, reviewed the proof.

## Where to read

Start with the [guide from the question to the checks](paper-lean-mapping/README.md)
and the [paper](paper/main.pdf). Section 1 states Theorem 1.1 and its
definitions, and Section 2 fixes the source conventions. Section 3 proves
existence of the limits and settles the two-factor case. Section 4 proves
the entropy inequality for laws invariant under an irreducible rational
action, and Section 5 applies it to permutation fibers and counts partners
over the full support. Sections 6 to 8 supply average-free sets,
rank-dependent hashing and isolation against the full original support;
Section 9 combines them into the coordinate-restriction lower bound.
Section 10 proves the slice-rank upper bound for arbitrary linear
restrictions, and Section 11 describes the exact finite checks. The
[result map](paper-lean-mapping/by-section.md) states the precise coverage
of each numbered result.

The [mathematical statement](verification/core/proofs/STATEMENT.md), [full proof](verification/core/proofs/PROOF.md)
and [source notes](verification/core/proofs/SOURCES.md) provide a text version with its own
section numbering. For the formal core, read [Definitions](lean/TR28/Definitions.lean),
[Statement](lean/TR28/Statement.lean), then [Proofs](lean/TR28/Proofs.lean).
The [Lean guide](lean/README.md) and [exact-check guide](verification/README.md)
explain how to reproduce the checks.

## Reproduce the checks

From the repository root, with Python 3.11 or later:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
python3 tools/check_markdown_math.py
```

The Python programs use only the standard library. Their normal and optimized
outputs must agree. For the pinned Lean toolchain and dependencies:

```sh
cd lean
lake exe cache get
./verify
```

See [VERIFICATION.md](VERIFICATION.md) for the commands and observed outputs,
and [paper/README.md](paper/README.md) for the manuscript build.

## Layout

- `paper/`: LaTeX source, bibliography, PDF, build guide, licence and source manifest.
- `lean/`: the pinned finite algebraic core and verification script.
- `paper-lean-mapping/`: reading guide and checked numbered-result map.
- `verification/`: one entry point for the exact checks; `core/proofs/` holds the statement, proof and source conventions in text form, and `core/verification/` the exact Python checks and integrity controls.
- `tools/`: a static guard for GitHub Markdown math.

## License and citation

Files outside `paper/` are available under the [MIT license](LICENSE).
The files in `paper/`, including the manuscript source and PDF, are licensed
under [CC BY-SA 4.0](paper/LICENSE).
Citation information is in [CITATION.cff](CITATION.cff).

## Acknowledgements

We thank [NetMind.AI](https://www.netmind.ai/) and [AI4ALPHA](https://www.ai4alpha.ca/) for their support of this project. The research of Wenqi Zhu was also supported by the Engineering and Physical Sciences Research Council under grant EP/Y028872/1, *Mathematical Foundations of Intelligence: An "Erlangen Programme" for AI*.
