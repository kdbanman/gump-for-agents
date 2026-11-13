#!/usr/bin/env python3
"""Run many single engine lineages and record every plateau (residence at one hull radius).

  python3 research/lineage/run_lineages.py struct N COUNT [JOBS=3] [CAP=4e7] [START=0]
        COUNT structured O_h seeds built on the closed cube of side N (research/lineage/seeds.py):
        the cube itself, cube minus one surface orbit (notch), minus two (notch2), hollow cubes, nested shells
  python3 research/lineage/run_lineages.py soup R COUNT [JOBS=3] [CAP=4e7] [START=0]
        COUNT O_h-symmetric soups (density 0.35) in the octahedron of radius R, centred on a cube centre (R odd)
        or a vertex (R even), rng START+1 ...

Rows are appended to research/scratch/lineage/plateaus_<kind><N|R>.csv:
  tag, kind, centre, idx (0 = first plateau of the run, after layers lost in the first 1000 generations), r, t0 (start), T (residence), died (1 = the outer layer
  died; 0 = run ended first: 'cap' or chaos settled), end, sig (hash of the run's whole schedule, for de-duplication)
Radius convention as research/experiments/cube_vs_ensemble.py: r = s - s_centre for the outermost living layer
of diagonal 0, s > 0 (all 8 faces peel together under O_h). Events are sampled every 8 generations.
"""
import subprocess, sys, json, os, hashlib, itertools
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seeds
TRANS = 1000                         # layers dead before this generation are part of the seed's initial burst, not plateaus
G = "engine/target/release/gump"; D = "research/scratch/lineage"; os.makedirs(f"{D}/tmp", exist_ok=True)

def struct_specs(n):
    """deterministic list of structured seeds for side n; duplicates are removed later by schedule signature"""
    c = seeds.centre(n); cube = seeds.box_cells(c, n); orbs = seeds.orbits_of(cube, c)
    surf = [k for k, o in enumerate(orbs) if max(max(abs(p[i] - c[i]) for i in range(3)) for p in o) >= n - 1]
    surf.reverse()                                                   # outermost first
    out = [("cube", None)]
    out += [(f"notch:{n}:{k}", ("notch", k)) for k in surf]
    out += [(f"hollow:{n}:{k}", None) for k in range(n - 2, 0, -2)]
    out += [(f"nest:{n}:{k}", None) for k in range(1, 256) if k != 127]
    out += [(f"notch2:{n}:{a}:{b}", ("notch2", a, b)) for a, b in itertools.combinations(surf, 2)]
    return out, cube, orbs

def schedule(ev, s0):
    last = {}
    for line in open(ev):
        e = json.loads(line)
        if e["type"] == "layer_death" and e["axis"] == 0 and e["cause"] == "hull" and e["s"] > 0:
            last.setdefault(e["s"], e["last_alive"])
    return last

def plateaus(last, smax, s0, end, status):
    rows = []; t = 0; idx = 0
    for s in range(smax, s0, -2):
        if s in last:
            if last[s] <= t: continue                            # never alive after t (the seed's empty outer layers)
            if last[s] < TRANS: t = last[s]; continue            # outer layers of the seed lost in its first burst

            rows.append((idx, s - s0, t, last[s] - t, 1, "")); t = last[s]; idx += 1
        else:
            rows.append((idx, s - s0, t, end - t, 0, "cap" if status == "running" or status == "cap" else status)); break
    return rows

def one(job):
    kind, tag, args, s0, cells = job
    ev = f"{D}/tmp/{tag.replace(':', '_')}.jsonl"; cf = None
    if cells is not None:
        cf = ev.replace(".jsonl", ".txt")
        with open(cf, "w") as f:
            for p in sorted(cells): f.write(f"{p[0]} {p[1]} {p[2]}\n")
        args = ["--cells", cf] + args
    out = subprocess.run([G, "run"] + args + ["--events", ev, "--every", "8"], capture_output=True, text=True).stdout
    summ = json.loads(out.strip().split("\n")[-1])
    if not summ.get("hull_initial"):                              # seed burned out at once: no hull, no plateaus
        os.remove(ev); cf and os.remove(cf); return []
    smax = max(summ["hull_initial"][0]); last = schedule(ev, s0)
    os.remove(ev); cf and os.remove(cf)
    rows = plateaus(last, smax, s0, summ["gen"], summ["status"])
    sig = hashlib.md5(repr([(r[1], r[3]) for r in rows]).encode()).hexdigest()[:12]
    return [(tag, kind, "c" if s0 == 0 else "v") + r + (sig,) for r in rows]

def main():
    kind, N, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 3; cap = int(float(sys.argv[5])) if len(sys.argv) > 5 else 40_000_000
    start = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    s0 = 0 if N % 2 else 3
    todo = []
    if kind == "struct":
        specs, cube, orbs = struct_specs(N)
        for tag, how in specs[start:start + count]:
            if tag == "cube": cells = cube; tag = f"cube:{N}:0"
            elif how and how[0] == "notch": cells = cube - orbs[how[1]]
            elif how and how[0] == "notch2": cells = cube - orbs[how[1]] - orbs[how[2]]
            else: cells = seeds.make(tag)
            todo.append((kind, tag, ["--gens", str(cap)], s0, cells))
    else:
        cen = "0,0,0" if N % 2 else "1,1,1"
        for i in range(start + 1, start + count + 1):
            todo.append((kind, f"soup:{N}:{i}", ["--soup", "0.35", "--radius", str(N), "--sym", "oh", "--center", cen,
                                                  "--rng", str(i), "--gens", str(cap)], s0, None))
    path = f"{D}/plateaus_{kind}{N}.csv"; new = not os.path.exists(path)
    with open(path, "a") as f, ThreadPoolExecutor(jobs) as ex:
        if new: f.write("tag,kind,centre,idx,r,t0,T,died,end,sig\n")
        for rows in ex.map(one, todo):
            for row in rows: f.write(",".join(map(str, row)) + "\n")
            f.flush()

if __name__ == "__main__":
    main()
