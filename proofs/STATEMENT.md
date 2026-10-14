# Theorem: the entropy formula for all Dicke tensors

Let n>=2 and let d=(d_1,...,d_n) be any tuple of positive integers. Put
k=sum_a d_a, p_a=d_a/k, and H(p)=-sum_a p_a log p_a, using natural logarithms.
Over C define

    D_d = sum e_(a_1) tensor ... tensor e_(a_k),

where the sum runs over all words (a_1,...,a_k) in {1,...,n}^k containing
symbol a exactly d_a times.

For a nonzero k-tensor T, its subrank Q(T) is the largest q for which
independently chosen complex linear maps on its k factors take T to

    Delta_q = sum_(j=1)^q e_j tensor ... tensor e_j.

Write T^boxtimes N for the tensor power in which corresponding factors are
grouped, retaining exactly k factors. Define

    Qtilde(T) = lim_(N->infinity) Q(T^boxtimes N)^(1/N).

The limit exists by supermultiplicativity. Relative to the displayed word
bases, let Q_M(T) be the largest diagonal obtainable by independently deleting
local basis vectors, then relabelling and rescaling the retained basis
vectors. Define Qtilde_M analogously. This is the coordinate/monomial
restriction version; always Q_M<=Q.

**Claim. For every n>=2 and every positive integer tuple d,**

    Qtilde_M(D_d) = Qtilde(D_d) = exp H(p) = 2^H_2(p).

Here H_2 uses base-two logarithms. In particular, the ordinary-subrank
equality answers the full catalogue TR-28 question; the monomial equality
also answers the stronger formula in Christandl--Vrana--Zuiddam (2019),
Question 1.58. The ordinary maps need not be symmetric or monomial. All k
modes remain separate throughout; only corresponding modes in repeated
copies are grouped.

The proof establishes the finite-power upper bound

    Q(D_d^boxtimes N) <= k exp(N H(p))  for every N>=1,

and the matching asymptotic lower bound using coordinate restrictions.
The assertion is pointwise in each fixed multiplicity tuple d. It asserts
no convergence rate uniform in d and no algorithmic efficiency bound for
finding the restrictions. It is not a claim about finite subrank being
exp H(p), tensor rank, border rank, or tensors with modes merged together.
Multiplication of D_d by a nonzero scalar leaves the claim unchanged.

Published target: Oneto--Ventura (2025), Conjecture 4.26, and
Vrana--Christandl (2015), Section VI, equation (40). Source records and
precise methodological attribution are in SOURCES.md. The proof of the
claimed equality is given in full in PROOF.md; it does not assume an
unverified all-binary or all-distinct special case.
