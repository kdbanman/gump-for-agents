/-
The surrogate's kernel on bit masks, in the shape of `GumpMath/DiceDef.lean` (`Gump.Dice.Face.P`), so that
the chain theorems apply to it with no further work beyond casts and per-face facts.

States are `Fin (2 ^ A)`; cell i < A is alive in y iff `y.testBit i`; the empty face is 0.
  `bitP A a x y = ∏_{i < A} (a x i if y.testBit i else 1 - a x i)`.
Proved for every a with 0 ≤ a < 1: the rows sum to 1 (`bitP_row`, by induction on A over the top bit),
P x 0 = ∏ (1 - a x i) (`bitP_zero`), and the support (`bitP_pos_iff`).
`aliveProbR` is `Gump.Dice.aliveProb` transcribed over ℝ (binomial coins, `Gump.rule`), and
`one_sub_aliveProbR_three`, `one_sub_aliveProbR_two` identify its complement with `death3`, `death2`.
`bit_surrogate`: for every face whose cells have coins (2,1) and k ≤ 6, or (2,0) and k ≤ 2, the surrogate
has a quasi-stationary law, log τ = ∑_i c_i (Theorem 2) and log τ ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) · A
(Theorem 1).  `bit_one_class`: Lemma 0's uniqueness from a state u in which every cell can be alive next,
reached from every state that can survive.
-/
import Mathlib
import GumpMath.ChainInst
import Gump.Basic

set_option linter.unusedSectionVars false

namespace Gump.Chain.Bits
open Finset Gump.Chain Gump.Chain.KilledChain

/-- The product kernel on bit masks. -/
def bitP (A : ℕ) (a : ℕ → ℕ → ℝ) : Matrix (Fin (2 ^ A)) (Fin (2 ^ A)) ℝ :=
  fun x y => ∏ i ∈ range A, if (y : ℕ).testBit i then a x i else 1 - a x i

/-- The empty face. -/
def empty (A : ℕ) : Fin (2 ^ A) := ⟨0, Nat.two_pow_pos A⟩

/-- A sum over bit masks of a product over bits factorises. -/
theorem sum_bits (A : ℕ) (p q : ℕ → ℝ) :
    ∑ y ∈ range (2 ^ A), ∏ i ∈ range A, (if y.testBit i then p i else q i) =
      ∏ i ∈ range A, (p i + q i) := by
  induction A with
  | zero => simp
  | succ A ih =>
    rw [pow_succ, mul_two, Finset.sum_range_add, Finset.prod_range_succ]
    have h1 : ∀ y ∈ range (2 ^ A), ∏ i ∈ range (A + 1), (if y.testBit i then p i else q i) =
        (∏ i ∈ range A, (if y.testBit i then p i else q i)) * q A := by
      intro y hy
      rw [Finset.prod_range_succ, Nat.testBit_lt_two_pow (mem_range.1 hy)]
      simp
    have h2 : ∀ y ∈ range (2 ^ A), ∏ i ∈ range (A + 1), (if (2 ^ A + y).testBit i then p i else q i) =
        (∏ i ∈ range A, (if y.testBit i then p i else q i)) * p A := by
      intro y hy
      rw [Finset.prod_range_succ, Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow (mem_range.1 hy)]
      simp only [Bool.not_false, ite_true]
      congr 1
      exact Finset.prod_congr rfl (fun i hi => by rw [Nat.testBit_two_pow_add_gt (mem_range.1 hi)])
    rw [Finset.sum_congr rfl h1, Finset.sum_congr rfl h2, ← Finset.sum_mul, ← Finset.sum_mul, ih]
    ring

variable {A : ℕ} {a : ℕ → ℕ → ℝ}

theorem bitP_row (x : Fin (2 ^ A)) : ∑ y, bitP A a x y = 1 := by
  have := Fin.sum_univ_eq_sum_range
    (fun y : ℕ => ∏ i ∈ range A, if y.testBit i then a x i else 1 - a x i) (2 ^ A)
  simp only [bitP]
  rw [this, sum_bits]
  simp

theorem bitP_nonneg (h0 : ∀ (x : Fin (2 ^ A)) i, i < A → 0 ≤ a x i)
    (h1 : ∀ (x : Fin (2 ^ A)) i, i < A → a x i ≤ 1) (x y : Fin (2 ^ A)) : 0 ≤ bitP A a x y :=
  prod_nonneg (fun i hi => by
    have hi' := mem_range.1 hi
    split_ifs
    · exact h0 x i hi'
    · linarith [h1 x i hi'])

theorem bitP_zero (x : Fin (2 ^ A)) : bitP A a x (empty A) = ∏ i ∈ range A, (1 - a x i) := by
  simp [bitP, empty]

/-- The support: x → y is possible iff every cell alive in y can be alive next. -/
theorem bitP_pos_iff (h0 : ∀ (x : Fin (2 ^ A)) i, i < A → 0 ≤ a x i)
    (h1 : ∀ (x : Fin (2 ^ A)) i, i < A → a x i < 1) (x y : Fin (2 ^ A)) :
    0 < bitP A a x y ↔ ∀ i, i < A → (y : ℕ).testBit i → 0 < a x i := by
  constructor
  · intro h i hi hy
    rcases (h0 x i hi).lt_or_eq with h' | h'
    · exact h'
    · exfalso
      have : bitP A a x y = 0 := prod_eq_zero (mem_range.2 hi) (by simp [hy, ← h'])
      linarith
  · intro h
    apply prod_pos
    intro i hi
    have hi' := mem_range.1 hi
    split_ifs with hy
    · exact h i hi' hy
    · linarith [h1 x i hi']

/-! ### The coins, as in `Gump.Dice.aliveProb` -/

/-- m coins of density ρ show exactly j heads. -/
noncomputable def binR (m : ℕ) (ρ : ℝ) (j : ℕ) : ℝ := (m.choose j : ℝ) * ρ ^ j * (1 - ρ) ^ (m - j)

/-- The probability that a cell is alive next (`Gump.Dice.aliveProb` over ℝ). -/
noncomputable def aliveProbR (ρ1 ρ2 : ℝ) (m1 m2 k : ℕ) (s : Bool) : ℝ :=
  ∑ j ∈ range (m1 + 1), ∑ l ∈ range (m2 + 1),
    if Gump.rule s (k + j + l) then binR m1 ρ1 j * binR m2 ρ2 l else 0

theorem one_sub_aliveProbR_three (ρ1 ρ2 : ℝ) (k : ℕ) (s : Bool) :
    1 - aliveProbR ρ1 ρ2 2 1 k s = death3 ρ1 ρ2 s k := by
  have ht := coin3_total ρ1 ρ2
  simp only [aliveProbR, death3, aliveNext_eq_rule, Finset.sum_range_succ, Finset.sum_range_zero,
    binR, coin3] at ht ⊢
  simp only [zero_add, add_zero, Nat.choose, show k + 1 + 1 = k + 2 by ring,
    show k + 2 + 1 = k + 3 by ring] at ht ⊢
  split_ifs <;> norm_num at ht ⊢ <;> linarith

theorem one_sub_aliveProbR_two (ρ1 ρ2 : ℝ) (k : ℕ) (s : Bool) :
    1 - aliveProbR ρ1 ρ2 2 0 k s = death2 ρ1 s k := by
  have ht := coin2_total ρ1
  simp only [aliveProbR, death2, aliveNext_eq_rule, Finset.sum_range_succ, Finset.sum_range_zero,
    binR, coin2] at ht ⊢
  simp only [zero_add, add_zero, Nat.choose] at ht ⊢
  split_ifs <;> norm_num at ht ⊢ <;> linarith

/-! ### Theorems 1 and 2 for the surrogate on bit masks -/

/-- **Theorems 1 and 2 for every face of the surrogate.**  If cell i of a face with A ≥ 1 cells is alive
next with probability `aliveProbR ρ1 ρ2 (m1 i) (m2 i) (k x i) (x.testBit i)`, where each cell has coins
(2,1) and k ≤ 6, or coins (2,0) and k ≤ 2, then the killed chain at the empty face has a quasi-stationary
law, log τ = ∑_i c_i, and log τ ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) · A. -/
theorem bit_surrogate (A : ℕ) (hA : 0 < A) (ρ1 ρ2 : ℝ) (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2)
    (h2' : ρ2 < 1) (m1 m2 : ℕ → ℕ) (k : ℕ → ℕ → ℕ)
    (hcell : ∀ (x : Fin (2 ^ A)) i, i < A →
      (m1 i = 2 ∧ m2 i = 1 ∧ k x i ≤ 6) ∨ (m1 i = 2 ∧ m2 i = 0 ∧ k x i ≤ 2)) :
    let a : ℕ → ℕ → ℝ := fun x i => aliveProbR ρ1 ρ2 (m1 i) (m2 i) (k x i) ((x : ℕ).testBit i)
    ∃ (hP : ∀ x y, 0 ≤ bitP A a x y) (μ : {x : Fin (2 ^ A) // x ≠ empty A} → ℝ) (lam : ℝ)
      (L : (ofStochastic (bitP A a) (empty A) hP bitP_row).LocalDeath (Fin A)),
      (ofStochastic (bitP A a) (empty A) hP bitP_row).IsQSD μ lam ∧
      Real.log ((ofStochastic (bitP A a) (empty A) hP bitP_row).lifetime μ) = ∑ i, L.price μ i ∧
      Real.log ((ofStochastic (bitP A a) (empty A) hP bitP_row).lifetime μ) ≤
        -Real.log (atomMin ρ1 ρ2) * A := by
  intro a
  have hd : ∀ (x : Fin (2 ^ A)) i, i < A → atomMin ρ1 ρ2 ≤ 1 - a x i := by
    intro x i hi
    rcases hcell x i hi with ⟨e1, e2, hk⟩ | ⟨e1, e2, hk⟩
    · simp only [a, e1, e2, one_sub_aliveProbR_three]
      exact threeCoins_death_ge h1.le h1'.le h2.le h2'.le _ _ hk
    · simp only [a, e1, e2, one_sub_aliveProbR_two]
      exact twoCoins_death_ge h1.le h1'.le h2.le h2'.le _ _ hk
  have hm := atomMin_pos h1 h1' h2 h2'
  have hle1 : ∀ (x : Fin (2 ^ A)) i, i < A → a x i < 1 := fun x i hi => by
    have := hd x i hi; linarith
  have hge0 : ∀ (x : Fin (2 ^ A)) i, i < A → 0 ≤ a x i := fun x i hi => by
    rcases hcell x i hi with ⟨e1, e2, hk⟩ | ⟨e1, e2, hk⟩
    · have e : a x i = 1 - death3 ρ1 ρ2 ((x : ℕ).testBit i) (k x i) := by
        have := one_sub_aliveProbR_three ρ1 ρ2 (k x i) ((x : ℕ).testBit i)
        simp only [a, e1, e2]; linarith
      have : death3 ρ1 ρ2 ((x : ℕ).testBit i) (k x i) ≤ 1 := by
        have ht := coin3_total ρ1 ρ2
        unfold death3
        rw [← ht]
        refine Finset.sum_le_sum (fun b hb => ?_)
        have hb' := mem_range.1 hb
        split_ifs
        · interval_cases b <;> simp [coin3] <;> positivity
        · exact le_refl _
      linarith
    · have e : a x i = 1 - death2 ρ1 ((x : ℕ).testBit i) (k x i) := by
        have := one_sub_aliveProbR_two ρ1 ρ2 (k x i) ((x : ℕ).testBit i)
        simp only [a, e1, e2]; linarith
      have : death2 ρ1 ((x : ℕ).testBit i) (k x i) ≤ 1 := by
        have ht := coin2_total ρ1
        unfold death2
        rw [← ht]
        refine Finset.sum_le_sum (fun b hb => ?_)
        have hb' := mem_range.1 hb
        split_ifs
        · interval_cases b <;> simp [coin2] <;> positivity
        · exact le_refl _
      linarith
  have hP : ∀ x y, 0 ≤ bitP A a x y :=
    bitP_nonneg hge0 (fun x i hi => (hle1 x i hi).le)
  have hne : ∃ x : Fin (2 ^ A), x ≠ empty A :=
    ⟨⟨1, Nat.one_lt_two_pow hA.ne'⟩, by simp [empty, Fin.ext_iff]⟩
  let a' : Fin A → Fin (2 ^ A) → ℝ := fun i x => a x i
  have hprod : ∀ x, x ≠ empty A → bitP A a x (empty A) = ∏ i, (1 - a' i x) := fun x _ => by
    rw [bitP_zero]
    exact (Fin.prod_univ_eq_prod_range (fun i => 1 - a x i) A).symm
  obtain ⟨μ, lam, hμ, he, hb⟩ := surrogate_theorems (V := Fin A) (bitP A a) (empty A) hne hP bitP_row a'
    (fun i x => hge0 x i i.2) (fun i x => hle1 x i i.2) hprod h1 h1' h2 h2' (fun i x => hd x i i.2)
  refine ⟨hP, μ, lam, _, hμ, he, ?_⟩
  simpa using hb

/-- **Lemma 0 on bit masks.**  If in the state u every cell can be alive next, and every state that can
survive one step leads to u, the quasi-stationary law with λ > 0 is unique and charges every living state. -/
theorem bit_one_class (h0 : ∀ (x : Fin (2 ^ A)) i, i < A → 0 ≤ a x i)
    (h1 : ∀ (x : Fin (2 ^ A)) i, i < A → a x i < 1) (u : Fin (2 ^ A)) (hu0 : u ≠ empty A)
    (hu : ∀ i, i < A → 0 < a u i)
    (hreach : ∀ x, (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le))
        bitP_row).CanSurvive x →
      ∃ k, 0 < ((ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le))
        bitP_row).Q ^ k) x ⟨u, hu0⟩) :
    ∃ μ lam, (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le))
        bitP_row).IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      ∀ ν lam', (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le))
        bitP_row).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam :=
  one_class _ ⟨u, hu0⟩ (fun y => (bitP_pos_iff h0 h1 u y).2 (fun i hi _ => hu i hi)) hreach

end Gump.Chain.Bits
