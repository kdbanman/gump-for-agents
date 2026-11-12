#!/usr/bin/env python3
"""How does the population of an outer face layer fluctuate while the face is alive?

Asymmetric octahedral soups of radius R; outermost {111} layers (8 faces per run) sampled every
generation from the engine's kymograph. If the face population n were Gaussian with mean mu*A and
variance v*A, the chance of n = 0 would go like exp(-A * mu^2 / (2 v)), to be compared with the
measured face law's 0.209 per cell.   python3 research/experiments/face_fluct.py R GENS [RNG...]
"""
import subprocess, sys, csv, math, collections
G = "engine/target/release/gump"
R, GENS = int(sys.argv[1]), int(sys.argv[2]); rngs = [int(x) for x in sys.argv[3:]] or [1, 2, 3]
m = (R - 1) // 2; A = 3 * (m + 1) * (m + 2) // 2
hist = collections.Counter(); series = []
for rng in rngs:
    f = f"research/scratch/facefluct/k{R}_{rng}.csv"
    subprocess.run([G, "run", "--soup", "0.35", "--radius", str(R), "--rng", str(rng), "--gens", str(GENS),
                    "--kymo", f, "--every", "1"], capture_output=True)
    rd = csv.reader(open(f)); head = next(rd); s_vals = [int(x) for x in head[2:]]
    lo, hi = s_vals.index(-R), s_vals.index(R)
    per_axis = collections.defaultdict(lambda: ([], []))
    for row in rd:
        g = int(row[0])
        if g < 200: continue
        a = int(row[1]); per_axis[a][0].append(int(row[2 + lo])); per_axis[a][1].append(int(row[2 + hi]))
    faces = [ser for x, y in per_axis.values() for ser in (x, y)]
    if any(min(ser) == 0 for ser in faces):       # a peel shrinks the neighbouring faces: the run is not at fixed geometry
        print(f"  rng {rng}: a face died within the window - run excluded"); continue
    for ser in faces: series.append(ser); hist.update(ser)
N = sum(hist.values()); mu = sum(k * c for k, c in hist.items()) / N
var = sum((k - mu) ** 2 * c for k, c in hist.items()) / N
sk = sum((k - mu) ** 3 * c for k, c in hist.items()) / N / var ** 1.5
ac = []
for lag in (1, 2, 3, 5, 10, 20):
    num = den = 0.0
    for ser in series:
        mm = sum(ser) / len(ser)
        num += sum((ser[i] - mm) * (ser[i + lag] - mm) for i in range(len(ser) - lag)); den += sum((x - mm) ** 2 for x in ser)
    ac.append((lag, round(num / den, 3)))
print(f"R={R}: face sites A={A}; {len(series)} face-histories, {N} face-generations")
print(f"  population: mean {mu:.2f} ({mu/A:.3f} per site), variance {var:.1f} ({var/A:.3f} per site; binomial would be {mu/A*(1-mu/A):.3f}), skew {sk:+.2f}, min seen {min(hist)}, max {max(hist)}")
print(f"  autocorrelation (lag, r): {ac}")
print(f"  Gaussian-tail estimate of the cost per cell: mu^2/(2 v) = {(mu/A)**2/(2*var/A):.3f}   (measured face law: 0.209)")
tot = 0; rows = []
for k in sorted(hist):
    tot += hist[k]
    if tot >= 20: rows.append((k / A, -math.log(tot / N) / A, (mu / A - k / A) ** 2 / (2 * var / A)))
pick = [rows[i] for i in sorted(set([0, len(rows) // 8, len(rows) // 4, len(rows) // 2 - 1]))]
print("  empirical rate function I(x) = -ln P(n/A <= x) / A   vs Gaussian (mu-x)^2/2v:")
print("   " + "; ".join(f"x={x:.2f}: {i:.3f} vs {g:.3f}" for x, i, g in pick if x < mu / A))
qs = sorted(hist); cum = 0; out = []
for k in qs:
    cum += hist[k]
    if cum / N >= 1e-5 and not out: out.append(("1e-5 quantile", k))
    if cum / N >= 1e-3 and len(out) == 1: out.append(("1e-3 quantile", k))
    if cum / N >= 0.5 and len(out) == 2: out.append(("median", k)); break
z = lambda k: (k - mu) / math.sqrt(var)
print("  left tail:", ", ".join(f"{n} = {k} (z = {z(k):+.2f}; Gaussian would put it at z = {zz})" for (n, k), zz in zip(out, ("-4.26", "-3.09", "0"))))
