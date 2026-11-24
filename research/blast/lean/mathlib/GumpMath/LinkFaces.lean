/-
One self-contained lifetime theorem per face certified by the dice agent, about `Gump.Dice.Face.P` itself at
(ρ1, ρ2) = (0.44, 0.42) (`<face>_full`): the quasi-stationary law exists, is unique among λ > 0 and charges every
living state; λ and ln τ lie in the certified intervals; survival from every state that can survive decays at
exactly the rate λ; ln τ is the sum of the per-cell prices of the cells' own death probabilities; and those prices
are equal within each class of the face's table symmetries.
-/
import GumpMath.LinkHull3Sym
import GumpMath.LinkTorus103Sym
import GumpMath.LinkTorus113Sym
import GumpMath.LinkStrip13Sym
import GumpMath.LinkPatch13Sym

namespace Gump.Link
open Gump.Dice Gump.Chain Gump.Chain.KilledChain

namespace Hull3

/-- **The lifetime of the face `(hull 3)`**, everything named, nothing existential but the law itself. -/
theorem hull3_full :
    ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
      2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧
      (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (hull 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := hull3_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => hull3_prices hD.qsd hlam huniq i j h, hdec⟩

end Hull3

namespace Torus103

/-- **The lifetime of the face `(torus 1 0 3)`**, everything named, nothing existential but the law itself. -/
theorem torus103_full :
    ∃ μ lam, (chain (torus 1 0 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 1 0 3) ρ1 ρ2 (extend (torus 1 0 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (torus 1 0 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9664099275695942426 : ℝ) ≤ lam ∧ lam ≤ 0.9664099275695942427 ∧
      3.3935247190 < Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) < 3.3935247191 ∧
      (∀ i x, L.dc i x = 1 - (((torus 1 0 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (torus 1 0 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (torus 1 0 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (torus 1 0 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (torus 1 0 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := torus103_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => torus103_prices hD.qsd hlam huniq i j h, hdec⟩

end Torus103

namespace Torus113

/-- **The lifetime of the face `(torus 1 1 3)`**, everything named, nothing existential but the law itself. -/
theorem torus113_full :
    ∃ μ lam, (chain (torus 1 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 1 1 3) ρ1 ρ2 (extend (torus 1 1 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (torus 1 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9324323935928482210 : ℝ) ≤ lam ∧ lam ≤ 0.9324323935928482211 ∧
      2.6946266059 < Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) < 2.6946266060 ∧
      (∀ i x, L.dc i x = 1 - (((torus 1 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (torus 1 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (torus 1 1 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (torus 1 1 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (torus 1 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := torus113_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => torus113_prices hD.qsd hlam huniq i j h, hdec⟩

end Torus113

namespace Strip13

/-- **The lifetime of the face `(strip 1 3)`**, everything named, nothing existential but the law itself. -/
theorem strip13_full :
    ∃ μ lam, (chain (strip 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (strip 1 3) ρ1 ρ2 (extend (strip 1 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (strip 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9391216736592712685 : ℝ) ≤ lam ∧ lam ≤ 0.9391216736592712686 ∧
      2.7988780569 < Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) < 2.7988780570 ∧
      (∀ i x, L.dc i x = 1 - (((strip 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (strip 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (strip 1 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (strip 1 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (strip 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := strip13_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => strip13_prices hD.qsd hlam huniq i j h, hdec⟩

end Strip13

namespace Patch13

/-- **The lifetime of the face `(patch 1 3)`**, everything named, nothing existential but the law itself. -/
theorem patch13_full :
    ∃ μ lam, (chain (patch 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (patch 1 3) ρ1 ρ2 (extend (patch 1 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (patch 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.8474738060566295030 : ℝ) ≤ lam ∧ lam ≤ 0.8474738060566295031 ∧
      1.8804189341 < Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) < 1.8804189342 ∧
      (∀ i x, L.dc i x = 1 - (((patch 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (patch 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (patch 1 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (patch 1 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (patch 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := patch13_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => patch13_prices hD.qsd hlam huniq i j h, hdec⟩

end Patch13

end Gump.Link
