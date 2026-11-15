#!/usr/bin/env python3
"""Tests of the cycle guard (research/gpu/guard.py) on this card.

  python -u research/gpu-local/guard_test.py planted   # exact detection generations on the 373 engine-run soups
  python -u research/gpu-local/guard_test.py identical # guard on vs off on a face-law run: lives equal lane for lane
  python -u research/gpu-local/guard_test.py all

planted: the R = 9 soups of `check.py periodic-cases` (gump ensemble ran each to its end and reported cycle_start c and
period P; still lives have P = 1, extinct ones are the empty state from c on). The state at generation s equals the
state at b > s iff s >= c and P | (b - s) (two equal states mean the cycle has begun by s). So the guard's detection
boundary is a deterministic function of (c, P, the launch boundaries, the snapshot thresholds), computed here in plain
Python by `predict` and compared exactly with the GPU run:
  (a) freeze off (the kernel never ends a life): every soup must be recognised by the guard exactly at the predicted
      boundary, for several launch lengths and first thresholds, including launch lengths coprime to every period;
  (b) freeze on with pw = 32, as a production run would be: the two soups with P > 32 (48 and 66) must end as kind 5
      exactly at the predicted boundary; every other soup must end by the kernel (kind 2 or 3, at the generation
      check_periodic expects) and never as kind 5;
  (c) negative controls: test (a) run with three deliberately broken guards must fail: snapshot taken before the
      comparison (a replica matches itself), the comparison made against the neighbouring column's snapshots, and
      thresholds that never double (a snapshot at every boundary, so only periods dividing K are found).
identical: facelaw.run with a fixed launch length and generation cap, guard off and on, same seed: lives (age, kind,
birth, replica) must be equal lane for lane, except lanes in which the guard recognised a cycle, which must agree up to
that life and contain a kind-5 life there.
"""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
import gsim, guard, check, facelaw  # noqa: E402
from gsim import fl  # noqa: E402

PERIODIC = os.path.join(ROOT, 'research', 'scratch', 'gpu', 'periodic_cases.npz')


def predict(c, P, K, first, Gmax):
    """the guard's first detection boundary for a replica born at 0 that enters a cycle of period P at generation c,
    with launches of length K (a list cycles), thresholds first * 2^j. None if not within Gmax."""
    Ks = K if isinstance(K, (list, tuple)) else [K]
    b, i, nxt, snap = 0, 0, first, None
    while b < Gmax:
        b += Ks[i % len(Ks)]; i += 1
        if snap is not None and snap >= c and (b - snap) % P == 0:
            return b
        if b >= nxt:
            snap = b
            while nxt <= b:
                nxt *= 2
    return None


def load_cases():
    d = np.load(PERIODIC)
    meta = d['meta'].astype(np.int64)
    P = np.where(meta[:, 2] <= 0, 1, meta[:, 2])          # still and extinct: period 1
    return d['bits'], meta, P, meta[:, 3]


class SnapFirst(guard.CycleGuard):          # broken: takes the due snapshots before comparing
    def boundary(self, G, birth):
        age = G - np.asarray(birth, np.int64)
        live = ~self._words_to_bits(self.s._np(self.s.frz))
        self._take(live & (age >= self.next_age), age)
        hit = self._compare(live)
        reps = np.nonzero(hit)[0]
        return reps, self.snap_age[reps].copy()


class OtherColumn(guard.CycleGuard):        # broken: compares with the neighbouring column's snapshots
    def _compare(self, live):
        s, xp = self.s, self.xp
        saved = self.snap
        self.snap = xp.roll(self._shape(saved), 1, axis=0 if s.kernel == 'shared' else 1).reshape(-1)
        try:
            return super()._compare(live)
        finally:
            self.snap = saved


class NoDoubling(guard.CycleGuard):         # broken: a fresh snapshot at every boundary
    def _take(self, due, age):
        super()._take(due, age)
        self.next_age[:] = self.first


def planted_run(K, first, freeze, pw, Gmax, guard_cls=guard.CycleGuard, **kw):
    bits0, meta, P, c = load_cases()
    v = fl.Vessel(fl.octa_hull(9), 'c', False)
    s = gsim.Sim(v, 0, 'gpu', faces=False, pw=pw, **kw)
    n = len(meta)
    lanes = np.arange(s.R) % n                              # every lane holds one of the cases
    s.set_all(bits0[lanes])
    gd = guard_cls(s, first=first)
    birth = np.zeros(s.R, np.int64)
    ev5, evk = {}, {}
    Ks = K if isinstance(K, (list, tuple)) else [K]
    G, i = 0, 0
    while G < Gmax:
        k = Ks[i % len(Ks)]; i += 1
        reps, tt, kk = s.step(k, freeze=freeze)
        for r, t, q in zip(reps, tt, kk):
            evk.setdefault(int(r), (G + int(t), int(q)))
        G += k
        g_reps, _ = gd.boundary(G, birth)
        for r in g_reps:
            ev5.setdefault(int(r), G)
    return s, lanes, meta, P, c, ev5, evk


def test_planted_nofreeze(K, first, Gmax=1 << 19, guard_cls=guard.CycleGuard, quiet=False):
    # Gmax: detection takes up to ~lcm(launch grid, P) after a snapshot on the cycle, and a window that is too short
    # for it waits for the next (doubled) snapshot; 1 << 17 left 4-25 lanes unfound (as predicted) for K = 997 or
    # mixed launches, 1 << 19 finds all.
    s, lanes, meta, P, c, ev5, _ = planted_run(K, first, freeze=False, pw=128, Gmax=Gmax, guard_cls=guard_cls)
    bad = []
    for r in range(s.R):
        j = lanes[r]
        want = predict(int(c[j]), int(P[j]), K, first, Gmax)
        if want is None or ev5.get(r) != want:          # every planted cycle must be found within Gmax
            bad.append((r, int(c[j]), int(P[j]), want, ev5.get(r)))
    if not quiet:
        print(f'planted, freeze off, K={K}, first={first}: {s.R} lanes ({len(meta)} soups), periods 1-{P.max()}: '
              f'{"all at the predicted boundary" if not bad else f"{len(bad)} WRONG: {bad[:5]}"}', flush=True)
    return not bad, len(bad)


def test_planted_freeze(K=1000, first=16, pw=32, Gmax=1 << 17):
    s, lanes, meta, P, c, ev5, evk = planted_run(K, first, freeze=True, pw=pw, Gmax=Gmax)
    bad, n5 = [], 0
    for r in range(s.R):
        j = lanes[r]
        p, cc = int(P[j]), int(c[j])
        if p > pw:
            want5 = predict(cc, p, K, first, Gmax); n5 += 1
            if ev5.get(r) != want5 or r in evk:
                bad.append(('long', r, cc, p, want5, ev5.get(r), evk.get(r)))
        else:
            wantk = (cc + 2, 2) if p <= 2 else (-(-cc // K) * K + p, 3)
            if evk.get(r) != wantk or r in ev5:
                bad.append(('short', r, cc, p, wantk, evk.get(r), ev5.get(r)))
    print(f'planted, freeze on, pw={pw}, K={K}, first={first}: {n5} lanes with P > pw end as kind 5 at the predicted '
          f'boundary, {s.R - n5} others end by the kernel as check_periodic expects, none as kind 5: '
          f'{"yes" if not bad else f"NO, {len(bad)} wrong: {bad[:5]}"}', flush=True)
    return not bad


def test_negative(K=997, first=16):
    ok = True
    for cls in (SnapFirst, OtherColumn, NoDoubling):
        passed, nbad = test_planted_nofreeze(K, first, guard_cls=cls, quiet=True)
        print(f'negative control {cls.__name__}: {nbad} lanes wrong -> {"caught" if not passed else "NOT CAUGHT"}', flush=True)
        ok &= not passed
    return ok


def test_identical(R=15, gens=1 << 20, K=4096, seed=990001, first=16, **cfg):
    a = facelaw.run(R, 1e9, seed, max_gens=gens, launch_gens=K, keep_reps=True, raw_cap=10 ** 9, log=lambda x: None, **cfg)
    b = facelaw.run(R, 1e9, seed, max_gens=gens, launch_gens=K, keep_reps=True, raw_cap=10 ** 9, log=lambda x: None,
                    guard=first, **cfg)
    la, lb = [np.vstack([facelaw.unpack(x['raw']), facelaw.unpack(x['raw_reps'])]) for x in (a, b)]
    n5 = b['guard']['recognised']
    # The driver draws each reseed from (seed, a counter that advances at every boundary where some life ended). The
    # two runs' counters stay equal only while the same boundaries carry reseeds; Gs = the first boundary where they
    # do not (it exists only when the guard ended lives at a boundary where the kernel ended none). Lives born
    # before Gs are comparable; later ones are different soups by construction.
    SA, SB = np.unique(la[2]), np.unique(lb[2])
    m = min(len(SA), len(SB))
    d = np.nonzero(SA[:m] != SB[:m])[0]
    Gs = int(min(SA[d[0]], SB[d[0]])) if len(d) else (int(max(SA[m - 1], SB[m - 1])) + 1 if len(SA) != len(SB) else None)
    bad = cmp5 = 0
    for r in range(a['replicas']):
        A_, B_ = la[:3, la[3] == r], lb[:3, lb[3] == r]
        if Gs is not None:
            A_, B_ = A_[:, A_[2] < Gs], B_[:, B_[2] < Gs]
        k5 = np.nonzero(B_[1] == guard.KIND)[0]
        if len(k5) == 0:
            bad += not np.array_equal(A_, B_)
        else:        # equal up to the first kind-5 life; guard off, that life (same birth) is still running at that age
            f = k5[0]; cmp5 += 1
            bad += not (np.array_equal(A_[:, :f], B_[:, :f]) and A_.shape[1] > f and A_[2, f] == B_[2, f]
                        and A_[0, f] >= B_[0, f])
    ok = bad == 0
    print(f'guard on vs off, R={R} asym {cfg or ""}, {a["replicas"]} replicas, {gens} gens, K={K}: {la.shape[1]} vs {lb.shape[1]} '
          f'lives, {n5} recognised by the guard ({b["guard"]["compares"]} comparisons), lives compared: '
          f'{"all" if Gs is None else f"born before generation {Gs}"}; {cmp5} lanes compared up to a kind-5 life: '
          f'{"equal lane for lane" if ok else f"{bad} lanes DIFFER"}', flush=True)
    return ok


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    ok = True
    t = time.time()
    if what in ('planted', 'all'):
        for K in (1024, 1000, 997, [997, 1024, 4096]):
            for first in (16, 1000):
                ok &= test_planted_nofreeze(K, first)[0]
        ok &= test_planted_freeze()
        ok &= test_planted_freeze(K=4096, first=16, pw=32)
        ok &= test_negative()
    if what in ('identical', 'all'):
        ok &= test_identical()                                   # long lives: few reseeds
        ok &= test_identical(R=9, gens=1 << 21, K=1024, seed=990002)            # short lives: many reseeds
        ok &= test_identical(R=9, gens=1 << 21, K=1024, seed=990003, pw=32)     # natural cycles of period > 32 -> kind 5
        ok &= test_identical(R=11, gens=1 << 21, K=997, seed=990004, pw=16, first=1000)
        # pw = 1: the kernel recognises only periods 1-2, so every natural cycle of period >= 3 is the guard's: the
        # kind-5 path of the driver (recognise, reseed, reset) is exercised and the lanes must agree up to it
        ok &= test_identical(R=9, gens=1 << 21, K=1024, seed=990005, pw=1)
        # faces off as well: a life ends only by settling, so the lanes fill with natural cycles (about 6% of R = 9
        # soups end in a period > 2). Guard off, those hold their lanes to the end; guard on, they end as kind 5.
        ok &= test_identical(R=9, gens=1 << 19, K=1024, seed=990006, pw=1, faces=False)
    print(f'{"ALL OK" if ok else "FAILURES"} ({time.time() - t:.0f} s)')
    sys.exit(0 if ok else 1)
