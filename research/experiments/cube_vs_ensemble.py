#!/usr/bin/env python3
"""Every plateau of the closed cubes 13-16 against the ensemble mean residence at the same hull.

Cube schedules: research/scratch/cubes/evN.jsonl (regenerate with research/experiments/cube_ckpt.sh N; side 16 is
kept in research/data/cube16_events.jsonl). Ensemble means: research/fluct/data/sym_residence.csv (O_h soups and
cube copies on the orbit stepper); where a vertex-centred value was not measured, the cube-centred one times VF.
Prints T / tau for each plateau with A >= AMIN and the tail statistics under exponential waits.
   python3 research/experiments/cube_vs_ensemble.py [AMIN=408] [VF=1.6]"""
import json, sys, math, csv, os
AMIN = int(sys.argv[1]) if len(sys.argv) > 1 else 408; VF = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
area = lambda r: 3 * ((r - 1) // 2 + 1) * ((r - 1) // 2 + 2) // 2
tau = {}
for row in csv.DictReader(open("research/fluct/data/sym_residence.csv")):
    k = (int(row["A"]), row["centre"]); d = int(row["deaths"]); e = float(row["exposure"])
    D, E = tau.get(k, (0, 0.0)); tau[k] = (D + d, E + e)                       # pool sources at the same (A, centre)
ratios = []
for n in (13, 14, 15, 16):
    f = f"research/scratch/cubes/ev{n}.jsonl"
    if n == 16 and not os.path.exists(f): f = "research/data/cube16_events.jsonl"
    last = {}
    for line in open(f):
        e = json.loads(line)
        if e["type"] == "layer_death" and e["axis"] == 0 and e.get("cause") == "hull" and e["s"] > 0: last.setdefault(e["s"], e["last_alive"])
    cen = "v" if n % 2 == 0 else "c"; c0 = 3 if cen == "v" else 0; t = 0
    for s in sorted(last, reverse=True):
        r = s - c0; A = area(r)
        if last[s] <= t: continue
        T = last[s] - t; t = last[s]
        if A < AMIN: continue
        if (A, cen) in tau: D, E = tau[(A, cen)]; m = E / D; src = f"{D} deaths"
        elif (A, "c") in tau: D, E = tau[(A, "c")]; m = VF * E / D; src = f"c x {VF}"
        else: continue
        ratios.append(T / m)
        print(f"  side {n}  R={r:2d} A={A} {cen}:  T = {T:11.4g}   tau = {m:9.3g} ({src:10s})  T/tau = {T/m:6.3f}   P(wait >= T) = {math.exp(-T/m):.4f}")
k = len(ratios); s = sum(ratios)
p_sum = math.exp(-s) * sum(s ** i / math.factorial(i) for i in range(k))            # P(Gamma(k) >= s)
big = sum(r > 4 for r in ratios); q = math.exp(-4)
p_big = 1 - sum(math.comb(k, i) * q ** i * (1 - q) ** (k - i) for i in range(big))
print(f"{k} plateaus: sum of T/tau = {s:.1f} (expected {k}); P(sum this large) = {p_sum:.4f}")
print(f"  {big} plateaus beyond 4 tau (expected {k*q:.2f}); P(this many or more) = {p_big:.4f};  shortest {min(ratios):.3f}")
