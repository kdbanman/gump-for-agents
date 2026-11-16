"""Lit clock, N = a..b, with gs (exact domain: the diagonal hull, T2): generation at which the cycle is entered and
its period, found by stepping to t0 = 2N + 10 and comparing every later state with that one; then the transient by
comparing X(t) with X(t + P) from t = 0.   python3 clock_scan.py a b"""
import sys
import numpy as np
import gs, clockobj as K
a, b = int(sys.argv[1]), int(sys.argv[2]); bad = []
for N in range(a, b + 1):
    o = K.obj(N) | {K.ign(N)}; D, _ = K.hull_dom(o)
    x = D.run(D.state(o), 2 * N + 10); r = x.copy(); P = None
    for t in range(1, 8 * N + 20):
        x = D.step(x)
        if (x == r).all():
            P = t; break
    y = D.state(o); z = D.run(y, P); t1 = 0
    while not (y == z).all():
        y = D.step(y); z = D.step(z); t1 += 1
    if P != 4 * N + 2 or t1 != max(N - 2, 0):
        bad.append((N, P, t1))
print(f'N = {a}..{b}: period 4N+2 and transient max(N-2,0) for all except {bad}')
