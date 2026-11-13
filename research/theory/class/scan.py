"""scan.py -- the capped-threshold family of one lattice: torus class, then the face law at two or three sizes.

    python3 scan.py LATTICE [b] [--cs 5,6,7] [--sizes 12,20,28] [--m 16] [--sec 15] [--w 1]

Verdict per rule (class.md section 4 defines the classes):
  die / freeze / glass : the torus bulk does not sustain chaos (no face test needed, but run anyway at the small size)
  ERODE  : faces die, but the wait does not grow with the face (d ln tau / dA <= 0.02 per cell or tau small)
  WALL   : faces never die and the face layer is inactive, or replicas settle with live faces
  GUMP   : chaos in the bulk, face deaths outnumber other endings, the wait grows exponentially with the face
           (ln tau increases by >= 0.5 from the smallest to the largest size, per-cell slope reported), CV ~ 1
  GUMP?  : as GUMP but too few deaths at the larger sizes to measure a slope
"""
import argparse, json, math, os, sys
import lattices as LT, theory as TH, run as RN


def verdict(bk, faces):
    cls = bk["cls"]
    if cls in ("die", "freeze"):
        return cls
    out = []
    f0, f1 = faces[0], faces[-1]
    nonface0 = f0["seal"] + f0["p2"] + f0["cyc"]
    tot_face = sum(f["face"] for f in faces)
    tot_other = sum(f["seal"] + f["p2"] + f["cyc"] for f in faces)
    if tot_face == 0:
        if tot_other == 0:
            return "GUMP?(no deaths)" if cls == "chaos" else cls + "/noevents"
        return "WALL" if (f1["p2"] + f1["cyc"]) >= f1["seal"] else "CUT"
    have = [f for f in faces if f["face"] >= 5]
    if len(have) >= 2:
        slope = (have[-1]["lntau"] - have[0]["lntau"]) / (have[-1]["A"] - have[0]["A"])
        gain = have[-1]["lntau"] - have[0]["lntau"]
        if gain >= 0.5 and len(have) == len(faces):
            v = "GUMP" if cls == "chaos" else cls + "+edge"
        elif gain >= 0.5:
            v = "GUMP?" if cls == "chaos" else cls + "+edge?"
        else:
            v = "ERODE"
        return f"{v} slope={slope:.3f}"
    # deaths only at the smallest size: lifetimes grew past the budget
    if f0["face"] >= 5 and tot_other <= tot_face:
        return ("GUMP?" if cls == "chaos" else cls + "+edge?") + "(grows beyond budget)"
    if f0["face"] < 5 and tot_other > tot_face:
        return "WALL" if sum(f["p2"] + f["cyc"] for f in faces) >= sum(f["seal"] for f in faces) else "CUT"
    return "unclear"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("lattice")
    ap.add_argument("b", nargs="?", type=int)
    ap.add_argument("--cs")
    ap.add_argument("--sizes")
    ap.add_argument("--m", type=int)
    ap.add_argument("--sec", type=float, default=15)
    ap.add_argument("--w", type=int, default=1)
    ap.add_argument("--n", type=int)
    ap.add_argument("--T", type=int, default=4096)
    a = ap.parse_args()
    L = LT.get(a.lattice)
    b = a.b if a.b is not None else TH.confinement(L)["b_min"]
    K = L.K
    cs = [int(x) for x in a.cs.split(",")] if a.cs else list(range(b + 1, K + 2))
    sizes = [int(x) for x in a.sizes.split(",")] if a.sizes else ([12, 20] if L.dim == 2 else [3, 4])
    m = a.m if a.m else (16 if L.dim == 2 else 8)
    u = TH.sealed_rays(L, b)[0]
    print(f"# {a.lattice}: K={K} b={b} u={u} slab m={m} sizes={sizes}")
    for c in cs:
        B, S = TH.capped(b, c, K, a.w)
        bk = RN.bulk(a.lattice, B, S, n=a.n, T=a.T, quiet=True)
        p = max(0.3, min(0.8, bk["dens"] + 0.05)) if bk["dens"] and bk["dens"] > 0.05 else None
        faces = []
        for n in sizes:
            f = RN.face(a.lattice, B, S, m, n, sec=a.sec, p=p, quiet=True)
            faces.append(f)
            if f["face"] < 5 and (f["seal"] + f["p2"] + f["cyc"]) < 5 and len(faces) >= 1 and bk["cls"] == "chaos":
                break  # already beyond the budget
        v = verdict(bk, faces)
        line = (f"{a.lattice:9s} c={c:2d} {TH.rule_name(B, S):20s} bulk={bk['cls']:6s} rho={bk['dens']:.3f} act={bk['act']:.3f} | " +
                " ; ".join(f"A={f['A']}: face={f['face']} seal={f['seal']} set={f['p2'] + f['cyc']} "
                           f"lnT={'%.2f' % f['lntau'] if f['lntau'] else '-'} cv={'%.2f' % f['cv'] if f['cv'] else '-'} "
                           f"rf={f['dens'][1]:.2f} af={f['act'][1]:.2f}" for f in faces) + f" | {v}")
        print(line, flush=True)
        RN.save(dict(kind="scan", lattice=a.lattice, b=b, c=c, rule=TH.rule_name(B, S), verdict=v, bulk=bk["cls"],
                     rho=bk["dens"], act=bk["act"], faces=[{k: f[k] for k in ("A", "m", "n", "face", "seal", "p2", "cyc", "lntau", "cv", "dens", "act", "exposure", "early")} for f in faces]))
