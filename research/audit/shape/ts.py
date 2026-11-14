#!/usr/bin/env python3
"""Driver for ts.c (independent stepper for the review of research/shape/). Graph from geom_check.my_slab
(AUTOMATON.md's cube-index table), layers with own indexing.

    python3 research/audit/shape/ts.py validate a k b GENS N      # trace vs the engine on the cubic N-torus
    python3 research/audit/shape/ts.py run a k b W GENS SEED [CAP]  # renewal lives; appends to scratch
    python3 research/audit/shape/ts.py stats a k b [CAP]          # ln tau_face etc. from all runs of that torus
"""
import glob, math, os, random, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geom_check as gc  # noqa: E402

OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_shape')
BIN = os.path.join(OUT, 'ts')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
M = 8
os.makedirs(OUT, exist_ok=True)


def build():
    src = os.path.join(HERE, 'ts.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', BIN + '.new', src])
        os.replace(BIN + '.new', BIN)


def vessel(L):
    cells, idx, nb = gc.my_slab(L, M)
    P = gc.periods(L)
    face0 = [n for n, c in enumerate(cells) if c[3] == 0]
    face1 = [n for n, c in enumerate(cells) if c[3] == M - 1]
    diags = []
    for d, dv in enumerate([(-1, 1, 1), (1, -1, 1), (1, 1, -1)]):
        lay = {}
        for n, c in enumerate(cells):
            p = gc.doubled(c)
            lay.setdefault(sum(dv[x] * p[x] for x in range(3)) % P[d], []).append(n)
        assert sorted(lay) == list(range(1, P[d], 2))
        diags.append([lay[s] for s in sorted(lay)])
    inter = [[n for n, c in enumerate(cells) if c[3] == t] for t in range(1, M - 1)]
    path = os.path.join(OUT, f'v_{L[0]}_{L[1]}_{L[2]}.bin')
    with open(path + '.tmp', 'wb') as f:
        w = lambda x: f.write(struct.pack('<i', x))
        w(len(cells))
        for row in nb:
            for x in row:
                w(-1 if x is None else x)
        for lst in (face0, face1):
            w(len(lst)); [w(x) for x in lst]
        w(len(diags))
        for d in diags:
            w(len(d))
            for lst in d:
                w(len(lst)); [w(x) for x in lst]
        w(len(inter))
        for lst in inter:
            w(len(lst)); [w(x) for x in lst]
    os.replace(path + '.tmp', path)
    return cells, path


def validate(L, gens, N, seed=11):
    build()
    cells, path = vessel(L)
    assert gc.embed_ok(L, N)
    rng = random.Random(seed)
    live = [n for n in range(len(cells)) if rng.random() < 0.4]
    ini = os.path.join(OUT, f'init_{os.getpid()}.txt'); open(ini, 'w').write('\n'.join(map(str, live)))
    ev = os.path.join(OUT, f'ev_{os.getpid()}.txt')
    out = subprocess.run([BIN, path, '1', '0.4', '1', '1', '1', str(gens), ev, '-i', ini], capture_output=True, text=True, check=True).stdout
    mine = [int(l.split()[2]) for l in out.splitlines() if l.startswith('T')]
    reps = [(x, y) for x in range(N) for y in range(N) if gc.in_lat((x, y), L)]
    kc = len(reps); assert kc * L[0] * L[2] == N * N, (kc, L, N)
    pts = set()
    for n in live:
        p = gc.doubled(cells[n])
        for x, y in reps:
            pts.add(tuple((p[i] + 2 * v) % (2 * N) for i, v in enumerate((x, y, -x - y))))
    assert len(pts) == kc * len(live)
    cf = os.path.join(OUT, f'cells_{os.getpid()}.txt'); open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in pts))
    pl = os.path.join(OUT, f'pl_{os.getpid()}.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(N), '--gens', str(gens), '--no-halt', '--poplog', pl],
                   check=True, capture_output=True)
    ref = [list(map(int, l.split())) for l in open(pl)]
    refd = {g: v for g, v in ref}
    nmatch = sum(1 for g, v in enumerate(mine) if g in refd and refd[g] == v * kc)
    ncomp = sum(1 for g in range(len(mine)) if g in refd)
    first_bad = next((g for g, v in enumerate(mine) if g in refd and refd[g] != v * kc), None)
    print(f'validate {L} N={N} x{kc}: compared {ncomp} generations, matching {nmatch}, first mismatch {first_bad}; '
          f'pops {mine[:3]}..{mine[-1]}; distinct {len(set(mine))}')
    for x in (ini, ev, cf, pl):
        os.remove(x)
    return ncomp >= gens - 1 and nmatch == ncomp


def run(L, W, gens, seed, cap=500000, K=8):
    build()
    _, path = vessel(L)
    tag = f'{L[0]}_{L[1]}_{L[2]}_c{cap}_s{seed}'
    ev = os.path.join(OUT, f'ev_{tag}.txt')
    out = subprocess.run([BIN, path, str(W), '0.4', str(seed), str(cap), str(K), str(gens), ev + '.tmp'],
                         capture_output=True, text=True, check=True).stdout
    os.replace(ev + '.tmp', ev)
    open(os.path.join(OUT, f'sum_{tag}.txt'), 'w').write(out)
    print(tag, out.strip(), flush=True)


def stats(L, cap=500000, quiet=False):
    files = sorted(glob.glob(os.path.join(OUT, f'ev_{L[0]}_{L[1]}_{L[2]}_c{cap}_s*.txt')))
    seeds = [f.rsplit('_s', 1)[1][:-4] for f in files]
    assert len(set(seeds)) == len(seeds)
    E = 0.0; cnt = {}; ages = []
    for f in files:
        for line in open(f):
            t, a = line.split(); a = int(a)
            E += a; cnt[t] = cnt.get(t, 0) + 1
            ages.append((a, t))
    sums = [open(os.path.join(OUT, 'sum_' + os.path.basename(f)[3:])).read().split() for f in files]
    near2 = sum(int(s[s.index('near2') + 1]) for s in sums); intfw = sum(int(s[s.index('intfw') + 1]) for s in sums)
    F = cnt.get('F', 0); X = cnt.get('X', 0); Wn = cnt.get('W', 0)
    # three age bins of equal exposure
    ages.sort()
    tot = E; cuts = []
    import numpy as np
    A = np.array([a for a, _ in ages], float); isF = np.array([t == 'F' for _, t in ages])
    def expo(lo, hi):
        return (np.clip(A, lo, hi) - lo).clip(0).sum()
    lo_hi = [0.0]
    for target in (tot / 3, 2 * tot / 3):
        lo, hi = 0.0, A.max()
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if expo(0, mid) < target else (lo, mid)
        lo_hi.append(lo)
    lo_hi.append(A.max() + 1)
    thirds = []
    for lo, hi in zip(lo_hi[:-1], lo_hi[1:]):
        nf = int((isF & (A >= lo) & (A < hi)).sum())
        thirds.append((math.log(2 * expo(lo, hi) / nf) if nf else float('nan'), 1 / math.sqrt(nf) if nf else float('nan'), int(lo)))
    r = dict(runs=len(files), E=E, cnt=cnt, F=F, lnF=math.log(2 * E / F) if F else float('nan'), eF=1 / math.sqrt(F) if F else 0,
             lnFX=math.log(2 * E / (F + X)) if F + X else float('nan'), near2=near2, intfw=intfw, thirds=thirds,
             lnW=math.log(E / Wn) if Wn else float('inf'))
    if not quiet:
        print(f'{L} cap {cap}: {r["runs"]} runs, exposure {E:.4e}, counts {cnt}; ln tau_face = {r["lnF"]:.4f} +- {r["eF"]:.4f} '
              f'(ties counted as face: {r["lnFX"]:.4f}); ln tau_fw = {r["lnW"]:.3f}; checks with 2 adjacent dead transverse '
              f'layers {near2}; interior d0 firewalls {intfw}; hazard thirds ' +
              ', '.join(f'{x:.3f}+-{e:.3f} (from {lo})' for x, e, lo in thirds))
    return r


if __name__ == '__main__':
    c = sys.argv[1]; args = list(map(int, sys.argv[2:]))
    L = tuple(args[:3])
    if c == 'validate':
        sys.exit(0 if validate(L, args[3], args[4]) else 1)
    elif c == 'run':
        run(L, args[3], args[4], args[5], *(args[6:7] or [500000]))
    else:
        stats(L, *(args[3:4] or [500000]))
