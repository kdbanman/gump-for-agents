#!/usr/bin/env python3
"""rep.c's soups re-generated (its xoshiro256** and seeding, copied into Python) for research/shape2's 4x4 seeds:
are the 4096 soups of a job distinct from every other job's, and is the soup density 0.4?  Also the per-job dispersion
of face deaths (chi^2 against Poisson) in the original files and in a re-run with fresh seeds.
    python3 research/audit/gpu_local_pr23/repseed.py [JOBS]"""
import glob, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
M = (1 << 64) - 1
rotl = lambda x, k: ((x << k) | (x >> (64 - k))) & M


def soups(seed, n=384, W=64, p=0.4):
    s = [0x9E3779B97F4A7C15 ^ seed, (0xD1B54A32D192ED03 + seed * 7) & M, 0x8CB92BA72F3D8DD7, (seed * 0x2545F4914F6CDD1D + 1) & M]
    def nxt():
        r = (rotl((s[1] * 5) & M, 7) * 9) & M; t = (s[1] << 17) & M
        s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45)
        return r
    for _ in range(20):
        nxt()
    thr = int(p * 18446744073709551616.0)
    out = np.zeros((64 * W, n), bool)
    for o in range(n):
        for w in range(W):
            for k in range(64):
                if nxt() < thr:
                    out[64 * w + k, o] = True
    return out


def dispersion(files):
    rows = []
    for f in files:
        z = np.load(f)
        face, fw, st, ge = z['face'], z['fw'], z['settle'], int(z['gen_end'])
        stop = np.where(st >= 0, st, ge).astype(float); fwm = fw.min(1)
        end = np.minimum.reduce([face, fwm, stop]); kF = (face == end) & (face < fwm) & (face <= stop)
        rows.append((end.sum(), kF.sum()))
    E, F = np.array(rows, float).T
    lam = F.sum() / E.sum()
    return float(((F - lam * E) ** 2 / (lam * E)).sum()), len(rows) - 1


if __name__ == '__main__':
    J = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 6
    if "--cross" in sys.argv:
        J = 0
    seen = {}
    dens = []
    for j in range(J):
        S = soups(1008000 + j)
        dens.append(S.mean())
        for r, row in enumerate(S):
            seen.setdefault(np.packbits(row).tobytes(), []).append((j, r))
    dup = sum(len(v) - 1 for v in seen.values())
    print(f'rep.c soups of seeds 1008000..{1008000 + J - 1}: {J * 4096} soups, {dup} repeated; density per job '
          f'{np.round(dens, 4).tolist()}')
    for name, pat in (('original', 'research/scratch/shape2/ch_4_0_4_s*.npz'),
                      ('fresh', 'research/scratch/audit_gpu_local_pr23/fresh/ch_4_0_4_s*.npz')):
        fs = sorted(glob.glob(os.path.join(ROOT, pat)))
        if fs:
            c, d = dispersion(fs)
            print(f'{name}: per-job face deaths, chi2 {c:.1f} on {d} dof')


def cross(J=4):
    """bit agreement of adjacent seeds' soups, lane by lane, and lane-by-lane correlation of the end times of adjacent
    jobs in the original files (identical streams would show as agreement far from 2p(1-p) = 0.48, or correlation)"""
    S = [soups(1008000 + j) for j in range(J)]
    xs = [float((S[j] ^ S[j + 1]).mean()) for j in range(J - 1)]
    fs = sorted(glob.glob(os.path.join(ROOT, 'research/scratch/shape2/ch_4_0_4_s*.npz')))
    ends = []
    for f in fs:
        z = np.load(f)
        ends.append(np.minimum(z['face'], 16384.0))
    cs = [float(np.corrcoef(ends[j], ends[j + 1])[0, 1]) for j in range(len(ends) - 1)]
    print(f'adjacent seeds: soup bits differ in {np.round(xs, 4).tolist()} (iid: 0.48); lane-by-lane correlation of '
          f'face times, adjacent original jobs: mean {np.mean(cs):+.4f}, sd {np.std(cs):.4f} (iid: 0 +- {1 / 64:.4f})')


if __name__ == '__main__' and '--cross' in sys.argv:
    cross()
