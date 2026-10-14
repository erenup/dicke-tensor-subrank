# Paper results and their checks

The guide begins with diagonal extraction and follows the entropy
argument through coordinate selection to the asymptotic bound. The
numbering below is read from [the paper source](../paper/main.tex).
There are ten numbered results. No numbered corollaries, definitions
or remarks occur in this version.

| Paper result | Label | Coverage |
| --- | --- | --- |
| Theorem 1.1: main entropy formula and finite upper bound | `thm:main` | Paper only; finite components are mapped below |
| Lemma 3.1: limits and unbounded subsequences | `lem:limits` | Paper only |
| Lemma 4.1: supermodularity | `lem:supermodular` | Paper only |
| Lemma 4.2: irreducible invariance | `lem:invariant` | Partial Lean coverage: abstract density argument |
| Lemma 5.1: fixed-coordinate fiber entropy | `lem:fiber-entropy` | Exact checks for specified finite cases |
| Lemma 6.1: average-free sets | `lem:average-free` | One exact finite instance; the construction and estimate are paper only |
| Lemma 7.1: uniform reduction of ranks | `lem:rank-reduction` | Paper only |
| Lemma 10.1: coordinatewise product dimension | `lem:product-dimension` | Paper only |
| Lemma 10.2: diagonal slice rank | `lem:diagonal-slice` | Paper only |
| Proposition 10.3: finite-power upper bound | `prop:upper` | Paper only |

## 1. From Dicke tensors to an entropy-determined growth rate

Theorem 1.1 is over the complex numbers, for every positive multiplicity
tuple with at least two symbols. All original modes remain separate.
Both ordinary and coordinate-restriction asymptotic subrank equal the
exponential of Shannon entropy. The finite upper bound holds for every
positive power. The full result and the tensor definitions are in the
paper; `TR28.core_theorems` is a conjunction of finite algebraic targets,
not this theorem.

## 2. Relation to earlier work

This section fixes the source convention and separates coordinate
restrictions from the cited monomial-degeneration convention. It has
no numbered result or direct Lean target. The notation comparison and
literature discussion are part of the paper. Related conditional-entropy
and group-action results provide context; no dynamical-entropy theorem
is used as a direct input to the finite Shannon-entropy proof.

## 3. Powers, limits and the two-factor case

Lemma 3.1 proves supermultiplicativity, existence of the logarithmic
subrank limits and the passage from any unbounded subsequence. These
steps, the flattening bound and the separate two-factor calculation are
paper only. Finite supporting computations do not establish these
limits.

## 4. An entropy inequality from irreducible invariance

Lemma 4.1 identifies a supermodular function on rational subspaces using
conditional mutual information and quotient labels. There is no Lean
definition of Shannon entropy in this core, so the lemma is paper only.

Lemma 4.2 uses that functional and an irreducible group action. The
theorem `TR28.invariant_supermodular_density` in
[Density.lean](../lean/TR28/Density.lean) proves the abstract algebraic
maximizer argument. Its explicit hypotheses are finite positive rational
dimension, a real function with finite range and value zero at the zero
subspace, supermodularity, invariance and irreducibility. The subspace
lattice need not be finite. The existence of a maximizing slope and the
dimension comparison are conclusions of the proof.

Identifying this function with quotient entropy, checking all its
hypotheses and identifying its value at the full space remain in the
paper. Thus this is partial coverage of Lemma 4.2.

## 5. Permutation fibers and counts over the full support

Lemma 5.1 is the conditional-distribution application of Lemma 4.2.
Translation into the collision space, irreducibility of the concrete
permutation action and the entropy averaging argument are paper only.

`check_entropy.py:check` verifies the equivalent integer inequality for
all nonzero difference-generated collision subspaces in one fixed
shared mode for five multiplicities:

| Multiplicities | Support size | Nonzero collision subspaces |
| --- | ---: | ---: |
| `(1,1,1)` | 6 | 1 |
| `(2,1,1)` | 12 | 7 |
| `(1,1,1,1)` | 24 | 13 |
| `(2,2,1)` | 30 | 191 |
| `(3,1,1)` | 20 | 176 |

`check_hashing.py:check_fibers` checks 405 rank-one cases, with shared
mode counted, across `(2,1)`, `(1,1,1)`, `(2,2)`, `(2,1,1)`,
`(1,1,1,1)`, `(3,1,1)` and `(2,2,1)`. These are finite supporting
checks, not the all-subspace entropy proof.

The integer-product part of equation `eq:fiber-count` is covered by
[Counting.lean](../lean/TR28/Counting.lean):

| Lean theorem | Exact conclusion |
| --- | --- |
| `TR28.partner_position_count` | The full partner count factors over positions |
| `TR28.partner_histogram_count` | The product is regrouped by the first word's histogram |
| `TR28.balanced_partner_count` | The balanced first word gives a common exponent in the product |
| `TR28.exact_span_partner_subset` | Exact-span partners belong to the full coset-partner set |
| `TR28.exact_span_partner_bound` | Their number is bounded by the full fiber product |

The second word is never restricted to the candidate joint type.
Identifying the product with an exponential of entropy and applying
Lemma 5.1 remain in the paper. The multinomial estimate
`eq:type-count` is also paper only.

## 6. Large average-free sets

Lemma 6.1 gives the no-carry sphere construction and its size estimate
for every fixed `L >= 2` and sufficiently large integer `q`.
These universal statements are paper only.

`check_hashing.py:validate_average_free` checks the particular set
`B={0,1,3}` modulo `11` for `L=2`; it rejects `B={0,1,2}`.
This checks the property of that small set, not the existence or size
assertions of the lemma.

## 7. Hashes and exact survival probabilities

Lemma 7.1 bounds integer minors to obtain a uniform prime threshold.
It is paper only. The theorem `TR28.finite_field_kernel_count` in
[LinearCount.lean](../lean/TR28/LinearCount.lean) supplies one ingredient
of `eq:pair-survival`: the kernel of an actual finite-field linear map
has cardinality `|K|^(N-rank(A))`. The rank is computed from the map,
rather than supplied as a conclusion-shaped hypothesis.

Constructing the hash constraint map, proving its rational rank,
transferring that rank modulo a large prime, and justifying removal of
the redundant row remain in the paper. The general single and pair
survival probabilities are not Lean statements.

`check_hashing.py:test_hash` enumerates all `11^5=161051` assignments
for the three-column support `(-1,-1,2)` and its permutations, with
`N=3`, `q=11` and `B={0,1,3}`. It checks all 27 original edges, six
candidates and 54 ordered candidate/collider pairs. Every edge survives
3993 assignments; every listed pair survives 363. This is one exact
finite experiment.

## 8. Isolation against the full original support

[Isolation.lean](../lean/TR28/Isolation.lean) proves:

| Lean theorem | Exact conclusion |
| --- | --- |
| `TR28.isolation_count` | `X <= number_of_isolated_candidates + Y`, with `Y` counting ordered collisions against all surviving original edges |
| `TR28.exact_coordinate_extraction` | For a positive number of modes, keeping the coordinate images of computed isolated candidates leaves exactly those candidates; every coordinate map is injective |
| `TR28.uniform_isolation_extraction` | On a nonempty finite uniform sample space, one sample gives this extraction and the cross-multiplied bound by the mean of `X-Y` |

The first theorem permits zero modes; extraction requires a positive
number of modes. The candidates are a subset of the literal original
support. Neither isolation nor a bound on the isolated set is assumed
as a premise.

These are the finite support statements underlying
`eq:expected-diagonal`. Interpreting an induced matching as a tensor
diagonal after independent local relabelling remains in the paper.
The exponential expected-collision estimate also uses the entropy and
hashing steps described above. The finite hashing experiment checks
extraction against the entire original support and rejects a control
with a hidden mixed edge outside the candidate set.

## 9. The entropy lower bound

The prime-indexed choice of powers, decay of the collision ratio,
average-free size estimate, limit passage and removal of the positive
parameter are paper only. Equation `eq:monomial-lower` and the
coordinate-restriction asymptotic bound are not Lean conclusions.

## 10. The upper bound for arbitrary linear restrictions

Lemma 10.1 proves the dimension inequality for coordinatewise products
over the complex numbers. Lemma 10.2 derives the slice rank of a
diagonal and the bound of subrank by slice rank. Proposition 10.3 uses
a probability-score count to cover the entire power by at most
`k exp(N H(p))` slices. All three results and their application to
arbitrary independent complex-linear restriction maps are paper only.

## 11. Exact finite verification

Equation `eq:integer-entropy-check` states the integer form used by
`check_entropy.py`. Both checkers use exact integer or rational
arithmetic, explicit failure exits and substantive negative controls.
Their mathematical output agrees under normal and optimized Python.
See [verification](../verification/README.md) for commands and scope.

The mapping checker verifies source links and the full numbered-result
inventory. The Lean audit separately checks the ten exact proposition
types and their conjunction, with permitted axioms only. Neither the
mapping check nor the finite computations replace the paper's entropy,
rank-transfer, asymptotic or upper-bound arguments.
