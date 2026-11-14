#!/usr/bin/env python3
"""Re-derive the memorylessness numbers for O_h vertex R = 40 from the raw lives in PR 8's JSON (own code).
  python3 research/audit/gpu_pr8/lineage_r40.py PR8_WORKTREE"""
import base64, json, math, os, sys, zlib
import numpy as np
r = json.load(open(os.path.join(sys.argv[1], 'research/data/gpu_facelaw/symvR40_s103_A10G.json')))
a, k, b = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), np.int64).reshape(r['raw']['shape'])
G, T0 = r['gens'], 1000
keep = a >= T0
D = int(((k == 1) & keep).sum()); X = (a[keep] - T0).sum(); tau = X / D
print(f'tau = {tau:.4g} ({D} deaths), ln tau = {math.log(tau):.3f} +- {1 / math.sqrt(D):.3f}; kinds {np.unique(k, return_counts=True)}')
# settled lives: how long did they live, and what share of exposure
st = (k >= 2) & keep
print(f'settled after T0: {st.sum()}, their exposure share {(a[st] - T0).sum() / X:.2e}')
# without the settled lives' exposure, and with settled counted as censored (as here): both
print(f'tau excluding settled lives entirely: {(a[keep & ~st] - T0).sum() / D:.4g}')
for Lm in (5, 10):
    L = Lm * tau
    sel = keep & (b <= G - T0 - L) & (k < 2)
    rr = (a[sel] - T0).astype(float); died = (k[sel] == 1) & (rr < L); x = np.where(died, rr, L); n = sel.sum()
    m1 = 1 - math.exp(-Lm); m2 = 2 * (1 - math.exp(-Lm) * (1 + Lm)); cve = math.sqrt(m2 / m1 ** 2 - 1)
    print(f'complete lives (born >= {Lm} tau before the end): {n}; CV {x.std() / x.mean():.4f} (exp {cve:.4f}); '
          f'P(>4tau) {(rr >= 4 * tau).mean():.4f} (0.0183); P(<0.05tau) {(rr < 0.05 * tau).mean():.4f} (0.0488)')
# the full-sample hazard, all lives, censoring handled exactly
x = (a[keep] - T0) / tau; d = (k[keep] == 1)
edges = [0, .001, .01, .05, .25, .5, 1, 2, 3, 4, 6, 10]
print('hazard x tau by age/tau (all lives):', ', '.join(
    f'[{lo},{hi}) {int((d & (x >= lo) & (x < hi)).sum())}/{np.clip(np.minimum(x, hi) - lo, 0, None).sum():.0f}' for lo, hi in zip(edges[:-1], edges[1:])))
