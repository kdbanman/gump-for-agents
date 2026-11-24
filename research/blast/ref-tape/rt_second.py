#!/usr/bin/env python3
"""ref-tape, second review (2026-11-24): the call law's objects and interaction set, and `clockOf`.

    python3 rt_second.py DUMP2      (DUMP2 = output of RtDump2.lean; about 2 minutes)

1. callStart k (k = 1, 3) = store wire (units 8..46) + call line + CALL, from call9.json (rt_objects.py);
2. Lf t, read by Lean through its 128 x 128 x 16 box, = the oracle run of line + CALL, t = 0..46;
3. clockOf N, N = 1..20: N <= 5 the oracle lit clock at max(N-2, 0); N >= 6 one state of the oracle cycle of the lit
   clock of N units; exact period 4N + 2 on the oracle; the two-clocks object of the first review is not clockOf 7;
4. the interaction set: Z' = {cells whose closed neighbourhood meets HV and HL}, HV and HL transcribed from
   Gump/CallUnion.lean, by brute force over a box that holds HL + 2 = Lean's zoneZ; HL's eight bounds against the true
   diagonal hull of line + CALL; on oracle runs (k = 1, 3, 10) V_k stays in HV, Lf in HL, and every cell whose
   closed neighbourhood holds a live cell of both V_k(t) and Lf(t) is in Z.
"""
import sys
from rt_lib import orc_run, orc_ring, ringwrap, trs, tr, unit_of, is_cell
import rt_objects as O
from rt_dyn import report
import rt_dyn

D = {}
for line in open(sys.argv[1]):
    line = line.rstrip('\n')
    if line:
        name, pts = line.split('|', 1)
        D[name] = frozenset(tuple(map(int, p.split(','))) for p in pts.split()) if pts else frozenset()

LINE = frozenset(O.CALL_LINE) | frozenset(O.CALL_CELLS)

# 1. callStart
inreg = lambda c: 16 <= c[0] <= 93 and -48 <= c[1] <= 24 and -56 <= c[0] + c[2] <= 16 and is_cell(c)
for k in (1, 3):
    ref = frozenset(c for c in O.call_store_cells(k, 8, 46) | LINE if inreg(c))
    report(D[f'callStart.{k}'] == ref and all(inreg(c) for c in LINE),
           f'callStart {k}: Lean = store wire (units 8..46) + line + CALL from call9.json, {len(ref)} cells in the region')

# 2. Lf through the new box
orb = orc_run(LINE, 46, margin=16)
incore = lambda c: -12 <= c[0] + 0 < 108 and -12 <= c[1] + 40 < 108 and -12 <= c[2] + 64 < -4
report(all(incore(c) for s in orb for c in s), 'the oracle run of line + CALL stays in the new box core (moved by lineFrame)')
bad = [t for t in range(47) if D[f'Lf.{t}'] != orb[t]]
report(not bad, f'Lf t read through Gump.Call.Box = the oracle run, t = 0..46 (differ at {bad})')
report(orb[42] == frozenset(O.CALL_LINE) and orb[44] == orb[42] and orb[43] != orb[42],
       'oracle: the free line is `line` at 42 and 44, and not at 43')

# 3. clockOf
for N in range(1, 21):
    P = 4 * N + 2
    mu = max(N - 2, 0)
    o = orc_run(O.clock_cells(N), mu + 2 * P)
    C = D[f'clockOf.{N}']
    inbox = all(-6 <= unit_of(c) <= N + 5 and -8 <= c[1] <= 8 and -24 <= c[0] + c[2] <= 24 for t in range(mu, mu + P)
                for c in o[t])
    if N <= 5:
        where = [mu] if C == o[mu] else []
    else:
        where = [t for t in range(mu, mu + P) if o[t] == C]
    oc = orc_run(C, P + 1)
    exact = oc[P] == oc[0] and all(oc[k] != oc[0] for k in range(1, P))
    report(len(where) == 1 and inbox and exact, f'clockOf {N}: = the lit clock of {N} units at generation {where} '
           f'(cycle entered at {mu}); exact period {P} on the oracle: {exact}')
two = frozenset(O.clock_cells(1)) | frozenset((c[0], c[1] + 16, c[2]) for c in O.clock_cells(2))
o7 = orc_run(O.clock_cells(7), 5 + 30)
report(all(two != o7[t] for t in range(5, 35)) and two != D['clockOf.7'],
       'the two-clocks object is not clockOf 7, nor any state of the lit clock of 7 units')

# 4. the interaction set
def HV(p):
    s1 = p[0] + p[1] + p[2]; s2 = p[0] - p[1] + p[2]
    return 1 <= s1 <= 5 and -1 <= s2 <= 5


CL = {(1, 1, 1): 33, (1, 1, -1): 177, (1, -1, 1): -5, (1, -1, -1): 139,
      (-1, 1, 1): -135, (-1, 1, -1): 9, (-1, -1, 1): -51, (-1, -1, -1): 93}
dot = lambda d, p: d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def HL(p):
    return all(dot(d, p) <= C for d, C in CL.items())


hull = {d: max(dot(d, c) for c in LINE) for d in CL}
report(hull == CL, f'HL\'s eight bounds are exactly the diagonal hull of line + CALL ({hull == CL})')
import oracle
offs = [oracle.offsets(a) for a in range(3)]
axis = lambda c: [i for i in range(3) if c[i] & 1][0]
nb = lambda p: [p] + [(p[0] + o[0], p[1] + o[1], p[2] + o[2]) for o in offs[axis(p)]]
# HL is bounded: x in [21, 86], y in [-44, 21], z in [-104, -39] (sums of the bounds); a cell within 2 of it
Zp = set()
for x in range(19, 89):
    for y in range(-46, 24):
        for z in range(-106, -36):
            p = (x, y, z)
            if not is_cell(p):
                continue
            N = nb(p)
            if any(HL(q) for q in N) and any(HV(q) for q in N):
                Zp.add(p)
report(frozenset(Zp) == D['zoneZ'], f'zoneZ (44 cells in Lean: {len(D["zoneZ"])}) = brute-force set of cells whose closed '
       f'neighbourhood meets HV and HL ({len(Zp)} cells)')
report(all(HL(c) for s in orb for c in s), 'oracle: Lf stays in HL, t = 0..46')

c = O.CROSS
for k in (1, 3, 10):
    L = max(76, 4 * k + 48)
    T = 2 * (k + 19)
    wire = O.hex_word_cells(O.store_word(k, c + 1), c - L // 2, c - L // 2 + L - 1)
    Vpre = orc_ring(wire, 29, L)
    Vpost = orc_ring(Vpre[29] | ringwrap([O.E1], L), T - 29, L)
    V = Vpre[:29] + Vpost
    Lf = orc_ring(LINE, T, L, 104, -56)
    # torus z back to the lattice: the representative nearest to -x (the wire has x + z in 0..6, the line -51..14)
    unwrap = lambda q: (q[0], q[1], q[2] - 2 * L * round((q[0] + q[2]) / (2 * L)))
    inHV = all(HV(unwrap(q)) for s in V for q in s)
    used = set()
    for t in range(T + 1):
        Vs = {unwrap(q) for q in V[t]}; Ls = {unwrap(q) for q in Lf[t]}
        for p in Vs | Ls:
            for q in nb(p):
                if not is_cell(q):
                    continue
                N = nb(q)
                if any(r in Vs for r in N) and any(r in Ls for r in N):
                    used.add(q)
    report(inHV and used <= D['zoneZ'], f'k={k}: V_k in HV at every generation ({inHV}); the {len(used)} cells where V_k and Lf '
           f'both reach the closed neighbourhood, t = 0..{T}, all in Z ({used <= D["zoneZ"]})')

print('ALL PASS' if rt_dyn.ok else 'SOME CHECKS FAILED')
sys.exit(0 if rt_dyn.ok else 1)
