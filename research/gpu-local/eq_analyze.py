#!/usr/bin/env python3
"""Per-torus analysis of the eqtorus runs: pooled ln tau_face, seed consistency, hazard by age, oldest lives.

  python research/gpu-local/eq_analyze.py A K B
  python research/gpu-local/eq_analyze.py A K B save    # also write the per-run age tables to the data directory

Reads research/data/gpu_local_eqtorus/eqtorus_A_K_B.csv (the committed per-run rows) and, where present, the per-run
json in research/scratch/gpu-local/ (age histograms, raw lives). CPU only.
"""
import csv, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
import facelaw  # noqa: E402

a, k, b = map(int, sys.argv[1:4])
rows = list(csv.DictReader(open(os.path.join(ROOT, 'research', 'data', 'gpu_local_eqtorus', f'eqtorus_{a}_{k}_{b}.csv'))))
E = sum(int(r['exposure']) for r in rows); F = sum(int(r['face']) for r in rows); W = sum(int(r['fw']) for r in rows)
y = math.log(2 * E / F)
print(f'torus ({a},{k}),(0,{b}) A = {rows[0]["A"]}: {len(rows)} runs, E = {E:.5g}, face {F}, fw {W}, '
      f'settled {sum(int(r["settled12"]) + int(r["settled3pw"]) for r in rows)}, guard {sum(int(r["guard"]) for r in rows)}, '
      f'fw_settled {sum(int(r["fw_settled"]) for r in rows)}')
print(f'  ln tau_face = {y:.4f} +- {1 / math.sqrt(F):.4f}' + (f'   ln tau_fw (fw + fw_settled) = '
      f'{math.log(E / (W + sum(int(r["fw_settled"]) for r in rows))):.3f}' if W else ''))
chi2 = 0
for r in rows:
    e, f = int(r['exposure']), int(r['face'])
    chi2 += (f - F * e / E) ** 2 / (F * e / E)
    print(f'  seed {r["seed"]}: face {f}, ln = {math.log(2 * e / f):.4f} +- {1 / math.sqrt(f):.4f}, open at end {r["open"]}')
print(f'  seeds: chi2 = {chi2:.2f} on {len(rows) - 1}')
hs, raws, saved, cut = [], [], {}, 0
HIST = os.path.join(ROOT, 'research', 'data', 'gpu_local_eqtorus', f'hist_{a}_{k}_{b}.json')
for r in rows:
    p = os.path.join(ROOT, 'research', 'scratch', 'gpu-local', f'eqtorus_{a}_{k}_{b}_s{r["seed"]}.json')
    if os.path.exists(p):
        j = json.load(open(p)); hs.append(j['hist'])
        gl = facelaw.unpack(j['guard_lives'])                # per kind-5 life: replica, age at recognition, snapshot age
        cut += int((gl[1] - gl[2]).sum())
        saved[r['seed']] = dict(hist=j['hist'], guard_lives=gl.tolist(), gens=j['gens'], replicas=j['replicas'])
        if 'raw' in j:
            raws.append(facelaw.unpack(j['raw']))
if saved and sys.argv[4:] == ['save']:
    json.dump(dict(torus=[a, k, b], note='per run: exposure and ends by kind (1 face death, 2 period 1-2, 3 period 3-128, 4 firewall, '
                   '5 guard) in the age bins `edges`; guard_lives = [replica, age, snapshot age] rows', runs=saved),
              open(HIST, 'w'), separators=(',', ':'))
elif not hs and os.path.exists(HIST):                       # no per-run json on this machine: the committed tables
    hs = [x['hist'] for x in json.load(open(HIST))['runs'].values()]
g5 = sum(int(r['guard']) for r in rows)
if g5:                                                      # the two exposure conventions for kind-5 lives
    print(f'  kind 5: {g5} lives; ln tau_face with their exposure cut at the snapshot age = {math.log(2 * (E - cut) / F):.4f} '
          f'(whole age, above: {y:.4f})')
else:
    print('  kind 5: none, so cutting kind-5 exposure at the snapshot age changes nothing')
if hs:
    ed = hs[0]['edges']
    ex = np.sum([h['exposure'] for h in hs], 0); fd = np.sum([h['ends']['1'] for h in hs], 0)
    print('  hazard of a face death by age (relative to the pooled rate F/E):')
    tot = F / E
    i = 0
    while i < len(ex):                         # merge bins until each has >= 400 deaths
        j, e, f = i, 0, 0
        while j < len(ex) and (f < 400 or e == 0):
            e += ex[j]; f += fd[j]; j += 1
        if e > 0:
            print(f'    age {ed[i]:>11} - {ed[j]:<11}: deaths {int(f):6d}, hazard / mean = {f / e / tot:.3f} +- {math.sqrt(max(f, 1)) / e / tot:.3f}')
        i = j
if raws:
    R = np.concatenate(raws, axis=1)
    ages, kinds = R[0], R[1]
    mean = E / F
    G = np.mean([int(r['gens']) for r in rows])           # run length: a life born later than G - 8 means cannot reach 8
    print(f'  lives {len(ages)}; mean time to a face death per slab {mean:.4g}; runs {G / mean:.1f} means long; oldest life '
          f'{ages.max() / mean:.2f} means; lives older than 8 means: {int((ages > 8 * mean).sum())} (memoryless, allowing for '
          f'the end of the run: {len(ages) * math.exp(-8) * max(0, 1 - 8 * mean / G):.1f})')
