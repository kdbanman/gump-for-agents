/-
The lifetime of the face `(strip 1 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42), as one self-contained
theorem about `Gump.Dice.Face.P` (written by the chain agent's generator from the dice agent's tables
`GumpMath/DiceStrip13Data.lean`; every check below is run by the kernel, `decide +kernel`).

The reachability certificate: u = 14 (every cell can be alive next), and for each of the 511 states that
can survive a possible next state (`nxt`) one step closer to u (`dist`, at most 3).
-/
import GumpMath.LinkUnique
import GumpMath.DiceStrip13

set_option maxRecDepth 100000

namespace Gump.Link.Strip13
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The state from which every state can be reached in one step. -/
def u : ℕ := 14
/-- A possible next state, one step closer to u. -/
def nxt : List ℕ := [0, 33, 17, 17, 1, 33, 17, 17, 16, 14, 14, 14, 14, 14, 0, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 260, 33, 17, 17, 257, 33, 17, 17, 12, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 18, 17, 17, 17, 17, 17, 17, 17, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 18, 17, 17, 17, 17, 17, 17, 17, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 200, 14, 14, 14, 14, 14, 14, 14, 80, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 12, 14, 14, 14, 14, 14, 14, 14, 12, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 10, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 9, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
/-- The number of steps to u. -/
def dist : List ℕ := [0, 2, 2, 2, 3, 2, 2, 2, 3, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

theorem cells : cellsD Strip13Data.data (strip 1 3).A = true := by decide +kernel
theorem uok : uOK Strip13Data.data (strip 1 3).A u = true := by decide +kernel
theorem reach : reachOK Strip13Data.data (strip 1 3).A u nxt dist = true := by decide +kernel
theorem hA : 0 < (strip 1 3).A := by decide +kernel

theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath (strip 1 3) sdens (cellsOK_of_tab (strip 1 3) Strip13Data.data Strip13Data.tab cells)

/-- **The lifetime of the face `(strip 1 3)`.**  Its killed chain (`Face.P` itself, killed at the empty face) has a
quasi-stationary law (the dominant one), unique among those with λ > 0 and charging every living state; it is the
dice agent's `IsQSD`; 0.9391216736592712685 ≤ λ ≤ 0.9391216736592712686 and 2.7988780569 < ln τ < 2.7988780570 (τ = E_μ T); ln τ = Σ_i c_i with c_i the tilt price of
cell i's own death probability; and survival from every state that can survive decays at exactly the rate λ. -/
theorem strip13_link :
    ∃ μ lam, (chain (strip 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (strip 1 3) ρ1 ρ2 (extend (strip 1 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (strip 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9391216736592712685 : ℝ) ≤ lam ∧ lam ≤ 0.9391216736592712686 ∧
      2.7988780569 < Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) < 2.7988780570 ∧
      (∀ i x, L.dc i x = 1 - (((strip 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (strip 1 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (strip 1 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (strip 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) :=
  face_lifetime (strip 1 3) Strip13Data.data Strip13Data.tab sdens cells hA u nxt dist uok reach _ _ _ _
    (fun μ lam hq _ => strip13_tau μ lam hq)

end Gump.Link.Strip13
