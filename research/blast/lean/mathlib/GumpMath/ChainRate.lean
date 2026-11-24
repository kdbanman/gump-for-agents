/-
The quasi-stationary rate is the rate seen from every start (the step from "τ := E_μ T" to the lifetime a
simulation from a fair start measures).

`decay_bounds`: for a killed chain whose states that can survive form one irreducible class C (every other
state dying surely), with w > 0 the Perron column vector of the block on C (eigenvalue r) and m ≤ w ≤ M:
  for x ∈ C and every t,  (m/M) r^t ≤ P_x(T > t)   and   P_x(T > t + 1) ≤ (M/m) r^t,
and every quasi-stationary law with λ > 0 has λ = r.  So (1/t) log P_x(T > t) → log λ from every x ∈ C, and
the mean lifetime from x lies between (m/M)/(1 - λ) and 1 + (M/m)/(1 - λ) (`lifetime_from_bounds`), i.e.
log E_x T = log τ up to log(M/m) + O(1).  The spread M/m of the Perron vector is not bounded here.
-/
import Mathlib
import GumpMath.ChainInst

set_option linter.unusedSectionVars false

namespace Gump.Chain.KilledChain
open Finset Matrix

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

/-- P_x(T > t) = ∑_y (Q^t)(x, y). -/
def survFrom (K : KilledChain σ) (t : ℕ) (x : σ) : ℝ := ((K.Q ^ t) *ᵥ (fun _ => (1 : ℝ))) x

/-- E_x T = ∑_t P_x(T > t). -/
noncomputable def lifetimeFrom (K : KilledChain σ) (x : σ) : ℝ := ∑' t, K.survFrom t x

theorem survFrom_nonneg (K : KilledChain σ) (t : ℕ) (x : σ) : 0 ≤ K.survFrom t x := by
  unfold survFrom
  simp only [Matrix.mulVec, dotProduct, mul_one]
  exact Finset.sum_nonneg (fun y _ => pow_entry_nonneg K.nonneg t x y)

/-- **Decay at the quasi-stationary rate from every start in the living class.** -/
theorem decay_bounds (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] [Nonempty {x // p x}]
    (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) :
    ∃ r m M : ℝ, 0 ≤ r ∧ 0 < m ∧ m ≤ M ∧
      (∀ ν lam, K.IsQSD ν lam → 0 < lam → lam = r) ∧
      (∀ t x, p x → m / M * r ^ t ≤ K.survFrom t x) ∧
      (∀ t x, K.survFrom (t + 1) x ≤ M / m * r ^ t) := by
  obtain ⟨r, hr, w, hw, hwe⟩ := exists_pos_eigenvector (A := K.block p) (fun a b => K.nonneg a b) hirr
  set m := univ.inf' univ_nonempty w with hm
  set M := univ.sup' univ_nonempty w with hM
  have hmw : ∀ a, m ≤ w a := fun a => Finset.inf'_le _ (mem_univ a)
  have hwM : ∀ a, w a ≤ M := fun a => Finset.le_sup' _ (mem_univ a)
  obtain ⟨a0⟩ := ‹Nonempty {x // p x}›
  have hm0 : 0 < m := by
    rw [hm, Finset.lt_inf'_iff]; exact fun a _ => hw a
  have hmM : m ≤ M := (hmw a0).trans (hwM a0)
  -- the Perron vector, extended by zero off the class
  let W : σ → ℝ := fun x => if h : p x then w ⟨x, h⟩ else 0
  have hW0 : ∀ x, 0 ≤ W x := fun x => by
    simp only [W]; split_ifs
    · exact (hw _).le
    · exact le_refl _
  have hWe : ∀ x, (K.Q *ᵥ W) x = r * W x := fun x => by
    by_cases hx : p x
    · have h1 := congrFun hwe ⟨x, hx⟩
      simp only [Matrix.mulVec, dotProduct, Pi.smul_apply, smul_eq_mul, block] at h1
      simp only [Matrix.mulVec, dotProduct]
      rw [← Fintype.sum_subtype_add_sum_subtype p]
      have h0 : ∑ i : {x // ¬ p x}, K.Q x i * W i = 0 :=
        Finset.sum_eq_zero (fun i _ => by simp [W, i.2])
      rw [h0, add_zero]
      simp only [W, hx, ↓reduceDIte]
      have : ∑ i : {x // p x}, K.Q x i * (if h : p i then w ⟨i, h⟩ else 0) =
          ∑ i : {x // p x}, K.Q x i * w i := Finset.sum_congr rfl (fun i _ => by simp [i.2])
      rw [this, h1]
    · simp only [Matrix.mulVec, dotProduct, hout x hx, zero_mul, Finset.sum_const_zero, W, hx]
      simp
  have hQ := K.nonneg
  have hup := Gump.Certificate.pow_mulVec_le K.Q hQ W r hr (fun x => (hWe x).le)
  have hlo := Gump.Certificate.le_pow_mulVec K.Q hQ W r hr (fun x => (hWe x).ge)
  refine ⟨r, m, M, hr, hm0, hmM, ?_, ?_, ?_⟩
  · -- every QSD with λ > 0 has the Perron eigenvalue
    intro ν lam hν hlam
    have hpair : lam * ∑ x, ν x * W x = r * ∑ x, ν x * W x := by
      have e1 : ∑ y, (∑ x, ν x * K.Q x y) * W y = ∑ x, ν x * (K.Q *ᵥ W) x := by
        simp only [Matrix.mulVec, dotProduct, Finset.sum_mul, Finset.mul_sum]
        rw [Finset.sum_comm]; exact Finset.sum_congr rfl (fun x _ => Finset.sum_congr rfl
          (fun y _ => by ring))
      simp_rw [hν.eigen, hWe] at e1
      simp only [Finset.mul_sum]
      rw [← Finset.sum_congr rfl (fun y _ => by ring : ∀ y ∈ univ, lam * ν y * W y = lam * (ν y * W y))]
      rw [← Finset.sum_congr rfl (fun x _ => by ring : ∀ x ∈ univ, ν x * (r * W x) = r * (ν x * W x))]
      rw [← e1]
    have hpos : 0 < ∑ x, ν x * W x := by
      have hmass := hν.block_mass_pos p hout hlam
      obtain ⟨a, ha⟩ := exists_pos_term hmass
      exact Finset.sum_pos' (fun x _ => mul_nonneg (hν.nonneg x) (hW0 x))
        ⟨a, mem_univ _, mul_pos ha (by simp [W, a.2, hw])⟩
    exact mul_right_cancel₀ hpos.ne' hpair
  · -- lower bound: 1 ≥ W / M
    intro t x hx
    have h1 : ∀ y, W y / M ≤ 1 := fun y => by
      rw [div_le_one (hm0.trans_le hmM)]
      simp only [W]; split_ifs
      · exact hwM _
      · exact (hm0.trans_le hmM).le
    have hmono := Gump.Certificate.mulVec_mono (K.Q ^ t) (pow_entry_nonneg hQ t) h1 x
    have hsc := Gump.Certificate.mulVec_smul_fun (K.Q ^ t) (1 / M) W x
    have hwx : m ≤ W x := by simp only [W, hx, ↓reduceDIte]; exact hmw _
    have hlx := hlo t x
    unfold survFrom
    calc m / M * r ^ t ≤ r ^ t * W x / M := by
          rw [div_mul_eq_mul_div, mul_comm m]
          exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left hwx (pow_nonneg hr t))
            (hm0.trans_le hmM).le
      _ ≤ ((K.Q ^ t) *ᵥ W) x / M := div_le_div_of_nonneg_right hlx (hm0.trans_le hmM).le
      _ = ((K.Q ^ t) *ᵥ (fun y => 1 / M * W y)) x := by rw [hsc]; ring
      _ ≤ ((K.Q ^ t) *ᵥ (fun _ => (1 : ℝ))) x := by
          convert hmono using 2; funext y; ring
  · -- upper bound: Q 1 ≤ W / m
    intro t x
    have h1 : ∀ y, (K.Q *ᵥ (fun _ => (1 : ℝ))) y ≤ 1 / m * W y := fun y => by
      by_cases hy : p y
      · have hs : (K.Q *ᵥ (fun _ => (1 : ℝ))) y ≤ 1 := by
          simp only [Matrix.mulVec, dotProduct, mul_one]; exact K.sub y
        have : 1 ≤ 1 / m * W y := by
          simp only [W, hy, ↓reduceDIte]; rw [one_div, inv_mul_eq_div, le_div_iff₀ hm0, one_mul]
          exact hmw _
        linarith
      · simp only [Matrix.mulVec, dotProduct, hout y hy, zero_mul, Finset.sum_const_zero, W, hy]
        simp
    have hmono := Gump.Certificate.mulVec_mono (K.Q ^ t) (pow_entry_nonneg hQ t) h1 x
    have hsc := Gump.Certificate.mulVec_smul_fun (K.Q ^ t) (1 / m) W x
    have hux := hup t x
    have hWx : W x ≤ M := by
      simp only [W]; split_ifs
      · exact hwM _
      · exact (hm0.trans_le hmM).le
    unfold survFrom
    rw [pow_succ, ← Matrix.mulVec_mulVec]
    calc ((K.Q ^ t) *ᵥ (K.Q *ᵥ fun _ => (1 : ℝ))) x ≤ ((K.Q ^ t) *ᵥ fun y => 1 / m * W y) x := hmono
      _ = 1 / m * ((K.Q ^ t) *ᵥ W) x := hsc
      _ ≤ 1 / m * (r ^ t * W x) := mul_le_mul_of_nonneg_left hux (by positivity)
      _ ≤ 1 / m * (r ^ t * M) :=
          mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hWx (pow_nonneg hr t)) (by positivity)
      _ = M / m * r ^ t := by ring

theorem survFrom_zero (K : KilledChain σ) (x : σ) : K.survFrom 0 x = 1 := by
  simp [survFrom]

/-- **The mean lifetime from any living start is τ up to the Perron vector's spread**:
(m/M)/(1 - λ) ≤ E_x T ≤ 1 + (M/m)/(1 - λ), with λ = r < 1 the quasi-stationary eigenvalue. -/
theorem lifetime_from_bounds (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] [Nonempty {x // p x}]
    (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) :
    ∃ r m M : ℝ, 0 ≤ r ∧ 0 < m ∧ m ≤ M ∧
      (∀ ν lam, K.IsQSD ν lam → 0 < lam → lam = r) ∧
      (r < 1 → ∀ x, p x → m / M / (1 - r) ≤ K.lifetimeFrom x ∧
        K.lifetimeFrom x ≤ 1 + M / m / (1 - r)) := by
  obtain ⟨r, m, M, hr, hm, hmM, hq, hlo, hup⟩ := K.decay_bounds p hirr hout
  refine ⟨r, m, M, hr, hm, hmM, hq, fun hr1 x hx => ?_⟩
  have hgeo : Summable (fun t : ℕ => r ^ t) := summable_geometric_of_lt_one hr hr1
  have hsum1 : Summable (fun t => K.survFrom (t + 1) x) :=
    Summable.of_nonneg_of_le (fun t => K.survFrom_nonneg _ _) (fun t => hup t x) (hgeo.mul_left _)
  have hsum : Summable (fun t => K.survFrom t x) := (summable_nat_add_iff 1).1 hsum1
  constructor
  · have := Summable.tsum_le_tsum (fun t => hlo t x hx) (hgeo.mul_left _) hsum
    rw [tsum_mul_left, tsum_geometric_of_lt_one hr hr1] at this
    unfold lifetimeFrom
    calc m / M / (1 - r) = m / M * (1 - r)⁻¹ := by ring
      _ ≤ _ := this
  · unfold lifetimeFrom
    rw [hsum.tsum_eq_zero_add, survFrom_zero]
    have := Summable.tsum_le_tsum (fun t => hup t x) hsum1 (hgeo.mul_left _)
    rw [tsum_mul_left, tsum_geometric_of_lt_one hr hr1] at this
    have e : M / m / (1 - r) = M / m * (1 - r)⁻¹ := by ring
    rw [e]; linarith

end Gump.Chain.KilledChain
