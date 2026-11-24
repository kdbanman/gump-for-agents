/-
**The unzip law** (`research/signals/push8/README.md` section 5, "Exactly k pulses for every k ≥ 1"; the proof in
`research/signals/push8/prove_unzip8.py`'s docstring; `research/audit/REVIEW-signals-8.md` section 3, which closes
three gaps and sharpens the time bound). Here: the statement, on the whole lattice with the infinite wire, the
moving-seam gluing that its proof (and the call law's) uses, proved; and one base fact of the induction that is
itself a law for every k: a stretch stands (`stretch_stands`).

Units of the wire family of pushes 7 to 9 are hex letters: the stators (0,1,2), (0,1,4) and the sites (1,0,0),
(1,0,2), (1,0,4), (0,2,3) of the bits of the letter. `7` is wire B and `b` wire C (the letters B, C of
`Gump/Tape.lean`: `tape_eq_hcfg`), `d` is wire B′, `f` the edge unit.

`UnzipLaw` (push 8's statement): wire B with the stretch d^k f on units 0 .. k; at an even generation remove the
stator (0,1,2) of unit −1; then at every even generation t ≥ 4k + 8 the whole state is plain wire B carrying exactly
k units of wire C two units apart, the leading one at unit 2 − t/2. `UnzipLawSharp` is the review's form: from
2k + 6 on, and not at 2k + 4. Both are proved in `Gump/UnzipProof.lean` (`unzip_law`, `unzip_law_sharp`).
-/
import Gump.TapeSignals
import Gump.Tape

namespace Gump.Unzip
open Gump Gump.Tape Gump.Bits

/-! ### The unit alphabet of pushes 7 to 9 -/

/-- The cells of the unit with hex letter h (bit j of h: site j). -/
def hexCells (h : Nat) : List Pt :=
  [⟨0, 1, 2⟩, ⟨0, 1, 4⟩] ++ (if h.testBit 0 then [⟨1, 0, 0⟩] else []) ++
    (if h.testBit 1 then [⟨1, 0, 2⟩] else []) ++ (if h.testBit 2 then [⟨1, 0, 4⟩] else []) ++
    (if h.testBit 3 then [⟨0, 2, 3⟩] else [])

/-- A word of hex letters on the wire: unit u is the unit w u, moved u units. -/
def hcfg (w : Int → Nat) : Config := ucfg (fun u => hexCells (w u))

/-- The letters of the tape theorem: B is `7`, C is `b`. -/
def hexOf : Letter → Nat
  | .B => 7
  | .C => 11

theorem tape_eq_hcfg (w : Int → Letter) : tape w = hcfg (fun u => hexOf (w u)) := by
  funext p
  simp only [tape, hcfg, ucfg]
  have hB : lcfg (cellsOf .B) = lcfg (hexCells 7) := (sameL_iff _ _).mp (by decide)
  have hC : lcfg (cellsOf .C) = lcfg (hexCells 11) := (sameL_iff _ _).mp (by decide)
  cases w (unitOf p) <;> simp only [hexOf, hB, hC]

/-! ### The statement -/

/-- The store wire: wire B (`7`) with the stretch d^k f on the units 0 .. k (`d` = 13, `f` = 15). -/
def storeWord (k : Nat) (u : Int) : Nat := if 0 ≤ u ∧ u < k then 13 else if u = k then 15 else 7

/-- The store wire, a configuration of the whole lattice, infinite along the wire. -/
def store (k : Nat) : Config := hcfg (storeWord k)

/-- **The count read**: the stator (0,1,2) of unit −1 removed, at an even generation. -/
def countRead (k : Nat) : Config := fun p => store k p && p != shiftPt (-1) ⟨0, 1, 2⟩

/-- k pulses (units of wire C) two units apart in wire B, the leading one at unit `lead`. -/
def pulses (k : Nat) (lead : Int) (u : Int) : Letter :=
  if lead ≤ u ∧ u < lead + 2 * k ∧ (u - lead) % 2 = 0 then .C else .B

/-- **The unzip law**, as push 8 states it (`prove_unzip8.py`): for every k ≥ 1 and every even generation
t = 2n ≥ 4k + 8, the count read has left plain wire B with exactly k pulses two apart, the leading one at unit
2 − t/2. -/
def UnzipLaw : Prop :=
  ∀ k : Nat, 1 ≤ k → ∀ n : Nat, 2 * k + 4 ≤ n → run (countRead k) (2 * n) = tape (pulses k (2 - n))

/-- **The unzip law, sharp** (`REVIEW-signals-8.md` section 3 (ii)): final from generation 2k + 6 on, and not at
2k + 4. -/
def UnzipLawSharp : Prop :=
  ∀ k : Nat, 1 ≤ k → (∀ n : Nat, k + 3 ≤ n → run (countRead k) (2 * n) = tape (pulses k (2 - n))) ∧
    run (countRead k) (2 * (k + 2)) ≠ tape (pulses k (2 - (k + 2)))

theorem unzipLawSharp_imp : UnzipLawSharp → UnzipLaw :=
  fun h k hk n hn => (h k hk).1 n (by omega)

/-! ### A stretch stands, for every k -/

theorem hexCells_unit (h : Nat) : ∀ q ∈ hexCells h, unitOf q = 0 := by
  unfold hexCells
  cases h.testBit 0 <;> cases h.testBit 1 <;> cases h.testBit 2 <;> cases h.testBit 3 <;> decide

/-- The five letters of a word around unit u. -/
def win (w : Int → Nat) (u : Int) : List Nat := [w (u - 2), w (u - 1), w u, w (u + 1), w (u + 2)]

/-- The window σ on the units −2 .. 2 (wire B beyond). -/
def winF (σ : List Nat) (v : Int) : List Pt := hexCells (σ.getD (v + 2).toNat 7)

/-- Two generations of the window σ leave on unit 0 the letter that was on unit s. -/
def hexWindowCheck (s : Int) (σ : List Nat) : Bool :=
  pieceCheck (winF σ) (fun _ => hexCells (σ.getD (s + 2).toNat 7)) (-2) 5 [] [] 2 0 0 ⟨0, 0, 0⟩

/-- **Two generations of a hex word, locally**: if the window of w around the unit of p passes the check, any
configuration that is the word w on those five units holds at p, two generations on, the word moved by s. -/
theorem hex_local (w : Int → Nat) (s : Int) (hs : -2 ≤ s ∧ s ≤ 2) (c : Config) (p : Pt)
    (hc : hexWindowCheck s (win w (unitOf p)) = true)
    (h : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = hcfg w q) :
    run c 2 p = hcfg (fun u => w (u + s)) p := by
  let u := unitOf p
  let σ := win w u
  have key : ∀ d : Int, -2 ≤ d → d ≤ 2 → σ.getD (d + 2).toNat 7 = w (u + d) := by
    intro d h1 h2
    rcases (show d = -2 ∨ d = -1 ∨ d = 0 ∨ d = 1 ∨ d = 2 by omega) with rfl | rfl | rfl | rfl | rfl <;>
      simp [σ, win] <;> congr 1 <;> omega
  have agree : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 → c q = shiftC u (ucfg (winF σ)) q := by
    intro q h1 h2
    rw [h q h1 h2]
    simp only [shiftC, hcfg, ucfg, winF, unitOf_shiftPt, shiftPt_shiftPt]
    rw [show unitOf q + -u + 2 = (unitOf q - u) + 2 by omega, key _ (by omega) (by omega),
      show u + (unitOf q - u) = unitOf q by omega, show -(unitOf q + -u) + -u = -unitOf q by omega]
  rw [run_eq_of_units 2 (fun q h1 h2 => agree q (by omega) (by omega)), run_shiftC]
  simp only [shiftC]
  have spec := pieceCheck_spec (f := winF σ) (fun v => hexCells_unit _) (fun v => hexCells_unit _)
    zero_even hc (by decide) (by decide) (by decide) (by decide) (by decide)
    (ucfg (winF σ)) (fun q _ _ => by simp only [xorC, lcfg_nil', Bool.xor_false]) (shiftPt (-u) p)
    (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)
  rw [spec]
  simp only [xorC, lcfg_nil', Bool.xor_false, ucfg, hcfg, unitOf_shiftPt, shiftPt_shiftPt]
  have k : (win w (unitOf p)).getD (s + 2).toNat 7 = w (unitOf p + s) := key s hs.1 hs.2
  rw [k, show -(unitOf p + -u) + -u = -unitOf p by omega]

theorem win_congr (w w' : Int → Nat) (u u' : Int) (h : ∀ i : Int, -2 ≤ i → i ≤ 2 → w (u + i) = w' (u' + i)) :
    win w u = win w' u' := by
  have e1 := h (-2) (by decide) (by decide)
  have e2 := h (-1) (by decide) (by decide)
  have e3 := h 0 (by decide) (by decide)
  have e4 := h 1 (by decide) (by decide)
  have e5 := h 2 (by decide) (by decide)
  rw [show u + -2 = u - 2 by omega, show u' + -2 = u' - 2 by omega] at e1
  rw [show u + -1 = u - 1 by omega, show u' + -1 = u' - 1 by omega] at e2
  rw [Int.add_zero, Int.add_zero] at e3
  simp only [win, e1, e2, e3, e4, e5]

theorem storeWord_eq (k k' : Nat) (u u' : Int)
    (h : ∀ i : Int, -2 ≤ i → i ≤ 2 → ((0 ≤ u + i ∧ u + i < k) ↔ (0 ≤ u' + i ∧ u' + i < k')) ∧
      (u + i = k ↔ u' + i = k')) :
    win (storeWord k) u = win (storeWord k') u' := by
  apply win_congr
  intro i h1 h2
  obtain ⟨a, b⟩ := h i h1 h2
  simp only [storeWord]
  by_cases c1 : 0 ≤ u + i ∧ u + i < k
  · rw [if_pos c1, if_pos (a.mp c1)]
  · rw [if_neg c1, if_neg (fun h => c1 (a.mpr h))]
    by_cases c2 : u + i = k
    · rw [if_pos c2, if_pos (b.mp c2)]
    · rw [if_neg c2, if_neg (fun h => c2 (b.mpr h))]

set_option maxHeartbeats 1000000 in
/-- Every window of a stretch is a window of a stretch of at most six units, around a unit in −3 .. 9. -/
theorem win_canon (k : Nat) (hk : 1 ≤ k) (u : Int) : ∃ k' : Nat, ∃ u' : Int, 1 ≤ k' ∧ k' ≤ 6 ∧ -3 ≤ u' ∧ u' ≤ 9 ∧
    win (storeWord k) u = win (storeWord k') u' := by
  by_cases h6 : k ≤ 6
  · by_cases ha : u ≤ -3
    · exact ⟨k, -3, hk, h6, by decide, by decide, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
    · by_cases hb : (k : Int) + 3 ≤ u
      · exact ⟨k, k + 3, hk, h6, by omega, by omega, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
      · exact ⟨k, u, hk, h6, by omega, by omega, rfl⟩
  · by_cases ha : u ≤ -3
    · exact ⟨6, -3, by decide, by decide, by decide, by decide, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
    · by_cases hb : u ≤ 3
      · exact ⟨6, u, by decide, by decide, by omega, by omega, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
      · by_cases hc : u < (k : Int) - 3
        · exact ⟨6, 3, by decide, by decide, by decide, by decide, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
        · by_cases hd : u < (k : Int) + 3
          · exact ⟨6, u - (k - 6), by decide, by decide, by omega, by omega,
              storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩
          · exact ⟨6, 9, by decide, by decide, by decide, by decide, storeWord_eq _ _ _ _ (fun i _ _ => by omega)⟩

/-- The 78 canonical windows of a stretch, each stepped twice by the kernel. -/
def storeWinOK : Bool :=
  (List.range 6).all fun a => (List.range 13).all fun b => hexWindowCheck 0 (win (storeWord (a + 1)) ((b : Int) - 3))

theorem storeWinOK_ok : storeWinOK = true := by decide +kernel

theorem store_window (k : Nat) (hk : 1 ≤ k) (u : Int) : hexWindowCheck 0 (win (storeWord k) u) = true := by
  obtain ⟨k', u', h1, h2, h3, h4, e⟩ := win_canon k hk u
  rw [e]
  have := storeWinOK_ok
  simp only [storeWinOK, List.all_eq_true, List.mem_range] at this
  have h := this (k' - 1) (by omega) (u' + 3).toNat (by omega)
  rw [show k' - 1 + 1 = k' by omega, show (((u' + 3).toNat : Nat) : Int) - 3 = u' by omega] at h
  exact h

/-- **A stretch stands**: wire B with the stretch d^k f (`store k`) has period dividing 2, for every k ≥ 1, on
the whole lattice (`research/signals/push8/README.md` section 6, the memory cell holding k: the infinite-wire form;
a base fact of the unzip law's induction). -/
theorem stretch_stands (k : Nat) (hk : 1 ≤ k) : ∀ n : Nat, run (store k) (2 * n) = store k := by
  have two : run (store k) 2 = store k := by
    funext p
    have := hex_local (storeWord k) 0 ⟨by decide, by decide⟩ (store k) p (store_window k hk _) (fun _ _ _ => rfl)
    rw [this]
    simp only [Int.add_zero]
    rfl
  intro n
  induction n with
  | zero => rfl
  | succ n ih => rw [show 2 * (n + 1) = 2 + 2 * n by omega, run_add, two, ih]

/-! ### The moving seam -/

/-- **Gluing along a moving seam** (push 8's and the call law's step). A on the units ≤ m t, Z on the units > m t;
if A obeys the rule on the units ≤ m t and Z on the units > m t, the two agree on the three units m t − 1 .. m t + 1,
and the seam moves at most one unit per generation, the glued sequence is the orbit of the glued start. -/
theorem glue_run_moving (m : Nat → Int) (A Z : Nat → Config)
    (hm : ∀ t, m (t + 1) ≤ m t + 1 ∧ m t ≤ m (t + 1) + 1)
    (hA : ∀ t p, unitOf p ≤ m t → step (A t) p = A (t + 1) p)
    (hZ : ∀ t p, m t < unitOf p → step (Z t) p = Z (t + 1) p)
    (hAZ : ∀ t p, m t - 1 ≤ unitOf p → unitOf p ≤ m t + 1 → A t p = Z t p) :
    ∀ t, run (glue (m 0) (A 0) (Z 0)) t = glue (m t) (A t) (Z t) := by
  intro t
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [run, ih]
    funext p
    obtain ⟨hm1, hm2⟩ := hm t
    show step (fun q => if unitOf q ≤ m t then A t q else Z t q) p =
      (if unitOf p ≤ m (t + 1) then A (t + 1) p else Z (t + 1) p)
    by_cases hu : unitOf p ≤ m t
    · have e : step (fun q => if unitOf q ≤ m t then A t q else Z t q) p = A (t + 1) p := by
        rw [← hA t p hu]
        apply step_eq_of_units
        intro q h1 h2
        split
        · rfl
        · exact (hAZ t q (by omega) (by omega)).symm
      rw [e]
      split
      · rfl
      · exact hAZ (t + 1) p (by omega) (by omega)
    · have e : step (fun q => if unitOf q ≤ m t then A t q else Z t q) p = Z (t + 1) p := by
        rw [← hZ t p (by omega)]
        apply step_eq_of_units
        intro q h1 h2
        split
        · exact hAZ t q (by omega) (by omega)
        · rfl
      rw [e]
      split
      · exact (hAZ (t + 1) p (by omega) (by omega)).symm
      · rfl

end Gump.Unzip
