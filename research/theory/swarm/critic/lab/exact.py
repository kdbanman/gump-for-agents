"""Critic's lab, part 1: exact tools on small finite vessels (no sampling anywhere).

A vessel is a finite cell graph: nb[i] = list of the neighbours of cell i that lie inside the vessel
(cells outside are dead forever; that is exact for the vessels used here, by confinement).
A state is an integer 0 <= s < 2^N, bit i = cell i alive.

  full_map(nb, B, S)        F[s] = successor of s, for every state (uint32 array of length 2^N), N <= 26
  step_state(nb, B, S, s)   one state, plain Python (used to cross-check full_map)
  death_times(F, living)    T[s] = min{t >= 0 : F^t(s) is not living}, -1 if the orbit is living for ever
  cyclic(F)                 boolean array: s lies on a cycle
  periods(F, cyc)           dict period -> number of cyclic states with that period

"Living" is supplied by the caller as a boolean array over states (e.g. "every edge row non-empty").
THE TRAP (it has bitten four agents): a state whose orbit is living for ever has settled into a cycle
that keeps every edge occupied (debris). It is not "long-lived chaos"; death_times returns -1 for it and
every lifetime statistic must leave it out or report it separately.
"""
import numpy as np


def full_map(nb, B, S, chunk_bits=20):
    """B, S: iterables of neighbour counts giving birth / survival."""
    N = len(nb)
    assert N <= 26, "2^N states must fit in memory"
    K = max(len(v) for v in nb)
    Bt = np.zeros(K + 1, np.uint8); St = np.zeros(K + 1, np.uint8)
    for k in B:
        if k <= K: Bt[k] = 1
    for k in S:
        if k <= K: St[k] = 1
    total = 1 << N
    F = np.empty(total, np.uint32)
    cb = min(chunk_bits, N)
    for lo in range(0, total, 1 << cb):
        s = np.arange(lo, lo + (1 << cb), dtype=np.uint32)
        bits = [((s >> np.uint32(i)) & np.uint32(1)).astype(np.uint8) for i in range(N)]
        out = np.zeros(1 << cb, np.uint32)
        for i in range(N):
            n = np.zeros(1 << cb, np.uint8)
            for j in nb[i]:
                n += bits[j]
            new = np.where(bits[i] == 1, St[n], Bt[n])
            out |= new.astype(np.uint32) << np.uint32(i)
        F[lo:lo + (1 << cb)] = out
    return F


def step_state(nb, B, S, s):
    out = 0
    for i, v in enumerate(nb):
        n = sum((s >> j) & 1 for j in v)
        if (n in S) if (s >> i) & 1 else (n in B):
            out |= 1 << i
    return out


def death_times(F, living):
    """T[s] = first t >= 0 at which F^t(s) is not living; -1 if never."""
    T = np.where(living, -1, 0).astype(np.int32)
    unk = np.flatnonzero(T < 0)
    t = 0
    while len(unk):
        t += 1
        done = T[F[unk]] == t - 1
        if not done.any():
            break
        T[unk[done]] = t
        unk = unk[~done]
    return T


def cyclic(F):
    """States on cycles = the eventual image of F."""
    cyc = np.ones(len(F), bool)
    n = len(F)
    while True:
        img = np.zeros(len(F), bool)
        img[F[cyc]] = True
        img &= cyc
        m = int(img.sum())
        if m == n:
            return img
        cyc, n = img, m


def periods(F, cyc):
    """period -> number of cyclic states with that period."""
    idx = np.flatnonzero(cyc)
    per = np.zeros(len(idx), np.int64)
    cur = F[idx].copy()
    p = 1
    left = np.ones(len(idx), bool)
    while left.any():
        hit = left & (cur == idx)
        per[hit] = p
        left &= ~hit
        cur = F[cur]
        p += 1
    vals, cnt = np.unique(per, return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, cnt)}


def bit(states, i):
    return ((states >> np.uint32(i)) & np.uint32(1)).astype(bool)


def any_alive(nstates_bits, cells):
    """boolean array over all 2^N states: some cell of `cells` is alive."""
    s = np.arange(1 << nstates_bits, dtype=np.uint32)
    m = np.uint32(sum(1 << c for c in cells))
    return (s & m) != 0


def popcount_over(nstates_bits, cells):
    """uint8 array over all states: number of live cells among `cells`."""
    s = np.arange(1 << nstates_bits, dtype=np.uint32)
    out = np.zeros(len(s), np.uint8)
    for c in cells:
        out += ((s >> np.uint32(c)) & np.uint32(1)).astype(np.uint8)
    return out
