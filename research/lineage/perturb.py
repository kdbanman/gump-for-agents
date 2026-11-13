#!/usr/bin/env python3
"""Unperturbed vs perturbed continuations of structured lineages, for many source states.

For each of the first M distinct structured seeds of side N whose first plateau (hull radius r0) is still alive
at generation TS: take the state at TS, then run
  copy 0  : the state itself (unperturbed; must reproduce the lineage's own remaining wait - checked)
  copy 1..K: the state with one O_h orbit of live cells killed (orbit of a random live cell well inside the hull)
and record the residual wait until the r0 layer dies. Rows -> research/scratch/lineage/perturb_<N>_<TS>.csv:
  src, copy, resid, died, lineage_resid (the residual the original lineage had)
  python3 research/lineage/perturb.py N TS M K [JOBS=3] [CAP=4e7]
Needs research/scratch/lineage/plateaus_struct<N>.csv (run_lineages.py struct N ...) for the lineage residuals.
"""
import sys, os, csv, json, random, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seeds, run_lineages as L
G = L.G; D = L.D

def cells_of(path):
    return [tuple(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith("#")]

def write(cells, path):
    with open(path, "w") as f:
        for p in sorted(cells): f.write(f"{p[0]} {p[1]} {p[2]}\n")

def wait_for(cellfile, s_layer, cap, tag):
    ev = f"{D}/tmp/{tag}.jsonl"
    out = subprocess.run([G, "run", "--cells", cellfile, "--gens", str(cap), "--events", ev, "--every", "8"],
                         capture_output=True, text=True).stdout
    summ = json.loads(out.strip().split("\n")[-1]); last = L.schedule(ev, 0); os.remove(ev)
    return (last[s_layer], 1) if s_layer in last else (summ["gen"], 0)

def job(a):
    src, tag, cells, s0, r0, ts, resid, K, cap = a
    base = f"{D}/tmp/pt_{src}"; write(cells, base + "_seed.txt")
    subprocess.run([G, "run", "--cells", base + "_seed.txt", "--gens", str(ts), "--no-halt", "--cells-out", base + "_st.txt"],
                   capture_output=True, text=True)
    st = cells_of(base + "_st.txt"); c = seeds.centre(int(tag.split(":")[1])); rng = random.Random(src)
    out = []
    for k in range(K + 1):
        cs = set(st)
        if k:
            inner = [p for p in st if sum(abs(p[i] - c[i]) for i in range(3)) < r0 - 8]
            cs -= seeds.orbit(rng.choice(inner), c)
        write(cs, f"{base}_{k}.txt")
        w, died = wait_for(f"{base}_{k}.txt", s0 + r0, cap, f"pt_{src}_{k}")
        os.remove(f"{base}_{k}.txt"); out.append((src, k, w, died, resid, tag, r0))
    os.remove(base + "_seed.txt"); os.remove(base + "_st.txt")
    return out

def main():
    N, TS, M, K = (int(float(x)) for x in sys.argv[1:5])
    jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 3; cap = int(float(sys.argv[6])) if len(sys.argv) > 6 else 40_000_000
    s0 = 0 if N % 2 else 3
    first = {}; seen = set()
    for r in csv.DictReader(open(f"{D}/plateaus_struct{N}.csv")):
        if r["idx"] == "0" and r["sig"] not in seen and r["died"] == "1" and int(r["T"]) > TS:
            seen.add(r["sig"]); first[r["tag"]] = (int(r["r"]), int(r["T"]) - TS)
    specs, cube, orbs = L.struct_specs(N); todo = []
    for tag, how in specs:
        t2 = f"cube:{N}:0" if tag == "cube" else tag
        if t2 not in first: continue
        if tag == "cube": cells = cube
        elif how and how[0] == "notch": cells = cube - orbs[how[1]]
        elif how and how[0] == "notch2": cells = cube - orbs[how[1]] - orbs[how[2]]
        else: cells = seeds.make(tag)
        r0, resid = first[t2]
        todo.append((len(todo), t2, cells, s0, r0, TS, resid, K, cap))
        if len(todo) >= M: break
    path = f"{D}/perturb_{N}_{TS}.csv"
    with open(path, "w") as f, ThreadPoolExecutor(jobs) as ex:
        f.write("src,copy,resid,died,lineage_resid,tag,r0\n")
        for rows in ex.map(job, todo):
            for row in rows: f.write(",".join(map(str, row)) + "\n")
            f.flush()

if __name__ == "__main__":
    main()
