# TR-28: exact scope of the Lean finite algebraic core

This file describes the mathematical scope of [Definitions.lean](TR28/Definitions.lean)
and [Statement.lean](TR28/Statement.lean). The theorem `TR28.core_theorems`
proves all ten targets below. The mathematical source is the
[written TR-28 proof](../verification/core/proofs/PROOF.md).

## Literal objects

The general alphabet Omega is any finite type. A word is a function
Fin N -> Omega, with universally quantified natural length N. For any
relation R on Omega, relationFiber(R,s) is the actual finite set of all
t satisfying R(s,t), and allPartners(R,I) is the actual finite set of
all words J with R(I(t),J(t)) at every position. fullTypeCount(I,s) is
the number of positions where I(t)=s. balancedFullType(I,c) means every
such count is c. It constrains I alone; J is never restricted to the
candidate joint type.

For the rational specialization, S is any finite set of vectors in Q^k,
and V is an actual rational linear subspace. The alphabet is the subtype
of elements of S. The collision relation is J(t)-I(t) in V, and
differenceSpan(I,J) is the actual rational span of those column
differences. exactSpanPartners requires that span to equal V. No rank
or membership conclusion is built into an opaque admissibility object.

For isolation, a support edge is a tuple in a product of k arbitrary
coordinate types; these types need not themselves be finite. E and A
are finite sets of such tuples, with candidate hypothesis A subset E.
The sets L_i are literal local coordinate filters. restrictSupport(E,L)
filters the full E by all coordinate conditions, and survivingCandidates
intersects that result with A. orderedCollisions consists of ordered
pairs whose first member is a surviving candidate and whose second
member is any distinct surviving original edge sharing at least one
coordinate. A pair is counted once even if it shares several modes.
isolatedCandidates is computed by absence of all such full-support
partners. retainedWords(I,i) is the actual image of I in coordinate i.

For the dimension bound, E is an arbitrary positive finite-dimensional
rational vector space, A is a family of actual rational linear
automorphisms, and F is a real-valued function on actual rational
submodules. IrreducibleUnder(A) means a submodule fixed by every member
of A is bottom or top. SubmoduleSupermodular(F) is exactly
F(U)+F(V)<=F(U+V)+F(U intersection V). It is an explicit premise, not
a formalized entropy theorem or a disguised dimension-bound conclusion.

## Ten universal targets

1. PartnerPositionCount: for every finite Omega, N, R and I, the
   cardinality of allPartners(R,I) equals the product over positions
   t of card(relationFiber(R,I(t))). No distribution hypothesis is used.
2. PartnerHistogramCount: the same cardinality equals the product over
   s in Omega of card(relationFiber(R,s))^fullTypeCount(I,s).
3. BalancedPartnerCount: if I has balanced full type c, the count is
   exactly the product over s of card(relationFiber(R,s))^c. For the
   source support alphabet and N=c*|S| this is the integer product in
   source equation (6), before its entropy/exponential interpretation.
4. ExactSpanPartnerSubset: every full-support partner with exact
   difference span V is in the actual coset-partner set for V.
5. ExactSpanPartnerBound: for balanced I, the exact-span partner count
   is at most that full coset-fiber product. There is no hypothesis on
   the type of the second word or on V beyond being a rational subspace.
6. FiniteFieldKernelCount: for any finite field K and actual linear map
   A:K^N -> K^r, the literal finite set of solutions to A(x)=0 has
   cardinality |K|^(N-finrank(range A)). The rank is computed from A;
   it is not supplied as a premise. Natural subtraction is justified
   in the proof through rank-nullity. Zero dimensions are included.
7. IsolationCountTheorem: the number X of surviving candidates is at
   most the number of computed isolated candidates plus the number Y
   of ordered collisions against the full surviving original support.
   No isolation conclusion is assumed. This count permits k=0.
8. ExactCoordinateExtraction: for k>0, restricting the original E to
   the coordinate images of its computed isolated candidates leaves
   exactly those candidates, and every coordinate map is injective on
   them. These are the exact finite support conditions for the final
   induced matching. k>0 is necessary: with no modes, empty retained
   images impose no restrictions on the possible empty tuple.
9. UniformIsolationExtraction: for any nonempty finite sample type Omega
   and any sample-dependent local filters, some sample omega has the
   preceding exact restriction and injectivity conclusions, and

       sum_t X_t <= |Omega| * |isolatedCandidates_omega| + sum_t Y_t.

   This is the cross-multiplied finite uniform expectation statement
   |isolatedCandidates_omega| >= E[X-Y]. It uses natural sums with no
   truncating subtraction and does not assume an isolated size bound.
10. InvariantSupermodularDensity: suppose the real-valued F has finite
    range, F(bottom)=0, is supermodular, is invariant under mapping by
    every automorphism in A, and A is irreducible as just defined.
    Then for every actual submodule V,

        F(V)*dim(E) <= dim(V)*F(top).

    The submodule lattice is not assumed finite. Neither a maximizing
    witness, an invariant maximizer, nor any density estimate is a
    premise. The proof must derive the finite maxima and use the
    submodule dimension formula. No positivity of F is assumed.
    This formalizes the algebraic maximizer mechanism of source Lemma 2.

CoreTheorems is the conjunction of all ten targets. The target propositions quantify over Lean Type (ordinary
small types); helper definitions may be universe-polymorphic. No maximum
support size, exponent, dimension, word length or number of samples is
imposed. Empty alphabets/supports, zero word length and empty products
have the ordinary Lean meanings; the explicit positivity/nonemptiness
hypotheses appear only where stated above.

## What remains handwritten

This contract does not define Shannon entropy or prove conditional
entropy inequalities. In particular it does not prove supermodularity
for the actual quotient-entropy functional, its finite-range/invariance
identification, the irreducibility of the concrete permutation action,
or the conditioning argument establishing source Lemma 3. The abstract
density theorem cannot be advertised as an unconditional formalization
of that concrete entropy inequality.

It also does not formalize the balanced multinomial estimate (7), the
average-free set construction, integer/finitely generated rank transfer
to large prime fields, the exact hashing maps and pair probabilities,
or their combination into the exponential expected-collision bound.
The finite-field kernel count supplies the linear-system cardinality
ingredient only; it does not identify a particular hash constraint matrix
or prove that matrix has the required rank after reduction modulo q.

The final support equality and coordinate injectivity are proved on
literal finite supports. The tensor interpretation as a diagonal after
local relabelling, the lower-bound asymptotic passage and existence of
subrank limits, the slice-rank upper bound, and the cited external tools
remain in the written proof. No Lean theorem here states the full entropy
formula, solves the entire catalogue problem formally, or asserts a
finite subrank/rank/border-rank formula. All original tensor modes remain
separate in the written application; no mode regrouping is introduced
by the support definitions.

The [finite Python checks](../verification/README.md) use exact integer/rational
arithmetic. They are supporting regressions and are not premises of these
universal formal targets.

## Trust and resources

Lean v4.34.0-rc2 and Mathlib 85e3a25e006c35636f0e53b0e9296caca2685bc0
are pinned. Only propext, Classical.choice and Quot.sound are permitted;
there are no placeholder or custom-axiom proofs, native_decide calls,
external oracles or checking overrides. The audit performs a clean build,
exact-type and transitive-axiom probes, source-binding checks and substantive
negative controls. It builds modules serially with two Lean workers and
Lean's `-M6000` memory limit, checks measured peak RSS against 7 GiB, and
enforces a 90-minute limit. See [README.md](README.md) for the commands.
