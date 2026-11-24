/-
**The tape theorem** (`research/signals/README.md` section 10, "The tape"; reviewed in
`research/audit/REVIEW-signals-2.md` row 5 and re-derived in `REVIEW-signals-9.md` section 3, part A).

Wire C and wire B run along v = (1, 0, −1) with one unit per move τ = (2, 0, −2). At an even generation a unit
of wire C holds the five cells (0,1,2), (0,1,4), (0,2,3), (1,0,0), (1,0,2) moved by its index times τ, and a
unit of wire B the same with (0,2,3) replaced by (1,0,4) (the hex digits `b` and `7` of the scripts). A word
w : ℤ → {B, C} is the configuration `tape w` whose unit u is a unit of wire w(u), on the whole lattice.

`tape_run`: for every word, two generations move the whole configuration one unit towards −v:
run (tape w) (2n) = tape (u ↦ w (u + n)). `tape_local_run` is the form the gluing arguments use: any
configuration that is a tape word on a stretch of units is, 2n generations later, the shifted word on the stretch
shortened by 2n units at each end, whatever lies outside.

The proof is the source's: two generations of a unit read the two units on either side (`run_eq_of_units`, from
the light cone), so the claim is local, and the 32 windows of five letters are checked by the kernel on the
bit-parallel stepper (`window_ok`, `decide +kernel`); translation along the wire (`run_shiftC`) carries a window
from unit 0 to any unit. The source checked the 32 windows on one ring of 40 units; here each is a finite run of
its own five units in empty space, which is what the light cone needs.
-/
import Gump.TapeBase

namespace Gump.Tape
open Gump

/-- The two letters of the tape: a unit of wire B or of wire C. -/
inductive Letter where
  | B | C
deriving DecidableEq, Repr

/-- The cells of unit 0 of wire B and of wire C at an even generation. -/
def cellsOf : Letter → List Pt
  | .C => [⟨0, 1, 2⟩, ⟨0, 1, 4⟩, ⟨0, 2, 3⟩, ⟨1, 0, 0⟩, ⟨1, 0, 2⟩]
  | .B => [⟨0, 1, 2⟩, ⟨0, 1, 4⟩, ⟨1, 0, 0⟩, ⟨1, 0, 2⟩, ⟨1, 0, 4⟩]

/-- **The tape of a word** w : ℤ → {B, C}: unit u is a unit of wire w(u), moved u units along the wire. -/
def tape (w : Int → Letter) : Config := fun p => lcfg (cellsOf (w (unitOf p))) (shiftPt (-unitOf p) p)

theorem cellsOf_unit (l : Letter) : ∀ q ∈ cellsOf l, unitOf q = 0 := by
  cases l <;> decide

theorem unitOf_of_lcfg {l : Letter} {q : Pt} (h : lcfg (cellsOf l) q = true) : unitOf q = 0 :=
  cellsOf_unit l q ((lcfg_iff _ _).mp h)

/-- A finite word placed on the units a, a + 1, … -/
def wordList : Int → List Letter → List Pt
  | _, [] => []
  | a, l :: ls => (cellsOf l).map (shiftPt a) ++ wordList (a + 1) ls

theorem lcfg_append (A B : List Pt) (p : Pt) : lcfg (A ++ B) p = (lcfg A p || lcfg B p) := by
  simp [lcfg]

theorem lcfg_nil (p : Pt) : lcfg [] p = false := rfl

/-- What a placed word holds at a point. -/
theorem lcfg_wordList : ∀ (ls : List Letter) (a : Int) (p : Pt), lcfg (wordList a ls) p =
    (decide (a ≤ unitOf p ∧ unitOf p < a + ls.length) &&
      lcfg (cellsOf (ls.getD (unitOf p - a).toNat .C)) (shiftPt (-unitOf p) p))
  | [], a, p => by simp only [wordList, lcfg_nil, List.length_nil]; simp; omega
  | l :: ls, a, p => by
    rw [wordList, lcfg_append, lcfg_map_shiftPt, lcfg_wordList ls (a + 1) p]
    simp only [shiftC, List.length_cons]
    by_cases hu : unitOf p = a
    · have e1 : decide (a + 1 ≤ unitOf p ∧ unitOf p < a + 1 + (ls.length : Int)) = false := by
        simp only [decide_eq_false_iff_not]; omega
      have e2 : decide (a ≤ unitOf p ∧ unitOf p < a + ((ls.length + 1 : Nat) : Int)) = true := by
        simp only [decide_eq_true_eq]; omega
      rw [e1, e2, Bool.false_and, Bool.or_false, Bool.true_and, hu, Int.sub_self, Int.toNat_zero,
        List.getD_cons_zero]
    · have h0 : lcfg (cellsOf l) (shiftPt (-a) p) = false := by
        cases e : lcfg (cellsOf l) (shiftPt (-a) p)
        · rfl
        · have := unitOf_of_lcfg e
          simp only [unitOf_shiftPt] at this
          omega
      rw [h0, Bool.false_or]
      by_cases hr : a + 1 ≤ unitOf p ∧ unitOf p < a + 1 + (ls.length : Int)
      · have hr' : a ≤ unitOf p ∧ unitOf p < a + ((ls.length + 1 : Nat) : Int) := by omega
        simp only [hr, hr']
        have e : (unitOf p - a).toNat = (unitOf p - (a + 1)).toNat + 1 := by omega
        rw [e, List.getD_cons_succ]
      · have hr' : ¬ (a ≤ unitOf p ∧ unitOf p < a + ((ls.length + 1 : Nat) : Int)) := by omega
        simp only [hr, hr', decide_false, Bool.false_and]

/-! ### The 32 windows, checked by the kernel -/

open Bits in
/-- A window of five letters on the units −2 .. 2: after two generations, unit 0 holds a unit of the letter that
was on unit 1. -/
def windowCheck (σ : List Letter) : Bool :=
  let L := wordList (-2) σ
  let S := ofList L
  L.all inBox && inCore S && inCore (bstep S) &&
    eqOn (unitMask 0 0) (brun S 2) (ofList (cellsOf (σ.getD 3 .C))) && (cellsOf (σ.getD 3 .C)).all inBox

theorem window_ok (a0 a1 a2 a3 a4 : Letter) : windowCheck [a0, a1, a2, a3, a4] = true := by
  cases a0 <;> cases a1 <;> cases a2 <;> cases a3 <;> cases a4 <;> decide +kernel

open Bits in
theorem window_spec (σ : List Letter) (h : windowCheck σ = true) (p : Pt) (hp : unitOf p = 0) :
    run (lcfg (wordList (-2) σ)) 2 p = lcfg (cellsOf (σ.getD 3 .C)) p := by
  simp only [windowCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩ := h
  rw [← bcfg_ofList _ h1, ← bcfg_ofList _ h5, run_bcfg_of_core (n := 2) (fun j hj => by
    rcases (show j = 0 ∨ j = 1 by omega) with rfl | rfl
    · exact h2
    · exact h3)]
  exact eqOn_spec (by decide) (by decide) (by decide) h4 p (by omega) (by omega)

/-! ### The tape theorem -/

/-- **The tape theorem, one double step, local form.** If a configuration agrees with the tape of w on the five
units around p, then two generations later p holds what the tape of the shifted word holds. -/
theorem tape_local (c : Config) (w : Int → Letter) (p : Pt)
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = tape w q) :
    run c 2 p = tape (fun u => w (u + 1)) p := by
  let u := unitOf p
  let σ : List Letter := [w (u - 2), w (u - 1), w u, w (u + 1), w (u + 2)]
  have key : ∀ d : Int, -2 ≤ d → d ≤ 2 → σ.getD (d + 2).toNat .C = w (u + d) := by
    intro d h1 h2
    rcases (show d = -2 ∨ d = -1 ∨ d = 0 ∨ d = 1 ∨ d = 2 by omega) with rfl | rfl | rfl | rfl | rfl <;>
      simp [σ] <;> congr 1 <;> omega
  have agree : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 →
      c q = shiftC u (lcfg (wordList (-2) σ)) q := by
    intro q h1 h2
    rw [h q h1 h2]
    simp only [shiftC, tape, lcfg_wordList, unitOf_shiftPt, shiftPt_shiftPt]
    have r1 : -2 ≤ unitOf q + -u ∧ unitOf q + -u < -2 + (σ.length : Int) := by
      simp only [σ, List.length_cons, List.length_nil]; omega
    rw [decide_eq_true r1, Bool.true_and]
    rw [show unitOf q + -u - -2 = (unitOf q - u) + 2 by omega, key _ (by omega) (by omega),
      show u + (unitOf q - u) = unitOf q by omega, show -(unitOf q + -u) + -u = -unitOf q by omega]
  rw [run_eq_of_units 2 (fun q h1 h2 => agree q (by omega) (by omega)), run_shiftC]
  simp only [shiftC]
  rw [window_spec σ (window_ok _ _ _ _ _) _ (by simp only [unitOf_shiftPt]; omega)]
  simp only [tape]
  have k1 := key 1 (by decide) (by decide)
  simp only [show ((1 : Int) + 2).toNat = 3 from rfl] at k1
  rw [k1]

/-- **The tape theorem, local form.** A configuration that is the tape of w on the units a − 2n .. b + 2n is,
2n generations later, the tape of w shifted by n on the units a .. b, whatever lies outside. -/
theorem tape_local_run (w : Int → Letter) (a b : Int) :
    ∀ (n : Nat) (c : Config), (∀ q, a - 2 * n ≤ unitOf q → unitOf q ≤ b + 2 * n → c q = tape w q) →
      ∀ p, a ≤ unitOf p → unitOf p ≤ b → run c (2 * n) p = tape (fun u => w (u + n)) p := by
  intro n
  induction n generalizing w with
  | zero =>
    intro c h p h1 h2
    change c p = _
    rw [h p (by omega) (by omega)]
    simp
  | succ n ih =>
    intro c h p h1 h2
    rw [show 2 * (n + 1) = 2 + 2 * n by omega, run_add]
    have := ih (fun u => w (u + 1)) (run c 2) (fun q h1 h2 => tape_local c w q (fun q' h1' h2' =>
      h q' (by push_cast at *; omega) (by push_cast at *; omega))) p h1 h2
    rw [this]
    simp only [tape]
    congr 3
    push_cast; omega

/-- **The tape theorem.** For every word w over {B, C}, on the whole lattice, 2n generations move the tape n
units towards −v: unit u then holds the letter that was on unit u + n. -/
theorem tape_run (w : Int → Letter) (n : Nat) : run (tape w) (2 * n) = tape (fun u => w (u + n)) := by
  funext p
  exact tape_local_run w (unitOf p) (unitOf p) n (tape w) (fun _ _ _ => rfl) p (Int.le_refl _) (Int.le_refl _)

/-- The same, as a rigid motion: the state after 2n generations is the start moved n units towards −v. -/
theorem tape_run_shift (w : Int → Letter) (n : Nat) : run (tape w) (2 * n) = fun p => tape w (shiftPt n p) := by
  rw [tape_run]
  funext p
  simp only [tape, unitOf_shiftPt, shiftPt_shiftPt]
  congr 2
  omega

/-- Wire C (every letter C) and wire B (every letter B) have period dividing 2. -/
theorem wire_two (l : Letter) : run (tape fun _ => l) 2 = tape fun _ => l := by
  have := tape_run (fun _ => l) 1
  simpa using this

end Gump.Tape
