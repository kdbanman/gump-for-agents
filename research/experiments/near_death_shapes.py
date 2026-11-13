#!/usr/bin/env python3
"""What do near-empty faces look like?  Asymmetric soups (density 0.35) in an octahedral hull of radius R, stepped
with a from-the-rule-text stepper. Whenever a living outer face holds exactly n = 1..4 cells (generation >= T0),
record the shape of those cells as the sorted multiset of pairwise squared distances (doubled coordinates:
2 = edge-sharing in-layer neighbours, 8 = coplanar corner-touching, larger = not neighbours).
   python3 research/experiments/near_death_shapes.py R SOUPS SEED0   (R=9, 300 soups: ~6 min)"""
import sys, random, collections, itertools
R, SOUPS, SEED0 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); T0 = 200; CAPG = 60000
def offs(a):
    b, c = [i for i in range(3) if i != a]; o = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; o.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; o.append(tuple(v))
    return o
OFF = [offs(a) for a in range(3)]
D = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
def axis(c): return 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
def step(S):
    cnt = {}
    for c in S:
        for o in OFF[axis(c)]:
            n = (c[0] + o[0], c[1] + o[1], c[2] + o[2]); cnt[n] = cnt.get(n, 0) + 1
    return {c for c, k in cnt.items() if (k == 4 or k == 5) or (k == 3 and c in S)}
hull = [c for c in itertools.product(range(-R - 1, R + 2), repeat=3)
        if sum(x & 1 for x in c) == 1 and all(abs(sum(d[i] * c[i] for i in range(3))) <= R for d in D)]
face_of = {}
for c in hull:
    for k, d in enumerate(D):
        s = sum(d[i] * c[i] for i in range(3))
        if abs(s) == R: face_of.setdefault(c, []).append((k, s > 0))
shapes = collections.defaultdict(collections.Counter); visits = collections.Counter(); deaths = 0; expo = 0
dwell = collections.Counter(); nxt = collections.Counter(); TRI = (2, 2, 2)
for run in range(SOUPS):
    rng = random.Random(SEED0 + run); S = {c for c in hull if rng.random() < 0.35}
    tri_prev = {}
    for g in range(1, CAPG):
        S = step(S)
        faces = collections.defaultdict(list)
        for c in S:
            if c in face_of:
                for f in face_of[c]: faces[f].append(c)
        for f, (cs0, run0) in list(tri_prev.items()):               # what a triangle becomes one generation later
            cs1 = faces.get(f, [])
            if frozenset(cs1) != cs0: nxt[len(cs1) if len(cs1) < 6 else 6] += 1; dwell[run0] += 1; del tri_prev[f]
        if len(faces) < 8:
            if g >= T0: deaths += 1
            break
        if g < T0: continue
        expo += 1
        for f, cs in faces.items():
            n = len(cs)
            if n <= 4:
                visits[n] += 1
                if n >= 2:
                    sh = tuple(sorted(sum((a[i] - b[i]) ** 2 for i in range(3)) for a, b in itertools.combinations(cs, 2)))
                    shapes[n][sh] += 1
                    if sh == TRI:
                        fs = frozenset(cs); old = tri_prev.get(f)
                        tri_prev[f] = (fs, old[1] + 1 if old and old[0] == fs else 1)
print(f"R={R}: {SOUPS} soups, exposure {expo} soup-gens, {deaths} first peels (mean {expo/max(1,deaths):.0f})")
for n in (1, 2, 3, 4):
    print(f" n={n}: {visits[n]} face-generations" + ("" if n == 1 else "; shapes (pairwise d^2): " +
          ", ".join(f"{sh} {100*c/visits[n]:.0f}%" for sh, c in shapes[n].most_common(5))))
tot = sum(nxt.values())
print(" a lone triangle, one generation later, is replaced by a face of n = " + ", ".join(f"{k}{'+' if k == 6 else ''}: {100*c/tot:.0f}%" for k, c in sorted(nxt.items())))
print(" triangle dwell (consecutive generations as the same triangle): " + ", ".join(f"{k}: {c}" for k, c in sorted(dwell.items())))
