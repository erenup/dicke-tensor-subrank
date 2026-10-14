import TR28

/-! Exact alias and literal-statement checks against the frozen core contract. -/

namespace TR28.FinalProbe
open scoped BigOperators

-- Named target aliases, including the complete core conjunction.
example : PartnerPositionCount := partner_position_count

example : PartnerHistogramCount := partner_histogram_count

example : BalancedPartnerCount := balanced_partner_count

example : ExactSpanPartnerSubset := exact_span_partner_subset

example : ExactSpanPartnerBound := exact_span_partner_bound

example : FiniteFieldKernelCount := finite_field_kernel_count

example : IsolationCountTheorem := isolation_count

example : ExactCoordinateExtraction := exact_coordinate_extraction

example : UniformIsolationExtraction := uniform_isolation_extraction

example : InvariantSupermodularDensity := invariant_supermodular_density

example : CoreTheorems := core_theorems

-- Literal bodies copied verbatim from the frozen Statement.lean.
-- PartnerPositionCount
example :
  ∀ (Ω : Type) [Fintype Ω] (N : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    (allPartners R I).card = ∏ t, (relationFiber R (I t)).card :=
  partner_position_count

-- PartnerHistogramCount
example :
  ∀ (Ω : Type) [Fintype Ω] (N : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    (allPartners R I).card = ∏ s, (relationFiber R s).card ^ fullTypeCount I s :=
  partner_histogram_count

-- BalancedPartnerCount
example :
  ∀ (Ω : Type) [Fintype Ω] (N c : ℕ) (R : Ω → Ω → Prop) (I : Fin N → Ω),
    balancedFullType I c →
    (allPartners R I).card = ∏ s, (relationFiber R s).card ^ c :=
  balanced_partner_count

-- ExactSpanPartnerSubset
example :
  ∀ (k N : ℕ) (S : Finset (Fin k → ℚ)) (V : Submodule ℚ (Fin k → ℚ))
    (I : Fin N → S),
    exactSpanPartners S V I ⊆ allPartners (rationalCollisionRelation S V) I :=
  exact_span_partner_subset

-- ExactSpanPartnerBound
example :
  ∀ (k N c : ℕ) (S : Finset (Fin k → ℚ)) (V : Submodule ℚ (Fin k → ℚ))
    (I : Fin N → S), balancedFullType I c →
    (exactSpanPartners S V I).card ≤
      ∏ s : S, (relationFiber (rationalCollisionRelation S V) s).card ^ c :=
  exact_span_partner_bound

-- FiniteFieldKernelCount
example :
  ∀ (K : Type) [Field K] [Fintype K] (N r : ℕ)
    (A : (Fin N → K) →ₗ[K] (Fin r → K)),
    (kernelSolutions A).card = Fintype.card K ^ (N - Module.finrank K A.range) :=
  finite_field_kernel_count

-- IsolationCountTheorem
example :
  ∀ (k : ℕ) (α : Fin k → Type) (E A : Finset (SupportEdge k α))
    (L : (i : Fin k) → Finset (α i)),
  A ⊆ E →
  (survivingCandidates E A L).card ≤
    (isolatedCandidates E A L).card + (orderedCollisions E A L).card :=
  isolation_count

-- ExactCoordinateExtraction
example :
  ∀ (k : ℕ) (α : Fin k → Type) (E A : Finset (SupportEdge k α))
    (L : (i : Fin k) → Finset (α i)),
  0 < k → A ⊆ E →
  restrictSupport E (retainedWords (isolatedCandidates E A L)) =
    isolatedCandidates E A L ∧
  ∀ i, Set.InjOn (fun e : SupportEdge k α => e i)
    (↑(isolatedCandidates E A L) : Set (SupportEdge k α)) :=
  exact_coordinate_extraction

-- UniformIsolationExtraction
example :
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
      ∑ t : Ω, (orderedCollisions E A (L t)).card :=
  uniform_isolation_extraction

-- InvariantSupermodularDensity
example :
  ∀ (E : Type) [AddCommGroup E] [Module ℚ E] [FiniteDimensional ℚ E],
  0 < Module.finrank ℚ E →
  ∀ (A : Set (E ≃ₗ[ℚ] E)) (F : Submodule ℚ E → ℝ),
  Set.Finite (Set.range F) → F ⊥ = 0 → SubmoduleSupermodular F →
  (∀ g ∈ A, ∀ V, F (V.map g.toLinearMap) = F V) →
  IrreducibleUnder A →
  ∀ V : Submodule ℚ E,
    F V * (Module.finrank ℚ E : ℝ) ≤
      (Module.finrank ℚ V : ℝ) * F ⊤ :=
  invariant_supermodular_density

-- CoreTheorems
example :
  PartnerPositionCount ∧ PartnerHistogramCount ∧ BalancedPartnerCount ∧
  ExactSpanPartnerSubset ∧ ExactSpanPartnerBound ∧ FiniteFieldKernelCount ∧
  IsolationCountTheorem ∧ ExactCoordinateExtraction ∧ UniformIsolationExtraction ∧
  InvariantSupermodularDensity :=
  core_theorems

end TR28.FinalProbe

-- Report the transitive axiom dependencies of every delivered theorem.
#print axioms TR28.partner_position_count
#print axioms TR28.partner_histogram_count
#print axioms TR28.balanced_partner_count
#print axioms TR28.exact_span_partner_subset
#print axioms TR28.exact_span_partner_bound
#print axioms TR28.finite_field_kernel_count
#print axioms TR28.isolation_count
#print axioms TR28.exact_coordinate_extraction
#print axioms TR28.uniform_isolation_extraction
#print axioms TR28.invariant_supermodular_density
#print axioms TR28.core_theorems
