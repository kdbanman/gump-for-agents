"""E of REVIEW-signals-6: the reflector (capA with C18.23a beside it, research/audit/signals5/end_echo.json records).

    python3 refl6.py couple      the one-cell coupling, on reference/oracle.py              (~1 min)
    python3 refl6.py words       one hole, K0, and two holes at every spacing s = 1..20 rakes (st6)   (~2 min)

couple: for records 0 (C18.23a, gap 0) and 2 (C20.33c), plain and holed, for 60 generations from the hole's
generation: J = oracle.step of the joint state; S = oracle.step(line part) | oracle.step(oscillator part), the
oscillator part = the joint state's cells inside the support of the free oscillator's orbit (orbit by st6.step);
printed: the generations and cells where J and S differ.  Each oracle step is on a box torus around the object.
words: the line of N = 60 units (line-C.json, stepped 2N + 8 generations with st6.step, equal near capA to the
record), the oscillator beside capA; after 60 generations, at train phase 1 on units 10..30, the signals xored
in (push frame; H at units 21, 21 + 2s); read at generation tw + G on units 3..N-6: the difference as signals, or
'front' (growing) and whether wire B appears.
"""
import json, os, sys, time
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import sig6, glue6, meet6r

RECS = json.load(open(os.path.join(st6.ROOT, 'research', 'audit', 'signals5', 'end_echo.json')))
LINE = json.load(open(os.path.join(st6.ROOT, 'research', 'signals', 'objects', 'line-C.json')))
LT = lambda k: [tuple(c) for c in LINE[k]]


def osc_support(osc0):
    orb = [osc0]
    while True:
        n = st6.step(orb[-1])
        if n == osc0:
            break
        orb.append(n)
        assert len(orb) < 200
    return frozenset().union(*orb), len(orb)


def ostep(s, box):
    return dict(st6.oracle_torus(s, 1, *box))[1]


def couple():
    for ri in (0, 2):
        r = RECS[ri]
        osc0 = frozenset(map(tuple, r['oscillator'])); line0 = frozenset(map(tuple, r['line']))
        sup, P = osc_support(osc0)
        allc = line0 | osc0
        lo = [min(c[i] for c in allc) - 40 for i in range(3)]; hi = [max(c[i] for c in allc) + 40 for i in range(3)]
        lo = [v - v % 2 for v in lo]
        box = (tuple(((hi[i] - lo[i]) // 2 + 1) * 2 for i in range(3)), tuple(lo))
        for holed in (False, True):
            X = line0 | osc0
            for t in range(r['tg']):
                X = st6.step(X)
            if holed:
                X = X - {tuple(r['hole'])}
            coup = []
            for t in range(r['tg'], r['tg'] + 60):
                J = ostep(X, box)
                assert J == st6.step(X)
                o = X & sup; l = X - sup
                S = ostep(o, box) | ostep(l, box)
                if J != S:
                    coup.append((t + 1 - r['tg'], sorted(J - S), sorted(S - J)))
                X = J
            print(f"{r['osc']} gap {r['gap_k']} {'holed' if holed else 'plain'} (oracle; oscillator period {P}): "
                  f"{len(coup)} coupled generations in 60: {coup[:5]}{' ...' if len(coup) > 5 else ''}", flush=True)


def line_object(N):
    return frozenset(LT('capA')) | frozenset(tr(c, k) for c in LT('unit') for k in range(N)) | trs(LT('gun'), N)


def reflector(ri, N):
    r = RECS[ri]
    X = st6.run(line_object(N), 2 * N + 8)
    assert units(X, -10, 8) == units(frozenset(map(tuple, r['line'])), -10, 8)
    return X | frozenset(map(tuple, r['oscillator'])), r['osc']


def phase_at(S, ua, ub):
    for f in range(4):
        if units(S, ua, ub) == T.train(f, ua, ub):
            return f


def words():
    N = 70
    for ri in (0, 2):
        X0, name = reflector(ri, N)
        X0 = st6.run(X0, 60)
        while phase_at(X0, 10, 30) != 1:
            X0 = st6.step(X0)
        tests = [('H at 21', [('H', 21)]), ('K0 at 20', [('K0', 20)])] + \
                [(f'H at 21, {21 + 2 * s} (s={s})', [('H', 21), ('H', 21 + 2 * s)]) for s in range(1, 21)]
        for nm, w in tests:
            Y = X0
            for k, u in w:
                Y = Y ^ sig6.sig(k, u)
            G = 2 * max(u for _, u in w) + 40
            X, Yt = X0, Y
            for t in range(G):
                X = st6.step(X); Yt = st6.step(Yt)
            D = X ^ Yt
            f = phase_at(X, 30, 50)
            mid = units(D, 3, N - 6)
            near = frozenset(c for c in D if unit_of(c) < 3)
            # read: shift to phase 1 frame
            rd = None
            if f in (1, 3):
                dd = trs(mid, 1) if f == 3 else mid
                cs = T.components(dd)
                rd = []
                for c in cs:
                    sh = T.shape(c)
                    nmk = [k for k in sig6.SIGS if T.shape(sig6.sig(k, sig6.SIGS[k][0])) == sh]
                    rd.append(nmk[0] if nmk else f'?{len(c)}cells@{min(unit_of(q) for q in c)}')
            # wire B on the stream: count units whose cells equal wire B at this generation
            wb = sum(1 for u in range(3, N - 6) if glue6.base_at(Yt, u) == meet6r.WB[0] or glue6.base_at(Yt, u) == meet6r.WB[1])
            print(f'{name}: {nm}: +{G}: {len(mid)} cells differ on units 3..{N - 7} read {rd}; {len(near)} below unit 3; '
                  f'{wb} units of wire B on the stream', flush=True)


if __name__ == '__main__':
    t0 = time.time()
    {'couple': couple, 'words': words}[sys.argv[1]]()
    print(f'{time.time() - t0:.0f} s')
