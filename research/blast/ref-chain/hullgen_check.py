#!/usr/bin/env python3
"""ref-chain (fifth review): the construction of LinkHullGen.lean's `hull_lemma0`, simulated as supports on my
oracle-built hull faces (link_numbers.py), and LinkHullSym's maps against LinkHullCert's per-R lists.

  python3 research/blast/ref-chain/hullgen_check.py        (a few seconds)

A step x -> y is possible iff y is non-empty and every live cell of y can be alive next from x (some coin outcome puts
k + heads in B45/S345's window).  Definitions copied from LinkHullGen.lean: T = cells with z even and not a corner;
stuck q = (x odd and y = 0) or (y odd and x = 0 and z != R-1); phi = 3(R-1-z) + [stuck]; c0 = (0,1,R-1);
G n = T and phi <= n; Zp = {(R-1,0,1), (0,R-1,1)}; U = z even (u = mask U).
Checked: every cell of U can be alive next from u ... every cell can (aliveF_u); every T cell but c0 has a T neighbour
of smaller phi and the singleton step to it is possible (descent, walk_step); every non-T cell has a T neighbour with
a possible singleton step (enterT); G 0 = {c0}; G n -> G n+1 possible for n < 3R and G 3R = T (grow); T -> T u Zp
-> U possible (step_TZ, step_U).  Negative controls: skipping the Zp step (T -> U directly), and a growth that skips
a level, must fail somewhere.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_numbers import face, tables
from oracle import BIRTH, SURVIVE

def rule(s, n): return (n in SURVIVE) if s else (n in BIRTH)

def check(R):
    cells, red, coin = face('hull', R)
    nb, m1, m2 = tables(cells, red, coin)
    A = len(cells); idx = {p: i for i, p in enumerate(cells)}
    def alive(xset, i):
        k = sum(1 for j in nb[i] if j in xset)
        return any(rule(i in xset, k + a + b) for a in range(m1[i] + 1) for b in range(m2[i] + 1))
    def step(x, y): return bool(y) and all(alive(x, i) for i in y)
    corner = lambda p: (p[1] == 0 and p[2] == 0) or (p[0] == 0 and p[2] == 0) or (p[0] == 0 and p[1] == 0)
    T = lambda p: p[2] % 2 == 0 and not corner(p)
    stuck = lambda p: (p[0] % 2 == 1 and p[1] == 0) or (p[1] % 2 == 1 and p[0] == 0 and p[2] != R - 1)
    phi = lambda p: 3 * (R - 1 - p[2]) + (1 if stuck(p) else 0)
    c0 = (0, 1, R - 1)
    S = lambda pred: frozenset(i for i, p in enumerate(cells) if pred(p))
    u = S(lambda p: p[2] % 2 == 0)
    res = {}
    res['u_all_alive'] = all(alive(u, i) for i in range(A))
    res['u_mask'] = sum(1 << i for i in u)
    # walks of singletons to c0
    ok_walk = True; maxlen = 0
    for i, p in enumerate(cells):
        cur = p; steps = 0
        if not T(cur):
            nxt = [cells[j] for j in nb[i] if T(cells[j]) and step({i}, {j})]
            if not nxt: ok_walk = False; continue
            cur = nxt[0]; steps += 1
        while cur != c0:
            ci = idx[cur]
            nxt = [cells[j] for j in nb[ci] if T(cells[j]) and phi(cells[j]) < phi(cur) and step({ci}, {j})]
            if not nxt: ok_walk = False; break
            cur = nxt[0]; steps += 1
        maxlen = max(maxlen, steps)
    res['walks_to_c0'] = ok_walk; res['longest_walk'] = maxlen
    G = lambda n: S(lambda p: T(p) and phi(p) <= n)
    res['G0_is_c0'] = G(0) == frozenset({idx[c0]})
    res['grow_steps'] = all(step(G(n), G(n + 1)) for n in range(3 * R))
    res['G3R_is_T'] = G(3 * R) == S(T)
    TZ = S(lambda p: T(p) or p in ((R - 1, 0, 1), (0, R - 1, 1)))
    res['T_to_TZ'] = step(S(T), TZ); res['TZ_to_U'] = step(TZ, u)
    res['neg_T_to_U'] = step(S(T), u)
    res['neg_skip_level'] = all(step(G(n), G(n + 2)) for n in range(0, 3 * R, 2))
    return res, cells

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lean', 'mathlib', 'GumpMath', 'LinkHullCert.lean')).read()
lists = {(int(m.group(1)), m.group(2)): eval(m.group(3)) for m in
         re.finditer(r"theorem hull(\d+)_(rot|refl) : autOK \(Gump\.Dice\.hull \d+\) (\[[^\]]*\]) = true", src)}
for R in (3, 5, 7, 9, 11, 13):
    res, cells = check(R)
    idx = {p: i for i, p in enumerate(cells)}
    rot = [idx[(p[1], p[2], p[0])] for p in cells]; refl = [idx[(p[1], p[0], p[2])] for p in cells]
    same = lists.get((R, 'rot')) == rot and lists.get((R, 'refl')) == refl
    print(f"hull {R:2d} ({len(cells):3d} cells): {res};  gList rot/refl = LinkHullCert's lists: {same}")
