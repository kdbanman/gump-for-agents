#!/usr/bin/env python3
"""Pool the PRE lines of several `tube1d bandp` runs: share of band-emptying events with a one-generation fall of at
least half the band's cells in the band's last 9 generations, by width; s.e. over the runs.
    python3 bandboom.py FILE1 FILE2 ..."""
import sys, statistics as st
agg = {}
for fn in sys.argv[1:]:
    for l in open(fn):
        if l.startswith('PRE ') and 'fall>=half:' in l:
            p = l.split(); w = float(p[1]); n = float(p[2]); sh = float(p[9]); a = agg.setdefault(w, [0, 0, []]); a[0] += n; a[1] += n * sh; a[2].append(sh)
print("width (units): share pooled +- s.e. over runs (events)")
for w, a in sorted(agg.items()):
    print(f"  {w:4.1f}: {a[1]/a[0]*100:5.1f} +- {(st.stdev(a[2])/len(a[2])**0.5*100 if len(a[2])>1 else 0):4.1f} %  ({a[0]:.0f})")
