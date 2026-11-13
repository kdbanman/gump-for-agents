#!/usr/bin/env python3
"""Audit: headline numbers re-derived from the committed data and tables (no simulation; a few seconds).

Each check re-computes a number that README / STATUS / NOTEBOOK quote, from the curated file it was derived from,
and compares it with the quoted value. Claim ids refer to research/CLAIMS.md.

  python3 research/audit/data_claims.py      # one line per check; exit 1 on any failure
"""
import csv, json, math, os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)
FAIL = []


def report(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}", flush=True)
    if not ok:
        FAIL.append(name)


def gamma_sf(k, s):  # P(Gamma(k,1) >= s) for integer k
    return math.exp(-s) * sum(s ** i / math.factorial(i) for i in range(k))


def main():
    # C-peel-16: side-16 schedule from research/data/cube16_events.jsonl
    last = {}
    for line in open(P("research/data/cube16_events.jsonl")):
        e = json.loads(line)
        if e["axis"] == 0 and e["s"] > 0 and e["cause"] == "hull":
            last.setdefault(e["s"], e["last_alive"])
    seq = sorted((v, s) for s, v in last.items() if v > 0)
    res, t = {}, 0
    for v, s in seq:
        res[s - 3] = v - t; t = v
    want = {42: 2362434048, 40: 523666432, 38: 30768448, 36: 2712064, 34: 7040, 32: 27712, 30: 128, 24: 256, 22: 64}
    ok = all(res.get(k) == v for k, v in want.items()) and res.get(28, 0) + res.get(26, 0) == 1344
    summ = json.loads(open(P("research/data/cube16_summary.json")).read())
    ok &= summ["gen"] == 2919617676 and summ["pop"] == 96 and summ["status"] == "still" and summ["theorem_violations"] == 0
    report("cube16", ok, f"residences R=42..22 as in NOTEBOOK table; first peel at last_alive {seq[0][0]:,}, second {seq[1][0]:,}; "
           f"ends still at {summ['gen']:,} with {summ['pop']} cells")
    # all 8 faces die together (every axis/direction has the same last_alive for each radius)
    by = {}
    for line in open(P("research/data/cube16_events.jsonl")):
        e = json.loads(line)
        if e["cause"] == "hull":
            by.setdefault((e["axis"], e["s"] > 0), []).append(e["last_alive"])
    firsts = {k: sorted(x for x in v if x > 0)[0] for k, v in by.items()}
    report("cube16-lockstep", len(set(firsts.values())) == 1 and len(firsts) == 8,
           f"first nonzero face death identical on all 8 faces: {sorted(set(firsts.values()))}")
    # face law: weighted refit of the flat-slab table (selection as in research/peeling/figures.py)
    rows = [r for r in csv.DictReader(open(P("research/peeling/slab_area.csv")))
            if r["m"] == "8" and int(r["fw_before_peel"]) < 0.06 * int(r["replicas"]) and int(r["A"]) >= 27]
    A = np.array([float(r["A"]) for r in rows]); y = np.log(2 * np.array([float(r["mean_first"]) for r in rows]))
    w = 1 / ((np.log(2 * np.array([float(r["ci_hi"]) for r in rows])) - np.log(2 * np.array([float(r["ci_lo"]) for r in rows]))) / 3.92) ** 2
    X = np.c_[np.ones(len(A)), A]; W = np.diag(w)
    a, b = np.linalg.solve(X.T @ W @ X, X.T @ W @ y); rmax = np.abs(y - X @ [a, b]).max()
    report("facelaw", abs(a + 0.09) < 0.03 and abs(b - 0.209) < 0.002 and rmax < 0.2,
           f"tau_face = exp({a:.3f} + {b:.4f} A) over {len(A)} slab batches, max residual {rmax:.2f} (claimed -0.09 + 0.209 A, <= 0.18)")
    # rule space
    R = {r["rule"]: r for r in csv.DictReader(open(P("research/phase/rules.csv")))}
    cls = {}
    for r in R.values():
        cls[r["torus"]] = cls.get(r["torus"], 0) + 1
    f = lambda x: float(x) if x not in ("", "nan") else None
    long = [r["rule"] for r in R.values() if f(r["med10"]) is not None and f(r["med10"]) >= 1e3]
    bits = lambda rule: frozenset("B" + c for c in rule.split("/")[0][1:]) | frozenset("S" + c for c in rule.split("/")[1][1:])
    L = [bits(x) for x in long]; mins = [x for x in L if not any(y < x for y in L)]
    g = f(R["B45/S345"]["med10"])
    sub = {k: f(R[k]["med10"]) for k in ("B4/S345", "B5/S345", "B45/S45", "B45/S35", "B45/S34")}
    ok = (len(R) == 960 and cls == {"chaos": 421, "slow": 15, "freeze": 132, "die": 392} and len(long) == 146
          and sum("4" in x.split("/")[0] for x in long) == 142 and g == 3420 and len(mins) == 50 and bits("B45/S345") in mins
          and sub == {"B4/S345": 104, "B5/S345": 21, "B45/S45": 20, "B45/S35": 22, "B45/S34": 36})
    report("rulespace", ok, f"960 rules, torus classes {cls}, {len(long)} long-lived ({sum('4' in x.split('/')[0] for x in long)} with B4), "
           f"gump median {g:g}, {len(mins)} minimal elements incl. gump; one-bit removals {sub}")
    # symmetric face fit, the lead's form a + (0.209/6) A + c sqrt(A), cube-centred, pooled by A, weights = deaths
    pool = {}
    for r in csv.DictReader(open(P("research/fluct/data/sym_residence.csv"))):
        if r["centre"] == "c":
            d, e = pool.get(int(r["A"]), (0, 0.0)); pool[int(r["A"])] = (d + int(r["deaths"]), e + float(r["exposure"]))
    pts = [(a, math.log(e / d), d) for a, (d, e) in sorted(pool.items()) if d >= 10]
    Aa = np.array([p[0] for p in pts]); yy = np.array([p[1] for p in pts]) - 0.209 / 6 * Aa; ww = np.array([p[2] for p in pts], float)
    Xs = np.c_[np.ones(len(Aa)), np.sqrt(Aa)]; Ws = np.diag(ww)
    a0, c0 = np.linalg.solve(Xs.T @ Ws @ Xs, Xs.T @ Ws @ yy)
    report("symfit", abs(a0 - 0.69) < 0.03 and abs(c0 + 0.195) < 0.003,
           f"ln tau = {a0:.3f} + (0.209/6) A {c0:+.4f} sqrt(A) on A = {list(Aa)} (STATUS: 0.69, -0.195)")
    # QSD endpoint fit: I(0) = a + b/A from qsd_summary.json
    q = json.load(open(P("research/fluct/data/qsd_summary.json")))["sizes"]
    pts = [(v["A"], v["I0"]) for v in q.values() if v["deaths"] >= 100]
    Xq = np.c_[np.ones(len(pts)), [1 / p[0] for p in pts]]; aq, bq = np.linalg.lstsq(Xq, [p[1] for p in pts], rcond=None)[0]
    report("I0", abs(aq - 0.2077) < 0.002 and abs(bq - 0.55) < 0.05,
           f"-ln h / A = {aq:.4f} + {bq:.2f}/A over A = {[p[0] for p in pts]} (claimed 0.2077 + 0.55/A)")
    # statistics quoted for side 16 / the cube lineages (arithmetic only, from the stated ratios)
    ok = (abs(math.exp(-7.4) - 6e-4) < 0.5e-4 and abs(math.exp(-11.8) - 7e-6) < 1e-6 and abs(gamma_sf(16, 27.2) - 0.008) < 0.001
          and abs(gamma_sf(16, 26.5) - 0.011) < 0.001 and abs(1 - sum(math.comb(16, i) * math.exp(-4) ** i * (1 - math.exp(-4)) ** (16 - i) for i in range(3)) - 0.003) < 0.001)
    report("pvalues", ok, "exp(-7.4)=6e-4, exp(-11.8)=7e-6, P(Gamma16>=27.2)=0.008, P(Gamma16>=26.5)=0.011, P(>=3 of 16 beyond 4 means)=0.003")
    print("data_claims.py:", "ALL OK" if not FAIL else "FAILED: " + ", ".join(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
