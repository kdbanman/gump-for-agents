"""Claim 4 (README section 18): turn classes of rake-turning caps, measured with our own code (gs.Dom on the
diagonal hull, exact by T2; `--oracle` repeats a run on reference/oracle.py).

Conventions (README): rake f at unit u at an even generation t: a = t - 2u.  Mirror rake '5f' ('5' at unit u) at
even t: b = t + 2u.  A right turn has constant b - a, a left turn a' - b.  Round a clock a advances by P, so
P = (b - a) + (a' - b) exactly; the content of the claim is that each bracket is a constant of its cap (plus 4 x
its first unit), whatever arrives before the rake and whatever the other cap is.  We report the exact constants
c_R = (b - a) - 4 K_R, c_L = (a' - b) + 4 K_L (K_R the first unit of the right cap, K_L = 0 the first unit of
the wire after capL), measured (i) for a lone rake / lone mirror rake and (ii) inside lit clocks.

    python3 turn_check.py clockC [N ...]           capR / capL of clock-C: lone constants, and in clocks of length N
    python3 turn_check.py table FILE [--max M]     each cap of a clocks_*.json list: lone c_R and in a clock
    python3 turn_check.py k2 [FILE]                the k = 2 caps (frame: first cap unit 10): lone turn, survival,
                                                   and in clocks with capL
"""
import hashlib, json, os, sys
import numpy as np
import r3
from r3 import tr, unit, uc
SCR = os.path.join(r3.gs.ROOT, 'research', 'scratch', 'signals')


def wireC(a, b):
    return set().union(*[uc('C', u) for u in range(a, b)]) if b > a else set()


def find_mirror(S, lo, hi):
    """units u with '5f' at (u, u+1), lo <= u < hi."""
    d = r3.dec(S, lo - 1, hi + 2)
    return [lo - 1 + i for i in range(1, len(d) - 1) if d[i:i + 2] == '5f' and d[i - 1] in 'b7' and lo - 1 + i < hi]


def find_rake(S, lo, hi):
    d = r3.dec(S, lo - 1, hi + 1)
    return [lo - 1 + i for i in range(1, len(d) - 1) if d[i] == 'f' and d[i - 1] in 'b7' and lo - 1 + i < hi and lo - 1 + i >= lo]


def H(x):
    return hashlib.blake2b(x.tobytes(), digest_size=16).digest()


def lone_right(cap, K, r=None, T=None, pre=None):
    """cap: cells with first unit K.  capL at the left end, wire C on 0..K-1, rake at unit r at t = 0.
    pre: optional extra cells (e.g. a p> train ahead of the rake).  Returns dict."""
    r = r if r is not None else K - 12
    base = set(r3.capL) | wireC(0, K) | set(cap)
    st = set(base) ^ uc('C', r) ^ uc(0xf, r)
    if pre:
        st ^= pre
    run = r3.Run(st, extra=base)
    a = -2 * r; out = {'a': a}
    T = T or 2 * (K - r) + 80
    t = 0; seen_m = None
    while t < T:
        run.step(2); t += 2
        S = run.cells()
        ms = find_mirror(S, 0, K - 3)
        if ms and seen_m is None:
            u = max(ms)
            run2 = r3.Run(S, extra=base); run2.step(2)
            if (u - 1) in find_mirror(run2.cells(), 0, K - 3):
                seen_m = (t, u); out['b'] = t + 2 * u; out['bma'] = t + 2 * u - a; out['cR'] = t + 2 * u - a - 4 * K
                out['k'] = (t + 2 * u - a) % 4
                break
    return out, run


def ref_cycle(cap, K, D=None):
    """the cap region (units >= K-1) when the cap eats a long p> train (spacing 2), 4 consecutive generations
    long after the train began, as a cyclic list.  None if the region is not periodic with period dividing 4."""
    base = set(r3.capL) | wireC(0, K) | set(cap)
    st = set(base)
    for u in range(4, K - 3, 2):                      # p>: remove (1,0,2) of unit u, add (1,0,4) of u+1
        st ^= {tr((1, 0, 2), u), tr((1, 0, 4), u + 1)}
    run = r3.Run(st, extra=base)
    run.step(2 * K - 40 if K > 30 else 20)
    reg = lambda S: frozenset(c for c in S if unit(c) >= K - 1)
    seq = []
    for i in range(8):
        seq.append(reg(run.cells())); run.step(1)
    return seq[:4] if seq[:4] == seq[4:] else None


def clock_run(capR_cells, N, ign_unit=None, T=None, kymo=0):
    """capL + N units of wire C + capR_cells (first unit N), lit by (1,0,4) at unit ign_unit.  gs stepping.
    Returns (transient, period, events) where events lists (t, 'R' a | 'M' b) of rake / mirror-rake passings."""
    base = set(r3.capL) | wireC(0, N) | set(capR_cells)
    ign = tr((1, 0, 4), N // 2 if ign_unit is None else ign_unit)
    run = r3.Run(base | {ign}, extra=base)
    seen = {H(run.x): 0}; t = 0; T = T or 40 * N + 800; ev = []; ky = []
    while t < T:
        run.step(1); t += 1
        if t % 2 == 0:
            S = run.cells()
            for u in find_rake(S, 1, N - 1):
                ev.append((t, 'R', t - 2 * u, u))
            for u in find_mirror(S, 1, N - 2):
                ev.append((t, 'M', t + 2 * u, u))
            if t <= kymo:
                ky.append('%4d %s' % (t, r3.dec(S, -4, N + 8)))
        k = H(run.x)
        if k in seen:
            return seen[k], t - seen[k], ev, ky
        seen[k] = t
    return None, None, ev, ky


def clock_constants(ev, N, P):
    """from the passings: in-clock c_R = (b - a) - 4N and c_L = (a' - b), taking a then the next b, then the next a."""
    seq = []                                    # distinct passings in time order: ('R', a) / ('M', b)
    for t, k, v, u in ev:
        if not seq or seq[-1] != (k, v):
            if (k, v) not in seq:
                seq.append((k, v))
    out = []
    for i in range(len(seq) - 2):
        if seq[i][0] == 'R' and seq[i + 1][0] == 'M' and seq[i + 2][0] == 'R':
            a, b, a2 = seq[i][1], seq[i + 1][1], seq[i + 2][1]
            out.append((b - a - 4 * N, a2 - b, a2 - a))
    return sorted(set(out)), ''.join(k for k, v in seq)


def main():
    cmd = sys.argv[1]
    if cmd == 'clockC':
        K = 40
        capR = {tr(c, K) for c in r3.capR0}
        o, _ = lone_right(capR, K); print('clock-C capR, lone rake from 12 units: ', o)
        o, _ = lone_right(capR, K, r=K - 25); print('clock-C capR, lone rake from 25 units:', o)
        print('clock-C capR eats a p> train with a period-4 cycle:', ref_cycle(capR, K) is not None)
        for N in map(int, sys.argv[2:]):
            tr0, P, ev, _ = clock_run({tr(c, N) for c in r3.capR0}, N)
            print(f'clock N={N}: transient {tr0} period {P} (4N+2 = {4*N+2}); in-clock (c_R, c_L) pairs: {clock_constants(ev, N, P)}')
    elif cmd == 'table':
        L = json.load(open(sys.argv[2])); mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 10 ** 9
        for e in L[:mx]:
            cap0 = [tuple(c) for c in e['cap']]
            K = 40; o, _ = lone_right({tr(c, K) for c in cap0}, K)
            res = []
            for N in (5, 8):
                tr0, P, ev, _ = clock_run({tr(c, N) for c in cap0}, N)
                res.append((N, P, clock_constants(ev, N, P)))
            print(f"state {e['state']}: lone c_R {o.get('cR')} k {o.get('k')}; clocks (N, P, in-clock (c_R, c_L)): {res}", flush=True)
    elif cmd == 'k2':
        F = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCR, 'k2caps_16_47.json')
        if F.endswith('turn-k2-cap-5x5.json'):
            caps = [[tuple(c) for c in json.load(open(F))['cap']]]
        else:
            caps = [[tuple(c) for c in e['cap']] for e in json.load(open(F))]
        for i, cap0 in enumerate(caps):
            K = 40; cap = {tr(c, K - 10) for c in cap0}
            # stationary?
            base = set(r3.capL) | wireC(0, K) | cap
            run = r3.Run(base); run.step(2)
            stat = run.cells() == frozenset(base)
            o, run = lone_right(cap, K)
            ref = ref_cycle(cap, K)
            # survival after the lone turn: cap region against the reference p>-eating cycle, 40..48 gens after turn
            surv = None
            if 'b' in o and ref is not None:
                run.step(40); seq = []
                for j in range(4):
                    seq.append(frozenset(c for c in run.cells() if unit(c) >= K - 1)); run.step(1)
                surv = any(seq == ref[s:] + ref[:s] for s in range(4))
            print(f'#{i} {len(cap0)} cells: stationary {stat}; lone turn {o}; eats a p> train periodically: {ref is not None}; '
                  f'cap region after the turn on that cycle: {surv}', flush=True)
            for N in (5, 6, 9):
                tr0, P, ev, ky = clock_run({tr(c, N - 10) for c in cap0}, N, kymo=0)
                print(f'    clock N={N}: enters cycle at {tr0}, period {P}; in-clock (c_R, c_L): {clock_constants(ev, N, P)}', flush=True)


if __name__ == '__main__':
    main()
