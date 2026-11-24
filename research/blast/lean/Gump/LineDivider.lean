/-
**The divider for every N ≥ 8** (`research/signals/README.md` section 21b, "Period exactly 8 from generation 2N − 3
for every N ≥ 8"; the base facts of `research/signals/prove_divider.py`). The divider of N units
(`objects/divider-C8.json`) is line-C(N) and the oscillator `osc` moved N units (units N − 4 .. N − 2, off the wire's
tube): a finite configuration of the whole lattice. `divider_period`: for every N ≥ 8 its state at generation
2N − 3 returns after 8 generations and after no fewer, and the state at 2N − 4 does not return after 8.

The proof is `Line.lean`'s induction (the source says so too), with the oscillator carried in the right chart: `S N m`
says period 8 from 2N − 3, not period 4 there at every later generation (seen right of the seam), not periodic from
2N − 4 (seen left of it), the window at the seam, and the left end unchanged at generation 2. The base S 14 3 and
the cases N = 8 .. 13 are kernel runs on the bit-parallel stepper (`decide +kernel`); `tape_divider.py` checks the
same periods on `reference/oracle.py` for N = 8 .. 16.
-/
import Gump.Line
import Gump.LineDividerData

namespace Gump.Divider
open Gump Gump.Tape Gump.Bits

/-- The cells of the divider of N units: line-C(N) and the oscillator moved N units. -/
def divList (N : Nat) : List Pt := Line.lineList N ++ osc.map (shiftPt N)

/-- **The divider of N units**, a finite configuration of the whole lattice. -/
def divC (N : Nat) : Config := lcfg (divList N)

theorem osc_unit : ∀ q ∈ osc, -4 ≤ unitOf q ∧ unitOf q ≤ -2 := by decide

theorem divC_eq (N : Nat) (p : Pt) : divC N p = (Line.lineC N p || lcfg osc (shiftPt (-N) p)) := by
  simp only [divC, divList, Line.lineC, lcfg_append, lcfg_map_shiftPt, shiftC]

theorem osc_off {N : Nat} {p : Pt} (h : unitOf p < (N : Int) - 4) : lcfg osc (shiftPt (-N) p) = false := by
  cases e : lcfg osc (shiftPt (-N) p)
  · rfl
  · have := osc_unit _ ((lcfg_iff _ _).mp e); simp only [unitOf_shiftPt] at this; omega

/-- The orbit of the divider. -/
def X (N t : Nat) : Config := run (divC N) t

/-- The orbit delayed by two generations (and, before that, the orbit itself). -/
def L (N t : Nat) : Config := if 2 ≤ t then X N (t - 2) else X N t

/-- The statement of the induction, with the seam at unit m. -/
structure S (N : Nat) (m : Int) : Prop where
  side : 1 ≤ m ∧ m + 7 ≤ N
  per : ∀ t, 2 * N - 3 ≤ t → X N (t + 8) = X N t
  wit4 : ∀ t, 2 * N - 3 ≤ t → ∃ p, m + 1 ≤ unitOf p ∧ X N (t + 4) p ≠ X N t p
  wit7 : ∃ p, unitOf p ≤ m + 1 ∧ X N (2 * N + 4) p ≠ X N (2 * N - 4) p
  win : ∀ t q, m - 1 ≤ unitOf q → unitOf q ≤ m → X N t q = L N t (shiftPt 1 q)
  rest : ∀ p, unitOf p ≤ m + 1 → X N 2 p = X N 0 p

theorem shift_X (N t : Nat) : shiftC 1 (X N t) = run (shiftC 1 (divC N)) t := (run_shiftC 1 _ t).symm

/-- **The induction step.** -/
theorem S_succ {N : Nat} {m : Int} (h : S N m) :
    S (N + 1) (m + 1) ∧ ∀ t, X (N + 1) t = glue m (L N t) (shiftC 1 (X N t)) := by
  obtain ⟨⟨hm1, hm2⟩, per, wit4, wit7, win, rest⟩ := h
  have hX : ∀ t p, unitOf p ≤ m → step (L N t) p = L N (t + 1) p := by
    intro t p hp
    simp only [L]
    by_cases h2 : 2 ≤ t
    · simp only [h2, show 2 ≤ t + 1 by omega, ite_true]
      rw [show t + 1 - 2 = (t - 2) + 1 by omega]
      rfl
    · by_cases h1 : t = 1
      · subst h1
        simp only [show ¬ (2 ≤ 1) by decide, show 2 ≤ 1 + 1 by decide, ite_true, ite_false]
        exact rest p (by omega)
      · obtain rfl : t = 0 := by omega
        simp only [show ¬ (2 ≤ 0) by decide, show ¬ (2 ≤ 0 + 1) by decide, ite_false]
        rfl
  have hZ : ∀ t p, m + 1 ≤ unitOf p → step (shiftC 1 (X N t)) p = shiftC 1 (X N (t + 1)) p := by
    intro t p _
    rw [shift_X, shift_X]
    rfl
  have hXZ : ∀ t p, m ≤ unitOf p → unitOf p ≤ m + 1 → L N t p = shiftC 1 (X N t) p := by
    intro t p h1 h2
    simp only [shiftC]
    rw [win t _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
      shiftPt_shiftPt_neg]
  have h0 : glue m (L N 0) (shiftC 1 (X N 0)) = divC (N + 1) := by
    funext p
    simp only [glue, L, X, show ¬ (2 ≤ 0) by decide, ite_false, run, shiftC]
    simp only [divC_eq]
    split
    · rename_i hp
      rw [osc_off (by omega), osc_off (by push_cast; omega)]
      by_cases hu : unitOf p < 0
      · rw [Line.lineC_left hu, Line.lineC_left hu]
      · rw [Line.lineC_mid (by omega) (by omega), Line.lineC_mid (by omega) (by push_cast; omega)]
    · rename_i hp
      rw [shiftPt_shiftPt, show -(N : Int) + -1 = -((N + 1 : Nat) : Int) by push_cast; omega]
      congr 1
      by_cases hu : unitOf p - 1 < N
      · rw [Line.lineC_mid (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
          Line.lineC_mid (by omega) (by push_cast; omega)]
        simp only [tape, unitOf_shiftPt, shiftPt_shiftPt]
        congr 2
        omega
      · rw [Line.lineC_right (by simp only [unitOf_shiftPt]; omega), Line.lineC_right (by push_cast; omega),
          shiftPt_shiftPt]
        congr 2
        push_cast; omega
  have hY : ∀ t, X (N + 1) t = glue m (L N t) (shiftC 1 (X N t)) := by
    intro t
    have := glue_run m (L N) (fun t => shiftC 1 (X N t)) hX hZ hXZ t
    rw [h0] at this
    exact this
  have Ya : ∀ t p, unitOf p ≤ m + 1 → X (N + 1) t p = L N t p := by
    intro t p hp
    rw [hY t]
    simp only [glue]
    split
    · rfl
    · exact (hXZ t p (by omega) hp).symm
  have Yb : ∀ t p, m ≤ unitOf p → X (N + 1) t p = X N t (shiftPt (-1) p) := by
    intro t p hp
    rw [hY t]
    simp only [glue]
    split
    · exact hXZ t p hp (by omega)
    · rfl
  have LX : ∀ t p, 2 ≤ t → L N t p = X N (t - 2) p := by
    intro t p ht; simp [L, ht]
  refine ⟨⟨⟨by omega, by push_cast; omega⟩, ?_, ?_, ?_, ?_, ?_⟩, hY⟩
  · -- period 8 from 2(N + 1) − 3
    intro t ht
    funext p
    by_cases hp : unitOf p ≤ m + 1
    · rw [Ya _ _ hp, Ya _ _ hp, LX _ _ (by omega), LX _ _ (by omega),
        show t + 8 - 2 = (t - 2) + 8 by omega, per _ (by omega)]
    · rw [Yb _ _ (by omega), Yb _ _ (by omega), per _ (by omega)]
  · -- not period 4, seen right of the seam
    intro t ht
    obtain ⟨p, hp, hne⟩ := wit4 t (by omega)
    refine ⟨shiftPt 1 p, by simp only [unitOf_shiftPt]; omega, ?_⟩
    rw [Yb _ _ (by simp only [unitOf_shiftPt]; omega), Yb _ _ (by simp only [unitOf_shiftPt]; omega),
      shiftPt_neg_shiftPt]
    exact hne
  · -- not periodic from 2(N + 1) − 4, seen left of the seam
    obtain ⟨p, hp, hne⟩ := wit7
    refine ⟨p, by omega, ?_⟩
    rw [Ya _ _ (by omega), Ya _ _ (by omega), LX _ _ (by omega), LX _ _ (by omega),
      show 2 * (N + 1) + 4 - 2 = 2 * N + 4 by omega, show 2 * (N + 1) - 4 - 2 = 2 * N - 4 by omega]
    exact hne
  · -- the window, one unit on
    intro t q h1 h2
    have rhs : L (N + 1) t (shiftPt 1 q) = L N t q := by
      by_cases ht : 2 ≤ t
      · simp only [L, ht, ite_true]
        rw [Yb _ _ (by simp only [unitOf_shiftPt]; omega), shiftPt_neg_shiftPt]
      · simp only [L, ht, ite_false]
        rw [Yb _ _ (by simp only [unitOf_shiftPt]; omega), shiftPt_neg_shiftPt]
    rw [rhs, Yb _ _ (by omega), win t _ (by simp only [unitOf_shiftPt]; omega)
      (by simp only [unitOf_shiftPt]; omega), shiftPt_shiftPt_neg]
  · -- the left end has not yet felt the gun at generation 2
    intro p hp
    by_cases hp' : unitOf p ≤ m + 1
    · rw [Ya _ _ hp', Ya _ _ hp']
      simp only [L, show 2 ≤ 2 by decide, show ¬ (2 ≤ 0) by decide, ite_true, ite_false]
    · rw [Yb _ _ (by omega), Yb _ _ (by omega)]
      exact rest _ (by simp only [unitOf_shiftPt]; omega)

/-! ### The base runs, checked by the kernel -/

theorem dframe_even : dframe.even := by
  show (2 : Int) % 2 = 0 ∧ (12 : Int) % 2 = 0 ∧ (24 : Int) % 2 = 0
  decide

theorem unitOf_dframe (q : Pt) : unitOf (q + dframe) = unitOf q + 1 := by
  simp only [unitOf, dframe, Pt.add_x]; omega

def dunframe : Pt := ⟨-dframe.x, -dframe.y, -dframe.z⟩

theorem dunframe_dframe (p : Pt) : p + dunframe + dframe = p := Tape.Pt.add_add_neg p dframe

theorem run_dframe (L : List Pt) (hb : (L.map (· + dframe)).all inBox = true) (n : Nat)
    (hc : ∀ j, j < n → inCore (brun (ofList (L.map (· + dframe))) j) = true) (q : Pt) :
    run (lcfg L) n q = bcfg (brun (ofList (L.map (· + dframe))) n) (q + dframe) := by
  rw [← run_lcfg_map_add L dframe_even n q, ← bcfg_ofList _ hb, run_bcfg_of_core hc]

theorem run_dframe_eq {L : List Pt} {a b : Nat} (hb : (L.map (· + dframe)).all inBox = true)
    (hc : ∀ j, j < max a b + 1 → inCore (brun (ofList (L.map (· + dframe))) j) = true)
    (h : run (lcfg L) a = run (lcfg L) b) :
    brun (ofList (L.map (· + dframe))) a = brun (ofList (L.map (· + dframe))) b := by
  apply bcfg_inj ((inCore_iff _).mp (hc a (by omega))) ((inCore_iff _).mp (hc b (by omega)))
  funext p
  have := congrFun h (p + dunframe)
  rw [run_dframe L hb a (fun j hj => hc j (by omega)), run_dframe L hb b (fun j hj => hc j (by omega)),
    dunframe_dframe] at this
  exact this

def boxed (N : Nat) : Nat := ofList ((divList N).map (· + dframe))
def boxedShift (N : Nat) : Nat := ofList (((divList N).map (shiftPt 1)).map (· + dframe))

/-- The base facts of `S 14 3`. Units in the box are units + 1. -/
def baseCheck : Bool :=
  ((divList 14).map (· + dframe)).all inBox && (((divList 14).map (shiftPt 1)).map (· + dframe)).all inBox &&
  coreRun (boxed 14) 37 &&
  (brun (boxed 14) 33 == brun (boxed 14) 25) &&
  (List.range 8).all (fun i => !eqOn (unitMask 5 23) (brun (boxed 14) (25 + i + 4)) (brun (boxed 14) (25 + i))) &&
  !eqOn (unitMask (-8) 5) (brun (boxed 14) 32) (brun (boxed 14) 24) &&
  eqOn (unitMask (-8) 5) (brun (boxed 14) 2) (boxed 14) &&
  agree (unitMask 4 5) 1 (boxedShift 14) (boxed 14) &&
  agree (unitMask 4 5) 32 (brun (boxedShift 14) 2) (boxed 14)

theorem baseCheck_ok : baseCheck = true := by decide +kernel

theorem periodic8 (c : Config) (μ : Nat) (h : run c (μ + 8) = run c μ) :
    ∀ t, μ ≤ t → run c (t + 8) = run c t := by
  intro t ht
  obtain ⟨d, rfl⟩ : ∃ d, t = μ + d := ⟨t - μ, by omega⟩
  induction d with
  | zero => exact h
  | succ d ih =>
    rw [show μ + (d + 1) + 8 = (μ + d + 8) + 1 by omega, show μ + (d + 1) = (μ + d) + 1 by omega]
    exact congrArg step (ih (by omega))

theorem S_base : S 14 3 := by
  have h := baseCheck_ok
  simp only [baseCheck, Bool.and_eq_true, Bool.not_eq_true'] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨hb, hbs⟩, hc⟩, hper⟩, hw4⟩, hw7⟩, hrest⟩, hwa⟩, hwb⟩ := h
  have core := coreRun_spec 37 _ hc
  have Xf : ∀ n, n ≤ 38 → ∀ q, X 14 n q = bcfg (brun (boxed 14) n) (q + dframe) :=
    fun n hn q => run_dframe _ hb n (fun j hj => core j (by omega)) q
  have wa := agree_spec _ 1 _ _ hwa
  have wb := agree_spec _ 32 _ _ hwb
  have coreS : ∀ j, j ≤ 34 → inCore (brun (boxedShift 14) j) = true := by
    intro j hj
    by_cases h2 : 2 ≤ j
    · obtain ⟨i, rfl⟩ : ∃ i, j = 2 + i := ⟨j - 2, by omega⟩
      rw [brun_add]; exact (wb i (by omega)).1
    · exact (wa j (by omega)).1
  have Xs : ∀ n, n ≤ 35 → ∀ q, shiftC 1 (X 14 n) q = bcfg (brun (boxedShift 14) n) (q + dframe) := by
    intro n hn q
    rw [shift_X, divC, ← lcfg_map_shiftPt]
    exact run_dframe _ hbs n (fun j hj => coreS j (by omega)) q
  have per8 : X 14 (25 + 8) = X 14 25 := by
    funext q; rw [Xf _ (by decide), Xf _ (by decide), eq_of_beq hper]
  have per : ∀ t, 2 * 14 - 3 ≤ t → X 14 (t + 8) = X 14 t := periodic8 _ 25 per8
  have perm := return_mul (divC 14) per
  have win34 : ∀ t, t ≤ 34 → ∀ p, 3 ≤ unitOf p → unitOf p ≤ 4 → shiftC 1 (X 14 t) p = L 14 t p := by
    intro t ht p h1 h2
    rw [Xs t (by omega)]
    by_cases h2t : 2 ≤ t
    · simp only [L, h2t, ite_true]
      rw [Xf _ (by omega)]
      obtain ⟨i, rfl⟩ : ∃ i, t = 2 + i := ⟨t - 2, by omega⟩
      rw [brun_add, show 2 + i - 2 = i by omega]
      exact eqOn_spec (by decide) (by decide) (by decide) (wb i (by omega)).2.2 _
        (by rw [unitOf_dframe]; omega) (by rw [unitOf_dframe]; omega)
    · simp only [L, h2t, ite_false]
      rw [Xf _ (by omega)]
      exact eqOn_spec (by decide) (by decide) (by decide) (wa t (by omega)).2.2 _
        (by rw [unitOf_dframe]; omega) (by rw [unitOf_dframe]; omega)
  have winAll : ∀ t p, 3 ≤ unitOf p → unitOf p ≤ 4 → shiftC 1 (X 14 t) p = L 14 t p := by
    intro t
    induction t using Nat.strongRecOn with
    | ind t ih =>
      by_cases ht : t ≤ 34
      · exact win34 t ht
      · intro p h1 h2
        have := ih (t - 8) (by omega) p h1 h2
        simp only [L, show 2 ≤ t by omega, show 2 ≤ t - 8 by omega, ite_true] at this ⊢
        rw [show t = (t - 8) + 8 by omega, per _ (by omega), show t - 8 + 8 - 2 = (t - 10) + 8 by omega,
          per _ (by omega), show t - 10 = t - 8 - 2 by omega]
        exact this
  refine ⟨⟨by decide, by decide⟩, per, ?_, ?_, ?_, ?_⟩
  · intro t ht
    simp only [List.all_eq_true, List.mem_range, Bool.not_eq_true'] at hw4
    have hi := hw4 ((t - 25) % 8) (Nat.mod_lt _ (by decide))
    obtain ⟨p, h1, -, hne⟩ := neqOn_spec (by decide) (by decide) (by decide) hi
    refine ⟨p + dunframe, ?_, ?_⟩
    · have := unitOf_dframe (p + dunframe); rw [dunframe_dframe] at this; omega
    · have e1 : X 14 t = X 14 (25 + (t - 25) % 8) := by
        have := perm ((t - 25) / 8) (25 + (t - 25) % 8) (by omega)
        rw [show 25 + (t - 25) % 8 + 8 * ((t - 25) / 8) = t by omega] at this
        exact this
      have e2 : X 14 (t + 4) = X 14 (25 + (t - 25) % 8 + 4) := by
        have := perm ((t - 25) / 8) (25 + (t - 25) % 8 + 4) (by omega)
        rw [show 25 + (t - 25) % 8 + 4 + 8 * ((t - 25) / 8) = t + 4 by omega] at this
        exact this
      rw [e1, e2, Xf _ (by omega), Xf _ (by omega), dunframe_dframe]; exact hne
  · obtain ⟨p, -, h2, hne⟩ := neqOn_spec (by decide) (by decide) (by decide) hw7
    refine ⟨p + dunframe, ?_, ?_⟩
    · have := unitOf_dframe (p + dunframe); rw [dunframe_dframe] at this; omega
    · rw [Xf _ (by decide), Xf _ (by decide), dunframe_dframe]; exact hne
  · intro t q h1 h2
    have := winAll t (shiftPt 1 q) (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
    simp only [shiftC, shiftPt_neg_shiftPt] at this
    exact this
  · intro p hp
    rw [Xf _ (by decide), Xf _ (by decide)]
    exact eqOn_spec_le (by decide) (by decide) hrest _ (by rw [unitOf_dframe]; omega)

theorem S_all : ∀ k, S (14 + k) (3 + k)
  | 0 => S_base
  | k + 1 => by
    have := (S_succ (S_all k)).1
    rw [show 14 + (k + 1) = 14 + k + 1 by omega]
    push_cast
    rw [show (3 : Int) + (k + 1) = 3 + k + 1 by omega]
    exact this

/-- The direct runs for N = 8 .. 13. -/
def directCheck (N : Nat) : Bool :=
  ((divList N).map (· + dframe)).all inBox && coreRun (boxed N) (2 * N + 6) &&
  (brun (boxed N) (2 * N - 3 + 8) == brun (boxed N) (2 * N - 3)) &&
  (List.range 7).all (fun i => brun (boxed N) (2 * N - 3 + (i + 1)) != brun (boxed N) (2 * N - 3)) &&
  (brun (boxed N) (2 * N - 4 + 8) != brun (boxed N) (2 * N - 4))

def directOK : Bool := (List.range 6).all (fun i => directCheck (i + 8))

theorem directOK_ok : directOK = true := by decide +kernel

/-- What the theorem says about the divider of N units. -/
def Facts (N : Nat) : Prop :=
  X N (2 * N - 3 + 8) = X N (2 * N - 3) ∧ (∀ k, 0 < k → k < 8 → X N (2 * N - 3 + k) ≠ X N (2 * N - 3)) ∧
    X N (2 * N - 4 + 8) ≠ X N (2 * N - 4)

theorem direct_facts (N : Nat) (h8 : 8 ≤ N) (h : directCheck N = true) : Facts N := by
  simp only [directCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨hb, hc⟩, h8'⟩, hk⟩, hpre⟩ := h
  simp only [List.all_eq_true, List.mem_range, bne_iff_ne, ne_eq] at hk
  simp only [bne_iff_ne, ne_eq] at hpre
  have core := coreRun_spec _ _ hc
  have hc' : ∀ a b, a ≤ 2 * N + 6 → b ≤ 2 * N + 6 → ∀ j, j < max a b + 1 →
      inCore (brun (boxed N) j) = true := fun a b ha hb j hj => core j (by omega)
  refine ⟨?_, ?_, ?_⟩
  · funext q
    simp only [X, divC]
    have e8 := eq_of_beq h8'
    simp only [boxed] at e8 core
    rw [run_dframe _ hb _ (fun j hj => core j (by omega)), run_dframe _ hb _ (fun j hj => core j (by omega)), e8]
  · intro k hk0 hk8 e
    have := hk (k - 1) (by omega)
    rw [show k - 1 + 1 = k by omega] at this
    exact this (run_dframe_eq hb (hc' _ _ (by omega) (by omega)) e)
  · intro e; exact hpre (run_dframe_eq hb (hc' _ _ (by omega) (by omega)) e)

theorem period_k (c : Config) (μ k : Nat) (h : run c (μ + k) = run c μ) : ∀ a, run c (μ + k * a) = run c μ
  | 0 => rfl
  | a + 1 => by
    rw [show μ + k * (a + 1) = (μ + k) + k * a by rw [Nat.mul_succ]; omega, run_add, h, ← run_add,
      period_k c μ k h a]

theorem S_facts {N : Nat} {m : Int} (h : S N m) : Facts N := by
  have hN : 7 ≤ N := by have := h.side; omega
  refine ⟨h.per _ (Nat.le_refl _), fun k hk0 hk8 e => ?_, ?_⟩
  · -- a return after k < 8 gives one after 4
    have pk := period_k (divC N) (2 * N - 3) k e
    have perm := return_mul (divC N) h.per
    have four : X N (2 * N - 3 + 4) = X N (2 * N - 3) := by
      obtain ⟨a, b, hab⟩ : ∃ a b, k * a = 4 + 8 * b := by
        rcases (show k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 by omega) with
          rfl | rfl | rfl | rfl | rfl | rfl | rfl
        · exact ⟨4, 0, rfl⟩
        · exact ⟨2, 0, rfl⟩
        · exact ⟨4, 1, rfl⟩
        · exact ⟨1, 0, rfl⟩
        · exact ⟨4, 2, rfl⟩
        · exact ⟨2, 1, rfl⟩
        · exact ⟨4, 3, rfl⟩
      have e1 := pk a
      rw [hab, show 2 * N - 3 + (4 + 8 * b) = (2 * N - 3 + 4) + 8 * b by omega,
        perm b _ (by omega)] at e1
      exact e1
    obtain ⟨p, -, hne⟩ := h.wit4 _ (Nat.le_refl _)
    exact hne (congrFun four p)
  · obtain ⟨p, -, hne⟩ := h.wit7
    intro e
    apply hne
    rw [show 2 * N + 4 = 2 * N - 4 + 8 by omega, e]

/-- **The divider has period exactly 8 from generation 2N − 3, for every N ≥ 8** (section 21b): the state at
2N − 3 returns after 8 generations and after no fewer, and the state at 2N − 4 does not return after 8. -/
theorem divider_period (N : Nat) (hN : 8 ≤ N) :
    run (divC N) (2 * N - 3 + 8) = run (divC N) (2 * N - 3) ∧
    (∀ k, 0 < k → k < 8 → run (divC N) (2 * N - 3 + k) ≠ run (divC N) (2 * N - 3)) ∧
    run (divC N) (2 * N - 4 + 8) ≠ run (divC N) (2 * N - 4) := by
  by_cases h13 : N ≤ 13
  · have hz := directOK_ok
    simp only [directOK, List.all_eq_true, List.mem_range] at hz
    have := hz (N - 8) (by omega)
    rw [show N - 8 + 8 = N by omega] at this
    exact direct_facts N hN this
  · have := S_all (N - 14)
    rw [show 14 + (N - 14) = N by omega] at this
    exact S_facts this

end Gump.Divider
