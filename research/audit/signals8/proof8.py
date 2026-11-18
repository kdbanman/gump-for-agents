#!/usr/bin/env python3
"""proof8 (REVIEW-signals-8): the facts under "the count read releases exactly k pulses for every k", on the oracle.

    python3 proof8.py [--K0 10] [--direct 11,12,...]

The push's argument (docstring of prove_unzip8.py): X_k(t) = the orbit of the infinite wire ...777 d^k f 777... (first
d at unit w) after the stator (0,1,2) of unit w - 1 is removed at generation 0; tau = the move by one unit towards
+v.  H(k): a path m(t), t >= 2, with |m(t+1) - m(t)| <= 1, m(t) <= m(t-2) + 1, w + 3 <= m(2) <= w + K0 - 4, such that
X_k(t) = tau X_k(t-2) on units m(t)-1 .. m(t)+1.  Then X_{k+1}(t) = X_k(t) on units <= m(t) + 1 and tau X_k(t-2) on
units >= m(t), and H(k+1) holds with the same path.

What is checked here, with a8.Orc (oracle.step, nothing wrapping) on finite cells capL + 7^nl d^k f 7^nr + right cap:

  T  the tape theorem for the words used: a ring of 32 units of {7, b} holding every run of five (a de Bruijn word)
     is itself moved one unit towards -v after 2 generations (oracle.step on the ring torus 64 x 16 x 64).
  A  k = 1..K0: at every even generation t from 4k + 8 to 4k + 28 the whole state is the plain cell with exactly k
     units b two apart, the leading one at unit w + 2 - t/2.
  F  (not in the push's script) for every k run here and every generation 0..T the run equals the standing plain
     cell on all units <= lead(t) - 4 and on all units >= w + k + 3, at the right phase: nothing ever comes near a
     cap, so by gluing with the standing cap the finite run IS the infinite wire's run on the units between.
  B  H(K0) on 2 <= t <= T = 4 K0 + 40 by my own dynamic programme (agreement on units m-1..m+1 of the whole slab),
     with m(T) = lead(T) + 3; and the continuation used for t > T, m(T + 2j) = m(T + 2j + 1) = lead(T) + 3 - j, checked at
     BOTH parities for T <= t <= T + 12 (the push's script checks even t only; the odd ones follow from the tape
     theorem by one step of the rule, see the review).
  S  the two places the docstring passes over: H(k+1) at t = 2 and t = 3 (where tau X(t-2) is not yet covered by
     the glued orbit) is checked directly for k + 1 = K0 + 1 and K0 + 2 along the same path, at every t = 2..T.
  D  direct runs for larger k (the theorem's conclusion, not part of the proof): the whole state at 4k + 8 and 4k + 12.
"""
import sys, time
import numpy as np
import a8
from a8 import tr, SR

sys.path.insert(0, a8.os.path.join(a8.ROOT, 'reference'))
import oracle  # noqa: E402

T0 = time.time(); OK = [True]


def say(ok, text):
    OK[0] &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - T0:.0f} s]', flush=True)


def tape_ring():
    # a de Bruijn word of order 5 over {7, b}
    seq = [0] * 5; seen = {tuple(seq)}
    while len(seq) < 32 + 4:
        for bit in (1, 0):
            cand = tuple(seq[-4:] + [bit])
            if cand not in seen:
                seen.add(cand); seq.append(bit); break
        else:
            raise RuntimeError('no de Bruijn extension')
    word = ''.join('b' if v else '7' for v in seq[:32])
    assert len({tuple(word[(i + j) % 32] for j in range(5)) for i in range(32)}) == 32
    L = 32; shape = (2 * L, 16, 2 * L)
    par = np.indices(shape) % 2
    m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]

    def arr(w):
        h = np.zeros(shape, np.int8)
        for c in a8.word_cells(w, 0):
            i = (c[0] % shape[0], c[1] % shape[1], c[2] % shape[2]); assert m[0][i] or m[1][i] or m[2][i]
            h[i] = 1
        return h
    h = arr(word); ok = True
    for j in range(1, 41):
        h = oracle.step(oracle.step(h, m), m)
        ok &= np.array_equal(h, arr(word[j % 32:] + word[:j % 32]))
    say(ok, f'T  tape: the ring {word} (every run of five over 7, b) is moved one unit towards -v every 2 generations, j = 1..40 (oracle, ring torus 64 x 16 x 64)')


class Orbit:
    def __init__(self, k, T, nr=14):
        self.k = k; self.nl = T // 2 + 24; self.nr = nr; self.w = 4 + self.nl
        self.word = '7' * self.nl + 'd' * k + 'f' + '7' * nr; self.N = len(self.word)
        self.O = a8.Orc(-6, self.N + 16)
        h = self.O.arr(a8.cell_state(self.word)); self.O.kill(h, tr(SR, self.w - 1))
        plain = self.O.arr(a8.cell_state('7' * self.N)); self.plain = [plain, self.O.run(plain, 1)]
        self.X = [h]
        for _ in range(T):
            self.X.append(self.O.run(self.X[-1], 1))

    def lead(self, t):
        return self.w + 2 - t // 2

    def sl(self, h, ua, ub):
        """the whole slab of units ua..ub"""
        x0 = 2 * ua - self.O.o[0]
        return h[x0: x0 + 2 * (ub - ua + 1)]

    def pulses(self, t):
        w = ['7'] * self.N
        for j in range(self.k):
            w[self.lead(t) + 2 * j - 4] = 'b'
        return self.O.arr(a8.cell_state(''.join(w)))

    def far_ok(self, T):
        """F: at every generation the run is the standing plain cell left of lead(t) - 4 (and of w - 4 early on) and right of w + k + 3"""
        for t in range(T + 1):
            left = min(self.w - 4, self.lead(t) - 4); p = self.plain[t % 2]
            if not np.array_equal(self.sl(self.X[t], -6, left), self.sl(p, -6, left)):
                return False
            if not np.array_equal(self.sl(self.X[t], self.w + self.k + 3, self.N + 15), self.sl(p, self.w + self.k + 3, self.N + 15)):
                return False
        return True

    def tau(self, h):
        """the state moved one unit towards +v: (x, z) -> (x + 2, z - 2); the array's rim is dead"""
        return np.roll(h, (2, -2), axis=(0, 2))


def agree_sets(ob, T, lo, hi):
    ag = {}
    for t in range(2, T + 1):
        Z = ob.tau(ob.X[t - 2])
        ag[t] = {u for u in range(lo, hi) if np.array_equal(ob.sl(ob.X[t], u - 1, u + 1), ob.sl(Z, u - 1, u + 1))}
    return ag


def find_path(ag, w, K0, T, end):
    """a path m(2..T) with steps <= 1, m(t) <= m(t-2) + 1, start in [w+3, w+K0-4], m(T) = end; None if there is none"""
    layers = [{(u, u): None for u in ag[2] if w + 3 <= u <= w + K0 - 4}]
    for t in range(3, T + 1):
        nxt = {}
        for (a, b) in layers[-1]:
            for u in (b - 1, b, b + 1):
                if u in ag[t] and u <= a + 1 and (b, u) not in nxt:
                    nxt[(b, u)] = (a, b)
        layers.append(nxt)
    last = [s for s in layers[-1] if s[1] == end]
    if not last:
        return None
    s = last[0]; path = {T: s[1]}
    for t in range(T, 2, -1):
        prev = layers[t - 2][s]; path[t - 1] = s[0]; s = prev
    return path


def main():
    K0 = int(sys.argv[sys.argv.index('--K0') + 1]) if '--K0' in sys.argv else 10
    direct = [int(v) for v in sys.argv[sys.argv.index('--direct') + 1].split(',')] if '--direct' in sys.argv else [11, 12, 13, 14, 15, 16, 20, 25, 30, 40]
    tape_ring()
    okA = okF = True; first = []
    for k in range(1, K0 + 1):
        T = 4 * k + 28; ob = Orbit(k, T)
        okA &= all(np.array_equal(ob.X[t], ob.pulses(t)) for t in range(4 * k + 8, T + 1, 2))
        first.append(next(t for t in range(0, T + 1, 2) if np.array_equal(ob.X[t], ob.pulses(t))))
        okF &= ob.far_ok(T)
    say(okA, f'A  k = 1..{K0}: at every even generation 4k + 8 .. 4k + 28 the whole state is the plain cell with exactly k units b two apart, leading one at unit w + 2 - t/2')
    say(first == [2 * k + 6 for k in range(1, K0 + 1)], f'A  ... and it is so from generation 2k + 6 on, not only from 4k + 8 (first even generation, k = 1..{K0}: {first})')
    say(okF, f'F  k = 1..{K0}: at every generation the run is the standing plain cell on all units <= lead - 4 and >= w + k + 3: nothing nears a cap; the runs are the infinite wire\'s')
    T = 4 * K0 + 40; TT = T + 12
    ob = Orbit(K0, TT, nr=16)
    say(ob.far_ok(TT), f'F  k = {K0}, generations 0..{TT}: the same')
    lo, hi = ob.w - TT // 2 - 8, ob.w + K0 + 8
    ag = agree_sets(ob, TT, lo, hi)
    path = find_path(ag, ob.w, K0, T, ob.lead(T) + 3)
    say(path is not None, f'B  H({K0}) on t = 2..{T}: a seam path exists with m(2) in [w + 3, w + {K0 - 4}] and m({T}) = lead + 3' +
        ('' if path is None else f"; one such path relative to w: {[path[t] - ob.w for t in range(2, T + 1, 6)]} (every 6th)"))
    cont = {T + i: ob.lead(T) + 3 - i // 2 for i in range(0, 13)}
    say(all(cont[t] in ag[t] for t in cont) and np.array_equal(ob.X[T], ob.pulses(T)),
        f'B  the continuation m(T + 2j) = m(T + 2j + 1) = lead(T) + 3 - j agrees at every t = {T}..{TT}, both parities; the state at {T} is the plain cell with {K0} pulses')
    # how wide is the choice?
    say(True, f'B  (size of the agreement sets on units {lo}..{hi - 1}: from {min(len(v) for v in ag.values())} to {max(len(v) for v in ag.values())} units)')
    if path is not None:
        full = dict(path); full.update(cont)
        okS = True; okG = True
        prev = ob
        for kk in (K0 + 1, K0 + 2):
            ob2 = Orbit(kk, TT, nr=16 - (kk - K0))          # the same array as ob: equal total length
            assert ob2.O.shape == ob.O.shape and ob2.O.o == ob.O.o
            sh = ob2.w - ob.w
            for t in range(2, TT + 1):
                mt = full[t] + sh
                Z = ob2.tau(ob2.X[t - 2])
                okS &= np.array_equal(ob2.sl(ob2.X[t], mt - 1, mt + 1), ob2.sl(Z, mt - 1, mt + 1))
            # the glued orbit: X_{kk}(t) = X_{kk-1}(t) on units <= m + 1, tau X_{kk-1}(t-2) on units >= m, compared on the units both runs hold away from caps
            shp = ob2.w - prev.w
            for t in range(2, TT + 1):
                mt = full[t] + sh
                a_lo = ob2.w - TT // 2 - 10; a_hi = ob2.w + kk + 8
                left = ob2.sl(ob2.X[t], a_lo, mt + 1); want_left = prev.sl(prev.X[t], a_lo - shp, mt + 1 - shp)
                right = ob2.sl(ob2.X[t], mt, a_hi); want_right = prev.sl(prev.tau(prev.X[t - 2]), mt - shp, a_hi - shp)
                okG &= left.shape == want_left.shape and np.array_equal(left, want_left) and np.array_equal(right, want_right)
            okS &= ob2.far_ok(TT)
            prev = ob2
        say(okS, f'S  H({K0 + 1}) and H({K0 + 2}) hold along the same path at every t = 2..{TT} (t = 2, 3 included), on direct runs')
        say(okG, f'S  the direct runs of k = {K0 + 1}, {K0 + 2} are the glued orbits (left chart X_(k-1)(t) up to m + 1, right chart tau X_(k-1)(t-2) from m) at every t = 2..{TT}')
    okD = True; done = []
    for k in direct:
        T = 4 * k + 12; ob = Orbit(k, T, nr=8)
        good = np.array_equal(ob.X[4 * k + 8], ob.pulses(4 * k + 8)) and np.array_equal(ob.X[T], ob.pulses(T)) and ob.far_ok(T)
        okD &= good; done.append(k)
        print(f'     direct k = {k}: {good}  [{time.time() - T0:.0f} s]', flush=True)
    say(okD, f'D  direct oracle runs, k in {done}: exactly k pulses two apart at 4k + 8 and 4k + 12, nothing else, nothing near a cap')
    print('ALL PASS' if OK[0] else 'SOME FAIL')
    sys.exit(0 if OK[0] else 1)


if __name__ == '__main__':
    main()
