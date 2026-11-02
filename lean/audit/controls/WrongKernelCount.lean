import TR28.Counting
import TR28.LinearCount
import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic

/-! Must fail mathematically: a zero map on a two-dimensional F_2-space has four solutions. -/
namespace TR28.Controls.WrongKernelCount
open TR28

example :
    (kernelSolutions (0 : (Fin 2 → ZMod 2) →ₗ[ZMod 2] (Fin 1 → ZMod 2))).card = 2 := by
  classical
  rw [finite_field_kernel_count (ZMod 2) 2 1]
  rw [LinearMap.range_zero]
  norm_num

end TR28.Controls.WrongKernelCount
