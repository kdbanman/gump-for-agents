/-
**The free call line, run by the kernel** (push 9's line with the CALL, `Gump.Call.Lf`), on the 128 × 128 × 16 box
of `Gump/CallBox.lean`: `line_rest` (the line is at rest, `lcfg line`, at every even generation from 42 on: the
statement `Gump.Call.LineRest`, part B of `research/audit/signals9/proof9.py`), `Lf_period` (period 2 from 42), and
`Lf_snap` (its state on the closed neighbourhood NZ of the interaction set, at every generation, from the snapshots
of `Gump/CallUnionData.lean`).
-/
import Gump.CallBox
import Gump.CallUnionData
import Gump.Call

namespace Gump.Call
open Gump Gump.Tape

/-- The line's translation into the box. -/
def lineFrame : Pt := ⟨0, 40, 64⟩

theorem lineFrame_even : lineFrame.even := by
  show (0 : Int) % 2 = 0 ∧ (40 : Int) % 2 = 0 ∧ (64 : Int) % 2 = 0
  decide

def lineCallList : List Pt := line ++ callCells

theorem lineCall_eq : lineCall = lcfg lineCallList := by
  funext p; simp only [lineCall, lineCallList, lcfg, List.contains_append]

/-- The line with the CALL, in the box. -/
def LS : Nat := Box.ofList (lineCallList.map (· + lineFrame))

def boxCoreRun (S : Nat) : Nat → Bool
  | 0 => Box.inCore S
  | n + 1 => Box.inCore S && boxCoreRun (Box.bstep S) n

theorem boxCoreRun_spec : ∀ n S, boxCoreRun S n = true → ∀ j, j ≤ n → Box.inCore (Box.brun S j) = true
  | 0, S, h, j, hj => by obtain rfl : j = 0 := by omega
                         exact h
  | n + 1, S, h, j, hj => by
    simp only [boxCoreRun, Bool.and_eq_true] at h
    cases j with
    | zero => exact h.1
    | succ j => rw [← Box.brun_shift]; exact boxCoreRun_spec n _ h.2 j (by omega)

/-- S and T agree on the points of the list M. -/
def boxEqOn (M : List Pt) (S T : Nat) : Bool := S &&& Box.ofList M == T &&& Box.ofList M

theorem boxEqOn_spec {M : List Pt} (hM : M.all Box.inBox = true) {S T : Nat} (h : boxEqOn M S T = true) :
    ∀ p ∈ M, Box.bcfg S p = Box.bcfg T p := by
  intro p hp
  have hb : Box.inBox p = true := by simp only [List.all_eq_true] at hM; exact hM p hp
  have hm : (Box.ofList M).testBit (Box.idx p) = true := by
    rw [Box.ofList, Box.testBit_foldl]
    simp only [Nat.zero_testBit, Bool.false_or, List.any_eq_true, beq_iff_eq]
    exact ⟨p, hp, rfl⟩
  have e := congrArg (fun n => n.testBit (Box.idx p)) (eq_of_beq h)
  simp only [Nat.testBit_and, hm, Bool.and_true] at e
  simp only [Box.bcfg, hb, Bool.true_and, e]

/-- The snapshots, generation by generation. -/
def snapWalk : Nat → Nat → Nat → Bool
  | 0, t, S => boxEqOn (zoneNZ.map (· + lineFrame)) S (Box.ofList ((lineSnap t).map (· + lineFrame)))
  | n + 1, t, S => boxEqOn (zoneNZ.map (· + lineFrame)) S (Box.ofList ((lineSnap t).map (· + lineFrame))) &&
      snapWalk n (t + 1) (Box.bstep S)

theorem snapWalk_spec : ∀ n t S, snapWalk n t S = true → ∀ i, i ≤ n →
    boxEqOn (zoneNZ.map (· + lineFrame)) (Box.brun S i) (Box.ofList ((lineSnap (t + i)).map (· + lineFrame))) = true
  | 0, t, S, h, i, hi => by obtain rfl : i = 0 := by omega
                            exact h
  | n + 1, t, S, h, i, hi => by
    simp only [snapWalk, Bool.and_eq_true] at h
    cases i with
    | zero => exact h.1
    | succ i =>
      rw [← Box.brun_shift, show t + (i + 1) = (t + 1) + i by omega]
      exact snapWalk_spec n (t + 1) _ h.2 i (by omega)

def snapsInBox : Bool := (List.range 44).all fun t => ((lineSnap t).map (· + lineFrame)).all Box.inBox

/-- **The line's run**: in the box, in the core for 45 generations, the line at rest at 42 and 44, and the
snapshots on NZ at 0 .. 43. -/
def lineCheck : Bool :=
  (lineCallList.map (· + lineFrame)).all Box.inBox && (zoneNZ.map (· + lineFrame)).all Box.inBox &&
  (line.map (· + lineFrame)).all Box.inBox && snapsInBox && boxCoreRun LS 45 &&
  (Box.brun LS 42 == Box.ofList (line.map (· + lineFrame))) && (Box.brun LS 44 == Box.brun LS 42) &&
  snapWalk 43 0 LS

theorem lineCheck_ok : lineCheck = true := by decide +kernel

theorem lc : (lineCallList.map (· + lineFrame)).all Box.inBox = true ∧ (zoneNZ.map (· + lineFrame)).all Box.inBox = true ∧
    (line.map (· + lineFrame)).all Box.inBox = true ∧ snapsInBox = true ∧ boxCoreRun LS 45 = true ∧
    Box.brun LS 42 = Box.ofList (line.map (· + lineFrame)) ∧ Box.brun LS 44 = Box.brun LS 42 ∧
    snapWalk 43 0 LS = true := by
  have h := lineCheck_ok
  simp only [lineCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩, h8⟩ := h
  exact ⟨h1, h2, h3, h4, h5, eq_of_beq h6, eq_of_beq h7, h8⟩

/-- The line's run, read in the box. -/
theorem Lf_frame (n : Nat) (hn : n ≤ 46) (q : Pt) : Lf n q = Box.bcfg (Box.brun LS n) (q + lineFrame) := by
  have core := boxCoreRun_spec _ _ lc.2.2.2.2.1
  simp only [Lf, lineCall_eq]
  rw [← run_lcfg_map_add lineCallList lineFrame_even n q, ← Box.bcfg_ofList _ lc.1]
  show run (Box.bcfg LS) n (q + lineFrame) = _
  rw [Box.run_brun _ n (fun j hj => core j (by omega))]

theorem Lf_42 : Lf 42 = lcfg line := by
  funext q
  rw [Lf_frame 42 (by decide), lc.2.2.2.2.2.1, Box.bcfg_ofList _ lc.2.2.1, lcfg_map_add]

theorem Lf_44 : Lf 44 = Lf 42 := by
  funext q
  rw [Lf_frame 44 (by decide), Lf_frame 42 (by decide), lc.2.2.2.2.2.2.1]

/-- **The free line has period 2 from generation 42.** -/
theorem Lf_period (t : Nat) (ht : 42 ≤ t) : Lf (t + 2) = Lf t := by
  obtain ⟨d, rfl⟩ : ∃ d, t = 42 + d := ⟨t - 42, by omega⟩
  induction d with
  | zero => exact Lf_44
  | succ d ih =>
    show step (Lf (42 + d + 2)) = step (Lf (42 + d))
    rw [ih (by omega)]

theorem Lf_late (t : Nat) (ht : 42 ≤ t) : Lf t = Lf (42 + t % 2) := by
  obtain ⟨m, r, hr, rfl⟩ : ∃ m r, r < 2 ∧ t = 42 + r + 2 * m := ⟨(t - 42) / 2, (t - 42) % 2, by omega, by omega⟩
  induction m with
  | zero => congr 1; omega
  | succ m ih =>
    rw [show 42 + r + 2 * (m + 1) = (42 + r + 2 * m) + 2 by omega, Lf_period _ (by omega), ih (by omega)]
    congr 1; omega

/-- **The line at rest from generation 42** (`LineRest`). -/
theorem line_rest : LineRest := by
  intro n hn
  rw [Lf_late _ (by omega), show 42 + 2 * n % 2 = 42 by omega, Lf_42]

/-- The line on NZ at every generation. -/
def lineSnapAt (t : Nat) : List Pt := if t < 44 then lineSnap t else lineSnap (42 + t % 2)

theorem Lf_snap (t : Nat) : ∀ q ∈ zoneNZ, Lf t q = lcfg (lineSnapAt t) q := by
  have key : ∀ t, t < 44 → ∀ q ∈ zoneNZ, Lf t q = lcfg (lineSnap t) q := by
    intro t ht q hq
    have w := snapWalk_spec 43 0 LS lc.2.2.2.2.2.2.2 t (by omega)
    rw [Nat.zero_add] at w
    have hin : ((lineSnap t).map (· + lineFrame)).all Box.inBox = true := by
      have := lc.2.2.2.1
      simp only [snapsInBox, List.all_eq_true, List.mem_range] at this
      exact List.all_eq_true.mpr (this t ht)
    have := boxEqOn_spec lc.2.1 w (q + lineFrame) (List.mem_map.mpr ⟨q, hq, rfl⟩)
    rw [Lf_frame t (by omega), this, Box.bcfg_ofList _ hin, lcfg_map_add]
  intro q hq
  simp only [lineSnapAt]
  split
  · exact key t (by omega) q hq
  · rw [Lf_late t (by omega)]
    exact key _ (by omega) q hq

end Gump.Call
