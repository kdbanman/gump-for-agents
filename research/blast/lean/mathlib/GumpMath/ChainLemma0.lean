/-
Lemma 0 of `research/blast/rigour/THEOREMS.md` (one living class), and the product kernel that the
one-layer dice surrogate is.

`ProductKernel V`: every cell i is alive next with probability `a i x` given the present state x (a set of
live cells), independently over cells, with `0 ≤ a i x < 1` (the standing assumption (K): every cell can
die).  The kernel on states is P(x, y) = ∏_i (a i x if i ∈ y else 1 - a i x); it is stochastic
(`total`), its death probability is ∏_i (1 - a i x) (`death_eq`), so it carries local death factors and
Theorem 2 applies to it as it stands (`ProductKernel.tilt_identity`).

`SubsetChain V`: any chain on the subsets of V whose possible successors from x are exactly the subsets
of a set M x (for the product kernel M x = {i | a i x > 0}: step (1) of Lemma 0's proof).
`SubsetChain.lemma0`: if singletons communicate, some state u has M u = V and u is reachable from a
singleton (steps (2)–(4) of the proof, the geometric part, taken here as hypotheses), then the states
with M x ≠ ∅ form one irreducible class, u → u, every other non-empty state dies surely and is entered
from u; hence (`lemma0_qsd`) exactly one quasi-stationary law with λ > 0, charging every non-empty state.
-/
import Mathlib
import GumpMath.ChainExist

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Matrix Relation

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- The non-empty states (sets of live cells). -/
abbrev Living (V : Type*) [Fintype V] [DecidableEq V] := {x : Finset V // x.Nonempty}

/-- A chain on the subsets of V whose possible successors from x are exactly the subsets of M x. -/
structure SubsetChain (V : Type*) [Fintype V] [DecidableEq V] where
  P : Finset V → Finset V → ℝ
  M : Finset V → Finset V
  nonneg : ∀ x y, 0 ≤ P x y
  total : ∀ x, ∑ y, P x y = 1
  supp : ∀ x y, 0 < P x y ↔ y ⊆ M x

namespace SubsetChain
variable (C : SubsetChain V)

/-- The killed chain on the non-empty states. -/
def killed : KilledChain (Living V) where
  Q := fun a b => C.P a b
  nonneg := fun a b => C.nonneg a b
  sub := fun a => by
    have h := C.total a
    rw [← Fintype.sum_subtype_add_sum_subtype (fun y : Finset V => y.Nonempty)] at h
    have : 0 ≤ ∑ i : {y : Finset V // ¬ y.Nonempty}, C.P a i :=
      sum_nonneg (fun i _ => C.nonneg _ _)
    show ∑ y : Living V, C.P a y ≤ 1
    linarith

/-- The death probability of the killed chain is P(x, ∅). -/
theorem killed_death (a : Living V) : C.killed.death a = C.P a ∅ := by
  have h := C.total a
  rw [← Fintype.sum_subtype_add_sum_subtype (fun y : Finset V => y.Nonempty)] at h
  have e : ∑ i : {y : Finset V // ¬ y.Nonempty}, C.P a i = C.P a ∅ := by
    rw [Fintype.sum_eq_single (⟨∅, by simp⟩ : {y : Finset V // ¬ y.Nonempty})]
    intro i hi
    exact absurd (Subtype.ext (not_nonempty_iff_eq_empty.1 i.2)) hi
  simp only [KilledChain.death, killed]
  linarith

/-- (K) in its weak form: from every state the face is empty one generation later with positive
probability (∅ ⊆ M x). -/
theorem death_pos (a : Living V) : 0 < C.killed.death a := by
  rw [killed_death]; exact (C.supp a ∅).2 (empty_subset _)

/-- One possible step between non-empty states. -/
def Step (x y : Finset V) : Prop := y.Nonempty ∧ y ⊆ C.M x

/-- The states some cell of which can be alive next (the set L of Lemma 0). -/
def canLive (a : Living V) : Prop := (C.M a.1).Nonempty

instance : DecidablePred C.canLive := fun _ => Finset.decidableNonempty

theorem lift (b : {a : Living V // C.canLive a}) :
    ∀ x, ReflTransGen C.Step x b.1.1 → ∀ (hx : x.Nonempty) (hpx : (C.M x).Nonempty),
      ∃ k, 0 < (C.killed.block C.canLive ^ k) ⟨⟨x, hx⟩, hpx⟩ b := by
  intro x h
  induction h using Relation.ReflTransGen.head_induction_on with
  | refl =>
    intro hx hpx
    have e : (⟨⟨b.1.1, hx⟩, hpx⟩ : {a : Living V // C.canLive a}) = b := rfl
    exact ⟨0, by rw [e, pow_zero]; simp⟩
  | @head x c hxc hcb ih =>
    intro hx hpx
    have hc : c.Nonempty := hxc.1
    have hpc : (C.M c).Nonempty := by
      rcases hcb.cases_head with h | ⟨d, hcd, -⟩
      · rw [h]; exact b.2
      · exact hcd.1.mono hcd.2
    obtain ⟨k, hk⟩ := ih hc hpc
    refine ⟨k + 1, ?_⟩
    rw [pow_succ', Matrix.mul_apply]
    have hstep : 0 < C.killed.block C.canLive ⟨⟨x, hx⟩, hpx⟩ ⟨⟨c, hc⟩, hpc⟩ :=
      (C.supp x c).2 hxc.2
    exact lt_of_lt_of_le (mul_pos hstep hk)
      (single_le_sum (f := fun z => C.killed.block C.canLive ⟨⟨x, hx⟩, hpx⟩ z *
          (C.killed.block C.canLive ^ k) z b)
        (fun z _ => mul_nonneg (C.nonneg _ _) (pow_entry_nonneg (fun i j => C.nonneg _ _) k _ _))
        (mem_univ _))

/-- **Lemma 0 (one living class)**, with its geometric steps (2)–(4) as hypotheses. -/
theorem lemma0 [Nonempty V]
    (hsing : ∀ i j : V, ReflTransGen C.Step {i} {j})
    (u : Finset V) (hun : u.Nonempty) (hu : C.M u = univ)
    (hreach : ∃ i, ReflTransGen C.Step {i} u) :
    Irreducible (C.killed.block C.canLive) ∧
    (∀ y, ¬ C.canLive y → ∀ z, C.killed.Q y z = 0) ∧
    (∀ y : Living V, 0 < C.killed.Q ⟨u, hun⟩ y) ∧
    C.canLive ⟨u, hun⟩ := by
  have hcu : C.canLive ⟨u, hun⟩ := by simp only [canLive, hu]; exact univ_nonempty
  refine ⟨?_, ?_, fun y => (C.supp u y).2 (hu ▸ subset_univ _), hcu⟩
  · intro a b
    obtain ⟨i, hi⟩ := a.2
    obtain ⟨i0, hi0⟩ := hreach
    have hab : ReflTransGen C.Step a.1.1 b.1.1 :=
      ReflTransGen.head ⟨singleton_nonempty i, singleton_subset_iff.2 hi⟩
        ((hsing i i0).trans (hi0.trans
          (ReflTransGen.single ⟨b.1.2, hu ▸ subset_univ _⟩)))
    obtain ⟨k, hk⟩ := C.lift b a.1.1 hab a.1.2 a.2
    exact ⟨k, hk⟩
  · intro y hy z
    apply le_antisymm _ (C.nonneg _ _)
    by_contra h
    push Not at h
    have hz := (C.supp y z).1 h
    exact hy (z.2.mono hz)

/-- **Lemma 0, conclusion**: exactly one quasi-stationary law with λ > 0, and it charges every
non-empty state. -/
theorem lemma0_qsd [Nonempty V]
    (hsing : ∀ i j : V, ReflTransGen C.Step {i} {j})
    (u : Finset V) (hun : u.Nonempty) (hu : C.M u = univ)
    (hreach : ∃ i, ReflTransGen C.Step {i} u) :
    ∃ μ lam, C.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      ∀ ν lam', C.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam := by
  obtain ⟨hirr, hout, hin, hcu⟩ := C.lemma0 hsing u hun hu hreach
  exact C.killed.qsd_exists_unique C.canLive hirr hout (fun y _ => ⟨⟨u, hun⟩, hcu, hin y⟩)
    ⟨⟨u, hun⟩, hcu, hin _⟩

end SubsetChain

/-- A product kernel: cell i is alive next with probability `a i x`, independently, and (K) every
cell can die. -/
structure ProductKernel (V : Type*) [Fintype V] [DecidableEq V] where
  a : V → Finset V → ℝ
  nonneg : ∀ i x, 0 ≤ a i x
  lt_one : ∀ i x, a i x < 1

namespace ProductKernel
variable (G : ProductKernel V)

/-- The kernel on states: P(x, y) = ∏_i (a_i(x) if i ∈ y else 1 - a_i(x)). -/
def P (x y : Finset V) : ℝ := ∏ i, (if i ∈ y then G.a i x else 1 - G.a i x)

/-- The cells that can be alive next. -/
noncomputable def M (x : Finset V) : Finset V := univ.filter (fun i => 0 < G.a i x)

theorem kernel_nonneg (x y : Finset V) : 0 ≤ G.P x y :=
  prod_nonneg (fun i _ => by
    split_ifs
    · exact G.nonneg i x
    · linarith [G.lt_one i x])

theorem total (x : Finset V) : ∑ y, G.P x y = 1 := by
  have h := Finset.prod_add (fun i => G.a i x) (fun i => 1 - G.a i x) (univ : Finset V)
  simp only [add_sub_cancel, prod_const_one, powerset_univ] at h
  rw [h]
  refine Finset.sum_congr rfl (fun y _ => ?_)
  rw [P, prod_ite]
  congr 1
  · congr 1; ext i; simp
  · congr 1; ext i; simp

/-- Step (1) of Lemma 0: the possible successors of x are exactly the subsets of M x. -/
theorem supp (x y : Finset V) : 0 < G.P x y ↔ y ⊆ G.M x := by
  constructor
  · intro h i hi
    simp only [M, mem_filter, mem_univ, true_and]
    rcases (G.nonneg i x).lt_or_eq with h' | h'
    · exact h'
    · exfalso
      have : G.P x y = 0 := prod_eq_zero (mem_univ i) (by simp [hi, ← h'])
      linarith
  · intro h
    apply prod_pos
    intro i _
    split_ifs with hi
    · have := h hi; simpa [M] using this
    · linarith [G.lt_one i x]

noncomputable def toSubsetChain : SubsetChain V where
  P := G.P
  M := G.M
  nonneg := G.kernel_nonneg
  total := G.total
  supp := G.supp

/-- The death probability is the product of the local factors 1 - a_i. -/
theorem death_eq (a : Living V) : G.toSubsetChain.killed.death a = ∏ i, (1 - G.a i a) := by
  rw [SubsetChain.killed_death]; simp [toSubsetChain, P]

/-- The local death factors of the product kernel. -/
noncomputable def localDeath : G.toSubsetChain.killed.LocalDeath V where
  dc := fun i a => 1 - G.a i a
  pos := fun i a => by linarith [G.lt_one i a]
  le_one := fun i a => by linarith [G.nonneg i a]
  prod := G.death_eq

/-- **Theorem 2 for every product kernel** (every face of the surrogate, wrapped or rimmed). -/
theorem tilt_identity_product [Nonempty V] :
    ∃ μ lam, G.toSubsetChain.killed.IsQSD μ lam ∧
      Real.log (G.toSubsetChain.killed.lifetime μ) =
        ∫ s in (0:ℝ)..1, tiltMean μ G.localDeath.energy s G.localDeath.energy ∧
      Real.log (G.toSubsetChain.killed.lifetime μ) = ∑ i, G.localDeath.price μ i := by
  have : Nonempty (Living V) := ⟨⟨univ, univ_nonempty⟩⟩
  exact KilledChain.tilt_identity_exists _ G.localDeath

end ProductKernel
end Gump.Chain
