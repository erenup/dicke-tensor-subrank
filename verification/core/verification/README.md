# Exact supporting checks for TR-28

The all-multiplicity theorem is proved in [PROOF.md](../proofs/PROOF.md). The finite calculations here are supporting regressions using standard-library Python and exact integer/rational arithmetic.

Run from this directory:

~~~sh
python3 -S -s -B run.py
~~~

The runner authenticates all verification files, checks the written proof bindings, and runs both checkers normally, under -O and with a second hash seed. It requires successful exits, empty stderr, byte-identical stdout and the registered output hashes. It also executes integrity rejection controls and verifies that no input changed during the runs. SOURCE_BINDINGS.txt records the original and included hashes of each proof document; PROOF.md is unchanged.

- check_entropy.py enumerates every nonzero collision-generated subspace for five small supports, with counts 1, 7, 13, 191 and 176. Quotient fibres are checked independently and entropy inequalities are reduced to integer-power comparisons. Five lowered-rank controls must reject.
- check_hashing.py checks 405 rank-one fibres across seven small families, then exhausts all 161051 hash assignments for the three-mode W support with N=3, q=11 and B={0,1,3}. It checks all 27 original edges, six candidates and 54 ordered candidate/collider pairs, the exact survival probabilities, the X-Y bound, and the final restriction against the full support.
- The three hashing controls reject a counterexample to dropping invariance, a non-average-free set, and candidate-only isolation leaving a hidden cross-edge. The first is a counterexample to removing the hypothesis, not a general invariance detector.

These computations do not replace the all-subspace entropy proof, all-collider count, rational/modular rank argument, average-free construction, asymptotic passage, or ordinary-subrank upper bound. No floating-point calculation or uniform-in-d convergence claim is used.
