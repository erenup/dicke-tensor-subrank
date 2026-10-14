# Entropy and coordinate restrictions for Dicke tensors

All tensor spaces and restriction maps are over C. Auxiliary vector spaces
used for entropy and ranks are over Q. Logarithms are natural. We prove the
entire statement in STATEMENT.md, including its coordinate-restriction
strengthening. The number k of tensor factors is never reduced.

The argument combines rank-dependent tight-support hashing with an entropy
inequality from permutation invariance. We count candidates from one full
joint type, but test their isolation against the entire original support.
Higher-order hashing, average-free sets, and weighted isolation have
published precedents, specified in SOURCES.md. The proofs needed here are
included below; no general tight-tensor asymptotic theorem is invoked.

## 1. Conventions and existence of the limits

Use the definitions of D_d, Q, Q_M, and the grouped power boxtimes in
STATEMENT.md. A coordinate restriction deletes chosen basis vectors in each
factor. If the remaining support consists of q entries that have distinct
coordinates in every factor, relabelling those coordinates takes its
all-one tensor to Delta_q. Such a support is an induced matching.

Both Q and Q_M are at least one on every power of D_d: retain one nonzero
entry. Tensoring two restrictions and identifying each pair of local
output indices with one index shows, for R equal to Q or Q_M,

    R(D_d^boxtimes(N+L)) >= R(D_d^boxtimes N) R(D_d^boxtimes L).       (1)

Also R(D_d^boxtimes N)<=n^N. For ordinary subrank, this follows already
from the rank of the flattening along one factor: it is at most n^N,
cannot increase under restriction, and equals q on Delta_q. Thus, writing
a_N=log R(D_d^boxtimes N) and a_0=0, we have 0<=a_N<=N log n and a_N is
superadditive. Fix m>=1. If N=hm+r, 0<=r<m, then a_N>=h a_m, so

    liminf_(N->infinity) a_N/N >= a_m/m.

Taking the supremum over m proves that the limit of a_N/N exists and
equals sup_m a_m/m. In particular, a lower bound along any unbounded
subsequence is a lower bound for this limit.

If k=2, positivity and n>=2 force n=2 and d=(1,1). Then
D_d=e_1 tensor e_2+e_2 tensor e_1 is a two-by-two permutation matrix.
Its powers have Q_M=Q=2^N, and exp H(1/2,1/2)=2. Henceforth k>=3.

## 2. An invariant entropy inequality

For a finite random variable X in a rational vector space E, and a rational
linear subspace V, write X mod V for its finite-valued coset label and put

    F_X(V)=H(X | X mod V)=H(X)-H(X mod V).

Entropy is the finite Shannon entropy, with 0 log 0=0. We use its chain
rule and nonnegativity of conditional mutual information; these follow
directly from the definition and nonnegativity of relative entropy.

**Lemma 1 (supermodularity).** For rational U,V<=E,

    F_X(U)+F_X(V) <= F_X(U+V)+F_X(U intersection V).                 (2)

Proof. Put A=X mod U, B=X mod V, and C=X mod(U+V). The pair (A,B) and
X mod(U intersection V) determine each other on the finite support:
equality of the two quotient labels means that the difference lies in
both subspaces. C is a deterministic function of A and also of B. Thus

    H(A)+H(B)-H(A,B)=I(A;B)=H(C)+I(A;B | C)>=H(C).

Subtracting the relevant quotient entropies from 2H(X) gives (2). QED.

**Lemma 2 (irreducible invariance).** Suppose dim E=t>0, a group G acts
Q-linearly and irreducibly on E, and gX has the same law as X for every
g in G. Then for every rational V<=E,

    F_X(V) <= (dim V/t) H(X).                                       (3)

Proof. A finite support has finitely many set partitions. The quotient
partition determines F_X(V), so it takes finitely many values as V varies.
Dimensions are integers between 0 and t. Consequently

    lambda=max_(0!=V<=E) F_X(V)/dim V

exists. Choose a maximizing V of largest dimension. Invariance implies
that gV is another maximizer. Since F_X(0)=0, (2) and maximality give

    lambda(dim V+dim gV)
      <= F_X(V+gV)+F_X(V intersection gV)
      <= lambda(dim(V+gV)+dim(V intersection gV)).

The two outer expressions are equal by the dimension formula. Therefore
V+gV is also a maximizer. Maximal dimension forces V+gV=V, whence gV=V
for every g. Irreducibility and V!=0 give V=E. Since F_X(E)=H(X),
lambda=H(X)/t, proving (3). The argument includes H(X)=0. QED.

## 3. Permutation fibers and the exact collision count

Fix d for the remainder of the proof. Set

    M=k!/(product_a d_a!),  p_a=d_a/k,  h=log M,
    alpha_a=k*a-sum_b b*d_b.

The alpha_a are distinct integers. Identify each symbol a with alpha_a,
and let S be the set of all k-tuples with multiplicities d. This is an
injective labelling of basis symbols, not a tensor operation. Every s in S
has coordinate sum zero. Let Z be uniform on S. Each Z_j has distribution
p (on the integer labels), so H(Z)=h and H(Z_j)=H(p).

For each j define

    E_j={v in Q^k : sum_i v_i=0, v_j=0},  dim E_j=k-2,
    beta=(h-H(p))/(k-2)>=0.

**Lemma 3.** If V<=E_j and r=dim V, then

    F_Z(V)<=r beta.                                                (4)

Proof. Since every vector of V has coordinate j zero, Z mod V determines
Z_j. Condition on Z_j=alpha_a. The remaining coordinates are uniformly
distributed among permutations of the remaining multiset, with total
sum -alpha_a. Subtract their common mean -alpha_a/(k-1), and set coordinate
j to zero. This translates the conditional support into E_j, without
changing differences or quotient conditional entropy. Its law is invariant
under all permutations of the other k-1 coordinates.

The standard action of S_(k-1) on E_j is irreducible over Q. Indeed, a
nonzero vector of coordinate sum zero on these k-1 coordinates has two
unequal entries. Subtracting its transposed image yields a nonzero
multiple of e_u-e_v. Permuting these differences spans all of E_j.
This proves irreducibility for k=3 as well. Applying Lemma 2 to each
conditional law gives

    H(Z | Z mod V, Z_j=alpha_a)
      <= r/(k-2) H(Z | Z_j=alpha_a).

A conditional law supported at one point has entropy zero and obeys the
same inequality. Average with weights p_a. Since the quotient determines
Z_j, the left side averages to F_Z(V). The right side averages to
r/(k-2) (h-H(p)), proving (4). QED.

For s in S let C_V(s)=(s+V) intersection S. Uniformity gives the exact
identity

    F_Z(V)=(1/M) sum_(s in S) log |C_V(s)|.                         (5)

Let N be a positive multiple of M. Denote by A_N the support sequences
I=(I(1),...,I(N)) in S^N containing each s in S exactly N/M times.
These are the **candidate** edges. They are only a counting class; we
do not assert that A_N can be selected by local linear maps.

For a fixed candidate I, the number of all J in the full S^N satisfying
J(t)-I(t) in V for every t is exactly

    product_(s in S) |C_V(s)|^(N/M)=exp(N F_Z(V)).                  (6)

The columns of J can be chosen independently in their specified fibers.
No type constraint of any kind is imposed on J. If V<=E_j has dimension
r, (4) bounds (6) by exp(N r beta). In particular this bounds the number
of J whose differences span exactly V, as well as the larger count (6).

We will also use the elementary candidate-count estimate

    M^N/(N+1)^M <= |A_N|=N!/((N/M)!)^M <= M^N.                    (7)

To see the lower bound, there are at most (N+1)^M different count vectors
for words in an M-letter alphabet. For N divisible by M, the balanced
count vector maximizes its multinomial coefficient: if two counts differ
by at least two, moving one occurrence from the larger to the smaller
strictly decreases the factorial denominator. The largest class is at
least M^N/(N+1)^M. Therefore log|A_N|=Nh-o(N) for fixed d.

## 4. Large average-free sets

**Lemma 4.** Fix an integer L>=2. For every sufficiently large positive
integer q there is B contained in {0,...,floor((q-1)/L)} such that

    x_1+...+x_L=L y,  x_1,...,x_L,y in B
        implies x_1=...=x_L=y,                                   (8)
    log |B|=log q-O_L(sqrt(log q)).                               (9)

Proof. Put ell=floor(sqrt(log q)),
m=floor((q/(2L))^(1/ell)/L), and b=Lm. For large q, ell>=1, m tends
to infinity, and b^ell<=q/(2L). Among the m^ell integer vectors
a in {0,...,m-1}^ell there are at most ell(m-1)^2+1 possible values of
||a||^2. Choose a norm level containing at least

    m^ell/[ell(m-1)^2+1]

vectors, and encode each such vector as the integer sum_(t=0)^(ell-1)
a_t b^t. These encodings are distinct and less than b^ell, hence lie
in the required range for large q.

In an equation as in (8), every digit sum on either side is at most
L(m-1)<b. Thus neither side has carries, and the encoded vectors obey
a^(1)+...+a^(L)=L c. They all have the same squared norm. Consequently

    (1/L) sum_i ||a^(i)-c||^2
      =(1/L) sum_i ||a^(i)||^2-||c||^2=0.

Every a^(i)=c, proving (8). If t=log q, then ell is of order sqrt(t),
log m=(t-log(2L))/ell-log L+O_L(1/m), and log m is of order sqrt(t).
It follows that

    ell log m-log(ell(m-1)^2+1)>=log q-O_L(sqrt(log q)).

The upper bound |B|<=q proves (9). QED.

## 5. Hashes and exact survival probabilities

Let C=max_(s,s' in S,i)|s_i-s'_i| and fix

    B_0>max(k, k! max(1,C)^k).

For any integer matrix with columns from S-S, its rational rank equals
its rank over F_q for every prime q>B_0. In fact a nonzero r-by-r minor
has absolute value at most r! C^r<=k! max(1,C)^k<q, and cannot vanish
modulo q. All larger minors are zero integers. This is uniform in the
number of columns N.

Take such a prime q, a multiple N of M, and a (k-1)-average-free set B
from Lemma 4. Choose v=(v_1,...,v_N) and u_1,...,u_(k-1) independently
and uniformly in F_q. For an integer-labelled local word w define

    b_i(w)=u_i+sum_t w_t v_t                     (i<k),
    b_k(w)=(sum_(i<k)u_i-sum_t w_t v_t)/(k-1).                     (10)

The denominator is invertible because q>k. An original support edge
I consists of k local words I_1,...,I_k and N columns I(t) in S. Since
the coordinate sum of each column is zero, its hashes satisfy

    sum_(i<k) b_i(I_i)=(k-1)b_k(I_k) in F_q.                       (11)

Keep precisely those local words whose hash is in B. This is an actual
coordinate restriction of each of the k factors. Representing hashes in
B by their nonnegative integers, both sides of (11) are in [0,q-1].
Thus the congruence lifts to an integer equality. Lemma 4 forces all k
hashes of a surviving edge to equal one common b in B. Conversely such
an edge survives.

For any fixed edge I and any fixed b in B, every choice of v permits
exactly one tuple of offsets u such that b_i(I_i)=b for i<k. Equation
(11) then gives b_k(I_k)=b. Therefore

    Pr[I survives]=|B| q^(-(k-1)).                               (12)

Now let distinct edges I,J share a local word in some mode j. Define

    V=span_Q{I(t)-J(t): 1<=t<=N},  r=dim V.

Because each column difference has coordinate sum zero and coordinate
j zero, V<=E_j and 1<=r<=k-2. The lower inequality follows from
injectivity of the integer labels: rank zero would mean I=J.

If both edges survive, their common hash values agree, since the shared
local word has the same hash. For a specified b in B, after choosing v,
the offsets are uniquely fixed by I. The additional equations for J are

    sum_t (I_i(t)-J_i(t)) v_t=0,  i<k.                            (13)

The kth equation is redundant, because the rows of the full difference
matrix sum to zero. Deleting that row does not change its rank, over
either Q or F_q. The rank of (13) is r by the minor bound. It has exactly
q^(N-r) solutions for v. Counting v and offsets therefore gives

    Pr[I and J survive]=|B| q^(-(k-1+r)).                         (14)

This is valid for every such pair, whether or not either edge has uniform
joint type, and for shared mode j=k as well as the other modes.

## 6. Isolation against the entire support

Let X count the surviving candidates in A_N. Let Y count ordered pairs
(I,J) with I a surviving candidate, J any other surviving original edge,
and I,J sharing at least one local word. By (12),

    E X=|A_N| |B| q^(-(k-1)).                                    (15)

There are finitely many possible rational spans of subsets of S-S. Let
mathcal V be those nonzero spans contained in at least one E_j and of
dimension at most k-2, and let K=|mathcal V|. K depends on d but not N.
Each pair counted by Y has exactly one such difference span. For each
candidate I and V in mathcal V of dimension r, (6) and (4) bound the
number of partners with exact span V by exp(Nr beta). Summing (14),

    E Y <= E X sum_(V in mathcal V) exp(N dim(V) beta) q^(-dim(V)).  (16)

There is no factor for a choice of shared mode: each span is counted once,
and the existence of a shared mode is enough to apply Lemma 3. Counting
more J by using the full fiber count only increases this upper bound.

For a realization of the hashes, call a surviving candidate isolated if
it shares no local word with any other surviving original edge. Every
nonisolated candidate contributes at least one ordered pair to Y. Thus
the number of isolated candidates is at least X-Y.

Retain exactly the local words of those isolated candidates. The selected
edges have pairwise distinct local words in every mode. No extra edge
can remain after this last coordinate restriction: it would have survived
the earlier hash restriction, and would share a retained word with one
of the isolated candidates. If it is different from that candidate, this
contradicts isolation. Hence the final support consists precisely of the
selected candidates, and is a diagonal after independent relabelling.
It follows that some coordinate restriction has diagonal size at least
E(X-Y), since the maximum of X-Y is at least its expectation.

This argument uses all original edges as possible partners. Treating A_N
itself as a locally selectable tensor, or checking isolation only among
candidates, would not justify the same conclusion.

## 7. The entropy lower bound

Fix delta>0 and put lambda=beta+delta>0. Take any sequence of primes
q tending to infinity and define, for sufficiently large q,

    N=N(q)=M floor(log q/(M lambda)).                             (17)

There are unbounded primes (Euclid's argument suffices). Then N is a
positive multiple of M, N tends to infinity, and

    N lambda<=log q<(N+M)lambda.                                 (18)

No estimate on gaps between primes is needed: we choose N after q and
use the existence of the asymptotic limits established in Section 1.
For all sufficiently large q the rank threshold and Lemma 4 hold.
From (16), (18), and dim V>=1,

    E Y <= E X K exp(-N delta).

Using (15) and the isolation argument, we obtain

    Q_M(D_d^boxtimes N)
       >= (1-K exp(-N delta)) |A_N| |B| q^(-(k-1))                (19)

for these N and all sufficiently large q. The prefactor is positive and
tends to one. By (7), (9), and (18), the logarithm of the right side is

    N h-(k-2)log q-o(N)
       =N[H(p)-(k-2)delta]-o(N).                                (20)

All parameters d,k,M,K,beta,delta are fixed before q tends to infinity;
log q=O(N), so the error in (9) is o(N). Section 1 turns this subsequence
lower bound into

    log Qtilde_M(D_d)>=H(p)-(k-2)delta.

As this holds for every delta>0,

    Qtilde(D_d)>=Qtilde_M(D_d)>=exp H(p).                         (21)

## 8. The matching upper bound for arbitrary linear maps

A slice in mode i is a tensor a tensor B, where a belongs to the ith
factor and B to the tensor product of the others, in the original order.
The slice rank sr(T) is the least number of such slices summing to T,
allowing their distinguished modes to differ.

We first prove sr(Delta_q)=q, to justify its use for ordinary subrank.
For U,V<=C^q let U*V denote the span of coordinatewise products. Then

    dim(U*V)>=dim U+dim V-q.                                    (22)

Indeed, let A be the union of the coordinate supports of vectors in U.
There is u in U nonzero on every coordinate of A: finitely many proper
linear hyperplanes cannot cover a complex vector space. Equivalently,
the product of the finitely many nonzero coordinate linear functions is
a nonzero polynomial, and does not vanish everywhere over an infinite
field. If U=0, take A empty and u=0. Multiplication by u has kernel of
dimension q-|A|, and dim U<=|A|. Hence

    dim(U*V)>=dim(u*V)>=dim V-(q-|A|)>=dim V+dim U-q.

Iterating (22) yields

    dim span(U_1*...*U_l)>=q-sum_(i=1)^l codim U_i.               (23)

For a slice decomposition of Delta_q, let r_i be the number of slices
in mode i, and let U_i<=C^q annihilate the coefficient vectors of these
slices under the bilinear pairing sum_j x_j y_j. Then codim U_i<=r_i.
All slices vanish on U_1 x ... x U_k, so

    sum_(j=1)^q u_(1,j)...u_(k,j)=0  for all u_i in U_i.

The span of U_1*...*U_(k-1) is contained in U_k's annihilator. By (23),

    q-sum_(i<k)codim U_i<=codim U_k,

and q<=sum_i r_i. The expression defining Delta_q supplies q slices,
proving its slice rank equals q. Applying linear maps separately to the
factors takes a slice to a slice or zero. Thus

    Q(T)<=sr(T).                                                (24)

For a word w=(w_1,...,w_N) in {1,...,n}^N, define its score and product
probability by

    s(w)=-sum_t log p_(w_t),  P(w)=product_t p_(w_t)=exp(-s(w)),
    L_N={w:s(w)<=N H(p)}.

Since sum_w P(w)=1 and each w in L_N has P(w)>=exp(-NH(p)),

    |L_N|<=exp(NH(p)).                                         (25)

For every support edge (w^(1),...,w^(k)) of the full tensor power,
each column has multiplicities d, so

    sum_i s(w^(i))=-N sum_a d_a log p_a=NkH(p).

At least one of its words therefore belongs to L_N. Assign each edge
to the least such mode. For each i and w in L_N, collect all assigned
terms whose ith word is w into one slice with distinguished factor e_w.
This partitions the full tensor's support and gives at most k|L_N|
slices. By (24)--(25), for every N>=1,

    Q(D_d^boxtimes N)<=sr(D_d^boxtimes N)<=k exp(NH(p)).          (26)

Taking Nth roots and the limit gives Qtilde(D_d)<=exp H(p).
Together with (21) and the k=2 case, this proves

    Qtilde_M(D_d)=Qtilde(D_d)=exp H(p)

for every positive tuple d of length n>=2, with all k=sum d factors
separate, as claimed. QED.
