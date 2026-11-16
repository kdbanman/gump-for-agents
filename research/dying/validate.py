#!/usr/bin/env python3
"""validate.py: the death histories written by sd.c against the Rust engine, bit-exact.

For K deaths per group (spread over the dump), the oldest recorded state (511 generations before the check) is
expanded from the orbit graph to the full symmetric cell set and run by `gump run` in open space (the vessel is
exact there by T2) for 511 generations. Compared: the population at every generation with the history's
(node weights summed), and the engine's final cell set with the history's state at the check.
The lives file written by sd.c is compared separately, byte for byte, with sy's (see README).

    python3 research/dying/validate.py [K=12]
"""
import os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from load import geometry, read_dump, SCR, ROOT, H, GROUPS
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')


def check(group, K):
    q = geometry(group)[0]; f = q.f
    hdr, hist = read_dump(os.path.join(SCR, f'dump_{group}.bin'), q.n)
    ok = True
    for d in np.linspace(0, len(hdr) - 1, K).astype(int):
        h = hist[d]; T = H - 1
        pops = (h[::-1].astype(np.int64) * q.w).sum(1)                 # generation g = T - j
        with tempfile.TemporaryDirectory(dir=SCR) as tmp:
            cf, pl, co = (os.path.join(tmp, x) for x in ('c.txt', 'p.txt', 'o.txt'))
            np.savetxt(cf, f.cells[h[T][q.orb]], fmt='%d')
            subprocess.run([GUMP, 'run', '--cells', cf, '--gens', str(T), '--no-halt', '--poplog', pl, '--cells-out', co],
                           capture_output=True, text=True, check=True)
            eg = {int(a): int(b) for a, b in np.loadtxt(pl, dtype=np.int64, ndmin=2)}
            bad = [g for g in range(1, T + 1) if eg.get(g) != pops[g]]
            ec = np.loadtxt(co, dtype=np.int64, comments='#', ndmin=2).reshape(-1, 3)
            same = set(map(tuple, ec.tolist())) == set(map(tuple, f.cells[h[0][q.orb]].tolist()))
        good = not bad and same
        ok &= good
        print(f'{"OK  " if good else "FAIL"} {group:4s} death {d:5d} (life {hdr[d,0]}, replica {hdr[d,1]}, check gen {hdr[d,4]}) '
              f'{T} generations, pop at check {pops[T]}{"" if not bad else "  first mismatch gen " + str(bad[0])}{"" if same else "  final sets differ"}', flush=True)
    return ok


if __name__ == '__main__':
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    res = [check(g, K) for g in GROUPS]
    print('ALL OK' if all(res) else 'SOME FAILED')
