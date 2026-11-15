#!/usr/bin/env python3
"""research/gpu/guard.py exercised on the CPU: numpy in place of cupy, a stand-in for gsim.Sim's device arrays (both
word layouts), and planted state sequences of our own (no stepping): every replica runs a sequence of lives; a life is
a run of distinct random states (64 nodes, so no accidental repeat) until its entry age e, then a cycle of period P
through random states (or never enters one). Some replicas are frozen at random boundaries ("the kernel ended the
life") and reseeded. The driver loop is facelaw.run's guard hook, copied (boundary, reset, reseed order).

Checks (exit non-zero on failure):
  1. no life is recognised before it is in its cycle, and a recognised life's state truly repeats (soundness);
  2. a frozen replica is never recognised;
  3. the recognition boundary equals an independent prediction (written here from the rule as stated in guard.py's
     docstring, as a search over the life's own boundary ages, not a port of guard_test.predict);
  4. every cycling life is recognised before the horizon, for fixed, prime, mixed and doubling launch schedules;
  5. the latency b - e (unrecognised time in the cycle) against the stated bound (b - s) + (s - e), and its size.

    python3 research/audit/gpu_local_pr23/guard_cpu.py WORKTREE/research/gpu
"""
import sys, types
import numpy as np

sys.path.insert(0, sys.argv[1])
import guard  # noqa: E402

guard._kernel = lambda: (lambda a, b, axis: np.bitwise_or.reduce(a ^ b, axis=axis))   # cupy ReductionKernel stand-in
N = 64


class FakeSim:
    def __init__(self, WT, kernel):
        self.backend, self.xp, self.kernel = 'gpu', np, kernel
        self.WT, self.n, self.R = WT, N, 32 * WT
        self.A = np.zeros((N + 1) * WT, np.uint32)
        self.frz = np.zeros(WT, np.uint32)

    def _cur(self):
        return self.A

    def _np(self, a):
        return a.copy()

    def put(self, bits):                       # bits (R, N) -> device layout (gsim.set_all's packing)
        by = np.packbits(bits.T, axis=1, bitorder='little')
        cols = np.ascontiguousarray(by).view(np.uint32)
        if self.kernel == 'shared':
            st = np.zeros((self.WT, N + 1), np.uint32); st[:, :N] = cols.T
        else:
            st = np.zeros((N + 1, self.WT), np.uint32); st[:N] = cols
        self.A[...] = st.reshape(-1)

    def freeze(self, reps):
        for r in reps:
            self.frz[r >> 5] |= np.uint32(1) << np.uint32(r & 31)

    def unfreeze(self, reps):
        for r in reps:
            self.frz[r >> 5] &= ~(np.uint32(1) << np.uint32(r & 31))


def h(*k):
    x = 1469598103934665603
    for v in k:
        x = ((x ^ (int(v) & 0xFFFFFFFFFFFFFFFF)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        x ^= x >> 29
    return x


def state(r, life, age, e, P):
    ph = age if (e is None or age < e) else e + (age - e) % P
    x = h(r, life, ph, 7) | (h(r, life, ph, 8) << 64)
    return np.array([(x >> i) & 1 for i in range(N)], bool)


def predict(bounds_age, e, P, first):
    """independent of guard.py's code: the snapshot ages are the first boundary ages crossing first * 2^j (each
    threshold taken once, the latest snapshot replaces the earlier one); recognition is at the first boundary age a
    with some current snapshot s (the latest one taken strictly before a), s >= e and P | (a - s)."""
    if e is None:
        return None, None
    snaps = []                                  # (age taken)
    thr = first
    for a in bounds_age:
        # compare with the latest snapshot taken at an earlier boundary
        if snaps and snaps[-1] >= e and (a - snaps[-1]) % P == 0:
            return a, snaps[-1]
        if a >= thr:
            snaps.append(a)
            while thr <= a:
                thr *= 2
    return None, None


def schedule(kind, horizon):
    out, G, K = [], 0, 1024
    while G < horizon:
        if kind == 'doubling':                   # facelaw: K doubles each launch up to a cap (here 2^18)
            k = K; K = min(2 * K, 1 << 18)
        elif kind == 'mixed':
            k = [997, 1024, 4096][len(out) % 3]
        else:
            k = kind
        G += k; out.append(G)
    return out


def run(WT, kernel, sched, first, horizon, rng):
    s = FakeSim(WT, kernel)
    gd = guard.CycleGuard(s, first=first)
    R = s.R
    life = np.zeros(R, np.int64); birth = np.zeros(R, np.int64)
    params = {}

    def newlife(r):
        u = rng.random()
        if u < 0.15:
            e, P = None, None                       # never cycles
        else:
            e = int(rng.integers(0, 60000)); P = int(rng.choice([1, 2, 3, 9, 13, 48, 52, 66, 129, 997, 1000, 4096, 5000, 12345]))
        params[(r, int(life[r]))] = (e, P)

    for r in range(R):
        newlife(r)
    boundaries = schedule(sched, horizon)
    rec = {}                                   # (r, life) -> (birth, end boundary or None, cause, (age, snap) if guard)
    for G in boundaries:
        bits = np.zeros((R, N), bool)
        for r in range(R):
            e, P = params[(r, int(life[r]))]
            bits[r] = state(r, int(life[r]), G - birth[r], e, P)
        s.put(bits)
        fz = [r for r in range(R) if rng.random() < 0.002]          # the kernel ended these lives in this launch
        s.freeze(fz)
        g_reps, g_snap = gd.boundary(G, birth)
        res = {int(r): (int(G - birth[r]), int(sn)) for r, sn in zip(g_reps, g_snap)}
        for r in fz:
            rec[(r, int(life[r]))] = (int(birth[r]), G, 'freeze', None)
        for r, v in res.items():
            rec[(r, int(life[r]))] = (int(birth[r]), G, 'guard' if r not in fz else 'BOTH', v)
        ended = sorted(set(fz) | set(res))
        gd.reset(np.array(ended, np.int64))
        for r in ended:                                              # reseed
            life[r] += 1; birth[r] = G; newlife(r)
        s.unfreeze(fz)
    for r in range(R):
        rec[(r, int(life[r]))] = (int(birth[r]), None, 'open', None)
    bad = {'unsound': 0, 'frozen_recognised': 0, 'mismatch': 0, 'missed': 0}
    lat, open_cycling = [], 0
    for (r, l), (b0, Ge, cause, v) in rec.items():
        e, P = params[(r, l)]
        upto = [G - b0 for G in boundaries if G > b0 and (Ge is None or G < Ge or (cause != 'freeze' and G == Ge))]
        pa, ps = predict(upto, e, P, first)
        if cause == 'BOTH':
            bad['frozen_recognised'] += 1
        elif cause == 'guard':
            age, sn = v
            if e is None or sn < e or (age - sn) % P:
                bad['unsound'] += 1
            if (pa, ps) != (age, sn):
                bad['mismatch'] += 1
            lat.append((age - e, age - sn, sn - e, e, P))
        elif pa is not None:                    # frozen or open, but the guard should have recognised it before
            bad['missed'] += 1
        elif cause == 'open' and e is not None and e < boundaries[-1] - b0:
            open_cycling += 1
    bad['open_in_cycle_not_yet_due'] = open_cycling
    return bad, lat, len(params)


if __name__ == '__main__':
    rng = np.random.default_rng(23)
    ok = True
    for kernel in ('shared', 'global'):
        for sched, first, hor in ((1024, 16, 1 << 21), (997, 16, 1 << 21), ('mixed', 1000, 1 << 21), ('doubling', 16, 1 << 23)):
            bad, lat, nl = run(4, kernel, sched, first, hor, rng)
            L = np.array(lat) if lat else np.zeros((0, 5))
            this = all(v == 0 for k, v in bad.items() if k != 'open_in_cycle_not_yet_due')
            ok &= this
            rel = (L[:, 0] / np.maximum(L[:, 3], 1)) if len(L) else np.zeros(0)
            print(f'{kernel:6s} launches {str(sched):8s} first {first:4d}: {nl} lives, {len(L)} recognised; {bad}; '
                  f'latency b-e median {np.median(L[:, 0]) if len(L) else 0:.0f}, max {L[:, 0].max() if len(L) else 0:.0f} '
                  f'(grid part b-s max {L[:, 1].max() if len(L) else 0:.0f}); max (b-e)/e {rel.max() if len(rel) else 0:.2f} '
                  f'for e > 1e4: {(rel[L[:, 3] > 1e4]).max() if (L[:, 3] > 1e4).any() else 0:.2f}', flush=True)
    print('OK' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
