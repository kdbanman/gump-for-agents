"""Depth series at 63 cells (eps 1/4): the watched face's ln tau minus gump's, coins at depth >= d under it.
Rows: data/brute/lead_depth_d*.txt (this directory's nb.c; sh research/audit/blastnoisy/depth.sh) beside the
author's research/blast/noisy/data/depth.txt (its nz.c, other seeds)."""
import glob, math, os, re
H = os.path.dirname(os.path.abspath(__file__)); GUMP = 13.633
auth = {}
for l in open(os.path.join(H, '../../blast/noisy/data/depth.txt')):
    g = l.split(); k = dict(zip(g[1::2], g[2::2])) if g and g[0] == 'BRUTE' else None
    m = re.search(r'DW (\d+) .* nN (\d+) .* M (\d+) .* exposure (\S+) .* watched (\d+) ', l)
    if m: auth[int(m.group(1))] = (int(m.group(2)), int(m.group(3)), float(m.group(4)), int(m.group(5)))
print('  d   nN    M   | nb.c: deaths  ln tau - gump       | nz.c: deaths  ln tau - gump       | difference')
for d in (6, 5, 4, 3, 2, 1):
    f = glob.glob(os.path.join(H, 'data/brute', f'lead_depth_d{d}_s*.txt'))
    g = open(f[0]).read().split(); k = dict(zip(g[2::2][:12], g[3::2][:12]))
    E = float(g[g.index('exposure') + 1]); d0 = int(g[g.index('d') + 1]); nN = int(g[g.index('nN') + 1]); M = int(g[g.index('M') + 1])
    a = auth[d]; assert (nN, M) == a[:2], (d, nN, M, a)
    x = math.log(E / d0) - GUMP; ex = 1 / math.sqrt(d0); y = math.log(a[2] / a[3]) - GUMP; ey = 1 / math.sqrt(a[3])
    print(f'  {d}  {nN:4d} {M:4d}   |  {d0:6d}     {x:+.3f} +- {ex:.3f}     |  {a[3]:6d}     {y:+.3f} +- {ey:.3f}     | {x - y:+.3f} +- {math.hypot(ex, ey):.3f}')
