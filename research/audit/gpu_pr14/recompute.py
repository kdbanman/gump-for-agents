#!/usr/bin/env python3
"""PR 14 review: recompute the README table and the PREDICTIONS outcome numbers from the JSON files, independently of
fwslab.summary (own unpacking of `raw`, own estimators), and the A = 108 pooling, the slope and the line's errors.

    git show origin/claude/awesome-cray-boq9vz:research/data/gpu_facelaw/<f>.json > research/scratch/pr14/<f>.json
    python3 research/audit/gpu_pr14/recompute.py research/scratch/pr14
Only 6x6x8 and 6x7x8 carry `raw` (3x6x8 and 4x7x8 exceed raw_cap = 60,000 lives); for those two only the totals are
re-derived.
"""
import base64, csv, glob, json, math, os, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'research', 'scratch', 'pr14')


def unpack(x):
    return np.frombuffer(zlib.decompress(base64.b64decode(x['b64'])), np.int64).reshape(x['shape'])


def line(A):
    return -0.091 + 0.2088 * A


agg = {}
for p in sorted(glob.glob(os.path.join(d, 'fwslab*.json'))):
    r = json.load(open(p))
    key = tuple(r['slab'])
    E, F, W, S = r['exposure'], r['face'], r['fw'], r['settled']
    print(f"{os.path.basename(p)}: gens {r['gens']:.4g}, R {r['replicas']}, wall {r['wall_s']:.0f} s, cuts {r['cuts']}")
    if 'raw' in r:
        a, k, b, dr = unpack(r['raw'])
        assert len(a) == r['replicas'] + F + W + S, 'lives != replicas + events'
        assert int(a.sum()) == E and int((k == 1).sum()) == F and int((k == 4).sum()) == W and int(((k == 2) | (k == 3)).sum()) == S
        assert ((k == 0).sum()) == r['replicas']
        assert (a >= 0).all() and (b + a <= r['gens']).all()
        byd = {int(x): int(((k == 4) & (dr == x)).sum()) for x in (1, 2, 3)}
        assert byd == {int(x): v for x, v in r['fw_by_direction'].items()}, (byd, r['fw_by_direction'])
        # renewal check: per replica, lives tile [0, gens] -- each life starts where the previous ended (at a boundary)
        ev = k != 0
        print(f"   raw ok: {len(a)} lives; event ages: min {a[ev].min():.3g} median {np.median(a[ev]):.3g}; "
              f"open-life ages: min {a[~ev].min():.3g} max {a[~ev].max():.3g}; fw ages {sorted(a[k == 4].tolist())[:3]}...")
        # births of reseeded lives must be launch boundaries; ages of fw lives detected at a boundary end on one
        print(f"   fw lives ending exactly at a birth-grid point (boundary detection): "
              f"{int(np.isin(b[k == 4] + a[k == 4], np.unique(b)).sum())} of {W}")
    else:
        print('   no raw (totals only)')
    g = agg.setdefault(key, dict(E=0, F=0, W=0, S=0, byd={1: 0, 2: 0, 3: 0}, n=0))
    g['E'] += E; g['F'] += F; g['W'] += W; g['S'] += S; g['n'] += 1
    for x, v in r['fw_by_direction'].items():
        g['byd'][int(x)] += v

res = {}
for key, g in sorted(agg.items()):
    A = 3 * key[0] * key[1]
    E, F, W = g['E'], g['F'], g['W']
    lf, lw, l1 = math.log(2 * E / F), math.log(E / W), math.log(2 * E / (F + W))
    sh = W / (F + W); she = math.sqrt(sh * (1 - sh) / (F + W))
    res[key] = (lf, 1 / math.sqrt(F), E, F, W)
    print(f"{key} A={A}: runs {g['n']} E {E:.4g} face {F} fw {W} share {sh:.2%} +- {she:.2%} by dir {g['byd']} settled {g['S']}")
    print(f"   ln tau_face {lf:.3f} +- {1/math.sqrt(F):.3f} (line {line(A):.3f}, diff {lf - line(A):+.3f});"
          f" ln tau_fw {lw:.3f} +- {1/math.sqrt(W):.3f}; first-event {l1:.3f}")

# the earlier unscreened A = 108 run (PR 12), pooled as the PR does
old = json.load(open(os.path.join(ROOT, 'research', 'data', 'gpu_facelaw', 'slab6x6x8_s401_A10G.json')))
E1 = old['lineage']['tau'] * old['lineage']['deaths']; D1 = old['lineage']['deaths']
print(f"old 6x6x8: E {E1:.4g}, deaths {D1}, ln(2E/D) {math.log(2 * E1 / D1):.3f}")
lf2, _, E2, F2, W2 = res[(6, 6, 8)]
share = W2 / (F2 + W2)
F1 = D1 * (1 - share)
pool = math.log(2 * (E1 + E2) / (F1 + F2)); pe = 1 / math.sqrt(F1 + F2)
print(f"pooled A=108 face channel {pool:.3f} +- {pe:.3f} (line {line(108):.3f}, diff {pool - line(108):+.3f})")
# consistency of the two A = 108 runs (first-event rates): Poisson test on counts given exposures
n_new = F2 + W2; p = E2 / (E1 + E2); n = D1 + n_new
z = (n_new - n * p) / math.sqrt(n * p * (1 - p))
print(f"A=108 runs, first events: old {D1} in {E1:.3g}, new {n_new} in {E2:.3g}: z = {z:+.2f}")
lf126, e126 = res[(6, 7, 8)][:2]
sl = (lf126 - pool) / 18; se = math.hypot(e126, pe) / 18
print(f"slope 108->126 = {sl:.4f} +- {se:.4f} (both points' errors); with the unscreened 22.470 +- 0.047: "
      f"{(lf126 - 22.470) / 18:.4f} +- {math.hypot(e126, 0.047) / 18:.4f}")

# the line's own uncertainty at 108 and 126 and its residual scatter (face_law_fit.py's selection)
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, 'research', 'peeling', 'slab_area.csv')))
        if r['m'] == '8' and int(r['fw_before_peel']) < 0.06 * int(r['replicas']) and int(r['A']) >= 27]
A = np.array([float(r['A']) for r in rows]); y = np.log(2 * np.array([float(r['mean_first']) for r in rows]))
ci = lambda k: np.log(2 * np.array([float(r[k]) for r in rows]))
w = 1 / ((ci('ci_hi') - ci('ci_lo')) / 3.92) ** 2
X = np.c_[np.ones(len(A)), A]
cov = np.linalg.inv(X.T @ (X * w[:, None])); ab = cov @ (X.T @ (w * y))
chi2 = float((w * (y - X @ ab) ** 2).sum()); dof = len(A) - 2
intr = math.sqrt(max(0.0, (chi2 - dof) / w.sum() * len(A) / dof))
print(f"line fit: chi2 {chi2:.1f} / {dof} dof; excess scatter ~ {intr:.3f} nats per batch (rough)")
for AA in (108, 126):
    x = np.array([1, AA]); s = math.sqrt(x @ cov @ x)
    print(f"   line at A={AA}: {x @ ab:.3f} +- {s:.3f} (stat; x sqrt(chi2/dof) = {s * math.sqrt(chi2 / dof):.3f})")
