#!/usr/bin/env python3
"""Reduce research/scratch/wraplocal/st_*.npz (live.py runs) to statistics with standard errors from the
independent blocks (512 replicas each, all seeds of a torus pooled).

    python3 research/wraplocal/ana.py H K D [H K D ...]     # one line per torus
    python3 research/wraplocal/ana.py --all                 # every torus with runs
"""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'wrap'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import lattices as L  # noqa: E402
import geom_check as gc  # noqa: E402
import validate  # noqa: E402

SCR = os.environ.get('WRAPLOCAL_DIR', os.path.join(ROOT, 'research', 'scratch', 'wraplocal'))
DISPS = []


def nbgraph(h, k, d):
    cells, path = validate.ts.vessel((h, k, d))
    return validate.read_bin(path)[1]


def load(h, k, d):
    fs = sorted(glob.glob(os.path.join(SCR, f'st_{h}_{k}_{d}_s*.npz')))
    zs = [dict(np.load(f)) for f in fs]
    if not zs:
        return None
    keys = ['lay_live', 'lay_birth', 'lay_death', 'lay_exp', 'sN', 'sN2', 'sRG', 'hist_in', 'hist_tot', 'S1', 'S2',
            'SC', 'acx', 'acN', 'acC', 'acM', 'acX']
    z = {k_: np.concatenate([q[k_] for q in zs]) for k_ in keys}
    z['gens'] = sum(int(q['gens']) * int(q['W']) * 64 for q in zs)
    z['dropped'] = sum(int(q['dropped']) for q in zs)
    z['nseed'] = len(zs)
    return z


def tmap(h, k, d):
    cells, path = validate.ts.vessel((h, k, d))
    idx = {c: n for n, c in enumerate(cells)}

    def T(i, X, Y):
        ax, a, b, t = cells[i]
        a2, b2 = gc.reduce_ij(a + X, b + Y, (h, k, d))
        return idx[(ax, a2, b2, t)]
    return cells, T


def blockstats(z, h, k, d):
    A = 3 * h * d
    out = {}
    face = [0, 7]
    e = z['lay_exp']
    out['rho_face'] = (z['lay_live'][:, face].sum(1) / e[:, face].sum(1))
    out['rho_int'] = (z['lay_live'][:, 1:7].sum(1) / e[:, 1:7].sum(1))
    out['birth_face'] = (z['lay_birth'][:, face].sum(1) / e[:, face].sum(1))
    out['death_face'] = (z['lay_death'][:, face].sum(1) / e[:, face].sum(1))
    out['act_int'] = ((z['lay_birth'][:, 1:7] + z['lay_death'][:, 1:7]).sum(1) / e[:, 1:7].sum(1))
    mN = z['sN'] / z['sRG'][:, None]
    vN = z['sN2'] / z['sRG'][:, None] - mN ** 2
    out['varN_per_cell'] = vN.mean(1) / A
    out['fano'] = vN.mean(1) / mN.mean(1)
    # neighbour-count histograms, live and dead face cells
    hi = z['hist_in']; ht = z['hist_tot']
    for s_, nm in ((0, 'dead'), (1, 'live')):
        p = ht[:, s_] / ht[:, s_].sum(1, keepdims=True)
        out[f'ntot_{nm}'] = (p * np.arange(13)).sum(1)
        q = hi[:, s_] / hi[:, s_].sum(1, keepdims=True)
        out[f'nin_{nm}'] = (q * np.arange(7)).sum(1)
    pd = ht[:, 0] / (ht[:, 0].sum(1) + ht[:, 1].sum(1))[:, None]
    pl = ht[:, 1] / (ht[:, 0].sum(1) + ht[:, 1].sum(1))[:, None]
    out['P_dead_n45'] = pd[:, 4:6].sum(1)      # birth-ready share of face cells
    out['P_live_n345'] = pl[:, 3:6].sum(1)
    # covariance matrix
    cells, T = tmap(h, k, d)
    f0 = [i for i, c in enumerate(cells) if c[3] == 0]
    f7 = [i for i, c in enumerate(cells) if c[3] == 7]
    m = z['S1'] / z['SC'][:, None]
    C = z['S2'] / z['SC'][:, None, None] - m[:, :, None] * m[:, None, :]
    NB = nbgraph(h, k, d)
    tt = np.array([c[3] for c in cells])
    groups = {'C_perp': [], 'C_copl': [], 'C_adj': [], 'C_next': []}
    for f in (f0, f7):
        for i in f:
            for j in NB[i]:
                if j < 0:
                    continue
                dt = abs(tt[j] - tt[i])
                if dt == 0:
                    groups['C_copl' if cells[j][0] == cells[i][0] else 'C_perp'].append((i, j))
                else:
                    groups['C_adj' if dt == 1 else 'C_next'].append((i, j))
    for nm, pr in groups.items():
        I = np.array([p[0] for p in pr]); J = np.array([p[1] for p in pr])
        out[nm] = C[:, I, J].mean(1)
    if DISPS:
        for X, Y in DISPS:
            for ax in range(3):
                vals = [C[:, i, T(i, X, Y)] for i in f0 + f7 if cells[i][0] == ax]
                out[f'C({X},{Y})q{L.Q(X, Y)}a{ax}'] = np.mean(vals, axis=0)
    var0 = np.mean([C[:, i, i] for i in f0 + f7], axis=0)
    out['C0'] = var0
    # face total covariance per cell from the matrix (same quantity as varN_per_cell, from snapshots)
    out['varN_snap'] = np.mean([C[:, f][:, :, f].sum((1, 2)) for f in (f0, f7)], axis=0) / A
    # lagged
    rho = z['acX'] / (z['acC'] * 2 * A)
    acx = z['acx'] / (z['acC'][:, None] * 2 * A) - rho[:, None] ** 2
    out['tau_cell'] = 0.5 + (acx[:, 1:] / acx[:, :1]).sum(1)
    out['ac1_cell'] = acx[:, 1] / acx[:, 0]
    mNN = z['acM'] / (z['acC'] * 2)
    acN = z['acN'] / (z['acC'][:, None] * 2) - mNN[:, None] ** 2
    out['tau_N'] = 0.5 + (acN[:, 1:] / acN[:, :1]).sum(1)
    return out


def summary(h, k, d):
    z = load(h, k, d)
    if z is None:
        return None
    b = blockstats(z, h, k, d)
    nb = len(z['sRG'])
    res = {key: (v.mean(), v.std(ddof=1) / np.sqrt(nb)) for key, v in b.items()}
    res['_nb'] = nb
    res['_gens'] = z['gens']
    res['_dropped'] = z['dropped']
    return res


def tori_with_runs():
    s = set()
    for f in glob.glob(os.path.join(SCR, 'st_*.npz')):
        p = os.path.basename(f).split('_')
        s.add((int(p[1]), int(p[2]), int(p[3])))
    return sorted(s, key=lambda t: (L.gram(*t)[0], 3 * t[0] * t[2]))


if __name__ == '__main__':
    if '--disp' in sys.argv:
        i = sys.argv.index('--disp'); v = list(map(int, sys.argv[i + 1].split(',')))
        DISPS[:] = [tuple(v[j:j + 2]) for j in range(0, len(v), 2)]
        del sys.argv[i:i + 2]
    if '--all' in sys.argv:
        tori = tori_with_runs()
    else:
        a = list(map(int, sys.argv[1:]))
        tori = [tuple(a[i:i + 3]) for i in range(0, len(a), 3)]
    allres = {}
    for t in tori:
        r = summary(*t)
        if r:
            allres[t] = r
    keys = [k_ for k_ in next(iter(allres.values())) if not k_.startswith('_')]
    for key in keys:
        print(key)
        for t, r in allres.items():
            g = L.gram(*t)
            m, e = r[key]
            print(f'   {str(t):12s} A={3 * t[0] * t[2]:3d} loops {L.loops(*t, cap=30)!s:16s} {m:+.6f} ± {e:.6f}')
    for t, r in allres.items():
        print(t, 'blocks', r['_nb'], 'replica-generations', r['_gens'], 'dropped', r['_dropped'])
