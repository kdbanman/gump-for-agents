/-
`survFrom` of the killed chain is the dice agent's `Face.survival`, cast to ℝ (`survFrom_cast`), on every face
whose empty state is absorbing (`Absorbing`: every hull face by `hull_P_empty_row`, every face with all its coins
by `P_empty_row`). So the decay clause of `hull3_full` and the dice agent's `hull3_lifetime` are statements about
one function, and `hull3_complete` states both, with the dice agent's explicit constants:
0.72 · λ₋^t ≤ P_full(T > t) and P_x(T > t) ≤ 1384 · λ₊^t.
-/
import GumpMath.LinkFaces
import GumpMath.DiceHull

namespace Gump.Link
open Gump.Dice Gump.Chain Gump.Chain.KilledChain
open Finset

/-- The empty face is absorbing: from it, no other state has positive probability. -/
def Absorbing (F : Face) (ρ1 ρ2 : ℚ) : Prop := ∀ y : Fin (2 ^ F.A), y ≠ F.empty → F.P ρ1 ρ2 F.empty y = 0

theorem absorbing_hull (R : ℕ) (ρ1 ρ2 : ℚ) : Absorbing (hull R) ρ1 ρ2 :=
  fun y hy => Face.hull_P_empty_row R ρ1 ρ2 y (fun e => hy ((empty_iff _ y).2 e))

theorem absorbing_of_coins (F : Face) (ρ1 ρ2 : ℚ) (hc : ∀ q, F.coin q = true) : Absorbing F ρ1 ρ2 :=
  fun y hy => Face.P_empty_row F ρ1 ρ2 hc y (fun e => hy ((empty_iff _ y).2 e))

theorem survival_empty_of (F : Face) {ρ1 ρ2 : ℚ} (h : Absorbing F ρ1 ρ2) :
    ∀ t, F.survival ρ1 ρ2 t F.empty = 0
  | 0 => by
    simp only [Face.survival, pow_zero, Matrix.one_mulVec, Face.live]
    exact ite_eq_left_iff.2 (fun h => absurd rfl h)
  | t + 1 => by
    rw [Face.survival_succ]
    refine sum_eq_zero (fun y _ => ?_)
    by_cases hy : y = F.empty
    · rw [hy, survival_empty_of F h t, mul_zero]
    · rw [h y hy, zero_mul]

theorem survFrom_succ' {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ) (t : ℕ) (x : σ) :
    K.survFrom (t + 1) x = ∑ y, K.Q x y * K.survFrom t y := by
  unfold survFrom
  rw [pow_succ', ← Matrix.mulVec_mulVec]
  rfl

/-- **`survFrom` is `Face.survival`**: on every face whose empty state is absorbing, the survival function of
the killed chain from a living state x is the dice agent's P_x(T > t) = ((P^t) · live)(x), cast to ℝ. -/
theorem survFrom_cast (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (h : Absorbing F ρ1 ρ2) :
    ∀ t (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}),
      (chain F hd).survFrom t x = ((F.survival ρ1 ρ2 t x : ℚ) : ℝ)
  | 0, x => by
    rw [survFrom_zero]
    simp only [Face.survival, pow_zero, Matrix.one_mulVec, Face.live]
    rw [if_neg (fun e => x.2 ((empty_iff F x).2 e))]
    norm_num
  | t + 1, x => by
    rw [survFrom_succ', Face.survival_succ]
    push_cast
    rw [← sum_ne_add (fun y => ((F.P ρ1 ρ2 x y : ℚ) : ℝ) * ((F.survival ρ1 ρ2 t y : ℚ) : ℝ)) F.empty,
      survival_empty_of F h t]
    simp only [Rat.cast_zero, mul_zero, add_zero]
    refine sum_congr rfl (fun y _ => ?_)
    rw [chain_Q, survFrom_cast F hd h t y]

theorem lifetime_eq_sum (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ)
    (t : ℕ) : (chain F hd).survival μ t = ∑ x, μ x * (chain F hd).survFrom t x := by
  unfold KilledChain.survival survFrom
  simp only [Matrix.vecMul, Matrix.mulVec, dotProduct, mul_one]
  rw [Finset.sum_comm]
  exact sum_congr rfl (fun x _ => by rw [mul_sum])

namespace Hull3

theorem full_ne : (hull 3).full ≠ (hull 3).empty := fun e => by
  have h := (empty_iff _ _).1 e
  rw [show (((hull 3).full : Fin _) : ℕ) = 511 from rfl] at h
  exact absurd h (by norm_num)

/-- The full face as a living state of the chain. -/
def full' : {x : Fin (2 ^ (hull 3).A) // x ≠ (hull 3).empty} := ⟨(hull 3).full, full_ne⟩

/-- **The lifetime of the face `(hull 3)`, with the decay constants.** Everything in `hull3_full`, and:
the chain's survival function is the dice agent's `Face.survival` (`P_x(T > t)`), the empty face never revives,
and from `hull3_lifetime`: 0.72 · λ₋^t ≤ P_full(T > t), P_x(T > t) ≤ 1384 · λ₊^t for every living x and every t,
with λ₋ ≤ λ ≤ λ₊ the certified interval of the same theorem. -/
theorem hull3_complete :
    ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
      2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧
      (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (hull 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧
      (∀ t x, (chain (hull 3) sdens.dens).survFrom t x = (((hull 3).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧
      (∀ t, (hull 3).survival ρ1 ρ2 t (hull 3).empty = 0) ∧
      (∀ t, (0.72 : ℝ) * 0.9165673655948901373 ^ t ≤ (chain (hull 3) sdens.dens).survFrom t full') ∧
      (∀ t x, (chain (hull 3) sdens.dens).survFrom t x ≤ 1384 * (0.9165673655948901374 : ℝ) ^ t) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hcls, hdec⟩ := hull3_full
  have hc := survFrom_cast (hull 3) sdens.dens (absorbing_hull 3 ρ1 ρ2)
  refine ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hcls, hdec, hc,
    survival_empty_of (hull 3) (absorbing_hull 3 ρ1 ρ2), fun t => ?_, fun t x => ?_⟩
  · rw [hc]
    have h' := Rat.cast_le (K := ℝ) |>.2 (hull3_lifetime t).1
    rw [Rat.cast_mul, Rat.cast_pow] at h'
    have e1 : ((0.72 : ℚ) : ℝ) = 0.72 := by norm_num
    have e2 : ((0.9165673655948901373 : ℚ) : ℝ) = 0.9165673655948901373 := by norm_num
    rw [e1, e2] at h'
    exact h'
  · rw [hc]
    have h' := Rat.cast_le (K := ℝ) |>.2 ((hull3_lifetime t).2 x)
    rw [Rat.cast_mul, Rat.cast_pow] at h'
    have e1 : ((1384 : ℚ) : ℝ) = 1384 := by norm_num
    have e2 : ((0.9165673655948901374 : ℚ) : ℝ) = 0.9165673655948901374 := by norm_num
    rw [e1, e2] at h'
    exact h'

end Hull3

end Gump.Link
