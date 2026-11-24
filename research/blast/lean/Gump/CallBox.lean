/-
A second bit-parallel stepper, proved equal to `Gump.step`: the box [−16, 112) × [−16, 112) × [−16, 0) (doubled
coordinates), shaped for push 9's call line, which spans 65 units in x and in y and five in z. A configuration in the
box is one natural number S of 2^18 bits: point p is bit idx p = (x+16) + 128 (y+16) + 16384 (z+16) of S. The rule
is the same Boolean formula in the same bit-sliced counter as in `Gump.Bits` (whose generic parts are reused);
only the geometry differs: the neighbour planes are shifts by o.x + 128 o.y + 16384 o.z and the masks select the
cells of each axis in the interior [−14, 110) × [−14, 110) × [−14, −2).

`bstep_spec`: for every S whose live points lie in the core [−12, 108) × [−12, 108) × [−12, −4),
`bcfg (bstep S) = step (bcfg S)`. `Gump.Bits` and its 64-cube are unchanged.
-/
import Gump.Bits

namespace Gump.Call.Box
open Gump Gump.Bits

def inBox (p : Pt) : Bool := decide (-16 ≤ p.x ∧ p.x < 112 ∧ -16 ≤ p.y ∧ p.y < 112 ∧ -16 ≤ p.z ∧ p.z < 0)

/-- The interior: every neighbour of an interior point is in the box. -/
def interior (p : Pt) : Bool :=
  decide (-14 ≤ p.x ∧ p.x < 110 ∧ -14 ≤ p.y ∧ p.y < 110 ∧ -14 ≤ p.z ∧ p.z < -2)

/-- The core: every neighbour of a point outside the interior is outside the core. -/
def inCoreP (p : Pt) : Prop := -12 ≤ p.x ∧ p.x < 108 ∧ -12 ≤ p.y ∧ p.y < 108 ∧ -12 ≤ p.z ∧ p.z < -4

def idx (p : Pt) : Nat := (p.x + 16 + 128 * (p.y + 16) + 16384 * (p.z + 16)).toNat

/-- The point with index i. -/
def ptOf (i : Nat) : Pt := ⟨((i % 128 : Nat) : Int) - 16, ((i / 128 % 128 : Nat) : Int) - 16, ((i / 16384 : Nat) : Int) - 16⟩

theorem idx_ptOf (i : Nat) (h : i < 262144) : idx (ptOf i) = i := by
  simp only [idx, ptOf]; omega

theorem inBox_ptOf (i : Nat) (h : i < 262144) : inBox (ptOf i) = true := by
  unfold inBox ptOf
  apply decide_eq_true
  dsimp only
  omega

theorem idx_coords (p : Pt) (h : inBox p = true) :
    idx p % 128 = (p.x + 16).toNat ∧ idx p / 128 % 128 = (p.y + 16).toNat ∧ idx p / 16384 = (p.z + 16).toNat ∧
      idx p < 262144 := by
  simp only [inBox, decide_eq_true_eq] at h
  simp only [idx]
  omega

theorem idx_inj {p q : Pt} (hp : inBox p = true) (hq : inBox q = true) (h : idx p = idx q) : p = q := by
  have a := idx_coords p hp
  have b := idx_coords q hq
  simp only [inBox, decide_eq_true_eq] at hp hq
  rw [h] at a
  apply Pt.ext' <;> omega

/-- A configuration inside the box, as a number. -/
def bcfg (S : Nat) : Config := fun p => inBox p && S.testBit (idx p)

/-- Bits with x-coordinate of parity `par` in the interior. -/
def xPar (par : Nat) : Nat := rep2 (rep2 (2 ^ par) 2 6 &&& (2 ^ 126 - 2 ^ 2)) 128 11
/-- Bits with y-coordinate of parity `par` in the interior. -/
def yPar (par : Nat) : Nat := rep2 (rep2 ((2 ^ 128 - 1) <<< (128 * par)) 256 6 &&& (2 ^ 16128 - 2 ^ 256)) 16384 4
/-- Bits with z-coordinate of parity `par` in the interior. -/
def zPar (par : Nat) : Nat := rep2 ((2 ^ 16384 - 1) <<< (16384 * par)) 32768 3 &&& (2 ^ 229376 - 2 ^ 32768)
/-- The bits of the core. -/
def core : Nat :=
  rep2 (2 ^ 124 - 2 ^ 4) 128 11 &&& rep2 (2 ^ 15872 - 2 ^ 512) 16384 4 &&& (2 ^ 196608 - 2 ^ 65536)

theorem testBit_xPar (par : Nat) (hp : par ≤ 1) (i : Nat) :
    (xPar par).testBit i = decide (i < 262144 ∧ i % 128 % 2 = par ∧ 2 ≤ i % 128 ∧ i % 128 < 126) := by
  have h1 : 2 ^ par < 2 ^ 2 := Nat.pow_lt_pow_right (by decide) (by omega)
  have h2 : rep2 (2 ^ par) 2 6 &&& (2 ^ 126 - 2 ^ 2) < 2 ^ 128 :=
    Nat.and_lt_two_pow _ (Nat.lt_of_le_of_lt (Nat.sub_le _ _) (Nat.pow_lt_pow_right (by decide) (by decide)))
  rw [xPar, testBit_rep2 _ 128 h2, Nat.testBit_and, testBit_rep2 _ 2 h1, Nat.testBit_two_pow,
    testBit_interval 2 126 _ (by decide)]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, show (128 * 2 ^ 11 : Nat) = 262144 from rfl,
    show (2 * 2 ^ 6 : Nat) = 128 from rfl]
  omega

theorem testBit_yPar (par : Nat) (hp : par ≤ 1) (i : Nat) :
    (yPar par).testBit i =
      decide (i < 262144 ∧ i / 128 % 128 % 2 = par ∧ 2 ≤ i / 128 % 128 ∧ i / 128 % 128 < 126) := by
  have h1 : (2 ^ 128 - 1) <<< (128 * par) < 2 ^ 256 := by
    rw [Nat.shiftLeft_eq]
    have : 2 ^ (128 * par) ≤ 2 ^ 128 := two_pow_mono (by omega)
    have h3 : (2 ^ 128 - 1) * 2 ^ (128 * par) ≤ (2 ^ 128 - 1) * 2 ^ 128 := Nat.mul_le_mul_left _ this
    have h4 : (2 ^ 128 - 1) * 2 ^ 128 < 2 ^ 128 * 2 ^ 128 :=
      Nat.mul_lt_mul_of_pos_right (Nat.sub_lt (Nat.two_pow_pos _) (by decide)) (Nat.two_pow_pos _)
    rw [← Nat.pow_add] at h4
    exact Nat.lt_of_le_of_lt h3 h4
  have h2 : rep2 ((2 ^ 128 - 1) <<< (128 * par)) 256 6 &&& (2 ^ 16128 - 2 ^ 256) < 2 ^ 16384 :=
    Nat.and_lt_two_pow _ (Nat.lt_of_le_of_lt (Nat.sub_le _ _) (Nat.pow_lt_pow_right (by decide) (by decide)))
  rw [yPar, testBit_rep2 _ 16384 h2, Nat.testBit_and, testBit_rep2 _ 256 h1, Nat.testBit_shiftLeft,
    Nat.testBit_two_pow_sub_one, testBit_interval 256 16128 _ (by decide)]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, show (16384 * 2 ^ 4 : Nat) = 262144 from rfl,
    show (256 * 2 ^ 6 : Nat) = 16384 from rfl]
  omega

theorem testBit_zPar (par : Nat) (hp : par ≤ 1) (i : Nat) :
    (zPar par).testBit i = decide (i < 262144 ∧ i / 16384 % 2 = par ∧ 2 ≤ i / 16384 ∧ i / 16384 < 14) := by
  have h1 : (2 ^ 16384 - 1) <<< (16384 * par) < 2 ^ 32768 := by
    rw [Nat.shiftLeft_eq]
    have : 2 ^ (16384 * par) ≤ 2 ^ 16384 := two_pow_mono (by omega)
    have h3 : (2 ^ 16384 - 1) * 2 ^ (16384 * par) ≤ (2 ^ 16384 - 1) * 2 ^ 16384 := Nat.mul_le_mul_left _ this
    have h4 : (2 ^ 16384 - 1) * 2 ^ 16384 < 2 ^ 16384 * 2 ^ 16384 :=
      Nat.mul_lt_mul_of_pos_right (Nat.sub_lt (Nat.two_pow_pos _) (by decide)) (Nat.two_pow_pos _)
    rw [← Nat.pow_add] at h4
    exact Nat.lt_of_le_of_lt h3 h4
  rw [zPar, Nat.testBit_and, testBit_rep2 _ 32768 h1, Nat.testBit_shiftLeft, Nat.testBit_two_pow_sub_one,
    testBit_interval 32768 229376 _ (by decide)]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, show (32768 * 2 ^ 3 : Nat) = 262144 from rfl]
  omega

theorem testBit_core (i : Nat) :
    core.testBit i = decide (4 ≤ i % 128 ∧ i % 128 < 124 ∧ 4 ≤ i / 128 % 128 ∧ i / 128 % 128 < 124 ∧
      4 ≤ i / 16384 ∧ i / 16384 < 12) := by
  have h1 : 2 ^ 124 - 2 ^ 4 < 2 ^ 128 := Nat.lt_of_le_of_lt (Nat.sub_le _ _) (Nat.pow_lt_pow_right (by decide) (by decide))
  have h2 : 2 ^ 15872 - 2 ^ 512 < 2 ^ 16384 :=
    Nat.lt_of_le_of_lt (Nat.sub_le _ _) (Nat.pow_lt_pow_right (by decide) (by decide))
  rw [core, Nat.testBit_and, Nat.testBit_and, testBit_rep2 _ 128 h1, testBit_rep2 _ 16384 h2,
    testBit_interval 4 124 _ (by decide), testBit_interval 512 15872 _ (by decide),
    testBit_interval 65536 196608 _ (by decide)]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, show (128 * 2 ^ 11 : Nat) = 262144 from rfl,
    show (16384 * 2 ^ 4 : Nat) = 262144 from rfl]
  omega

/-- The cells of each axis in the interior. -/
def mask : Axis → Nat
  | .X => xPar 1 &&& yPar 0 &&& zPar 0
  | .Y => xPar 0 &&& yPar 1 &&& zPar 0
  | .Z => xPar 0 &&& yPar 0 &&& zPar 1

theorem testBit_mask (a : Axis) (p : Pt) (hp : inBox p = true) :
    (mask a).testBit (idx p) = (interior p && cellAx p a) := by
  obtain ⟨c1, c2, c3, c4⟩ := idx_coords p hp
  simp only [inBox, decide_eq_true_eq] at hp
  rw [cellAx_eq]
  apply Bool.eq_iff_iff.mpr
  cases a <;>
    simp only [mask, Nat.testBit_and, testBit_xPar 0 (by decide), testBit_xPar 1 (by decide),
      testBit_yPar 0 (by decide), testBit_yPar 1 (by decide), testBit_zPar 0 (by decide),
      testBit_zPar 1 (by decide), interior, Bool.and_eq_true, decide_eq_true_eq, c1, c2, c3] <;>
    omega

/-! ### One generation -/

/-- The index offset of a neighbour offset. -/
def delta (o : Pt) : Int := o.x + 128 * o.y + 16384 * o.z

/-- The plane whose bit i is bit i + d of S. -/
def sh (S : Nat) (d : Int) : Nat := if 0 ≤ d then S >>> d.toNat else S <<< (-d).toNat

theorem testBit_sh (S i : Nat) (d : Int) (h : 0 ≤ (i : Int) + d) :
    (sh S d).testBit i = S.testBit ((i : Int) + d).toNat := by
  unfold sh
  split
  · rw [Nat.testBit_shiftRight]
    congr 1
    omega
  · rw [Nat.testBit_shiftLeft]
    have : i ≥ (-d).toNat := by omega
    simp only [this, decide_true, Bool.true_and]
    congr 1
    omega

/-- The live-neighbour counter of every cell of axis a, at once. -/
def ctrAx (S : Nat) (a : Axis) : Ctr := ((offsets a).map delta).foldl (fun c d => c.add (sh S d)) ⟨0, 0, 0, 0⟩

/-- One generation on the cells of axis a in the interior. -/
def bstepAx (S : Nat) (a : Axis) : Nat := mask a &&& ruleBits S (ctrAx S a)

/-- **One generation, bit-parallel.** -/
def bstep (S : Nat) : Nat := bstepAx S .X ||| bstepAx S .Y ||| bstepAx S .Z

theorem idx_add (p o : Pt) (hp : interior p = true) (ho : o.x.natAbs ≤ 2 ∧ o.y.natAbs ≤ 2 ∧ o.z.natAbs ≤ 2) :
    inBox (p + o) = true ∧ ((idx (p + o) : Nat) : Int) = (idx p : Int) + delta o := by
  simp only [interior, decide_eq_true_eq] at hp
  simp only [inBox, idx, delta, Pt.add_x, Pt.add_y, Pt.add_z, decide_eq_true_eq]
  omega

theorem val_ctrAx (S : Nat) (p : Pt) (hp : interior p = true) :
    (ctrAx S p.axis).val (idx p) = count (bcfg S) p := by
  unfold ctrAx
  rw [val_foldl (sh S) (idx p) _ ⟨0, 0, 0, 0⟩ (by simp [Ctr.val, List.length_map, offsets_length]),
    List.countP_map]
  simp only [Ctr.val, Nat.zero_testBit, Bool.toNat_false, Nat.mul_zero, Nat.add_zero, Nat.zero_add]
  unfold count nbrs
  rw [List.countP_map]
  apply List.countP_congr
  intro o ho
  obtain ⟨hb, hi⟩ := idx_add p o hp (offsets_small _ o ho)
  simp only [Function.comp, bcfg, hb, Bool.true_and]
  rw [testBit_sh S (idx p) (delta o) (by omega)]
  rw [show ((idx p : Int) + delta o).toNat = idx (p + o) by omega]

theorem testBit_bstep_interior (S : Nat) (p : Pt) (hp : interior p = true) :
    (bstep S).testBit (idx p) = step (bcfg S) p := by
  have hb : inBox p = true := by
    simp only [interior, inBox, decide_eq_true_eq] at hp ⊢; omega
  have hS : S.testBit (idx p) = bcfg S p := by simp [bcfg, hb]
  simp only [bstep, bstepAx, Nat.testBit_or, Nat.testBit_and, testBit_mask _ p hb, hp, Bool.true_and,
    testBit_ruleBits, hS]
  simp only [step]
  cases hc : p.isCell
  · simp [cellAx, hc]
  · have hax : ∀ a, cellAx p a = decide (p.axis = a) := by intro a; simp [cellAx, hc]
    simp only [hax, Bool.true_and]
    cases hpa : p.axis <;> simp [← val_ctrAx S p hp, hpa]

theorem bcfg_core (S : Nat) (hS : S &&& core = S) (p : Pt) (h : bcfg S p = true) : inCoreP p := by
  simp only [bcfg, Bool.and_eq_true] at h
  obtain ⟨hb, ht⟩ := h
  have : core.testBit (idx p) = true := by
    rw [← hS, Nat.testBit_and] at ht
    simp only [Bool.and_eq_true] at ht
    exact ht.2
  rw [testBit_core] at this
  obtain ⟨c1, c2, c3, _⟩ := idx_coords p hb
  simp only [decide_eq_true_eq, c1, c2, c3] at this
  simp only [inBox, decide_eq_true_eq] at hb
  simp only [inCoreP]
  omega

theorem step_not_interior (S : Nat) (hS : S &&& core = S) (p : Pt) (hp : interior p = false) :
    step (bcfg S) p = false := by
  have hnc : ∀ q, Near 2 p q → bcfg S q = false := by
    intro q hq
    cases h : bcfg S q with
    | false => rfl
    | true =>
      have := bcfg_core S hS q h
      simp only [interior, decide_eq_false_iff_not] at hp
      simp only [Near, inCoreP] at hq this
      omega
  apply step_dead_of_count_le_three (hnc p (by simp [Near]))
  have : count (bcfg S) p = 0 := by
    unfold count
    rw [List.countP_eq_zero]
    intro q hq
    simp [hnc q (nbrs_near p q hq)]
  omega

/-- **The bit-parallel stepper is `step`**, for every configuration in the core. -/
theorem bstep_spec (S : Nat) (hS : S &&& core = S) : bcfg (bstep S) = step (bcfg S) := by
  funext p
  cases hi : interior p
  · rw [step_not_interior S hS p hi]
    simp only [bcfg]
    cases hb : inBox p
    · rfl
    · simp only [Bool.true_and, bstep, bstepAx, Nat.testBit_or, Nat.testBit_and, testBit_mask _ p hb, hi,
        Bool.false_and, Bool.or_false]
  · have hb : inBox p = true := by
      simp only [interior, inBox, decide_eq_true_eq] at hi ⊢; omega
    simp only [bcfg, hb, Bool.true_and]
    exact testBit_bstep_interior S p hi

/-! ### Orbits and oscillators -/

/-- All live points in the core. -/
def inCore (S : Nat) : Bool := S &&& core == S

theorem inCore_iff (S : Nat) : inCore S = true ↔ S &&& core = S := by simp [inCore]

/-- Configurations in the core are equal iff their numbers are. -/
theorem bcfg_inj {S T : Nat} (hS : S &&& core = S) (hT : T &&& core = T) (h : bcfg S = bcfg T) : S = T := by
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < 262144
  · have := congrFun h (ptOf i)
    simp only [bcfg, inBox_ptOf i hi, idx_ptOf i hi, Bool.true_and] at this
    exact this
  · have hc : core.testBit i = false := by
      rw [testBit_core]
      simp only [decide_eq_false_iff_not]
      omega
    rw [← hS, ← hT, Nat.testBit_and, Nat.testBit_and, hc]
    simp

/-- n generations, bit-parallel. -/
def brun (S : Nat) : Nat → Nat
  | 0 => S
  | n + 1 => bstep (brun S n)

theorem run_brun (S : Nat) : ∀ n, (∀ j, j < n → inCore (brun S j) = true) → run (bcfg S) n = bcfg (brun S n)
  | 0, _ => rfl
  | n + 1, h => by
    rw [run, run_brun S n (fun j hj => h j (by omega)), brun,
      bstep_spec _ ((inCore_iff _).mp (h n (by omega)))]

theorem brun_shift (S : Nat) : ∀ j, brun (bstep S) j = brun S (j + 1)
  | 0 => rfl
  | j + 1 => by rw [brun, brun_shift S j]; rfl

/-- `bOsc S0 k S`: the states S, bstep S, ..., k steps on, stay in the core; the first k differ from S0
and the last equals it. -/
def bOsc (S0 : Nat) : Nat → Nat → Bool
  | 0, S => inCore S && S == S0
  | k + 1, S => inCore S && S != S0 && bOsc S0 k (bstep S)

theorem bOsc_spec (S0 : Nat) : ∀ k S, bOsc S0 k S = true →
    (∀ j, j ≤ k → inCore (brun S j) = true) ∧ brun S k = S0 ∧ ∀ j, j < k → brun S j ≠ S0
  | 0, S, h => by
    simp only [bOsc, Bool.and_eq_true, beq_iff_eq] at h
    refine ⟨fun j hj => ?_, h.2, fun j hj => absurd hj (Nat.not_lt_zero j)⟩
    rw [show j = 0 by omega]
    exact h.1
  | k + 1, S, h => by
    simp only [bOsc, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
    obtain ⟨⟨h1, h2⟩, h3⟩ := h
    obtain ⟨i1, i2, i3⟩ := bOsc_spec S0 k (bstep S) h3
    refine ⟨fun j hj => ?_, by rw [← brun_shift]; exact i2, fun j hj => ?_⟩
    · cases j with
      | zero => exact h1
      | succ j => rw [← brun_shift]; exact i1 j (by omega)
    · cases j with
      | zero => exact h2
      | succ j => rw [← brun_shift]; exact i3 j (by omega)

/-- S is an oscillator of exact period P (a still life if P = 1), staying in the core. -/
def isOscB (S P : Nat) : Bool := match P with
  | 0 => false
  | k + 1 => bOsc S k (bstep S)

theorem isOscB_spec (S P : Nat) (hS : inCore S = true) (h : isOscB S P = true) :
    0 < P ∧ run (bcfg S) P = bcfg S ∧ ∀ k, 0 < k → k < P → run (bcfg S) k ≠ bcfg S := by
  cases P with
  | zero => simp [isOscB] at h
  | succ k =>
    obtain ⟨i1, i2, i3⟩ := bOsc_spec S k (bstep S) h
    have core_all : ∀ j, j ≤ k + 1 → inCore (brun S j) = true := by
      intro j hj
      cases j with
      | zero => exact hS
      | succ j => rw [← brun_shift]; exact i1 j (by omega)
    have hrun : ∀ m, m ≤ k + 1 → run (bcfg S) m = bcfg (brun S m) :=
      fun m hm => run_brun S m (fun j hj => core_all j (by omega))
    refine ⟨Nat.succ_pos k, ?_, fun m hm0 hmP => ?_⟩
    · rw [hrun (k + 1) (by omega), ← brun_shift, i2]
    · rw [hrun m (by omega)]
      intro he
      obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
      have := bcfg_inj ((inCore_iff _).mp (core_all (j + 1) (by omega))) ((inCore_iff _).mp hS) he
      rw [← brun_shift] at this
      exact i3 j (by omega) this

/-! ### From a list of points -/

/-- The number of a finite list of points. -/
def ofList (L : List Pt) : Nat := L.foldl (fun S p => S ||| (1 <<< idx p)) 0

theorem testBit_foldl (i : Nat) : ∀ (L : List Pt) (S : Nat),
    (L.foldl (fun S p => S ||| (1 <<< idx p)) S).testBit i = (S.testBit i || L.any (fun p => idx p == i))
  | [], S => by simp
  | p :: L, S => by
    rw [List.foldl_cons, testBit_foldl i L, Nat.testBit_or, Nat.shiftLeft_eq, Nat.one_mul, Nat.testBit_two_pow,
      List.any_cons]
    cases S.testBit i <;> cases L.any (fun p => idx p == i) <;> by_cases he : idx p = i <;> simp [he]

theorem bcfg_ofList (L : List Pt) (h : L.all inBox = true) : bcfg (ofList L) = lcfg L := by
  funext p
  apply Bool.eq_iff_iff.mpr
  rw [lcfg_iff]
  simp only [List.all_eq_true] at h
  simp only [bcfg, ofList, testBit_foldl, Nat.zero_testBit, Bool.false_or, Bool.and_eq_true, List.any_eq_true,
    beq_iff_eq]
  constructor
  · rintro ⟨hb, q, hq, he⟩
    rw [← idx_inj (h q hq) hb he]
    exact hq
  · intro hp
    exact ⟨h p hp, p, hp, rfl⟩


end Gump.Call.Box
