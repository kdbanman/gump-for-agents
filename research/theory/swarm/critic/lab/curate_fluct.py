"""Critic's lab: copy the tables that path_r1.py reads out of the bulk tallies research/scratch/fluct/qsd_R*.npz
(not in git; written by research/fluct/qsd.py on 2026-11-13) into a small committed file, data/fluct_tables.npz.

    python3 curate_fluct.py        (needs the scratch files; re-creates data/fluct_tables.npz)

Kept for each hull R = 7, 9, 11, 13 (face area A = 30, 45, 63, 84):
  Tr_R[k, k']      one-step transitions of the population of a face from k < (A+1)//2 to k' (k' = 0: that face died),
                   over replicas with all 8 faces alive and age >= T0 = 200 (see qsd.py for the exact conditions)
  H_R[n]           histogram of the face population over measured living states (8 faces pooled)
  deaths_R, expo_R deaths and replica-generations of exposure (hazard per face = deaths / (8 * expo))
  prehist_R[s, n]  number of recorded deaths whose dying face had n live cells s generations before the death
                   (s = 0..64; row 0 is all at n = 0). From the `pre` array, which is too large to commit whole.
  lasthalf_R[s]    number of deaths for which s is the smallest lag >= 1 with n >= half the living mean
                   (living mean from research/fluct/data/qsd_summary.json; index 65 = never within 64 generations)
"""
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
AREA = {7: 30, 9: 45, 11: 63, 13: 84}

if __name__ == '__main__':
    s = json.load(open(os.path.join(RES, 'fluct', 'data', 'qsd_summary.json')))['sizes']
    out = {}
    for R, A in AREA.items():
        z = np.load(os.path.join(RES, 'scratch', 'fluct', f'qsd_R{R}.npz'), allow_pickle=True)
        assert int(z['deaths'][0]) == s[str(R)]['deaths'], "scratch tallies do not match the committed summary"
        out[f'Tr_{R}'] = z['Tr'].astype(np.int64)
        out[f'H_{R}'] = z['H'].astype(np.int64)
        out[f'deaths_{R}'] = z['deaths'].astype(np.int64)
        out[f'expo_{R}'] = z['expo'].astype(np.int64)
        pre = z['pre'][:, :, 0].astype(np.int64)                     # (deaths, 65); index 64 = the death
        ph = np.zeros((65, A + 1), np.int64)
        for lag in range(65):
            ph[lag] = np.bincount(pre[:, 64 - lag], minlength=A + 1)
        out[f'prehist_{R}'] = ph
        half = s[str(R)]['mean'] * A / 2
        rev = pre[:, ::-1][:, 1:] >= half                             # columns = lags 1..64
        first = np.where(rev.any(1), rev.argmax(1) + 1, 65)
        out[f'lasthalf_{R}'] = np.bincount(first, minlength=66)
    fn = os.path.join(HERE, 'data', 'fluct_tables.npz')
    np.savez_compressed(fn, **out)
    print('wrote', fn, os.path.getsize(fn), 'bytes')
