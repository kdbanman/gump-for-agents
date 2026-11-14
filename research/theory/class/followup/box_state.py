"""box_state.py -- what a bond10 B34/S234 box is doing: density and activity (x(t) != x(t-2)) of the interior,
the wall sheets, the layers beneath and the box edges, at ages 10^2 .. 10^5.   python3 box_state.py n [vessel]"""
import sys, json
import numpy as np
import fu, three_d
n = int(sys.argv[1]); kind = sys.argv[2] if len(sys.argv) > 2 else "box"
L = fu.lattice("bond10"); B, S = three_d.rule("bond10", 5)
hi = 2 * n + 1
if kind == "box":
    V = three_d.box_vessel(L, n)
else:
    V = three_d.column_vessel(L, n, n)
P = V.P
inw = lambda a: (P[:, a] == 1) | (P[:, a] == hi)
nb = lambda a: (P[:, a] == 2) | (P[:, a] == hi - 1)
axes = (0, 1, 2) if kind == "box" else (0, 1)
sheet = np.zeros(V.N, bool); beneath = np.zeros(V.N, bool)
for a in axes:
    sheet |= inw(a); beneath |= nb(a)
nsh = sum(inw(a).astype(int) for a in axes)
edge = (sheet & beneath)             # sheet cells of one wall lying in the layer beneath another (edge rows)
groups = dict(interior=~sheet & ~beneath, sheet_not_edge=sheet & ~beneath, edge_rows=edge, beneath_not_edge=beneath & ~sheet)
rng = np.random.default_rng(5)
x = fu.pack((rng.random((64, V.N)) < 0.45).astype(np.uint8))
hist = [fu.unpack(x)]
out = {}
for t in range(1, 100001):
    x = fu.step(V, x, B, S)
    if t in (100, 101, 102, 1000, 1001, 1002, 10000, 10001, 10002, 100000, 100001, 100002):
        hist.append(fu.unpack(x))
    if t in (102, 1002, 10002, 100002):
        u0, u2 = hist[-3], hist[-1]
        out[t - 2] = {k: [round(float(u2[:, m].mean()), 3), round(float((u2[:, m] != u0[:, m]).mean()), 3)]
                      for k, m in groups.items() if m.any()}
print(json.dumps(dict(vessel=kind, n=n, N=V.N, cells={k: int(m.sum()) for k, m in groups.items()},
                      density_activity_by_age=out)))
