/-
The lifetime of the face `(hull 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42), as one self-contained
theorem about `Gump.Dice.Face.P` (written by the chain agent's generator from the dice agent's tables
`GumpMath/DiceHull3Data.lean`; every check below is run by the kernel, `decide +kernel`).

The reachability certificate: u = 207 (every cell can be alive next), and for each of the 511 states that
can survive a possible next state (`nxt`) one step closer to u (`dist`, at most 3).
-/
import GumpMath.LinkUnique
import GumpMath.DiceHull3

set_option maxRecDepth 100000

namespace Gump.Link.Hull3
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The state from which every state can be reached in one step. -/
def u : ℕ := 207
/-- A possible next state, one step closer to u. -/
def nxt : List ℕ := [0, 18, 6, 5, 6, 54, 54, 39, 36, 54, 54, 39, 6, 30, 30, 207, 18, 18, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 15, 207, 207, 20, 54, 54, 39, 30, 30, 30, 207, 20, 30, 30, 15, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 20, 6, 6, 5, 54, 54, 54, 39, 20, 54, 54, 39, 30, 30, 30, 207, 54, 39, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 20, 54, 54, 39, 30, 30, 30, 207, 20, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 34, 18, 54, 39, 6, 54, 54, 39, 6, 54, 54, 39, 6, 30, 30, 207, 18, 18, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 54, 54, 54, 39, 30, 30, 30, 207, 30, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 54, 54, 54, 39, 54, 54, 54, 39, 54, 54, 54, 39, 30, 30, 30, 0, 54, 39, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 54, 54, 54, 39, 30, 30, 30, 207, 30, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 192, 18, 6, 5, 6, 54, 54, 39, 36, 54, 54, 39, 6, 30, 30, 207, 18, 18, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 20, 54, 54, 39, 30, 30, 30, 207, 20, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 20, 6, 6, 5, 54, 54, 54, 39, 20, 54, 54, 39, 30, 30, 30, 207, 54, 39, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 20, 54, 54, 39, 30, 30, 30, 207, 20, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 34, 18, 54, 39, 6, 54, 54, 39, 6, 54, 54, 39, 6, 30, 30, 207, 18, 18, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 54, 54, 54, 39, 30, 30, 30, 207, 30, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207, 54, 54, 54, 39, 54, 54, 54, 39, 54, 54, 54, 39, 30, 30, 30, 207, 54, 39, 39, 39, 54, 39, 39, 39, 54, 39, 39, 39, 30, 207, 207, 207, 54, 54, 54, 39, 30, 30, 30, 207, 30, 30, 30, 207, 30, 30, 30, 207, 54, 39, 39, 39, 30, 207, 207, 207, 30, 207, 207, 207, 30, 207, 207, 207]
/-- The number of steps to u. -/
def dist : List ℕ := [0, 3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1]

theorem cells : cellsD Hull3Data.data (hull 3).A = true := by decide +kernel
theorem uok : uOK Hull3Data.data (hull 3).A u = true := by decide +kernel
theorem reach : reachOK Hull3Data.data (hull 3).A u nxt dist = true := by decide +kernel
theorem hA : 0 < (hull 3).A := by decide +kernel

theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath (hull 3) sdens (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells)

/-- **The lifetime of the face `(hull 3)`.**  Its killed chain (`Face.P` itself, killed at the empty face) has a
quasi-stationary law (the dominant one), unique among those with λ > 0 and charging every living state; it is the
dice agent's `IsQSD`; 0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374 and 2.4837157463 < ln τ < 2.4837157464 (τ = E_μ T); ln τ = Σ_i c_i with c_i the tilt price of
cell i's own death probability; and survival from every state that can survive decays at exactly the rate λ. -/
theorem hull3_link :
    ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
      2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧
      (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) :=
  face_lifetime (hull 3) Hull3Data.data Hull3Data.tab sdens cells hA u nxt dist uok reach _ _ _ _
    (fun μ lam hq _ => hull3_tau μ lam hq)

end Gump.Link.Hull3
