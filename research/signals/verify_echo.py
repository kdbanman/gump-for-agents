#!/usr/bin/env python3
"""Verify the signals of the rake train and their meetings (sixth push, README sections 30-32) with
reference/oracle.py as the judge.

    python3 verify_echo.py [objects/echo-train.json]          (about 40 s)

Everything is stepped with oracle.masks / oracle.step on a cubic array torus of side H = 96 (a ring of 48 units:
the train along (1,0,-1) closes on itself; whole states compared cell for cell).  From the JSON: the train's base
cells, the signals, one-cell events, meetings with their measured outcomes, and a gun.
  A  the plain train is an orbit of period 4 and moves one unit towards -v every 2 generations;
  B  each signal (E, U up the stream; H, K0 down) rides the train: X(2j) = the train moved -j units xor the signal
     moved (dir + 1) j - j = dir * j units, for j = 0..60 (more than a lap of the ring for the up-signals' relative
     motion), whole torus;
  C  each one-cell event (one cell of the plain train flipped) becomes that signal, at the stated place;
  D  meetings: E with H and U with H leave wire B (the wire of the first push) between two edges that move apart;
     U with K0 cancel: the whole torus is the plain train again; E with K0 leaves the train with every rake holed;
     E with three, four, five holes: wire B with a stretch of other units whose length grows by one per hole;
  E  the gun #4 of the C = 37 census, at the end of a finite train, absorbs U: from 8 generations after U reaches
     the gun the run equals the undisturbed run on the whole torus (U starts 5 units in front of the gun).
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'objects/echo-train.json'))
H = 96; L = H // 2
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
OFF = (48, 48, 48)
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
BASE = [[[tuple(c) for c in ob['base'][t][p]] for p in (0, 1)] for t in range(4)]
SIG = {K: (v['parity'], [tuple(c) for c in v['cells']], v['dir']) for K, v in ob['sig'].items()}
WB = [[tuple(c) for c in w] for w in ob['wireB']]


def arr(cells):
    a = np.zeros((H, H, H), dtype=bool)
    for c in cells:
        x = tuple((c[i] + OFF[i]) % H for i in range(3))
        assert valid[x], c
        a[x] ^= True
    return a


def train(t):
    return [tr(c, u) for u in range(L) for c in BASE[t % 4][u % 2]]


def sigc(K, u):
    par, cells, _ = SIG[K]
    assert u % 2 == par
    return [tr(c, u) for c in cells]


def unit_cells(cells_by_unit, u):
    return [tr(c, u) for c in cells_by_unit]


def shift(a, k):     # move by k units (2k in x, -2k in z)
    return np.roll(np.roll(a, 2 * k, axis=0), -2 * k, axis=2)


def run(a, g, mm=None):
    mm = m if mm is None else mm
    for _ in range(g):
        a = oracle.step(a, mm)
    return a


def units_of(a):
    """lowest-unit index (mod L) of each live cell of a, measured as x // 2 with x relative to OFF."""
    idx = np.argwhere(a)
    return sorted({((int(v[0]) - OFF[0]) // 2) % L for v in idx})


allok = True
def report(name, ok):
    global allok
    allok &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


# A
P1 = arr(train(1))
X = P1.copy(); okA = True
for t in range(1, 9):
    X = oracle.step(X, m)
    okA &= np.array_equal(X, arr(train(1 + t)))
okA &= np.array_equal(arr(train(3)), shift(P1, -1)) and np.array_equal(arr(train(5)), P1)
report('A  the plain train: period 4, train(t + 2) = train(t) moved one unit towards -v', okA)

# B
for K, (par, cells, d) in SIG.items():
    X = arr(train(1)) ^ arr(sigc(K, par)); ok = True
    for j in range(1, 61):
        X = run(X, 2)
        # train(1 + 2j) = train(1) moved -j; the signal at unit par + d*j
        want = shift(P1, -j) ^ shift(arr(sigc(K, par)), d * j)
        ok &= np.array_equal(X, want)
    report(f'B  signal {K} ({len(cells)} cells at phase 1, moving {d:+d} unit per 2 generations) rides the train 120 generations, whole torus', ok)

# C
for e in ob['events']:
    c = tuple(e['cell']); f = e['phase']
    X0 = arr(train(f)); X = X0.copy()
    x = tuple((c[i] + OFF[i]) % H for i in range(3))
    assert X[x] == (e['flip'] == 'remove')
    X[x] = not X[x]
    X = run(X, e['gen'])
    want = arr(train(f + e['gen'])) ^ arr(sigc(e['kind'], e['unit']))
    report(f"C  one cell {e['cell']} {e['flip']}d at phase {f} becomes signal {e['kind']} (lowest unit {e['unit']} at generation {e['gen']})",
           np.array_equal(X, want))

# D
for r in ob['meetings']:
    X = arr(train(1))
    for K, u in r['signals']:
        X ^= arr(sigc(K, u))
    T = r['gen']; ok = True
    if r['outcome'] == 'cancel':
        for t in range(1, T + 1):
            X = oracle.step(X, m)
            if t >= r['empty_from']:
                ok &= np.array_equal(X, arr(train(1 + t)))
        report(f"D  {r['signals']}: cancel: the whole torus is the plain train from generation {r['empty_from']} to {T}", ok)
        continue
    X = run(X, T)
    Pt = arr(train(1 + T))
    D = X ^ Pt
    us = units_of(D)
    lo, hi = r['lo'] % L, r['hi'] % L
    span = sorted(((u - r['lo']) % L) for u in us)
    ok &= span[0] == 0 and span[-1] == (r['hi'] - r['lo']) and (r['hi'] - r['lo']) < L - 2
    if r['outcome'] == 'wireB':
        w = WB[(T + 1) % 2]
        bad = []
        for u in range(r['lo'] + 3, r['hi'] - 5):
            cu = arr([tr(c, u) for c in w])
            # compare the 3 x 3 tube cells of unit u: cells of X with x in 2u..2u+1 (relative)
            sl = np.zeros((H, H, H), bool)
            xs = [(2 * u + OFF[0]) % H, (2 * u + 1 + OFF[0]) % H]
            sl[xs, :, :] = True
            if not np.array_equal(X & sl, cu):
                bad.append(u)
        ok &= bad == r['not_wireB']
        report(f"D  {r['signals']}: at generation {T} the difference spans units {r['lo']}..{r['hi']}; between, wire B "
               f"except units {bad}", ok)
    else:
        Y = arr(train(1 + T))
        for u in range(r['lo'] - 10, r['hi'] + 10):
            if u % 2 == SIG['H'][0]:
                Y ^= arr(sigc('H', u))
        a, b = r['holed_equal_units']
        sl = np.zeros((H, H, H), bool)
        for u in range(a, b):
            sl[[(2 * u + OFF[0]) % H, (2 * u + 1 + OFF[0]) % H], :, :] = True
        ok &= np.array_equal(X & sl, Y & sl)
        report(f"D  {r['signals']}: at generation {T} the difference spans units {r['lo']}..{r['hi']}; units {a}..{b - 1}: "
               f"the train with every rake holed", ok)

# E: a gun absorbs U (finite train, larger torus)
g = ob['gun_absorbs_U']; KS = g['KS']
H2 = 128
m2 = oracle.masks(H2); valid2 = m2[0] | m2[1] | m2[2]
OFF2 = (64, 64, 64)
def arr2(cells):
    a = np.zeros((H2, H2, H2), dtype=bool)
    for c in cells:
        x = tuple((c[i] + OFF2[i]) % H2 for i in range(3))
        assert valid2[x]
        a[x] ^= True
    return a
# the gun's own train phase: find t0 such that the gun's state (train units -24..KS-1 as sat_gun builds it) is
# consistent: the json stores the cap at sat_gun's generation 0; sat_gun's train at generation 0 is train(t0)
cap = [tuple(c) for c in g['cap']]
okE = False
for t0 in range(4):
    base = [tr(c, u) for u in range(-24, KS) for c in BASE[t0 % 4][u % 2]]
    A0 = arr2(base + cap)
    A4 = run(A0, 4, m2)
    near = np.zeros((H2, H2, H2), bool); near[(2 * (KS - 6) + OFF2[0]) % H2:, :, :] = True
    if np.array_equal(A0 & near, A4 & near):
        t1 = (1 - t0) % 4
        A = run(A0, t1, m2)                    # train phase 1
        U = A ^ arr2([tr(c, 1) for c in SIG['U'][1]])    # U at unit 1 (odd), moving up into the gun
        okE = True; hist = []
        gunpart = np.zeros((H2, H2, H2), bool); gunpart[(OFF2[0] + 8) % H2:(OFF2[0] + 40) % H2, :, :] = True
        for t in range(1, 45):
            A = oracle.step(A, m2); U = oracle.step(U, m2)
            hist.append(A & gunpart)
            if t >= 28:
                okE &= np.array_equal(A, U)
        # the undisturbed gun (units >= 4) is still in its period-4 cycle at the end (the far end of the finite
        # train, burning back, has not reached it)
        eqs = okE
        per = np.array_equal(hist[-1], hist[-5]) and not np.array_equal(hist[-1], hist[-3])
        print(f'   (equal from 28 to 44: {eqs}; gun part period 4 at the end: {per}; t0 = {t0})')
        okE = eqs and per
        break
report(f"E  U reaches the gun #4 of the C = 37 census ({len(cap)} cells) and is absorbed: the whole torus equals the "
       f"undisturbed run from generation 28 to 44, the gun in its cycle", okE)
print('ALL PASS' if allok else 'SOME FAIL')
