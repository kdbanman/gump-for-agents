/-
**The gun's line for every N** (`research/signals/README.md` section 21, "The line has period exactly 4 from
generation 2N on for every N ≥ 2"; the base facts of `research/signals/prove_line.py`; `REVIEW-signals-4.md`).

line-C(N) is capA (a cap at rest) + N units of bare wire C + the rake gun, in empty space: a finite configuration
of the whole lattice (`lineC N`, 33 + 5N cells, the coordinates of `research/signals/objects/line-C.json`).

`line_orbit`: for every N ≥ 2, the state at generation s returns after p > 0 generations **exactly when s ≥ 2N
and 4 divides p**. So from generation 2N on the line is an oscillator of exact period 4, and the state at 2N − 1
is on no cycle at all: the preperiod is exactly 2N.

The proof is the source's induction, with the gluing made a theorem (`Gump.Tape.glue_run`). Write X_N(t) for the
orbit and L_N(t) = X_N(t − 2) (t ≥ 2), X_N(t) (t < 2). The statement `S N m` says: X_N has period 4 from 2N, not
period 2 there (seen at a unit > m), not period 4 from 2N − 1 (seen at a unit ≤ m + 1); X_N(t) on the units
m − 1, m, moved one unit, is L_N(t) on the units m, m + 1, for every t; X_N(2) = X_N(0) on the units ≤ m + 1.
Then (`S_succ`) L_N on the units ≤ m glued to X_N moved one unit on the units > m is an orbit whose start is
line-C(N + 1), so it is X_{N+1}, and `S (N+1) (m+1)` follows. The base `S 4 1` and the cases N = 2, 3 are
kernel-checked runs on the bit-parallel stepper (`decide +kernel`); every one of them is also checked against
`reference/oracle.py` by `tape_line.py`, which also writes `Gump/LineData.lean`.
-/
import Gump.LineData

namespace Gump.Line
open Gump Gump.Tape Gump.Bits

/-- The cells of line-C(N): capA, N units of wire C on the units 0 .. N − 1, and the gun moved N units. -/
def lineList (N : Nat) : List Pt := capA ++ wordList 0 (List.replicate N .C) ++ gun.map (shiftPt N)

/-- **line-C(N)**, a finite configuration of the whole lattice. -/
def lineC (N : Nat) : Config := lcfg (lineList N)

theorem capA_unit : ∀ q ∈ capA, unitOf q < 0 := by decide
theorem gun_unit : ∀ q ∈ gun, 0 ≤ unitOf q := by decide

theorem getD_replicate_C : ∀ (N i : Nat), (List.replicate N Letter.C).getD i .C = .C
  | 0, i => by simp
  | N + 1, 0 => by simp [List.replicate_succ]
  | N + 1, i + 1 => by simp only [List.replicate_succ, List.getD_cons_succ]; exact getD_replicate_C N i

theorem lineC_eq (N : Nat) (p : Pt) : lineC N p =
    (lcfg capA p || (decide (0 ≤ unitOf p ∧ unitOf p < N) && tape (fun _ => .C) p) ||
      lcfg gun (shiftPt (-N) p)) := by
  simp only [lineC, lineList, lcfg_append, lcfg_wordList, lcfg_map_shiftPt, getD_replicate_C, shiftC,
    List.length_replicate, tape]
  simp

theorem capA_off {p : Pt} (h : 0 ≤ unitOf p) : lcfg capA p = false := by
  cases e : lcfg capA p
  · rfl
  · have := capA_unit p ((lcfg_iff _ _).mp e); omega

theorem gun_off {N : Nat} {p : Pt} (h : unitOf p < N) : lcfg gun (shiftPt (-N) p) = false := by
  cases e : lcfg gun (shiftPt (-N) p)
  · rfl
  · have := gun_unit _ ((lcfg_iff _ _).mp e); simp only [unitOf_shiftPt] at this; omega

theorem lineC_left {N : Nat} {p : Pt} (h : unitOf p < 0) : lineC N p = lcfg capA p := by
  rw [lineC_eq, gun_off (by omega)]
  have : ¬ (0 ≤ unitOf p ∧ unitOf p < (N : Int)) := by omega
  simp [this]

theorem lineC_mid {N : Nat} {p : Pt} (h1 : 0 ≤ unitOf p) (h2 : unitOf p < N) :
    lineC N p = tape (fun _ => .C) p := by
  rw [lineC_eq, gun_off h2, capA_off h1]
  simp [h1, h2]

theorem lineC_right {N : Nat} {p : Pt} (h : N ≤ unitOf p) : lineC N p = lcfg gun (shiftPt (-N) p) := by
  rw [lineC_eq, capA_off (by omega)]
  have : ¬ (0 ≤ unitOf p ∧ unitOf p < (N : Int)) := by omega
  simp [this]

/-- The orbit of line-C(N). -/
def X (N t : Nat) : Config := run (lineC N) t

/-- The orbit delayed by two generations (and, before that, the orbit itself). -/
def L (N t : Nat) : Config := if 2 ≤ t then X N (t - 2) else X N t

/-- The statement of the induction, with the seam at unit m. -/
structure S (N : Nat) (m : Int) : Prop where
  side : 1 ≤ m ∧ m + 2 ≤ N
  per : ∀ t, 2 * N ≤ t → X N (t + 4) = X N t
  wit2 : ∃ p, m + 1 ≤ unitOf p ∧ X N (2 * N + 2) p ≠ X N (2 * N) p
  wit3 : ∃ p, unitOf p ≤ m + 1 ∧ X N (2 * N + 3) p ≠ X N (2 * N - 1) p
  win : ∀ t q, m - 1 ≤ unitOf q → unitOf q ≤ m → X N t q = L N t (shiftPt 1 q)
  rest : ∀ p, unitOf p ≤ m + 1 → X N 2 p = X N 0 p

theorem X_succ (N t : Nat) : X N (t + 1) = step (X N t) := rfl

theorem shift_X (N t : Nat) : shiftC 1 (X N t) = run (shiftC 1 (lineC N)) t := (run_shiftC 1 _ t).symm

/-- **The induction step.** -/
theorem S_succ {N : Nat} {m : Int} (h : S N m) :
    S (N + 1) (m + 1) ∧ ∀ t, X (N + 1) t = glue m (L N t) (shiftC 1 (X N t)) := by
  obtain ⟨⟨hm1, hm2⟩, per, wit2, wit3, win, rest⟩ := h
  -- the two charts and their overlap
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
  have h0 : glue m (L N 0) (shiftC 1 (X N 0)) = lineC (N + 1) := by
    funext p
    simp only [glue, L, X, show ¬ (2 ≤ 0) by decide, ite_false, run, shiftC]
    split
    · rename_i hp
      by_cases hu : unitOf p < 0
      · rw [lineC_left hu, lineC_left hu]
      · rw [lineC_mid (by omega) (by omega), lineC_mid (by omega) (by push_cast; omega)]
    · rename_i hp
      by_cases hu : unitOf p - 1 < N
      · rw [lineC_mid (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
          lineC_mid (by omega) (by push_cast; omega)]
        simp only [tape, unitOf_shiftPt, shiftPt_shiftPt]
        congr 2
        omega
      · rw [lineC_right (by simp only [unitOf_shiftPt]; omega), lineC_right (by push_cast; omega),
          shiftPt_shiftPt]
        congr 2
        push_cast; omega
  have hY : ∀ t, X (N + 1) t = glue m (L N t) (shiftC 1 (X N t)) := by
    intro t
    have := glue_run m (L N) (fun t => shiftC 1 (X N t)) hX hZ hXZ t
    rw [h0] at this
    exact this
  -- the two charts, read off the glued orbit
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
  · -- period 4 from 2(N + 1)
    intro t ht
    funext p
    by_cases hp : unitOf p ≤ m + 1
    · rw [Ya _ _ hp, Ya _ _ hp, LX _ _ (by omega), LX _ _ (by omega),
        show t + 4 - 2 = (t - 2) + 4 by omega, per _ (by omega)]
    · rw [Yb _ _ (by omega), Yb _ _ (by omega), per _ (by omega)]
  · -- not period 2, seen right of the seam
    obtain ⟨p, hp, hne⟩ := wit2
    refine ⟨shiftPt 1 p, by simp only [unitOf_shiftPt]; omega, ?_⟩
    rw [Yb _ _ (by simp only [unitOf_shiftPt]; omega), Yb _ _ (by simp only [unitOf_shiftPt]; omega),
      shiftPt_neg_shiftPt, show 2 * (N + 1) + 2 = 2 * N + 4 by omega, show 2 * (N + 1) = 2 * N + 2 by omega,
      per _ (Nat.le_refl _)]
    exact fun e => hne e.symm
  · -- not periodic from 2(N + 1) − 1, seen left of the seam
    obtain ⟨p, hp, hne⟩ := wit3
    refine ⟨p, by omega, ?_⟩
    rw [Ya _ _ hp, Ya _ _ hp, LX _ _ (by omega), LX _ _ (by omega),
      show 2 * (N + 1) + 3 - 2 = 2 * N + 3 by omega, show 2 * (N + 1) - 1 - 2 = 2 * N - 1 by omega]
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

theorem S_all : ∀ j : Nat, S (4 + j) (1 + j) → ∀ k, S (4 + j + k) (1 + j + k) := by
  intro j h k
  induction k with
  | zero => simpa using h
  | succ k ih =>
    have := (S_succ ih).1
    rw [show 4 + j + (k + 1) = 4 + j + k + 1 by omega]
    push_cast at this ⊢
    rw [show (1 : Int) + j + (k + 1) = 1 + j + k + 1 by omega]
    exact this

/-! ### The base runs, checked by the kernel -/

theorem frame_even : frame.even := by
  show (16 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

theorem unitOf_frame (q : Pt) : unitOf (q + frame) = unitOf q + 8 := by
  simp only [unitOf, frame, Pt.add_x]; omega

/-- The negative of the frame. -/
def unframe : Pt := ⟨-frame.x, -frame.y, -frame.z⟩

theorem unframe_frame (p : Pt) : p + unframe + frame = p := Tape.Pt.add_add_neg p frame

/-- A run of a list, read in the box. -/
theorem run_frame (L : List Pt) (hb : (L.map (· + frame)).all inBox = true) (n : Nat)
    (hc : ∀ j, j < n → inCore (brun (ofList (L.map (· + frame))) j) = true) (q : Pt) :
    run (lcfg L) n q = bcfg (brun (ofList (L.map (· + frame))) n) (q + frame) := by
  rw [← run_lcfg_map_add L frame_even n q, ← bcfg_ofList _ hb, run_bcfg_of_core hc]

theorem run_frame_eq {L : List Pt} {a b : Nat} (hb : (L.map (· + frame)).all inBox = true)
    (hc : ∀ j, j < max a b + 1 → inCore (brun (ofList (L.map (· + frame))) j) = true)
    (h : run (lcfg L) a = run (lcfg L) b) :
    brun (ofList (L.map (· + frame))) a = brun (ofList (L.map (· + frame))) b := by
  apply bcfg_inj ((inCore_iff _).mp (hc a (by omega))) ((inCore_iff _).mp (hc b (by omega)))
  funext p
  have := congrFun h (p + unframe)
  rw [run_frame L hb a (fun j hj => hc j (by omega)), run_frame L hb b (fun j hj => hc j (by omega)),
    unframe_frame] at this
  exact this

/-- The number of line-C(N) in the box. -/
def boxed (N : Nat) : Nat := ofList ((lineList N).map (· + frame))

/-- The number of line-C(N) moved one unit, in the box. -/
def boxedShift (N : Nat) : Nat := ofList (((lineList N).map (shiftPt 1)).map (· + frame))

/-- The base facts of `S 4 1`, as one Boolean the kernel evaluates. Units in the box are units + 8. -/
def baseCheck : Bool :=
  ((lineList 4).map (· + frame)).all inBox && (((lineList 4).map (shiftPt 1)).map (· + frame)).all inBox &&
  coreRun (boxed 4) 12 &&
  (brun (boxed 4) 12 == brun (boxed 4) 8) &&
  !eqOn (unitMask 10 23) (brun (boxed 4) 10) (brun (boxed 4) 8) &&
  !eqOn (unitMask (-8) 10) (brun (boxed 4) 11) (brun (boxed 4) 7) &&
  eqOn (unitMask (-8) 10) (brun (boxed 4) 2) (boxed 4) &&
  agree (unitMask 9 10) 1 (boxedShift 4) (boxed 4) &&
  agree (unitMask 9 10) 11 (brun (boxedShift 4) 2) (boxed 4)

theorem baseCheck_ok : baseCheck = true := by decide +kernel

theorem S_four : S 4 1 := by
  have h := baseCheck_ok
  simp only [baseCheck, Bool.and_eq_true, Bool.not_eq_true'] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨hb, hbs⟩, hc⟩, hper⟩, hw2⟩, hw3⟩, hrest⟩, hwa⟩, hwb⟩ := h
  have core := coreRun_spec 12 _ hc
  have Xf : ∀ n, n ≤ 13 → ∀ q, X 4 n q = bcfg (brun (boxed 4) n) (q + frame) :=
    fun n hn q => run_frame _ hb n (fun j hj => core j (by omega)) q
  have wa := agree_spec _ 1 _ _ hwa
  have wb := agree_spec _ 11 _ _ hwb
  have coreS : ∀ j, j ≤ 13 → inCore (brun (boxedShift 4) j) = true := by
    intro j hj
    by_cases h2 : 2 ≤ j
    · obtain ⟨i, rfl⟩ : ∃ i, j = 2 + i := ⟨j - 2, by omega⟩
      rw [brun_add]; exact (wb i (by omega)).1
    · exact (wa j (by omega)).1
  have Xs : ∀ n, n ≤ 14 → ∀ q, shiftC 1 (X 4 n) q = bcfg (brun (boxedShift 4) n) (q + frame) := by
    intro n hn q
    rw [shift_X, lineC, ← lcfg_map_shiftPt]
    exact run_frame _ hbs n (fun j hj => coreS j (by omega)) q
  have per4 : X 4 (8 + 4) = X 4 8 := by
    funext q; rw [Xf _ (by decide), Xf _ (by decide), eq_of_beq hper]
  have per : ∀ t, 2 * 4 ≤ t → X 4 (t + 4) = X 4 t := periodic_from _ 8 per4
  -- the window for t ≤ 13
  have win13 : ∀ t, t ≤ 13 → ∀ p, 1 ≤ unitOf p → unitOf p ≤ 2 → shiftC 1 (X 4 t) p = L 4 t p := by
    intro t ht p h1 h2
    rw [Xs t (by omega)]
    by_cases h2t : 2 ≤ t
    · simp only [L, h2t, ite_true]
      rw [Xf _ (by omega)]
      obtain ⟨i, rfl⟩ : ∃ i, t = 2 + i := ⟨t - 2, by omega⟩
      rw [brun_add, show 2 + i - 2 = i by omega]
      exact eqOn_spec (by decide) (by decide) (by decide) (wb i (by omega)).2.2 _
        (by rw [unitOf_frame]; omega) (by rw [unitOf_frame]; omega)
    · simp only [L, h2t, ite_false]
      rw [Xf _ (by omega)]
      exact eqOn_spec (by decide) (by decide) (by decide) (wa t (by omega)).2.2 _
        (by rw [unitOf_frame]; omega) (by rw [unitOf_frame]; omega)
  have winAll : ∀ t p, 1 ≤ unitOf p → unitOf p ≤ 2 → shiftC 1 (X 4 t) p = L 4 t p := by
    intro t
    induction t using Nat.strongRecOn with
    | ind t ih =>
      by_cases ht : t ≤ 13
      · exact win13 t ht
      · intro p h1 h2
        have := ih (t - 4) (by omega) p h1 h2
        simp only [L, show 2 ≤ t by omega, show 2 ≤ t - 4 by omega, ite_true] at this ⊢
        rw [show t = (t - 4) + 4 by omega, per _ (by omega), show t - 4 + 4 - 2 = (t - 6) + 4 by omega,
          per _ (by omega), show t - 6 = t - 4 - 2 by omega]
        exact this
  refine ⟨⟨by decide, by decide⟩, per, ?_, ?_, ?_, ?_⟩
  · obtain ⟨p, h1, -, hne⟩ := neqOn_spec (by decide) (by decide) (by decide) hw2
    refine ⟨p + unframe, ?_, ?_⟩
    · have := unitOf_frame (p + unframe); rw [unframe_frame] at this; omega
    · rw [Xf _ (by decide), Xf _ (by decide), unframe_frame]; exact hne
  · obtain ⟨p, -, h2, hne⟩ := neqOn_spec (by decide) (by decide) (by decide) hw3
    refine ⟨p + unframe, ?_, ?_⟩
    · have := unitOf_frame (p + unframe); rw [unframe_frame] at this; omega
    · rw [Xf _ (by decide), Xf _ (by decide), unframe_frame]; exact hne
  · intro t q h1 h2
    have := winAll t (shiftPt 1 q) (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
    simp only [shiftC, shiftPt_neg_shiftPt] at this
    exact this
  · intro p hp
    rw [Xf _ (by decide), Xf _ (by decide)]
    exact eqOn_spec_le (by decide) (by decide) hrest _ (by rw [unitOf_frame]; omega)

/-- The direct runs for N = 2, 3. -/
def directCheck (N : Nat) : Bool :=
  ((lineList N).map (· + frame)).all inBox && coreRun (boxed N) (2 * N + 4) &&
  (brun (boxed N) (2 * N + 4) == brun (boxed N) (2 * N)) &&
  (brun (boxed N) (2 * N + 2) != brun (boxed N) (2 * N)) &&
  (brun (boxed N) (2 * N + 3) != brun (boxed N) (2 * N - 1))

theorem directCheck_two : directCheck 2 = true := by decide +kernel
theorem directCheck_three : directCheck 3 = true := by decide +kernel

theorem direct_facts (N : Nat) (h : directCheck N = true) :
    X N (2 * N + 4) = X N (2 * N) ∧ X N (2 * N + 2) ≠ X N (2 * N) ∧ X N (2 * N + 3) ≠ X N (2 * N - 1) := by
  simp only [directCheck, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
  obtain ⟨⟨⟨⟨hb, hc⟩, h4⟩, h2⟩, h3⟩ := h
  have core := coreRun_spec _ _ hc
  have hc' : ∀ a b, a ≤ 2 * N + 4 → b ≤ 2 * N + 4 → ∀ j, j < max a b + 1 →
      inCore (brun (boxed N) j) = true := fun a b ha hb j hj => core j (by omega)
  refine ⟨?_, ?_, ?_⟩
  · funext q
    simp only [X, lineC]
    have e4 := eq_of_beq h4
    simp only [boxed] at e4 core
    rw [run_frame _ hb _ (fun j hj => core j (by omega)), run_frame _ hb _ (fun j hj => core j (by omega)),
      e4]
  · intro e; exact h2 (run_frame_eq hb (hc' _ _ (by omega) (by omega)) e)
  · intro e; exact h3 (run_frame_eq hb (hc' _ _ (by omega) (by omega)) e)

theorem S_facts {N : Nat} {m : Int} (h : S N m) :
    X N (2 * N + 4) = X N (2 * N) ∧ X N (2 * N + 2) ≠ X N (2 * N) ∧ X N (2 * N + 3) ≠ X N (2 * N - 1) := by
  refine ⟨h.per _ (Nat.le_refl _), ?_, ?_⟩
  · obtain ⟨p, -, hne⟩ := h.wit2; exact fun e => hne (congrFun e p)
  · obtain ⟨p, -, hne⟩ := h.wit3; exact fun e => hne (congrFun e p)

/-! ### The gun's line -/

/-- **The gun's line, for every N ≥ 2.** The state of line-C(N) at generation s returns after p > 0
generations exactly when s ≥ 2N and 4 divides p: an oscillator of exact period 4 from generation 2N on, with
preperiod exactly 2N. -/
theorem line_orbit (N : Nat) (hN : 2 ≤ N) (s p : Nat) (hp : 0 < p) :
    run (lineC N) (s + p) = run (lineC N) s ↔ 2 * N ≤ s ∧ p % 4 = 0 := by
  have facts : X N (2 * N + 4) = X N (2 * N) ∧ X N (2 * N + 2) ≠ X N (2 * N) ∧
      X N (2 * N + 3) ≠ X N (2 * N - 1) := by
    rcases (show N = 2 ∨ N = 3 ∨ 4 ≤ N by omega) with rfl | rfl | h4
    · exact direct_facts 2 directCheck_two
    · exact direct_facts 3 directCheck_three
    · obtain ⟨k, rfl⟩ : ∃ k, N = 4 + 0 + k := ⟨N - 4, by omega⟩
      exact S_facts (S_all 0 (by simpa using S_four) k)
  obtain ⟨h4, h2, h3⟩ := facts
  exact orbit_classify (lineC N) (2 * N) (by omega) h4 h2 h3 s p hp

/-- **The gun's line, in the form of `Gump.Signals`**: from generation 2N on, an oscillator of exact period 4;
and not periodic from generation 2N − 1. -/
theorem line_period_four (N : Nat) (hN : 2 ≤ N) :
    run (lineC N) (2 * N + 4) = run (lineC N) (2 * N) ∧
    (∀ k, 0 < k → k < 4 → run (lineC N) (2 * N + k) ≠ run (lineC N) (2 * N)) ∧
    run (lineC N) (2 * N - 1 + 4) ≠ run (lineC N) (2 * N - 1) := by
  refine ⟨(line_orbit N hN _ 4 (by decide)).mpr ⟨Nat.le_refl _, rfl⟩, ?_, ?_⟩
  · intro k hk0 hk4 e
    have := ((line_orbit N hN _ k hk0).mp e).2
    omega
  · intro e
    have := ((line_orbit N hN _ 4 (by decide)).mp e).1
    omega

end Gump.Line
