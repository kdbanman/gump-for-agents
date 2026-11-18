#!/usr/bin/env python3
"""Table of the brute-force runs of nb (the last RES line of every file), pooled by size and M.

    python3 research/audit/blastnoisy/brute.py [DIR ...]     (default: research/scratch/audit_noisy/brute and
                                                               this directory's data/brute)
Columns: watched = ln(exposure / d0) with error 1/sqrt(d0) (lives ended by the watched face, alone or tied);
others = ln(7 exposure / (d1 + ... + d7)); minus gump = minus the anchor of that size (the lead's, from fd.c:
13.633 +- 0.001, 18.141 +- 0.005, 23.3392 +- 0.0099; 45 cells: this code at M = 0, all eight faces).
"""
import glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or [os.path.join(HERE, '..', '..', 'scratch', 'audit_noisy', 'brute'), os.path.join(HERE, 'data', 'brute')]
ANCH = {63: (13.633, 0.001), 84: (18.141, 0.005), 108: (23.3392, 0.0099)}
rows = {}
seen = set()
for d in dirs:
    for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
        if os.path.basename(f) in seen:
            continue
        seen.add(os.path.basename(f))
        last = None
        for line in open(f):
            if line.startswith('RES'):
                last = line.split()
        if not last:
            continue
        g = dict(zip(last[1:19:2], last[2:20:2]))
        dd = [int(x) for x in last[20:28]]
        key = (int(g['A']), int(g['M']), g['mode'])
        r = rows.setdefault(key, dict(E=0, d=[0] * 8, ties=0, settled=0, B=int(g['B']), nN=int(g['nN']), files=0, gens=0))
        r['E'] += int(g['exposure']); r['d'] = [a + b for a, b in zip(r['d'], dd)]
        r['ties'] += int(last[29]); r['settled'] += int(last[33]); r['files'] += 1; r['gens'] += int(g['gens'])
for A in sorted({k[0] for k in rows}):
    if (A, 0, 'F') in rows and A not in ANCH:
        r = rows[(A, 0, 'F')]
        ANCH[A] = (math.log(8 * r['E'] / sum(r['d'])), 1 / math.sqrt(sum(r['d'])))
print('cells   eps      M mode runs  generations   exposure   watched deaths (ties)   ln tau watched       minus gump          '
      'ln tau others (7 faces)   minus gump          settled')
for key in sorted(rows):
    A, M, mode = key; r = rows[key]; E = r['E']; d0 = r['d'][0]; do = sum(r['d'][1:])
    if not d0 or not do:
        continue
    lw = math.log(E / d0); ew = 1 / math.sqrt(d0); lo = math.log(7 * E / do); eo = 1 / math.sqrt(do)
    a = ANCH.get(A)
    s = f"{A:5d} {M / r['B']:8.5f} {M:5d}  {mode}   {r['files']:3d}  {r['gens']:11d}  {E:.3e}   {d0:7d} ({r['ties']:4d})      {lw:8.4f} +- {ew:.4f}"
    s += f"   {lw - a[0]:+.4f} +- {math.hypot(ew, a[1]):.4f}" if a else ' ' * 22
    s += f"   {lo:8.4f} +- {eo:.4f}     "
    s += f"   {lo - a[0]:+.4f} +- {math.hypot(eo, a[1]):.4f}" if a else ' ' * 22
    print(s + f"   {r['settled']}")
print('anchors used: ' + ', '.join(f'{A} cells {v[0]:.4f} +- {v[1]:.4f}' for A, v in sorted(ANCH.items())))
