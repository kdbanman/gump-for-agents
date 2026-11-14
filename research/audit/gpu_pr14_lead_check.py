#!/usr/bin/env python3
"""Lead's own re-derivation of the headline numbers of pull request 14 (GPU session: slab faces with the transverse
firewall channel resolved) from the per-life data in its JSON files. Shares no code with research/gpu/.

  python3 research/audit/gpu_pr14_lead_check.py DIR     DIR holds fwslab*.json (research/data/gpu_facelaw after the merge)

Per-life rows in `raw` (int64, zlib, base64): age, kind, birth generation, firewall direction.
Kinds: 0 open at the end, 1 face death, 2 and 3 settled, 4 transverse firewall.
"""
import base64, glob, json, math, sys, zlib
import numpy as np

def lives(d):
    r = d["raw"]
    return np.frombuffer(zlib.decompress(base64.b64decode(r["b64"])), np.int64).reshape(r["shape"])

def lt(E, n, faces=1):
    return math.log(faces * E / n), 1 / math.sqrt(n)

tot = {}
for f in sorted(glob.glob(sys.argv[1] + "/fwslab*.json")):
    d = json.load(open(f)); name = "x".join(map(str, d["slab"]))
    if "raw" not in d:
        E, nf, nw = d["exposure"], d["face"], d["fw"]; src = "summary fields only (no per-life data in the file)"
    else:
        a, k, b, dr = lives(d)
        E, nf, nw = int(a.sum()), int((k == 1).sum()), int((k == 4).sum())
        assert E == d["exposure"] and nf == d["face"] and nw == d["fw"], "summary fields disagree with the lives"
        assert (k == 0).sum() == d["replicas"] and len(a) == d["replicas"] + nf + nw + ((k == 2) | (k == 3)).sum()
        src = (f"{len(a)} lives: {int((k == 0).sum())} open, {nf} face, {nw} firewall "
               f"(directions {np.bincount(dr[k == 4], minlength=4)[1:].tolist()}), {int(((k == 2) | (k == 3)).sum())} settled")
        # is the face hazard flat in the age of the life?  three age bins holding equal exposure
        order = np.argsort(a); cum = np.cumsum(a[order]); edges = [0]
        ages = np.sort(a)
        # exposure accumulated below age t: sum(min(a, t)); find t at 1/3 and 2/3 of E by bisection
        for q in (1 / 3, 2 / 3):
            lo, hi = 0, int(a.max())
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if np.minimum(a, mid).sum() < q * E: lo = mid
                else: hi = mid
            edges.append(hi)
        edges.append(int(a.max()) + 1)
        bins = []
        for i in range(3):
            e = (np.minimum(a, edges[i + 1]) - np.minimum(a, edges[i])).sum()
            n = int(((k == 1) & (a >= edges[i]) & (a < edges[i + 1])).sum())
            bins.append(f"[{edges[i]:.2e},{edges[i+1]:.2e}): {n} deaths, ln tau {math.log(2 * e / max(n, 1)):.3f}")
        src += "\n      face hazard by age of the life (equal exposure): " + "; ".join(bins)
    t = tot.setdefault(name, [0, 0, 0]); t[0] += E; t[1] += nf; t[2] += nw
    print(f"{f.split('/')[-1]}: {src}")
print()
res = {}
for name, (E, nf, nw) in tot.items():
    A = 3 * int(name.split("x")[0]) * int(name.split("x")[1])
    f_, fe = lt(E, nf, 2); w_, we = lt(E, nw); first, _ = lt(E, nf + nw, 2)
    res[name] = (f_, fe)
    print(f"{name} (A = {A}): exposure {E:.4e}; face {nf}, firewall {nw} ({100 * nw / (nf + nw):.1f}% of first events); "
          f"ln tau_face = {f_:.3f} +- {fe:.3f}; ln tau_fw = {w_:.3f} +- {we:.3f}; first-event statistic {first:.3f}; "
          f"slab line -0.091 + 0.2088 A = {-0.091 + 0.2088 * A:.3f}")
if "6x6x8" in tot and "6x7x8" in tot:
    # pool A = 108 with the earlier unscreened run (NOTEBOOK 2026-11-14: 22.470 +- 0.047 on 447 first deaths),
    # its face deaths taken as first deaths x (1 - firewall share measured here)
    E2, nf2, nw2 = tot["6x6x8"]; share = nw2 / (nf2 + nw2)
    E1 = 447 * math.exp(22.470) / 2; n1 = 447 * (1 - share)
    p = math.log(2 * (E1 + E2) / (n1 + nf2)); pe = 1 / math.sqrt(n1 + nf2)
    f126, e126 = res["6x7x8"]
    print(f"pooled A = 108: {p:.3f} +- {pe:.3f} ({p - (-0.091 + 0.2088 * 108):+.3f} on the slab line)")
    print(f"slope 108 -> 126: pooled {(f126 - p) / 18:.4f} +- {math.hypot(e126, pe) / 18:.4f}; "
          f"this run alone {(f126 - res['6x6x8'][0]) / 18:.4f} +- {math.hypot(e126, res['6x6x8'][1]) / 18:.4f}")
