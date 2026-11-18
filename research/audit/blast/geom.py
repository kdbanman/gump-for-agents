#!/usr/bin/env python3
"""Vessels for the audit of research/blast, built from the lattice definition with reference/oracle.py's own
neighbour offsets, and the check of this directory's stepper (fd.c) against the oracle.

  slab torus (h,k,d): 8 {111} layers t = (x+y+z-1)/2 = 0..7 (doubled coordinates), periodic under the cube steps
      (a, b, -a-b) for (a, b) in the lattice Z(h,k) + Z(0,d); 3hd cells a layer; faces are layers 0 and 7.
  hull R: the octahedron max over sign patterns s of s.p <= R (R odd, centred on a cube centre); 8 faces s.p = R.

    python3 research/audit/blast/geom.py slab 1 4 21         # writes research/scratch/audit_blast/slab_1_4_21.{bin,npz}
    python3 research/audit/blast/geom.py hull 11
    python3 research/audit/blast/geom.py check slab 1 4 21 [GENS]   # oracle = numpy on the graph = fd.c, state for state
    python3 research/audit/blast/geom.py check hull 11 [GENS]       # (default 1200 generations) + negative control

File format (int32 LE): n; nbr[n][12] (n = outside, always dead); nfaces; nlay; per face, per layer: size, cells.
Layer 0 of a face is the face layer, layer j the layer j steps beneath it.  The .npz holds the doubled coordinates.
"""
import itertools, os, struct, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_blast')
NLAY = 6


def axis_of(p):
    return [i for i in range(3) if p[i] % 2][0]


def slab(h, k, d, T=8):
    def key(p):                                    # canonical representative of p modulo the period lattice
        x, y, z = p
        t = (x + y + z - 1) // 2
        m = x // (2 * h)
        x -= 2 * h * m; y -= 2 * k * m
        y %= 2 * d
        return (x, y, 2 * t + 1 - x - y)
    cells = []
    for t in range(T):
        for x in range(2 * h):
            for y in range(2 * d):
                p = (x, y, 2 * t + 1 - x - y)
                if sum(c % 2 for c in p) == 1:
                    assert key(p) == p
                    cells.append(p)
    idx = {p: i for i, p in enumerate(cells)}
    n = len(cells)
    assert n == 3 * h * d * T
    nb = np.full((n, 12), n, np.int32)
    for i, p in enumerate(cells):
        for j, o in enumerate(oracle.offsets(axis_of(p))):
            q = tuple(a + b for a, b in zip(p, o))
            if 0 <= (sum(q) - 1) // 2 < T:
                nb[i, j] = idx[key(q)]
    lay = [[i for i, p in enumerate(cells) if (sum(p) - 1) // 2 == t] for t in range(T)]
    faces = [[lay[j] for j in range(NLAY)], [lay[T - 1 - j] for j in range(NLAY)]]
    return cells, nb, faces, key


def hull(R):
    assert R % 2 == 1
    sig = list(itertools.product((1, -1), repeat=3))
    rng = range(-R - 1, R + 2)
    cells = [p for p in itertools.product(rng, rng, rng)
             if sum(c % 2 for c in p) == 1 and max(sum(a * b for a, b in zip(s, p)) for s in sig) <= R]
    idx = {p: i for i, p in enumerate(cells)}
    n = len(cells)
    nb = np.full((n, 12), n, np.int32)
    for i, p in enumerate(cells):
        for j, o in enumerate(oracle.offsets(axis_of(p))):
            nb[i, j] = idx.get(tuple(a + b for a, b in zip(p, o)), n)
    faces = []
    for s in sig:
        v = [sum(a * b for a, b in zip(s, p)) for p in cells]
        faces.append([[i for i in range(n) if v[i] == R - 2 * j] for j in range(NLAY)])
    return cells, nb, faces, None


def write(name, cells, nb, faces):
    os.makedirs(SCR, exist_ok=True)
    n = len(cells)
    out = [n] + nb.reshape(-1).tolist() + [len(faces), NLAY]
    for f in faces:
        for l in f:
            out += [len(l)] + list(l)
    path = os.path.join(SCR, name + '.bin')
    open(path, 'wb').write(struct.pack(f'<{len(out)}i', *out))
    mx = max(len(l) for f in faces for l in f)
    fa = -np.ones((len(faces), NLAY, mx), np.int32)
    for i, f in enumerate(faces):
        for j, l in enumerate(f):
            fa[i, j, :len(l)] = l
    np.savez(os.path.join(SCR, name + '.npz'), cells=np.array(cells), nb=nb, faces=fa)
    return path


def vessel(kind, *a):
    if kind == 'slab':
        cells, nb, faces, key = slab(*a); name = 'slab_' + '_'.join(map(str, a))
    else:
        cells, nb, faces, key = hull(*a); name = f'hull_{a[0]}'
    return name, cells, nb, faces, key


def build_fd():
    exe = os.path.join(SCR, 'fd')
    src = os.path.join(HERE, 'fd.c')
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', exe, src])
    return exe


def check(kind, a, gens=1200, neg=False):
    """Oracle on its array-index torus against a plain numpy stepper on the graph and against fd.c (trace mode)."""
    name, cells, nb, faces, key = vessel(kind, *a)
    n = len(cells)
    path = write(name, cells, nb, faces)
    if kind == 'slab':
        h, k, d = a
        N = h * d                                   # N Z^2 lies in the period lattice; the slab recurs every N layers
        assert N >= 11
        H = 2 * N
        pos = [[] for _ in range(n)]                # every site of the cubic torus that is a copy of slab cell i
        idx = {p: i for i, p in enumerate(cells)}
        for q in itertools.product(range(H), repeat=3):
            if sum(c % 2 for c in q) != 1:
                continue
            s = sum(q) % H
            if (s - 1) // 2 >= 8:
                continue
            pos[idx[key((q[0], q[1], s - q[0] - q[1]))]].append(q)
        assert len({len(x) for x in pos}) == 1
    else:
        R = a[0]
        H = 2 * (R + 6)
        H += H % 4                                  # centre H/2 even: a cube centre
        pos = [[tuple(c + H // 2 for c in p)] for p in cells]
    ncopy = len(pos[0])
    flat = np.array([np.ravel_multi_index(np.array(x).T, (H, H, H)) for x in pos])        # n x ncopy
    m = oracle.masks(H)
    rng = np.random.default_rng(12345 + sum(a))
    live = rng.random(n) < 0.4
    grid = np.zeros(H ** 3, np.int8); grid[flat[live].ravel()] = 1; grid = grid.reshape(H, H, H)
    x = np.zeros(n + 1, np.int8); x[:n] = live
    NB = nb.copy()
    path_c = path
    if neg:                                         # one swapped neighbour entry: must fail
        i0 = next(i for i in range(n) if NB[i, 0] != NB[i + 1, 0] and NB[i, 0] < n and NB[i + 1, 0] < n)
        NB[i0, 0] = nb[i0 + 1, 0]
        path_c = write(name + '_neg', cells, NB, faces)
    ini = os.path.join(SCR, f'ini_{os.getpid()}.txt')
    open(ini, 'w').write('\n'.join(map(str, np.nonzero(live)[0])) + '\n')
    tr = os.path.join(SCR, f'trace_{os.getpid()}.bin')
    subprocess.check_call([build_fd(), path_c, 'trace', ini, str(gens), tr])
    ctrace = np.unpackbits(np.fromfile(tr, np.uint8).reshape(gens + 1, -1), axis=1, bitorder='little')[:, :n]
    os.remove(ini); os.remove(tr)
    bad = None; pops = []
    for g in range(gens + 1):
        og = grid.reshape(-1)
        cop = og[flat]                              # the oracle's state on every copy of every cell
        same = (cop == cop[:, :1]).all() and int(og.sum()) == int(cop.sum())      # periodic, and nothing outside
        if not same or not (cop[:, 0] == x[:n]).all() or not (ctrace[g] == cop[:, 0]).all():
            bad = g; break
        pops.append(int(x.sum()))
        cnt = x[NB].sum(1)
        x = np.append(np.where(x[:n] == 1, (cnt >= 3) & (cnt <= 5), (cnt >= 4) & (cnt <= 5)).astype(np.int8), 0)
        grid = oracle.step(grid, m)
    print(f'check {kind} {a}: n = {n}, face layer {len(faces[0][0])} cells, {len(faces)} faces, oracle H = {H}, '
          f'{ncopy} copies{"; NEGATIVE CONTROL" if neg else ""}: '
          f'{"MATCH over %d generations" % gens if bad is None else "MISMATCH at generation %d" % bad}'
          f' (oracle = numpy on the graph = fd.c trace); populations {pops[0]}..{pops[-1]}, {len(set(pops))} distinct',
          flush=True)
    return bad is None


if __name__ == '__main__':
    if sys.argv[1] == 'check':
        kind = sys.argv[2]
        na = 3 if kind == 'slab' else 1
        a = tuple(int(v) for v in sys.argv[3:3 + na])
        gens = int(sys.argv[3 + na]) if len(sys.argv) > 3 + na else 1200
        ok = check(kind, a, gens)
        okneg = not check(kind, a, min(gens, 300), neg=True)
        print('PASS' if ok and okneg else 'FAIL')
        sys.exit(0 if ok and okneg else 1)
    kind = sys.argv[1]
    a = tuple(int(v) for v in sys.argv[2:])
    name, cells, nb, faces, _ = vessel(kind, *a)
    print(write(name, cells, nb, faces), len(cells), 'cells;', len(faces), 'faces; layer sizes of face 0:',
          [len(l) for l in faces[0]])
