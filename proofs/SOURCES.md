# Sources, exact target, and methodological attribution

The references identify the published all-multiplicity Dicke asymptotic-subrank question and the prior tools used in the proof. The mathematical argument is self-contained. The comparison below is bounded to the cited sources; it is not an exhaustive novelty or priority claim.

## Exact published question

The [TR-28 catalogue entry](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/eb7c9d6/tensor-computations/TR-28/README.md) asks for every n>=2 and every positive integer tuple d=(d_1,...,d_n), with k=sum d_i, whether

    Qtilde(D_d)=2^H_2(d/k)=exp H(d/k).

Here D_d is the sum of all order-k basis tensors with multiplicities d, ordinary subrank uses arbitrary independent complex linear maps, and powers group corresponding modes while retaining k factors. A nonzero scalar relating the Dicke tensor to its symmetric-monomial convention is immaterial. These are the conventions in STATEMENT.md.

1. **Oneto--Ventura (2025), Conjecture 4.26.** Alessandro Oneto and Emanuele Ventura, *Ranks of tensors: geometry and applications*, Bollettino dell'Unione Matematica Italiana **18** (2025), 751--778, DOI [10.1007/s40574-025-00472-9](https://doi.org/10.1007/s40574-025-00472-9). The conjecture is on printed p.774 / PDF p.24 and explicitly states the ordinary asymptotic-subrank entropy formula for the symmetric tensor corresponding to a monomial. The conjecture is stated in the published version linked by the DOI.

2. **Vrana--Christandl (2015), section VI, equation (40).** Péter Vrana and Matthias Christandl, *Asymptotic entanglement transformation between W and GHZ states*, Journal of Mathematical Physics **56** (2015), 022204, DOI [10.1063/1.4908106](https://doi.org/10.1063/1.4908106), arXiv:1310.3244. The page references here use arXiv:1310.3244v2. On p.10, equation (40) proposes the conversion cost 1/H_2(d/k). Its convention counts input copies per output two-level GHZ copy; this is the reciprocal of log_2 Qtilde(D_d), so it gives the same question. [arXiv version](https://arxiv.org/abs/1310.3244v2).

3. **Christandl--Vrana--Zuiddam (2019), Question 1.58.** Matthias Christandl, Péter Vrana and Jeroen Zuiddam, *Asymptotic tensor rank of graph tensors: beyond matrix multiplication*, Computational Complexity **28** (2019), 57--111, DOI [10.1007/s00037-019-0172-8](https://doi.org/10.1007/s00037-019-0172-8), arXiv:1609.07476. Cited numbering is from the published version. Question 1.58, printed pp.78--79 / PDF pp.22--23, asks the stronger equality

       q_M(D_lambda)=q(D_lambda)=H_2(lambda/k),

   Here q is the ordinary asymptotic subrank logarithm, while q_M is the monomial subexponent defined using monomial degeneration (Definition 1.7, equation (1.9), and Definition 1.18; equivalently Proposition 1.19 uses monomial border subrank). Remark 1.12 explicitly distinguishes this from monomial restriction in general. The Qtilde_M in STATEMENT.md is instead defined using coordinate/monomial restrictions and proves the stronger lower bound. Together with the ordinary upper bound, it implies Question 1.58 through

       log_2 Qtilde_M^restriction <= q_M^CVZ <= q^CVZ = log_2 Qtilde.

   The comparison with q^CVZ uses ordinary restriction/degeneration equivalence from Theorem 1.11. Both endpoints equal H_2(d/k), so the intermediate quantities have that value too. This comparison does not assert general equivalence of monomial restriction and monomial degeneration. Permuting symbol labels identifies partitions with arbitrary positive multiplicity tuples. The DOI above links the published primary source.

## Existing methods used and re-derived

**Rank-dependent tight-support hashing.** The higher-order Coppersmith--Winograd method in Christandl--Vrana--Zuiddam, Theorem 1.52 and its proof in section 3.3, printed pp.95--101, is a direct precedent for the hash construction. The proof's equations (3.11)--(3.17) and its claims give the average-free consistency condition and the dependence of pair survival on a rational difference rank. Generic random hashing and this rank-dependent calculation are existing methods, not claimed innovations of this package. PROOF.md includes the required finite-support rank argument and survival-probability derivation for its own candidate/collider counting setup.

There is an important hypothesis distinction. In the optimization stated in Theorem 1.52, a law Q on support pairs has its **2k one-coordinate marginals** prescribed. Its two full support-valued marginal laws are not required to equal the chosen law P. A bound established for a uniform full first law cannot simply be substituted into that displayed optimization. The proof does not invoke or claim to evaluate that theorem's optimization. It instead counts candidates of one full joint type and tests them against every possible surviving original edge, with an explicit bound on those collisions.

**Weighted global isolation.** Péter Vrana and Matthias Christandl, *Distillation of Greenberger--Horne--Zeilinger States by Combinatorial Methods*, IEEE Transactions on Information Theory **65**(9) (2019), 5945--5958, DOI [10.1109/TIT.2019.2908646](https://doi.org/10.1109/TIT.2019.2908646), arXiv:1805.09096. Page and lemma references here use arXiv:1805.09096v2, dated January 2020. Section 2, Lemma 2.3, pp.4--5, allows an arbitrary nonnegative weight on the full supported set and bounds its sum over vertices globally isolated in the collision graph. An indicator weight for a chosen full joint-type class is already within this principle. Counting selected candidates while retaining every collider is therefore not claimed as new. The lemma's quantitative homogeneous-restriction/conditional-max-entropy estimate is not assumed to be the rank-stratified estimate needed here; the proof supplies its own counting and entropy arguments. [arXiv version](https://arxiv.org/abs/1805.09096v2).

**Average-free sets.** Vrana--Christandl (2015), Lemma 10, p.8, and Appendix A, p.11, prove the fixed-length generalized average-free statement with density N^(-o(1)); Christandl--Vrana--Zuiddam, Proposition 3.2, printed p.91, quotes it. This is an existing auxiliary construction. The package includes a no-carry digit encoding on a common Euclidean sphere and its size estimate, so no external existence theorem is needed. The 2015 source credits the Salem--Spencer tradition; the original Salem--Spencer paper concerns three-term arithmetic progressions, and we do not attribute the full generalized formulation to that original paper without qualification.

**Diagonal slice rank and the entropy upper bound.** Terence Tao and Will Sawin, *Notes on the “slice rank” of tensors*, 24 August 2016, [public note](https://terrytao.wordpress.com/2016/08/24/notes-on-the-slice-rank-of-tensors/), Example 5 and Proposition 6, are precedents for the diagonal slice-rank value and entropy upper bounds. PROOF.md proves the needed diagonal slice-rank fact by coordinatewise-product dimensions and proves the specific finite-power Dicke upper bound by an explicit score cover. Neither fact is claimed to be new.

## What the written proof actually assumes

The all-multiplicity conclusion follows from the invariant entropy and collision bounds combined with these existing construction principles. The proof itself is included in full and uses only elementary finite-dimensional linear algebra, standard finite Shannon-entropy identities and inequalities, finite-field linear equations, and explicitly proved combinatorial estimates.

In particular:

- It does not assume the general tight-tensor lower theorem or its marginal optimization as a black box.
- It does not assume an all-binary or all-distinct special-case theorem as an induction input.
- Its balanced full-type class estimate is an exact counting bound; it does not require Stirling's formula.
- Its prime sequence uses only the infinitude of primes and chooses the power length after the prime; it does not require Bertrand's postulate, a prime-gap estimate, or uniform control in d.
- Its average-free construction, finite rank-exception bound, induced-matching isolation, diagonal slice-rank lower bound, and existence of the asymptotic limits are all proved in PROOF.md.

## Limits of the literature comparison

The cited 2025 survey states the entropy formula as Conjecture 4.26. The comparison here identifies that conjecture, the earlier conversion-cost question, and the specified methodological precedents. It does not claim an exhaustive search of later literature or a priority guarantee.

The survey's Conjecture 4.26 text says that all binary multiplicity tuples and all-distinct tuples are known. A primary theorem covering both complete families is not identified here. That citation limitation is not a claim that the survey is false or that those families are open. The proof avoids dependence on either assertion.
