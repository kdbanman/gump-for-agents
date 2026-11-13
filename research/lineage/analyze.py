#!/usr/bin/env python3
"""Plateau residences of structured lineages vs O_h soup lineages vs the memoryless ensemble means.

  python3 research/lineage/analyze.py [CSV ...]      (default: research/scratch/lineage/plateaus_*.csv,
                                                      or research/lineage/data/plateaus.csv.gz if those are absent)
Reference means:
  tau_q  = orbit-stepper ensembles, research/fluct/data/sym_residence.csv (pooled per (A, centre)); reliable r >= 31
  tau_s  = engine soup lineages of this directory, late hazard: exposure beyond 0.05*tau_q / deaths beyond it
x = T / tau_q for every plateau ending in a peel (censored ones, 'cap' or 'settled', are counted and listed).
"""
import sys, csv, glob, math, gzip, os, collections
import numpy as np
from scipy import stats

area = lambda r: 3 * ((r - 1) // 2 + 1) * ((r - 1) // 2 + 2) // 2
RELIABLE = lambda r, c: (r >= 31 and c == "c") or (r >= 32 and c == "v")

def tau_q():
    tau = {}
    for row in csv.DictReader(open("research/fluct/data/sym_residence.csv")):
        if row["tag"].startswith("snap_"): continue                          # copies of the cube: not soups
        k = (int(row["A"]), row["centre"]); D, E = tau.get(k, (0, 0.0))
        tau[k] = (D + int(row["deaths"]), E + float(row["exposure"]))
    return {k: E / D for k, (D, E) in tau.items()}

def load(files):
    rows, seen = [], {}
    for f in files:
        op = gzip.open if f.endswith(".gz") else open
        for r in csv.DictReader(op(f, "rt")):
            r["r"] = int(r["r"]); r["idx"] = int(r["idx"]); r["T"] = int(r["T"]); r["died"] = int(r["died"])
            # identical structured seeds give identical schedules: keep one lineage per signature
            key = (r["kind"], r["sig"]); first = seen.setdefault(key, r["tag"])
            if r["kind"] == "struct" and first != r["tag"]: continue
            rows.append(r)
    return rows

def summary(x, label):
    x = np.asarray(x); n = len(x)
    if n < 3: return None
    m = x.mean(); cv = x.std(ddof=1) / m
    big, small = (x > 4).sum(), (x < 0.05).sum()
    pb = stats.binom.sf(big - 1, n, math.exp(-4)); ps = stats.binom.sf(small - 1, n, 1 - math.exp(-0.05))
    ks = stats.kstest(x, "expon").pvalue
    # mean against Gamma(n, 1): two-sided
    pm = 2 * min(stats.gamma.cdf(x.sum(), n), stats.gamma.sf(x.sum(), n))
    return f"{label:34s} {n:5d}  mean {m:5.3f} (p {pm:5.3f})  CV {cv:4.2f}  >4: {big:3d}/{n*math.exp(-4):5.1f} (p {pb:5.3f})  <0.05: {small:3d}/{n*(1-math.exp(-0.05)):5.1f} (p {ps:5.3f})  KS p {ks:5.3f}"

def main():
    files = sys.argv[1:] or sorted(glob.glob("research/scratch/lineage/plateaus_*.csv")) or ["research/lineage/data/plateaus.csv.gz"]
    rows = load(files); tq = tau_q()
    print(f"{len(rows)} plateaus from {len(set((r['kind'], r['tag']) for r in rows))} distinct lineages; files {files}")
    # censoring
    cens = collections.Counter((r["kind"], r["centre"], r["r"], r["end"]) for r in rows if not r["died"] and RELIABLE(r["r"], r["centre"]))
    if cens: print("censored plateaus at reliable radii (kind, centre, r, why): count:", dict(cens))

    print("\n== per radius: deaths, mean T / tau_q (first plateau | after a peel) ==")
    print(" kind   r c   A      tau_q     | first: n  mean  CV   | after: n  mean  CV   | late-hazard tau / tau_q")
    by = collections.defaultdict(list)
    for r in rows: by[(r["kind"], r["r"], r["centre"])].append(r)
    for (kind, rr, c), lst in sorted(by.items(), key=lambda kv: (kv[0][0], kv[0][2], -kv[0][1])):
        if (area(rr), c) not in tq: continue
        t = tq[(area(rr), c)]; out = []
        for sel in (lambda r: r["idx"] == 0, lambda r: r["idx"] > 0):
            x = np.array([r["T"] / t for r in lst if sel(r) and r["died"]])
            out.append(f"{len(x):5d} {x.mean() if len(x) else float('nan'):5.2f} {x.std(ddof=1)/x.mean() if len(x) > 2 else float('nan'):4.2f}")
        # late hazard: exposure and deaths beyond 0.05 tau_q (all plateaus, censored ones included)
        e = sum(max(0, r["T"] / t - 0.05) for r in lst); d = sum(1 for r in lst if r["died"] and r["T"] / t > 0.05)
        late = f"{e/d:5.2f} +- {e/d/math.sqrt(d):4.2f}  ({d} deaths)" if d else ""
        flag = "" if RELIABLE(rr, c) else "  (tau_q unreliable here)"
        print(f" {kind:6s} {rr:2d} {c} {area(rr):3d}  {t:10.4g}   | {out[0]} | {out[1]} | {late}{flag}")

    print("\n== pooled over reliable radii: x = T / tau_q, plateaus ending in a peel ==")
    for kind in ("struct", "soup"):
        for name, sel in (("all", lambda r: True), ("first plateau", lambda r: r["idx"] == 0), ("after a peel", lambda r: r["idx"] > 0)):
            x = [r["T"] / tq[(area(r["r"]), r["centre"])] for r in rows if r["kind"] == kind and r["died"] and sel(r)
                 and RELIABLE(r["r"], r["centre"]) and (area(r["r"]), r["centre"]) in tq]
            s = summary(x, f"{kind} {name}")
            if s: print(s)
    for cen in ("c", "v"):
        for kind in ("struct", "soup"):
            x = [r["T"] / tq[(area(r["r"]), r["centre"])] for r in rows if r["kind"] == kind and r["died"] and r["centre"] == cen
                 and RELIABLE(r["r"], r["centre"])]
            s = summary(x, f"{kind} centre {cen}")
            if s: print(s)
    xs = {k: [r["T"] / tq[(area(r["r"]), r["centre"])] for r in rows if r["kind"] == k and r["died"] and RELIABLE(r["r"], r["centre"])]
          for k in ("struct", "soup")}
    if all(len(v) > 5 for v in xs.values()):
        print(f"two-sample struct vs soup: KS p = {stats.ks_2samp(xs['struct'], xs['soup']).pvalue:.3f}, "
              f"Mann-Whitney p = {stats.mannwhitneyu(xs['struct'], xs['soup']).pvalue:.3f}, "
              f"log-mean ratio {math.log(np.mean(xs['struct']) / np.mean(xs['soup'])):+.3f}")

    print("\n== hazard vs age within a plateau (units 1/tau_q; 1 = memoryless at the ensemble rate), reliable radii ==")
    edges = [0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 4, 1e9]
    for kind in ("struct", "soup"):
        for name, sel in (("first", lambda r: r["idx"] == 0), ("after a peel", lambda r: r["idx"] > 0)):
            lst = [(r["T"] / tq[(area(r["r"]), r["centre"])], r["died"]) for r in rows if r["kind"] == kind and sel(r)
                   and RELIABLE(r["r"], r["centre"])]
            if not lst: continue
            cells = []
            for a, b in zip(edges, edges[1:]):
                e = sum(max(0.0, min(x, b) - a) for x, _ in lst); d = sum(1 for x, died in lst if died and a <= x < b)
                cells.append(f"{d / e:5.2f}({d})" if e > 0 else "   -  ")
            print(f" {kind:6s} {name:12s} n={len(lst):5d}: " + " ".join(cells))
    print("   bins: " + " ".join(f"[{a:g},{b:g})" for a, b in zip(edges, edges[1:])))

if __name__ == "__main__":
    main()
