#!/usr/bin/env python3
"""Bit-for-bit validation of tube1d.c (deterministic limit, no dice) against reference/oracle.py.

The slab with in-plane period lattice (h,k),(0,d) is unfolded into the oracle's cubic array torus of m cubes a side
(H = 2m), where m e1 and m e2 are lattice vectors; the oracle is stepped and every slab cell compared with the
C stepper's lane 0 at every generation; cells of the oracle outside the slab must stay dead.

    python3 validate.py EXE h k d nl m seed gens [bad]
"""
import sys, subprocess, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', '..', '..', 'reference'))
import oracle

def fdiv(a, b): return a // b

def main():
    exe = sys.argv[1]; h, k, d, nl, m, seed, gens = map(int, sys.argv[2:9]); bad = len(sys.argv) > 9
    assert m % d == 0 and (m % h == 0) and ((m // h) * k) % d == 0, "m e1, m e2 must be lattice vectors"
    assert m >= nl + 3
    out = subprocess.run([exe, 'trace', str(h), str(k), str(d), str(nl), str(seed), str(gens)] + (['bad'] if bad else []),
                         capture_output=True, text=True).stdout.split('\n')
    states = [np.frombuffer(l.encode(), dtype=np.uint8).astype(np.int8) - 48 for l in out if l]
    assert len(states) == gens + 1
    H = 2 * m
    imap = -np.ones((H, H, H), np.int64)
    for x in range(H):
        for y in range(H):
            for z in range(H):
                if (x & 1) + (y & 1) + (z & 1) != 1: continue
                a = 0 if x & 1 else 1 if y & 1 else 2
                s = x + y + z; sp = s % H
                if sp > 2 * nl - 1: continue
                p = [x, y, z - (s - sp)]; p[a] -= 1
                i, j, kk = p[0] // 2, p[1] // 2, p[2] // 2
                l = i + j + kk; assert l == (sp - 1) // 2
                X, Y = i, -i - j
                q = X // h; X -= q * h; Y -= q * k; Y %= d
                imap[x, y, z] = ((l * 3 + a) * h + X) * d + Y
    inside = imap >= 0
    N = 3 * h * d * nl
    assert inside.sum() == N * (m * m // (h * d)), (inside.sum(), N)
    masks = oracle.masks(H)
    hh = np.zeros((H, H, H), np.int8); hh[inside] = states[0][imap[inside]]
    bad_gen = None
    for g in range(1, gens + 1):
        hh = oracle.step(hh, masks)
        if hh[~inside].any(): bad_gen = g; print("oracle left the slab at gen", g); break
        if not (hh[inside] == states[g][imap[inside]]).all(): bad_gen = g; break
    pop = int(states[-1].sum())
    if bad_gen is None:
        print(f"OK   ({h},{k}),(0,{d}) nl={nl} m={m} seed={seed}: {gens} generations bit for bit; N={N}; population gen0 {int(states[0].sum())}, last {pop}, distinct states {len(set(s.tobytes() for s in states))}")
    else:
        print(f"FAIL ({h},{k}),(0,{d}) nl={nl} m={m} seed={seed}{' [bad neighbour]' if bad else ''}: first mismatch at generation {bad_gen}")
    sys.exit(0 if bad_gen is None else 1)

main()
