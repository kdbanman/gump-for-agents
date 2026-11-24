/-
A sharper Theorem 1 on every wrapped face (repair D7 of `research/blast/ref-chain/REVIEW.md`, formalising the
referee's paper proof): log τ ≤ (2 ε_max + ε₂)/3 · A ≤ 2.2412 · A at (ρ1, ρ2) = (0.44, 0.42).

The argument (agent `ref-chain`): only a live cell with exactly three live neighbours has cost ε_max = -log ρ1²ρ2;
every other (state, k) dies with probability at least (1-ρ1)²(1-ρ2), cost at most ε₂.  Each such ε_max-cell has
three neighbour slots pointing at dead cells, and every cell is the target of exactly six slots (`indeg`), so
3|S| ≤ 6 · #dead ≤ 6(A - |S|): at most 2A/3 cells pay ε_max, and E(x) ≤ (2ε_max + ε₂)/3 · A for every state.
  `indeg`            Σ_c (number of times d is a neighbour of c) = 6, for every cell d;
  `card_S_le`        3 · #{live cells with k = 3} ≤ 2 · A;
  `energy_le_sharp`  E(x) ≤ (2 ε_max + ε₂)/3 · A, with ε_max = -log(ρ1²ρ2), ε₂ = -log((1-ρ1)²(1-ρ2));
  `kagome_sharp_bound` log τ ≤ 2.2412 · A for every quasi-stationary law at (0.44, 0.42).
(The dice agent's `Gump.Dice.lntau_le_regular`, a different weighted argument on its own faces, gives
ln τ < 1.9228 · A on faces it proves regular; that theorem is about `Gump.Dice.Face`, not this model.)
-/
import Mathlib
import GumpMath.ChainKagome

set_option linter.unusedSectionVars false

namespace Gump.Chain.Kagome
open Finset Real

variable {T : Type*} [AddCommGroup T] [Fintype T] [DecidableEq T] (e1 e2 : T)

theorem sum_count_snd (l : List (Cell T)) (o' : Orient) :
    ∑ q : T, l.count (o', q) = l.countP (fun e => decide (e.1 = o')) := by
  induction l with
  | nil => simp
  | cons e l ih =>
    simp only [List.count_cons, List.countP_cons, Finset.sum_add_distrib, ih]
    congr 1
    rcases e with ⟨o, r⟩
    by_cases h : o = o'
    · subst h; simp
    · simp [h]

/-- **Every cell is the neighbour of exactly six slots** (in-degree six, multiplicities included). -/
theorem indeg (d : Cell T) : ∑ c, (nbrs e1 e2 c).count d = 6 := by
  rw [Fintype.sum_prod_type]
  have h : ∀ o, ∑ p : T, (nbrs e1 e2 (o, p)).count d = 2 := by
    intro o
    have hp : ∀ p : T, (nbrs e1 e2 (o, p)).count d = (nbrs e1 e2 (o, 0)).count (d.1, d.2 - p) := by
      intro p
      have h1 := nbrs_tr e1 e2 p (o, 0)
      rw [tr_apply] at h1
      simp only [zero_add] at h1
      rw [h1]
      have hd : d = tr p (d.1, d.2 - p) := by simp [tr_apply]
      conv_lhs => rw [hd]
      exact List.count_map_of_injective _ _ (tr p).injective _
    simp_rw [hp]
    rw [Fintype.sum_equiv (Equiv.subLeft d.2) (fun p => (nbrs e1 e2 (o, 0)).count (d.1, d.2 - p))
      (fun q => (nbrs e1 e2 (o, 0)).count (d.1, q)) (fun p => rfl)]
    rw [sum_count_snd, count_orient]
  simp only [h, Finset.sum_const, Finset.card_univ, card_orient, smul_eq_mul]

theorem countP_eq_sum_count' (l : List (Cell T)) (s : Finset (Cell T)) :
    l.countP (fun d => decide (d ∈ s)) = ∑ d ∈ s, l.count d := by
  induction l with
  | nil => simp
  | cons e l ih =>
    rw [List.countP_cons, ih]
    simp only [List.count_cons, Finset.sum_add_distrib]
    congr 1
    by_cases he : e ∈ s
    · simp [he, beq_iff_eq]
    · simp only [he, decide_false]
      symm
      exact Finset.sum_eq_zero (fun d hd => by
        have : e ≠ d := fun h => he (h ▸ hd)
        simp [beq_iff_eq, this])

/-- The slots pointing at dead cells, summed over all cells: six per dead cell. -/
theorem sum_dead_slots (x : Finset (Cell T)) :
    ∑ c, (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) = 6 * (xᶜ).card := by
  simp_rw [countP_eq_sum_count']
  rw [Finset.sum_comm]
  simp_rw [indeg]
  simp [mul_comm]

/-- **At most two thirds of the cells are live with three live neighbours**: 3·|S| ≤ 2·A. -/
theorem card_S_le (x : Finset (Cell T)) :
    3 * (x.filter (fun c => k e1 e2 x c = 3)).card ≤ 2 * Fintype.card (Cell T) := by
  set S := x.filter (fun c => k e1 e2 x c = 3) with hS
  have hdead : ∀ c ∈ S, (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) = 3 := by
    intro c hc
    have hk := (mem_filter.1 hc).2
    have hlen := List.length_eq_countP_add_countP (fun d => decide (d ∈ x)) (l := nbrs e1 e2 c)
    rw [length_nbrs] at hlen
    have : (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) =
        (nbrs e1 e2 c).countP (fun a => decide ¬decide (a ∈ x) = true) :=
      List.countP_congr (fun d _ => by simp)
    unfold k at hk
    omega
  have h1 : 3 * S.card = ∑ c ∈ S, (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) := by
    rw [Finset.sum_congr rfl hdead]; simp [mul_comm]
  have h2 : ∑ c ∈ S, (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) ≤
      ∑ c, (nbrs e1 e2 c).countP (fun d => decide (d ∈ xᶜ)) :=
    Finset.sum_le_sum_of_subset_of_nonneg (subset_univ _) (fun _ _ _ => Nat.zero_le _)
  have h3 := sum_dead_slots e1 e2 x
  have hSx : S ⊆ x := filter_subset _ _
  have h4 : S.card ≤ x.card := card_le_card hSx
  have h5 : (xᶜ).card = Fintype.card (Cell T) - x.card := card_compl x
  have h6 : x.card ≤ Fintype.card (Cell T) := card_le_univ x
  omega

/-! ### The one-cell costs at (0.44, 0.42) -/

theorem death3_alive3 : death3 0.44 0.42 true 3 = 0.44 ^ 2 * 0.42 := by
  simp [death3, aliveNext, coin3, Finset.sum_range_succ]

theorem death3_ge_second (s : Bool) (kk : ℕ) (hk : kk ≤ 6) (hne : ¬ (s = true ∧ kk = 3)) :
    (1 - 0.44) ^ 2 * (1 - 0.42) ≤ death3 0.44 0.42 s kk := by
  interval_cases kk <;> cases s <;> simp_all [death3, aliveNext, coin3, Finset.sum_range_succ] <;> norm_num

theorem e1_le : -log (0.44 ^ 2 * 0.42 : ℝ) ≤ 2.5095 := by
  rw [neg_le, le_log_iff_exp_le (by norm_num)]
  have hs := sum_le_exp_of_nonneg (x := (2.5095 : ℝ)) (by norm_num) 18
  have h : 1 ≤ (0.44 ^ 2 * 0.42) * ∑ i ∈ range 18, (2.5095 : ℝ) ^ i / (i.factorial) := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    norm_num
  rw [exp_neg, inv_le_iff_one_le_mul₀ (exp_pos _)]
  nlinarith [exp_pos (2.5095 : ℝ)]

theorem e2_le : -log ((1 - 0.44) ^ 2 * (1 - 0.42) : ℝ) ≤ 1.7045 := by
  rw [neg_le, le_log_iff_exp_le (by norm_num)]
  have hs := sum_le_exp_of_nonneg (x := (1.7045 : ℝ)) (by norm_num) 14
  have h : 1 ≤ ((1 - 0.44) ^ 2 * (1 - 0.42)) * ∑ i ∈ range 14, (1.7045 : ℝ) ^ i / (i.factorial) := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    norm_num
  rw [exp_neg, inv_le_iff_one_le_mul₀ (exp_pos _)]
  nlinarith [exp_pos (1.7045 : ℝ)]

section Sharp
variable (h1 : (0:ℝ) < 0.44) (h1' : (0.44:ℝ) < 1) (h2 : (0:ℝ) < 0.42) (h2' : (0.42:ℝ) < 1)

/-- **E(x) ≤ (2ε_max + ε₂)/3 · A for every state** of the surrogate on the kagome layer at (0.44, 0.42). -/
theorem energy_le_sharp (x : Living (Cell T)) :
    (kernel e1 e2 0.44 0.42 h1 h1' h2 h2').localDeath.energy x ≤
      (2 * -log (0.44 ^ 2 * 0.42 : ℝ) + -log ((1 - 0.44) ^ 2 * (1 - 0.42) : ℝ)) / 3 *
        Fintype.card (Cell T) := by
  set G := kernel e1 e2 0.44 0.42 h1 h1' h2 h2'
  set S := x.1.filter (fun c => k e1 e2 x.1 c = 3)
  set ea := -log (0.44 ^ 2 * 0.42 : ℝ)
  set eb := -log ((1 - 0.44) ^ 2 * (1 - 0.42) : ℝ)
  have hcost : ∀ c, G.localDeath.cost c x = -log (death3 0.44 0.42 (decide (c ∈ x.1)) (k e1 e2 x.1 c)) :=
    fun c => by
      show -log (1 - (1 - death3 0.44 0.42 (decide (c ∈ x.1)) (k e1 e2 x.1 c))) = _
      rw [sub_sub_cancel]
  have hS : ∀ c ∈ S, G.localDeath.cost c x = ea := fun c hc => by
    have ⟨hcx, hk⟩ := mem_filter.1 hc
    rw [hcost, hk]; simp [hcx, death3_alive3, ea]
  have hnS : ∀ c, c ∉ S → G.localDeath.cost c x ≤ eb := fun c hc => by
    rw [hcost]
    have hne : ¬ (decide (c ∈ x.1) = true ∧ k e1 e2 x.1 c = 3) := by
      rintro ⟨h1, h2⟩; exact hc (mem_filter.2 ⟨by simpa using h1, h2⟩)
    have hd := death3_ge_second _ _ (k_le_six e1 e2 x.1 c) hne
    exact neg_le_neg (log_le_log (by norm_num) hd)
  have hab : eb ≤ ea := neg_le_neg (log_le_log (by norm_num) (by norm_num))
  have hcard := card_S_le e1 e2 x.1
  have hsplit : G.localDeath.energy x = ∑ c ∈ S, G.localDeath.cost c x + ∑ c ∈ Sᶜ, G.localDeath.cost c x :=
    (Finset.sum_add_sum_compl S _).symm
  have hA : (S.card : ℝ) + (Sᶜ.card : ℝ) = Fintype.card (Cell T) := by
    rw [← Nat.cast_add, Finset.card_add_card_compl]
  have hS' : ∑ c ∈ S, G.localDeath.cost c x = S.card * ea := by
    rw [Finset.sum_congr rfl hS]; simp
  have hnS' : ∑ c ∈ Sᶜ, G.localDeath.cost c x ≤ Sᶜ.card * eb := by
    calc ∑ c ∈ Sᶜ, G.localDeath.cost c x ≤ ∑ _c ∈ Sᶜ, eb :=
          Finset.sum_le_sum (fun c hc => hnS c (mem_compl.1 hc))
      _ = Sᶜ.card * eb := by simp
  have hcardR : 3 * (S.card : ℝ) ≤ 2 * Fintype.card (Cell T) := by exact_mod_cast hcard
  have key : 0 ≤ (ea - eb) * (2 * (Sᶜ.card : ℝ) - S.card) :=
    mul_nonneg (by linarith) (by linarith)
  rw [hsplit, hS', ← hA]
  nlinarith [hnS', key]

/-- **The sharper Theorem 1 on every wrapped face**: log τ ≤ 2.2412 · A for every quasi-stationary law of the
surrogate on the kagome layer over T, at (0.44, 0.42), A = 3|T|. -/
theorem kagome_sharp_bound {μ : Living (Cell T) → ℝ} {lam : ℝ}
    (hμ : (kernel e1 e2 0.44 0.42 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam) :
    Real.log ((kernel e1 e2 0.44 0.42 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) ≤
      2.2412 * (3 * Fintype.card T) := by
  set G := kernel e1 e2 0.44 0.42 h1 h1' h2 h2'
  obtain ⟨-, -, -, -, h5, h6⟩ := KilledChain.tilt_identity G.localDeath hμ
  have hlog := h6 ▸ h5
  have hE := energy_le_sharp e1 e2 h1 h1' h2 h2'
  have hnum : (2 * -log (0.44 ^ 2 * 0.42 : ℝ) + -log ((1 - 0.44) ^ 2 * (1 - 0.42) : ℝ)) / 3 ≤ 2.2412 := by
    have := e1_le; have := e2_le; linarith
  have hcard : (Fintype.card (Cell T) : ℝ) = 3 * Fintype.card T := by
    rw [Fintype.card_prod, card_orient]; push_cast; ring
  have hA0 : (0 : ℝ) ≤ Fintype.card (Cell T) := Nat.cast_nonneg _
  calc Real.log (G.toSubsetChain.killed.lifetime μ) ≤ ∑ x, μ x * G.localDeath.energy x := hlog
    _ ≤ ∑ x, μ x * (2.2412 * Fintype.card (Cell T)) := Finset.sum_le_sum (fun x _ =>
        mul_le_mul_of_nonneg_left ((hE x).trans (mul_le_mul_of_nonneg_right hnum hA0)) (hμ.nonneg x))
    _ = 2.2412 * (3 * Fintype.card T) := by rw [← Finset.sum_mul, hμ.total, one_mul, hcard]

end Sharp
end Gump.Chain.Kagome
