#!/usr/bin/env python3
"""Is the kill 'every cluster of survivors fails on its own'?  (the PI's question of 04:15 UTC)

    python3 island.py NAME [THETA_MIN]   -> out/island_NAME.txt     (runs boom3 island on NAME.par first)

For every stored parent with P = p >= THETA_MIN A: one generation on (the bust), clusters of the live face cells
(connected through in-layer neighbours), then the same state run (a) untouched, (b) once per cluster with all other
cells of that face killed. Deterministic, so for one state each cluster either regrows the face (>= L cells) or not.
  d_nat(p)      share of parents whose untouched face is empty before it is >= L again        (the truth, = d(p))
  d_all(p)      share of parents in which every cluster fails on its own                      (clusters independent, same state)
  d_mf(p)       mean over parents of prod_clusters fail(size), fail(size) pooled over the parents with that p   (size only)
  d_an(p)       the same product with anatomy's table for islands over a *stationary* layer (fail = 0.86, 0.55, 0.22, 0.08, 0.02, 0.01)
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
nm = sys.argv[1]; thmin = float(sys.argv[2]) if len(sys.argv) > 2 else 0.66
sm = open(os.path.join(SCR, nm + '.sum')).read().split(); A = int(sm[5]); L = (A + 1) // 2
graph = [l for l in open(os.path.join(HERE, 'vessels.txt')) if l.split()[0] == nm][0].split()[1]
res = os.path.join(SCR, nm + '.island.txt')
subprocess.check_call([os.path.join(SCR, 'boom3'), os.path.join(SCR, graph + '.bin'), 'island', os.path.join(SCR, nm + '.par'), '48', '1', str(int(np.ceil(thmin * A))), str(A), res])
AN = [0.86, 0.55, 0.22, 0.08, 0.02]
rows = {}
for l in open(res):
    t = l.split(); p, q, U, ncl, o0 = int(t[2]), int(t[3]), int(t[4]), int(t[5]), int(t[6])
    cs = [tuple(map(int, x.split(':'))) for x in t[8:]]
    rows.setdefault(p, []).append((q, U, o0, cs))
out = []; w = out.append
w(f'{nm}: A {A}, L {L}; outcome 2 (undecided after 48 generations) is counted as a regrowth')
w('   p  theta parents |  after the bust: P/A   U/A  clusters  largest/P  singles |   d_nat      d_all      d_mf       d_an    | P(nat dies | all fail)  P(all fail | nat dies) | fail(size 1, 2, 3, 4-6, 7-12, >12) alone')
tot = np.zeros(4); js = {}
for p in sorted(rows):
    R = rows[p]; n = len(R)
    if n < 200: continue
    fs = {}; 
    for q, U, o0, cs in R:
        for s, o, t in cs: fs.setdefault(s, []).append(o == 0)
    fail = {s: np.mean(v) for s, v in fs.items()}
    dn = np.mean([o0 == 0 for q, U, o0, cs in R]); da = np.mean([all(o == 0 for s, o, t in cs) for q, U, o0, cs in R])
    dm = np.mean([np.prod([fail[s] for s, o, t in cs]) for q, U, o0, cs in R])
    dan = np.mean([np.prod([AN[s - 1] if s <= 5 else 0.01 for s, o, t in cs]) for q, U, o0, cs in R])
    both = sum(1 for q, U, o0, cs in R if o0 == 0 and all(o == 0 for s, o, t in cs)); na_ = sum(1 for q, U, o0, cs in R if all(o == 0 for s, o, t in cs)); nn = sum(1 for q, U, o0, cs in R if o0 == 0)
    js[p] = (n, dn, da, dm, dan)
    def pool(lo, hi):
        v = [x for s, vv in fs.items() if lo <= s <= hi for x in vv]; return f'{np.mean(v):.3f}' if len(v) >= 20 else '  -  '
    w(f' {p:3d} {p / A:.3f} {n:6d} |  {np.mean([r[0] for r in R]) / A:.3f} {np.mean([r[1] for r in R]) / A:.3f}   {np.mean([len(r[3]) for r in R]):5.2f}    {np.mean([max([c[0] for c in r[3]] + [0]) / max(r[0], 1) for r in R]):.3f}    {np.mean([sum(1 for c in r[3] if c[0] == 1) for r in R]):5.2f}'
      f' | {dn:.3e}  {da:.3e}  {dm:.3e}  {dan:.3e} |   {both / max(na_, 1):.3f} ({na_})            {both / max(nn, 1):.3f} ({nn})   | ' + ' '.join(pool(*x) for x in ((1, 1), (2, 2), (3, 3), (4, 6), (7, 12), (13, 999))))
# the dying parents: what their bust leaves, against the survivors' typical state at the same p
w('parents whose untouched face dies, against all parents of the same p: P/A after the bust, U/A, clusters, largest cluster / P')
for p in sorted(rows):
    R = rows[p]; D = [r for r in R if r[2] == 0]
    if len(D) < 30: continue
    f = lambda X: f'{np.mean([r[0] for r in X]) / A:.3f} {np.mean([r[1] for r in X]) / A:.3f} {np.mean([len(r[3]) for r in X]):5.2f} {np.mean([max([c[0] for c in r[3]] + [0]) / max(r[0], 1) for r in X]):.3f}'
    w(f' {p:3d} {p / A:.3f}  dying ({len(D):5d}): {f(D)}   all: {f(R)}')
import json; json.dump(dict(A=A, d=js), open(os.path.join(HERE, 'out', 'island_' + nm + '.json'), 'w'))
open(os.path.join(HERE, 'out', 'island_' + nm + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
