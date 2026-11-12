# Per-generation layer populations along (1,1,1) for the legacy side-11 cube. Run from repo root; writes research/scratch/kymo11.npz
import sys, numpy as np
sys.path.insert(0, '/home/user/gump-for-agents/reference')
from oracle import masks, step, fill_box, legacy_seed_span
H = 60; lo, hi = legacy_seed_span(H); m = masks(H); h = fill_box(H, lo, hi, m)
c = (lo + hi) // 2
idx = np.indices((H, H, H)) - c
s = idx.sum(0)                       # layer index along d=(1,1,1), relative to centre (odd values)
R = 31; layers = np.arange(-R, R + 1, 2)      # 32 layers
G = 4218; K = np.zeros((G + 1, len(layers)), np.int32); pop = np.zeros(G + 1, np.int64)
linf = np.zeros(G + 1, np.int32)
def rec(g, h):
    live = h == 1
    K[g] = np.bincount(((s[live] + R) // 2), minlength=len(layers))[:len(layers)]
    pop[g] = live.sum()
    p = np.argwhere(live) - c
    linf[g] = np.abs(p).max() if len(p) else 0
rec(0, h)
for g in range(1, G + 1):
    h = step(h, m); rec(g, h)
np.savez_compressed('research/scratch/kymo11.npz', K=K, pop=pop, linf=linf, layers=layers)
