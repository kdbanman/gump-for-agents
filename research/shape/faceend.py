#!/usr/bin/env python3
"""Where a slab face dies: the dying face layer's last 64 states, for the first face death of each life.

Stepper: research/shape/rep_ring.c (rep.c's stepping code verbatim, plus a ring buffer of the two face layers).
`validate` checks it against rep.c (which tslab.py validate checks against the engine): the population trace of
replica 0 and every replica's final output line must be identical, for the same vessel and seed.

    python3 research/shape/faceend.py validate 4 3 6
    taskset -c 2 python3 research/shape/faceend.py run 4 0 6 CAP SEED W
    python3 research/shape/faceend.py analyze 4 0 6

A recorded death is the first generation at which either face layer is entirely dead (whatever happened before:
lives whose first event was a firewall are flagged, from rep's layer times at resolution 16, and left out of the
statistics). `analyze` prints, for generations -50 … 0 before the death: the mean number of live face cells, and
for the live cells a band statistic: R_n = |mean over live cells of exp(2 pi i n.c)| (c = the cell's coordinates
in the lattice basis, n an integer wave), for the wave whose stripes run along the systole (a band wrapping the
short loop), and for the waves along the other short lattice vectors; each divided by its value for the same
number of cells drawn at random from the face (the null, by simulation).  Ratio 1: no band in that direction.
"""
import glob, math, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tslab, geom                                    # noqa: E402
from lattice import Q, reduced                        # noqa: E402
from analyze import death_times, ring_firewall, INF   # noqa: E402

RR = os.path.join(tslab.OUT, 'rep_ring')
H = 64


def build():
    src = os.path.join(HERE, 'rep_ring.c')
    if not os.path.exists(RR) or os.path.getmtime(RR) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', RR + '.new', src]); os.replace(RR + '.new', RR)


def face_layers(v, m=tslab.M):
    keys = [k for k, _ in v.layers]
    return keys.index((0, 1)), keys.index((0, 2 * m - 1))


def validate(a, k, b, gens=3000):
    build(); geom.build_rep()
    v = tslab.tslab(a, k, b)
    L0, L1 = face_layers(v)
    vb = os.path.join(tslab.OUT, f'fe_{os.getpid()}.bin'); v.write(vb)
    r1 = subprocess.run([geom.REP, vb, '4', '0.4', '5', str(gens), '16', '-t'], capture_output=True, text=True).stdout
    r2 = subprocess.run([RR, vb, '4', '0.4', '5', str(gens), '16', '-t', '-r', str(L0), str(L1)], capture_output=True, text=True).stdout
    os.remove(vb)
    l1 = r1.splitlines(); l2 = [l for l in r2.splitlines() if not l.startswith('D')]
    D = [l for l in r2.splitlines() if l.startswith('D')]
    ok = l1 == l2
    # each record ends in an all-dead state preceded by a not-all-dead one
    okD = all(set(l.split()[-1]) == {'0'} and set(l.split()[-2]) != {'0'} for l in D)
    print(f'rep_ring vs rep on ({a},{k}),(0,{b}): {len(l1)} lines identical: {ok}; {len(D)} death records well formed: {okD}')
    return ok and okD


def run(a, k, b, cap, seed, W):
    build()
    v = tslab.tslab(a, k, b)
    L0, L1 = face_layers(v)
    vb = os.path.join(tslab.OUT, f'fe_{os.getpid()}.bin'); v.write(vb)
    pr = subprocess.run([RR, vb, str(W), '0.4', str(seed), str(cap), '16', '-r', str(L0), str(L1)], capture_output=True, text=True, check=True)
    os.remove(vb)
    ge = int(pr.stderr.split()[-1])
    rows, recs = [], []
    for l in pr.stdout.splitlines():
        if l.startswith('D'):
            f = l.split(); recs.append((int(f[1]), int(f[2]), int(f[3]), f[4:]))
        else:
            rows.append(list(map(int, l.split())))
    arr = np.array(rows, dtype=np.int64)
    D = death_times(arr[:, 4:], ge)
    keys = [kk for kk, _ in v.layers]
    fw = np.full(len(arr), INF)
    for d in (1, 2, 3):
        cols = [i for i, kk in enumerate(keys) if kk[0] == d]
        if len(cols) >= 3:
            fw = np.minimum(fw, ring_firewall(D[:, cols], ring=True))
    n = 3 * a * b
    hist = np.zeros((len(recs), H, n), np.uint8)
    r_, f_, g_, fwfirst = [], [], [], []
    for i, (r, f, g, ss) in enumerate(recs):
        ss = ss[-H:]
        for j, s in enumerate(ss):
            hist[i, H - len(ss) + j] = np.frombuffer(s.encode(), np.uint8) - 48
        r_.append(r); f_.append(f); g_.append(g); fwfirst.append(fw[r] <= g)
    out = os.path.join(tslab.OUT, f'fe_{a}_{k}_{b}_s{seed}.npz')
    np.savez_compressed(out, hist=hist, rep=r_, face=f_, gen=g_, fwfirst=fwfirst)
    print(f'{out}: {len(recs)} face deaths ({int(np.sum(fwfirst))} after a firewall), gen_end {ge}')


def coords(a, k, b):
    """lattice-basis coordinates (c1, c2) of the face-layer cells in layer order (same for both faces up to a shift)."""
    v = tslab.tslab(a, k, b)
    L0, L1 = face_layers(v)
    out = []
    for L in (L0, L1):
        P = np.array([v.cells[i] for i in v.layers[L][1]], float) / 2
        x, y = P[:, 0], P[:, 1]
        c1 = x / a; c2 = (y - c1 * k) / b
        out.append(np.stack([c1, c2], 1))
    return out


def waves(a, k, b):
    """integer waves n with stripes along the shortest few lattice vectors (n . coeffs(v) = 0)."""
    vs = []
    for p in range(-6, 7):
        for q in range(-6, 7):
            if (p, q) == (0, 0) or math.gcd(p, q) != 1:
                continue
            x, y = p * a, p * k + q * b
            vs.append((Q(x, y), (p, q), (x, y)))
    vs.sort()
    seen, out = set(), []
    for q2, (p, q), xy in vs:
        n = (q, -p) if (q, -p) > (-q, p) else (-q, p)
        if n in seen:
            continue
        seen.add(n); out.append((q2, xy, n))
        if len(out) == 3:
            break
    return out


def analyze(a, k, b, G=50):
    fs = sorted(glob.glob(os.path.join(tslab.OUT, f'fe_{a}_{k}_{b}_s*.npz')))
    hist = np.concatenate([np.load(f)['hist'] for f in fs]); face = np.concatenate([np.load(f)['face'] for f in fs])
    fwf = np.concatenate([np.load(f)['fwfirst'] for f in fs])
    keep = ~fwf
    hist, face = hist[keep], face[keep]
    C = coords(a, k, b); W = waves(a, k, b)
    print(f'({a},{k}),(0,{b}): {len(hist)} face deaths without an earlier firewall ({int(fwf.sum())} with, left out); '
          f'waves (stripes along lattice vector, systole^2): ' + ', '.join(f'{xy} [{q2}]' for q2, xy, n in W))
    rng = np.random.default_rng(1)
    n = hist.shape[2]
    # null: R for c random cells of face 0's layout
    def R(cells_c, nvec):
        ph = 2 * np.pi * (cells_c @ np.array(nvec, float))
        return np.abs(np.exp(1j * ph).mean())
    null = {}
    for c in range(1, n + 1):
        null[c] = [np.mean([R(C[0][rng.choice(n, c, replace=False)], w[2]) for _ in range(300)]) for w in W]
    print(f'{"gen":>4s} {"live":>6s} ' + ' '.join(f'{"R/null " + str(w[1]):>16s}' for w in W) + '   (lives with >= 1 live cell)')
    rows = []
    for g in list(range(-G, -10, 10)) + list(range(-10, 0)):
        idx = H - 1 + g
        live = hist[:, idx, :].sum(1)
        rat = [[] for _ in W]
        for i in range(len(hist)):
            c = live[i]
            if c < 2:
                continue
            cc = C[face[i]][hist[i, idx].astype(bool)]
            for j, w in enumerate(W):
                rat[j].append(R(cc, w[2]) / null[c][j])
        rr = [(np.mean(x), np.std(x) / math.sqrt(len(x))) for x in rat]
        rows.append((g, live.mean(), rr))
        print(f'{g:4d} {live.mean():6.2f} ' + ' '.join(f'{m:8.3f} ± {e:5.3f}' for m, e in rr))
    return rows


if __name__ == '__main__':
    c = sys.argv[1]; args = list(map(int, sys.argv[2:]))
    if c == 'validate':
        sys.exit(0 if validate(*args) else 1)
    elif c == 'run':
        run(*args)
    else:
        analyze(*args)
