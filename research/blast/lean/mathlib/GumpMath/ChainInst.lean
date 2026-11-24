/-
The interface for instantiating the chain theorems with a concrete surrogate (`GumpMath/Dice*.lean` builds
one: states `Fin (2 ^ A)` as bit masks, the empty face 0 absorbing, a product kernel over ℚ).

`ofStochastic P o`: the killed chain of a stochastic matrix P on a finite set S at the absorbing state o
(the empty face); its death probability is P x o (`ofStochastic_death`).
`isQSD_of`: a law on S vanishing at o and a left eigenvector on the other states is a quasi-stationary law
of that killed chain (the form of `Gump.Dice.IsQSD`).
`ofStochastic_local`: P x o = ∏_i (1 - a_i x) with 0 ≤ a_i < 1 gives the local death factors.
`one_class`: **Lemma 0 in its abstract form**: if some living state u leads to every living state in one
step, and every state that can survive one step leads to u, then the quasi-stationary law with λ > 0 is
unique and charges every living state.
`surrogate_theorems`: Theorems 1 and 2 at once for such a chain.
-/
import Mathlib
import GumpMath.ChainExist
import GumpMath.ChainCoins

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Matrix

variable {S : Type*} [Fintype S] [DecidableEq S]

namespace KilledChain

theorem sum_ne_add (f : S → ℝ) (o : S) : ∑ y : {y : S // y ≠ o}, f y + f o = ∑ y, f y := by
  rw [← Finset.sum_erase_add univ f (mem_univ o)]
  congr 1
  exact (Finset.sum_subtype (univ.erase o) (fun y => by simp) f).symm

/-- The killed chain of a stochastic matrix at an absorbing state o. -/
def ofStochastic (P : Matrix S S ℝ) (o : S) (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1) :
    KilledChain {x : S // x ≠ o} where
  Q := fun x y => P x y
  nonneg := fun x y => hP x y
  sub := fun x => by
    have := sum_ne_add (fun y => P x y) o
    rw [hrow] at this
    linarith [hP x o]

theorem ofStochastic_death (P : Matrix S S ℝ) (o : S) (hP : ∀ x y, 0 ≤ P x y)
    (hrow : ∀ x, ∑ y, P x y = 1) (x : {x : S // x ≠ o}) :
    (ofStochastic P o hP hrow).death x = P x o := by
  have := sum_ne_add (fun y => P x y) o
  rw [hrow] at this
  simp only [death, ofStochastic]
  linarith

/-- A law on S that vanishes at o and is a left eigenvector on the other states is quasi-stationary. -/
theorem isQSD_of (P : Matrix S S ℝ) (o : S) (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1)
    (μ : S → ℝ) (lam : ℝ) (h0 : μ o = 0) (hnn : ∀ x, 0 ≤ μ x) (htot : ∑ x, μ x = 1)
    (heig : ∀ y, y ≠ o → ∑ x, μ x * P x y = lam * μ y) :
    (ofStochastic P o hP hrow).IsQSD (fun x => μ x) lam := by
  refine ⟨fun x => hnn x, ?_, fun y => ?_⟩
  · have := sum_ne_add μ o; rw [h0, add_zero, htot] at this; exact this
  · have := sum_ne_add (fun x => μ x * P x y) o
    simp only [h0, zero_mul, add_zero] at this
    rw [heig y y.2] at this
    exact this

/-- Local death factors from P x o = ∏_i (1 - a_i x), 0 ≤ a_i < 1. -/
noncomputable def ofStochastic_local {V : Type*} [Fintype V] (P : Matrix S S ℝ) (o : S)
    (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1) (a : V → S → ℝ)
    (ha0 : ∀ i x, 0 ≤ a i x) (ha1 : ∀ i x, a i x < 1)
    (hprod : ∀ x, x ≠ o → P x o = ∏ i, (1 - a i x)) :
    (ofStochastic P o hP hrow).LocalDeath V where
  dc := fun i x => 1 - a i x
  pos := fun i x => by linarith [ha1 i x]
  le_one := fun i x => by linarith [ha0 i x]
  prod := fun x => by rw [ofStochastic_death]; exact hprod x x.2

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

theorem exists_pos_term {ι : Type*} [Fintype ι] {f : ι → ℝ} (h : 0 < ∑ i, f i) : ∃ i, 0 < f i := by
  by_contra hc
  push Not at hc
  have := Finset.sum_nonpos (fun i (_ : i ∈ (univ : Finset ι)) => hc i)
  linarith

theorem pos_pos_of_mul_pos {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (h : 0 < a * b) : 0 < a ∧ 0 < b :=
  ⟨lt_of_le_of_ne ha (fun e => by rw [← e, zero_mul] at h; exact lt_irrefl 0 h),
   lt_of_le_of_ne hb (fun e => by rw [← e, mul_zero] at h; exact lt_irrefl 0 h)⟩

theorem p_of_pow_pos (K : KilledChain σ) (p : σ → Prop) (hp : ∀ x y, 0 < K.Q x y → p x)
    (k : ℕ) (y z : σ) (hz : p z) (h : 0 < (K.Q ^ k) y z) : p y := by
  cases k with
  | zero =>
    simp only [pow_zero, Matrix.one_apply] at h
    split_ifs at h with hyz
    · exact hyz ▸ hz
    · exact absurd h (lt_irrefl 0)
  | succ k =>
    rw [pow_succ', Matrix.mul_apply] at h
    obtain ⟨w, hw⟩ := exists_pos_term h
    exact hp y w (pos_pos_of_mul_pos (K.nonneg y w) (pow_entry_nonneg K.nonneg k w z) hw).1

/-- Positive powers between states that can survive lift to the block on those states. -/
theorem block_pow_pos (K : KilledChain σ) (p : σ → Prop) [DecidablePred p]
    (hp : ∀ x y, 0 < K.Q x y → p x) :
    ∀ (k : ℕ) (x z : σ) (hx : p x) (hz : p z), 0 < (K.Q ^ k) x z →
      0 < (K.block p ^ k) ⟨x, hx⟩ ⟨z, hz⟩ := by
  intro k
  induction k with
  | zero =>
    intro x z hx hz h
    simp only [pow_zero, Matrix.one_apply] at h ⊢
    split_ifs at h with hxz
    · subst hxz; simp
    · exact absurd h (lt_irrefl 0)
  | succ k ih =>
    intro x z hx hz h
    rw [pow_succ', Matrix.mul_apply] at h
    obtain ⟨y, hy⟩ := exists_pos_term h
    obtain ⟨hxy, hyz⟩ := pos_pos_of_mul_pos (K.nonneg x y) (pow_entry_nonneg K.nonneg k y z) hy
    have py : p y := K.p_of_pow_pos p hp k y z hz hyz
    have ih' := ih y z py hz hyz
    rw [pow_succ', Matrix.mul_apply]
    exact lt_of_lt_of_le (mul_pos (show 0 < K.block p ⟨x, hx⟩ ⟨y, py⟩ from hxy) ih')
      (single_le_sum (f := fun w => K.block p ⟨x, hx⟩ w * (K.block p ^ k) w ⟨z, hz⟩)
        (fun w _ => mul_nonneg (K.nonneg _ _) (pow_entry_nonneg (A := K.block p) (fun a b => K.nonneg a b) k _ _))
        (mem_univ _))

/-- The states that can survive one more generation. -/
def CanSurvive (K : KilledChain σ) (x : σ) : Prop := ∃ y, 0 < K.Q x y

noncomputable instance (K : KilledChain σ) : DecidablePred K.CanSurvive := Classical.decPred _

/-- **Lemma 0, abstract form.**  If a living state u leads to every living state in one step, and every
state that can survive one step leads to u, then there is exactly one quasi-stationary law with λ > 0,
and it charges every living state. -/
theorem one_class (K : KilledChain σ) (u : σ) (hu : ∀ y, 0 < K.Q u y)
    (hreach : ∀ x, K.CanSurvive x → ∃ k, 0 < (K.Q ^ k) x u) :
    ∃ μ lam, K.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam := by
  have hp : ∀ x y, 0 < K.Q x y → K.CanSurvive x := fun x y h => ⟨y, h⟩
  have hpu : K.CanSurvive u := ⟨u, hu u⟩
  have hirr : Irreducible (K.block K.CanSurvive) := by
    intro a b
    obtain ⟨k, hk⟩ := hreach a.1 a.2
    have h1 := K.block_pow_pos K.CanSurvive hp k a.1 u a.2 hpu hk
    refine ⟨k + 1, ?_⟩
    rw [pow_succ, Matrix.mul_apply]
    exact lt_of_lt_of_le (mul_pos h1 (show 0 < K.block K.CanSurvive ⟨u, hpu⟩ b from hu b.1))
      (single_le_sum (f := fun w => (K.block K.CanSurvive ^ k) a w * K.block K.CanSurvive w b)
        (fun w _ => mul_nonneg (pow_entry_nonneg (A := K.block K.CanSurvive) (fun a b => K.nonneg a b) k _ _)
          (K.nonneg _ _))
        (mem_univ _))
  have hout : ∀ y, ¬ K.CanSurvive y → ∀ z, K.Q y z = 0 := fun y hy z => by
    apply le_antisymm _ (K.nonneg y z)
    by_contra h
    exact hy ⟨z, lt_of_not_ge h⟩
  exact K.qsd_exists_unique K.CanSurvive hirr hout (fun y _ => ⟨u, hpu, hu y⟩) ⟨u, hpu, hu u⟩

end KilledChain

open KilledChain in
/-- **Theorems 1 and 2 for a stochastic matrix with an absorbing empty face and a product death
probability** (the shape of the surrogate in `GumpMath/DiceDef.lean`), for the dominant quasi-stationary law
(`IsDominantQSD`): log τ = ∑_i c_i with c_i the price of the cell's own factor 1 - a_i, τ ≥ 1/(1 - Q u u) for
every living u, and if every local factor 1 - a_i is at least the smallest atom of the coins,
log τ ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) · A. -/
theorem surrogate_theorems {V : Type*} [Fintype V] (P : Matrix S S ℝ) (o : S) (hne : ∃ x, x ≠ o)
    (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1) (a : V → S → ℝ)
    (ha0 : ∀ i x, 0 ≤ a i x) (ha1 : ∀ i x, a i x < 1)
    (hprod : ∀ x, x ≠ o → P x o = ∏ i, (1 - a i x)) {ρ1 ρ2 : ℝ}
    (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1)
    (hatom : ∀ i x, atomMin ρ1 ρ2 ≤ 1 - a i x) :
    ∃ μ lam, (ofStochastic P o hP hrow).IsDominantQSD μ lam ∧
      Real.log ((ofStochastic P o hP hrow).lifetime μ) =
        ∑ i, (ofStochastic_local P o hP hrow a ha0 ha1 hprod).price μ i ∧
      Real.log ((ofStochastic P o hP hrow).lifetime μ) ≤
        -Real.log (atomMin ρ1 ρ2) * Fintype.card V ∧
      ∀ u, 1 / (1 - (ofStochastic P o hP hrow).Q u u) ≤ (ofStochastic P o hP hrow).lifetime μ := by
  obtain ⟨x, hx⟩ := hne
  have : Nonempty {x : S // x ≠ o} := ⟨⟨x, hx⟩⟩
  set L := ofStochastic_local P o hP hrow a ha0 ha1 hprod
  obtain ⟨μ, lam, hD, -, he, -, hu⟩ := (ofStochastic P o hP hrow).tilt_identity_exists L
  exact ⟨μ, lam, hD, he, upper_bound_coins L hD.qsd h1 h1' h2 h2' (fun i x => hatom i x), hu⟩

end Gump.Chain
