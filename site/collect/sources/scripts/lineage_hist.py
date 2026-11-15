#!/usr/bin/env python3
"""Series 5. Same selection as research/experiments/lineage_check.py ('structured' summary: struct kind,
de-duplicated by (kind, sig), reliable radii c>=31 / v>=32 with soup tau from >= 50 soup deaths, died plateaus only),
ratio T / tau_soup(centre, r). Cube plateaus: printed by research/experiments/cube_vs_ensemble.py (parsed here).
  python3 <dir>/lineage_hist.py <dir>/part_lineage.json      (from the repo root)
"""
import csv, gzip, sys, json, subprocess, re
rows = list(csv.DictReader(gzip.open('research/lineage/data/plateaus.csv.gz', 'rt')))
for r in rows:
    r['r'] = int(r['r']); r['T'] = float(r['T']); r['died'] = int(r['died']); r['idx'] = int(r['idx'])
keep = {}
for r in rows: keep.setdefault((r['kind'], r['sig']), r['tag'])
rows = [r for r in rows if keep[(r['kind'], r['sig'])] == r['tag']]
soup = [r for r in rows if r['kind'] == 'soup']; struct = [r for r in rows if r['kind'] == 'struct']
tau = {}
for key in {(r['centre'], r['r']) for r in soup}:
    rs = [r for r in soup if (r['centre'], r['r']) == key]; d = sum(r['died'] for r in rs)
    if d >= 50: tau[key] = sum(r['T'] for r in rs) / d
rel = lambda r: (r['centre'], r['r']) in tau and ((r['centre'] == 'c' and r['r'] >= 31) or (r['centre'] == 'v' and r['r'] >= 32))
def hist(rs):
    xs = [r['T'] / tau[(r['centre'], r['r'])] for r in rs if r['died'] and rel(r)]
    h = [0] * 25
    for x in xs: h[min(int(x / 0.25), 24)] += 1
    return xs, h
xs, h = hist(struct)
xo, ho = hist(soup)
out = subprocess.run(['python3', 'research/experiments/cube_vs_ensemble.py'], capture_output=True, text=True).stdout
cubes = [{"side": int(m[0]), "R": int(m[1]), "A": int(m[2]), "centre": m[3], "T": float(m[4]), "tau": float(m[5]), "ratio": float(m[6])}
         for m in re.findall(r'side (\d+)\s+R=\s*(\d+) A=(\d+) (\w):\s+T =\s+([\d.e+]+)\s+tau =\s+([\d.e+]+).*?T/tau =\s+([\d.]+)', out)]
assert len(cubes) == 16
res = {"bins": "width 0.25 from 0 to 6 (24 bins) + overflow bin [6, inf)",
       "structured": {"n": len(xs), "mean": round(sum(xs) / len(xs), 4), "counts": h, "max": round(max(xs), 3)},
       "soups_self_referenced": {"n": len(xo), "mean": round(sum(xo) / len(xo), 4), "counts": ho},
       "exp_expected_structured": [round(len(xs) * (__import__('math').exp(-0.25 * i) - __import__('math').exp(-0.25 * (i + 1))), 2) for i in range(24)]
                                   + [round(len(xs) * __import__('math').exp(-6), 2)],
       "cube_plateaus": cubes}
json.dump(res, open(sys.argv[1], 'w'), separators=(',', ':'))
print(len(xs), res['structured']['mean'], h, len(xo), res['soups_self_referenced']['mean'])
