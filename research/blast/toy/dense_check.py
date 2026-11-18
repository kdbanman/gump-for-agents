"""Independent exact check of ex1d.c / exg.c on small rows: the full 2^L x 2^L transition matrix in numpy, its
killed block's top eigenvalue, against the C codes (rings and segments; cross2 and rules A, B).
Usage: python3 dense_check.py   -> ALL OK"""
import subprocess, os, sys, itertools, math, re
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'toy')
def lntau(L, ring, R, nc, T, C, rho):
    pb = [math.comb(nc, b) * rho ** b * (1 - rho) ** (nc - b) for b in range(nc + 1)]
    q = lambda e, k: sum(pb[b] for b in range(nc + 1) if k + b + e >= T and k + b <= C)
    N = 1 << L; P = np.zeros((N, N))
    for s in range(N):
        pr = []
        for x in range(L):
            k = 0
            for d in list(range(-R, 0)) + list(range(1, R + 1)):
                y = x + d
                if ring: y %= L
                elif y < 0 or y >= L: continue
                k += (s >> y) & 1
            pr.append(q((s >> x) & 1, k))
        v = np.ones(1)
        for x in range(L): v = np.concatenate([v * (1 - pr[x]), v * pr[x]])   # bit x set in the upper half
        P[s] = v
    lam = max(abs(np.linalg.eigvals(P[1:, 1:]))); return -math.log(1 - lam)
ok = True
for L, ring, R, nc, T, C, rho in [(8, 1, 2, 2, 3, 4, 0.472), (8, 0, 2, 2, 3, 4, 0.472), (9, 0, 2, 2, 3, 4, 0.472), (8, 1, 3, 3, 4, 6, 0.5), (8, 0, 3, 3, 4, 6, 0.5), (8, 1, 1, 2, 2, 2, 0.5), (8, 0, 1, 2, 2, 2, 0.5)]:
    a = lntau(L, ring, R, nc, T, C, rho)
    o = subprocess.run([f'{S}/exg', str(L), str(ring), str(R), str(nc), str(T), str(C), str(rho)], capture_output=True, text=True).stdout
    b = float(re.search(r'lntau (\S+)', o).group(1)); good = abs(a - b) < 1e-7; ok &= good
    print(f'L {L} ring {ring} R {R} coins {nc} T {T} C {C} rho {rho}: dense {a:.9f} exg {b:.9f}', 'OK' if good else 'FAIL')
print('ALL OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
