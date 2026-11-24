/-
The seam identity of `research/blast/image/README.md` (section "The identity"; checked by the referee,
`research/blast/ref-proofs/REVIEW.md` B), as an identity between ring products of a transfer matrix.

Setting.  A ring of bands, each band in a finite set B of band histories, with weight the product around
the ring of one non-negative matrix F (the transfer matrix 𝒯): the weight of the ring a₀, a₁, …, a_{N-1}
is F a₀ a₁ · F a₁ a₂ ⋯ F a_{N-1} a₀ (`ringL`).  That every rule factor touches at most two consecutive
bands, so that the space-time weight of a history factorises this way, and that the cover has the same F,
is the modelling step of the source (bands two graph steps thick); it is the hypothesis here.

The torus has m = M + 1 bands; its configurations are cut at the seam: (a, xs) with a the seam's band and
xs : Fin M → B the others.  The cover has N = m + L bands, cut at the seam and at its image one loop along:
(a, xs, c, ys), c the image of the seam.  `torusW_eq_ringL` and `coverW_eq_ringL` say these are the ring
products of the concatenated lists.  Proved:
  `sum_pathF`        ∑ over the interior of an open path = (F^(n+1)) a b (Chapman–Kolmogorov);
  `torusZ`, `coverZ` the normalisations are Tr F^m and Tr F^N;
  `cover_marginal`   ∑_ys W_C(a, xs, a, ys) = W_T(a, xs) · (F^L) a a;
  `seam_identity`    P_T(a, xs) = P_C(a, xs, image = a) · Tr F^N / (Tr F^m · (F^L) a a), for F ≥ 0 and L a
                     multiple of m (then (F^L) a a = 0 forces P_T(a, ·) = 0, and both sides vanish):
                     "a torus is its cover conditioned on the seam's history recurring one loop along,
                     divided by how likely that recurrence is";
  `seam_identity_obs` the same for the mean of any observable of the torus (the window form ★);
  `seam_sharp`       the double cover with traces 1 (a deterministic rule from a normalised soup):
                     P_C(seam = a, rest = xs, image = a) = P_T(a, xs) · P_T(seam = a).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace Gump.Chain.Seam
open Finset Matrix

variable {B : Type*} [Fintype B] [DecidableEq B] (F : Matrix B B ℝ)

/-- The weight F a c₀ · F c₀ c₁ ⋯ F c_{k-1} b of the path a, c₀, …, c_{k-1}, b. -/
def pathL : B → List B → B → ℝ
  | a, [], b => F a b
  | a, c :: l, b => F a c * pathL c l b

/-- The weight of a ring a₀, a₁, …, a_{N-1}: the product around the ring. -/
def ringL : List B → ℝ
  | [] => 1
  | a :: l => pathL F a l a

theorem pathL_append (a b c : B) (l₁ l₂ : List B) :
    pathL F a (l₁ ++ c :: l₂) b = pathL F a l₁ c * pathL F c l₂ b := by
  induction l₁ generalizing a with
  | nil => rfl
  | cons d l ih => simp only [List.cons_append, pathL, ih, mul_assoc]

/-- The same path with its interior given as a function on Fin n. -/
def pathF : (n : ℕ) → B → (Fin n → B) → B → ℝ
  | 0, a, _, b => F a b
  | n + 1, a, x, b => F a (x 0) * pathF n (x 0) (Fin.tail x) b

theorem pathF_eq_pathL (n : ℕ) (a b : B) (x : Fin n → B) :
    pathF F n a x b = pathL F a (List.ofFn x) b := by
  induction n generalizing a with
  | zero => simp [pathF, pathL]
  | succ n ih => rw [pathF, List.ofFn_succ, pathL, ih]; rfl

/-- **Chapman–Kolmogorov**: summing a path's interior gives a matrix power. -/
theorem sum_pathF (n : ℕ) (a b : B) : ∑ x : Fin n → B, pathF F n a x b = (F ^ (n + 1)) a b := by
  induction n generalizing a with
  | zero => simp [pathF]
  | succ n ih =>
    rw [← (Fin.consEquiv (fun _ : Fin (n + 1) => B)).sum_comp, Fintype.sum_prod_type]
    simp only [Fin.consEquiv, Equiv.coe_fn_mk, pathF, Fin.cons_zero, Fin.tail_cons]
    simp_rw [← Finset.mul_sum, ih]
    rw [pow_succ' F (n + 1), Matrix.mul_apply]

/-- The torus of M + 1 bands, cut at the seam a. -/
def torusW (M : ℕ) (a : B) (xs : Fin M → B) : ℝ := pathF F M a xs a

/-- The cover of (M + 1) + (L' + 1) bands, cut at the seam a and at its image c. -/
def coverW (M L' : ℕ) (a : B) (xs : Fin M → B) (c : B) (ys : Fin L' → B) : ℝ :=
  pathF F M a xs c * pathF F L' c ys a

theorem torusW_eq_ringL (M : ℕ) (a : B) (xs : Fin M → B) :
    torusW F M a xs = ringL F (a :: List.ofFn xs) := by
  simp [torusW, ringL, pathF_eq_pathL]

theorem coverW_eq_ringL (M L' : ℕ) (a : B) (xs : Fin M → B) (c : B) (ys : Fin L' → B) :
    coverW F M L' a xs c ys = ringL F (a :: (List.ofFn xs ++ c :: List.ofFn ys)) := by
  simp [coverW, ringL, pathF_eq_pathL, pathL_append]

theorem torusZ (M : ℕ) : ∑ a, ∑ xs : Fin M → B, torusW F M a xs = Matrix.trace (F ^ (M + 1)) := by
  simp only [torusW, sum_pathF, Matrix.trace, Matrix.diag]

theorem coverZ (M L' : ℕ) :
    ∑ a, ∑ xs : Fin M → B, ∑ c, ∑ ys : Fin L' → B, coverW F M L' a xs c ys =
      Matrix.trace (F ^ (M + 1 + (L' + 1))) := by
  have e : ∀ a, ∑ xs : Fin M → B, ∑ c, ∑ ys : Fin L' → B, coverW F M L' a xs c ys =
      ∑ c, (F ^ (M + 1)) a c * (F ^ (L' + 1)) c a := by
    intro a
    simp only [coverW, ← Finset.mul_sum, sum_pathF]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun c _ => ?_)
    rw [← Finset.sum_mul, sum_pathF]
  simp only [e, Matrix.trace, Matrix.diag, pow_add F (M + 1) (L' + 1), Matrix.mul_apply]

/-- **The cover's marginal** on the seam, the rest of the torus's bands, and the seam's image. -/
theorem cover_marginal (M L' : ℕ) (a : B) (xs : Fin M → B) :
    ∑ ys : Fin L' → B, coverW F M L' a xs a ys = torusW F M a xs * (F ^ (L' + 1)) a a := by
  simp only [coverW, ← Finset.mul_sum, sum_pathF, torusW]

/-- The torus law and the cover law. -/
noncomputable def PT (M : ℕ) (a : B) (xs : Fin M → B) : ℝ :=
  torusW F M a xs / Matrix.trace (F ^ (M + 1))

noncomputable def PC (M L' : ℕ) (a : B) (xs : Fin M → B) (c : B) (ys : Fin L' → B) : ℝ :=
  coverW F M L' a xs c ys / Matrix.trace (F ^ (M + 1 + (L' + 1)))

theorem pathF_nonneg (hF : ∀ i j, 0 ≤ F i j) (n : ℕ) (a b : B) (x : Fin n → B) : 0 ≤ pathF F n a x b := by
  induction n generalizing a with
  | zero => exact hF a b
  | succ n ih => exact mul_nonneg (hF _ _) (ih _ _)

theorem pow_nonneg_entry (hF : ∀ i j, 0 ≤ F i j) (k : ℕ) (i j : B) : 0 ≤ (F ^ k) i j := by
  induction k generalizing j with
  | zero => simp only [pow_zero, Matrix.one_apply]; split <;> norm_num
  | succ k ih =>
    rw [pow_succ, Matrix.mul_apply]
    exact Finset.sum_nonneg (fun l _ => mul_nonneg (ih l) (hF l j))

/-- A closed path of length m at a repeats: (F^(j m)) a a ≥ ((F^m) a a)^j. -/
theorem pow_mul_diag_ge (hF : ∀ i j, 0 ≤ F i j) (m j : ℕ) (a : B) :
    ((F ^ m) a a) ^ j ≤ (F ^ (m * j)) a a := by
  induction j with
  | zero => simp
  | succ j ih =>
    rw [pow_succ, mul_add, mul_one, pow_add, Matrix.mul_apply]
    calc (F ^ m) a a ^ j * (F ^ m) a a ≤ (F ^ (m * j)) a a * (F ^ m) a a :=
          mul_le_mul_of_nonneg_right ih (pow_nonneg_entry F hF m a a)
      _ ≤ ∑ l, (F ^ (m * j)) a l * (F ^ m) l a :=
          single_le_sum (f := fun l => (F ^ (m * j)) a l * (F ^ m) l a)
            (fun l _ => mul_nonneg (pow_nonneg_entry F hF _ _ _) (pow_nonneg_entry F hF _ _ _))
            (mem_univ a)

/-- **The seam identity.**  For F ≥ 0 and a cover whose extra length L = L' + 1 is a whole number k ≥ 1
of loops (L = k · (M + 1)): P_T(a, xs) = P_C(a, xs, image = a) · Tr F^N / (Tr F^m · (F^L) a a). -/
theorem seam_identity (hF : ∀ i j, 0 ≤ F i j) (M L' k : ℕ) (hk : 1 ≤ k) (hL : L' + 1 = k * (M + 1))
    (a : B) (xs : Fin M → B) :
    PT F M a xs = (∑ ys : Fin L' → B, PC F M L' a xs a ys) *
      Matrix.trace (F ^ (M + 1 + (L' + 1))) / (Matrix.trace (F ^ (M + 1)) * (F ^ (L' + 1)) a a) := by
  simp only [PC, ← Finset.sum_div, cover_marginal, PT]
  by_cases h0 : (F ^ (L' + 1)) a a = 0
  · -- then (F^m) a a = 0, every torus weight at a vanishes, and both sides are 0
    have hm : (F ^ (M + 1)) a a = 0 := by
      have h := pow_mul_diag_ge F hF (M + 1) k a
      rw [mul_comm, ← hL, h0] at h
      have hnn := pow_nonneg_entry F hF (M + 1) a a
      exact (pow_eq_zero_iff (by omega)).1 (le_antisymm h (pow_nonneg hnn k))
    have hw : torusW F M a xs = 0 := by
      have hs : ∑ ys : Fin M → B, torusW F M a ys = 0 := by simp only [torusW, sum_pathF, hm]
      exact (Finset.sum_eq_zero_iff_of_nonneg (fun ys _ => pathF_nonneg F hF M a a ys)).1 hs xs
        (mem_univ xs)
    simp [hw]
  · by_cases hN : Matrix.trace (F ^ (M + 1 + (L' + 1))) = 0
    · -- then every cover weight vanishes, in particular torusW · F^L(a,a) = 0
      have hw : torusW F M a xs * (F ^ (L' + 1)) a a = 0 := by
        rw [← cover_marginal]
        have hz := coverZ F M L'
        rw [hN] at hz
        have hnn : ∀ a xs c ys, 0 ≤ coverW F M L' a xs c ys := fun a xs c ys =>
          mul_nonneg (pathF_nonneg F hF _ _ _ _) (pathF_nonneg F hF _ _ _ _)
        have h1 := (Finset.sum_eq_zero_iff_of_nonneg (fun a _ => Finset.sum_nonneg (fun xs _ =>
          Finset.sum_nonneg (fun c _ => Finset.sum_nonneg (fun ys _ => hnn a xs c ys))))).1 hz a
          (mem_univ a)
        have h2 := (Finset.sum_eq_zero_iff_of_nonneg (fun xs _ => Finset.sum_nonneg (fun c _ =>
          Finset.sum_nonneg (fun ys _ => hnn a xs c ys)))).1 h1 xs (mem_univ xs)
        have h3 := (Finset.sum_eq_zero_iff_of_nonneg (fun c _ =>
          Finset.sum_nonneg (fun ys _ => hnn a xs c ys))).1 h2 a (mem_univ a)
        exact h3
      have : torusW F M a xs = 0 := (mul_eq_zero.1 hw).resolve_right h0
      simp [this]
    · field_simp

/-- **The window form (★)**: for any observable f of the torus, its torus mean is the cover mean of f
over histories whose seam recurs, each weighted by Tr F^N / (Tr F^m · (F^L) a a). -/
theorem seam_identity_obs (hF : ∀ i j, 0 ≤ F i j) (M L' k : ℕ) (hk : 1 ≤ k)
    (hL : L' + 1 = k * (M + 1)) (f : B → (Fin M → B) → ℝ) :
    ∑ a, ∑ xs, PT F M a xs * f a xs =
      ∑ a, ∑ xs, ∑ ys : Fin L' → B, PC F M L' a xs a ys * f a xs *
        (Matrix.trace (F ^ (M + 1 + (L' + 1))) / (Matrix.trace (F ^ (M + 1)) * (F ^ (L' + 1)) a a)) := by
  refine Finset.sum_congr rfl (fun a _ => Finset.sum_congr rfl (fun xs _ => ?_))
  rw [seam_identity F hF M L' k hk hL a xs, ← Finset.sum_mul, ← Finset.sum_mul]
  ring

/-- The torus's law of its seam: P_T(seam = a) = (F^m) a a / Tr F^m. -/
theorem PT_seam (M : ℕ) (a : B) :
    ∑ xs : Fin M → B, PT F M a xs = (F ^ (M + 1)) a a / Matrix.trace (F ^ (M + 1)) := by
  simp only [PT, ← Finset.sum_div, torusW, sum_pathF]

/-- **The sharp form for the double cover** (the referee's K = 2 check): if Tr F^m = Tr F^{2m} = 1
(a deterministic rule started from a normalised soup), then
P_C(seam = a, rest = xs, image = a) = P_T(a, xs) · P_T(seam = a). -/
theorem seam_sharp (M : ℕ) (h1 : Matrix.trace (F ^ (M + 1)) = 1)
    (h2 : Matrix.trace (F ^ (M + 1 + (M + 1))) = 1) (a : B) (xs : Fin M → B) :
    ∑ ys : Fin M → B, PC F M M a xs a ys = PT F M a xs * ∑ ys : Fin M → B, PT F M a ys := by
  simp only [PC, cover_marginal, PT, h1, h2, div_one]
  rw [show ∑ ys : Fin M → B, torusW F M a ys = (F ^ (M + 1)) a a from sum_pathF F M a a]

end Gump.Chain.Seam
