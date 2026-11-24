"""Writes GumpMath/Link<Face>Sym.lean: the table automorphisms (all, by backtracking), one sending each class
representative to each cell, their symOK checks and <face>_prices.

  python3 research/blast/lean/link_gen_sym.py          (LINK_OUT=dir to write elsewhere)"""
import sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'
SRC = os.path.join(HERE, 'mathlib', 'GumpMath') + '/'
from link_reach import tables
from collections import Counter
def autos(G, C):
    A = len(G); res = []
    def ok_partial(s, i):
        # check constraints involving cells < len(s) fully assigned
        return True
    def bt(s, used):
        k = len(s)
        if k == A:
            if all(Counter(G[s[i]]) == Counter(s[j] for j in G[i]) and C[s[i]] == C[i] for i in range(A)):
                res.append(list(s))
            return
        for v in range(A):
            if v in used or C[v] != C[k] or len(G[v]) != len(G[k]): continue
            s.append(v); used.add(v)
            good = True
            for i in range(k + 1):
                if all(j < k + 1 for j in G[i]):
                    if Counter(G[s[i]]) != Counter(s[j] for j in G[i]): good = False; break
            if good: bt(s, used)
            s.pop(); used.discard(v)
    bt([], set())
    return res
FACES = [('DiceHull3', '(hull 3)', 'Hull3Data', 'Hull3', 'hull3'), ('DiceTorus103', '(torus 1 0 3)', 'Torus103Data', 'Torus103', 'torus103'),
         ('DiceTorus113', '(torus 1 1 3)', 'Torus113Data', 'Torus113', 'torus113'), ('DiceStrip13', '(strip 1 3)', 'Strip13Data', 'Strip13', 'strip13'),
         ('DicePatch13', '(patch 1 3)', 'Patch13Data', 'Patch13', 'patch13')]
for mod, F, ns, name, low in FACES:
    G, C = tables(mod); A = len(G)
    au = autos(G, C)
    # orbits and, for each cell, an automorphism sending the orbit's representative to it
    cls = [None] * A; rep = []; via = {}
    for i in range(A):
        if cls[i] is not None: continue
        r = i; c = len(rep); rep.append(r)
        for s in au:
            j = s[r]
            if cls[j] is None: cls[j] = c; via[j] = s
    used = []
    for j in range(A):
        s = via[j]
        if j != rep[cls[j]] and s not in used: used.append(s)
    print(name, 'automorphisms', len(au), 'orbits', [[j for j in range(A) if cls[j] == c] for c in range(len(rep))], 'sigmas used', len(used))
    lines = [f'''/-
Equal prices within the symmetry classes of the face `{F}` ({len(au)} table automorphisms, found by the chain agent's
generator; each one used is checked by the kernel, `Data.symOK`, `decide +kernel`).  Classes of cells:
{[[j for j in range(A) if cls[j] == c] for c in range(len(rep))]}.
-/
import GumpMath.Link{name}
import GumpMath.LinkSym

set_option maxRecDepth 100000

namespace Gump.Link.{name}
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The class of each cell. -/
def cls : List ℕ := {cls}
''']
    for k, s in enumerate(used):
        lines.append(f'def σ{k} : List ℕ := {s}\n')
        lines.append(f'theorem sym{k} : {ns}.data.symOK {F}.A σ{k} (Tree.build {F}.A (act σ{k}) 0) = true := by decide +kernel\n')
    lines.append(f'''theorem hA9 : {F}.A = {A} := by decide +kernel

section
variable {{μ : {{x : Fin (2 ^ {F}.A) // x ≠ {F}.empty}} → ℝ}} {{lam : ℝ}}
  (hμ : (chain {F} sdens.dens).IsQSD μ lam) (hlam : 0 < lam)
  (huniq : ∀ ν lam', (chain {F} sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
include hμ hlam huniq
''')
    for j in range(A):
        r = rep[cls[j]]
        if j == r:
            lines.append(f'theorem price{j} (h{j} : {j} < {F}.A) (h{r}r : {r} < {F}.A) : L.price μ ⟨{j}, h{j}⟩ = L.price μ ⟨{r}, h{r}r⟩ := rfl\n')
        else:
            k = used.index(via[j])
            lines.append(f'''theorem price{j} (h{j} : {j} < {F}.A) (h{r}r : {r} < {F}.A) : L.price μ ⟨{j}, h{j}⟩ = L.price μ ⟨{r}, h{r}r⟩ := by
  have := price_sym {F} {ns}.data {ns}.tab sym{k} sdens {ns}.hρ1 {ns}.hρ2 (cellsOK_of_tab {F} {ns}.data {ns}.tab cells) hμ hlam huniq ⟨{r}, h{r}r⟩
  have e : cellPerm {F} {ns}.data sym{k} ⟨{r}, h{r}r⟩ = ⟨{j}, h{j}⟩ := Fin.ext (show σ{k}.getD {r} 0 = {j} by decide)
  rw [e] at this; exact this
''')
    cases = '\n'.join(f'    · exact (price{j} hμ hlam huniq _ (by rw [hA9]; norm_num)).trans (price{j2} hμ hlam huniq _ _).symm' for j, j2 in [])
    lines.append(f'''
/-- The representative of each class. -/
def rep : List ℕ := {[rep[cls[j]] for j in range(A)]}

theorem price_rep (i : Fin {F}.A) :
    ∃ h : rep.getD i 0 < {F}.A, L.price μ i = L.price μ ⟨rep.getD i 0, h⟩ := by
  rcases i with ⟨i, hi⟩
  have hi2 : i < {A} := lt_of_lt_of_eq hi hA9
  interval_cases i
''')
    for j in range(A):
        r = rep[cls[j]]
        lines.append(f'  · exact ⟨lt_of_lt_of_eq (show rep.getD {j} 0 < {A} by decide) hA9.symm, price{j} hμ hlam huniq hi (lt_of_lt_of_eq (show {r} < {A} by decide) hA9.symm)⟩\n')
    lines.append(f'''
/-- **Equal prices within each symmetry class**: c_i = c_j whenever i and j are in the same class. -/
theorem {low}_prices (i j : Fin {F}.A) (hij : cls.getD i 0 = cls.getD j 0) : L.price μ i = L.price μ j := by
  obtain ⟨hi, ei⟩ := price_rep hμ hlam huniq i
  obtain ⟨hj, ej⟩ := price_rep hμ hlam huniq j
  have hr : rep.getD i 0 = rep.getD j 0 := by
    have hi2 : (i : ℕ) < {A} := lt_of_lt_of_eq i.2 hA9
    have hj2 : (j : ℕ) < {A} := lt_of_lt_of_eq j.2 hA9
    generalize (i : ℕ) = a at hi2 hij ⊢
    generalize (j : ℕ) = b at hj2 hij ⊢
    revert hij
    interval_cases a <;> interval_cases b <;> decide
  rw [ei, ej]
  congr 1
  exact Fin.ext hr

end
end Gump.Link.{name}
''')
    open(D + f'Link{name}Sym.lean', 'w').write(''.join(lines))
