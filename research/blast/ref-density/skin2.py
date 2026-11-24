#!/usr/bin/env python3
"""ref-density, second review: the skin rows at full replacement (my rd.c, RD_FULL=1) against my gump and theirs.

  python3 research/blast/ref-density/skin2.py [ROWDIR]     (default research/blast/ref-density/data/rows)

ln tau = ln(E / watched deaths) +- 1/sqrt(deaths). Delta against my own gump of the same size (same estimator, same code)
and against theirs (9.8177 +- 0.0036 at 45 cells, 13.633 +- 0.001 at 63, as their skin.py uses). Dips = descents from
>= H to <= H-1 per lane-generation (H = round(A/4): 11 at 45 cells, 16 at 63), deadliness = share of them that die
before the face is back at H, P1 = share of descents to <= 1 cell that die (my DESC lines, the agent's REC).
"""
import glob, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "rows")
THEIRS = {("9", "3"): (0.169, 0.008), ("9", "4"): (0.004, 0.007), ("11", "3"): (0.295, 0.023), ("11", "4"): (0.016, 0.012)}
GREF = {"9": (9.8177, 0.0036), "11": (13.633, 0.001)}


def load(path):
    t = open(path).read()
    if "\nBEGIN " in t:
        t = t[t.rfind("\nBEGIN "):]
    m = re.findall(r"^RESULT R (\d+) M \S+ B \S+ D0 (\d+) coin (\S+) seed \S+ gens \S+ expo (\S+) deaths (\S+)", t, re.M)
    if not m:
        return None
    R, D0, coin, E, Dd = m[-1]
    desc = {int(k): (float(a), float(b)) for k, a, b in re.findall(r"^DESC (\d+) desc (\S+) died (\S+)", t, re.M)}
    H = 11 if R == "9" else 16
    return dict(R=R, D0=D0, coin=coin, E=float(E), D=float(Dd), desc=desc, H=H)


def stats(rs):
    E = sum(r["E"] for r in rs); Dd = sum(r["D"] for r in rs); H = rs[0]["H"]
    dn = sum(r["desc"][H - 1][0] for r in rs); dd = sum(r["desc"][H - 1][1] for r in rs)
    n1 = sum(r["desc"][1][0] for r in rs); k1 = sum(r["desc"][1][1] for r in rs)
    return dict(lt=math.log(E / Dd), er=Dd ** -0.5, D=Dd, dips=dn / E, dead=dd / dn, edead=math.sqrt(dd * (1 - dd / dn)) / dn,
                dn=dn, dd=dd, P1=k1 / n1, eP1=math.sqrt(k1 / n1 * (1 - k1 / n1) / n1))


def main():
    rows = {}
    for p in sorted(glob.glob(os.path.join(D, "*.txt"))):
        r = load(p)
        if r:
            rows[os.path.basename(p)[:-4]] = r
    gumps = {"9": [rows[t] for t in rows if t.startswith("r9_gump_s96")], "11": [rows["gump_R11_s1001"]] if "gump_R11_s1001" in rows else []}
    for R in ("9", "11"):
        if not gumps[R]:
            continue
        g = stats(gumps[R])
        print(f"R = {R}: my gump ln tau {g['lt']:.4f} +- {g['er']:.4f} ({g['D']:.0f} deaths); dips {g['dips']:.4e}, deadliness {g['dead']:.5f} +- {g['edead']:.5f}, P1 {g['P1']:.4f} +- {g['eP1']:.4f}")
        for t, r in rows.items():
            if not t.startswith(f"full{R}_"):
                continue
            s = stats([r])
            dm, em = s["lt"] - g["lt"], math.hypot(s["er"], g["er"])
            dt, et = s["lt"] - GREF[R][0], math.hypot(s["er"], GREF[R][1])
            th = THEIRS.get((R, r["D0"])) if "p01" not in t and "m01" not in t else None
            z = f"  theirs {th[0]:+.3f} +- {th[1]:.3f}: diff {(dt - th[0]) / math.hypot(et, th[1]):+.2f} sigma (on their ref)" if th else ""
            dl = math.log(s["dips"] / g["dips"]); edl = math.sqrt(1 / s["dn"] + 1 / g["dn"])
            dlp = math.log(s["dead"] / g["dead"]); edlp = math.sqrt((1 - s["dead"]) / s["dd"] + (1 - g["dead"]) / g["dd"])
            print(f"  {t:24s} d={r['D0']} ln tau {s['lt']:.4f} +- {s['er']:.4f} ({s['D']:.0f})  Delta vs my gump {dm:+.4f} +- {em:.4f}, vs their ref {dt:+.4f} +- {et:.4f}{z}")
            print(f"  {'':24s}     d ln dips {dl:+.4f} +- {edl:.4f}  d ln deadliness {dlp:+.4f} +- {edlp:.4f}  P1 {s['P1']:.4f} +- {s['eP1']:.4f} (gump {g['P1']:.4f})")


if __name__ == "__main__":
    main()
