#!/usr/bin/env python3
"""Audit: re-derive the clockwork headline facts with the auditor's own stepper (research/audit/independent.py).

For each object: period P, union size, the first k > 0 at which phase k is a symmetric image (O_h x translation)
of phase 0 (so L = k, twist m = P / L), and the multiset of per-cell periods. Expected values are the ones
claimed in research/clockwork/README.md and NOTEBOOK 2026-11-13. ~10 s.

  python3 research/audit/clockwork_check.py      # exit 1 on any mismatch
"""
import itertools, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from independent import step  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CAT = {}
for line in open(os.path.join(ROOT, "research/atlas/catalogue.jsonl")):
    o = json.loads(line)
    CAT[o["id"]] = o


def load(oid):
    if oid in CAT:
        return frozenset(tuple(c) for c in CAT[oid]["cells"])
    path = os.path.join(ROOT, "research/clockwork/objects", oid + ".cells")
    cells = []
    for line in open(path):
        line = line.split("#")[0].split()
        if line:
            cells.append(tuple(int(v) for v in line))
    return frozenset(cells)


OH = [(perm, signs) for perm in itertools.permutations(range(3)) for signs in itertools.product((1, -1), repeat=3)]


def apply(g, S):
    perm, signs = g
    return frozenset(tuple(signs[i] * c[perm[i]] for i in range(3)) for c in S)


def norm(S):
    # translate so the min of each coordinate is 0 or 1 (an even translation keeps the lattice)
    m = [min(c[i] for c in S) for i in range(3)]
    sh = [mi - (mi % 2) for mi in m]
    return frozenset(tuple(c[i] - sh[i] for i in range(3)) for c in S)


def canon_set(S):
    return {norm(apply(g, S)) for g in OH}


def analyse(S0, cap=400):
    orbit = [S0]
    S = S0
    for t in range(1, cap + 1):
        S = step(S)
        if S == S0:
            break
        orbit.append(S)
    else:
        return None
    P = len(orbit)
    images = canon_set(S0)
    L = next(k for k in range(1, P + 1) if k == P or norm(orbit[k]) in images)
    union = frozenset().union(*orbit)
    per = collections.Counter()
    for c in union:
        seq = [c in X for X in orbit]
        q = next(d for d in range(1, P + 1) if P % d == 0 and all(seq[i] == seq[(i + d) % P] for i in range(P)))
        per[q] += 1
    return P, L, len(union), dict(sorted(per.items()))


# id: (period, L, union, per-cell periods or None)
EXPECT = {
    "P66.27a": (66, 33, 45, {1: 2, 33: 3, 66: 40}),
    "P48.34a": (48, 24, 56, None),
    "C48.24a": (48, 8, 42, None),
    "C36.33a": (36, 9, None, None),
    "C12.43a": (12, 2, None, None),
    "C40.24a": (40, 20, 47, None),
    "P15.22a": (15, 5, None, None),
    "C35.29a": (35, 35, 47, None),
}


def main():
    bad = 0
    for oid, (P, L, U, per) in EXPECT.items():
        r = analyse(load(oid))
        ok = r is not None and r[0] == P and r[1] == L and (U is None or r[2] == U) and (per is None or r[3] == per)
        extra = ""
        if oid == "C35.29a" and r:
            extra = f", cells of full period {r[3].get(35, 0)} (claimed 37)"
            ok &= r[3].get(35, 0) == 37
        print(f"{'PASS' if ok else 'FAIL'} {oid}: period {r and r[0]}, first symmetric return L={r and r[1]} "
              f"(twist {r and r[0] // r[1]}), union {r and r[2]}, per-cell periods {r and r[3]}{extra}")
        bad += not ok
    r = analyse(load("C44.26a"))
    ok = r is not None and r[0] == 44 and 44 not in r[3] and set(r[3]) <= {1, 2, 4, 11, 22}
    print(f"{'PASS' if ok else 'FAIL'} C44.26a: period {r and r[0]}, per-cell periods {r and r[3]} (compound: no cell of period 44)")
    bad += not ok
    print("clockwork_check.py:", "ALL OK" if not bad else f"{bad} FAILED")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
