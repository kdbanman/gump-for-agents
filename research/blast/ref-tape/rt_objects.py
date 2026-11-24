#!/usr/bin/env python3
"""ref-tape: the catalogue's objects, built from the catalogue's JSON files and prose only (cell sets, doubled
coordinates, the frame of objects/line-C.json: unit u = cells with x in {2u, 2u+1}, tr(c, k) = (x+2k, y, z-2k)).

Sources: research/signals/objects/{line-C,clock-C,tape-BC}.json, research/signals/push8/objects/cell8.json,
research/signals/push9/objects/call9.json, the table SIGS of research/audit/signals6/sig6.py (read with ast, not run).
Nothing from research/blast/lean/ is used.
"""
import ast, os
from rt_lib import load, OBJ, SIG, ROOT, tr, trs, unit_of

LINE = load(os.path.join(OBJ, 'line-C.json'))
CLOCK = load(os.path.join(OBJ, 'clock-C.json'))
TAPE = load(os.path.join(OBJ, 'tape-BC.json'))
CELL8 = load(os.path.join(SIG, 'push8', 'objects', 'cell8.json'))
CALL9 = load(os.path.join(SIG, 'push9', 'objects', 'call9.json'))
T = lambda key, d=LINE: [tuple(c) for c in d[key]]

# --- the two letters of the tape -------------------------------------------------------------------------------
UNIT_C = frozenset(T('unit'))                                   # wire C, one unit, even generation
assert UNIT_C == frozenset(T('unit', CLOCK)) == frozenset(map(tuple, TAPE['bg']))


def _tape_ring_cells():
    L = len(TAPE['sequence'])
    bg = frozenset().union(*[trs(map(tuple, TAPE['bg']), k) for k in range(L)])
    return bg ^ frozenset(map(tuple, TAPE['defect'])), L


def _unit_B():
    """wire B's unit, read off tape-BC.json at every B of its sequence (all must agree)"""
    cells, L = _tape_ring_cells()
    seen = set()
    for u, ch in enumerate(TAPE['sequence']):
        loc = frozenset(tr(c, -u) for c in cells if unit_of(c) == u)
        if ch == 'C':
            assert loc == UNIT_C, u
        else:
            seen.add(loc)
    assert len(seen) == 1
    return seen.pop()


UNIT_B = _unit_B()


def tape_cells(word, a, b):
    """word: function unit -> 'B' / 'C'; the cells of units a .. b"""
    out = set()
    for u in range(a, b + 1):
        out |= trs(UNIT_B if word(u) == 'B' else UNIT_C, u)
    return frozenset(out)


# --- the line (section 21) ------------------------------------------------------------------------------------
def line_cells(N):
    """objects/line-C.json 'note': capA + unit moved by k(2,0,-2), k = 0..N-1 + gun moved by N(2,0,-2)"""
    cells = set(T('capA'))
    for k in range(N):
        cells |= trs(UNIT_C, k)
    cells |= trs(T('gun'), N)
    assert len(cells) == 18 + 5 * N + 15
    return frozenset(cells)


# --- the clock (section 11) -----------------------------------------------------------------------------------
def clock_cells(N, lit=True):
    """objects/clock-C.json: capL + N units of wire C + capR moved N units; lit: + ignite moved N // 2 units
    (verify_clock.py's convention for 'the middle unit')"""
    cells = set(T('capL', CLOCK))
    for k in range(N):
        cells |= trs(UNIT_C, k)
    cells |= trs(T('capR', CLOCK), N)
    assert len(cells) == 32 + 5 * N
    if lit:
        ig = tr(tuple(CLOCK['ignite']), N // 2)
        assert ig not in cells
        cells.add(ig)
    return frozenset(cells)


# --- the rake train (section 30) and the nine signals (sig6.py) ------------------------------------------------
RAKE5, RAKEF = frozenset(T('rake5')), frozenset(T('rakef'))


def train0_cells(a, b):
    """generation 0 of the plain train: rake5 on the even units, rakef on the odd units (section 30)"""
    out = set()
    for u in range(a, b + 1):
        out |= trs(RAKE5 if u % 2 == 0 else RAKEF, u)
    return frozenset(out)


def _sigs():
    src = open(os.path.join(ROOT, 'research', 'audit', 'signals6', 'sig6.py')).read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', None) == 'SIGS':
            return ast.literal_eval(node.value)
    raise RuntimeError('SIGS not found')


SIGS = _sigs()     # name -> (parity of the lowest unit, cells at train phase 1 relative to it, direction)


def sig_cells(k, u):
    par, cells, _ = SIGS[k]
    assert u % 2 == par
    return trs(cells, u)


# --- push 8: the store wire and the count read ----------------------------------------------------------------
STATORS8 = [tuple(c) for c in CELL8['stators']]
SITES8 = [tuple(c) for c in CELL8['sites']]


def hex_unit(h, stators=STATORS8, sites=SITES8):
    return frozenset(stators) | frozenset(sites[j] for j in range(4) if h >> j & 1)


def hex_word_cells(word, a, b, stators=STATORS8, sites=SITES8):
    """word: function unit -> hex digit (int); units a .. b"""
    out = set()
    for u in range(a, b + 1):
        out |= trs(hex_unit(word(u), stators, sites), u)
    return frozenset(out)


def store_word(k, w=0):
    """push 8 section 5: ...777 d^k f 777..., the first d at unit w"""
    return lambda u: 0xd if w <= u < w + k else (0xf if u == w + k else 0x7)


def count_read_cells(k, a, b, w=0):
    """the store with the stator (0,1,2) of unit w - 1 removed (an even generation)"""
    S = hex_word_cells(store_word(k, w), a, b)
    c = tr(STATORS8[0], w - 1)
    assert c in S
    return S - {c}


def pulses_word(k, lead):
    """plain wire B with k units of wire C two apart, the leading (lowest) one at `lead` (push 8 section 5)"""
    return lambda u: 'C' if (lead <= u < lead + 2 * k and (u - lead) % 2 == 0) else 'B'


# --- push 9: the call line ------------------------------------------------------------------------------------
STATORS9 = [tuple(c) for c in CALL9['stators']]
SITES9 = [tuple(c) for c in CALL9['sites']]
CALL_LINE = frozenset(map(tuple, CALL9['runs'][0]['extra']))
CALL_CELLS = [tuple(c) for c in CALL9['runs'][0]['ops'][3][2]]
CROSS = 4 + CALL9['runs'][0]['crossings'][0]
assert STATORS9 == STATORS8 and SITES9 == SITES8 and len(CALL_LINE) == 162 and CROSS == 35
E1 = tr((1, 2, 0), CROSS)          # REVIEW-signals-9 section 2.2: e1 = (1,2,0) of the crossing unit = (71, 2, -70)
assert E1 == (71, 2, -70)


def call_store_cells(k, a, b):
    """REVIEW-signals-9 section 3: wire B with d^k f on the units c+1 .. c+k+1"""
    return hex_word_cells(store_word(k, CROSS + 1), a, b, STATORS9, SITES9)
