"""V4: parity.c's trace against an independent numpy stepper, bit for bit (python3 check_parity.py)."""
import subprocess, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, '..', '..', '..', 'scratch', 'exam')
exe = os.path.join(SCR, 'parity')
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', exe, os.path.join(HERE, 'parity.c')])

def ref_step(g):
    H1, L = g.shape; n = np.zeros_like(g)
    out = np.zeros_like(g)
    def get(j, dx):  # row j shifted so that result[x] = g[j, x + dx]; rows outside -> 0
        return np.roll(g[j], -dx) if 0 <= j < H1 else np.zeros(L, g.dtype)
    for j in range(H1):
        if j == 0:
            k = sum(get(0, d) for d in (-2, -1, 1, 2)) + get(1, 0) + get(2, 0)
            out[0] = np.where(g[0] == 1, np.isin(k, (2, 3, 4)), np.isin(k, (3, 4)))
        else:
            k = sum(get(j, d) for d in (-2, -1, 1, 2)) + get(j - 1, 0) + get(j - 2, 0) + get(j + 1, 0) + get(j + 2, 0)
            out[j] = k % 2
    return out.astype(np.int64)

ok = True
for L, H, gens, seed in ((6, 9, 25, 1), (12, 40, 30, 7), (16, 20, 40, 3), (5, 3, 20, 11)):
    txt = subprocess.run([exe, 'trace', str(L), str(H), str(gens), str(seed)], capture_output=True, text=True, check=True).stdout
    blocks = [b.strip().split('\n')[1:] for b in txt.split('gen ')[1:]]
    grids = [np.array([[int(c) for c in row] for row in b]) for b in blocks]
    g = grids[0]
    for t in range(1, gens + 1):
        g = ref_step(g)
        if not np.array_equal(g, grids[t]):
            print('MISMATCH', L, H, t); ok = False; break
    print('L=%d H=%d %d generations: %s (row-0 population at the end %d)' % (L, H, gens, 'identical' if ok else 'FAIL', grids[-1][0].sum()))
print('ALL OK' if ok else 'FAIL')
