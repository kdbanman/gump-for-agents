"""Anatomy of edge deaths from ed.c records.  Usage: python3 anat.py [L ...]   (reads ../../scratch/blast/toy/{r,b}L.rec/.out)
r = ring edge (strip 16 x L periodic along the edge), b = box edge (L x L).
bustK = share of deaths whose last K steps (fatal step included) contain a one-generation fall >= L/2 of the row;
liveK = share of living windows of K transitions that contain one; pop@lag = population j generations before
the empty row; peak = population just before the largest fall; spread = sd over cells of the last-alive lag."""
import sys, os, numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'toy')
def pc(v): return bin(v).count('1')
def load(fn):
    D, V = [], []
    for line in open(fn):
        t = line.split()
        if len(t) != 18: continue
        (D if t[0] == 'D' else V).append([int(z, 16) for z in t[2:]])
    return D, V
def maxfall(p):  # p: populations in time order
    d = [p[i] - p[i + 1] for i in range(len(p) - 1)]
    i = int(np.argmax(d)); return d[i], p[i], len(d) - i
def q(a, f): return np.percentile(a, f)
Ls = [int(z) for z in sys.argv[1:]] or [12, 16, 20, 24, 28, 32]
import json
J = {}
for L in Ls:
    for g in 'rb':
        fn = f'{S}/{g}{L}.rec'
        if not os.path.exists(fn) or not os.path.exists(f'{S}/{g}{L}.out'): continue
        D, V = load(fn); n = len(D)
        if n == 0: continue
        P = np.array([[pc(v) for v in d] + [0] for d in D])      # 16 living generations + the empty row
        half = (L + 1) // 2
        out = {}
        for K in (2, 4, 6, 12):
            mf = np.array([maxfall(p[-(K + 1):])[0] for p in P]); out[K] = (mf >= half).mean()
        PV = np.array([[pc(v) for v in d] for d in V]) if V else np.zeros((0, 16), int)
        live = {K: np.mean([maxfall(p[-(K + 1):])[0] >= half for p in PV]) for K in (6, 12)} if len(PV) else {6: float('nan'), 12: float('nan')}
        mfd = np.array([maxfall(p[-13:]) for p in P]); mfl = np.array([maxfall(p[-13:]) for p in PV]) if len(PV) else np.zeros((1, 3))
        # last-alive lag per cell (1 = alive in the last living generation; cells not alive in the window are left out)
        spread, lastpos, prof, cnt = [], np.zeros(L), np.zeros(L), np.zeros(L)
        for d in D:
            la = np.zeros(L)
            for j in range(1, 17):
                v = d[16 - j]
                for x in range(L):
                    if la[x] == 0 and (v >> x) & 1: la[x] = j
            m = la > 0
            if m.sum() > 1: spread.append(la[m].std())
            prof[m] += la[m]; cnt[m] += 1
            last = [x for x in range(L) if (d[15] >> x) & 1]
            for x in last: lastpos[x] += 1.0 / len(last)
        err = lambda p: np.sqrt(max(p * (1 - p), 1e-9) / n)
        J[f'{g}{L}'] = dict(deaths=n, bust={str(K): float(out[K]) for K in out}, live={str(K): float(live[K]) for K in live}, windows=len(PV), pop_lag=[float(P[:, 16 - j].mean()) for j in range(1, 9)], living_mean=float(PV.mean()) if len(PV) else None, spread=float(np.mean(spread)))
        print(f"{'ring' if g == 'r' else 'box '} L={L:2d} deaths={n:5d} bust2={out[2]:.3f} bust4={out[4]:.3f} bust6={out[6]:.3f}±{err(out[6]):.3f} bust12={out[12]:.3f}±{err(out[12]):.3f} | live6={live[6]:.4f} live12={live[12]:.4f} (n={len(PV)})")
        print("     pop@lag1..8 mean  " + ' '.join(f"{P[:, 16 - j].mean():5.2f}" for j in range(1, 9)) + f"   (living mean {PV.mean():.2f})" if len(PV) else '')
        print("     pop@lag1..8 10/50/90% " + ' '.join(f"{q(P[:, 16 - j], 10):.0f}/{q(P[:, 16 - j], 50):.0f}/{q(P[:, 16 - j], 90):.0f}" for j in range(1, 9)))
        print(f"     largest fall in 12 steps: deaths mean {mfd[:, 0].mean():.2f} 10/50/90% {q(mfd[:, 0], 10):.0f}/{q(mfd[:, 0], 50):.0f}/{q(mfd[:, 0], 90):.0f}; living mean {mfl[:, 0].mean():.2f} 10/50/90% {q(mfl[:, 0], 10):.0f}/{q(mfl[:, 0], 50):.0f}/{q(mfl[:, 0], 90):.0f}; peak before it: deaths {mfd[:, 1].mean():.2f} living {mfl[:, 1].mean():.2f}; steps before the empty row (median) {np.median(mfd[:, 2]):.0f}")
        w = 2
        endshare = (lastpos[:w].sum() + lastpos[-w:].sum()) / lastpos.sum()
        pr = prof / np.maximum(cnt, 1)
        dist = [np.mean([pr[x] for x in range(L) if min(x, L - 1 - x) == k]) for k in range(min(6, L // 2))]
        print(f"     last-alive: spread {np.mean(spread):.2f} generations; last living cells within 2 of an end: {endshare:.3f} (uniform {2 * w / L:.3f}); mean last-alive lag by distance from the nearest end 0..5: " + ' '.join(f"{z:.2f}" for z in dist))
if not sys.argv[1:]: json.dump(J, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'anat.json'), 'w'), indent=1)
