#!/usr/bin/env python3
"""Pick what the figures need out of sources/*.json into ../data/<key>.json, one file per key.   python3 site/collect/collect.py
The source files were gathered from the repository by helper agents on 2026-11-14 and carry their own
"src" and "how" fields; this script only selects and reshapes, it does not compute results."""
import json, pathlib
here = pathlib.Path(__file__).parent
S = lambda n: json.loads((here / "sources" / n).read_text())
out = {}

s11 = S("side11.json")
out["side11"] = {"pops": s11["pops"], "peels": [c for c in s11["rads_changes"] if c[0] > 100]}

se = S("series.json")
ss = se["soup_staircase"]
out["soup"] = {k: ss[k] for k in ("radius", "generations", "final_pop", "pop_bucket_width", "pop_min", "pop_max", "outer_face_area_initial")}
out["soup"]["deaths"] = sorted([g, s] for v in ss["layer_deaths_by_direction"].values() for g, s in v)
out["soup"]["by_dir"] = list(ss["layer_deaths_by_direction"].values())
fd = se["face_death_closeup"]
out["death"] = {"faces": [{"area": f["area_at_death"], "gen": f["death_gen"], "pop": f["pop"]} for f in fd["faces"]],
                "ordinary": {"area": fd["ordinary_life"]["area"], "mean": fd["ordinary_life"]["mean"], "pop": fd["ordinary_life"]["pop"][:600]}}
kg = se["kagome_face"]
out["kagome"] = {"area": kg["area"], "live": kg["live"], "gen": kg["gen"], "sites": [[round(s[3], 3), round(s[4], 3), s[5]] for s in kg["sites"]]}
t2 = se["toy2d_run"]
out["toy"] = {k: t2[k] for k in ("box", "final_state_entered_gen", "final_pop", "bbox_steps", "pop_bucket_width", "pop_min", "pop_max", "snapshot_gen", "snapshot_rows")}
lh = se["lineage_histogram"]
out["lineage"] = {"n": lh["structured"]["n"], "mean": lh["structured"]["mean"], "max": lh["structured"]["max"], "counts": lh["structured"]["counts"],
                  "expected": lh["exp_expected_structured"], "cubes": [[c["side"], c["ratio"]] for c in lh["cube_plateaus"]]}

st = S("structure.json")
rs = st["rule_survey"]
out["rules"] = {"B": rs["B_sets"], "S": rs["S_sets"], "cls": rs["torus_class"], "life": rs["log10_med_lifetime"], "gump": [rs["gump"]["row"], rs["gump"]["col"]],
                "counts": rs["counts"], "removed": rs["one_count_removed"]["value"], "added": list(rs["add_S2_or_S7"]["value"])[:2]}
fc = st["fauna_cells"]
out["fauna"] = {k: {"cells": fc[k]["phase0"], "period": fc[k]["period"], "n": fc[k]["cells"], "L": fc[k].get("loop_L"), "m": fc[k].get("twist_m")}
                for k in ("S6a", "S12a", "P2.6a", "S8b", "P66.27a", "C48.24a", "C36.33a")}
cnt = st["fauna_counts"]
out["still"] = {"n": cnt["strict_still_lifes_by_cells"]["value"]["n"], "count": cnt["strict_still_lifes_by_cells"]["value"]["count"]}
out["clocks"] = [[r[0], r[1], r[2], r[3], r[5]] for r in st["clockwork"]["all_long_objects"]["rows"]]
sl = st["thickness_and_threshold"]["slab_lifetimes"]["value"]
out["slabs"] = {m: [sl[f"{m}_mean_life"]["N"], sl[f"{m}_mean_life"]["tau"]] for m in ("m1", "m2", "m3")}


# ---- measured results (measurements.json) ----
me = S("measurements.json")
fl = me["face_law"]
out["law"] = {
    "oct": fl["octahedral_engine"]["points"]["rows"],                                   # A, R, ln tau, se, deaths
    "gpu": [r for r in fl["octahedral_gpu"]["points"]["rows"] if r[0] >= 108],
    "slab": fl["slab_faces"]["points"]["rows"],                                         # A, ln tau, se, peels, ...
    "slab_fit": [-0.091, 0.2088],                                                       # from slab_faces.fit
    "slopes": [r for r in fl["local_slopes"]["points"]["rows"] if r[4] in ("", "GPU 84")],
}
assert "-0.091" in fl["slab_faces"]["fit"] and "0.2088" in fl["slab_faces"]["fit"]
fdh = me["face_death"]
out["tail"] = {"A": fdh["tail_table"]["A"], "ln_p": fdh["tail_table"]["ln_p"], "ln_h": fdh["tail_table"]["ln_h_k0"],
               "share": fdh["single_cell_share"]["pct_from_n1_n2_n3"]["45"]}
sy = me["symmetric_faces"]
out["sym"] = {"cpu": [r[:5] for r in sy["cpu"]["points"]["rows"] if r[5] in ("", "soups") and r[0] < 759 and not (r[0] == 693 and r[1] == "v" and r[2] < 10)],
              "gpu": [[r[0], r[1], r[3], r[4], r[5]] for r in sy["gpu"]["points"]["rows"]],   # A, centre, deaths, ln tau, se
              "fit": [0.698, 0.209 / 6, -0.196]}
lc = me["legacy_cubes"]
assert "39,142,675-631,552,622" in lc["side16"]["forecast"] and "1.8-4.0e10" in lc["side17"]["committed"]
out["cubes"] = {"rows": [r[:3] for r in lc["cubes"]["rows"]], "f16": [39142675, 238971017, 631552622], "f17": [1.8e10, 2.6e10, 4.0e10]}
out["toylaw"] = me["toy2d"]["points"]["rows"]
out["forecasts"] = [{"line": f["line"], "result": f.get("result") or "; ".join(f.get("items", [])), "pred": f.get("pred"), "actual": f.get("actual")} for f in me["forecasts"]]
def who(by):
    b = (by or "").lower()
    for key, name in (("automaton", "the automaton itself"), ("critic", "the swarm's critic"), ("reviewer", "a reviewer"), ("auditor", "the auditor"), ("lead", "the lead's own re-check")):
        if key in b: return name
    return "another agent"
corr = [{"said": r[2], "now": r[3], "by": r[4], "who": who(r[4]), "line": r[1]} for r in me["corrections"]["rows"] if r[2]]
corr += [{"said": f["said"], "now": f["why"], "by": f["by"], "who": who(f["by"]), "line": f["line"]} for f in fl["retired_fits"]]
corr += [{"said": f["formula"], "now": f.get("why", "replaced by a refit"), "by": f["by"], "who": who(f["by"]), "line": f["line"]} for f in sy["fits"]
         if f["status"] == "retired" and "automaton" not in f["by"]]      # the automaton's refutation of A/7.7 is already in the list above
out["corrections"] = corr

# ---- the swarm (swarm.json) ----
sw = S("swarm.json")
out["swarm"] = {
    "problem": sw["problem"]["line"],
    "lines": {k: {"label": v["label"], "line": v["line"], "written": v["rounds_written"], "refereed": v["rounds_refereed"], "state": v["state_at_pause"],
                  "results": [[r["label"], r["line"], r["tag"]] for r in v["results"]], "dropped": len(v["refuted_or_withdrawn"]),
                  "top": v["most_important_per_critic"]["line"], "next": v["next"]} for k, v in sw["lines"].items()},
    "dead": [[x["label"], x["line"]] for x in sw["joint_picture"]["dead"]], "alive": [[x["label"], x["line"]] for x in sw["joint_picture"]["alive"]],
    "formula": sw["joint_picture"]["formula_for_gamma"], "theorems": sw["joint_picture"]["theorems"],
    "counts": sw["counts"], "library": sw["library"]["counts"], "errors": [[c[0], c[1], c[2]] for c in sw["board"]["corrections"]],
    "graveyard": [g[1] for g in sw["board"]["graveyard"]], "predictions": [[p["who"], p["predicts"]] for p in sw["predictions"]["entries"]],
}

# ---- the project (project.json) ----
pj = S("project.json")
ck = pj["checking"]
out["project"] = {
    "grades": ck["claims_ledger"]["recount_all_rows"], "grade_meaning": ck["claims_ledger"]["grades"], "checks": ck["check_sh"]["families"], "checks_n": ck["check_sh"]["checks_default"],
    "audits": [[a["label"], a["line"]] for a in ck["audits"]],
    "prior": [[r["year"], r["authors"], r["line"], r["read"]] for r in pj["prior_art"]["refs"]], "ours": pj["prior_art"]["own_contributions_possibly_new"], "known": pj["prior_art"]["not_new"],
    "timeline": pj["timeline"], "programme": [[n["id"], n["label"], n["line"], n["status"]] for n in pj["programme"]["nodes"]],
    "open": [[o["n"], o["label"], o["line"], o["status"]] for o in pj["open_problems"]],
    "class": [[x["label"], x["line"]] for x in pj["theory_unchecked"]["class_md"]],
}

# ---- the refresh of 2026-11-14 (afternoon): update-2026-11-14.json, every quote checked against the repository ----
import re, subprocess
repo = here.parent.parent
norm = lambda s: re.sub(r"\s+", " ", s)
corpus = norm((repo / "research" / "NOTEBOOK.md").read_text()) + " " + norm((repo / "research" / "CLAIMS.md").read_text())
def checked(item):
    q = norm(item["quote"])
    if "file" in item:   # a quote from another file of the repository (added 2026-11-15, third refresh: the essay)
        # (late morning refresh: block-quote markers at line starts are dropped, for the owner's journal)
        assert q in norm(re.sub(r"\n> ?", "\n", (repo / item["file"]).read_text())), "quote not found in " + item["file"] + ": " + q[:80]
    else:
        assert q in corpus, "quote not found in NOTEBOOK.md or CLAIMS.md: " + q[:80]
    for w in item.get("words", []): assert w in q, (w, q)
    for e in item.get("pow10", []): assert "10" + "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] for c in str(e)) in q, (e, q[:80])
    if "words" not in item:
        for v in item.get("value", []):
            forms = {str(v), format(v, ","), ("%g" % v)}
            if isinstance(v, float) and 0 < abs(v) < 1e-3: forms.add(("%.6f" % v).rstrip("0"))   # 2.9e-05 written 0.000029 (evening refresh)
            assert any(f in q for f in forms), ("number not in its quote", v, q[:80])
    return item
U = S("update-2026-11-14.json")
for sec in ("face12e", "gpu", "noise", "swarm"):
    for k, v in U[sec].items(): checked(v)
for k in ("bond10", "bond10_columns", "oos_escapes", "law_cases"): checked(U["family"][k])
for r in U["family"]["rows"]: checked(r)
for f in U["forecasts"]: checked(f)
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in U["forecasts"]]
for a in U["audits"]: assert (repo / a["file"]).exists(), a["file"]
fe, gp, no, sw = U["face12e"], U["gpu"], U["noise"], U["swarm"]
out["face12e"] = {"box": list(zip(fe["box_life"]["n"], fe["box_life"]["value"])) + [[7, fe["box7"]["value"][0] * 1e8]],
                  "box7": fe["box7_count"]["value"], "sym": list(zip(fe["sym_life"]["n"], fe["sym_life"]["value"])),
                  "wall": [list(r) for r in zip(fe["wall"]["A"], fe["wall"]["value"], fe["wall"]["se"])], "slope": fe["wall_slope"]["value"],
                  "torus": fe["torus"]["value"], "symfactor": fe["sym_factor"]["value"][0], "layers": fe["layers"]["value"], "gen1": fe["cube_gen1"]["value"]}
out["family"] = {"rows": [{k: r[k] for k in ("name", "rule", "lattice", "hull", "law", "note", "status")} for r in U["family"]["rows"]],
                 "bond10": U["family"]["bond10"]["value"], "bond10_median_pow10": U["family"]["bond10"]["pow10"][3], "bond10_factor_pow10": U["family"]["bond10"]["pow10"][0], "columns": U["family"]["bond10_columns"]["value"], "oos": U["family"]["oos_escapes"]["value"], "cases": U["family"]["law_cases"]["value"]}
out["law"]["slab_gpu"] = [[108] + gp["slab_a"]["value"], [126] + gp["slab_b"]["value"][3:5]]     # A, ln tau, se (firewall channel separated; 108 pooled)
out["law"]["slab_slope"] = gp["slope"]["value"]                                                  # 108, 126, slope, se
out["law"]["mirror"] = [list(r) for r in zip(gp["mirror"]["A"], gp["mirror"]["value"][:3])]
out["law"]["rim"] = gp["rim"]["value"]; out["law"]["width"] = gp["width_test"]["value"]
out["weibull"] = gp["weibull"]["value"]
out["noise"] = {"toy": [list(r) for r in zip(no["toy"]["L"], no["toy"]["strip"], no["toy"]["model"])], "gump": [list(r) for r in zip(no["gump"]["A"], no["gump"]["slab"], no["gump"]["model"])],
                "w5": no["w5"]["value"], "w4": no["w4"]["value"], "mirror": no["mirror"]["value"], "notch": no["notch"]["value"]}
out["closed"] = {"relative": [list(r) for r in zip(sw["relative"]["L"], sw["relative"]["ln"])], "exam": list(zip(sw["exam"]["labels"], sw["exam"]["value"])),
                 "share": sw["share"]["value"], "V": sw["V"]["value"], "lone": sw["lone"]["value"]}
# claims ledger: the counts line of research/CLAIMS.md as it stands
cl = norm((repo / "research" / "CLAIMS.md").read_text())
m = re.search(r"(\d+) claims, by the best grade any part of the claim has: \*\*A\*\* (\d+) .*?\*\*B\*\* (\d+) .*?\*\*C\*\* (\d+) · \*\*D\*\* (\d+)", cl)
out["project"]["grades"] = {"total": int(m[1]), "A": int(m[2]), "B": int(m[3]), "C": int(m[4]), "D": int(m[5])}
out["project"]["audits"] += [[a["label"], a["line"]] for a in U["audits"]]
# timeline: totals and merged pull requests from git; milestones of 2026-11-14 from the update file
git = lambda *a: subprocess.run(["git", "-C", str(repo)] + list(a), capture_output=True, text=True, check=True).stdout.strip()
tl = out["project"]["timeline"]
last = git("log", "-1", "--format=%cI|%h")
tl["last_commit"] = last.split("|")[0][:19] + "Z (" + last.split("|")[1] + ")" if last.split("|")[0].endswith("+00:00") else tl["last_commit"]
tl["totals"]["commits"] = int(git("rev-list", "--count", "HEAD"))
have = {p["n"] for p in tl["pull_requests"]}
for line in git("log", "--format=%cI|%s").splitlines():
    iso, subj = line.split("|", 1); mm = re.search(r"\(#(\d+)\)$", subj)
    if mm and int(mm[1]) not in have:
        import datetime
        t = datetime.datetime.fromisoformat(iso).astimezone(datetime.timezone.utc)
        tl["pull_requests"].append({"n": int(mm[1]), "title": subj[: mm.start()].strip(), "date": t.strftime("%Y-%m-%dT%H:%MZ")}); have.add(int(mm[1]))
tl["pull_requests"].sort(key=lambda p: p["date"])
out["width"] = gp["width_test"]["value"][5:7]
tl["milestones"] = tl["milestones"] + [{"date": x["date"], "text": x["text"]} for x in U["milestones"]]

# ---- the second refresh of 2026-11-14: update-2026-11-14b.json (width of a periodic face, GP9; twisted faces, SH1, SH2) ----
V = S("update-2026-11-14b.json")
for sec in ("width", "shape"):
    for k, v in V[sec].items():
        if k != "rows": checked(v)
for r in V["shape"]["rows"]: checked(r)
for f in V["forecasts"]: checked(f)
for a in V["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in V["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in V["audits"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in V["milestones"]]
vw, vs = V["width"], V["shape"]
out["shape"] = {
    # loop squared, loop length, ln tau (experiment), se, ln tau (review's independent stepper), se, tori
    "rows": [r["value"][:4] + (r["value"][4:6] if len(r["value"]) > 4 else [None, None]) + [r["tori"]] for r in vs["rows"]],
    "agree": vs["agree"]["value"], "control": vs["control"]["value"], "pair60": vs["pair60"]["value"], "pair60_review": vs["pair60_review"]["value"],
    "size": vs["size"]["value"], "forecast": vs["forecast"]["value"],
    "pairs": [[l, a] + vw["pairs"]["value"][2 * i: 2 * i + 2] for i, (l, a) in enumerate(zip(vw["pairs"]["labels"], vw["pairs"]["A"]))],
    "cpu72": vw["cpu72"]["value"],
}
out["law"]["families"] = [[s] + vw["families"]["value"][2 * i: 2 * i + 2] for i, s in enumerate(vw["families"]["s"])]   # short side, slope, se
out["law"]["wide"] = vw["wide"]["value"][:2]; out["law"]["mixed"] = vw["mixed"]["value"]
assert out["law"]["slab_fit"][1] == out["law"]["mixed"][1]

# ---- the third refresh of 2026-11-14: update-2026-11-14c.json (the census of every torus of a given area, SH2-SH5) ----
C = S("update-2026-11-14c.json")
for k, v in C["census"].items(): checked(v)
for f in C["forecasts"]: checked(f)
for a in C["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in C["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in C["audits"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in C["milestones"]]
cc = C["census"]
out["census"] = {
    "cost": [list(r) for r in zip(cc["cost"]["loop2"], cc["cost"]["value"])],                      # loop², d ln tau / dA (48 -> 60)
    "review": [list(r) for r in zip([3, 4, 7, 12, 16], cc["cost_review"]["value"])],              # the review's own stepper (no loop² 13)
    "pair": cc["pair"]["value"], "pair48": cc["pair48"]["value"], "laws": cc["laws"]["value"],
}


# ---- the refresh of 2026-11-15: update-2026-11-15.json (CN1, GP10, SH6-SH9, TH1-TH6, ZL1-ZL2, prior art, second readings) ----
R = S("update-2026-11-15.json")
for sec in ("pairs", "thin", "constant", "patches", "zombie", "swarm"):
    for k, v in R[sec].items():
        if k != "rows": checked(v)
for r in R["pairs"]["rows"]: checked(r)
checked(R["prior"]["list"])
for r in R["prior"]["refs"]: checked(r)
for f in R["forecasts"]: checked(f)
for a in R["audits"]: assert (repo / a["file"]).exists(), a["file"]
pl = R["prior"]["list"]
assert all(w in pl["words"] for w in pl["ours"] + pl["known"])
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in R["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in R["audits"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in R["milestones"]]
rp, rt, rc, rz, rq = R["pairs"], R["thin"], R["constant"], R["zombie"], R["patches"]
out["pairs"] = {   # id, A, loop², d (signed), se, review d (signed) or None, review se
    "rows": [[r["id"], r["value"][0], r["value"][1], r["sign"] * r["value"][2], r["value"][3]] + ([r["sign"] * r["value"][4], r["value"][5]] if len(r["value"]) > 4 else [None, None]) for r in rp["rows"]],
    "nodiff": rp["nodiff"]["value"], "candidates": rp["candidates"]["value"], "gram": rp["gram"]["value"][0]}
v = rt["slopes"]["value"]
out["thin"] = {"slopes": [[48, 60, v[0], None], [60, 72, v[1], None], [72, 84, v[2], v[3]], [84, 96, v[4], v[5]], [96, 108, v[6], None]],   # from A, to A, cost per cell, se ("about 0.103 at 108": the 96 -> 108 step)
               "wall": rt["wall"]["value"], "limit": rt["limit"]["value"], "overlap": rt["overlap"]["value"], "layers": rt["layers"]["value"],
               "exact": rt["exact"]["value"][0], "profile_review": rt["profile"]["value"][0:6], "profile": rt["profile"]["value"][7:13], "b": rt["profile"]["value"][6], "wide": rt["half"]["value"][0]}
out["constant"] = {"verdict": rc["verdict"]["value"], "periodic": rc["periodic"]["value"], "hull": rc["hull"]["value"], "slopes": rc["slopes"]["value"],
                   "single": rc["single"]["value"], "split": rc["split"]["value"], "gpu": rc["gpu"]["value"]}
L5 = rq["lnp"]
out["patches"] = {"lnp": [[c, lab, L5["sign"] * x] for c, lab, x in zip(L5["cells"], L5["labels"], L5["value"])], "se": {"48": L5["se"][0], "60": L5["se"][1], "75": L5["se"][2]},
                  "cpu45": [60, -rq["cpu45"]["value"][0], rq["cpu45"]["value"][1], rq["cpu45"]["value"][2]], "cpu45_cost": rq["cpu45_cost"]["value"][0],
                  "cost": [list(r) for r in zip(rq["cost"]["cells"], rq["cost"]["value"][:4])], "cost_se": rq["cost"]["value"][4], "range": rq["range"]["value"], "fit": rq["fit"]["value"]}
assert L5["cells"][5] == 60 and L5["labels"][5] == "4×5"
g = rz["gpu"]["value"]
out["zombie"] = {"rate": rz["rate"]["value"], "stuck": rz["stuck"]["value"], "cpu": rz["cpu"]["value"], "periods": rz["periods"]["value"], "state": rz["state"]["value"],
                 "gpu": [[rz["gpu"]["runs"][0], g[0] * 1e-3, g[1]], [rz["gpu"]["runs"][1], g[2] * 1e-2, g[3]], [rz["gpu"]["runs"][2], g[4] * 1e-2, g[5]]], "r11": g[6] * 1e-4}
assert "6.7 × 10⁻³" in rz["gpu"]["quote"] and "1.2 × 10⁻²" in rz["gpu"]["quote"] and "1.0 × 10⁻²" in rz["gpu"]["quote"] and "1.3 × 10⁻⁴" in rz["gpu"]["quote"]
zj = S("zombie.json")    # the state itself (scripts/zombie.py, from research/audit/shape3/zombie_1_4_12_p16.txt)
assert zj["live_slab"] == out["zombie"]["state"][0]
out["zombie"]["sim"] = {"H": zj["H"], "cells": zj["cells"], "lifted": zj["lifted"]}
out["prior3"] = {"ours": pl["ours"], "known": pl["known"], "refs": [[r["year"], r["who"], r["line"], r["read"]] for r in R["prior"]["refs"]]}
out["swarm2"] = {"counting": R["swarm"]["counting"]["value"][0]}


# ---- the second refresh of 2026-11-15: update-2026-11-15b.json (the symmetric collapse, S5-S9; the new clocks and wires, Z12, Z13) ----
B = S("update-2026-11-15b.json")
for k, v in B["sym"].items():
    if k != "ladder": checked(v)
for r in B["sym"]["ladder"]: checked(r)
for k, v in B["clocks"].items(): checked(v)
for c in B["corrections"]: checked(c)
for f in B["forecasts"]: checked(f)
for a in B["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in B["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in B["audits"]]
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in B["corrections"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in B["milestones"]]
bs, bc = B["sym"], B["clocks"]
v = lambda k: bs[k]["value"]
out["ladder"] = {   # id, edges tied, label, line ln tau, se, review ln tau, se (, review bracket lo, hi)
    "rows": [[r["id"], r["edges"], r["label"]] + r["value"][:4] + (r["value"][5:7] if len(r["value"]) > 4 else []) for r in bs["ladder"]],
    "per_edge": v("per_edge"), "inversion": [v("inversion")[0], bs["inversion"]["sign"] * v("inversion")[1], v("inversion")[2]], "rotation": v("rotation"),
    "slab": v("slab"), "sixth": v("sixth"), "c": v("sixth_verdict"), "rim": v("rim")[:4] + [-v("rim")[4], -v("rim")[5], -v("rim")[6]],
    "pinned": [-v("pinned")[0], v("pinned")[1], -v("pinned")[2]], "bend": v("bend"), "centring": v("centring"), "centring_rim": v("centring_rim"), "vessel": v("vessel")}
assert bs["ladder"][3]["value"][4] == 35 and bs["inversion"]["sign"] == -1 and bs["rim"]["sign"] == -1 and bs["pinned"]["sign"] == -1
# the compound clock C52.33a, read from the catalogue's own cell file (phase 0, doubled coordinates)
cf = (repo / "research" / "clockwork" / "objects" / "C52.33a.cells").read_text()
assert "period 52" in cf and "union 42" in cf and "cell periods {1: 24, 4: 4, 13: 14}" in cf
out["c52"] = {"cells": [list(map(int, l.split())) for l in cf.splitlines() if l.strip() and not l.startswith("#")], "period": 52, "union": bc["split"]["value"][0],
              "split": {"1": bc["split"]["value"][1], "4": bc["split"]["value"][2], "13": bc["split"]["value"][3]},
              "kinds": bc["kinds"]["value"], "new": bc["new"]["words"], "periods": [9, 9, 11, 13, 52]}
assert all(str(p) in bc["periods"]["quote"] for p in out["c52"]["periods"]) and "periods 9, 9, 11, 13, 52" in bc["periods"]["quote"]


# ---- the third refresh of 2026-11-15: update-2026-11-15c.json (dying faces DY1-DY7; the 4 x 5 patch rerun, GP10; the second card, GL1, GL2) ----
import base64, csv
Y = S("update-2026-11-15c.json")
for sec in ("dying", "patches", "card"):
    for k, v in Y[sec].items(): checked(v)
for c in Y["corrections"]: checked(c)
for f in Y["forecasts"]: checked(f)
for a in Y["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in Y["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in Y["audits"]]
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in Y["corrections"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in Y["milestones"]]
yd, yp, yc = Y["dying"], Y["patches"], Y["card"]
# the 4 x 5 patch: the CPU rerun replaces the first CPU value; second differences from both codes and combined
v = yp["cpu45"]["value"]
out["patches"]["cpu45"] = [60, -v[0], v[1], v[2]]; out["patches"]["comb45"] = [-v[6], v[7]]; out["patches"]["sigma45"] = v[5]
assert out["patches"]["lnp"][5][2] == -v[3] and out["patches"]["se"]["60"] == v[4]
v = yp["small"]["value"]
out["patches"]["cpu_small"] = {"36": [-v[0], v[1]], "48": [-v[4], v[5]]}
assert abs(out["patches"]["lnp"][3][2] + v[2]) < 6e-4 and abs(out["patches"]["lnp"][4][2] + v[6]) < 6e-4   # GPU 3x4, 4x4 as in the first update (rounded there)
v = yp["cost"]["value"]
out["patches"]["cost_cpu"] = [[12, v[0], None], [18, v[1], v[2]], [27, v[3], v[4]], [36, v[5], v[6]]]
out["patches"]["cost_gpu"] = [[12, v[7], None], [18, v[8], None], [27, v[9], None], [36, v[10], v[11]]]
out["patches"]["cost_comb"] = [36, v[12], v[13]]
assert v[10] == out["patches"]["cost"][3][1]
out["patches"]["laws_range"] = yp["withdrawn"]["value"][2:4]; out["patches"]["was"] = yp["withdrawn"]["value"][:2]
out["patches"]["range"] = yp["open"]["value"][2:4]; out["patches"]["extrap"] = yp["open"]["value"][:2]
del out["patches"]["cpu45_cost"]
# the 4 x 4 torus anchor (GL1) and what it moves on the census plate (SH3, SH4)
out["card"] = {"best": yc["best"]["value"], "old": yc["old"]["value"], "codes": yc["codes"]["value"], "sh4": yc["sh4"]["value"]}
assert yc["sh3"]["value"][4] == out["census"]["cost"][5][1] and out["census"]["cost"][5][0] == 16
out["census"]["cost16"] = yc["sh3"]["value"][3]
# dying faces: quoted numbers
out["dying"] = {k: [x * yd[k].get("sign", 1) for x in yd[k]["value"]] for k in yd if "value" in yd[k]}
# ... the study's tables (research/dying/data), drawn as they are; round 3 (r3_*) is not read
dd = repo / "research" / "dying" / "data"
rows = lambda n: list(csv.DictReader(open(dd / n)))
GR = ["c1", "csz", "c2v", "d2h"]
ex = rows("r2_excursions.csv")
out["dying"]["ex"] = {g: [[float(r["p"]), round(float(r["ln_nu"]), 3), float(r["q"])] for r in ex if r["group"] == g] for g in GR}
for g, want in zip(GR, out["dying"]["nu07"][:4]):
    assert round([r[1] for r in out["dying"]["ex"][g] if r[0] == 0.7][0], 2) == want, g
assert round([r[2] for r in out["dying"]["ex"]["c1"] if r[0] == 0.5][0], 4) == out["dying"]["q05"][1]
lag = rows("occupancy_by_lag.csv")
null = {r["group"]: float(r["face_pop"]) for r in lag if r["lag"] == "null"}
out["dying"]["lag"] = {g: [round(float(r["face_pop"]) / null[g], 4) for r in lag if r["group"] == g and r["lag"] != "null" and int(r["lag"]) <= 40] for g in GR}
assert all(len(v) == 41 and v[0] == 0 for v in out["dying"]["lag"].values())
ru = rows("r2_runup.csv")
runup = [[int(r["lag"]), round(float(r["birth_over_stat"]), 3), round(float(r["survival_over_stat"]), 3)] for r in ru if r["group"] == "c1" and int(r["lag"]) <= 40]
assert [[round(x[1], 2), round(x[2], 2)] for x in runup if x[0] == 8][0] == out["dying"]["births"][5:7]   # the table behind the quoted 0.45, 0.88 at lag 8
# ... real deaths recorded for the page (record_deaths.py: research/dying/sd.c, fresh seeds, every frame checked against the oracle)
dj = S("deaths.json")
canon = [tuple(c) for c in dj["canon"]]
oc = rows("occupancy_by_cell.csv")
LAGS = ["null", "lag16", "lag8", "lag4", "lag2", "lag1"]
maps = {}
for g in ("c1", "d2h"):
    byc = {(int(r["x"]), int(r["y"]), int(r["z"])): r for r in oc if r["group"] == g}
    assert set(byc) == set(canon)
    maps[g] = [[round(float(byc[c][k]), 3) for c in canon] for k in LAGS]
out["dying"]["maps"] = {"lags": [None, 16, 8, 4, 2, 1], "c1": maps["c1"], "d2h": maps["d2h"]}
T = dj["T"]
for g, G in dj["groups"].items():
    for L in G["lives"]:
        b = base64.b64decode(L["frames"]); bits = [(b[i >> 3] >> (i & 7)) & 1 for i in range(T * 63)]
        assert not any(bits[(T - 1) * 63:]) and any(bits[(T - 2) * 63:(T - 1) * 63]), "a recorded life must end on its first empty frame"
out["dying"]["films"] = {"T": T, "canon": dj["canon"], "groups": {g: {"tied": G["tied"], "lives": [{"f": L["frames"], "age": L["age"]} for L in G["lives"]]} for g, G in dj["groups"].items()}}


# ---- the refresh of 2026-11-15 (late morning): update-2026-11-15d.json (signals SG1-SG10; state space SS1-SS3;
#      dying faces rounds 3 and 4, DY8-DY15; the five wrapped faces on the owner's card, GL1, GL3) ----
import math
Q = S("update-2026-11-15d.json")
for sec in ("signals", "statespace", "dying", "tori"):
    for k, v in Q[sec].items(): checked(v)
for c in Q["corrections"]: checked(c)
for f in Q["forecasts"]: checked(f)
for a in Q["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["forecasts"] += [{"line": f["line"], "result": f["result"]} for f in Q["forecasts"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in Q["audits"]]
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in Q["corrections"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in Q["milestones"]]
qv = lambda sec, k: Q[sec][k].get("value")
# signals: the three objects drawn live, copied from research/signals/objects (check-signals.js checks them on the page's stepper)
so = lambda n: json.loads((repo / "research" / "signals" / "objects" / (n + ".json")).read_text())
pc, ck, gt = so("pulse-C"), so("clock-C"), so("gate-C")
assert pc["bg"] == ck["unit"] == gt["bg"] and pc["p"] == 2 and pc["s"] == 1 and ck["period"] == "4N + 2"
assert [c["expect"] for c in gt["cases"]] == ["left", "left", "right", "right"] and [c["sep"] % 2 for c in gt["cases"]] == [0, 0, 1, 1]
out["signals"] = {
    "objects": {"pulseC": {k: pc[k] for k in ("v", "bg", "defect")}, "clock": {k: ck[k] for k in ("capL", "unit", "capR", "ignite")},
                "gate": {k: gt[k] for k in ("v", "bg", "right", "left", "T")}},
    "lead_periods": qv("signals", "clock_lead"), "study_N": qv("signals", "clock_study"), "gate_T": qv("signals", "gate_lead")[0],
    "soup": qv("signals", "soup"), "chaos": qv("signals", "chaos"), "isolate": qv("signals", "isolate"), "escape": qv("signals", "escape"),
    "transmission": qv("signals", "transmission")[0], "capacity": qv("signals", "capacity"), "open600": qv("signals", "open600")[0],
    "clock_review": qv("signals", "clock_review"), "soup2": qv("signals", "soup2"), "chaos2": qv("signals", "chaos2")[0], "speed": qv("signals", "speed"), "gap": qv("signals", "gap"), "escape2": qv("signals", "escape2")}
assert out["signals"]["lead_periods"] == [4 * n + 2 for n in (1, 2, 3, 4, 7, 12)]
# state space: quoted numbers, and the study's own tables (research/statespace/data)
sd = repo / "research" / "statespace" / "data"
ves = [json.loads(l) for l in (sd / "vessels.jsonl").read_text().splitlines() if l.strip()]
assert len(ves) == qv("statespace", "listed")[0] and max(r["N"] for r in ves) == qv("statespace", "listed")[1]
v27 = [r for r in ves if r["N"] >= 27]; sm = qv("statespace", "small")
assert len(v27) == sm[0] and [min(r["max_visited"] for r in v27), max(r["max_visited"] for r in v27)] == sm[5:7] and [round(min(r["mean_visited"] for r in v27), 1), round(max(r["mean_visited"] for r in v27), 1)] == sm[3:5]
fl_ = [r for r in csv.DictReader(open(sd / "large_facelaw.csv")) if r["measured"] == "True"]
lc_ = list(csv.DictReader(open(sd / "large_cubes.csv")))
ent = json.loads((sd / "entropy.json").read_text())
s16 = [r for r in lc_ if r["side"] == "16"][0]
assert int(s16["visited"]) == qv("statespace", "side16")[0] and int(s16["hull_cells"]) == qv("statespace", "side16")[2] and round(float(s16["log2_visited"]), 2) == qv("statespace", "side16")[1]
assert all(qv("statespace", "law_range")[0] <= round(float(r["bits_per_face_cell"]), 3) <= qv("statespace", "law_range")[1] for r in fl_)   # measured rows 0.296-0.300; the 0.301 is an extrapolated row
assert ent["top_layer"] == qv("statespace", "entropy")[0] and abs(ent["slab_hi"] - qv("statespace", "entropy")[1]) < 0.002   # the study 0.958, the review 0.9585
out["statespace"] = {k: Q["statespace"][k].get("value") for k in Q["statespace"] if "value" in Q["statespace"][k]}
out["statespace"]["vessels"] = [[r["N"], r["family"], round(math.log2(r["max_visited"]), 3), round(math.log2(r["mean_visited"]), 3), round(math.log2(r["image_t"][1]), 3)] for r in ves]
out["statespace"]["facelaw"] = [[int(r["A"]), float(r["log2_visited"])] for r in fl_]
out["statespace"]["cube_rows"] = [[int(r["side"]), int(r["face_cells_A"]), float(r["bits_per_A_over_7p7"]), int(r["visited"])] for r in lc_]
out["statespace"]["slab_lo"] = ent["slab_lo"]
# dying faces, rounds 3 and 4: quoted numbers, and the company table (research/dying/data/r4_company.csv, the study's) with the
# review's finite-face null (research/audit/dying4/null_r1{1,3,5}.txt, read as research/dying/round4_figure.py reads it)
out["dying"]["r34"] = {k: Q["dying"][k].get("value") for k in Q["dying"] if "value" in Q["dying"][k]}
r4 = [r for r in csv.DictReader(open(dd / "r4_company.csv")) if int(r["n_faces"]) >= 200 and r["kind"] in ("caught", "control")]
comp = {}
for r in r4: comp.setdefault(r["A"] + r["kind"], []).append([float(r["p"]), float(r["C"]), float(r["C_se"])])
for v in comp.values(): v.sort()
assert all(abs(a[1] - b) < 6e-4 for a, b in zip(sorted(comp["108caught"], reverse=True), qv("dying", "company108")))
ratio = lambda A: [x[1] for x in comp[A + "caught"] if x[0] == 0.15][0] / [x[1] for x in comp[A + "caught"] if x[0] == 0.45][0]
assert [round(ratio(A), 2) for A in ("63", "84", "108")] == qv("dying", "ratio")
NULL = {}
for A, fn in ((63, "null_r11.txt"), (84, "null_r13.txt"), (108, "null_r15.txt")):
    cur = levels = None
    for line in open(repo / "research" / "audit" / "dying4" / fn):
        if line.startswith("#"): levels = [float(x) for x in re.findall(r"(0\.\d+):", line)]
        mm = re.match(r"at level\s+p ([\d.]+)", line)
        if mm: cur = float(mm.group(1)); continue
        mm = re.match(r"\s+null p_t ([\d.]+): C ([\d.]+) V ([\d.]+)", line)
        if mm:
            if cur is None or (A, cur) in NULL and len(NULL[(A, cur)]) == 4: cur = [q for q in levels if (A, q) not in NULL][0]
            NULL.setdefault((A, cur), []).append(float(mm.group(2)))
assert all(len(v) == 4 for v in NULL.values())
out["dying"]["company"] = {A: {"caught": comp[A + "caught"], "control": comp[A + "control"],
                               "null": sorted([p, min(v), max(v)] for (AA, p), v in NULL.items() if str(AA) == A)} for A in ("63", "84", "108")}
nr = lambda A: [min(NULL[(A, 0.15)][i] / NULL[(A, 0.45)][i] for i in range(4)), max(NULL[(A, 0.15)][i] / NULL[(A, 0.45)][i] for i in range(4))]
assert [round(x, 2) for A in (63, 84, 108) for x in nr(A)] == qv("dying", "null")[:6]   # the review's 0.45-0.48, 0.58-0.61, 0.65-0.69
# the five wrapped faces (GL1, GL3): A, ln tau, se
t = Q["tori"]; v = t["t57_75"]["value"]
out["tori"] = {"rows": [[48] + t["t48"]["value"], [57, v[1], v[2]], [63, v[4], v[5]], [75, v[7], v[8]], [93] + t["t93"]["value"][:2]],
               "line": t["line"]["value"][:2], "deficit": [[48, t["line"]["value"][2]], [57, t["line"]["value"][4]]], "slope": t["slope"]["value"], "kink": t["kink"]["value"][0],
               "chi": t["nosmooth"]["value"], "f63": t["f63"]["value"], "f93": t["f93"]["value"], "next": t["next"]["value"], "hull": t["hull"]["value"], "two": t["two"]["value"]}
# ---- the refresh of 2026-11-15 (afternoon; the site's phase 2): update-2026-11-15e.json. The nine wrapped faces reviewed
#      (GL3), the wrapping law tested (WL1-WL3), the third and fourth signals pushes (SG12, SG14, SG16-SG19, SG22) ----
V = S("update-2026-11-15e.json")
for sec in ("tori", "wrap", "signals4"):
    for k, v in V[sec].items():
        if k != "measured84": checked(v)
for c in V["corrections"]: checked(c)
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in V["corrections"]]
vv = lambda sec, k: V[sec][k].get("value")
# the nine wrapped faces on the owner's card, recomputed from the rows: ln tau_face = ln(2 sum exposure / sum face), error
# 1 / sqrt(sum face) (as research/audit/wrap_haz_lead.py and the reviews compute them); checked against CLAIMS GL3
nine = []
for f in sorted((repo / "research" / "data" / "gpu_local_eqtorus").glob("eqtorus_*.csv")):
    rs = list(csv.DictReader(open(f)))
    E_, F_ = sum(int(r["exposure"]) for r in rs), sum(int(r["face"]) for r in rs)
    nine.append([int(rs[0]["A"]), round(math.log(2 * E_ / F_), 4), round(F_ ** -0.5, 4), len(rs)])
nine.sort()
assert [r[0] for r in nine] == [48, 57, 63, 75, 81, 84, 93, 108, 111], nine
quoted = {48: t["t48"]["value"], 57: vv("tori", "t57"), 63: t["t57_75"]["value"][4:6], 75: t["t57_75"]["value"][7:9], 93: t["t93"]["value"][:2]}
nv = vv("tori", "nine"); quoted.update({81: nv[0:2], 84: [nv[3], nv[1]], 108: nv[5:7], 111: nv[8:10]})
for A_, y_, se_, _ in nine:
    assert abs(y_ - quoted[A_][0]) < 1.5e-4 and abs(se_ - quoted[A_][1]) < 1.5e-4, (A_, y_, se_, quoted[A_])
l7 = vv("tori", "line7")
out["tori"] = {"rows": nine, "line63": [l7[2], l7[3]], "deficit": [[48, l7[7]], [57, l7[8]]], "chi7": l7[4],
               "slope": [l7[3], 0.00009], "price": vv("tori", "price"), "smooth": vv("tori", "smooth"), "kink": vv("tori", "kink")[0],
               "scatter": vv("tori", "scatter"), "second81": vv("tori", "second81"), "low4": V["tori"]["low4"]["value"],
               "five": t["line"]["value"][:2], "next": t["next"]["value"], "f63": t["f63"]["value"], "f93": t["f93"]["value"],
               "hull": t["hull"]["value"], "two": t["two"]["value"]}
assert "0.20867(9)" in V["tori"]["line7"]["quote"]
# a short way round (WL1-WL3): the faces and frozen forms of the lead's refit (sources/wrap.json, written by
# sources/scripts/wrap.py from research/audit/wrap_haz_lead.py), the quoted numbers, and the card's 84-cell face when measured
wj = S("wrap.json")
assert [round(x, 3) for x in (wj["line0"]["c"],)] == [0.209] and abs(wj["line0"]["c"] - vv("wrap", "noloop")[3]) < 0.0002
fz = wj["frozen"]
src84 = "research/audit/wrap_haz_lead.py --predict 1 12 28"
f84 = vv("wrap", "forecast84")
m84 = V["wrap"]["measured84"]
if m84.get("value") is not None:
    checked({"value": [m84["value"], m84["se"]], "quote": m84["quote"]})
    f84r = [f for f in wj["faces"] if f[0] == 84 and f[1] == 12]
    assert len(f84r) == 1 and abs(f84r[0][2] - m84["value"]) < 1e-4 and abs(f84r[0][3] - m84["se"]) < 1e-4, f84r
tq = vv("wrap", "tubes")
assert [wj["tubes"][k]["c"] for k in ("12", "13", "16", "none")] == tq[0::2] and [wj["tubes"][k]["se_c"] for k in ("12", "13", "16", "none")] == tq[1::2], wj["tubes"]
out["wrap"] = {"faces": wj["faces"], "line0": wj["line0"], "frozen": {k: fz[k] for k in ("LINES", "POW", "HAZ")},
               "discount": vv("wrap", "discount"), "noloop": vv("wrap", "noloop"), "loop12": vv("wrap", "loop12"), "law11": vv("wrap", "law11"),
               "forecast84": {"A": f84[0], "law": f84[1], "LINES": f84[2], "POW": f84[3], "HAZ": f84[4], "src": src84},
               "measured84": {"value": m84.get("value"), "se": m84.get("se"), "deaths": m84.get("deaths"), "src": m84.get("src")},
               "tubes": wj["tubes"], "scored84": vv("wrap", "scored84"), "percent": vv("wrap", "percent"),
               "next": [vv("wrap", "next96"), vv("wrap", "next108")]}
# the frozen parameters must give the quoted forecasts at 84 cells, one loop of 12 (the plate draws the curves from them)
L_, P_, H_ = fz["LINES"], fz["POW"], fz["HAZ"]
assert abs(L_["a"] + L_["c"] * 21 - L_["k"][0] * (84 - L_["z"][0]) - f84[2]) < 2e-4
assert abs(P_["a"] + P_["c"] * 21 - math.log1p(P_["r"][0] * (84 / 63) ** P_["m"][0]) - f84[3]) < 2e-4
assert abs(H_["a"] + H_["c"] * 21 - math.log1p(H_["r"][0] * math.exp(H_["g"][0] * 21)) - f84[4]) < 2e-4
# the fourth signals push: the line and the divider, copied from research/signals/objects (CLAIMS SG16-SG19)
sob = lambda n: json.loads((repo / "research" / "signals" / "objects" / (n + ".json")).read_text())
lc, dv = sob("line-C"), sob("divider-C8")
assert lc["capA"] == dv["capA"] and lc["unit"] == dv["unit"] and lc["gun"] == dv["gun"] and len(lc["gun"]) == vv("signals4", "gun")[0]
assert len(dv["osc"]) == 24
out["signals4"] = {"objects": {"line": {k: lc[k] for k in ("v", "capA", "unit", "gun")}, "divider": {k: dv[k] for k in ("v", "capA", "unit", "gun", "osc")}},
                   "gun": vv("signals4", "gun"), "line": vv("signals4", "line"), "divider": [24, 8, 3], "stroke": vv("signals4", "stroke"), "heal": vv("signals4", "heal")}

# ---- the refresh of 2026-11-15 (evening): update-2026-11-15f.json. Why a tube is cheaper (WL4-WL6, the forecast W13); the
#      fifth signals push and its review (SG23-SG27: no listener, four kinds of end, the echo) ----
F = S("update-2026-11-15f.json")
for sec in ("dens", "ends", "echo"):
    for k, v in F[sec].items():
        if k not in ("w13measured", "cells"): checked(v)
for c in F["corrections"]: checked(c)
for a in F["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in F["corrections"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in F["audits"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in F["milestones"]]
fv = lambda sec, k: F[sec][k].get("value")
# the density deficit per loop length with its error, read from the study's output (dens.py rho_face --price) and checked
# against the notebook's quote; loops² 9 to 28 (31 and up are not resolved, 37 comes out negative)
dtxt = (repo / "research" / "wraplocal" / "data" / "dens_rho_face.txt").read_text()
fq = {int(m[1]): [float(m[2]), float(m[3])] for m in re.finditer(r"f\(\s*(\d+)\) = \+?(-?[\d.]+) ± ([\d.]+)", dtxt)}
qf = fv("dens", "f"); quotedf = {9: qf[1], 12: qf[3], 13: qf[5], 16: qf[7], 19: qf[9], 21: qf[11], 25: qf[13], 27: qf[16], 28: qf[16]}
assert all(abs(fq[q][0] - x) <= 2e-6 for q, x in quotedf.items()), fq
assert all(4e-6 <= fq[q][1] <= 19e-6 for q in quotedf), "errors 4 to 19 × 10⁻⁶"
mm = re.search(r"s_inf = ([\d.]+) ± ([\d.]+)", dtxt); assert [float(mm[1]), float(mm[2])] == fv("dens", "rhoinf")
mm = re.search(r"kappa = ([\d.]+) ± ([\d.]+)", dtxt); assert abs(float(mm[1]) - fv("dens", "kappa")[0]) < 0.005 and abs(float(mm[2]) - fv("dens", "kappa")[1]) < 0.005
w13m = F["dens"]["w13measured"]
if w13m.get("value") is not None:
    checked({"value": [w13m["value"], w13m["se"]], "quote": w13m["quote"], **({"file": w13m["file"]} if "file" in w13m else {})})
out["dens"] = {"rhoinf": fv("dens", "rhoinf"), "f": [[q, round(math.sqrt(q), 4)] + fq[q] for q in sorted(quotedf)], "fit": fv("dens", "fit"), "percell": fv("dens", "percell"), "f21": fv("dens", "f21")[0],
               "kappa": fv("dens", "kappa")[:2], "f13": fv("dens", "f13"), "disc": [fv("dens", k) for k in ("d12", "d13", "d16", "d19")],
               "lead": {"tori": F["dens"]["lead"]["tori"], "rows": [fv("dens", "lead")[3 * i: 3 * i + 3] for i in range(5)], "within": fv("dens", "lead")[15]},
               "leaddef": fv("dens", "leaddef"), "lead21": fv("dens", "lead21"), "noloop": fv("dens", "noloop"),
               "w13": fv("dens", "w13"), "w13eq": fv("dens", "w13eq"), "w13p": fv("dens", "w13p"),
               "w13measured": {"value": w13m.get("value"), "se": w13m.get("se"), "src": w13m.get("src")}, "firewalls": fv("dens", "firewalls")}
assert [d[0] for d in out["dens"]["disc"]] == [12, 13, 16, 19] and out["dens"]["f13"][3:5] == out["dens"]["disc"][1][1:3]
# the ends of the stream (SG23-SG25, SG27)
out["ends"] = {k: fv("ends", k) for k in ("sat", "limits", "census", "holes", "oracle", "four", "lead124", "events", "beside", "divbeside", "pushes")}
assert sum(out["ends"]["four"]) == out["ends"]["census"][0] == out["ends"]["holes"][0] + out["ends"]["holes"][2]
fo = out["ends"]["four"]; assert fo[0] + fo[1] == out["ends"]["holes"][0] and fo[2] + fo[3] == out["ends"]["holes"][2]   # healed by a hole: 113 + 486
assert out["ends"]["events"][1] == out["ends"]["events"][0] * out["ends"]["census"][0]
# the echo (SG26): the initial cells of research/audit/signals5/end_echo.json, first record, drawn live on the page and
# checked by site/checks/check-signals.js; the quoted counts
ee = json.loads((repo / "research" / "audit" / "signals5" / "end_echo.json").read_text())[0]
assert ee["osc"] == "C18.23a" and ee["gap_k"] == 0 and ee["tg"] == 45 and len(ee["oscillator"]) == 24
lce = so("line-C"); assert len(lce["gun"]) == 15
out["echo"] = {"osc": ee["osc"], "line": ee["line"], "oscillator": ee["oscillator"], "tg": ee["tg"], "hole": ee["hole"], "N": 12,
               "found": fv("echo", "found"), "deaths": fv("echo", "deaths")}

# ---- the refresh of 2026-11-15 (night): update-2026-11-15g.json. The sixth signals push and its review (SG28-SG32: nine
#      signals, the meetings, no gun survives an echo, the reflector works once, the events review 5 had not followed) ----
G = S("update-2026-11-15g.json")
for sec in ("meet", "echo6", "ends6"):
    for k, v in G[sec].items():
        if k not in ("train", "signals"): checked(v)
for c in G["corrections"]: checked(c)
for a in G["audits"]: assert (repo / a["file"]).exists(), a["file"]
out["corrections"] += [{"said": c["said"], "now": c["now"], "by": c["by"], "who": who(c["by"]), "line": c["line"]} for c in G["corrections"]]
out["project"]["audits"] += [[a["label"], a["line"]] for a in G["audits"]]
tl["milestones"] += [{"date": x["date"], "text": x["text"]} for x in G["milestones"]]
gv = lambda sec, k: G[sec][k].get("value")
# the plain rake train and the four signals of the push (research/signals/objects/echo-train.json), and the nine signals of
# the review (research/audit/signals6/sig6.py, the literal SIGS, read with ast; the four must be the train file's)
import ast
et = so("echo-train")
sg6 = next(ast.literal_eval(n.value) for n in ast.parse((repo / "research" / "audit" / "signals6" / "sig6.py").read_text()).body
           if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SIGS")
assert list(sg6) == ["E", "U", "H", "K0", "K3", "N1", "N2", "N3", "N4"]
for k in ("E", "U", "H", "K0"):
    assert sg6[k][0] == et["sig"][k]["parity"] and sorted(map(list, sg6[k][1])) == sorted(et["sig"][k]["cells"]) and sg6[k][2] == et["sig"][k]["dir"], k
assert sum(1 for v in sg6.values() if v[2] > 0) == 3 and sum(1 for v in sg6.values() if v[2] < 0) == 6   # "six down and three up"
fl6 = gv("meet", "flips"); assert fl6[0] == fl6[1] + fl6[2] + fl6[3]
made = {"E": "one cell flipped", "U": "one cell flipped", "H": "one cell flipped", "K0": "one cell flipped", "K3": "two cells flipped",
        "N1": "two cells flipped", "N2": "two cells flipped", "N3": "two cells flipped", "N4": "one cell flipped just outside the tube"}   # REVIEW-signals-6 section 2, "made by"
out["meet"] = {"v": et["v"], "unit": et["unit"], "base": et["base"], "wireB": et["wireB"],
               "sig": {k: {"parity": v[0], "cells": [list(c) for c in v[1]], "dir": v[2], "made": made[k], "push": k in et["sig"]} for k, v in sg6.items()},
               "flips": fl6, "offsets": gv("meet", "offsets"), "lead": gv("meet", "lead"), "steppers": gv("meet", "steppers")[0]}
# the echo plate's result (SG30, SG31) and the ends plate's additions (SG32; the forecasts after six pushes)
out["echo"]["sixth"] = {"guns": gv("echo6", "guns"), "sat": gv("echo6", "sat"), "once": gv("echo6", "once")}
fw = gv("ends6", "followed"); assert fw[0] == fw[2] + fw[3]
rw = gv("ends6", "rows"); assert rw[0] == out["ends"]["census"][0] and rw[1] == fw[2] * rw[0] and rw[2] == fw[3] * rw[0]   # 14 × 741, 2 × 741
assert gv("ends6", "all")[0] == out["ends"]["events"][0]
pz = gv("ends6", "pushes"); assert pz[0] == pz[1] + pz[2]
out["ends"].update({"followed": fw, "rows": rw, "count": gv("ends6", "count"), "pushes": pz})

# the footer's date: the newest date among the files the data were gathered into (update-<date>*.json); the stamp under it
# gives the repository state the timeline was read from
out["project"]["gathered"] = max(re.match(r"update-(\d{4}-\d\d-\d\d)", f.name).group(1) for f in (here / "sources").glob("update-*.json"))

# one file per key: a page of the site fetches only the keys its plates read (site/build.py finds them). A key that
# is no longer produced leaves its old file behind on purpose: delete it by hand once no plate reads it.
dd_out = here.parent / "data"
for k, v in out.items():
    (dd_out / (k + ".json")).write_text(json.dumps(v, separators=(",", ":")) + "\n")
print(f"{len(out)} files in site/data/, {sum((dd_out / (k + '.json')).stat().st_size for k in out)} bytes;", ", ".join(out))
