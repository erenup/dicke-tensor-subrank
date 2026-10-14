import TR28.Statement
import Mathlib.Tactic

/-! The finite-range supermodular maximizer argument on actual submodules. -/

noncomputable section
namespace TR28

/-- Normalize by the modular dimension function, then choose a maximizer
of largest dimension. Irreducibility forces its value to be an endpoint value. -/
theorem invariant_supermodular_density : InvariantSupermodularDensity := by
  classical
  intro E _ _ _ ht A F hfinite hbot hsuper hinv hirred V
  let t : ℝ := Module.finrank ℚ E
  let J : Submodule ℚ E → ℝ := fun W =>
    F W * t - (Module.finrank ℚ W : ℝ) * F ⊤
  have htpos : 0 < t := by
    dsimp [t]
    exact_mod_cast ht
  have hJbot : J ⊥ = 0 := by
    simp [J, t, hbot]
  have hJtop : J ⊤ = 0 := by
    simp [J, t, mul_comm]
  have hJinv : ∀ g ∈ A, ∀ W : Submodule ℚ E,
      J (W.map g.toLinearMap) = J W := by
    intro g hg W
    dsimp [J]
    rw [hinv g hg W, g.finrank_map_eq]
  have hJsuper : SubmoduleSupermodular J := by
    intro U W
    have hs := mul_le_mul_of_nonneg_right (hsuper U W) htpos.le
    have hd :
        (Module.finrank ℚ ↥(U ⊔ W) : ℝ) + (Module.finrank ℚ ↥(U ⊓ W) : ℝ) =
          (Module.finrank ℚ U : ℝ) + (Module.finrank ℚ W : ℝ) := by
      exact_mod_cast Submodule.finrank_sup_add_finrank_inf_eq U W
    have hd' := congrArg (fun x : ℝ => x * F ⊤) hd
    dsimp [J]
    nlinarith
  have hdims : Set.Finite (Set.range (fun W : Submodule ℚ E => Module.finrank ℚ W)) := by
    apply (Set.finite_Iic (Module.finrank ℚ E)).subset
    rintro _ ⟨W, rfl⟩
    exact Submodule.finrank_le W
  have hJfinite : Set.Finite (Set.range J) := by
    apply ((hfinite.prod hdims).image
      (fun p : ℝ × ℕ => p.1 * t - (p.2 : ℝ) * F ⊤)).subset
    rintro _ ⟨W, rfl⟩
    exact ⟨(F W, Module.finrank ℚ W),
      ⟨Set.mem_range_self W, Set.mem_range_self W⟩, rfl⟩
  by_contra hbad
  have hpositive : 0 < J V := by
    dsimp [J, t]
    exact sub_pos.mpr (lt_of_not_ge hbad)
  obtain ⟨j, hj, hmaxj⟩ := Set.exists_max_image (Set.range J) id hJfinite
    ⟨J V, Set.mem_range_self V⟩
  obtain ⟨W₀, rfl⟩ := hj
  have hmax₀ : ∀ W : Submodule ℚ E, J W ≤ J W₀ := by
    intro W
    exact hmaxj (J W) (Set.mem_range_self W)
  let D : Set ℕ := {d | ∃ W : Submodule ℚ E, J W = J W₀ ∧ Module.finrank ℚ W = d}
  have hDfinite : D.Finite := by
    apply (Set.finite_Iic (Module.finrank ℚ E)).subset
    rintro _ ⟨W, _, rfl⟩
    exact Submodule.finrank_le W
  have hDnonempty : D.Nonempty := ⟨Module.finrank ℚ W₀, W₀, rfl, rfl⟩
  obtain ⟨d, hd, hdmax⟩ := Set.exists_max_image D id hDfinite hDnonempty
  obtain ⟨W, hWJ, hWd⟩ := hd
  have hmax : ∀ U : Submodule ℚ E, J U ≤ J W := by
    intro U
    rw [hWJ]
    exact hmax₀ U
  have hmaxdim : ∀ U : Submodule ℚ E, J U = J W →
      Module.finrank ℚ U ≤ Module.finrank ℚ W := by
    intro U hU
    have h := hdmax (Module.finrank ℚ U) ⟨U, hU.trans hWJ, rfl⟩
    simpa only [id_eq, ← hWd] using h
  have hWpos : 0 < J W := lt_of_lt_of_le hpositive (hmax V)
  have hWinvariant : InvariantUnder A W := by
    intro g hg
    let Wg := W.map g.toLinearMap
    have hgJ : J Wg = J W := hJinv g hg W
    have hsupJ : J (W ⊔ Wg) = J W := by
      apply le_antisymm (hmax _)
      have hs := hJsuper W Wg
      have hi := hmax (W ⊓ Wg)
      rw [hgJ] at hs
      linarith
    have hsupdim : Module.finrank ℚ ↥(W ⊔ Wg) ≤ Module.finrank ℚ W :=
      hmaxdim _ hsupJ
    have hsuple : W ⊔ Wg = W :=
      (Submodule.eq_of_le_of_finrank_eq le_sup_left
        (le_antisymm (Submodule.finrank_mono le_sup_left) hsupdim)).symm
    have hgle : Wg ≤ W := by
      rw [← hsuple]
      exact le_sup_right
    apply Submodule.eq_of_le_of_finrank_eq hgle
    exact g.finrank_map_eq W
  rcases hirred W hWinvariant with hWbot | hWtop
  · rw [hWbot, hJbot] at hWpos
    exact (lt_irrefl 0) hWpos
  · rw [hWtop, hJtop] at hWpos
    exact (lt_irrefl 0) hWpos

end TR28
