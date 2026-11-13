"""summarize.py -- curated tables from research/scratch/class/results.jsonl.

    python3 summarize.py scan   > data/scan_table.md      (one line per (lattice, cap): torus class, strip/slab face data, R1)
    python3 summarize.py faces  > data/faces.tsv          (every face-law measurement)
"""
import json, math, os, sys
import lattices as LT, theory as TH

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scratch", "class", "results.jsonl")


def load():
    return [json.loads(l) for l in open(RES) if l.strip()]


def geom(lat, b):
    L = LT.get(lat)
    u = TH.sealed_rays(L, b)[0]
    cs = TH.counts(L, u)
    return dict(K=L.K, a0=min(c[1] for c in cs), am=max(c[0] for c in cs), Kf=max(c[0] + c[1] for c in cs))


def classify(sc):
    """Final verdict from the raw numbers of a scan record (same rules as PREDICTIONS.md 'SLAB')."""
    fs = sc["faces"]
    if sc["bulk"] in ("die", "freeze"):
        return sc["bulk"]
    ok = [f for f in fs if f["face"] >= 20 and f["lntau"] is not None]
    wall = [f for f in fs if f["face"] == 0 and f["dens"][1] > 0.9 and f["act"][1] < 0.02]
    if wall and len(wall) >= len([f for f in fs if f["dens"][1] >= 0]) :
        return "WALL"
    glassy = sum(f["p2"] + f["cyc"] for f in fs) > sum(f["face"] for f in fs)
    if len(ok) >= 2:
        gain = ok[-1]["lntau"] - ok[0]["lntau"]
        slope = gain / (ok[-1]["A"] - ok[0]["A"])
        cvok = all(f["cv"] is None or 0.8 <= f["cv"] <= 1.25 for f in ok)
        if glassy or sc["bulk"] != "chaos":
            return f"{sc['bulk']}, settles ({slope:+.3f})"
        if gain >= 1.0 and cvok:
            return f"FACE LAW {slope:.3f}/cell" + (" strong" if slope >= 0.15 else (" weak" if slope < 0.10 else ""))
        return f"faces die, gain {gain:+.2f} ({slope:+.3f}/cell)"
    if all(f["face"] == 0 and f["seal"] + f["p2"] + f["cyc"] == 0 and sum(f["early"]) > 1000 for f in fs):
        return "faces die before burn-in at these sizes"
    return "unclear"


if __name__ == "__main__":
    recs = load()
    if sys.argv[1] == "scan":
        last = {}
        for r in recs:
            if r.get("kind") == "scan":
                last[(r["lattice"], r["c"])] = r
        cur = None
        for (lat, c), r in sorted(last.items(), key=lambda kv: (LT.ALL.index(kv[0][0]), kv[0][1])):
            g = geom(lat, r["b"])
            if lat != cur:
                cur = lat
                print(f"\n### {lat}: K={g['K']} b={r['b']} a0={g['a0']} a-={g['am']} K_f={g['Kf']} (wall cap {g['Kf'] + 1})\n")
                print("| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |")
                print("|---|---|---|---|---|---|---|---|")
            rho = r["rho"] if r["rho"] and r["rho"] > 0 else None
            R1 = (g["a0"] + 1) * rho ** g["am"] if rho else None
            fs = " ; ".join(f"A={f['A']}: {f['face']}/{f['seal']}/{f['p2'] + f['cyc']}"
                            + (f", {f['lntau']:.2f}" if f["lntau"] else "") + (f", cv {f['cv']:.2f}" if f["cv"] else "")
                            + (f", ρ_f {f['dens'][1]:.2f}" if f["dens"][1] >= 0 else ", none survive burn-in") for f in r["faces"])
            rule = r["rule"] if len(r["rule"]) < 26 else f"cap {c}"
            print(f"| {c} | {rule} | {r['bulk']} | {rho if rho is None else round(rho, 3)} | {r['act'] if r['act'] > 0 else '-'} | "
                  f"{'-' if R1 is None else round(R1, 2)} | {fs} | {classify(r)} |")
    else:
        print("lattice\trule\tu\tm\tA\tN\tface\tseal\tsettle\tearly\tlntau\terr\tcv\trho_int\trho_face\tact_face\tgens")
        for r in recs:
            if r.get("kind") == "face":
                print("\t".join(str(x) for x in (r["lattice"], r["rule"], r["u"], r["m"], r["A"], r["N"], r["face"], r["seal"],
                                                 r["p2"] + r["cyc"], sum(r["early"]), None if r["lntau"] is None else round(r["lntau"], 3),
                                                 None if r["err"] is None else round(r["err"], 3), None if r["cv"] is None else round(r["cv"], 2),
                                                 r["dens"][0], r["dens"][1], r["act"][1], r["gens"])))
