/-
The link between the dice agent's surrogate (`GumpMath/DiceDef.lean`: `Gump.Dice.Face.P`, rational, on bit
masks) and the chain theorems (`GumpMath/Chain*.lean`).

  `aliveProb_cast`, `P_cast`  (F.P ρ1 ρ2 x y : ℝ) = bitP F.A (aR F ρ1 ρ2) x y, for every face (step (1) of the plan);
  `aliveProb_mem`             0 ≤ aliveProb ≤ 1 for 0 ≤ ρ ≤ 1, any coins (binomial theorem);
  `chain F …`                 the killed chain of `Face.P` itself at the empty face (`Face.empty`);
  `toDice`, `ofDice`          `Gump.Dice.IsQSD F ρ1 ρ2` ↔ the chain's `IsQSD` (extension by 0 at the empty face);
  `face_theorems`             for every face whose cells have coins (2,1), or (2,0) with at most two neighbours
                              (every wrapped face, strip and hull face of `geom.py`), at 0 < ρ1, ρ2 < 1: the dominant
                              quasi-stationary law of `Face.P` exists, is a `Gump.Dice.IsQSD`, log τ = Σ_i c_i with c_i
                              the price of cell i's own death probability 1 - F.a x i, log τ ≤ ε_max · A, and
                              τ ≥ 1/(1 - Q u u) for every living u;
  `face_theorems_allcoins`    the same for every face with all its coins (`coins_of_all`).
-/
import Mathlib
import GumpMath.DiceDef
import GumpMath.DiceLife
import GumpMath.DiceBound
import GumpMath.ChainBits
import GumpMath.ChainRate
import GumpMath.ChainKagome

set_option linter.unusedSectionVars false

namespace Gump.Link
open Finset Gump.Chain Gump.Chain.Bits Gump.Chain.KilledChain Gump.Dice

theorem bin_cast (m : ℕ) (ρ : ℚ) (j : ℕ) : ((bin m ρ j : ℚ) : ℝ) = binR m (ρ : ℝ) j := by
  simp [bin, binR]

theorem aliveProb_cast (ρ1 ρ2 : ℚ) (m1 m2 k : ℕ) (s : Bool) :
    ((aliveProb ρ1 ρ2 m1 m2 k s : ℚ) : ℝ) = aliveProbR (ρ1 : ℝ) (ρ2 : ℝ) m1 m2 k s := by
  simp only [aliveProb, aliveProbR, Rat.cast_sum]
  refine Finset.sum_congr rfl (fun j _ => Finset.sum_congr rfl (fun l _ => ?_))
  split_ifs <;> simp [bin_cast]

/-- The face's alive probabilities over ℝ. -/
noncomputable def aR (F : Face) (ρ1 ρ2 : ℚ) : ℕ → ℕ → ℝ :=
  fun x i => aliveProbR (ρ1 : ℝ) (ρ2 : ℝ) (F.m1 i) (F.m2 i) (F.k x i) (x.testBit i)

theorem a_cast (F : Face) (ρ1 ρ2 : ℚ) (x i : ℕ) : ((F.a ρ1 ρ2 x i : ℚ) : ℝ) = aR F ρ1 ρ2 x i :=
  aliveProb_cast _ _ _ _ _ _

/-- **The bridge**: `Face.P` over ℝ is the bit-mask product kernel of the chain arm. -/
theorem P_cast (F : Face) (ρ1 ρ2 : ℚ) (x y : Fin (2 ^ F.A)) :
    ((F.P ρ1 ρ2 x y : ℚ) : ℝ) = bitP F.A (aR F ρ1 ρ2) x y := by
  simp only [Face.P, bitP, Rat.cast_prod]
  refine Finset.prod_congr rfl (fun i _ => ?_)
  split_ifs <;> simp [a_cast]

theorem bin_sum (m : ℕ) (ρ : ℚ) : ∑ j ∈ range (m + 1), bin m ρ j = 1 := by
  have := add_pow ρ (1 - ρ) m
  rw [add_sub_cancel, one_pow] at this
  rw [this]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  simp only [bin]; ring

theorem bin_nonneg (m : ℕ) {ρ : ℚ} (h0 : 0 ≤ ρ) (h1 : ρ ≤ 1) (j : ℕ) : 0 ≤ bin m ρ j := by
  have : 0 ≤ 1 - ρ := by linarith
  simp only [bin]; positivity

/-- 0 ≤ aliveProb ≤ 1 for densities in [0, 1], whatever the coins. -/
theorem aliveProb_mem {ρ1 ρ2 : ℚ} (h0 : 0 ≤ ρ1) (h1 : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h3 : ρ2 ≤ 1)
    (m1 m2 k : ℕ) (s : Bool) : 0 ≤ aliveProb ρ1 ρ2 m1 m2 k s ∧ aliveProb ρ1 ρ2 m1 m2 k s ≤ 1 := by
  have hterm : ∀ j l, 0 ≤ bin m1 ρ1 j * bin m2 ρ2 l := fun j l =>
    mul_nonneg (bin_nonneg m1 h0 h1 j) (bin_nonneg m2 h2 h3 l)
  constructor
  · exact Finset.sum_nonneg (fun j _ => Finset.sum_nonneg (fun l _ => by
      split_ifs
      · exact hterm j l
      · exact le_refl _))
  · calc aliveProb ρ1 ρ2 m1 m2 k s ≤ ∑ j ∈ range (m1 + 1), ∑ l ∈ range (m2 + 1), bin m1 ρ1 j * bin m2 ρ2 l :=
          Finset.sum_le_sum (fun j _ => Finset.sum_le_sum (fun l _ => by
            split_ifs
            · exact le_refl _
            · exact hterm j l))
      _ = 1 := by simp_rw [← Finset.mul_sum, bin_sum, mul_one, bin_sum]

/-- Densities in [0, 1]. -/
structure Dens (ρ1 ρ2 : ℚ) : Prop where
  h0 : 0 ≤ ρ1
  h1 : ρ1 ≤ 1
  h2 : 0 ≤ ρ2
  h3 : ρ2 ≤ 1

theorem P_nonneg' (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (x y : Fin (2 ^ F.A)) :
    0 ≤ ((F.P ρ1 ρ2 x y : ℚ) : ℝ) := by
  have : 0 ≤ F.P ρ1 ρ2 x y := by
    unfold Face.P
    refine prod_nonneg (fun i _ => ?_)
    have h := aliveProb_mem hd.h0 hd.h1 hd.h2 hd.h3 (F.m1 i) (F.m2 i) (F.k x i) (Nat.testBit x i)
    have ha : F.a ρ1 ρ2 x i = aliveProb ρ1 ρ2 (F.m1 i) (F.m2 i) (F.k x i) (Nat.testBit x i) := rfl
    split_ifs
    · rw [ha]; exact h.1
    · rw [ha]; linarith [h.2]
  exact_mod_cast this

theorem P_row' (F : Face) (ρ1 ρ2 : ℚ) (x : Fin (2 ^ F.A)) : ∑ y, ((F.P ρ1 ρ2 x y : ℚ) : ℝ) = 1 := by
  have := Face.P_row_sum F ρ1 ρ2 x
  exact_mod_cast this

/-- **The killed chain of `Face.P` itself**, at the empty face. -/
noncomputable def chain (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) : KilledChain {x : Fin (2 ^ F.A) // x ≠ F.empty} :=
  ofStochastic (fun x y => ((F.P ρ1 ρ2 x y : ℚ) : ℝ)) F.empty (P_nonneg' F hd) (P_row' F ρ1 ρ2)

theorem chain_Q (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (x y : {x : Fin (2 ^ F.A) // x ≠ F.empty}) :
    (chain F hd).Q x y = ((F.P ρ1 ρ2 x y : ℚ) : ℝ) := rfl

theorem empty_iff (F : Face) (x : Fin (2 ^ F.A)) : x = F.empty ↔ (x : ℕ) = 0 :=
  ⟨fun h => by rw [h]; rfl, fun h => Fin.ext h⟩

/-- A law on the living states, extended by 0 at the empty face. -/
noncomputable def extend (F : Face) (μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ) : Fin (2 ^ F.A) → ℝ :=
  fun x => if h : x = F.empty then 0 else μ ⟨x, h⟩

/-- The chain's quasi-stationary laws are the dice agent's. -/
theorem toDice (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ}
    {lam : ℝ} (h : (chain F hd).IsQSD μ lam) : IsQSD F ρ1 ρ2 (extend F μ) lam := by
  refine ⟨fun x => ?_, fun x hx => ?_, ?_, fun y hy => ?_⟩
  · simp only [extend]; split_ifs
    · exact le_refl _
    · exact h.nonneg _
  · simp [extend, (empty_iff F x).2 hx]
  · rw [← sum_ne_add (extend F μ) F.empty]
    simp only [extend, dite_true, add_zero]
    rw [← h.total]
    refine Finset.sum_congr rfl (fun x _ => ?_)
    simp [x.2]
  · have hy' : y ≠ F.empty := fun e => hy ((empty_iff F y).1 e)
    have e := h.eigen ⟨y, hy'⟩
    rw [← sum_ne_add (fun x => extend F μ x * ((F.P ρ1 ρ2 x y : ℚ) : ℝ)) F.empty]
    simp only [extend, dite_true, zero_mul, add_zero, hy', dite_false]
    rw [← e]
    refine Finset.sum_congr rfl (fun x _ => ?_)
    simp [x.2, chain_Q]

theorem ofDice (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) {μ : Fin (2 ^ F.A) → ℝ} {lam : ℝ}
    (h : IsQSD F ρ1 ρ2 μ lam) : (chain F hd).IsQSD (fun x => μ x) lam :=
  isQSD_of _ F.empty (P_nonneg' F hd) (P_row' F ρ1 ρ2) μ lam (h.empty _ rfl) h.nonneg h.total
    (fun y hy => h.eigen y (fun e => hy ((empty_iff F y).2 e)))

/-! ### The local factors: (K) from the cells' coins -/

/-- Each cell has coins (2,1), or coins (2,0) and at most two neighbours. -/
def CellsOK (F : Face) : Prop :=
  ∀ i < F.A, (F.m1 i = 2 ∧ F.m2 i = 1) ∨ (F.m1 i = 2 ∧ F.m2 i = 0 ∧ (F.nb i).length ≤ 2)

theorem death3_eq_one (ρ1 ρ2 : ℝ) (s : Bool) (k : ℕ) (hk : 6 ≤ k) : death3 ρ1 ρ2 s k = 1 := by
  rw [← coin3_total ρ1 ρ2]
  unfold death3
  refine Finset.sum_congr rfl (fun b _ => ?_)
  have : aliveNext s (k + b) = false := by
    cases s <;> simp [aliveNext] <;> omega
  simp [this]

theorem atom_le_death3 {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) (s : Bool)
    (k : ℕ) : atomMin ρ1 ρ2 ≤ death3 ρ1 ρ2 s k := by
  by_cases hk : k ≤ 6
  · exact threeCoins_death_ge h1.le h1'.le h2.le h2'.le s k hk
  · rw [death3_eq_one ρ1 ρ2 s k (by omega)]
    unfold atomMin
    exact (min_le_left _ _).trans (by nlinarith [mul_pos (mul_pos h1 h1) h2])

/-- Strict densities. -/
structure SDens (ρ1 ρ2 : ℚ) : Prop where
  h0 : 0 < ρ1
  h1 : ρ1 < 1
  h2 : 0 < ρ2
  h3 : ρ2 < 1

theorem SDens.dens {ρ1 ρ2 : ℚ} (h : SDens ρ1 ρ2) : Dens ρ1 ρ2 := ⟨h.h0.le, h.h1.le, h.h2.le, h.h3.le⟩

theorem atom_le_one_sub_a (F : Face) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) (x : ℕ) (i : ℕ)
    (hi : i < F.A) : atomMin (ρ1 : ℝ) (ρ2 : ℝ) ≤ 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ) := by
  have r0 : (0 : ℝ) < ρ1 := by exact_mod_cast hs.h0
  have r1 : (ρ1 : ℝ) < 1 := by exact_mod_cast hs.h1
  have r2 : (0 : ℝ) < ρ2 := by exact_mod_cast hs.h2
  have r3 : (ρ2 : ℝ) < 1 := by exact_mod_cast hs.h3
  rw [a_cast]
  simp only [aR]
  rcases hc i hi with ⟨e1, e2⟩ | ⟨e1, e2, hl⟩
  · rw [e1, e2, one_sub_aliveProbR_three]
    exact atom_le_death3 r0 r1 r2 r3 _ _
  · rw [e1, e2, one_sub_aliveProbR_two]
    have hk : F.k x i ≤ 2 := (List.countP_le_length).trans hl
    exact twoCoins_death_ge r0.le r1.le r2.le r3.le _ _ hk

/-- **The local death factors of `Face.P`**: cell i's own death probability 1 - F.a x i. -/
noncomputable def localDeath (F : Face) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) :
    (chain F hs.dens).LocalDeath (Fin F.A) :=
  ofStochastic_local _ F.empty (P_nonneg' F hs.dens) (P_row' F ρ1 ρ2)
    (fun i x => ((F.a ρ1 ρ2 x i : ℚ) : ℝ))
    (fun i x => by
      have h := aliveProb_mem hs.dens.h0 hs.dens.h1 hs.dens.h2 hs.dens.h3 (F.m1 i) (F.m2 i)
        (F.k x i) (Nat.testBit x i)
      have : (0 : ℝ) ≤ ((F.a ρ1 ρ2 x i : ℚ) : ℝ) := by exact_mod_cast h.1
      exact this)
    (fun i x => by
      have := atom_le_one_sub_a F hs hc x i i.2
      have hpos := atomMin_pos (ρ1 := (ρ1 : ℝ)) (ρ2 := (ρ2 : ℝ)) (by exact_mod_cast hs.h0)
        (by exact_mod_cast hs.h1) (by exact_mod_cast hs.h2) (by exact_mod_cast hs.h3)
      linarith)
    (fun x _ => by
      rw [Face.P_zero_col, Face.death, Rat.cast_prod,
        ← Fin.prod_univ_eq_prod_range (fun i => ((1 - F.a ρ1 ρ2 x i : ℚ) : ℝ)) F.A]
      push_cast; rfl)

theorem localDeath_dc (F : Face) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) (i : Fin F.A)
    (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}) :
    (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ) := rfl

/-- **Theorems 1 and 2 for `Face.P` itself, on every face whose cells have their coins.** -/
theorem face_theorems (F : Face) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) (hA : 0 < F.A) :
    ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧
      (∀ i x, (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs hc).price μ i ∧
      Real.log ((chain F hs.dens).lifetime μ) ≤ -Real.log (atomMin (ρ1 : ℝ) (ρ2 : ℝ)) * F.A ∧
      ∀ u, 1 / (1 - (chain F hs.dens).Q u u) ≤ (chain F hs.dens).lifetime μ := by
  have hne : ∃ x : Fin (2 ^ F.A), x ≠ F.empty :=
    ⟨⟨1, Nat.one_lt_two_pow hA.ne'⟩, fun h => by
      have := (empty_iff F _).1 h; simp at this⟩
  obtain ⟨μ, lam, hD, he, hb, hu⟩ := surrogate_theorems (V := Fin F.A)
    (fun x y => ((F.P ρ1 ρ2 x y : ℚ) : ℝ)) F.empty hne (P_nonneg' F hs.dens) (P_row' F ρ1 ρ2)
    (fun i x => ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) _ _ _ (by exact_mod_cast hs.h0) (by exact_mod_cast hs.h1)
    (by exact_mod_cast hs.h2) (by exact_mod_cast hs.h3) (fun i x => atom_le_one_sub_a F hs hc x i i.2)
  refine ⟨μ, lam, hD, toDice F hs.dens hD.qsd, fun i x => rfl, he, ?_, hu⟩
  have hb' := hb
  rw [Fintype.card_fin] at hb'
  exact hb'

theorem cellsOK_of_allcoins (F : Face) (hc : ∀ q, F.coin q = true) : CellsOK F :=
  fun i _ => Or.inl (coins_of_all F hc i)

/-- **The same for every face with all its coins** (every wrapped face and strip of `geom.py`). -/
theorem face_theorems_allcoins (F : Face) (hcoin : ∀ q, F.coin q = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)
    (hA : 0 < F.A) :
    ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧
      (∀ i x, (localDeath F hs (cellsOK_of_allcoins F hcoin)).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain F hs.dens).lifetime μ) =
        ∑ i, (localDeath F hs (cellsOK_of_allcoins F hcoin)).price μ i ∧
      Real.log ((chain F hs.dens).lifetime μ) ≤ -Real.log (atomMin (ρ1 : ℝ) (ρ2 : ℝ)) * F.A ∧
      ∀ u, 1 / (1 - (chain F hs.dens).Q u u) ≤ (chain F hs.dens).lifetime μ :=
  face_theorems F hs (cellsOK_of_allcoins F hcoin) hA

end Gump.Link
