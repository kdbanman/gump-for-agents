#!/usr/bin/env python3
"""The equivalent coin density p*: where coins of density p at every replaced depth give the watched face gump's life.

    python3 research/blast/density/zeros.py [DIR ...]       (row files; default data/rows)

Rows with one bias at every depth (scan_*, e4_*, e16_*, full_*, R9_*) are grouped by face size and replacement
(eps = M/B with darts, or "full" = NZD_FULL=1). For each group: Delta = ln tau - gump (63 cells: 13.633 +- 0.001;
45 cells: gump's watched face, nz's 9.8161 +- 0.0044 pooled with this directory's R9_gump rows), +- from death counts.
p* from a weighted straight line through the rows with |Delta| < WIN (default 0.2; at least the two rows that
bracket the zero), its error by the delta method from the fit's covariance (the gump reference's error added to
every row). Also the slope dDelta/dp there.
"""
import glob, math, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or [os.path.join(HERE, 'data', 'rows')]
WIN = float(os.environ.get('WIN', '0.2'))
rows = []; seen = set()
for d in dirs:
    for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
        if os.path.basename(f) in seen: continue
        seen.add(os.path.basename(f)); t = open(f).read()
        if '\nREC' not in '\n' + t: continue
        br = [l for l in t.splitlines() if l.startswith('BRUTE')][0]
        bias = [l for l in t.splitlines() if l.startswith('BIAS')][0]
        A = int(re.search(r' A (\d+)', br).group(1)); M = int(re.search(r' M (\d+)', br).group(1)); B = int(re.search(r' B (\d+)', br).group(1))
        DW = int(re.search(r' DW (\d+)', br).group(1))
        E = float(re.search(r'exposure ([0-9.e+]+)', br).group(1)); n0 = int(re.search(r' watched (\d+)', br).group(1))
        full = ' full 1 ' in bias; frozen = ' frozen 1 ' in bias
        vals = re.findall(r'\d+\(\d+\):([0-9.]+|s|c[0-9./]+)', bias)
        rows.append(dict(f=os.path.basename(f), A=A, M=M, B=B, DW=DW, E=E, n0=n0, full=full, frozen=frozen, vals=vals))
# gump references
g45 = [(9.8161, 0.0044)]
for r in rows:
    if r['A'] == 45 and r['M'] == 0 and not r['full'] and not r['frozen']:
        g45.append((math.log(r['E'] / r['n0']), 1 / math.sqrt(r['n0'])))
w = sum(1 / e ** 2 for v, e in g45); G = {63: (13.633, 0.001), 45: (sum(v / e ** 2 for v, e in g45) / w, 1 / math.sqrt(w))}
print(f'gump references: 63 cells {G[63][0]:.4f} +- {G[63][1]:.4f}; 45 cells {G[45][0]:.4f} +- {G[45][1]:.4f} (pooled from {len(g45)})')
groups = defaultdict(list)
for r in rows:
    if r['M'] == 0 and not r['full'] or r['frozen'] or r['DW'] != 1: continue
    if len(set(r['vals'])) != 1 or not re.match(r'^[0-9.]+$', r['vals'][0]): continue
    key = (r['A'], 'full' if r['full'] else f'eps {r["M"] / r["B"]:.4f}')
    v = math.log(r['E'] / r['n0']); g, ge = G[r['A']]
    groups[key].append((float(r['vals'][0]), v - g, math.hypot(1 / math.sqrt(r['n0']), ge), r['f'], r['n0']))
for key in sorted(groups):
    pts = sorted(groups[key])
    print(f'\n{key[0]} cells, {key[1]}:')
    for p, D, e, f, n in pts:
        print(f'   p {p:.4f}  Delta {D:+.4f} +- {e:.4f}  ({n} deaths, {f})')
    sel = [x for x in pts if abs(x[1]) < WIN]
    br = [i for i in range(len(pts) - 1) if pts[i][1] < 0 <= pts[i + 1][1]]
    if br:
        i = br[0]
        for x in (pts[i], pts[i + 1]):
            if x not in sel: sel.append(x)
    if len(sel) < 2:
        print('   no zero bracketed'); continue
    S = sum(1 / e ** 2 for p, D, e, *_ in sel); Sx = sum(p / e ** 2 for p, D, e, *_ in sel); Sy = sum(D / e ** 2 for p, D, e, *_ in sel)
    Sxx = sum(p * p / e ** 2 for p, D, e, *_ in sel); Sxy = sum(p * D / e ** 2 for p, D, e, *_ in sel)
    det = S * Sxx - Sx * Sx; b = (S * Sxy - Sx * Sy) / det; a = (Sy - b * Sx) / S
    va, vb, cab = Sxx / det, S / det, -Sx / det
    ps = -a / b; dpa, dpb = -1 / b, a / b ** 2
    eps_ = math.sqrt(dpa ** 2 * va + dpb ** 2 * vb + 2 * dpa * dpb * cab)
    chi = sum((D - a - b * p) ** 2 / e ** 2 for p, D, e, *_ in sel)
    print(f'   line through {len(sel)} rows (p {min(x[0] for x in sel):.3f} .. {max(x[0] for x in sel):.3f}): '
          f'p* = {ps:.4f} +- {eps_:.4f}, slope {b:.2f} +- {math.sqrt(vb):.2f} per unit p, chi2 {chi:.2f} on {len(sel) - 2}')
