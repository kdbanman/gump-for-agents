#!/usr/bin/env python3
"""Exact death rate of the one-layer model on a ring or on a segment with free ends (planner for sweep.c).

    python3 sweep.py ring b [rho16]        # ring of b sites (b <= 6: the working tensor has 3b + 10 bits)
    python3 sweep.py seg n [rho16]         # segment of n sites {Z_s, Y_s, X_{s+1}}, s = 0..n-1, cells outside held
                                           # dead (n <= 8: 3n + 5 bits)
    python3 sweep.py table                 # the filed table: rings 5..6, segments 2..8
    python3 sweep.py seq                   # steps of ln tau between successive exact segments, and their limit

Model and triples: exact1.py. Result: h = quasi-stationary probability that the face is empty one generation
later; ln tau = -ln h. Results are appended to data/exact.json.
"""
import json, math, os, subprocess, sys, time
import numpy as np
import thin, exact1

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'scratch', 'thin')
BIN = os.path.join(OUT, 'sweep')
DATA = os.path.join(HERE, 'data', 'exact.json')
SLOT = [(0, +1), (1, -1), (2, 0)]          # triple c = (X_{c+1}, Y_{c-1}, Z_c)


def build():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(HERE, 'sweep.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', BIN + '.new', src, '-lm'])
        os.replace(BIN + '.new', BIN)


def plan(kind, n, rho, path, P3=None):
    if kind == 'ring':
        mod = n; cells = {(o, c) for o in range(3) for c in range(n)}; trip = list(range(n))
        exact1.triples(n)                                    # asserts the coin-sharing structure
    else:
        mod = None; cells = {(2, s) for s in range(n)} | {(1, s) for s in range(n)} | {(0, s + 1) for s in range(n)}
        trip = list(range(n + 1))
    wrap = (lambda c: c % mod) if mod else (lambda c: c)
    members = [[(o, wrap(c + d)) if (o, wrap(c + d)) in cells else None for o, d in SLOT] for c in trip]
    assert sorted(x for mm in members for x in mm if x) == sorted(cells)
    nbrs = {cell: [(o2, wrap(cell[1] + dc)) for (dt, o2, dc) in thin.TAB[cell[0]] if dt == 0 and (o2, wrap(cell[1] + dc)) in cells]
            for cell in cells}
    assert all(len(set(v)) == len(v) and cell not in v for cell, v in nbrs.items())
    if P3 is None:
        P3 = exact1.triple_table(rho)
    var = [('old', x) for mm in members for x in mm if x]
    n0 = len(var); first = [v[1] for v in var]
    lines = []; nmax = n0
    for i, mm in enumerate(members):
        pos = {v: k for k, v in enumerate(var)}
        need = set()
        for later in members[i + 1:]:
            for x in later:
                if x:
                    need.add(x); need.update(nbrs[x])
        s = []; mk = []
        for x in mm:
            if x is None:
                s.append(-1); mk.append(0)
            else:
                s.append(pos[('old', x)]); mk.append(sum(1 << pos[('old', y)] for y in nbrs[x]))
        kept = [v for v in var if v[0] == 'new' or v[1] in need]
        keep = sum(1 << pos[v] for v in kept)
        present = [j for j, x in enumerate(mm) if x]
        m = len(present)
        # outcome table over the present cells (absent cells' outcomes summed out)
        T = np.zeros((2, 7, 2, 7, 2, 7, 1 << m))
        for y in range(8):
            o = sum(((y >> j) & 1) << r for r, j in enumerate(present))
            T[..., o] += P3[..., y]
        lines.append((len(var), keep, len(kept), m, s[0], mk[0], s[1], mk[1], s[2], mk[2], T.reshape(-1)))
        var = kept + [('new', mm[j]) for j in present]
        nmax = max(nmax, len(var))
    assert [v[0] for v in var] == ['new'] * n0 and [v[1] for v in var] == first
    with open(path, 'w') as f:
        f.write(f'{n0} {len(lines)}\n')
        for L in lines:
            f.write(' '.join(map(str, L[:10])) + '\n')
            f.write(' '.join(repr(float(x)) for x in L[10]) + '\n')
    return n0, nmax


def solve(kind, n, rho16=26112, tol=1e-11, quiet=False, P3=None, key=None):
    """P3, key: another kernel that is a product over the triples (pca.py), filed under `key`"""
    build()
    path = os.path.join(OUT, f'plan_{kind}_{n}_{os.getpid()}.txt')
    n0, nmax = plan(kind, n, rho16 / 65536, path, P3)
    t0 = time.time()
    out = subprocess.run([BIN, path, str(tol), '3000'], capture_output=True, text=True, check=True).stdout.splitlines()
    os.remove(path)
    r = out[-1].split(); assert r[0] == 'RESULT'
    h, lt, its = float(r[1]), float(r[2]), int(r[3])
    if not quiet:
        print(f'{kind} {n}: {n0} cells, working tensor 2^{nmax}, h = {h:.10g}, ln tau = {lt:.6f}  ({its} iterations, {time.time() - t0:.0f} s)', flush=True)
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    d = json.load(open(DATA)) if os.path.exists(DATA) else {}
    if key is None:
        d[f'{kind}_{n}_rho{rho16}'] = dict(kind=kind, n=n, rho16=rho16, h=h, lntau=lt, iterations=its, cells=n0)
    else:
        d[f'{key}_{kind}_{n}'] = dict(kind=kind, n=n, model=key, h=h, lntau=lt, iterations=its, cells=n0)
    json.dump(d, open(DATA, 'w'), indent=1, sort_keys=True)
    return h, lt


def seq(rho16=26112):
    """Steps s_n = ln tau_seg(n) - ln tau_seg(n-1); limit by Aitken's formula on the last three steps (exact if the
    steps approach their limit geometrically); the spread between the last step and that limit is the error offered."""
    d = json.load(open(DATA))
    a = {v['n']: v['lntau'] for v in d.values() if v['kind'] == 'seg' and v.get('rho16') == rho16}
    ns = sorted(a)
    print('  n   ln tau_seg (exact)   step      Aitken limit of the steps')
    steps = {}
    for n in ns:
        line = f'{n:3d}   {a[n]:.6f}'
        if n - 1 in a:
            steps[n] = a[n] - a[n - 1]; line += f'          {steps[n]:.4f}'
            if n - 2 in steps:
                s0, s1, s2 = steps[n - 2], steps[n - 1], steps[n]
                den = s2 - 2 * s1 + s0
                if abs(den) > 1e-12:
                    line += f'    {s2 - (s2 - s1) ** 2 / den:.4f}  (ratio of successive differences {(s2 - s1) / (s1 - s0):+.3f})'
        print(line)
    return a, steps


if __name__ == '__main__':
    if sys.argv[1] == 'seq':
        seq()
    elif sys.argv[1] == 'table':
        for b in (5, 6):
            solve('ring', b)
        for n in range(2, 9):
            solve('seg', n)
    else:
        solve(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 26112)
