import TR28.Statement
import Mathlib.Tactic

/-! The literal cardinality of a finite-field homogeneous solution set. -/

noncomputable section
namespace TR28

theorem finite_field_kernel_count : FiniteFieldKernelCount := by
  classical
  intro K _ _ N r A
  have hcard : (kernelSolutions A).card = Fintype.card A.ker := by
    simpa [kernelSolutions, LinearMap.mem_ker] using
      (Fintype.card_subtype (fun x => A x = 0)).symm
  rw [hcard, Module.card_eq_pow_finrank (K := K) (V := A.ker)]
  have hrank := A.finrank_range_add_finrank_ker
  rw [Module.finrank_fin_fun] at hrank
  congr 1
  omega

end TR28
