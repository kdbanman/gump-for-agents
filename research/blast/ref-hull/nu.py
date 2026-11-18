#!/usr/bin/env python3
"""nu.py DIR  -- referee's analysis of the dip-rate route (split-hull's forecast).
Reads DIR/nu<R>.txt (lines of `rh nu`), prints: (a) ln nu(p P-bar) with replication errors against split-hull's
table; (b) -ln q(p) = ln tau(anchor) + ln nu(p), straight line in A, line + rim term, and what each says at
R = 17 (and 19, 21 when measured); fixed-density levels too."""
import sys, math, glob, os
import numpy as np
D = sys.argv[1]
ANCH = {9: (9.819, 0.005), 11: (13.633, 0.005), 13: (18.141, 0.005), 15: (23.3392, 0.0099)}   # errors of 9, 11 assumed
THEIRS = {  # split-hull README, DIPTABLE (value, Poisson error) at p = .85 .8 .7 .6 .5 .4 .3
 9: (21.597, [(-2.503, 0), (-2.797, 0), (-3.455, .001), (-4.208, .001), (-5.058, .002), (-5.988, .003), (-6.978, .004)]),
 11: (31.255, [(-2.620, 0), (-2.994, 0), (-3.881, .001), (-4.965, .002), (-6.239, .003), (-7.659, .006), (-9.172, .012)]),
 13: (42.445, [(-2.730, 0), (-3.212, .001), (-4.400, .001), (-5.899, .002), (-7.687, .004), (-9.669, .014), (-11.770, .039)]),
 15: (55.203, [(-2.891, 0), (-3.492, 0), (-5.026, .001), (-7.005, .002), (-9.354, .006), (-11.999, .021), (-14.785, .097)]),
 17: (69.480, [(-3.063, 0), (-3.811, 0), (-5.765, .001), (-8.304, .003), (-11.299, .015), (-14.727, .086), None]),
 19: (85.381, [(-3.264, 0), (-4.172, 0), (-6.595, .002), (-9.749, .007), (-13.450, .049), None, None]),
 21: (102.780, [(-3.490, 0), (-4.589, .001), (-7.545, .003), (-11.387, .018), None, None, None]),
}
PS = [0.85, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
runs = {}
for fn in glob.glob(os.path.join(D, "nu*.txt")):
    for line in open(fn):
        t = line.split()
        if not t or t[0] != "NU": continue
        d = {t[i]: t[i + 1] for i in range(1, t.index("cross"), 2)}
        d["cross"] = np.array(list(map(float, t[t.index("cross") + 1:])))
        runs.setdefault(int(d["R"]), []).append(d)
Rs = sorted(runs)
info = {}
for R in Rs:
    rs = runs[R]; K = len(rs)
    expo = np.array([float(r["expo"]) for r in rs]); cr = np.array([r["cross"] for r in rs])
    pbar = sum(float(r["sumP"]) for r in rs) / sum(float(r["nP"]) for r in rs)
    sig = math.sqrt(sum(float(r["sumP2"]) for r in rs) / sum(float(r["nP"]) for r in rs) - pbar ** 2)
    nu = cr.sum(0) / (8 * expo.sum())                       # pooled, per face
    per = cr / (8 * expo[:, None])
    rel = per.std(0, ddof=1) / math.sqrt(K) / np.where(nu > 0, nu, 1)       # replication error of ln nu
    poi = 1 / np.sqrt(np.maximum(cr.sum(0), 1))
    pbs = [float(r["sumP"]) / float(r["nP"]) for r in rs]
    info[R] = dict(K=K, expo=expo.sum(), pbar=pbar, sig=sig, nu=nu, err=np.maximum(rel, poi), cnt=cr.sum(0), A=int(rs[0]["A"]), per=per,
                   pbe=float(np.std(pbs, ddof=1) / math.sqrt(K)),
                   lamA=int(rs[0]["lamA"]), deaths=sum(int(r["deaths"]) for r in rs))
def lnnu(R, L):
    """ln nu at real level L (linear interpolation of ln nu in L), its error, and the event count at floor(L)."""
    I = info[R]; lo = int(math.floor(L)); hi = lo + 1; f = L - lo
    if lo < 0 or hi >= len(I["nu"]) or I["cnt"][lo] < 20: return None
    v = (1 - f) * math.log(I["nu"][lo]) + f * math.log(I["nu"][hi])
    e = (1 - f) * I["err"][lo] + f * I["err"][hi]
    return v, e, I["cnt"][lo]
print("PART A: plain-running dip rates (first passages of P <= L per hull-generation and per face, from above lamA = ceil(P-bar))")
for R in Rs:
    I = info[R]; th = THEIRS.get(R)
    dl = f"; direct ln tau = ln(8E/D) = {math.log(8 * I['expo'] / I['deaths']):.4f} +- {1 / math.sqrt(I['deaths']):.4f} ({I['deaths']} first deaths)" if I["deaths"] > 30 else f"; {I['deaths']} first deaths"
    print(f" R {R} A {I['A']} K {I['K']} exposure {I['expo']:.3g} hull-gens x 8 faces; P-bar {I['pbar']:.4f} +- {I['pbe']:.4f} (split-hull {th[0] if th else '?'}), sigma {I['sig']:.3f}, lamA {I['lamA']}{dl}")
    for j, p in enumerate(PS):
        r = lnnu(R, p * I["pbar"])
        if r is None: continue
        s = f"   p {p}: ln nu = {r[0]:.4f} +- {r[1]:.4f} ({int(r[2])} events)"
        if th and th[1][j]:
            tv, te = th[1][j]; ce = math.hypot(r[1], max(te, 0.0005))
            s += f"   split-hull {tv:.3f} +- {te:.3f}   diff {r[0] - tv:+.4f} = {(r[0] - tv) / ce:+.1f} combined errors"
        print(s)
def fit(xs, ys, es, cols, x0s):
    X = np.array([[c(x) for c in cols] for x in xs]); W = np.diag(1 / np.array(es) ** 2)
    cov = np.linalg.inv(X.T @ W @ X); b = cov @ X.T @ W @ np.array(ys)
    chi2 = float(((np.array(ys) - X @ b) ** 2 / np.array(es) ** 2).sum())
    out = []
    for x0 in x0s:
        v = np.array([c(x0) for c in cols]); out.append((float(v @ b), float(math.sqrt(v @ cov @ v))))
    return b, np.sqrt(np.diag(cov)), chi2, out
kof = lambda R: (R + 1) // 2
Aof = lambda R: 3 * kof(R) * (kof(R) + 1) // 2
FIT = [R for R in (9, 11, 13, 15) if R in info]; EXT = [R for R in (7, 17, 19, 21) if R in info]
def block(name, level):
    pts = [(R, lnnu(R, level(R))) for R in FIT]
    if any(v is None for _, v in pts) or len(pts) < 4: print(f" {name}: not enough events at the fit sizes"); return
    ys = [ANCH[R][0] + v[0] for R, v in pts]; es = [math.hypot(ANCH[R][1], v[1]) for R, v in pts]
    line = fit(FIT, ys, es, [lambda R: 1.0, lambda R: float(Aof(R))], EXT)
    rim = fit(FIT, ys, es, [lambda R: 1.0, lambda R: float(Aof(R)), lambda R: float(kof(R))], EXT)
    sd = [ys[i + 2] - 2 * ys[i + 1] + ys[i] for i in range(2)]
    print(f" {name}: -ln q = " + " ".join(f"{y:.3f}" for y in ys) + f"   second differences in k {sd[0]:.3f} {sd[1]:.3f}")
    print(f"     line a + cA: c = {line[0][1]:.5f} +- {line[1][1]:.5f}, chi2 {line[2]:.1f} on 2;   with rim a + cA + rk: c = {rim[0][1]:.4f} +- {rim[1][1]:.4f}, r = {rim[0][2]:+.3f} +- {rim[1][2]:.3f}, chi2 {rim[2]:.1f} on 1")
    for i, R in enumerate(EXT):
        v = lnnu(R, level(R))
        if v is None: continue
        l = line[3][i]; q = rim[3][i]
        rep = ys[3] + (ys[3] - ys[2]) * 0 + 0   # placeholder
        # constant second difference continued from the last three points (exact quadratic in k through R = 11, 13, 15)
        n = kof(R) - 8; quad3 = ys[3] + n * (ys[3] - ys[2]) + n * (n + 1) / 2 * sd[1]
        print(f"     R {R}: ln nu = {v[0]:.4f} +- {v[1]:.4f};  ln tau: line {l[0] - v[0]:.3f} +- {math.hypot(l[1], v[1]):.3f} | line+rim {q[0] - v[0]:.3f} +- {math.hypot(q[1], v[1]):.3f} | last second difference repeated {quad3 - v[0]:.3f}")
print("\nPART B: -ln q(p) = ln tau(anchor) + ln nu(p P-bar) at R = 9, 11, 13, 15; fits; forecasts (anchor errors of R = 9, 11 assumed 0.005)")
for p in PS: block(f"p = {p}", lambda R, p=p: p * info[R]["pbar"])
print("\nPART C: the same at fixed density x (level L = x A)")
for x in (0.40, 0.36, 0.32, 0.30, 0.28, 0.26, 0.24, 0.20, 0.16): block(f"x = {x}", lambda R, x=x: x * Aof(R))
print("\nPART D: second differences in k of ln nu at p = 0.6 and 0.5 (centred on R = 11 ...)")
for p in (0.6, 0.5):
    v = [lnnu(R, p * info[R]["pbar"]) for R in Rs]; v = [x for x in v if x is not None]
    print(f" p = {p}: " + "  ".join(f"{v[i + 2][0] - 2 * v[i + 1][0] + v[i][0]:+.3f}+-{math.sqrt(v[i + 2][1] ** 2 + 4 * v[i + 1][1] ** 2 + v[i][1] ** 2):.3f}" for i in range(len(v) - 2)))

def lndiff(R, L1, L2):
    """ln nu(L1) - ln nu(L2) with a replication error (per-seed differences when every seed has events)."""
    a, b = lnnu(R, L1), lnnu(R, L2)
    if a is None or b is None: return None
    I = info[R]; per = I["per"]; vals = []
    for k in range(I["K"]):
        def one(L):
            lo = int(math.floor(L)); f = L - lo
            if per[k][lo] <= 0 or per[k][lo + 1] <= 0: return None
            return (1 - f) * math.log(per[k][lo]) + f * math.log(per[k][lo + 1])
        x, y = one(L1), one(L2)
        if x is None or y is None: vals = None; break
        vals.append(x - y)
    e = float(np.std(vals, ddof=1) / math.sqrt(len(vals))) if vals else math.hypot(a[1], b[1])
    return a[0] - b[0], max(e, 1e-4)
print("\nPART E: a test that needs no lifetime. ln q(p1) - ln q(p2) = ln nu(p2) - ln nu(p1) exactly, so 'no rim term in -ln q below 0.6'")
print("        says y = ln nu(0.6 P-bar) - ln nu(p P-bar) is a straight line in A at EVERY size. Line fitted on R = 9..15 only, then compared at R = 7 and at R = 17, 19, 21.")
def partE(name, lev1, lev2):
    pts = [(R, lndiff(R, lev1(R), lev2(R))) for R in FIT]
    if any(v is None for _, v in pts): print(f" {name}: not enough events"); return
    ys = [v[0] for _, v in pts]; es = [v[1] for _, v in pts]
    line = fit(FIT, ys, es, [lambda R: 1.0, lambda R: float(Aof(R))], EXT)
    rim = fit(FIT, ys, es, [lambda R: 1.0, lambda R: float(Aof(R)), lambda R: float(kof(R))], EXT)
    print(f" {name}: y(9..15) = " + " ".join(f"{y:.4f}+-{e:.4f}" for y, e in zip(ys, es)) + f";  line: slope {line[0][1]:.5f} +- {line[1][1]:.5f}, chi2 {line[2]:.1f} on 2;  rim term if allowed: r = {rim[0][2]:+.4f} +- {rim[1][2]:.4f}")
    for i, R in enumerate(EXT):
        v = lndiff(R, lev1(R), lev2(R))
        if v is None: continue
        l = line[3][i]; ce = math.hypot(l[1], v[1]); q = rim[3][i]; cq = math.hypot(q[1], v[1])
        print(f"     R {R} (A {Aof(R)}): measured {v[0]:.4f} +- {v[1]:.4f};  line from 9..15: {l[0]:.4f} +- {l[1]:.4f}, measured - line = {v[0] - l[0]:+.4f} ({(v[0] - l[0]) / ce:+.1f} errors);  line+rim: {q[0]:.4f} +- {q[1]:.4f}, measured - fit = {v[0] - q[0]:+.4f} ({(v[0] - q[0]) / cq:+.1f} errors)")
for p in (0.5, 0.4, 0.3):
    partE(f"0.6 against {p}", lambda R: 0.6 * info[R]["pbar"], lambda R, p=p: p * info[R]["pbar"])
partE("0.5 against 0.4", lambda R: 0.5 * info[R]["pbar"], lambda R: 0.4 * info[R]["pbar"])
partE("0.8 against 0.6 (control: a rim term is known here)", lambda R: 0.8 * info[R]["pbar"], lambda R: 0.6 * info[R]["pbar"])
partE("x 0.30 against x 0.24", lambda R: 0.30 * Aof(R), lambda R: 0.24 * Aof(R))
print("\nPART F: the anchors alone (no dip rates): ln tau = a + cA + rk fitted to 45, 63, 84, 108 cells, i.e. the lifetime's own quadratic in k")
ys = [ANCH[R][0] for R in (9, 11, 13, 15)]; es = [ANCH[R][1] for R in (9, 11, 13, 15)]
q = fit([9, 11, 13, 15], ys, es, [lambda R: 1.0, lambda R: float(Aof(R)), lambda R: float(kof(R))], [17, 19, 21])
print(f"   c = {q[0][1]:.4f} +- {q[1][1]:.4f}, r = {q[0][2]:+.3f} +- {q[1][2]:.3f}, chi2 {q[2]:.2f} on 1;  R 17: {q[3][0][0]:.3f} +- {q[3][0][1]:.3f};  R 19: {q[3][1][0]:.3f} +- {q[3][1][1]:.3f};  R 21: {q[3][2][0]:.3f} +- {q[3][2][1]:.3f}")

print("\nPART G: how good is a one-step extrapolation? ln nu(p P-bar) itself, fitted on R = 9..15 (a + cA + rk, the quadratic in k), against its measured value at R = 17, 19, 21")
for p in PS:
    pts = [(R, lnnu(R, p * info[R]["pbar"])) for R in FIT]
    if any(v is None for _, v in pts): continue
    ys = [v[0] for _, v in pts]; es = [max(v[1], 2e-4) for _, v in pts]
    rim = fit(FIT, ys, es, [lambda R: 1.0, lambda R: float(Aof(R)), lambda R: float(kof(R))], EXT)
    out = []
    for i, R in enumerate(EXT):
        v = lnnu(R, p * info[R]["pbar"])
        if v is None: continue
        q = rim[3][i]; out.append(f"R {R}: measured - quadratic = {v[0] - q[0]:+.4f} +- {math.hypot(q[1], v[1]):.4f}")
    print(f" p = {p}: chi2 {rim[2]:.1f} on 1; " + ";  ".join(out))

print("\nPART H: is the change of curvature an artefact of interpolating ln nu linearly between integer levels? The same second differences")
print("        with a three-point (quadratic) interpolation in the level, at p = 0.6, 0.5 and at fixed density 0.30, 0.28")
def lnnu3(R, L):
    I = info[R]; m = int(round(L))
    if m - 1 < 0 or m + 1 >= len(I["nu"]) or I["cnt"][m - 1] < 20: return None
    y = [math.log(I["nu"][m + d]) for d in (-1, 0, 1)]; t = L - m
    v = y[1] + t * (y[2] - y[0]) / 2 + t * t * (y[2] - 2 * y[1] + y[0]) / 2
    return v, max(I["err"][m - 1], I["err"][m], I["err"][m + 1])
for name, lev in (("p = 0.6", lambda R: 0.6 * info[R]["pbar"]), ("p = 0.5", lambda R: 0.5 * info[R]["pbar"]),
                  ("x = 0.30", lambda R: 0.30 * Aof(R)), ("x = 0.28", lambda R: 0.28 * Aof(R))):
    for label, fn in (("linear", lambda R, L: lnnu(R, L)), ("3-point", lnnu3)):
        v = [(R, fn(R, lev(R))) for R in Rs]; v = [(R, x) for R, x in v if x is not None]
        print(f" {name} {label}: values " + " ".join(f"{x[0]:.4f}" for _, x in v))
        print("      second differences (centred on R = 11 ...): " + "  ".join(
            f"{v[i + 2][1][0] - 2 * v[i + 1][1][0] + v[i][1][0]:+.4f}+-{math.sqrt(v[i + 2][1][1] ** 2 + 4 * v[i + 1][1][1] ** 2 + v[i][1][1] ** 2):.4f}" for i in range(len(v) - 2)))
