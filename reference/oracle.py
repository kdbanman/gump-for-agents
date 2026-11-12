#!/usr/bin/env python3
"""Tiny, deliberately naive, legacy-faithful oracle for the gump automaton (numpy only).

This is the independent ground truth that faster engines are checked against.
It mirrors the original Processing implementation's semantics exactly, including
its array-index torus (see docs/AUTOMATON.md, "Legacy semantics"). Keep it simple;
do not optimise it.

  oracle.py legacy-cube H [--compare LOG] [--gens N]   closed-cube seed as legacy generate(mode=1, fraction=0.38)
  oracle.py legacy-key  H K [--gens N]                 legacy number-key seed (K in 1..9), H is habitatSize
Prints "generation population" lines (generation 0 = the seed) unless --compare is given.
With --compare, also runs the same seed in a padded (effectively infinite) box in lockstep
and reports the first generation, if any, at which the legacy torus changes the outcome.
"""
import argparse, math, sys, time
import numpy as np

BIRTH, SURVIVE = (4, 5), (3, 4, 5)


def offsets(axis):
    """The 12 neighbour offsets (doubled coordinates) of a face whose normal is `axis`."""
    a = axis
    b, c = [i for i in range(3) if i != a]
    offs = []
    for sb in (2, -2):
        for sc in (2, -2):          # 4 coplanar faces touching only at a corner
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):      # 8 perpendicular faces sharing an edge
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs


def masks(H):
    """masks[a] = boolean array of valid cells with normal axis a (coordinate a odd, others even)."""
    par = np.indices((H, H, H)) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def step(h, m, birth=BIRTH, survive=SURVIVE):
    """One generation on the legacy array-index torus. Invalid sites are never written."""
    new = np.zeros_like(h)
    for a in range(3):
        cnt = np.zeros(h.shape, np.int8)
        for o in offsets(a):
            cnt += np.roll(h, tuple(-d for d in o), axis=(0, 1, 2))
        born = (h == 0) & np.isin(cnt, birth)
        stay = (h == 1) & np.isin(cnt, survive)
        new[m[a] & (born | stay)] = 1
    return new


def fill_box(H, lo, hi, m):
    """All valid cells with every doubled coordinate in [lo, hi] (inclusive)."""
    h = np.zeros((H, H, H), np.int8)
    box = np.zeros((H, H, H), bool)
    box[lo:hi + 1, lo:hi + 1, lo:hi + 1] = True
    h[(m[0] | m[1] | m[2]) & box] = 1
    return h


def legacy_seed_span(H, fraction=0.38):
    """getSeedStart/getSeedEnd from the original, with float32 arithmetic and Java rounding."""
    f = np.float32
    jround = lambda v: int(math.floor(f(v) + f(0.5)))
    seed_len = f(H) * f(fraction)
    lo = jround(f(H // 2) - seed_len / f(2)); lo += (lo % 2 == 0); lo = min(lo, H - 1)
    hi = jround(f(H // 2) + seed_len / f(2)); hi += (hi % 2 == 0); hi = min(hi, H - 1)
    return lo, hi


def legacy_key_span(H, key):
    """ConstructionCamera.generateFull(key - 40) with key the ASCII digit: seedSize = key + 8."""
    size = key + 8
    lo = H // 2 - size // 2
    return lo, lo + size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["legacy-cube", "legacy-key"])
    ap.add_argument("H", type=int)
    ap.add_argument("key", type=int, nargs="?")
    ap.add_argument("--gens", type=int, default=None)
    ap.add_argument("--compare", default=None, help="legacy log file with 'generation population' lines")
    a = ap.parse_args()

    H = a.H
    lo, hi = legacy_seed_span(H) if a.mode == "legacy-cube" else legacy_key_span(H, a.key)
    m = masks(H)
    h = fill_box(H, lo, hi, m)
    if not a.compare:
        print(0, int(h.sum()))
        g = 0
        while a.gens is None or g < a.gens:
            n = step(h, m); g += 1
            print(g, int(n.sum()))
            if a.gens is None and (n == h).all():
                break
            h = n
        return

    ref = [int(l.split()[1]) for l in open(a.compare) if l.strip()]
    pad = 12                                          # even shift keeps coordinate parity
    HP = H + 2 * pad + (H % 2)                        # padded box must be a proper (even) torus
    mp = masks(HP)
    hp = fill_box(HP, lo + pad, hi + pad, mp)
    gens = len(ref) - 1 if a.gens is None else min(a.gens, len(ref) - 1)
    print(f"H={H} seed span {lo}..{hi} seed population {int(h.sum())}; comparing {gens} generations", flush=True)
    mism = 0; diverged = None; edge = None; t = time.time()
    for g in range(1, gens + 1):
        h = step(h, m); hp = step(hp, mp)
        pop, popp = int(h.sum()), int(hp.sum())
        if pop != ref[g]:
            mism += 1
            if mism <= 3: print(f"  MISMATCH vs legacy log at gen {g}: oracle {pop}, log {ref[g]}", flush=True)
        if diverged is None and pop != popp:
            diverged = g; print(f"  torus changes the outcome: first population difference vs padded box at gen {g}", flush=True)
        if edge is None and (h[[0, -1]].any() or h[:, [0, -1]].any() or h[:, :, [0, -1]].any()):
            edge = g; print(f"  live cell first reaches the outermost array layer at gen {g}", flush=True)
        if g % 20000 == 0: print(f"  ... gen {g} ({time.time() - t:.0f}s)", flush=True)
    print(f"done: {gens} gens in {time.time() - t:.0f}s; mismatches vs log: {mism}; final population {pop} "
          f"(padded box: {popp}); torus divergence: {diverged}; edge contact: {edge}")


if __name__ == "__main__":
    main()
