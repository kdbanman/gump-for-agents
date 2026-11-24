/-
The two exits of a face of the dice surrogate: the bust and the fade, as `rigour/qsd.c` defines them
("halffall_share"): a death is a **bust** if its last K transitions (the death itself included) contain a fall
of at least half = ⌈A/2⌉ live cells in one generation; otherwise it is a **fade**.

`Face.noBust K x` = P_x(T = K and no fall ≥ half in the K transitions), by the recursion
    noBust 0 v = [v = ∅],   noBust (k+1) u = [u ≠ ∅] Σ_v P(u, v) [pop u - pop v < half] noBust k v.
For a quasi-stationary law (μ, λ) the death time from μ is geometric and the window before a death at T ≥ K
starts from μ, so the share of the death flux through the bust is
    bustShare K μ λ = 1 - μ·noBust K / (λ ^ (K-1) (1 - λ))      (P_μ(T = K) = λ ^ (K-1) (1 - λ)),
the quantity `qsd.c ... bust` prints as `halffall_share K=…` (README claim 4 uses K = 6).
The identification of this formula with the share of the death flux (stationarity of the window) is the
standard argument above, written in prose, not formalised; the theorems are about `bustShare` as defined.

Certificates (`dice_exit.py`): the vectors D^k noBust k (exact integers, checked row by row by the masked
contraction `Tree.mask`), and a Poisson certificate p, w with |noBust K - p d - (λ' w - P w)| ≤ ε d and
|w| ≤ ω d (d(x) = P(x, ∅)); then for every quasi-stationary law, |μ·noBust K / μ·d - p| ≤ ε + |λ' - λ| ω.
-/
import GumpMath.DiceBound

namespace Gump.Dice
open Gump Finset Matrix

/-- The number of set bits of y below n. -/
def lowPop (n y : ℕ) : ℕ := (List.range n).countP fun i => y.testBit i

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

/-- The population of a state. -/
def pop (x : ℕ) : ℕ := lowPop F.A x

/-- Half the face, rounded up (`qsd.c`: half = (A + 1) / 2). -/
def half : ℕ := (F.A + 1) / 2

/-- P_x(T = k and none of the k transitions is a fall of at least half the face). -/
def noBust : ℕ → Fin (2 ^ F.A) → ℚ
  | 0, v => if (v : ℕ) = 0 then 1 else 0
  | k + 1, u => if (u : ℕ) = 0 then 0 else
      ∑ v, F.P ρ1 ρ2 u v * (if F.pop u < F.pop v + F.half then noBust k v else 0)

/-- **The bust share** of a quasi-stationary law (μ, λ): the share of its death flux whose last K transitions
contain a fall of at least half the face. -/
noncomputable def bustShare (K : ℕ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) : ℝ :=
  1 - (∑ x, μ x * (F.noBust ρ1 ρ2 K x : ℝ)) / (lam ^ (K - 1) * (1 - lam))

end Face

namespace Tree

/-- Keep the entries whose index has c + (set bits) satisfying p; the others become 0. -/
def mask : Tree → ℕ → ℕ → (ℕ → Bool) → Tree
  | leaf a, 0, m, p => if p m then leaf a else leaf 0
  | node l r, n + 1, m, p => node (l.mask n m p) (r.mask n (m + 1) p)
  | t, _, _, _ => t

theorem lowPop_succ (n y : ℕ) : lowPop (n + 1) y = lowPop n y + if y.testBit n then 1 else 0 := by
  simp only [lowPop, List.range_succ, List.countP_append, List.countP_singleton]

theorem get_mask : ∀ (t : Tree) (n m : ℕ) (p : ℕ → Bool) (y : ℕ),
    (t.mask n m p).get n y = if p (m + lowPop n y) then t.get n y else 0
  | leaf a, 0, m, p, y => by
      simp only [mask, lowPop, List.range_zero, List.countP_nil, add_zero]
      split <;> simp [get]
  | leaf _, _ + 1, _, _, _ => by simp [mask, get]
  | node _ _, 0, _, _, _ => by simp [mask, get]
  | node l r, n + 1, m, p, y => by
      simp only [mask, get, lowPop_succ]
      by_cases hb : y.testBit n
      · simp only [hb, ite_true, get_mask r n (m + 1) p y, show m + 1 + lowPop n y = m + (lowPop n y + 1) by omega]
      · simp only [hb, Bool.false_eq_true, ite_false, get_mask l n m p y, add_zero]

end Tree

namespace Data
variable (c : Data) (F : Face)

/-- Row check for one step of the recursion, D ^ (k+1) noBust (k+1) from D ^ k noBust k. -/
def nbRow (A hf : ℕ) (Nk Nk1 : Tree) (u : ℕ) : Bool :=
  if u = 0 then Nk.get A 0 == 0 else
    Nk.get A u == (Nk1.mask A 0 (fun m => decide (lowPop A u < m + hf))).eval A (c.fac u)

/-- The base: the tree of [v = ∅]. -/
def nbBase (A : ℕ) (N0 : Tree) : Bool :=
  allRows (fun v => N0.get A v == if v = 0 then 1 else 0) (2 ^ A)

theorem nbBase_spec (A : ℕ) (N0 : Tree) (h : nbBase A N0 = true) (ρ1 ρ2 : ℚ) (F : Face) (hA : F.A = A)
    (v : Fin (2 ^ F.A)) : (N0.get F.A v : ℚ) = (c.Dt F.A : ℚ) ^ 0 * F.noBust ρ1 ρ2 0 v := by
  subst hA
  have := allRows_spec _ _ h v v.isLt
  simp only [beq_iff_eq] at this
  rw [this, Face.noBust]; split <;> simp

theorem nbRow_spec (htab : c.tabOK F = true) (Nk Nk1 : Tree) (k : ℕ)
    (hr : allRows (c.nbRow F.A F.half Nk Nk1) (2 ^ F.A) = true)
    (hrep : ∀ v : Fin (2 ^ F.A), (Nk1.get F.A v : ℚ) =
      (c.Dt F.A : ℚ) ^ k * F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) k v)
    (u : Fin (2 ^ F.A)) :
    (Nk.get F.A u : ℚ) = (c.Dt F.A : ℚ) ^ (k + 1) * F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) (k + 1) u := by
  have hu := allRows_spec _ _ hr u u.isLt
  simp only [nbRow, beq_iff_eq] at hu
  by_cases h0 : (u : ℕ) = 0
  · simp only [h0, ite_true] at hu
    rw [Face.noBust, if_pos h0, h0, beq_iff_eq.mp hu]; simp
  · simp only [h0, ite_false] at hu
    have hD : (0 : ℚ) < c.Dt F.A := by
      rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F htab i
    set M := Nk1.mask F.A 0 (fun m => decide (lowPop F.A u < m + F.half))
    have hm := c.mulVec_eq F htab M u
    have hv : vec M F.A = fun (v : Fin (2 ^ F.A)) => if F.pop u < F.pop v + F.half then
        (c.Dt F.A : ℚ) ^ k * F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) k v else 0 := by
      funext v
      simp only [vec, M, Tree.get_mask, zero_add, Face.pop, decide_eq_true_eq]
      by_cases hc : lowPop F.A u < lowPop F.A v + F.half
      · simp only [hc, ite_true]; exact hrep v
      · simp only [hc, ite_false, Nat.cast_zero]
    rw [hv] at hm
    rw [beq_iff_eq.mp hu, Face.noBust, if_neg h0]
    have : (M.eval F.A (c.fac u) : ℚ) = c.Dt F.A * ((c.Dt F.A : ℚ) ^ k *
        ∑ v, F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) u v *
          (if F.pop u < F.pop v + F.half then F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) k v else 0)) := by
      have hE := (div_eq_iff hD.ne').mp hm.symm
      rw [hE]
      simp only [mulVec, dotProduct, mul_sum, sum_mul]
      refine sum_congr rfl fun v _ => ?_
      split <;> ring
    rw [this]; ring

/-- For a quasi-stationary law, μ·d = 1 - λ. -/
theorem qsd_death (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) :
    ∑ x, μ x * (F.P ρ1 ρ2 x F.empty : ℝ) = 1 - lam := by
  have h1 : ∑ x, μ x * ((F.P ρ1 ρ2 *ᵥ F.live) x : ℝ) = lam * ∑ y, μ y * (F.live y : ℝ) :=
    qsd_pair F ρ1 ρ2 μ lam hq F.live (fun y hy => by simp [Face.live, hy])
  have hl : ∀ y, (F.live y : ℝ) = 1 - (if y = F.empty then 1 else 0) := by
    intro y
    by_cases hy : (y : ℕ) = 0
    · have : y = F.empty := Fin.ext hy
      rw [if_pos this]; simp [Face.live, hy]
    · have : y ≠ F.empty := fun h => hy (by rw [h]; rfl)
      rw [if_neg this]; simp [Face.live, hy]
  have hrow : ∀ x, ((F.P ρ1 ρ2 *ᵥ F.live) x : ℝ) = 1 - (F.P ρ1 ρ2 x F.empty : ℝ) := by
    intro x
    simp only [mulVec, dotProduct, Rat.cast_sum, Rat.cast_mul, hl, mul_sub, mul_one, mul_ite, mul_zero,
      sum_sub_distrib, sum_ite_eq', mem_univ, ite_true]
    rw [← Rat.cast_sum, Face.P_row_sum, Rat.cast_one]
  have hmass : ∑ y, μ y * (F.live y : ℝ) = 1 := by
    rw [← hq.total]; refine sum_congr rfl fun y _ => ?_
    by_cases hy : (y : ℕ) = 0
    · simp [Face.live, hy, hq.empty y hy]
    · simp [Face.live, hy]
  simp only [hrow, mul_sub, mul_one, sum_sub_distrib, hq.total, hmass, mul_one] at h1
  linarith

/-- The Poisson certificate check at row x ≠ 0, in exact rationals: with d = P(x, ∅), w = (W⁺ - W⁻)/S,
|D^-K N_K(x) - p d - (λ' w(x) - (P w)(x))| ≤ ε d and |w(x)| ≤ ω d. -/
def poisRow (A Dt K : ℕ) (NK Wp Wm : Tree) (S : ℕ) (p lam' eps om : ℚ) (x : ℕ) : Bool :=
  x == 0 || (
    decide (|(NK.get A x : ℚ) / (Dt : ℚ) ^ K - p * (((∏ i ∈ range A, (c.fac x i).1 : ℕ) : ℚ) / Dt) -
        (lam' * (((Wp.get A x : ℚ) - Wm.get A x) / S) -
          ((Wp.eval A (c.fac x) : ℚ) - Wm.eval A (c.fac x)) / (Dt * S))| ≤
      eps * (((∏ i ∈ range A, (c.fac x i).1 : ℕ) : ℚ) / Dt)) &&
    decide (|((Wp.get A x : ℚ) - Wm.get A x) / S| ≤ om * (((∏ i ∈ range A, (c.fac x i).1 : ℕ) : ℚ) / Dt)))

theorem death_eq (htab : c.tabOK F = true) (x : Fin (2 ^ F.A)) :
    F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x F.empty =
      ((∏ i ∈ range F.A, (c.fac x i).1 : ℕ) : ℚ) / (c.Dt F.A : ℚ) := by
  rw [c.P_eq F htab]
  congr 2
  refine prod_congr rfl fun i _ => ?_
  simp [Tree.sel, Face.empty]

/-- **The Poisson bound.** For every quasi-stationary law (μ, λ): |μ·N_K - p (1 - λ)| ≤ (ε + |λ' - λ| ω)(1 - λ). -/
theorem poisson_bound (htab : c.tabOK F = true) (K : ℕ) (NK Wp Wm : Tree) (S : ℕ) (hS : 0 < S)
    (p lam' eps om : ℚ)
    (hr : allRows (c.poisRow F.A (c.Dt F.A) K NK Wp Wm S p lam' eps om) (2 ^ F.A) = true)
    (hw0 : Wp.get F.A 0 = 0 ∧ Wm.get F.A 0 = 0)
    (hrep : ∀ v : Fin (2 ^ F.A), (NK.get F.A v : ℚ) =
      (c.Dt F.A : ℚ) ^ K * F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) K v)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) μ lam) :
    |∑ x, μ x * (F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) K x : ℝ) - (p : ℝ) * (1 - lam)| ≤
      ((eps : ℝ) + |(lam' : ℝ) - lam| * om) * (1 - lam) := by
  set P := F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2)
  set N := F.noBust ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) K
  have hD : (0 : ℚ) < c.Dt F.A := by
    rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F htab i
  have hS' : (0 : ℚ) < S := by exact_mod_cast hS
  set w : Fin (2 ^ F.A) → ℚ := fun y => ((Wp.get F.A y : ℚ) - Wm.get F.A y) / S
  set d : Fin (2 ^ F.A) → ℚ := fun x => P x F.empty
  have hw0' : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → w y = 0 := fun y hy => by simp [w, hy, hw0.1, hw0.2]
  have hPw : ∀ x, (P *ᵥ w) x = ((Wp.eval F.A (c.fac x) : ℚ) - Wm.eval F.A (c.fac x)) / (c.Dt F.A * S) := by
    intro x
    have e1 := c.mulVec_eq F htab Wp x
    have e2 := c.mulVec_eq F htab Wm x
    have : w = fun y => (1 / (S : ℚ)) * (vec Wp F.A y - vec Wm F.A y) := by
      funext y; simp only [w, vec]; ring
    rw [this]
    simp only [mulVec, dotProduct] at e1 e2 ⊢
    have : ∑ y, P x y * ((1 / (S : ℚ)) * (vec Wp F.A y - vec Wm F.A y)) =
        (1 / (S : ℚ)) * (∑ y, P x y * vec Wp F.A y - ∑ y, P x y * vec Wm F.A y) := by
      rw [← sum_sub_distrib, mul_sum]; exact sum_congr rfl fun y _ => by ring
    rw [this, e1, e2]; field_simp
  -- the per-row facts
  have hrow : ∀ x : Fin (2 ^ F.A), (x : ℕ) ≠ 0 →
      |N x - p * d x - (lam' * w x - (P *ᵥ w) x)| ≤ eps * d x ∧ |w x| ≤ om * d x := by
    intro x hx
    have := allRows_spec _ _ hr x x.isLt
    simp only [poisRow, Bool.or_eq_true, beq_iff_eq, hx, false_or, Bool.and_eq_true,
      decide_eq_true_eq] at this
    have hd : d x = ((∏ i ∈ range F.A, (c.fac x i).1 : ℕ) : ℚ) / (c.Dt F.A : ℚ) := c.death_eq F htab x
    have hN : N x = (NK.get F.A x : ℚ) / (c.Dt F.A : ℚ) ^ K := by
      rw [hrep x]; field_simp
    rw [hd, hN, hPw x]
    exact this
  -- sums against μ
  have hμ := hq.nonneg
  have hpair := qsd_pair F _ _ μ lam hq w hw0'
  have hdeath : ∑ x, μ x * (d x : ℝ) = 1 - lam := qsd_death F _ _ μ lam hq
  have hres : |∑ x, μ x * ((N x - p * d x - (lam' * w x - (P *ᵥ w) x) : ℚ) : ℝ)| ≤ eps * (1 - lam) := by
    rw [← hdeath, mul_sum]
    refine (abs_sum_le_sum_abs _ _).trans (sum_le_sum fun x _ => ?_)
    by_cases hx : (x : ℕ) = 0
    · simp [hq.empty x hx]
    · rw [abs_mul, abs_of_nonneg (hμ x)]
      have := (hrow x hx).1
      have : |((N x - p * d x - (lam' * w x - (P *ᵥ w) x) : ℚ) : ℝ)| ≤ (eps : ℝ) * d x := by
        rw [← Rat.cast_abs]; exact_mod_cast this
      calc μ x * |((N x - p * d x - (lam' * w x - (P *ᵥ w) x) : ℚ) : ℝ)| ≤ μ x * ((eps : ℝ) * d x) :=
            mul_le_mul_of_nonneg_left this (hμ x)
        _ = (eps : ℝ) * (μ x * d x) := by ring
  have hwb : |∑ x, μ x * (w x : ℝ)| ≤ om * (1 - lam) := by
    rw [← hdeath, mul_sum]
    refine (abs_sum_le_sum_abs _ _).trans (sum_le_sum fun x _ => ?_)
    by_cases hx : (x : ℕ) = 0
    · simp [hq.empty x hx]
    · rw [abs_mul, abs_of_nonneg (hμ x)]
      have := (hrow x hx).2
      have : |(w x : ℝ)| ≤ (om : ℝ) * d x := by rw [← Rat.cast_abs]; exact_mod_cast this
      calc μ x * |(w x : ℝ)| ≤ μ x * ((om : ℝ) * d x) := mul_le_mul_of_nonneg_left this (hμ x)
        _ = (om : ℝ) * (μ x * d x) := by ring
  have hsplit : ∑ x, μ x * ((N x - p * d x - (lam' * w x - (P *ᵥ w) x) : ℚ) : ℝ) =
      (∑ x, μ x * (N x : ℝ)) - p * (1 - lam) - ((lam' : ℝ) - lam) * ∑ x, μ x * (w x : ℝ) := by
    have : ∀ x, μ x * ((N x - p * d x - (lam' * w x - (P *ᵥ w) x) : ℚ) : ℝ) =
        μ x * (N x : ℝ) - p * (μ x * (d x : ℝ)) - lam' * (μ x * (w x : ℝ)) + μ x * ((P *ᵥ w) x : ℝ) := by
      intro x; push_cast; ring
    have hpair' : ∑ x, μ x * ((P *ᵥ w) x : ℝ) = lam * ∑ y, μ y * (w y : ℝ) := hpair
    simp only [this, sum_add_distrib, sum_sub_distrib, ← mul_sum, hdeath]
    rw [hpair']
    ring
  rw [hsplit] at hres
  have habs : |((lam' : ℝ) - lam) * ∑ x, μ x * (w x : ℝ)| ≤ |(lam' : ℝ) - lam| * (om * (1 - lam)) := by
    rw [abs_mul]; exact mul_le_mul_of_nonneg_left hwb (abs_nonneg _)
  have := abs_add_le ((∑ x, μ x * (N x : ℝ)) - p * (1 - lam) - ((lam' : ℝ) - lam) * ∑ x, μ x * (w x : ℝ))
    (((lam' : ℝ) - lam) * ∑ x, μ x * (w x : ℝ))
  rw [sub_add_cancel] at this
  calc |∑ x, μ x * (N x : ℝ) - p * (1 - lam)| ≤ eps * (1 - lam) + |(lam' : ℝ) - lam| * (om * (1 - lam)) := by
        linarith
    _ = ((eps : ℝ) + |(lam' : ℝ) - lam| * om) * (1 - lam) := by ring

end Data

/-- From |X - p (1 - λ)| ≤ η (1 - λ) and a ≤ λ ≤ b: the bust share 1 - X/(λ^(K-1)(1 - λ)) lies between
1 - (p + η)/a^(K-1) and 1 - (p - η)/b^(K-1). -/
theorem share_interval (X lam p η a b : ℝ) (K : ℕ) (ha0 : 0 < a) (ha : a ≤ lam) (hb : lam ≤ b) (hl1 : lam < 1)
    (hpη : 0 < p - η) (h : |X - p * (1 - lam)| ≤ η * (1 - lam)) :
    1 - (p + η) / a ^ (K - 1) ≤ 1 - X / (lam ^ (K - 1) * (1 - lam)) ∧
      1 - X / (lam ^ (K - 1) * (1 - lam)) ≤ 1 - (p - η) / b ^ (K - 1) := by
  have h1l : 0 < 1 - lam := by linarith
  have hlam : 0 < lam := lt_of_lt_of_le ha0 ha
  have hpow : 0 < lam ^ (K - 1) := pow_pos hlam _
  have hapow : 0 < a ^ (K - 1) := pow_pos ha0 _
  have hap : a ^ (K - 1) ≤ lam ^ (K - 1) := pow_le_pow_left₀ ha0.le ha _
  have hbp : lam ^ (K - 1) ≤ b ^ (K - 1) := pow_le_pow_left₀ hlam.le hb _
  obtain ⟨hlo, hhi⟩ := abs_le.mp h
  set q := X / (1 - lam)
  have hq1 : p - η ≤ q := by rw [le_div_iff₀ h1l]; nlinarith
  have hq2 : q ≤ p + η := by rw [div_le_iff₀ h1l]; nlinarith
  have e : X / (lam ^ (K - 1) * (1 - lam)) = q / lam ^ (K - 1) := by
    simp only [q]; rw [div_div, mul_comm]
  rw [e]
  constructor
  · have : q / lam ^ (K - 1) ≤ (p + η) / a ^ (K - 1) :=
      (div_le_div_of_nonneg_right hq2 hpow.le).trans
        (div_le_div_of_nonneg_left (by linarith) hapow hap)
    linarith
  · have : (p - η) / b ^ (K - 1) ≤ q / lam ^ (K - 1) :=
      (div_le_div_of_nonneg_left hpη.le hpow hbp).trans (div_le_div_of_nonneg_right hq1 hpow.le)
    linarith

end Gump.Dice
