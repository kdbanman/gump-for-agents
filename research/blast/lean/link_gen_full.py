"""Writes GumpMath/LinkFaces.lean: <face>_full, the conjunction of <face>_link and <face>_prices.

  python3 research/blast/lean/link_gen_full.py         (LINK_OUT=dir to write elsewhere)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'
SRC = os.path.join(HERE, 'mathlib', 'GumpMath') + '/'
FACES = [('Hull3','hull3','(hull 3)','0.9165673655948901373','0.9165673655948901374','2.4837157463','2.4837157464'),
 ('Torus103','torus103','(torus 1 0 3)','0.9664099275695942426','0.9664099275695942427','3.3935247190','3.3935247191'),
 ('Torus113','torus113','(torus 1 1 3)','0.9324323935928482210','0.9324323935928482211','2.6946266059','2.6946266060'),
 ('Strip13','strip13','(strip 1 3)','0.9391216736592712685','0.9391216736592712686','2.7988780569','2.7988780570'),
 ('Patch13','patch13','(patch 1 3)','0.8474738060566295030','0.8474738060566295031','1.8804189341','1.8804189342')]
out = ['''/-
One self-contained lifetime theorem per face certified by the dice agent, about `Gump.Dice.Face.P` itself at
(ρ1, ρ2) = (0.44, 0.42) (`<face>_full`): the quasi-stationary law exists, is unique among λ > 0 and charges every
living state; λ and ln τ lie in the certified intervals; survival from every state that can survive decays at
exactly the rate λ; ln τ is the sum of the per-cell prices of the cells' own death probabilities; and those prices
are equal within each class of the face's table symmetries.
-/
''']
out += [f'import GumpMath.Link{n}Sym\n' for n, *_ in FACES]
out.append('\nnamespace Gump.Link\nopen Gump.Dice Gump.Chain Gump.Chain.KilledChain\n')
for n, l, F, lo, hi, a, b in FACES:
    out.append(f'''
namespace {n}

/-- **The lifetime of the face `{F}`**, everything named, nothing existential but the law itself. -/
theorem {l}_full :
    ∃ μ lam, (chain {F} sdens.dens).IsDominantQSD μ lam ∧ IsQSD {F} ρ1 ρ2 (extend {F} μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain {F} sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      ({lo} : ℝ) ≤ lam ∧ lam ≤ {hi} ∧
      {a} < Real.log ((chain {F} sdens.dens).lifetime μ) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) < {b} ∧
      (∀ i x, L.dc i x = 1 - (({F}.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin {F}.A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain {F} sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain {F} sdens.dens).survFrom t x) ∧
        (∀ t x, (chain {F} sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr, hdec⟩ := {l}_link
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, h1, h2, h3, h4, hdc, hpr,
    fun i j h => {l}_prices hD.qsd hlam huniq i j h, hdec⟩

end {n}
''')
out.append('\nend Gump.Link\n')
open(D + 'LinkFaces.lean', 'w').write(''.join(out))
