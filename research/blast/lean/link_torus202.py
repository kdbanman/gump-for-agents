"""Writes GumpMath/LinkTorus202.lean (the 12-cell torus (2,0),(0,2)): the certificate (u, nxt, dist as trees of
depth 12), 3 generating table automorphisms with a spanning tree of the cells, and torus202_full.  The tables G
and T are those printed by `#eval` of (torus 2 0 2).nb, .m1/.m2 and aliveNum (checked in Lean by Torus202.tab).

  python3 research/blast/lean/link_torus202.py          (LINK_OUT=dir to write elsewhere)"""
import sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'
SRC = os.path.join(HERE, 'mathlib', 'GumpMath') + '/'
from link_reach import alive
from collections import Counter
def autos(G, C):
    A = len(G); res = []
    cnt = [Counter(G[i]) for i in range(A)]
    def bt(s, used):
        k = len(s)
        if k == A:
            res.append(list(s)); return
        for v in range(A):
            if v in used or C[v] != C[k]: continue
            ok = all(cnt[i][k] == cnt[s[i]][v] and cnt[k][i] == cnt[v][s[i]] for i in range(k)) and cnt[k][k] == cnt[v][v]
            if not ok: continue
            s.append(v); used.add(v); bt(s, used); s.pop(); used.discard(v)
    bt([], set())
    return res
G = [[9, 9, 7, 1, 5, 2], [4, 4, 6, 0, 11, 2], [8, 8, 3, 0, 10, 1], [6, 6, 10, 4, 2, 5], [1, 1, 9, 3, 8, 5],
  [11, 11, 0, 3, 7, 4], [3, 3, 1, 7, 11, 8], [10, 10, 0, 6, 5, 8], [2, 2, 9, 6, 4, 7], [0, 0, 4, 10, 8, 11],
  [7, 7, 3, 9, 2, 11], [5, 5, 6, 9, 1, 10]]
C = [[2, 1]] * 12
A = 12; N = 1 << A
M = [sum(1 << i for i in range(A) if alive(G, C, x, i)) for x in range(N)]
u = [x for x in range(1, N) if M[x] == N - 1][0]
surv = [x for x in range(1, N) if M[x] != 0]
dist = {u: 0}; nxt = {}; frontier = [u]; d = 0
while frontier:
    d += 1; new = []
    for x in surv:
        if x in dist: continue
        for y in frontier:
            if y & ~M[x] == 0:
                dist[x] = d; nxt[x] = y; new.append(x); break
    frontier = new
print('u', u, 'surv', len(surv), 'missing', len([x for x in surv if x not in dist]), 'maxdist', d - 1, 'die', [x for x in range(1, N) if M[x] == 0])
au = autos(G, C)
print('autos', len(au))
# small generating set acting transitively on cells, BFS tree
gens = []
reached = {0}; parent = {}
for s in au:
    new = {s[j] for j in reached} - reached
    if new or len(gens) == 0:
        pass
# greedy: pick automorphisms that enlarge the orbit of 0 under the generated group
def orbit(gs):
    o = {0}; fr = [0]
    while fr:
        j = fr.pop()
        for g in gs:
            if g[j] not in o: o.add(g[j]); fr.append(g[j])
    return o
for s in au:
    if len(orbit(gens + [s])) > len(orbit(gens)): gens.append(s)
    if len(orbit(gens)) == A: break
# BFS tree
par = {0: None}; fr = [0]
while fr:
    j = fr.pop(0)
    for k, g in enumerate(gens):
        if g[j] not in par: par[g[j]] = (j, k); fr.append(g[j])
print('gens', gens, 'tree', par)
def tree(vals):
    if len(vals) == 1: return str(vals[0])
    h = len(vals) // 2
    return "(.node %s %s)" % (tree(vals[:h]), tree(vals[h:]))
def treeL(vals):
    if len(vals) == 1: return "(.leaf %d)" % vals[0]
    h = len(vals) // 2
    return "(.node %s %s)" % (treeL(vals[:h]), treeL(vals[h:]))
import json
J = dict(u=u, nxt=[nxt.get(x, 0) for x in range(N)], dist=[dist.get(x, 0) for x in range(N)], gens=gens, par={str(k): v for k, v in par.items()}, G=G)
J = json.loads(json.dumps(J))

T = [[0, 2541, 2541, 12518, 12518, 25566, 23025, 28709, 18732, 18732, 5684, 5684, 0, 0]] * 12
def treeL(vals):
    if len(vals) == 1: return "(.leaf %d)" % vals[0]
    h = len(vals) // 2
    return "(.node %s %s)" % (treeL(vals[:h]), treeL(vals[h:]))
F = '(torus 2 0 2)'
par = {int(k): v for k, v in J['par'].items()}
L = [f'''/-
The 12-cell torus (2,0),(0,2) of the one-layer dice surrogate (`rigour/data/exact.csv`: ln τ = 3.9818365883), for
`Gump.Dice.Face.P` itself at (0.44, 0.42).  The dice agent's certificate for this face was not built (its notes,
section 4), so there is no certified interval for λ here; what is proved: the quasi-stationary law exists, is
unique among λ > 0 and charges every living state; survival from every state that can survive decays at exactly
its rate; all twelve cells have the same price c, so ln τ = 12 c; and ln τ < 1.9228 · 12 (the dice agent's
`lntau_le_regular`, the face being regular by its `regular_torus202`).

The tables are written here (`data`, checked against `Face.nb`, `Face.m1/m2` and `aliveNum` by the kernel,
`Data.tabOK`); the reachability certificate: u = {J['u']}, every one of the 4,094 states that can survive is
at most 2 steps from u (only the full face, 4095, dies surely); `nxt`, `dist` as trees of depth 12.  Prices: 3 of
the 48 table automorphisms (`Data.symOK`), acting transitively on the cells.
-/
import GumpMath.LinkNoCert
import GumpMath.LinkSym
import GumpMath.DiceBound2

set_option maxRecDepth 100000

namespace Gump.Link.Torus202
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The tables of the face (written by the chain agent from `#eval` of `Face.nb`, `Face.m1/m2`, `aliveNum`;
checked by `tab`). -/
def data : Data where
  n1 := 11
  d1 := 25
  n2 := 21
  d2 := 50
  G := {J['G']}
  C := {[(2, 1)] * 12}
  T := {T}

theorem tab : data.tabOK {F} = true := by decide +kernel
theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]
theorem hA12 : {F}.A = 12 := by decide +kernel
theorem hA : 0 < {F}.A := by rw [hA12]; norm_num
theorem hcoin : ∀ q, {F}.coin q = true := fun _ => rfl
theorem sdens : SDens ρ1 ρ2 := ⟨by norm_num [ρ1], by norm_num [ρ1], by norm_num [ρ2], by norm_num [ρ2]⟩
theorem hcells : CellsOK {F} := cellsOK_of_allcoins {F} hcoin

def u : ℕ := {J['u']}
def nxtT : Tree := {treeL(J['nxt'])}
def distT : Tree := {treeL(J['dist'])}

theorem uok : uOK data {F}.A u = true := by decide +kernel
theorem reach : reachOKF data {F}.A u (nxtT.get 12) (distT.get 12) = true := by decide +kernel

/-- The local death factors: each cell's own death probability. -/
noncomputable abbrev L := localDeath {F} sdens hcells
''']
for k, g in enumerate(J['gens']):
    L.append(f'def σ{k} : List ℕ := {g}\n')
    L.append(f'theorem sym{k} : data.symOK {F}.A σ{k} (Tree.build {F}.A (act σ{k}) 0) = true := by decide +kernel\n')
L.append(f'''
section
variable {{μ : {{x : Fin (2 ^ {F}.A) // x ≠ {F}.empty}} → ℝ}} {{lam : ℝ}}
  (hμ : (chain {F} sdens.dens).IsQSD μ lam) (hlam : 0 < lam)
  (huniq : ∀ ν lam', (chain {F} sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
include hμ hlam huniq

/-- cell j's price equals its parent's in the spanning tree of the generators. -/
''')
order = sorted(par, key=lambda j: 0)
# emit in BFS order so parents come first
bfs = [0]; seen = {0}
while len(bfs) < 12:
    for j, v in par.items():
        if v is not None and v[0] in seen and j not in seen: bfs.append(j); seen.add(j)
for j in bfs:
    if par[j] is None:
        L.append(f'theorem price{j} (h : {j} < {F}.A) (h0 : 0 < {F}.A) : L.price μ ⟨{j}, h⟩ = L.price μ ⟨0, h0⟩ := rfl\n')
    else:
        p, k = par[j]
        L.append(f'''theorem price{j} (h : {j} < {F}.A) (h0 : 0 < {F}.A) : L.price μ ⟨{j}, h⟩ = L.price μ ⟨0, h0⟩ := by
  have hp : {p} < {F}.A := by rw [hA12]; norm_num
  have s := price_sym {F} data tab sym{k} sdens hρ1 hρ2 hcells hμ hlam huniq ⟨{p}, hp⟩
  have e : cellPerm {F} data sym{k} ⟨{p}, hp⟩ = ⟨{j}, h⟩ := Fin.ext (show σ{k}.getD {p} 0 = {j} by decide)
  rw [e] at s
  exact s.trans (price{p} hμ hlam huniq hp h0)
''')
L.append(f'''
theorem price_all (i : Fin {F}.A) : L.price μ i = L.price μ ⟨0, hA⟩ := by
  rcases i with ⟨i, hi⟩
  have hi2 : i < 12 := lt_of_lt_of_eq hi hA12
  interval_cases i
''')
for j in range(12):
    L.append(f'  · exact price{j} hμ hlam huniq hi hA\n')
L.append(f'''
end

/-- **The 12-cell torus (2,0),(0,2)**: unique quasi-stationary law of `Face.P`, positive on every living state,
one price for all twelve cells, ln τ = 12 c, ln τ < 1.9228 · 12, and the decay rate from every start. -/
theorem torus202_full :
    ∃ μ lam, (chain {F} sdens.dens).IsDominantQSD μ lam ∧ IsQSD {F} ρ1 ρ2 (extend {F} μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain {F} sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, L.dc i x = 1 - (({F}.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin {F}.A, L.price μ i = L.price μ j) ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) = 12 * L.price μ ⟨0, hA⟩ ∧
      Real.log ((chain {F} sdens.dens).lifetime μ) < 1.9228 * 12 ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain {F} sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain {F} sdens.dens).survFrom t x) ∧
        (∀ t x, (chain {F} sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, hdec⟩ :=
    face_unique {F} data tab sdens hcells hA u (nxtT.get 12) (distT.get 12) uok reach
  have hall := price_all hD.qsd hlam huniq
  have h12 : Real.log ((chain {F} sdens.dens).lifetime μ) = 12 * L.price μ ⟨0, hA⟩ := by
    rw [hpr, Finset.sum_congr rfl (fun i _ => hall i), Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul]
    rw [show (({F}.A : ℕ) : ℝ) = 12 by exact_mod_cast hA12]
  have hreg := lntau_le_regular {F} hcoin regular_torus202 (extend {F} μ) lam hdice hA
  have hlog := log_lifetime_eq L hD.qsd
  rw [hA12] at hreg
  refine ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, fun i j => (hall i).trans (hall j).symm, h12,
    by rw [hlog]; exact_mod_cast hreg, hdec⟩

end Gump.Link.Torus202
''')
open(D + 'LinkTorus202.lean', 'w').write(''.join(L))
print('ok')
