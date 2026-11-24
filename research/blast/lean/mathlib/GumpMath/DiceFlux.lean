/-
The bust share is the share of the death flux through a bust (added 2026-11-24, second task).

`DiceExit.lean` defines `bustShare K μ λ = 1 - μ·noBust K / (λ^(K-1)(1 - λ))` and argued in prose that it is the
share of the quasi-stationary death flux whose last K transitions contain a fall of at least half the face. Here
that is a theorem about paths. A path of n generations from x is a list x = X₀, X₁, …, Xₙ of states; its weight
is the product of its transition probabilities (`pathWeight`); `pathE n f x` sums f over all such paths with their
weights (E_x[f(X₀, …, Xₙ)]). Events on a path:
* `dies l`: the last state is the empty face and no earlier one is (the face dies exactly at generation n);
* `bustLast K l`: among the last K transitions (the death included) there is a fall of at least half the face,
  pop u ≥ pop v + half (`qsd.c`: m − n' ≥ half, half = (A+1)/2).
`flux_share`: for every quasi-stationary law (μ, λ) with 0 < λ < 1, every K ≥ 1 and every m, the deaths from μ at
generation m + K split as
    P_μ(T = m+K, bust in the last K) / P_μ(T = m+K) = bustShare K μ λ,
with P_μ(T = m+K) = λ^(m+K-1) (1 - λ) (`death_flux`): the same share in every generation, which is the share of
the whole death flux. So `hull3_bust` and `torus113_bust` are statements about the exits (`hull3_bust_flux`,
`torus113_bust_flux`).
-/
import GumpMath.DiceTorus113Exit
import GumpMath.DiceHull3Exit

namespace Gump.Dice
open Gump Finset Matrix

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

/-- The weight of a path: the product of its transition probabilities. -/
def pathWeight : List (Fin (2 ^ F.A)) → ℚ
  | a :: b :: l => F.P ρ1 ρ2 a b * pathWeight (b :: l)
  | _ => 1

/-- E_x[f(X₀, …, Xₙ)]: f summed over every path of n generations from x, with its weight. -/
def pathE (n : ℕ) (f : List (Fin (2 ^ F.A)) → ℚ) (x : Fin (2 ^ F.A)) : ℚ :=
  ∑ ω : Fin n → Fin (2 ^ F.A), F.pathWeight ρ1 ρ2 (x :: List.ofFn ω) * f (x :: List.ofFn ω)

/-- The face dies exactly at the end of the path: the last state is empty, no earlier one is. -/
def dies : List (Fin (2 ^ F.A)) → Bool
  | [a] => (a : ℕ) == 0
  | a :: b :: l => (a : ℕ) != 0 && dies (b :: l)
  | [] => false

theorem dies_cons (x y : Fin (2 ^ F.A)) (l : List (Fin (2 ^ F.A))) :
    F.dies (x :: y :: l) = ((x : ℕ) != 0 && F.dies (y :: l)) := rfl

/-- A fall of at least half the face from u to v. -/
def fall (u v : Fin (2 ^ F.A)) : Bool := decide (F.pop v + F.half ≤ F.pop u)

/-- No transition of the path is a fall of at least half the face. -/
def noFallAll : List (Fin (2 ^ F.A)) → Bool
  | a :: b :: l => !F.fall a b && noFallAll (b :: l)
  | _ => true

/-- **The bust**: among the last K transitions of the path (its last K + 1 states) there is a fall of at least
half the face. -/
def bustLast (K : ℕ) (l : List (Fin (2 ^ F.A))) : Bool := !F.noFallAll (l.drop (l.length - 1 - K))

theorem pathE_zero (f : List (Fin (2 ^ F.A)) → ℚ) (x : Fin (2 ^ F.A)) : F.pathE ρ1 ρ2 0 f x = f [x] := by
  simp [pathE, pathWeight]

/-- The Markov property, one step: E_x[f] = Σ_y P(x, y) E_y[f(x, ·)]. -/
theorem pathE_succ (n : ℕ) (f : List (Fin (2 ^ F.A)) → ℚ) (x : Fin (2 ^ F.A)) :
    F.pathE ρ1 ρ2 (n + 1) f x = ∑ y, F.P ρ1 ρ2 x y * F.pathE ρ1 ρ2 n (fun l => f (x :: l)) y := by
  unfold pathE
  rw [← (Fin.consEquiv fun _ => Fin (2 ^ F.A)).sum_comp, Fintype.sum_prod_type]
  refine sum_congr rfl fun y _ => ?_
  rw [mul_sum]
  refine sum_congr rfl fun ω _ => ?_
  simp only [Fin.consEquiv, Equiv.coe_fn_mk, List.ofFn_succ, Fin.cons_zero, Fin.cons_succ, pathWeight]
  ring

/-- E_y[f] depends only on the values of f on the paths from y. -/
theorem pathE_congr (n : ℕ) (f g : List (Fin (2 ^ F.A)) → ℚ) (y : Fin (2 ^ F.A))
    (h : ∀ ω : Fin n → Fin (2 ^ F.A), f (y :: List.ofFn ω) = g (y :: List.ofFn ω)) :
    F.pathE ρ1 ρ2 n f y = F.pathE ρ1 ρ2 n g y := by
  unfold pathE; exact sum_congr rfl fun ω _ => by rw [h ω]

theorem ind_and (a b : Bool) : (if (a && b) = true then (1 : ℚ) else 0) = (if a then 1 else 0) * (if b then 1 else 0) := by
  cases a <;> cases b <;> simp

/-- P_x(T = K, no fall ≥ half in the K transitions) is `noBust K x`. -/
theorem pathE_noBust : ∀ (K : ℕ) (x : Fin (2 ^ F.A)),
    F.pathE ρ1 ρ2 K (fun l => if (F.dies l && F.noFallAll l) = true then 1 else 0) x = F.noBust ρ1 ρ2 K x
  | 0, x => by
      rw [pathE_zero]; simp [dies, noFallAll, noBust]
  | K + 1, x => by
      rw [pathE_succ, noBust]
      by_cases hx : (x : ℕ) = 0
      · rw [if_pos hx]
        refine sum_eq_zero fun y _ => ?_
        rw [F.pathE_congr ρ1 ρ2 K _ (fun _ => 0) y (fun ω => by simp [dies, hx])]
        simp [pathE]
      · rw [if_neg hx]
        refine sum_congr rfl fun y _ => ?_
        congr 1
        rw [F.pathE_congr ρ1 ρ2 K _ (fun l => (if F.pop x < F.pop y + F.half then 1 else 0) *
          (if (F.dies l && F.noFallAll l) = true then 1 else 0)) y (fun ω => ?_)]
        · rw [show F.pathE ρ1 ρ2 K (fun l => (if F.pop x < F.pop y + F.half then 1 else 0) *
            (if (F.dies l && F.noFallAll l) = true then 1 else 0)) y =
            (if F.pop x < F.pop y + F.half then 1 else 0) *
              F.pathE ρ1 ρ2 K (fun l => if (F.dies l && F.noFallAll l) = true then 1 else 0) y by
            unfold pathE; rw [mul_sum]; exact sum_congr rfl fun _ _ => by ring]
          rw [pathE_noBust K y]
          split <;> simp
        · show (if (F.dies (x :: y :: List.ofFn ω) && F.noFallAll (x :: y :: List.ofFn ω)) = true then (1 : ℚ) else 0) = _
          rw [dies_cons, show F.noFallAll (x :: y :: List.ofFn ω) = (!F.fall x y && F.noFallAll (y :: List.ofFn ω)) from rfl]
          have hxb : ((x : ℕ) != 0) = true := by simp [hx]
          rw [hxb, Bool.true_and]
          unfold fall
          generalize F.dies (y :: List.ofFn ω) = a
          generalize F.noFallAll (y :: List.ofFn ω) = b
          by_cases hc : F.pop x < F.pop y + F.half
          · have : decide (F.pop y + F.half ≤ F.pop x) = false := by simp; omega
            rw [this]; cases a <;> cases b <;> simp [hc]
          · have : decide (F.pop y + F.half ≤ F.pop x) = true := by simp; omega
            rw [this]; cases a <;> cases b <;> simp [hc]

/-- The window recursion: before the last K transitions the path only has to stay alive. -/
def Nm (K : ℕ) : ℕ → Fin (2 ^ F.A) → ℚ
  | 0, x => F.noBust ρ1 ρ2 K x
  | m + 1, x => if (x : ℕ) = 0 then 0 else ∑ y, F.P ρ1 ρ2 x y * Nm K m y

theorem bustLast_cons (K : ℕ) (x : Fin (2 ^ F.A)) (l : List (Fin (2 ^ F.A))) (hl : K + 1 ≤ l.length) :
    F.bustLast K (x :: l) = F.bustLast K l := by
  unfold bustLast
  have : (x :: l).length - 1 - K = (l.length - 1 - K) + 1 := by simp; omega
  rw [this, List.drop_succ_cons]

theorem bustLast_exact (K : ℕ) (l : List (Fin (2 ^ F.A))) (hl : l.length = K + 1) :
    F.bustLast K l = !F.noFallAll l := by
  unfold bustLast; rw [hl, show K + 1 - 1 - K = 0 by omega, List.drop_zero]

/-- P_x(T = m + K, no fall ≥ half in the last K transitions) = Nm m x. -/
theorem pathE_window (K : ℕ) : ∀ (m : ℕ) (x : Fin (2 ^ F.A)),
    F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && !F.bustLast K l) = true then 1 else 0) x = F.Nm ρ1 ρ2 K m x
  | 0, x => by
      rw [Nm, ← pathE_noBust, zero_add]
      refine F.pathE_congr ρ1 ρ2 K _ _ x fun ω => ?_
      rw [F.bustLast_exact K _ (by simp), Bool.not_not]
  | m + 1, x => by
      rw [show m + 1 + K = (m + K) + 1 by omega, pathE_succ,
        show F.Nm ρ1 ρ2 K (m + 1) x = (if (x : ℕ) = 0 then 0 else ∑ y, F.P ρ1 ρ2 x y * F.Nm ρ1 ρ2 K m y) from rfl]
      by_cases hx : (x : ℕ) = 0
      · rw [if_pos hx]
        refine sum_eq_zero fun y _ => ?_
        rw [F.pathE_congr ρ1 ρ2 (m + K) _ (fun _ => 0) y (fun ω => by simp [dies_cons, hx])]
        simp [pathE]
      · rw [if_neg hx]
        refine sum_congr rfl fun y _ => ?_
        congr 1
        refine (F.pathE_congr ρ1 ρ2 (m + K) _ _ y fun ω => ?_).trans (pathE_window K m y)
        rw [dies_cons, F.bustLast_cons K x _ (by simp)]
        have hxb : ((x : ℕ) != 0) = true := by simp [hx]
        rw [hxb, Bool.true_and]

/-- P_x(T = n + 1) by the same recursion. -/
def Dm : ℕ → Fin (2 ^ F.A) → ℚ
  | 0, x => if (x : ℕ) = 0 then 0 else F.P ρ1 ρ2 x F.empty
  | m + 1, x => if (x : ℕ) = 0 then 0 else ∑ y, F.P ρ1 ρ2 x y * Dm m y

theorem pathE_dies : ∀ (m : ℕ) (x : Fin (2 ^ F.A)),
    F.pathE ρ1 ρ2 (m + 1) (fun l => if F.dies l = true then 1 else 0) x = F.Dm ρ1 ρ2 m x
  | 0, x => by
      rw [pathE_succ, show F.Dm ρ1 ρ2 0 x = (if (x : ℕ) = 0 then 0 else F.P ρ1 ρ2 x F.empty) from rfl]
      have hy : ∀ y : Fin (2 ^ F.A), F.pathE ρ1 ρ2 0 (fun l => if F.dies (x :: l) = true then 1 else 0) y =
          if (x : ℕ) = 0 then 0 else (if y = F.empty then 1 else 0) := by
        intro y
        rw [pathE_zero]
        have e : (y = F.empty) ↔ (y : ℕ) = 0 := ⟨fun h => by rw [h]; rfl, fun h => Fin.ext h⟩
        by_cases hx : (x : ℕ) = 0 <;> by_cases hy0 : (y : ℕ) = 0 <;> simp [dies, hx, hy0, e]
      simp_rw [hy]
      by_cases hx : (x : ℕ) = 0
      · simp [hx]
      · simp [hx]
  | m + 1, x => by
      rw [pathE_succ,
        show F.Dm ρ1 ρ2 (m + 1) x = (if (x : ℕ) = 0 then 0 else ∑ y, F.P ρ1 ρ2 x y * F.Dm ρ1 ρ2 m y) from rfl]
      by_cases hx : (x : ℕ) = 0
      · rw [if_pos hx]
        refine sum_eq_zero fun y _ => ?_
        rw [F.pathE_congr ρ1 ρ2 (m + 1) _ (fun _ => 0) y (fun ω => by simp [List.ofFn_succ, dies_cons, hx])]
        simp [pathE]
      · rw [if_neg hx]
        refine sum_congr rfl fun y _ => ?_
        congr 1
        refine (F.pathE_congr ρ1 ρ2 (m + 1) _ _ y fun ω => ?_).trans (pathE_dies m y)
        rw [List.ofFn_succ, dies_cons]
        have hxb : ((x : ℕ) != 0) = true := by simp [hx]
        rw [hxb, Bool.true_and]

end Face

/-- From a quasi-stationary law, one more generation of a recursion of the form [x ≠ ∅] Σ_y P(x,y) v(y) multiplies
μ·v by λ (v(∅) = 0). -/
theorem qsd_step (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam)
    (v : Fin (2 ^ F.A) → ℚ) (hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → v y = 0) :
    ∑ x, μ x * ((if (x : ℕ) = 0 then 0 else ∑ y, F.P ρ1 ρ2 x y * v y : ℚ) : ℝ) = lam * ∑ y, μ y * (v y : ℝ) := by
  rw [← Data.qsd_pair F ρ1 ρ2 μ lam hq v hv0]
  refine sum_congr rfl fun x _ => ?_
  by_cases hx : (x : ℕ) = 0
  · simp [hx, hq.empty x hx]
  · simp only [hx, if_false]; rfl

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

theorem Nm_zero_at (K : ℕ) (hK : 1 ≤ K) : ∀ (m : ℕ) (y : Fin (2 ^ F.A)), (y : ℕ) = 0 → F.Nm ρ1 ρ2 K m y = 0
  | 0, y, hy => by
      obtain ⟨k, rfl⟩ : ∃ k, K = k + 1 := ⟨K - 1, by omega⟩
      simp [Nm, noBust, hy]
  | m + 1, y, hy => by simp [Nm, hy]

theorem Dm_zero_at : ∀ (m : ℕ) (y : Fin (2 ^ F.A)), (y : ℕ) = 0 → F.Dm ρ1 ρ2 m y = 0
  | 0, y, hy => by simp [Dm, hy]
  | m + 1, y, hy => by simp [Dm, hy]

end Face

theorem mu_Nm (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (K : ℕ)
    (hK : 1 ≤ K) : ∀ m, ∑ x, μ x * (F.Nm ρ1 ρ2 K m x : ℝ) = lam ^ m * ∑ x, μ x * (F.noBust ρ1 ρ2 K x : ℝ)
  | 0 => by simp [Face.Nm]
  | m + 1 => by
      have := qsd_step F ρ1 ρ2 μ lam hq (F.Nm ρ1 ρ2 K m) (F.Nm_zero_at ρ1 ρ2 K hK m)
      simp only [Face.Nm] at this ⊢
      rw [this, mu_Nm F ρ1 ρ2 μ lam hq K hK m, pow_succ]; ring

theorem mu_Dm (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) :
    ∀ m, ∑ x, μ x * (F.Dm ρ1 ρ2 m x : ℝ) = lam ^ m * (1 - lam)
  | 0 => by
      rw [← Data.qsd_death F ρ1 ρ2 μ lam hq, pow_zero, one_mul]
      refine sum_congr rfl fun x _ => ?_
      by_cases hx : (x : ℕ) = 0
      · simp [Face.Dm, hx, hq.empty x hx]
      · simp [Face.Dm, hx]
  | m + 1 => by
      have := qsd_step F ρ1 ρ2 μ lam hq (F.Dm ρ1 ρ2 m) (F.Dm_zero_at ρ1 ρ2 m)
      simp only [Face.Dm] at this ⊢
      rw [this, mu_Dm F ρ1 ρ2 μ lam hq m, pow_succ]; ring

/-- **The death flux from a quasi-stationary law**: P_μ(T = n + 1) = λ^n (1 - λ). -/
theorem death_flux (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (n : ℕ) :
    ∑ x, μ x * (F.pathE ρ1 ρ2 (n + 1) (fun l => if F.dies l = true then 1 else 0) x : ℝ) = lam ^ n * (1 - lam) := by
  simp only [Face.pathE_dies]; exact mu_Dm F ρ1 ρ2 μ lam hq n

/-- **The bust share is the share of the death flux through a bust**, in every generation: for every
quasi-stationary law (μ, λ) with 0 < λ < 1, K ≥ 1 and m ≥ 0, among the deaths from μ at generation m + K, the
share whose last K transitions contain a fall of at least half the face is `bustShare K μ λ`. -/
theorem flux_share (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam)
    (h0 : 0 < lam) (h1 : lam < 1) (K : ℕ) (hK : 1 ≤ K) (m : ℕ) :
    (∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && F.bustLast K l) = true then 1 else 0) x : ℝ)) /
      (∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if F.dies l = true then 1 else 0) x : ℝ)) =
    F.bustShare ρ1 ρ2 K μ lam := by
  -- bust = dies - (dies and no bust)
  have split : ∀ x, F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && F.bustLast K l) = true then 1 else 0) x =
      F.pathE ρ1 ρ2 (m + K) (fun l => if F.dies l = true then 1 else 0) x -
        F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && !F.bustLast K l) = true then 1 else 0) x := by
    intro x; unfold Face.pathE; rw [← sum_sub_distrib]
    refine sum_congr rfl fun ω _ => ?_
    rw [← mul_sub]; congr 1
    have key : ∀ a b : Bool, (if (a && b) = true then (1 : ℚ) else 0) =
        (if a = true then 1 else 0) - (if (a && !b) = true then 1 else 0) := by
      intro a b; cases a <;> cases b <;> norm_num
    exact key _ _
  have hD : ∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if F.dies l = true then 1 else 0) x : ℝ) =
      lam ^ (m + K - 1) * (1 - lam) := by
    rw [show m + K = (m + K - 1) + 1 by omega]; rw [death_flux F ρ1 ρ2 μ lam hq]; congr 2
  have hW : ∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && !F.bustLast K l) = true then 1 else 0) x : ℝ) =
      lam ^ m * ∑ x, μ x * (F.noBust ρ1 ρ2 K x : ℝ) := by
    simp only [Face.pathE_window]; exact mu_Nm F ρ1 ρ2 μ lam hq K hK m
  simp only [split, Rat.cast_sub, mul_sub, sum_sub_distrib]
  rw [hD, hW, Face.bustShare]
  have hl : lam ^ m ≠ 0 := pow_ne_zero _ h0.ne'
  have hD' : lam ^ (m + K - 1) * (1 - lam) ≠ 0 := mul_ne_zero (pow_ne_zero _ h0.ne') (by linarith)
  have e : lam ^ (m + K - 1) = lam ^ m * lam ^ (K - 1) := by rw [← pow_add]; congr 1; omega
  rw [e] at hD' ⊢
  field_simp

open Hull3Data in
/-- **The rimmed face dies by the fade**: among the deaths of the 9-cell hull triangle from any quasi-stationary
law, in every generation m + 6, the share whose last 6 transitions contain a fall of at least 5 cells is in
(0.017017, 0.017018). -/
theorem hull3_bust_flux (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) (m : ℕ) :
    0.017017 < (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6)
        (fun l => if ((hull 3).dies l && (hull 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) /
      (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if (hull 3).dies l = true then 1 else 0) x : ℝ)) ∧
    (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6)
        (fun l => if ((hull 3).dies l && (hull 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) /
      (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if (hull 3).dies l = true then 1 else 0) x : ℝ)) <
      0.017018 := by
  obtain ⟨l1, l2, -, -⟩ := hull3_tau μ lam hq
  rw [flux_share (hull 3) ρ1 ρ2 μ lam hq (by linarith) (by linarith) 6 (by norm_num) m]
  exact hull3_bust μ lam hq

open Torus113Data in
/-- **The wrapped face dies by the bust**: for the 9-cell torus (1,1),(0,3), the same share is in
(0.936852, 0.936853), for every quasi-stationary law with λ > 0 and every generation m + 6. -/
theorem torus113_bust_flux (μ : Fin (2 ^ (torus 1 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 1 3) ρ1 ρ2 μ lam)
    (hlam : 0 < lam) (m : ℕ) :
    0.936852 < (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6)
        (fun l => if ((torus 1 1 3).dies l && (torus 1 1 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) /
      (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if (torus 1 1 3).dies l = true then 1 else 0) x : ℝ)) ∧
    (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6)
        (fun l => if ((torus 1 1 3).dies l && (torus 1 1 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) /
      (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if (torus 1 1 3).dies l = true then 1 else 0) x : ℝ)) <
      0.936853 := by
  obtain ⟨l1, l2, -, -⟩ := torus113_tau μ lam hq hlam
  rw [flux_share (torus 1 1 3) ρ1 ρ2 μ lam hq hlam (by linarith) 6 (by norm_num) m]
  exact torus113_bust μ lam hq hlam

end Gump.Dice
