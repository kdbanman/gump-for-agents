#!/usr/bin/env python3
"""Scattering table of a wire's caps: for every cap state and every kind of arriving pulse, what the cap becomes and
what (if anything) it sends back; then a search for closed cycles of a pulse bouncing between two caps.

    python3 scatter_table.py W C [--survey FILE] [--max 4000] [--out FILE]

W: line of the survey file (a wire of the closed 3 x 3 tube with a reversing symmetry M found by
survey.reversing_symmetry; M may map phase 0 of the wire to phase 1).  Steps:
 1. pulse kinds: start from the survey's right-moving pulse cut into its elementary pulses (--pulses can name
    them), and close the set under "what caps send back" and under M.  A kind is the set of cells that differ from
    the bare wire at an even generation, moved so that its lowest unit is 0, with its direction.
 2. cap states: all caps inside the planes (caps.enumerate_caps, period 2), then every state a cap is left in
    after a hit, until nothing new appears.  A state is the live cells from the first unit that is not the bare
    wire, moved so that this unit is 0 (so a cap that has crept along the wire is the same state).
 3. table[state][kind] = (verdict, new state, kind sent back, creep), verdict in eats / changed / back / fire / other.
 4. two-ended search: right cap in state a, left cap the mirror image of state b, a pulse of kind p between them;
    the three evolve by the table.  Any (a, b, p) that returns to itself is a candidate oscillator; bounce.py-like
    direct simulation and then the oracle must confirm it.
"""
import argparse, json, sys, time
from collections import Counter
import numpy as np
import sg, plab, scat, caps, caps_any, survey

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)


class Table:
    def __init__(self, ob, C, lo=1, hi=5, L=260):
        self.ob = ob; self.wire = scat.Wire(ob, None); self.C = C; self.L = L
        sym = survey.reversing_symmetry([tuple(c) for c in ob['bg']], self.wire.P)
        assert sym, 'no reversing symmetry'
        (perm, sgn), t, self.mph = sym
        self.M = lambda c: tuple(sgn[k] * c[perm[k]] + t[k] for k in range(3))
        w = self.wire
        self.W = [frozenset(scat.tr(c, k) for c in w.bg[ph] for k in range(-L, 60)) for ph in range(w.P)]
        self.g = sg.Geom([], [(S1, lo, hi), (S2, lo, hi), (S3, -4 * L - 40, C + 80), (S4, -4 * L - 40, C + 80)], seeds=list(self.W[0]))
        self.kinds = {}        # name -> (direction, frozenset of cells at unit >= 0)
        self.states = {}       # canonical frozenset -> name
        self.table = {}

    # ---- pulse kinds
    def canon_pulse(self, cells):
        u = min(scat.unit(c) for c in cells)
        return frozenset(scat.tr(c, -u) for c in cells), u

    def kind_name(self, cells, direction):
        key, u = self.canon_pulse(cells)
        for n, (d, k) in self.kinds.items():
            if d == direction and k == key:
                return n, u
        n = 'pqrstuvwxyz'[len(self.kinds) // 2] + ('>' if direction > 0 else '<')
        self.kinds[n] = (direction, key)
        # its mirror image
        mirror = self.mirror_pulse(key, direction)
        n2 = n[0] + ('<' if direction > 0 else '>')
        self.kinds[n2] = (-direction, mirror)
        return n, u

    def mirror_pulse(self, key, direction):
        """The image under M of a pulse, brought back to an even generation."""
        Wl = frozenset(scat.tr(c, k) for c in self.wire.bg[0] for k in range(-40, 41))
        x = Wl ^ key
        z = Wl
        for _ in range(self.mph):                          # M maps phase mph -> phase 0
            x = sg.step_set(x); z = sg.step_set(z)
        mx = frozenset(self.M(c) for c in x); mz = frozenset(self.M(c) for c in z)
        d = frozenset(c for c in mx ^ mz if abs(scat.unit(c)) < 20)
        return self.canon_pulse(d)[0]

    def is_pulse(self, cells, direction):
        """Is this set of cells (differences at an even generation) a (2,1) pulse of the bare wire?"""
        cells, _ = self.canon_pulse(cells)
        Wl = frozenset(scat.tr(c, k) for c in self.wire.bg[0] for k in range(-40, 41))
        x = Wl ^ cells; z = Wl
        for _ in range(4):
            x = sg.step_set(x); z = sg.step_set(z)
        d = frozenset(c for c in x ^ z if abs(scat.unit(c)) < 25)
        return d == frozenset(scat.tr(c, 2 * direction) for c in cells)

    # ---- cap states
    def canon_state(self, live, upto):
        """live: cells at an even generation; the wire is bare below some unit.  Returns (key, first unit)."""
        w0 = self.wire.bg[0]
        by = {}
        for c in live:
            if scat.unit(c) >= upto:
                by.setdefault(scat.unit(c), set()).add(scat.tr(c, -scat.unit(c)))
        u = upto
        while by.get(u) == set(w0):
            u += 1
        key = frozenset(scat.tr(c, -u) for c in live if scat.unit(c) >= u)
        return key, u

    def state_name(self, key):
        if key not in self.states:
            self.states[key] = len(self.states)
        return self.states[key]

    def shoot(self, key, kind, KS=6, k_launch=-16, T=140):
        """Cap state `key` placed with its first unit at KS; a pulse of `kind` (right-moving) launched at unit
        k_launch.  Returns (verdict, new state key or None, kind sent back or None, creep in units)."""
        g = self.g; L = self.L
        cap = frozenset(scat.tr(c, KS) for c in key)
        base = frozenset(c for c in self.W[0] if scat.unit(c) < KS) | cap
        z = g.state(base)
        x = z.copy()
        for c in self.kinds[kind][1]:
            x[g.index[scat.tr(c, k_launch)]] ^= 1
        x = g.run(x, T, sparse=True); zT = g.run(z, T, sparse=True)
        umin = -L + T + 10
        d = [g.cells[i] for i in np.nonzero((x != zT)[:g.n])[0] if scat.unit(g.cells[i]) >= umin]
        if not d:
            return 'eats', key, None, 0
        us = sorted(set(scat.unit(c) for c in d))
        away = [c for c in d if scat.unit(c) < k_launch - 6]
        near = [c for c in d if scat.unit(c) >= k_launch - 6]
        nus = sorted(set(scat.unit(c) for c in near))
        if near and (nus[0] < k_launch or len(nus) > 14):
            return 'fire', None, None, 0
        x2 = g.run(x, 2, sparse=True)
        live = g.cells_of(x); live2 = g.cells_of(x2)
        if frozenset(c for c in live if scat.unit(c) >= k_launch - 4) != frozenset(c for c in live2 if scat.unit(c) >= k_launch - 4):
            return 'other', None, None, 0                 # not stationary near the cap (a clock, or still settling)
        nkey, u = self.canon_state(live, k_launch - 4)
        out = None
        if away:
            if not self.is_pulse(away, -1):
                return 'other', None, None, 0
            out, _ = self.kind_name(away, -1)
        return ('back' if out else 'changed'), nkey, out, u - KS

    def build(self, caplist, pulses, maxstates=20000, verbose=True):
        for p in pulses:
            self.kind_name(frozenset(p), 1)
        for cap in caplist:
            key, u = self.canon_state(frozenset(scat.tr(c, k) for c in self.wire.bg[0] for k in range(0, 6)) | frozenset(cap), 0)
            self.state_name(key)
        while True:
            missing = [(key, kind) for key in list(self.states) for kind in self.kinds if self.kinds[kind][0] > 0 and (key, kind) not in self.table]
            if not missing or len(self.states) >= maxstates:
                break
            for key, kind in missing:
                if key and max(scat.unit(c) for c in key) > 14:      # a cap that keeps growing: not followed further
                    self.table[(key, kind)] = ('big', None, None, 0); continue
                v, nkey, out, creep = self.shoot(key, kind)
                self.table[(key, kind)] = (v, nkey, out, creep)
                if nkey is not None:
                    self.state_name(nkey)
        return self

    def cycles(self, maxlen=64):
        """All (a, b, p) that return to themselves under alternate reflections (right cap first)."""
        rk = [k for k in self.kinds if self.kinds[k][0] > 0]
        found = []
        okstates = [s for s in self.states if any(self.table.get((s, k), ('x',))[0] == 'back' for k in rk)]
        for a in okstates:
            for b in okstates:
                for p in rk:
                    cur = (a, b, p, 0, 0); seen = {}; path = []
                    for step in range(maxlen):
                        A, Bk, P, ca, cb = cur
                        if (A, Bk, P) in seen:
                            if (A, Bk, P) == (a, b, p):
                                found.append(dict(a=self.states[a], b=self.states[b], p=p, length=step, creep=(ca, cb), path=path))
                            break
                        seen[(A, Bk, P)] = step
                        v, na, out, creep = self.table.get((A, P), ('x', None, None, 0))
                        if v != 'back':
                            break
                        q = out[0] + '>'                 # the pulse going left, seen in the mirror, is this right-mover
                        v2, nb, out2, creep2 = self.table.get((Bk, q), ('x', None, None, 0))
                        if v2 != 'back':
                            break
                        path.append((self.states[A], P, self.states[na], out, self.states[Bk], q, self.states[nb], out2))
                        cur = (na, nb, out2[0] + '>', ca + creep, cb + creep2)
        return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('W', type=int); ap.add_argument('C', type=int)
    ap.add_argument('--survey', default='../scratch/signals/survey.jsonl'); ap.add_argument('--max', type=int, default=4000)
    ap.add_argument('--pulses', help='python list of lists of indices into the survey defect, e.g. "[[0,2],[1,3]]"')
    ap.add_argument('--out')
    a = ap.parse_args()
    ob = [json.loads(l) for l in open(a.survey)][a.W]
    T = Table(ob, a.C)
    full = [tuple(c) for c in ob['defect']]
    pulses = [[full[i] for i in sel] for sel in eval(a.pulses)] if a.pulses else [full]
    for p in pulses:
        assert T.is_pulse(p, 1), ('not a pulse', p)
    t0 = time.time()
    cs, status, nfree = caps.enumerate_caps(T.wire, a.C, 1, 5, 6, T.wire.P, a.max, 1200, verbose=False)
    T.build(cs, pulses)
    res = Counter(v[0] for v in T.table.values())
    print(f'wire {a.W}, C={a.C}: {len(cs)} caps ({status}), {len(T.states)} cap states after closure, kinds {sorted(T.kinds)}; table: {dict(res)}; {time.time() - t0:.0f}s', flush=True)
    for n, (d, k) in sorted(T.kinds.items()):
        print('   kind', n, sorted(k))
    back = Counter((kind, v[2], v[3]) for (key, kind), v in T.table.items() if v[0] == 'back')
    print('   reflections (kind in, kind out, creep): ', dict(back))
    same = [(T.states[key], kind, v[2]) for (key, kind), v in T.table.items() if v[0] == 'back' and v[1] == key and v[3] == 0]
    print('   reflections that leave the cap exactly as it was:', same[:20], len(same))
    cyc = T.cycles()
    print(f'   closed cycles (right state, left state, pulse): {len(cyc)}')
    for c in cyc[:10]:
        print('     ', {k: v for k, v in c.items() if k != 'path'}, c['path'][:4])
    if a.out:
        inv = {v: sorted(k) for k, v in T.states.items()}
        json.dump(dict(wire=a.W, C=a.C, kinds={n: [d, sorted(k)] for n, (d, k) in T.kinds.items()}, states=inv,
                       table=[[T.states[key], kind, v[0], (T.states[v[1]] if v[1] is not None else None), v[2], v[3]] for (key, kind), v in T.table.items()],
                       cycles=cyc), open(a.out, 'w'))


if __name__ == '__main__':
    main()
