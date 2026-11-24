#!/usr/bin/env python3
"""The support under the watched face while it is low, chain by chain (layer-diagnostic outputs, NZD_LAYERS=1).

    python3 research/blast/density/chains.py FILE [FILE ...]

Per file: the density of the replaced core of layer 1 and 2 and of the whole layer 1, overall and given face population
<= 10 and <= 4; the variance of the core-1 count over its binomial value (1 = independent cells) given face <= 10;
the supply = dead face cells with 3 (and with 2) of their 3 cells below alive, and the conversion = births with 3
below / that supply, averaged over face populations 1..10 (weights: gump's counts at each population, so that chains
are compared at the same populations); the drift (births - deaths per generation) averaged the same way.
"""
import re, sys

def load(f):
    t = open(f).read()
    L = {}
    for l in t.splitlines():
        if l.startswith('LAYER'):
            w = l.split(); name = w[1]
            L[name] = {'all': float(w[5])}
            for m in re.finditer(r'pop<=(\d+) ([0-9.]+)', l):
                L[name][int(m.group(1))] = float(m.group(2))
    V = {}
    for l in t.splitlines():
        if l.startswith('VAR'):
            m = re.search(r'pop<=10: var/binom ([0-9.]+)', l)
            if m: V[l.split()[1]] = float(m.group(1))
    D = {}
    for l in t.splitlines():
        w = l.split()
        if l.startswith('DRIFT') and w[1].isdigit():
            v = [float(x) for x in w[3:]]
            D[int(w[1])] = dict(n=v[0], b=v[1:5], d=v[5], s2=v[6], s3=v[7])
    lt = re.search(r'lntau_watched ([0-9.]+) \+- ([0-9.]+)', t)
    return L, V, D, lt.groups() if lt else ('-', '-')

files = sys.argv[1:]
data = [(f.split('/')[-1].replace('.txt', ''), *load(f)) for f in files]
ref = next((D for n, L, V, D, lt in data if 'gump' in n), data[0][3])
ps = [p for p in range(1, 11) if p in ref]
wt = {p: ref[p]['n'] for p in ps}; W = sum(wt.values())
print(f'{"chain":24s} {"ln tau (this run)":>18s}  core1: all  <=10  <=4 | core2: <=10 | full1: <=10 | var/binom core1 <=10 | supply3 supply2 conv3 drift (face 1..10)')
for n, L, V, D, lt in data:
    def avg(fn):
        return sum(wt[p] * fn(D[p]) for p in ps if p in D) / sum(wt[p] for p in ps if p in D)
    s3 = avg(lambda r: r['s3']); s2 = avg(lambda r: r['s2']); cv = avg(lambda r: r['b'][3] / r['s3'] if r['s3'] else 0)
    dr = avg(lambda r: sum(r['b']) - r['d'])
    c1 = L.get('core1', {}); c2 = L.get('core2', {}); f1 = L.get('full1', {})
    print(f'{n:24s} {lt[0]:>9s} +- {lt[1]:6s}  {c1.get("all", -1):.3f} {c1.get(10, -1):.3f} {c1.get(4, -1):.3f} | {c2.get(10, -1):.3f} | {f1.get(10, -1):.3f} | '
          f'{V.get("core1", -1):8.3f}            | {s3:6.3f} {s2:7.3f} {cv:.4f} {dr:+.3f}')
