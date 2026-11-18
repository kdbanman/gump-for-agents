#!/usr/bin/env python3
"""blast/ref-proofs: Lemma R against rigour's own tube rows (data/mc.csv, data/mc_routes.csv; tube (1,1),(0,D)).
h_starve(D) = h(D) (1 - p(D)), h_bust(D) = h(D) p(D); the lemma's reading needs each to be exponential in D."""
import csv, math, collections
R = '../rigour/data/'
lt = collections.defaultdict(list); p = {}
for r in csv.DictReader(open(R + 'mc.csv')):
    if r['shape'].startswith('torus_1_1_'):
        lt[int(r['shape'].split('_')[3])].append((float(r['lntau']), float(r['stderr'])))
for r in csv.DictReader(open(R + 'mc_routes.csv')):
    if r['shape'].startswith('torus_1_1_'):
        D = int(r['shape'].split('_')[3]); n = int(r['deaths']); q = float(r['halffall6'])
        lt[D].append((float(r['lntau']), float(r['stderr']))); p[D] = (q, math.sqrt(q * (1 - q) / n))
lt[5] = [(4.387194740124, 1e-9)]; p[5] = (0.817663, 1e-6)        # exact (reproduced by ref.py for 9 and 12 cells only)
L = {}
for D, v in lt.items():
    w = [1 / e ** 2 for _, e in v]; L[D] = (sum(x * wi for (x, _), wi in zip(v, w)) / sum(w), 1 / math.sqrt(sum(w)))
Ds = sorted(d for d in L if d in p)
print(' D   lntau          bust share p      ln odds')
for D in Ds:
    q, e = p[D]; print('%2d  %.4f+-%.4f  %.4f+-%.4f  %+.3f+-%.3f' % (D, L[D][0], L[D][1], q, e, math.log(q / (1 - q)), e / (q * (1 - q))))
print('\nper unit of length (3 cells), between consecutive measured D:')
print(' D->D\'  step lntau     -d ln odds      c_starve=-d ln h_s   c_bust=-d ln h_b    step - 0.29*p(D)   exact discrete: step + ln(1 - p(D)(1-e^-0.29))')
for a, b in zip(Ds, Ds[1:]):
    n = b - a
    st = (L[b][0] - L[a][0]) / n; est = math.hypot(L[a][1], L[b][1]) / n
    (qa, ea), (qb, eb) = p[a], p[b]
    lo = (math.log(qa / (1 - qa)) - math.log(qb / (1 - qb))) / n; elo = math.hypot(ea / (qa * (1 - qa)), eb / (qb * (1 - qb))) / n
    cs = st - (math.log(1 - qb) - math.log(1 - qa)) / n; ecs = math.sqrt(est ** 2 + ((ea / (1 - qa)) ** 2 + (eb / (1 - qb)) ** 2) / n ** 2)
    cb = st - (math.log(qb) - math.log(qa)) / n; ecb = math.sqrt(est ** 2 + ((ea / qa) ** 2 + (eb / qb) ** 2) / n ** 2)
    lin = st - 0.29 * qa
    ex = st + math.log(1 - qa * (1 - math.exp(-0.29))) if n == 1 else float('nan')
    print('%2d->%2d  %.3f+-%.3f  %.3f+-%.3f  %.3f+-%.3f      %.3f+-%.3f      %.3f              %.3f' % (a, b, st, est, lo, elo, cs, ecs, cb, ecb, lin, ex))
