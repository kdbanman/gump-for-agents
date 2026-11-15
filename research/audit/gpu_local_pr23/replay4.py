#!/usr/bin/env python3
"""t4.c's event logic against a plain numpy replay: every life of a short t4 run (64 lanes) is regenerated from its life
id (same hash), stepped with numpy (count of live neighbours, B45/S345), and its first event (firewall / face death /
return to the snapshot taken at ages 1, 2, 4, ...) must give the same age, kind and snapshot age. Exits non-zero on
any difference.  python3 research/audit/gpu_local_pr23/replay4.py [GENS] [SEED] [W]"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_pr23')
sys.path.insert(0, HERE)
import geom4  # noqa: E402
M64 = (1 << 64) - 1


def mix(z):
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return z ^ (z >> 31)


THR = int(0.4 * 2 ** 53)


def soup(seed, life, n):
    h = mix(seed ^ mix(life))
    return np.array([(mix((h + c) & M64) >> 11) < THR for c in range(n)])


def replay(starts, nb, face, trans, cap):
    L, n = starts.shape
    x = np.zeros((L, n + 1), bool); x[:, :n] = starts
    nbp = np.where(nb < 0, n, nb)
    res = np.full((L, 3), -2, np.int64)
    snap = np.zeros_like(x); sv = np.zeros(L, bool); sage = np.full(L, -1); nexts = np.ones(L, np.int64)
    alive = np.ones(L, bool)
    for age in range(1, cap + 1):
        c = x[:, nbp].sum(2)[:, :n]
        new = np.zeros_like(x); new[:, :n] = (c == 4) | (c == 5) | (x[:, :n] & (c == 3))
        x = new
        fdead = ~x[:, face[0]].any(1) | ~x[:, face[1]].any(1)
        fw = np.zeros(L, bool)
        for d in trans:
            occ = np.stack([x[:, l].any(1) for l in d], 1)
            for k in range(8):
                fw |= ~occ[:, k] & ~occ[:, (k + 1) % 8] & ~occ[:, (k + 2) % 8]
        eq = sv & (x == snap).all(1)
        kind = np.where(fw, 4, np.where(fdead, 1, np.where(eq, 5, 0)))
        hit = alive & (kind > 0)
        res[hit, 0] = age; res[hit, 1] = kind[hit]; res[hit, 2] = np.where(kind[hit] == 5, sage[hit], -1)
        alive &= ~hit
        due = alive & (nexts == age)
        snap[due] = x[due]; sv |= due; sage[due] = age; nexts[due] *= 2
        if not alive.any():
            break
    return res


if __name__ == '__main__':
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    W = sys.argv[3] if len(sys.argv) > 3 else '1'
    g = os.path.join(SCR, 'g44.bin'); geom4.write(g)
    out = os.path.join(SCR, 'replay.bin')
    subprocess.run([os.path.join(SCR, 't4'), g, W, str(seed), str(gens), out], check=True, capture_output=True)
    r = np.fromfile(out, np.int64).reshape(-1, 4)
    ended = r[r[:, 1] > 0]
    if W != '1':                       # wider runs: every firewall and settled life, and the first 300 face deaths
        ended = np.concatenate([ended[ended[:, 1] != 1], ended[ended[:, 1] == 1][:300]])
    nb = geom4.graph(); face, trans = geom4.layers()
    starts = np.array([soup(seed, int(l), len(geom4.CELLS)) for l in ended[:, 3]])
    res = replay(starts, nb, face, trans, int(ended[:, 0].max()) + 1)
    bad = int((res != ended[:, :3]).any(1).sum())
    kinds = {k: int((ended[:, 1] == k).sum()) for k in (1, 4, 5)}
    print(f'{len(ended)} ended lives replayed (kinds {kinds}); differences in (age, kind, snapshot age): {bad}')
    # negative control: a replay one generation off must differ everywhere
    print('control (ages + 1):', int((res[:, 0] != ended[:, 0] + 1).sum()), 'of', len(ended), 'differ')
    sys.exit(0 if bad == 0 else 1)
