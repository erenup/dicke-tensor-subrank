import Mathlib.Data.Fintype.BigOperators
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.FieldTheory.Finiteness
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Prod
import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Data.Set.Finite.Lemmas
import Mathlib.Data.Real.Basic

/-! Literal finite collision, support-restriction and submodule definitions. -/

noncomputable section
namespace TR28
universe u
open scoped BigOperators

/-- The literal relation fiber in the entire finite alphabet. -/
def relationFiber {Ω : Type*} [Fintype Ω] (R : Ω → Ω → Prop) (s : Ω) : Finset Ω := by
  classical
  exact Finset.univ.filter (R s)

/-- The full joint histogram of the first word. -/
def fullTypeCount {Ω : Type*} [Fintype Ω] {N : ℕ} (I : Fin N → Ω) (s : Ω) : ℕ := by
  classical
  exact (Finset.univ.filter (fun t => I t = s)).card

/-- All partner words in Ω^N. In particular, no histogram condition is imposed on J. -/
def allPartners {Ω : Type*} [Fintype Ω] {N : ℕ}
    (R : Ω → Ω → Prop) (I : Fin N → Ω) : Finset (Fin N → Ω) := by
  classical
  exact Finset.univ.filter (fun J => ∀ t, R (I t) (J t))

/-- Balanced full joint type, a property only of the indicated word. -/
def balancedFullType {Ω : Type*} [Fintype Ω] {N : ℕ}
    (I : Fin N → Ω) (c : ℕ) : Prop := ∀ s, fullTypeCount I s = c

/-- Actual coset membership for an arbitrary finite rational support. -/
def rationalCollisionRelation {k : ℕ} (S : Finset (Fin k → ℚ))
    (V : Submodule ℚ (Fin k → ℚ)) (s t : S) : Prop := t.val - s.val ∈ V

/-- The actual rational span of every column difference; no rank is supplied as a premise. -/
def differenceSpan {k N : ℕ} {S : Finset (Fin k → ℚ)}
    (I J : Fin N → S) : Submodule ℚ (Fin k → ℚ) :=
  Submodule.span ℚ (Set.range (fun t => (J t).val - (I t).val))

/-- All full-support partners having exactly the prescribed difference span. -/
def exactSpanPartners {k N : ℕ} (S : Finset (Fin k → ℚ))
    (V : Submodule ℚ (Fin k → ℚ)) (I : Fin N → S) : Finset (Fin N → S) := by
  classical
  exact Finset.univ.filter (fun J => differenceSpan I J = V)

/-- Every vector satisfying the homogeneous linear constraints. -/
def kernelSolutions {K : Type*} [Field K] [Fintype K] {N r : ℕ}
    (A : (Fin N → K) →ₗ[K] (Fin r → K)) : Finset (Fin N → K) := by
  classical
  exact Finset.univ.filter (fun x => A x = 0)

/-- A literal edge of the original multipartite support. -/
abbrev SupportEdge (k : ℕ) (α : Fin k → Type u) := (i : Fin k) → α i

/-- Delete local coordinates separately in every mode, starting from the full support E. -/
noncomputable def restrictSupport {k : ℕ} {α : Fin k → Type u}
    (E : Finset (SupportEdge k α)) (L : (i : Fin k) → Finset (α i)) :
    Finset (SupportEdge k α) := by
  classical
  exact E.filter (fun e => ∀ i, e i ∈ L i)

/-- A is only the candidate counting class; its surviving members are intersected with E. -/
noncomputable def survivingCandidates {k : ℕ} {α : Fin k → Type u}
    (E A : Finset (SupportEdge k α)) (L : (i : Fin k) → Finset (α i)) :
    Finset (SupportEdge k α) := by
  classical
  exact A ∩ restrictSupport E L

/-- Ordered collisions: first edge is a surviving candidate, second is any
other surviving original edge; a pair is counted once even if it shares several modes. -/
noncomputable def orderedCollisions {k : ℕ} {α : Fin k → Type u}
    (E A : Finset (SupportEdge k α)) (L : (i : Fin k) → Finset (α i)) :
    Finset (SupportEdge k α × SupportEdge k α) := by
  classical
  exact ((survivingCandidates E A L).product (restrictSupport E L)).filter
    (fun p => p.1 ≠ p.2 ∧ ∃ i, p.1 i = p.2 i)

/-- The selected candidates are computed from collision absence in the full
surviving original support, rather than supplied with an isolation hypothesis. -/
noncomputable def isolatedCandidates {k : ℕ} {α : Fin k → Type u}
    (E A : Finset (SupportEdge k α)) (L : (i : Fin k) → Finset (α i)) :
    Finset (SupportEdge k α) := by
  classical
  exact (survivingCandidates E A L).filter
    (fun e => ∀ f ∈ restrictSupport E L, (∃ i, e i = f i) → f = e)

/-- The actual local coordinate sets retained in the final restriction. -/
noncomputable def retainedWords {k : ℕ} {α : Fin k → Type u}
    (I : Finset (SupportEdge k α)) (i : Fin k) : Finset (α i) := by
  classical
  exact I.image (fun e => e i)

/-- An actual rational subspace is fixed by each listed linear automorphism. -/
def InvariantUnder {E : Type*} [AddCommGroup E] [Module ℚ E]
    (A : Set (E ≃ₗ[ℚ] E)) (V : Submodule ℚ E) : Prop :=
  ∀ g ∈ A, V.map g.toLinearMap = V

/-- Irreducibility stated directly on actual rational subspaces. -/
def IrreducibleUnder {E : Type*} [AddCommGroup E] [Module ℚ E]
    (A : Set (E ≃ₗ[ℚ] E)) : Prop :=
  ∀ V : Submodule ℚ E, InvariantUnder A V → V = ⊥ ∨ V = ⊤

/-- The explicit supermodular inequality; this is an input, not an entropy theorem. -/
def SubmoduleSupermodular {E : Type*} [AddCommGroup E] [Module ℚ E]
    (F : Submodule ℚ E → ℝ) : Prop :=
  ∀ U V, F U + F V ≤ F (U ⊔ V) + F (U ⊓ V)


end TR28
