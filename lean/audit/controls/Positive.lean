import TR28.Counting
import TR28.LinearCount
import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic

/-! Positive actual-data regressions; no native computation or supplied counts. -/

namespace TR28.Controls.Positive
open TR28

def firstWord : Fin 2 → Fin 2 := fun i => i

theorem firstWord_balanced : balancedFullType firstWord 1 := by
  classical
  let : DecidableEq (Fin 2) := Classical.decEq _
  intro s
  unfold fullTypeCount
  apply Finset.card_eq_one.mpr
  refine ⟨s, ?_⟩
  ext t
  rw [Finset.mem_filter, Finset.mem_singleton]
  simp [firstWord]

example : (allPartners (fun _ _ : Fin 2 => True) firstWord).card = 4 := by
  classical
  rw [balanced_partner_count (Fin 2) 2 1 _ firstWord firstWord_balanced]
  norm_num [relationFiber]

-- A nonbalanced full-support partner is still counted.
example : (fun _ : Fin 2 => (0 : Fin 2)) ∈ allPartners (fun _ _ : Fin 2 => True) firstWord := by
  classical
  simp [allPartners]

example : ¬ balancedFullType (fun _ : Fin 2 => (0 : Fin 2)) 1 := by
  classical
  intro h
  have h1 := h (1 : Fin 2)
  norm_num [fullTypeCount] at h1

-- Empty position set: its single empty word is a partner even for an empty relation.
example : (allPartners (fun _ _ : Fin 2 => False) (fun i : Fin 0 => Fin.elim0 i)).card = 1 := by
  classical
  rw [partner_position_count (Fin 2) 0]
  simp

example :
    (kernelSolutions (0 : (Fin 2 → ZMod 2) →ₗ[ZMod 2] (Fin 1 → ZMod 2))).card = 4 := by
  classical
  rw [finite_field_kernel_count (ZMod 2) 2 1]
  rw [LinearMap.range_zero]
  norm_num

example :
    (kernelSolutions (0 : (Fin 0 → ZMod 2) →ₗ[ZMod 2] (Fin 1 → ZMod 2))).card = 1 := by
  classical
  rw [finite_field_kernel_count (ZMod 2) 0 1]
  rw [LinearMap.range_zero]
  norm_num

example :
    (kernelSolutions (LinearMap.id : (Fin 2 → ZMod 2) →ₗ[ZMod 2] (Fin 2 → ZMod 2))).card = 1 := by
  classical
  rw [finite_field_kernel_count (ZMod 2) 2 2]
  rw [LinearMap.range_id]
  norm_num [Module.finrank_fin_fun]

-- With zero modes the correct local restriction keeps the full original support.
example (E : Finset (SupportEdge 0 (fun _ => Fin 2))) :
    restrictSupport E (retainedWords (∅ : Finset (SupportEdge 0 (fun _ => Fin 2)))) = E := by
  classical
  simp [restrictSupport]

end TR28.Controls.Positive
