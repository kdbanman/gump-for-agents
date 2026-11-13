"""Critic's lab, part 2: the 2D rule (B34/S234 on the range-2 cross) on small strips and boxes, exactly.

Vessels (as research/toy2d/geom.py): strip H x L = H rows, L columns, periodic in x, rows outside dead for ever;
box H x L = no wrap, everything outside dead for ever. Cell (y, x) has index y*L + x. Edges: rows 0 and H-1
(and, in a box, columns 0 and L-1).

  python3 toy2d_lab.py selftest          stepper vs research/experiments/toy2d_check.py (strip) and vs the
                                         strip-with-three-dead-columns embedding (box); full_map vs both
  python3 toy2d_lab.py census strip H L  exhaustive fate of every state of a small vessel
  python3 toy2d_lab.py census box H L
"""
import os, sys, importlib.util
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact

B, S = (3, 4), (2, 3, 4)
OFFS = [(0, 1), (0, -1), (0, 2), (0, -2), (1, 0), (-1, 0), (2, 0), (-2, 0)]   # (dy, dx)


def nbrs(H, L, periodic):
    nb = []
    for y in range(H):
        for x in range(L):
            v = []
            for dy, dx in OFFS:
                yy, xx = y + dy, x + dx
                if periodic:
                    xx %= L
                if 0 <= yy < H and 0 <= xx < L:
                    v.append(yy * L + xx)
            nb.append(v)        # on very short rings (L <= 4) a neighbour can repeat: kept, as a multigraph
    return nb


def step_grid(x, periodic):
    """x: (H, L) 0/1 array -> next state, by the neighbour lists (slow, obviously right)."""
    H, L = x.shape
    nb = nbrs(H, L, periodic)
    f = x.reshape(-1)
    out = np.zeros(H * L, np.uint8)
    for i, v in enumerate(nb):
        n = sum(int(f[j]) for j in v)
        out[i] = (n in S) if f[i] else (n in B)
    return out.reshape(H, L)


def to_state(x):
    return int(sum(int(b) << i for i, b in enumerate(x.reshape(-1))))


def from_state(s, H, L):
    return np.array([(s >> i) & 1 for i in range(H * L)], np.uint8).reshape(H, L)


def rows(H, L):
    return [[y * L + x for x in range(L)] for y in range(H)]


def cols(H, L):
    return [[y * L + x for y in range(H)] for x in range(L)]


def living_mask(kind, H, L):
    """Every edge occupied: rows 0 and H-1, and for a box columns 0 and L-1."""
    N = H * L
    r, c = rows(H, L), cols(H, L)
    m = exact.any_alive(N, r[0]) & exact.any_alive(N, r[H - 1])
    if kind == 'box':
        m &= exact.any_alive(N, c[0]) & exact.any_alive(N, c[L - 1])
    return m


def cut_mask(H, L):
    """Strip only: three adjacent columns empty (a transverse firewall: the ring is cut open)."""
    N = H * L
    c = cols(H, L)
    occ = [exact.any_alive(N, c[x]) for x in range(L)]
    m = np.zeros(1 << N, bool)
    for x in range(L):
        m |= ~(occ[x] | occ[(x + 1) % L] | occ[(x + 2) % L])
    return m


def census(kind, H, L, verbose=True):
    N = H * L
    nb = nbrs(H, L, kind == 'strip')
    F = exact.full_map(nb, B, S)
    living = living_mask(kind, H, L)
    T = exact.death_times(F, living)
    cyc = exact.cyclic(F)
    per = exact.periods(F, cyc)
    imm = T < 0
    res = dict(kind=kind, H=H, L=L, N=N, states=1 << N,
               dead_at_0=int((T == 0).sum()), immortal_basin=int(imm.sum()),
               cyclic_states=int(cyc.sum()), immortal_cyclic=int((cyc & imm).sum()),
               periods=per, immortal_periods=exact.periods(F, cyc & imm) if (cyc & imm).any() else {},
               death_hist=np.bincount(T[T >= 0]).tolist())
    if verbose:
        mort = T[T > 0]
        print(f"{kind} {H}x{L}: N={N}, states {1 << N}")
        print(f"  an edge already empty at t=0: {res['dead_at_0']}")
        print(f"  mortal (lose an edge at some t>=1): {len(mort)}, max death time {mort.max() if len(mort) else 0}, "
              f"mean {mort.mean() if len(mort) else 0:.4f}")
        print(f"  immortal basin (never lose an edge: settle into debris touching every edge): {res['immortal_basin']} "
              f"= {res['immortal_basin'] / (1 << N):.6f} of all states")
        print(f"  cyclic states {res['cyclic_states']} by period {per}")
        print(f"  immortal cyclic states {res['immortal_cyclic']} by period {res['immortal_periods']}")
        print(f"  death-time histogram (t=0,1,2,...): {res['death_hist']}")
    return res, F, T


def _load_lead_stepper():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, '..', '..', '..', '..', 'experiments', 'toy2d_check.py'))
    src = open(path).read()
    src = src[:src.index('def run(')]            # the step function only; the file runs a simulation on import
    ns = {}
    exec(compile(src, path, 'exec'), ns)
    return ns['step']


def selftest():
    lead_step = _load_lead_stepper()
    rng = np.random.default_rng(12345)
    ok = True
    # 1. strip: my list stepper vs the lead's numpy stepper, 200 generations, several shapes and densities
    for (H, L) in [(3, 5), (4, 7), (6, 9), (16, 12), (5, 6)]:
        for rho in (0.3, 0.5, 0.7):
            x = (rng.random((H, L)) < rho).astype(np.uint8)
            y = x.copy()
            for t in range(200):
                x = step_grid(x, True)
                y = lead_step(y[None])[0][0]
                if not (x == y).all():
                    ok = False; print('MISMATCH strip', H, L, rho, t); break
    print('strip stepper vs research/experiments/toy2d_check.py step: 15 runs x 200 generations',
          'identical' if ok else 'FAILED')
    # 2. box = strip of length L+3 whose last three columns are dead (they stay dead, and nothing crosses them)
    ok2 = True
    for (H, L) in [(4, 4), (5, 7), (8, 8), (3, 6)]:
        for rho in (0.3, 0.5, 0.7):
            x = (rng.random((H, L)) < rho).astype(np.uint8)
            y = np.zeros((H, L + 3), np.uint8); y[:, :L] = x
            for t in range(200):
                x = step_grid(x, False)
                y = lead_step(y[None])[0][0]
                if y[:, L:].any() or not (x == y[:, :L]).all():
                    ok2 = False; print('MISMATCH box', H, L, rho, t); break
    print('box stepper vs the same stepper on a strip with three dead columns: 12 runs x 200 generations',
          'identical' if ok2 else 'FAILED')
    # 3. full_map vs the steppers, every state of two small vessels
    ok3 = True
    for kind, H, L in (('strip', 3, 5), ('box', 3, 4), ('strip', 2, 7)):
        nb = nbrs(H, L, kind == 'strip')
        F = exact.full_map(nb, B, S)
        for s in range(1 << (H * L)):
            x = from_state(s, H, L)
            if kind == 'strip':
                y = lead_step(x[None])[0][0]
            else:
                z = np.zeros((H, L + 3), np.uint8); z[:, :L] = x
                y = lead_step(z[None])[0][0][:, :L]
            if to_state(y) != int(F[s]) or exact.step_state(nb, B, S, s) != int(F[s]):
                ok3 = False; print('MISMATCH full_map', kind, H, L, s); break
    print('full_map vs the lead stepper, every state of strip 3x5, box 3x4, strip 2x7:', 'identical' if ok3 else 'FAILED')
    # 4. census against the numbers recorded by the exponent agent's independent fg.c (data/fg_summary.json)
    import json
    here = os.path.dirname(os.path.abspath(__file__))
    fg = os.path.normpath(os.path.join(here, '..', '..', '..', 'exponent', 'data', 'fg_summary.json'))
    ok4 = True
    if os.path.exists(fg):
        rec = {(r['kind'], r['H'], r['L']): r for r in json.load(open(fg))}
        for key in [('strip', 2, 5), ('strip', 2, 7), ('strip', 2, 8)]:
            if key not in rec:
                continue
            res, F, T = census(*key, verbose=False)
            r = rec[key]
            same = (res['cyclic_states'] == r['cyclic_states'] and res['immortal_cyclic'] == r['immortal_states']
                    and abs(res['immortal_basin'] / res['states'] - r['basin_frac']) < 1e-12
                    and abs(res['dead_at_0'] / res['states'] - r['dead_at_0']) < 1e-12)
            print('  census', key, 'vs fg_summary.json:', 'same' if same else 'DIFFERENT',
                  f"(cyclic {res['cyclic_states']}, immortal cyclic {res['immortal_cyclic']}, "
                  f"basin {res['immortal_basin'] / res['states']:.6f})")
            ok4 &= same
    allok = ok and ok2 and ok3 and ok4
    print('ALL OK' if allok else 'FAILED')
    return allok


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'selftest':
        sys.exit(0 if selftest() else 1)
    elif len(sys.argv) == 5 and sys.argv[1] == 'census':
        census(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        print(__doc__)
