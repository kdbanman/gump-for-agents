"""Occupancy of an octahedral face vs distance from the face's edge (min over the 3 coordinates, after flipping
signs so the face is d0 = (1,1,1)); includes never-occupied cells of the face."""
import sys, numpy as np
sys.path.insert(0, '.')
from cubeface import face_area
f = np.load(sys.argv[1]); D = np.array([(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)])
C = f['C']; prof = {}
for d in range(4):
    for sg in (1, -1):
        c = C[d][0 if sg == 1 else 1]
        sel = (f['d'] == d) & (f['sg'] == sg)
        q = f['p'][sel] * D[d] * sg          # map to the (+,+,+) octant face
        occ = dict(zip(map(tuple, q), f['occ'][sel]))
        # all cells of that face: x,y,z >= 0, sum = c, one odd coordinate
        for x in range(c + 1):
            for y in range(c + 1 - x):
                z = c - x - y; p = (x, y, z)
                if sum(v % 2 for v in p) != 1: continue
                e = min(p); prof.setdefault(e, []).append(occ.get(p, 0.0))
print('edge-dist  ncells  mean-occupancy')
for e in sorted(prof): print(f'{e:5d} {len(prof[e])//8:6d} {np.mean(prof[e]):.3f}')
