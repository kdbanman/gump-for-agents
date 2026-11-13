"""validate.py -- gstep (C, bit-sliced) against the numpy reference stepper of vessel.py, on several lattices,
vessels and rules; the sealed-set routine against a plain Python peeling; and the gump lattice definition against
the golden log of the original (side-8 closed cube, reference/golden/legacy_cube_side08_H40.txt).

    python3 validate.py        ->  ALL OK
"""
import os, subprocess, sys, tempfile
import numpy as np
import lattices as LT, theory as TH, vessel as VS

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "..", "..", "scratch", "class")
GSTEP = os.path.join(SCR, "gstep")


def mask(s):
    m = 0
    for k in s:
        m |= 1 << k
    return m


def run_case(name, V, b, c, T=60, p=0.45, seed=1):
    L = V.L
    B, S = TH.capped(b, c, L.K)
    rng = np.random.default_rng(seed)
    x = (rng.random(V.N) < p).astype(np.int8)
    with tempfile.TemporaryDirectory(dir=SCR) as td:
        gf, inf = os.path.join(td, "g.bin"), os.path.join(td, "init.bin")
        V.write(gf)
        open(inf, "wb").write(bytes(x.tolist()))
        out = subprocess.run([GSTEP, "trace", gf, str(mask(B)), str(mask(S)), str(b), inf, "0", str(T)],
                             capture_output=True, text=True, check=True).stdout.split("\n")
    pops = [int(a) for a in out[0].split()]
    final = np.array([int(ch) for ch in out[1].strip()], dtype=np.int8)
    sealed_any = int(out[2])
    kc = np.array([int(ch) for ch in out[3].strip()], dtype=bool)
    y = x.copy()
    ref = []
    for t in range(T):
        y = VS.numpy_step(V, y, B, S)
        ref.append(int(y.sum()))
    kp = VS.max_sealed(V, y == 0, b)
    ok = pops == ref and np.array_equal(final, y) and (np.array_equal(kc, kp) if kp.any() else sealed_any == 0)
    print(f"{'OK ' if ok else 'FAIL'} {name:34s} N={V.N:6d} rule={TH.rule_name(B, S)} pop(T)={ref[-1]} sealed={int(kp.sum())}")
    return ok


def golden():
    """Side-8 closed cube on the doubled-coordinate torus H = 40: populations of generations 1..23."""
    L = LT.get("gump")
    V = VS.torus(L, 20)
    idx = {p: i for i, p in enumerate(V.cells)}
    x = np.zeros(V.N, dtype=np.int8)
    lo, hi = 13, 29
    for p, i in idx.items():
        if all(lo <= a <= hi for a in p):
            x[i] = 1
    B, S = {4, 5}, {3, 4, 5}
    want = [int(l.split()[1]) for l in open(os.path.join(HERE, "..", "..", "..", "reference", "golden", "legacy_cube_side08_H40.txt"))][1:]
    got = []
    for t in range(len(want)):
        x = VS.numpy_step(V, x, B, S)
        got.append(int(x.sum()))
    ok = got == want
    print(f"{'OK ' if ok else 'FAIL'} golden side-8 cube: {len(want)} generations, final population {got[-1]} (want {want[-1]})")
    return ok


if __name__ == "__main__":
    oks = [golden()]
    cases = [
        ("cross2 torus 12", lambda: VS.torus(LT.get("cross2"), 12), 3, 5),
        ("cross2 strip 8x12", lambda: VS.slab(LT.get("cross2"), (0, 1), 8, 12), 3, 5),
        ("moore strip diag 9x10", lambda: VS.slab(LT.get("moore"), (1, 1), 9, 10), 4, 7),
        ("tri6 strip 8x10", lambda: VS.slab(LT.get("tri6"), TH.sealed_rays(LT.get("tri6"), 3)[0], 8, 10), 3, 5),
        ("hex9 torus 4", lambda: VS.torus(LT.get("hex9"), 4), 5, 7),
        ("kagome6 strip", lambda: VS.slab(LT.get("kagome6"), TH.sealed_rays(LT.get("kagome6"), 3)[0], 8, 6), 3, 5),
        ("gump torus 6", lambda: VS.torus(LT.get("gump"), 6), 4, 6),
        ("gump {111} slab 5x4", lambda: VS.slab(LT.get("gump"), (1, 1, 1), 5, 4), 4, 6),
        ("gump {111} slab 1x6 (kagome)", lambda: VS.slab(LT.get("gump"), (1, 1, 1), 1, 6), 4, 6),
        ("gump hull R=6", lambda: VS.hull(LT.get("gump"), 4, 6), 4, 6),
        ("fcc {111} slab 6x5", lambda: VS.slab(LT.get("fcc"), (1, 1, 1), 6, 5), 4, 6),
        ("bcc8 {110} slab 6x5", lambda: VS.slab(LT.get("bcc8"), (1, 1, 0), 6, 5), 3, 5),
        ("sc18 slab 5x6", lambda: VS.slab(LT.get("sc18"), (1, 0, 0), 5, 6), 6, 9),
        ("bond10 slab 6x4", lambda: VS.slab(LT.get("bond10"), (1, 1, 1), 6, 4), 4, 6),
        ("cross3 box hull R=5", lambda: VS.hull(LT.get("cross3"), 4, 5), 4, 6),
    ]
    for name, mk, b, c in cases:
        V = mk()
        # structural checks: degree, symmetry, face sizes
        for i, lst in enumerate(V.nbr):
            for q in lst:
                if q >= 0:
                    assert i in V.nbr[q], (name, "asymmetric graph")
        oks.append(run_case(name, V, b, c))
    print("ALL OK" if all(oks) else "SOME FAILED")
    sys.exit(0 if all(oks) else 1)
