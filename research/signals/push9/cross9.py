#!/usr/bin/env python3
"""cross9 (push 9): a pulse on a second wire that crosses the store near the wall of a stretch: does it release it?

    python3 cross9.py B|C [--part i/n] [--out F.jsonl]

Placements: push 8b's survey of every non-parallel placement of a capped wire B (or C) beside wire B, modulo sliding
(research/scratch/signals/p8b/survey_B.jsonl, survey_C.jsonl; written by ../push8b/survey.py), those that stand
beside plain wire B ('transparent' or 'junction').  Stepper and wires: push 8b's lab.py (st.c, checked against the
oracle by ../push8b/check_st.py) and wires.py, imported unchanged.
Store: push 8's cell with 24 units of wire B, the stretch d^3 f and 10 more units.  For each placement the crossing
is put at the unit before the wall + j, j = -3..4; the pair is run 160 generations and kept if it then has period
dividing 4 and the store's tube still reads 7^24 d^3 f 7^10.  Probes on the second wire, launched 9 and 10 of its
units before the crossing: one right-going pulse; two in adjacent units.  The store's tube is read 30, 36, 44, 60 and 260
generations later; 'reader as it was': at 260 every cell outside the store's tube is what it would have been.
One JSON line per (placement, j, probe) in which the store's letters changed; a summary is printed.
"""
import sys, os, json, argparse, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'push8'))
import exp8 as X, wire8 as W8           # noqa: E402
sys.path.insert(0, os.path.join(HERE, '..', 'push8b'))
import lab, wires, survey               # noqa: E402  (push 8b)
from lab import tr, unit                # noqa: E402

NL, K, NRT = 24, 3, 10
WALL = 4 + NL
STS = set(W8.ST); SITES = W8.SITES


def in_tube(c):
    return abs(c[1]) + abs(c[0] + c[2] - 3) <= 2


def letters(keys, u0, u1):
    by = {}
    for c in lab.up(keys):
        if in_tube(c):
            by.setdefault(unit(c), set()).add(tr(c, -unit(c)))
    out = []
    for u in range(u0, u1):
        uc = by.get(u, set())
        if not uc:
            out.append('_'); continue
        rest = uc - STS
        if len(uc) - len(rest) != 2 or not rest <= set(SITES):
            out.append('?'); continue
        out.append('%x' % sum(1 << i for i in range(4) if SITES[i] in rest))
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('reader'); ap.add_argument('--part', default='0/1'); ap.add_argument('--out')
    a = ap.parse_args()
    i, n = map(int, a.part.split('/'))
    rows = [json.loads(l) for l in open(os.path.join(lab.SCR, f'survey_{a.reader}.jsonl'))]
    rows = [r for r in rows if r['res']['B'].get('static', '').startswith(('transparent', 'junction'))][i::n]
    rc, pulse, wire0 = survey.reader_spec(a.reader)
    obj, N = X.cell('d' * K + 'f', NL, NRT)
    store = lab.pk(obj)
    want = '7' * NL + 'd' * K + 'f' + '7' * NRT
    assert letters(store, 4, 4 + N) == want
    capcells = frozenset(q for q in obj if not in_tube(q))
    out = open(a.out, 'w') if a.out else None
    c = Counter(); t0 = time.time(); hits = []
    for r in rows:
        g = lab.SYMS[r['g']]; t = tuple(r['t']); us, ur, phi = r['us'], r['ur'], r['phi']
        own = lab.run(lab.pk(rc), phi)
        for j in range(-3, 5):
            m = WALL - 1 + j - us
            tt = (t[0] + 2 * m, t[1], t[2] - 2 * m)
            Rk = lab.pk([lab.app(g, q, tt) for q in lab.up(own)])
            U = lab.union(store, Rk)
            if len(U) != len(store) + len(Rk):
                c['overlap'] += 1; continue
            J = lab.run(U, 160)
            if not lab.same(lab.run(J, 4), J) or letters(J, 4, 4 + N) != want:
                c['does not stand'] += 1; continue
            c['stands'] += 1
            Y = lab.run(J, phi)
            for name, ats in (('1@9', (9,)), ('1@10', (10,)), ('2@9', (9, 10)), ('2@10', (10, 11))):
                P = lab.pk([lab.app(g, q, tt) for at in ats for q in wires.pulse(pulse, ur - at)])
                Xs = lab.xor(Y, P)
                seen = []; Xt = Xs
                for dt in (30, 6, 8, 16):
                    Xt = lab.run(Xt, dt); seen.append(letters(Xt, 4, 4 + N))
                X260 = lab.run(Xt, 200); s260 = letters(X260, 4, 4 + N)
                if all(v == want for v in seen) and s260 == want:
                    c['store unchanged'] += 1; continue
                Jt = lab.run(J, (phi + 260) % 4)
                other = lambda k: frozenset(q for q in lab.up(k) if not in_tube(q) and q not in capcells)
                reader_ok = other(X260) == other(Jt)
                moving = [X.hexrle(v.strip('7') or '7') for v in seen]
                kind = ('EMPTIED' if not (set(s260) - set('7')) else 'changed') + (', reader as it was' if reader_ok else ', reader changed')
                c[kind] += 1
                rec = dict(reader=a.reader, g=r['g'], phi=phi, t=list(t), us=us, ur=ur, j=j, probe=name, seen=moving, s260=X.hexrle(s260), kind=kind)
                hits.append(rec)
                if out:
                    out.write(json.dumps(rec) + '\n'); out.flush()
                if kind.startswith('EMPTIED'):
                    print('  ', kind, {k_: rec[k_] for k_ in ('g', 'phi', 't', 'us', 'ur', 'j', 'probe', 'seen')}, flush=True)
    print(f'reader {a.reader}, part {a.part}: {len(rows)} placements standing beside plain wire B; (placement, j): {dict(c)}   [{time.time() - t0:.0f} s]')


if __name__ == '__main__':
    main()
