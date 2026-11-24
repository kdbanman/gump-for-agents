/-
ref-chain, second review: attacks on the repaired chain statements and on the Link modules.

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/RefChainLink.lean
  (about 1 minute)

1. `IsDominantQSD` (repair of D2) excludes the junk law: on every wrapped face a dominant law has λ > 0
   (`dominant_lam_pos`), so it is the unique physical law (`dominant_is_physical`), and the point mass on the
   all-alive state is not dominant (`junk_not_dominant`).  In general the dominant λ is unique
   (`dominant_lam_unique`), hence so is τ = 1/(1 - λ) (`dominant_lifetime_unique`).
2. The kernel checks reject wrong certificates and tables (each `= false` is proved by `decide +kernel`):
   a wrong next state (`reach_rejects_nxt`), a wrong distance (`reach_rejects_dist`), a permutation that is
   not a table symmetry (`sym_rejects_perm`), a correct permutation with a wrong state action
   (`sym_rejects_action`), a wrong coin table (`tab_rejects_coins`), a wrong neighbour table
   (`tab_rejects_nbrs`).
3. What `hull3_full` is about: ρ1 = 11/25, ρ2 = 21/50; its `L` is `localDeath (hull 3)`; the face has 9 cells.
-/
import GumpMath.LinkFaces
import GumpMath.ChainKagome

open Finset Gump.Chain Gump.Chain.KilledChain Gump.Dice Gump.Link

namespace RefChainLink

/-! ### 1. The dominant law -/

theorem dominant_lam_unique {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ)
    {μ ν : σ → ℝ} {lam lam' : ℝ} (h : K.IsDominantQSD μ lam) (h' : K.IsDominantQSD ν lam') : lam = lam' :=
  le_antisymm (h'.max μ lam h.qsd) (h.max ν lam' h'.qsd)

theorem dominant_lifetime_unique {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ)
    {V : Type*} [Fintype V] (L : K.LocalDeath V)
    {μ ν : σ → ℝ} {lam lam' : ℝ} (h : K.IsDominantQSD μ lam) (h' : K.IsDominantQSD ν lam') :
    K.lifetime μ = K.lifetime ν := by
  have hh : 0 < K.hazard μ := by rw [L.hazard_eq_Z]; exact Z_pos h.qsd.isProb _ _
  have hh' : 0 < K.hazard ν := by rw [L.hazard_eq_Z]; exact Z_pos h'.qsd.isProb _ _
  rw [h.qsd.lifetime_eq hh, h'.qsd.lifetime_eq hh']
  have e1 := h.qsd.lam_eq; have e2 := h'.qsd.lam_eq
  have := dominant_lam_unique K h h'
  congr 1; linarith

section Kagome
open Gump.Chain.Kagome
variable {T : Type*} [AddCommGroup T] [Fintype T] [DecidableEq T] (e1 e2 : T)
variable {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1)
variable (hgen : AddSubgroup.closure ({e1, e2} : Set T) = ⊤)

def allLive : Living (Cell T) := ⟨univ, ⟨(Orient.X, 0), mem_univ _⟩⟩

include hgen in
theorem dominant_lam_pos {μ : Living (Cell T) → ℝ} {lam : ℝ}
    (hD : (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsDominantQSD μ lam) : 0 < lam := by
  obtain ⟨-, -, -, μ0, lam0, hq0, hl0, -, -⟩ := kagome_lemma0 e1 e2 h1 h1' h2 h2' hgen
  exact lt_of_lt_of_le hl0 (hD.max μ0 lam0 hq0)

include hgen in
theorem dominant_is_physical {μ : Living (Cell T) → ℝ} {lam : ℝ}
    (hD : (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsDominantQSD μ lam) :
    ∀ ν lam', (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD ν lam' → 0 < lam' → ν = μ := by
  obtain ⟨-, -, -, μ0, lam0, hq0, hl0, -, huniq⟩ := kagome_lemma0 e1 e2 h1 h1' h2 h2' hgen
  have hm := (huniq μ lam hD.qsd (dominant_lam_pos e1 e2 h1 h1' h2 h2' hgen hD)).1
  intro ν lam' h h'
  exact (huniq ν lam' h h').1.trans hm.symm

include hgen in
theorem junk_not_dominant :
    ¬ (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsDominantQSD
      (fun y => if y = allLive then 1 else 0) 0 :=
  fun hD => lt_irrefl _ (dominant_lam_pos e1 e2 h1 h1' h2 h2' hgen hD)

end Kagome

/-! ### 2. The kernel checks reject wrong data -/

/-- State 492 = all cells but 0 and its two neighbours 1, 4: cell 0 is dead with no live neighbour, so it
cannot be born; a certificate claiming 492 → 493 (cell 0 added) must fail.  (Chosen near the top so that the
kernel meets it after 19 rows; a full run of the check needs more memory than this review may use.) -/
theorem reach_rejects_nxt :
    reachOK Hull3Data.data (hull 3).A Hull3.u (Hull3.nxt.set 492 493) Hull3.dist = false := by decide +kernel

/-- The full face claimed at distance 0 from u: the decrease of `dist` fails at once. -/
theorem reach_rejects_dist :
    reachOK Hull3Data.data (hull 3).A Hull3.u Hull3.nxt (Hull3.dist.set 511 0) = false := by decide +kernel

/-- Swap a corner (cell 0, coins (2,0)) with a rim cell (cell 1, coins (2,1)). -/
def badσ : List ℕ := [1, 0, 2, 3, 4, 5, 6, 7, 8]

theorem sym_rejects_perm :
    Hull3Data.data.symOK (hull 3).A badσ (Tree.build (hull 3).A (act badσ) 0) = false := by decide +kernel

theorem sym_rejects_action :
    Hull3Data.data.symOK (hull 3).A Hull3.σ0 (Tree.build (hull 3).A (act Hull3.σ1) 0) = false := by
  decide +kernel

theorem tab_rejects_coins :
    ({ Hull3Data.data with C := Hull3Data.data.C.set 0 (2, 1) } : Data).tabOK (hull 3) = false := by
  decide +kernel

theorem tab_rejects_nbrs :
    ({ Hull3Data.data with G := Hull3Data.data.G.set 0 [1, 2] } : Data).tabOK (hull 3) = false := by
  decide +kernel

/-- Positive control: the true certificate passes (the chain agent's `Hull3.reach`, taken from its olean). -/
theorem reach_accepts : reachOK Hull3Data.data (hull 3).A Hull3.u Hull3.nxt Hull3.dist = true := Hull3.reach

/-! ### 3. What the statements are about -/

example : Gump.Dice.ρ1 = 11 / 25 ∧ Gump.Dice.ρ2 = 21 / 50 := ⟨rfl, rfl⟩
example : (hull 3).A = 9 := by decide +kernel
example : Hull3.L = localDeath (hull 3) Hull3.sdens (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab Hull3.cells) := rfl
example : Hull3Data.data.C.getD 0 (0, 0) = (2, 0) ∧ Hull3Data.data.C.getD 1 (0, 0) = (2, 1) := by decide +kernel

end RefChainLink

#print axioms RefChainLink.dominant_lifetime_unique
#print axioms RefChainLink.dominant_is_physical
#print axioms RefChainLink.junk_not_dominant
#print axioms RefChainLink.reach_rejects_nxt
#print axioms RefChainLink.tab_rejects_nbrs
