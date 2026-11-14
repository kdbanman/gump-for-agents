#!/usr/bin/env python3
"""Independent recomputation of PR 16's width table, differences, fits and burn-in checks from the JSON files.

  python3 research/audit/gpu_pr16/recompute.py <dir holding fwslab*.json>   (e.g. a worktree of the PR branch)
"""
import base64, glob, json, math, sys, zlib
import numpy as np

D = sys.argv[1] if len(sys.argv) > 1 else 'research/data/gpu_facelaw'
recs = {}
for p in sorted(glob.glob(f'{D}/fwslab*.json')):
    r = json.load(open(p)); r['_p'] = p.split('/')[-1]
    recs.setdefault(tuple(r['slab']), []).append(r)

def unpack(d):
    return np.frombuffer(zlib.decompress(base64.b64decode(d['b64'])), np.int64).reshape(d['shape'])

pts = {}
print('slab     A  s  runs  cap      exposure        F        W   fw%   ln tau_face  +-     ln tau_fw  E/W(mean fw life)')
for key, rs in sorted(recs.items()):
    N1, N2, m = key
    E = sum(r['exposure'] for r in rs); F = sum(r['face'] for r in rs); W = sum(r['fw'] for r in rs)
    y = math.log(2 * E / F); se = 1 / math.sqrt(F)
    caps = ','.join(str(r.get('max_launch', 'old2^18')) for r in rs)
    print(f'{N1}x{N2}x{m} {3*N1*N2:4d} {min(N1,N2)} {len(rs):3d}  {caps:14s} {E:.4e} {F:8d} {W:8d} {100*W/(F+W):5.1f}  {y:8.3f} {se:.3f}   {math.log(E/W):7.3f}   {E/W:.3g}')
    for r in rs:
        yi = math.log(2 * r['exposure'] / r['face'])
        msg = f'    {r["_p"]}: ln tau_face {yi:.3f} +- {1/math.sqrt(r["face"]):.3f}'
        if 'hist' in r:
            h = r['hist']; ex = np.array(h['exposure']); 
            ok = (ex.sum() == r['exposure'], sum(h['deaths']['1']) == r['face'], sum(h['deaths']['4']) == r['fw'],
                  sum(h['deaths']['2']) + sum(h['deaths']['3']) == r['settled'])
            msg += f'; hist totals match (E,F,W,S): {ok}'
        if 'raw' in r:
            a, k, b, dr = unpack(r['raw'])
            msg += (f'; raw n={a.size} sum(a)==E {a.sum()==r["exposure"]} F {int((k==1).sum())==r["face"]} '
                    f'W {int((k==4).sum())==r["fw"]} censored {int((k==0).sum())==r["censored"]}')
        else:
            n = r['face'] + r['fw'] + r['settled'] + r['censored']
            msg += f'; no raw (lives {n})'
        print(msg)
    pts[(N1, N2)] = dict(s=min(N1, N2), A=3 * N1 * N2, y=y, se=se, F=F, W=W, E=E)

def diff(a, b):
    p, q = pts[a], pts[b]
    return p['y'] - q['y'], math.hypot(p['se'], q['se'])
print()
for a, b in [((4, 9), (6, 6)), ((3, 8), (4, 6)), ((3, 8), (6, 4)), ((3, 10), (5, 6)), ((4, 6), (6, 4)), ((4, 5), (3, 6))]:
    d, e = diff(a, b); print(f'{a} - {b}: {d:+.3f} +- {e:.3f}')

# fits
P = list(pts.values())
y = np.array([p['y'] for p in P]); w = np.array([1 / p['se'] ** 2 for p in P]); A = np.array([p['A'] for p in P], float)
S = sorted({p['s'] for p in P}); si = np.array([S.index(p['s']) for p in P])
def wls(X):
    cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); r = y - X @ beta
    return beta, cov, r, float((w * r * r).sum()), len(y) - X.shape[1]
I = np.eye(len(S))[si]
models = dict(A=np.c_[np.ones(len(y)), A], O=np.c_[I, A], W=np.c_[I, I * A[:, None]])
print()
for nm, X in models.items():
    beta, cov, r, chi2, dof = wls(X)
    print(f'{nm}: chi2 = {chi2:.1f} / {dof} dof')
    if nm == 'W':
        for i, s in enumerate(S):
            print(f'   b({s}) = {beta[len(S)+i]:.4f} +- {math.sqrt(cov[len(S)+i, len(S)+i]):.4f}, a({s}) = {beta[i]:.3f}')
        for (N1, N2), p, ri in zip(pts, P, r):
            print(f'   resid {N1}x{N2}: {ri:+.4f} ({ri/p["se"]:+.1f} sigma)')
        # pairwise slope differences
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                d = beta[len(S)+j] - beta[len(S)+i]; e = math.sqrt(cov[len(S)+i, len(S)+i] + cov[len(S)+j, len(S)+j])
                print(f'   b({S[j]}) - b({S[i]}) = {d:+.4f} +- {e:.4f} ({d/e:.1f} sigma)')
    if nm == 'O':
        print('   b =', round(beta[-1], 4), 'a(s) =', [round(x, 3) for x in beta[:-1]])

# W plus long side? per-family quadratic in A for families with >= 3 points; and W fitted with s = 6 removed
print()
for s in S:
    idx = si == S.index(s)
    if idx.sum() >= 3:
        X = np.c_[np.ones(idx.sum()), A[idx], A[idx] ** 2]
        Xl = X[:, :2]; ww = w[idx]; yy = y[idx]
        def f(X):
            cov = np.linalg.inv(X.T @ (X * ww[:, None])); b = cov @ (X.T @ (ww * yy)); rr = yy - X @ b
            return b, cov, float((ww * rr * rr).sum())
        bl, cl, chl = f(Xl); bq, cq, chq = f(X)
        print(f's={s}: line chi2 {chl:.1f}/{idx.sum()-2}; quadratic coef {bq[2]:.2e} +- {math.sqrt(cq[2,2]):.1e}, chi2 {chq:.1f}/{idx.sum()-3}')
# local slopes
print()
for s in S:
    q = sorted([p for p in P if p['s'] == s], key=lambda p: p['A'])
    for u, v in zip(q, q[1:]):
        if u['A'] == v['A']: continue
        d = (v['y'] - u['y']) / (v['A'] - u['A']); e = math.hypot(u['se'], v['se']) / (v['A'] - u['A'])
        print(f's={s}: A {u["A"]}->{v["A"]}: slope {d:.4f} +- {e:.4f}')

# burn-in: hazard by age bins, face and fw, per slab with hist
print('\nface hazard by age (ln tau_face over the bin = ln(2 x exposure / face deaths)), cumulative fraction of exposure')
for key, rs in sorted(recs.items()):
    hs = [r['hist'] for r in rs if 'hist' in r]
    if not hs: continue
    ed = hs[0]['edges']; ex = np.sum([h['exposure'] for h in hs], 0); fd = np.sum([h['deaths']['1'] for h in hs], 0)
    wd = np.sum([h['deaths']['4'] for h in hs], 0)
    E = ex.sum(); F = fd.sum()
    out = []
    # coarse bins: [0,200), [200,1e3), [1e3,1e4), [1e4,1e5), [1e5,1e6), [1e6,1e7), [1e7,1e8), >=1e8
    cb = [0, 200, 1000, 10000, 100000, 10**6, 10**7, 10**8, 10**16]
    for lo, hi in zip(cb, cb[1:]):
        i = [j for j in range(len(ed) - 1) if ed[j] >= lo and ed[j + 1] <= hi]
        e = ex[i].sum(); f = fd[i].sum(); ww = wd[i].sum()
        if e == 0: continue
        z = math.log(2 * e / f) if f else float('nan')
        dz = (1 / math.sqrt(f)) if f else float('nan')
        out.append(f'[{lo:.0e},{hi:.0e}) {z:.3f}±{dz:.3f} (F{f},W{ww},E{e/E:.1%})')
    print(f'{key[0]}x{key[1]}x{key[2]} all {math.log(2*E/F):.3f}: ' + '; '.join(out))
    # >= T0 checks and their correlated-difference error
    for T0 in (200, 1000, 10000, 100000):
        if T0 not in ed: continue
        i = ed.index(T0); e = ex[i:].sum(); f = fd[i:].sum()
        if f:
            # difference late - all: error ~ sqrt(1/f - 1/F) (nested samples)
            print(f'     ages >= {T0}: {math.log(2*e/f):.3f} ({f} deaths), minus all {math.log(2*e/f)-math.log(2*E/F):+.3f} +- {math.sqrt(max(1/f-1/F,0)):.3f}')
