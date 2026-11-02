# Referee report B: the entropy law for Dicke tensors

Reviewed: the written statement and proof now in verification/core/proofs/, and the exact checks in verification/core/verification/, before the paper was typeset.

Verdict: **ACCEPT WITH CORRECTIONS**. The full mathematical statement and proof are accepted; one source-convention correction C1 is required in SOURCES.md item 3. This is one independent review. Its separate entropy, combinatorial and executable component audits are parts of this one review (the executable audit is report 03) and do not count as a second review.

For every n>=2 and positive integer tuple d, putting k=sum d and p=d/k,
over C with all k original modes kept separate, I accept

    Qtilde_M(D_d)=Qtilde(D_d)=exp H(p)=2^H_2(p).

The lower bound uses coordinate restrictions. The ordinary-subrank upper
bound allows arbitrary independent complex-linear maps and holds at every
power as Q(D_d^boxtimes N)<=k exp(NH(p)). Powers group only corresponding
modes. The result is pointwise in fixed d; it asserts no uniform convergence,
finite-subrank equality, construction efficiency, tensor rank, border rank,
or result for tensors with modes merged together. It answers the full
catalogue TR-28 question and the stated stronger monomial version.

Reviewed proof: SHA256 de6b1e56044a2810b640fa1ad22efc25be23e10be87032e813b58cd2066a4457,
identical to verification/core/proofs/PROOF.md. The proof line numbers below
refer to that file.

## Independence

The catalogue snapshot supplied with the statement is byte-identical to the
TR-28 catalogue entry. Before reading the proof, checks, code or source
commentary, I read only the statement and catalogue entry and wrote down my
independent derivation. Focus points for the review were indicated to me in
advance. Each component audit likewise wrote its own outline before reading
the proof or code. I contacted neither the authors nor the other referee and
saw no other review.

## Line audit

The decisive checks of the complete line audit are:

| Proof lines | Obligation | Finding |
|---|---|---|
| 15–43 | Definitions, limits, k=2 | Supermultiplicativity proves both full limits; the only k=2 tuple is handled exactly as a permutation matrix. |
| 45–136 | Entropy inequality for every rational collision subspace | Quotient entropy is supermodular. The finite-valued maximum-slope argument plus irreducible permutation invariance gives the correct dimension bound, including singleton conditional laws. |
| 138–167 | Full joint type versus arbitrary colliders | The product of quotient-fiber sizes counts every supported partner, with no joint-type or marginal constraint on the partner. The balanced candidate count is exact up to the proved polynomial factor. |
| 169–203 | Higher-order average-free sets | The fixed-norm digit construction has no carries and the required density; it forbids the full averaging equation, not only three-term progressions. |
| 205–265 | Rational/modular rank and survival | A fixed integer-minor bound works for all N. Local hashes give exact single-edge and rank-dependent pair probabilities, including pairs sharing the final mode. |
| 267–345 | Global isolation and asymptotics | Isolation is tested in the entire original support; restricting the isolated vertices leaves exactly a diagonal. Choosing primes first needs only their infinitude and yields the claimed rate without uniformity in d. |
| 347–419 | Upper bound for arbitrary maps | The coordinatewise-product proof establishes diagonal slice rank exactly. The probability-score slice cover then proves the finite-power bound for all local complex-linear maps. |

## Required correction C1 (source convention)

The source audit found one required correction, **C1**, in SOURCES.md item 3.
CVZ2019's q_M in Question 1.58 is defined using monomial **degeneration**,
not the package's coordinate/monomial restriction limit. Definition 1.18,
equation (1.9), Proposition 1.19's underlined monomial border subrank, and
Remark 1.12 distinguish these notions explicitly. I confirmed this in the
primary PDF; the underline is lost in the plain-text extraction.

Replace the item 3 convention paragraph to state that this package proves
the stronger restriction lower bound, and that its result answers the CVZ
question through

    log_2 Qtilde_M^restriction <= q_M^CVZ <= q^CVZ = log_2 Qtilde.

The right comparison uses the source's Theorem 1.11 on ordinary asymptotic
restriction/degeneration equivalence. Both outer terms equal H_2(p), so
CVZ's formula follows. No change to the precise statement or proof is
required. C1 corrects the source comparison; it does not weaken the proved
theorem.

Source details. The location to correct is SOURCES.md, numbered item 3,
especially the clause

> where q and q_M denote logarithms of the ordinary and monomial asymptotic subranks.

and the following sentence identifying the package's coordinate-deletion
convention with the source's monomial version. Definition 1.7, equation (1.9),
defines omega_M via monomial degeneration. Remark 1.12 (printed p.64,
PDF p.8) explicitly says it is not known in general whether monomial
degeneration can be replaced by monomial restriction in that rate.
Definition 1.18 (printed p.65, PDF p.9) defines q_M=1/omega_M, and
Proposition 1.19 gives its limit in terms of the **underlined monomial
border subrank**. That underline is lost in the plain text; the rendered
PDF pages were inspected directly.

The mathematical conclusion about answering Question 1.58 remains true.
The package proves log_2 Qtilde_M^restriction=H_2(p) and
log_2 Qtilde^restriction=H_2(p). Monomial restriction is a special case of
monomial degeneration, and monomial degeneration is an ordinary
degeneration. The source's Theorem 1.11 identifies ordinary asymptotic
restriction and degeneration. Consequently

    H_2(p)=log_2 Qtilde_M^restriction(D_d)
      <= q_M^CVZ(D_d)
      <= q^CVZ(D_d)=log_2 Qtilde(D_d)=H_2(p).

This squeezes the source's monomial-degeneration subexponent to the same
value. No assertion of general equality between monomial restriction and
monomial degeneration is needed.

A sufficient replacement for the convention paragraph in item 3 is:

> Here q is the ordinary asymptotic subrank logarithm, while q_M is the
> monomial subexponent defined using monomial degeneration (Definition 1.7,
> equation (1.9), and Definition 1.18; equivalently Proposition 1.19 uses
> monomial border subrank). Remark 1.12 explicitly distinguishes this from
> monomial restriction in general. Our Qtilde_M is instead defined using
> coordinate/monomial restrictions and proves the stronger lower bound.
> Together with the ordinary upper bound, it implies Question 1.58 through
> log_2 Qtilde_M^restriction <= q_M^CVZ <= q^CVZ = log_2 Qtilde; the last
> comparison uses ordinary restriction/degeneration equivalence from
> Theorem 1.11. Permuting symbol labels identifies partitions with arbitrary
> positive multiplicity tuples.

No change to STATEMENT.md's precise restriction definition or to PROOF.md
is requested. Its claim to answer the source question is correct with
this explicit comparison. All mathematical proof arguments are elementary
and self-contained; Theorem 1.11 is needed here only to compare conventions
with this additional cited source question, not to prove the catalogue
TR-28 ordinary-subrank formula.

## Other source attributions

The other checked source attributions stand. Oneto–Ventura Conjecture 4.26
and Vrana–Christandl Eq. (40) match the full ordinary-subrank target. The
higher-order hashing, average-free construction, and weighted global
isolation are correctly credited. The proof avoids substituting a uniform
full-law estimate into CVZ Theorem 1.52's different 2k-marginal optimization,
and instead supplies the unrestricted partner count itself. The needed
average-free and slice-rank lemmas are proved in the package. This review
accepts correctness and the match to the located targets subject to C1;
it does not certify an exhaustive novelty search.

## Exact checks

Both runner executions pass normally and under -O, and propagate the
optimization setting to their children. The entropy/hash mathematical
outputs are identical between modes and to the recorded outputs,
with SHA256 8a5475b6c07384f9f287395a0acf9506aeea91b8c21ec41800f0f475e8ac1fc2
and f9abf354872f883b09f496b6131969a353be4e3890a9ae0e13c3d9c59466cb25.
All five entropy and three hashing controls reject. The supported counts
are 1,7,13,191,176 collision subspaces, 405 rank-one cases, and all
161,051 assignments in the finite W hashing example.

Two additional corruptions, each applied to a separate copy, each exit 1
identically in both modes, with empty stdout:

- Merging distinct line cosets rejects at `quotient class/membership mismatch`.
- Replacing the hash denominator inverse by 1 rejects at
  `average-free filter did not force equal hashes`.

The executable audit (report 03) records those runs and audits the
arbitrary-map upper bound. A further independent d=(2,2), N=6 regression
confirms that the full partner count is 16, while only four partners have
uniform full joint type; two colliders even preserve every local type while
having nonuniform full type. Its normal/-O outputs agree and its two
controls reject. This directly tests the reason the proof must count all
colliders.

The combinatorial audit and the entropy/source audit of this review reach
mathematical conclusions that agree with the main line audit; the
primary-source audit supplies C1.

## Conclusion

The executable regressions concern finite supports and one finite hash
experiment. They do not prove the asymptotic result by enumeration. The
all-positive-tuple conclusion is supported by the written proof audited
above. The only required correction is C1 above. The mathematical proof and
executable evidence require no correction.
