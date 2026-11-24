#!/usr/bin/env python3
"""Shared helpers for the tape_*.py scripts (the Lean arm's "for every N" laws): orbits of finite objects under
reference/oracle.py, the ground truth, in a box large enough by the light cone that the oracle's torus is never felt
(a live cell moves at most 2 doubled units per generation, so a box of side extent + 4*gens + 8 suffices).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

TAU = (2, 0, -2)          # one unit of the wire towards +v


def load(rel):
    return json.load(open(os.path.join(ROOT, rel)))


def tr(c, k, v=TAU):
    return (c[0] + k * v[0], c[1] + k * v[1], c[2] + k * v[2])


def unit(c):
    return c[0] >> 1      # floor(x / 2)


def orbit(cells, gens):
    """[X(0), ..., X(gens)] as frozensets of points, by reference/oracle.py on a box that is never wrapped."""
    cells = [tuple(c) for c in cells]
    if not cells:
        return [frozenset()] * (gens + 1)
    a = np.array(cells)
    lo, hi = a.min(0), a.max(0)
    H = int((hi - lo).max()) + 4 * gens + 12
    H += H % 2
    off = [int(H // 2 - ((int(hi[i]) + int(lo[i])) // 2)) & ~1 for i in range(3)]
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    m = oracle.masks(H)
    out = []
    for t in range(gens + 1):
        pts = np.argwhere(h == 1)
        if len(pts):
            assert pts.min() >= 2 and pts.max() < H - 2, 'box felt'
        out.append(frozenset((int(x) - off[0], int(y) - off[1], int(z) - off[2]) for x, y, z in pts))
        if t < gens:
            h = oracle.step(h, m)
    return out


def units(s, a, b):
    return frozenset(c for c in s if a <= unit(c) <= b)


def shift(s, k):
    return frozenset(tr(c, k) for c in s)


def lean_list(cells):
    return '[' + ', '.join(f'⟨{x}, {y}, {z}⟩' for x, y, z in sorted(cells)) + ']'


def orbit_box(cells, gens):
    """As orbit, on a box with a size of its own along each axis (extent + 4*gens + 12, even), masks by the oracle's
    formula (coordinate a odd, the others even), stepped by oracle.step; checked never to be felt."""
    cells = [tuple(c) for c in cells]
    a = np.array(cells)
    lo, hi = a.min(0), a.max(0)
    shape = tuple(int(hi[i] - lo[i]) + 4 * gens + 12 + ((int(hi[i] - lo[i]) + 4 * gens + 12) % 2) for i in range(3))
    off = [int(shape[i] // 2 - ((int(hi[i]) + int(lo[i])) // 2)) & ~1 for i in range(3)]
    par = np.indices(shape) % 2
    m = [(par[i] == 1) & (par.sum(0) == 1) for i in range(3)]
    h = np.zeros(shape, np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    out = []
    for t in range(gens + 1):
        pts = np.argwhere(h == 1)
        if len(pts):
            assert (pts.min(0) >= 2).all() and (pts.max(0) < np.array(shape) - 2).all(), 'box felt'
        out.append(frozenset((int(x) - off[0], int(y) - off[1], int(z) - off[2]) for x, y, z in pts))
        if t < gens:
            h = oracle.step(h, m)
    return out
