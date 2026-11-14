"""V5: ce2.c's exhaustive counts at L = 3 against an independent numpy enumeration (python3 check_ce2.py)."""
import subprocess, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, '..', '..', '..', 'scratch', 'exam')
exe = os.path.join(SCR, 'ce2')
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', exe, os.path.join(HERE, 'ce2.c')])
L, R = 3, 9                                  # numpy uses 9 rows (rows 7, 8 present): must not matter by generation 3
i = np.arange(2 ** (7 * L), dtype=np.int64)
g = np.zeros((len(i), R, L), np.int8)
for c in range(7 * L):
    g[:, c // L, c % L] = (i >> c) & 1
# rows 7, 8 random (they cannot reach row 0 by generation 3)
rng = np.random.default_rng(1); g[:, 7:, :] = rng.integers(0, 2, (len(i), R - 7, L))
cnt = []
for k in range(3):
    n = np.zeros_like(g)
    for d in (1, -1, 2, -2):
        n += np.roll(g, -d, axis=2)
    for d in (1, 2):
        n[:, d:, :] += g[:, :-d, :]; n[:, :-d, :] += g[:, d:, :]
    g = (((n == 3) | (n == 4)) | ((g == 1) & (n == 2))).astype(np.int8)
    cnt.append(int((g[:, 0, :].sum(1) == 0).sum()))
out = subprocess.run([exe, 'enum', str(L)], capture_output=True, text=True, check=True).stdout.split()
c = [int(out[j]) for j in (5, 7, 9)]
print('numpy', cnt, ' ce2', c, ' soups', out[3])
print('ALL OK' if c == cnt else 'FAIL')
