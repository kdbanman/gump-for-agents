/-
Lemma 0 for `Face.P` from a reachability certificate given as functions (`reachOKF`; for 12 cells the certificate is
two trees of depth 12, `Tree.get`, so that a lookup costs 12 steps in the kernel), and the assembled theorem
without a certified λ interval (`face_unique`): for a face with checked tables whose certificate passes, the
dominant quasi-stationary law of `Face.P` is unique among λ > 0, charges every living state, survival from every
state that can survive decays at exactly its rate, and ln τ is the sum of the per-cell prices.
-/
import Mathlib
import GumpMath.LinkUnique

set_option linter.unusedSectionVars false

namespace Gump.Link
open Finset Gump.Chain Gump.Chain.Bits Gump.Chain.KilledChain Gump.Dice

/-- Every state that can survive has a possible next state `nx x` that is u or closer to u (`ds`). -/
def reachOKF (c : Data) (A u : ℕ) (nx ds : ℕ → ℕ) : Bool :=
  Data.allRows (fun x => x == 0 || !(survD c A x) || x == u ||
    (stepD c A x (nx x) && (nx x != 0) && decide (nx x < 2 ^ A) &&
      (nx x == u || survD c A (nx x)) && decide (ds (nx x) < ds x))) (2 ^ A)

section CertF
variable (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F)
variable (u : ℕ) (nx ds : ℕ → ℕ) (huOK : uOK c F.A u = true) (hR : reachOKF c F.A u nx ds = true)
include htab hc huOK hR

theorem u_neF (hu' : u < 2 ^ F.A) : (⟨u, hu'⟩ : Fin (2 ^ F.A)) ≠ F.empty := by
  intro e
  have := (empty_iff F _).1 e
  simp only [uOK, Bool.and_eq_true, bne_iff_ne] at huOK
  exact huOK.1.1 this

include hs in
/-- **Lemma 0 on the face, from the certificate**: u leads everywhere in one step, every state that can survive
leads to u. -/
theorem face_classF :
    ∃ hu' : u < 2 ^ F.A,
      (∀ y, 0 < (chain F hs.dens).Q ⟨⟨u, hu'⟩, u_neF F c htab hc u nx ds huOK hR hu'⟩ y) ∧
      ∀ x, (chain F hs.dens).CanSurvive x →
        ∃ k, 0 < ((chain F hs.dens).Q ^ k) x ⟨⟨u, hu'⟩, u_neF F c htab hc u nx ds huOK hR hu'⟩ := by
  have huOK' := huOK
  simp only [uOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at huOK'
  obtain ⟨⟨-, hu'⟩, hall⟩ := huOK'
  refine ⟨hu', fun y => ?_, ?_⟩
  · rw [Q_pos_iff F c htab hs hc]
    simp only [stepD, List.all_eq_true, List.mem_range, Bool.or_eq_true]
    exact fun i hi => Or.inr (hall i hi)
  · set U : {x : Fin (2 ^ F.A) // x ≠ F.empty} := ⟨⟨u, hu'⟩, u_neF F c htab hc u nx ds huOK hR hu'⟩
    have hrows := Data.allRows_spec _ _ hR
    have key : ∀ n, ∀ x : {x : Fin (2 ^ F.A) // x ≠ F.empty}, ds (x : ℕ) = n →
        ((x : ℕ) = u ∨ survD c F.A x = true) → ∃ k, 0 < ((chain F hs.dens).Q ^ k) x U := by
      intro n
      induction n using Nat.strong_induction_on with
      | _ n ih =>
        intro x hxn hxs
        by_cases hxu : (x : ℕ) = u
        · refine ⟨0, ?_⟩
          have : x = U := Subtype.ext (Fin.ext hxu)
          rw [this, pow_zero, Matrix.one_apply_eq]; exact one_pos
        · have hsx : survD c F.A x = true := hxs.resolve_left hxu
          have hr := hrows x (x : Fin (2 ^ F.A)).2
          have hx0 : ((x : Fin (2 ^ F.A)) : ℕ) ≠ 0 := fun e => x.2 ((empty_iff F _).2 e)
          have h0' : (((x : Fin (2 ^ F.A)) : ℕ) == 0) = false := by simpa using hx0
          have hs' : (!survD c F.A x) = false := by simp [hsx]
          have hu'' : (((x : Fin (2 ^ F.A)) : ℕ) == u) = false := by simpa using hxu
          rw [h0', hs', hu''] at hr
          simp only [Bool.false_or, Bool.and_eq_true, bne_iff_ne, decide_eq_true_eq, Bool.or_eq_true,
            beq_iff_eq] at hr
          obtain ⟨⟨⟨⟨hst, hn0⟩, hnA⟩, hnu⟩, hd⟩ := hr
          set z : {x : Fin (2 ^ F.A) // x ≠ F.empty} :=
            ⟨⟨nx x, hnA⟩, fun e => hn0 ((empty_iff F _).1 e)⟩
          have hQ : 0 < (chain F hs.dens).Q x z := (Q_pos_iff F c htab hs hc x z).2 hst
          obtain ⟨k, hk⟩ := ih _ (hxn ▸ hd) z rfl hnu
          refine ⟨k + 1, ?_⟩
          rw [pow_succ', Matrix.mul_apply]
          exact lt_of_lt_of_le (mul_pos hQ hk)
            (single_le_sum (f := fun w => (chain F hs.dens).Q x w * ((chain F hs.dens).Q ^ k) w U)
              (fun w _ => mul_nonneg ((chain F hs.dens).nonneg _ _)
                (pow_entry_nonneg (chain F hs.dens).nonneg k _ _)) (mem_univ z))
    exact fun x hx => key _ x rfl (Or.inr (survD_of_canSurvive F c htab hs hc x hx))

end CertF

/-- **The lifetime theorem of a face without a certified λ**: everything of `face_lifetime` but the interval. -/
theorem face_unique (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)
    (hc : CellsOK F) (hA : 0 < F.A) (u : ℕ) (nx ds : ℕ → ℕ) (huOK : uOK c F.A u = true)
    (hR : reachOKF c F.A u nx ds = true) :
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
  obtain ⟨hu', huall, hreach⟩ := face_classF F c htab hs hc u nx ds huOK hR
  set U : {x : Fin (2 ^ F.A) // x ≠ F.empty} := ⟨⟨u, hu'⟩, u_neF F c htab hc u nx ds huOK hR hu'⟩
  obtain ⟨hirr, hout, μ0, lam0, hq0, hlam0, hpos0, huniq⟩ := one_class' K U huall hreach
  have hlam : 0 < lam := lt_of_lt_of_le (huall U) (hD.diag U)
  obtain ⟨hμ, hl⟩ := huniq μ lam hD.qsd hlam
  have hpu : K.CanSurvive U := ⟨U, huall U⟩
  have : Nonempty {x // K.CanSurvive x} := ⟨⟨_, hpu⟩⟩
  obtain ⟨r, m, M, hr, hm, hmM, hrq, hlo, hup⟩ := K.decay_bounds K.CanSurvive hirr hout
  have hrl : lam = r := hrq μ lam hD.qsd hlam
  refine ⟨μ, lam, hD, hdice, hlam, fun x => hμ ▸ hpos0 x, fun ν lam' h h' => ?_, hdc, hprice,
    m, M, hm, hmM, fun t x hx => hrl ▸ hlo t x hx, fun t x => hrl ▸ hup t x⟩
  obtain ⟨e1, e2⟩ := huniq ν lam' h h'
  exact ⟨e1.trans hμ.symm, e2.trans hl.symm⟩

end Gump.Link
