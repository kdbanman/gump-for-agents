"""Writes GumpMath/Link<Face>.lean for the five certified 9-cell faces (certificate u, nxt, dist and <face>_link).

  python3 research/blast/lean/link_gen_faces.py        (LINK_OUT=dir to write elsewhere)"""
import sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'
SRC = os.path.join(HERE, 'mathlib', 'GumpMath') + '/'
from link_reach import cert
# (Dice module, Lean face term, namespace of data, tau theorem, needs lam>0, lo, hi, a, b, Link name)
FACES = [
 ('DiceHull3', '(hull 3)', 'Hull3Data', 'hull3_tau', False, '0.9165673655948901373', '0.9165673655948901374', '2.4837157463', '2.4837157464', 'Hull3'),
 ('DiceTorus103', '(torus 1 0 3)', 'Torus103Data', 'torus103_tau', True, '0.9664099275695942426', '0.9664099275695942427', '3.3935247190', '3.3935247191', 'Torus103'),
 ('DiceTorus113', '(torus 1 1 3)', 'Torus113Data', 'torus113_tau', True, '0.9324323935928482210', '0.9324323935928482211', '2.6946266059', '2.6946266060', 'Torus113'),
 ('DiceStrip13', '(strip 1 3)', 'Strip13Data', 'strip13_tau', False, '0.9391216736592712685', '0.9391216736592712686', '2.7988780569', '2.7988780570', 'Strip13'),
 ('DicePatch13', '(patch 1 3)', 'Patch13Data', 'patch13_tau', False, '0.8474738060566295030', '0.8474738060566295031', '1.8804189341', '1.8804189342', 'Patch13'),
]
for mod, F, ns, tau, pos, lo, hi, a, b, name in FACES:
    _, r = cert(mod)
    low = name[0].lower() + name[1:]
    taucall = f'fun μ lam hq hl => {tau} μ lam hq hl' if pos else f'fun μ lam hq _ => {tau} μ lam hq'
    txt = f'''/-
The lifetime of the face `{F}` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42), as one self-contained
theorem about `Gump.Dice.Face.P` (written by the chain agent's generator from the dice agent's tables
`GumpMath/{mod}Data.lean`; every check below is run by the kernel, `decide +kernel`).

The reachability certificate: u = {r['u']} (every cell can be alive next), and for each of the {r['nsurv']} states that
can survive a possible next state (`nxt`) one step closer to u (`dist`, at most {r['maxdist']}).
-/
import GumpMath.LinkUnique
import GumpMath.{mod}

set_option maxRecDepth 100000

namespace Gump.Link.{name}
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The state from which every state can be reached in one step. -/
def u : ℕ := {r['u']}
/-- A possible next state, one step closer to u. -/
def nxt : List ℕ := {r['nxt']}
/-- The number of steps to u. -/
def dist : List ℕ := {r['dist']}

theorem cells : cellsD {ns}.data {F}.A = true := by decide +kernel
theorem uok : uOK {ns}.data {F}.A u = true := by decide +kernel
theorem reach : reachOK {ns}.data {F}.A u nxt dist = true := by decide +kernel
theorem hA : 0 < {F}.A := by decide +kernel

theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath {F} sdens (cellsOK_of_tab {F} {ns}.data {ns}.tab cells)

/-- **The lifetime of the face `{F}`.**  Its killed chain (`Face.P` itself, killed at the empty face) has a
quasi-stationary law (the dominant one), unique among those with λ > 0 and charging every living state; it is the
dice agent's `IsQSD`; {lo} ≤ λ ≤ {hi} and {a} < ln τ < {b} (τ = E_μ T); ln τ = Σ_i c_i with c_i the tilt price of
cell i's own death probability; and survival from every state that can survive decays at exactly the rate λ. -/
theorem {low}_link :
    ∃ μ lam, (chain {F} sdens.dens).IsDominantQSD μ lam ∧ IsQSD {F} ρ1 ρ2 (extend {F} μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain {F} sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      ({lo} : ℝ) ≤ lam ∧ lam ≤ {hi} ∧
      {a} < Real.log ((chain {F} sdens.dens).lifetime μ) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) < {b} ∧
      (∀ i x, L.dc i x = 1 - (({F}.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain {F} sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain {F} sdens.dens).survFrom t x) ∧
        (∀ t x, (chain {F} sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) :=
  face_lifetime {F} {ns}.data {ns}.tab sdens cells hA u nxt dist uok reach _ _ _ _
    ({taucall})

end Gump.Link.{name}
'''
    open(D + f'Link{name}.lean', 'w').write(txt)
    print('wrote', f'Link{name}.lean')
