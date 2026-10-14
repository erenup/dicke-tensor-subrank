import TR28.Definitions

/-! Exact proposed universal targets, declared before proof implementations.
These definitions name propositions and do not assert their truth. -/

namespace TR28
open scoped BigOperators

/-- The full partner count factors over positions, without any distribution hypothesis. -/
def PartnerPositionCount : Prop :=
  ∀ (Ω : Type) [Fintype Ω] (N : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    (allPartners R I).card = ∏ t, (relationFiber R (I t)).card

/-- The same count regrouped by the literal full joint histogram of I. -/
def PartnerHistogramCount : Prop :=
  ∀ (Ω : Type) [Fintype Ω] (N : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    (allPartners R I).card = ∏ s, (relationFiber R s).card ^ fullTypeCount I s

/-- Exact formula (6) for balanced I; J still ranges over the entire support Ω^N. -/
def BalancedPartnerCount : Prop :=
  ∀ (Ω : Type) [Fintype Ω] (N c : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    balancedFullType I c →
    (allPartners R I).card = ∏ s, (relationFiber R s).card ^ c

/-- Literal rational collision subspaces: exact-span partners form a subset of all coset partners. -/
def ExactSpanPartnerSubset : Prop :=
  ∀ (k N : ℕ) (S : Finset (Fin k → ℚ)) (V : Submodule ℚ (Fin k → ℚ))
    (I : Fin N → S),
    exactSpanPartners S V I ⊆ allPartners (rationalCollisionRelation S V) I

/-- The actual exact-span count obeys the full-support product bound, with only I balanced. -/
def ExactSpanPartnerBound : Prop :=
  ∀ (k N c : ℕ) (S : Finset (Fin k → ℚ)) (V : Submodule ℚ (Fin k → ℚ))
    (I : Fin N → S), balancedFullType I c →
    (exactSpanPartners S V I).card ≤
      ∏ s : S, (relationFiber (rationalCollisionRelation S V) s).card ^ c

/-- Literal finite-field solution count, with rank computed from A. -/
def FiniteFieldKernelCount : Prop :=
  ∀ (K : Type) [Field K] [Fintype K] (N r : ℕ)
    (A : (Fin N → K) →ₗ[K] (Fin r → K)),
    (kernelSolutions A).card = Fintype.card K ^ (N - Module.finrank K A.range)

/-- All finite dimensions, with candidates explicitly drawn from the original
support. No positivity of the number of modes is needed for this count. -/
def IsolationCountTheorem : Prop :=
  ∀ (k : ℕ) (α : Fin k → Type) (E A : Finset (SupportEdge k α))
    (L : (i : Fin k) → Finset (α i)),
  A ⊆ E →
  (survivingCandidates E A L).card ≤
    (isolatedCandidates E A L).card + (orderedCollisions E A L).card

/-- Restrict the original support using exactly the retained coordinate words.
The result equals the computed isolated candidates, and every local coordinate
map is injective on them. The positive-mode hypothesis is necessary. -/
def ExactCoordinateExtraction : Prop :=
  ∀ (k : ℕ) (α : Fin k → Type) (E A : Finset (SupportEdge k α))
    (L : (i : Fin k) → Finset (α i)),
  0 < k → A ⊆ E →
  restrictSupport E (retainedWords (isolatedCandidates E A L)) =
    isolatedCandidates E A L ∧
  ∀ i, Set.InjOn (fun e : SupportEdge k α => e i)
    (↑(isolatedCandidates E A L) : Set (SupportEdge k α))

/-- One finite uniform sample produces an actual exact coordinate restriction
and matching of size at least E[X-Y]. The final inequality is cross-multiplied
in N, so it entails no truncated subtraction and no division convention. -/
def UniformIsolationExtraction : Prop :=
  ∀ (k : ℕ) (α : Fin k → Type) (E A : Finset (SupportEdge k α))
    (Ω : Type) [Fintype Ω] [Nonempty Ω]
    (L : Ω → (i : Fin k) → Finset (α i)),
  0 < k → A ⊆ E →
  ∃ ω : Ω,
    restrictSupport E (retainedWords (isolatedCandidates E A (L ω))) =
      isolatedCandidates E A (L ω) ∧
    (∀ i, Set.InjOn (fun e : SupportEdge k α => e i)
      (↑(isolatedCandidates E A (L ω)) : Set (SupportEdge k α))) ∧
    (∑ t : Ω, (survivingCandidates E A (L t)).card) ≤
      Fintype.card Ω * (isolatedCandidates E A (L ω)).card +
      ∑ t : Ω, (orderedCollisions E A (L t)).card

/-- The algebraic maximizer argument of accepted Lemma 2, isolated from entropy.
The range of F is finite; the lattice of rational subspaces need not be finite.
No density estimate, maximizing witness, or invariant maximizer is a premise. -/
def InvariantSupermodularDensity : Prop :=
  ∀ (E : Type) [AddCommGroup E] [Module ℚ E] [FiniteDimensional ℚ E],
  0 < Module.finrank ℚ E →
  ∀ (A : Set (E ≃ₗ[ℚ] E)) (F : Submodule ℚ E → ℝ),
  Set.Finite (Set.range F) → F ⊥ = 0 → SubmoduleSupermodular F →
  (∀ g ∈ A, ∀ V, F (V.map g.toLinearMap) = F V) →
  IrreducibleUnder A →
  ∀ V : Submodule ℚ E,
    F V * (Module.finrank ℚ E : ℝ) ≤
      (Module.finrank ℚ V : ℝ) * F ⊤

/-- All ten universal targets are required for completion of this core. -/
def CoreTheorems : Prop :=
  PartnerPositionCount ∧ PartnerHistogramCount ∧ BalancedPartnerCount ∧
  ExactSpanPartnerSubset ∧ ExactSpanPartnerBound ∧ FiniteFieldKernelCount ∧
  IsolationCountTheorem ∧ ExactCoordinateExtraction ∧ UniformIsolationExtraction ∧
  InvariantSupermodularDensity

end TR28
