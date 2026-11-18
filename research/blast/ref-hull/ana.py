#!/usr/bin/env python3
"""ana.py FILE...  pool the RESULT lines of independent replications (per R and parameter set).
ln tau = -ln(mean of rates); error = sd(rates)/(sqrt(K) mean); jackknife beside it."""
import sys, math, collections
rows = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("RESULT"): continue
        t = line.split(); d = {t[i]: t[i + 1] for i in range(1, len(t) - 1, 2)}
        key = (int(d["R"]), int(d["M"]), int(d["NS"]), int(d["LAG"]), int(d["STEP"]), int(d.get("PMODE", 0)), int(d.get("DIV", 0)), int(d.get("DL", 0)), int(d.get("mflip", 0)))
        rows[key].append(d)
for key in sorted(rows):
    ds = rows[key]; K = len(ds)
    rates = [math.exp(-float(d["lnTau"])) for d in ds]
    m = sum(rates) / K
    sd = math.sqrt(sum((r - m) ** 2 for r in rates) / (K - 1)) if K > 1 else float("nan")
    err = sd / (math.sqrt(K) * m) if K > 1 else float("nan")
    jk = [-math.log((m * K - r) / (K - 1)) for r in rates] if K > 1 else [0]
    jm = sum(jk) / len(jk); jerr = math.sqrt((K - 1) / K * sum((x - jm) ** 2 for x in jk)) if K > 1 else float("nan")
    logs = [float(d["lnTau"]) for d in ds]; ml = sum(logs) / K
    sdl = math.sqrt(sum((x - ml) ** 2 for x in logs) / (K - 1)) if K > 1 else float("nan")
    nd = sum(int(d["deathsSampled"]) for d in ds)
    big = sum(float(d["bigFallShare"]) * int(d["deathsSampled"]) for d in ds) / max(nd, 1)
    fm = sum(float(d["fallMean"]) * int(d["deathsSampled"]) for d in ds) / max(nd, 1)
    bigs = [float(d["bigFallShare"]) for d in ds]; mb = sum(bigs) / K
    eb = math.sqrt(sum((x - mb) ** 2 for x in bigs) / (K - 1) / K) if K > 1 else float("nan")
    ex = sum(int(d["expo"]) for d in ds); dd = sum(int(d["deathsDirect"]) for d in ds)
    direct = f"{math.log(8 * ex / dd):.4f} ± {1 / math.sqrt(dd):.4f} ({dd} deaths)" if dd > 0 else "none"
    print(f"R {key[0]} A {ds[0]['A']} M {key[1]} NS {key[2]} LAG {key[3]} STEP {key[4]} PMODE {key[5]} DIV {key[6]} DL {key[7]} mflip {key[8]} K {K}: lnTau {-math.log(m):.4f} ± {err:.4f} (jackknife {jerr:.4f}); "
          f"mean of logs {ml:.4f}, sd of one log {sdl:.4f}; bigFallShare {mb:.4f} ± {eb:.4f}; mean max fall {fm:.2f}; "
          f"fallMax {max(int(d['fallMax']) for d in ds)}; replaybad {sum(int(d['replaybad']) for d in ds)}; timeouts {sum(int(d['timeouts']) for d in ds)}; "
          f"direct lnTau {direct}; cpu {sum(float(d['sec']) for d in ds):.0f}s")
