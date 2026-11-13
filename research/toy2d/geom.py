"""Graphs for t2d.c: lattices, vessels, watched lines, events, seeding orbits.

Lattices (neighbourhood offsets on Z^2):
  moore  8 neighbours                   confinement: birth >= 4 (axis and diagonal half-planes)
  vn     4 neighbours (von Neumann)     birth >= 2 confines axis half-planes, >= 3 also diagonals
  hex    6 neighbours (axial coords)    birth >= 3 confines the three lattice-line half-planes
  cross2 8 neighbours (+-1,0),(+-2,0),(0,+-1),(0,+-2)   birth >= 3 confines axis half-planes (not diagonals)
Vessels:
  box L      L x L cells, everything outside dead forever (a valid vessel when births are confined)
  strip W L  W rows, L columns, periodic in x; rows outside dead forever
Symmetry of the seed (orbits of the seeding map; the dynamics preserves it):
  none, mx (x -> -x), my, mxy, c2, c4, d4, diag (x <-> y), t<k> (strip: translation by L/k)
Lines watched: box -> the 4 edges (flag 1 = histogram), strip -> every row (edges flagged 1).
Events: box -> each edge empty; strip -> each edge row empty (events 0, 1), then each interior pair of
adjacent rows empty (FIREWALL rows: a firewall), events 2...
"""
import os, struct, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, '..', 'scratch', 'toy2d', 't2d')
SCR = os.path.join(HERE, '..', 'scratch', 'toy2d')

OFFS = {
    'moore': [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy) != (0, 0)],
    'vn': [(1, 0), (-1, 0), (0, 1), (0, -1)],
    'hex': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)],
    'cross2': [(1, 0), (-1, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2)],
}
# dead rows needed for a firewall (a cell in it sees < bmin live cells whatever lies outside)
FIREWALL = {'moore': 2, 'vn': 2, 'hex': 2, 'cross2': 3}


def build(lattice, vessel, dims, sym='none'):
    offs = OFFS[lattice]
    if vessel == 'box':
        L = dims[0]; Wd, Lx, per = L, L, False
    elif vessel == 'strip':
        Wd, Lx = dims; per = True
    else:
        raise ValueError(vessel)
    idx = -np.ones((Wd, Lx), int)
    cells = [(y, x) for y in range(Wd) for x in range(Lx)]
    for i, (y, x) in enumerate(cells):
        idx[y, x] = i
    N = len(cells)
    nb = np.full((N, len(offs)), -1, np.int32)
    for i, (y, x) in enumerate(cells):
        for k, (dx, dy) in enumerate(offs):
            yy, xx = y + dy, x + dx
            if per:
                xx %= Lx
            if 0 <= yy < Wd and 0 <= xx < Lx:
                nb[i, k] = idx[yy, xx]
    # seeding orbits
    def images(y, x):
        out = {(y, x)}
        if sym == 'none':
            pass
        elif sym == 'mx':
            out.add((y, (-x - 1) % Lx if per else Lx - 1 - x))
        elif sym == 'my':
            out.add((Wd - 1 - y, x))
        elif sym == 'mxy':
            xm = (-x - 1) % Lx if per else Lx - 1 - x
            out |= {(Wd - 1 - y, x), (y, xm), (Wd - 1 - y, xm)}
        elif sym == 'c2':
            xm = (-x - 1) % Lx if per else Lx - 1 - x
            out.add((Wd - 1 - y, xm))
        elif sym in ('c4', 'd4', 'diag'):
            assert vessel == 'box'
            Lm = Lx - 1
            rots = [(y, x), (x, Lm - y), (Lm - y, Lm - x), (Lm - x, y)]
            if sym == 'diag':
                out.add((x, y))
            elif sym == 'c4':
                out |= set(rots)
            else:
                out |= set(rots) | {(b, a) for (a, b) in rots}
        elif sym.startswith('t'):
            k = int(sym[1:]); assert per and Lx % k == 0
            out |= {(y, (x + j * Lx // k) % Lx) for j in range(k)}
        else:
            raise ValueError(sym)
        return out
    orb = -np.ones(N, np.int32); R = 0
    for i, (y, x) in enumerate(cells):
        if orb[i] >= 0:
            continue
        for (yy, xx) in images(y, x):
            orb[idx[yy, xx]] = R
        R += 1
    lines, events = [], []
    if vessel == 'box':
        L = Wd
        lines = [(1, [idx[0, x] for x in range(L)]), (1, [idx[L - 1, x] for x in range(L)]),
                 (1, [idx[y, 0] for y in range(L)]), (1, [idx[y, L - 1] for y in range(L)])]
        events = [[0], [1], [2], [3]]
    else:
        for y in range(Wd):
            lines.append((1 if y in (0, Wd - 1) else 0, [idx[y, x] for x in range(Lx)]))
        fw = FIREWALL[lattice]
        events = [[0], [Wd - 1]] + [list(range(y, y + fw)) for y in range(1, Wd - fw)]
    return dict(N=N, nb=nb, orb=orb, R=R, lines=lines, events=events, shape=(Wd, Lx), idx=idx)


def write(g, fn):
    with open(fn, 'wb') as f:
        f.write(struct.pack('<ii', g['N'], g['nb'].shape[1]))
        f.write(g['nb'].astype('<i4').tobytes())
        f.write(g['orb'].astype('<i4').tobytes())
        f.write(struct.pack('<ii', g['R'], len(g['lines'])))
        for flag, cl in g['lines']:
            f.write(struct.pack('<ii', flag, len(cl)))
            f.write(np.asarray(cl, '<i4').tobytes())
        f.write(struct.pack('<i', len(g['events'])))
        for ev in g['events']:
            f.write(struct.pack('<i', len(ev)))
            f.write(np.asarray(ev, '<i4').tobytes())


def compile_bin(W=4):
    os.makedirs(SCR, exist_ok=True)
    src = os.path.join(HERE, 't2d.c')
    out = BIN if W == 4 else BIN + f'_w{W}'
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', f'-DW={W}', '-o', out, src, '-lm'])
    return out


def graph_file(lattice, vessel, dims, sym='none'):
    fn = os.path.join(SCR, 'g_%s_%s_%s_%s.bin' % (lattice, vessel, 'x'.join(map(str, dims)), sym))
    if not os.path.exists(fn):
        os.makedirs(SCR, exist_ok=True)
        write(build(lattice, vessel, dims, sym), fn)
    return fn


def mask(counts):
    return sum(1 << k for k in counts)


def parse_rule(s):
    """'B45/S345' -> (Bmask, Smask)"""
    b, s = s.upper().split('/')
    return mask(int(c) for c in b[1:]), mask(int(c) for c in s[1:])


def life(rule, lattice, vessel, dims, p, seed, Tmax, sym='none', W=4):
    B, S = parse_rule(rule) if isinstance(rule, str) else rule
    exe = compile_bin(W)
    fn = graph_file(lattice, vessel, dims, sym)
    out = subprocess.run([exe, 'life', fn, str(B), str(S), str(p), str(seed), str(Tmax)],
                         capture_output=True, text=True, check=True).stdout
    a = np.array([list(map(int, l.split())) for l in out.strip().split('\n')])
    return a  # columns: settle, final pop, event times...


def qsd(rule, lattice, vessel, dims, p, seed, T0, gens, out, sym='none', W=4):
    B, S = parse_rule(rule) if isinstance(rule, str) else rule
    exe = compile_bin(W)
    fn = graph_file(lattice, vessel, dims, sym)
    subprocess.run([exe, 'qsd', fn, str(B), str(S), str(p), str(seed), str(T0), str(gens), out], check=True)
    return read_qsd(out)


def read_qsd(fn):
    d = {}
    for line in open(fn):
        k, *v = line.split()
        v = [float(t) for t in v]
        d[k] = v[0] if len(v) == 1 else np.array(v)
    return d


if __name__ == '__main__':
    print(compile_bin())
