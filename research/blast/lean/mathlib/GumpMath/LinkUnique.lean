/-
Lemma 0 for `Face.P` face by face, from a reachability certificate checked by the kernel, and the assembly of one
self-contained lifetime theorem per face.

Combinatorics (`canB`, `aliveProbR_pos_iff`): for 0 < ρ1, ρ2 < 1 a cell can be alive next iff some coin outcome
puts k + heads in the rule's window.  With the dice agent's checked tables (`Data.tabOK`), `aliveD`, `stepD`,
`survD` decide the support of `Face.P` (`Q_pos_iff`).  A certificate (u, nxt, dist) — u a state in which every cell
can be alive next, and for every state that can survive a possible next state closer to u — is checked by
`reachOK`/`uOK` (`decide +kernel`) and gives, through `one_class` (here `one_class'`, with the irreducibility
exported), uniqueness of the quasi-stationary law with λ > 0, positivity on every living state, and the decay
rate from every start of the living class (`decay_bounds`).

`face_lifetime`: the assembled statement for a face, given the dice agent's certified interval for λ.
-/
import Mathlib
import GumpMath.LinkBridge

set_option linter.unusedSectionVars false

namespace Gump.Link
open Finset Gump.Chain Gump.Chain.Bits Gump.Chain.KilledChain Gump.Dice

/-! ### One cell: positivity of the alive probability -/

/-- Some coin outcome puts k + heads in the rule's window. -/
def canB (m1 m2 k : ℕ) (s : Bool) : Bool :=
  (List.range (m1 + 1)).any fun j => (List.range (m2 + 1)).any fun l => Gump.rule s (k + j + l)

theorem binR_pos {m j : ℕ} {ρ : ℝ} (h0 : 0 < ρ) (h1 : ρ < 1) (hj : j ≤ m) : 0 < binR m ρ j := by
  have : 0 < 1 - ρ := by linarith
  have hc : (0 : ℝ) < (m.choose j : ℝ) := by exact_mod_cast Nat.choose_pos hj
  simp only [binR]; positivity

theorem aliveProbR_pos_iff {ρ1 ρ2 : ℝ} (h0 : 0 < ρ1) (h1 : ρ1 < 1) (h2 : 0 < ρ2) (h3 : ρ2 < 1)
    (m1 m2 k : ℕ) (s : Bool) : 0 < aliveProbR ρ1 ρ2 m1 m2 k s ↔ canB m1 m2 k s = true := by
  have hterm : ∀ j ∈ range (m1 + 1), ∀ l ∈ range (m2 + 1), 0 ≤ binR m1 ρ1 j * binR m2 ρ2 l :=
    fun j hj l hl => mul_nonneg (binR_pos h0 h1 (Nat.lt_succ_iff.1 (mem_range.1 hj))).le
      (binR_pos h2 h3 (Nat.lt_succ_iff.1 (mem_range.1 hl))).le
  simp only [canB, List.any_eq_true, List.mem_range]
  constructor
  · intro h
    by_contra hc
    push Not at hc
    have : aliveProbR ρ1 ρ2 m1 m2 k s = 0 := by
      unfold aliveProbR
      refine Finset.sum_eq_zero (fun j hj => Finset.sum_eq_zero (fun l hl => ?_))
      have := hc j (mem_range.1 hj) l (mem_range.1 hl)
      simp [this]
    linarith
  · rintro ⟨j, hj, l, hl, hr⟩
    unfold aliveProbR
    have hin : ∀ j ∈ range (m1 + 1), 0 ≤ ∑ l ∈ range (m2 + 1),
        (if Gump.rule s (k + j + l) then binR m1 ρ1 j * binR m2 ρ2 l else 0) := fun j hj =>
      Finset.sum_nonneg (fun l hl => by split_ifs; exacts [hterm j hj l hl, le_refl _])
    refine lt_of_lt_of_le ?_ (single_le_sum hin (mem_range.2 hj))
    refine lt_of_lt_of_le ?_ (single_le_sum (f := fun l =>
      (if Gump.rule s (k + j + l) then binR m1 ρ1 j * binR m2 ρ2 l else 0))
      (fun l hl => by split_ifs; exacts [hterm j (mem_range.2 hj) l hl, le_refl _]) (mem_range.2 hl))
    simp only [hr, ite_true]
    exact mul_pos (binR_pos h0 h1 (Nat.lt_succ_iff.1 hj)) (binR_pos h2 h3 (Nat.lt_succ_iff.1 hl))

/-! ### The support of `Face.P`, decided on the dice agent's tables -/

/-- Cell i can be alive next from x, by the tables. -/
def aliveD (c : Data) (x i : ℕ) : Bool :=
  canB (c.C.getD i (0, 0)).1 (c.C.getD i (0, 0)).2 (c.kk x i) (x.testBit i)

/-- x → y is possible. -/
def stepD (c : Data) (A x y : ℕ) : Bool := (List.range A).all fun i => !(y.testBit i) || aliveD c x i

/-- Some cell can be alive next. -/
def survD (c : Data) (A x : ℕ) : Bool := (List.range A).any fun i => aliveD c x i

/-- The cells' coins, by the tables: (2,1), or (2,0) with at most two neighbours. -/
def cellsD (c : Data) (A : ℕ) : Bool :=
  (List.range A).all fun i => c.C.getD i (0, 0) == (2, 1) ||
    (c.C.getD i (0, 0) == (2, 0) && decide ((c.G.getD i []).length ≤ 2))

section Face
variable (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)
include htab

theorem cellsOK_of_tab (hcd : cellsD c F.A = true) : CellsOK F := by
  intro i hi
  obtain ⟨-, -, -, -, h⟩ := Data.tabOK_spec c F htab
  obtain ⟨hG, hC, -, -⟩ := h i hi
  simp only [cellsD, List.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq, Bool.and_eq_true,
    decide_eq_true_eq] at hcd
  rcases hcd i hi with h1 | ⟨h1, h2⟩
  · rw [h1] at hC; left; exact ⟨(Prod.mk.inj hC).1.symm, (Prod.mk.inj hC).2.symm⟩
  · rw [h1] at hC; right; exact ⟨(Prod.mk.inj hC).1.symm, (Prod.mk.inj hC).2.symm, hG ▸ h2⟩

include hs in
theorem aR_pos_iff (x i : ℕ) (hi : i < F.A) : 0 < aR F ρ1 ρ2 x i ↔ aliveD c x i = true := by
  obtain ⟨-, -, -, -, h⟩ := Data.tabOK_spec c F htab
  obtain ⟨hG, hC, -, -⟩ := h i hi
  have hk : c.kk x i = F.k x i := by simp only [Data.kk, Face.k, hG]
  simp only [aR, aliveD, hC, hk]
  exact aliveProbR_pos_iff (by exact_mod_cast hs.h0) (by exact_mod_cast hs.h1) (by exact_mod_cast hs.h2)
    (by exact_mod_cast hs.h3) _ _ _ _

include hs in
theorem Q_pos_iff (hc : CellsOK F) (x y : {x : Fin (2 ^ F.A) // x ≠ F.empty}) :
    0 < (chain F hs.dens).Q x y ↔ stepD c F.A x y = true := by
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
  simp only [stepD, List.all_eq_true, List.mem_range, Bool.or_eq_true, Bool.not_eq_true']
  constructor
  · intro h i hi
    by_cases hy : (y : ℕ).testBit i
    · right; exact (aR_pos_iff F c htab hs x i hi).1 (h i hi hy)
    · left; simpa using hy
  · intro h i hi hy
    rcases h i hi with h' | h'
    · simp [hy] at h'
    · exact (aR_pos_iff F c htab hs x i hi).2 h'

include hs in
theorem survD_of_canSurvive (hc : CellsOK F) (x : {x : Fin (2 ^ F.A) // x ≠ F.empty})
    (h : (chain F hs.dens).CanSurvive x) : survD c F.A x = true := by
  obtain ⟨y, hy⟩ := h
  have hst := (Q_pos_iff F c htab hs hc x y).1 hy
  have hy0 : (y : ℕ) ≠ 0 := fun e => y.2 ((empty_iff F _).2 e)
  obtain ⟨i, hi⟩ := Nat.exists_testBit_of_ne_zero hy0
  have hiA : i < F.A := by
    by_contra hcon
    have h1 := Nat.ge_two_pow_of_testBit hi
    have h2 := (y : Fin (2 ^ F.A)).2
    have h3 : 2 ^ F.A ≤ 2 ^ i := Nat.pow_le_pow_right (by norm_num) (by omega)
    omega
  simp only [stepD, List.all_eq_true, List.mem_range, Bool.or_eq_true, Bool.not_eq_true'] at hst
  simp only [survD, List.any_eq_true, List.mem_range]
  rcases hst i hiA with h' | h'
  · simp [hi] at h'
  · exact ⟨i, hiA, h'⟩

end Face

/-! ### The certificate -/

/-- u is a state in which every cell can be alive next. -/
def uOK (c : Data) (A u : ℕ) : Bool :=
  u != 0 && decide (u < 2 ^ A) && (List.range A).all (aliveD c u)

/-- Every state that can survive has a possible next state that is u or closer to u. -/
def reachOK (c : Data) (A u : ℕ) (nxt dist : List ℕ) : Bool :=
  Data.allRows (fun x => x == 0 || !(survD c A x) || x == u ||
    (stepD c A x (nxt.getD x 0) && (nxt.getD x 0 != 0) && decide (nxt.getD x 0 < 2 ^ A) &&
      (nxt.getD x 0 == u || survD c A (nxt.getD x 0)) &&
      decide (dist.getD (nxt.getD x 0) 0 < dist.getD x 0))) (2 ^ A)

/-- Lemma 0's abstract form with the irreducibility exported (as in `KilledChain.one_class`). -/
theorem one_class' {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ) (u : σ)
    (hu : ∀ y, 0 < K.Q u y) (hreach : ∀ x, K.CanSurvive x → ∃ k, 0 < (K.Q ^ k) x u) :
    Chain.Irreducible (K.block K.CanSurvive) ∧ (∀ y, ¬ K.CanSurvive y → ∀ z, K.Q y z = 0) ∧
    ∃ μ lam, K.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam := by
  have hp : ∀ x y, 0 < K.Q x y → K.CanSurvive x := fun x y h => ⟨y, h⟩
  have hpu : K.CanSurvive u := ⟨u, hu u⟩
  have hirr : Chain.Irreducible (K.block K.CanSurvive) := by
    intro a b
    obtain ⟨k, hk⟩ := hreach a.1 a.2
    have h1 := K.block_pow_pos K.CanSurvive hp k a.1 u a.2 hpu hk
    refine ⟨k + 1, ?_⟩
    rw [pow_succ, Matrix.mul_apply]
    exact lt_of_lt_of_le (mul_pos h1 (show 0 < K.block K.CanSurvive ⟨u, hpu⟩ b from hu b.1))
      (single_le_sum (f := fun w => (K.block K.CanSurvive ^ k) a w * K.block K.CanSurvive w b)
        (fun w _ => mul_nonneg (pow_entry_nonneg (A := K.block K.CanSurvive) (fun a b => K.nonneg a b) k _ _)
          (K.nonneg _ _)) (mem_univ _))
  have hout : ∀ y, ¬ K.CanSurvive y → ∀ z, K.Q y z = 0 := fun y hy z => by
    apply le_antisymm _ (K.nonneg y z)
    by_contra h
    exact hy ⟨z, lt_of_not_ge h⟩
  exact ⟨hirr, hout, K.qsd_exists_unique K.CanSurvive hirr hout (fun y _ => ⟨u, hpu, hu y⟩) ⟨u, hpu, hu u⟩⟩

section Cert
variable (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F)
variable (u : ℕ) (nxt dist : List ℕ) (huOK : uOK c F.A u = true) (hR : reachOK c F.A u nxt dist = true)
include htab hc huOK hR

theorem u_ne (hu' : u < 2 ^ F.A) : (⟨u, hu'⟩ : Fin (2 ^ F.A)) ≠ F.empty := by
  intro e
  have := (empty_iff F _).1 e
  simp only [uOK, Bool.and_eq_true, bne_iff_ne] at huOK
  exact huOK.1.1 this

include hs in
/-- **Lemma 0 on the face, from the certificate**: u leads everywhere in one step, every state that can survive
leads to u. -/
theorem face_class :
    ∃ hu' : u < 2 ^ F.A,
      (∀ y, 0 < (chain F hs.dens).Q ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩ y) ∧
      ∀ x, (chain F hs.dens).CanSurvive x →
        ∃ k, 0 < ((chain F hs.dens).Q ^ k) x ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩ := by
  have huOK' := huOK
  simp only [uOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at huOK'
  obtain ⟨⟨-, hu'⟩, hall⟩ := huOK'
  refine ⟨hu', fun y => ?_, ?_⟩
  · rw [Q_pos_iff F c htab hs hc]
    simp only [stepD, List.all_eq_true, List.mem_range, Bool.or_eq_true]
    exact fun i hi => Or.inr (hall i hi)
  · set U : {x : Fin (2 ^ F.A) // x ≠ F.empty} := ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩
    have hrows := Data.allRows_spec _ _ hR
    have key : ∀ n, ∀ x : {x : Fin (2 ^ F.A) // x ≠ F.empty}, dist.getD (x : ℕ) 0 = n →
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
            ⟨⟨nxt.getD x 0, hnA⟩, fun e => hn0 ((empty_iff F _).1 e)⟩
          have hQ : 0 < (chain F hs.dens).Q x z := (Q_pos_iff F c htab hs hc x z).2 hst
          obtain ⟨k, hk⟩ := ih _ (hxn ▸ hd) z rfl hnu
          refine ⟨k + 1, ?_⟩
          rw [pow_succ', Matrix.mul_apply]
          exact lt_of_lt_of_le (mul_pos hQ hk)
            (single_le_sum (f := fun w => (chain F hs.dens).Q x w * ((chain F hs.dens).Q ^ k) w U)
              (fun w _ => mul_nonneg ((chain F hs.dens).nonneg _ _)
                (pow_entry_nonneg (chain F hs.dens).nonneg k _ _)) (mem_univ z))
    exact fun x hx => key _ x rfl (Or.inr (survD_of_canSurvive F c htab hs hc x hx))

end Cert

/-! ### The assembled lifetime theorem of a face -/

theorem log_lifetime_eq {σ : Type*} [Fintype σ] [DecidableEq σ] {V : Type*} [Fintype V]
    {K : KilledChain σ} (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hq : K.IsQSD μ lam) :
    Real.log (K.lifetime μ) = -Real.log (1 - lam) := by
  have hh : 0 < K.hazard μ := by rw [L.hazard_eq_Z]; exact Z_pos hq.isProb _ _
  rw [hq.lifetime_eq hh, one_div, Real.log_inv, hq.lam_eq]; ring_nf

/-- **The lifetime of a certified face**, assembled: given the tables, the reachability certificate and the dice
agent's interval [lo, hi] for λ (with a < -log(1 - λ) < b) for every quasi-stationary law with λ > 0. -/
theorem face_lifetime (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)
    (hcd : cellsD c F.A = true) (hA : 0 < F.A) (u : ℕ) (nxt dist : List ℕ) (huOK : uOK c F.A u = true)
    (hR : reachOK c F.A u nxt dist = true) (lo hi a b : ℝ)
    (hτ : ∀ μ lam, IsQSD F ρ1 ρ2 μ lam → 0 < lam →
      lo ≤ lam ∧ lam ≤ hi ∧ a < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < b) :
    ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ 0 < lam ∧
      (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      lo ≤ lam ∧ lam ≤ hi ∧
      a < Real.log ((chain F hs.dens).lifetime μ) ∧ Real.log ((chain F hs.dens).lifetime μ) < b ∧
      (∀ i x, (localDeath F hs (cellsOK_of_tab F c htab hcd)).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain F hs.dens).lifetime μ) =
        ∑ i, (localDeath F hs (cellsOK_of_tab F c htab hcd)).price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain F hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain F hs.dens).survFrom t x) ∧
        (∀ t x, (chain F hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  have hc := cellsOK_of_tab F c htab hcd
  set K := chain F hs.dens
  obtain ⟨μ, lam, hD, hdice, hdc, hprice, -, -⟩ := face_theorems F hs hc hA
  obtain ⟨hu', huall, hreach⟩ := face_class F c htab hs hc u nxt dist huOK hR
  set U : {x : Fin (2 ^ F.A) // x ≠ F.empty} := ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩
  obtain ⟨hirr, hout, μ0, lam0, hq0, hlam0, hpos0, huniq⟩ := one_class' K U huall hreach
  -- the dominant law has λ ≥ Q u u > 0, so it is the unique one
  have hlam : 0 < lam := lt_of_lt_of_le (huall U) (hD.diag U)
  obtain ⟨hμ, hl⟩ := huniq μ lam hD.qsd hlam
  have hpu : K.CanSurvive U := ⟨U, huall U⟩
  have : Nonempty {x // K.CanSurvive x} := ⟨⟨_, hpu⟩⟩
  obtain ⟨r, m, M, hr, hm, hmM, hrq, hlo, hup⟩ := K.decay_bounds K.CanSurvive hirr hout
  have hrl : lam = r := hrq μ lam hD.qsd hlam
  obtain ⟨b1, b2, b3, b4⟩ := hτ _ _ hdice hlam
  have hlog := log_lifetime_eq (localDeath F hs hc) hD.qsd
  refine ⟨μ, lam, hD, hdice, hlam, fun x => hμ ▸ hpos0 x, fun ν lam' h h' => ?_, b1, b2,
    hlog ▸ b3, hlog ▸ b4, hdc, hprice, m, M, hm, hmM, fun t x hx => hrl ▸ hlo t x hx, fun t x => hrl ▸ hup t x⟩
  obtain ⟨e1, e2⟩ := huniq ν lam' h h'
  exact ⟨e1.trans hμ.symm, e2.trans hl.symm⟩

end Gump.Link
