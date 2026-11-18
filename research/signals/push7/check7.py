#!/usr/bin/env python3
"""Check push 7's stepper (step7.c / step7.py) bit for bit against reference/oracle.py on the objects of
objects/echo-train.json, and its 'train' boundary mode against its own dead-boundary mode.

    python check7.py          (about 2 min)

  R  ring mode against the oracle's ring torus (H = 96, a ring of 48 units, as verify_echo.py): the plain train, each
     signal of the json on it, each one-cell event, each meeting: whole state compared at every generation, 120
     generations (meetings: to their stated generation);
  G  dead mode against the oracle on a cubic torus H = 128 (as verify_echo.py check E): the gun #4 at the end of a
     finite train (units -24..5) with U set in front of it: whole state at every generation, 60 generations;
  W  train mode against dead mode: for the first 20 ends of each list given (default: none; check7.py LIST.json ...
     adds them), the end at the end of the train with one hole, stepped in a window of units -40..20 with the plain
     train below, and in dead mode on a window of units -260..20 holding a finite train: equal on units -40..20 at
     every generation up to 200, for as long as units -40..-31 of the long run are the plain train (train mode is exact
     only then; census7 stops a run before a difference gets that far).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sg
from scat import unit, tr
from step7 import Window, NC
oracle = sg.oracle

ob = json.load(open(os.path.join(shim.SIG, 'objects', 'echo-train.json')))
BASE = [[[tuple(c) for c in ob['base'][t][p]] for p in (0, 1)] for t in range(4)]
SIG = {K: (v['parity'], [tuple(c) for c in v['cells']], v['dir']) for K, v in ob['sig'].items()}
allok = True


def report(name, ok):
    global allok
    allok &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def canon_ring(c, L, lo=-1, hi=7):
    """A torus cell (coordinates mod 2L) -> its representative in the tube with unit in [0, L)."""
    H = 2 * L
    x = c[0] % H; y = ((c[1] + L) % H) - L
    for z in range(-H, 2 * H):
        if (z - c[2]) % H == 0 and lo <= x + y + z <= hi and lo <= x - y + z <= hi:
            return (x, y, z)
    raise ValueError(c)


# ---- R: ring mode vs the oracle's ring torus
H = 96; L = 48; OFF = (48, 48, 48)
m = oracle.masks(H)


def oarr(cells):
    a = np.zeros((H, H, H), np.int8)
    for c in cells:
        a[(c[0] + OFF[0]) % H, (c[1] + OFF[1]) % H, (c[2] + OFF[2]) % H] ^= 1
    return a


def ocells(a):
    return frozenset(canon_ring((int(p[0]) - OFF[0], int(p[1]) - OFF[1], int(p[2]) - OFF[2]), L) for p in np.argwhere(a))


Wr = Window('fb', 0, L)


def wring(cells):
    return Wr.array(canon_ring(c, L) for c in cells)


def train(t):
    return [tr(c, u) for u in range(L) for c in BASE[t % 4][u % 2]]


def sigc(K, u):
    return [tr(c, u) for c in SIG[K][1]]


def ring_check(name, cells, gens):
    A = oarr(cells); a = wring(cells)
    ok = ocells(A) == Wr.cells(a)
    for t in range(gens):
        A = oracle.step(A, m); Wr.run(a, t, 1, 'ring')
        if ocells(A) != Wr.cells(a):
            ok = False; break
    report(f'R  {name}: ring mode equals the oracle, whole ring, {gens} generations' + ('' if ok else f' (first difference at {t + 1})'), ok)


ring_check('plain train', train(1), 120)
for K in SIG:
    ring_check(f'signal {K}', frozenset(train(1)) ^ frozenset(sigc(K, SIG[K][0])), 120)
for e in ob['events']:
    c = tuple(e['cell']); X = frozenset(train(e['phase'])) ^ {c}
    ring_check(f"event {e['cell']} {e['flip']} at phase {e['phase']}", X, max(e['gen'], 60))
for r in ob['meetings']:
    X = frozenset(train(1))
    for K, u in r['signals']:
        X = X ^ frozenset(sigc(K, u))
    ring_check(f"meeting {r['signals']}", X, r['gen'])

# ---- G: dead mode vs the oracle, the gun of the json with U
g = ob['gun_absorbs_U']; KS = g['KS']; H2 = 128; OFF2 = (64, 64, 64); m2 = oracle.masks(H2)
cap = [tuple(c) for c in g['cap']]


def oarr2(cells):
    a = np.zeros((H2, H2, H2), np.int8)
    for c in cells:
        a[(c[0] + OFF2[0]) % H2, (c[1] + OFF2[1]) % H2, (c[2] + OFF2[2]) % H2] ^= 1
    return a


def ocells2(a):
    out = set()
    for p in np.argwhere(a):
        c = (int(p[0]) - OFF2[0], int(p[1]) - OFF2[1], int(p[2]) - OFF2[2])
        out.add(c)
    return frozenset(out)


Wd = Window('fb', -30, 30)
okG = True
for t0 in range(4):
    cells = frozenset([tr(c, u) for u in range(-24, KS) for c in BASE[t0 % 4][u % 2]] + cap) ^ frozenset(sigc('U', 1)) \
        if t0 == 1 else None
    if cells is None:
        continue
    A = oarr2(cells); a = Wd.array(cells)
    assert Wd.cells(a) == cells
    for t in range(60):
        A = oracle.step(A, m2); Wd.run(a, t, 1, 'dead')
        if ocells2(A) != Wd.cells(a):
            okG = False; break
report('G  dead mode equals the oracle (torus 128): the gun #4 of echo-train.json with U in front of it, 60 generations', okG)

# ---- W: train mode vs dead mode on the ends of the given lists
import sat_gun as G
for fn in sys.argv[1:]:
    d = json.load(open(fn)); pat, _ = G.train([0xf, 0xb], True, 1)
    bad = 0; n = 0; gens = []
    for e in d['list'][:20]:
        cap = frozenset(tuple(c) for c in e['cap'])
        Wt = Window('fb', -40, 20); Wf = Window('fb', -260, 20)
        rakes = [u for u in range(-10, 6) if tr((1, 0, 4), u) in G.train_cells(pat, 0, -10, 6, 1)]
        hole = {tr((1, 0, 4), max(rakes))}
        x0 = (G.train_cells(pat, 0, -260, 6, 1) | cap) - hole
        a = Wt.array(x0); b = Wf.array(x0); g = 0
        for t in range(200):
            Wt.run(a, t, 1, 'train'); Wf.run(b, t, 1, 'dead')
            # train mode is exact while the true state below the window is the plain train; stop comparing once
            # units -40..-31 of the long run are no longer the plain train (a burning end, an echo)
            if not np.array_equal(b[220:230], Wt.train(t + 1)[:10]):
                break
            if not np.array_equal(a, b[220:]):
                bad += 1; break
            g += 1
        n += 1; gens.append(g)
    report(f'W  {fn}: train mode equals dead mode with a finite train on units -40..20 while units -40..-31 are the plain train ({n} ends with a hole; generations compared: min {min(gens)}, max {max(gens)})', bad == 0)
print('ALL PASS' if allok else 'SOME FAIL')
