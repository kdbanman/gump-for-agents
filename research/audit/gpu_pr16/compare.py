#!/usr/bin/env python3
"""PR 16 review: the A = 72 pair 3x8x8 / 4x6x8 from independent CPU histories (rep.c via gpu_pr14/cpu_channels.py run),
channel-resolved truth (T) and with fwslab.py's detection rules at the GPU's launch cap (G); against the GPU and the CPU
table research/peeling/slab_fw.csv. Also the face hazard in equal-exposure age thirds (T).
  python3 research/audit/gpu_pr16/compare.py <dir with the PR's fwslab*.json>
"""
import csv, glob, json, math, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr14')
GPU = sys.argv[1]
tab = {(int(r['N1']), int(r['N2'])): r for r in csv.DictReader(open(os.path.join(ROOT, 'research/peeling/slab_fw.csv'))) if r['m'] == '8'}
res = {}
for (N1, N2, K) in ((3, 8, 2048), (4, 6, 65536), (3, 6, 2048)):
    fs = sorted(glob.glob(f'{OUT}/ch_{N1}x{N2}x8_s1[46]*.npz'))
    if not fs: continue
    z = [np.load(f) for f in fs]
    assert len({int(x['seed']) for x in z}) == len(z)
    face = np.concatenate([x['face'] for x in z]).astype(float); fw = np.concatenate([x['fw'] for x in z]).min(1).astype(float)
    st = np.concatenate([x['settle'] for x in z]); ge = np.concatenate([np.full(len(x['face']), int(x['gen_end'])) for x in z])
    stop = np.where(st >= 0, st, ge).astype(float)
    end = np.minimum.reduce([face, fw, stop])
    kF = (face == end) & (face < fw) & (face <= stop); kW = (fw == end) & (fw <= face) & (fw <= stop)
    E = end.sum(); F = kF.sum(); W = kW.sum()
    B = np.ceil(fw / K) * K; det = np.where(face <= B, face, B)
    gW = kW & ~(stop < det); gS = kW & (stop < det)
    endG = np.where(kF, face, np.where(gW, det, np.where(gS, stop, end))); EG = endG.sum()
    yT = math.log(2 * E / F); yG = math.log(2 * EG / F); se = 1 / math.sqrt(F)
    g = [json.load(open(p)) for p in glob.glob(f'{GPU}/fwslab{N1}x{N2}x8_s*.json') if json.load(open(p)).get('max_launch') == K]
    yg = math.log(2 * sum(r['exposure'] for r in g) / sum(r['face'] for r in g)); seg = 1 / math.sqrt(sum(r['face'] for r in g))
    t = tab.get((N1, N2)); yt = math.log(2 * float(t['exposure']) / int(t['peel_first'])); set_ = 1 / math.sqrt(int(t['peel_first']))
    print(f'{N1}x{N2}x8: {len(z)} runs, {len(face)} lives; face {F}, firewall {W} ({W/(F+W):.1%}), censored {len(face)-F-W}')
    print(f'   (T) ln tau_face {yT:.3f} ± {se:.3f}, ln tau_fw {math.log(E/W):.3f} ± {1/math.sqrt(W):.3f};  (G, K={K}) {yG:.3f} (G-T {yG-yT:+.4f})')
    print(f'   GPU (cap {K}) {yg:.3f} ± {seg:.3f}: GPU - CPU(G) {yg-yG:+.3f} ± {math.hypot(se,seg):.3f};  CPU table {yt:.3f} ± {set_:.3f}')
    # face hazard in equal-exposure thirds of age (truth)
    srt = np.sort(end); cs = np.concatenate([[0], np.cumsum(srt)])
    expo = lambda T: cs[np.searchsorted(srt, T)] + T * (len(srt) - np.searchsorted(srt, T))
    ts = [0]
    for q in (1 / 3, 2 / 3):
        lo, hi = 0, srt[-1] + 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            lo, hi = (m, hi) if expo(m) < q * E else (lo, m)
        ts.append(hi)
    ts.append(srt[-1] + 1)
    th = []
    for a, b in zip(ts, ts[1:]):
        f = (kF & (face >= a) & (face < b)).sum(); e = expo(b) - expo(a)
        th.append(f'[{a:.2g},{b:.2g}) {math.log(2*e/f):.3f}±{1/math.sqrt(f):.3f}')
    print('   face hazard by age thirds (T):', '; '.join(th))
    res[(N1, N2)] = (yT, yG, se, yg, seg, yt, set_)
if (3, 8) in res and (4, 6) in res:
    a, b = res[(3, 8)], res[(4, 6)]
    print(f'\n3x8x8 - 4x6x8: CPU (T) {a[0]-b[0]:+.3f} ± {math.hypot(a[2],b[2]):.3f}; CPU (G) {a[1]-b[1]:+.3f}; GPU {a[3]-b[3]:+.3f} ± {math.hypot(a[4],b[4]):.3f}; CPU table {a[5]-b[5]:+.3f} ± {math.hypot(a[6],b[6]):.3f}')
