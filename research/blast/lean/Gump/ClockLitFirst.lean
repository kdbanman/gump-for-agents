/-
**At no earlier generation** (even N). For every even N ≥ 6 the lit clock of N units is on the cycle of `clockOf N`
from generation N − 2 on (`ClockLit.lit_clock`) and at no earlier generation (`lit_first_even`): its state at any
generation g < N − 2 is no state of that cycle. The witness is the left end: at generation N − 3 the units ≤ 2 of the
lit clock are the same for every even N (one generation of capL + C C B C, `lit_left`), while every state of the cycle
shows on its units ≤ 3 one of the 26 states of the base (`cycle_left`), and the kernel finds for each of the 26 a
cell of the units ≤ 2 where they differ (`firstCheck_ok`; the 26 cells from `tape_lit.py`). For odd N this argument
fails: at generation N − 3 the left end is that of base times 11, 15, 19, 23, so the odd case is not proved here.
-/
import Gump.ClockLit

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-- The lit clock's units ≤ 3 at generation N − 4 (even N): capL, then C, C, B, C. -/
def FE (u : Int) : List Pt := if u < 0 then capLU u else if u ≤ 3 then hexCells (if u = 2 then 7 else 11) else []

theorem FE_unit : ∀ u, ∀ q ∈ FE u, unitOf q = 0 := by
  intro u; unfold FE; split
  · exact capLU_unit u
  · split
    · exact hexCells_unit _
    · simp

def bE : List Pt := (piece FE (-4) 8).map (· + frame)
def SE : Nat := ofList bE

/-- For each base time n, a cell of the units ≤ 2 where the base differs from the lit clock at generation N − 3. -/
def wit : List Pt := [⟨0, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨2, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨0, 0, 5⟩, ⟨-4, 0, 5⟩, ⟨0, 0, 3⟩, ⟨-4, 0, 5⟩,
  ⟨2, 0, 1⟩, ⟨-4, 0, 5⟩, ⟨0, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨2, 0, 1⟩, ⟨-4, 0, 5⟩, ⟨0, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨2, 0, 1⟩, ⟨-4, 0, 5⟩,
  ⟨0, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨2, 0, 1⟩, ⟨-4, 0, 5⟩, ⟨0, 0, 3⟩, ⟨-4, 0, 5⟩, ⟨2, 0, 1⟩, ⟨-4, 0, 5⟩]

def firstCheck : Bool :=
  bE.all inBox && inCore SE &&
    (List.range 26).all (fun n => decide (unitOf (wit.getD n ⟨0, 0, 0⟩) ≤ 2) &&
      (bcfg (brun bS n) (wit.getD n ⟨0, 0, 0⟩ + frame) != bcfg (brun SE 1) (wit.getD n ⟨0, 0, 0⟩ + frame)))

theorem firstCheck_ok : firstCheck = true := by decide +kernel

theorem LW_first (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) (u : Int) (h0 : 0 ≤ u) (h3 : u ≤ 3) :
    LW N (mmax N - 1) u = if u = 2 then 7 else 11 := by
  obtain ⟨k, rfl⟩ : ∃ k, N = 2 * k := ⟨N / 2, by omega⟩
  unfold LW mmax; repeat' split
  all_goals omega

theorem FE_lcfg : ucfg FE = lcfg (piece FE (-4) 8) := by
  funext q
  rw [lcfg_piece _ FE_unit]
  by_cases h : -4 ≤ unitOf q ∧ unitOf q < -4 + ((8 : Nat) : Int)
  · rw [decide_eq_true h, Bool.true_and]
  · rw [decide_eq_false h, Bool.false_and]
    simp only [ucfg, FE]
    by_cases h0 : unitOf q < 0
    · rw [if_pos h0, capLU_nil' (by push_cast at h; omega)]; rfl
    · rw [if_neg h0, if_neg (by push_cast at h; omega)]; rfl

theorem FL_FE (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) (u : Int) (hu : u ≤ 3) : FL N (mmax N - 1) u = FE u := by
  unfold FL FE
  by_cases h0 : u < 0
  · rw [if_pos h0, if_pos h0]
  · rw [if_neg h0, if_neg h0, if_pos (show u < (N : Int) by omega), if_pos hu, LW_first N h6 he u (by omega) hu]

/-- The lit clock's units ≤ 2 at generation N − 3, for every even N ≥ 6. -/
theorem lit_left (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) (q : Pt) (hq : unitOf q ≤ 2) :
    run (lcfg (litList N)) (N - 3) q = bcfg (brun SE 1) (q + frame) := by
  have hc := firstCheck_ok
  simp only [firstCheck, Bool.and_eq_true] at hc
  obtain ⟨⟨hin, hcore⟩, -⟩ := hc
  have h4 : N - 3 = 2 * (mmax N - 1) + 1 := by unfold mmax; omega
  rw [h4, run_add, lit_word N h6 _ (by omega)]
  rw [run_eq_of_units (c' := ucfg FE) 1 (fun q' h1 h2 => ?_)]
  · rw [FE_lcfg, ← run_lcfg_map_add _ frame_even 1 q]
    show run (lcfg bE) 1 (q + frame) = _
    rw [← bcfg_ofList _ hin, show ofList bE = SE from rfl,
      run_bcfg_of_core (fun j hj => by obtain rfl : j = 0 := by omega
                                       exact hcore)]
  · simp only [ucfg]
    rw [FL_FE N h6 he _ (by omega)]

/-- Every state of the cycle of `clockOf N` (N ≥ 6) shows on its units ≤ 3 one of the 26 states of the base. -/
theorem cycle_left (N : Nat) (h6 : 6 ≤ N) (k : Nat) :
    ∃ n, n < 26 ∧ ∀ q, unitOf q ≤ 3 → run (clockOf N) k q = bcfg (brun bS n) (q + frame) := by
  have hP := (clock_cycle (N - 6)).1
  have hm := run_mul_period _ _ hP
  have e : run (clockY (N - 6)) k = run (clockY (N - 6)) (k % (4 * (6 + (N - 6)) + 2)) := by
    have := congrArg (run (clockY (N - 6))) (Nat.div_add_mod k (4 * (6 + (N - 6)) + 2)).symm
    rw [this, run_add, hm]
  have hlt : k % (4 * (6 + (N - 6)) + 2) ≤ 26 + 4 * (N - 6) := by
    have := Nat.mod_lt k (show 0 < 4 * (6 + (N - 6)) + 2 by omega); omega
  refine ⟨((chart (N - 6) 0 (5 + ((k % (4 * (6 + (N - 6)) + 2) : Nat) : Int)) + 7) % 26).toNat, by omega, ?_⟩
  intro q hq
  rw [clockOf, if_neg (show ¬ N ≤ 5 by omega), e, clockY_run _ _ hlt]
  simp only [surg]
  have hi : cidx 3 (N - 6) q = 0 := by simp only [cidx]; omega
  rw [hi, show -(0 : Int) = 0 from rfl, shiftPt_zero, Xb_frame]

/-- **At no earlier generation**: for every even N ≥ 6, no state of the lit clock before generation N − 2 is a state
of the cycle of `clockOf N`. -/
theorem lit_first_even (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) (g : Nat) (hg : g < N - 2) (k : Nat) :
    run (lcfg (litList N)) g ≠ run (clockOf N) k := by
  intro e
  have e' : run (lcfg (litList N)) (g + (N - 3 - g)) = run (clockOf N) (k + (N - 3 - g)) := by
    rw [run_add, e, ← run_add]
  rw [show g + (N - 3 - g) = N - 3 by omega] at e'
  obtain ⟨n, hn, hR⟩ := cycle_left N h6 (k + (N - 3 - g))
  have hc := firstCheck_ok
  simp only [firstCheck, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hc
  obtain ⟨h1, h2⟩ := hc.2 n hn
  have hu : unitOf (wit.getD n ⟨0, 0, 0⟩) ≤ 2 := of_decide_eq_true h1
  have := congrFun e' (wit.getD n ⟨0, 0, 0⟩)
  rw [lit_left N h6 he _ hu, hR _ (by omega)] at this
  rw [this] at h2
  simp at h2

/-- **The lit clock of even length, exactly**: on the cycle of `clockOf N` from generation N − 2, and not before. -/
theorem lit_enters_exact (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) :
    (∃ s, run (lcfg (litList N)) (N - 2) = run (clockOf N) s) ∧
    ∀ g, g < N - 2 → ∀ k, run (lcfg (litList N)) g ≠ run (clockOf N) k := by
  refine ⟨(lit_clock N (by omega) (N - 2) ?_).1, fun g hg k => lit_first_even N h6 he g hg k⟩
  simp only [litEntry, if_neg (show ¬ N ≤ 5 by omega), mmax]; omega

end Gump.Clock
