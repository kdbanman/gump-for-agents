"""Static and dynamic statistics of the steady chaotic state on a torus.
usage: python3 bulk.py SNAP [SNAP ...] --gens T --out OUT.json
Each SNAP is a steady-state torus snapshot (engine). For each: neighbour-count histograms,
spatial correlations C_ab(r) (FFT), layer-density fluctuations along {111}/{100}/{110},
then T generations stepped in numpy for temporal autocorrelation, turnover and run lengths.
"""
import sys, os, json, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

ap = argparse.ArgumentParser()
ap.add_argument('snaps', nargs='+')
ap.add_argument('--gens', type=int, default=200)
ap.add_argument('--out', required=True)
ap.add_argument('--rmax', type=int, default=12)
args = ap.parse_args()

DIRS = {  # cube-displacement unit vectors (up to sign); classified per face orientation below
    '100': [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    '110': [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)],
    '111': [(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)],
}

res = []
for path in args.snaps:
    V, meta = gl.read_snapshot(path)
    n = V.shape[1]; ncell = V.size
    rho = V.mean()
    out = {'snap': path, 'n': n, 'rho': float(rho), 'rho_axis': V.mean(axis=(1, 2, 3)).tolist()}
    # --- neighbour counts
    N = gl.counts(V)
    out['hist_live'] = np.bincount(N[V], minlength=13).tolist()
    out['hist_dead'] = np.bincount(N[~V], minlength=13).tolist()
    # --- spatial correlations, all orientation pairs, via FFT over cube displacement
    D = V.astype(np.float64) - rho
    F = np.fft.rfftn(D, axes=(1, 2, 3))
    C = np.empty((3, 3, n, n, n))
    for a in range(3):
        for b in range(3):
            C[a, b] = np.fft.irfftn(np.conj(F[a]) * F[b], s=(n, n, n), axes=(0, 1, 2)) / n ** 3
    var = rho * (1 - rho)
    C /= var  # C[a,b][r] = <dV_a(x) dV_b(x+r)>/var
    rm = args.rmax
    prof = {}
    for a in range(3):
        for key, vs in DIRS.items():
            for v in vs:
                v = np.array(v)
                # label relative to face normal a: component along normal and in-plane
                lab = f'a{a}_{key}_n{abs(v[a])}'
                vals = [float(C[a, a][tuple((m * v) % n)]) for m in range(rm + 1)]
                prof.setdefault(lab, []).append(vals)
    out['C_same'] = {k: np.mean(v, axis=0).tolist() for k, v in prof.items()}
    # nearest cross-orientation correlations at r = 0 (neighbouring and non-neighbouring perpendicular faces)
    out['C_cross_r0'] = [[float(C[a, b][0, 0, 0]) for b in range(3)] for a in range(3)]
    # --- layer density fluctuations: variance of plane densities relative to independent cells
    I, J, K = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')
    lay = {}
    for name, d in [('111', (1, 1, 1)), ('100', (1, 0, 0)), ('110', (1, 1, 0))]:
        rats = []
        for perm in set([tuple(np.array(d)[list(p)]) for p in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]] +
                        ([(-1, 1, 1), (1, -1, 1), (1, 1, -1)] if name == '111' else []) +
                        ([(1, -1, 0), (0, 1, -1), (-1, 0, 1)] if name == '110' else [])):
            dd = np.array(perm)
            for a in range(3):
                # doubled layer coordinate s = d.(2x + e_a); planes of constant s, mod torus period
                s = (2 * (dd[0] * I + dd[1] * J + dd[2] * K) + dd[a]) % (2 * n)
                cnt = np.bincount(s.ravel(), weights=V[a].ravel(), minlength=2 * n)
                tot = np.bincount(s.ravel(), minlength=2 * n)
                m = tot > 0
                dens = cnt[m] / tot[m]
                rats.append(float(np.var(dens) / (var / tot[m].mean())))
        lay[name] = [float(np.mean(rats)), float(np.std(rats) / np.sqrt(len(rats)))]
    out['plane_var_ratio'] = lay
    # --- dynamics
    T = args.gens
    pops = []; changed = []
    S0 = V.copy(); acf = np.zeros(T + 1)
    # run-length bookkeeping: time each cell entered its current state
    since = np.zeros(V.shape, np.int32)
    runs_live = np.zeros(T + 2, np.int64); runs_dead = np.zeros(T + 2, np.int64)
    birth_n = np.zeros(13, np.int64); death_n = np.zeros(13, np.int64)
    cur = V
    tab = gl.make_table('B45/S345')
    Dhist = []
    for t in range(1, T + 1):
        Nc = gl.counts(cur)
        nxt = gl.step(cur, tab, Nc)
        ch = nxt != cur
        birth_n += np.bincount(Nc[ch & nxt], minlength=13)
        death_n += np.bincount(Nc[ch & cur], minlength=13)
        # completed runs (exclude runs that started at t=0: censored on the left)
        done = ch & (since > 0)
        L = t - since[done]
        wasl = cur[done]
        runs_live += np.bincount(L[wasl], minlength=T + 2)[:T + 2]
        runs_dead += np.bincount(L[~wasl], minlength=T + 2)[:T + 2]
        since[ch] = t
        cur = nxt
        pops.append(float(cur.mean())); changed.append(float(ch.mean()))
        acf[t] = (np.mean(S0 & cur) - rho * cur.mean()) / var
    acf[0] = 1.0
    out.update(pops=pops, changed=changed, acf=acf.tolist(), runs_live=runs_live.tolist(),
               runs_dead=runs_dead.tolist(), birth_n=birth_n.tolist(), death_n=death_n.tolist())
    res.append(out)
    print(path, 'rho', round(float(rho), 4), 'turnover', round(np.mean(changed), 4), 'acf1..4', np.round(acf[1:5], 3), flush=True)
json.dump(res, open(args.out, 'w'))
