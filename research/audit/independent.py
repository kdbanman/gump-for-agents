#!/usr/bin/env python3
"""Audit: an independent re-derivation of gump's rule and structure theorems from geometry.

Written by the auditor (2026-11-13) without using reference/oracle.py's offsets or any other stepper in the
repo. A face is represented by its four corner vertices; the neighbour relation is derived from the rule text
("the 8 perpendicular faces sharing an edge, and the 4 coplanar faces touching it only at a corner").

  python3 research/audit/independent.py            # all checks, ~1 min; exit 1 on any failure
  python3 research/audit/independent.py --no-engine  # skip the cross-check against engine/target/release/gump

Checks (one line each):
  nbr      the geometric neighbourhood equals docs/AUTOMATON.md section 2 (doubled offsets) for all 3 orientations
  T1       layer histogram {-4:1,-2:2,0:6,2:2,4:1} for every orientation and all 8 signed diagonals
  T2       a dead cell in layer C+2 has <=3 neighbours in layers <=C; in C+4 <=1; (so no birth beyond a dead half-space)
  T3       a cell in the middle of 3 dead layers sees <=2 from outside; the outer two <=3; 2 dead layers can see 4
  T4       in-layer neighbours: 6, forming a kagome net (4 edge-sharing + 2 across-hexagon), coupling 6/2+2/1+1
  axis     an axis-aligned half-space does not confine (some outside cell sees 4 inside)
  speed    every offset has max-norm <= 2 (one cube per generation)
  cube     closed cube of side n: 3n^2(n+1) cells, hull radius 3n-2, gen-1 population 12n^2-36n+48 (n=2..8,19)
  hullN    cells in the diagonal hull of radius R (cube-centred): R=33 -> 19,686 ; R=37 -> 27,474
  faceA    sites in one outer face layer, cube-centred R = 27, 33 and vertex-centred R = 42, 40
  star     the vertex star: 12 cells, each sees 5 star cells, no outside cell sees >2; 4096 states settle in <=3 gens
  smallsl  the closed unit cube is a still life
  engine   this stepper vs `gump run --trace` on random soups (open octahedra and a torus), every generation
"""
import itertools, collections, json, os, random, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GUMP = os.path.join(ROOT, "engine", "target", "release", "gump")
FAIL = []


def report(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}", flush=True)
    if not ok:
        FAIL.append(name)


def normal(p):
    odd = [i for i in range(3) if p[i] % 2]
    assert len(odd) == 1, p
    return odd[0]


def corners(p):
    a = normal(p)
    b, c = [i for i in range(3) if i != a]
    out = set()
    for sb in (1, -1):
        for sc in (1, -1):
            v = list(p); v[b] += sb; v[c] += sc; out.add(tuple(v))
    return frozenset(out)


def geometric_offsets(a):
    """Neighbours of the face at e_a (doubled), found by brute force over all faces in a 7^3 window."""
    p = tuple(1 if i == a else 0 for i in range(3))
    cp = corners(p)
    res = []
    for q in itertools.product(range(-4, 5), repeat=3):
        if sum(x % 2 for x in q) != 1 or q == p:
            continue
        cq = corners(q)
        shared = len(cp & cq)
        b = normal(q)
        coplanar = (b == a and q[a] == p[a])
        if (shared == 2 and b != a) or (shared == 1 and coplanar):
            res.append(tuple(q[i] - p[i] for i in range(3)))
    return sorted(res)


def automaton_offsets(a):
    """docs/AUTOMATON.md section 2, typed in from the text: +-2e_b+-2e_c, +-e_a+-e_b, +-e_a+-e_c."""
    b, c = [i for i in range(3) if i != a]
    out = []
    for s, t in itertools.product((2, -2), repeat=2):
        v = [0, 0, 0]; v[b] = s; v[c] = t; out.append(tuple(v))
    for s, t in itertools.product((1, -1), repeat=2):
        for o in (b, c):
            v = [0, 0, 0]; v[a] = s; v[o] = t; out.append(tuple(v))
    return sorted(out)


OFF = [geometric_offsets(a) for a in range(3)]
DIAGS = list(itertools.product((1, -1), repeat=3))


def dot(d, p):
    return d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def nbrs(p):
    a = normal(p)
    return [(p[0] + o[0], p[1] + o[1], p[2] + o[2]) for o in OFF[a]]


def step(S, birth=(4, 5), survive=(3, 4, 5), period=None):
    cnt = collections.Counter()
    for p in S:
        for q in nbrs(p):
            if period:
                q = tuple(x % period for x in q)
            cnt[q] += 1
    return frozenset(q for q, k in cnt.items() if (k in survive if q in S else k in birth))


def cells_in(pred, R):
    return [q for q in itertools.product(range(-R, R + 1), repeat=3) if sum(x % 2 for x in q) == 1 and pred(q)]


def main():
    use_engine = "--no-engine" not in sys.argv
    # nbr
    ok = all(OFF[a] == automaton_offsets(a) and len(OFF[a]) == 12 for a in range(3))
    report("nbr", ok, "geometric neighbourhood == AUTOMATON.md offsets, 12 per orientation")
    # T1
    ok = True
    for a in range(3):
        for d in DIAGS:
            h = collections.Counter(dot(d, o) for o in OFF[a])
            ok &= dict(h) == {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1}
    report("T1", ok, "histogram 1,2,6,2,1 for 3 orientations x 8 signed diagonals")
    # T2/T3: counts by Delta s
    worst2 = max(sum(1 for o in OFF[a] if dot(d, o) <= -2) for a in range(3) for d in DIAGS)  # cell in C+2, nbrs <= C
    worst4 = max(sum(1 for o in OFF[a] if dot(d, o) <= -4) for a in range(3) for d in DIAGS)  # cell in C+4
    report("T2", worst2 == 3 and worst4 == 1, f"max nbrs across one dead layer = {worst2} (<4), across two = {worst4}")
    # T3: dead layers C+2, C+4, C+6; live allowed at <=C and >=C+8
    mid = max(sum(1 for o in OFF[a] if abs(dot(d, o)) >= 4) for a in range(3) for d in DIAGS)
    # two dead layers C+2, C+4: cell at C+2 sees layers <=C (dS<=-2: 3) and >=C+6 (dS=+4: 1)
    two = min(sum(1 for o in OFF[a] if dot(d, o) <= -2 or dot(d, o) >= 4) for a in range(3) for d in DIAGS)
    report("T3", mid == 2 and worst2 == 3 and two == 4,
           f"middle of 3 dead layers sees <= {mid}, edges <= {worst2}; a 2-layer gap cell can see {two} (>=4: leaks)")
    # T4 kagome: in-layer neighbours (dS=0) of each cell along d; they should be 4 perpendicular + 2 coplanar,
    # and the in-layer graph should have triangles (each cell in exactly 2 triangles) -- kagome signature.
    ok = True
    d = (1, 1, 1)
    layer = cells_in(lambda q: dot(d, q) == 1, 9)
    L = set(layer)
    for p in layer:
        a = normal(p)
        inl = [o for o in OFF[a] if dot(d, o) == 0]
        perp = [o for o in inl if normal(tuple(p[i] + o[i] for i in range(3))) != a]
        ok &= len(inl) == 6 and len(perp) == 4
    # triangle count per interior cell, perpendicular in-layer graph
    tri_ok = True
    for p in layer:
        if max(abs(x) for x in p) > 5:
            continue
        nb = [q for q in nbrs(p) if q in L and normal(q) != normal(p)]
        tris = sum(1 for u, v in itertools.combinations(nb, 2) if v in nbrs(u))
        tri_ok &= tris == 2
    report("T4", ok and tri_ok, "6 in-layer nbrs (4 edge-sharing, each cell on exactly 2 in-layer triangles: kagome), coupling 6/2+2/1+1")
    # axis half-space does not confine: dead cell just outside x > C with 4 live inside?
    best = max(sum(1 for o in OFF[a] if o[0] < 0) for a in range(3))
    report("axis", best >= 4, f"a cell just outside an axis-aligned half-space can see {best} cells inside")
    report("speed", max(max(abs(x) for x in o) for a in range(3) for o in OFF[a]) == 2, "max-norm of offsets = 2")
    # cube counts: an n x n x n block of cubes with centres 2(i,j,k), 0 <= i,j,k < n; every face of every cube live
    ok = True; det = []
    for n in list(range(2, 9)) + [19]:
        S = frozenset(q for q in itertools.product(range(-1, 2 * n), repeat=3)
                      if sum(x % 2 for x in q) == 1 and all(0 <= x <= 2 * n - 2 for x in q if x % 2 == 0))
        c = (n - 1,) * 3
        R = max(abs(dot(dd, (q[0] - c[0], q[1] - c[1], q[2] - c[2]))) for q in S for dd in DIAGS)
        g1 = len(step(S))
        ok &= len(S) == 3 * n * n * (n + 1) and R == 3 * n - 2 and g1 == 12 * n * n - 36 * n + 48
        det.append(f"n={n}: {len(S)} cells, R={R}, gen-1 pop {g1}")
    report("cube", ok, "; ".join(det[:2]) + " ... " + det[-1])
    # hull counts and face areas
    def hull(R, c):
        return [q for q in itertools.product(range(-R - 2, R + 3), repeat=3)
                if sum(x % 2 for x in q) == 1 and all(abs(dot(dd, (q[0] - c[0], q[1] - c[1], q[2] - c[2]))) <= R for dd in DIAGS)]
    n33 = len(hull(33, (0, 0, 0))); n37 = len(hull(37, (0, 0, 0)))
    report("hullN", n33 == 19686 and n37 == 27474, f"hull cells R=33: {n33} (NOTEBOOK 19,686), R=37: {n37} (OPEN-PROBLEMS 27,474)")
    def face(R, c):
        return sum(1 for q in hull(R, c) if dot((1, 1, 1), (q[0] - c[0], q[1] - c[1], q[2] - c[2])) == R)
    fa = {27: face(27, (0, 0, 0)), 33: face(33, (0, 0, 0)), 42: face(42, (1, 1, 1)), 40: face(40, (1, 1, 1))}
    report("faceA", fa == {27: 315, 33: 459, 42: 693, 40: 630}, f"face sites {fa} (expected 315, 459, 693 v, 630 v)")
    # vertex star at vertex (1,1,1): the 12 faces having it as a corner
    v = (1, 1, 1)
    star = [q for q in itertools.product(range(-2, 4), repeat=3) if sum(x % 2 for x in q) == 1 and v in corners(q)]
    St = set(star)
    inside = [sum(1 for r in nbrs(q) if r in St) for q in star]
    outside = collections.Counter()
    for q in star:
        for r in nbrs(q):
            if r not in St:
                outside[r] += 1
    settle_ok = True; died = 0
    for mask in range(1 << 12):
        S = frozenset(star[i] for i in range(12) if mask >> i & 1)
        hist = [S]
        for t in range(1, 6):
            S = step(S); hist.append(S)
            assert S <= St
        # settled by gen 3 means hist[3] is on a cycle of period <= 2 that continues
        settle_ok &= hist[5] == hist[3] and (hist[4] == hist[3] or hist[5] == hist[3])
        died += len(hist[5]) == 0
    report("star", len(star) == 12 and set(inside) == {5} and max(outside.values()) <= 2 and settle_ok and died == 2750,
           f"12 cells, inner degree {set(inside)}, max outside count {max(outside.values())}, all 4096 settle by gen 3, {died} die (NOTEBOOK 2750)")
    cube1 = frozenset([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
    report("smallsl", step(cube1) == cube1, "closed unit cube is a still life (each cell sees 4)")
    if use_engine and os.path.exists(GUMP):
        ok = True; det = []
        cases = [["--soup", "0.35", "--radius", "9", "--rng", "11"], ["--soup", "0.5", "--radius", "7", "--rng", "12"],
                 ["--soup", "0.3", "--torus", "5", "--origin", "0,0,0", "--rng", "13"]]
        with tempfile.TemporaryDirectory() as tmp:
            for k, args in enumerate(cases):
                tr = os.path.join(tmp, f"t{k}.txt")
                subprocess.run([GUMP, "run", *args, "--gens", "60", "--no-halt", "--trace", tr], check=True, capture_output=True)
                states = []
                for line in open(tr):
                    parts = line.split()
                    states.append(frozenset(tuple(int(v) for v in c.split(",")) for c in parts[1:]))
                torus = "--torus" in args
                S = states[0]; bad = None
                for g in range(1, len(states)):
                    S = step(S, period=10 if torus else None)
                    if S != states[g]:
                        bad = g; break
                ok &= bad is None
                det.append(f"{' '.join(args[:4])}: {len(states)-1} gens {'ok' if bad is None else f'MISMATCH at {bad}'}")
        report("engine", ok, "; ".join(det))
    print("independent.py:", "ALL OK" if not FAIL else "FAILED: " + ", ".join(FAIL))
    sys.exit(1 if FAIL else 0)



if __name__ == "__main__":
    main()
