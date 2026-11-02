# From diagonal extraction to the entropy law

Start with the three-mode tensor

```math
D_{(2,1)}=e_1\otimes e_1\otimes e_2+
  e_1\otimes e_2\otimes e_1+
  e_2\otimes e_1\otimes e_1.
```

Its subrank asks how large a diagonal tensor
$`\Delta_q=\sum_{j=1}^q e_j\otimes e_j\otimes e_j`$
can be obtained by independent linear maps on its three factors.
The grouped power $`D_{(2,1)}^{\boxtimes N}`$ still has three factors;
each has dimension $`2^N`$. This is the case $k=3$ of the example
$`\mathbf d=(k-1,1)`$ in Section 1 of the paper, and Theorem 1.1
identifies the exponential growth rate of the largest diagonal:

```math
\widetilde Q(D_{(2,1)})=2^{H_2(2/3,1/3)}
  =\frac{3}{2^{2/3}}\approx1.8899.
```

This is a limit of $N$th roots, rather than a formula for the
integer subrank at each finite power. For every positive multiplicity
tuple $\mathbf d$ with at least two symbols, the same theorem gives
$`\exp H(\mathbf d/k)`$, with $`k=\sum_a d_a`$ separate factors.
The lower bound uses coordinate restrictions, which keep selected
local basis vectors and then allow independent relabelling and rescaling.

The theorem settles the leading diagonal-growth exponent for every
fixed positive multiplicity tuple: it is determined by the symbol
entropy. Section 2 of the paper relates this conclusion to the 2015
conversion-cost proposal, the 2025 ordinary-subrank conjecture and the
monomial-degeneration convention of the 2019 question. The theorem does
not give exact subrank at each finite power, an efficient extraction
algorithm or a convergence rate uniform over multiplicity tuples.

| Symbol | Meaning |
| --- | --- |
| $k$ | Number of separate tensor factors |
| $N$ | Number of copies in the grouped power |
| $Q$, $`Q_{\mathrm M}`$ | Ordinary and coordinate-restriction subrank |
| $`p_a=d_a/k`$ | Symbol distribution |
| $H(p)$, $`H_2(p)`$ | Shannon entropy in natural and base-two logarithms |
| $`F_X(V)`$ | $`H(X\mid X\bmod V)`$, with the coset label as conditioning variable |

## Symmetry, entropy, and selection

The entropy inequality of Section 4 concerns a finite-support random
variable $X$ in a positive finite-dimensional rational vector space $E$.
If its law is invariant under an irreducible rational linear group
action, then every rational subspace $V\leq E$ satisfies

```math
H(X\mid X\bmod V)\leq\frac{\dim V}{\dim E}H(X).
```

Supermodularity (Lemma 4.1) and irreducibility prove this bound
(Lemma 4.2). Applied in Section 5 to the permutation-symmetric
conditional distributions of a Dicke support, it controls how many
full-support partners can collide with a candidate of one full joint
type. Average-free sets (Section 6) and rank-dependent hashes
(Section 7) then allow coordinate selection. Isolation is checked
against the entire original support, including edges outside the
candidate class (Section 8), and Section 9 passes to the asymptotic
lower bound. A slice cover supplies the upper bound for arbitrary
complex-linear restriction maps (Section 10).

Read [by-section.md](by-section.md) alongside the
[paper](../paper/main.pdf). It follows the eleven numbered sections and
lists every numbered result. [mapping.json](mapping.json) records the
paper title, the section titles, the exact paper labels, Lean
declarations, Python functions, and coverage limits.

## What each kind of evidence establishes

The [Lean core](../lean/README.md) proves ten universal finite algebraic
targets: five partner-counting results, a finite-field kernel count,
three isolation and extraction results, and an abstract invariant
supermodular density theorem. Their conjunction is
`TR28.core_theorems`.

The abstract density theorem is only part of Lemma 4.2. It assumes a
finite-range supermodular invariant real function on rational
subspaces. Shannon entropy, the verification of these assumptions for
the quotient-entropy function, and the concrete permutation action
remain in the paper. Likewise, the kernel theorem does not identify
the rank of an integer hash matrix after reduction modulo a prime.
No complete numbered paper result is claimed to be formalized in Lean.

The [exact Python checks](../verification/README.md) enumerate specified
finite collision spaces and one complete hashing experiment, as
described in Section 11 of the paper. They check integer or rational
inequalities and include false inputs that must be rejected. Their
finite ranges are recorded in the mapping; they do not establish the
all-multiplicity theorem by extrapolation.

The entropy identification, modular rank transfer, average-free size
estimate, asymptotic bridge and slice-rank upper bound are proved in
the paper. In particular, the asymptotic theorem is a written result
with formalized finite components, rather than a complete Lean theorem.

## Check the correspondence

From the repository root, run:

```sh
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
```

The standard-library script builds indexes of the TeX and Lean sources.
It checks the paper title and its PDF metadata title, every numbered
section title, and the complete numbered-result inventory in TeX order,
including shared section-based numbering and the bracketed result
names. It also checks all mapped paper anchors; actual Lean
declarations, their named proposition types and the target registry;
the mapped Python functions; and both tables and all section headings
of [by-section.md](by-section.md). Comments cannot supply a missing
Lean declaration. Unsupported counter changes, missing or extra paper
inputs, missing links, duplicate JSON keys, omitted results and
unlabelled results fail closed.

Twenty-three in-memory negative controls exercise these checks without
changing the sources, including a stale paper title, an obsolete
section title, a reinstated section file, a renamed result and a stale
table row. Both commands print the same output. This checks the
correspondence and its coverage labels; it does not compile Lean,
build the PDF or execute the mathematical Python checks. Their separate
commands are in [Lean verification](../lean/README.md) and
[exact verification](../verification/README.md).
