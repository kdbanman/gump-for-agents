#!/usr/bin/env python3
"""Numbers derived from the pooled sampler results (slopes of the tube, tube against wide, wide against the wide line).   python3 derived.py"""
import glob, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
pool = {}
for f in glob.glob(os.path.join(HERE, 'data', 'sub_*_s*.txt')):
    H, K, D, seed = map(int, re.match(r'sub_(\d+)_(\d+)_(\d+)_s(\d+).txt', os.path.basename(f)).groups())
    pool.setdefault((H, K, D), []).extend(float(l.split('rate')[1].split()[0]) for l in open(f) if l.startswith('REP') and 'rate' in l)
res = {}
for L, r in pool.items():
    n = len(r); m = sum(r) / n; sd = math.sqrt(sum((x - m) ** 2 for x in r) / (n - 1)); ln = [-math.log(x) for x in r if x > 0]
    mu = sum(ln) / len(ln); s2 = sum((x - mu) ** 2 for x in ln) / (len(ln) - 1)
    # error if the replications were lognormal with the observed log-sd (the sample sd misses the tail)
    res[L] = (-math.log(m), sd / m / math.sqrt(n), n, math.sqrt(s2), math.sqrt((math.exp(s2) - 1) / n))
    print(f'{L} A={3 * L[0] * L[2]}: {res[L][0]:.3f} ± {res[L][1]:.3f} ({n} replications; sd of ln(rate) between replications {res[L][3]:.2f}; lognormal error {res[L][4]:.3f})')
wide = lambda A: 13.1622 + 0.20866 * (A - 63)
def sl(a, b):
    A1, A2 = 3 * a[0] * a[2], 3 * b[0] * b[2]
    return (res[b][0] - res[a][0]) / (A2 - A1), math.hypot(res[a][1], res[b][1]) / (A2 - A1), math.hypot(res[a][4], res[b][4]) / (A2 - A1)
T = [(1, 12, 28), (1, 16, 36), (1, 18, 40), (1, 22, 48), (1, 30, 64)]
for a, b in [(T[1], T[4]), (T[1], T[2]), (T[2], T[3]), (T[3], T[4]), (T[2], T[4])]:
    if a in res and b in res:
        s = sl(a, b); print(f'tube slope {3 * a[2]} -> {3 * b[2]} cells: {s[0]:.4f} ± {s[1]:.4f} (lognormal error {s[2]:.4f})')
for t, w in [((1, 16, 36), (6, 0, 6)), ((1, 22, 48), (4, 4, 12)), ((1, 30, 64), (8, 0, 8))]:
    if t in res and w in res:
        A = 3 * t[2]
        print(f'{A} cells: wide - tube = {res[w][0] - res[t][0]:.2f} ± {math.hypot(res[w][1], res[t][1]):.2f} (lognormal {math.hypot(res[w][4], res[t][4]):.2f}); wide - wide line {wide(A):.2f} = {res[w][0] - wide(A):+.2f} ± {res[w][1]:.2f} (lognormal {res[w][4]:.2f})')
