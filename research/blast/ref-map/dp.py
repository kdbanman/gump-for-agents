#!/usr/bin/env python3
"""Gaussian chain on (P,B) from a tally of gs.c: minimum action (value iteration), route, exact ln tau (quasi-stationary
death rate by power iteration).   dp.py <tal> [d=0|1] [mode] [nmin] [src.tal for mode carry]
Modes (how drift and covariance are defined where the tally is thin, n < nmin):
  visited  only cells with n >= nmin are states; mass sent elsewhere is renormalised away (ref-anatomy's rule)
  nearest  every cell is a state; a thin cell copies drift (mean - position) and covariance of the nearest measured cell
  poly2/3  thin cells take a weighted polynomial fit (degree 2/3 in the fillings; weights min(n,1e4)) of drift/A and cov/A
  carry    thin cells take another size's map at equal fillings (bilinear), then nearest
  carryabs thin cells take another size's map at equal absolute P and equal filling of B, then nearest
Death: P' < 0.5 (rounded to 0). Start: the mode of the living histogram."""
import sys, numpy as np

class Map:
    def __init__(s, fn, d=0):
        s.n = None; s.expo = 0.0; s.deaths = 0.0
        for f1 in fn.split('+'):          # several tallies of one vessel are summed
            rows = []
            for line in open(f1):
                w = line.split()
                if w[0] == '#': s.hdr = {w[i]: w[i + 1] for i in range(1, len(w) - 1, 2)}
                elif w[0] == 'T' and int(w[1]) == d: rows.append([float(v) for v in w[2:]])
            h = s.hdr; s.A = int(h['A']); s.nB = int(h['nB'] if d == 0 else h['nB2']); s.NF = int(h['NF'])
            s.expo += float(h['expo']); s.deaths += float(h['deaths'])
            sh = (s.A + 1, s.nB + 1)
            if s.n is None: s.n = np.zeros(sh); t = np.zeros(sh + (5,))
            for r in rows: s.n[int(r[0]), int(r[1])] += r[2]; t[int(r[0]), int(r[1])] += r[3:]
        n = np.maximum(s.n, 1)
        s.mP = t[..., 0] / n; s.mB = t[..., 1] / n
        s.vPP = t[..., 2] / n - s.mP ** 2; s.vBB = t[..., 3] / n - s.mB ** 2; s.vPB = t[..., 4] / n - s.mP * s.mB
        s.P, s.B = np.meshgrid(np.arange(s.A + 1), np.arange(s.nB + 1), indexing='ij')
    def lntau(s): return np.log(s.NF * s.expo / s.deaths), 1 / np.sqrt(s.deaths)
    def fields(s):   # drift and covariance per cell of area, on the grid
        return np.stack([(s.mP - s.P) / s.A, (s.mB - s.B) / s.nB, s.vPP / s.A, s.vBB / s.A, s.vPB / s.A], -1)

def build(m, mode='visited', nmin=200, src=None):
    ok = (m.n >= nmin) & (m.P >= 1); F = m.fields()
    if mode == 'visited':
        sel = ok
    else:
        sel = (m.P >= 1) & (m.P <= 0.85 * m.A) & (m.B <= 0.85 * m.nB)
        thin = sel & ~ok
        if mode == 'carryall': ok = ok & False; thin = sel; mode = 'carry'   # every cell from the other size's map
        if mode.startswith('poly'):
            q = int(mode[4:]); x = m.P / m.A; b = m.B / m.nB
            feats = np.stack([x ** i * b ** j for i in range(q + 1) for j in range(q + 1 - i)], -1)
            w = np.sqrt(np.minimum(m.n[ok], 1e4))
            for k in range(5):
                co = np.linalg.lstsq(feats[ok] * w[:, None], F[ok][:, k] * w, rcond=None)[0]
                F[..., k][thin] = (feats @ co)[thin]
        else:
            if mode == 'carry':
                Fs = src.fields(); oks = (src.n >= nmin) & (src.P >= 1)
                xs = m.P / m.A * src.A; bs = m.B / m.nB * src.nB
                i0 = np.clip(np.floor(xs).astype(int), 0, src.A - 1); j0 = np.clip(np.floor(bs).astype(int), 0, src.nB - 1)
                fx = xs - i0; fb = bs - j0
                good = oks[i0, j0] & oks[i0 + 1, j0] & oks[i0, j0 + 1] & oks[i0 + 1, j0 + 1]
                val = (Fs[i0, j0] * ((1 - fx) * (1 - fb))[..., None] + Fs[i0 + 1, j0] * (fx * (1 - fb))[..., None]
                       + Fs[i0, j0 + 1] * ((1 - fx) * fb)[..., None] + Fs[i0 + 1, j0 + 1] * (fx * fb)[..., None])
                use = thin & good; F[use] = val[use]; ok = ok | use; thin = sel & ~ok
            if mode == 'carryabs':     # thin cells: another size's map at equal ABSOLUTE P and equal filling of B
                Fs = src.fields(); oks = (src.n >= nmin) & (src.P >= 1)
                i0 = np.clip(m.P, 0, src.A); j0 = np.clip(np.rint(m.B / m.nB * src.nB).astype(int), 0, src.nB)
                r = src.A / m.A; val = Fs[i0, j0] * np.array([r, 1.0, r, 1.0, np.sqrt(r)])
                use = thin & oks[i0, j0] & (m.P <= src.A); F[use] = val[use]; ok = ok | use; thin = sel & ~ok
            src_p = np.argwhere(ok); th = np.argwhere(thin)
            for c0 in range(0, len(th), 512):
                c = th[c0:c0 + 512]
                d2 = ((c[:, None, :] - src_p[None, :, :]) ** 2).sum(-1); j = d2.argmin(1)
                F[c[:, 0], c[:, 1]] = F[src_p[j, 0], src_p[j, 1]]
    P = m.P[sel].astype(float); B = m.B[sel].astype(float); f = F[sel]
    M = np.stack([P + f[:, 0] * m.A, B + f[:, 1] * m.nB], -1)
    vPP = np.maximum(f[:, 2] * m.A, 0.05); vBB = np.maximum(f[:, 3] * m.A, 0.05)
    vPB = np.clip(f[:, 4] * m.A, -0.95 * np.sqrt(vPP * vBB), 0.95 * np.sqrt(vPP * vBB))
    return P, B, M, vPP, vBB, vPB

def chain(m, P, B, M, vPP, vBB, vPB, tau=True, verbose=False):
    ns = len(P); det = vPP * vBB - vPB ** 2
    a = vBB / det; b = -vPB / det; c = vPP / det           # inverse covariance
    C = np.empty((ns, ns), np.float32); Dm = np.zeros(ns); Z = np.zeros(ns)
    E = 30; pe = np.arange(-E, 1.0); be = np.arange(-E, m.nB + E + 1.0)
    for i0 in range(0, ns, 256):
        sl = slice(i0, min(ns, i0 + 256))
        dP = P[None, :] - M[sl, 0:1]; dB = B[None, :] - M[sl, 1:2]
        c64 = 0.5 * (a[sl, None] * dP ** 2 + 2 * b[sl, None] * dP * dB + c[sl, None] * dB ** 2)
        C[sl] = c64; Z[sl] = np.exp(-c64).sum(1)
        dP = pe[None, :, None] - M[sl, 0][:, None, None]; dB = be[None, None, :] - M[sl, 1][:, None, None]
        Dm[sl] = np.exp(-0.5 * (a[sl, None, None] * dP ** 2 + 2 * b[sl, None, None] * dP * dB + c[sl, None, None] * dB ** 2)).sum((1, 2))
    Cd = 0.5 * np.maximum(M[:, 0] - 0.5, 0) ** 2 / vPP        # cheapest way to P' = 0.5, B' free
    V = Cd.copy(); nxt = -np.ones(ns, int)
    for it in range(200):
        W = C + V[None, :].astype(np.float32); j = W.argmin(1); w = W[np.arange(ns), j]
        better = w < V - 1e-7
        if not better.any(): break
        V[better] = w[better]; nxt[better] = j[better]
    start = int(np.argmax(m.n[P.astype(int), B.astype(int)])); route = []; i = start; cost = []
    while i >= 0 and len(route) < 80:
        route.append((int(P[i]), int(B[i]))); j = nxt[i]; cost.append(float(C[i, j]) if j >= 0 else float(Cd[i])); i = j
    out = dict(S=float(V[start]), route=route, cost=cost, ns=ns)
    if tau:
        Zt = Z + Dm; K = np.exp(-C); K /= Zt[:, None].astype(np.float32); kd = Dm / Zt
        v = m.n[P.astype(int), B.astype(int)].astype(np.float32) + 1e-3; v /= v.sum()
        rate = None
        for it in range(600):          # capped: a rule whose chain has a second basin does not converge; its ln tau is then void
            v2 = v @ K; v2 /= v2.sum()
            if it % 50 == 49:
                r = float(v2.astype(float) @ kd)
                if rate is not None and abs(np.log(r / rate)) < 1e-5: rate = r; break
                rate = r
            v = v2
        out['lntau'] = -np.log(rate); out['its'] = it
    return out

if __name__ == '__main__':
    fn = sys.argv[1]; d = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'visited'; nmin = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    m = Map(fn, d); src = Map(sys.argv[5], d) if len(sys.argv) > 5 else None
    lt, e = m.lntau(); i = np.unravel_index(m.n.argmax(), m.n.shape)
    print(f"{fn}: A={m.A} nB={m.nB} expo={m.expo:.4g} deaths={m.deaths:.0f} gump ln tau here {lt:.3f} +- {e:.3f}; mode {i}; "
          f"cov/A at mode {m.vPP[i]/m.A:.3f} {m.vBB[i]/m.A:.3f} {m.vPB[i]/m.A:.3f}; cells n>={nmin}: {(m.n>=nmin).sum()}")
    r = chain(m, *build(m, mode, nmin, src))
    print(f"  d={d} {mode} nmin={nmin} states={r['ns']}: S={r['S']:.3f} S/A={r['S']/m.A:.4f} chain ln tau={r['lntau']:.3f} (its {r['its']})")
    print("  route:", ' '.join(f"({p},{b})" for p, b in r['route']))
    print("  costs:", ' '.join(f"{c:.2f}" for c in r['cost']))
