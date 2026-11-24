/-
**The call law, part (a)**: the line never feels the store wire (`research/audit/REVIEW-signals-9.md` section 3, P2).
For every k ≥ 1 and every generation t, the whole state is the disjoint union of V_k(t) (the store wire alone, e1
forced at 29) and Lf(t) (the line with the CALL alone): `call_law_a`; with `call_law_b`, `call_law : CallLaw`.

The proof is the review's, with every step a theorem. V_k stays in the tube H_V (1 ≤ x+y+z ≤ 5, −1 ≤ x−y+z ≤ 5:
`confinement` on four diagonals) and Lf in its diagonal hull H_L (`hull`), where x − y + z ≤ −5: so the two parts are
disjoint, and at a cell whose closed neighbourhood misses one of them the union steps to the union (`step_or`). The
cells whose neighbourhood meets both form the finite set Z (44 cells, `zone_cover`). At the cells of Z the union
law is checked by the kernel at every generation (`LC_spec`), from V_k's state on units 32 .. 39 and the line's
state on NZ (`Gump/CallLine.lean`): for t ≤ 27 the standing store (k through min(k, 4)), for t = 28 .. 31 the start
(the birth of e1 at 28 is the one cell where the union law fails, and it is what V_k's forcing puts in), for
t = 32 .. 43 the words `VW k n` (k through min(k, 8)), and for t ≥ 44 every word of {7, b} on the eight units
(the review's lemma T): the line is then at rest, of period 2.
-/
import Gump.CallLine
import Gump.CallProof

namespace Gump.Call
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-! ### Supports -/

/-- The tube of the store wire (with e1). -/
def HV (p : Pt) : Prop := 1 ≤ p.x + p.y + p.z ∧ p.x + p.y + p.z ≤ 5 ∧ -1 ≤ p.x - p.y + p.z ∧ p.x - p.y + p.z ≤ 5

instance (p : Pt) : Decidable (HV p) := by unfold HV; infer_instance

/-- The diagonal hull of the line with the CALL. -/
def HL (p : Pt) : Prop :=
  p.x + p.y + p.z ≤ 33 ∧ p.x + p.y - p.z ≤ 177 ∧ p.x - p.y + p.z ≤ -5 ∧ p.x - p.y - p.z ≤ 139 ∧
  -p.x + p.y + p.z ≤ -135 ∧ -p.x + p.y - p.z ≤ 9 ∧ -p.x - p.y + p.z ≤ -51 ∧ -p.x - p.y - p.z ≤ 93

instance (p : Pt) : Decidable (HL p) := by unfold HL; infer_instance

theorem dot_eq (d : Diag) (p : Pt) : d.dot p = sg d.sx p.x + sg d.sy p.y + sg d.sz p.z := rfl

/-- A configuration in the tube stays in it. -/
theorem run_HV (c : Config) (h : ∀ p, c p = true → HV p) : ∀ n p, run c n p = true → HV p := by
  have conf : ∀ (d : Diag) (C : Int), (∀ p, C < d.dot p → c p = false) → ∀ n p, C < d.dot p → run c n p = false :=
    fun d C hd => confinement d C c hd
  have dead : ∀ (d : Diag) (C : Int), (∀ p, HV p → d.dot p ≤ C) → ∀ p, C < d.dot p → c p = false := by
    intro d C hd p hp
    cases e : c p
    · rfl
    · exact absurd (hd p (h p e)) (by omega)
  intro n p hp
  have a1 := conf ⟨true, true, true⟩ 5 (dead _ _ (fun q hq => by simp only [dot_eq, sg, ite_true]; unfold HV at hq; omega)) n p
  have a2 := conf ⟨false, false, false⟩ (-1) (dead _ _ (fun q hq => by
    simp only [dot_eq, sg, Bool.false_eq_true, ite_false]; unfold HV at hq; omega)) n p
  have a3 := conf ⟨true, false, true⟩ 5 (dead _ _ (fun q hq => by
    simp only [dot_eq, sg, Bool.false_eq_true, ite_false, ite_true]; unfold HV at hq; omega)) n p
  have a4 := conf ⟨false, true, false⟩ 1 (dead _ _ (fun q hq => by
    simp only [dot_eq, sg, Bool.false_eq_true, ite_false, ite_true]; unfold HV at hq; omega)) n p
  simp only [dot_eq, sg, Bool.false_eq_true, ite_false, ite_true] at a1 a2 a3 a4
  unfold HV
  refine ⟨?_, ?_, ?_, ?_⟩
  · apply Classical.byContradiction; intro hn; rw [a2 (by omega)] at hp; exact absurd hp (by decide)
  · apply Classical.byContradiction; intro hn; rw [a1 (by omega)] at hp; exact absurd hp (by decide)
  · apply Classical.byContradiction; intro hn; rw [a4 (by omega)] at hp; exact absurd hp (by decide)
  · apply Classical.byContradiction; intro hn; rw [a3 (by omega)] at hp; exact absurd hp (by decide)

theorem hexCells_HV (h : Nat) : ∀ q ∈ hexCells h, HV q := by
  unfold hexCells
  cases h.testBit 0 <;> cases h.testBit 1 <;> cases h.testBit 2 <;> cases h.testBit 3 <;> decide

theorem HV_shift (k : Int) (p : Pt) : HV (shiftPt k p) ↔ HV p := by
  simp only [HV, shiftPt]; omega

theorem hcfg_HV (w : Int → Nat) (p : Pt) (h : hcfg w p = true) : HV p := by
  simp only [hcfg, ucfg] at h
  have := hexCells_HV _ _ ((lcfg_iff _ _).mp h)
  rwa [HV_shift] at this

theorem e1_HV : HV e1 := by decide +kernel

/-- **V_k stays in the tube.** -/
theorem V_HV (k t : Nat) (p : Pt) (h : V k t p = true) : HV p := by
  simp only [V] at h
  split at h
  · exact run_HV _ (fun q hq => hcfg_HV _ q hq) t p h
  · refine run_HV _ (fun q hq => ?_) _ p h
    simp only [Bool.or_eq_true, beq_iff_eq] at hq
    rcases hq with hq | rfl
    · exact run_HV _ (fun r hr => hcfg_HV _ r hr) 29 q hq
    · exact e1_HV

/-- The eight bounds of the line's hull. -/
def CL (d : Diag) : Int :=
  match d.sx, d.sy, d.sz with
  | true, true, true => 33 | true, true, false => 177 | true, false, true => -5 | true, false, false => 139
  | false, true, true => -135 | false, true, false => 9 | false, false, true => -51 | false, false, false => 93

theorem lineCall_hull : ∀ p ∈ lineCallList, HL p := by decide +kernel

theorem HL_iff (p : Pt) : HL p ↔ ∀ d, d.dot p ≤ CL d := by
  constructor
  · intro h d
    obtain ⟨sx, sy, sz⟩ := d
    unfold HL at h
    cases sx <;> cases sy <;> cases sz <;> simp only [dot_eq, sg, CL, Bool.false_eq_true, ite_false, ite_true] <;> omega
  · intro h
    have := fun a b c => h ⟨a, b, c⟩
    have h1 := this true true true; have h2 := this true true false; have h3 := this true false true
    have h4 := this true false false; have h5 := this false true true; have h6 := this false true false
    have h7 := this false false true; have h8 := this false false false
    simp only [dot_eq, sg, CL, Bool.false_eq_true, ite_false, ite_true] at h1 h2 h3 h4 h5 h6 h7 h8
    unfold HL; omega

/-- **The free line stays in its hull.** -/
theorem Lf_HL (t : Nat) (p : Pt) (h : Lf t p = true) : HL p := by
  rw [HL_iff]
  refine hull CL lineCall (fun q hq => ?_) t p h
  rw [lineCall_eq, lcfg_iff] at hq
  exact (HL_iff q).mp (lineCall_hull q hq)

/-- **The two parts never share a point.** -/
theorem V_Lf_disjoint (k t : Nat) (p : Pt) : ¬ (V k t p = true ∧ Lf t p = true) := by
  rintro ⟨h1, h2⟩
  have a := V_HV k t p h1
  have b := Lf_HL t p h2
  unfold HV at a; unfold HL at b; omega

/-! ### The union law away from the zone -/

theorem step_congr_N {c c' : Config} {p : Pt} (h : ∀ q ∈ p :: nbrs p, c q = c' q) : step c p = step c' p := by
  have hc : count c p = count c' p := by
    unfold count; apply List.countP_congr; intro q hq; rw [h q (List.mem_cons_of_mem _ hq)]
  have hp : c p = c' p := h p List.mem_cons_self
  simp [step, hc, hp]

/-- At a point whose closed neighbourhood misses one part, the union steps to the union. -/
theorem step_or (A B : Config) (p : Pt)
    (h : (∀ q ∈ p :: nbrs p, A q = false) ∨ (∀ q ∈ p :: nbrs p, B q = false)) :
    step (fun q => A q || B q) p = (step A p || step B p) := by
  have dead : ∀ c : Config, (∀ q ∈ p :: nbrs p, c q = false) → step c p = false := by
    intro c hc
    have : step c p = step (fun _ => false) p := step_congr_N hc
    rw [this]; simp [step, rule, count]
  rcases h with h | h
  · rw [dead A h, Bool.false_or]
    exact step_congr_N (fun q hq => by rw [h q hq, Bool.false_or])
  · rw [dead B h, Bool.or_false]
    exact step_congr_N (fun q hq => by rw [h q hq, Bool.or_false])

/-- The four diagonal sums of a neighbour offset lie in −4 .. 4. -/
theorem offsets_diag : ∀ a : Axis, ∀ o ∈ offsets a, -4 ≤ o.x + o.y + o.z ∧ o.x + o.y + o.z ≤ 4 ∧
    -4 ≤ o.x - o.y + o.z ∧ o.x - o.y + o.z ≤ 4 ∧ -4 ≤ -o.x + o.y + o.z ∧ -o.x + o.y + o.z ≤ 4 ∧
    -4 ≤ o.x + o.y - o.z ∧ o.x + o.y - o.z ≤ 4 := by
  intro a; cases a <;> decide

def HVb (p : Pt) : Bool := decide (HV p)
def HLb (p : Pt) : Bool := decide (HL p)

/-- The cells of the box x 64 .. 76, y −1 .. 7, x + z −4 .. 4 whose neighbourhood meets both are in Z. -/
def zoneBoxOK : Bool :=
  (List.range 13).all fun a => (List.range 9).all fun b => (List.range 9).all fun c =>
    let p : Pt := ⟨64 + (a : Int), -1 + (b : Int), -4 - (64 + (a : Int)) + (c : Int)⟩
    !(p.isCell && (p :: nbrs p).any HVb && (p :: nbrs p).any HLb) || zoneZ.contains p

theorem zoneBoxOK_ok : zoneBoxOK = true := by decide +kernel

theorem zone_arith (px py pz ux uy uz vx vy vz : Int)
    (h1 : 1 ≤ px + ux + (py + uy) + (pz + uz)) (h1' : px + ux + (py + uy) + (pz + uz) ≤ 5)
    (h2 : -1 ≤ px + ux - (py + uy) + (pz + uz))
    (g2 : px + vx - (py + vy) + (pz + vz) ≤ -5) (g4 : px + vx - (py + vy) - (pz + vz) ≤ 139)
    (g5 : -(px + vx) + (py + vy) + (pz + vz) ≤ -135)
    (a1 : -4 ≤ ux + uy + uz) (a2 : ux + uy + uz ≤ 4) (a3 : -4 ≤ ux - uy + uz) (a4 : ux - uy + uz ≤ 4)
    (b3 : -4 ≤ vx - vy + vz) (b4 : vx - vy + vz ≤ 4) (b5 : -4 ≤ -vx + vy + vz) (b6 : -vx + vy + vz ≤ 4) :
    64 ≤ px ∧ px ≤ 76 ∧ -1 ≤ py ∧ py ≤ 7 ∧ -4 ≤ px + pz ∧ px + pz ≤ 4 := by
  omega

/-- **The interaction set.** A cell whose closed neighbourhood meets the tube and the line's hull is in Z. -/
theorem zone_cover (p : Pt) (hc : p.isCell = true) (hA : ∃ q ∈ p :: nbrs p, HV q) (hB : ∃ q ∈ p :: nbrs p, HL q) :
    p ∈ zoneZ := by
  have near : ∀ q ∈ p :: nbrs p, ∃ o : Pt, q = p + o ∧ -4 ≤ o.x + o.y + o.z ∧ o.x + o.y + o.z ≤ 4 ∧
      -4 ≤ o.x - o.y + o.z ∧ o.x - o.y + o.z ≤ 4 ∧ -4 ≤ -o.x + o.y + o.z ∧ -o.x + o.y + o.z ≤ 4 ∧
      -4 ≤ o.x + o.y - o.z ∧ o.x + o.y - o.z ≤ 4 := by
    intro q hq
    rcases List.mem_cons.mp hq with rfl | hq
    · exact ⟨⟨0, 0, 0⟩, by apply Pt.ext' <;> simp, by decide⟩
    · simp only [nbrs, List.mem_map] at hq
      obtain ⟨o, ho, rfl⟩ := hq
      exact ⟨o, rfl, offsets_diag _ o ho⟩
  obtain ⟨q1, hq1, h1⟩ := hA
  obtain ⟨q2, hq2, h2⟩ := hB
  obtain ⟨o1, rfl, a1, a2, a3, a4, -, -, -, -⟩ := near q1 hq1
  obtain ⟨o2, e2, -, -, b3, b4, b5, b6, -, -⟩ := near q2 hq2
  subst e2
  have hV := h1
  have hL := h2
  unfold HV at h1; unfold HL at h2
  simp only [Pt.add_x, Pt.add_y, Pt.add_z] at h1 h2
  obtain ⟨c1, c2, c3, -⟩ := h1
  obtain ⟨-, -, d2, d4, d5, -, -, -⟩ := h2
  obtain ⟨bx1, bx2, by1, by2, bz1, bz2⟩ :=
    zone_arith p.x p.y p.z o1.x o1.y o1.z o2.x o2.y o2.z c1 c2 c3 d2 d4 d5 a1 a2 a3 a4 b3 b4 b5 b6
  clear c1 c2 c3 d2 d4 d5 a1 a2 a3 a4 b3 b4 b5 b6 near
  have hok := zoneBoxOK_ok
  simp only [zoneBoxOK, List.all_eq_true, List.mem_range, Bool.or_eq_true, Bool.not_eq_true',
    Bool.and_eq_false_iff] at hok
  have := hok (p.x - 64).toNat (by omega) (p.y + 1).toNat (by omega) (p.x + p.z + 4).toNat (by omega)
  have ep : (⟨64 + (((p.x - 64).toNat : Nat) : Int), -1 + (((p.y + 1).toNat : Nat) : Int),
      -4 - (64 + (((p.x - 64).toNat : Nat) : Int)) + (((p.x + p.z + 4).toNat : Nat) : Int)⟩ : Pt) = p := by
    apply Pt.ext' <;> simp <;> omega
  rw [ep] at this
  rcases this with ((h | h) | h) | h
  · rw [hc] at h; exact absurd h (by decide)
  · exfalso
    simp only [List.any_eq_false, HVb, decide_eq_false_iff_not] at h
    exact h _ hq1 (decide_eq_true hV)
  · exfalso
    simp only [List.any_eq_false, HLb, decide_eq_false_iff_not] at h
    exact h _ hq2 (decide_eq_true hL)
  · exact (List.contains_iff_mem).mp h

end Gump.Call
