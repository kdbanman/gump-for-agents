#!/usr/bin/env python3
"""Item 3 of the third task: the 84-cell face on coins alone (full replacement, DO = 1) at p = 0.385, chunks pooled.

    python3 research/blast/density/pool84.py [DIR ...]       (row files R13_fullDO1_p0.385_s*.txt; default data/rows)

Pools exposure and deaths of the watched face over the chunks run with the hashed second stream (seeds >= 20000,
binary nzd_fix) and, separately, over the earlier chunks (seeds 8885, 8890-8892, binary nzd_prod4, whose adjacent seeds
share the coin stream). Delta = ln tau - 18.141 +- 0.005 (gump's 84-cell face, research/blast/noisy/README.md; all
faces, ties included). Also the share of descents to <= 1 cell that die (REC k = 1).
"""
import glob, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or [os.path.join(HERE, 'data', 'rows')]
seen = {}
for d in dirs:
    for f in glob.glob(os.path.join(d, 'R13_fullDO1_p0.385_s*.txt')):
        seen.setdefault(os.path.basename(f), f)
G = (18.141, 0.005)
for name, test in (('hashed stream (seeds >= 20000)', lambda s: s >= 20000), ('old stream (8885, 8890-)', lambda s: s < 20000)):
    E = 0; n = 0; N1 = 0; D1 = 0; k = 0
    for b, f in sorted(seen.items()):
        s = int(re.search(r'_s(\d+)\.txt', b).group(1))
        if not test(s): continue
        t = open(f).read()
        E += float(re.search(r'exposure ([0-9.e+]+)', t).group(1)); n += int(re.search(r' watched (\d+)', t).group(1)); k += 1
        rec = re.search(r' 1:(\d+)/(\d+)/', t); N1 += int(rec.group(1)); D1 += int(rec.group(2))
    if not n: continue
    v = math.log(E / n); e = 1 / math.sqrt(n)
    print(f'{name}: {k} chunks, exposure {E:.4e}, {n} deaths: ln tau {v:.4f} +- {e:.4f}, Delta {v - G[0]:+.4f} +- {math.hypot(e, G[1]):.4f}; '
          f'death from one cell {D1}/{N1} = {D1 / N1:.3f}')
