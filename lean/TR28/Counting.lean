import TR28.Statement

/-! Exact full-support partner counts and rational collision-span bounds. -/

noncomputable section
namespace TR28
open scoped BigOperators

theorem partner_position_count : PartnerPositionCount := by
  classical
  intro Ω _ N R I
  have hset : allPartners R I = Fintype.piFinset (fun t => relationFiber R (I t)) := by
    ext J
    simp [allPartners, relationFiber]
  rw [hset, Fintype.card_piFinset]

theorem partner_histogram_count : PartnerHistogramCount := by
  classical
  intro Ω _ N R I
  rw [partner_position_count Ω N R I]
  simpa [Finset.prod_const, fullTypeCount] using
    (Finset.prod_fiberwise' (Finset.univ : Finset (Fin N)) I
      (fun s => (relationFiber R s).card)).symm

theorem balanced_partner_count : BalancedPartnerCount := by
  classical
  intro Ω _ N c R I hI
  rw [partner_histogram_count Ω N R I]
  apply Finset.prod_congr rfl
  intro s _
  rw [hI s]

theorem exact_span_partner_subset : ExactSpanPartnerSubset := by
  classical
  intro k N S V I J hJ
  have hspan : differenceSpan I J = V := by
    simpa [exactSpanPartners] using hJ
  simp only [allPartners, Finset.mem_filter, Finset.mem_univ, true_and]
  intro t
  change (J t).val - (I t).val ∈ V
  rw [← hspan]
  exact Submodule.subset_span (Set.mem_range_self t)

theorem exact_span_partner_bound : ExactSpanPartnerBound := by
  classical
  intro k N c S V I hI
  calc
    (exactSpanPartners S V I).card ≤
        (allPartners (rationalCollisionRelation S V) I).card :=
      Finset.card_le_card (exact_span_partner_subset k N S V I)
    _ = ∏ s : S, (relationFiber (rationalCollisionRelation S V) s).card ^ c :=
      balanced_partner_count S N c (rationalCollisionRelation S V) I hI

end TR28
