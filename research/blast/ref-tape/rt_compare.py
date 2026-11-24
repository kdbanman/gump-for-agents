#!/usr/bin/env python3
"""ref-tape, check 1: do the Lean objects equal the catalogue's objects?

    python3 rt_compare.py DUMP        (DUMP = the output of RtDump.lean; about 1 minute)

Compares every object printed by RtDump.lean (the Lean definitions evaluated to explicit cell sets) with the object
built by rt_objects.py from the catalogue's JSON files, and the oracle-derived ones (the train's phases, the base
state X0, the surgery states clockY j) with reference/oracle.py runs of the catalogue's objects. Prints one PASS/FAIL
line per comparison and ALL PASS.
"""
import sys
from rt_lib import orc_run, orc_ring, ringwrap, trs, tr, unit_of
import rt_objects as O

BOXY, BOXS = (-8, 8), (-24, 24)


def inbox(c, a, b):
    return 2 * a <= c[0] <= 2 * b + 1 and BOXY[0] <= c[1] <= BOXY[1] and BOXS[0] <= c[0] + c[2] <= BOXS[1]


def parse(path):
    D = {}
    for line in open(path):
        line = line.rstrip('\n')
        if not line:
            continue
        parts = line.split('|')
        if parts[0] == 'kind':
            D['kind.' + parts[1]] = (int(parts[2]), int(parts[3]),
                                     frozenset(tuple(map(int, p.split(','))) for p in parts[4].split()))
        elif parts[0] == 'cross':
            D['cross'] = int(parts[1])
        else:
            D[parts[0]] = [tuple(map(int, p.split(','))) for p in parts[1].split()] if parts[1] else []
    return D


ok = True


def report(good, msg):
    global ok
    ok &= bool(good)
    print('PASS' if good else 'FAIL', msg, flush=True)


def same_list(name, lean, ref):
    L = D[name]
    report(len(L) == len(set(L)) and frozenset(L) == frozenset(ref),
           f'{name}: Lean list ({len(L)} entries, {len(set(L))} distinct) = catalogue object ({len(ref)} cells)')


def same_box(name, ref, a, b):
    ref = frozenset(ref)
    report(all(inbox(c, a, b) for c in ref), f'{name}: the catalogue object lies inside the evaluation box (units {a}..{b})')
    report(frozenset(D[name]) == ref, f'{name}: Lean configuration on the box = catalogue object ({len(ref)} cells)')


D = parse(sys.argv[1])

# the tape's letters and a word
same_list('cellsOf.B', None, O.UNIT_B)
same_list('cellsOf.C', None, O.UNIT_C)
wTest = lambda u: 'C' if (u % 3 == 0 or u == 1) else 'B'
same_box('tape.wTest.-6.8', O.tape_cells(wTest, -6, 8), -6, 8)

# the line
for N in [2, 3, 4, 5, 7, 12, 20, 31]:
    same_list(f'lineList.{N}', None, O.line_cells(N))

# the clock
for N in range(1, 13):
    same_list(f'litList.{N}', None, O.clock_cells(N))
run6 = orc_run(O.clock_cells(6), 41 + 26)
report(frozenset(D['X0']) == run6[41], 'X0 = the oracle run of the lit clock of 6 units (clock-C.json) at generation 41')
report(run6[41 + 26] == run6[41] and all(run6[41 + k] != run6[41] for k in range(1, 26)),
       'X0 lies on a cycle of exact period 26 = 4*6 + 2 (oracle)')
for j in range(7):
    N = 6 + j
    P = 4 * N + 2
    mu = max(N - 2, 0)
    orb = orc_run(O.clock_cells(N), mu + 2 * P)
    Y = frozenset(D[f'clockY.{j}'])
    hits = [t for t in range(mu, mu + P) if orb[t] == Y]
    report(len(hits) == 1, f'clockY.{j} is the state at generation {hits} of the oracle run of the lit clock of {N} units '
           f'(cycle from {mu}, searched {mu}..{mu + P - 1})')
    report(all(inbox(c, -6, 11 + j) for t in range(mu, mu + P) for c in orb[t]),
           f'clock {N}: every state of the lit cycle lies in the evaluation box, so clockY.{j} was compared whole')
    report(orb[mu + P] == orb[mu] and all(orb[mu + k] != orb[mu] for k in range(1, P)) and
           (mu == 0 or orb[mu - 1 + P] != orb[mu - 1]),
           f'clock {N}: the lit clock has exact period {P} from generation {mu}, and generation {mu - 1} is not on the cycle')

# the train: generation 0 from line-C.json (rake5 even, rakef odd), phases 1..3 by the oracle on a ring of 16 units
L = 16
ring = orc_ring(O.train0_cells(0, L - 1), 4, L)
for t in range(4):
    for par in (0, 1):
        units_t = {}
        for c in ring[t]:
            units_t.setdefault(unit_of(c), set()).add(c)
        good = all(frozenset(units_t.get(u, ())) == ringwrap(trs(D[f'trainBase.{t}.{par}'], u), L)
                   for u in range(L) if u % 2 == par)
        report(good,
               f'trainBase.{t}.{par} = unit of parity {par} of the oracle train at generation {t} (ring of {L} units)')
    lean = ringwrap(D[f'train.{t}.-4.5'], L)
    want = frozenset(c for c in ring[t] if unit_of(c) in {u % L for u in range(-4, 6)})
    report(lean == want, f'train.{t} (Lean ucfg) on units -4..5 = the oracle train at generation {t}')

# the nine signals
for k, (par, cells, d) in O.SIGS.items():
    lp, ld, lc = D['kind.' + {'K0': 'Gump.Tape.Signals.Kind.K0'}.get(k, 'Gump.Tape.Signals.Kind.' + k)]
    report((lp, ld, lc) == (par, d, frozenset(cells)), f'signal {k}: parity, direction and cells as sig6.py')

# push 8
for h in range(16):
    same_list(f'hexCells.{h}', None, O.hex_unit(h))
for k in [1, 2, 3, 5]:
    same_box(f'store.{k}', O.hex_word_cells(O.store_word(k), -5, k + 5), -5, k + 5)
    same_box(f'countRead.{k}', O.count_read_cells(k, -5, k + 5), -5, k + 5)
    same_box(f'pulsesTape.{k}.-3', O.tape_cells(O.pulses_word(k, -3), -6, 2 * k + 2), -6, 2 * k + 2)

# push 9
for k in [1, 2, 4]:
    same_box(f'storeAt.{k}', O.call_store_cells(k, 30, 40 + k), 30, 40 + k)
same_list('callLine', None, O.CALL_LINE)
same_list('callCells', None, O.CALL_CELLS)
same_list('e1', None, [O.E1])
report(D['cross'] == O.CROSS, f'cross = {O.CROSS} (call9.json crossings[0] + 4)')

print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
