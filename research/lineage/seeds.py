#!/usr/bin/env python3
"""Deterministic O_h-symmetric structured seeds (cell lists in doubled coordinates).

A seed is named  FAMILY:N:K  and centred on a cube centre (N odd, c = 0) or a vertex (N even, c = (1,1,1)),
exactly like `gump --cube N`.
  cube:N:0       the closed cube of side N (= gump --cube N)
  notch:N:K      closed cube minus the K-th O_h orbit of its cells (orbits sorted by (|p-c|^2, canonical rep))
  decor:N:K      closed cube plus the K-th O_h orbit of dead cells in the shell max|p-c| in (N, N+2]
  nest:N:K       hollow shell of side N (its surface faces) + the inner shells of sides N-2, N-4, ... selected by the
                 bits of K (bit j = side N-2-2j), plus, if bit 7 is set, the closed cube of the largest selected side
  sc:N:K         closed cube of side N plus the hollow shell of side N+2, minus the K-th O_h orbit of that shell's
                 cells (orbits sorted outermost first; K = -1: nothing removed). sc2:N:A:B removes two. Side 13 + shell 15 starts at r = 37.
  hollow:N:K     closed cube minus all faces strictly inside the concentric cube of side K (K < N, same parity)
  python3 research/lineage/seeds.py FAMILY:N:K OUT.txt     writes a gump cell list
"""
import itertools, sys

def centre(n): return (0, 0, 0) if n % 2 else (1, 1, 1)

OPS = [(perm, sg) for perm in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)]

def orbit(p, c):
    q = [p[i] - c[i] for i in range(3)]
    return {tuple(c[i] + sg[i] * q[perm[i]] for i in range(3)) for perm, sg in OPS}

def valid(p): return sum(x & 1 for x in p) == 1

def box_cells(c, h):
    """valid cells with all coordinates in [c-h, c+h] (h odd: a closed cube of side h)"""
    r = [range(c[i] - h, c[i] + h + 1) for i in range(3)]
    return {p for p in itertools.product(*r) if valid(p)}

def shell_cells(c, h):
    """surface faces of the cube [c-h, c+h]^3: cells lying in one of its six bounding planes, inside the square"""
    return {p for p in box_cells(c, h) if any(abs(p[i] - c[i]) == h and p[i] % 2 for i in range(3))}

def orbits_of(cells, c):
    seen, out = set(), []
    for p in sorted(cells, key=lambda p: (sum((p[i] - c[i]) ** 2 for i in range(3)), p)):
        if p in seen: continue
        o = orbit(p, c); seen |= o; out.append(o)
    return out

def make(spec):
    fam, n, k = spec.split(":")[:3]; n, k = int(n), int(k); c = centre(n)
    cube = box_cells(c, n)
    if fam == "cube": return cube
    if fam == "notch": return cube - orbits_of(cube, c)[k]
    if fam == "decor":
        ring = box_cells(c, n + 2) - cube
        return cube | orbits_of(ring, c)[k]
    if fam == "sc":
        sh = shell_cells(c, n + 2); cells = cube | sh
        if k >= 0: cells -= orbits_of(sh, c)[::-1][k]
        return cells
    if fam == "sc2":                                    # sc2:N:A:B  - as sc, two shell orbits A < B removed
        a, b = k, int(spec.split(":")[3]); sh = shell_cells(c, n + 2); o = orbits_of(sh, c)[::-1]
        return (cube | sh) - o[a] - o[b]
    if fam == "hollow":
        assert k < n and (n - k) % 2 == 0
        inner = {p for p in box_cells(c, k) if all(abs(p[i] - c[i]) < k for i in range(3))}
        return cube - inner
    if fam == "nest":
        cells = shell_cells(c, n); sides = [n - 2 - 2 * j for j in range(7) if k >> j & 1 and n - 2 - 2 * j > 0]
        for h in sides: cells |= shell_cells(c, h)
        if k >> 7 & 1 and sides: cells |= box_cells(c, max(sides))
        return cells
    raise ValueError(spec)

def write(spec, path):
    cells = make(spec)
    with open(path, "w") as f:
        f.write(f"# gump cells v1: seed {spec}\n")
        for p in sorted(cells): f.write(f"{p[0]} {p[1]} {p[2]}\n")
    return len(cells)

if __name__ == "__main__":
    print(write(sys.argv[1], sys.argv[2]))
