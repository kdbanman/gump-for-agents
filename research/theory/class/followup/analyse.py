"""analyse.py -- tables of OUTCOMES.md from the run outputs in research/scratch/class_followup/.

    python3 analyse.py slab FILE [nwalls] [key]     waiting-time table + weighted fit of ln tau against wall size
    python3 analyse.py life FILE                    lifetime table
key: the size field ('wall_cells' for strips, 'A' for 3D slabs and columns).
Hazard: consecutive log2 age bins merged until each holds >= max(20, deaths/5) deaths; tau per wall in each,
+- tau/sqrt(deaths).
"""
import json, sys
import numpy as np


def hazard_groups(be, bw, nwalls, mind=20):
    be = np.array(be, float); bw = np.array(bw, float)
    tot = bw.sum()
    need = max(mind, tot / 5)
    out, e, d, k0 = [], 0.0, 0.0, 0
    for k in range(len(be)):
        e += be[k]; d += bw[k]
        if d >= need:
            out.append((2 ** k0, 2 ** (k + 1), int(d), nwalls * e / d)); e = d = 0.0; k0 = k + 1
    if d > 0 and out:          # leftover old ages: fold into the last group
        a, b_, dd, tau = out.pop()
        ee = tau * dd / nwalls + e
        out.append((a, 2 ** len(be), int(dd + d), nwalls * ee / (dd + d)))
    elif d > 0:
        out.append((2 ** k0, 2 ** len(be), int(d), nwalls * e / d))
    return out


def fit(xs, ys, es):
    w = 1 / np.array(es) ** 2
    X = np.vstack([np.ones(len(xs)), xs]).T
    cov = np.linalg.inv(X.T @ (X * w[:, None]))
    beta = cov @ X.T @ (w * np.array(ys))
    chi2 = float((w * (np.array(ys) - X @ beta) ** 2).sum())
    return beta, np.sqrt(np.diag(cov)), chi2


def slab(path, nwalls=2, key="wall_cells", deathkey="walls"):
    rows = [json.loads(l) for l in open(path) if l.strip().startswith("{")]
    pts = []
    print(f"{'size':>5} {'deaths':>7} {'ln tau':>8} {'+-':>6} {'CV':>6} cuts pits deep periodic | early(w,c,p,per,deep) | "
          f"oldest-alive  max-age | hazard (age bins after burn-in: deaths, tau)")
    for r in rows:
        d = r[deathkey]
        lt = r.get("lntau", r.get("lntau_per_wall"))
        hz = hazard_groups(r["binexp"], r["binwall"], nwalls) if "binexp" in r else r.get("hazard")
        hs = "  ".join(f"[{a},{b}): {dd}, {t:.3g}" for a, b, dd, t in hz) if "binexp" in r else str(hz)
        print(f"{r[key]:>5} {d:>7} {lt if lt is not None else float('nan'):8.3f} {r['err'] if r['err'] else float('nan'):6.3f} "
              f"{r['cv'] if r['cv'] else float('nan'):6.3f} {r['cuts']:>5} {r['pits']:>4} {r.get('deep', 0):>5} "
              f"{r['periodic']:>5} | {r['early']} | {r['max_age_end']:>9} {r['max_age']:>9} | {hs}")
        if d >= 20 and lt is not None:
            pts.append((r[key], lt, r["err"]))
    if len(pts) >= 2:
        xs, ys, es = zip(*pts)
        beta, se, chi2 = fit(np.array(xs, float), ys, es)
        print(f"weighted fit over {len(pts)} sizes {list(xs)}: ln tau = {beta[0]:.3f} + {beta[1]:.4f} x size "
              f"(+- {se[1]:.4f}), chi2 = {chi2:.1f} on {len(pts) - 2} dof")
        loc = [(xs[i + 1] + xs[i]) / 2 for i in range(len(xs) - 1)]
        sl = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
        sle = [np.hypot(es[i + 1], es[i]) / (xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
        print("local slopes: " + ", ".join(f"{a:g}: {s:.3f} +- {e:.3f}" for a, s, e in zip(loc, sl, sle)))


def life(path):
    for l in open(path):
        if not l.strip().startswith("{"):
            continue
        r = json.loads(l)
        r.pop("lifetimes_finished", None)
        print(r)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "slab":
        slab(a[1], int(a[2]) if len(a) > 2 else 2, a[3] if len(a) > 3 else "wall_cells")
    else:
        life(a[1])
