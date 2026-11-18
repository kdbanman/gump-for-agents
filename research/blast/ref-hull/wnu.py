#!/usr/bin/env python3
"""wnu.py DIR -- dip rates on slab tori (rows of `sl nu`, files DIR/w_H_K_D.txt) against the anchors' lifetimes.
Same definitions as for the hull (nu.py): first passages of P <= p P-bar per face-generation from above ceil(P-bar)."""
import sys, math, glob, os
import numpy as np
D = sys.argv[1]
ANCH = {  # (H,K,D): (ln tau_face, error, kind)
 (4, 0, 4): (9.9251, 0.0004, "wide"), (1, 7, 19): (11.8751, 0.0004, "wide"), (1, 4, 21): (13.1622, 0.0007, "wide"),
 (1, 9, 25): (15.6442, 0.0030, "wide"), (1, 4, 28): (17.5387, 0.0031, "wide"), (6, 0, 6): (22.5405, 0.0074, "wide"),
 (1, 12, 28): (17.3175, 0.0031, "tube"), (1, 17, 32): (19.7446, 0.0059, "tube"), (1, 16, 36): (22.1599, 0.0121, "tube")}
HULLQ = {0.8: 0.20332, 0.7: 0.18953, 0.6: 0.17016, 0.5: 0.14626, 0.4: 0.11925}   # hull slopes of -ln q(p) (nu.py PART B)
HULLNU = {0.6: {45: -4.2102, 63: -4.9660, 84: -5.8975, 108: -7.0097, 135: -8.2976}, 0.5: {45: -5.0610, 63: -6.2405, 84: -7.6784, 108: -9.3672},
          0.4: {45: -5.9916, 63: -7.6604, 84: -9.6638, 108: -11.9972}}
PS = [0.8, 0.7, 0.6, 0.5, 0.4]
info = {}
for fn in glob.glob(os.path.join(D, "w_*.txt")):
    rs = []
    for line in open(fn):
        t = line.split()
        if not t or t[0] != "NU": continue
        d = {t[i]: t[i + 1] for i in range(1, t.index("cross"), 2)}
        ic, ib = t.index("cross"), t.index("bust")
        d["cross"] = np.array(list(map(float, t[ic + 1:ib]))); d["bust"] = np.array(list(map(float, t[ib + 1:])))
        rs.append(d)
    if not rs: continue
    key = tuple(map(int, rs[0]["T"].split(","))); K = len(rs)
    expo = np.array([float(r["expo"]) for r in rs]); cr = np.array([r["cross"] for r in rs]); bu = np.array([r["bust"] for r in rs])
    nP = sum(float(r["nP"]) for r in rs); pbar = sum(float(r["sumP"]) for r in rs) / nP
    nu = cr.sum(0) / (2 * expo.sum()); per = cr / (2 * expo[:, None])
    rel = per.std(0, ddof=1) / math.sqrt(K) / np.where(nu > 0, nu, 1) if K > 1 else np.ones_like(nu)
    poi = 1 / np.sqrt(np.maximum(cr.sum(0), 1))
    info[key] = dict(K=K, expo=expo.sum(), pbar=pbar, sig=math.sqrt(sum(float(r["sumP2"]) for r in rs) / nP - pbar ** 2), nu=nu, err=np.maximum(rel, poi),
                     cnt=cr.sum(0), bust=bu.sum(0), A=int(rs[0]["A"]), lamA=int(rs[0]["lamA"]), deaths=sum(int(r["deaths"]) for r in rs),
                     fdead=sum(int(r["fdead"]) for r in rs), over=sum(float(r["nover"]) for r in rs) / nP)
def lnnu(key, L, which="cnt"):
    I = info[key]; lo = int(math.floor(L)); f = L - lo
    if lo < 0 or lo + 1 >= len(I["nu"]) or I[which][lo] < 20: return None
    sc = lambda j: I[which][j] / (2 * I["expo"])
    v = (1 - f) * math.log(sc(lo)) + f * math.log(sc(lo + 1))
    e = (1 - f) * I["err"][lo] + f * I["err"][lo + 1] if which == "cnt" else 1 / math.sqrt(I[which][lo])
    return v, e
keys = sorted(info, key=lambda k: (ANCH[k][2], info[k]["A"], k))
print("PART 1: tori, P-bar, direct lifetime where deaths occurred, dip rates ln nu(p P-bar) per face-generation")
for k in keys:
    I = info[k]; a = ANCH[k]
    dl = f"direct ln(2E/D) = {math.log(2 * I['expo'] / I['deaths']):.4f} +- {1 / math.sqrt(I['deaths']):.4f} ({I['deaths']} first deaths; faces empty per death {I['fdead'] / I['deaths']:.4f})" if I["deaths"] > 30 else f"{I['deaths']} first deaths"
    print(f" {a[2]} ({k[0]},{k[1]}),(0,{k[2]}) A {I['A']}: K {I['K']} exposure {2 * I['expo']:.3g} face-gens; P-bar {I['pbar']:.4f} = {I['pbar'] / I['A']:.5f} A, sigma {I['sig']:.3f}, lamA {I['lamA']}; anchor {a[0]}; {dl}; share of face-gens with P >= 0.7A: {I['over']:.2e}")
    print("     " + "  ".join(f"p {p}: {lnnu(k, p * I['pbar'])[0]:.4f}+-{lnnu(k, p * I['pbar'])[1]:.4f}" for p in PS if lnnu(k, p * I["pbar"])))
def fit(xs, ys, es, cols):
    X = np.array([[c(x) for c in cols] for x in xs]); W = np.diag(1 / np.array(es) ** 2)
    cov = np.linalg.inv(X.T @ W @ X); b = cov @ X.T @ W @ np.array(ys)
    return b, np.sqrt(np.diag(cov)), float(((np.array(ys) - X @ b) ** 2 / np.array(es) ** 2).sum())
wide = [k for k in keys if ANCH[k][2] == "wide"]; tubes = [k for k in keys if ANCH[k][2] == "tube"]
print("\nPART 2: wide faces. -ln q(p) = ln tau + ln nu(p P-bar) and -ln nu(p P-bar): straight lines in the area?")
for p in PS:
    pts = [(k, lnnu(k, p * info[k]["pbar"])) for k in wide]
    if any(v is None for _, v in pts) or len(pts) < 3: continue
    As = [info[k]["A"] for k, _ in pts]
    q = [ANCH[k][0] + v[0] for k, v in pts]; qe = [math.hypot(ANCH[k][1], v[1]) for k, v in pts]
    nn = [-v[0] for _, v in pts]; ne = [max(v[1], 3e-4) for _, v in pts]
    fq = fit(As, q, qe, [lambda A: 1.0, lambda A: float(A)]); fn = fit(As, nn, ne, [lambda A: 1.0, lambda A: float(A)])
    ft = fit(As, [ANCH[k][0] for k, _ in pts], [ANCH[k][1] for k, _ in pts], [lambda A: 1.0, lambda A: float(A)])
    print(f" p = {p}: A = {As}")
    print(f"     -ln q  = " + " ".join(f"{y:.3f}" for y in q) + f";  line {fq[0][0]:+.3f} + {fq[0][1]:.5f} A (+- {fq[1][1]:.5f}), chi2 {fq[2]:.1f} on {len(As) - 2}; residuals " + " ".join(f"{y - fq[0][0] - fq[0][1] * A:+.3f}" for y, A in zip(q, As)) + f";  hull slope {HULLQ[p]:.5f}")
    print(f"     -ln nu = " + " ".join(f"{y:.3f}" for y in nn) + f";  line {fn[0][0]:+.3f} + {fn[0][1]:.5f} A (+- {fn[1][1]:.5f}), chi2 {fn[2]:.1f} on {len(As) - 2}; residuals " + " ".join(f"{y - fn[0][0] - fn[0][1] * A:+.3f}" for y, A in zip(nn, As)))
    if p == 0.6: print(f"     (ln tau itself on these tori: slope {ft[0][1]:.5f} +- {ft[1][1]:.5f}, chi2 {ft[2]:.1f})")
    if p in HULLNU:
        print("     same area, hull against wide torus, -ln nu and -ln q: " + ";  ".join(
            f"A {info[k]['A']}: torus nu {-v[0]:.3f} hull nu {-HULLNU[p][info[k]['A']]:.3f} (hull dips {'rarer' if -HULLNU[p][info[k]['A']] > -v[0] else 'more often'} by {abs(-HULLNU[p][info[k]['A']] + v[0]):.3f}); torus q {ANCH[k][0] + v[0]:.3f} hull q {dict(zip((45, 63, 84, 108), (9.819, 13.633, 18.141, 23.3392)))[info[k]['A']] + HULLNU[p][info[k]['A']]:.3f}"
            for k, v in pts if info[k]["A"] in HULLNU[p] and info[k]["A"] in (63, 84, 108)))
print("\nPART 3: tube against wide face of the same area: where does the tube's discount in ln tau sit?")
for A in (84, 108):
    w = [k for k in wide if info[k]["A"] == A]; t = [k for k in tubes if info[k]["A"] == A]
    if not w or not t: continue
    w, t = w[0], t[0]
    print(f" A = {A}: wide {w} ln tau {ANCH[w][0]}, tube {t} ln tau {ANCH[t][0]}: discount {ANCH[w][0] - ANCH[t][0]:.4f} +- {math.hypot(ANCH[w][1], ANCH[t][1]):.4f}; P-bar wide {info[w]['pbar']:.4f} tube {info[t]['pbar']:.4f}")
    for p in PS:
        a, b = lnnu(w, p * info[w]["pbar"]), lnnu(t, p * info[t]["pbar"])
        if a is None or b is None: continue
        dnu = (-a[0]) - (-b[0]); dq = (ANCH[w][0] + a[0]) - (ANCH[t][0] + b[0])
        print(f"     p = {p}: discount in -ln nu = {dnu:+.4f} +- {math.hypot(a[1], b[1]):.4f};  in -ln q = {dq:+.4f} +- {math.sqrt(a[1] ** 2 + b[1] ** 2 + ANCH[w][1] ** 2 + ANCH[t][1] ** 2):.4f}")
        # same absolute level (the wide face's p P-bar) on the tube
        b2 = lnnu(t, p * info[w]["pbar"])
        if b2: print(f"            at the same absolute level L = {p * info[w]['pbar']:.2f}: in -ln nu = {(-a[0]) - (-b2[0]):+.4f}, in -ln q = {(ANCH[w][0] + a[0]) - (ANCH[t][0] + b2[0]):+.4f}")
print("\nPART 4: dips preceded within 3 generations by an over-full face (P >= 0.7 A): share of first passages at each level")
for k in keys:
    I = info[k]
    s = []
    for p in (0.8, 0.6, 0.4, 0.2):
        L = int(math.floor(p * I["pbar"]))
        if I["cnt"][L] >= 20: s.append(f"p {p}: {I['bust'][L] / I['cnt'][L]:.2e} ({int(I['bust'][L])}/{int(I['cnt'][L])})")
    if I["cnt"][0] >= 5: s.append(f"deaths (P = 0): {I['bust'][0] / I['cnt'][0]:.3f} ({int(I['bust'][0])}/{int(I['cnt'][0])})")
    print(f" {ANCH[k][2]} {k} A {I['A']}: " + ";  ".join(s))
