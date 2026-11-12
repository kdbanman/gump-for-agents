#!/usr/bin/env python3
"""Lead's independent check of the face law (research/peeling) using the main engine only.

Asymmetric octahedral soups of L1 radius R: time from generation T0 to the first death of any
face layer, for runs whose hull is still the full octahedron at T0 (all 8 faces have
A(R) = 3(m+1)(m+2)/2 cells, m = (R-1)/2). The law tau_face = exp(-0.09 + 0.209 A) predicts
an exponential waiting time with mean tau_face / 8.

  python3 research/experiments/verify_face_law.py R RUNS [CAP]
"""
import json, math, subprocess, sys, tempfile, os
from concurrent.futures import ThreadPoolExecutor
G = "engine/target/release/gump"; T0 = 60
R, RUNS = int(sys.argv[1]), int(sys.argv[2]); CAP = int(sys.argv[3]) if len(sys.argv) > 3 else 400000
m = (R - 1) // 2; A = 3 * (m + 1) * (m + 2) // 2

def one(rng):
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f: ev = f.name
    out = subprocess.run([G, "run", "--soup", "0.35", "--radius", str(R), "--rng", str(rng), "--events", ev,
                          "--every", "1", "--gens", str(CAP), "--out", "/dev/null"], capture_output=True, text=True).stdout
    summ = json.loads(out.strip().splitlines()[-1])
    evs = [json.loads(l) for l in open(ev)]; os.unlink(ev)
    hull = [e for e in evs if e["cause"] == "hull"]
    early = [e for e in hull if e["gen"] < T0]
    late = sorted(e["gen"] for e in hull if e["gen"] >= T0)
    full = summ["hull_initial"] == [[-R, R]] * 4 and not early
    return full, (late[0] - T0 if late else None), summ["gen"]

with ThreadPoolExecutor(2) as ex: res = list(ex.map(one, range(1000, 1000 + RUNS)))
clean = [r for r in res if r[0]]
t = [r[1] for r in clean if r[1] is not None]; cens = [r for r in clean if r[1] is None]
expo = sum(t) + sum(r[2] - T0 for r in cens)            # total exposure (censored runs count their full length)
mean = expo / max(1, len(t)); se = mean / math.sqrt(max(1, len(t)))
cv = (sum((x - sum(t)/len(t))**2 for x in t) / len(t))**0.5 / (sum(t)/len(t)) if t else float("nan")
pred = math.exp(-0.09 + 0.209 * A) / 8
print(f"R={R} face cells A={A}: {len(clean)}/{RUNS} runs start with a full hull; {len(t)} peeled, {len(cens)} censored at {CAP}")
print(f"  mean wait to first peel (any of 8 faces): {mean:.3g} +- {se:.2g}  -> tau_face = {8*mean:.3g}   CV of waits = {cv:.2f} (1 = exponential)")
print(f"  slab law predicts first-peel mean {pred:.3g} (tau_face {8*pred:.3g}); measured/predicted = {mean/pred:.2f}")
