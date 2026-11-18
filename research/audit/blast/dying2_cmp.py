#!/usr/bin/env python3
"""The GTX 1080 session's tables of the dying face by lag (research/dying2 on origin/claude/gpu-local-1080, read
with git show) beside this directory's own (fd.c's L table: every death of the pooled runs).

    python3 research/audit/blast/dying2_cmp.py
"""
import io, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyse as an
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
REF = 'origin/claude/gpu-local-1080'


def show(path):
    t = subprocess.run(['git', '-C', ROOT, 'show', f'{REF}:{path}'], capture_output=True, text=True, check=True).stdout
    rows = [l.split(',') for l in t.strip().splitlines()]
    return rows[0], [[float(v) for v in r] for r in rows[1:]]


def mine(prefixes):
    S, H, J, K, L, Q, QB, DB = an.load_sum(prefixes)
    x = np.arange(256); mean = (H * x).sum() / H.sum()
    return S, H, L, mean


CASES = [('W63 torus (1,4),(0,21)', 'research/dying2/data/1_4_21_lags.csv', ['slab63_s11', 'slab63_s12', 'slab63_s13', 'slab63_s14'], 63, 'w'),
         ('T84 tube (1,12),(0,28)', 'research/dying2/data/1_12_28_lags.csv', ['tube84_s31', 'tube84_s32'], 84, 'w'),
         ('E84 torus (2,4),(0,14) there, (1,4),(0,28) here', 'research/dying2/data/2_4_14_lags.csv', ['wide84_s41', 'wide84_s42'], 84, 'w'),
         ('hull R = 11', 'research/dying2/hull/data/R11_death_timecourse.csv', ['hull63_s21', 'hull63_s22', 'hull63_s23', 'hull63_s24'], 63, 'h')]
for name, path, prefixes, A, kind in CASES:
    hd, rows = show(path)
    S, H, L, mean = mine(prefixes)
    print(f'\n{name}: {S["deaths"]} deaths here, mean population {mean:.3f}; ordinary 90% and 95% points here: {an.quant(H, [.9, .95])} cells')
    print('  lag | there: mean/Pbar, upper quantile (cells, share of the face) | here: mean/Pbar, the same quantile | here: share of deaths with >= 0.70 A, >= 0.746 A at that lag')
    for r in rows:
        lag = int(r[0])
        if not 1 <= lag <= 12: continue
        h = L[lag]
        if kind == 'w':
            m_t, q_t = r[2], r[7] * mean; qn = 0.90
        else:
            m_t, q_t = r[1], r[7]; qn = 0.95
        q_h = an.quant(h, [qn])[0]
        print(f'  {lag:3d} | {m_t:.4f}  q{int(qn * 100)} {q_t:5.1f} ({q_t / A:.3f} A) | {(h * np.arange(256)).sum() / h.sum() / mean:.4f}  {q_h:3d} ({q_h / A:.3f} A) | '
              f'{h[int(np.ceil(0.70 * A)):].sum() / h.sum():.4f}  {h[int(np.ceil(0.746 * A)):].sum() / h.sum():.4f}')
