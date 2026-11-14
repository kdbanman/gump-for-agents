"""summary.py -- tables of REVIEW-class.md from the run outputs in research/scratch/audit-class/.

    python3 summary.py          (after run_face12e.sh, run_measured.sh gump|fcc, run_extra.sh)
"""
import json, os
import numpy as np

O = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scratch", "audit-class")


def load(fn):
    out = []
    p = os.path.join(O, fn)
    if not os.path.exists(p):
        return out
    for l in open(p):
        l = l.strip()
        if l.startswith("{"):
            out.append(json.loads(l))
    return out


def wfit(A, y, e):
    A, y, w = np.array(A, float), np.array(y, float), 1 / np.array(e, float) ** 2
    Am, ym = (w * A).sum() / w.sum(), (w * y).sum() / w.sum()
    s = (w * (A - Am) * (y - ym)).sum() / (w * (A - Am) ** 2).sum()
    return s, 1 / np.sqrt((w * (A - Am) ** 2).sum())


def hazard_line(r, mind=30):
    hz = [(k, d, t) for k, d, t in r["hazard"] if d >= mind]
    if not hz:
        return "-"
    ts = [t for _, _, t in hz]
    return f"tau by age bin 2^{hz[0][0]}..2^{hz[-1][0]} (bins with >= {mind} deaths): {min(ts):.0f}..{max(ts):.0f}"


def law(rows, title, theirs=None):
    print(title)
    rows = [r for r in rows if r["lntau"] is not None]
    for r in rows:
        t = "" if theirs is None or r["A"] not in theirs else f"   class.md: {theirs[r['A']]}"
        print(f"   A={r['A']:3d} N={r['N']:4d} deaths={r['deaths']:7d} early={r['early']:8d} settled={r['settle']:5d} "
              f"ln tau = {r['lntau']:.3f} +- {r['err']:.3f}  CV {r['cv']:.3f}  density interior/boundary/next "
              f"{r['dens'][0]:.3f}/{r['dens'][1]:.3f}/{r['dens'][2]:.3f}{t}")
        print(f"         {hazard_line(r)}")
    if len(rows) >= 2:
        s, se = wfit([r["A"] for r in rows], [r["lntau"] for r in rows], [max(r["err"], 0.01) for r in rows])
        print(f"   weighted slope over all sizes: {s:.4f} +- {se:.4f} per cell of A;  successive: "
              + ", ".join(f"{(b['lntau'] - a['lntau']) / (b['A'] - a['A']):.3f}" for a, b in zip(rows, rows[1:])))
        if len(rows) >= 3:
            s2, se2 = wfit([r["A"] for r in rows[1:]], [r["lntau"] for r in rows[1:]], [max(r["err"], 0.01) for r in rows[1:]])
            print(f"   without the smallest size: {s2:.4f} +- {se2:.4f}")


S = load("face12e_slab.jsonl")
law([r for r in S if r["watch"] == "two" and r["depth"] == 4], "== face12e B45/S345, wall + layer beneath both empty (permanent), slab 4 cubes deep; A = wall faces")
law([r for r in S if r["watch"] == "two" and r["depth"] == 6], "== same, slab 6 cubes deep")
law([r for r in S if r["watch"] == "one"], "== face12e: wall sheet alone empty (not permanent)")
law([r for r in S if r["watch"] == "second"], "== face12e: layer beneath the wall alone empty")
print("== face12e boxes of n^3 cubes (64 soups, density 0.45)")
for r in load("face12e_life.jsonl"):
    print(f"   n={r['n']} cells={r['N']:4d} finished {r['finished']}/64 median {r['median']} (q25 {r['q25']}, q75 {r['q75']}) "
          f"final density {r['mean_final_density']} empty endings {r['empty_endings']} long cycles {r['long_cycles']}")
G = load("measured_gump.jsonl")
T6 = {27: "5.48+-0.02", 36: "7.39", 48: "9.92", 60: "12.50+-0.04", 75: "15.53+-0.20"}
T7 = {27: "5.42", 36: "7.33", 48: "9.88", 60: "12.59+-0.04", 75: "15.92+-0.23"}
law([r for r in G if r["rule"] == "B[4, 5]/S[3, 4, 5]"], "== gump B45/S345, {111} slab 8 layers (class.md: slope 0.212)", T6)
law([r for r in G if r["rule"] == "B[4, 5, 6]/S[3, 4, 5, 6]"], "== gump lattice B456/S3456 (class.md: slope 0.215)", T7)
F = load("measured_fcc.jsonl")
TF = {25: "4.61", 36: "6.85", 49: "9.25", 64: "11.97+-0.04", 81: "14.68+-0.24"}
law([r for r in F if r["rule"] == "B[4, 5]/S[3, 4, 5]"], "== fcc B45/S345, {111} slab 8 layers (class.md: slope 0.19)", TF)
for r in F:
    if r["rule"] != "B[4, 5]/S[3, 4, 5]":
        print(f"   fcc {r['rule']} A={r['A']}: deaths {r['deaths']}, early {r['early']}, settled {r['settle']}+{r['early_settle']}, "
              f"ln tau {r['lntau']}, boundary density {r['dens'][1]}, interior {r['dens'][0]}")
V = load("vnbox.jsonl")
if V:
    print("== von Neumann B2/S12 boxes")
    for r in V:
        print(f"   side {r['side']:3d}: median {r['median']:.0f} (q25 {r['q25']:.0f}, q75 {r['q75']:.0f}), finished {r['finished']}/64, "
              f"by snapshot {r['by_snapshot']}, final density {r['final_density']}, "
              f"d ln T / d side {r.get('rate_per_side', '-')}, d ln T / d ln side {r.get('local_power', '-')}")
