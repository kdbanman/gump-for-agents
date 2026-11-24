#!/usr/bin/env python3
"""ref-density: the table of my rows (rd.c) against the density agent's, and the R = 9 rows against nzd.c run by me.

  python3 research/blast/ref-density/collect.py [ROWDIR]     (default: research/blast/ref-density/data/rows)

ln tau = ln(exposure / watched deaths) +- 1/sqrt(deaths). Differences in sigma use the two rows' errors in quadrature.
"""
import glob, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "rows")

# theirs (research/blast/density/README.md at 9a105d3): ln tau of the row, its error; gump anchor 13.633 +- 0.001
THEIRS = {
    "gump_R11": (13.633, 0.001, "gump (anchor; their own seed 13.644 +- 0.012)"),
    "fair_d1": (14.311, 0.016, "fair coins d=1"),
    "mean_d1": (14.165, 0.011, "mean-density coins d=1"),
    "shufcore_d1": (13.199, 0.013, "copy from the replaced cells d=1"),
    "shufwhole_d1": (13.464, 0.011, "copy from the whole layer d=1"),
    "scan_p0.1": (13.312, 0.022, "every depth at p=0.1"),
    "scan_p0.2": (13.676, 0.024, "every depth at p=0.2"),
    "low10_d1": (14.096, 0.010, "coins at the low-face density d=1"),
    "fair_d2": (13.965, 0.014, "fair coins d=2"),
    "mean_d2": (13.877, 0.013, "mean-density coins d=2"),
    "e16_mean_d1": (13.797, 0.013, "mean-density coins, eps=1/16"),
}
GUMP = 13.633


def mine(path):
    t = open(path).read()
    if "\nBEGIN " in t:                       # periodic full reports: use the last complete one
        last = t.rfind("\nBEGIN ")
        if "\nEND " not in t[last:]:
            prev = t.rfind("\nBEGIN ", 0, last)
            last = prev if prev >= 0 else last
        t = t[last:]
    m = re.search(r"^RESULT .* expo (\S+) deaths (\S+) lntau (\S+) err (\S+) deaths_any8 (\S+) maxage (\S+)", t, re.M)
    if not m:
        m2 = re.findall(r"^CKPT (\d+) expo (\S+) deaths (\S+) lntau (\S+) err (\S+) any (\S+)", t, re.M)
        if not m2:
            return None
        g, e, d, lt, er, an = m2[-1]
        r = dict(E=float(e), D=float(d), part=int(g))
        r["Dany"] = float(an)
    else:
        r = dict(E=float(m.group(1)), D=float(m.group(2)), Dany=float(m.group(5)), maxage=int(m.group(6)), part=0)
    r["lt"] = math.log(r["E"] / r["D"]); r["er"] = 1 / math.sqrt(r["D"])
    r["lt8"] = math.log(8 * r["E"] / r["Dany"]); r["er8"] = 1 / math.sqrt(r["Dany"])
    desc = {int(k): (float(a), float(b)) for k, a, b in re.findall(r"^DESC (\d+) desc (\S+) died (\S+)", t, re.M)}
    r["desc"] = desc
    r["dens"] = {f"{k}{n}": float(v) for k, n, v in re.findall(r"^DENS (core|full) (\d+) n \d+ (\S+)", t, re.M)}
    mpost = re.search(r"^DENS core1 after darts.* (\S+)$", t, re.M)
    if mpost:
        r["post"] = float(mpost.group(1))
    byf = {int(f): (float(n), float(c1), float(l1)) for f, n, c1, l1 in re.findall(r"^BYF (\d+) n (\S+) core1 (\S+) full1 (\S+)", t, re.M)}
    r["byf"] = byf
    r["byfpost"] = {int(f): (float(n), float(c)) for f, n, c in re.findall(r"^BYFPOST (\d+) n (\S+) core1 (\S+)", t, re.M)}
    fm = re.search(r"^FACE mean (\S+) sd (\S+)", t, re.M)
    if fm:
        r["face"] = (float(fm.group(1)), float(fm.group(2)))
    r["lag"] = {name: [float(x) for x in vals.split()] for name, vals in re.findall(r"^LAG (\S+) (.*)$", t, re.M)}
    return r


def nzd(path):
    t = open(path).read()
    m = re.search(r"exposure (\S+) deaths_any (\d+) watched (\d+)", t)
    if not m:
        return None
    E, Dany, D = float(m.group(1)), float(m.group(2)), float(m.group(3))
    rec = {int(k): (float(a), float(b)) for k, a, b, c in re.findall(r" (\d+):(\d+)/(\d+)/(\d+)", t.split("REC")[1].split("\n")[0])}
    return dict(E=E, D=D, Dany=Dany, lt=math.log(E / D), er=1 / math.sqrt(D), lt8=math.log(8 * E / Dany), er8=1 / math.sqrt(Dany), desc=rec)


def low_density(r, thr=10, key=1):
    n = sum(v[0] for f, v in r["byf"].items() if f <= thr)
    s = sum(v[0] * v[key] for f, v in r["byf"].items() if f <= thr)
    return s / n if n else float("nan"), n


def main():
    rows = {}
    for p in sorted(glob.glob(os.path.join(D, "*.txt")) + glob.glob(os.path.join(D, "*.txt.part"))):
        tag = os.path.basename(p).replace(".txt.part", "").replace(".txt", "")
        if p.endswith(".part") and os.path.exists(p[:-5]):
            continue
        r = mine(p)
        if r and p.endswith(".part"):
            r["inprog"] = True
        if r:
            rows[tag] = r
    g = rows.get("gump_R11_s1001")
    print(f"{'row':28s} {'theirs ln tau':>16s} {'mine ln tau':>18s} {'diff/sigma':>10s} {'mine - my gump':>16s} {'mine - 13.633':>14s} {'deaths':>7s}")
    for tag, r in rows.items():
        if tag.startswith("r9_"):
            continue
        key = re.sub(r"_s\d+$", "", tag)
        th = THEIRS.get(key)
        part = f" (partial, gen {r['part']})" if r["part"] else (" (in progress)" if r.get("inprog") else "")
        dg = f"{r['lt'] - g['lt']:+.3f} +- {math.hypot(r['er'], g['er']):.3f}" if g and tag != "gump_R11_s1001" else ""
        if th:
            z = (r["lt"] - th[0]) / math.hypot(r["er"], th[1])
            print(f"{tag:28s} {th[0]:9.3f} +- {th[1]:.3f} {r['lt']:10.4f} +- {r['er']:.4f} {z:+10.2f} {dg:>16s} {r['lt'] - GUMP:+14.3f} {r['D']:7.0f}{part}")
        else:
            print(f"{tag:28s} {'':16s} {r['lt']:10.4f} +- {r['er']:.4f} {'':10s} {dg:>16s} {r['lt'] - GUMP:+14.3f} {r['D']:7.0f}{part}")
    if g:
        print(f"\ngump R=11, all eight faces: 8E/D = {g['lt8']:.4f} +- {g['er8']:.4f} ({g['Dany']:.0f} deaths); anchor 13.633 +- 0.001")
    print("\nR = 9: my chain against nzd.c (commit 9a105d3) run by me, same settings, own seeds")
    for name in ("gump", "fair_d1", "shufcore_d1", "p0.2_d1"):
        a = [r for t, r in rows.items() if t.startswith(f"r9_{name}_")]
        bs = [nzd(p) for p in glob.glob(os.path.join(D, "..", "nzd", f"r9_{name}_*.txt"))]
        bs = [b for b in bs if b]
        if a and bs:
            a, b = a[0], bs[0]
            z = (a["lt"] - b["lt"]) / math.hypot(a["er"], b["er"])
            p1a = a["desc"][0][1] / a["desc"][1][0] if a["desc"].get(1, (0,))[0] else float("nan")
            p1b = b["desc"][0][1] / b["desc"][1][0] if b["desc"].get(1, (0,))[0] else float("nan")
            print(f"  {name:12s} mine {a['lt']:.4f} +- {a['er']:.4f} ({a['D']:.0f})  nzd {b['lt']:.4f} +- {b['er']:.4f} ({b['D']:.0f})  diff {z:+.2f} sigma;"
                  f"  8 faces: mine {a['lt8']:.4f} nzd {b['lt8']:.4f};  P1 mine {p1a:.3f} nzd {p1b:.3f}")
    print("\nDescents of the watched face from >= 16 (P_k = died/desc); layer-1 core density all-time, at F <= 10, after darts")
    for tag, r in rows.items():
        dsc = r["desc"]
        if not dsc or not dsc.get(1, (0,))[0]:
            continue
        P = {k: dsc[k][1] / dsc[k][0] for k in (1, 2, 4, 8, 15) if dsc[k][0]}
        eP1 = math.sqrt(P[1] * (1 - P[1]) / dsc[1][0])
        lo, n = low_density(r, 10, 1)
        lo4, n4 = low_density(r, 4, 1)
        lf, _ = low_density(r, 10, 2)
        post_lo = ""
        if r.get("byfpost"):
            nn = sum(v[0] for f, v in r["byfpost"].items() if f <= 10)
            ss = sum(v[0] * v[1] for f, v in r["byfpost"].items() if f <= 10)
            post_lo = f" after darts {r.get('post', float('nan')):.4f} (F<=10: {ss / nn:.4f})" if nn else ""
        print(f"  {tag:26s} P1 {P[1]:.3f} +- {eP1:.3f}  P2 {P.get(2, 0):.3f} P4 {P.get(4, 0):.3f} P8 {P.get(8, 0):.4f} P15 {P.get(15, 0):.5f} | "
              f"core1 {r['dens'].get('core1', 0):.4f} F<=10 {lo:.4f} (F<=4 {lo4:.4f}; n {n:.0f}) full1 {r['dens'].get('full1', 0):.4f} F<=10 {lf:.4f}{post_lo}")
    if g:
        print("\nExcursion split against my gump (ln tau = -ln f_k - ln P_k): d ln f_k for k = 15, 4, 1 and d ln P_1, d ln P_4")
        for tag, r in rows.items():
            if tag.startswith("r9_") or tag == "gump_R11_s1001" or not r["desc"].get(1, (0,))[0]:
                continue
            f = lambda rr, k: rr["desc"][k][0] / rr["E"]
            P = lambda rr, k: rr["desc"][k][1] / rr["desc"][k][0]
            eP1 = math.sqrt((1 - P(r, 1)) / r["desc"][1][1] + (1 - P(g, 1)) / g["desc"][1][1])
            print(f"  {tag:26s} dln f15 {math.log(f(r, 15) / f(g, 15)):+.3f}  dln f4 {math.log(f(r, 4) / f(g, 4)):+.3f}  dln f1 {math.log(f(r, 1) / f(g, 1)):+.3f}"
                  f"  dln P1 {math.log(P(r, 1) / P(g, 1)):+.3f} +- {eP1:.3f}  dln P4 {math.log(P(r, 4) / P(g, 4)):+.3f}"
                  + (f"  face mean {r['face'][0]:.2f} sd {r['face'][1]:.2f}" if 'face' in r else ""))
        print("\nDensities (all time, after the step, before darts) against my gump: core 1..3, full 1..2")
        for tag, r in rows.items():
            if tag.startswith("r9_"):
                continue
            print(f"  {tag:26s} " + " ".join(f"{k} {r['dens'].get(k, float('nan')):.4f}" for k in ("core1", "core2", "core3", "core4", "full1", "full2"))
                  + f"  core1 after darts {r.get('post', float('nan')):.4f}" + (f"  face {r['face'][0]:.2f}" if 'face' in r else ""))
    for tag, r in rows.items():
        if r["lag"]:
            print(f"\nLAG (Pearson, L = 0..8) {tag}")
            for name, v in r["lag"].items():
                print(f"  {name:14s} " + " ".join(f"{x:+.3f}" for x in v))


if __name__ == "__main__":
    main()
