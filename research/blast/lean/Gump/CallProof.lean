/-
**The call law, part (b), proved** (`Gump.Call.CallLaw`, second conjunct; P1 of `research/audit/REVIEW-signals-9.md`
section 3): for every k ≥ 1, V_k (the store wire alone, e1 = (1,2,0) of the crossing unit made live at generation 29)
is at every even generation t ≥ 2k + 34 plain wire B carrying exactly k pulses two units apart, the leading one at
unit c + 3 − (t − 28)/2. Part (a) (the line never feels the store wire) is not proved: see `notes/tape.md`.

The method is that of `Gump/UnzipProof.lean`. With the crossing moved to unit 0, from generation 32 on V_k is at
generation 28 + 2n the hex word `VW k n` (`tape_call_front.py` checks it against `reference/oracle.py` for k = 1 .. 8):
pulses behind a front `f b 9`, one unit wider than the count read's, which moves one unit per double step through
the standing stretch. The start (generation 29, e1 forced, to 32) is one finite run of its own (`forcedCheck`).
-/
import Gump.UnzipProof
import Gump.Call

namespace Gump.Call
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-! ### The words, the crossing at unit 0 -/

/-- The store wire with the crossing at unit 0: d on units 1 .. k, f on unit k + 1. -/
def sw (k : Nat) (u : Int) : Nat := storeWord k (u - 1)

/-- 2 ≤ n ≤ k: pulses up to unit n − 3 (the lead at 3 − n), then f, b, 9 at n − 2, n − 1, n, then the stretch. -/
def Vg (k n : Nat) (u : Int) : Nat :=
  if u ≤ (n : Int) - 3 then (if 3 - (n : Int) ≤ u ∧ (u - (3 - (n : Int))) % 2 = 0 then 11 else 7)
  else if u = (n : Int) - 2 then 15 else if u = (n : Int) - 1 then 11 else if u = (n : Int) then 9
  else if u ≤ k then 13 else if u = (k : Int) + 1 then 15 else 7

/-- n = k + 1. -/
def Ve1 (k : Nat) (u : Int) : Nat :=
  if u ≤ (k : Int) - 2 then (if 2 - (k : Int) ≤ u ∧ (u - (2 - (k : Int))) % 2 = 0 then 11 else 7)
  else if u = (k : Int) - 1 then 15 else if u = (k : Int) then 11 else 7

/-- n = k + 2. -/
def Ve2 (k : Nat) (u : Int) : Nat :=
  if u ≤ (k : Int) - 1 then (if 1 - (k : Int) ≤ u ∧ (u - (1 - (k : Int))) % 2 = 0 then 11 else 7)
  else if u = (k : Int) then 15 else 7

/-- n ≥ k + 3: the k pulses, the lead at 3 − n. -/
def Vf (k n : Nat) (u : Int) : Nat :=
  if 3 - (n : Int) ≤ u ∧ u < 3 - (n : Int) + 2 * k ∧ (u - (3 - (n : Int))) % 2 = 0 then 11 else 7

/-- **V_k at generation 28 + 2n** (n ≥ 2), the crossing at unit 0. -/
def VW (k n : Nat) (u : Int) : Nat :=
  if n ≤ k then Vg k n u else if n = k + 1 then Ve1 k u else if n = k + 2 then Ve2 k u else Vf k n u

theorem VW_g {k n : Nat} (h : n ≤ k) : VW k n = Vg k n := by funext u; simp [VW, h]
theorem VW_e1 (k : Nat) : VW k (k + 1) = Ve1 k := by
  funext u; simp only [VW]; rw [if_neg (by omega)]; simp
theorem VW_e2 (k : Nat) : VW k (k + 2) = Ve2 k := by
  funext u; simp only [VW]; rw [if_neg (by omega), if_neg (by omega)]; simp
theorem VW_f {k n : Nat} (h : k + 3 ≤ n) : VW k n = Vf k n := by
  funext u; simp only [VW]; rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]

/-! ### The zones -/

def gN (a j : Nat) (v : Int) : Nat :=
  if v ≤ -3 then (if 3 - 2 * (a : Int) ≤ v ∧ (v - 1) % 2 = 0 then 11 else 7)
  else if v = -2 then 15 else if v = -1 then 11 else if v = 0 then 9 else if v ≤ j then 13
  else if v = (j : Int) + 1 then 15 else 7
def gT (a j : Nat) (v : Int) : Nat :=
  if v ≤ -2 then (if 2 - 2 * (a : Int) ≤ v ∧ v % 2 = 0 then 11 else 7)
  else if v = -1 then 15 else if v = 0 then 11 else if v = 1 then 9 else if v ≤ j then 13
  else if v = (j : Int) + 1 then 15 else 7
def f1N (a : Nat) (v : Int) : Nat :=
  if v ≤ -3 then (if 3 - 2 * (a : Int) ≤ v ∧ (v - 1) % 2 = 0 then 11 else 7)
  else if v = -2 then 15 else if v = -1 then 11 else if v = 0 then 9 else if v = 1 then 15 else 7
def f1T (a : Nat) (v : Int) : Nat :=
  if v ≤ -2 then (if 2 - 2 * (a : Int) ≤ v ∧ v % 2 = 0 then 11 else 7) else if v = -1 then 15
  else if v = 0 then 11 else 7
def f2T (a : Nat) (v : Int) : Nat :=
  if v ≤ -1 then (if 1 - 2 * (a : Int) ≤ v ∧ (v - 1) % 2 = 0 then 11 else 7) else if v = 0 then 15 else 7
def f3T (a : Nat) (v : Int) : Nat := if -2 * (a : Int) ≤ v ∧ v < 0 ∧ v % 2 = 0 then 11 else 7

def zoneVG (a j : Nat) : Bool :=
  pieceCheck (fun v => hexCells (gN a j v)) (fun v => hexCells (gT a j v)) (-6) 11 [] [] 2 (-4) 2 zoneFrame
def zoneV1 (a : Nat) : Bool :=
  pieceCheck (fun v => hexCells (f1N a v)) (fun v => hexCells (f1T a v)) (-6) 11 [] [] 2 (-4) 2 zoneFrame
def zoneV2 (a : Nat) : Bool :=
  pieceCheck (fun v => hexCells (f1T a v)) (fun v => hexCells (f2T a v)) (-5) 10 [] [] 2 (-3) 2 zoneFrame
def zoneV3 (a : Nat) : Bool :=
  pieceCheck (fun v => hexCells (f2T a v)) (fun v => hexCells (f3T a v)) (-5) 10 [] [] 2 (-3) 2 zoneFrame

/-! ### The start: one generation of the store, e1 forced, three more -/

/-- The start's target on units −3 .. 3 (j = min(k, 7)). -/
def sT (j : Nat) (v : Int) : Nat :=
  if v ≤ -1 then 7 else if v = 0 then 15 else if v = 1 then 11 else if v = 2 then (if 2 ≤ j then 9 else 7)
  else if v ≤ j then 13 else if v = (j : Int) + 1 then 15 else 7

/-- The piece of f on units a .. a + n − 1, stepped once, with the cell e made live, stepped three times more,
agrees on units lo .. hi with the piece of g; in the box after the translation V. -/
def forcedCheck (f g : Int → List Pt) (a : Int) (n : Nat) (e : Pt) (lo hi : Int) (V : Pt) : Bool :=
  ((piece f a n).map (· + V)).all inBox && inBox (e + V) && ((piece g a n).map (· + V)).all inBox &&
    inCore (ofList ((piece f a n).map (· + V))) &&
    coreRun (bstep (ofList ((piece f a n).map (· + V))) ||| ofList [e + V]) 3 &&
    eqOn (unitMask (lo + V.x / 2) (hi + V.x / 2))
      (brun (bstep (ofList ((piece f a n).map (· + V))) ||| ofList [e + V]) 3) (ofList ((piece g a n).map (· + V)))

/-- The translation into the box for the start (units move by 6). -/
def startFrame : Pt := ⟨12, 8, 16⟩

theorem startFrame_even : startFrame.even := by
  show (12 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

def zoneS (j : Nat) : Bool :=
  forcedCheck (fun v => hexCells (sw j v)) (fun v => hexCells (sT j v)) (-7) 15 ⟨1, 2, 0⟩ (-3) 3 startFrame

def zonesV : Bool :=
  (List.range 4).all (fun a => (List.range 5).all (fun j => zoneVG (a + 2) (j + 1))) &&
  (List.range 4).all (fun a => zoneV1 (a + 2)) &&
  (List.range 5).all (fun a => zoneV2 (a + 1) && zoneV3 (a + 1)) &&
  (List.range 7).all (fun j => zoneS (j + 1))

theorem zonesV_ok : zonesV = true := by decide +kernel

theorem bcfg_or (S T : Nat) (p : Pt) : bcfg (S ||| T) p = (bcfg S p || bcfg T p) := by
  simp only [bcfg, Nat.testBit_or]; cases inBox p <;> simp

theorem lcfg_single (e q : Pt) : lcfg [e] q = (q == e) := by
  apply Bool.eq_iff_iff.mpr; rw [lcfg_iff]; simp

theorem forcedCheck_spec {f g : Int → List Pt} (hf : ∀ u, ∀ q ∈ f u, unitOf q = 0)
    (hg : ∀ u, ∀ q ∈ g u, unitOf q = 0) {a : Int} {n : Nat} {e : Pt} {lo hi : Int} {V : Pt} (hV : V.even)
    (h : forcedCheck f g a n e lo hi V = true) (hb1 : -8 ≤ lo + V.x / 2) (hb2 : hi + V.x / 2 ≤ 23)
    (hlh : lo ≤ hi + 1) (hlo : a ≤ lo - 4) (hhi : hi + 4 < a + n) (c : Config)
    (hc : ∀ q, lo - 4 ≤ unitOf q → unitOf q ≤ hi + 4 → c q = ucfg f q) :
    ∀ p, lo ≤ unitOf p → unitOf p ≤ hi → run (fun q => step c q || q == e) 3 p = ucfg g p := by
  simp only [forcedCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩ := h
  intro p hp1 hp2
  have core := coreRun_spec _ _ h5
  have hu := unitOf_add_even p V hV
  -- the forced configuration of c and of the piece agree near p
  have e1 : run (fun q => step c q || q == e) 3 p =
      run (fun q => step (lcfg (piece f a n)) q || q == e) 3 p := by
    apply run_eq_of_units 3
    intro q q1 q2
    rw [step_eq_of_units (c' := lcfg (piece f a n)) (fun r r1 r2 => by
      rw [hc r (by omega) (by omega), lcfg_piece f hf]
      have : a ≤ unitOf r ∧ unitOf r < a + (n : Int) := by omega
      rw [decide_eq_true this, Bool.true_and])]
  -- the forced piece, read in the box
  have e2 : (fun q => step (lcfg (piece f a n)) q || q == e) =
      fun q => bcfg (bstep (ofList ((piece f a n).map (· + V))) ||| ofList [e + V]) (q + V) := by
    funext q
    rw [bcfg_or, bstep_spec _ ((inCore_iff _).mp h4), bcfg_ofList _ h1]
    have : step (lcfg ((piece f a n).map (· + V))) (q + V) = step (lcfg (piece f a n)) q :=
      run_lcfg_map_add (piece f a n) hV 1 q
    rw [this, bcfg_ofList [e + V] (by simp [h2]), show [e + V] = [e].map (· + V) from rfl, lcfg_map_add,
      lcfg_single]
  rw [e1, e2, run_translate _ hV]
  dsimp only
  rw [run_bcfg_of_core (fun j hj => core j (by omega)),
    eqOn_spec hb1 hb2 (by omega) h6 (p + V) (by omega) (by omega), bcfg_ofList _ h3, lcfg_map_add, lcfg_piece g hg]
  have : a ≤ unitOf p ∧ unitOf p < a + (n : Int) := by omega
  rw [decide_eq_true this, Bool.true_and]

/-! ### The steps, the crossing at unit 0 -/

theorem zonesV_facts :
    (∀ a j, 2 ≤ a → a ≤ 5 → 1 ≤ j → j ≤ 5 → zoneVG a j = true) ∧ (∀ a, 2 ≤ a → a ≤ 5 → zoneV1 a = true) ∧
    (∀ a, 1 ≤ a → a ≤ 5 → zoneV2 a = true ∧ zoneV3 a = true) ∧ (∀ j, 1 ≤ j → j ≤ 7 → zoneS j = true) := by
  have hz := zonesV_ok
  simp only [zonesV, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hz
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hz
  refine ⟨fun a j ha hb hj hj' => ?_, fun a ha hb => ?_, fun a ha hb => ?_, fun j hj hj' => ?_⟩
  · have := h1 (a - 2) (by omega) (j - 1) (by omega); rwa [show a - 2 + 2 = a by omega, show j - 1 + 1 = j by omega] at this
  · have := h2 (a - 2) (by omega); rwa [show a - 2 + 2 = a by omega] at this
  · have := h3 (a - 1) (by omega); rwa [show a - 1 + 1 = a by omega] at this
  · have := h4 (j - 1) (by omega); rwa [show j - 1 + 1 = j by omega] at this

theorem sw_window (k : Nat) (hk : 1 ≤ k) (u : Int) : hexWindowCheck 0 (win (sw k) u) = true := by
  have e : win (sw k) u = win (storeWord k) (u - 1) := win_congr _ _ _ _ (fun i _ _ => by simp only [sw]; congr 1; omega)
  rw [e]; exact store_window k hk _

/-- A step where the word stands. -/
theorem step_stand (w w' : Int → Nat) (c : Config) (p : Pt) (hc : hexWindowCheck 0 (win w (unitOf p)) = true)
    (hw' : w' (unitOf p) = w (unitOf p))
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = hcfg w q) : run c 2 p = hcfg w' p := by
  rw [hex_local w 0 ⟨by decide, by decide⟩ c p hc h]
  simp only [hcfg, ucfg, Int.add_zero, hw']

theorem step_sw (k : Nat) (hk : 1 ≤ k) (w w' : Int → Nat) (c : Config) (p : Pt)
    (hw : ∀ i : Int, -2 ≤ i → i ≤ 2 → w (unitOf p + i) = sw k (unitOf p + i))
    (hw' : w' (unitOf p) = sw k (unitOf p))
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = hcfg w q) : run c 2 p = hcfg w' p := by
  have e : win w (unitOf p) = win (sw k) (unitOf p) := win_congr _ _ _ _ hw
  have hc := sw_window k hk (unitOf p)
  rw [← e] at hc
  apply step_stand w w' c p hc _ h
  have := hw 0 (by decide) (by decide)
  simp only [Int.add_zero] at this
  rw [hw', this]

set_option maxHeartbeats 4000000 in
theorem vstep_generic (k n : Nat) (hk : 1 ≤ k) (h2 : 2 ≤ n) (hnk : n + 1 ≤ k) :
    run (hcfg (VW k n)) 2 = hcfg (VW k (n + 1)) := by
  rw [VW_g (by omega), VW_g (n := n + 1) (by omega)]
  have zg := zonesV_facts.1 (min n 5) (min (k - n) 5) (by omega) (by omega) (by omega) (by omega)
  unfold zoneVG at zg
  funext p
  by_cases hL : unitOf p ≤ (n : Int) - 5
  · apply step_left (Vg k n) (Vg k (n + 1)) _ p
    · intro i h1 h2; simp only [Vg]; repeat' split
      all_goals omega
    · simp only [Vg]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (n : Int) + 3 ≤ unitOf p
    · apply step_sw k hk (Vg k n) (Vg k (n + 1)) _ p
      · intro i h1 h2; simp only [Vg, sw, storeWord]; repeat' split
        all_goals omega
      · simp only [Vg, sw, storeWord]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Vg k n) (Vg k (n + 1)) [] n (-4) 2 (-6) (gN (min n 5) (min (k - n) 5))
        (gT (min n 5) (min (k - n) 5)) 11 (by decide) (by decide) zg (by decide)
      · intro v h1 h2; simp only [Vg, gN]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Vg, gT]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

set_option maxHeartbeats 4000000 in
theorem vstep_e1 (k : Nat) (hk : 2 ≤ k) : run (hcfg (VW k k)) 2 = hcfg (VW k (k + 1)) := by
  rw [VW_g (Nat.le_refl _), VW_e1]
  have ze := zonesV_facts.2.1 (min k 5) (by omega) (by omega)
  unfold zoneV1 at ze
  funext p
  by_cases hL : unitOf p ≤ (k : Int) - 5
  · apply step_left (Vg k k) (Ve1 k) _ p
    · intro i h1 h2; simp only [Vg]; repeat' split
      all_goals omega
    · simp only [Vg, Ve1]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (k : Int) + 3 ≤ unitOf p
    · apply step_sw k (by omega) (Vg k k) (Ve1 k) _ p
      · intro i h1 h2; simp only [Vg, sw, storeWord]; repeat' split
        all_goals omega
      · simp only [Ve1, sw, storeWord]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Vg k k) (Ve1 k) [] k (-4) 2 (-6) (f1N (min k 5)) (f1T (min k 5)) 11 (by decide)
        (by decide) ze (by decide)
      · intro v h1 h2; simp only [Vg, f1N]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Ve1, f1T]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

set_option maxHeartbeats 4000000 in
theorem vstep_e2 (k : Nat) (hk : 1 ≤ k) : run (hcfg (VW k (k + 1))) 2 = hcfg (VW k (k + 2)) := by
  rw [VW_e1, VW_e2]
  have ze := (zonesV_facts.2.2.1 (min k 5) (by omega) (by omega)).1
  unfold zoneV2 at ze
  funext p
  by_cases hL : unitOf p ≤ (k : Int) - 4
  · apply step_left (Ve1 k) (Ve2 k) _ p
    · intro i h1 h2; simp only [Ve1]; repeat' split
      all_goals omega
    · simp only [Ve1, Ve2]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (k : Int) + 3 ≤ unitOf p
    · apply step_left (Ve1 k) (Ve2 k) _ p
      · intro i h1 h2; simp only [Ve1]; repeat' split
        all_goals omega
      · simp only [Ve1, Ve2]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Ve1 k) (Ve2 k) [] k (-3) 2 (-5) (f1T (min k 5)) (f2T (min k 5)) 10 (by decide)
        (by decide) ze (by decide)
      · intro v h1 h2; simp only [Ve1, f1T]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Ve2, f2T]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

set_option maxHeartbeats 4000000 in
theorem vstep_e3 (k : Nat) (hk : 1 ≤ k) : run (hcfg (VW k (k + 2))) 2 = hcfg (VW k (k + 3)) := by
  rw [VW_e2, VW_f (Nat.le_refl _)]
  have ze := (zonesV_facts.2.2.1 (min k 5) (by omega) (by omega)).2
  unfold zoneV3 at ze
  funext p
  by_cases hL : unitOf p ≤ (k : Int) - 4
  · apply step_left (Ve2 k) (Vf k (k + 3)) _ p
    · intro i h1 h2; simp only [Ve2]; repeat' split
      all_goals omega
    · simp only [Ve2, Vf]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (k : Int) + 3 ≤ unitOf p
    · apply step_left (Ve2 k) (Vf k (k + 3)) _ p
      · intro i h1 h2; simp only [Ve2]; repeat' split
        all_goals omega
      · simp only [Ve2, Vf]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Ve2 k) (Vf k (k + 3)) [] k (-3) 2 (-5) (f2T (min k 5)) (f3T (min k 5)) 10 (by decide)
        (by decide) ze (by decide)
      · intro v h1 h2; simp only [Ve2, f2T]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Vf, f3T]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

/-! ### V_k with the crossing at unit 0 -/

def S0 (k : Nat) : Config := hcfg (sw k)
def e0 : Pt := ⟨1, 2, 0⟩

/-- V_k with the crossing at unit 0. -/
def V0 (k t : Nat) : Config :=
  if t < 29 then run (S0 k) t else run (fun p => run (S0 k) 29 p || p == e0) (t - 29)

theorem hcfg_shift (w : Int → Nat) (m : Int) : shiftC m (hcfg w) = hcfg (fun u => w (u - m)) := by
  funext p
  show lcfg _ _ = lcfg _ _
  simp only [unitOf_shiftPt, shiftPt_shiftPt]
  rw [show unitOf p + -m = unitOf p - m by omega, show -(unitOf p - m) + -m = -unitOf p by omega]

theorem S0_eq (k : Nat) : S0 k = shiftC 1 (store k) := by
  rw [store, hcfg_shift]; rfl

theorem S0_stands (k : Nat) (hk : 1 ≤ k) (n : Nat) : run (S0 k) (2 * n) = S0 k := by
  rw [S0_eq, run_shiftC, stretch_stands k hk n]

theorem V0_forced (k : Nat) (hk : 1 ≤ k) (m : Nat) :
    V0 k (29 + m) = run (fun p => step (S0 k) p || p == e0) m := by
  simp only [V0, show ¬ (29 + m < 29) by omega, if_false, show 29 + m - 29 = m by omega]
  rw [show (29 : Nat) = 1 + 2 * 14 from rfl, run_add]
  have : run (run (S0 k) 1) (2 * 14) = run (S0 k) 1 := by
    rw [← run_add, show 1 + 2 * 14 = 2 * 14 + 1 by omega, run_add, S0_stands k hk]
  rw [this]; rfl

set_option maxHeartbeats 4000000 in
theorem V0_start (k : Nat) (hk : 1 ≤ k) : V0 k (28 + 2 * 2) = hcfg (VW k 2) := by
  rw [show 28 + 2 * 2 = 29 + 3 by omega, V0_forced k hk]
  have zs := zonesV_facts.2.2.2 (min k 7) (by omega) (by omega)
  unfold zoneS at zs
  have agr : ∀ q, -3 - 4 ≤ unitOf q → unitOf q ≤ 3 + 4 →
      S0 k q = ucfg (fun v => hexCells (sw (min k 7) v)) q := by
    intro q h1 h2
    have e : sw k (unitOf q) = sw (min k 7) (unitOf q) := by
      simp only [sw, storeWord]; repeat' split
      all_goals omega
    simp only [S0, hcfg, ucfg, e]
  rw [show e0 = ⟨1, 2, 0⟩ from rfl]
  funext p
  by_cases hz : -3 ≤ unitOf p ∧ unitOf p ≤ 3
  · rw [forcedCheck_spec (fun v => hexCells_unit _) (fun v => hexCells_unit _) startFrame_even zs
      (by decide) (by decide) (by decide) (by decide) (by decide) (S0 k) agr p hz.1 hz.2]
    simp only [ucfg, hcfg]
    congr 2
    by_cases hk2 : 2 ≤ k
    · rw [VW_g hk2]; simp only [sT, Vg]; repeat' split
      all_goals omega
    · obtain rfl : k = 1 := by omega
      rw [show (2 : Nat) = 1 + 1 from rfl, VW_e1]; simp only [sT, Ve1]; repeat' split
      all_goals omega
  · have far : run (fun p => step (S0 k) p || p == ⟨1, 2, 0⟩) 3 p = run (step (S0 k)) 3 p := by
      apply run_eq_of_units 3
      intro q h1 h2
      have : q ≠ ⟨1, 2, 0⟩ := by
        intro e; rw [e] at h1 h2; have : unitOf ⟨1, 2, 0⟩ = 0 := by decide
        omega
      simp [this]
    rw [far, show run (step (S0 k)) 3 = run (S0 k) (1 + 3) from (run_add _ 1 3).symm,
      show 1 + 3 = 2 * 2 by omega, S0_stands k hk]
    simp only [S0, hcfg, ucfg]
    congr 2
    by_cases hk2 : 2 ≤ k
    · rw [VW_g hk2]; simp only [sw, storeWord, Vg]; repeat' split
      all_goals omega
    · obtain rfl : k = 1 := by omega
      rw [show (2 : Nat) = 1 + 1 from rfl, VW_e1]; simp only [sw, storeWord, Ve1]; repeat' split
      all_goals omega

theorem V0_W (k : Nat) (hk : 1 ≤ k) : ∀ n, 2 ≤ n → n ≤ k + 3 → V0 k (28 + 2 * n) = hcfg (VW k n) := by
  intro n h1 h2
  induction n with
  | zero => omega
  | succ n ih =>
    by_cases h0 : n = 1
    · subst h0; exact V0_start k hk
    · have e : V0 k (28 + 2 * (n + 1)) = run (V0 k (28 + 2 * n)) 2 := by
        rw [show 28 + 2 * (n + 1) = 29 + ((2 * n - 1) + 2) by omega, V0_forced k hk, run_add,
          show 28 + 2 * n = 29 + (2 * n - 1) by omega, V0_forced k hk]
      rw [e, ih (by omega) (by omega)]
      by_cases e1 : n + 1 ≤ k
      · exact vstep_generic k n hk (by omega) e1
      · by_cases e2 : n = k
        · subst e2; exact vstep_e1 n (by omega)
        · by_cases e3 : n = k + 1
          · subst e3; exact vstep_e2 k hk
          · obtain rfl : n = k + 2 := by omega
            exact vstep_e3 k hk

theorem V0_final (k : Nat) (hk : 1 ≤ k) (n : Nat) (hn : k + 3 ≤ n) :
    V0 k (28 + 2 * n) = tape (pulses k (3 - n)) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = k + 3 + m := ⟨n - (k + 3), by omega⟩
  have e : V0 k (28 + 2 * (k + 3 + m)) = run (V0 k (28 + 2 * (k + 3))) (2 * m) := by
    rw [show 28 + 2 * (k + 3 + m) = 29 + ((2 * (k + 3) - 1) + 2 * m) by omega, V0_forced k hk, run_add,
      show 28 + 2 * (k + 3) = 29 + (2 * (k + 3) - 1) by omega, V0_forced k hk]
  rw [e, V0_W k hk _ (by omega) (Nat.le_refl _), VW_f (Nat.le_refl _)]
  have ht : hcfg (Vf k (k + 3)) = tape (pulses k (3 - ((k + 3 : Nat) : Int))) := by
    rw [tape_eq_hcfg]; congr 1; funext u; simp only [Vf, pulses, hexOf]; split <;> simp_all
  rw [ht, tape_run]
  congr 1; funext u; simp only [pulses]
  have e1 : (3 - ((k + 3 : Nat) : Int) ≤ u + (m : Int)) ↔ (3 - ((k + 3 + m : Nat) : Int) ≤ u) := by omega
  have e2 : (u + (m : Int) < 3 - ((k + 3 : Nat) : Int) + 2 * k) ↔ (u < 3 - ((k + 3 + m : Nat) : Int) + 2 * k) := by
    omega
  have e3 : ((u + (m : Int) - (3 - ((k + 3 : Nat) : Int))) % 2 = 0) ↔
      ((u - (3 - ((k + 3 + m : Nat) : Int))) % 2 = 0) := by omega
  simp only [e1, e2, e3]

/-! ### Back to the crossing at unit 35: the call law, part (b) -/

theorem storeAt_eq (k : Nat) : storeAt k = shiftC cross (S0 k) := by
  rw [S0, hcfg_shift, storeAt]
  congr 1; funext u; simp only [sw]; congr 1; omega

theorem beq_shift (m : Int) (p e : Pt) : (shiftPt (-m) p == e) = (p == shiftPt m e) := by
  apply Bool.eq_iff_iff.mpr
  simp only [beq_iff_eq]
  constructor
  · intro h; rw [← h, shiftPt_shiftPt_neg]
  · intro h; rw [h, shiftPt_neg_shiftPt]

theorem V_eq (k t : Nat) : V k t = shiftC cross (V0 k t) := by
  simp only [V, V0]
  split
  · rw [storeAt_eq, run_shiftC]
  · have : (fun p => run (storeAt k) 29 p || p == e1) = shiftC cross (fun p => run (S0 k) 29 p || p == e0) := by
      funext p
      rw [storeAt_eq, run_shiftC]
      simp only [shiftC, e1, e0, beq_shift]
    rw [this, run_shiftC]

/-- **The call law, part (b)** (REVIEW-signals-9 §3 (b), P1 of its proof): for every k ≥ 1 and every even
generation t = 2n ≥ 2k + 34, V_k(t) is plain wire B carrying exactly k pulses two units apart, the leading one at
unit c + 3 − (t − 28)/2. -/
theorem call_law_b (k : Nat) (hk : 1 ≤ k) (n : Nat) (hn : k + 17 ≤ n) :
    V k (2 * n) = tape (pulses k (cross + 3 - ((n : Int) - 14))) := by
  rw [V_eq, show 2 * n = 28 + 2 * (n - 14) by omega, V0_final k hk _ (by omega), tape_eq_hcfg, hcfg_shift,
    tape_eq_hcfg]
  congr 1; funext u; simp only [pulses]
  have e1 : (3 - ((n - 14 : Nat) : Int) ≤ u - cross) ↔ (cross + 3 - ((n : Int) - 14) ≤ u) := by omega
  have e2 : (u - cross < 3 - ((n - 14 : Nat) : Int) + 2 * k) ↔ (u < cross + 3 - ((n : Int) - 14) + 2 * k) := by
    omega
  have e3 : ((u - cross - (3 - ((n - 14 : Nat) : Int))) % 2 = 0) ↔ ((u - (cross + 3 - ((n : Int) - 14))) % 2 = 0) := by
    omega
  simp only [e1, e2, e3]

end Gump.Call
