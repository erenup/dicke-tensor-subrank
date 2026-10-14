# From diagonal extraction to the entropy bound

Start with the three-mode tensor

$$
D=e_1\otimes e_1\otimes e_2+
  e_1\otimes e_2\otimes e_1+
  e_2\otimes e_1\otimes e_1.
$$

Its subrank asks how large a diagonal tensor
$\Delta_q=\sum_{j=1}^q e_j\otimes e_j\otimes e_j$
can be obtained by independent linear maps on its three factors.
The grouped power $D^{\boxtimes N}$ still has three factors;
each has dimension $2^N$. The theorem identifies the exponential
growth rate of the largest diagonal:

$$
\widetilde Q(D)=2^{H_2(2/3,1/3)}
  =\frac{3}{2^{2/3}}\approx1.8899.
$$

This is a limit of $N$th roots, rather than a formula for the
integer subrank at each finite power. For every positive multiplicity
tuple $\mathbf d$ with at least two symbols, the same result gives
$\exp H(\mathbf d/k)$, with $k=\sum_a d_a$ separate factors.
The lower bound uses coordinate restrictions, which keep selected
local basis vectors and then allow independent relabelling and rescaling.

The formula settles the leading diagonal-growth exponent for every
fixed positive multiplicity tuple: it is determined by the symbol
entropy. The paper relates this conclusion to the 2015 entropy proposal
and the 2025 ordinary-subrank conjecture. It does not give exact subrank
at each finite power, an efficient extraction algorithm or a convergence
rate uniform over multiplicity tuples.

| Symbol | Meaning |
| --- | --- |
| $k$ | Number of separate tensor factors |
| $N$ | Number of copies in the grouped power |
| $Q$, $Q_{\mathrm M}$ | Ordinary and coordinate-restriction subrank |
| $p_a=d_a/k$ | Symbol distribution |
| $H(p)$, $H_2(p)$ | Shannon entropy in natural and base-two logarithms |
| $F_X(V)$ | $H(X\mid X\bmod V)$, with the coset label as conditioning variable |

## Symmetry, entropy, and selection

The central entropy lemma concerns a finite-support random variable
in a positive finite-dimensional rational vector space $E$.
If its law is invariant under an irreducible rational linear group
action, then every rational subspace $V\leq E$ satisfies

$$
H(X\mid X\bmod V)\leq\frac{\dim V}{\dim E}H(X).
$$

Supermodularity and irreducibility prove this bound. Applied to the
permutation-symmetric conditional distributions of a Dicke support,
it controls how many full-support partners can collide with a candidate.
Average-free sets and rank-dependent hashes then allow coordinate
selection. Isolation is checked against the entire original support,
including edges outside the candidate class. A slice cover supplies
the upper bound for arbitrary complex-linear restriction maps.

Related work on conditional entropy, group actions and sequence entropy
provides background for this viewpoint. No theorem about dynamical
entropy or independence tuples is used as a direct substitute for this
finite Shannon-entropy argument or its induced-matching construction.

Read [by-section.md](by-section.md) alongside the
[paper](../paper/main.pdf). It follows this chain and lists every numbered
result. [mapping.json](mapping.json) records the exact paper labels,
Lean declarations, Python functions, and coverage limits.

## What each kind of evidence establishes

The [Lean core](../lean/README.md) proves ten universal finite algebraic
targets: five partner-counting results, a finite-field kernel count,
three isolation and extraction results, and an abstract invariant
supermodular density theorem. Their conjunction is
`TR28.core_theorems`.

The abstract density theorem is only part of the entropy lemma. It
assumes a finite-range supermodular invariant real function on rational
subspaces. Shannon entropy, the verification of these assumptions for
the quotient-entropy functional, and the concrete permutation action
remain in the paper. Likewise, the kernel theorem does not identify
the rank of an integer hash matrix after reduction modulo a prime.
No complete numbered paper result is claimed to be formalized in Lean.

The [exact Python checks](../verification/README.md) enumerate specified
finite collision spaces and one complete hashing experiment. They check
integer or rational inequalities and include false inputs that must be
rejected. Their finite ranges are recorded in the mapping; they do not
establish the all-multiplicity theorem by extrapolation.

The entropy identification, modular rank transfer, average-free size
estimate, asymptotic bridge and slice-rank upper bound are proved in
the paper. In particular, the asymptotic theorem is a written result
with formalized finite components, rather than a complete Lean theorem.

## Check the correspondence

From the repository root, run:

```sh
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
```

The standard-library script builds indexes of the TeX and Lean sources.
It checks the complete numbered-result inventory in TeX order, including
shared section-based numbering; all mapped paper anchors; actual Lean
declarations, their named proposition types and the target registry;
and the mapped Python functions. Comments cannot supply a missing Lean
declaration. Unsupported counter changes, missing links, duplicate JSON
keys, omitted results and unlabelled results fail closed.

Fourteen in-memory negative controls exercise these checks without
changing the sources. Both commands print the same output. This checks
the correspondence and its coverage labels; it does not compile Lean,
build the PDF or execute the mathematical Python checks. Their separate
commands are in [Lean verification](../lean/README.md) and
[exact verification](../verification/README.md).
