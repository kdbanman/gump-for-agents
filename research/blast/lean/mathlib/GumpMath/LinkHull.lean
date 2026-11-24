/-
**Every hull face**, for `Face.P` itself.

1. `cellsOK_hull R` for every R (from the dice agent's `hull_type`), hence `hull_theorems R`: the dominant
   quasi-stationary law, the tilt identity with named per-cell factors, ln τ < 2.2165·A (`lntau_le_hull_all`),
   and `survFrom = Face.survival` (`absorbing_hull`). No hypothesis.
2. Lemma 0, stated combinatorially and density-free as `Lemma0F F` (a state u from which every living state is
   possible next, reached from every state some cell of which can be alive next, through possible transitions),
   gives on every face with `CellsOK` the full lifetime theorem (`face_full_of`): unique law among λ > 0, positive
   on every living state, decay at exactly λ from every state that can survive. `hull_full_all R` is that theorem on
   `hull R` under `Lemma0F (Gump.Dice.hull R)`, the single named hypothesis; `lemma0_of_cert` proves it from a polynomial-size
   certificate (walks between single cells and one growth path), checked by the kernel in `LinkHullCert.lean`.
-/
import GumpMath.LinkSurv
import GumpMath.DiceHullAll

set_option linter.unusedSectionVars false

namespace Gump.Link
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Chain.Bits Finset

/-! ### Every hull face: the cells' coins, and Theorems 1 and 2 -/

/-- **Every hull face has its coins**: (2,1), or (2,0) at the corners, which have two neighbours. -/
theorem cellsOK_hull (R : ℕ) : CellsOK (Gump.Dice.hull R) := by
  intro i hi
  rcases Face.hull_type R i hi with h | h | h <;> simp only [Prod.mk.injEq] at h
  · exact Or.inl ⟨h.2.1, h.2.2⟩
  · exact Or.inl ⟨h.2.1, h.2.2⟩
  · exact Or.inr ⟨h.2.1, h.2.2, h.1.le⟩

/-- The local death factors of `Face.P` on the hull face. -/
noncomputable abbrev LH (R : ℕ) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) := localDeath (Gump.Dice.hull R) hs (cellsOK_hull R)

/-- **Theorems 1 and 2 on every hull face, for `Face.P` itself, at every 0 < ρ1, ρ2 < 1.** -/
theorem hull_theorems_at (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) :
    ∃ μ lam, (chain (Gump.Dice.hull R) hs.dens).IsDominantQSD μ lam ∧ IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧
      (∀ i x, (LH R hs).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (Gump.Dice.hull R) hs.dens).lifetime μ) = ∑ i, (LH R hs).price μ i ∧
      (∀ t x, (chain (Gump.Dice.hull R) hs.dens).survFrom t x = (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ)) := by
  obtain ⟨μ, lam, hD, hdice, hdc, hpr, -, -⟩ := face_theorems (Gump.Dice.hull R) hs (cellsOK_hull R) hA
  exact ⟨μ, lam, hD, hdice, hdc, hpr, survFrom_cast _ _ (absorbing_hull R ρ1 ρ2)⟩

/-- **Theorems 1 and 2 on every hull face at (0.44, 0.42)**, with the dice agent's ln τ < 2.2165·A. -/
theorem hull_theorems (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) :
    ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧
      IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧
      (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧
      (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x =
        (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ)) := by
  obtain ⟨μ, lam, hD, hdice, hdc, hpr, hs⟩ := hull_theorems_at R hA Hull3.sdens
  refine ⟨μ, lam, hD, hdice, hdc, hpr, ?_, hs⟩
  rw [log_lifetime_eq (LH R Hull3.sdens) hD.qsd]
  exact lntau_le_hull_all R _ lam hdice hA

/-! ### Lemma 0, combinatorially -/

section Abstract
variable (F : Face)

/-- Cell i can be alive next from x (some coin outcome puts k + heads in the rule's window). -/
def aliveF (x i : ℕ) : Bool := canB (F.m1 i) (F.m2 i) (F.k x i) (x.testBit i)

/-- x → y is possible: every live cell of y can be alive next from x. -/
def stepF (x y : ℕ) : Bool := (List.range F.A).all fun i => !(y.testBit i) || aliveF F x i

/-- A possible transition between living states. -/
def StepN (x y : ℕ) : Prop := y < 2 ^ F.A ∧ y ≠ 0 ∧ stepF F x y = true

/-- **Lemma 0, the single named hypothesis**: a living state u from which every living state is possible next
(every cell can be alive next), reached by possible transitions from every living state some cell of which can be
alive next. -/
def Lemma0F : Prop :=
  ∃ u, u < 2 ^ F.A ∧ u ≠ 0 ∧ (∀ i < F.A, aliveF F u i = true) ∧
    ∀ x, x < 2 ^ F.A → x ≠ 0 → (∃ i < F.A, aliveF F x i = true) → Relation.ReflTransGen (StepN F) x u

variable {F} {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)

include hs in
theorem aR_pos_iffF (x i : ℕ) : 0 < aR F ρ1 ρ2 x i ↔ aliveF F x i = true := by
  simp only [aR, aliveF]
  exact aliveProbR_pos_iff (by exact_mod_cast hs.h0) (by exact_mod_cast hs.h1) (by exact_mod_cast hs.h2)
    (by exact_mod_cast hs.h3) _ _ _ _

theorem Q_pos_iffF (hc : CellsOK F) (x y : {x : Fin (2 ^ F.A) // x ≠ F.empty}) :
    0 < (chain F hs.dens).Q x y ↔ stepF F x y = true := by
  rw [chain_Q, P_cast]
  have h0 : ∀ (x : Fin (2 ^ F.A)) i, i < F.A → 0 ≤ aR F ρ1 ρ2 x i := fun x i _ => by
    have h := aliveProb_mem hs.dens.h0 hs.dens.h1 hs.dens.h2 hs.dens.h3 (F.m1 i) (F.m2 i) (F.k x i)
      (Nat.testBit x i)
    rw [← a_cast]; exact_mod_cast h.1
  have h1 : ∀ (x : Fin (2 ^ F.A)) i, i < F.A → aR F ρ1 ρ2 x i < 1 := fun x i hi => by
    have := atom_le_one_sub_a F hs hc x i hi
    have hp := atomMin_pos (ρ1 := (ρ1 : ℝ)) (ρ2 := (ρ2 : ℝ)) (by exact_mod_cast hs.h0)
      (by exact_mod_cast hs.h1) (by exact_mod_cast hs.h2) (by exact_mod_cast hs.h3)
    rw [← a_cast]; linarith
  rw [bitP_pos_iff h0 h1]
  simp only [stepF, List.all_eq_true, List.mem_range, Bool.or_eq_true, Bool.not_eq_true']
  constructor
  · intro h i hi
    by_cases hy : (y : ℕ).testBit i
    · right; exact (aR_pos_iffF hs x i).1 (h i hi hy)
    · left; simpa using hy
  · intro h i hi hy
    rcases h i hi with h' | h'
    · simp [hy] at h'
    · exact (aR_pos_iffF hs x i).2 h'

/-- A living state from a number. -/
def liv (F : Face) (a : ℕ) (ha : a < 2 ^ F.A) (ha0 : a ≠ 0) : {x : Fin (2 ^ F.A) // x ≠ F.empty} :=
  ⟨⟨a, ha⟩, fun e => ha0 ((empty_iff F _).1 e)⟩

theorem rtg_pow (hc : CellsOK F) {a b : ℕ} (h : Relation.ReflTransGen (StepN F) a b) :
    ∀ (ha : a < 2 ^ F.A) (ha0 : a ≠ 0) (hb : b < 2 ^ F.A) (hb0 : b ≠ 0),
      ∃ k, 0 < ((chain F hs.dens).Q ^ k) (liv F a ha ha0) (liv F b hb hb0) := by
  induction h using Relation.ReflTransGen.head_induction_on with
  | refl => intro ha ha0 _ _; exact ⟨0, by simp⟩
  | @head a c hac _ ih =>
    intro ha ha0 hb hb0
    obtain ⟨hc1, hc0, hst⟩ := hac
    obtain ⟨k, hk⟩ := ih hc1 hc0 hb hb0
    have hq := (Q_pos_iffF hs hc (liv F a ha ha0) (liv F c hc1 hc0)).2 hst
    refine ⟨k + 1, ?_⟩
    rw [pow_succ', Matrix.mul_apply]
    exact lt_of_lt_of_le (mul_pos hq hk)
      (single_le_sum (f := fun w => (chain F hs.dens).Q (liv F a ha ha0) w *
        ((chain F hs.dens).Q ^ k) w (liv F b hb hb0))
        (fun w _ => mul_nonneg ((chain F hs.dens).nonneg _ _)
          (pow_entry_nonneg (fun x y => (chain F hs.dens).nonneg x y) k _ _)) (mem_univ _))

theorem lt_A_of_testBit (y : Fin (2 ^ F.A)) (i : ℕ) (h : (y : ℕ).testBit i = true) : i < F.A := by
  by_contra hcon
  have h1 := Nat.ge_two_pow_of_testBit h
  have h2 := y.2
  have h3 : 2 ^ F.A ≤ 2 ^ i := Nat.pow_le_pow_right (by norm_num) (by omega)
  omega

/-- **The full lifetime theorem of a face from Lemma 0**: on every face with its coins, `Lemma0F` gives the
unique law among λ > 0, positive on every living state, and decay at exactly λ from every state that can survive. -/
theorem face_full_of (hc : CellsOK F) (hA : 0 < F.A) (h0 : Lemma0F F) :
    ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ 0 < lam ∧
      (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs hc).price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain F hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain F hs.dens).survFrom t x) ∧
        (∀ t x, (chain F hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  set K := chain F hs.dens
  obtain ⟨μ, lam, hD, hdice, hdc, hprice, -, -⟩ := face_theorems F hs hc hA
  obtain ⟨u, hu, hu0, hall, hreach⟩ := h0
  set U := liv F u hu hu0
  have huall : ∀ y, 0 < K.Q U y := fun y => by
    rw [Q_pos_iffF hs hc]
    simp only [stepF, List.all_eq_true, List.mem_range]
    intro i hi
    exact Bool.or_eq_true_iff.2 (Or.inr (hall i hi))
  have hreach' : ∀ x, K.CanSurvive x → ∃ k, 0 < (K.Q ^ k) x U := by
    intro x ⟨y, hy⟩
    have hst := (Q_pos_iffF hs hc x y).1 hy
    have hy0 : (y.1 : ℕ) ≠ 0 := fun e => y.2 ((empty_iff F y.1).2 e)
    obtain ⟨i, hi⟩ := Nat.exists_testBit_of_ne_zero hy0
    have hiA := lt_A_of_testBit y.1 i hi
    have hal : aliveF F x i = true := by
      simp only [stepF, List.all_eq_true, List.mem_range] at hst
      have := hst i hiA
      rw [hi] at this
      simpa using this
    have hx0 : (x.1 : ℕ) ≠ 0 := fun e => x.2 ((empty_iff F x.1).2 e)
    exact rtg_pow hs hc (hreach x x.1.2 hx0 ⟨i, hiA, hal⟩) x.1.2 hx0 hu hu0
  obtain ⟨hirr, hout, μ0, lam0, hq0, hlam0, hpos0, huniq⟩ := one_class' K U huall hreach'
  have hlam : 0 < lam := lt_of_lt_of_le (huall U) (hD.diag U)
  obtain ⟨hμ, hl⟩ := huniq μ lam hD.qsd hlam
  have hpu : K.CanSurvive U := ⟨U, huall U⟩
  have : Nonempty {x // K.CanSurvive x} := ⟨⟨_, hpu⟩⟩
  obtain ⟨r, m, M, -, hm, hmM, hrq, hlo, hup⟩ := K.decay_bounds K.CanSurvive hirr hout
  have hrl : lam = r := hrq μ lam hD.qsd hlam
  refine ⟨μ, lam, hD, hdice, hlam, fun x => hμ ▸ hpos0 x, fun ν lam' h h' => ?_, hdc, hprice,
    m, M, hm, hmM, fun t x hx => hrl ▸ hlo t x hx, fun t x => hrl ▸ hup t x⟩
  obtain ⟨e1, e2⟩ := huniq ν lam' h h'
  exact ⟨e1.trans hμ.symm, e2.trans hl.symm⟩

end Abstract

/-! ### Every hull face under Lemma 0 -/

/-- **Every hull face at (0.44, 0.42), for `Face.P` itself, under `Lemma0F (Gump.Dice.hull R)`**: unique law among λ > 0,
positive on every living state; ln τ = Σ c_i (named per-cell factors); ln τ < 2.2165·A; decay at exactly λ from
every state that can survive; survFrom = Face.survival. -/
theorem hull_full_all (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) (h0 : Lemma0F (Gump.Dice.hull R)) :
    ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧
      IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧
      (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x = (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, hdec⟩ :=
    face_full_of Hull3.sdens (cellsOK_hull R) hA h0
  refine ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, ?_, hdec,
    survFrom_cast _ _ (absorbing_hull R ρ1 ρ2)⟩
  rw [log_lifetime_eq (LH R Hull3.sdens) hD.qsd]
  exact lntau_le_hull_all R _ lam hdice hA

/-! ### Lemma 0 from a polynomial-size certificate -/

section Cert
variable (F : Face)

/-- `l` lists the states after a, in order, of a chain of possible transitions from a ending at b. -/
def pathFrom : ℕ → List ℕ → ℕ → Bool
  | a, [], b => a == b
  | a, c :: l, b => decide (c < 2 ^ F.A) && decide (c ≠ 0) && stepF F a c && pathFrom c l b

theorem pathFrom_rtg : ∀ (l : List ℕ) (a b : ℕ), pathFrom F a l b = true → Relation.ReflTransGen (StepN F) a b
  | [], a, b, h => by
    simp only [pathFrom, beq_iff_eq] at h
    rw [h]
  | c :: l, a, b, h => by
    simp only [pathFrom, Bool.and_eq_true, decide_eq_true_eq] at h
    exact Relation.ReflTransGen.head ⟨h.1.1.1, h.1.1.2, h.1.2⟩ (pathFrom_rtg l c b h.2)

/-- The certificate: u (every cell can be alive next from it), a base cell c0 with a path from {c0} to u, and for
every cell i a walk from {i} to {c0}. -/
def certOK (u c0 : ℕ) (common : List ℕ) (walks : List (List ℕ)) : Bool :=
  decide (u < 2 ^ F.A) && decide (u ≠ 0) && (List.range F.A).all (fun i => aliveF F u i) &&
    pathFrom F (2 ^ c0) common u &&
    (List.range F.A).all (fun i => pathFrom F (2 ^ i) (walks.getD i []) (2 ^ c0))

theorem step_single (x i : ℕ) (h : aliveF F x i = true) : stepF F x (2 ^ i) = true := by
  simp only [stepF, List.all_eq_true, List.mem_range]
  intro j _
  rw [Nat.testBit_two_pow]
  by_cases hij : i = j
  · subst hij; rw [h, Bool.or_true]
  · simp [hij]

/-- **Lemma 0 from the certificate.** -/
theorem lemma0_of_cert (u c0 : ℕ) (common : List ℕ) (walks : List (List ℕ))
    (h : certOK F u c0 common walks = true) : Lemma0F F := by
  simp only [certOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at h
  obtain ⟨⟨⟨⟨hu, hu0⟩, hall⟩, hcom⟩, hwalk⟩ := h
  refine ⟨u, hu, hu0, hall, fun x _ _ ⟨i, hi, hal⟩ => ?_⟩
  have h2 : 2 ^ i < 2 ^ F.A := Nat.pow_lt_pow_right (by norm_num) hi
  exact Relation.ReflTransGen.head ⟨h2, by positivity, step_single F x i hal⟩
    ((pathFrom_rtg F _ _ _ (hwalk i hi)).trans (pathFrom_rtg F _ _ _ hcom))

end Cert

end Gump.Link
