"""Cycle guard: recognise replicas that have settled into a cycle of any period (README "Zombie lives").

Kernel B recognises periods 1-2 (kind 2) and 3..pw (kind 3, within the first pw generations of a launch); a replica in
a longer cycle was never recognised and added exposure until the run ended. The guard closes that gap. It runs on the
host side between launches, on the state buffer, and does not touch the kernels: with the guard off nothing differs
from before, and with it on the stepping is unchanged (it only reads the state).

Rule (AGENT.md "To do", option (i)):
  * every replica keeps one snapshot of its own state. A new snapshot is taken at the first launch boundary at which
    the replica's age is >= first * 2^j (j = 0, 1, 2, ...), replacing the previous one. The snapshot ages
    (first, 2 first, 4 first, ...: the thresholds; the actual ages are the boundaries that crossed them) are a
    parameter of the result and must be stated with it.
  * at every launch boundary, a live replica (not frozen by the kernel) that has a snapshot and whose state equals it
    is periodic, with period dividing (age - snapshot age). Its life ends there as KIND (= 5), at the boundary
    generation: "censored at the first exact match". Like kinds 2 and 3 it is censored, never a death.

Completeness: a replica that enters a cycle of period P at age e is caught at the first boundary b with a snapshot
taken at an age s >= e (so the snapshot lies on the cycle) and P | (b - s). With launches of a fixed length K after
the warm-up, b - s runs over multiples of K, so a match comes within lcm(K, P) generations of s, and the doubling
snapshot schedule guarantees some snapshot interval exceeds that. Upper bound on the unrecognised (zombie) time of a
caught life: (b - e) <= (b - s) + (s - e), both terms recorded per life (`snap_age`).

Order at a boundary: compare first, then take the snapshots that are due (so a replica is never compared with a
snapshot taken at the same boundary).

Exposure note: for estimators that count exposure to the end of every life, a kind-5 life contributes its time in the
cycle up to detection (at most the bound above). Drivers record `snap_age` so that exposure can instead be cut at the
snapshot age if wanted (the cycle was certainly entered by then).
"""
import numpy as np

KIND = 5            # kinds in use: 0 open at the end, 1 face death, 2 period 1-2, 3 period 3..pw, 4 firewall (fwslab)

_xor_or = None


def _kernel():
    global _xor_or
    if _xor_or is None:
        import cupy as cp
        _xor_or = cp.ReductionKernel('uint32 a, uint32 b', 'uint32 y', 'a ^ b', 'a | b', 'y = a', '0', 'gump_guard_xor_or')
    return _xor_or


class CycleGuard:
    def __init__(self, sim, first=16):
        assert sim.backend == 'gpu'
        self.s, self.first = sim, int(first)
        self.xp = sim.xp
        self.snap = self.xp.zeros_like(sim.A)
        R = sim.R
        self.snap_age = np.full(R, -1, np.int64)          # age at which the current snapshot was taken (-1: none)
        self.next_age = np.full(R, self.first, np.int64)  # take the next snapshot at the first boundary with age >= this
        self.compares = 0

    def _shape(self, a):
        s = self.s
        return a.reshape(s.WT, s.n + 1) if s.kernel == 'shared' else a.reshape(s.n + 1, s.WT)

    def _words_to_bits(self, w):
        return np.unpackbits(np.ascontiguousarray(w, np.uint32).view(np.uint8), bitorder='little').astype(bool)

    def _bits_to_words(self, b):
        return np.packbits(b, bitorder='little').view(np.uint32)

    def boundary(self, G, birth):
        """call right after a launch ends at generation G, before any reseed. birth: (R,) generation of each replica's
        birth. Returns (reps, snap_age): live replicas whose state equals their snapshot, with that snapshot's age."""
        age = G - np.asarray(birth, np.int64)
        live = ~self._words_to_bits(self.s._np(self.s.frz))
        hit = self._compare(live)
        reps = np.nonzero(hit)[0]
        out = (reps, self.snap_age[reps].copy())
        self._take(live & ~hit & (age >= self.next_age), age)
        return out

    def _compare(self, live):
        s = self.s
        hit = np.zeros(s.R, bool)
        cand = live & (self.snap_age >= 0)
        if cand.any():
            axis = 1 if s.kernel == 'shared' else 0
            diff = s._np(_kernel()(self._shape(s._cur()), self._shape(self.snap), axis=axis))  # per column: OR of state ^ snapshot
            hit = cand & ~self._words_to_bits(diff)
            self.compares += 1
        return hit

    def _take(self, due, age):
        if not due.any():
            return
        s = self.s
        cur, snap = self._shape(s._cur()), self._shape(self.snap)
        m = self.xp.asarray(self._bits_to_words(due))
        mm = m[:, None] if s.kernel == 'shared' else m[None, :]
        snap[...] = (snap & ~mm) | (cur & mm)
        self.snap_age[due] = age[due]
        na = self.next_age[due]
        while True:                                                       # next threshold above the current age
            low = na <= age[due]
            if not low.any():
                break
            na[low] *= 2
        self.next_age[due] = na

    def reset(self, reps):
        """forget the snapshots of replicas that are reseeded (a new life starts)."""
        reps = np.asarray(reps, np.int64)
        self.snap_age[reps] = -1
        self.next_age[reps] = self.first
