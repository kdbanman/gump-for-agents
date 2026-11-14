#!/usr/bin/env python3
"""Curated numbers from the chunk files in research/scratch/thin into data/ (small, in git).

    python3 collect.py        # data/lifetimes.json (every tag), data/windows.json (E(l) of the tags with samples)
"""
import glob, json, math, os
import numpy as np
import run as R, analyze as A

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
life = {}; wins = {}
for d in sorted(glob.glob(os.path.join(R.OUT, '*', ''))):
    tag = os.path.basename(d.rstrip('/'))
    acc = R.load(tag)
    if acc is None:
        continue
    lt, er, F, excess = R.lntau(acc, full=True); h = acc['head']; t = acc['tot']
    life[tag] = dict(mode=h['mode'], b=int(h['b']), layers=int(h['layers']), wall=int(h.get('notch', 0)), rho16=int(h['rho16']),
                     T0=int(h['T0']), twist=int(h.get('twist', 1)), chunks=acc['n'], deaths=F, left_out=excess, lntau=None if F == 0 else round(lt, 5),
                     err=None if F == 0 else round(er, 5), settled=int(t['settled']), firewalls=int(t['interior']),
                     both_faces=int(t['both']), face_samples=t['nsamp'])
    if t['nsamp'] > 0:
        cs = A.chunks(tag); b = int(h['b'])
        hp = sum(c['hpop'] for c in cs); dp = sum(c['dpop'] for c in cs)
        pre = sum(c['pre'] for c in cs); npre = sum(c['tot']['npre'] for c in cs)
        le, ee, k, ke = A.win(tag, quiet=True)
        n = np.arange(len(hp))
        wins[tag] = dict(b=b, face_samples=t['nsamp'], lnE=[None if not np.isfinite(x) else round(float(x), 5) for x in le],
                         lnE_err=[None if not np.isfinite(x) else round(float(x), 5) for x in ee],
                         mean_pop=float((hp * n).sum() / hp.sum()), hpop=[int(x) for x in hp], dpop=[int(x) for x in dp],
                         pre_death_pop=[round(float(x / npre), 3) for x in pre] if npre else None,
                         hrun=[int(x) for x in sum(c['hrun'] for c in cs)], hmax=[int(x) for x in sum(c['hmax'] for c in cs)])
        for key in ('hfl', 'hfr'):
            if all(key in c for c in cs):
                wins[tag][key] = [int(x) for x in sum(c[key] for c in cs)]
json.dump(life, open(os.path.join(HERE, 'data', 'lifetimes.json'), 'w'), indent=1, sort_keys=True)
json.dump(wins, open(os.path.join(HERE, 'data', 'windows.json'), 'w'), sort_keys=True)
print(f'{len(life)} tags, {len(wins)} with face samples')
