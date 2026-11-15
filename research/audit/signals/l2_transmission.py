#!/usr/bin/env python3
"""L2 audit: the transmission, rebuilt from the stored cells and stepped with oracle.step only.

    nice -n 10 python3 l2_transmission.py [N] [shots] [gap]        (default N = 48, shots = 40, gap = 120)

Wire B ring of N cubes on the box torus (2N, 20, 2N); receiver cells (transmission-B.json) flipped; the cell A =
(8,1,-6) flipped at generations t_first + k*gap (k = 0, 1, ...).  Three runs side by side: signalled, control (A
never touched), bare wire.  N > 48 puts the receiver 36 cubes from A as stored but lengthens the far side of the ring
(receiver -> A the other way round) from 12 to N - 36 cubes.  After each shot (just before the next) it reports:
stationary (period 2)?; set of cells differing from the bare wire, by cube, and whether it is the previous set plus
2 cells one cube nearer A; whether every cube between A and the receiver, A included, is exactly bare; and mid-flight
the pulse: cells in transit and their cube positions (also checks nothing travels the other way from A).
Runs until the record stops following the pattern, or `shots` shots.
"""
import json, subprocess, sys
from lat import ring_torus, wire, shift, ROOT

N = int(sys.argv[1]) if len(sys.argv) > 1 else 48
SHOTS = int(sys.argv[2]) if len(sys.argv) > 2 else 40
ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'bcd5844:research/signals/objects/transmission-B.json']))
GAP = int(sys.argv[3]) if len(sys.argv) > 3 else ob['gap']
T = ring_torus(N)
bg = [tuple(c) for c in ob['bg']]
bare0 = wire(bg, 0, N)
recv = frozenset(tuple(c) for c in ob['receiver'])
A = T.mod(tuple(ob['flip']))
cube = lambda c: (c[0] // 2) % N
ax = cube(A)
sig = T.arr(bare0 ^ recv); ctl = sig.copy(); bare = T.arr(bare0)
start = T.cells(sig)
t = 0


def adv(n):
    global sig, ctl, bare, t
    for _ in range(n):
        sig = T.step(sig); ctl = T.step(ctl); bare = T.step(bare); t += 1


def bycube(cells):
    out = {}
    for c in cells:
        out.setdefault(cube(c), []).append(c)
    return out


adv(ob['t_first'])
assert (sig == ctl).all() and T.cells(sig) == start, 'wire + receiver not stationary'
prev = T.cells(sig) ^ T.cells(bare); prevnew = None
print(f'ring N={N}, torus {T.shape}; A in cube {ax}; receiver cubes {sorted(bycube(prev))}; gap {GAP}', flush=True)
rows = []
for k in range(1, SHOTS + 1):
    sig[A] ^= 1
    t_shot = t
    trans = []
    for h in range(GAP - 2):
        adv(1)
        if (t - t_shot) % 10 == 0 or h == 1:
            d = (T.cells(sig) ^ T.cells(ctl)) - (prev - recv) if False else (T.cells(sig) ^ T.cells(bare)) ^ prev
            trans.append((t - t_shot, len(d), sorted(set(cube(c) for c in d))))
    a = sig.copy(); adv(2)
    stat = (sig == a).all()
    cur = T.cells(sig) ^ T.cells(bare)
    new = cur - prev; lost = prev - cur
    rc = sorted(bycube(cur))
    # cubes from A (inclusive) forward to the receiver's first cube: exactly bare?
    first = min(((c - ax) % N for c in rc), default=None)
    line_bare = all(((cube(c) - ax) % N) >= first for c in cur) if first is not None else True
    pattern = (len(new) == 2 and not lost and (prevnew is None or new == frozenset(T.mod(c) for c in shift(prevnew, -1))))
    # did anything travel backwards from A (towards -v)?  (cells in transit behind A, from the snapshots)
    pf = min((c - ax) % N for c in bycube(prev))
    back = any(any((c - ax) % N > pf + 4 for c in cs) for _, _, cs in trans)
    rows.append(dict(k=k, t=t, stat=bool(stat), ncells=len(cur), receiver_from_A=first, line_bare=line_bare, pattern=pattern,
                     new=sorted(new), lost=sorted(lost)))
    print(f'shot {k:2d} at t={t_shot}: then stationary={stat}; differs from bare in {len(cur)} cells, cubes {rc[0] if rc else "-"}..{rc[-1] if rc else "-"} '
          f'(receiver front {first} cubes from A); line A..receiver bare: {line_bare}; record = previous + 2 cells one cube nearer A: {pattern}; '
          f'lost {len(lost)}; transit outside [A, receiver]: {back}; in flight (gens after shot, cells, cubes): {trans[1]}, {trans[len(trans) // 2]}', flush=True)
    if not (stat and line_bare and pattern):
        print('pattern broken at shot', k); break
    prev, prevnew = cur, new
print('control unchanged all along:', T.cells(ctl) == start, 'at t =', t)
json.dump(rows, open(f'{__import__("lat").SCR}/l2_N{N}_gap{GAP}.json', 'w'))
