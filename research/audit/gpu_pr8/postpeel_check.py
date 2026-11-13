#!/usr/bin/env python3
"""Re-derive PR 8's post-peel numbers and look at what the 'aftershock' is made of.
  python3 research/audit/gpu_pr8/postpeel_check.py PR8_WORKTREE"""
import json, math, os, sys
import numpy as np
root = sys.argv[1]
TAU = {36: 2.247e6, 38: 1.254e7}          # the PR's stationary values (fresh soups, T0 = 1000)
for f, Ra in (('postpeel_vR38_s302.json', 36), ('postpeel_vR40_s301.json', 38)):
    r = json.load(open(os.path.join(root, 'research/data/gpu_facelaw', f)))
    w = np.array(r['waits'], float); k = np.array(r['kinds'])
    tau = TAU[Ra]
    died = k == 1
    print(f"{f}: states {len(w)}, kinds {dict(zip(*np.unique(k, return_counts=True)))}")
    keep = (k == 1) | (k == 0)
    tp = w[keep].sum() / died.sum()
    print(f"  mean post-peel wait / tau({Ra}v) = {tp / tau:.4f} +- {tp / tau / math.sqrt(died.sum()):.4f}")
    x = w / tau
    for lo, hi in ((0, 1e-5), (1e-5, 1e-4), (1e-4, 1e-3), (1e-3, 1e-2), (1e-2, 2e-2), (2e-2, 5e-2)):
        e = np.clip(np.minimum(x[keep], hi) - lo, 0, None).sum()
        d = int((died & (x >= lo) & (x < hi)).sum())
        print(f"   [{lo:g},{hi:g}) tau: deaths {d:4d}, expected at the stationary rate {e:7.1f}")
    print('   smallest waits (generations):', np.sort(w[died])[:25].astype(int).tolist())
