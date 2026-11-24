/-
The Perron-type facts Theorem 2 and Lemma 0 of `research/blast/rigour/THEOREMS.md` need, built here
(Mathlib has no Perron–Frobenius theorem).

  `exists_pos_eigenvector`       an irreducible non-negative matrix on a finite set has a strictly positive
                                 eigenvector with a non-negative eigenvalue (Wielandt's proof: maximise the
                                 Collatz–Wielandt function on the compact image of the simplex under the
                                 positive matrix ∑_{k ≤ N} A^k).
  `exists_pos_left_eigenvector`  the same for row vectors.
  `left_eigen_pos`               a non-negative non-zero row eigenvector of an irreducible matrix is positive.
  `left_eigen_unique`            two probability row eigenvectors of an irreducible matrix are equal and have
                                 the same eigenvalue.
  `qsd_exists_unique`            **one living class**: a killed chain whose living states are one irreducible
                                 class C, aperiodic somewhere, plus states that die surely and are entered
                                 from C, has exactly one quasi-stationary law with λ > 0, and it charges every
                                 state.  This is the consequence of Lemma 0 used by Theorem 2.
  `price_invariant`              with that uniqueness, a symmetry of the chain and of its local factors
                                 leaves the local prices c_i invariant (one price per orbit of cells).
-/
import Mathlib
import GumpMath.Certificate
import GumpMath.ChainTilt

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Matrix

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

/-- Irreducible: every state leads to every other one with positive probability in some number of steps. -/
def Irreducible (A : Matrix σ σ ℝ) : Prop := ∀ x y, ∃ k : ℕ, 0 < (A ^ k) x y

theorem pow_entry_nonneg {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j) (k : ℕ) (i j : σ) :
    0 ≤ (A ^ k) i j :=
  Gump.Certificate.pow_nonneg' A hA k i j

theorem vecMul_pow_of_eigen {A : Matrix σ σ ℝ} {ν : σ → ℝ} {lam : ℝ} (he : ν ᵥ* A = lam • ν) (k : ℕ) :
    ν ᵥ* (A ^ k) = lam ^ k • ν := by
  induction k with
  | zero => simp
  | succ k ih => rw [pow_succ, ← Matrix.vecMul_vecMul, ih, Matrix.smul_vecMul, he, smul_smul, pow_succ]

/-- The probability vectors (the standard simplex), with its compactness proved here. -/
def probSet (σ : Type*) [Fintype σ] : Set (σ → ℝ) := {f | (∀ x, 0 ≤ f x) ∧ ∑ x, f x = 1}

theorem isCompact_probSet : IsCompact (probSet σ) := by
  apply IsCompact.of_isClosed_subset (isCompact_Icc (a := (0 : σ → ℝ)) (b := 1))
  · have e : probSet σ = (⋂ i, {f : σ → ℝ | 0 ≤ f i}) ∩ {f | ∑ x, f x = 1} := by
      ext f; simp [probSet]
    rw [e]
    apply IsClosed.inter
    · exact isClosed_iInter (fun i => isClosed_le continuous_const (continuous_apply i))
    · exact isClosed_eq (by fun_prop) continuous_const
  · intro f hf
    refine ⟨fun i => hf.1 i, fun i => ?_⟩
    have := single_le_sum (f := f) (fun j _ => hf.1 j) (mem_univ i)
    rw [hf.2] at this; exact this

theorem exists_pos_poly {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j) (hirr : Irreducible A) :
    ∃ N : ℕ, ∀ x y, 0 < (∑ k ∈ range (N + 1), A ^ k) x y := by
  choose k hk using hirr
  refine ⟨univ.sup (fun p : σ × σ => k p.1 p.2), fun x y => ?_⟩
  rw [Matrix.sum_apply]
  have hmem : k x y ∈ range (univ.sup (fun p : σ × σ => k p.1 p.2) + 1) := by
    rw [mem_range, Nat.lt_succ_iff]
    exact le_sup (f := fun p : σ × σ => k p.1 p.2) (mem_univ (x, y))
  exact lt_of_lt_of_le (hk x y) (single_le_sum (fun j _ => pow_entry_nonneg hA j x y) hmem)

/-- **Perron (existence), by Wielandt's argument.**  An irreducible non-negative matrix on a nonempty finite
set has an eigenvector with every entry positive, for a non-negative eigenvalue. -/
theorem exists_pos_eigenvector [Nonempty σ] {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j)
    (hirr : Irreducible A) :
    ∃ r : ℝ, 0 ≤ r ∧ ∃ v : σ → ℝ, (∀ i, 0 < v i) ∧ A *ᵥ v = r • v := by
  obtain ⟨N, hP⟩ := exists_pos_poly hA hirr
  set P : Matrix σ σ ℝ := ∑ k ∈ range (N + 1), A ^ k with hPdef
  have hcomm : P * A = A * P := by
    rw [hPdef, Finset.sum_mul, Finset.mul_sum]
    exact Finset.sum_congr rfl (fun k _ => pow_mul_comm' A k)
  have hPpos : ∀ x : σ → ℝ, (∀ i, 0 ≤ x i) → (∃ j, 0 < x j) → ∀ i, 0 < (P *ᵥ x) i := by
    rintro x hx ⟨j, hj⟩ i
    simp only [Matrix.mulVec, dotProduct]
    exact lt_of_lt_of_le (mul_pos (hP i j) hj)
      (single_le_sum (f := fun j => P i j * x j) (fun j _ => mul_nonneg (hP i j).le (hx j)) (mem_univ j))
  set S : Set (σ → ℝ) := (fun x => P *ᵥ x) '' probSet σ with hSdef
  have hScpt : IsCompact S :=
    isCompact_probSet.image (continuous_const.matrix_mulVec continuous_id)
  have hSpos : ∀ y ∈ S, ∀ i, 0 < y i := by
    rintro y ⟨x, hx, rfl⟩ i
    obtain ⟨j, hj⟩ := exists_pos_of_isProb (μ := x) ⟨hx.1, hx.2⟩
    exact hPpos x hx.1 ⟨j, hj⟩ i
  obtain ⟨i0⟩ := ‹Nonempty σ›
  have hSne : S.Nonempty := by
    refine ⟨_, Pi.single i0 1, ⟨fun x => ?_, ?_⟩, rfl⟩
    · by_cases h : x = i0
      · subst h; simp
      · simp [h]
    · simp
  let r : (σ → ℝ) → ℝ := fun y => univ.inf' univ_nonempty (fun i => (A *ᵥ y) i / y i)
  have hrc : ContinuousOn r S := by
    apply ContinuousOn.finset_inf'_apply
    intro i _
    apply ContinuousOn.div
    · exact ((continuous_apply i).comp (continuous_const.matrix_mulVec continuous_id)).continuousOn
    · exact (continuous_apply i).continuousOn
    · exact fun y hy => (hSpos y hy i).ne'
  obtain ⟨z, hzS, hzmax⟩ := hScpt.exists_isMaxOn hSne hrc
  set ρ := r z with hρ
  have hzpos := hSpos z hzS
  have hρle : ∀ i, ρ * z i ≤ (A *ᵥ z) i := fun i => by
    have : ρ ≤ (A *ᵥ z) i / z i := Finset.inf'_le _ (mem_univ i)
    rwa [le_div_iff₀ (hzpos i)] at this
  have hAz_nonneg : ∀ i, 0 ≤ (A *ᵥ z) i := fun i => by
    simp only [Matrix.mulVec, dotProduct]
    exact sum_nonneg (fun j _ => mul_nonneg (hA i j) (hzpos j).le)
  have heq : A *ᵥ z = ρ • z := by
    by_contra hne
    have hex : ∃ j, ρ * z j < (A *ᵥ z) j := by
      by_contra h
      push Not at h
      apply hne; funext i
      simp only [Pi.smul_apply, smul_eq_mul]
      exact le_antisymm (h i) (hρle i)
    obtain ⟨j, hj⟩ := hex
    set u : σ → ℝ := A *ᵥ z - ρ • z with hu_def
    have hu : ∀ i, 0 ≤ u i := fun i => by
      simp only [u, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; linarith [hρle i]
    have huj : 0 < u j := by simp only [u, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; linarith
    have hPu := hPpos u hu ⟨j, huj⟩
    set w := P *ᵥ z with hw_def
    have hw : ∀ i, 0 < w i := hPpos z (fun i => (hzpos i).le) ⟨i0, hzpos i0⟩
    have hPu' : P *ᵥ u = A *ᵥ w - ρ • w := by
      simp only [u, w, Matrix.mulVec_sub, Matrix.mulVec_smul, Matrix.mulVec_mulVec, hcomm]
    have hgt : ∀ i, ρ < (A *ᵥ w) i / w i := fun i => by
      rw [lt_div_iff₀ (hw i)]
      have := hPu i
      rw [hPu'] at this
      simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
      linarith
    set c := ∑ i, z i with hc_def
    have hc : 0 < c := Finset.sum_pos (fun i _ => hzpos i) univ_nonempty
    have hx1 : c⁻¹ • z ∈ probSet σ := by
      refine ⟨fun i => ?_, ?_⟩
      · simp only [Pi.smul_apply, smul_eq_mul]
        exact mul_nonneg (inv_nonneg.2 hc.le) (hzpos i).le
      · simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum, ← hc_def]
        exact inv_mul_cancel₀ hc.ne'
    have hmem : P *ᵥ (c⁻¹ • z) ∈ S := ⟨_, hx1, rfl⟩
    have hrscale : r (P *ᵥ (c⁻¹ • z)) = r w := by
      simp only [r, Matrix.mulVec_smul]
      congr 1; funext i
      simp only [Pi.smul_apply, smul_eq_mul, ← hw_def]
      have : c⁻¹ ≠ 0 := inv_ne_zero hc.ne'
      field_simp
    have h1 : ρ < r w := (Finset.lt_inf'_iff _).2 (fun i _ => hgt i)
    have h2 := isMaxOn_iff.1 hzmax _ hmem
    rw [hrscale] at h2
    linarith
  refine ⟨ρ, ?_, z, hzpos, heq⟩
  by_contra hneg
  push Not at hneg
  have := hAz_nonneg i0
  rw [heq] at this
  simp only [Pi.smul_apply, smul_eq_mul] at this
  nlinarith [hzpos i0]

theorem Irreducible.transpose {A : Matrix σ σ ℝ} (h : Irreducible A) : Irreducible Aᵀ := fun x y => by
  obtain ⟨k, hk⟩ := h y x
  exact ⟨k, by rw [← Matrix.transpose_pow]; exact hk⟩

/-- **Perron (existence), row version**: a positive left eigenvector. -/
theorem exists_pos_left_eigenvector [Nonempty σ] {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j)
    (hirr : Irreducible A) :
    ∃ r : ℝ, 0 ≤ r ∧ ∃ v : σ → ℝ, (∀ i, 0 < v i) ∧ v ᵥ* A = r • v := by
  obtain ⟨r, hr, v, hv, he⟩ := exists_pos_eigenvector (A := Aᵀ) (fun i j => hA j i) hirr.transpose
  exact ⟨r, hr, v, hv, by rw [← Matrix.mulVec_transpose]; exact he⟩

/-- A non-negative, non-zero row eigenvector of an irreducible non-negative matrix is positive. -/
theorem left_eigen_pos {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j) (hirr : Irreducible A)
    {ν : σ → ℝ} {lam : ℝ} (hν : ∀ x, 0 ≤ ν x) (hne : ∃ x, 0 < ν x) (he : ν ᵥ* A = lam • ν) :
    ∀ y, 0 < ν y := by
  intro y
  by_contra hy
  have hy0 : ν y = 0 := le_antisymm (not_lt.1 hy) (hν y)
  obtain ⟨x0, hx0⟩ := hne
  obtain ⟨k, hk⟩ := hirr x0 y
  have h1 : (ν ᵥ* (A ^ k)) y = 0 := by
    rw [vecMul_pow_of_eigen he]; simp [hy0]
  have h2 : 0 < (ν ᵥ* (A ^ k)) y := by
    simp only [Matrix.vecMul, dotProduct]
    exact lt_of_lt_of_le (mul_pos hx0 hk)
      (single_le_sum (f := fun x => ν x * (A ^ k) x y)
        (fun x _ => mul_nonneg (hν x) (pow_entry_nonneg hA k x y)) (mem_univ x0))
  linarith

/-- Every probability row eigenvector of an irreducible non-negative matrix has the eigenvalue of the
positive column eigenvector. -/
theorem left_eigenvalue_eq {A : Matrix σ σ ℝ} {u : σ → ℝ} {r : ℝ} (hu : ∀ i, 0 < u i)
    (heu : A *ᵥ u = r • u) {ξ : σ → ℝ} {l : ℝ} (hξ : IsProb ξ) (hl : ξ ᵥ* A = l • ξ) : l = r := by
  have h1 : ξ ⬝ᵥ (A *ᵥ u) = (ξ ᵥ* A) ⬝ᵥ u := Matrix.dotProduct_mulVec ξ A u
  rw [heu, hl, dotProduct_smul, smul_dotProduct, smul_eq_mul, smul_eq_mul] at h1
  have hpos : 0 < ξ ⬝ᵥ u := by
    obtain ⟨x, hx⟩ := exists_pos_of_isProb hξ
    simp only [dotProduct]
    exact sum_pos' (fun y _ => mul_nonneg (hξ.1 y) (hu y).le) ⟨x, mem_univ x, mul_pos hx (hu x)⟩
  exact (mul_right_cancel₀ hpos.ne' h1).symm

/-- **Perron (uniqueness).**  Two probability row eigenvectors of an irreducible non-negative matrix are
equal and have the same eigenvalue. -/
theorem left_eigen_unique [Nonempty σ] {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j)
    (hirr : Irreducible A) {μ ν : σ → ℝ} {lam lam' : ℝ}
    (hμ : IsProb μ) (hν : IsProb ν) (he : μ ᵥ* A = lam • μ) (he' : ν ᵥ* A = lam' • ν) :
    lam = lam' ∧ μ = ν := by
  obtain ⟨r, -, u, hu, heu⟩ := exists_pos_eigenvector hA hirr
  have hl := left_eigenvalue_eq hu heu hμ he
  have hl' := left_eigenvalue_eq hu heu hν he'
  refine ⟨hl.trans hl'.symm, ?_⟩
  have hμp := left_eigen_pos hA hirr hμ.1 (exists_pos_of_isProb hμ) he
  obtain ⟨x0, -, hx0⟩ := exists_min_image univ (fun x => ν x / μ x) univ_nonempty
  set c := ν x0 / μ x0 with hc
  set ξ : σ → ℝ := ν - c • μ with hξ
  have hξnn : ∀ x, 0 ≤ ξ x := fun x => by
    have h := hx0 x (mem_univ x)
    simp only [ξ, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    rw [div_le_div_iff₀ (hμp x0) (hμp x)] at h
    have : c * μ x = ν x0 * μ x / μ x0 := by rw [hc]; ring
    have h' : ν x0 * μ x / μ x0 ≤ ν x := by rw [div_le_iff₀ (hμp x0)]; linarith
    rw [this]; linarith
  have hξ0 : ξ x0 = 0 := by
    simp only [ξ, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, hc]
    field_simp [(hμp x0).ne']; ring
  have hξe : ξ ᵥ* A = lam • ξ := by
    rw [hξ, Matrix.sub_vecMul, Matrix.smul_vecMul, he, he', ← hl.trans hl'.symm, smul_sub, smul_comm]
  have hξz : ∀ x, ξ x = 0 := by
    by_contra h
    push Not at h
    obtain ⟨x, hx⟩ := h
    have := left_eigen_pos hA hirr hξnn ⟨x, lt_of_le_of_ne (hξnn x) (Ne.symm hx)⟩ hξe x0
    linarith
  have hνc : ∀ x, ν x = c * μ x := fun x => by
    have := hξz x
    simp only [ξ, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
    linarith
  have hc1 : c = 1 := by
    have := hν.2
    simp_rw [hνc, ← Finset.mul_sum, hμ.2, mul_one] at this
    exact this
  funext x; rw [hνc x, hc1, one_mul]

namespace KilledChain

/-- The block of `Q` on the states satisfying `p`. -/
def block (K : KilledChain σ) (p : σ → Prop) : Matrix {x // p x} {x // p x} ℝ := fun a b => K.Q a b

theorem IsQSD.block_eigen {K : KilledChain σ} (p : σ → Prop) [DecidablePred p]
    (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) {ν : σ → ℝ} {lam : ℝ} (hν : K.IsQSD ν lam) :
    (fun a : {x // p x} => ν a) ᵥ* K.block p = lam • (fun a : {x // p x} => ν a) := by
  funext b
  have h := hν.eigen b
  rw [← Fintype.sum_subtype_add_sum_subtype p] at h
  have h0 : ∑ i : {x // ¬ p x}, ν i * K.Q i b = 0 :=
    Finset.sum_eq_zero (fun i _ => by rw [hout i i.2 b, mul_zero])
  rw [h0, add_zero] at h
  simpa [Matrix.vecMul, dotProduct, block] using h

/-- The mass a quasi-stationary law with λ > 0 puts on the class is positive. -/
theorem IsQSD.block_mass_pos {K : KilledChain σ} (p : σ → Prop) [DecidablePred p]
    (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) {ν : σ → ℝ} {lam : ℝ} (hν : K.IsQSD ν lam)
    (hlam : 0 < lam) : 0 < ∑ a : {x // p x}, ν a := by
  rcases (Finset.sum_nonneg (fun a _ => hν.nonneg a) : 0 ≤ ∑ a : {x // p x}, ν a).lt_or_eq with h | h
  · exact h
  · exfalso
    have hz : ∀ a : {x // p x}, ν a = 0 := fun a =>
      (Finset.sum_eq_zero_iff_of_nonneg (s := univ) (f := fun a : {x // p x} => ν a)
        (fun a _ => hν.nonneg a)).1 h.symm a (mem_univ a)
    have hall : ∀ y, ν y = 0 := fun y => by
      have e := hν.eigen y
      rw [← Fintype.sum_subtype_add_sum_subtype p] at e
      have h1 : ∑ i : {x // p x}, ν i * K.Q i y = 0 :=
        Finset.sum_eq_zero (fun i _ => by rw [hz i, zero_mul])
      have h2 : ∑ i : {x // ¬ p x}, ν i * K.Q i y = 0 :=
        Finset.sum_eq_zero (fun i _ => by rw [hout i i.2 y, mul_zero])
      rw [h1, h2, add_zero] at e
      exact (mul_eq_zero.1 e.symm).resolve_left hlam.ne'
    have := hν.total
    simp [hall] at this

/-- **One living class ⇒ one quasi-stationary law (the consequence of Lemma 0).**  Suppose the states
satisfying `p` form one irreducible class of `Q`, with a state `u` in it with `Q u u > 0`; every other
state dies surely in one step, and is entered from the class.  Then there is exactly one quasi-stationary
law with λ > 0, and it charges every state. -/
theorem qsd_exists_unique (K : KilledChain σ) (p : σ → Prop) [DecidablePred p]
    (hirr : Irreducible (K.block p))
    (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0)
    (hin : ∀ y, ¬ p y → ∃ x, p x ∧ 0 < K.Q x y)
    (hu : ∃ u, p u ∧ 0 < K.Q u u) :
    ∃ μ lam, K.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam := by
  obtain ⟨u, hpu, hQu⟩ := hu
  have : Nonempty {x // p x} := ⟨⟨u, hpu⟩⟩
  have : Nonempty σ := ⟨u⟩
  have hB : ∀ a b, 0 ≤ K.block p a b := fun a b => K.nonneg a b
  obtain ⟨r, -, v, hv, hve⟩ := exists_pos_left_eigenvector hB hirr
  have hve' : ∀ b : {x // p x}, ∑ a : {x // p x}, v a * K.Q a b = r * v b := fun b => by
    have := congrFun hve b
    simpa [Matrix.vecMul, dotProduct, block] using this
  -- r > 0, from the aperiodic state u
  have hr : 0 < r := by
    have e := hve' ⟨u, hpu⟩
    have : v ⟨u, hpu⟩ * K.Q u u ≤ ∑ a : {x // p x}, v a * K.Q a u :=
      single_le_sum (f := fun a : {x // p x} => v a * K.Q a u)
        (fun a _ => mul_nonneg (hv a).le (K.nonneg a u)) (mem_univ (⟨u, hpu⟩ : {x // p x}))
    have hpos := mul_pos (hv ⟨u, hpu⟩) hQu
    by_contra h
    push Not at h
    nlinarith [hv ⟨u, hpu⟩]
  -- extend v off the class
  let w : σ → ℝ := fun x => if h : p x then v ⟨x, h⟩ else r⁻¹ * ∑ a : {x // p x}, v a * K.Q a x
  have hwin : ∀ a : {x // p x}, w a = v a := fun a => by simp [w, a.2]
  have hwpos : ∀ x, 0 < w x := fun x => by
    by_cases h : p x
    · simp only [w, h]; exact hv _
    · simp only [w, h]
      obtain ⟨x', hx', hq⟩ := hin x h
      apply mul_pos (inv_pos.2 hr)
      exact lt_of_lt_of_le (mul_pos (hv ⟨x', hx'⟩) hq)
        (single_le_sum (f := fun a : {x // p x} => v a * K.Q a x)
          (fun a _ => mul_nonneg (hv a).le (K.nonneg a x)) (mem_univ (⟨x', hx'⟩ : {x // p x})))
  have hweig : ∀ y, ∑ x, w x * K.Q x y = r * w y := fun y => by
    rw [← Fintype.sum_subtype_add_sum_subtype p]
    have h0 : ∑ i : {x // ¬ p x}, w i * K.Q i y = 0 :=
      Finset.sum_eq_zero (fun i _ => by rw [hout i i.2 y, mul_zero])
    rw [h0, add_zero]
    simp_rw [hwin]
    by_cases h : p y
    · have := hve' ⟨y, h⟩; simp only at this; rw [this]; simp [w, h]
    · rw [show w y = r⁻¹ * ∑ a : {x // p x}, v a * K.Q a y by simp [w, h]]
      field_simp
  set S := ∑ x, w x with hS
  have hSpos : 0 < S := Finset.sum_pos (fun x _ => hwpos x) univ_nonempty
  set μ : σ → ℝ := fun x => w x / S with hμdef
  have hμ : K.IsQSD μ r := by
    refine ⟨fun x => (div_pos (hwpos x) hSpos).le, ?_, fun y => ?_⟩
    · simp only [μ, ← Finset.sum_div, ← hS]; exact div_self hSpos.ne'
    · simp only [μ, div_mul_eq_mul_div, ← Finset.sum_div, hweig y]; ring
  refine ⟨μ, r, hμ, hr, fun x => div_pos (hwpos x) hSpos, ?_⟩
  intro ν lam' hν hlam'
  -- restrict both to the class, normalise, and use uniqueness there
  have hmν := hν.block_mass_pos p hout hlam'
  have hmμ := hμ.block_mass_pos p hout hr
  set mν := ∑ a : {x // p x}, ν a
  set mμ := ∑ a : {x // p x}, μ a
  have hPν : IsProb (fun a : {x // p x} => ν a / mν) :=
    ⟨fun a => div_nonneg (hν.nonneg a) hmν.le, by rw [← Finset.sum_div]; exact div_self hmν.ne'⟩
  have hPμ : IsProb (fun a : {x // p x} => μ a / mμ) :=
    ⟨fun a => div_nonneg (hμ.nonneg a) hmμ.le, by rw [← Finset.sum_div]; exact div_self hmμ.ne'⟩
  have heν : (fun a : {x // p x} => ν a / mν) ᵥ* K.block p = lam' • (fun a : {x // p x} => ν a / mν) := by
    have := hν.block_eigen p hout
    have e : (fun a : {x // p x} => ν a / mν) = mν⁻¹ • (fun a : {x // p x} => ν a) := by
      funext a; simp [div_eq_inv_mul]
    rw [e, Matrix.smul_vecMul, this, smul_comm]
  have heμ : (fun a : {x // p x} => μ a / mμ) ᵥ* K.block p = r • (fun a : {x // p x} => μ a / mμ) := by
    have := hμ.block_eigen p hout
    have e : (fun a : {x // p x} => μ a / mμ) = mμ⁻¹ • (fun a : {x // p x} => μ a) := by
      funext a; simp [div_eq_inv_mul]
    rw [e, Matrix.smul_vecMul, this, smul_comm]
  obtain ⟨hlr, heq⟩ := left_eigen_unique hB hirr hPμ hPν heμ heν
  set c := mν / mμ with hc
  have hin' : ∀ a : {x // p x}, ν a = c * μ a := fun a => by
    have := congrFun heq a
    rw [hc]; field_simp at this ⊢; linarith
  have hall : ∀ y, ν y = c * μ y := fun y => by
    by_cases h : p y
    · exact hin' ⟨y, h⟩
    · have e1 := hν.eigen y
      have e2 := hμ.eigen y
      rw [← Fintype.sum_subtype_add_sum_subtype p] at e1 e2
      have h1 : ∑ i : {x // ¬ p x}, ν i * K.Q i y = 0 :=
        Finset.sum_eq_zero (fun i _ => by rw [hout i i.2 y, mul_zero])
      have h2 : ∑ i : {x // ¬ p x}, μ i * K.Q i y = 0 :=
        Finset.sum_eq_zero (fun i _ => by rw [hout i i.2 y, mul_zero])
      rw [h1, add_zero] at e1
      rw [h2, add_zero] at e2
      simp_rw [hin', mul_assoc, ← Finset.mul_sum, e2] at e1
      rw [← hlr] at e1
      have : r * ν y = r * (c * μ y) := by linarith
      exact mul_left_cancel₀ hr.ne' this
  have hc1 : c = 1 := by
    have := hν.total
    simp_rw [hall, ← Finset.mul_sum, hμ.total, mul_one] at this
    exact this
  refine ⟨funext fun y => by rw [hall y, hc1, one_mul], hlr.symm⟩

open LocalDeath in
/-- **One price per orbit.**  If the quasi-stationary law with λ > 0 is unique, a permutation `g` of the
states that preserves `Q`, together with a permutation `π` of the cells that carries the local factors
along (d_{π i}(g x) = d_i(x)), leaves every local price invariant: c_{π i} = c_i. -/
theorem price_invariant {V : Type*} [Fintype V] {K : KilledChain σ} (L : K.LocalDeath V)
    {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) (hlam : 0 < lam)
    (huniq : ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ)
    (g : σ ≃ σ) (hg : ∀ x y, K.Q (g x) (g y) = K.Q x y) (π : V ≃ V)
    (hc : ∀ i x, L.dc (π i) (g x) = L.dc i x) (i : V) : L.price μ (π i) = L.price μ i := by
  have hνq : K.IsQSD (fun x => μ (g x)) lam := by
    refine ⟨fun x => hμ.nonneg _, ?_, fun y => ?_⟩
    · rw [Equiv.sum_comp g μ]; exact hμ.total
    · have := hμ.eigen (g y)
      rw [← Equiv.sum_comp g] at this
      simpa [hg] using this
  have hinv : (fun x => μ (g x)) = μ := huniq _ _ hνq hlam
  have hinv' : ∀ x, μ (g x) = μ x := fun x => congrFun hinv x
  have hE : ∀ x, L.energy (g x) = L.energy x := fun x => by
    simp only [energy, cost]
    rw [← Equiv.sum_comp π]
    simp [hc]
  have hcost : ∀ x, L.cost (π i) (g x) = L.cost i x := fun x => by simp [cost, hc]
  have hZ : ∀ s, Z μ L.energy s = Z μ L.energy s := fun s => rfl
  simp only [price]
  congr 1; funext s
  simp only [tiltMean, Z, tw]
  rw [← Equiv.sum_comp g (fun x => μ x * Real.exp (-(s * L.energy x)) * L.cost (π i) x),
    ← Equiv.sum_comp g (fun x => μ x * Real.exp (-(s * L.energy x)))]
  simp only [hinv', hE, hcost]

end KilledChain
end Gump.Chain
