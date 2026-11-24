/-
**The odd lit clocks enter at N − 2** (completing `ClockLit.lit_enters` for odd N). For odd N ≥ 7 the lit clock at
generation N − 2 (an odd generation, one after the word `FL N (mmax N − 1)`) is the state of `clockOf N` at generation
2(N − 6) + 2, the surgery's time 2(N − 6) + 7 (`lit_odd_entry`). At that time chart i shows base time 9 or 11 by the
parity of j − i, and chart j base time 7 (`chart_odd`); one generation of the word is checked against the base at
those times on three local pieces (`oddCheck_ok`: the left end, a three-unit window of the wire in each parity, the
right end). With `ClockLitFirst.lit_first` the lit clock of every N ≥ 6 enters the cycle of `clockOf N` exactly at
generation N − 2 (`lit_enters_at`).
-/
import Gump.ClockLitFirst

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits Gump.Unzip

set_option maxHeartbeats 4000000 in
theorem chart_odd (j : Nat) (i : Int) (h0 : 0 ≤ i) (h1 : i ≤ j) :
    chart j i (2 * j + 7) = if i = j then 7 else if ((j : Int) - i) % 2 = 1 then 9 else 11 := by
  simp only [chart, first]
  repeat' split
  all_goals omega

/-- The word at generation N − 3 (odd N) on the units ≤ 4: capL, C B C B C. -/
def FLo (u : Int) : List Pt :=
  if u < 0 then capLU u else if u ≤ 4 then hexCells (if u % 2 = 1 then 7 else 11) else []
/-- A window of the wire: b on unit 3, a on the units 2 and 4. -/
def WM (a b : Nat) (v : Int) : List Pt := if v = 3 then hexCells b else if v = 2 ∨ v = 4 then hexCells a else []
/-- The word at generation N − 3 (odd N) on the units ≥ N − 4, moved back N − 6 units: B C f C capR. -/
def FRo (v : Int) : List Pt :=
  if v < 2 then [] else if v = 2 then hexCells 7 else if v = 3 then hexCells 11 else if v = 4 then hexCells 15
  else if v = 5 then hexCells 11 else capRU (v - 6)

theorem FLo_unit : ∀ u, ∀ q ∈ FLo u, unitOf q = 0 := by
  intro u; unfold FLo; split
  · exact capLU_unit u
  · split
    · exact hexCells_unit _
    · simp
theorem WM_unit (a b : Nat) : ∀ u, ∀ q ∈ WM a b u, unitOf q = 0 := by
  intro u; unfold WM; split
  · exact hexCells_unit _
  · split
    · exact hexCells_unit _
    · simp
theorem FRo_unit : ∀ u, ∀ q ∈ FRo u, unitOf q = 0 := by
  intro u; unfold FRo; split
  · simp
  · split
    · exact hexCells_unit _
    · split
      · exact hexCells_unit _
      · split
        · exact hexCells_unit _
        · split
          · exact hexCells_unit _
          · exact capRU_unit _

def pL : List Pt := (piece FLo (-4) 9).map (· + frame)
def pW (a b : Nat) : List Pt := (piece (WM a b) 2 3).map (· + frame)
def pR : List Pt := (piece FRo 2 8).map (· + frame)

def oddCheck : Bool :=
  pL.all inBox && (pW 11 7).all inBox && (pW 7 11).all inBox && pR.all inBox &&
  inCore (ofList pL) && inCore (ofList (pW 11 7)) && inCore (ofList (pW 7 11)) && inCore (ofList pR) &&
  eqOn (unitMask (-8) 11) (brun (ofList pL) 1) (brun bS 16) &&
  eqOn (unitMask 11 11) (brun (ofList (pW 11 7)) 1) (brun bS 16) &&
  eqOn (unitMask 11 11) (brun (ofList (pW 7 11)) 1) (brun bS 18) &&
  eqOn (unitMask 11 23) (brun (ofList pR) 1) (brun bS 14)

theorem oddCheck_ok : oddCheck = true := by decide +kernel

/-- One generation of a word given on the units a .. a + n − 1, in the box. -/
theorem ucfg_run1 (F : Int → List Pt) (hF : ∀ u, ∀ q ∈ F u, unitOf q = 0) (a : Int) (n : Nat)
    (hlo : ∀ u, u < a → F u = []) (hhi : ∀ u, a + n ≤ u → F u = [])
    (hin : ((piece F a n).map (· + frame)).all inBox = true) (hc : inCore (ofList ((piece F a n).map (· + frame))) = true)
    (q : Pt) : run (ucfg F) 1 q = bcfg (brun (ofList ((piece F a n).map (· + frame))) 1) (q + frame) := by
  have e : ucfg F = lcfg (piece F a n) := by
    funext p
    rw [lcfg_piece _ hF]
    by_cases h : a ≤ unitOf p ∧ unitOf p < a + n
    · rw [decide_eq_true h, Bool.true_and]
    · rw [decide_eq_false h, Bool.false_and]
      simp only [ucfg]
      by_cases h1 : unitOf p < a
      · rw [hlo _ h1]; rfl
      · rw [hhi _ (by omega)]; rfl
  rw [e, ← run_lcfg_map_add _ frame_even 1 q, ← bcfg_ofList _ hin,
    run_bcfg_of_core (fun j hj => by obtain rfl : j = 0 := by omega
                                     exact hc)]

theorem LW_odd (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) (u : Int) (h0 : 0 ≤ u) (h1 : u < N) :
    LW N (mmax N - 1) u = if u = (N : Int) - 2 then 15 else if u % 2 = 1 ∧ u < (N : Int) - 2 then 7 else 11 := by
  obtain ⟨k, rfl⟩ : ∃ k, N = 2 * k + 1 := ⟨N / 2, by omega⟩
  unfold LW mmax; repeat' split
  all_goals omega

theorem LW_odd_par (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) (u : Int) (h0 : 0 ≤ u) (h1 : u ≤ (N : Int) - 3) :
    LW N (mmax N - 1) u = if u % 2 = 1 then 7 else 11 := by
  rw [LW_odd N h7 ho u h0 (by omega), if_neg (show ¬ u = (N : Int) - 2 by omega)]
  by_cases h : u % 2 = 1
  · rw [if_pos ⟨h, by omega⟩, if_pos h]
  · rw [if_neg (fun h' => h h'.1), if_neg h]

theorem FL_FLo (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) (u : Int) (hu : u ≤ 4) : FL N (mmax N - 1) u = FLo u := by
  unfold FL FLo
  by_cases h0 : u < 0
  · rw [if_pos h0, if_pos h0]
  · rw [if_neg h0, if_neg h0, if_pos (show u < (N : Int) by omega), if_pos hu,
      LW_odd_par N h7 ho u (by omega) (by omega)]

theorem FL_FRo (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) (u : Int) (hu : (N : Int) - 4 ≤ u) :
    FL N (mmax N - 1) u = FRo (u + -((N - 6 : Nat) : Int)) := by
  have hj : ((N - 6 : Nat) : Int) = (N : Int) - 6 := by omega
  rw [hj]
  unfold FL FRo
  rw [if_neg (show ¬ u < 0 by omega), if_neg (show ¬ u + -((N : Int) - 6) < 2 by omega)]
  by_cases h1 : u < (N : Int)
  · rw [if_pos h1, LW_odd N h7 ho u (by omega) h1]
    by_cases e2 : u + -((N : Int) - 6) = 2
    · rw [if_pos e2, if_neg (show ¬ u = (N : Int) - 2 by omega), if_pos ⟨by omega, by omega⟩]
    · rw [if_neg e2]
      by_cases e3 : u + -((N : Int) - 6) = 3
      · rw [if_pos e3, if_neg (show ¬ u = (N : Int) - 2 by omega), if_neg (show ¬ (u % 2 = 1 ∧ u < (N : Int) - 2) by omega)]
      · rw [if_neg e3]
        by_cases e4 : u + -((N : Int) - 6) = 4
        · rw [if_pos e4, if_pos (show u = (N : Int) - 2 by omega)]
        · rw [if_neg e4, if_pos (show u + -((N : Int) - 6) = 5 by omega), if_neg (show ¬ u = (N : Int) - 2 by omega),
            if_neg (show ¬ (u % 2 = 1 ∧ u < (N : Int) - 2) by omega)]
  · rw [if_neg h1, if_neg (show ¬ u + -((N : Int) - 6) = 2 by omega), if_neg (show ¬ u + -((N : Int) - 6) = 3 by omega),
      if_neg (show ¬ u + -((N : Int) - 6) = 4 by omega), if_neg (show ¬ u + -((N : Int) - 6) = 5 by omega),
      show u + -((N : Int) - 6) - 6 = u - N by omega]

theorem FL_WM (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) (u u' : Int) (h3 : 3 < u) (hN : u < (N : Int) - 3)
    (h1 : u - 1 ≤ u') (h2 : u' ≤ u + 1) :
    FL N (mmax N - 1) u' =
      WM (if u % 2 = 1 then 11 else 7) (if u % 2 = 1 then 7 else 11) (u' + -(u - 3)) := by
  unfold FL WM
  rw [if_neg (show ¬ u' < 0 by omega), if_pos (show u' < (N : Int) by omega),
    LW_odd_par N h7 ho u' (by omega) (by omega)]
  by_cases e : u' = u
  · subst e; rw [if_pos (show u' + -(u' - 3) = 3 by omega)]
  · rw [if_neg (show ¬ u' + -(u - 3) = 3 by omega), if_pos (show u' + -(u - 3) = 2 ∨ u' + -(u - 3) = 4 by omega)]
    by_cases hu : u % 2 = 1
    · rw [if_pos hu, if_neg (show ¬ u' % 2 = 1 by omega)]
    · rw [if_neg hu, if_pos (show u' % 2 = 1 by omega)]

set_option maxHeartbeats 4000000 in
/-- **The odd lit clock at generation N − 2 is on the cycle**: it is `clockOf N` at generation 2(N − 6) + 2. -/
theorem lit_odd_entry (N : Nat) (h7 : 7 ≤ N) (ho : N % 2 = 1) :
    run (lcfg (litList N)) (N - 2) = run (clockOf N) (2 * (N - 6) + 2) := by
  have hc := oddCheck_ok
  simp only [oddCheck, Bool.and_eq_true] at hc
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨iL, iW1⟩, iW2⟩, iR⟩, cL⟩, cW1⟩, cW2⟩, cR⟩, eL⟩, eW1⟩, eW2⟩, eR⟩ := hc
  have hj : ((N - 6 : Nat) : Int) = (N : Int) - 6 := by omega
  rw [show N - 2 = 2 * (mmax N - 1) + 1 by unfold mmax; omega, run_add, lit_word N (by omega) _ (by omega),
    clockOf, if_neg (show ¬ N ≤ 5 by omega), clockY_run _ _ (by omega)]
  funext p
  simp only [surg]
  have hc0 : 0 ≤ cidx 3 (N - 6) p ∧ cidx 3 (N - 6) p ≤ ((N - 6 : Nat) : Int) := by simp only [cidx]; omega
  rw [show (5 : Int) + ((2 * (N - 6) + 2 : Nat) : Int) = 2 * ((N - 6 : Nat) : Int) + 7 by push_cast; omega,
    chart_odd _ _ hc0.1 hc0.2]
  have hfl : ∀ q, 0 ≤ unitOf q → unitOf q < N →
      ucfg (FL N (mmax N - 1)) q = lcfg (hexCells (LW N (mmax N - 1) (unitOf q))) (shiftPt (-unitOf q) q) := by
    intro q h1 h2; simp only [ucfg, FL, if_neg (show ¬ unitOf q < 0 by omega), if_pos h2]
  by_cases hA : unitOf p ≤ 3
  · have hi : cidx 3 (N - 6) p = 0 := by simp only [cidx]; omega
    rw [hi, if_neg (show ¬ (0 : Int) = ((N - 6 : Nat) : Int) by omega),
      if_pos (show (((N - 6 : Nat) : Int) - 0) % 2 = 1 by omega), show -(0 : Int) = 0 from rfl, shiftPt_zero,
      run_eq_of_units (c' := ucfg FLo) 1 (fun q h1 h2 => ?_),
      ucfg_run1 FLo FLo_unit (-4) 9 (fun u hu => by simp only [FLo]; rw [if_pos (by omega), capLU_nil' hu])
        (fun u hu => by simp only [FLo]; rw [if_neg (by push_cast at hu; omega), if_neg (by push_cast at hu; omega)])
        iL cL p, show (List.map (fun x => x + frame) (piece FLo (-4) 9)) = pL from rfl,
      eqOn_spec_le (by decide) (by decide) eL (p + frame) (by rw [unitOf_frame]; omega), Xb_frame,
      show ((9 + 7 : Int) % 26).toNat = 16 from rfl]
    · simp only [ucfg]
      rw [FL_FLo N h7 ho _ (by omega)]
  by_cases hC : 3 + ((N - 6 : Nat) : Int) ≤ unitOf p
  · have hi : cidx 3 (N - 6) p = ((N - 6 : Nat) : Int) := by simp only [cidx]; omega
    rw [hi, if_pos rfl,
      run_eq_of_units (c' := shiftC ((N - 6 : Nat) : Int) (ucfg FRo)) 1 (fun q h1 h2 => ?_), run_shiftC]
    · show run (ucfg FRo) 1 (shiftPt (-((N - 6 : Nat) : Int)) p) = _
      rw [ucfg_run1 FRo FRo_unit 2 8 (fun u hu => by simp only [FRo]; rw [if_pos hu])
          (fun u hu => by
            simp only [FRo]
            rw [if_neg (by push_cast at hu; omega), if_neg (by push_cast at hu; omega),
              if_neg (by push_cast at hu; omega), if_neg (by push_cast at hu; omega),
              if_neg (by push_cast at hu; omega), capRU_nil' (by push_cast at hu; omega)])
          iR cR, show (List.map (fun x => x + frame) (piece FRo 2 8)) = pR from rfl,
        eqOn_spec_ge (by decide) (by decide) eR (shiftPt (-((N - 6 : Nat) : Int)) p + frame)
          (by rw [unitOf_frame, unitOf_shiftPt]; omega), Xb_frame, show ((7 + 7 : Int) % 26).toNat = 14 from rfl]
    · simp only [shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
      rw [show -(unitOf q + -((N - 6 : Nat) : Int)) + -((N - 6 : Nat) : Int) = -unitOf q by omega,
        FL_FRo N h7 ho _ (by omega)]
  · have hi : cidx 3 (N - 6) p = unitOf p - 3 := by simp only [cidx]; omega
    rw [hi, if_neg (show ¬ unitOf p - 3 = ((N - 6 : Nat) : Int) by omega)]
    have par : unitOf p % 2 = 1 ∨ unitOf p % 2 = 0 := by omega
    rcases par with hodd | hev
    · rw [if_pos (show (((N - 6 : Nat) : Int) - (unitOf p - 3)) % 2 = 1 by omega),
        run_eq_of_units (c' := shiftC (unitOf p - 3) (ucfg (WM 11 7))) 1 (fun q h1 h2 => ?_), run_shiftC]
      · show run (ucfg (WM 11 7)) 1 (shiftPt (-(unitOf p - 3)) p) = _
        rw [ucfg_run1 (WM 11 7) (WM_unit 11 7) 2 3 (fun u hu => by simp only [WM]; rw [if_neg (by omega), if_neg (by omega)])
            (fun u hu => by simp only [WM]; rw [if_neg (by push_cast at hu; omega), if_neg (by push_cast at hu; omega)])
            iW1 cW1, show (List.map (fun x => x + frame) (piece (WM 11 7) 2 3)) = pW 11 7 from rfl,
          eqOn_spec (by decide) (by decide) (by decide) eW1 (shiftPt (-(unitOf p - 3)) p + frame)
            (by rw [unitOf_frame, unitOf_shiftPt]; omega) (by rw [unitOf_frame, unitOf_shiftPt]; omega), Xb_frame,
          show ((9 + 7 : Int) % 26).toNat = 16 from rfl]
      · simp only [shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
        rw [show -(unitOf q + -(unitOf p - 3)) + -(unitOf p - 3) = -unitOf q by omega,
          FL_WM N h7 ho (unitOf p) _ (by omega) (by omega) (by omega) (by omega), if_pos hodd, if_pos hodd]
    · rw [if_neg (show ¬ (((N - 6 : Nat) : Int) - (unitOf p - 3)) % 2 = 1 by omega),
        run_eq_of_units (c' := shiftC (unitOf p - 3) (ucfg (WM 7 11))) 1 (fun q h1 h2 => ?_), run_shiftC]
      · show run (ucfg (WM 7 11)) 1 (shiftPt (-(unitOf p - 3)) p) = _
        rw [ucfg_run1 (WM 7 11) (WM_unit 7 11) 2 3 (fun u hu => by simp only [WM]; rw [if_neg (by omega), if_neg (by omega)])
            (fun u hu => by simp only [WM]; rw [if_neg (by push_cast at hu; omega), if_neg (by push_cast at hu; omega)])
            iW2 cW2, show (List.map (fun x => x + frame) (piece (WM 7 11) 2 3)) = pW 7 11 from rfl,
          eqOn_spec (by decide) (by decide) (by decide) eW2 (shiftPt (-(unitOf p - 3)) p + frame)
            (by rw [unitOf_frame, unitOf_shiftPt]; omega) (by rw [unitOf_frame, unitOf_shiftPt]; omega), Xb_frame,
          show ((11 + 7 : Int) % 26).toNat = 18 from rfl]
      · simp only [shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
        rw [show -(unitOf q + -(unitOf p - 3)) + -(unitOf p - 3) = -unitOf q by omega,
          FL_WM N h7 ho (unitOf p) _ (by omega) (by omega) (by omega) (by omega), if_neg (show ¬ unitOf p % 2 = 1 by omega),
          if_neg (show ¬ unitOf p % 2 = 1 by omega)]

/-- **The lit clock enters its cycle exactly at generation N − 2, for every N ≥ 6**: its state at N − 2 is a state
of the cycle of `clockOf N`, and no earlier state is. -/
theorem lit_enters_at (N : Nat) (h6 : 6 ≤ N) :
    (∃ s, run (lcfg (litList N)) (N - 2) = run (clockOf N) s) ∧
    ∀ g, g < N - 2 → ∀ k, run (lcfg (litList N)) g ≠ run (clockOf N) k := by
  refine ⟨?_, fun g hg k => lit_first N h6 g hg k⟩
  rcases Nat.mod_two_eq_zero_or_one N with he | ho
  · exact (lit_enters_exact N h6 he).1
  · exact ⟨_, lit_odd_entry N (by omega) ho⟩

/-- **The clock from a single cell, exactly**: for every N ≥ 6, from generation N − 2 on (and from no earlier
generation, `lit_enters_at`) the lit clock is on the cycle of `clockOf N` and has exact period 4N + 2. -/
theorem lit_clock_exact (N : Nat) (h6 : 6 ≤ N) (g : Nat) (hg : N - 2 ≤ g) :
    (∃ s, run (lcfg (litList N)) g = run (clockOf N) s) ∧
    run (run (lcfg (litList N)) g) (4 * N + 2) = run (lcfg (litList N)) g ∧
    ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) g) k ≠ run (lcfg (litList N)) g := by
  obtain ⟨s, hs⟩ := (lit_enters_at N h6).1
  have e : run (lcfg (litList N)) ((N - 2) + (g - (N - 2))) = run (clockOf N) (s + (g - (N - 2))) := by
    rw [run_add, hs, ← run_add]
  rw [show N - 2 + (g - (N - 2)) = g by omega] at e
  obtain ⟨p1, p2, -⟩ := clockOf_period N (by omega)
  rw [e]
  exact ⟨⟨_, rfl⟩, exact_period_run _ _ p1 p2 _⟩

end Gump.Clock
