"""Tiny numpy stepper for pictures and spot checks (Moore lattice, dead outside a W x L box, optional
periodic x). step(x, B, S, periodic) -> next state."""
import numpy as np
import geom


def counts(x, periodic=False):
    W, L = x.shape
    p = np.zeros((W + 2, L + 2), np.int16)
    p[1:-1, 1:-1] = x
    if periodic:
        p[1:-1, 0] = x[:, -1]; p[1:-1, -1] = x[:, 0]
    n = np.zeros((W, L), np.int16)
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            if dy == 1 and dx == 1:
                continue
            n += p[dy:dy + W, dx:dx + L]
    return n


def step(x, B, S, periodic=False):
    n = counts(x, periodic)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1).astype(np.uint8)


def run(rule, x, gens, periodic=False):
    B, S = geom.parse_rule(rule)
    out = [x]
    for _ in range(gens):
        x = step(x, B, S, periodic); out.append(x)
    return np.array(out)
