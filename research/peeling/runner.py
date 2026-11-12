#!/usr/bin/env python3
"""Run many independent `gump run`s with layer-death events; one JSON line per run.

Usage: runner.py OUT.jsonl --rngs A:B [--jobs 2] [--every K] [--gens CAP] -- <gump run args>
The gump args must not contain --rng/--events/--every/--gens/--out (added here).
A literal {rng} in the gump args is replaced by the run's seed (e.g. for --cells files).
Each output line: {"rng", "args", "status", "gen", "pop", "events": [[gen, last_alive, axis, s, cause], ...]}
(gen-0 events, i.e. layers dead in the seed, are dropped). Runs already in OUT are skipped,
so an interrupted sweep can be resumed. Runs reaching CAP have status "running" = censored.
"""
import json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

G = os.path.join(os.path.dirname(__file__), "..", "..", "engine", "target", "release", "gump")


def one(args, rng, every, gens, tmp):
    ev = os.path.join(tmp, f"ev{rng}.jsonl")
    a = [x.replace("{rng}", str(rng)) for x in args]
    cmd = [G, "run", *a, "--rng", str(rng), "--events", ev, "--every", str(every),
           "--gens", str(gens), "--out", "/dev/null", "--hash-window", "65536"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    s = json.loads(out.strip().splitlines()[-1])
    evs = []
    if os.path.exists(ev):
        for line in open(ev):
            e = json.loads(line)
            if e["gen"] > 0:
                evs.append([e["gen"], e["last_alive"], e["axis"], e["s"], e["cause"][0]])
        os.remove(ev)
    return {"rng": rng, "args": " ".join(args), "status": s["status"], "gen": s["gen"],
            "pop": s["pop"], "seed_pop": s["seed_pop"], "events": evs}


def main():
    argv = sys.argv[1:]
    k = argv.index("--")
    opts, gargs = argv[:k], argv[k + 1:]
    out = opts[0]
    o = dict(zip(opts[1::2], opts[2::2]))
    a, b = map(int, o["--rngs"].split(":"))
    jobs, every, gens = int(o.get("--jobs", 2)), int(o.get("--every", 64)), int(o.get("--gens", 10**6))
    done = set()
    if os.path.exists(out):
        for line in open(out):
            r = json.loads(line)
            if r["args"] == " ".join(gargs):
                done.add(r["rng"])
    todo = [r for r in range(a, b) if r not in done]
    with tempfile.TemporaryDirectory() as tmp, open(out, "a") as f, ThreadPoolExecutor(jobs) as ex:
        for res in ex.map(lambda r: one(gargs, r, every, gens, tmp), todo):
            f.write(json.dumps(res) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
