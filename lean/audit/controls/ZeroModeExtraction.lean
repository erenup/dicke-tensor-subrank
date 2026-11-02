import TR28.Counting
import TR28.LinearCount
import Mathlib.Tactic

/-! Must fail mathematically: with zero modes a local restriction cannot delete the empty tuple. -/
namespace TR28.Controls.ZeroModeExtraction
open TR28

def emptyEdge : SupportEdge 0 (fun _ => Fin 2) := fun i => Fin.elim0 i
def fullSupport : Finset (SupportEdge 0 (fun _ => Fin 2)) := {emptyEdge}
def candidates : Finset (SupportEdge 0 (fun _ => Fin 2)) := ∅
def localFilter (_ : Fin 0) : Finset (Fin 2) := ∅

example :
    restrictSupport fullSupport
        (retainedWords (isolatedCandidates fullSupport candidates localFilter)) =
      isolatedCandidates fullSupport candidates localFilter := by
  classical
  simp [restrictSupport, retainedWords, isolatedCandidates, survivingCandidates,
    fullSupport, candidates]

end TR28.Controls.ZeroModeExtraction
