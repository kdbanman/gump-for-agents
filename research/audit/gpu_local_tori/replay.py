#!/usr/bin/env python3
"""replay.py: tor.c's event logic against an independent numpy replay of the same lives.

    python3 replay.py A K B W GENS SEED NSAMPLE
Runs `tor run` (64*W lanes, GENS generations), then regenerates the soups of a sample of its lives (every life of
kind 2 or 4, NSAMPLE of kind 1, NSAMPLE open ones) from (seed, lane, life) with this file's own copy of the hash,
steps them with a numpy rule (counts by fancy indexing, not bit slicing), and applies the event rules written out
again here: firewall (3 cyclically consecutive dead transverse layers, diagonals with >= 3 layers) before face death
(t = 0 or 7 empty) before a return to the snapshot of ages 1, 2, 4, ... . Every sampled life must end with the same
kind at the same age (and, for cycles, the same snapshot age); open lives must have no event up to their age.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geo, val  # noqa: E402
REC = np.dtype([('lane', '<i4'), ('kind', '<i4'), ('birth', '<i8'), ('age', '<i8'), ('snap', '<i8'), ('life', '<i8')])
M64 = (1 << 64) - 1


def mix(z):
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return z ^ (z >> 31)


def soup(seed, lane, life, n):
    h0 = mix(mix(mix(seed) ^ lane) ^ life)
    thr = int(0.4 * 9007199254740992.0)
    return np.array([(mix(h0 ^ c) >> 11) < thr for c in range(n)], bool)


def replay(g, lives, seed):
    n = g['n']; L = len(lives)
    nb = np.where(g['nb'] < 0, n, g['nb'])
    x = np.zeros((L, n + 1), bool)
    for r, lv in enumerate(lives):
        x[r, :n] = soup(seed, int(lv['lane']), int(lv['life']), n)
    f0 = np.nonzero(g['t'] == 0)[0]; f1 = np.nonzero(g['t'] == g['m'] - 1)[0]
    diags = [d for d in range(3) if g['P'][d] // 2 >= 3]
    onehot = {d: np.eye(g['P'][d] // 2, dtype=int)[g['sd'][d]] for d in diags}      # [n, layers]
    snap = np.zeros_like(x); hasnap = np.zeros(L, bool); snapage = np.full(L, -1)
    kind = np.full(L, 0); end = np.zeros(L, np.int64); done = np.zeros(L, bool)
    horizon = np.array([int(lv['age']) for lv in lives])
    for age in range(1, horizon.max() + 1):
        c = x[:, nb].sum(-1)                                   # [L, n]
        xn = np.zeros_like(x)
        xn[:, :n] = (c == 4) | (c == 5) | (x[:, :n] & (c == 3))
        x = xn
        act = ~done
        fw = np.zeros(L, bool)
        for d in diags:
            alive = (x[:, :n].astype(int) @ onehot[d]) > 0      # [L, layers]
            dead = ~alive
            fw |= (dead & np.roll(dead, -1, 1) & np.roll(dead, -2, 1)).any(1)
        face = ~x[:, f0].any(1) | ~x[:, f1].any(1)
        cyc = hasnap & (x == snap).all(1)
        ev = act & (fw | face | cyc)
        kind[ev] = np.where(fw[ev], 4, np.where(face[ev], 1, 2)); end[ev] = age; done |= ev
        pw = act & ~ev & ((age & (age - 1)) == 0)
        snap[pw] = x[pw]; hasnap |= pw; snapage[pw] = age
        if done.all() or (age >= horizon).all():
            break
    return kind, end, snapage


if __name__ == '__main__':
    a, k, b, W, gens, seed, ns = map(int, sys.argv[1:8])
    g = geo.build(a, k, b)
    gp = os.path.join(val.SCR, f'rp_{a}_{k}_{b}.bin'); geo.write(g, gp)
    exe = val.build()
    out = os.path.join(val.SCR, f'rp_{a}_{k}_{b}_s{seed}.rec')
    subprocess.run([exe, 'run', gp, str(W), str(seed), str(gens), out], check=True)
    R = np.fromfile(out, REC)
    rng = np.random.default_rng(1)
    pick = []
    for kd, cap in ((2, 10 ** 9), (4, 10 ** 9), (1, ns), (0, ns)):
        idx = np.nonzero(R['kind'] == kd)[0]
        pick += list(rng.permutation(idx)[:cap])
    lives = R[np.array(sorted(pick))]
    kind, end, snapage = replay(g, lives, seed)
    bad = 0; byk = {}
    for lv, kd, e, s in zip(lives, kind, end, snapage):
        if lv['kind'] == 0:
            okk = kd == 0 or e > lv['age']
        else:
            okk = kd == lv['kind'] and e == lv['age'] and (kd != 2 or s == lv['snap'])
        bad += not okk; byk.setdefault(int(lv['kind']), [0, 0])[0] += 1; byk[int(lv['kind'])][1] += not okk
    print(f'({a},{k}),(0,{b}) seed {seed}: {len(R)} records (kinds {np.bincount(R["kind"], minlength=5).tolist()}); '
          f'replayed {len(lives)}: by kind [n, mismatches] {byk}; {"ALL OK" if bad == 0 else "FAILURES"}')
    sys.exit(0 if bad == 0 else 1)
