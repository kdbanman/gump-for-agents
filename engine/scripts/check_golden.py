#!/usr/bin/env python3
"""Check `gump` against the original's population logs, every generation.

  check_golden.py [--gump PATH] [LOG H ...]

Default: the four golden logs in reference/golden/ (sides 8-11). Runs each legacy cube
in open space (box = its diagonal hull, exact for infinite space by T2) and, for even H,
also on the legacy torus of H/2 cubes. Line 0 of a legacy log is "0 0" (seed population
never recorded); lines g >= 1 are compared. Prints one JSON line per check; exit 1 on any
mismatch.
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GUMP = os.path.join(ROOT, "engine", "target", "release", "gump")


def read_log(path):
    pops = []
    with open(path) as f:
        for line in f:
            if line.strip():
                g, p = line.split()
                assert int(g) == len(pops)
                pops.append(int(p))
    return pops


def run(args, gens, tmp):
    log = os.path.join(tmp, "pop.txt")
    cmd = [GUMP, "run", *args, "--gens", str(gens), "--no-halt", "--poplog", log]
    out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    summary = json.loads(out.strip().splitlines()[-1])
    return read_log(log), summary


def compare(name, ref, got):
    n = len(ref) - 1
    first = next((g for g in range(1, n + 1) if got[g] != ref[g]), None)
    return {"check": name, "gens": n, "ok": first is None, "first_mismatch": first,
            "ref": None if first is None else ref[first], "got": None if first is None else got[first]}


def main():
    argv = sys.argv[1:]
    global GUMP
    if argv[:1] == ["--gump"]:
        GUMP, argv = argv[1], argv[2:]
    if argv:
        cases = [(argv[i], int(argv[i + 1])) for i in range(0, len(argv), 2)]
    else:
        gd = os.path.join(ROOT, "reference", "golden")
        cases = []
        for f in sorted(os.listdir(gd)):
            m = re.match(r"legacy_cube_side\d+_H(\d+)\.txt", f)
            if m:
                cases.append((os.path.join(gd, f), int(m.group(1))))
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for path, H in cases:
            ref = read_log(path)
            n = len(ref) - 1
            checks = [("open", ["--legacy-cube", str(H)])]
            if H % 2 == 0:
                checks.append((f"torus{H // 2}", ["--legacy-cube", str(H), "--torus", str(H // 2), "--origin", "0,0,0"]))
            for kind, args in checks:
                got, summ = run(args, n, tmp)
                r = compare(f"{os.path.basename(path)} {kind}", ref, got)
                r["elapsed_s"] = summ["elapsed_s"]
                print(json.dumps(r), flush=True)
                bad += not r["ok"]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
