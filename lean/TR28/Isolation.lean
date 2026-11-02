import TR28.Statement
import Mathlib.Data.Finset.Max
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

noncomputable section
namespace TR28
open scoped BigOperators

theorem isolation_count : IsolationCountTheorem := by
  classical
  intro k α E A L _hA
  -- Projecting ordered collisions gives exactly the nonisolated candidates.
  have heq : survivingCandidates E A L \ isolatedCandidates E A L =
      (orderedCollisions E A L).image Prod.fst := by
    ext e
    constructor
    · intro he
      rcases Finset.mem_sdiff.mp he with ⟨heC, heI⟩
      have hnot : ¬ ∀ f ∈ restrictSupport E L, (∃ i, e i = f i) → f = e := by
        intro hiso
        exact heI (Finset.mem_filter.mpr ⟨heC, hiso⟩)
      push Not at hnot
      rcases hnot with ⟨f, hf, hshare, hne⟩
      apply Finset.mem_image.mpr
      refine ⟨(e, f), ?_, rfl⟩
      exact Finset.mem_filter.mpr
        ⟨Finset.mem_product.mpr ⟨heC, hf⟩, Ne.symm hne, hshare⟩
    · intro he
      rcases Finset.mem_image.mp he with ⟨⟨c, f⟩, hpair, hce⟩
      change c = e at hce
      subst c
      rcases Finset.mem_filter.mp hpair with ⟨hprod, hne, hshare⟩
      rcases Finset.mem_product.mp hprod with ⟨heC, hf⟩
      apply Finset.mem_sdiff.mpr
      refine ⟨heC, ?_⟩
      intro heI
      exact hne ((Finset.mem_filter.mp heI).2 f hf hshare).symm
  have hsub : isolatedCandidates E A L ⊆ survivingCandidates E A L :=
    Finset.filter_subset _ _
  have hcard := Finset.card_sdiff_add_card_eq_card hsub
  have hproj := Finset.card_image_le
    (s := orderedCollisions E A L) (f := Prod.fst)
  rw [← heq] at hproj
  omega

theorem exact_coordinate_extraction : ExactCoordinateExtraction := by
  classical
  intro k α E A L hk _hA
  constructor
  · ext e
    constructor
    · intro he
      rcases Finset.mem_filter.mp he with ⟨heE, heWords⟩
      have heS : e ∈ restrictSupport E L := by
        apply Finset.mem_filter.mpr
        refine ⟨heE, ?_⟩
        intro i
        rcases Finset.mem_image.mp (heWords i) with ⟨c, hc, hci⟩
        have hcS := (Finset.mem_inter.mp (Finset.mem_filter.mp hc).1).2
        have hcL := (Finset.mem_filter.mp hcS).2 i
        exact hci ▸ hcL
      let i : Fin k := ⟨0, hk⟩
      rcases Finset.mem_image.mp (heWords i) with ⟨c, hc, hci⟩
      have heq : e = c := (Finset.mem_filter.mp hc).2 e heS ⟨i, hci⟩
      rw [heq]
      exact hc
    · intro he
      have heS := (Finset.mem_inter.mp (Finset.mem_filter.mp he).1).2
      apply Finset.mem_filter.mpr
      refine ⟨(Finset.mem_filter.mp heS).1, ?_⟩
      intro i
      exact Finset.mem_image.mpr ⟨e, he, rfl⟩
  · intro i e he f hf hef
    have hfS := (Finset.mem_inter.mp (Finset.mem_filter.mp hf).1).2
    exact ((Finset.mem_filter.mp he).2 f hfS ⟨i, hef⟩).symm

theorem uniform_isolation_extraction : UniformIsolationExtraction := by
  classical
  intro k α E A Ω _ _ L hk hA
  obtain ⟨ω, _, hmax⟩ := Finset.exists_max_image (Finset.univ : Finset Ω)
    (fun t => (isolatedCandidates E A (L t)).card) Finset.univ_nonempty
  rcases exact_coordinate_extraction k α E A (L ω) hk hA with ⟨hE, hInj⟩
  refine ⟨ω, hE, hInj, ?_⟩
  calc
    (∑ t : Ω, (survivingCandidates E A (L t)).card) ≤
        ∑ t : Ω, ((isolatedCandidates E A (L ω)).card +
          (orderedCollisions E A (L t)).card) := by
      apply Finset.sum_le_sum
      intro t _ht
      exact (isolation_count k α E A (L t) hA).trans
        (Nat.add_le_add_right (hmax t (Finset.mem_univ t)) _)
    _ = Fintype.card Ω * (isolatedCandidates E A (L ω)).card +
        ∑ t : Ω, (orderedCollisions E A (L t)).card := by
      simp [Finset.sum_add_distrib]

end TR28
