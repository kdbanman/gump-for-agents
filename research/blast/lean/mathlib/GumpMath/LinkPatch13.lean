/-
The lifetime of the face `(patch 1 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42), as one self-contained
theorem about `Gump.Dice.Face.P` (written by the chain agent's generator from the dice agent's tables
`GumpMath/DicePatch13Data.lean`; every check below is run by the kernel, `decide +kernel`).

The reachability certificate: u = 73 (every cell can be alive next), and for each of the 511 states that
can survive a possible next state (`nxt`) one step closer to u (`dist`, at most 4).
-/
import GumpMath.LinkUnique
import GumpMath.DicePatch13

set_option maxRecDepth 100000

namespace Gump.Link.Patch13
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The state from which every state can be reached in one step. -/
def u : ℕ := 73
/-- A possible next state, one step closer to u. -/
def nxt : List ℕ := [0, 2, 16, 16, 2, 2, 16, 16, 288, 257, 257, 257, 257, 257, 257, 257, 138, 137, 137, 137, 137, 137, 137, 137, 138, 137, 137, 137, 137, 137, 137, 137, 8, 8, 8, 8, 8, 8, 8, 8, 257, 257, 257, 257, 257, 257, 257, 257, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 128, 96, 81, 81, 257, 96, 81, 81, 96, 0, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 16, 81, 81, 81, 81, 81, 81, 81, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 16, 81, 81, 81, 81, 81, 81, 81, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 8, 73, 73, 73, 73, 73, 73, 73, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 8, 73, 73, 73, 73, 73, 73, 73, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 8, 73, 73, 73, 73, 73, 73, 73, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 8, 73, 73, 73, 73, 73, 73, 73, 96, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73]
/-- The number of steps to u. -/
def dist : List ℕ := [0, 4, 3, 3, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

theorem cells : cellsD Patch13Data.data (patch 1 3).A = true := by decide +kernel
theorem uok : uOK Patch13Data.data (patch 1 3).A u = true := by decide +kernel
theorem reach : reachOK Patch13Data.data (patch 1 3).A u nxt dist = true := by decide +kernel
theorem hA : 0 < (patch 1 3).A := by decide +kernel

theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath (patch 1 3) sdens (cellsOK_of_tab (patch 1 3) Patch13Data.data Patch13Data.tab cells)

/-- **The lifetime of the face `(patch 1 3)`.**  Its killed chain (`Face.P` itself, killed at the empty face) has a
quasi-stationary law (the dominant one), unique among those with λ > 0 and charging every living state; it is the
dice agent's `IsQSD`; 0.8474738060566295030 ≤ λ ≤ 0.8474738060566295031 and 1.8804189341 < ln τ < 1.8804189342 (τ = E_μ T); ln τ = Σ_i c_i with c_i the tilt price of
cell i's own death probability; and survival from every state that can survive decays at exactly the rate λ. -/
theorem patch13_link :
    ∃ μ lam, (chain (patch 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (patch 1 3) ρ1 ρ2 (extend (patch 1 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (patch 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.8474738060566295030 : ℝ) ≤ lam ∧ lam ≤ 0.8474738060566295031 ∧
      1.8804189341 < Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) < 1.8804189342 ∧
      (∀ i x, L.dc i x = 1 - (((patch 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (patch 1 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (patch 1 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (patch 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) :=
  face_lifetime (patch 1 3) Patch13Data.data Patch13Data.tab sdens cells hA u nxt dist uok reach _ _ _ _
    (fun μ lam hq _ => patch13_tau μ lam hq)

end Gump.Link.Patch13
