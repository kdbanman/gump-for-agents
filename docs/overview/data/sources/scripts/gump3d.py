#!/usr/bin/env python3
"""Series 1-3 (soup_staircase, face_death_closeup, kagome_face) from one engine run.
Run from the repo root:
  E=<this dir>; G=./engine/target/release/gump
  $G run --soup 0.4 --radius 11 --rng 61 --every 1 --kymo $E/run61/kymo.csv --events $E/run61/events.jsonl \
        --poplog $E/run61/pop.txt --out /dev/null
  $G run --soup 0.4 --radius 11 --rng 61 --gens 150000 --cells-out $E/run61/cells150000.txt
  python3 $E/gump3d.py $E          -> $E/part3d.json
"""
import sys, json, math
import numpy as np, pandas as pd

E = sys.argv[1]; R = 11; RNG = 61
D = [(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]          # engine's diag axes 0..3

pop = np.loadtxt(f'{E}/run61/pop.txt', dtype=np.int64)
gens, P = pop[:, 0], pop[:, 1]
assert (gens == np.arange(len(gens))).all()
W = math.ceil(len(P) / 600)
mins = [int(P[i:i + W].min()) for i in range(0, len(P), W)]
maxs = [int(P[i:i + W].max()) for i in range(0, len(P), W)]

ev = [json.loads(l) for l in open(f'{E}/run61/events.jsonl')]
summary_final_pop = int(P[-1])

k = pd.read_csv(f'{E}/run61/kymo.csv')
layers = [int(c) for c in k.columns[2:]]
K = {a: k[k.axis == a].drop(columns=['axis']).set_index('gen') for a in range(4)}   # K[a].loc[g, str(s)]

def cells_of_layer(a, s, hull):
    """all lattice sites with d_a.p = s inside hull {axis: (lo, hi)}"""
    out = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if sum(v % 2 for v in (x, y, z)) != 1: continue
                p = (x, y, z)
                if sum(di * pi for di, pi in zip(D[a], p)) != s: continue
                if all(hull[b][0] <= sum(di * pi for di, pi in zip(D[b], p)) <= hull[b][1] for b in range(4)):
                    out.append(p)
    return out

def hull_at(g):
    h = {}
    for a in range(4):
        row = K[a].loc[g]
        live = [s for s in layers if row[str(s)] > 0]
        h[a] = (min(live), max(live))
    return h

# --- series 1: face deaths per signed direction
per_dir = {}
for e in ev:
    a, s = e['axis'], e['s']
    sign = 1 if s > 0 else -1
    d = tuple(sign * c for c in D[a])
    per_dir.setdefault(str(list(d)), []).append([e['gen'], abs(s)])
soup = {
    "radius": R, "seed": f"--soup 0.4 --radius {R} --rng {RNG}", "density": 0.4, "centre": [0, 0, 0],
    "initial_pop": int(P[0]), "generations": int(len(P) - 1), "end_status": "still life entered at gen 416569",
    "final_pop": summary_final_pop, "pop_bucket_width": W, "pop_min": mins, "pop_max": maxs,
    "outer_face_area_initial": 63,
    "layer_deaths_by_direction": per_dir,
    "layer_deaths_format": "per signed diagonal direction d: [generation the layer d.p = s is first all-dead, s]; "
                            "s = 11 is the original outer face, then 9, 7, ... (each later layer is the new face)",
    "layer_deaths_chronological": [[e['gen'], e['axis'], e['s']] for e in ev],
}

# --- series 2: closeups of the first three deaths (all original outer faces)
close = []
for e in ev[:3]:
    a, s, g = e['axis'], e['s'], e['gen']
    h = hull_at(g - 1)
    area = len(cells_of_layer(a, s, h))
    series = [int(v) for v in K[a].loc[g - 300:g - 1, str(s)].values]
    assert len(series) == 300 and int(K[a].loc[g, str(s)]) == 0 and series[-1] > 0
    sign = 1 if s > 0 else -1
    close.append({"axis": a, "s": s, "direction": [sign * c for c in D[a]], "death_gen": g,
                  "area_at_death": area, "hull_at_death": {str(b): list(h[b]) for b in range(4)},
                  "gens": [g - 300, g - 1], "pop": series})
a0, s0 = ev[0]['axis'], ev[0]['s']
life = [int(v) for v in K[a0].loc[150000:152999, str(s0)].values]
assert len(life) == 3000
face_close = {"faces": close,
              "ordinary_life": {"axis": a0, "s": s0, "gens": [150000, 152999], "area": 63, "pop": life,
                                "mean": round(float(np.mean(life)), 2)}}

# --- series 3: one outer face as a kagome lattice, gen 150000
live = set()
for l in open(f'{E}/run61/cells150000.txt'):
    if l.startswith('#'): continue
    live.add(tuple(map(int, l.split())))
full = {a: (-R, R) for a in range(4)}
sites = cells_of_layer(0, 11, full)
pts = []
for p in sites:
    x, y, z = p
    pts.append([x, y, z, round((x - y) / math.sqrt(2), 4), round((x + y - 2 * z) / math.sqrt(6), 4), int(p in live)])
nlive = sum(q[5] for q in pts)
assert nlive == int(K[0].loc[150000, '11']), (nlive, K[0].loc[150000, '11'])
kag = {"radius": R, "seed": soup["seed"], "gen": 150000, "layer": "d=(1,1,1), s=x+y+z=11 (axis 0)",
       "area": len(sites), "live": nlive,
       "u": "(1,-1,0)/sqrt(2)", "v": "(1,1,-2)/sqrt(6)",
       "sites_format": "[x, y, z, u.p, v.p, alive]", "sites": pts}
json.dump({"soup_staircase": soup, "face_death_closeup": face_close, "kagome_face": kag},
          open(f'{E}/part3d.json', 'w'), separators=(',', ':'))
print('W', W, 'buckets', len(mins), 'areas', [c['area_at_death'] for c in close], 'kagome', len(sites), nlive)
