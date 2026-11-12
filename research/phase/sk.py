"""Static structure factor S(k) of torus snapshots (exact face positions, doubled coords
x = 2c + e_a; normalised so uncorrelated cells give S = 1). Full 3D, binned in |k| (per cube,
k = 2*pi*q/n) both spherically and in 20-degree cones about <100>, <110>, <111>.
usage: python3 sk.py OUT.json SNAP [SNAP ...]"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

out = sys.argv[1]
tot = None; cnt = 0
for p in sys.argv[2:]:
    V, _ = gl.read_snapshot(p)
    n = V.shape[1]; rho = V.mean(); var = rho * (1 - rho)
    q = np.fft.fftfreq(n, 1.0 / n)  # signed integers
    Q = np.stack(np.meshgrid(q, q, q, indexing='ij'))
    amp = sum(np.fft.fftn(V[a].astype(float) - rho) * np.exp(-1j * np.pi * Q[a] / n) for a in range(3))
    S = np.abs(amp) ** 2 / (3 * n ** 3 * var)
    tot = S if tot is None else tot + S
    cnt += 1
S = tot / cnt
k = 2 * np.pi * np.sqrt((Q ** 2).sum(0)) / n
u = Q / np.maximum(np.sqrt((Q ** 2).sum(0)), 1e-9)
bins = np.linspace(0, np.pi * np.sqrt(3), 40)
res = {'n': n, 'snaps': cnt, 'kbins': bins.tolist()}
def binned(mask):
    idx = np.digitize(k[mask], bins)
    s = np.bincount(idx, weights=S[mask], minlength=len(bins) + 1)
    s2 = np.bincount(idx, weights=S[mask] ** 2, minlength=len(bins) + 1)
    c = np.bincount(idx, minlength=len(bins) + 1)
    m = s / np.maximum(c, 1); e = np.sqrt(np.maximum(s2 / np.maximum(c, 1) - m ** 2, 0) / np.maximum(c * cnt, 1))
    return m[1:-1].tolist(), e[1:-1].tolist(), c[1:-1].tolist()
nz = k > 0
res['all'] = binned(nz)
au = np.abs(u)
for name, d in [('100', [1, 0, 0]), ('110', [1, 1, 0]), ('111', [1, 1, 1])]:
    d = np.array(d) / np.linalg.norm(d)
    srt = np.sort(au, axis=0)[::-1]       # |u| components sorted descending
    cosang = (srt * np.sort(d)[::-1][:, None, None, None]).sum(0)
    res[name] = binned(nz & (cosang > np.cos(np.radians(20))))
json.dump(res, open(out, 'w'))
kc = 0.5 * (bins[1:] + bins[:-1])
for name in ['all', '100', '110', '111']:
    m, e, c = res[name]
    print(name.ljust(4), ' '.join(f'{x:.2f}' for x in m[:16]))
print('k   ', ' '.join(f'{x:.2f}' for x in kc[:16]))
