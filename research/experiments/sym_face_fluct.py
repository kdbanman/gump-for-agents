#!/usr/bin/env python3
"""Fluctuations of the outer face of a *symmetric* state (closed cubes), while the face is alive.

Streams the engine's per-generation kymograph through a FIFO and histograms the population n of
the outermost [111] layer over a window of generations. Prints mean, variance, and
J(x) = -ln P(n/A <= x); the symmetric face law (ln tau = -0.14 + 0.0272 A) corresponds to
J(0)/A = 0.0272 at every size. A = sites in the layer, from the hull radius.

  python3 research/experiments/sym_face_fluct.py FROM TO -- <gump run seed args>
  e.g.  ... 200 130000 -- --cube 13        ... 0 2000000 -- --snapshot research/scratch/cubes/cube16.ckpt.gump
"""
import subprocess, sys, os, math, collections, tempfile
G = "engine/target/release/gump"
i = sys.argv.index("--"); g0, g1 = int(sys.argv[1]), int(sys.argv[2]); seed = sys.argv[i + 1:]
fifo = os.path.join(tempfile.mkdtemp(), "kymo"); os.mkfifo(fifo)
p = subprocess.Popen([G, "run", *seed, "--gens", str(g1), "--kymo", fifo, "--every", "1"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
hist = collections.Counter(); col = None; base = None; died = None; prev = None; ac1 = [0.0, 0]
with open(fifo) as f:
    head = f.readline().rstrip("\n").split(","); s_vals = [int(x) for x in head[2:]]
    for line in f:
        a = line.find(","); b = line.find(",", a + 1)
        if line[a + 1:b] != "0": continue                       # axis 0 only: all 8 faces are images of each other
        g = int(line[:a])
        if base is None: base = g
        if g - base < g0: continue
        row = line.rstrip("\n").split(",")
        if col is None:
            live = [k for k in range(2, len(row)) if row[k] != "0"]
            lo, hi = live[0], live[-1]; col = hi; R = (s_vals[hi - 2] - s_vals[lo - 2]) // 2
        n = int(row[col])
        if n == 0: died = g; break
        hist[n] += 1
        if prev is not None: ac1[0] += n * prev; ac1[1] += 1
        prev = n
p.kill(); os.remove(fifo)
m = (R - 1) // 2; A = 3 * (m + 1) * (m + 2) // 2
N = sum(hist.values()); mu = sum(k * c for k, c in hist.items()) / N
var = sum((k - mu) ** 2 * c for k, c in hist.items()) / N
sk = sum((k - mu) ** 3 * c for k, c in hist.items()) / N / var ** 1.5
rho1 = (ac1[0] / ac1[1] - mu * mu) / var
print(f"{' '.join(seed)}: R={R} A={A} layer s={s_vals[col-2]}; {N} generations from {base + g0}"
      + (f"; face died at {died}" if died else ""))
print(f"  n: mean {mu:.1f} ({mu/A:.3f}/site), var {var:.0f} ({var/A:.2f}/site), skew {sk:+.2f}, lag-1 autocorr {rho1:.2f}, min {min(hist)} ({min(hist)/A:.3f})")
print(f"  Gaussian estimate of J(0)/A = mu^2/(2 var) / A = {mu*mu/(2*var)/A:.4f}")
cum = 0; out = []; xs = [0.30, 0.275, 0.25, 0.225, 0.20, 0.175, 0.15, 0.125, 0.10]
ks = sorted(hist)
for x in xs:
    c = sum(hist[k] for k in ks if k <= x * A)
    out.append(f"x={x}: " + (f"J={-math.log(c/N):.2f} J/A={-math.log(c/N)/A:.4f} (n={c})" if c >= 20 else f"- (n={c})"))
print("  " + "\n  ".join(out))
