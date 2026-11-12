#!/usr/bin/env python3
"""Ensemble `--layer-deaths all` (packed lanes, exact re-simulated windows) must list the
same layer deaths as `gump run --events F --every 1` (every generation), run by run.

  check_deaths.py [--gump PATH]
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUMP = os.path.join(HERE, "..", "target", "release", "gump")
CASES = [  # (seed args, runs, cap)
    ("--soup 0.35 --radius 9", 24, 20000),
    ("--soup 0.3 --radius 13", 8, 6000),
    ("--soup 0.4 --torus 10 --slab-layers 3", 12, 3000),
    ("--soup 0.3 --half 6", 12, 4000),
    ("--cube 9", 1, 1000),
]


def main():
    global GUMP
    if sys.argv[1:2] == ["--gump"]:
        GUMP = sys.argv[2]
    bad = 0
    for args, runs, cap in CASES:
        a = args.split()
        out = subprocess.run([GUMP, "ensemble", *a, "--runs", str(runs), "--gens", str(cap), "--rng", "500",
                              "--layer-deaths", "all"], check=True, capture_output=True, text=True).stdout
        ens = {d["rng"]: d for d in map(json.loads, out.splitlines()) if d["type"] == "summary"}
        mism, nev = 0, 0
        for rng, d in sorted(ens.items()):
            with tempfile.NamedTemporaryFile(suffix=".jsonl") as f:
                extra = [] if "--cube" in a else ["--rng", str(rng)]
                subprocess.run([GUMP, "run", *a, *extra, "--gens", str(cap), "--events", f.name, "--every", "1",
                                "--out", "/dev/null"], check=True, capture_output=True)
                want = [(e["gen"], e["axis"], e["s"], e["cause"]) for e in map(json.loads, open(f.name))]
            got = [(e["gen"], e["axis"], e["s"], e["cause"]) for e in d["layer_deaths"]]
            nev += len(want)
            if sorted(got) != sorted(want):
                mism += 1
                if mism == 1:
                    print("  first mismatch rng", rng, sorted(set(got) ^ set(want))[:5])
        print(json.dumps({"case": args, "runs": len(ens), "events": nev, "mismatching_runs": mism}), flush=True)
        bad += mism
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
