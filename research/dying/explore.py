#!/usr/bin/env python3
"""explore.py: measurements added after the first look at the data (not forecast; PREDICTIONS.md note 2).

    python3 research/dying/explore.py

1. Relative curves: population at lag l over its stationary mean, for the dying face, the layers beneath it
   (cells with s.p = 9 and 7 and s*p >= 0: 45 and 30 cells), and, in c1, the three adjacent faces.
2. Relative band profile: each band's and the interior's occupancy at lag l over its own stationary occupancy.
3. Which edge band has the largest relative deficit 1 - occ/null at t_h (a version of L6 that does not
   inherit the stationary profile of the face).
4. Last-alive lag: for each cell of the dying face the last lag >= 1 at which it was alive (mean over deaths).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from load import geometry, read_dump, regions, SCR, GROUPS, TIED, H, CHK, R_HULL
DATA = os.path.join(HERE, 'data')


def main():
    rng = np.random.default_rng(1)
    rows = []; lastmaps = {}
    for g in GROUPS:
        q, canon, fidx, reps, face_orbit = geometry(g); f = q.f
        z = np.load(os.path.join(SCR, f'canon_{g}.npz'))
        X, W, DID, FS, NUL, jd = z['X'], z['W'], z['DID'], z['FS'], z['NUL'], z['jd']
        band, interior, apex = regions(canon)
        hdr, hist = read_dump(os.path.join(SCR, f'dump_{g}.bin'), q.n)
        L = X.shape[1]
        # layers beneath the dying face; their stationary mean from the dump itself at lags 300-507
        sub = {}
        for s_ in (9, 7):
            pops = np.zeros((len(X), L))
            for k in range(len(X)):
                s = tuple(FS[k]); d = DID[k]
                sel = np.nonzero((f.cells @ np.array(s) == s_) & ((f.cells * np.array(s)) >= 0).all(1))[0]
                pops[k] = hist[d, jd[d]:jd[d] + L][:, q.orb[sel]].sum(1)
            sub[s_] = pops
        P = X.sum(2).astype(float); Pbar = NUL.sum(1).mean()
        rel = {'face': P.mean(0) / Pbar}
        for s_ in (9, 7):
            rel[f'layer{s_}'] = sub[s_].mean(0) / sub[s_][:, 300:].mean()
        nbb = [NUL[:, b].mean() for b in band]; ni = NUL[:, interior].mean()
        relB = [X[:, :, b].mean(2).mean(0) / nbb[a] for a, b in enumerate(band)]
        relI = X[:, :, interior].mean(2).mean(0) / ni
        if g == 'c1':
            rel['nbr'] = z['NBR'].sum(3).mean((0, 1)) / Pbar
        for l in range(0, 41):
            rows.append([g, l] + [rel['face'][l], rel['layer9'][l], rel['layer7'][l], rel.get('nbr', np.full(L, np.nan))[l],
                                  relB[0][l], relB[1][l], relB[2][l], relI[l]])
        print(f'== {g}: relative population (lag: face, layer 9, layer 7' + (', neighbours' if g == 'c1' else '') + '; bands x y z, interior over own null)')
        for l in (0, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64):
            print(f'  {l:3d}: {rel["face"][l]:.3f} {rel["layer9"][l]:.3f} {rel["layer7"][l]:.3f}' + (f' {rel["nbr"][l]:.3f}' if g == 'c1' else '')
                  + f'   | {relB[0][l]:.3f} {relB[1][l]:.3f} {relB[2][l]:.3f} {relI[l]:.3f}')
        # 3. largest relative band deficit at t_h
        lh = np.cumprod(P < Pbar / 2, axis=1).sum(1) - 1
        dB = np.stack([1 - X[np.arange(len(X)), lh][:, b].mean(1) / nbb[a] for a, b in enumerate(band)], 1)
        top = np.argmax(dB + 1e-9 * rng.random(dB.shape), 1)               # ties broken at random
        fr = [float((W * (top == a)).sum() / W.sum()) for a in range(3)]
        se = [np.sqrt(p * (1 - p) / len(X)) for p in fr]
        print(f'  largest relative band deficit at t_h: ' + ', '.join(f'{"xyz"[a]}{"*" if a in TIED[g] else ""} {fr[a]:.3f} ± {se[a]:.3f}' for a in range(3))
              + f'; mean relative deficit x y z {dB.mean(0).round(3).tolist()}, interior {float((1 - X[np.arange(len(X)), lh][:, interior].mean(1) / ni).mean()):.3f}')
        # 4. last-alive lag per cell
        alive = X[:, 1:]                                                    # lags 1..L-1
        first = np.where(alive.any(1), np.argmax(alive, 1) + 1, L)          # smallest lag >= 1 alive = last alive generation
        lastmaps[g] = first.mean(0)
        lb = [lastmaps[g][b].mean() for b in band]; li = lastmaps[g][interior].mean()
        print(f'  mean last-alive lag: bands {", ".join(f"{v:.2f}" for v in lb)}, interior {li:.2f}, apex {lastmaps[g][apex].mean():.2f}')
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, 'relative_by_lag.csv'), 'w') as fh:
        fh.write('group,lag,face,layer9,layer7,neighbours,band_x,band_y,band_z,interior\n')
        for r in rows:
            fh.write(','.join([r[0], str(r[1])] + [f'{v:.5f}' for v in r[2:]]) + '\n')
    np.savez(os.path.join(SCR, 'lastmaps.npz'), **lastmaps)


if __name__ == '__main__':
    main()
