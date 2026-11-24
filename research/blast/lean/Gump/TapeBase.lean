/-
The tools every "for every N" law of the signals catalogue needs (`research/signals/README.md` sections 10, 11, 21):
units of a wire, translation along it, the locality of the rule in units, the gluing of two orbits along a seam,
and kernel-checkable certificates that compare two configurations on a range of units.

The wires of the catalogue run along v = (1, 0, −1); one unit is the move τ = (2, 0, −2) in doubled coordinates,
and the unit of a point is ⌊x / 2⌋ (the scripts' `c[0] >> 1`). A neighbour changes x by at most 2, so it lies in
the same unit or the next one on either side: n generations of a unit read only the n units on either side.
-/
import Gump.Bits
import Gump.Equivariance

namespace Gump.Tape
open Gump

/-! ### Units and the move along the wire -/

/-- The unit of the wire a point lies in: ⌊x / 2⌋. -/
def unitOf (p : Pt) : Int := p.x / 2

/-- p moved k units of the wire towards +v, i.e. by k·(2, 0, −2). -/
def shiftPt (k : Int) (p : Pt) : Pt := ⟨p.x + 2 * k, p.y, p.z - 2 * k⟩

@[simp] theorem unitOf_shiftPt (k : Int) (p : Pt) : unitOf (shiftPt k p) = unitOf p + k := by
  simp only [unitOf, shiftPt]; omega

@[simp] theorem shiftPt_shiftPt (j k : Int) (p : Pt) : shiftPt j (shiftPt k p) = shiftPt (j + k) p := by
  apply Pt.ext' <;> simp only [shiftPt] <;> omega

@[simp] theorem shiftPt_zero (p : Pt) : shiftPt 0 p = p := by
  simp only [shiftPt]; apply Pt.ext' <;> simp

theorem shiftPt_neg_shiftPt (k : Int) (p : Pt) : shiftPt (-k) (shiftPt k p) = p := by
  rw [shiftPt_shiftPt, show -k + k = 0 by omega, shiftPt_zero]

theorem shiftPt_shiftPt_neg (k : Int) (p : Pt) : shiftPt k (shiftPt (-k) p) = p := by
  rw [shiftPt_shiftPt, show k + -k = 0 by omega, shiftPt_zero]

/-- A configuration moved k units towards +v. -/
def shiftC (k : Int) (c : Config) : Config := fun p => c (shiftPt (-k) p)

/-- The identity of O_h. -/
def symId : Sym := ⟨Perm3.id, true, true, true⟩

theorem symId_act (v p : Pt) : symId.act v p = p + v := by
  obtain ⟨x, y, z⟩ := p
  simp only [Sym.act, Sym.apply, symId, Perm3.apply, sg]
  rfl

/-- **Translations by even vectors commute with `run`.** -/
theorem run_translate (c : Config) {v : Pt} (hv : v.even) (n : Nat) :
    run (fun p => c (p + v)) n = fun p => run c n (p + v) := by
  have := run_act symId hv c n
  simp only [symId_act] at this
  exact this

theorem shiftPt_eq_add (k : Int) (p : Pt) : shiftPt k p = p + ⟨2 * k, 0, -2 * k⟩ := by
  simp only [shiftPt]; apply Pt.ext' <;> simp <;> omega

/-- **The move along the wire commutes with `run`.** -/
theorem run_shiftC (k : Int) (c : Config) (n : Nat) : run (shiftC k c) n = shiftC k (run c n) := by
  have hv : (⟨2 * -k, 0, -2 * -k⟩ : Pt).even := by simp only [Pt.even]; omega
  have := run_translate c hv n
  unfold shiftC
  simp only [shiftPt_eq_add]
  exact this

/-! ### Locality in units -/

theorem near_unitOf {r : Nat} {p q : Pt} (h : Near (2 * r) p q) :
    unitOf p - r ≤ unitOf q ∧ unitOf q ≤ unitOf p + r := by
  simp only [Near] at h; simp only [unitOf]; omega

/-- **n generations of a point read only the n units on either side of its unit.** -/
theorem run_eq_of_units {c c' : Config} {p : Pt} (n : Nat)
    (h : ∀ q, unitOf p - n ≤ unitOf q → unitOf q ≤ unitOf p + n → c q = c' q) : run c n p = run c' n p := by
  refine light_cone (p := p) n 0 (fun q hq => ?_) p (by simp only [Near]; omega)
  rw [Nat.zero_add] at hq
  have := near_unitOf hq
  exact h q this.1 this.2

theorem step_eq_of_units {c c' : Config} {p : Pt}
    (h : ∀ q, unitOf p - 1 ≤ unitOf q → unitOf q ≤ unitOf p + 1 → c q = c' q) : step c p = step c' p :=
  run_eq_of_units (c := c) (c' := c') 1 (by simpa using h)

/-! ### Gluing two orbits along a seam -/

/-- X on the units ≤ m, Z on the units > m. -/
def glue (m : Int) (X Z : Config) : Config := fun p => if unitOf p ≤ m then X p else Z p

/-- **The seam.** If X obeys the rule on the units ≤ m, Z on the units ≥ m + 1, and the two agree on the units
m and m + 1, then the glued configuration steps to the glued successors. -/
theorem glue_step (m : Int) {X Z X' Z' : Config}
    (hX : ∀ p, unitOf p ≤ m → step X p = X' p)
    (hZ : ∀ p, m + 1 ≤ unitOf p → step Z p = Z' p)
    (hXZ : ∀ p, m ≤ unitOf p → unitOf p ≤ m + 1 → X p = Z p) :
    step (glue m X Z) = glue m X' Z' := by
  funext p
  simp only [glue]
  split
  · rename_i hp
    rw [← hX p hp]
    apply step_eq_of_units
    intro q h1 h2
    simp only [glue]
    split
    · rfl
    · exact (hXZ q (by omega) (by omega)).symm
  · rename_i hp
    rw [← hZ p (by omega)]
    apply step_eq_of_units
    intro q h1 h2
    simp only [glue]
    split
    · exact hXZ q (by omega) (by omega)
    · rfl

/-- **Gluing orbits.** Under the same three conditions at every generation, the glued sequence is the orbit of
the glued start. -/
theorem glue_run (m : Int) (X Z : Nat → Config)
    (hX : ∀ t p, unitOf p ≤ m → step (X t) p = X (t + 1) p)
    (hZ : ∀ t p, m + 1 ≤ unitOf p → step (Z t) p = Z (t + 1) p)
    (hXZ : ∀ t p, m ≤ unitOf p → unitOf p ≤ m + 1 → X t p = Z t p) :
    ∀ t, run (glue m (X 0) (Z 0)) t = glue m (X t) (Z t)
  | 0 => rfl
  | t + 1 => by rw [run, glue_run m X Z hX hZ hXZ t, glue_step m (hX t) (hZ t) (hXZ t)]

/-! ### Orbits that return: preperiod and period exactly -/

theorem run_succ_eq (c : Config) (n : Nat) : run c (n + 1) = step (run c n) := rfl

/-- Periodic from μ with period 4: every later state returns after every multiple of 4. -/
theorem periodic_from (c : Config) (μ : Nat) (h : run c (μ + 4) = run c μ) :
    ∀ t, μ ≤ t → run c (t + 4) = run c t := by
  intro t ht
  obtain ⟨d, rfl⟩ : ∃ d, t = μ + d := ⟨t - μ, by omega⟩
  induction d with
  | zero => exact h
  | succ d ih =>
    rw [show μ + (d + 1) + 4 = (μ + d + 4) + 1 by omega, show μ + (d + 1) = (μ + d) + 1 by omega]
    exact congrArg step (ih (by omega))

theorem return_mul (c : Config) {s p : Nat} (h : ∀ t, s ≤ t → run c (t + p) = run c t) :
    ∀ q t, s ≤ t → run c (t + p * q) = run c t
  | 0, t, _ => rfl
  | q + 1, t, ht => by
    rw [show t + p * (q + 1) = (t + p * q) + p by rw [Nat.mul_succ, Nat.add_assoc], h _ (by omega),
      return_mul c h q t ht]

theorem return_forever (c : Config) {s p : Nat} (h : run c (s + p) = run c s) :
    ∀ t, s ≤ t → run c (t + p) = run c t := by
  intro t ht
  obtain ⟨d, rfl⟩ : ∃ d, t = s + d := ⟨t - s, by omega⟩
  induction d with
  | zero => exact h
  | succ d ih =>
    rw [show s + (d + 1) + p = (s + d + p) + 1 by omega, show s + (d + 1) = (s + d) + 1 by omega]
    exact congrArg step (ih (by omega))

/-- **An orbit with preperiod exactly μ and period exactly 4.** If the state at μ returns after 4 generations
and not after 2, and the state at μ − 1 does not return after 4, then the state at s returns after p > 0
generations exactly when s ≥ μ and 4 divides p. -/
theorem orbit_classify (c : Config) (μ : Nat) (hμ : 1 ≤ μ) (h4 : run c (μ + 4) = run c μ)
    (h2 : run c (μ + 2) ≠ run c μ) (ht : run c (μ + 3) ≠ run c (μ - 1)) :
    ∀ s p, 0 < p → (run c (s + p) = run c s ↔ μ ≤ s ∧ p % 4 = 0) := by
  have per := periodic_from c μ h4
  have per' : ∀ q t, μ ≤ t → run c (t + 4 * q) = run c t := return_mul c per
  -- no return after 1, 2 or 3 at any s ≥ μ
  have h1 : run c (μ + 1) ≠ run c μ := by
    intro e
    apply h2
    have : run c ((μ + 1) + 1) = run c (μ + 1) := congrArg step e
    rw [show μ + 1 + 1 = μ + 2 by omega, e] at this
    exact this
  have h3 : run c (μ + 3) ≠ run c μ := by
    intro e
    apply h1
    have : run c ((μ + 3) + 1) = run c (μ + 1) := congrArg step e
    rw [show μ + 3 + 1 = μ + 4 by omega, h4] at this
    exact this.symm
  have noret : ∀ r, 0 < r → r < 4 → ∀ s, μ ≤ s → run c (s + r) ≠ run c s := by
    intro r hr0 hr4 s hs e
    have fwd := return_forever c e
    -- move s forward to a multiple of 4 past μ
    obtain ⟨d, rfl⟩ : ∃ d, s = μ + d := ⟨s - μ, by omega⟩
    have e' : run c (μ + 4 * (d + 1) + r) = run c (μ + 4 * (d + 1)) :=
      fwd _ (by omega)
    rw [show μ + 4 * (d + 1) + r = (μ + r) + 4 * (d + 1) by omega, per' _ _ (by omega),
      per' _ _ (by omega)] at e'
    rcases (show r = 1 ∨ r = 2 ∨ r = 3 by omega) with rfl | rfl | rfl
    · exact h1 e'
    · exact h2 e'
    · exact h3 e'
  intro s p hp
  constructor
  · intro e
    have fwd := return_forever c e
    have fwdq : ∀ q t, s ≤ t → run c (t + p * q) = run c t := return_mul c fwd
    have hs : μ ≤ s := by
      apply Classical.byContradiction
      intro hs
      apply ht
      have a := fwdq 4 (μ - 1) (by omega)
      rw [show μ - 1 + p * 4 = (μ + 3) + 4 * (p - 1) by
        have : 1 ≤ p := hp
        rw [Nat.mul_comm]; omega, per' _ _ (by omega)] at a
      exact a
    refine ⟨hs, ?_⟩
    apply Classical.byContradiction
    intro hr
    apply noret (p % 4) (by omega) (Nat.mod_lt _ (by decide)) s hs
    have := e
    rw [← Nat.mod_add_div p 4, show s + (p % 4 + 4 * (p / 4)) = (s + p % 4) + 4 * (p / 4) by omega,
      per' _ _ (by omega)] at this
    exact this
  · rintro ⟨hs, hp4⟩
    obtain ⟨q, rfl⟩ : ∃ q, p = 4 * q := ⟨p / 4, by omega⟩
    exact per' q s hs

/-! ### Lists of points moved along the wire and across the lattice -/

theorem lcfg_map_shiftPt (k : Int) (L : List Pt) : lcfg (L.map (shiftPt k)) = shiftC k (lcfg L) := by
  funext p
  apply Bool.eq_iff_iff.mpr
  simp only [shiftC, lcfg_iff, List.mem_map]
  constructor
  · rintro ⟨q, hq, rfl⟩
    rw [shiftPt_neg_shiftPt]; exact hq
  · intro h
    exact ⟨_, h, shiftPt_shiftPt_neg k p⟩

theorem Pt.add_neg_add (p v : Pt) : p + v + ⟨-v.x, -v.y, -v.z⟩ = p := by
  apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

theorem Pt.add_add_neg (p v : Pt) : p + ⟨-v.x, -v.y, -v.z⟩ + v = p := by
  apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

theorem lcfg_map_add (v : Pt) (L : List Pt) (p : Pt) : lcfg (L.map (· + v)) (p + v) = lcfg L p := by
  apply Bool.eq_iff_iff.mpr
  simp only [lcfg_iff, List.mem_map]
  constructor
  · rintro ⟨q, hq, e⟩
    have : q = p := by
      have := congrArg (· + ⟨-v.x, -v.y, -v.z⟩) e
      simp only [Pt.add_neg_add] at this
      exact this
    rw [← this]; exact hq
  · intro h; exact ⟨p, h, rfl⟩

/-- **A run of a list moved by an even vector** is the run of the list, moved. -/
theorem run_lcfg_map_add (L : List Pt) {v : Pt} (hv : v.even) (n : Nat) (p : Pt) :
    run (lcfg (L.map (· + v))) n (p + v) = run (lcfg L) n p := by
  have hv' : (⟨-v.x, -v.y, -v.z⟩ : Pt).even := by
    obtain ⟨a, b, c⟩ := hv; simp only [Pt.even]; omega
  have e : lcfg L = fun q => lcfg (L.map (· + v)) (q + v) := funext fun q => (lcfg_map_add v L q).symm
  rw [e, run_translate _ hv n]

/-! ### Certificates on ranges of units, for the bit-parallel stepper -/

open Bits

/-- The bits of the box whose x index (x + 16) lies in [lo, hi). -/
def xMask (lo hi : Nat) : Nat := rep2 (2 ^ hi - 2 ^ lo) 64 12

theorem testBit_xMask {lo hi : Nat} (h1 : lo ≤ hi) (h2 : hi ≤ 64) (i : Nat) :
    (xMask lo hi).testBit i = decide (i < 262144 ∧ lo ≤ i % 64 ∧ i % 64 < hi) := by
  have hp : 2 ^ hi - 2 ^ lo < 2 ^ 64 :=
    Nat.lt_of_lt_of_le (Nat.sub_lt (Nat.two_pow_pos hi) (Nat.two_pow_pos lo)) (two_pow_mono h2)
  rw [xMask, testBit_rep2 _ 64 hp, testBit_interval lo hi _ h1]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, show (64 * 2 ^ 12 : Nat) = 262144 from rfl]

/-- The points of the box in the units a .. b (box coordinates, −8 ≤ a, b ≤ 23). -/
def unitMask (a b : Int) : Nat := xMask (2 * a + 16).toNat (2 * b + 18).toNat

theorem testBit_unitMask {a b : Int} (ha : -8 ≤ a) (hb : b ≤ 23) (hab : a ≤ b + 1) (p : Pt)
    (hp : inBox p = true) :
    (unitMask a b).testBit (idx p) = decide (a ≤ unitOf p ∧ unitOf p ≤ b) := by
  obtain ⟨c1, -, -, c4⟩ := idx_coords p hp
  simp only [inBox, decide_eq_true_eq] at hp
  rw [unitMask, testBit_xMask (by omega) (by omega), c1]
  apply Bool.eq_iff_iff.mpr
  simp only [decide_eq_true_eq]
  simp only [unitOf]
  omega

/-- S and T agree on the bits of M. -/
def eqOn (M S T : Nat) : Bool := S &&& M == T &&& M

/-- **Agreement on a range of units**, read off two numbers. -/
theorem eqOn_spec {a b : Int} (ha : -8 ≤ a) (hb : b ≤ 23) (hab : a ≤ b + 1) {S T : Nat}
    (h : eqOn (unitMask a b) S T = true) (p : Pt) (h1 : a ≤ unitOf p) (h2 : unitOf p ≤ b) :
    bcfg S p = bcfg T p := by
  simp only [bcfg]
  cases hbx : inBox p
  · rfl
  · simp only [Bool.true_and]
    have e := congrArg (fun n => n.testBit (idx p)) (eq_of_beq h)
    simp only [Nat.testBit_and, testBit_unitMask ha hb hab p hbx, h1, h2] at e
    simpa using e

theorem bcfg_out {S : Nat} {p : Pt} (h : unitOf p < -8 ∨ 23 < unitOf p) : bcfg S p = false := by
  simp only [bcfg]
  have : inBox p = false := by
    simp only [inBox, decide_eq_false_iff_not]
    simp only [unitOf] at h
    omega
  rw [this, Bool.false_and]

/-- Agreement on all units ≤ b (the box ends at unit −8). -/
theorem eqOn_spec_le {b : Int} (hb : b ≤ 23) (hb' : -9 ≤ b) {S T : Nat}
    (h : eqOn (unitMask (-8) b) S T = true) (p : Pt) (h2 : unitOf p ≤ b) : bcfg S p = bcfg T p := by
  by_cases h1 : -8 ≤ unitOf p
  · exact eqOn_spec (by decide) hb (by omega) h p h1 h2
  · rw [bcfg_out (Or.inl (by omega)), bcfg_out (Or.inl (by omega))]

/-- Agreement on all units ≥ a (the box ends at unit 23). -/
theorem eqOn_spec_ge {a : Int} (ha : -8 ≤ a) (ha' : a ≤ 24) {S T : Nat}
    (h : eqOn (unitMask a 23) S T = true) (p : Pt) (h1 : a ≤ unitOf p) : bcfg S p = bcfg T p := by
  by_cases h2 : unitOf p ≤ 23
  · exact eqOn_spec ha (by decide) (by omega) h p h1 h2
  · rw [bcfg_out (Or.inr (by omega)), bcfg_out (Or.inr (by omega))]

/-- **Disagreement on a range of units**, read off two numbers. -/
theorem neqOn_spec {a b : Int} (ha : -8 ≤ a) (hb : b ≤ 23) (hab : a ≤ b + 1) {S T : Nat}
    (h : eqOn (unitMask a b) S T = false) : ∃ p, a ≤ unitOf p ∧ unitOf p ≤ b ∧ bcfg S p ≠ bcfg T p := by
  have hne : S &&& unitMask a b ≠ T &&& unitMask a b := by
    intro e; simp [eqOn, e] at h
  have : ∃ i, (S &&& unitMask a b).testBit i ≠ (T &&& unitMask a b).testBit i := by
    apply Classical.byContradiction
    intro hn
    apply hne
    apply Nat.eq_of_testBit_eq
    intro i
    apply Classical.byContradiction
    intro hi
    exact hn ⟨i, hi⟩
  obtain ⟨i, hi⟩ := this
  have hm : (unitMask a b).testBit i = true := by
    apply Classical.byContradiction
    intro hm
    simp only [Bool.not_eq_true] at hm
    simp [Nat.testBit_and, hm] at hi
  have hm' := hm
  rw [unitMask, testBit_xMask (by omega) (by omega)] at hm'
  simp only [decide_eq_true_eq] at hm'
  have hi' : i < 262144 := hm'.1
  refine ⟨ptOf i, ?_, ?_, ?_⟩
  · simp only [unitOf, ptOf]; omega
  · simp only [unitOf, ptOf]; omega
  · simp only [bcfg, inBox_ptOf i hi', idx_ptOf i hi', Bool.true_and]
    intro e
    apply hi
    simp only [Nat.testBit_and, hm, Bool.and_true, e]

/-- `agree M n A B`: the orbits of A and B stay in the core for n generations and agree on M at each of them. -/
def agree (M : Nat) : Nat → Nat → Nat → Bool
  | 0, A, B => inCore A && inCore B && eqOn M A B
  | n + 1, A, B => inCore A && inCore B && eqOn M A B && agree M n (bstep A) (bstep B)

theorem agree_spec (M : Nat) : ∀ n A B, agree M n A B = true → ∀ j, j ≤ n →
    inCore (brun A j) = true ∧ inCore (brun B j) = true ∧ eqOn M (brun A j) (brun B j) = true
  | 0, A, B, h, j, hj => by
    obtain rfl : j = 0 := by omega
    simp only [agree, Bool.and_eq_true] at h
    exact ⟨h.1.1, h.1.2, h.2⟩
  | n + 1, A, B, h, j, hj => by
    simp only [agree, Bool.and_eq_true] at h
    cases j with
    | zero => exact ⟨h.1.1.1, h.1.1.2, h.1.2⟩
    | succ j =>
      have := agree_spec M n _ _ h.2 j (by omega)
      rw [← brun_shift, ← brun_shift]
      exact this

/-- All states of the orbit of S up to generation n are in the core. -/
def coreRun (S : Nat) : Nat → Bool
  | 0 => inCore S
  | n + 1 => inCore S && coreRun (bstep S) n

theorem coreRun_spec : ∀ n S, coreRun S n = true → ∀ j, j ≤ n → inCore (brun S j) = true
  | 0, S, h, j, hj => by obtain rfl : j = 0 := by omega
                         exact h
  | n + 1, S, h, j, hj => by
    simp only [coreRun, Bool.and_eq_true] at h
    cases j with
    | zero => exact h.1
    | succ j => rw [← brun_shift]; exact coreRun_spec n _ h.2 j (by omega)

theorem run_bcfg_of_core {S n : Nat} (h : ∀ j, j < n → inCore (brun S j) = true) :
    run (bcfg S) n = bcfg (brun S n) := run_brun S n h

theorem brun_add (S : Nat) : ∀ a b, brun S (a + b) = brun (brun S a) b
  | a, 0 => rfl
  | a, b + 1 => by rw [← Nat.add_assoc, brun, brun, brun_add S a b]

end Gump.Tape
