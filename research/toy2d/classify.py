"""Classify the strip screen (screen.py output) into behaviour classes and print the candidate table.

python3 classify.py research/scratch/toy2d/screen_moore_*.jsonl [--csv OUT]
Classes (strip W = 10, L = 12 and 20, 20000 generations x 256 replicas):
  settle   : most replicas settle (period <= 4096) before anything else           (settles > 2 x other events)
  frozen   : the edge rows freeze (non-period-2 activity in edge rows < 0.02)       ("walled cities")
  firewall : interior firewalls outnumber edge deaths
  erode    : edges die but tau_edge(20) / tau_edge(12) < e (no exponential cost of length)
  quiet    : no event of any kind at L = 20 (and the bulk is not frozen) -- lifetime beyond reach
  EDGE     : active edges that die, tau growing at least e-fold from L = 12 to 20: the gump-like class
"""
import json, math, sys
import numpy as np

files = [a for a in sys.argv[1:] if not a.startswith('--')]
csv = sys.argv[sys.argv.index('--csv') + 1] if '--csv' in sys.argv else None
if csv in files:
    files.remove(csv)
R = [json.loads(l) for f in files for l in open(f)]


def cls(r):
    a, b = r['12'], r['20']
    ev20 = b['edge_deaths'] + b['firewalls']
    if b['settles'] > 2 * ev20 and b['settles'] > 20:
        return 'settle'
    if (b['act_edge'] or 0) < 0.02:
        return 'frozen'
    if b['firewalls'] > b['edge_deaths']:
        return 'firewall'
    if ev20 == 0 and b['settles'] <= 20:
        return 'quiet'
    t12 = a['tau_edge'] or 0; t20 = b['tau_edge'] or float('inf')
    if t12 and t20 / t12 < math.e:
        return 'erode'
    return 'EDGE'


rows = []
for r in R:
    c = cls(r)
    t12 = r['12']['tau_edge']; t20 = r['20']['tau_edge']
    slope = (math.log(t20) - math.log(t12)) / 8 if t12 and t20 else float('nan')
    rows.append(dict(rule=r['rule'], cls=c, p=r['p'], tau12=t12, tau20=t20, slope=slope,
                     act_bulk=r['20']['act_bulk'], act_edge=r['20']['act_edge'], edge_dens=r['20']['edge_mean'],
                     edge20=r['20']['edge_deaths'], fw20=r['20']['firewalls'], settle20=r['20']['settles']))
from collections import Counter
print('classes:', dict(Counter(x['cls'] for x in rows)), 'of', len(rows))
E = sorted([x for x in rows if x['cls'] == 'EDGE'], key=lambda x: -x['slope'] if x['slope'] == x['slope'] else 0)
print('%-20s %5s %9s %9s %6s %6s %6s %6s %5s %4s %5s' % ('rule', 'p', 'tau12', 'tau20', 'slope', 'actB', 'actE', 'rhoE', 'edgeD', 'fw', 'sett'))
for x in E:
    print('%-20s %5.2f %9.3g %9.3g %6.3f %6.3f %6.3f %6.3f %5d %4d %5d' % (x['rule'], x['p'], x['tau12'] or 0, x['tau20'] or 0, x['slope'],
          x['act_bulk'], x['act_edge'], x['edge_dens'] or 0, x['edge20'], x['fw20'], x['settle20']))
if csv:
    import csv as C
    with open(csv, 'w', newline='') as f:
        w = C.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); [w.writerow(x) for x in sorted(rows, key=lambda x: (x['cls'], x['rule']))]
