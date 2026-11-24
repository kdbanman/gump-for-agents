/-
**The unzip law, proved** (statement: `Gump.Unzip.UnzipLawSharp`, `UnzipLaw`). The proof is not the source's seam
argument (`prove_unzip8.py`); it is an induction on time, which the kymograph suggests: from generation 2 on the
store wire is, at every even generation 2n, the hex word `W k n` (`tape_unzip.py` checks the formula against
`reference/oracle.py` for k = 1 .. 10): plain wire B and k pulses `b7b7…` behind a front `f 9` that moves one unit
towards +v every two generations through the stretch `d…d f`, which stands. One double step of `W k n` is
`W k (n + 1)`:
  on the units left of the front the word is a tape word over {7, b}, which moves one unit (the 32 tape windows);
  on the units right of it the word is the stretch, which stands (the stretch windows of `Gump.Unzip`);
  on six units at the front one finite piece, moved to the front, is stepped twice by the kernel; its content
  depends on n and k only through min(n, 5) and min(k − n, 3).
The first double step (from the count read, a cell removed) and the two last ones (the front meets the edge) have
pieces of their own. From n = k + 3 on the word is the tape of the k pulses and `tape_run` carries it for ever.
-/
import Gump.Unzip

namespace Gump.Unzip
open Gump Gump.Tape Gump.Bits

/-! ### The word at generation 2n -/

/-- The word at n = 1. -/
def W1 (k : Nat) (u : Int) : Nat := if u = -1 then 5 else if 0 ≤ u ∧ u < k then 13 else if u = k then 15 else 7

/-- The word for 2 ≤ n ≤ k + 1: pulses behind the front f 9, then the stretch. -/
def Wg (k n : Nat) (u : Int) : Nat :=
  if u ≤ (n : Int) - 4 then (if 2 - (n : Int) ≤ u ∧ (u - (2 - (n : Int))) % 2 = 0 then 11 else 7)
  else if u = (n : Int) - 3 then 15 else if u = (n : Int) - 2 then 9 else if u < k then 13
  else if u = k then 15 else 7

/-- The word at n = k + 2. -/
def We (k : Nat) (u : Int) : Nat :=
  if u ≤ (k : Int) - 2 then (if -(k : Int) ≤ u ∧ (u + k) % 2 = 0 then 11 else 7) else if u = (k : Int) - 1 then 15 else 7

/-- The word for n ≥ k + 3: the k pulses. -/
def Wf (k n : Nat) (u : Int) : Nat :=
  if 2 - (n : Int) ≤ u ∧ u < 2 - (n : Int) + 2 * k ∧ (u - (2 - (n : Int))) % 2 = 0 then 11 else 7

/-- **The store wire at generation 2n after the count read** (n ≥ 1). -/
def W (k n : Nat) (u : Int) : Nat :=
  if n = 1 then W1 k u else if n ≤ k + 1 then Wg k n u else if n = k + 2 then We k u else Wf k n u

theorem W_one (k : Nat) : W k 1 = W1 k := by funext u; simp [W]
theorem W_gen {k n : Nat} (h1 : 2 ≤ n) (h2 : n ≤ k + 1) : W k n = Wg k n := by
  funext u; simp only [W]; rw [if_neg (by omega), if_pos h2]
theorem W_edge (k : Nat) : W k (k + 2) = We k := by
  funext u; simp only [W]; rw [if_neg (by omega), if_neg (by omega)]; simp
theorem W_fin {k n : Nat} (h : k + 3 ≤ n) : W k n = Wf k n := by
  funext u; simp only [W]; rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]

/-! ### Three kinds of local step -/

def b2h (b : Bool) : Nat := if b then 11 else 7

/-- The 32 windows of the tape over {7, b}, moved one unit. -/
theorem tape_hex_window (a0 a1 a2 a3 a4 : Bool) : hexWindowCheck 1 [b2h a0, b2h a1, b2h a2, b2h a3, b2h a4] = true := by
  cases a0 <;> cases a1 <;> cases a2 <;> cases a3 <;> cases a4 <;> decide +kernel

theorem b2h_of {x : Nat} (h : x = 7 ∨ x = 11) : ∃ b, x = b2h b := by
  rcases h with rfl | rfl
  · exact ⟨false, rfl⟩
  · exact ⟨true, rfl⟩

/-- A step on the tape side. -/
theorem step_left (w w' : Int → Nat) (c : Config) (p : Pt)
    (hw : ∀ i : Int, -2 ≤ i → i ≤ 2 → w (unitOf p + i) = 7 ∨ w (unitOf p + i) = 11)
    (hw' : w' (unitOf p) = w (unitOf p + 1))
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = hcfg w q) :
    run c 2 p = hcfg w' p := by
  have hc : hexWindowCheck 1 (win w (unitOf p)) = true := by
    obtain ⟨b0, e0⟩ := b2h_of (hw (-2) (by decide) (by decide))
    obtain ⟨b1, e1⟩ := b2h_of (hw (-1) (by decide) (by decide))
    obtain ⟨b2, e2⟩ := b2h_of (hw 0 (by decide) (by decide))
    obtain ⟨b3, e3⟩ := b2h_of (hw 1 (by decide) (by decide))
    obtain ⟨b4, e4⟩ := b2h_of (hw 2 (by decide) (by decide))
    rw [show unitOf p + -2 = unitOf p - 2 by omega] at e0
    rw [show unitOf p + -1 = unitOf p - 1 by omega] at e1
    rw [Int.add_zero] at e2
    simp only [win, e0, e1, e2, e3, e4]
    exact tape_hex_window _ _ _ _ _
  rw [hex_local w 1 ⟨by decide, by decide⟩ c p hc h]
  simp only [hcfg, ucfg, hw']

/-- A step on the stretch side. -/
theorem step_right (k : Nat) (hk : 1 ≤ k) (w w' : Int → Nat) (c : Config) (p : Pt)
    (hw : ∀ i : Int, -2 ≤ i → i ≤ 2 → w (unitOf p + i) = storeWord k (unitOf p + i))
    (hw' : w' (unitOf p) = storeWord k (unitOf p))
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = hcfg w q) :
    run c 2 p = hcfg w' p := by
  have e : win w (unitOf p) = win (storeWord k) (unitOf p) := win_congr _ _ _ _ hw
  have hc := store_window k hk (unitOf p)
  rw [← e] at hc
  rw [hex_local w 0 ⟨by decide, by decide⟩ c p hc h]
  simp only [hcfg, ucfg, Int.add_zero, hw']
  have := hw 0 (by decide) (by decide)
  simp only [Int.add_zero] at this
  rw [this]

/-- The translation into the box for the zone checks. -/
def zoneFrame : Pt := ⟨8, 8, 0⟩

theorem zoneFrame_even : zoneFrame.even := by
  show (8 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (0 : Int) % 2 = 0
  decide

/-- A step in a zone of units lo .. hi around unit n, checked on a finite piece moved to unit 0 (σ: cells flipped). -/
theorem step_zone (w w' : Int → Nat) (σ : List Pt) (n lo hi a : Int) (f g : Int → Nat) (len : Nat)
    (ha : a = lo - 2) (hlen : (len : Int) = hi - lo + 5)
    (h : pieceCheck (fun v => hexCells (f v)) (fun v => hexCells (g v)) a len σ [] 2 lo hi zoneFrame = true)
    (hb : -12 ≤ lo ∧ hi ≤ 19 ∧ lo ≤ hi) (c : Config)
    (hw : ∀ v, lo - 2 ≤ v → v ≤ hi + 2 → w (v + n) = f v)
    (hw' : ∀ v, lo ≤ v → v ≤ hi → w' (v + n) = g v)
    (hc : ∀ q, lo + n - 2 ≤ unitOf q → unitOf q ≤ hi + n + 2 →
      c q = xor (hcfg w q) (lcfg (σ.map (shiftPt n)) q))
    (p : Pt) (hp1 : lo + n ≤ unitOf p) (hp2 : unitOf p ≤ hi + n) : run c 2 p = hcfg w' p := by
  subst ha
  have agree : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 →
      c q = shiftC n (xorC (ucfg (fun v => hexCells (f v))) (lcfg σ)) q := by
    intro q h1 h2
    rw [hc q (by omega) (by omega)]
    simp only [shiftC, xorC, hcfg, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
    rw [lcfg_map_shiftPt]
    simp only [shiftC]
    rw [← hw (unitOf q + -n) (by omega) (by omega), show unitOf q + -n + n = unitOf q by omega,
      show -(unitOf q + -n) + -n = -unitOf q by omega]
  rw [run_eq_of_units 2 (fun q h1 h2 => agree q (by omega) (by omega)), run_shiftC]
  simp only [shiftC]
  have spec := pieceCheck_spec (fun v => hexCells_unit _) (fun v => hexCells_unit _) zoneFrame_even h
    (by simp only [zoneFrame]; omega) (by simp only [zoneFrame]; omega) (by omega) (by omega) (by omega)
    (xorC (ucfg (fun v => hexCells (f v))) (lcfg σ)) (fun q _ _ => rfl) (shiftPt (-n) p)
    (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
  rw [spec]
  simp only [xorC, lcfg_nil', Bool.xor_false, ucfg, hcfg, unitOf_shiftPt, shiftPt_shiftPt]
  rw [← hw' (unitOf p + -n) (by omega) (by omega), show unitOf p + -n + n = unitOf p by omega,
    show -(unitOf p + -n) + -n = -unitOf p by omega]

/-! ### The zones, normalised, and their checks -/

/-- The generic zone before a double step (front f at −3, 9 at −2; a = min(n, 5), j = min(k − n, 3)). -/
def zN (a j : Nat) (v : Int) : Nat :=
  if v ≤ -4 then (if 2 - 2 * (a : Int) ≤ v ∧ v % 2 = 0 then 11 else 7)
  else if v = -3 then 15 else if v = -2 then 9 else if v < j then 13 else if v = j then 15 else 7

/-- … and after it (front at −2, −1). -/
def zT (a j : Nat) (v : Int) : Nat :=
  if v ≤ -3 then (if 1 - 2 * (a : Int) ≤ v ∧ (v - 1) % 2 = 0 then 11 else 7)
  else if v = -2 then 15 else if v = -1 then 9 else if v < j then 13 else if v = j then 15 else 7

def zoneG (a j : Nat) : Bool :=
  pieceCheck (fun v => hexCells (zN a j v)) (fun v => hexCells (zT a j v)) (-7) 10 [] [] 2 (-5) 0 zoneFrame

/-- The first double step: the store (j = min(k, 4)) with the stator of unit −1 removed, and W k 1. -/
def s0N (j : Nat) (v : Int) : Nat := if 0 ≤ v ∧ v < j then 13 else if v = j then 15 else 7
def s1N (j : Nat) (v : Int) : Nat := if v = -1 then 5 else if 0 ≤ v ∧ v < j then 13 else if v = j then 15 else 7
def s2N (j : Nat) (v : Int) : Nat :=
  if v ≤ -2 then 7 else if v = -1 then 15 else if v = 0 then 9 else if v < j then 13 else if v = j then 15 else 7

def zone0 (j : Nat) : Bool :=
  pieceCheck (fun v => hexCells (s0N j v)) (fun v => hexCells (s1N j v)) (-5) 9 [⟨-2, 1, 4⟩] [] 2 (-3) 1 zoneFrame
def zone1 (j : Nat) : Bool :=
  pieceCheck (fun v => hexCells (s1N j v)) (fun v => hexCells (s2N j v)) (-5) 9 [] [] 2 (-3) 1 zoneFrame

/-- The front meets the edge (n = k + 1, then k + 2), normalised at unit k + 1 and at unit k; a = min(k, 4). -/
def e1N (a : Nat) (v : Int) : Nat :=
  if v ≤ -4 then (if -2 * (a : Int) ≤ v ∧ v % 2 = 0 then 11 else 7)
  else if v = -3 then 15 else if v = -2 then 9 else if v = -1 then 15 else 7
def e1T (a : Nat) (v : Int) : Nat :=
  if v ≤ -3 then (if -2 * (a : Int) - 1 ≤ v ∧ (v - 1) % 2 = 0 then 11 else 7) else if v = -2 then 15 else 7
def e2N (a : Nat) (v : Int) : Nat :=
  if v ≤ -2 then (if -2 * (a : Int) ≤ v ∧ v % 2 = 0 then 11 else 7) else if v = -1 then 15 else 7
def e2T (a : Nat) (v : Int) : Nat :=
  if -1 - 2 * (a : Int) ≤ v ∧ v < -1 ∧ (v - 1) % 2 = 0 then 11 else 7

def zoneE1 (a : Nat) : Bool :=
  pieceCheck (fun v => hexCells (e1N a v)) (fun v => hexCells (e1T a v)) (-7) 10 [] [] 2 (-5) 0 zoneFrame
def zoneE2 (a : Nat) : Bool :=
  pieceCheck (fun v => hexCells (e2N a v)) (fun v => hexCells (e2T a v)) (-6) 10 [] [] 2 (-4) 1 zoneFrame

/-- All zone checks: 16 generic, 4 + 4 at the start, 4 + 4 at the edge. -/
def zonesOK : Bool :=
  (List.range 4).all (fun a => (List.range 4).all (fun j => zoneG (a + 2) j)) &&
  (List.range 4).all (fun j => zone0 (j + 1) && zone1 (j + 1)) &&
  (List.range 4).all (fun a => zoneE1 (a + 1) && zoneE2 (a + 1))

theorem zonesOK_ok : zonesOK = true := by decide +kernel

theorem zones (a j : Nat) :
    (2 ≤ a → a ≤ 5 → j ≤ 3 → zoneG a j = true) ∧ (1 ≤ j → j ≤ 4 → zone0 j = true ∧ zone1 j = true) ∧
    (1 ≤ a → a ≤ 4 → zoneE1 a = true ∧ zoneE2 a = true) := by
  have hz := zonesOK_ok
  simp only [zonesOK, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hz
  obtain ⟨⟨h1, h2⟩, h3⟩ := hz
  refine ⟨fun ha hb hj => ?_, fun hj hj' => ?_, fun ha hb => ?_⟩
  · have := h1 (a - 2) (by omega) j (by omega); rwa [show a - 2 + 2 = a by omega] at this
  · have := h2 (j - 1) (by omega); rwa [show j - 1 + 1 = j by omega] at this
  · have := h3 (a - 1) (by omega); rwa [show a - 1 + 1 = a by omega] at this

theorem xor_nil (c : Config) (n : Int) (q : Pt) : c q = xor (c q) (lcfg (([] : List Pt).map (shiftPt n)) q) := by
  simp [lcfg]

set_option maxHeartbeats 4000000 in
/-- **The generic double step**: the front moves one unit through the stretch. -/
theorem step_generic (k n : Nat) (hk : 1 ≤ k) (h2 : 2 ≤ n) (hnk : n ≤ k) :
    run (hcfg (W k n)) 2 = hcfg (W k (n + 1)) := by
  have zg := (zones (min n 5) (min (k - n) 3)).1 (by omega) (by omega) (by omega)
  unfold zoneG at zg
  rw [W_gen h2 (by omega), W_gen (n := n + 1) (by omega) (by omega)]
  funext p
  by_cases hL : unitOf p ≤ (n : Int) - 6
  · apply step_left (Wg k n) (Wg k (n + 1)) _ p
    · intro i h1 h2; simp only [Wg]; repeat' split
      all_goals omega
    · simp only [Wg]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (n : Int) + 1 ≤ unitOf p
    · apply step_right k hk (Wg k n) (Wg k (n + 1)) _ p
      · intro i h1 h2; simp only [Wg, storeWord]; repeat' split
        all_goals omega
      · simp only [Wg, storeWord]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Wg k n) (Wg k (n + 1)) [] n (-5) 0 (-7) (zN (min n 5) (min (k - n) 3))
        (zT (min n 5) (min (k - n) 3)) 10 (by decide) (by decide) zg (by decide)
      · intro v h1 h2; simp only [Wg, zN]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Wg, zT]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

theorem store_removed (k : Nat) : store k ⟨-2, 1, 4⟩ = true := by
  show lcfg (hexCells (storeWord k (unitOf ⟨-2, 1, 4⟩))) (shiftPt (-unitOf ⟨-2, 1, 4⟩) ⟨-2, 1, 4⟩) = true
  have hu : unitOf ⟨-2, 1, 4⟩ = -1 := by decide
  have hs : storeWord k (-1) = 7 := by simp only [storeWord]; repeat' split
                                       all_goals omega
  rw [hu, hs]
  decide

set_option maxHeartbeats 4000000 in
/-- **The first double step**: the count read. -/
theorem step_first (k : Nat) (hk : 1 ≤ k) : run (countRead k) 2 = hcfg (W k 1) := by
  have z0 := ((zones 0 (min k 4)).2.1 (by omega) (by omega)).1
  unfold zone0 at z0
  have far : ∀ q, (unitOf q ≤ -2 ∨ 0 ≤ unitOf q) → countRead k q = hcfg (storeWord k) q := by
    intro q hq
    simp only [countRead, store]
    have : q ≠ shiftPt (-1) ⟨0, 1, 2⟩ := by
      intro e; rw [e] at hq; simp only [unitOf_shiftPt] at hq
      have : unitOf ⟨0, 1, 2⟩ = 0 := by decide
      omega
    simp [this]
  rw [W_one]
  funext p
  by_cases hL : unitOf p ≤ -4
  · apply step_right k hk (storeWord k) (W1 k) _ p (fun i _ _ => rfl)
    · simp only [W1, storeWord]; repeat' split
      all_goals omega
    · intro q h1 h2; exact far q (by omega)
  · by_cases hR : 2 ≤ unitOf p
    · apply step_right k hk (storeWord k) (W1 k) _ p (fun i _ _ => rfl)
      · simp only [W1, storeWord]; repeat' split
        all_goals omega
      · intro q h1 h2; exact far q (by omega)
    · apply step_zone (storeWord k) (W1 k) [⟨-2, 1, 4⟩] 0 (-3) 1 (-5) (s0N (min k 4)) (s1N (min k 4)) 9 (by decide) (by decide)
        z0 (by decide)
      · intro v h1 h2; simp only [storeWord, s0N]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [W1, s1N]; repeat' split
        all_goals omega
      · intro q _ _
        simp only [List.map, shiftPt_zero]
        simp only [countRead, store, lcfg, List.contains_cons, List.contains_nil, Bool.or_false]
        by_cases e : q = ⟨-2, 1, 4⟩
        · subst e
          have := store_removed k
          simp only [store] at this
          simp [this, shiftPt]
        · have : (q == (⟨-2, 1, 4⟩ : Pt)) = false := by simp [e]
          have e' : q ≠ shiftPt (-1) ⟨0, 1, 2⟩ := by simp only [shiftPt]; exact e
          simp [this, e']
      · omega
      · omega

set_option maxHeartbeats 4000000 in
/-- **The second double step.** -/
theorem step_second (k : Nat) (hk : 1 ≤ k) : run (hcfg (W k 1)) 2 = hcfg (W k 2) := by
  have z1 := ((zones 0 (min k 4)).2.1 (by omega) (by omega)).2
  unfold zone1 at z1
  rw [W_one, W_gen (n := 2) (by omega) (by omega)]
  funext p
  by_cases hL : unitOf p ≤ -4
  · apply step_right k hk (W1 k) (Wg k 2) _ p
    · intro i h1 h2; simp only [W1, Wg, storeWord]; repeat' split
      all_goals omega
    · simp only [W1, Wg, storeWord]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : 2 ≤ unitOf p
    · apply step_right k hk (W1 k) (Wg k 2) _ p
      · intro i h1 h2; simp only [W1, Wg, storeWord]; repeat' split
        all_goals omega
      · simp only [W1, Wg, storeWord]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (W1 k) (Wg k 2) [] 0 (-3) 1 (-5) (s1N (min k 4)) (s2N (min k 4)) 9 (by decide) (by decide) z1 (by decide)
      · intro v h1 h2; simp only [W1, Wg, s1N]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [W1, Wg, s2N]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

set_option maxHeartbeats 4000000 in
/-- **The front meets the edge.** -/
theorem step_edge1 (k : Nat) (hk : 1 ≤ k) : run (hcfg (W k (k + 1))) 2 = hcfg (W k (k + 2)) := by
  have ze := ((zones (min k 4) 0).2.2 (by omega) (by omega)).1
  unfold zoneE1 at ze
  rw [W_gen (n := k + 1) (by omega) (by omega), W_edge]
  funext p
  by_cases hL : unitOf p ≤ (k : Int) - 5
  · apply step_left (Wg k (k + 1)) (We k) _ p
    · intro i h1 h2; simp only [Wg, We]; repeat' split
      all_goals omega
    · simp only [Wg, We]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (k : Int) + 2 ≤ unitOf p
    · apply step_right k hk (Wg k (k + 1)) (We k) _ p
      · intro i h1 h2; simp only [Wg, We, storeWord]; repeat' split
        all_goals omega
      · simp only [Wg, We, storeWord]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (Wg k (k + 1)) (We k) [] ((k : Int) + 1) (-5) 0 (-7) (e1N (min k 4)) (e1T (min k 4)) 10
        (by decide) (by decide) ze (by decide)
      · intro v h1 h2; simp only [Wg, We, e1N]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [Wg, We, e1T]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

set_option maxHeartbeats 4000000 in
/-- **The last double step**: the edge is gone, the train leaves. -/
theorem step_edge2 (k : Nat) (hk : 1 ≤ k) : run (hcfg (W k (k + 2))) 2 = hcfg (W k (k + 3)) := by
  have ze := ((zones (min k 4) 0).2.2 (by omega) (by omega)).2
  unfold zoneE2 at ze
  rw [W_edge, W_fin (n := k + 3) (by omega)]
  funext p
  by_cases hL : unitOf p ≤ (k : Int) - 5
  · apply step_left (We k) (Wf k (k + 3)) _ p
    · intro i h1 h2; simp only [We, Wf]; repeat' split
      all_goals omega
    · simp only [We, Wf]; repeat' split
      all_goals omega
    · intro q _ _; rfl
  · by_cases hR : (k : Int) + 2 ≤ unitOf p
    · apply step_left (We k) (Wf k (k + 3)) _ p
      · intro i h1 h2; simp only [We, Wf]; repeat' split
        all_goals omega
      · simp only [We, Wf]; repeat' split
        all_goals omega
      · intro q _ _; rfl
    · apply step_zone (We k) (Wf k (k + 3)) [] (k : Int) (-4) 1 (-6) (e2N (min k 4)) (e2T (min k 4)) 10
        (by decide) (by decide) ze (by decide)
      · intro v h1 h2; simp only [We, Wf, e2N]; repeat' split
        all_goals omega
      · intro v h1 h2; simp only [We, Wf, e2T]; repeat' split
        all_goals omega
      · intro q _ _; exact xor_nil _ _ _
      · omega
      · omega

/-! ### The unzip law -/

/-- **The orbit of the count read**: at generation 2n (1 ≤ n ≤ k + 3) the store wire is the word W k n. -/
theorem countRead_W (k : Nat) (hk : 1 ≤ k) : ∀ n, 1 ≤ n → n ≤ k + 3 → run (countRead k) (2 * n) = hcfg (W k n) := by
  intro n h1 h2
  induction n with
  | zero => omega
  | succ n ih =>
    by_cases h0 : n = 0
    · subst h0; exact step_first k hk
    · rw [show 2 * (n + 1) = 2 * n + 2 by omega, run_add, ih (by omega) (by omega)]
      by_cases e1 : n = 1
      · subst e1; exact step_second k hk
      · by_cases e2 : n ≤ k
        · exact step_generic k n hk (by omega) e2
        · by_cases e3 : n = k + 1
          · subst e3; exact step_edge1 k hk
          · obtain rfl : n = k + 2 := by omega
            exact step_edge2 k hk

theorem W_final_tape (k : Nat) : hcfg (W k (k + 3)) = tape (pulses k (2 - ((k + 3 : Nat) : Int))) := by
  rw [tape_eq_hcfg, W_fin (Nat.le_refl _)]
  congr 1
  funext u
  simp only [Wf, pulses, hexOf]
  split <;> simp_all

/-- **The unzip law, sharp** (`REVIEW-signals-8.md` section 3): for every k ≥ 1, from generation 2k + 6 on the count
read has left plain wire B with exactly k pulses two units apart, the leading one at unit 2 − t/2; not at 2k + 4. -/
theorem unzip_law_sharp : UnzipLawSharp := by
  intro k hk
  refine ⟨fun n hn => ?_, ?_⟩
  · obtain ⟨m, rfl⟩ : ∃ m, n = k + 3 + m := ⟨n - (k + 3), by omega⟩
    rw [show 2 * (k + 3 + m) = 2 * (k + 3) + 2 * m by omega, run_add, countRead_W k hk _ (by omega) (Nat.le_refl _),
      W_final_tape, tape_run]
    congr 1
    funext u
    simp only [pulses]
    have e1 : (2 - ((k + 3 : Nat) : Int) ≤ u + (m : Int)) ↔ (2 - ((k + 3 + m : Nat) : Int) ≤ u) := by omega
    have e2 : (u + (m : Int) < 2 - ((k + 3 : Nat) : Int) + 2 * k) ↔ (u < 2 - ((k + 3 + m : Nat) : Int) + 2 * k) := by
      omega
    have e3 : ((u + (m : Int) - (2 - ((k + 3 : Nat) : Int))) % 2 = 0) ↔
        ((u - (2 - ((k + 3 + m : Nat) : Int))) % 2 = 0) := by omega
    simp only [e1, e2, e3]
  · rw [countRead_W k hk _ (by omega) (by omega), W_edge]
    intro e
    have := congrFun e (shiftPt ((k : Int) - 1) ⟨0, 2, 3⟩)
    have hu : unitOf (shiftPt ((k : Int) - 1) ⟨0, 2, 3⟩) = (k : Int) - 1 := by
      have h0 : unitOf ⟨0, 2, 3⟩ = 0 := by decide
      rw [unitOf_shiftPt, h0]; omega
    simp only [hcfg, tape, ucfg, hu, shiftPt_shiftPt] at this
    rw [show -((k : Int) - 1) + ((k : Int) - 1) = 0 by omega, shiftPt_zero] at this
    have hW : We k ((k : Int) - 1) = 15 := by
      simp only [We]
      rw [if_neg (show ¬ ((k : Int) - 1 ≤ (k : Int) - 2) by omega)]
      simp
    have hP : pulses k (2 - ((k : Int) + 2)) ((k : Int) - 1) = .B := by
      simp only [pulses]; split
      · omega
      · rfl
    rw [hW, hP] at this
    exact absurd this (by decide)

/-- **The unzip law** as push 8 states it (from generation 4k + 8). -/
theorem unzip_law : UnzipLaw :=
  unzipLawSharp_imp unzip_law_sharp

end Gump.Unzip
