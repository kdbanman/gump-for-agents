#!/usr/bin/env python3
"""validate.py: the orbit-graph stepper (geom.py + sy.c) against the Rust engine, bit-exact.

For each SPEC: a random state on the orbit graph (one draw per node, density 0.4) is stepped T generations by
`sy trace`; the same state, expanded to the full symmetric cell set, is stepped by `gump run` (a slab torus is
replicated periodically on a cubic N-torus with N.u1, N.u2 in the period lattice and N >= 11, so that at least
three dead layers separate the slab from its image; a vessel runs in open space). Compared: the population at
every generation 1..T (engine population = copies x sy population) and the final cell set.

    python3 research/theory/symmetric/validate.py [T] [SPEC ...]      # default T = 1500, default list below
"""
import os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'symmetric')
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
SY = os.path.join(SCR, 'sy')
sys.path.insert(0, HERE)
import geom

DEFAULT = ['rect_4_2_c1', 'gen_2_2_8_c1', 'hex_4_0_c1', 'rect_8_2_cs', 'rect_6_3_cs', 'cent_6_6_cs', 'cent_4_8_cs',
           'hex_7_0_c3', 'hex_7_0_c3_o2', 'hex_7_0_c3_o4', 'hex_5_2_c3', 'hex_4_4_c3', 'hex_8_0_c3v', 'hex_9_0_c3v_o2',
           'hex_10_0_c3v_o4', 'hex_6_6_c3v', 'oct_9_c_c1', 'oct_10_v_c1', 'oct_11_c_d2h', 'oct_12_v_d2h', 'oct_23_c_td',
           'oct_24_v_td', 'oct_23_c_oh', 'oct_24_v_oh', 'oct_15_c_c3v', 'oct_16_v_th']


def build_sy():
    os.makedirs(SCR, exist_ok=True)
    src = os.path.join(HERE, 'sy.c')
    if not os.path.exists(SY) or os.path.getmtime(SY) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', SY, src])


def torus_N(f):
    A, K, B = geom.hnf2(f.g1, f.g2)
    def inlat(v):
        x, y = int(v[0]), int(v[1])
        return x % A == 0 and (y - (x // A) * K) % B == 0
    N = 11
    while not (inlat(N * geom.U1) and inlat(N * geom.U2)):
        N += 1
    return N


def expand(q, state, N=None):
    """full cell list of the symmetric state; on a cubic N-torus if N (slab), else open space (vessel)."""
    f = q.f; live = state[q.orb]
    if N is None:
        return f.cells[live]
    r = np.arange(2 * N)
    g = np.stack(np.meshgrid(r, r, r, indexing='ij'), -1).reshape(-1, 3)
    g = g[(g % 2).sum(1) == 1]
    s0 = g.sum(1) % (2 * N)
    g = g[(s0 >= 1) & (s0 <= 2 * geom.M_SLAB - 1)]
    out = []
    for p in g:
        k = (int(p.sum()) - int(p.sum()) % (2 * N)) // (2 * N)
        lift = (int(p[0]), int(p[1]), int(p[2]) - 2 * N * k)
        if live[f.index[f.canon(lift)]]:
            out.append(p)
    return np.array(out).reshape(-1, 3)


def check(spec, T, rng):
    q = geom.build(spec); f = q.f
    N = torus_N(f) if f.kind == 'slab' else None
    for attempt in range(40):
        state = rng.random(q.n) < 0.4
        with tempfile.TemporaryDirectory(dir=SCR) as d:
            gf, init = os.path.join(d, 'g.txt'), os.path.join(d, 'init.txt')
            geom.write_graph(q, gf)
            open(init, 'w').write(' '.join(str(i) for i in np.nonzero(state)[0]) + '\n')
            out = subprocess.run([SY, gf, 'trace', init, str(T)], capture_output=True, text=True, check=True).stdout.splitlines()
            pops = np.array([int(l.split()[1]) for l in out[:T + 1]])
            fin = np.zeros(q.n, bool); fin[[int(x) for x in out[T + 1].split()[1:]]] = True
            if pops[-1] == 0 or (pops[-1] == pops[-3] and attempt < 39):
                continue                              # want a state that is still changing at T: retry another soup
            cells0 = expand(q, state, N)
            cf, pl, co = os.path.join(d, 'c.txt'), os.path.join(d, 'pop.txt'), os.path.join(d, 'out.txt')
            np.savetxt(cf, cells0, fmt='%d')
            args = [GUMP, 'run', '--cells', cf, '--gens', str(T), '--no-halt', '--poplog', pl, '--cells-out', co]
            if N:
                args += ['--torus', str(N)]
            subprocess.run(args, capture_output=True, text=True, check=True)
            ep = np.loadtxt(pl, dtype=np.int64, ndmin=2)
            eg = {int(a): int(b) for a, b in ep}
            copies = (N * N * 3 // f.area) if N else 1
            bad = [g for g in range(1, T + 1) if eg.get(g) != copies * pops[g]]
            ec = np.loadtxt(co, dtype=np.int64, comments='#', ndmin=2).reshape(-1, 3)
            mine = expand(q, fin, N)
            if N:
                ec = ec % (2 * N); mine = mine % (2 * N)
            same = set(map(tuple, ec.tolist())) == set(map(tuple, mine.tolist()))
            ok = (not bad) and same
            print(f'{"OK  " if ok else "FAIL"} {spec:18s} order {q.order:3d} nodes {q.n:5d} cells {len(f.cells):6d} '
                  f'{"torus " + str(N) + " x" + str(copies) if N else "open space"}  T {T}  pop(T) {pops[-1]} (x{copies})'
                  f'{"" if not bad else "  first population mismatch at gen " + str(bad[0])}{"" if same else "  final cell sets differ"}', flush=True)
            return ok
    print('FAIL', spec, 'no surviving soup'); return False


if __name__ == '__main__':
    build_sy()
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    specs = sys.argv[2:] or DEFAULT
    rng = np.random.default_rng(20261115)
    res = [check(s, T, rng) for s in specs]
    print('ALL OK' if all(res) else 'SOME FAILED')
