#!/usr/bin/env python3
"""Residence times of O_h-symmetric octahedral soups at each hull radius, against the symmetric face law.

Each run: `gump run --soup 0.35 --radius R --sym oh --rng i` to its end (or CAP); all 8 faces peel together,
so the hull history is read off axis 0, s > 0. A residence is the time the hull spends at one radius
(censored ones, still alive at CAP, are counted in the exposure only). Estimate: mean = exposure / deaths.
Law (peeling study, cube-centred): ln tau = -0.14 + 0.0272 A.

  python3 research/experiments/sym_soup_peels.py R RUNS CAP [JOBS]
"""
import subprocess, sys, json, math, os, collections
from concurrent.futures import ThreadPoolExecutor
G = "engine/target/release/gump"; D = "research/scratch/symsoup"; os.makedirs(D, exist_ok=True)
R, RUNS, CAP = int(sys.argv[1]), int(sys.argv[2]), int(float(sys.argv[3])); JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 4
area = lambda r: 3 * ((r - 1) // 2 + 1) * ((r - 1) // 2 + 2) // 2

def one(i):
    ev = f"{D}/r{R}_{i}.jsonl"
    out = subprocess.run([G, "run", "--soup", "0.35", "--radius", str(R), "--sym", "oh", "--rng", str(i), "--gens", str(CAP),
                          "--events", ev, "--every", "16"], capture_output=True, text=True).stdout.strip().split("\n")[-1]
    end = json.loads(out)["gen"]; last = {}
    for line in open(ev):
        e = json.loads(line)
        if e["type"] == "layer_death" and e["axis"] == 0 and e["s"] > 0: last[e["s"]] = e["last_alive"]
    os.remove(ev)
    res = []; t = 60; r = R                                    # hull at radius r from time t (60: the soup has settled)
    while r > 0:
        if r not in last: res.append((r, end - t, False)); break          # still alive at the end of the run
        if last[r] > t: res.append((r, last[r] - t, True)); t = last[r]
        r -= 2
    return res

dead = collections.Counter(); expo = collections.Counter(); first = []
with ThreadPoolExecutor(JOBS) as ex:
    for res in ex.map(one, range(1, RUNS + 1)):
        for r, dt, died in res:
            expo[r] += dt; dead[r] += died
        if res and res[0][0] == R: first.append(res[0][1:])
print(f"R={R}, {RUNS} symmetric soups, cap {CAP:g}")
print("  radius  area  deaths  mean residence [95%]            ln   law   ln-law")
for r in sorted(expo, reverse=True):
    k = dead[r]
    if k < 5: continue
    mean = expo[r] / k; lo, hi = mean / (1 + 1.96 / math.sqrt(k)), mean / max(1e-9, 1 - 1.96 / math.sqrt(k))
    law = -0.14 + 0.0272 * area(r)
    print(f"  {r:5d} {area(r):5d} {k:6d}   {mean:10.4g} [{lo:9.4g}, {hi:9.4g}]  {math.log(mean):6.2f} {law:6.2f}  {math.log(mean)-law:+.2f}")
d = [x for x, died in first if died]
if len(d) > 2:
    m = sum(d) / len(d); cv = (sum((x - m) ** 2 for x in d) / (len(d) - 1)) ** 0.5 / m
    print(f"  first peels observed: {len(d)}/{len(first)}, mean of observed {m:.4g}, CV {cv:.2f}")
