#!/usr/bin/env python3
"""Analysis of this review's runs (research/scratch/audit_shape3/ev_*.txt, from plan.py).

    python3 research/audit/shape3/ana.py            # per torus, pair differences, settled-life periods

Per torus: exposure E (sum of ages; settled lives censored at the snapshot age, inside the cycle), counts;
ln tau_face = ln(2E/F) +- 1/sqrt(F) with events resolved per generation ("gen"); the same with every ended life's age
rounded up to a multiple of 8 ("w8", what an 8-generation check window gives for lives born on a check); ties
(face death and firewall in the same generation) counted as face deaths ("ties as face"); E with settled lives'
exposure removed ("no S"). Settled lives: how many have a period not dividing 840 (missed by the one-lag test of
ts.c), how many have p / gcd(p, 840) > 128 (missed by ts3's test too), their share of lives.
"""
import collections, glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as v  # noqa: E402

ZOMBIE = '--all' in sys.argv   # include the diagnostic jobs (seeds >= 71101; zombie rates only, never in d)
PAIRS = [('Q36', (1, 4, 12), (1, 3, 12)), ('Q45', (1, 5, 15), (1, 4, 15)), ('P1', (2, 2, 8), (1, 6, 16))]


def load(L):
    files = sorted(glob.glob(os.path.join(v.OUT, f'ev_{L[0]}_{L[1]}_{L[2]}_s*.txt')))
    files = [f for f in files if int(f.rsplit('_s', 1)[1][:-4]) < 71100] if not ZOMBIE else files
    r = collections.Counter(); r['jobs'] = len(files)
    per = collections.Counter(); per_lives = 0
    for f in files:
        for line in open(f):
            p = line.split(); t = p[0]; a = int(p[1])
            r[t] += 1; r['Exp'] += a
            if t in 'FWX':
                r['E8'] += 8 * (-(-a // 8))
            else:
                r['E8'] += a
            if t == 'S':
                per[int(p[2])] += 1; r['ES'] += a
                q = int(p[2]); m = q // math.gcd(q, 840)
                if 840 % q:
                    r['Z840'] += 1
                if m > 128:
                    r['Z128'] += 1
    r['lives'] = sum(r[t] for t in 'FWXSCE')
    return r, per


def lt(E, F):
    return math.log(2 * E / F), 1 / math.sqrt(F)


def main():
    res = {}
    print('torus       jobs  exposure     F         W      X     S    open  ln tau (gen)        w8       ties-as-face  no-S     '
          'S: p∤840  p/gcd>128  share of ended lives (p∤840)')
    for L in sorted({x for _, X, Y in PAIRS for x in (X, Y)} | {(2, 4, 12)}):
        r, per = load(L)
        if not r['jobs'] or not r['F']:
            continue
        res[L] = r
        g, e = lt(r['Exp'], r['F']); w8, _ = lt(r['E8'], r['F']); tf, _ = lt(r['Exp'], r['F'] + r['X']); ns, _ = lt(r['Exp'] - r['ES'], r['F'])
        w8t, _ = lt(r['E8'], r['F'] + r['X'])
        ended = r['F'] + r['W'] + r['X'] + r['S'] + r['C']
        print(f'{str(L):11s} {r["jobs"]:3d} {r["Exp"]:.4e} {r["F"]:9d} {r["W"]:6d} {r["X"]:5d} {r["S"]:5d} {r["E"]:5d}  '
              f'{g:.4f} +- {e:.4f}  {w8:.4f}  {tf:.4f}  {ns:.4f}  w8+ties {w8t:.4f}   {r["Z840"]:4d}  {r["Z128"]:4d}   {r["Z840"] / ended:.2e}')
        top = ', '.join(f'{p}:{c}' for p, c in sorted(per.items(), key=lambda x: -x[1])[:12])
        odd = ', '.join(f'{p}:{c}' for p, c in sorted(per.items()) if 840 % p)
        print(f'            settled periods (most common): {top}; periods not dividing 840: {odd}')
    print()
    for tag, X, Y in PAIRS:
        if X in res and Y in res:
            rx, ry = res[X], res[Y]
            out = []
            for key, fk in (('gen', 'F'), ('w8', 'F'), ('ties as face', 'FX'), ('no S', 'F')):
                Ek = {'gen': 'Exp', 'w8': 'E8', 'ties as face': 'Exp', 'no S': None}[key]
                def val(r):
                    E = r['Exp'] - r['ES'] if Ek is None else r[Ek]
                    F = r['F'] + (r['X'] if fk == 'FX' else 0)
                    return math.log(2 * E / F)
                out.append(f'{key} {val(ry) - val(rx):+.4f}')
            err = math.sqrt(1 / rx['F'] + 1 / ry['F'])
            print(f'{tag} {X} -> {Y}: d = ' + ', '.join(out) + f'  (+- {err:.4f})')


if __name__ == '__main__':
    main()
