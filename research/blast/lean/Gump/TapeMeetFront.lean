/-
**Fronts: the meetings of section 31 that do not vanish** (`research/signals/README.md` section 31; REVIEW-signals-6
§3, `glue6.py`). Once the two edges of a front have formed, the configuration four generations later is the present
one with everything at and below a seam m moved two units down (with the stream) and everything above it moved two
units up, while the units around the seam hold a medium (wire B) that is unchanged by those moves: `rigid_front`,
the chart argument of section 21 as a theorem. With the base runs checked by the kernel (`chainUH_ok`) this gives the
meeting U–H for every distance (`meet_U_H`): wire B between a lower edge running down with the stream and an upper
edge running up.
-/
import Gump.TapeMeet
import Gump.TapeMeetData

namespace Gump.Tape.Signals
open Gump Gump.Tape Gump.Bits

/-! ### Rigid fronts, in general -/

/-- The configuration with its units ≤ m moved two units down and its units > m moved two units up. -/
def front (m : Int) (C : Config) : Config := glue m (shiftC (-2) C) (shiftC 2 C)

theorem step_shiftC (k : Int) (C : Config) : step (shiftC k C) = shiftC k (step C) := run_shiftC k C 1

theorem shiftC_neg_of (C : Config) (h : shiftC 2 C = C) (q : Pt) : C (shiftPt 2 q) = C q := by
  have := congrFun h (shiftPt 2 q)
  simp only [shiftC, shiftPt_shiftPt, show (-2 : Int) + 2 = 0 from rfl, shiftPt_zero] at this
  exact this.symm

theorem shiftC_pos_of (C : Config) (h : shiftC 2 C = C) (q : Pt) : C (shiftPt (-2) q) = C q := by
  have := congrFun h q
  simp only [shiftC] at this
  exact this

/-- **A rigid front.** If four generations after g the configuration is its front, and the units m − 2 .. m + 3 hold
at g .. g + 3 a medium unchanged by moves of two units and periodic in time with period 4, then so for ever. -/
theorem rigid_front (S M : Nat → Config) (hS : ∀ t, S (t + 1) = step (S t)) (hM2 : ∀ t, shiftC 2 (M t) = M t)
    (hM4 : ∀ t, M (t + 4) = M t) (m : Int) (g : Nat) (h4 : S (g + 4) = front m (S g))
    (hI : ∀ r, r < 4 → ∀ q, m - 2 ≤ unitOf q → unitOf q ≤ m + 3 → S (g + r) q = M (g + r) q) :
    ∀ s, S (g + s + 4) = front m (S (g + s)) ∧
      ∀ q, m - 2 ≤ unitOf q → unitOf q ≤ m + 3 → S (g + s) q = M (g + s) q := by
  let I := fun s => ∀ q, m - 2 ≤ unitOf q → unitOf q ≤ m + 3 → S (g + s) q = M (g + s) q
  let P := fun s => S (g + s + 4) = front m (S (g + s))
  have stepP : ∀ s, P s → I s → P (s + 1) := by
    intro s hp hi
    show S (g + (s + 1) + 4) = front m (S (g + (s + 1)))
    rw [show g + (s + 1) + 4 = (g + s + 4) + 1 by omega, hS, hp, show g + (s + 1) = (g + s) + 1 by omega, hS]
    unfold front
    apply glue_step m
    · intro p _; rw [step_shiftC]
    · intro p _; rw [step_shiftC]
    · intro p h1 h2
      simp only [shiftC]
      rw [show - -(2 : Int) = 2 by omega, hi _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
        hi _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
        shiftC_neg_of _ (hM2 _), shiftC_pos_of _ (hM2 _)]
  have stepI : ∀ s, P s → I s → I (s + 4) := by
    intro s hp hi q h1 h2
    show S (g + (s + 4)) q = M (g + (s + 4)) q
    rw [show g + (s + 4) = g + s + 4 by omega, hp, hM4]
    unfold front
    simp only [glue, shiftC]
    split
    · rw [show - -(2 : Int) = 2 by omega, hi _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega),
        shiftC_neg_of _ (hM2 _)]
    · rw [hi _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega), shiftC_pos_of _ (hM2 _)]
  have Q : ∀ s, P s ∧ I s ∧ I (s + 1) ∧ I (s + 2) ∧ I (s + 3) := by
    intro s
    induction s with
    | zero =>
      exact ⟨by simpa [P] using h4, fun q => hI 0 (by omega) q, fun q => hI 1 (by omega) q,
        fun q => hI 2 (by omega) q, fun q => hI 3 (by omega) q⟩
    | succ s ih =>
      obtain ⟨p0, i0, i1, i2, i3⟩ := ih
      exact ⟨stepP s p0 i0, i1, i2, i3, stepI s p0 i0⟩
  exact fun s => ⟨(Q s).1, (Q s).2.1⟩

theorem front_shift (m : Int) (n : Int) (C : Config) : front (m + n) (shiftC n C) = shiftC n (front m C) := by
  funext p
  simp only [front, glue, shiftC, unitOf_shiftPt, shiftPt_shiftPt]
  by_cases h : unitOf p ≤ m + n
  · rw [if_pos h, if_pos (by omega)]; congr 1; congr 1; omega
  · rw [if_neg h, if_neg (by omega)]; congr 1; congr 1; omega

/-! ### Wire B, the medium of the fronts U–H and E–H -/

/-- Wire B's unit at the odd generations of wire B (`sat_writer.py --selftest`). -/
def BOc : List Pt := [⟨0, 0, 1⟩, ⟨0, 0, 5⟩, ⟨0, 1, 2⟩, ⟨0, 1, 4⟩, ⟨1, 2, 2⟩]

def BEc : List Pt := [⟨0, 1, 2⟩, ⟨0, 1, 4⟩, ⟨1, 0, 0⟩, ⟨1, 0, 2⟩, ⟨1, 0, 4⟩]

/-- **Wire B** at meeting generation t (its odd phase `BOc` when t is even, its even phase `BEc`, the letter B of the
tape, when t is odd). -/
def wireB (t : Nat) : Config := ucfg (fun _ => if t % 2 = 0 then BOc else BEc)

theorem ucfg_const_shift (L : List Pt) (k : Int) : shiftC k (ucfg (fun _ => L)) = ucfg (fun _ => L) := by
  funext p
  simp only [shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  congr 2; omega

theorem wireB_shift (t : Nat) (k : Int) : shiftC k (wireB t) = wireB t := ucfg_const_shift _ k

theorem wireB_four (t : Nat) : wireB (t + 4) = wireB t := by
  simp only [wireB, show (t + 4) % 2 = t % 2 by omega]

def wbFrame : Pt := ⟨0, 8, 16⟩

theorem wbFrame_even : wbFrame.even := by
  show (0 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

def wireBCheck : Bool :=
  pieceCheck (fun _ => BOc) (fun _ => BEc) (-1) 3 [] [] 1 0 0 wbFrame &&
  pieceCheck (fun _ => BEc) (fun _ => BOc) (-1) 3 [] [] 1 0 0 wbFrame

theorem wireBCheck_ok : wireBCheck = true := by decide +kernel

theorem const_unit (L : List Pt) (h : ∀ q ∈ L, unitOf q = 0) : ∀ u : Int, ∀ q ∈ (fun _ : Int => L) u, unitOf q = 0 :=
  fun _ => h

/-- Wire B is an orbit, of period 2. -/
theorem wireB_step (t : Nat) : step (wireB t) = wireB (t + 1) := by
  have hc := wireBCheck_ok
  simp only [wireBCheck, Bool.and_eq_true] at hc
  have hO : ∀ q ∈ BOc, unitOf q = 0 := by decide
  have hE : ∀ q ∈ BEc, unitOf q = 0 := by decide
  have hwb : ∀ t : Nat, wireB t = ucfg (fun _ => if t % 2 = 0 then BOc else BEc) := fun _ => rfl
  have local0 : ∀ p, unitOf p = 0 → step (wireB t) p = wireB (t + 1) p := by
    intro p hp
    rcases Nat.mod_two_eq_zero_or_one t with h | h
    · have e1 : wireB t = ucfg (fun _ => BOc) := by rw [hwb, if_pos h]
      have e2 : wireB (t + 1) = ucfg (fun _ => BEc) := by rw [hwb, if_neg (by omega)]
      rw [e1, e2]
      have := pieceCheck_spec (const_unit _ hO) (const_unit _ hE) wbFrame_even hc.1 (by decide) (by decide)
        (by decide) (by decide) (by decide) (ucfg (fun _ => BOc)) (fun q _ _ => by simp [xorC, lcfg_nil']) p
        (by omega) (by omega)
      rw [show step (ucfg (fun _ => BOc)) p = run (ucfg (fun _ => BOc)) 1 p from rfl, this]
      simp [xorC, lcfg_nil']
    · have e1 : wireB t = ucfg (fun _ => BEc) := by rw [hwb, if_neg (by omega)]
      have e2 : wireB (t + 1) = ucfg (fun _ => BOc) := by rw [hwb, if_pos (by omega)]
      rw [e1, e2]
      have := pieceCheck_spec (const_unit _ hE) (const_unit _ hO) wbFrame_even hc.2 (by decide) (by decide)
        (by decide) (by decide) (by decide) (ucfg (fun _ => BEc)) (fun q _ _ => by simp [xorC, lcfg_nil']) p
        (by omega) (by omega)
      rw [show step (ucfg (fun _ => BEc)) p = run (ucfg (fun _ => BEc)) 1 p from rfl, this]
      simp [xorC, lcfg_nil']
  funext p
  have a := congrFun (step_shiftC (unitOf p) (wireB t)) (shiftPt (unitOf p) (shiftPt (-unitOf p) p))
  rw [wireB_shift] at a
  simp only [shiftC] at a
  rw [shiftPt_shiftPt_neg] at a
  rw [a, local0 _ (by simp only [unitOf_shiftPt]; omega)]
  have b := congrFun (wireB_shift (t + 1) (unitOf p)) p
  simp only [shiftC] at b
  exact b

/-! ### Chains of kernel steps on the train -/

/-- k generations of train(s) ⊕ σ give train(s + k) ⊕ σ', checked on the units lo .. hi in the box moved by V. -/
def stepCheck (s k : Nat) (σ σ' : List Pt) (lo hi : Int) (V : Pt) : Bool :=
  pieceCheck (trainF s) (trainF (s + k)) (lo - k) (hi - lo + 1 + 2 * k).toNat σ σ' k lo hi V &&
  σ.all (fun q => decide (lo + k ≤ unitOf q ∧ unitOf q ≤ hi - k)) &&
  σ'.all (fun q => decide (lo ≤ unitOf q ∧ unitOf q ≤ hi)) &&
  decide (V.x % 2 = 0 ∧ V.y % 2 = 0 ∧ V.z % 2 = 0) && decide (-8 ≤ lo + V.x / 2 ∧ hi + V.x / 2 ≤ 23)

theorem stepCheck_spec {s k : Nat} {σ σ' : List Pt} {lo hi : Int} {V : Pt} (h : stepCheck s k σ σ' lo hi V = true) :
    run (xorC (train s) (lcfg σ)) k = xorC (train (s + k)) (lcfg σ') := by
  simp only [stepCheck, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨⟨hc, hσ⟩, hσ'⟩, hV⟩, hb⟩ := h
  funext p
  by_cases hin : lo ≤ unitOf p ∧ unitOf p ≤ hi
  · exact pieceCheck_spec (trainF_unit s) (trainF_unit (s + k)) hV hc hb.1 hb.2 (by omega) (by omega)
      (by omega) _ (fun q _ _ => rfl) p hin.1 hin.2
  · have away : ∀ q, unitOf p - k ≤ unitOf q → unitOf q ≤ unitOf p + k → xorC (train s) (lcfg σ) q = train s q := by
      intro q q1 q2
      simp only [xorC]
      cases e : lcfg σ q
      · simp
      · have := hσ q ((lcfg_iff _ _).mp e); omega
    rw [run_eq_of_units k away, train_run]
    simp only [xorC]
    cases e : lcfg σ' p
    · simp
    · have := hσ' p ((lcfg_iff _ _).mp e); omega

/-- The list of a front: σ moved down two units on the units ≤ m, up two units above. -/
def frontList (m : Int) (σ : List Pt) : List Pt :=
  (σ.map (shiftPt (-2))).filter (fun q => decide (unitOf q ≤ m)) ++
    (σ.map (shiftPt 2)).filter (fun q => decide (m < unitOf q))

theorem train_four (t : Nat) : train (t + 4) = train t := by
  rw [show t + 4 = (t + 2) + 2 by omega, train_shift, train_shift]
  funext p; simp only [shiftC, shiftPt_shiftPt]
  have := congrFun (train_shift_even t 2 (by decide)) (shiftPt 2 p)
  simp only [shiftC, shiftPt_shiftPt] at this
  rw [show - -(1 : Int) + - -1 = 2 by omega, ← this, show (-2 : Int) + 2 = 0 by omega, shiftPt_zero]

/-- A front of train(s) ⊕ σ is train(s + 4) ⊕ the front list. -/
theorem front_xor (m : Int) (s : Nat) (σ : List Pt) :
    front m (xorC (train s) (lcfg σ)) = xorC (train (s + 4)) (lcfg (frontList m σ)) := by
  funext q
  rw [train_four]
  simp only [front, glue, shiftC, xorC, frontList, lcfg_append', lcfg_filter]
  have e1 := congrFun (train_shift_even s (-2) (by decide)) q
  have e2 := congrFun (train_shift_even s 2 (by decide)) q
  have f1 := congrFun (lcfg_map_shiftPt (-2) σ) q
  have f2 := congrFun (lcfg_map_shiftPt 2 σ) q
  simp only [shiftC] at e1 e2 f1 f2
  split
  · rename_i h
    rw [e1, ← f1, decide_eq_true h, decide_eq_false (by omega)]; simp
  · rename_i h
    rw [e2, ← f2, decide_eq_false h, decide_eq_true (by omega)]; simp

/-- A unit of train(s) ⊕ σ holding the cells L. -/
def unitIs (s : Nat) (σ : List Pt) (u : Int) (L : List Pt) : Bool :=
  sameL (symDiff ((trainBase (s % 4) (u % 2).toNat).map (shiftPt u)) (σ.filter (fun q => decide (unitOf q = u))))
    (L.map (shiftPt u)) &&
  L.all (fun q => decide (unitOf q = 0))

theorem unitIs_spec {s : Nat} {σ : List Pt} {u : Int} {L : List Pt} (h : unitIs s σ u L = true) (q : Pt)
    (hq : unitOf q = u) : xorC (train s) (lcfg σ) q = ucfg (fun _ => L) q := by
  simp only [unitIs, Bool.and_eq_true] at h
  have e := (sameL_iff _ _).mp h.1
  have e' := congrFun e q
  rw [lcfg_symDiff, lcfg_filter, lcfg_map_shiftPt, lcfg_map_shiftPt] at e'
  simp only [shiftC, hq, decide_true, Bool.and_true] at e'
  simp only [xorC, train, ucfg, trainF, hq]
  exact e'

theorem chain_next {P : Config} {d : Nat → List Pt} {t k : Nat} {lo hi : Int} {V : Pt}
    (h : run P t = xorC (train (1 + t)) (lcfg (d t))) (c : stepCheck (1 + t) k (d t) (d (t + k)) lo hi V = true) :
    run P (t + k) = xorC (train (1 + (t + k))) (lcfg (d (t + k))) := by
  rw [run_add, h, stepCheck_spec c, Nat.add_assoc]

/-- The front law and the medium, from the kernel's facts at generations g .. g + 4. -/
theorem front_of_facts (P : Config) (d : Nat → List Pt) (m : Int) (g : Nat)
    (e : ∀ r, r ≤ 4 → run P (g + r) = xorC (train (1 + (g + r))) (lcfg (d (g + r))))
    (h4 : sameL (d (g + 4)) (frontList m (d g)) = true)
    (hI : ∀ r, r < 4 → ∀ i : Nat, i < 6 → unitIs (1 + (g + r)) (d (g + r)) (m - 2 + i)
      (if (g + r) % 2 = 0 then BOc else BEc) = true) :
    ∀ s, run P (g + s + 4) = front m (run P (g + s)) ∧
      ∀ q, m - 2 ≤ unitOf q → unitOf q ≤ m + 3 → run P (g + s) q = wireB (g + s) q := by
  apply rigid_front (fun t => run P t) wireB (fun t => rfl) (fun t => wireB_shift t 2) wireB_four m g
  · show run P (g + 4) = front m (run P g)
    have e0 := e 0 (by decide)
    simp only [Nat.add_zero] at e0
    rw [e 4 (by decide), e0, front_xor, (sameL_iff _ _).mp h4, show 1 + g + 4 = 1 + (g + 4) by omega]
  · intro r hr q h1 h2
    show run P (g + r) q = wireB (g + r) q
    rw [e r (by omega)]
    have hc := hI r hr (unitOf q - (m - 2)).toNat (by omega)
    rw [show m - 2 + (((unitOf q - (m - 2)).toNat : Nat) : Int) = unitOf q by omega] at hc
    exact unitIs_spec hc q rfl

/-! ### A medium given by its unit at each phase and parity (the holed train of E–K0) -/

/-- The medium whose unit u at generation t is `med (t % 4) (u % 2)`. -/
def medC (med : Nat → Nat → List Pt) (t : Nat) : Config := ucfg (fun u => med (t % 4) (u % 2).toNat)

theorem medC_shift2 (med : Nat → Nat → List Pt) (t : Nat) : shiftC 2 (medC med t) = medC med t := by
  funext p
  simp only [shiftC, medC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  rw [show (unitOf p + -2) % 2 = unitOf p % 2 by omega, show -(unitOf p + -2) + -2 = -unitOf p by omega]

theorem medC_four (med : Nat → Nat → List Pt) (t : Nat) : medC med (t + 4) = medC med t := by
  simp only [medC, show (t + 4) % 4 = t % 4 by omega]

theorem front_of_facts_med (P : Config) (d : Nat → List Pt) (med : Nat → Nat → List Pt) (m : Int) (g : Nat)
    (e : ∀ r, r ≤ 4 → run P (g + r) = xorC (train (1 + (g + r))) (lcfg (d (g + r))))
    (h4 : sameL (d (g + 4)) (frontList m (d g)) = true)
    (hI : ∀ r, r < 4 → ∀ i : Nat, i < 6 → unitIs (1 + (g + r)) (d (g + r)) (m - 2 + i)
      (med ((g + r) % 4) ((m - 2 + i) % 2).toNat) = true) :
    ∀ s, run P (g + s + 4) = front m (run P (g + s)) ∧
      ∀ q, m - 2 ≤ unitOf q → unitOf q ≤ m + 3 → run P (g + s) q = medC med (g + s) q := by
  apply rigid_front (fun t => run P t) (medC med) (fun t => rfl) (fun t => medC_shift2 med t) (medC_four med) m g
  · show run P (g + 4) = front m (run P g)
    have e0 := e 0 (by decide)
    simp only [Nat.add_zero] at e0
    rw [e 4 (by decide), e0, front_xor, (sameL_iff _ _).mp h4, show 1 + g + 4 = 1 + (g + 4) by omega]
  · intro r hr q h1 h2
    show run P (g + r) q = medC med (g + r) q
    rw [e r (by omega)]
    have hc := hI r hr (unitOf q - (m - 2)).toNat (by omega)
    rw [show m - 2 + (((unitOf q - (m - 2)).toNat : Nat) : Int) = unitOf q by omega] at hc
    exact unitIs_spec hc q rfl

end Gump.Tape.Signals
