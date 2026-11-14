#!/usr/bin/env python3
"""Pick what the figures need out of data/sources/*.json into data/data.json.   python3 docs/overview/collect.py
The source files were gathered from the repository by helper agents on 2026-11-14 and carry their own
"src" and "how" fields; this script only selects and reshapes, it does not compute results."""
import json, pathlib
here = pathlib.Path(__file__).parent
S = lambda n: json.loads((here / "data" / "sources" / n).read_text())
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
    assert q in corpus, "quote not found in NOTEBOOK.md or CLAIMS.md: " + q[:80]
    for w in item.get("words", []): assert w in q, (w, q)
    for e in item.get("pow10", []): assert "10" + "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] for c in str(e)) in q, (e, q[:80])
    if "words" not in item:
        for v in item.get("value", []):
            forms = {str(v), format(v, ","), ("%g" % v)}
            assert any(f in q for f in forms), ("number not in its quote", v, q[:80])
    return item
U = S("update-2026-11-14.json")
for sec in ("face12e", "gpu", "noise", "swarm"):
    for k, v in U[sec].items(): checked(v)
for k in ("bond10", "bond10_columns", "oos_escapes", "law_cases"): checked(U["family"][k])
for r in U["family"]["rows"]: checked(r)
for a in U["audits"]: assert (repo / a["file"]).exists(), a["file"]
fe, gp, no, sw = U["face12e"], U["gpu"], U["noise"], U["swarm"]
out["face12e"] = {"box": list(zip(fe["box_life"]["n"], fe["box_life"]["value"])) + [[7, fe["box7"]["value"][0] * 1e8]],
                  "box7": fe["box7_count"]["value"], "sym": list(zip(fe["sym_life"]["n"], fe["sym_life"]["value"])),
                  "wall": [list(r) for r in zip(fe["wall"]["A"], fe["wall"]["value"], fe["wall"]["se"])], "slope": fe["wall_slope"]["value"],
                  "torus": fe["torus"]["value"], "symfactor": fe["sym_factor"]["value"][0], "layers": fe["layers"]["value"], "gen1": fe["cube_gen1"]["value"]}
out["family"] = {"rows": [{k: r[k] for k in ("name", "rule", "lattice", "hull", "law", "note", "status")} for r in U["family"]["rows"]],
                 "bond10": U["family"]["bond10"]["value"], "columns": U["family"]["bond10_columns"]["value"], "oos": U["family"]["oos_escapes"]["value"], "cases": U["family"]["law_cases"]["value"]}
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
tl["milestones"] = tl["milestones"] + [{"date": x["date"], "text": x["text"]} for x in U["milestones"]]

(here / "data" / "data.json").write_text(json.dumps(out, separators=(",", ":")))
print("data.json", (here / "data" / "data.json").stat().st_size, "bytes;", ", ".join(out))
