/-
**The clock from a single cell** (`research/signals/README.md` section 11, "Lit by adding one cell, it becomes an
oscillator"; the owner's journal, 2026-11-15, 10:30). For every N ≥ 6 the lit clock of N units (capL, N units of
wire C, capR, and the one cell (1,0,4) of unit N / 2) is, once its rake reaches unit N − 1 (generation N − 2 for even
N, N − 1 for odd N), a state of the cycle `clockOf N` (`lit_enters`); so from then on it is an oscillator of exact
period 4N + 2 (`lit_clock`). With `lit_clock_small` (N ≤ 5) this holds for every N ≥ 1.

The transient is a word (`FL N m`, checked against `reference/oracle.py` by `tape_lit.py` for N = 6 .. 30): at
generation 2m the rake `f` is at unit N/2 + m, units of wire B (the pulses p<) at N/2 − m + 2i behind it, wire C
elsewhere, the caps untouched. One double step of it is proved as for the unzip law: tape windows on the wire,
one zone at each cap and one at the rake (`zonesLit_ok`), for N ≥ 17; N = 6 .. 16 by direct kernel runs. The match
with the surgery is arithmetic on `chart` (every chart then shows base time 8 or 10) and four facts about the base.
-/
import Gump.Clock
import Gump.ClockLitData
import Gump.UnzipProof
import Gump.Speed

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-! ### The transient as a word -/

/-- The wire's letter on unit u at generation 2m: the rake (15) at N/2 + m, wire B (7) at N/2 − m + 2i, else wire C. -/
def LW (N m : Nat) (u : Int) : Nat :=
  if u = ((N / 2 : Nat) : Int) + m then 15
  else if ((N / 2 : Nat) : Int) - m ≤ u ∧ u < ((N / 2 : Nat) : Int) + m ∧
    (u - (((N / 2 : Nat) : Int) - m)) % 2 = 0 then 7 else 11

/-- The whole lit clock at generation 2m, unit by unit. -/
def FL (N m : Nat) (u : Int) : List Pt := if u < 0 then capLU u else if u < N then hexCells (LW N m u) else capRU (u - N)

/-- The last m of the transient: the rake at unit N − 1. -/
def mmax (N : Nat) : Nat := (N + 1) / 2 - 1

theorem capLU_unit : ∀ u, ∀ q ∈ capLU u, unitOf q = 0 := by
  intro u; unfold capLU; split <;> decide
theorem capRU_unit : ∀ u, ∀ q ∈ capRU u, unitOf q = 0 := by
  intro u; unfold capRU; split <;> decide

theorem FL_unit (N m : Nat) : ∀ u, ∀ q ∈ FL N m u, unitOf q = 0 := by
  intro u; unfold FL; split
  · exact capLU_unit u
  · split
    · exact hexCells_unit _
    · exact capRU_unit _

/-- capL, unit by unit. -/
theorem capL_ucfg : lcfg capL = ucfg capLU := by
  have h1 : ∀ q ∈ capL, shiftPt (-unitOf q) q ∈ capLU (unitOf q) := by decide +kernel
  have h2 : ∀ u : Int, -4 ≤ u → u ≤ -1 → ∀ c ∈ capLU u, shiftPt u c ∈ capL := by
    intro u a b
    rcases (show u = -4 ∨ u = -3 ∨ u = -2 ∨ u = -1 by omega) with rfl | rfl | rfl | rfl <;> decide +kernel
  have h3 : ∀ u : Int, (u < -4 ∨ -1 < u) → capLU u = [] := by
    intro u hu; unfold capLU; split <;> first | rfl | omega
  funext p
  apply Bool.eq_iff_iff.mpr
  simp only [ucfg, lcfg_iff]
  constructor
  · exact h1 p
  · intro h
    by_cases hu : -4 ≤ unitOf p ∧ unitOf p ≤ -1
    · have := h2 _ hu.1 hu.2 _ h; rwa [shiftPt_shiftPt_neg] at this
    · rw [h3 _ (by omega)] at h; simp at h

/-- capR, unit by unit. -/
theorem capR_ucfg : lcfg capR = ucfg capRU := by
  have h1 : ∀ q ∈ capR, shiftPt (-unitOf q) q ∈ capRU (unitOf q) := by decide +kernel
  have h2 : ∀ u : Int, 0 ≤ u → u ≤ 3 → ∀ c ∈ capRU u, shiftPt u c ∈ capR := by
    intro u a b
    rcases (show u = 0 ∨ u = 1 ∨ u = 2 ∨ u = 3 by omega) with rfl | rfl | rfl | rfl <;> decide +kernel
  have h3 : ∀ u : Int, (u < 0 ∨ 3 < u) → capRU u = [] := by
    intro u hu; unfold capRU; split <;> first | rfl | omega
  funext p
  apply Bool.eq_iff_iff.mpr
  simp only [ucfg, lcfg_iff]
  constructor
  · exact h1 p
  · intro h
    by_cases hu : 0 ≤ unitOf p ∧ unitOf p ≤ 3
    · have := h2 _ hu.1 hu.2 _ h; rwa [shiftPt_shiftPt_neg] at this
    · rw [h3 _ (by omega)] at h; simp at h

theorem capLU_nil {u : Int} (h : 0 ≤ u) : capLU u = [] := by unfold capLU; split <;> first | rfl | omega
theorem capRU_nil {u : Int} (h : u < 0) : capRU u = [] := by unfold capRU; split <;> first | rfl | omega

theorem lcfg_one (e q : Pt) : lcfg [e] q = (q == e) := by
  apply Bool.eq_iff_iff.mpr; rw [lcfg_iff]; simp

theorem hex15 : lcfg (hexCells 15) = fun q => lcfg (cellsOf .C) q || q == ⟨1, 0, 4⟩ := by
  have e : lcfg (hexCells 15) = lcfg (cellsOf .C ++ [⟨1, 0, 4⟩]) := (sameL_iff _ _).mp (by decide)
  funext q; rw [e, lcfg_append', lcfg_one]

theorem hex11 : lcfg (hexCells 11) = lcfg (cellsOf .C) := (sameL_iff _ _).mp (by decide)

theorem getD_repC : ∀ (N i : Nat), (List.replicate N Letter.C).getD i .C = .C
  | 0, i => by simp
  | N + 1, 0 => by simp [List.replicate_succ]
  | N + 1, i + 1 => by simp only [List.replicate_succ, List.getD_cons_succ]; exact getD_repC N i

/-- **The lit clock at generation 0 is the word.** -/
theorem lit_init (N : Nat) (hN : 1 ≤ N) : lcfg (litList N) = ucfg (FL N 0) := by
  funext p
  have hign : lcfg [shiftPt ((N / 2 : Nat) : Int) ⟨1, 0, 4⟩] p =
      (decide (unitOf p = ((N / 2 : Nat) : Int)) && (shiftPt (-unitOf p) p == ⟨1, 0, 4⟩)) := by
    apply Bool.eq_iff_iff.mpr
    rw [lcfg_iff]
    simp only [List.mem_singleton, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq]
    constructor
    · intro h; rw [h]; refine ⟨?_, ?_⟩
      · rw [unitOf_shiftPt]; show (1 : Int) / 2 + _ = _; omega
      · rw [unitOf_shiftPt, show unitOf ⟨1, 0, 4⟩ = 0 by decide, Int.zero_add, shiftPt_neg_shiftPt]
    · rintro ⟨h1, h2⟩; rw [← h2, h1, shiftPt_shiftPt_neg]
  simp only [litList, lcfg_append', lcfg_wordList, lcfg_map_shiftPt, capL_ucfg, capR_ucfg, shiftC, hign]
  simp only [ucfg, FL, unitOf_shiftPt, shiftPt_shiftPt, List.length_replicate, getD_repC]
  rw [show -(unitOf p + -(N : Int)) + -(N : Int) = -unitOf p by omega]
  by_cases h0 : unitOf p < 0
  · rw [if_pos h0, capRU_nil (by omega), lcfg_nil']
    have : ¬ (0 ≤ unitOf p ∧ unitOf p < 0 + (N : Int)) := by omega
    have h2 : ¬ unitOf p = (N : Int) / 2 := by omega
    have h3 : ¬ (0 ≤ unitOf p) := by omega
    simp [h2, h3]
  · rw [if_neg h0, capLU_nil (by omega), lcfg_nil', Bool.false_or]
    by_cases h1 : unitOf p < N
    · rw [if_pos h1, capRU_nil (by omega), lcfg_nil', Bool.or_false]
      have : 0 ≤ unitOf p ∧ unitOf p < 0 + (N : Int) := by omega
      rw [decide_eq_true this, Bool.true_and]
      by_cases h2 : unitOf p = ((N / 2 : Nat) : Int)
      · have hl : LW N 0 (unitOf p) = 15 := by simp only [LW]; rw [if_pos (by omega)]
        rw [hl, hex15, decide_eq_true h2, Bool.true_and]
      · have hl : LW N 0 (unitOf p) = 11 := by
          simp only [LW]; rw [if_neg (by omega), if_neg (by omega)]
        rw [hl, hex11, decide_eq_false h2, Bool.false_and, Bool.or_false]
    · rw [if_neg h1]
      have : ¬ (0 ≤ unitOf p ∧ unitOf p < 0 + (N : Int)) := by omega
      have h2 : ¬ unitOf p = ((N / 2 : Nat) : Int) := by omega
      simp only [this, decide_false, Bool.false_and, Bool.false_or, h2, Bool.or_false]
      rfl

/-! ### One double step, locally -/

theorem capLU_nil' {u : Int} (h : u < -4) : capLU u = [] := by unfold capLU; split <;> first | rfl | omega
theorem capRU_nil' {u : Int} (h : 3 < u) : capRU u = [] := by unfold capRU; split <;> first | rfl | omega

theorem FL_out (N m : Nat) (q : Pt) (h : unitOf q < -4 ∨ (N : Int) + 3 < unitOf q) : ucfg (FL N m) q = false := by
  simp only [ucfg, FL]
  rcases h with h | h
  · rw [if_pos (by omega), capLU_nil' h]; rfl
  · rw [if_neg (by omega), if_neg (by omega), capRU_nil' (by omega)]; rfl

theorem FL_wire (N m : Nat) (q : Pt) (h0 : 0 ≤ unitOf q) (h1 : unitOf q < N) :
    ucfg (FL N m) q = hcfg (LW N m) q := by
  simp only [ucfg, hcfg, FL]; rw [if_neg (by omega), if_pos h1]

/-- Two generations of a point whose five units are empty. -/
theorem run2_empty (c : Config) (p : Pt) (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = false) :
    run c 2 p = false := by
  rw [run_eq_of_units (c' := fun _ => false) 2 h, run_empty]

/-- `UnzipProof.step_zone` for words given unit by unit (caps included). -/
theorem step_zoneU (F F' : Int → List Pt) (n lo hi a : Int) (f g : Int → List Pt)
    (hf : ∀ u, ∀ q ∈ f u, unitOf q = 0) (hg : ∀ u, ∀ q ∈ g u, unitOf q = 0) (len : Nat) (V : Pt) (hV : V.even)
    (ha : a = lo - 2) (hlen : (len : Int) = hi - lo + 5) (h : pieceCheck f g a len [] [] 2 lo hi V = true)
    (hb : -8 ≤ lo + V.x / 2 ∧ hi + V.x / 2 ≤ 23 ∧ lo ≤ hi) (c : Config)
    (hw : ∀ v, lo - 2 ≤ v → v ≤ hi + 2 → F (v + n) = f v)
    (hw' : ∀ v, lo ≤ v → v ≤ hi → F' (v + n) = g v)
    (hc : ∀ q, lo + n - 2 ≤ unitOf q → unitOf q ≤ hi + n + 2 → c q = ucfg F q)
    (p : Pt) (hp1 : lo + n ≤ unitOf p) (hp2 : unitOf p ≤ hi + n) : run c 2 p = ucfg F' p := by
  subst ha
  have agree : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 →
      c q = shiftC n (xorC (ucfg f) (lcfg [])) q := by
    intro q h1 h2
    rw [hc q (by omega) (by omega)]
    simp only [shiftC, xorC, ucfg, unitOf_shiftPt, shiftPt_shiftPt, lcfg_nil', Bool.xor_false]
    rw [← hw (unitOf q + -n) (by omega) (by omega), show unitOf q + -n + n = unitOf q by omega,
      show -(unitOf q + -n) + -n = -unitOf q by omega]
  rw [run_eq_of_units 2 (fun q h1 h2 => agree q (by omega) (by omega)), run_shiftC]
  simp only [shiftC]
  have spec := pieceCheck_spec hf hg hV h (by omega) (by omega) (by omega) (by omega) (by omega)
    (xorC (ucfg f) (lcfg [])) (fun q _ _ => rfl) (shiftPt (-n) p)
    (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
  rw [spec]
  simp only [xorC, lcfg_nil', Bool.xor_false, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  rw [← hw' (unitOf p + -n) (by omega) (by omega), show unitOf p + -n + n = unitOf p by omega,
    show -(unitOf p + -n) + -n = -unitOf p by omega]

/-! ### The zones of the transient, normalised, and their checks -/

/-- The box translation for the zone checks. -/
def litFrame : Pt := ⟨12, 8, 16⟩

theorem litFrame_even : litFrame.even := by
  show (12 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

/-- Left cap zone (units −8 .. 6), the first pulse p< of wire B at unit a (a = min(N/2 − m, 9)). -/
def zLN (a : Nat) (v : Int) : List Pt :=
  if v < 0 then capLU v else hexCells (if (a : Int) ≤ v ∧ (v - a) % 2 = 0 then 7 else 11)
def zLT (a : Nat) (v : Int) : List Pt :=
  if v < 0 then capLU v else hexCells (if (a : Int) - 1 ≤ v ∧ (v - a + 1) % 2 = 0 then 7 else 11)
def zoneL (a : Nat) : Bool := pieceCheck (zLN a) (zLT a) (-8) 15 [] [] 2 (-6) 4 litFrame

/-- Right cap zone (units N − 8 .. N + 7, moved by −N), the rake b + 1 units before the cap (b = min(d, 9)). -/
def zRN (b : Nat) (v : Int) : List Pt :=
  if v < 0 then hexCells (if v = -1 - b then 15 else if v < -1 - b ∧ (v + 1 + b) % 2 = 0 then 7 else 11)
  else capRU v
def zRT (b : Nat) (v : Int) : List Pt :=
  if v < 0 then hexCells (if v = -(b : Int) then 15 else if v < -(b : Int) ∧ (v + b) % 2 = 0 then 7 else 11)
  else capRU v
def zoneR (b : Nat) : Bool := pieceCheck (zRN b) (zRT b) (-8) 16 [] [] 2 (-6) 5 litFrame

/-- The rake zone (units R − 4 .. R + 4, moved by −R), c = min(m, 2) pulses behind it. -/
def zKN (c : Nat) (v : Int) : List Pt :=
  hexCells (if v = 0 then 15 else if -2 * (c : Int) ≤ v ∧ v < 0 ∧ v % 2 = 0 then 7 else 11)
def zKT (c : Nat) (v : Int) : List Pt :=
  hexCells (if v = 1 then 15 else if -2 * (c : Int) - 1 ≤ v ∧ v < 1 ∧ (v + 1) % 2 = 0 then 7 else 11)
def zoneK (c : Nat) : Bool := pieceCheck (zKN c) (zKT c) (-4) 9 [] [] 2 (-2) 2 litFrame

def zonesLit : Bool :=
  (List.range 9).all (fun a => zoneL (a + 1)) && (List.range 9).all (fun b => zoneR (b + 1)) &&
  (List.range 3).all zoneK

theorem zonesLit_ok : zonesLit = true := by decide +kernel

theorem zonesLit_spec (a b c : Nat) :
    (1 ≤ a → a ≤ 9 → zoneL a = true) ∧ (1 ≤ b → b ≤ 9 → zoneR b = true) ∧ (c ≤ 2 → zoneK c = true) := by
  have hz := zonesLit_ok
  simp only [zonesLit, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hz
  obtain ⟨⟨h1, h2⟩, h3⟩ := hz
  refine ⟨fun h h' => ?_, fun h h' => ?_, fun h => h3 c (by omega)⟩
  · have := h1 (a - 1) (by omega); rwa [show a - 1 + 1 = a by omega] at this
  · have := h2 (b - 1) (by omega); rwa [show b - 1 + 1 = b by omega] at this

theorem capLU_unit' : ∀ u, ∀ q ∈ capLU u, unitOf q = 0 := capLU_unit
theorem zLN_unit (a : Nat) : ∀ u, ∀ q ∈ zLN a u, unitOf q = 0 := by
  intro u; unfold zLN; split; exact capLU_unit u; exact hexCells_unit _
theorem zLT_unit (a : Nat) : ∀ u, ∀ q ∈ zLT a u, unitOf q = 0 := by
  intro u; unfold zLT; split; exact capLU_unit u; exact hexCells_unit _
theorem zRN_unit (b : Nat) : ∀ u, ∀ q ∈ zRN b u, unitOf q = 0 := by
  intro u; unfold zRN; split; exact hexCells_unit _; exact capRU_unit u
theorem zRT_unit (b : Nat) : ∀ u, ∀ q ∈ zRT b u, unitOf q = 0 := by
  intro u; unfold zRT; split; exact hexCells_unit _; exact capRU_unit u
theorem zKN_unit (c : Nat) : ∀ u, ∀ q ∈ zKN c u, unitOf q = 0 := fun _ => hexCells_unit _
theorem zKT_unit (c : Nat) : ∀ u, ∀ q ∈ zKT c u, unitOf q = 0 := fun _ => hexCells_unit _

/-! ### The double step of the transient -/

set_option maxHeartbeats 4000000 in
/-- **One double step of the transient**, for N ≥ 16: the rake moves one unit, a pulse p< is left behind it. -/
theorem lit_step_big (N m : Nat) (hN : 16 ≤ N) (hm : m + 1 ≤ mmax N) :
    run (ucfg (FL N m)) 2 = ucfg (FL N (m + 1)) := by
  have hmm : m + 1 ≤ (N + 1) / 2 - 1 := hm
  have zl := (zonesLit_spec (min (N / 2 - m) 9) (min (N - 1 - (N / 2 + m)) 9) (min m 2)).1 (by omega) (by omega)
  have zr := (zonesLit_spec (min (N / 2 - m) 9) (min (N - 1 - (N / 2 + m)) 9) (min m 2)).2.1 (by omega) (by omega)
  have zk := (zonesLit_spec (min (N / 2 - m) 9) (min (N - 1 - (N / 2 + m)) 9) (min m 2)).2.2 (by omega)
  unfold zoneL at zl; unfold zoneR at zr; unfold zoneK at zk
  funext p
  by_cases hA : unitOf p ≤ -7
  · rw [run2_empty _ p (fun q _ _ => FL_out N m q (by omega)), FL_out N (m + 1) p (by omega)]
  by_cases hB : unitOf p ≤ 4
  · refine step_zoneU (FL N m) (FL N (m + 1)) 0 (-6) 4 (-8) _ _ (zLN_unit _) (zLT_unit _) 15 litFrame
      litFrame_even (by decide) (by decide) zl (by decide) _ ?_ ?_ (fun _ _ _ => rfl) p (by omega) (by omega)
    · intro v h1 h2; simp only [FL, zLN, Int.add_zero]
      by_cases hv : v < 0
      · rw [if_pos hv, if_pos hv]
      · rw [if_neg hv, if_neg hv, if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
        all_goals omega
    · intro v h1 h2; simp only [FL, zLT, Int.add_zero]
      by_cases hv : v < 0
      · rw [if_pos hv, if_pos hv]
      · rw [if_neg hv, if_neg hv, if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
        all_goals omega
  by_cases hC : (N : Int) + 6 ≤ unitOf p
  · rw [run2_empty _ p (fun q _ _ => FL_out N m q (by omega)), FL_out N (m + 1) p (by omega)]
  by_cases hD : (N : Int) - 6 ≤ unitOf p
  · refine step_zoneU (FL N m) (FL N (m + 1)) N (-6) 5 (-8) _ _ (zRN_unit _) (zRT_unit _) 16 litFrame
      litFrame_even (by decide) (by decide) zr (by decide) _ ?_ ?_ (fun _ _ _ => rfl) p (by omega) (by omega)
    · intro v h1 h2; simp only [FL, zRN]
      by_cases hv : v < 0
      · rw [if_pos hv, if_neg (by omega), if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
        all_goals omega
      · rw [if_neg hv, if_neg (by omega), if_neg (by omega), show v + (N : Int) - N = v by omega]
    · intro v h1 h2; simp only [FL, zRT]
      by_cases hv : v < 0
      · rw [if_pos hv, if_neg (by omega), if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
        all_goals omega
      · rw [if_neg hv, if_neg (by omega), if_neg (by omega), show v + (N : Int) - N = v by omega]
  -- the wire: 5 ≤ unitOf p ≤ N − 7
  have hw0 : 0 ≤ unitOf p ∧ unitOf p < N := by omega
  by_cases hK : ((N / 2 : Nat) : Int) + m - 2 ≤ unitOf p ∧ unitOf p ≤ ((N / 2 : Nat) : Int) + m + 2
  · refine step_zoneU (FL N m) (FL N (m + 1)) (((N / 2 : Nat) : Int) + m) (-2) 2 (-4) _ _ (zKN_unit _)
      (zKT_unit _) 9 litFrame litFrame_even (by decide) (by decide) zk (by decide) _ ?_ ?_ (fun _ _ _ => rfl) p
      (by omega) (by omega)
    · intro v h1 h2; simp only [FL, zKN]
      rw [if_neg (by omega), if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
      all_goals omega
    · intro v h1 h2; simp only [FL, zKT]
      rw [if_neg (by omega), if_pos (by omega)]; congr 1; simp only [LW]; repeat' split
      all_goals omega
  rw [FL_wire N (m + 1) p hw0.1 hw0.2]
  apply step_left (LW N m) (LW N (m + 1)) _ p
  · intro i h1 h2; simp only [LW]; repeat' split
    all_goals omega
  · simp only [LW]; repeat' split
    all_goals omega
  · intro q h1 h2; exact FL_wire N m q (by omega) (by omega)

/-- The box translation for the short clock of N units (the units −8 .. 23 of the box are the units −8 .. 23). -/
def smallFrame (N : Nat) : Pt := ⟨0, 8, 2 * (N : Int)⟩

theorem smallFrame_even (N : Nat) : (smallFrame N).even := by
  show (0 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (2 * (N : Int)) % 2 = 0
  omega

/-- The whole lit clock of N ≤ 15 units, one double step, in the box. -/
def smallCheck (N m : Nat) : Bool :=
  pieceCheck (FL N m) (FL N (m + 1)) (-8) (N + 16) [] [] 2 (-6) ((N : Int) + 5) (smallFrame N)

def smallOK : Bool := (List.range 10).all (fun i => (List.range (mmax (i + 6))).all (fun m => smallCheck (i + 6) m))

theorem smallOK_ok : smallOK = true := by decide +kernel

/-- **One double step of the transient**, for 6 ≤ N ≤ 15, the whole clock at once. -/
theorem lit_step_small (N m : Nat) (h6 : 6 ≤ N) (h15 : N ≤ 15) (hm : m + 1 ≤ mmax N) :
    run (ucfg (FL N m)) 2 = ucfg (FL N (m + 1)) := by
  have hz := smallOK_ok
  simp only [smallOK, List.all_eq_true, List.mem_range] at hz
  have hc := hz (N - 6) (by omega) m (by rw [show N - 6 + 6 = N by omega]; omega)
  rw [show N - 6 + 6 = N by omega] at hc
  unfold smallCheck at hc
  funext p
  by_cases hA : unitOf p ≤ -7
  · rw [run2_empty _ p (fun q _ _ => FL_out N m q (by omega)), FL_out N (m + 1) p (by omega)]
  by_cases hC : (N : Int) + 6 ≤ unitOf p
  · rw [run2_empty _ p (fun q _ _ => FL_out N m q (by omega)), FL_out N (m + 1) p (by omega)]
  have hlen : ((N + 16 : Nat) : Int) = ((N : Int) + 5) - (-6) + 5 := by push_cast; omega
  have hb : -8 ≤ -6 + (smallFrame N).x / 2 ∧ (N : Int) + 5 + (smallFrame N).x / 2 ≤ 23 ∧ -6 ≤ (N : Int) + 5 := by
    simp only [smallFrame]; omega
  exact step_zoneU (FL N m) (FL N (m + 1)) 0 (-6) ((N : Int) + 5) (-8) _ _ (FL_unit N m) (FL_unit N (m + 1))
    (N + 16) (smallFrame N) (smallFrame_even N) (by decide) hlen hc hb _ (fun v _ _ => by rw [Int.add_zero])
    (fun v _ _ => by rw [Int.add_zero]) (fun _ _ _ => rfl) p (by omega) (by omega)

/-- One double step of the transient, for every N ≥ 6. -/
theorem lit_step (N m : Nat) (h6 : 6 ≤ N) (hm : m + 1 ≤ mmax N) : run (ucfg (FL N m)) 2 = ucfg (FL N (m + 1)) := by
  by_cases h : N ≤ 15
  · exact lit_step_small N m h6 h hm
  · exact lit_step_big N m (by omega) hm

/-- **The transient of the lit clock**: for every N ≥ 6, at generation 2m (m ≤ mmax N) it is the word `FL N m`. -/
theorem lit_word (N : Nat) (h6 : 6 ≤ N) : ∀ m, m ≤ mmax N → run (lcfg (litList N)) (2 * m) = ucfg (FL N m)
  | 0, _ => by rw [lit_init N (by omega)]; rfl
  | m + 1, hm => by
    rw [show 2 * (m + 1) = 2 * m + 2 by omega, run_add, lit_word N h6 m (by omega), lit_step N m h6 hm]

/-! ### The end of the transient is a state of the surgery's cycle -/

set_option maxHeartbeats 4000000 in
/-- At generation 2j + 8 every chart of the clock of 6 + j units shows base time 8 or 10. -/
theorem chart_entry (j : Nat) (i : Int) (h0 : 0 ≤ i) (h1 : i ≤ j) :
    chart j i (2 * j + 8) = 8 + 2 * (((j : Int) - i) % 2) := by
  simp only [chart, first]
  repeat' split
  all_goals omega

/-- The base at time 8 (e = 0) and 10 (e = 1) on the units ≤ 3: capL, then wire B on the units of parity 1 − e. -/
def BL (e : Int) (u : Int) : List Pt :=
  if u < 0 then capLU u else if u ≤ 3 then hexCells (if (u + e) % 2 = 1 then 7 else 11) else []

/-- The base at time 8 on the units ≥ 3: wire B, wire C, the rake, capR. -/
def BR (u : Int) : List Pt :=
  if u < 3 then [] else if u = 3 then hexCells 7 else if u = 4 then hexCells 11 else if u = 5 then hexCells 15
  else capRU (u - 6)

theorem BL_unit (e : Int) : ∀ u, ∀ q ∈ BL e u, unitOf q = 0 := by
  intro u; unfold BL; split
  · exact capLU_unit u
  · split
    · exact hexCells_unit _
    · simp
theorem BR_unit : ∀ u, ∀ q ∈ BR u, unitOf q = 0 := by
  intro u; unfold BR; split
  · simp
  · split
    · exact hexCells_unit _
    · split
      · exact hexCells_unit _
      · split
        · exact hexCells_unit _
        · exact capRU_unit _

def bL0 : List Pt := (piece (BL 0) (-4) 8).map (· + frame)
def bL1 : List Pt := (piece (BL 1) (-4) 8).map (· + frame)
def bR : List Pt := (piece BR 3 7).map (· + frame)

/-- Three facts about the base, by the kernel. -/
def baseLitCheck : Bool :=
  bL0.all inBox && bL1.all inBox && bR.all inBox &&
    eqOn (unitMask (-8) 11) (brun bS 15) (ofList bL0) && eqOn (unitMask (-8) 11) (brun bS 17) (ofList bL1) &&
    eqOn (unitMask 11 23) (brun bS 15) (ofList bR)

theorem baseLitCheck_ok : baseLitCheck = true := by decide +kernel

theorem ucfg_low (B : Int → List Pt) (a : Int) (hB : ∀ u, u < a → B u = []) (n : Nat) (q : Pt)
    (h : unitOf q < a + n) : (decide (a ≤ unitOf q ∧ unitOf q < a + n) && ucfg B q) = ucfg B q := by
  by_cases h1 : a ≤ unitOf q
  · rw [decide_eq_true ⟨h1, h⟩, Bool.true_and]
  · simp only [ucfg]; rw [hB _ (by omega)]; simp [lcfg_nil']

theorem ucfg_high (B : Int → List Pt) (a : Int) (n : Nat) (hB : ∀ u, a + n ≤ u → B u = []) (q : Pt)
    (h : a ≤ unitOf q) : (decide (a ≤ unitOf q ∧ unitOf q < a + n) && ucfg B q) = ucfg B q := by
  by_cases h1 : unitOf q < a + n
  · rw [decide_eq_true ⟨h, h1⟩, Bool.true_and]
  · simp only [ucfg]; rw [hB _ (by omega)]; simp [lcfg_nil']

/-- The base at time 8 + 2e on the units ≤ 3. -/
theorem baseL (e : Int) (he : e = 0 ∨ e = 1) (q : Pt) (hq : unitOf q ≤ 3) : Xb (8 + 2 * e) q = ucfg (BL e) q := by
  have hk := baseLitCheck_ok
  simp only [baseLitCheck, Bool.and_eq_true] at hk
  obtain ⟨⟨⟨⟨⟨i0, i1⟩, -⟩, h0⟩, h1⟩, -⟩ := hk
  have hlow : ∀ e', ∀ u, u < -4 → BL e' u = [] := by
    intro e' u hu; simp only [BL]; rw [if_pos (by omega), capLU_nil' hu]
  rcases he with rfl | rfl
  · rw [show (8 : Int) + 2 * 0 = 8 from rfl, Xb_frame, show ((8 + 7 : Int) % 26).toNat = 15 from rfl,
      eqOn_spec_le (by decide) (by decide) h0 (q + frame) (by rw [unitOf_frame]; omega), bcfg_ofList _ i0, bL0,
      lcfg_map_add, lcfg_piece _ (BL_unit 0)]
    exact ucfg_low _ (-4) (hlow 0) 8 q (by push_cast; omega)
  · rw [show (8 : Int) + 2 * 1 = 10 from rfl, Xb_frame, show ((10 + 7 : Int) % 26).toNat = 17 from rfl,
      eqOn_spec_le (by decide) (by decide) h1 (q + frame) (by rw [unitOf_frame]; omega), bcfg_ofList _ i1, bL1,
      lcfg_map_add, lcfg_piece _ (BL_unit 1)]
    exact ucfg_low _ (-4) (hlow 1) 8 q (by push_cast; omega)

/-- The base at time 8 on the units ≥ 3. -/
theorem baseR (q : Pt) (hq : 3 ≤ unitOf q) : Xb 8 q = ucfg BR q := by
  have hk := baseLitCheck_ok
  simp only [baseLitCheck, Bool.and_eq_true] at hk
  obtain ⟨⟨⟨⟨⟨-, -⟩, i2⟩, -⟩, -⟩, h2⟩ := hk
  rw [Xb_frame, show ((8 + 7 : Int) % 26).toNat = 15 from rfl,
    eqOn_spec_ge (by decide) (by decide) h2 (q + frame) (by rw [unitOf_frame]; omega), bcfg_ofList _ i2, bR,
    lcfg_map_add, lcfg_piece _ BR_unit]
  refine ucfg_high _ 3 7 (fun u hu => ?_) q hq
  simp only [BR]; rw [if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega),
    capRU_nil' (by push_cast at hu; omega)]

theorem ucfg_shift (B : Int → List Pt) (i : Int) (p : Pt) :
    ucfg B (shiftPt (-i) p) = lcfg (B (unitOf p - i)) (shiftPt (-unitOf p) p) := by
  simp only [ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  rw [show unitOf p + -i = unitOf p - i by omega, show -(unitOf p - i) + -i = -unitOf p by omega]

/-- The letters at the end of the transient: the rake at N − 1, wire B where N − u is odd. -/
theorem LW_entry (N : Nat) (h6 : 6 ≤ N) (u : Int) (h0 : 0 ≤ u) (h1 : u < N) :
    LW N (mmax N) u = if u = (N : Int) - 1 then 15 else if ((N : Int) - u) % 2 = 1 then 7 else 11 := by
  obtain ⟨k, hk | hk⟩ : ∃ k, N = 2 * k ∨ N = 2 * k + 1 := ⟨N / 2, by omega⟩
  all_goals subst hk; unfold LW mmax; repeat' split
  all_goals omega

set_option maxHeartbeats 4000000 in
/-- **The end of the transient**: the word `FL N (mmax N)` (the rake at unit N − 1) is the surgery's state
`Y_{N−6}` at time 2(N − 6) + 8. -/
theorem FL_entry (N : Nat) (h6 : 6 ≤ N) :
    ucfg (FL N (mmax N)) = surg Xb 3 (N - 6) (chart (N - 6)) (2 * ((N - 6 : Nat) : Int) + 8) := by
  funext p
  simp only [surg]
  have hc0 : 0 ≤ cidx 3 (N - 6) p ∧ cidx 3 (N - 6) p ≤ ((N - 6 : Nat) : Int) := by simp only [cidx]; omega
  rw [chart_entry _ _ hc0.1 hc0.2]
  have hu : ucfg (FL N (mmax N)) p = lcfg (FL N (mmax N) (unitOf p)) (shiftPt (-unitOf p) p) := rfl
  have hj : ((N - 6 : Nat) : Int) = (N : Int) - 6 := by omega
  rw [hu]
  by_cases hA : unitOf p ≤ 3
  · have hi : cidx 3 (N - 6) p = 0 := by simp only [cidx]; omega
    rw [hi, baseL _ (by omega) _ (by rw [unitOf_shiftPt]; omega), ucfg_shift]
    congr 1
    rw [show unitOf p - 0 = unitOf p by omega, hj]
    simp only [FL, BL]
    by_cases h0 : unitOf p < 0
    · simp only [if_pos h0]
    · simp only [if_neg h0, if_pos (show unitOf p < (N : Int) by omega), if_pos hA]
      congr 1
      rw [LW_entry N h6 _ (by omega) (by omega)]
      repeat' split
      all_goals omega
  by_cases hC : 3 + ((N - 6 : Nat) : Int) ≤ unitOf p
  · have hi : cidx 3 (N - 6) p = ((N - 6 : Nat) : Int) := by simp only [cidx]; omega
    rw [hi, show (8 : Int) + 2 * ((((N - 6 : Nat) : Int) - ((N - 6 : Nat) : Int)) % 2) = 8 by omega,
      baseR _ (by rw [unitOf_shiftPt]; omega), ucfg_shift]
    congr 1
    rw [hj]
    simp only [FL, BR]
    simp only [if_neg (show ¬ unitOf p < 0 by omega), if_neg (show ¬ unitOf p - ((N : Int) - 6) < 3 by omega)]
    by_cases h1 : unitOf p < N
    · simp only [if_pos h1]
      by_cases e3 : unitOf p - ((N : Int) - 6) = 3
      · simp only [if_pos e3]; congr 1; rw [LW_entry N h6 _ (by omega) h1]; repeat' split
        all_goals omega
      · simp only [if_neg e3]
        by_cases e4 : unitOf p - ((N : Int) - 6) = 4
        · simp only [if_pos e4]; congr 1; rw [LW_entry N h6 _ (by omega) h1]; repeat' split
          all_goals omega
        · simp only [if_neg e4, if_pos (show unitOf p - ((N : Int) - 6) = 5 by omega)]
          congr 1; rw [LW_entry N h6 _ (by omega) h1]; repeat' split
          all_goals omega
    · simp only [if_neg h1, if_neg (show ¬ unitOf p - ((N : Int) - 6) = 3 by omega),
        if_neg (show ¬ unitOf p - ((N : Int) - 6) = 4 by omega), if_neg (show ¬ unitOf p - ((N : Int) - 6) = 5 by omega)]
      congr 1; omega
  · have hi : cidx 3 (N - 6) p = unitOf p - 3 := by simp only [cidx]; omega
    rw [hi, baseL _ (by omega) _ (by rw [unitOf_shiftPt]; omega), ucfg_shift]
    congr 1
    rw [show unitOf p - (unitOf p - 3) = 3 by omega, hj]
    simp only [FL, BL]
    simp only [if_neg (show ¬ unitOf p < 0 by omega), if_pos (show unitOf p < (N : Int) by omega),
      if_neg (show ¬ (3 : Int) < 0 by omega), if_pos (show (3 : Int) ≤ 3 by omega)]
    congr 1
    rw [LW_entry N h6 _ (by omega) (by omega)]
    repeat' split
    all_goals omega

/-! ### The lit clock enters the cycle -/

/-- The generation at which the rake reaches unit N − 1: N − 2 for even N, N − 1 for odd N. -/
theorem two_mmax (N : Nat) (h6 : 6 ≤ N) : 2 * mmax N = if N % 2 = 0 then N - 2 else N - 1 := by
  unfold mmax; split <;> omega

/-- **The lit clock enters the cycle of `clockOf N`**: for every N ≥ 6, one cell lights the clock of N units, and
at generation 2 · mmax N (N − 2 for even N, N − 1 for odd N) it is the state of `clockOf N` = `clockY (N − 6)`
at generation 2(N − 6) + 3. -/
theorem lit_enters (N : Nat) (h6 : 6 ≤ N) :
    run (lcfg (litList N)) (2 * mmax N) = run (clockOf N) (2 * (N - 6) + 3) := by
  rw [lit_word N h6 _ (Nat.le_refl _), FL_entry N h6, clockOf, if_neg (show ¬ N ≤ 5 by omega),
    clockY_run (N - 6) _ (by omega)]
  congr 1
  push_cast
  omega

theorem run_mul_period (C : Config) (P : Nat) (h : run C P = C) : ∀ n, run C (P * n) = C
  | 0 => rfl
  | n + 1 => by rw [Nat.mul_succ, run_add, run_mul_period C P h n, h]

/-- Every state of an orbit of exact period P has exact period P. -/
theorem exact_period_run (C : Config) (P : Nat) (h1 : run C P = C) (h2 : ∀ k, 0 < k → k < P → run C k ≠ C)
    (t : Nat) : run (run C t) P = run C t ∧ ∀ k, 0 < k → k < P → run (run C t) k ≠ run C t := by
  rcases Nat.eq_zero_or_pos P with hP | hP
  · subst hP; exact ⟨rfl, fun k h1 h2 => absurd h2 (by omega)⟩
  refine ⟨by rw [← run_add, Nat.add_comm, run_add, h1], fun k hk0 hk1 e => h2 k hk0 hk1 ?_⟩
  let r := P - t % P
  have hr : t + r = P * (t / P + 1) := by
    have := Nat.div_add_mod t P; have := Nat.mod_lt t hP
    simp only [r, Nat.mul_succ]; omega
  have e2 : run (run (run C t) k) r = run (run C t) r := by rw [e]
  have : run C (t + r) = C := by rw [hr, run_mul_period C P h1]
  rw [← run_add, ← run_add, ← run_add, this, show t + (k + r) = (t + r) + k by omega, run_add, this] at e2
  exact e2

/-- The generation from which the lit clock of N units is on the cycle: max(N − 2, 0) for N ≤ 5, 2 · mmax N
(N − 2 for even N, N − 1 for odd N) for N ≥ 6. -/
def litEntry (N : Nat) : Nat := if N ≤ 5 then N - 2 else 2 * mmax N

/-- **The clock from a single cell, for every N ≥ 1**: the lit clock of N units is, from generation `litEntry N`
on, a state of the cycle of `clockOf N`, and so an oscillator of exact period 4N + 2. -/
theorem lit_clock (N : Nat) (hN : 1 ≤ N) (g : Nat) (hg : litEntry N ≤ g) :
    (∃ s, run (lcfg (litList N)) g = run (clockOf N) s) ∧
    run (run (lcfg (litList N)) g) (4 * N + 2) = run (lcfg (litList N)) g ∧
    ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) g) k ≠ run (lcfg (litList N)) g := by
  have hs : ∃ s, run (lcfg (litList N)) g = run (clockOf N) s := by
    have e : g = litEntry N + (g - litEntry N) := by omega
    by_cases h5 : N ≤ 5
    · refine ⟨g - litEntry N, ?_⟩
      rw [e, run_add, Nat.add_sub_cancel_left]
      simp only [litEntry, clockOf, if_pos h5]
    · refine ⟨2 * (N - 6) + 3 + (g - litEntry N), ?_⟩
      rw [e, run_add, Nat.add_sub_cancel_left, run_add (clockOf N)]
      simp only [litEntry, if_neg h5]
      rw [lit_enters N (by omega)]
  obtain ⟨s, hs'⟩ := hs
  obtain ⟨p1, p2, -⟩ := clockOf_period N hN
  rw [hs']
  exact ⟨⟨s, rfl⟩, exact_period_run _ _ p1 p2 s⟩

end Gump.Clock
