"""The register (README section 9) on the oracle, with operation sequences the study did not run.

    python3 register_check.py

Object(w) and the two operations exactly as research/signals/objects/register-BBp.json defines them (frame cells,
B and B' units on [ua, ub), wall at w; W = remove `write` at an even generation, E = remove `erase` at an odd one).
The cubic torus H = 80 of the study's own verifier.  A schedule is a list of (generation, op); after the last op
the run goes on to an even generation >= last + 80 and the WHOLE state is compared with Object(w0 - #W + #E), and
also 2 generations later (still standing).  The claim predicts a match in every case where the wall stays inside
the B/B' stretch.
"""
import json, os, sys
import numpy as np
import gs
oracle = gs.oracle
ob = json.load(open(os.path.join(gs.ROOT, 'research/signals/objects/register-BBp.json')))
H = 2 * ob['cubes']; m = oracle.masks(H)
frame = [tuple(c) for c in ob['frame']]; Bc = [tuple(c) for c in ob['B']]; Bp = [tuple(c) for c in ob['Bp']]
ua, ub, w0 = ob['ua'], ob['ub'], ob['w0']; WR = tuple(ob['write']); ER = tuple(ob['erase'])


def obj(w):
    s = set(frame)
    for u in range(ua, ub):
        s |= {gs.tr(c, u) for c in (Bc if u < w else Bp)}
    return gs.to_arr(s, (H, H, H))


def run(sched):
    """sched: list of (generation, 'W'|'E'), increasing generations; W at even, E at odd generations."""
    h = obj(w0); t = 0; w = w0
    for g, op in sched:
        assert (g % 2 == 0) == (op == 'W')
        while t < g:
            h = oracle.step(h, m); t += 1
        c = WR if op == 'W' else ER
        if h[c[0] % H, c[1] % H, c[2] % H] != 1:
            return False, w, f'the cell of operation at generation {g} is not live'
        h[c[0] % H, c[1] % H, c[2] % H] = 0
        w += -1 if op == 'W' else 1
    end = t + 80 + (t % 2)
    while t < end:
        h = oracle.step(h, m); t += 1
    e = obj(w); a = bool((h == e).all())
    h2 = oracle.step(oracle.step(h, m), m)
    return a and bool((h2 == e).all()), w, int((h != e).sum())


def regular(ops, gap):
    out = []; t = 0
    for op in ops:
        out.append((t + (op == 'E'), op)); t += gap
    return out


cases = []
for k in (1, 3, 6, 7, 8, 9, 10):
    cases.append((f'W x {k} (gap 40)', regular('W' * k, 40)))
for k in (1, 4, 6, 7, 8, 9, 10, 11):
    cases.append((f'E x {k} (gap 40)', regular('E' * k, 40)))
cases.append(('WEWEWEWEWE (gap 40)', regular('WEWEWEWEWE', 40)))
cases.append(('EEEEWWWWWWWWEEEE (gap 40)', regular('EEEEWWWWWWWWEEEE', 40)))
for d in (2, 4, 6, 8, 10, 14, 20, 30):
    cases.append((f'W then W {d} gens later', [(0, 'W'), (d, 'W')]))
for d in (1, 3, 5, 9, 13, 17, 21, 25, 31):
    cases.append((f'W then E {d} gens later', [(0, 'W'), (d, 'E')]))
for d in (1, 3, 5, 9, 15, 21, 27):
    cases.append((f'E then W {d} gens later', [(1, 'E'), (1 + d, 'W')]))
cases.append(('W W W W every 4 gens', [(0, 'W'), (4, 'W'), (8, 'W'), (12, 'W')]))
cases.append(('W W W W every 2 gens', [(0, 'W'), (2, 'W'), (4, 'W'), (6, 'W')]))
print(f'register: units {ua}..{ub - 1}, wall at {w0}; write at unit {WR[0] >> 1}, erase at unit {ER[0] >> 1}', flush=True)
for name, sch in cases:
    good, w, nd = run(sch)
    print('MATCH' if good else 'DIFFER', f'{name}: predicted wall at {w}' + ('' if good else f' ({nd} cells differ)'), flush=True)
