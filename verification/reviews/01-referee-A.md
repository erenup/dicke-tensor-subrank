# Referee report A: the entropy law for Dicke tensors

Reviewed: the written statement and proof now in verification/core/proofs/, and the exact checks in verification/core/verification/, before the paper was typeset.

Verdict: **ACCEPT**. No mathematical corrections required. The Addendum records one correction to the wording of the source comparison (correction C1 of report 02); it does not affect the proof.

This is an independent review. I did not contact the authors or see the other referee's report while preparing it.

## Exact verdict

ACCEPT the complete catalogue TR-28 conclusion and the stated monomial strengthening: for every n>=2 and every positive integer tuple d=(d_1,...,d_n), with k=sum d_i and p=d/k,

    Qtilde_M(D_d)=Qtilde(D_d)=exp H(p)=2^H_2(p).

The field is C. All k original tensor modes remain separate. Tensor powers group only corresponding modes. The lower bound is realized by coordinate deletion and independent relabelling, so it satisfies the stated monomial restriction convention. The upper bound covers arbitrary independent complex-linear maps and proves the finite inequality Q(D_d^boxtimes N)<=k exp(NH(p)) for every N>=1. Both asymptotic limits are justified.

This accepts all positive multiplicities, rather than only binary, all-distinct, equal-multiplicity or selected finite examples. It is a full solution at the catalogue's stated scope. It asserts no rate uniform in d, finite subrank equal to exp H(p), efficient construction algorithm, tensor-rank formula, border-rank formula, or result after merging original modes. No mathematical corrections required. This verdict is a correctness review, not an exhaustive novelty or priority guarantee.

## Derive-first record and hashes

Reviewed proof: SHA256 de6b1e56044a2810b640fa1ad22efc25be23e10be87032e813b58cd2066a4457, identical to verification/core/proofs/PROOF.md.

Before reading the proof I read only STATEMENT.md; the proof's main checkpoints were known to me in advance. I independently derived the probability-score slice cover, quotient-entropy supermodularity and maximal-slope argument, the stabilizer irreducibility, exact uniform-full-type collider count, and the need for global isolation. The exact hashing formulas, average-free construction, diagonal slice-rank argument and source correspondence were verified after reading the proof. The report below checks those as well as the already independently derived steps.

## 1. Limits and exceptional case

Tensoring coordinate or ordinary restrictions gives supermultiplicativity without changing the number of modes. Every power has subrank at least one and at most n^N, the latter already from a single-factor flattening. The elementary remainder argument for the superadditive logarithms proves both limits exist and equal the supremum of their finite-power normalized logarithms. Hence an unbounded subsequence lower bound suffices.

When k=2, positivity forces n=2,d=(1,1); the tensor is a permutation matrix and both subranks of its powers are exactly 2^N. The remaining proof correctly assumes k>=3, so division by k-2 is legitimate.

## 2. Supermodularity, irreducibility and every collision subspace

For finite X, quotient labels by rational subspaces are ordinary finite random variables. The pair of labels modulo U and V is equivalent, on the support, to the label modulo U intersect V. The label modulo U+V is a deterministic function of each. Consequently H(A)+H(B)-H(A,B)=H(C)+I(A;B|C)>=H(C), giving the displayed supermodularity for F_X(W)=H(X|X mod W). The direction of the inequality is correct.

There are finitely many support partitions, so F_X(W) has finitely many possible values; together with finitely many dimensions this ensures the maximal slope is attained. Select a maximizer of largest dimension. Invariance gives the same slope to each translate gW. Supermodularity and the dimension identity force W+gW to have that slope too, including the zero-intersection case because F_X(0)=0. Maximal dimension therefore makes W invariant. Irreducibility forces W to be the whole ambient space. This proves the entropy-per-dimension inequality, including distributions of entropy zero. It does not assume a coordinate-subspace lattice.

The integer labels `alpha_a=k*a-sum_b b*d_b` are distinct and put the full support S in the zero-sum hyperplane. For a shared mode j, every column difference lies in E_j={v:sum_i v_i=0,v_j=0}, of dimension k-2. Conditional on Z_j, subtracting the common mean of the remaining coordinates translates the support into E_j. Its law is invariant under permutations of the other k-1 coordinates. A nonzero vector in an invariant subspace has unequal coordinates; subtracting its transposed image gives a coordinate difference, and permutations span E_j. This proves irreducibility over Q, also when k=3.

Apply the maximal-slope lemma to each conditional law and average. Because V subset E_j makes Z mod V determine Z_j, this yields precisely

    F_Z(V)<=dim(V)*(log|S|-H(p))/(k-2).

Degenerate one-point conditional laws have entropy zero and cause no exception. The bound holds for every rational collision subspace, not merely the enumerated finite test cases or coordinate subspaces.

## 3. Uniform full-joint-type candidates count every possible partner

For uniform Z on S, F_Z(V) is exactly the average of log |(s+V) intersect S| over s in S. If N is divisible by M=|S| and candidate I uses every full support column s exactly N/M times, the number of arbitrary J in S^N with all column differences in V is exactly

    product_s |(s+V) intersect S|^(N/M)=exp(N F_Z(V)).

The choices of columns of J are independent. No type constraint, including even a local marginal constraint, is imposed on J. Thus this is an upper bound for the partners of exact difference span V, regardless of their joint type. It is here that the full joint type of I is essential; the proof never substitutes an equal-marginals hypothesis for it.

The candidate count N!/((N/M)!)^M is bounded below by M^N/(N+1)^M because the balanced count vector maximizes the multinomial coefficient. The elementary balancing argument and the upper count of possible types suffice. All error terms here are o(N) with the multiplicity tuple fixed.

The collection of rational spans of subsets of S-S is finite and depends only on d. Each colliding pair has one exact span in this collection. A span contained in several E_j is still counted once; any such j supplies the same entropy bound. There is no missing sum over shared modes or over N-dependent subspaces.

## 4. Average-free sets, modular ranks and exact probabilities

The average-free construction is valid for every fixed L>=2 and all sufficiently large q. With base b=Lm, each digit on either side of x_1+...+x_L=L y is at most `L(m-1)<b`, so there are no carries. Equality of the encoded integers gives equality of vector averages. Restricting the vectors to one squared-norm level makes equality in the squared-norm convexity identity possible only when every vector is equal. The chosen encodings lie below q/(2L), hence in the required interval. The norm-level pigeonhole estimate gives log|B|=log q-O_L(sqrt(log q)); floor errors are absorbed because m tends to infinity. Thus the density estimate and the no-wrap range are both justified.

A uniform bound on all nonzero minors of matrices with columns in S-S proves rational rank equals rank modulo every prime q>B_0. This applies independently of the number N of columns; the determinant order is bounded by k. The condition q>k also makes k-1 invertible.

The hash for the final mode has the required minus sign and denominator k-1. Tightness makes the sum of the first k-1 hashes equal (k-1) times the last. For retained hashes in B, both integer representatives of these sides lie in [0,q-1], so the modular identity is an integer identity. Average-freeness forces one common hash value for the whole edge.

For fixed edge I and target b, each random vector v permits exactly one offset tuple u. Hence the single-edge survival probability is |B|q^(-(k-1)). If two distinct edges share any local word, including in the final mode, survival forces their common hash values to coincide. Their additional equations are the row differences against v. The last row is redundant because all column sums are zero, and deleting it preserves rank. The rank is the rational dimension r of the difference span by the uniform minor argument, giving exactly |B|q^(-(k-1+r)) for pair survival. Rank zero is excluded for distinct edges by injective labelling. These probabilities use consistent hashes for shared local words and apply to noncandidate partners too.

## 5. Global isolation and a genuine coordinate restriction

X counts surviving candidates, but Y counts ordered candidate/partner collisions against every other surviving original edge. The exact partner count and pair probability give

    E Y <= E X * sum_V exp(N dim(V) beta) q^(-dim(V)).

Each nonisolated candidate contributes at least one ordered pair, so at least X-Y candidates are globally isolated. Retaining their local words cannot introduce an unwanted original support edge. Such an edge would already survive the hash filter, and any of its retained words belongs to an isolated candidate. If it differed from that candidate it would contradict isolation. The selected candidates themselves have distinct words in every mode. Therefore the final support is exactly an induced matching, and its all-one coefficients give a coordinate diagonal after relabelling.

This supplies the actual local restriction that a count of disjoint candidates alone would not supply. The full-joint-type candidates are used only for counting, never treated as a tensor that can first be selected locally. The weighted X-Y argument establishes a realization at least as good as its expectation and does not need independent collision events.

## 6. Asymptotic passage has the stated pointwise scope

Fix delta>0, lambda=beta+delta, and choose an unbounded prime sequence first. Setting N=M floor(log q/(M lambda)) gives N lambda<=log q<(N+M)lambda, N divisible by M and N unbounded. No estimate on prime gaps is needed.

With finitely many nonzero spans, E Y/E X<=K exp(-N delta), so the isolation prefactor tends to one. Candidate counting and the average-free density give lower logarithm

    N log M-(k-2)log q-o(N)
       =N[H(p)-(k-2)delta]-o(N).

All constants, including M,K and the average-free construction's dimension parameter, are allowed to depend on the fixed tuple d. The limits proved earlier turn this unbounded-subsequence bound into the lower asymptotic rate; letting delta decrease to zero gives exp H(p). No uniform-in-d conclusion is used or justified.

## 7. Upper bound for arbitrary complex-linear maps

The coordinatewise-product dimension lemma is correct over the infinite field C: choose u in U nonzero on every coordinate appearing anywhere in U, and bound the kernel of multiplication by u. This gives `dim(U*V)>=dim U+dim V-q`, including U=0. Iteration gives the stated product-space bound.

For a slice decomposition of Delta_q, the spaces annihilating the distinguished slice vectors have codimensions at most their respective slice counts. The diagonal multilinear form vanishes on their Cartesian product, forcing the product of the first k-1 spaces into the annihilator of the last. The dimension bound yields q no greater than the total number of slices. Together with the displayed q-term decomposition, this proves sr(Delta_q)=q. Since arbitrary independent linear maps take a slice to a slice or zero, Q(T)<=sr(T).

For local word w, its product probability P(w) is positive and all such probabilities sum to one. Consequently at most exp(NH(p)) words have score -log P(w)<=NH(p). Every original tensor-power edge has total score NkH(p), so at least one mode has such a word. Assigning each edge to one witnessing mode gives at most k exp(NH(p)) slices and proves the finite upper bound for every N. This part applies to the full tensor and arbitrary complex-linear restrictions, completing the matching ordinary-subrank result.

## 8. Published question and credited methods checked against sources

The TR-28 catalogue entry agrees exactly with the statement in its field, arbitrary local maps, multiplicity range, corresponding-mode power convention and base-two entropy target. A nonzero scalar from the symmetric-monomial normalization is immaterial.

I checked the four primary sources against their PDFs, rather than relying only on text extractions.

- Oneto--Ventura, Conjecture 4.26 on printed p.774, explicitly states the monomial/Dicke asymptotic-subrank entropy formula. The survey also states the binary and all-distinct cases are known; the present proof needs neither as input.
- Vrana--Christandl (2015), section VI, equation (40), gives the corresponding reciprocal-entropy extraction cost. Equation (1) defines input copies per output copy, so this is 1/log_2 Qtilde, agreeing with the proof's rate rather than reversing its direction.
- Christandl--Vrana--Zuiddam (2019), Definition 1.6, defines monomial matrices by at most one nonzero entry in each row and column. This is exactly deletion, relabelling and nonzero rescaling. Proposition 1.19 identifies q and q_M with base-two logarithms of the asymptotic subranks. Question 1.58 states their joint equality to H_2(lambda/k). Permuting alphabet labels identifies arbitrary positive tuples with partitions. (The convention for q_M in this item is corrected in the Addendum.)
- The same paper's Theorem 1.52 and section 3.3, equations (3.11)-(3.17), contain the higher-order tight-support hash scheme and rank-dependent pair probability used as precedents. Its optimization fixes the 2k one-coordinate marginals of a pair law, not both full support-valued marginal laws. The proof correctly does not claim to evaluate that optimization with a bound that assumes a full uniform first type; instead it derives its own all-partner count and isolation argument.
- Vrana--Christandl's combinatorial paper, Lemma 2.3 and its proof, permits an arbitrary nonnegative weight on the full supported set and counts globally isolated vertices. An indicator of a full-type candidate class is within this existing weighted-isolation principle. The proof does not incorrectly import the lemma's homogeneous/conditional-max-entropy quantitative estimate into its different rank-stratified setting.
- Vrana--Christandl (2015), Lemma 10 and Appendix A, and CVZ Proposition 3.2 provide the generalized average-free precedent. The source attribution appropriately distinguishes this from the original three-term Salem--Spencer result. Here the necessary fixed-length construction is proved directly.

Thus the named hashing, isolation and average-free tools are credited at their correct scope. The all-multiplicity proof does not rely on an unverified all-binary/all-distinct theorem or an external general tight-tensor theorem. I have not performed an exhaustive later-literature search or certified priority.

## 9. Exact supporting checks and additional corruptions

Both runner executions, normal and -O, passed. The optimization flag propagates to both child checkers. Child stderr is empty; mathematical outputs agree byte for byte across modes and with the recorded outputs. Timestamps and durations are correctly treated as metadata.

Entropy stdout SHA256 (verification/core/verification/check_entropy.py): 8a5475b6c07384f9f287395a0acf9506aeea91b8c21ec41800f0f475e8ac1fc2.
Hashing stdout SHA256 (verification/core/verification/check_hashing.py): f9abf354872f883b09f496b6131969a353be4e3890a9ae0e13c3d9c59466cb25.

I checked the integer-power conversion of the entropy inequality and the separate quotient-fibre membership calculation. The five tested supports enumerate 1,7,13,191,176 nonzero collision-generated subspaces; their five lowered-rank controls reject. The hashing checker verifies 405 rank-one fibres across its seven small families and all 161051 assignments in its finite W example: 27 original edges, six candidates and 54 ordered candidate/collider pairs, 3993 single-edge hits, 363 pair hits, total X=23958 and Y=19602. It validates the final restriction against the full original support at every assignment.

Its three explicit controls reject the stated failures. The first is accurately described as a concrete counterexample to dropping invariance, not a general invariance detector. The other two reject a non-average-free set and candidate-only isolation with a hidden cross-edge.

Two additional reviewer source corruptions reject with identical exit 1 and diagnostics in normal and optimized modes:

1. Forget the shared-coordinate label in the full-space quotient key: quotient class/membership mismatch.
2. Change the last hash's minus sign to plus: average-free filter did not force equal hashes.

The exact finite checks are supporting regressions. The all-multiplicity conclusion rests on the complete written argument checked above, not on enumeration or floating-point evidence.

## Final verdict

ACCEPT the full catalogue solution and monomial strengthening at the statement's exact scope. No mathematical corrections required.

## Addendum: source convention (correction C1)

The mathematical ACCEPT verdict on the statement and proof is unchanged.

After completing the report above, I read the source-convention correction C1 requested by the other referee (report 02) and verified it against the primary CVZ2019 PDF, including rendered PDF pages 8 and 9 (printed pages 64 and 65). C1 is correct. My original source-comparison paragraph did not distinguish the source's monomial-degeneration subexponent from the coordinate-restriction asymptotic subrank proved in the proof. That source-convention wording needs correction; it does not affect the all-multiplicity proof.

Definition 1.6 defines monomial restriction; Definition 1.7, equation (1.9), instead uses monomial degeneration for the asymptotic monomial conversion rate. Remark 1.12 explicitly leaves its general equivalence to monomial restriction open. Definition 1.18 defines q_M using that conversion rate, and Proposition 1.19 uses underlined monomial border subrank. The underline is visible in the PDF and absent from the text extraction.

The proof's restriction lower bound is stronger. For its Dicke tensors,

    H_2(p) = log_2 Qtilde_M^restriction(D_d)
           <= q_M^CVZ(D_d)
           <= q^CVZ(D_d) = log_2 Qtilde(D_d) = H_2(p).

The middle comparison uses inclusion of monomial in ordinary degeneration and Theorem 1.11's equivalence of ordinary asymptotic restriction and degeneration. Thus the implication to Question 1.58 remains valid with an explicit squeeze; no general monomial restriction/degeneration equivalence is asserted. This source comparison is separate from the self-contained catalogue theorem proof.

C1 is to be applied in the source comparison in SOURCES.md. No formula or argument in PROOF.md needs modification.
