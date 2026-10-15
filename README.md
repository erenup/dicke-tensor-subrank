# The asymptotic subrank of every Dicke tensor

Authors: TBD

Start with the $2\times2\times2$ tensor

```math
D_{(2,1)}=e_1\otimes e_1\otimes e_2
          +e_1\otimes e_2\otimes e_1
          +e_2\otimes e_1\otimes e_1.
```

Its only nonzero entries are the three arrangements of two first symbols and
one second symbol. Subrank asks how large a diagonal unit tensor
$`\Delta_q=\sum_{j=1}^q e_j^{\otimes k}`$ can be extracted by independent
complex-linear maps on the $k$ factors. The target diagonal is a different
tensor from the original example.

| Symbol | Meaning | Example |
| --- | --- | --- |
| $n$ | Symbols, or dimension of each original factor | $2$ |
| $\mathbf d$, $`k=\sum_a d_a`$ | Multiplicities and number of original factors | $(2,1)$, $3$ |
| $N$ | Copies of the whole tensor | Any positive integer |
| $`q_N`$ | Subrank of the grouped $N$th power | An integer |
| $p=\mathbf d/k$ | Symbol frequencies | $(2/3,1/3)$ |

Taking $N$ copies keeps $k$ factors by grouping corresponding positions only.
The formula identifies their diagonal-growth rate. In this example,
$`H_2(2/3,1/3)\approx0.9183`$ and the growth base is
$`2^{H_2(2/3,1/3)}=3/2^{2/3}\approx1.8899`$. It means
$`\log_2 q_N=NH_2(p)+o(N)`$ for this fixed tuple; it does not give an exact
finite-power value $`q_N=(1.8899)^N`$.

## Main theorem and what it settles

For every integer $n\geq2$ and every positive integer tuple
$`\mathbf d=(d_1,\ldots,d_n)`$, put $`k=\sum_a d_a`$ and $`p_a=d_a/k`$.
Over $\mathbb C$, let $`D_{\mathbf d}\in(\mathbb C^n)^{\otimes k}`$ be the sum of
all basis tensors whose symbol multiplicities are $\mathbf d$. Then

```math
\widetilde Q_{\mathrm M}(D_{\mathbf d})
 =\widetilde Q(D_{\mathbf d})
 =\exp H(p)=2^{H_2(p)}.
```

Here $`H(p)=-\sum_a p_a\log p_a`$ uses natural logarithms and $`H_2`$ uses base two.
The quantity $\widetilde Q$ allows arbitrary independent complex-linear maps.
The quantity $`\widetilde Q_{\mathrm M}`$ uses coordinate deletion followed by
independent relabelling and nonzero rescaling in each factor. Both are the
limits of the corresponding subranks of $N$th tensor powers, raised to $1/N$.
All $k$ original modes remain separate; powers group corresponding modes only.
The lower bound is obtained by coordinate restrictions. The upper bound allows
arbitrary linear restrictions and holds at every positive integer power:

```math
Q(D_{\mathbf d}^{\boxtimes N})\leq k\exp(NH(p))\qquad(N\geq1).
```

This answers the [catalogue TR-28 question](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/eb7c9d64f91757a82fbe9167e80ab9c1b7f36c22/tensor-computations/TR-28/README.md).
The limit is pointwise for each fixed multiplicity tuple. The theorem makes no
claim about a convergence rate uniform in $\mathbf d$, an efficient algorithm
for finding the restrictions, finite-subrank equality, tensor rank, border
rank, or tensors formed by merging original modes.

Read the [paper PDF](paper/main.pdf) or its [LaTeX source](paper/main.tex).

## Symmetry controls entropy, entropy controls selection

The central lemma concerns a finite-support random variable $X$ in a nonzero
finite-dimensional rational vector space $E$. If its law is invariant under
an irreducible rational-linear group action, then every rational subspace
$V\leq E$ satisfies

```math
H_2(X\mid X\bmod V)\leq\frac{\dim V}{\dim E}H_2(X).
```

The coset label $X\bmod V$ records what remains after quotienting by $V$.
Supermodularity of $`V\mapsto H_2(X\mid X\bmod V)`$ and irreducibility prove
the inequality. Applied to permutation-symmetric conditional distributions,
it controls collision counts. Rank-dependent hashing, average-free sets and
isolation against the **full original support** then yield coordinate
restrictions. A slice-rank upper bound matches their exponential rate.

The full multiplicity formula settles the ordinary asymptotic-subrank question
stated in the 2025 survey and the earlier 2015 conversion-rate question.
It determines exactly how the symbol-frequency entropy governs the leading
size of an extractable diagonal, even though each finite-power subrank is
an integer. The [paper's introduction](paper/main.pdf) explains this meaning
before giving the formal definitions and proof.

## Discussion and open questions

The entropy viewpoint offers a connection to the subjects of
[relative sequence entropy for amenable group actions](https://doi.org/10.1016/j.jde.2025.113582)
and [sequence entropy and IT-tuples for minimal group actions](https://doi.org/10.1016/j.aim.2025.110183).
These are background topics for comparison. No theorem from them is used here,
and no identification with the finite entropy or induced matchings of this
proof is asserted. The paper's discussion distinguishes these settings.

The asymptotic formula is settled for every fixed positive multiplicity tuple.
Exact finite-power values, uniform convergence rates and efficient extraction
remain questions outside the result proved here.

## Source conventions

This is the ordinary asymptotic-subrank formula in Oneto and Ventura, *Ranks of tensors: geometry and applications*, Bollettino dell'Unione Matematica Italiana 18 (2025), 751–778, [Conjecture 4.26](https://doi.org/10.1007/s40574-025-00472-9). It is equivalently the conversion cost in Vrana and Christandl, *Asymptotic entanglement transformation between W and GHZ states*, Journal of Mathematical Physics 56 (2015), 022204, [equation (40)](https://doi.org/10.1063/1.4908106): input copies per two-level GHZ output have cost 1/H_2(p).

Christandl, Vrana and Zuiddam, *Asymptotic tensor rank of graph tensors: beyond matrix multiplication*, Computational Complexity 28 (2019), 57–111, [Question 1.58](https://doi.org/10.1007/s00037-019-0172-8), uses a different monomial convention: its q_M is defined via monomial degeneration and monomial border subrank. It is not defined by the coordinate-restriction limit used here. The present lower bound is stronger; the ordinary upper bound then gives

    H_2(p) = log_2 Qtilde_M^restriction(D_d)
           <= q_M^CVZ(D_d) <= q^CVZ(D_d)
           = log_2 Qtilde(D_d) = H_2(p).

The last comparison uses their Theorem 1.11 for ordinary restriction and degeneration. Their Remark 1.12 explicitly distinguishes monomial restriction from monomial degeneration in general. No general equivalence of those two monomial notions is assumed.


## Evidence status

- **Formally proved in Lean:** ten universal finite algebraic and combinatorial
  targets: three partner-count identities, exact-span partner containment and
  its count bound, finite-field kernel cardinality, the isolation count,
  exact coordinate extraction, finite uniform isolation, and the abstract
  invariant-supermodular dimension bound. The aggregate declaration is
  `TR28.core_theorems`. Only `propext`, `Classical.choice`, and `Quot.sound`
  are permitted axioms. See the [precise scope](lean/SCOPE.md).
- **Exact computation:** standard-library Python checks integer and rational
  identities for the displayed small collision supports, 405 rank-one fibre
  cases, and all 161,051 assignments in the three-mode hashing example.
  Mathematical and integrity negative controls are required to reject.
- **Proved in the paper only:** identification of the abstract functional with
  quotient entropy, concrete irreducibility and conditional entropy, the
  multinomial and average-free estimates, rational-to-modular rank transfer,
  the particular hashing probabilities, and the tensor and asymptotic bridges.
  Limit existence, the slice-rank upper bound, and the full entropy formula
  are not Lean theorems in this repository. Finite checks do not establish
  the all-multiplicity theorem by enumeration.
- **Open questions in this treatment:** exact finite-power subranks, quantitative
  convergence uniform across multiplicities, and efficient construction of the
  restrictions are not resolved here. A formal proof of the complete entropy
  and asymptotic argument is also outside the supplied Lean core.

## Where to read

Start with the [guide from the question to the checks](paper-lean-mapping/README.md)
and the [paper](paper/main.pdf). Its entropy section proves the central
conditional-entropy lemma; the following sections turn it into full-support
selection and combine it with the slice-rank bound. The [result map](paper-lean-mapping/by-section.md)
states the precise coverage of each numbered result.

The [mathematical statement](proofs/STATEMENT.md), [full proof](proofs/PROOF.md)
and [source notes](proofs/SOURCES.md) provide a text version.
For the formal core, read [Definitions](lean/TR28/Definitions.lean),
[Statement](lean/TR28/Statement.lean), then [Proofs](lean/TR28/Proofs.lean).
The [Lean guide](lean/README.md) and [exact-check guide](verification/README.md)
explain how to reproduce the checks.

## Reproduce the checks

From the repository root, with Python 3.10 or later:

```sh
python3 -I -B verification/run.py
python3 -I -B -O verification/run.py
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
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

- `paper/`: LaTeX source, bibliography and built PDF.
- `lean/`: the pinned finite algebraic core and verification script.
- `paper-lean-mapping/`: reading guide and checked numbered-result map.
- `verification/`: exact Python checks and integrity controls.
- `proofs/`: statement, proof and source conventions in text form.

## License and citation

Files outside `paper/` use the [MIT license](LICENSE). The paper license is TBD.
[CITATION.cff](CITATION.cff) records the title and placeholder authorship.

## Acknowledgements

TBD
