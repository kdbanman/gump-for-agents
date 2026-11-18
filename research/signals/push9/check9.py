#!/usr/bin/env python3
"""check9 (push 9): every stepper and shortcut used in this push against reference/oracle.py, cell for cell.

    python3 check9.py [--only A,B,C,D,E]

The oracle side is always oracle.step on a cubic torus (oracle.masks(H)); the other side's live cells are reduced
mod H (which must be injective) and the two sets of live cells are compared at EVERY generation.
A  lab8 (push 8's dense stepper, dead outside its box), as cell9.py uses it: every run of objects/trigger9.json
   (capped cell + stretches + a six-cell still life + pulses and blocks), generations 0..G, torus H of the run.
B  lab8's ring mode with an object beside the ring, as beside9.py, wall9.py, ghost9.py and the laws use it; ring of
   60 units = torus H = 120, 200 generations each:
     B1 stretch d^3 f + the still life at the trigger place + a right-going pulse (the release);
     B2 plain ring + the same still life + a right-going pulse (the hazard: the wire burns);
     B3, B4 the first standing placement of the catalogue's P4.10a and P3.11a that does not pass a right-going pulse.
C  lab9.c's bias stepper (ghost9.py, ghostpairs9.py): a ring of 36 units with d^3 f, one cell held live and a pulse,
   against the oracle with that cell forced live after every step (H = 72, 120 generations); two held cells.
D  push 8b's sparse stepper (lab.run), as cross9.py, xlab9.py and call9.py use it: every run of objects/call9.json
   (store wires + call lines + calls), generations 0..G.
E  wall9.py's inert shortcut: for every placement of the catalogue's still lifes of at most 6 cells that stands beside
   plain wire, and e = -3..3: where the shortcut says 'inert' for the pulse scenario A, the scenario is stepped
   (lab8) and must equal the union of the two separate runs.
Prints PASS/FAIL per part and ALL PASS.
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle           # noqa: E402
import lab9 as Z        # noqa: E402
from lab9 import tr, X  # noqa: E402


class Tor:
    def __init__(self, H):
        self.H = H; self.m = oracle.masks(H)

    def ix(self, c):
        return (c[0] % self.H, c[1] % self.H, c[2] % self.H)

    def arr(self, cells):
        h = np.zeros((self.H,) * 3, np.int8)
        for c in cells:
            i = self.ix(c); assert self.m[0][i] or self.m[1][i] or self.m[2][i], c
            assert h[i] == 0
            h[i] = 1
        return h

    def step(self, h):
        return oracle.step(h, self.m)

    def same(self, h, cells):
        k = frozenset(self.ix(c) for c in cells)
        return len(k) == len(cells) and k == frozenset(zip(*[v.tolist() for v in np.nonzero(h)]))


def part_A():
    import cell9
    d = json.load(open(os.path.join(HERE, 'objects', 'trigger9.json')))
    ok = True; n = 0
    for run in d['runs']:
        Lb = cell9.lab_for(run['N']); T = Tor(run['H'])
        s = cell9.state(run['start'], run['extra'])
        a = Lb.arr(s); h = T.arr(s)
        ops = {g: [tuple(c) for c in cells] for g, cells in run['ops']}
        G = max(g for g, _ in run['checks'])
        for g in range(G + 1):
            if not T.same(h, Lb.cells(a)):
                ok = False; print(f"  A {run['name']}: differ at generation {g}"); break
            n += 1
            if g in ops:
                Lb.flip(a, ops[g])
                for c in ops[g]:
                    h[T.ix(c)] ^= 1
            Lb.run(a, 1); h = T.step(h)
        ok &= not Lb.touch
    return ok, f'lab8 = oracle on the {len(d["runs"])} runs of trigger9.json, {n} generations compared'


def ring_case(word, extra, flips, gens, R):
    """lab8's ring of R units against the oracle on the torus 2R; extra = list of cell sets, one per phase"""
    L = Z.box_for([c for o in extra for c in o], R); T = Tor(2 * R)
    s = set(X.hexword(word, 0)) | set(extra[0])
    a = L.arr(s); L.flip(a, flips)
    h = T.arr(s)
    for c in flips:
        h[T.ix(c)] ^= 1
    for g in range(gens + 1):
        if not T.same(h, L.cells(a)):
            return False, g
        L.run(a, 1); h = T.step(h)
    return (not L.touch), gens


def part_B():
    import cell9, beside9
    R = 60; ok = True; msg = []
    w = '7' * 40 + 'ddd' + 'f' + '7' * 16
    trig = [tr(c, 40) for c in cell9.TRIG]
    for name, word, extra, fl in (('B1', w, [trig], X.pulseR(29)), ('B2', '7' * R, [trig], X.pulseR(29))):
        good, g = ring_case(word, extra, fl, 200, R)
        ok &= good; msg.append(f'{name} {"equal" if good else "DIFFER"} to generation {g}')
    cat = {o['id']: o for o in Z.catalogue()}
    for name, oid in (('B3', 'P4.10a'), ('B4', 'P3.11a')):
        o = cat[oid]; P = o['period']; orb = Z.orbit([tuple(c) for c in o['cells']], P)
        for gi, ph, t, cells in Z.placements(orb):
            if beside9.stands(cells, P) and beside9.pulse_lap(cells, P, 'R') != 'pass':
                break
        else:
            ok = False; msg.append(f'{name} no placement'); continue
        m = 30 - min(c[0] // 2 for c in cells)
        full = Z.orbit([tr(c, m) for c in cells], P)
        good, g = ring_case('7' * R, full, X.pulseR(8), 200, R)
        ok &= good; msg.append(f'{name} ({oid} gi={gi} ph={ph} t={list(t)}) {"equal" if good else "DIFFER"} to generation {g}')
    return ok, "lab8's ring mode = oracle: " + '; '.join(msg)


def part_C():
    R = 36; W0 = 18; ok = True; n = 0
    word = '7' * W0 + 'dddf' + '7' * (R - W0 - 4)
    for ghost in ((0, 1, 8), (-2, 1, 10), (0, -3, 4)):
        gc = tr(ghost, W0)
        L = Z.Lab(0, R, -18, 18, -16, 22, ring=True); T = Tor(2 * R)
        s = set(X.hexword(word, 0))
        assert gc not in s
        a = L.arr(s); L.flip(a, X.pulseR(W0 - 11)); bias = Z.bias_of(L, [gc])
        h = T.arr(s | {gc})
        for c in X.pulseR(W0 - 11):
            h[T.ix(c)] ^= 1
        for g in range(121):
            if not T.same(h, L.cells(a) | {gc}):
                ok = False; print(f'  C held cell {ghost}: differ at generation {g}'); break
            n += 1
            Z.run_bias(L, a, bias, 1); h = T.step(h); h[T.ix(gc)] = 1
        ok &= not L.touch
    return ok, f'bias stepper = oracle with the cell forced live, 3 held cells, {n} generations compared'


def part_D():
    import call9
    from call9 import lab
    d = json.load(open(os.path.join(HERE, 'objects', 'call9.json')))
    ok = True; n = 0
    for run in d['runs']:
        offs = [tuple(o) for o in run['offsets']]; T = Tor(run['H'])
        s = call9.state(run['start'], run['extra'], offs)
        U = lab.pk(s); h = T.arr(s)
        ops = {g: [tuple(c) for c in off + on] for g, off, on in run['ops']}
        G = max(g for g, _ in run['checks'])
        for g in range(G + 1):
            if not T.same(h, lab.up(U)):
                ok = False; print(f"  D {run['name']}: differ at generation {g}"); break
            n += 1
            if g in ops:
                U = lab.xor(U, lab.pk(ops[g]))
                for c in ops[g]:
                    h[T.ix(c)] ^= 1
            U = lab.run(U, 1); h = T.step(h)
    return ok, f"push 8b's stepper = oracle on the {len(d['runs'])} runs of call9.json, {n} generations compared"


def part_E():
    import beside9, wall9
    ref = wall9.Ref(3); ok = True; n = nin = 0
    for o in Z.catalogue():
        if o['period'] != 1 or len(o['cells']) > 6:
            continue
        orb = Z.orbit([tuple(c) for c in o['cells']], 1)
        for gi, ph, t, cells in Z.placements(orb):
            if not beside9.stands(cells, 1):
                continue
            ob = wall9.Obj(Z.orbit(cells, 1))
            for e in range(-3, 4):
                m = wall9.W0 - 1 + e - ob.umax
                n += 1
                try:
                    if not (ob.inert(ref, 'rest', m) and ob.inert(ref, 'A', m)):
                        continue
                except ValueError:
                    continue
                nin += 1
                S0 = [tr(c, m) for c in cells]
                L = Z.box_for(S0, wall9.R)
                a = L.arr(X.hexword(ref.word, 0)); L.flip(a, X.pulseR(wall9.W0 - 11)); b = a.copy()
                L.flip(a, S0); L.run(a, wall9.T); L.run(b, wall9.T); L.flip(b, S0)
                if not np.array_equal(a, b):
                    ok = False; print(f"  E {o['id']} gi={gi} t={t} e={e}: the shortcut says inert, the stepped run differs")
    return ok, f"wall9's inert shortcut: {nin} of {n} (placement, e) called inert for the pulse scenario, each stepped and equal to the union"


def main():
    only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else list('ABCDE')
    ok_all = True
    for name, f in (('A', part_A), ('B', part_B), ('C', part_C), ('D', part_D), ('E', part_E)):
        if name not in only:
            continue
        t0 = time.time(); ok, msg = f(); ok_all &= ok
        print(('PASS ' if ok else 'FAIL ') + f'{name}: {msg}  [{time.time() - t0:.0f} s]', flush=True)
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
