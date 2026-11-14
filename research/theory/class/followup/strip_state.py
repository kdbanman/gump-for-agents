"""strip_state.py -- is the interior of a kagome4 B2/S12 strip stationary?  64 strips, no reseeding; density and
activity (x(t) != x(t-2)) by depth band at ages 10^2 .. 10^5, and the fraction of replicas still having a wall
row alive.   python3 strip_state.py LAT c ORBIT n depth T"""
import sys, json
import numpy as np
import fu, two_d
name, c, orb, n, depth, T = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
b = two_d.B_OF[name]; L = fu.lattice(name); B, S = fu.capped(b, c, L.K)
V, layers, gd, lab = two_d.strip(name, orb, n, depth)
h = V.h; hs = sorted(set(h.tolist())); dep = np.array([min(hs.index(v), len(hs) - 1 - hs.index(v)) for v in h])
bands = {"0-1": dep <= 1, "2-5": (dep >= 2) & (dep <= 5), "6-11": (dep >= 6) & (dep <= 11), "12+": dep >= 12}
rng = np.random.default_rng(11)
x = fu.pack((rng.random((64, V.N)) < 0.45).astype(np.uint8))
keep = {}
marks = sorted({int(round(10 ** k)) for k in np.arange(2, np.log10(T) + 0.01, 0.5)})
prev = {}
for t in range(1, T + 3):
    x = fu.step(V, x, B, S)
    if t in marks or t - 2 in marks:
        prev[t] = fu.unpack(x)
    if t - 2 in marks:
        u0, u2 = prev[t - 2], prev[t]
        D = fu.unpack(fu.peel(V, ~x, b))
        alive = ~D.any(1)
        keep[t - 2] = dict(no_dead_sealed_set=int(alive.sum()),
                           **{k: [round(float(u2[alive][:, m].mean()), 3) if alive.any() else None,
                                  round(float((u2[alive][:, m] != u0[alive][:, m]).mean()), 3) if alive.any() else None]
                              for k, m in bands.items() if m.any()})
print(json.dumps(dict(lattice=name, c=c, n=n, depth=depth, by_age=keep)))
