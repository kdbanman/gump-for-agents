#!/usr/bin/env python3
"""holes.py TORUSFILE [HULLFILE] -- referee's numbers for agent `holes`: f = -ln P(a x b rhombus of class-P unit cells empty).
Rows from `sl hole 12 0 12 SEED GENS` (8 groups of 32 lanes per seed) and `rh hole R SEED GENS`.
Errors: delete-one jackknife over ALL groups (8 per seed), and separately the scatter between seeds."""
import sys, math, collections
import numpy as np
def load(fn):
    d = collections.OrderedDict()
    for line in open(fn):
        t = line.split("#")[0].split()
        if not t or t[0] != "HOLE": continue
        key = (int(t[t.index("a") + 1]), int(t[t.index("b") + 1])) if "a" in t else int(t[t.index("type") + 1])
        seed = int(t[t.index("seed") + 1]); den = float(t[t.index("denom") + 1])
        c = np.array(list(map(float, t[t.index("counts") + 1:])))
        d.setdefault(key, []).append((seed, den, c))
    return d
def stats(fun, groups):
    """groups: list of dicts shape -> (count, denom) per independent group; fun maps pooled dict shape->f to a number."""
    def pooled(gs):
        tot = {}
        for g in gs:
            for k, (c, dn) in g.items():
                a = tot.setdefault(k, [0.0, 0.0]); a[0] += c; a[1] += dn
        return fun({k: -math.log(max(v[0], 0.5) / v[1]) for k, v in tot.items()})
    full = pooled(groups); n = len(groups)
    jk = [pooled(groups[:i] + groups[i + 1:]) for i in range(n)]
    m = sum(jk) / n
    return full, math.sqrt((n - 1) / n * sum((x - m) ** 2 for x in jk))
T = load(sys.argv[1])
seeds = sorted({s for v in T.values() for s, _, _ in v})
groups = []; byseed = []
for s in seeds:
    sg = {}
    for q in range(8):
        g = {}
        for k, v in T.items():
            for ss, den, c in v:
                if ss == s: g[k] = (c[q], den)
        groups.append(g)
    for k, v in T.items():
        for ss, den, c in v:
            if ss == s: sg[k] = (c.sum(), 8 * den)
    byseed.append(sg)
THEIRS = {(1, 1): 1.9718, (1, 2): 3.6260, (2, 2): 6.1598, (2, 3): 8.6753, (3, 3): 11.9849, (2, 4): 11.1417, (3, 4): 15.2298, (1, 3): 5.2975, (1, 4): 6.9565, (4, 4): 19.2377}
tot = sum(v[0][1] for k, v in T.items() if k == (1, 1)) * 8 * len(seeds) / len(seeds)
print(f"TORUS 12 x 12 x 8: {len(seeds)} seeds, {len(groups)} groups of 32 lanes; replica-generations {sum(den for _, den, _ in T[(1, 1)]) * 8 / (2 * 144):.3g}")
sym = lambda a, b: (lambda f: 0.5 * (f[(a, b)] + f[(b, a)]))
for (a, b) in [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)]:
    v, e = stats(sym(a, b), groups); v2, e2 = stats(sym(a, b), byseed)
    d, de = stats(lambda f: f[(a, b)] - f[(b, a)], groups)
    hits = sum(c.sum() for _, _, c in T[(a, b)]) + (sum(c.sum() for _, _, c in T[(b, a)]) if a != b else 0)
    print(f"  f({a}x{b}) = {v:.4f} +- {e:.4f} (jackknife over {len(groups)} groups; over {len(seeds)} seeds: {e2:.4f}); hits {int(hits)}; holes: {THEIRS[(a, b)]:.4f}; mine - holes {v - THEIRS[(a, b)]:+.4f}; a x b minus b x a (must be 0 by symmetry): {d:+.4f} +- {de:.4f}")
F = lambda a, b: (lambda f: 0.5 * (f[(a, b)] + f[(b, a)]))
def M(a, b):
    return lambda f: (F(a + 1, b + 1)(f) - F(a + 1, b)(f) - F(a, b + 1)(f) + F(a, b)(f)) / 3
for (a, b, th) in [(1, 1, 0.2932), (1, 2, 0.2814), (2, 2, 0.2646), (2, 3, 0.2595), (3, 3, 0.2543), (1, 3, 0.2691)]:
    v, e = stats(M(a, b), groups); v2, e2 = stats(M(a, b), byseed)
    print(f"  mixed second difference per cell M({a}.5, {b}.5)/3 = {v:.4f} +- {e:.4f} (seeds: {e2:.4f}); holes: {th:.4f}")
print("  pure second differences f(a+1,b) - 2 f(a,b) + f(a-1,b) (zero if f were bulk + perimeter + corner):")
for b in (2, 3, 4):
    out = []
    for a in (2, 3):
        v, e = stats(lambda f, a=a, b=b: F(a + 1, b)(f) - 2 * F(a, b)(f) + F(a - 1, b)(f), groups); out.append(f"a = {a}: {v:+.4f} +- {e:.4f}")
    print(f"    b = {b}: " + ";  ".join(out))
# the alternative that is not the mixed difference: what a pure (edge + corner + bulk) form would also give
v, e = stats(lambda f: (F(3, 3)(f) - 2 * F(2, 3)(f) + F(2, 2)(f)) / 3, groups)   # second difference in a at b... diagnostic only
if len(sys.argv) > 2:
    Hh = load(sys.argv[2]); hs = sorted({s for v in Hh.values() for s, _, _ in v})
    hg = []
    for s in hs:
        for q in range(8):
            g = {}
            for k, v in Hh.items():
                for ss, den, c in v:
                    if ss == s: g[k] = (c[q], den)
            hg.append(g)
    names = {0: ("interior, margin >= 2, 2x2", (2, 2), 6.1599), 1: ("interior, margin >= 2, 2x3", (2, 3), 8.6760), 2: ("interior, margin >= 2, 3x3", (3, 3), 11.9862),
             3: ("3x3 with its first row on a rim", None, 11.9849 - 0.98), 4: ("corner 2x2", None, 4.0556), 5: ("corner 2x3", None, 6.0608), 6: ("corner 3x3", None, 8.775), 7: ("interior, margin >= 2, 1x1", (1, 1), 1.9708)}
    print(f"HULL: {len(hs)} seeds, {len(hg)} groups")
    tor = {k: stats(sym(*k), groups) for k in [(1, 1), (2, 2), (2, 3), (3, 3)]}
    for t, (nm, shape, th) in names.items():
        v, e = stats(lambda f: f[t], hg)
        s = f"  {nm}: f = {v:.4f} +- {e:.4f}; holes (R = 29 or its R = 21 check): {th:.4f}; mine - holes {v - th:+.4f}"
        if shape: s += f"; my torus {tor[shape][0]:.4f} +- {tor[shape][1]:.4f}: hull - torus {v - tor[shape][0]:+.4f} +- {math.hypot(e, tor[shape][1]):.4f}"
        else: s += f"; against my torus 3x3: {v - tor[(3, 3)][0]:+.3f}" if "3x3" in nm else ""
        print(s)
