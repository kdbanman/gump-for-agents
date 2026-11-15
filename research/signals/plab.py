"""Pulse lab: the period-2 wire of objects/pulse-A.json ("wire A") on a ring, in a tube wide enough to be exact for
anything that starts within one neighbour step of the wire (T2: both tube diagonals are perpendicular to the wire)."""
import json, os
import numpy as np
import sg

HERE = os.path.dirname(os.path.abspath(__file__))
S1, S2 = (1, 1, 1), (1, -1, 1)
V = (1, 0, -1)


def load(name='pulse-A'):
    return json.load(open(os.path.join(HERE, 'objects', name + '.json')))


def geom(N, lo=-7, hi=13):
    return sg.Geom([(N, 0, -N)], [(S1, lo, hi), (S2, lo, hi)], unitvec=V)


def tr(cells, k, v=V):
    return [(c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2]) for c in cells]


def background(g, ob, phase=0):
    st = g.state(sg.lift_periodic([tuple(c) for c in ob['bg']], [V], [range(g.N)]))
    return g.run(st, phase, sparse=True) if phase else st


def with_defect(g, st, cells, k=0):
    st = st.copy()
    for c in tr([tuple(c) for c in cells], k):
        st[g.index[g.canon(c)]] ^= 1
    return st


def kymo(g, x, bg, gens, every=1, u_from=0, u_to=None):
    """Lines of text: per generation, one character per cube: '.' = as the background, else the number of differing cells."""
    out = []
    for t in range(gens + 1):
        if t % every == 0:
            d = (g.as_grid(x) != g.as_grid(bg)).sum(1)[u_from:u_to]
            out.append('%4d ' % t + ''.join('.' if v == 0 else (str(v) if v < 10 else '#') for v in d))
        x = g.run(x, 1, sparse=True); bg = g.run(bg, 1, sparse=True)
    return out
