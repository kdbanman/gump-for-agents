#!/usr/bin/env python3
"""The packed / checkpoint-hash ensemble engine must give the same summaries as the
per-generation engine (--per-gen-hash), field for field except timing.

  check_ensemble.py [--gump PATH] [--quick]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUMP = os.path.join(HERE, "..", "target", "release", "gump")
TIMING = {"elapsed_s", "gens_per_s", "cell_updates_per_s", "threads"}

CASES = [
    "--soup 0.3 --radius 6 --vary radius=6,8,10 --runs 60 --gens 20000",
    "--soup 0.3 --radius 12 --runs 12 --gens 3000",          # many runs hit the cap: closing check
    "--soup 0.35 --radius 8 --vary density=0.2,0.35,0.5 --runs 20 --gens 5000 --rule B45/S2345",
    "--soup 0.3 --radius 9 --runs 30 --gens 4000 --rule B4/S34",
    "--soup 0.3 --half 7 --runs 30 --gens 4000",
    "--soup 0.3 --torus 6 --runs 40 --gens 3000",
    "--soup 0.4 --torus 8 --slab-layers 3 --runs 30 --gens 3000",
    "--soup 0.3 --torus 5,7,9 --runs 20 --gens 2000 --rule B35/S236",
    "--cube 9 --runs 2",
    "--soup 0.3 --torus 4 --runs 80 --gens 3000",
    "--soup 0.25 --torus 3,4,5 --runs 80 --gens 3000 --rule B4/S345",
    "--soup 0.3 --radius 8 --runs 300 --gens 120",              # caps right after cycles close
    "--soup 0.3 --radius 8 --runs 300 --gens 120 --check-every 1",
    "--soup 0.3 --radius 10 --runs 16 --gens 30000 --check-every 7",
]


def run(args):
    out = subprocess.run([GUMP, "ensemble", *args], check=True, capture_output=True, text=True).stdout
    rows = [json.loads(l) for l in out.splitlines()]
    summ = {d["run"]: d for d in rows if d["type"] == "summary"}
    tail = [d for d in rows if d["type"] == "ensemble_summary"][0]
    return summ, tail


def main():
    global GUMP
    a = sys.argv[1:]
    if a[:1] == ["--gump"]:
        GUMP, a = a[1], a[2:]
    cases = CASES[:4] if "--quick" in a else CASES
    bad = 0
    for c in cases:
        args = c.split()
        new, tn = run(args)
        old, to = run(args + ["--per-gen-hash"])
        diffs = []
        for k in sorted(old):
            o, n = old[k], new[k]
            for f in o:
                if f not in TIMING and o[f] != n.get(f):
                    diffs.append((k, f, o[f], n.get(f)))
        st = {}
        for d in old.values():
            st[d["status"]] = st.get(d["status"], 0) + 1
        r = {"case": c, "runs": len(old), "statuses": st, "mismatches": len(diffs), "first": diffs[:3],
             "speedup": round(to["elapsed_s"] / tn["elapsed_s"], 2)}
        print(json.dumps(r), flush=True)
        bad += bool(diffs) or len(old) != len(new)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
