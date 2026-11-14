"""recount.py -- recount the headline tallies of class.md from the author's committed data files.

    python3 recount.py

Reads research/theory/class/data/scan_table.md (every cap of every family: torus class, verdict) and
data/faces.tsv (every slab run).  Applies the scoring rule fixed in PREDICTIONS.md:
  face law = ln tau rises by >= 1.0 over the sizes, >= 20 deaths at two or more sizes, CV in [0.8, 1.25]
  (CV judged where there are >= 50 deaths, as class.md S1 says).
"""
import collections, os, re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory", "class", "data")


def rule_name(b, c, K):
    f = lambda s: "".join(str(k) if k < 10 else f"({k})" for k in s)
    return f"B{f(range(b, min(c, K + 1)))}/S{f(range(b - 1, min(c, K + 1)))}"


# ---- scan table
fam = {}
rows = []
cur = None
for l in open(os.path.join(D, "scan_table.md")):
    m = re.match(r"### (\w+): K=(\d+) b=(\d+) a0=(\d+) a-=(\d+) K_f=(\d+)", l)
    if m:
        cur = m.group(1)
        fam[cur] = dict(K=int(m.group(2)), b=int(m.group(3)), a0=int(m.group(4)), am=int(m.group(5)), Kf=int(m.group(6)))
        continue
    if l.startswith("|") and not l.startswith("| c") and not l.startswith("|---"):
        cols = [c.strip() for c in l.strip().strip("|").split("|")]
        rows.append(dict(lat=cur, c=int(cols[0]), torus=cols[2], rho=cols[3], sizes=cols[6], verdict=cols[7]))

# ---- slab runs
runs = collections.defaultdict(dict)       # (lattice, rule, u) -> A -> best run (most deaths)
hdr = None
for l in open(os.path.join(D, "faces.tsv")):
    f = l.rstrip("\n").split("\t")
    if hdr is None:
        hdr = f
        continue
    r = dict(zip(hdr, f))
    if r["lntau"] in ("None", ""):
        continue
    key = (r["lattice"], r["rule"], r["u"])
    A = int(r["A"])
    rec = dict(deaths=int(r["face"]), lntau=float(r["lntau"]), cv=None if r["cv"] in ("None", "") else float(r["cv"]),
               seal=int(r["seal"]), settle=int(r["settle"]))
    if A not in runs[key] or rec["deaths"] > runs[key][A]["deaths"]:
        runs[key][A] = rec


def face_law(lat, rule):
    """Best verdict over face orientations: (has law, detail string)."""
    best = (False, "no slab run with deaths")
    for (l, r, u), byA in runs.items():
        if l != lat or r != rule:
            continue
        good = sorted(A for A in byA if byA[A]["deaths"] >= 20)
        if len(good) < 2:
            d = f"deaths >= 20 at {len(good)} size(s) only: " + ", ".join(f"A={A}: {byA[A]['deaths']}" for A in sorted(byA))
            if not best[0]:
                best = (False, d)
            continue
        rise = byA[good[-1]]["lntau"] - byA[good[0]]["lntau"]
        cvs = [byA[A]["cv"] for A in good if byA[A]["deaths"] >= 50 and byA[A]["cv"] is not None]
        cv_ok = all(0.8 <= c <= 1.25 for c in cvs)
        slope = rise / (good[-1] - good[0])
        d = f"A={good[0]}..{good[-1]}: ln tau {byA[good[0]]['lntau']:.2f} -> {byA[good[-1]]['lntau']:.2f}, slope {slope:.3f}, CV {min(cvs) if cvs else '-'}..{max(cvs) if cvs else '-'}"
        ok = rise >= 1.0 and cv_ok
        if ok or not best[0]:
            best = (ok, d)
        if ok:
            break
    return best


print("== S1: pairs the scan calls chaotic on the torus with the cap within reach (c <= K_f)")
inreach = [r for r in rows if r["torus"] == "chaos" and r["c"] <= fam[r["lat"]]["Kf"]]
n_law = 0
fails = []
for r in inreach:
    F = fam[r["lat"]]
    ok, d = face_law(r["lat"], rule_name(F["b"], r["c"], F["K"]))
    n_law += ok
    if not ok:
        fails.append((r["lat"], r["c"], r["verdict"], d))
print(f"   pairs: {len(inreach)}; with a face law by the fixed scoring rule: {n_law}; without: {len(fails)}")
for f in fails:
    print(f"      no law: {f[0]} c={f[1]}  scan verdict '{f[2]}'  [{f[3]}]")
bylat = collections.Counter(r["lat"] for r in inreach)
print("   by family: " + ", ".join(f"{k} {v}" for k, v in bylat.items()))

print("== N3: pairs beyond reach (c >= K_f + 1) with a0 >= b - 1")
beyond = [r for r in rows if r["c"] >= fam[r["lat"]]["Kf"] + 1 and fam[r["lat"]]["a0"] >= fam[r["lat"]]["b"] - 1]
vc = collections.Counter(r["verdict"] for r in beyond)
print(f"   pairs scanned: {len(beyond)} in {len({r['lat'] for r in beyond})} families; verdicts: {dict(vc)}")
alive = [r for r in beyond if "none survive burn-in" not in r["sizes"] or r["verdict"] == "WALL"]
print(f"   with anything alive after the burn-in: {len(alive)} in {len({r['lat'] for r in alive})} families; "
      f"WALL: {sum(r['verdict'] == 'WALL' for r in alive)}; other: "
      f"{[(r['lat'], r['c'], r['verdict']) for r in alive if r['verdict'] != 'WALL']}")
# any face death at all recorded in a WALL row?
bad = []
for r in beyond:
    for m in re.finditer(r"A=(\d+): (\d+)/(\d+)/(\d+)", r["sizes"]):
        if int(m.group(2)) > 0:
            bad.append((r["lat"], r["c"], m.group(0)))
print(f"   face deaths recorded in any of these rows: {bad if bad else 'none'}")
rf = []
for r in beyond:
    if r["verdict"] == "WALL":
        rf += [float(x) for x in re.findall(r"ρ_f ([0-9.]+)", r["sizes"])]
print(f"   boundary-layer density in WALL rows: min {min(rf):.2f}, max {max(rf):.2f} over {len(rf)} slab runs")
print("   beyond reach with a0 < b - 1 (not covered by the wall corollary):")
for r in rows:
    F = fam[r["lat"]]
    if r["c"] >= F["Kf"] + 1 and F["a0"] < F["b"] - 1 and r["torus"] in ("chaos", "glass"):
        ok, d = face_law(r["lat"], rule_name(F["b"], r["c"], F["K"]))
        print(f"      {r['lat']} c={r['c']} torus {r['torus']}: verdict '{r['verdict']}'; face law by the rule: {ok} [{d}]")

print("== sigma = K_f * rho / b for every in-reach chaotic pair, against the measured slope")
tab = []
for r in inreach:
    F = fam[r["lat"]]
    ok, d = face_law(r["lat"], rule_name(F["b"], r["c"], F["K"]))
    m = re.search(r"slope ([0-9.\-]+)", d)
    try:
        sig = F["Kf"] * float(r["rho"]) / F["b"]
    except ValueError:
        continue
    tab.append((sig, r["lat"], r["c"], float(m.group(1)) if m else None, ok))
tab.sort()
for sig, lat, c, sl, ok in tab:
    print(f"   sigma {sig:.2f}  {lat:9s} c={c:2d}  slope {'none' if sl is None else format(sl, '.3f')}  {'law' if ok else 'NO LAW'}")

print("== N3, the 38 again: boundary density in every slab run of every one of them")
lo = []
for r in alive:
    vals = [float(x) for x in re.findall(r"ρ_f ([0-9.]+)", r["sizes"])]
    lo.append((min(vals) if vals else None, r["lat"], r["c"], r["torus"], r["verdict"]))
print("   rows with a boundary density below 0.99 or missing: "
      f"{[x for x in lo if x[0] is None or x[0] < 0.99] or 'none'}")
print(f"   torus class of the 38: {dict(collections.Counter(x[3] for x in lo))}; "
      f"scan verdict: {dict(collections.Counter(x[4] for x in lo))}")
