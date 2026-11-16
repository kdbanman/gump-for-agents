#!/usr/bin/env python3
"""What the moving things of wire C do to each other, as text (hex masks per unit, family.py; b = bare wire C).

    python3 collisions_C.py

9f = pulse towards +v, 7 = pulse towards -v, f = rake towards +v (emits 7s), 5f = rake towards -v (emits 9fs).
Steps: sg.Geom on a finite piece of the closed 3 x 3 tube (family.Piece)."""
import family as F

pc = F.Piece(90); g = pc.g


def show(masks_at, title, gens=22, ua=-10, ub=26):
    print(title)
    x = pc.config(lambda u: masks_at.get(u, 0xb))
    for t in range(0, gens + 1, 2):
        print('%3d %s' % (t, pc.decode(x, ua, ub))); x = g.run(x, 2, sparse=True)


for d in (10, 11):
    show({0: 9, 1: 0xf, d: 7}, 'pulse 9f at units 0,1 against pulse 7 at unit %d' % d)
for d in (10, 11):
    show({0: 0xf, d: 7}, 'rake f at unit 0 against pulse 7 at unit %d' % d)
for d in (4, 5):
    show({15: 5, 16: 0xf, d: 9, d + 1: 0xf}, 'rake 5f at units 15,16 against pulse 9f at units %d,%d' % (d, d + 1))
for d in (12, 13):
    show({0: 0xf, d: 5, d + 1: 0xf}, 'rake f at unit 0 against rake 5f at units %d,%d' % (d, d + 1))
