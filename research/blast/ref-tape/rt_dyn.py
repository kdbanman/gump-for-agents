#!/usr/bin/env python3
"""ref-tape, check 2: the claimed behaviour of the catalogue's objects, on reference/oracle.py, at sizes and times the
Lean base cases do not cover, with the sharp boundaries. Objects from rt_objects.py (the JSON files only).

    python3 rt_dyn.py tape | line | clock | twoclocks | train | signals | unzip | call      (each under 10 minutes)

Infinite configurations (tape words, the train, the store wire) are run as rings on the oracle's torus
(2L, hy, 2L) (rt_lib.orc_ring); where the infinite word is not periodic, only units whose light cone sees one copy of
the defect are compared, and the ring is long enough for every unit that the claim concerns.
"""
import random, sys, time
from rt_lib import orc_run, orc_ring, ringwrap, trs, tr, unit_of
import rt_objects as O

ok = True


def report(good, msg):
    global ok
    ok &= bool(good)
    print('PASS' if good else 'FAIL', msg, flush=True)


def ring_units(S, L, us):
    us = {u % L for u in us}
    return frozenset(c for c in S if unit_of(c) in us)


def tape_ring(word, L):
    return ringwrap(O.tape_cells(lambda u: word[u % L], 0, L - 1), L)


def check_tape():
    """tape_run: run (tape w) (2n) = tape (u -> w (u + n)), for random periodic words (two-sided, whole torus)"""
    rnd = random.Random(1124)
    for L in (40, 37, 23):
        for trial in range(3):
            word = [rnd.choice('BC') for _ in range(L)]
            T = 2 * (L + 5)
            orb = orc_ring(O.tape_cells(lambda u: word[u % L], 0, L - 1), T, L)
            good = all(orb[2 * n] == tape_ring([word[(u + n) % L] for u in range(L)], L) for n in range(T // 2 + 1))
            neg = orb[2] == tape_ring([word[(u + 2) % L] for u in range(L)], L) or orb[2] == orb[0]
            report(not neg, f'tape: negative control, L = {L}: generation 2 is not the word shifted by 2, nor the start')
            report(good, f'tape: random word {"".join(word)[:20]}... on a ring of {L} units, whole torus, generations 0..{T}: '
                   f'state at 2n = the word shifted by n')


def line_check(N, extra=10, pmax=12):
    t0 = time.time()
    mu = 2 * N
    orb = orc_run(O.line_cells(N), mu + extra + pmax)
    f4 = orb[mu + 4] == orb[mu]
    f2 = orb[mu + 2] != orb[mu]
    f3 = orb[mu + 3] != orb[mu - 1]
    table = all((orb[s + p] == orb[s]) == (s >= mu and p % 4 == 0)
                for s in range(0, mu + extra + 1) for p in range(1, pmax + 1) if s + p <= mu + extra + pmax)
    report(f4 and f2 and f3 and table,
           f'line N={N}: X(2N+4)=X(2N) {f4}, X(2N+2)!=X(2N) {f2}, X(2N+3)!=X(2N-1) {f3}; '
           f'X(s+p)=X(s) iff s>=2N and 4|p for all s<={mu + extra}, 1<=p<={pmax}: {table} ({time.time() - t0:.0f} s)')


def check_line():
    for N in list(range(2, 15)) + [20, 31]:
        line_check(N)


def check_clock():
    """lit_clock_small for N = 1..5 and the lit clock's exact period for N = 13, 20 (rt_compare.py did 6..12)"""
    for N in [1, 2, 3, 4, 5, 13, 20]:
        P = 4 * N + 2
        mu = max(N - 2, 0)
        orb = orc_run(O.clock_cells(N), mu + 2 * P)
        exact = orb[mu + P] == orb[mu] and all(orb[mu + k] != orb[mu] for k in range(1, P))
        entry = mu == 0 or orb[mu - 1 + P] != orb[mu - 1]
        supp = all(-4 <= unit_of(c) <= N + 3 for t in range(mu, mu + P) for c in orb[t])
        report(exact and entry and supp, f'lit clock N={N}: exact period {P} from generation {mu} ({exact}), '
               f'generation {mu - 1} not on the cycle ({entry}), every state in units -4..{N + 3} ({supp})')


def check_twoclocks():
    """clock_every_length N = 7 is also witnessed by an object that is not a clock of 7 units: the lit clocks of 1 and
    of 2 units side by side (periods 6 and 10, lcm 30 = 4*7 + 2), inside units -4..10, |y| < 32, |x + z| < 64"""
    A = O.clock_cells(1)
    B = frozenset((c[0], c[1] + 16, c[2]) for c in O.clock_cells(2))
    S = A | B
    orb = orc_run(S, 31 + 30)
    exact = orb[30] == orb[0] and all(orb[k] != orb[0] for k in range(1, 30))
    tube = all(-4 <= unit_of(c) <= 7 + 3 and -32 <= c[1] < 32 and -64 <= c[0] + c[2] < 64 for t in range(31) for c in orb[t])
    report(exact and tube, f'two clocks (N=1 and N=2, the second moved by (0,16,0)), {len(S)} cells: exact period 30 = 4*7+2 '
           f'from generation 0 ({exact}); every state inside the tube of clock_every_length 7 ({tube})')


def train_ring(t, L):
    return orc_ring(O.train0_cells(0, L - 1), t, L)[t]


def check_train():
    """the line emits the plain train: line N=30, the units between the cap's and the gun's reach equal the oracle train"""
    N = 30
    orb = orc_run(O.line_cells(N), 2 * N + 8)
    tr_orb = orc_run(O.train0_cells(-60, 60), 8)        # valid on units -52..52 at generation <= 8
    for t in range(2 * N, 2 * N + 4):
        found = []
        for ph in range(8):
            for sh in (0, 1):
                want = frozenset(tr(c, sh) for c in tr_orb[ph] if 4 <= unit_of(c) + sh <= 24)
                got = frozenset(c for c in orb[t] if 4 <= unit_of(c) <= 24)
                if want == got:
                    found.append((ph, sh))
        report(len(found) >= 1, f'line N=30 at generation {t}: units 4..24 are the plain train (phase, shift) in {found}')


def check_signals():
    """signal_run: run (train 1 xor sig K u) (2n) = train (1 + 2n) xor sig K (u + dir n), ring of 48 units, whole torus"""
    L = 48
    ring = orc_ring(O.train0_cells(0, L - 1), 2 * L + 2, L)
    for k, (par, cells, d) in O.SIGS.items():
        for u in (par, par + 10, par + 22):
            S0 = ring[1] ^ ringwrap(O.sig_cells(k, u), L)
            T = 2 * L
            orb = orc_ring(S0, T, L)
            good = all(orb[2 * n] == ring[1 + 2 * n] ^ ringwrap(trs(cells, u + d * n), L) for n in range(T // 2 + 1))
            neg = orb[2] == ring[3] ^ ringwrap(trs(cells, u - d), L)
            report(not neg, f"signal {k}: negative control, the signal moved the wrong way fails")
            report(good, f'signal {k} (u = {u}): train(1+2n) xor the signal moved {d:+d}*n units, whole torus, n = 0..{T // 2}')


def check_unzip(kmax=10):
    """unzip_law_sharp: for n >= k+3 the count read at 2n is tape(pulses k (2-n)); not at n = k+2 (nor earlier)"""
    for k in range(1, kmax + 1):
        t0 = time.time()
        nmax = k + 7
        L = k + 4 * nmax + 4                                   # every compared unit's light cone sees one copy
        cells = O.hex_word_cells(O.store_word(k), -4, L - 5) - {tr(O.STATORS8[0], -1)}
        orb = orc_ring(cells, 2 * nmax, L)
        res = []
        for n in range(1, nmax + 1):
            win = range(-1 - 2 * n, k + 2 * n + 1)
            want = ringwrap(O.tape_cells(O.pulses_word(k, 2 - n), win[0], win[-1]), L)
            res.append(ring_units(orb[2 * n], L, win) == want)
        first = next((n for n, r in zip(range(1, nmax + 1), res) if r), None)
        good = all(res[n - 1] == (n >= k + 3) for n in range(1, nmax + 1))
        report(good, f'unzip k={k}: state at 2n = tape(pulses k (2-n)) exactly for n >= {first} (claimed k+3 = {k + 3}), '
               f'checked n = 1..{nmax}, ring of {L} units, units -1-2n..k+2n ({time.time() - t0:.0f} s)')


def check_call(ks=(1, 2, 3, 4, 5)):
    """the call law on the oracle: (a) X_k = V_k disjoint-union Lf and (b) V_k(2n) = k pulses at c+3-(n-14), n >= k+17,
    not at n = k+16; whole torus for (a), the light-cone window for (b)."""
    c = O.CROSS
    L, hy, y0 = 76, 104, -56
    Tmax = 2 * (max(ks) + 19)
    line = frozenset(O.CALL_LINE) | frozenset(O.CALL_CELLS)
    Lf = orc_ring(line, Tmax, L, hy, y0)
    for k in ks:
        t0 = time.time()
        nmax = k + 19
        T = 2 * nmax
        assert L > 3 * k + 44
        wire = O.hex_word_cells(O.store_word(k, c + 1), c - L // 2, c - L // 2 + L - 1)
        X = orc_ring(wire | line, T, L, hy, y0)
        Vpre = orc_ring(wire, 29, L)
        e1 = ringwrap([O.E1], L)
        assert not (e1 & Vpre[29])
        Vpost = orc_ring(Vpre[29] | e1, T - 29, L)
        V = Vpre[:29] + Vpost
        a = all(X[t] == V[t] | Lf[t] and not (V[t] & Lf[t]) for t in range(T + 1))
        res = {}
        for n in range(k + 14, nmax + 1):
            lead = c + 3 - (n - 14)
            win = range(lead - 3, c + k + 5)
            want = ringwrap(O.tape_cells(O.pulses_word(k, lead), win[0], win[-1]), L)
            res[n] = ring_units(V[2 * n], L, win) == want
        b = all(res[n] == (n >= k + 17) for n in res)
        rest = all(Lf[2 * n] == ringwrap(O.CALL_LINE, L) for n in range(21, nmax + 1))
        report(a and b and rest, f'call k={k}: (a) X_k = V_k + Lf, disjoint, whole torus, t = 0..{T}: {a}; (b) V_k(2n) = '
               f'k pulses at c+3-(n-14) exactly for n >= k+17 among n = {k + 14}..{nmax}: {b} {res}; the free line at '
               f'rest from 42: {rest} (ring of {L} units, {time.time() - t0:.0f} s)')


if __name__ == '__main__':
    what = sys.argv[1]
    {'tape': check_tape, 'line': check_line, 'clock': check_clock, 'twoclocks': check_twoclocks,
     'train': check_train, 'signals': check_signals, 'unzip': check_unzip, 'call': check_call}[what]()
    print('ALL PASS' if ok else 'SOME CHECKS FAILED')
    sys.exit(0 if ok else 1)
