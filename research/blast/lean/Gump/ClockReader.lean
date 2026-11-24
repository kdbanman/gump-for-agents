/-
**capL of the clock eats every word and remembers nothing** (`research/signals/README.md` section 15, `prove_reader.py`).
Put capL (the clock's left cap, units −4 .. −1) at the −v end of a tape holding any word w over {B, C} on the units
≥ 0 (`readerC w`). Two generations later the state is capL and the tape moved on one unit, cell for cell
(`reader_step`); so at every even generation 2n it is capL and the word w moved n units (`reader_run`): the cap
swallows the word letter by letter, sends nothing back into the tape, and keeps no trace of what it ate.

The proof is local: tape windows on the units ≥ 2, empty space on the units ≤ −7, and on the units −6 .. 1 one
kernel check for each of the 16 words on the units 0 .. 3 (`readerOK_ok`), which are the source's closed set of 16
cap states.
-/
import Gump.ClockLit

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-- capL on the units < 0, the tape of w on the units ≥ 0. -/
def readerC (w : Int → Letter) : Config := fun p => if unitOf p < 0 then lcfg capL p else tape w p

/-- The same, unit by unit, in hex letters. -/
def RW (w : Int → Letter) (u : Int) : List Pt := if u < 0 then capLU u else hexCells (hexOf (w u))

theorem RW_unit (w : Int → Letter) : ∀ u, ∀ q ∈ RW w u, unitOf q = 0 := by
  intro u; unfold RW; split; exact capLU_unit u; exact hexCells_unit _

theorem readerC_eq (w : Int → Letter) : readerC w = ucfg (RW w) := by
  funext p
  simp only [readerC, capL_ucfg, tape_eq_hcfg]
  by_cases h : unitOf p < 0
  · rw [if_pos h]; simp only [ucfg, RW, if_pos h]
  · rw [if_neg h]; simp only [ucfg, hcfg, RW, if_neg h]

/-- The zone at the cap for the letters σ on the units 0 .. 3 (moved one unit after the double step). -/
def rzN (σ : List Nat) (v : Int) : List Pt := if v < 0 then capLU v else hexCells (σ.getD v.toNat 11)
def rzT (σ : List Nat) (v : Int) : List Pt := if v < 0 then capLU v else hexCells (σ.getD (v + 1).toNat 11)

theorem rzN_unit (σ : List Nat) : ∀ u, ∀ q ∈ rzN σ u, unitOf q = 0 := by
  intro u; unfold rzN; split; exact capLU_unit u; exact hexCells_unit _
theorem rzT_unit (σ : List Nat) : ∀ u, ∀ q ∈ rzT σ u, unitOf q = 0 := by
  intro u; unfold rzT; split; exact capLU_unit u; exact hexCells_unit _

def readerZone (σ : List Nat) : Bool := pieceCheck (rzN σ) (rzT σ) (-8) 12 [] [] 2 (-6) 1 litFrame

/-- The 16 cap states: capL and every word on the units 0 .. 3. -/
theorem readerOK_ok (a0 a1 a2 a3 : Bool) : readerZone [b2h a0, b2h a1, b2h a2, b2h a3] = true := by
  cases a0 <;> cases a1 <;> cases a2 <;> cases a3 <;> decide +kernel

theorem hexOf_cases (l : Letter) : hexOf l = 7 ∨ hexOf l = 11 := by cases l <;> simp [hexOf]

set_option maxHeartbeats 1000000 in
/-- **Two generations of capL on any word**: capL, and the word moved one unit. -/
theorem reader_step (w : Int → Letter) : run (readerC w) 2 = readerC (fun u => w (u + 1)) := by
  rw [readerC_eq, readerC_eq]
  funext p
  by_cases hA : unitOf p ≤ -7
  · have off : ∀ (w' : Int → Letter) (q : Pt), unitOf q < -4 → ucfg (RW w') q = false := by
      intro w' q hq; simp only [ucfg, RW, if_pos (show unitOf q < 0 by omega), capLU_nil' hq]; rfl
    rw [run2_empty _ p (fun q _ _ => off w q (by omega)), off _ p (by omega)]
  by_cases hB : unitOf p ≤ 1
  · obtain ⟨b0, e0⟩ := b2h_of (hexOf_cases (w 0))
    obtain ⟨b1, e1⟩ := b2h_of (hexOf_cases (w 1))
    obtain ⟨b2, e2⟩ := b2h_of (hexOf_cases (w 2))
    obtain ⟨b3, e3⟩ := b2h_of (hexOf_cases (w 3))
    have hz := readerOK_ok b0 b1 b2 b3
    unfold readerZone at hz
    refine step_zoneU (RW w) (RW (fun u => w (u + 1))) 0 (-6) 1 (-8) _ _ (rzN_unit _) (rzT_unit _) 12 litFrame
      litFrame_even (by decide) (by decide) hz (by decide) _ ?_ ?_ (fun _ _ _ => rfl) p (by omega) (by omega)
    · intro v h1 h2
      simp only [RW, rzN, Int.add_zero]
      by_cases hv : v < 0
      · simp only [if_pos hv]
      · simp only [if_neg hv]
        congr 1
        rcases (show v = 0 ∨ v = 1 ∨ v = 2 ∨ v = 3 by omega) with rfl | rfl | rfl | rfl
        · exact e0
        · exact e1
        · exact e2
        · exact e3
    · intro v h1 h2
      simp only [RW, rzT, Int.add_zero]
      by_cases hv : v < 0
      · simp only [if_pos hv]
      · simp only [if_neg hv]
        congr 1
        rcases (show v = 0 ∨ v = 1 by omega) with rfl | rfl
        · exact e1
        · exact e2
  · have h0 : ∀ (w' : Int → Letter) (q : Pt), 0 ≤ unitOf q → ucfg (RW w') q = hcfg (fun u => hexOf (w' u)) q := by
      intro w' q hq; simp only [ucfg, hcfg, RW, if_neg (show ¬ unitOf q < 0 by omega)]
    rw [h0 _ p (by omega)]
    apply step_left (fun u => hexOf (w u)) (fun u => hexOf (w (u + 1))) _ p
    · intro i _ _; exact hexOf_cases _
    · rfl
    · intro q h1 _; exact h0 w q (by omega)

/-- **capL eats every word and remembers nothing**: at generation 2n the state is capL and the word moved n units. -/
theorem reader_run (w : Int → Letter) : ∀ n : Nat, run (readerC w) (2 * n) = readerC (fun u => w (u + n))
  | 0 => by
    show readerC w = _
    congr 1; funext u; congr 1; omega
  | n + 1 => by
    rw [show 2 * (n + 1) = 2 * n + 2 by omega, run_add, reader_run w n, reader_step]
    congr 1; funext u; congr 1; push_cast; omega

end Gump.Clock
