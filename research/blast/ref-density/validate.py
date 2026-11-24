#!/usr/bin/env python3
"""ref-density: rd.c's stepper against reference/oracle.py, bit for bit, on the octahedral hull.

  python3 research/blast/ref-density/validate.py RD_BINARY [GENS]

For R = 11 and R = 9 and seeds 101, 202: rd's lanes 0..2 (three soups at density 0.35 inside the hull) are
compared with the oracle's state, generation by generation, on a box of side 2R+4 (shift R+1, even, so parity
is kept; the hull confines a pattern by T2, so the box is the hull vessel). Checked each generation: every hull
cell, no live cell outside the hull in the oracle, the watched face's population, the eight faces' emptiness.
Negative control: RD_NEGCTL=1 (one neighbour of every x-normal cell swapped from corner-touching to
edge-sharing) must disagree. Exit status 0 iff every positive check passes and every negative control fails.
"""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "reference"))
import oracle  # noqa: E402

FACES = [(s0, s1, s2) for s0 in (1, -1) for s1 in (1, -1) for s2 in (1, -1)]  # rd.c's face order


def run(binary, R, seed, gens, negctl):
    env = dict(os.environ)
    if negctl:
        env["RD_NEGCTL"] = "1"
    else:
        env.pop("RD_NEGCTL", None)
    out = subprocess.run([binary, str(R), "validate", str(seed), str(gens)], capture_output=True, text=True,
                         env=env, check=True).stdout.split("\n")
    cells = [tuple(map(int, l.split()[1:])) for l in out if l.startswith("C ")]
    recs = {}
    for l in out:
        if l.startswith("G "):
            _, g, lane, F, emp, hx = l.split()
            bits = []
            for ch in hx:
                v = int(ch, 16)
                bits += [(v >> j) & 1 for j in range(4)]
            recs[(int(g), int(lane))] = (int(F), emp, np.array(bits[:len(cells)], np.int8))
    return cells, recs


def check(binary, R, seed, gens, negctl):
    cells, recs = run(binary, R, seed, gens, negctl)
    H, sh = 2 * R + 4, R + 1
    m = oracle.masks(H)
    idx = np.array([[x + sh, y + sh, z + sh] for x, y, z in cells])
    inhull = np.zeros((H, H, H), bool)
    inhull[idx[:, 0], idx[:, 1], idx[:, 2]] = True
    facecells = [[i for i, p in enumerate(cells) if sum(d[k] * p[k] for k in range(3)) == R] for d in FACES]
    first_bad = None
    for lane in range(3):
        h = np.zeros((H, H, H), np.int8)
        h[idx[:, 0], idx[:, 1], idx[:, 2]] = recs[(0, lane)][2]
        for g in range(gens + 1):
            if g:
                h = oracle.step(h, m)
            F, emp, bits = recs[(g, lane)]
            ost = h[idx[:, 0], idx[:, 1], idx[:, 2]]
            ok = (ost == bits).all() and not (h.astype(bool) & ~inhull).any()
            ok = ok and F == int(ost[facecells[0]].sum())
            ok = ok and emp == "".join("1" if not ost[fc].any() else "0" for fc in facecells)
            if not ok:
                first_bad = (lane, g) if first_bad is None or g < first_bad[1] else first_bad
                break
    return first_bad, len(cells)


def main():
    binary = sys.argv[1]
    gens = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    allok = True
    for R in (11, 9):
        for seed in (101, 202):
            bad, nc = check(binary, R, seed, gens, False)
            print(f"R={R} ({nc} cells) seed {seed}: 3 soups x {gens} generations: " +
                  ("identical (state, watched population, 8 face-empty flags)" if bad is None else f"MISMATCH lane {bad[0]} gen {bad[1]}"))
            allok &= bad is None
        bad, _ = check(binary, R, 101, gens, True)
        print(f"R={R} negative control (RD_NEGCTL=1): " + ("FAILS as it must, first at lane %d gen %d" % bad if bad else "PASSES (bad)"))
        allok &= bad is not None
    print("VALIDATION PASSED" if allok else "VALIDATION FAILED")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
