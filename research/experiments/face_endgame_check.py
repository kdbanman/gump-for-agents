#!/usr/bin/env python3
"""Lead's independent check of the fluct agent's small-face claims, using only the engine's kymograph.
Asymmetric soups (density 0.35) in an octahedron of radius R; from generation T0, while all 8 faces are alive,
histogram each face's population; stop at the first face death. Prints mean first-peel time, p_k, h/p_1, p_1/p_2,
and where deaths come from.   python3 research/experiments/face_endgame_check.py R RUNS [T0] [JOBS]   (R=9, 16000 soups: ~3 min)"""
import subprocess, sys, os, tempfile, collections, math
from multiprocessing import Pool
G = "engine/target/release/gump"
R, RUNS = int(sys.argv[1]), int(sys.argv[2]); T0 = int(sys.argv[3]) if len(sys.argv) > 3 else 200
JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 3
CAP = 4000000
def one(i):
    d = tempfile.mkdtemp(); fifo = os.path.join(d, "k"); os.mkfifo(fifo)
    p = subprocess.Popen([G, "run", "--soup", "0.35", "--radius", str(R), "--rng", str(i), "--gens", str(CAP),
                          "--kymo", fifo, "--every", "1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hist = collections.Counter(); expo = 0; death = None; prev = None
    with open(fifo) as f:
        head = f.readline().rstrip("\n").split(","); lo = head.index(str(-R)); hi = head.index(str(R))
        cur = []; g_cur = None
        for line in f:
            row = line.split(","); g = int(row[0])
            if g != g_cur:
                if g_cur is not None and len(cur) == 8:
                    if g_cur >= T0 or min(cur) == 0:
                        if min(cur) == 0:
                            if g_cur < T0 or prev is None: death = None; break          # peeled before T0: not counted
                            death = (g_cur - T0, tuple(prev[k] for k in range(8) if cur[k] == 0)); break
                        for n in cur: hist[n] += 1
                        expo += 1; prev = cur
                cur = []; g_cur = g
            cur.append(int(row[lo])); cur.append(int(row[hi]))
    p.kill(); p.wait(); os.remove(fifo); os.rmdir(d)
    return hist, expo, death
if __name__ == "__main__":
    H = collections.Counter(); E = 0; deaths = []; skipped = 0
    with Pool(JOBS) as pool:
        for hist, expo, death in pool.imap_unordered(one, range(1, RUNS + 1), chunksize=4):
            H.update(hist); E += expo
            if death: deaths.append(death)
            else: skipped += 1
    k = len(deaths); tau = E / k; A = 3 * ((R - 1) // 2 + 1) * ((R - 1) // 2 + 2) // 2
    print(f"R={R} A={A}: {RUNS} soups, {k} first peels after T0={T0} ({skipped} not counted), exposure {E} soup-gens")
    print(f"  mean first-peel time {tau:.1f} +- {tau/math.sqrt(k):.1f};  h per face-gen = {k/(8*E):.4g};  -ln h / A = {-math.log(k/(8*E))/A:.4f}")
    N = 8 * E; p = {n: H[n] / N for n in range(1, 13)}
    print("  k: count, ln p_k, p_k/p_{k+1}")
    for n in range(1, 11): print(f"   {n:2d}: {H[n]:8d}  {math.log(p[n]) if H[n] else float('nan'):8.3f}  {p[n]/p[n+1] if H[n+1] else float('nan'):.3f}")
    h = k / N; print(f"  h/p_1 = {h/p[1]:.3f}   p_1/p_2 = {p[1]/p[2]:.3f}   p_2/p_3 = {p[2]/p[3]:.3f}")
    frm = collections.Counter(n for _, ns in deaths for n in ns); tot = sum(frm.values())
    print("  deaths from n = " + ", ".join(f"{n}: {100*c/tot:.0f}%" for n, c in sorted(frm.items())[:6]))
