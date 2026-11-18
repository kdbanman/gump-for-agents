#!/usr/bin/env python3
"""push 8b: writing and erasing with the reader in place (st.c stepper).

    python3 rw.py cross      a pulse of the STORE passes under the reader (plain wire B): is anything changed?
    python3 rw.py erase      push 8's one-cell release of a stretch d^k f, the reader standing beside its interior
    python3 rw.py cross24    the same for all 24 reading placements of junc2.py (posmap.py)
    python3 rw.py train      all 24 reading placements beside push 7's line BEFORE the write (the rake train running),
                             crossing at units 38..49: does the reader stand there for 300 generations?
    python3 rw.py grow       pulses of the store born beside the reader (one stator removed, 1 to 6 times, every 4, 6 or 8
                             generations) towards a wall to its right or an edge to its left: can a stretch grow past it?

Store: a capped wire B on units -24..24 (wires.capped_B; the cell of push 8), with a stretch of k units of wire B'
and the edge unit f put in by hand (stretch_store).  Reader: cell.READERS, crossing at store unit 0.
Letters of the store as line.letters: b wire B, p wire B', c wire C (a left-going pulse of wire B is one unit c),
# anything else (the edge unit f; a right-going pulse is two units ##)."""
import sys
import lab, wires, line, cell, junc
from lab import tr, unit

UA, UB = -24, 24
F0 = sorted(set(lab.B0) | set(lab.BP0))
READ = {'b13': 1, 'b8': 1, 'r246': 3, 'r132': 3}     # spacing of the reading pair


def stretch_store(w=None, k=0):
    cells = set(wires.capped_B(UA, UB))
    if k:
        for u in range(w, w + k + 1):
            cells -= {tr(c, u) for c in lab.B0}
            cells |= {tr(c, u) for c in (lab.BP0 if u < w + k else F0)}
    S = lab.pk(sorted(cells))
    assert lab.same(lab.run(S, 2), S), 'the store does not stand'
    return S


def store_letters(X, ua=-12, ub=13):
    return line.letters(lab.pk([c for c in lab.up(X) if cell.in_tube(c)]), ua, ub)[1]


def reader_intact(X, rd, J):
    """the cells outside the store's tube are those of the standing state J (generation divisible by 4)."""
    a = sorted(c for c in lab.up(X) if not cell.in_tube(c)); b = sorted(c for c in lab.up(J) if not cell.in_tube(c))
    return a == b


def read_out(J, rd, spacing):
    arr, J2, verdict = cell.read(J, rd, spacing=spacing)
    return f'{arr}, {verdict}'


def experiment(name, S, flips, T=400, label=''):
    """S: store; reader `name` at unit 0; flips: list of (generation after the settling, cells)."""
    rd = cell.Reader(name, 0)
    v, J = cell.install(S, rd)
    if J is None:
        print(f'  {label}: the reader does not stand: {v}'); return
    X = J
    fl = dict(flips)
    for t in range(T):
        if t in fl:
            X = lab.xor(X, lab.pk(fl[t]))
        X = lab.run(X, 1)
    per = next((p for p in (2, 4) if lab.same(lab.run(X, p), X)), None)
    s0, s1 = store_letters(J), store_letters(X)
    ok = reader_intact(X, rd, J)
    row = f'  {label}: {s0} -> {s1}  period {per}, reader {"as it was" if ok else "CHANGED"}'
    if per and ok:
        row += '; reading pair now: ' + read_out(X, rd, READ[name])
    print(row, flush=True)


def stator(u, which=2):
    return (2 * u, 1, which - 2 * u)


if __name__ == '__main__':
    cmd = sys.argv[1]
    names = sys.argv[2].split(',') if len(sys.argv) > 2 else ['b13', 'b8', 'r246', 'r132']
    if cmd == 'cross':
        S = stretch_store()
        for name in names:
            print(f'reader {name}:')
            rd = cell.Reader(name, 0); v, J = cell.install(S, rd)
            for side, pc in (('right-going pulse from unit -10', wires.pulse(lab.PULSE_B, -10)), ('left-going pulse from unit 10', wires.pulse(junc.LEFT['B'], 10))):
                # compare with the same pulse on the store without the reader
                X = lab.xor(J, lab.pk(pc)); Xs = lab.xor(S, lab.pk(pc)); Y = J; Ys = S
                worst = 0
                for t in range(200):
                    X = lab.run(X, 1); Y = lab.run(Y, 1); Xs = lab.run(Xs, 1); Ys = lab.run(Ys, 1)
                    if not lab.same(lab.xor(X, Y), lab.xor(Xs, Ys)):
                        worst += 1
                print(f'  {side}: install {v}; generations (of 200) at which the pulse\'s trace differs from its trace without the reader: {worst}; at the end all as before: {lab.same(X, Y)}')
    elif cmd == 'cross24':
        import json, os, posmap
        S = stretch_store()
        for w in 'BC':
            for l in open(os.path.join(lab.SCR, f'junc2_{w}_0of1.jsonl')):
                r = json.loads(l)
                rd = posmap.R(w, r['g'], r['phi'], r['t'], 0)
                J = lab.run(lab.union(S, rd.place(lab.up(lab.run(rd.own, rd.phi)))), 160)
                assert lab.same(lab.run(J, 4), J)
                row = f"  reader {w} g={r['g']} phi={r['phi']} t={tuple(r['t'])}:"
                for side, pc in (('right-going', wires.pulse(lab.PULSE_B, -10)), ('left-going', wires.pulse(junc.LEFT['B'], 10))):
                    for delay in (0, 2):
                        X = lab.run(lab.xor(lab.run(J, delay), lab.pk(pc)), 240 - delay)
                        per = next((p for p in (2, 4) if lab.same(lab.run(X, p), X)), None)
                        row += f"  {side} +{delay}: " + ('as before' if lab.same(X, J) else f'changed ({len(lab.xor(X, J))} cells, period {per})')
                print(row, flush=True)
    elif cmd == 'train':
        import json, os, posmap
        L0 = cell.line0(); L300 = lab.run(L0, 300)
        print('one character per crossing unit 38..49: . the state at generation 300 is (line alone) u (reader alone); r the line is as alone, the reader not; X the line is not as alone')
        for w in 'BC':
            for l in open(os.path.join(lab.SCR, f'junc2_{w}_0of1.jsonl')):
                r = json.loads(l)
                row = ''
                for u in range(38, 50):
                    rd = posmap.R(w, r['g'], r['phi'], r['t'], u)
                    R0 = rd.place(lab.up(lab.run(rd.own, rd.phi)))
                    U = lab.union(L0, R0)
                    if len(U) != len(L0) + len(R0):
                        row += 'o'; continue
                    X = lab.run(U, 300)
                    if lab.same(X, lab.union(L300, lab.run(R0, 300))):
                        row += '.'
                    else:
                        tube = lab.pk([c for c in lab.up(X) if cell.in_tube(c)])
                        row += 'r' if lab.same(tube, lab.pk([c for c in lab.up(L300) if cell.in_tube(c)])) else 'X'
                print(f"  reader {w} g={r['g']} phi={r['phi']} t={tuple(r['t'])}:  {row}", flush=True)
    elif cmd == 'erase':
        for name in names:
            print(f'reader {name}: stretch d^k f from unit w, the stator (0,1,2) of unit w-1 removed at generation 0')
            for k in (2, 3, 4, 6):
                for w in range(-k, 1):
                    S = stretch_store(w, k)
                    experiment(name, S, [(0, [stator(w - 1)])], label=f'k={k} w={w}')
    elif cmd == 'grow':
        from collections import Counter
        for name in names:
            rd = cell.Reader(name, 0)
            cnt = Counter(); good = []
            cases = []
            for k in (1, 2):
                for w in range(1, 7):                      # the wall to the right of the reader; pulses born at u < w - 1
                    for u in range(-4, w - 1):
                        cases.append((w, k, 'R', u))
                for e in range(-6, 0):                     # the edge to the left of the reader; pulses born at u > e + 1
                    for u in range(e + 2, 5):
                        cases.append((e - k, k, 'L', u))
            for (w, k, side, u) in cases:
                S = stretch_store(w, k)
                v, J = cell.install(S, rd)
                if J is None:
                    cnt['the reader does not stand beside the start'] += 1; continue
                for m in range(1, 7):
                    for s_ in (2, 3, 4):
                        X = J
                        fl = {2 * s_ * i: [stator(u, 2 if side == 'R' else 4)] for i in range(m)}
                        for t in range(400):
                            if t in fl:
                                X = lab.xor(X, lab.pk(fl[t]))
                            X = lab.run(X, 1)
                        per = next((p for p in (2, 4) if lab.same(lab.run(X, p), X)), None)
                        ok = reader_intact(X, rd, J)
                        s0, s1 = store_letters(J), store_letters(X)
                        if per and ok and s1 == s0:
                            cnt['nothing changed'] += 1
                        elif per and ok:
                            cnt['store changed, standing, reader as it was'] += 1
                            good.append(f'    w={w} k={k} {side}@{u} x{m} every {2 * s_} generations: {s0} -> {s1}; reading pair now: ' + read_out(X, rd, READ[name]))
                        else:
                            cnt['burnt or reader changed'] += 1
            print(f'reader {name}: ' + ', '.join(f'{v} {k_}' for k_, v in cnt.most_common()))
            for g_ in good:
                print(g_)
