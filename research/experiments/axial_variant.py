"""What if the four coplanar neighbours were the edge-sharing ("axial") ones instead of the corner-touching ones?
Uses reference/oracle.py unchanged except for the offsets.  python3 research/experiments/axial_variant.py   (from the repo root; about a minute)"""
import sys, numpy as np
sys.path.insert(0, "reference")
import oracle

def offsets_axial(axis):
    a = axis; b, c = [i for i in range(3) if i != a]; offs = []
    for t in (b, c):
        for s in (2, -2):
            o = [0, 0, 0]; o[t] = s; offs.append(tuple(o))          # 4 coplanar faces sharing an edge
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs

def run(H, lo, hi, gens, offs):
    oracle.offsets = offs
    m = oracle.masks(H); h = oracle.fill_box(H, lo, hi, m); pops = [int(h.sum())]; ext = []
    for g in range(gens):
        h = oracle.step(h, m); pops.append(int(h.sum()))
        idx = np.argwhere(h); c = H // 2
        ext.append((int(np.abs(idx - c).sum(1).max()) if len(idx) else 0, int(np.abs(idx - c).max()) if len(idx) else 0))
    return pops, ext

orig = oracle.offsets
for side, H in ((8, 40), (9, 50)):
    ref = [int(l.split()[1]) for l in open(f"reference/golden/legacy_cube_side{side:02d}_H{H}.txt") if l.strip()]
    lo, hi = oracle.legacy_seed_span(H)
    for name, offs in (("corner-touching (as coded in 2012)", orig), ("edge-sharing (axial)", offsets_axial)):
        pops, _ = run(H, lo, hi, len(ref) - 1, offs)
        bad = [g for g in range(1, len(ref)) if pops[g] != ref[g]]
        print(f"side {side}, coplanar = {name}: {len(ref)-1} generations, mismatches vs 2012 log: {len(bad)}" + (f", first at generation {bad[0]} (log {ref[bad[0]]}, this {pops[bad[0]]})" if bad else ""))

# layer histogram along a body diagonal for each neighbourhood (T1)
for name, offs in (("corner-touching", orig), ("axial", offsets_axial)):
    hist = {}
    for o in offs(0): hist[sum(o)] = hist.get(sum(o), 0) + 1
    print("layer histogram,", name, dict(sorted(hist.items())))

# the axial variant in a roomy box: does a cube stay inside any hull?
H = 96; lo, hi = 48 - 8, 48 + 8; lo += (lo % 2 == 0); hi -= (hi % 2 == 0)
for name, offs in (("corner-touching", orig), ("axial", offsets_axial)):
    pops, ext = run(H, lo, hi, 60, offs)
    print(name, "cube span", lo, hi, "pop at gens 0,5,10,20,30,40,60:", [pops[g] for g in (0, 5, 10, 20, 30, 40, 60)], " L1 radius at 5,10,20,40,60:", [ext[g - 1][0] for g in (5, 10, 20, 40, 60)], " max |coord| at 5,10,20,40,60:", [ext[g - 1][1] for g in (5, 10, 20, 40, 60)])

# a random soup (density 0.4) in a 16-wide box, in a roomy torus: does it stay inside its diagonal hull?
def soup_run(offs, gens=80, H=80, half=8, seed=1):
    oracle.offsets = offs
    m = oracle.masks(H); rng = np.random.default_rng(seed); c = H // 2
    h = np.zeros((H, H, H), np.int8); box = np.zeros((H, H, H), bool); box[c - half:c + half + 1, c - half:c + half + 1, c - half:c + half + 1] = True
    h[(m[0] | m[1] | m[2]) & box & (rng.random((H, H, H)) < 0.4)] = 1
    out = []
    for g in range(gens + 1):
        if g in (0, 10, 20, 40, 60, 80):
            idx = np.argwhere(h); out.append((g, int(h.sum()), int(np.abs(idx - c).sum(1).max()) if len(idx) else 0, int(np.abs(idx - c).max()) if len(idx) else 0))
        h = oracle.step(h, m)
    return out
for name, offs in (("corner-touching", orig), ("axial", offsets_axial)):
    for seed in (1, 2):
        print("soup,", name, "seed", seed, "(generation, live, L1 radius, max |coord|):", soup_run(offs, seed=seed))
