"""Lead's independent check of the 2D toy (cross2 neighbourhood, B34/S234): strips H rows deep, L wide, periodic
along the edge; time to the first death of the top or bottom row, censoring strips that settle (period <= 64)
or are cut by three dead columns. Own stepper, numpy.   python3 research/experiments/toy2d_check.py 12 16 20 24   (~3 min)"""
import numpy as np, sys, math
def step(x):
    # x: (reps, H, L) uint8; periodic in L, dead outside in H
    n = np.roll(x, 1, 2) + np.roll(x, -1, 2) + np.roll(x, 2, 2) + np.roll(x, -2, 2)
    p = np.pad(x, ((0, 0), (2, 2), (0, 0)))
    n = n + p[:, 1:-3] + p[:, 3:-1] + p[:, 0:-4] + p[:, 4:]
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8), n
def run(L, H=16, reps=512, T0=200, cap=60000, seed=1, rho=0.45):
    rng = np.random.default_rng(seed); x = (rng.random((reps, H, L)) < rho).astype(np.uint8)
    alive = np.ones(reps, bool); deaths = 0; expo = 0; waits = []; settled = 0; cut = 0
    w8 = rng.integers(1, 2**61, size=(H, L)).astype(np.uint64); hist = np.zeros((64, reps), np.uint64)
    for t in range(1, cap):
        x, _ = step(x)
        hsh = (x.astype(np.uint64) * w8).sum((1, 2))                       # censor settled strips (period <= 64)
        st = alive & (hist == hsh).any(0); hist[t % 64] = hsh
        col = x.any(1)                                                     # censor strips cut by 3 dead columns
        c3 = alive & ~st & (~(col | np.roll(col, 1, 1) | np.roll(col, 2, 1))).any(1)
        settled += int(st.sum()) if t >= T0 else 0; cut += int(c3.sum()) if t >= T0 else 0
        alive &= ~(st | c3)
        top = x[:, 0].any(1); bot = x[:, -1].any(1)
        dead_edge = alive & ~(top & bot)
        if t >= T0:
            deaths += int(dead_edge.sum()); waits += [t - T0] * int(dead_edge.sum()); expo += int(alive.sum())
        alive &= ~dead_edge
        if not alive.any(): break
    k = deaths; tau_first = expo / max(k, 1); w = np.array(waits)
    print(f"L={L} H={H}: {reps} strips, {k} first edge deaths after T0={T0}, settled {settled}, cut {cut}, alive at cap {int(alive.sum())}; "
          f"mean first-death wait {tau_first:.0f} -> tau per edge {2*tau_first:.0f} (ln {math.log(2*tau_first):.2f}); "
          f"law 0.73+0.416L = {0.73+0.416*L:.2f};  CV of waits {w.std()/w.mean():.2f}")
for L in map(int, sys.argv[1:]): run(L)
