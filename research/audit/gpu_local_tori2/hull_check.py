#!/usr/bin/env python3
"""Job 1 of REVIEW-gpu-local-tori2.md: the hull-face calibration at R = 11 recomputed from the branch's row, against
the A10G run on file and the CPU values of research/dying, and the expected size of the R = 15 run.

  python3 research/audit/gpu_local_tori2/hull_check.py <checkout of claude/gpu-local-1080>
"""
import csv, json, math, os, sys

wt = sys.argv[1]
here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
rows = list(csv.DictReader(open(os.path.join(wt, 'research/data/gpu_local_hull/hull_R11.csv'))))
E = sum(int(r['exposure']) for r in rows); F = sum(int(r['deaths']) for r in rows)
card = math.log(8 * E / F); se = 1 / math.sqrt(F)
print(f'card R = 11: {len(rows)} row(s), E = {E}, F = {F}, kind 5 {sum(int(r["guard"]) for r in rows)}, '
      f'settled {sum(int(r["settled12"]) + int(r["settled3pw"]) for r in rows)}: ln tau_face = {card:.4f} +- {se:.4f}')
for name in ('R11_s1_A10G.json', 'R15_s1_A10G.json'):
    r = json.load(open(os.path.join(here, 'research/data/gpu_facelaw', name)))
    a = r['agg']['200']
    v = math.log(8 * a['exposure'] / a['deaths']); e = 1 / math.sqrt(a['deaths'])
    print(f'A10G {name}: deaths {a["deaths"]}, settled {a["settled"]}, max age {r["max_age"]:.3g}: ln tau_face = {v:.4f} +- {e:.4f}'
          + (f'; card - A10G = {card - v:+.4f} +- {math.hypot(se, e):.4f}' if r['R'] == 11 else ''))
for lab, v, e in (('research/dying round 4 (soup 0.4, T0 512)', 13.633, 0.005), ('REVIEW-dying round 4', 13.626, 0.012)):
    print(f'{lab}: {v} +- {e}; card - it = {card - v:+.4f} +- {math.hypot(se, e):.4f} ({(card - v) / math.hypot(se, e):+.1f} sigma)')
print('\nR = 15 run as launched (1,280 replicas, 3.5e8 replica-gens/s, 2 x 420 min):')
for lt in (23.273, 23.376):
    m = math.exp(lt) / 8; X = 3.5e8 * 2 * 420 * 60; D = X / m
    print(f'  if ln tau_face = {lt}: first-death mean {m:.3g}, deaths {D:.0f}, error {1 / math.sqrt(D):.4f}, '
          f'oldest age / mean {2.7e5 * 420 * 60 / m:.2f}')
print(f'  smallest grid delay of the guard for an odd period > 128 at K = 2^18: {129 * 2 ** 18:.3g} '
      f'= {129 * 2 ** 18 / (math.exp(23.273) / 8):.3f} first-death means')
