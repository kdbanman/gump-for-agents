"""Lead's check of GPU pull request 20 (zombie lives): two bounds recomputed from the committed logs.

    python3 research/audit/gpu_pr20_lead_check.py

For R11 (A = 63) and R13 (A = 84), from research/data/gpu_facelaw/*.json alone and sharing no code with
research/gpu/zombies.py: the hazard h = deaths / exposure over all age bins; the deaths in bins whose lower edge is at
or above k mean lives against h x their exposure; an upper bound on exposure that produced no deaths there
(exposure - exact one-sided 95% Poisson lower bound on the deaths / h), as a fraction of all exposure; and the same
scaled by (1 - a/G)^-2 for zombies born at a constant rate (derivation: a zombie born at t carries G - t of exposure,
of which G - t - a lies above age a; integrate over t). Also printed: the oldest age on record, in mean lives, next to
ln(lives), where memoryless lives put it. The Poisson bound here is exact (bisection on the Poisson tail), the pull
request's is the Wilson-Hilferty approximation: they should agree to a few per cent.
"""
import json, math, os
here = os.path.dirname(os.path.abspath(__file__))

def pois_cdf_ge(n, mu):          # P(X >= n | mu)
    if n <= 0: return 1.0
    # 1 - sum_{k<n} e^-mu mu^k/k!, in logs
    s = 0.0
    for k in range(n):
        s += math.exp(-mu + k * math.log(mu) - math.lgamma(k + 1)) if mu > 0 else (1.0 if k == 0 else 0.0)
    return 1 - s

def lower95(n):                  # largest mu with P(X >= n | mu) <= 0.05
    if n <= 0: return 0.0
    lo, hi = 0.0, float(n)
    for _ in range(80):
        mid = (lo + hi) / 2
        if pois_cdf_ge(n, mid) > 0.05: hi = mid
        else: lo = mid
    return lo

for name in ('R11_s1_A10G', 'R13_s1_A10G'):
    r = json.load(open(os.path.join(here, '..', 'data', 'gpu_facelaw', name + '.json')))
    e, d, x = r['bins']['edges'], r['bins']['deaths'], r['bins']['exposure']
    n = min(len(e) - 1, len(d), len(x))
    E = sum(x[:n]); D = sum(d[:n]); h = D / E; G = r['gens']
    print('%s: deaths %d, exposure %.4g, mean life %.0f, run = %.1f mean lives, oldest age %.1f mean lives (ln lives = %.1f)'
          % (name, D, E, 1 / h, G * h, r['max_age'] * h, math.log(D)))
    for k in (2, 3, 5):
        idx = [i for i in range(n) if e[i] >= k / h]
        if not idx: continue
        a = e[idx[0]]; Eb = sum(x[i] for i in idx); Db = sum(d[i] for i in idx)
        if Eb == 0: continue
        Z = max(0.0, Eb - lower95(Db) / h) / E
        print('   above %.1f mean lives: deaths %d against %.1f expected; zombie exposure / total <= %.1e; all ages <= %.1e'
              % (a * h, Db, h * Eb, Z, Z / (1 - a / G) ** 2))
