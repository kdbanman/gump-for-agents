/-
The lifetime of the face `(torus 1 0 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42), as one self-contained
theorem about `Gump.Dice.Face.P` (written by the chain agent's generator from the dice agent's tables
`GumpMath/DiceTorus103Data.lean`; every check below is run by the kernel, `decide +kernel`).

The reachability certificate: u = 10 (every cell can be alive next), and for each of the 510 states that
can survive a possible next state (`nxt`) one step closer to u (`dist`, at most 2).
-/
import GumpMath.LinkUnique
import GumpMath.DiceTorus103

set_option maxRecDepth 100000

namespace Gump.Link.Torus103
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The state from which every state can be reached in one step. -/
def u : ℕ := 10
/-- A possible next state, one step closer to u. -/
def nxt : List ℕ := [0, 10, 1, 10, 1, 10, 1, 10, 1, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 16, 10, 1, 10, 1, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 1, 10, 10, 10, 10, 10, 1, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 1, 10, 10, 10, 10, 10, 1, 10, 16, 16, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 16, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 1, 10, 10, 10, 10, 10, 1, 10, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 0]
/-- The number of steps to u. -/
def dist : List ℕ := [0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0]

theorem cells : cellsD Torus103Data.data (torus 1 0 3).A = true := by decide +kernel
theorem uok : uOK Torus103Data.data (torus 1 0 3).A u = true := by decide +kernel
theorem reach : reachOK Torus103Data.data (torus 1 0 3).A u nxt dist = true := by decide +kernel
theorem hA : 0 < (torus 1 0 3).A := by decide +kernel

theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath (torus 1 0 3) sdens (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells)

/-- **The lifetime of the face `(torus 1 0 3)`.**  Its killed chain (`Face.P` itself, killed at the empty face) has a
quasi-stationary law (the dominant one), unique among those with λ > 0 and charging every living state; it is the
dice agent's `IsQSD`; 0.9664099275695942426 ≤ λ ≤ 0.9664099275695942427 and 3.3935247190 < ln τ < 3.3935247191 (τ = E_μ T); ln τ = Σ_i c_i with c_i the tilt price of
cell i's own death probability; and survival from every state that can survive decays at exactly the rate λ. -/
theorem torus103_link :
    ∃ μ lam, (chain (torus 1 0 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 1 0 3) ρ1 ρ2 (extend (torus 1 0 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (torus 1 0 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9664099275695942426 : ℝ) ≤ lam ∧ lam ≤ 0.9664099275695942427 ∧
      3.3935247190 < Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) < 3.3935247191 ∧
      (∀ i x, L.dc i x = 1 - (((torus 1 0 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (torus 1 0 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (torus 1 0 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (torus 1 0 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) :=
  face_lifetime (torus 1 0 3) Torus103Data.data Torus103Data.tab sdens cells hA u nxt dist uok reach _ _ _ _
    (fun μ lam hq hl => torus103_tau μ lam hq hl)

end Gump.Link.Torus103
