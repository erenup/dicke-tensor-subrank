import TR28.Counting
import TR28.LinearCount
import Mathlib.Tactic

/-! Must fail mathematically: local endpoints of candidate edges retain an original crossing edge. -/
namespace TR28.Controls.CandidateOnlyIsolation
open TR28

def edge00 : SupportEdge 2 (fun _ => Fin 2) := ![0, 0]
def edge11 : SupportEdge 2 (fun _ => Fin 2) := ![1, 1]
def edge01 : SupportEdge 2 (fun _ => Fin 2) := ![0, 1]
def fullSupport : Finset (SupportEdge 2 (fun _ => Fin 2)) := {edge00, edge11, edge01}
def candidates : Finset (SupportEdge 2 (fun _ => Fin 2)) := {edge00, edge11}

example : restrictSupport fullSupport (retainedWords candidates) = candidates := by
  classical
  have hcross : edge01 ∈ restrictSupport fullSupport (retainedWords candidates) := by
    simp [restrictSupport, retainedWords, fullSupport, candidates, edge00, edge11, edge01,
      Fin.forall_fin_two]
  have hnot : edge01 ∉ candidates := by
    simp [candidates, edge00, edge11, edge01, Matrix.vecCons_inj]
  have hne : restrictSupport fullSupport (retainedWords candidates) ≠ candidates := by
    intro h
    rw [h] at hcross
    exact hnot hcross
  -- The false set equality reduces to False after exhibiting its actual crossing edge.
  simp only [hne]

end TR28.Controls.CandidateOnlyIsolation
