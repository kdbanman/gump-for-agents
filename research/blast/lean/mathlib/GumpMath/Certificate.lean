/-
Certified rates for a killed finite Markov chain, with no spectral theory.

Q is a non-negative matrix on a finite set of living states: Q i j is the probability of going from
i to j in one generation without dying, so (Q ^ t *ᵥ 1) i is the probability of surviving t
generations from i. A vector v with Q v ≤ λ v entrywise bounds survival above by a multiple of λ ^ t;
a vector with Q v ≥ μ v bounds it below by a multiple of μ ^ t. Each is one induction. A vector
found by any program outside Lean therefore certifies a two-sided bound on the chain's death rate
inside Lean, in exact arithmetic.
-/
import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.Order.Ring.Defs
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

open Matrix

namespace Gump.Certificate

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable {R : Type*} [CommRing R] [LinearOrder R] [IsStrictOrderedRing R]

/-- A non-negative matrix is monotone. -/
theorem mulVec_mono (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) {u w : ι → R}
    (h : ∀ i, u i ≤ w i) : ∀ i, (Q *ᵥ u) i ≤ (Q *ᵥ w) i := by
  intro i
  simp only [Matrix.mulVec, dotProduct]
  exact Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_left (h j) (hQ i j))

theorem mulVec_smul_fun (Q : Matrix ι ι R) (a : R) (v : ι → R) (i : ι) :
    (Q *ᵥ (fun j => a * v j)) i = a * (Q *ᵥ v) i := by
  simp only [Matrix.mulVec, dotProduct, Finset.mul_sum]
  exact Finset.sum_congr rfl (fun j _ => by ring)

/-- **Upper certificate.** If Q ≥ 0 and Q v ≤ λ v entrywise, then Q ^ t v ≤ λ ^ t v. -/
theorem pow_mulVec_le (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) (v : ι → R) (lam : R)
    (hlam : 0 ≤ lam) (h : ∀ i, (Q *ᵥ v) i ≤ lam * v i) :
    ∀ (t : ℕ) (i : ι), ((Q ^ t) *ᵥ v) i ≤ lam ^ t * v i := by
  intro t
  induction t with
  | zero => intro i; simp
  | succ t ih =>
    intro i
    have e : (Q ^ (t + 1)) *ᵥ v = Q *ᵥ (Q ^ t *ᵥ v) := by rw [pow_succ', Matrix.mulVec_mulVec]
    rw [e]
    calc (Q *ᵥ (Q ^ t *ᵥ v)) i ≤ (Q *ᵥ (fun j => lam ^ t * v j)) i := mulVec_mono Q hQ ih i
      _ = lam ^ t * (Q *ᵥ v) i := mulVec_smul_fun Q _ v i
      _ ≤ lam ^ t * (lam * v i) := mul_le_mul_of_nonneg_left (h i) (pow_nonneg hlam t)
      _ = lam ^ (t + 1) * v i := by ring

/-- **Lower certificate.** If Q ≥ 0 and Q v ≥ μ v entrywise, then Q ^ t v ≥ μ ^ t v. -/
theorem le_pow_mulVec (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) (v : ι → R) (mu : R)
    (hmu : 0 ≤ mu) (h : ∀ i, mu * v i ≤ (Q *ᵥ v) i) :
    ∀ (t : ℕ) (i : ι), mu ^ t * v i ≤ ((Q ^ t) *ᵥ v) i := by
  intro t
  induction t with
  | zero => intro i; simp
  | succ t ih =>
    intro i
    have e : (Q ^ (t + 1)) *ᵥ v = Q *ᵥ (Q ^ t *ᵥ v) := by rw [pow_succ', Matrix.mulVec_mulVec]
    rw [e]
    calc mu ^ (t + 1) * v i = mu ^ t * (mu * v i) := by ring
      _ ≤ mu ^ t * (Q *ᵥ v) i := mul_le_mul_of_nonneg_left (h i) (pow_nonneg hmu t)
      _ = (Q *ᵥ (fun j => mu ^ t * v j)) i := (mulVec_smul_fun Q _ v i).symm
      _ ≤ (Q *ᵥ (Q ^ t *ᵥ v)) i := mulVec_mono Q hQ ih i

/-- Powers of a non-negative matrix are non-negative. -/
theorem pow_nonneg' (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) : ∀ (t : ℕ) (i j : ι), 0 ≤ (Q ^ t) i j := by
  intro t
  induction t with
  | zero => intro i j; simp only [pow_zero, Matrix.one_apply]; split <;> simp
  | succ t ih =>
    intro i j
    rw [pow_succ, Matrix.mul_apply]
    exact Finset.sum_nonneg (fun k _ => mul_nonneg (ih i k) (hQ k j))

/-- **Survival is at most c · λ ^ t · v.** With c ≥ 0 and c v ≥ 1 everywhere, the chance of surviving t
generations from state i is at most c λ ^ t v i. -/
theorem survival_le (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) (v : ι → R) (lam c : R)
    (hlam : 0 ≤ lam) (hc : 0 ≤ c) (h : ∀ i, (Q *ᵥ v) i ≤ lam * v i) (hv : ∀ i, 1 ≤ c * v i) :
    ∀ (t : ℕ) (i : ι), ((Q ^ t) *ᵥ (fun _ => (1 : R))) i ≤ c * (lam ^ t * v i) := by
  intro t i
  have hQt := pow_nonneg' Q hQ t
  calc ((Q ^ t) *ᵥ (fun _ => (1 : R))) i ≤ ((Q ^ t) *ᵥ (fun j => c * v j)) i :=
        mulVec_mono (Q ^ t) hQt hv i
    _ = c * ((Q ^ t) *ᵥ v) i := mulVec_smul_fun (Q ^ t) c v i
    _ ≤ c * (lam ^ t * v i) :=
        mul_le_mul_of_nonneg_left (pow_mulVec_le Q hQ v lam hlam h t i) hc

/-- **Survival is at least μ ^ t · v / C.** With v ≤ C everywhere, C times the chance of surviving t
generations from state i is at least μ ^ t v i. -/
theorem survival_ge (Q : Matrix ι ι R) (hQ : ∀ i j, 0 ≤ Q i j) (v : ι → R) (mu C : R)
    (hmu : 0 ≤ mu) (h : ∀ i, mu * v i ≤ (Q *ᵥ v) i) (hv : ∀ i, v i ≤ C) :
    ∀ (t : ℕ) (i : ι), mu ^ t * v i ≤ C * ((Q ^ t) *ᵥ (fun _ => (1 : R))) i := by
  intro t i
  calc mu ^ t * v i ≤ ((Q ^ t) *ᵥ v) i := le_pow_mulVec Q hQ v mu hmu h t i
    _ ≤ ((Q ^ t) *ᵥ (fun _ => C * 1)) i := mulVec_mono (Q ^ t) (pow_nonneg' Q hQ t) (by simpa using hv) i
    _ = C * ((Q ^ t) *ᵥ (fun _ => (1 : R))) i := mulVec_smul_fun (Q ^ t) C (fun _ => 1) i

end Gump.Certificate
