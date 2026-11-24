#!/usr/bin/env python3
"""The executable tie between `Gump.Dice.Face.P` (GumpMath/DiceDef.lean) and research/blast/rigour/dense.py.

For each face below, Lean evaluates its own definition (`#eval` of `Face.P` on every pair of states for faces of
at most 6 cells, on 24 random rows of all 512 columns for 9-cell faces, and the per-cell alive probabilities
`Face.a` on every state and cell) in exact rationals; this script compares the numbers with dense.py's kernel
(`dense.kernel`, floats, built by enumerating each cell's coins over geom.py's graph) and with an exact Fraction
recomputation of dense.py's formula. Also compared: the neighbour lists (as multisets) and the coin counts.

    python3 research/blast/lean/dice_tie.py            # about two minutes; prints one line per face, then PASS
    python3 research/blast/lean/dice_tie.py --mutant   # negative control: the same with rho1 changed in Lean

What it does not cover: the survival function and the matrix power (defined in Lean from P, not compared), faces
other than those listed, and the parsing of Lean's output (a mismatch would show as a failure, not a pass).
"""
import sys, os, subprocess, tempfile, random, itertools
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'rigour'))
import geom, dense  # noqa: E402

FACES = [('hull', (1,)), ('torus', (1, 0, 1)), ('torus', (1, 0, 2)), ('torus', (1, 1, 2)), ('strip', (1, 2)),
         ('patch', (1, 2)), ('torus', (2, 0, 1)),
         ('hull', (3,)), ('torus', (1, 0, 3)), ('torus', (1, 1, 3)), ('strip', (1, 3)), ('patch', (1, 3))]
R1, R2 = Fraction(11, 25), Fraction(21, 50)


def lean_name(kind, args):
    return '(%s %s)' % (kind, ' '.join(map(str, args)))


def exact_a(nb, m, x, i, r1, r2):
    k = sum((x >> j) & 1 for j in nb[i])
    s = (x >> i) & 1
    tot = Fraction(0)
    for coins in itertools.product((0, 1), repeat=m[i][0] + m[i][1]):
        w = Fraction(1)
        for t, c in enumerate(coins):
            r = r1 if t < m[i][0] else r2
            w *= r if c else 1 - r
        n = k + sum(coins)
        if (3 <= n <= 5) if s else (n in (4, 5)):
            tot += w
    return tot


def main():
    mutant = '--mutant' in sys.argv
    rho1 = '(12/25 : ℚ)' if mutant else 'ρ1'
    rng = random.Random(7)
    plan = []
    src = ['import GumpMath.DiceDef', 'open Gump.Dice Finset', 'set_option maxRecDepth 100000',
           'def entry (F : Face) (r1 r2 : ℚ) (x y : ℕ) : ℚ :=',
           '  if h : x < 2 ^ F.A then if h2 : y < 2 ^ F.A then F.P r1 r2 ⟨x, h⟩ ⟨y, h2⟩ else 0 else 0']
    for kind, args in FACES:
        nb, m = geom.build(kind, *args)
        A = len(nb)
        F = lean_name(kind, args)
        rows = list(range(1 << A)) if A <= 6 else sorted(rng.sample(range(1 << A), 24))
        plan.append((kind, args, nb, m, A, rows))
        src.append('#eval show IO Unit from do')
        src.append('  for i in List.range %s.A do IO.println s!"G %d {i} {%s.nb i} {%s.m1 i} {%s.m2 i}"' % (F, len(plan) - 1, F, F, F))
        src.append('  for x in List.range (2 ^ %s.A) do IO.println s!"a %d {x} {(List.range %s.A).map fun i => %s.a %s ρ2 x i}"' % (
            F, len(plan) - 1, F, F, rho1))
        src.append('  for x in [%s] do IO.println s!"P %d {x} {(List.range (2 ^ %s.A)).map fun y => entry %s %s ρ2 x y}"' % (
            ', '.join(map(str, rows)), len(plan) - 1, F, F, rho1))
    d = tempfile.mkdtemp()
    fn = os.path.join(d, 'tie.lean')
    open(fn, 'w').write('\n'.join(src) + '\n')
    env = dict(os.environ, PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ['PATH'])
    out = subprocess.run(['lake', 'env', 'lean', fn], cwd=os.path.join(HERE, 'mathlib'), env=env,
                         capture_output=True, text=True)
    if out.returncode != 0:
        print(out.stdout[-2000:], out.stderr[-2000:]); raise SystemExit('FAIL: Lean')
    G, AT, PR = {}, {}, {}
    for line in out.stdout.splitlines():
        t = line.split(' ', 3)
        if len(t) < 4 or t[0] not in 'GaP':
            continue
        f, idx, rest = int(t[1]), int(t[2]), t[3]
        if t[0] == 'G':
            lst, m1, m2 = rest.rsplit(' ', 2)
            G.setdefault(f, {})[idx] = (conv(lst), int(m1), int(m2))
        elif t[0] == 'a':
            AT.setdefault(f, {})[idx] = conv(rest)
        else:
            PR.setdefault(f, {})[idx] = conv(rest)
    ok = True
    for f, (kind, args, nb, m, A, rows) in enumerate(plan):
        g, atab, prow = G[f], AT[f], [PR[f][x] for x in rows]
        geo = all(sorted(g[i][0]) == sorted(nb[i]) and (g[i][1], g[i][2]) == tuple(m[i]) for i in range(A))
        P = dense.kernel(A, nb, m, 0.44, 0.42)
        ea = max(abs(atab[x][i] - exact_a(nb, m, x, i, R1, R2)) for x in range(1 << A) for i in range(A))
        ep = max(abs(float(prow[r][y]) - P[x, y]) for r, x in enumerate(rows) for y in range(1 << A))
        sums = max(abs(sum(prow[r]) - 1) for r in range(len(rows)))
        good = geo and ea == 0 and ep < 1e-14 and sums == 0
        ok &= good
        print('%-6s %-10s A=%2d  graph %s  exact a-table %s  P rows %3d: max |Lean - dense.py| = %.1e  row sums exact 1: %s  %s' % (
            kind, args, A, 'same' if geo else 'DIFFERENT', 'same' if ea == 0 else 'DIFFERENT (%.3g)' % ea,
            len(rows), ep, sums == 0, 'ok' if good else 'MISMATCH'))
    print('PASS' if ok else 'FAIL')
    if mutant == ok:
        raise SystemExit(1)


def conv(b):
    import re
    b = b.replace('\n', ' ')
    b = re.sub(r'(-?\d+)/(\d+)', r'Fraction(\1,\2)', b)
    return eval(b, {'Fraction': Fraction})


if __name__ == '__main__':
    main()
