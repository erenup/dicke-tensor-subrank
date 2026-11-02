import TR28.Counting
import TR28.LinearCount
import Mathlib.Tactic

/-! Must fail mathematically: all four partners, not only the two balanced words. -/
namespace TR28.Controls.WrongFullPartnerCount
open TR28

example : (allPartners (fun _ _ : Fin 2 => True) (fun i : Fin 2 => i)).card = 2 := by
  classical
  rw [partner_position_count (Fin 2) 2]
  norm_num [relationFiber]

end TR28.Controls.WrongFullPartnerCount
