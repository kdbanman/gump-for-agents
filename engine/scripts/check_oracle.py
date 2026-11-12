#!/usr/bin/env python3
"""Cross-language check: `gump` vs reference/oracle.py, state for state, every generation.

  check_oracle.py [--cases N] [--gens G] [--gump PATH]

Random soups (various densities, rules, RNG seeds) on small even-H tori (the oracle's
array-index torus is a proper torus of H/2 cubes for even H). gump writes the full live
set every generation (--trace); the oracle replays from gump's generation-0 state and the
two cell sets are compared at every generation. Also checks a few open-space soups against
the oracle on a padded array (cells never reach the padding, by T2). Exit 1 on mismatch.
"""
import json, os, subprocess, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "reference"))
import oracle  # noqa: E402

GUMP = os.path.join(ROOT, "engine", "target", "release", "gump")


def parse_rule(r):
    b, s = r.split("/")
    return tuple(int(c) for c in b[1:]), tuple(int(c) for c in s[1:])


def trace(args, gens, tmp):
    path = os.path.join(tmp, "trace.txt")
    subprocess.run([GUMP, "run", *args, "--gens", str(gens), "--no-halt", "--trace", path],
                   check=True, capture_output=True, text=True)
    states = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            cells = {tuple(int(v) for v in c.split(",")) for c in parts[1:]}
            states.append((int(parts[0]), cells))
    return states


def oracle_states(cells0, H, shift, gens, rule):
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    for c in cells0:
        h[tuple((v + shift) % H for v in c)] = 1
    out = []
    birth, survive = rule
    for g in range(gens + 1):
        idx = np.argwhere(h == 1)
        out.append({tuple(int(v) - shift for v in p) for p in idx})
        h = oracle.step(h, m, birth, survive)
    return out


def main():
    a = sys.argv[1:]
    ncases, gens = 12, 40
    global GUMP
    while a:
        if a[0] == "--cases": ncases = int(a[1]); a = a[2:]
        elif a[0] == "--gens": gens = int(a[1]); a = a[2:]
        elif a[0] == "--gump": GUMP = a[1]; a = a[2:]
        else: sys.exit(__doc__)
    rules = ["B45/S345", "B45/S345", "B4/S34", "B456/S2345", "B35/S0246"]
    dens = [0.1, 0.25, 0.3, 0.45, 0.6]
    Ns = [4, 5, 6, 7, 8, 9, 10, 12]
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(ncases):
            N, rule, p = Ns[i % len(Ns)], rules[i % len(rules)], dens[i % len(dens)]
            torus = i % 3 != 2
            if torus:
                args = ["--soup", str(p), "--torus", str(N), "--origin", "0,0,0", "--rng", str(100 + i), "--rule", rule]
                H, shift = 2 * N, 0
            else:
                R = N + 3
                args = ["--soup", str(p), "--radius", str(R), "--rng", str(100 + i), "--rule", rule]
                # open space: a padded oracle array; for B>=4 rules nothing leaves the hull
                H, shift = 2 * (R + 4 * 1 + 2), R + 4 + 2
                if shift % 2: shift += 1
                if parse_rule(rule)[0][0] < 4:
                    continue
            got = trace(args, gens, tmp)
            want = oracle_states(got[0][1], H, shift, gens, parse_rule(rule))
            first = next((g for g, (gg, cells) in enumerate(got) if cells != want[g]), None)
            r = {"case": i, "space": f"torus{N}" if torus else f"open oct R={R}", "rule": rule, "density": p,
                 "gens": gens, "seed_pop": len(got[0][1]), "final_pop": len(got[-1][1]), "ok": first is None,
                 "first_mismatch": first}
            print(json.dumps(r), flush=True)
            bad += first is not None
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
