#!/usr/bin/env python3
"""push 8b: the crossing as a machine.  For every non-parallel placement of survey.py in which the reader stands beside
wire B AND beside wire B' (transparent, or settled into a standing junction), send words of pulses from both ends of the
reader and follow the states of the crossing.

    python3 junc.py READER [--depth 3] [--part i/m] [--out FILE]

Letters: L0, L2 (the right-going pulse put on 9 units before the crossing, 0 or 2 generations after a generation
divisible by 4), R0, R2 (the left-going pulse 9 units beyond the crossing).  After each letter the object is run 240
generations (both caps have swallowed what reached them) and the result is one of
  base       the whole object is exactly as before the first letter
  a mark     periodic (period dividing 4), no cell of the store's tube differs from the base, and every differing cell
             lies within 6 reader units of the crossing: a new state of the crossing; letters go on from it
  dead       anything else (the store changed, the reader converted or burnt, a cap changed, not periodic)
The *output* of a letter is the difference from the pulse-free run 32 generations after the launch, outside 3 units
of the crossing, in the reader's frame.
A word is a *read* if for store B and for store B' it ends in base and the two output sequences differ.  Words are
extended (to --depth letters) only while at least one of the two stores is in a mark and none is dead.
Output: JSON lines, one per placement that has a mark or a read; summary printed."""
import argparse, json, os, time
import lab, wires, survey
from lab import tr, unit
from survey import inv
from survey2 import in_tube

LEFT = {'B': [(12, 2, -9), (13, 0, -8)], 'C': lab.PULSE_C_LEFT, 'Cw': None}
U0 = 9
TS = 240


class Junction:
    def __init__(self, L, gi_, phi, t, kind):
        self.L = L; self.g = lab.SYMS[gi_]; self.gi = inv(self.g); self.phi = phi; self.t = t; self.kind = kind
        HRg = [lab.app(self.g, c) for c in L.FRh]
        self.us, self.ur = survey.crossing(self.g, t, HRg, L.HS)
        S0 = L.stores[kind]; R0 = L.reader(self.g, phi, t)
        U = lab.union(S0, R0)
        self.ok = True
        J = lab.run(U, 200)
        if not lab.same(lab.run(J, 4), J):
            self.ok = False; return
        D = lab.up(lab.xor(J, U))
        if any(abs(self.runit(c) - self.ur) > 6 for c in D):
            self.ok = False; return                    # not local
        self.jtube = sum(1 for c in D if in_tube(c))   # cells of the junction inside the store's tube (0: the store
        self.jsize = len(D)                            # stands exactly as it does alone)
        self.base = J
        self.memo = {}

    def runit(self, c):
        return unit(lab.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2])))

    def place(self, cells):
        return lab.pk([lab.app(self.g, c, self.t) for c in cells])

    def letter(self, state, a):
        """state: key array at a generation divisible by 4 (global).  Returns (output signature, new state or
        'dead:why')."""
        key = (state.tobytes(), a)
        if key in self.memo:
            return self.memo[key]
        side, delay = a[0], int(a[1])
        Y = lab.run(state, self.phi + delay)           # the reader's own generation is then even
        if side == 'L':
            pc = wires.pulse(self.L.pulse, self.ur - U0)
        else:
            pc = wires.pulse(LEFT[self.L.name], self.ur + U0)
        X = lab.xor(Y, self.place(pc))
        Xc = lab.run(X, 32); Yc = lab.run(Y, 32)
        D = lab.up(lab.xor(Xc, Yc))
        out = tuple(sorted(tr(lab.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2])), -self.ur)
                           for c in D if abs(self.runit(c) - self.ur) > 3))
        near = sum(1 for c in D if abs(self.runit(c) - self.ur) <= 3)
        n2 = TS - 32 - self.phi - delay
        Xf = lab.run(Xc, n2)
        if lab.same(Xf, self.base):
            res = (out, 'base')
        elif not lab.same(lab.run(Xf, 4), Xf):
            res = (out, 'dead:not periodic')
        else:
            D = lab.up(lab.xor(Xf, self.base))
            if any(in_tube(c) for c in D):
                res = (out, 'dead:store')
            elif any(abs(self.runit(c) - self.ur) > 6 for c in D):
                res = (out, 'dead:reader')
            else:
                res = (out, Xf)
        self.memo[key] = res
        return res


def explore(L, gi_, phi, t, depth):
    js = {k: Junction(L, gi_, phi, t, k) for k in ('B', 'Bp')}
    if not all(j.ok for j in js.values()):
        return None
    letters = ['L0', 'R0']
    per4 = any(not lab.same(lab.run(j.base, 2), j.base) for j in js.values())
    found = dict(g=gi_, phi=phi, t=list(t), reads=[], marks=[], per4=per4, jtube={k: js[k].jtube for k in js}, jsize={k: js[k].jsize for k in js})
    frontier = [((), {k: js[k].base for k in js}, {k: () for k in js})]
    for d in range(depth):
        nxt = []
        for word, states, outs in frontier:
            p4 = per4 or any(not lab.same(lab.run(states[k], 2), states[k]) for k in states)
            for a in (['L0', 'L2', 'R0', 'R2'] if p4 else letters):
                st2 = {}; o2 = {}; dead = False
                for k in js:
                    out, s = js[k].letter(states[k], a)
                    o2[k] = outs[k] + (out,)
                    st2[k] = s
                    if isinstance(s, str) and s.startswith('dead'):
                        dead = True
                w2 = word + (a,)
                at_base = {k: isinstance(st2[k], str) and st2[k] == 'base' for k in js}
                if dead:
                    continue
                if all(at_base.values()):
                    if o2['B'] != o2['Bp']:
                        found['reads'].append(dict(word=list(w2), out={k: [[list(c) for c in o] for o in o2[k]] for k in js}))
                    continue
                found['marks'].append(dict(word=list(w2), marked=[k for k in js if not at_base[k]],
                                           size={k: (0 if at_base[k] else int(len(lab.xor(st2[k], js[k].base)))) for k in js}))
                nxt.append((w2, {k: (js[k].base if at_base[k] else st2[k]) for k in js}, o2))
        frontier = nxt
        if not frontier:
            break
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--depth', type=int, default=3); ap.add_argument('--part', default='0/1'); ap.add_argument('--out')
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    out = a.out or os.path.join(lab.SCR, f'junc_{a.reader}_{pi}of{pm}.jsonl')
    L = survey.Lab(a.reader)
    t0 = time.time(); n = nok = nmark = nread = 0
    with open(out, 'w') as f:
        for j, (gi_, phi, t) in enumerate(survey.placements(a.reader)):
            if j % pm != pi:
                continue
            n += 1
            r = explore(L, gi_, phi, t, a.depth)
            if r is None:
                continue
            nok += 1
            if r['marks'] or r['reads']:
                nmark += bool(r['marks']); nread += bool(r['reads'])
                f.write(json.dumps(r) + '\n'); f.flush()
                if r['reads']:
                    print('READ', gi_, phi, t, [x['word'] for x in r['reads']], flush=True)
    print(f'{n} placements, {nok} standing beside both B and B\', {nmark} with a mark, {nread} with a read; {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
