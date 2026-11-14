#!/usr/bin/env python3
"""Calculator for journal entry 19 (path line): the mean-field closure, recorded as a dead end.

No simulation. Every cell of a layer is treated as an independent coin: a cell of layer l with density x_l is alive
next with probability F_l = x_l P(n in S) + (1 - x_l) P(n in B), n a sum of independent binomials over its
neighbours' layers.  Then the layer populations are binomial and the discrete-time quasi-potential is

    V(x) = min_y [ sum_l w_l KL(y_l || F_l(x)) + V(y) ],     V = 0 on the target (outer sealed set empty),

with the top d layers free and the deeper ones pinned at the mean-field profile (d = 1, 2).

    python3 mf_deadend.py            # profiles, V1 (with and without rising paths), gump's neighbours, the Moore
                                     # edge, and the closure's one-step roots against the measured ones
    python3 mf_deadend.py 100        # also V2 on a 101 x 101 grid (about a minute)
"""
import sys
from math import comb

import numpy as np


def binom(n, p):
    return np.array([comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)])


def cellmap(x_self, parts, B, S):
    d = np.array([1.0])
    for c, x in parts:
        if c > 0:
            d = np.convolve(d, binom(c, x))
    s = sum(d[n] for n in S if n < len(d))
    b = sum(d[n] for n in B if n < len(d))
    return x_self * s + (1 - x_self) * b


class Layers:
    """nb(l) -> [(count, layer)]; layer < 0 is outside the vessel (dead); layer >= D reads the bulk value."""

    def __init__(self, nb, B, S, K, weights, D=14):
        self.nb, self.B, self.S, self.D, self.w = nb, B, S, D, weights
        x = 0.4
        for _ in range(100000):
            xn = cellmap(x, [(K, x)], B, S)
            if abs(xn - x) < 1e-14:
                break
            x = 0.5 * x + 0.5 * xn
        self.bulk = x

    def step(self, prof):
        new = np.empty(self.D)
        for l in range(self.D):
            parts = [(c, prof[j] if j < self.D else self.bulk) for c, j in self.nb(l) if j >= 0]
            new[l] = cellmap(prof[l], parts, self.B, self.S)
        return new

    def profile(self):
        prof = np.full(self.D, self.bulk)
        for _ in range(200000):
            new = self.step(prof)
            if np.max(np.abs(new - prof)) < 1e-13:
                break
            prof = 0.5 * prof + 0.5 * new
        return prof

    def F_top(self, top, prof):
        p = prof.copy()
        p[: len(top)] = top
        return self.step(p)[: len(top)]


def KL(y, f):
    f = np.clip(f, 1e-300, 1 - 1e-15)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(y > 0, y * np.log(y / f), 0.0)
        b = np.where(y < 1, (1 - y) * np.log((1 - y) / (1 - f)), 0.0)
    return a + b


def V1(L, prof, G=1000):
    """Returns (V, V restricted to paths of decreasing density, largest density on the minimising path)."""
    xs = np.linspace(0, 1, G + 1)
    F = np.array([L.F_top(np.array([x]), prof)[0] for x in xs])
    I = L.w[0] * KL(xs[None, :], F[:, None])
    V = np.full(G + 1, np.inf)
    V[0] = 0
    for _ in range(10000):
        Vn = np.minimum(V, (I + V[None, :]).min(axis=1))
        Vn[0] = 0
        if np.allclose(Vn, V, atol=1e-13, rtol=0):
            break
        V = Vn
    Vd = np.full(G + 1, np.inf)
    Vd[0] = 0
    for i in range(1, G + 1):
        Vd[i] = (I[i, :i] + Vd[:i]).min()
    i = i0 = int(round(prof[0] * G))
    top = xs[i]
    for _ in range(200):
        j = int((I[i] + V).argmin())
        if j == i or i == 0:
            break
        i = j
        top = max(top, xs[i])
    return float(V[i0]), float(Vd[i0]), float(top)


def V2(L, prof, target, G=60, pw=1.5):
    g = (np.arange(G + 1) / G) ** pw
    n = (G + 1) ** 2
    F0 = np.empty((G + 1, G + 1))
    F1 = np.empty((G + 1, G + 1))
    for i in range(G + 1):
        for j in range(G + 1):
            F0[i, j], F1[i, j] = L.F_top(np.array([g[i], g[j]]), prof)
    K0 = L.w[0] * KL(g[None, :], F0.reshape(-1)[:, None])
    K1 = L.w[1] * KL(g[None, :], F1.reshape(-1)[:, None])
    tgt = np.array([[target(g[i], g[j]) for j in range(G + 1)] for i in range(G + 1)])
    V = np.where(tgt, 0.0, np.inf)
    for _ in range(3000):
        W = np.empty((n, G + 1))
        for y1 in range(G + 1):
            W[:, y1] = (K0 + V[None, :, y1]).min(axis=1)
        Vn = np.minimum((K1 + W).min(axis=1).reshape(G + 1, G + 1), V)
        Vn[tgt] = 0
        if np.allclose(Vn, V, atol=1e-12, rtol=0):
            break
        V = Vn
    ia = np.interp(prof[0], g, np.arange(G + 1))
    ib = np.interp(prof[1], g, np.arange(G + 1))
    i0, j0 = int(ia), int(ib)
    i1, j1, u, v = min(i0 + 1, G), min(j0 + 1, G), ia - int(ia), ib - int(ib)
    return float((1 - u) * (1 - v) * V[i0, j0] + u * (1 - v) * V[i1, j0] + (1 - u) * v * V[i0, j1] + u * v * V[i1, j1])


def gump_nb(l):
    return [(6, l), (2, l - 1), (1, l - 2), (2, l + 1), (1, l + 2)]


def fcc_nb(l):
    return [(6, l), (3, l - 1), (3, l + 1)]


def toy_nb(l):
    return [(4, l), (1, l - 1), (1, l - 2), (1, l + 1), (1, l + 2)]


def f12e_nb(l):          # even l: sheet of wall-parallel faces; odd l: layer of perpendicular faces (2 per wall face)
    if l % 2 == 0:
        return [(4, l), (4, l - 1), (4, l + 1)]
    return [(6, l), (2, l - 1), (2, l + 1), (1, l - 2), (1, l + 2)]


SYSTEMS = {  # name: (neighbours, B, S, K, weights, target, measured exponent)
    "gump B45/S345": (gump_nb, {4, 5}, {3, 4, 5}, 12, [1] * 14, lambda a, b: a == 0, "0.209-0.212 (slab)"),
    "gump lattice B456/S3456": (gump_nb, {4, 5, 6}, {3, 4, 5, 6}, 12, [1] * 14, lambda a, b: a == 0, "0.2156"),
    "fcc B45/S345": (fcc_nb, {4, 5}, {3, 4, 5}, 12, [1] * 14, lambda a, b: a == 0, "0.181"),
    "2D rule B34/S234": (toy_nb, {3, 4}, {2, 3, 4}, 8, [1] * 14, lambda a, b: a == 0, "0.346 (ends), 0.41 (ring)"),
    "face12e B45/S345": (f12e_nb, {4, 5}, {3, 4, 5}, 12, [1, 2] * 7, lambda a, b: a == 0 and b == 0, "0.410 per wall face"),
}

def one_layer(nb, B, S, K):
    L = Layers(nb, B, S, K, [1], D=1)
    return V1(L, L.profile())


if __name__ == "__main__":
    G2 = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    for name, (nb, B, S, K, w, tgt, meas) in SYSTEMS.items():
        L = Layers(nb, B, S, K, w)
        prof = L.profile()
        line = f"{name}: bulk {L.bulk:.3f}, profile from the wall {np.round(prof[:4], 3)}"
        if "face12e" not in name:
            v, vd, top = V1(L, prof)
            line += f", V1 = {v:.4f} (its path first rises to density {top:.2f}); decreasing paths only: {vd:.4f}"
        if G2:
            line += f", V2 = {V2(L, prof, tgt, G=G2):.4f}"
        print(line + f"   [measured {meas}]")
    print("one layer over the closure's own bulk density (V1, decreasing paths only, largest density on the path):")
    for name, B, S in (("gump B45/S345", {4, 5}, {3, 4, 5}), ("B45/S34", {4, 5}, {3, 4}), ("B45/S35", {4, 5}, {3, 5}),
                       ("B45/S45", {4, 5}, {4, 5}), ("B4/S345", {4}, {3, 4, 5})):
        print(f"   {name}: " + "%.4f, %.4f, %.2f" % one_layer(gump_nb, B, S, 12))
    print("   Moore B456/S3456 edge (2 in-row, 3 beneath): "
          + "%.4f, %.4f, %.2f" % one_layer(lambda l: [(2, l), (3, l + 1)], {4, 5, 6}, {3, 4, 5, 6}, 8))
    # the closure's one-step statistics against the measured ones (gump, A = 84; critic/to-path.md, round 3, section 2)
    L = Layers(gump_nb, {4, 5}, {3, 4, 5}, 12, [1] * 14)
    prof = L.profile()
    meas = {0.15: 0.573, 0.20: 0.540, 0.25: 0.504, 0.30: 0.466, 0.35: 0.411, 0.40: 0.333, 0.45: 0.228}
    print("gump, local root of the closure's binomial row against the measured root:")
    for x in (0.06, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45):
        F = L.F_top(np.array([x]), prof)[0]
        if F <= x:
            th = float("nan")
        else:
            lo, hi = 1e-9, 30.0
            for _ in range(200):          # root of ln(1 - F(1 - e^-t)) + t x = 0
                mid = 0.5 * (lo + hi)
                if np.log(1 - F * (1 - np.exp(-mid))) + mid * x < 0:
                    lo = mid
                else:
                    hi = mid
            th = 0.5 * (lo + hi)
        print(f"   x = {x:.2f}: F(x) - x = {F - x:+.3f}, closure root {th:.3f}, measured {meas.get(x, '(0.60 at x = 0.06-0.10)')}")
