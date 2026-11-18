#!/usr/bin/env python3
"""prove_unzip8 (push 8): the count read releases exactly k pulses for EVERY k (base facts on reference/oracle.py).

    python3 prove_unzip8.py [--K0 10]

Statement.  Wire B with a stretch of k units of wire B' and its edge unit (hex letters ...777 d^k f 777...), the first
d at unit w.  At an even generation (phase 0) remove the stator (0,1,2) of unit w - 1.  Then for every k >= 1 the
wire becomes plain wire B carrying exactly k left-going pulses (units of wire C) two units apart, the leading one at
unit w + 2 - t/2 at even generation t (t >= 4k + 8), and nothing else.

Proof.  X_k(t): the orbit for length k.  tau: the move by one unit towards +v.  A cell's neighbours lie in its own
unit and the two next to it.
  k <= K0: direct runs (check A).
  k -> k + 1 for k >= K0.  Let m(t), t >= 2, be a path of units with |m(t+1) - m(t)| <= 1, m(t) <= m(t-2) + 1 and
  w + 3 <= m(2) <= w + K0 - 4, such that X_k(t) and tau X_k(t - 2) agree on units m(t) - 1 .. m(t) + 1 for every
  t >= 2 (hypothesis H(k)).  Put Y(t) = X_k(t) on units <= m(t) + 1 and tau X_k(t - 2) on units >= m(t).  Both are
  orbits and they agree on the overlap, and the seam moves at most one unit per generation, so Y obeys the rule
  for t >= 2.  Y(2) = X_{k+1}(2): on units <= m(2) + 1 <= w + k - 3 the two starts differ only at units >= w + k, two
  generations away; on units >= m(2) >= w + 3 the start of X_{k+1} is the standing stretch, unchanged after two
  generations, and so is tau X_k(0).  Hence Y = X_{k+1} for t >= 2.  H(k + 1) holds with the same path: on units
  <= m(t) + 1 (which is <= m(t-2) + 2) the pair (X_{k+1}(t), tau X_{k+1}(t-2)) is the pair (X_k(t), tau X_k(t-2)).
  The end state: the left chart gives the leading pulse, the right chart the k pulses of X_k one unit on and two
  generations late, i.e. two units behind the leading one: k + 1 pulses two units apart.
  Checked here on the oracle for k = K0 (check B): a path m(t) exists for 2 <= t <= T = 4 K0 + 40 (found by
  dynamic programming over the units where the two states agree), and it ends at m(T) = (leading pulse) + 3 with
  the whole state at T equal to plain wire B with K0 pulses.  For t > T the state is a word of units of wire B and
  wire C, which moves rigidly one unit per 2 generations towards -v (the tape theorem, README section 10, proved
  there for all words), so the path continues for ever with m(t + 2) = m(t) - 1.
  Check C (not needed for the proof): Y built from X_K0 equals the oracle's own run of X_{K0+1} at every generation.

The runs are finite objects (capL + 7^70 + d^k f + 7^14 + capL turned round) on the oracle's box torus
(2L x 16 x 2L, L = 110); within T generations nothing reaches a cap, so on the units compared they are the runs of
the infinite wire.  Prints PASS lines and ALL PASS.
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402

D = json.load(open(os.path.join(HERE, 'objects', 'cell8.json')))
NLEFT, NRIGHT, LRING, HY = 70, 14, 110, 16
SHAPE = (2 * LRING, HY, 2 * LRING)
PAR = np.indices(SHAPE) % 2
M = [(PAR[a] == 1) & (PAR.sum(0) == 1) for a in range(3)]
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
W0 = 4 + NLEFT                      # unit of the first d


def arr(cells):
    h = np.zeros(SHAPE, np.int8)
    for c in cells:
        h[c[0] % SHAPE[0], c[1] % SHAPE[1], c[2] % SHAPE[2]] = 1
    assert not (h & ~(M[0] | M[1] | M[2])).any()
    return h


def state(word):
    cells = set(map(tuple, D['capL']))
    for i, ch in enumerate(word):
        hx = int(ch, 16)
        cells |= {tr(c, 4 + i) for c in D['stators']} | {tr(D['sites'][j], 4 + i) for j in range(4) if hx >> j & 1}
    return cells | {tr(c, 4 + len(word)) for c in D['capR']}


def orbit(k, T):
    h = arr(state('7' * NLEFT + 'd' * k + 'f' + '7' * NRIGHT))
    c = tr((0, 1, 2), W0 - 1); assert h[c[0], c[1] % HY, c[2] % SHAPE[2]] == 1
    h[c[0], c[1] % HY, c[2] % SHAPE[2]] = 0
    out = [h]
    for _ in range(T):
        h = oracle.step(h, M); out.append(h)
    return out


def tau(h):
    return np.roll(h, (2, -2), axis=(0, 2))


def units(h, a, b):
    """the slab of units a..b (x from 2a to 2b + 1); all units here are in 0..LRING-1"""
    return h[2 * a: 2 * b + 2]


def pulses(k, t):
    """plain wire with k left-going pulses, leading one at unit W0 + 2 - t/2 (even t)"""
    w = ['7'] * (NLEFT + k + 1 + NRIGHT)
    for p in range(k):
        w[W0 + 2 - t // 2 + 2 * p - 4] = 'b'
    return arr(state(''.join(w)))


def main():
    K0 = int(sys.argv[sys.argv.index('--K0') + 1]) if '--K0' in sys.argv else 10
    ok_all = True; t0 = time.time()

    def report(ok, text):
        nonlocal ok_all
        ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - t0:.0f} s]', flush=True)

    # A: k = 1..K0 directly
    okA = True
    for k in range(1, K0 + 1):
        T = 4 * k + 8
        X = orbit(k, T + 4)
        okA &= np.array_equal(X[T], pulses(k, T)) and np.array_equal(X[T + 4], pulses(k, T + 4))
    report(okA, f'A  k = 1..{K0}: at generations 4k + 8 and 4k + 12 the whole state is the plain wire with exactly k left-going pulses two units apart')
    # B: the path for k = K0
    T = 4 * K0 + 40
    X = orbit(K0, T + 8)
    lo, hi = W0 - T // 2 - 6, W0 + K0 + 6
    agree = {}
    for t in range(2, T + 9):
        Z = tau(X[t - 2])
        agree[t] = {u for u in range(lo, hi) if np.array_equal(units(X[t], u - 1, u + 1), units(Z, u - 1, u + 1))}
    # dynamic programming: reachable (m(t-1), m(t)) pairs
    start = [u for u in agree[2] if W0 + 3 <= u <= W0 + K0 - 4]
    reach = {(None, u): None for u in start}; back = [dict(reach)]
    cur = {(u, u) for u in start}       # (m(t-2) stand-in, m(t-1)) at t = 2: use (m2, m2)
    hist = [cur]
    for t in range(3, T + 9):
        nxt = set()
        for (a, b) in hist[-1]:
            for u in (b - 1, b, b + 1):
                if u in agree[t] and u <= a + 1:
                    nxt.add((b, u))
        hist.append(nxt)
    lead = lambda t: W0 + 2 - t // 2
    endok = any(b == lead(T) + 3 for (a, b) in hist[T - 2]) and all(lead(t) + 3 in agree[t] for t in range(T, T + 9, 2))
    report(bool(start) and all(hist) and endok,
           f'B  k = {K0}: a seam path m(t) exists for t = 2..{T} (m(2) in [w + 3, w + {K0 - 4}], steps <= 1, m(t) <= m(t-2) + 1), ending 3 units behind the leading pulse; '
           f'sizes of the agreement sets from {min(len(agree[t]) for t in agree)} units')
    report(np.array_equal(X[T], pulses(K0, T)) and np.array_equal(X[T + 8], pulses(K0, T + 8)),
           f'B  k = {K0}: at generations {T} and {T + 8} the whole state is the plain wire with {K0} pulses (a word of B and C units: rigid for ever by the tape theorem)')
    # C: the glued orbit against the oracle's own X_{K0+1}, with one concrete path
    path = {}
    # recover one path backwards
    b = lead(T) + 3; a = next(a_ for (a_, b_) in hist[T - 2] if b_ == b)
    path[T] = b; path[T - 1] = a
    for t in range(T - 1, 2, -1):
        prev = next(a_ for (a_, b_) in hist[t - 2] if b_ == path[t] and path[t + 1] <= a_ + 1) if t + 1 <= T else None
        path[t - 1] = prev
    Xn = orbit(K0 + 1, T)
    okC = True
    for t in range(2, T + 1):
        m = path[t]
        Y = tau(X[t - 2]).copy(); Y[: 2 * m + 2] = X[t][: 2 * m + 2]
        okC &= np.array_equal(Y, Xn[t])
    report(okC, f'C  the glued orbit built from X_{K0} equals the oracle run of X_{K0 + 1} at every generation 2..{T}')
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
