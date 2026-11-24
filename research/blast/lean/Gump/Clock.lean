/-
**A clock of every length** (`research/signals/README.md` section 11, "A clock of period exactly 4N + 2 exists for
every N ≥ 1"; the surgery of `research/signals/prove_clock.py`; reviewed in `research/audit/REVIEW-signals-2.md`
row 1).

`clock_every_length`: for every N ≥ 1 there is a configuration of the whole lattice, lying in the units −4 .. N + 3
(the clock's two caps and the N units of wire between them) and in a bounded tube, that is an oscillator of exact
period 4N + 2. For N ≤ 5 it is the lit clock (capL + N units of wire C + capR + one cell) from generation
max(N − 2, 0) on (`lit_clock_small`, direct kernel runs). For N = 6 + j it is the source's surgery Y_j on the
cycle of the lit clock of six units (`clock_cycle`): unit 3 + i of Y_j(t) shows the base's unit 3 at the base's
time c_i(t), moved i units (`chart`), and the base facts B1 – B5 are kernel-checked runs.

The gluing of j + 1 charts is a theorem (`surg_step`): if neighbouring charts agree on the two units where they
meet (A) and each chart's time advances by one or loops back where the base looks the same (B), the glued
configuration steps to the glued successor. (A) and (B) for every j, i and t are arithmetic facts about `chart`
(`chartA`, `chartB`, proved by `omega`).

Not proved, as in the source: that the one-cell ignition leads into this cycle for N ≥ 6 (measured to N = 400).
-/
import Gump.ClockData
import Gump.Tape

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits

/-! ### Charts glued unit by unit -/

/-- Which chart a point reads: 0 on the units ≤ m, i on unit m + i, j on the units ≥ m + j. -/
def cidx (m : Int) (j : Nat) (p : Pt) : Int := max 0 (min (unitOf p - m) j)

/-- **The surgery**: unit m + i shows chart i, that is X at time c i t, moved i units. -/
def surg (X : Int → Config) (m : Int) (j : Nat) (c : Int → Int → Int) (t : Int) : Config :=
  fun p => X (c (cidx m j p) t) (shiftPt (-cidx m j p) p)

theorem surg_near {X : Int → Config} {m : Int} {j : Nat} {c : Int → Int → Int} {t : Int}
    (hA : ∀ i : Int, 0 ≤ i → i < (j : Int) → ∀ q, m ≤ unitOf q → unitOf q ≤ m + 1 →
      X (c i t) q = X (c (i + 1) t) (shiftPt (-1) q))
    (p q : Pt) (h1 : unitOf p - 1 ≤ unitOf q) (h2 : unitOf q ≤ unitOf p + 1) :
    surg X m j c t q = X (c (cidx m j p) t) (shiftPt (-cidx m j p) q) := by
  simp only [surg]
  have hi : cidx m j q = cidx m j p ∨
      (cidx m j q = cidx m j p + 1 ∧ cidx m j p < j ∧ unitOf q = m + cidx m j p + 1 ∧ 0 ≤ cidx m j p) ∨
      (cidx m j q = cidx m j p - 1 ∧ 0 < cidx m j p ∧ cidx m j p ≤ j ∧ unitOf q = m + cidx m j p - 1) := by
    simp only [cidx]; omega
  rcases hi with e | ⟨e, h3, h4, h5⟩ | ⟨e, h3, h3', h4⟩
  · rw [e]
  · rw [e, hA _ h5 h3 (shiftPt (-cidx m j p) q) (by simp only [unitOf_shiftPt]; omega)
      (by simp only [unitOf_shiftPt]; omega), shiftPt_shiftPt]
    congr 2; omega
  · have := hA (cidx m j p - 1) (by omega) (by omega) (shiftPt (-(cidx m j p - 1)) q)
      (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
    rw [e, this, shiftPt_shiftPt, show cidx m j p - 1 + 1 = cidx m j p by omega]
    congr 2; omega

/-- **One generation of the surgery.** -/
theorem surg_step {X : Int → Config} (hX : ∀ s, step (X s) = X (s + 1)) {m : Int} {j : Nat}
    {c : Int → Int → Int} {t : Int}
    (hA : ∀ i : Int, 0 ≤ i → i < (j : Int) → ∀ q, m ≤ unitOf q → unitOf q ≤ m + 1 →
      X (c i t) q = X (c (i + 1) t) (shiftPt (-1) q))
    (hB : ∀ i : Int, 0 ≤ i → i ≤ (j : Int) → ∀ q, (0 < i → m ≤ unitOf q) → (i < j → unitOf q ≤ m) →
      X (c i t + 1) q = X (c i (t + 1)) q) :
    step (surg X m j c t) = surg X m j c (t + 1) := by
  funext p
  have e1 : step (surg X m j c t) p = step (shiftC (cidx m j p) (X (c (cidx m j p) t))) p :=
    step_eq_of_units (fun q h1 h2 => surg_near hA p q h1 h2)
  have e2 : step (shiftC (cidx m j p) (X (c (cidx m j p) t))) =
      shiftC (cidx m j p) (step (X (c (cidx m j p) t))) := run_shiftC _ _ 1
  rw [e1, e2, hX]
  simp only [shiftC, surg]
  apply hB _ (by simp only [cidx]; omega) (by simp only [cidx]; omega)
  · intro h; simp only [unitOf_shiftPt]; simp only [cidx] at h ⊢; omega
  · intro h; simp only [unitOf_shiftPt]; simp only [cidx] at h ⊢; omega

/-- **The surgery over a window of generations is an orbit.** -/
theorem surg_run {X : Int → Config} (hX : ∀ s, step (X s) = X (s + 1)) {m : Int} {j : Nat}
    {c : Int → Int → Int} {T0 : Int} {P : Nat}
    (hA : ∀ t, T0 ≤ t → t < T0 + P → ∀ i : Int, 0 ≤ i → i < (j : Int) → ∀ q, m ≤ unitOf q → unitOf q ≤ m + 1 →
      X (c i t) q = X (c (i + 1) t) (shiftPt (-1) q))
    (hB : ∀ t, T0 ≤ t → t < T0 + P → ∀ i : Int, 0 ≤ i → i ≤ (j : Int) → ∀ q, (0 < i → m ≤ unitOf q) →
      (i < j → unitOf q ≤ m) → X (c i t + 1) q = X (c i (t + 1)) q) :
    ∀ n : Nat, n ≤ P → run (surg X m j c T0) n = surg X m j c (T0 + n)
  | 0, _ => by
    show surg X m j c T0 = surg X m j c (T0 + ((0 : Nat) : Int))
    congr 1; omega
  | n + 1, h => by
    rw [run, surg_run hX hA hB n (by omega), surg_step hX (hA _ (by omega) (by omega))
      (hB _ (by omega) (by omega))]
    congr 1; push_cast; omega

/-! ### The charts of the clock (base: six units, period 26, cut at unit 3) -/

/-- One period of chart i, from its start −2 + 2i: R-run, the loop at ta = 11 (j − i times), L-run, the loop at
tb = 24 (i times). -/
def first (j : Nat) (i t : Int) : Int :=
  if t ≤ 11 + 2 * i then t - 2 * i
  else if t ≤ 11 + 4 * j - 2 * i then 8 + (t - 11 - 2 * i - 1) % 4
  else if t ≤ 24 + 4 * j - 2 * i then t - 4 * j + 2 * i
  else 21 + (t - 24 - 4 * j + 2 * i - 1) % 4

/-- **Chart i of the clock of 6 + j units**: the base's time shown at unit 3 + i at generation t (three periods
of 26 + 4j generations around the chart's start). -/
def chart (j : Nat) (i t : Int) : Int :=
  if t ≤ -2 + 2 * i then first j i (t + (26 + 4 * j)) - 26
  else if t ≤ -2 + 2 * i + (26 + 4 * j) then first j i t
  else first j i (t - (26 + 4 * j)) + 26

set_option maxHeartbeats 4000000 in
/-- (A): neighbouring charts differ by two generations, in a range where the base checks the strip. -/
theorem chartA (j : Nat) (i t : Int) (h0 : 0 ≤ i) (h1 : i < j) (ht0 : 5 ≤ t) (ht1 : t < 5 + (26 + 4 * j)) :
    (chart j (i + 1) t = chart j i t - 2 ∧ (chart j i t + 5) % 26 ≤ 16) ∨
    (chart j (i + 1) t = chart j i t + 2 ∧ (chart j i t - 8) % 26 ≤ 16) := by
  simp only [chart, first]
  repeat' split
  all_goals omega

set_option maxHeartbeats 4000000 in
/-- (B): a chart's time advances by one, or loops back by three at ta (charts i < j) or at tb (charts i > 0). -/
theorem chartB (j : Nat) (i t : Int) (h0 : 0 ≤ i) (h1 : i ≤ j) (ht0 : 5 ≤ t) (ht1 : t < 5 + (26 + 4 * j)) :
    chart j i (t + 1) = chart j i t + 1 ∨
    (i < j ∧ (chart j i t - 11) % 26 = 0 ∧ chart j i (t + 1) = chart j i t - 3) ∨
    (0 < i ∧ (chart j i t - 24) % 26 = 0 ∧ chart j i (t + 1) = chart j i t - 3) := by
  simp only [chart, first]
  repeat' split
  all_goals omega

theorem chartP (j : Nat) (i : Int) (h0 : 0 ≤ i) (h1 : i ≤ j) :
    chart j i (5 + (26 + 4 * j)) = chart j i 5 + 26 := by
  simp only [chart, first]
  repeat' split
  all_goals omega

theorem chart_zero (j : Nat) : chart j 0 5 = 5 := by
  simp only [chart, first]
  repeat' split
  all_goals omega

set_option maxHeartbeats 4000000 in
theorem chart_zero_ne (j : Nat) (k : Int) (h0 : 0 < k) (h1 : k < 26 + 4 * j) :
    (chart j 0 (5 + k) - 5) % 26 ≠ 0 := by
  simp only [chart, first]
  repeat' split
  all_goals omega

/-! ### The base: the cycle of the clock of six units, checked by the kernel -/

/-- The base's cycle at its time s (period 26; X0 is time −7). -/
def Xb (s : Int) : Config := run (lcfg X0) ((s + 7) % 26).toNat

/-- The translation into the box (units move by 8). -/
def frame : Pt := ⟨16, 16, 16⟩

def unframe : Pt := ⟨-16, -16, -16⟩

theorem frame_even : frame.even := by
  show (16 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

theorem unframe_frame (p : Pt) : p + unframe + frame = p := Tape.Pt.add_add_neg p frame

theorem unitOf_frame (q : Pt) : unitOf (q + frame) = unitOf q + 8 := by
  simp only [unitOf, frame, Pt.add_x]; omega

/-- The base in the box, and the base moved one unit, in the box. -/
def bS : Nat := ofList (X0.map (· + frame))
def bSs : Nat := ofList ((X0.map (shiftPt 1)).map (· + frame))

/-- Check the property P k of the states k, k + 1, …, k + n of the orbit of S. -/
def walk (P : Nat → Nat → Bool) : Nat → Nat → Nat → Bool
  | 0, k, S => P k S
  | n + 1, k, S => P k S && walk P n (k + 1) (bstep S)

theorem walk_spec (P : Nat → Nat → Bool) : ∀ n k S, walk P n k S = true → ∀ i, i ≤ n → P (k + i) (brun S i) = true
  | 0, k, S, h, i, hi => by obtain rfl : i = 0 := by omega
                            exact h
  | n + 1, k, S, h, i, hi => by
    simp only [walk, Bool.and_eq_true] at h
    cases i with
    | zero => exact h.1
    | succ i =>
      rw [← brun_shift, show k + (i + 1) = (k + 1) + i by omega]
      exact walk_spec P n (k + 1) _ h.2 i (by omega)

/-- B5: on units 2 .. 4 (box 10 .. 12) the state at index 12 (time 5 = tR) is seen at no other index of a period. -/
def b5 (R : Nat) : Bool := walk (fun k T => k == 12 || !eqOn (unitMask 10 12) T R) 25 0 bS

/-- Support: every state of the period lies in the units −4 .. 9 (box 4 .. 17). -/
def supp : Bool := walk (fun _ T => eqOn (unitMask (-8) 3) T 0 && eqOn (unitMask 18 23) T 0) 25 0 bS

/-- All base facts. Units m, m + 1 = 3, 4 are box units 11, 12. -/
def baseCheck : Bool :=
  (X0.map (· + frame)).all inBox && ((X0.map (shiftPt 1)).map (· + frame)).all inBox && inCore bS &&
  isOscB bS 26 && coreRun bS 34 && coreRun bSs 34 &&
  agree (unitMask 11 12) 16 (brun bS 2) bSs &&
  agree (unitMask 11 12) 16 (brun bS 15) (brun bSs 17) &&
  eqOn (unitMask (-8) 12) (brun bS 19) (brun bS 15) &&
  eqOn (unitMask 10 23) (brun bS 32) (brun bS 28) &&
  b5 (brun bS 12) && supp

theorem baseCheck_ok : baseCheck = true := by decide +kernel

theorem bc : (X0.map (· + frame)).all inBox = true ∧ ((X0.map (shiftPt 1)).map (· + frame)).all inBox = true ∧
    inCore bS = true ∧ isOscB bS 26 = true ∧ coreRun bS 34 = true ∧ coreRun bSs 34 = true ∧
    agree (unitMask 11 12) 16 (brun bS 2) bSs = true ∧ agree (unitMask 11 12) 16 (brun bS 15) (brun bSs 17) = true ∧
    eqOn (unitMask (-8) 12) (brun bS 19) (brun bS 15) = true ∧ eqOn (unitMask 10 23) (brun bS 32) (brun bS 28) = true ∧
    b5 (brun bS 12) = true ∧ supp = true := by
  have h := baseCheck_ok
  simp only [baseCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩, h8⟩, h9⟩, h10⟩, h11⟩, h12⟩ := h
  exact ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12⟩

/-- The base run, read in the box. -/
theorem frameX (n : Nat) (hn : n ≤ 35) (q : Pt) : run (lcfg X0) n q = bcfg (brun bS n) (q + frame) := by
  have core := coreRun_spec _ _ bc.2.2.2.2.1
  rw [← run_lcfg_map_add X0 frame_even n q, ← bcfg_ofList _ bc.1]
  show run (bcfg bS) n (q + frame) = _
  rw [run_bcfg_of_core (fun j hj => core j (by omega))]

theorem frameXs (n : Nat) (hn : n ≤ 35) (q : Pt) :
    shiftC 1 (run (lcfg X0) n) q = bcfg (brun bSs n) (q + frame) := by
  have core := coreRun_spec _ _ bc.2.2.2.2.2.1
  rw [← run_shiftC, ← lcfg_map_shiftPt, ← run_lcfg_map_add _ frame_even n q, ← bcfg_ofList _ bc.2.1]
  show run (bcfg bSs) n (q + frame) = _
  rw [run_bcfg_of_core (fun j hj => core j (by omega))]

theorem base_period : run (lcfg X0) 26 = lcfg X0 := by
  have := (isOscB_spec bS 26 bc.2.2.1 bc.2.2.2.1).2.1
  funext q
  rw [← run_lcfg_map_add X0 frame_even 26 q, ← bcfg_ofList _ bc.1]
  show run (bcfg bS) 26 (q + frame) = _
  rw [this]
  show bcfg (ofList (X0.map (· + frame))) (q + frame) = _
  rw [bcfg_ofList _ bc.1, lcfg_map_add]

theorem run_mod (n : Nat) : run (lcfg X0) n = run (lcfg X0) (n % 26) := by
  conv => lhs; rw [← Nat.mod_add_div n 26]
  generalize n / 26 = q
  induction q with
  | zero => rfl
  | succ q ih => rw [show n % 26 + 26 * (q + 1) = 26 + (n % 26 + 26 * q) by omega, run_add, base_period, ← ih]

theorem Xb_nat (n : Nat) : Xb (-7 + n) = run (lcfg X0) n := by
  simp only [Xb]; rw [run_mod n]; congr 1; omega

theorem Xb_step (s : Int) : step (Xb s) = Xb (s + 1) := by
  simp only [Xb]
  show run (lcfg X0) (((s + 7) % 26).toNat + 1) = _
  rw [run_mod (((s + 7) % 26).toNat + 1)]
  congr 1; omega

theorem Xb_congr {s s' : Int} (h : (s - s') % 26 = 0) : Xb s = Xb s' := by
  simp only [Xb]; congr 2; omega

theorem Xb_frame (s : Int) (q : Pt) : Xb s q = bcfg (brun bS ((s + 7) % 26).toNat) (q + frame) :=
  frameX _ (by omega) q

/-- B1, for every time in its range modulo the period. -/
theorem B1 (s : Int) (hs : (s + 5) % 26 ≤ 16) (q : Pt) (h1 : 3 ≤ unitOf q) (h2 : unitOf q ≤ 4) :
    Xb s q = Xb (s - 2) (shiftPt (-1) q) := by
  let s0 := -5 + (s + 5) % 26
  rw [Xb_congr (s := s) (s' := s0) (by omega), Xb_congr (s := s - 2) (s' := s0 - 2) (by omega)]
  obtain ⟨n, hn, hn2⟩ : ∃ n : Nat, s0 = -7 + n ∧ 2 ≤ n ∧ n ≤ 18 := ⟨(s0 + 7).toNat, by omega, by omega⟩
  rw [hn, show -7 + (n : Int) - 2 = -7 + ((n - 2 : Nat) : Int) by omega, Xb_nat, Xb_nat]
  show _ = shiftC 1 (run (lcfg X0) (n - 2)) q
  rw [frameX n (by omega), frameXs _ (by omega)]
  have := (agree_spec _ 16 _ _ bc.2.2.2.2.2.2.1 (n - 2) (by omega)).2.2
  rw [← brun_add, show 2 + (n - 2) = n by omega] at this
  exact eqOn_spec (by decide) (by decide) (by decide) this _ (by rw [unitOf_frame]; omega)
    (by rw [unitOf_frame]; omega)

/-- B2, for every time in its range modulo the period. -/
theorem B2 (s : Int) (hs : (s - 8) % 26 ≤ 16) (q : Pt) (h1 : 3 ≤ unitOf q) (h2 : unitOf q ≤ 4) :
    Xb s q = Xb (s + 2) (shiftPt (-1) q) := by
  let s0 := 8 + (s - 8) % 26
  rw [Xb_congr (s := s) (s' := s0) (by omega), Xb_congr (s := s + 2) (s' := s0 + 2) (by omega)]
  obtain ⟨n, hn, hn2⟩ : ∃ n : Nat, s0 = -7 + n ∧ 15 ≤ n ∧ n ≤ 31 := ⟨(s0 + 7).toNat, by omega, by omega⟩
  rw [hn, show -7 + (n : Int) + 2 = -7 + ((n + 2 : Nat) : Int) by omega, Xb_nat, Xb_nat]
  show _ = shiftC 1 (run (lcfg X0) (n + 2)) q
  rw [frameX n (by omega), frameXs _ (by omega)]
  have := (agree_spec _ 16 _ _ bc.2.2.2.2.2.2.2.1 (n - 15) (by omega)).2.2
  rw [← brun_add, ← brun_add, show 15 + (n - 15) = n by omega, show 17 + (n - 15) = n + 2 by omega] at this
  exact eqOn_spec (by decide) (by decide) (by decide) this _ (by rw [unitOf_frame]; omega)
    (by rw [unitOf_frame]; omega)

/-- B3: the loop at ta = 11 on the units ≤ 4. -/
theorem B3 (s : Int) (hs : (s - 11) % 26 = 0) (q : Pt) (h : unitOf q ≤ 4) : Xb (s + 1) q = Xb (s - 3) q := by
  rw [Xb_congr (s := s + 1) (s' := -7 + (19 : Nat)) (by omega), Xb_congr (s := s - 3) (s' := -7 + (15 : Nat)) (by omega),
    Xb_nat, Xb_nat, frameX _ (by decide), frameX _ (by decide)]
  exact eqOn_spec_le (by decide) (by decide) bc.2.2.2.2.2.2.2.2.1 _ (by rw [unitOf_frame]; omega)

/-- B4: the loop at tb = 24 on the units ≥ 2. -/
theorem B4 (s : Int) (hs : (s - 24) % 26 = 0) (q : Pt) (h : 2 ≤ unitOf q) : Xb (s + 1) q = Xb (s - 3) q := by
  rw [Xb_congr (s := s + 1) (s' := -7 + (32 : Nat)) (by omega), Xb_congr (s := s - 3) (s' := -7 + (28 : Nat)) (by omega),
    Xb_nat, Xb_nat, frameX _ (by decide), frameX _ (by decide)]
  exact eqOn_spec_ge (by decide) (by decide) bc.2.2.2.2.2.2.2.2.2.1 _ (by rw [unitOf_frame]; omega)

/-- B5: the strip of units 2 .. 4 looks as at tR = 5 only at tR, modulo the period. -/
theorem B5 (s : Int) (h : ∀ q, 2 ≤ unitOf q → unitOf q ≤ 4 → Xb s q = Xb 5 q) : (s - 5) % 26 = 0 := by
  apply Classical.byContradiction
  intro hne
  have w := walk_spec _ 25 0 bS bc.2.2.2.2.2.2.2.2.2.2.1 ((s + 7) % 26).toNat (by omega)
  simp only [Nat.zero_add, Bool.or_eq_true, beq_iff_eq, Bool.not_eq_true'] at w
  rcases w with w | w
  · omega
  · obtain ⟨p, h1, h2, hp⟩ := neqOn_spec (by decide) (by decide) (by decide) w
    apply hp
    have := h (p + unframe) (by have := unitOf_frame (p + unframe); rw [unframe_frame] at this; omega)
      (by have := unitOf_frame (p + unframe); rw [unframe_frame] at this; omega)
    rw [Xb_frame, Xb_frame, unframe_frame] at this
    exact this

/-- Support of the base: every state lies in the units −4 .. 9 and in the box (moved back). -/
theorem base_supp (s : Int) (q : Pt) (h : Xb s q = true) :
    -4 ≤ unitOf q ∧ unitOf q ≤ 9 ∧ inBox (q + frame) = true := by
  rw [Xb_frame] at h
  have w := walk_spec _ 25 0 bS bc.2.2.2.2.2.2.2.2.2.2.2 ((s + 7) % 26).toNat (by omega)
  simp only [Bool.and_eq_true] at w
  have hb : inBox (q + frame) = true := by
    simp only [bcfg, Bool.and_eq_true] at h; exact h.1
  refine ⟨?_, ?_, hb⟩
  · apply Classical.byContradiction; intro hu
    have := eqOn_spec_le (by decide) (by decide) w.1 (q + frame) (by rw [unitOf_frame]; omega)
    rw [h] at this; simp [bcfg] at this
  · apply Classical.byContradiction; intro hu
    have := eqOn_spec_ge (by decide) (by decide) w.2 (q + frame) (by rw [unitOf_frame]; omega)
    rw [h] at this; simp [bcfg] at this

/-! ### The clock of 6 + j units -/

/-- **The cycle of the clock of 6 + j units**, at the generation where chart 0 shows tR. -/
def clockY (j : Nat) : Config := surg Xb 3 j (chart j) 5

theorem hA_clock (j : Nat) : ∀ t, 5 ≤ t → t < 5 + ((26 + 4 * j : Nat) : Int) → ∀ i : Int, 0 ≤ i → i < (j : Int) → ∀ q,
    3 ≤ unitOf q → unitOf q ≤ 3 + 1 → Xb (chart j i t) q = Xb (chart j (i + 1) t) (shiftPt (-1) q) := by
  intro t h0 h1 i hi0 hi1 q hq1 hq2
  rcases chartA j i t hi0 (by omega) h0 (by push_cast at h1; omega) with ⟨e, r⟩ | ⟨e, r⟩
  · rw [e]; exact B1 _ r q hq1 (by omega)
  · rw [e]; exact B2 _ r q hq1 (by omega)

theorem hB_clock (j : Nat) : ∀ t, 5 ≤ t → t < 5 + ((26 + 4 * j : Nat) : Int) → ∀ i : Int, 0 ≤ i → i ≤ (j : Int) → ∀ q,
    (0 < i → 3 ≤ unitOf q) → (i < j → unitOf q ≤ 3) → Xb (chart j i t + 1) q = Xb (chart j i (t + 1)) q := by
  intro t h0 h1 i hi0 hi1 q hq1 hq2
  rcases chartB j i t hi0 (by omega) h0 (by push_cast at h1; omega) with e | ⟨hi, r, e⟩ | ⟨hi, r, e⟩
  · rw [e]
  · rw [e, show chart j i t + 1 = (chart j i t) + 1 from rfl, B3 _ r q (by have := hq2 hi; omega)]
  · rw [e, B4 _ r q (by have := hq1 hi; omega)]

theorem clockY_run (j : Nat) : ∀ n : Nat, n ≤ 26 + 4 * j → run (clockY j) n = surg Xb 3 j (chart j) (5 + n) :=
  surg_run Xb_step (hA_clock j) (hB_clock j)

theorem clockY_strip (j : Nat) (t : Int) (ht0 : 5 ≤ t) (ht1 : t < 5 + (26 + 4 * j)) (q : Pt) (h1 : 2 ≤ unitOf q)
    (h2 : unitOf q ≤ 4) : surg Xb 3 j (chart j) t q = Xb (chart j 0 t) q := by
  simp only [surg]
  by_cases hj : j = 0
  · subst hj
    have : cidx 3 0 q = 0 := by simp only [cidx]; omega
    rw [this, show -(0 : Int) = 0 from rfl, shiftPt_zero]
  · by_cases hu : unitOf q ≤ 3
    · have : cidx 3 j q = 0 := by simp only [cidx]; omega
      rw [this, show -(0 : Int) = 0 from rfl, shiftPt_zero]
    · have : cidx 3 j q = 1 := by simp only [cidx]; omega
      rw [this]
      have := hA_clock j t ht0 (by push_cast; omega) 0 (by decide) (by omega) q (by omega) (by omega)
      rw [this, show (0 : Int) + 1 = 1 from rfl]

/-- **The clock of 6 + j units has exact period 4(6 + j) + 2**, and lies in the units −4 .. 9 + j. -/
theorem clock_cycle (j : Nat) :
    run (clockY j) (4 * (6 + j) + 2) = clockY j ∧
    (∀ k, 0 < k → k < 4 * (6 + j) + 2 → run (clockY j) k ≠ clockY j) ∧
    ∀ q, clockY j q = true → -4 ≤ unitOf q ∧ unitOf q ≤ (6 + j : Nat) + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧
      -64 ≤ q.x + q.z ∧ q.x + q.z < 64 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [show 4 * (6 + j) + 2 = 26 + 4 * j by omega, clockY_run j _ (Nat.le_refl _)]
    funext q
    simp only [clockY, surg]
    rw [show (5 : Int) + ((26 + 4 * j : Nat) : Int) = 5 + (26 + 4 * j) by omega,
      chartP j _ (by simp only [cidx]; omega) (by simp only [cidx]; omega)]
    rw [Xb_congr (s := chart j (cidx 3 j q) 5 + 26) (s' := chart j (cidx 3 j q) 5) (by omega)]
  · intro k hk0 hk1 e
    rw [clockY_run j k (by omega)] at e
    apply chart_zero_ne j k (by omega) (by omega)
    apply B5
    intro q h1 h2
    have a := clockY_strip j (5 + k) (by omega) (by omega) q h1 h2
    have b := clockY_strip j 5 (by omega) (by omega) q h1 h2
    rw [e] at a
    simp only [clockY] at a
    rw [← a, b, chart_zero]
  · intro q hq
    simp only [clockY, surg] at hq
    obtain ⟨s1, s2, s3⟩ := base_supp _ _ hq
    simp only [unitOf_shiftPt] at s1 s2
    simp only [inBox, decide_eq_true_eq] at s3
    simp only [shiftPt, Pt.add_x, Pt.add_y, Pt.add_z, frame] at s3
    have c1 : 0 ≤ cidx 3 j q ∧ cidx 3 j q ≤ j := by simp only [cidx]; omega
    refine ⟨by omega, by push_cast; omega, by omega, by omega, by omega, by omega⟩

/-! ### Short clocks, directly -/

/-- The clock of N units lit by one cell: capL, N units of wire C, capR moved N units, and the cell (1,0,4) of
unit N / 2 (`objects/clock-C.json`). -/
def litList (N : Nat) : List Pt :=
  capL ++ wordList 0 (List.replicate N .C) ++ capR.map (shiftPt N) ++ [shiftPt (N / 2 : Nat) ⟨1, 0, 4⟩]

/-- From generation μ the lit clock is an oscillator of exact period P, and lies in the units −4 .. N + 3. -/
def litCheck (N μ P : Nat) : Bool :=
  ((litList N).map (· + frame)).all inBox &&
    match advance (ofList ((litList N).map (· + frame))) μ with
    | some T => inCore T && isOscB T P && eqOn (unitMask (-8) 3) T 0 && eqOn (unitMask (N + 12) 23) T 0
    | none => false

theorem litCheck_ok : litCheck 1 0 6 = true ∧ litCheck 2 0 10 = true ∧ litCheck 3 1 14 = true ∧
    litCheck 4 2 18 = true ∧ litCheck 5 3 22 = true := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide +kernel

/-- An oscillator moved by an even vector is an oscillator of the same exact period. -/
theorem osc_translate (c : Config) {v : Pt} (hv : v.even) (P : Nat) (h1 : run c P = c)
    (h2 : ∀ k, 0 < k → k < P → run c k ≠ c) :
    run (fun q => c (q + v)) P = (fun q => c (q + v)) ∧
    ∀ k, 0 < k → k < P → run (fun q => c (q + v)) k ≠ (fun q => c (q + v)) := by
  rw [run_translate c hv]
  refine ⟨by rw [h1], fun k hk0 hk1 e => h2 k hk0 hk1 ?_⟩
  rw [run_translate c hv] at e
  funext p
  have := congrFun e (p + ⟨-v.x, -v.y, -v.z⟩)
  simp only [Tape.Pt.add_add_neg] at this
  exact this

theorem lit_spec (N μ P : Nat) (hN : N ≤ 11) (h : litCheck N μ P = true) :
    run (run (lcfg (litList N)) μ) P = run (lcfg (litList N)) μ ∧
    (∀ k, 0 < k → k < P → run (run (lcfg (litList N)) μ) k ≠ run (lcfg (litList N)) μ) ∧
    ∀ q, run (lcfg (litList N)) μ q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧
      -64 ≤ q.x + q.z ∧ q.x + q.z < 64 := by
  simp only [litCheck, Bool.and_eq_true] at h
  obtain ⟨hb, h⟩ := h
  split at h
  · rename_i T hT
    simp only [Bool.and_eq_true] at h
    obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h
    obtain ⟨a1, a2⟩ := advance_spec μ _ T hT
    have hμ : run (lcfg ((litList N).map (· + frame))) μ = bcfg T := by
      rw [← bcfg_ofList _ hb, run_bcfg_of_core a1, a2]
    have ht : run (lcfg (litList N)) μ = fun q => bcfg T (q + frame) := by
      funext q; rw [← run_lcfg_map_add _ frame_even μ q, hμ]
    obtain ⟨o1, o2, o3⟩ := isOscB_spec T P h1 h2
    obtain ⟨t1, t2⟩ := osc_translate (bcfg T) frame_even P o2 o3
    rw [ht]
    refine ⟨t1, t2, fun q hq' => ?_⟩
    have hq : bcfg T (q + frame) = true := hq'
    have hbx : inBox (q + frame) = true := by simp only [bcfg, Bool.and_eq_true] at hq; exact hq.1
    simp only [inBox, decide_eq_true_eq] at hbx
    simp only [Pt.add_x, Pt.add_y, Pt.add_z, frame] at hbx
    refine ⟨?_, ?_, by omega, by omega, by omega, by omega⟩
    · apply Classical.byContradiction; intro hu
      have := eqOn_spec_le (by decide) (by decide) h3 (q + frame) (by rw [unitOf_frame]; omega)
      rw [hq] at this; simp [bcfg] at this
    · apply Classical.byContradiction; intro hu
      have := eqOn_spec_ge (by omega) (by omega) h4 (q + frame) (by rw [unitOf_frame]; omega)
      rw [hq] at this; simp [bcfg] at this
  · simp at h

/-- **The lit clocks of 1 .. 5 units**: from generation max(N − 2, 0) on, an oscillator of exact period 4N + 2. -/
theorem lit_clock_small (N : Nat) (h1 : 1 ≤ N) (h5 : N ≤ 5) :
    run (run (lcfg (litList N)) (N - 2)) (4 * N + 2) = run (lcfg (litList N)) (N - 2) ∧
    ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) (N - 2)) k ≠ run (lcfg (litList N)) (N - 2) := by
  obtain ⟨l1, l2, l3, l4, l5⟩ := litCheck_ok
  rcases (show N = 1 ∨ N = 2 ∨ N = 3 ∨ N = 4 ∨ N = 5 by omega) with rfl | rfl | rfl | rfl | rfl
  · exact ⟨(lit_spec _ _ _ (by decide) l1).1, (lit_spec _ _ _ (by decide) l1).2.1⟩
  · exact ⟨(lit_spec _ _ _ (by decide) l2).1, (lit_spec _ _ _ (by decide) l2).2.1⟩
  · exact ⟨(lit_spec _ _ _ (by decide) l3).1, (lit_spec _ _ _ (by decide) l3).2.1⟩
  · exact ⟨(lit_spec _ _ _ (by decide) l4).1, (lit_spec _ _ _ (by decide) l4).2.1⟩
  · exact ⟨(lit_spec _ _ _ (by decide) l5).1, (lit_spec _ _ _ (by decide) l5).2.1⟩

/-- **A clock of every length.** For every N ≥ 1 there is an oscillator of exact period 4N + 2 lying in the
units −4 .. N + 3 of the wire (and in a bounded tube around it). -/
theorem clock_every_length (N : Nat) (hN : 1 ≤ N) :
    ∃ c : Config, run c (4 * N + 2) = c ∧ (∀ k, 0 < k → k < 4 * N + 2 → run c k ≠ c) ∧
      ∀ q, c q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧
        -64 ≤ q.x + q.z ∧ q.x + q.z < 64 := by
  by_cases h6 : 6 ≤ N
  · obtain ⟨j, rfl⟩ : ∃ j, N = 6 + j := ⟨N - 6, by omega⟩
    exact ⟨clockY j, clock_cycle j⟩
  · obtain ⟨l1, l2, l3, l4, l5⟩ := litCheck_ok
    rcases (show N = 1 ∨ N = 2 ∨ N = 3 ∨ N = 4 ∨ N = 5 by omega) with rfl | rfl | rfl | rfl | rfl
    · exact ⟨_, lit_spec _ _ _ (by decide) l1⟩
    · exact ⟨_, lit_spec _ _ _ (by decide) l2⟩
    · exact ⟨_, lit_spec _ _ _ (by decide) l3⟩
    · exact ⟨_, lit_spec _ _ _ (by decide) l4⟩
    · exact ⟨_, lit_spec _ _ _ (by decide) l5⟩

end Gump.Clock

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits

/-- **The clock of N units, named**: for N ≤ 5 the lit clock (capL, N units of wire C, capR, the cell (1,0,4) of
unit N / 2) at generation max(N − 2, 0); for N = 6 + j the surgery's cycle `clockY j`, the cycle of the lit clock of
six units with j units of wire inserted at unit 3. (That `clockY j` is a state of the lit clock of 6 + j units is
not proved here.) -/
def clockOf (N : Nat) : Config := if N ≤ 5 then run (lcfg (litList N)) (N - 2) else clockY (N - 6)

/-- **The named clock of every length** has exact period 4N + 2 (no smaller period) and lies in the units
−4 .. N + 3 and a bounded tube. This is the form of `clock_every_length` that names its object. -/
theorem clockOf_period (N : Nat) (hN : 1 ≤ N) :
    run (clockOf N) (4 * N + 2) = clockOf N ∧ (∀ k, 0 < k → k < 4 * N + 2 → run (clockOf N) k ≠ clockOf N) ∧
      ∀ q, clockOf N q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧
        -64 ≤ q.x + q.z ∧ q.x + q.z < 64 := by
  unfold clockOf
  split
  · rename_i h5
    obtain ⟨l1, l2, l3, l4, l5⟩ := litCheck_ok
    rcases (show N = 1 ∨ N = 2 ∨ N = 3 ∨ N = 4 ∨ N = 5 by omega) with rfl | rfl | rfl | rfl | rfl
    · exact lit_spec _ _ _ (by decide) l1
    · exact lit_spec _ _ _ (by decide) l2
    · exact lit_spec _ _ _ (by decide) l3
    · exact lit_spec _ _ _ (by decide) l4
    · exact lit_spec _ _ _ (by decide) l5
  · rename_i h5
    obtain ⟨j, rfl⟩ : ∃ j, N = 6 + j := ⟨N - 6, by omega⟩
    rw [show 6 + j - 6 = j by omega]
    exact clock_cycle j

end Gump.Clock

namespace Gump.Clock
open Gump Gump.Tape Gump.Bits

/-- The lit clock of six units, run 41 generations by the kernel, is the base state X0. -/
def baseIsLit : Bool :=
  ((litList 6).map (· + frame)).all inBox &&
    match advance (ofList ((litList 6).map (· + frame))) 41 with
    | some T => T == ofList (X0.map (· + frame))
    | none => false

theorem baseIsLit_ok : baseIsLit = true := by decide +kernel

/-- **The base of the surgery is the lit clock**: X0 is the state of the lit clock of six units at generation 41,
so `clockY 0 = clockOf 6` is the lit clock's state at generation 53. -/
theorem X0_lit : run (lcfg (litList 6)) 41 = lcfg X0 := by
  have h := baseIsLit_ok
  simp only [baseIsLit, Bool.and_eq_true] at h
  obtain ⟨hb, h⟩ := h
  split at h
  · rename_i T hT
    obtain ⟨a1, a2⟩ := advance_spec 41 _ T hT
    have hT' : T = ofList (X0.map (· + frame)) := eq_of_beq h
    funext q
    rw [← run_lcfg_map_add _ frame_even 41 q, ← bcfg_ofList _ hb, run_bcfg_of_core a1, ← a2, hT',
      bcfg_ofList _ (by have := bc.1; exact this), lcfg_map_add]
  · simp at h

theorem clockY_zero_lit : clockY 0 = run (lcfg (litList 6)) 53 := by
  funext q
  simp only [clockY, surg]
  have hc : cidx 3 0 q = 0 := by simp only [cidx]; omega
  rw [hc, show -(0 : Int) = 0 from rfl, shiftPt_zero, chart_zero, Xb, show 53 = 41 + 12 from rfl, run_add, X0_lit]
  rfl

end Gump.Clock
