#!/usr/bin/env python3
"""wall9 (push 9): each standing placement of beside9.py put near the left wall of a stretch, and sent a pulse.

    python3 wall9.py F.jsonl [--k 3] [--part i/n] --out G.jsonl

Ring of 36 units of wire B with the stretch d^k f on units 18..18+k (wall: unit 17 | unit 18).  The object is placed
with its highest unit at 17 + e for e = -3..3 (e <= 0: wholly before the wall; e > 0: reaching beside the stretch).
Three scenarios for each e: 'rest' (nothing sent), 'A' and 'B' (a right-going pulse born at unit 18 - 11, 18 - 12:
the two parities), each read 76 generations after the start.

Exact shortcut (the inert test): if at every generation of the scenario run WITHOUT the object every cell of the
object's closed neighbourhood gets the same next state from the sum of the two neighbour counts as from the two
separately, the run with the object is the union of the two runs, and nothing is simulated.  Otherwise the scenario
is stepped (lab8) and read: the ring's letters (3 x 3 tube) and whether the cells outside the tube are those of the
undisturbed object.  Classes:
  inert      as above (the stretch stands / the pulse is absorbed as if the object were not there)
  absorbed, unchanged   the same end state reached with an interaction on the way
  RELEASE nL mR   no unit of the ring is d, f or unreadable, the units 12..24 are plain, the object is as it was,
             and the ring holds n units b (left-going pulses) and m units 6 (right-going)
  ERASED     the same with no pulse at all
  other      anything else (the letters are kept)
One JSON line per (placement, e) with a scenario that is not inert/absorbed/unchanged.
"""
import sys, os, json, argparse, math, time
import numpy as np
import lab9 as Z
from lab9 import Lab, tr, unit, X, W

R = 36; W0 = 18; T = 76
BOX = (-18, 18, -16, 22)      # ylo, yhi, wlo, whi of the reference box


def rule(n, x):
    return ((n == 4) | (n == 5) | ((n == 3) & (x == 1))).astype(np.uint8)


class Ref:
    """the scenario runs without an object: X[s][t] the state, N[s][t] the neighbour counts (flat arrays)"""

    def __init__(self, k):
        self.k = k
        self.L = L = Lab(0, R, *BOX, ring=True)
        self.word = '7' * W0 + 'd' * k + 'f' + '7' * (R - W0 - k - 1)
        base = L.arr(X.hexword(self.word, 0))
        self.X = {}; self.N = {}
        for s, fl, n in (('rest', [], 2), ('A', X.pulseR(W0 - 11), T), ('B', X.pulseR(W0 - 12), T)):
            a = base.copy(); L.flip(a, fl)
            xs = []; ns = []
            for t in range(n + 1):
                xs.append(a.ravel().copy()); ns.append(self.counts(L.cells(a)).ravel())
                L.run(a, 1)
            self.X[s] = np.array(xs); self.N[s] = np.array(ns)
        assert np.array_equal(self.X['rest'][0], self.X['rest'][2])

    def counts(self, cells):
        n = np.zeros(self.L.shape, np.uint8)
        for c in cells:
            for q in Z.nbrs(c):
                try:
                    n[self.L.idx(q)] += 1
                except ValueError:
                    pass
        return n

    def flat(self, cells):
        sh = self.L.shape
        out = []
        for c in cells:
            i, j, k = self.L.idx(c)
            out.append((i * sh[1] + j) * sh[2] + k)
        return np.array(out)


class Obj:
    """an object's orbit (list of cell sets), its closed neighbourhood H and, per phase, state and count on H"""

    def __init__(self, orb):
        self.P = len(orb)
        self.orb = orb
        un = frozenset().union(*orb)
        self.H = sorted(Z.halo(un))
        self.x = np.array([[1 if h in o else 0 for h in self.H] for o in orb], np.uint8)
        self.n = np.array([[sum(1 for q in Z.nbrs(h) if q in o) for h in self.H] for o in orb], np.uint8)
        self.umax = max(unit(c) for c in un)

    def inert(self, ref, s, m):
        """is the object, moved m units, inert in scenario s?"""
        idx = ref.flat([tr(h, m) for h in self.H])
        XW = ref.X[s][:, idx]; NW = ref.N[s][:, idx]
        n = XW.shape[0] - 1
        ph = np.arange(n + 1) % self.P
        xs = self.x[ph]; ns = self.n[ph]
        if (XW & xs).any():
            return False
        nxt = rule(NW[:-1] + ns[:-1], XW[:-1] | xs[:-1])
        return bool(np.array_equal(nxt, XW[1:] | xs[1:]))


def classify(L, a, ref_out, k, grown):
    s = Z.hexring(L, a)
    same = Z.outside(L, a) == ref_out
    if same and s == '7' * (W0 - grown) + 'd' * (k + grown) + 'f' + '7' * (R - W0 - k - 1):
        return 'absorbed' if grown else 'unchanged'
    if same and not (set(s) - set('7b6f')) and s[W0 - 6:W0 + 7] == '7' * 13:
        nb = s.count('b'); n6 = s.count('6')
        if nb + n6:
            return f'RELEASE {nb}L {n6}R  {X.hexrle(Z.canon_ring(s))}'
        return 'ERASED'
    return f'other {X.hexrle(s)} obj={"same" if same else "changed"}'


def simulate(ref, orb, m, s):
    """the scenario with the object moved m units, stepped; returns the class"""
    k = ref.k
    S0 = [tr(c, m) for c in orb[0]]
    un = [tr(c, m) for o in orb for c in o]
    L = Z.box_for(un, R)
    a = L.arr(X.hexword(ref.word, 0))
    L.flip(a, S0)
    if s != 'rest':
        L.flip(a, X.pulseR(W0 - 11 if s == 'A' else W0 - 12))
    L.run(a, T)
    free = L.arr([tr(c, m) for c in orb[T % len(orb)]])
    res = classify(L, a, Z.outside(L, free), k, 0 if s == 'rest' else 1)
    if L.touch:
        res += ' touch'
    return res


def wall_runs(ref, orb, es=range(-3, 4)):
    ob = Obj(orb)
    out = []
    for e in es:
        m = W0 - 1 + e - ob.umax
        res = {}
        try:
            for s in ('rest', 'A', 'B'):
                if s != 'rest' and res['rest'] not in ('inert', 'unchanged'):
                    continue
                res[s] = 'inert' if ob.inert(ref, s, m) else simulate(ref, orb, m, s)
        except ValueError:
            res = {'rest': 'outside box'}
        out.append((e, res))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('--k', type=int, default=3)
    ap.add_argument('--part', default='0/1'); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    i, n = map(int, a.part.split('/'))
    rows = [json.loads(l) for l in open(a.src)][i::n]
    ref = Ref(a.k)
    t0 = time.time(); nrel = 0; nsim = 0
    quiet = ('inert', 'absorbed', 'unchanged')
    with open(a.out, 'w') as f:
        for j, r in enumerate(rows):
            P = r['P']
            orb = Z.orbit([tuple(c) for c in r['cells']], P)
            for e, res in wall_runs(ref, orb):
                if all(v in quiet for v in res.values()) or res.get('rest') == 'outside box':
                    continue
                rec = dict(id=r['id'], P=P, gi=r['gi'], ph=r['ph'], t=r['t'], cells=r['cells'], e=e, res=res, R=r['R'], L=r['L'])
                f.write(json.dumps(rec) + '\n')
                if any(x.startswith('RELEASE') for x in res.values()):
                    nrel += 1
                    print(f"  {r['id']} gi={r['gi']} ph={r['ph']} t={r['t']} e={e}: {res}   | plain wire: R {r['R']}, L {r['L']}", flush=True)
            if j % 500 == 0:
                f.flush()
                print(f'[{j}/{len(rows)} placements, {nrel} with a release, {time.time() - t0:.0f} s]', flush=True)
    print(f'done: {len(rows)} placements, {nrel} (placement, e) with a release, {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()
