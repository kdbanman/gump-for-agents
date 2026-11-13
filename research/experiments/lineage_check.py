"""Lead's independent check of research/lineage (2026-11-13). Shares no code with research/lineage/analyze.py.

Reads only research/lineage/data/plateaus.csv.gz. The reference lifetime at each (centre, radius) is taken from
the soup lineages in that same file (exposure / deaths, censored rows counted in the exposure), not from the
orbit-stepper ensembles. Structured lineages are de-duplicated by their schedule signature.

    python3 research/experiments/lineage_check.py
"""
import csv, gzip, math, collections, random

rows = list(csv.DictReader(gzip.open('research/lineage/data/plateaus.csv.gz', 'rt')))
for r in rows:
    r['r'] = int(r['r']); r['T'] = float(r['T']); r['died'] = int(r['died']); r['idx'] = int(r['idx'])
kinds = collections.Counter(r['kind'] for r in rows)
print('rows', len(rows), dict(kinds))

# one tag per signature
keep = {}
for r in rows:
    keep.setdefault((r['kind'], r['sig']), r['tag'])
rows = [r for r in rows if keep[(r['kind'], r['sig'])] == r['tag']]
print('after de-duplication', len(rows), 'lineages', len({(r['kind'], r['tag']) for r in rows}))

soup = [r for r in rows if r['kind'] == 'soup']
struct = [r for r in rows if r['kind'] == 'struct']
tau = {}
for key in sorted({(r['centre'], r['r']) for r in soup}):
    rs = [r for r in soup if (r['centre'], r['r']) == key]
    d = sum(r['died'] for r in rs)
    if d >= 50:
        tau[key] = (sum(r['T'] for r in rs) / d, d)
print('soup tau_e:', {f'{k[1]}{k[0]}': (round(v[0]), v[1]) for k, v in tau.items()})

def reliable(r):
    return (r['centre'], r['r']) in tau and ((r['centre'] == 'c' and r['r'] >= 31) or (r['centre'] == 'v' and r['r'] >= 32))

def summary(name, rs):
    xs = [r['T'] / tau[(r['centre'], r['r'])][0] for r in rs if r['died']]
    n = len(xs); m = sum(xs) / n
    cv = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)) / m
    expo = sum(r['T'] / tau[(r['centre'], r['r'])][0] for r in rs)       # censored rows included
    print(f'{name:28s} n={n:5d} mean={m:.3f} CV={cv:.2f}  exposure/deaths={expo / n:.3f}  '
          f'>4tau {sum(x > 4 for x in xs)} (exp {n * math.exp(-4):.1f})  <0.05tau {sum(x < .05 for x in xs)} (exp {n * (1 - math.exp(-.05)):.1f})')
    return xs

xs = summary('structured', [r for r in struct if reliable(r)])
summary('structured, first plateau', [r for r in struct if reliable(r) and r['idx'] == 0])
summary('structured, after a peel', [r for r in struct if reliable(r) and r['idx'] > 0])
xo = summary('soups (self-referenced)', [r for r in soup if reliable(r)])
for key in sorted(tau):
    rs = [r for r in struct if (r['centre'], r['r']) == key and reliable(r)]
    d = sum(r['died'] for r in rs)
    if d >= 30:
        ratio = sum(r['T'] for r in rs) / d / tau[key][0]
        se = math.sqrt(1 / d + 1 / tau[key][1])
        print(f'  {key[1]}{key[0]}: structured tau / soup tau = {ratio:.2f}  (x/ {math.exp(2 * se):.2f} at 2 sigma; {d} and {tau[key][1]} deaths)')

# two-sample Kolmogorov-Smirnov, structured vs soups
a, b = sorted(xs), sorted(xo)
i = j = 0; D = 0.0
while i < len(a) and j < len(b):
    if a[i] <= b[j]: i += 1
    else: j += 1
    D = max(D, abs(i / len(a) - j / len(b)))
en = math.sqrt(len(a) * len(b) / (len(a) + len(b)))
lam = (en + 0.12 + 0.11 / en) * D
p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 101))
print(f'KS structured vs soups: D={D:.4f} p={min(1, p):.2f}')

# memory from one plateau to the next (Spearman over consecutive pairs of one lineage)
def rank(v):
    o = sorted(range(len(v)), key=lambda k: v[k]); rk = [0.0] * len(v)
    for pos, k in enumerate(o): rk[k] = pos
    return rk
def spearman(rs):
    by = collections.defaultdict(dict)
    for r in rs:
        if r['died'] and reliable(r):
            by[r['tag']][r['idx']] = r['T'] / tau[(r['centre'], r['r'])][0]
    u, v = [], []
    for d in by.values():
        for k in d:
            if k + 1 in d: u.append(d[k]); v.append(d[k + 1])
    ru, rv = rank(u), rank(v); n = len(u); mu = (n - 1) / 2
    rho = sum((x - mu) * (y - mu) for x, y in zip(ru, rv)) / sum((x - mu) ** 2 for x in ru)
    return rho, n
for name, rs in (('structured', struct), ('soups', soup)):
    rho, n = spearman(rs)
    print(f'consecutive plateaus, {name}: Spearman rho={rho:+.3f} over {n} pairs (1 sigma = {1 / math.sqrt(n):.3f})')

# how unusual are the cubes' 3 of 16 beyond 4 tau, against the structured sample itself?
k = sum(x > 4 for x in xs); n = len(xs); random.seed(1); hits = 0; N = 200000
for _ in range(N):
    hits += sum(random.random() < k / n for _ in range(16)) >= 3
print(f'P(>=3 of 16 beyond 4tau | rate {k}/{n}) = {hits / N:.4f}')
