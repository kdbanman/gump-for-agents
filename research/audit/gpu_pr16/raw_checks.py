#!/usr/bin/env python3
"""PR 16 review: per-life checks where `raw` exists. Firewall lives ended at a launch boundary (age a multiple of 1024,
since every launch length is a multiple of 1024 and births are at boundaries) against those ended at a face death on a
firewalled state; an upper bound on the exposure counted after a firewall formed (boundary-detected lives: <= one launch
each; at-death lives: the firewall->face lag, unknown, bounded by the launch); and the face hazard in equal-exposure age
thirds.   python3 research/audit/gpu_pr16/raw_checks.py <dir with fwslab*.json>
"""
import base64, glob, json, math, sys, zlib
import numpy as np
D = sys.argv[1]
for p in sorted(glob.glob(f'{D}/fwslab*.json')):
    r = json.load(open(p))
    if 'raw' not in r: continue
    a, k, b, dr = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), np.int64).reshape(r['raw']['shape'])
    K = r.get('max_launch', 1 << 18)
    w = k == 4; bd = w & (a % 1024 == 0); dd = w & ~bd
    E = a.sum(); F = (k == 1).sum()
    ub = bd.sum() * K + dd.sum() * K          # crude upper bound on post-firewall exposure
    half = bd.sum() * K / 2                    # uniform formation within the last launch
    # equal-exposure thirds of age
    order = np.argsort(a); 
    edges = []
    # exposure as a function of age threshold t: sum(min(a,t)); find t1,t2 at 1/3,2/3
    srt = np.sort(a); cs = np.concatenate([[0], np.cumsum(srt)])
    def expo(t):
        i = np.searchsorted(srt, t); return cs[i] + t * (len(srt) - i)
    lo, hi = 0, int(srt[-1]) + 1
    ts = []
    for q in (1 / 3, 2 / 3):
        l, h = 0, hi
        while h - l > 1:
            m = (l + h) // 2
            if expo(m) < q * E: l = m
            else: h = m
        ts.append(h)
    cuts = [0] + ts + [hi]
    thirds = []
    for t0, t1 in zip(cuts, cuts[1:]):
        e = expo(t1) - expo(t0); f = ((k == 1) & (a >= t0) & (a < t1)).sum()
        thirds.append(f'[{t0:.2g},{t1:.2g}) {math.log(2*e/f):.3f}±{1/math.sqrt(f):.3f}' if f else f'[{t0:.2g},{t1:.2g}) no deaths')
    print(f'{r["slab"]} K={K}: fw lives {w.sum()}: at boundary {bd.sum()}, at a face death {dd.sum()}; '
          f'post-firewall exposure <= {half/E:.2%} (K/2 per boundary life) / {ub/E:.2%} (K per life) '
          f'-> ln tau_face bias <= {-math.log(1-half/E):+.4f} / {-math.log(1-ub/E):+.4f}; face hazard by age thirds: ' + '; '.join(thirds))
