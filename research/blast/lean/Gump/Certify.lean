/-
Certified still lifes and oscillators. A list stepper `stepL`, proved equal to `Gump.step`, small enough
for Lean's kernel to evaluate; and a checker `isOsc L P` whose `true` is a proof that the finite pattern
L is an oscillator of exact period P under `Gump.run` (a still life when P = 1).

Usage: `example : isOsc [⟨1,2,2⟩, ...] 1 = true := by decide +kernel`, then `isOsc_spec`.
-/
import Gump.FiniteCorrect

namespace Gump

/-- The configuration of a finite list of points. -/
def lcfg (L : List Pt) : Config := fun p => L.contains p

theorem lcfg_iff (L : List Pt) (p : Pt) : lcfg L p = true ↔ p ∈ L := by
  simp [lcfg]

/-- Live points and their neighbours. -/
def lcand (L : List Pt) : List Pt := L.flatMap fun p => p :: nbrs p

/-- One generation of a finite list (without duplicates). -/
def stepL (L : List Pt) : List Pt := ((lcand L).filter (step (lcfg L))).eraseDups

/-- **The list stepper is `step`.** -/
theorem lcfg_stepL (L : List Pt) : lcfg (stepL L) = step (lcfg L) := by
  funext p
  apply Bool.eq_iff_iff.mpr
  rw [lcfg_iff, stepL, List.mem_eraseDups, List.mem_filter]
  constructor
  · exact fun h => h.2
  · intro h
    refine ⟨?_, h⟩
    simp only [lcand, List.mem_flatMap, List.mem_cons]
    rcases step_support _ p h with hp | ⟨r, hr, hpr⟩
    · exact ⟨p, (lcfg_iff L p).mp hp, Or.inl rfl⟩
    · exact ⟨r, (lcfg_iff L r).mp hr, Or.inr hpr⟩

/-- n generations of a finite list. -/
def runL (L : List Pt) : Nat → List Pt
  | 0 => L
  | n + 1 => stepL (runL L n)

theorem lcfg_runL (L : List Pt) : ∀ n, lcfg (runL L n) = run (lcfg L) n
  | 0 => rfl
  | n + 1 => by rw [runL, lcfg_stepL, lcfg_runL L n]; rfl

/-- Two lists hold the same points. -/
def sameL (A B : List Pt) : Bool := A.all (B.contains ·) && B.all (A.contains ·)

theorem sameL_iff (A B : List Pt) : sameL A B = true ↔ lcfg A = lcfg B := by
  simp only [sameL, Bool.and_eq_true, List.all_eq_true, List.contains_iff_mem]
  constructor
  · rintro ⟨h1, h2⟩
    funext p
    apply Bool.eq_iff_iff.mpr
    rw [lcfg_iff, lcfg_iff]
    exact ⟨h1 p, h2 p⟩
  · intro h
    refine ⟨fun p hp => ?_, fun p hp => ?_⟩
    · have := (lcfg_iff A p).mpr hp
      rw [h, lcfg_iff] at this
      exact this
    · have := (lcfg_iff B p).mpr hp
      rw [← h, lcfg_iff] at this
      exact this

/-- `oscCheck L0 k L`: the states L, stepL L, ..., k - 1 steps on differ from L0, and k steps on equal it. -/
def oscCheck (L0 : List Pt) : Nat → List Pt → Bool
  | 0, L => sameL L L0
  | k + 1, L => !sameL L L0 && oscCheck L0 k (stepL L)

/-- L is an oscillator of exact period P (a still life if P = 1). -/
def isOsc (L : List Pt) (P : Nat) : Bool := match P with
  | 0 => false
  | k + 1 => oscCheck L k (stepL L)

theorem oscCheck_spec (L0 : List Pt) : ∀ k L, oscCheck L0 k L = true →
    lcfg (runL L k) = lcfg L0 ∧ ∀ j, j < k → lcfg (runL L j) ≠ lcfg L0
  | 0, L, h => ⟨(sameL_iff _ _).mp h, fun j hj => absurd hj (Nat.not_lt_zero j)⟩
  | k + 1, L, h => by
    simp only [oscCheck, Bool.and_eq_true, Bool.not_eq_true'] at h
    obtain ⟨h1, h2⟩ := oscCheck_spec L0 k (stepL L) h.2
    have shift : ∀ j, runL (stepL L) j = runL L (j + 1) := by
      intro j
      induction j with
      | zero => rfl
      | succ j ih => rw [runL, ih]; rfl
    refine ⟨by rw [← shift]; exact h1, fun j hj => ?_⟩
    cases j with
    | zero =>
      intro he
      have := (sameL_iff L L0).mpr he
      rw [this] at h
      exact Bool.noConfusion h.1
    | succ j => rw [← shift]; exact h2 j (by omega)

/-- **A checked oscillator.** If `isOsc L P` evaluates to `true`, the pattern returns to itself after
exactly P generations of `Gump.run`, and not before. -/
theorem isOsc_spec (L : List Pt) (P : Nat) (h : isOsc L P = true) :
    0 < P ∧ run (lcfg L) P = lcfg L ∧ ∀ k, 0 < k → k < P → run (lcfg L) k ≠ lcfg L := by
  cases P with
  | zero => exact absurd h (by simp [isOsc])
  | succ k =>
    obtain ⟨h1, h2⟩ := oscCheck_spec L k (stepL L) h
    have shift : ∀ j, runL (stepL L) j = runL L (j + 1) := by
      intro j
      induction j with
      | zero => rfl
      | succ j ih => rw [runL, ih]; rfl
    refine ⟨Nat.succ_pos k, ?_, fun j hj0 hjP => ?_⟩
    · rw [← lcfg_runL, ← shift]; exact h1
    · rw [← lcfg_runL]
      obtain ⟨i, rfl⟩ : ∃ i, j = i + 1 := ⟨j - 1, by omega⟩
      rw [← shift]
      exact h2 i (by omega)

/-- **The six faces of a cube are a still life** (`docs/AUTOMATON.md`; catalogue entry S6a). -/
theorem cube_still : run (lcfg [⟨1, 0, 0⟩, ⟨-1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨0, -1, 0⟩, ⟨0, 0, 1⟩, ⟨0, 0, -1⟩]) 1 =
    lcfg [⟨1, 0, 0⟩, ⟨-1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨0, -1, 0⟩, ⟨0, 0, 1⟩, ⟨0, 0, -1⟩] :=
  (isOsc_spec _ 1 (by decide +kernel)).2.1

end Gump
