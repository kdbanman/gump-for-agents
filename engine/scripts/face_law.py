#!/usr/bin/env python3
"""Face-law check through the ensemble engine (same statistic as
research/experiments/verify_face_law.py, one `gump ensemble` call instead of one run each).

  face_law.py R RUNS [CAP] [--gump PATH]
"""
import json, math, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
G = os.path.join(HERE, "..", "target", "release", "gump")
if "--gump" in a:
    i = a.index("--gump"); G = a[i + 1]; del a[i:i + 2]
R, RUNS = int(a[0]), int(a[1]); CAP = int(a[2]) if len(a) > 2 else 400000
T0 = 60
m = (R - 1) // 2; A = 3 * (m + 1) * (m + 2) // 2
out = subprocess.run([G, "ensemble", "--soup", "0.35", "--radius", str(R), "--rng", "1000", "--runs", str(RUNS),
                      "--gens", str(CAP), "--layer-deaths", "all"], check=True, capture_output=True, text=True).stdout
rows = [json.loads(l) for l in out.splitlines()]
runs = [d for d in rows if d["type"] == "summary"]
tail = [d for d in rows if d["type"] == "ensemble_summary"][0]
t, cens, clean = [], [], 0
for d in runs:
    hull = [e for e in d["layer_deaths"] if e["cause"] == "hull"]
    if d["hull_initial"] != [[-R, R]] * 4 or any(e["gen"] < T0 for e in hull):
        continue
    clean += 1
    late = sorted(e["gen"] for e in hull if e["gen"] >= T0)
    if late:
        t.append(late[0] - T0)
    else:
        cens.append(d["gen"] - T0)
expo = sum(t) + sum(cens)
mean = expo / max(1, len(t)); se = mean / math.sqrt(max(1, len(t)))
pred = math.exp(-0.09 + 0.209 * A) / 8
print(json.dumps({"R": R, "A": A, "runs": len(runs), "full_hull_at_T0": clean, "peeled": len(t), "censored": len(cens),
                  "mean_wait": round(mean, 1), "se": round(se, 1), "predicted": round(pred, 1),
                  "elapsed_s": round(tail["elapsed_s"], 1), "total_gens": tail["total_gens"]}))
