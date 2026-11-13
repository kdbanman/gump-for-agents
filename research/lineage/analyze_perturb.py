#!/usr/bin/env python3
"""Unperturbed vs one-orbit-flip continuations of many structured lineages (output of perturb.py).

  python3 research/lineage/analyze_perturb.py [CSV]     (default research/scratch/lineage/perturb_13_20000.csv,
                                                         else research/lineage/data/perturb_13_20000.csv)
Residual waits are scaled by the engine-soup mean at the source's radius (tau_e; analyze.py's table: 33c 2.423e5,
35c from the orbit-stepper 1.399e6). Tests:
  - copy 0 (the lineage itself) and copies 1..K against Exp(1): mean, CV, tails, KS
  - does the lineage's own continuation predict its copies? Spearman(x0, mean of copies)
  - do copies of one source resemble each other more than copies of different sources? Kruskal-Wallis over sources,
    and the intra-class correlation of ln x
"""
import sys, os, csv, math, collections
import numpy as np
from scipy import stats
TAU = {33: 2.423e5, 35: 1.399e6, 31: 5.904e4}
f = sys.argv[1] if len(sys.argv) > 1 else "research/scratch/lineage/perturb_13_20000.csv"
if not os.path.exists(f): f = "research/lineage/data/perturb_13_20000.csv"
src = collections.defaultdict(dict); cens = 0
for r in csv.DictReader(open(f)):
    if int(r["r0"]) not in TAU: continue                       # sources whose first plateau is below r = 31: skipped
    if r["died"] != "1": cens += 1
    src[int(r["src"])][int(r["copy"])] = int(r["resid"]) / TAU[int(r["r0"])]
src = {s: d for s, d in src.items() if len(d) >= 3}
K = max(len(d) for d in src.values()) - 1
print(f"{len(src)} source states, up to {K} perturbed copies each, {cens} censored; radii {collections.Counter(int(r['r0']) for r in csv.DictReader(open(f)) if r['copy']=='0')}")
def line(x, label):
    x = np.array(x); n = len(x)
    print(f"  {label:28s} n={n:4d} mean {x.mean():5.3f} (Gamma p {2*min(stats.gamma.cdf(x.sum(), n), stats.gamma.sf(x.sum(), n)):.3f})"
          f"  CV {x.std(ddof=1)/x.mean():4.2f}  >4: {(x>4).sum()}/{n*math.exp(-4):.1f}  <0.05: {(x<0.05).sum()}/{n*(1-math.exp(-.05)):.1f}"
          f"  KS p {stats.kstest(x, 'expon').pvalue:.3f}")
x0 = [d[0] for d in src.values() if 0 in d]; xc = [v for d in src.values() for k, v in d.items() if k]
line(x0, "unperturbed (the lineage)"); line(xc, "one-orbit-flip copies")
print(f"  two-sample unperturbed vs copies: KS p {stats.ks_2samp(x0, xc).pvalue:.3f}, Mann-Whitney p {stats.mannwhitneyu(x0, xc).pvalue:.3f}")
a = [d[0] for d in src.values() if 0 in d and len(d) > 1]; b = [np.mean([v for k, v in d.items() if k]) for d in src.values() if 0 in d and len(d) > 1]
rho, p = stats.spearmanr(a, b); print(f"  Spearman(lineage's own residual, mean of its copies) = {rho:+.3f} (p {p:.3f})")
groups = [[v for k, v in d.items() if k] for d in src.values()]
groups = [g for g in groups if len(g) >= 2]
print(f"  Kruskal-Wallis across sources (copies only): p {stats.kruskal(*groups).pvalue:.3f}")
L = [np.log(g) for g in groups]; n = np.mean([len(g) for g in L]); grand = np.mean(np.concatenate(L))
msb = sum(len(g) * (g.mean() - grand) ** 2 for g in L) / (len(L) - 1); msw = sum(((g - g.mean()) ** 2).sum() for g in L) / sum(len(g) - 1 for g in L)
print(f"  intra-class correlation of ln x among copies of one source: {(msb - msw) / (msb + (n - 1) * msw):+.3f}")
same = sum(1 for g in groups for i in range(len(g)) for j in range(i) if g[i] == g[j])
print(f"  copy pairs with identical residuals (fate not changed by the flip): {same}")
