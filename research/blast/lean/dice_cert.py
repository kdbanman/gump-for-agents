#!/usr/bin/env python3
"""Certificates for the lifetime of small faces of the one-layer dice surrogate (blast/rigour), checked in Lean.

For a face (built by research/blast/rigour/geom.py, the same graph Lean's `Gump.Dice.Face` computes; the Lean
check compares them) at (rho1, rho2) = (11/25, 21/50) this script
  1. builds the integer transition numerators N(x, y) = prod_i (alpha_i(x) if y_i else D_i - alpha_i(x)), with
     D_i = 25^m1_i 50^m2_i and alpha_i(x) the number of coin outcomes (weighted by 11, 14, 21, 29) for which
     cell i is alive next; P = N / prod_i D_i;
  2. finds the right Perron vector r of the killed chain (Q r = lambda r, Q = P without the empty state):
     a float eigenvector refined by exact integer power iteration;
  3. rounds it to integer vectors V_up (positive on every non-empty state) and V_lo (zero where r = 0),
     and the exact Collatz-Wielandt ratios to decimal bounds lam_up >= max (N V_up)(x) / (D V_up(x)) and
     mu_lo <= min (N V_lo)(x) / (D V_lo(x));
  4. writes the Lean data file GumpMath/Dice<Name>Data.lean (the vectors as binary trees, the tables, the
     bounds), which `GumpMath/DiceCert.lean` checks in the kernel.

    python3 research/blast/lean/dice_cert.py hull 3        # -> GumpMath/DiceHull3Data.lean
    python3 research/blast/lean/dice_cert.py torus 1 1 3   # -> GumpMath/DiceTorus113Data.lean
"""
import sys, os, itertools
from fractions import Fraction
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'rigour'))
import geom  # noqa: E402

N1, D1, N2, D2 = 11, 25, 21, 50   # rho1 = 0.44, rho2 = 0.42


def rule(s, n):
    return (3 <= n <= 5) if s else (n in (4, 5))


def alive_num(m1, m2, k, s):
    """sum over coin outcomes (j heads of m1, l of m2) of C(m1,j) 11^j 14^(m1-j) C(m2,l) 21^l 29^(m2-l)
    [rule s (k+j+l)]; divided by 25^m1 50^m2 it is the probability that the cell is alive next"""
    t = 0
    for j in range(m1 + 1):
        for l in range(m2 + 1):
            if rule(s, k + j + l):
                t += comb(m1, j) * N1**j * (D1 - N1)**(m1 - j) * comb(m2, l) * N2**l * (D2 - N2)**(m2 - l)
    return t


# Gump.offsets of Gump/Basic.lean, in its order (the order of the lists `Face.nb` computes)
LEAN_OFF = {
    0: [(0, 2, 2), (0, 2, -2), (0, -2, 2), (0, -2, -2), (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
        (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1)],
    1: [(2, 0, 2), (2, 0, -2), (-2, 0, 2), (-2, 0, -2), (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
        (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)],
    2: [(2, 2, 0), (2, -2, 0), (-2, 2, 0), (-2, -2, 0), (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
        (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1)]}


def lean_face(kind, args):
    """A Python mirror of `Gump.Dice.hull`, `torus`, `strip`, `patch` (cells in order, the reduction `red`)."""
    if kind == 'hull':
        R, = args
        cells = [(x, y, R - x - y) for x in range(R + 1) for y in range(R + 1 - x)
                 if (x % 2) + (y % 2) + ((R - x - y) % 2) == 1]
        return cells, (lambda q: q)
    W, D = (args[0], args[2]) if kind == 'torus' else args
    cells = [geom.ab_cell(o, a, b, 1) for a in range(W) for b in range(D) for o in range(3)]
    if kind == 'torus':
        H, K, D = args
        def red(q):
            o, a, b = geom.cell_ab(q, 1)
            return geom.ab_cell(o, a % H, (b - (a // H) * K) % D, 1)
    elif kind == 'strip':
        def red(q):
            o, a, b = geom.cell_ab(q, 1)
            return geom.ab_cell(o, a, b % D, 1)
    else:
        def red(q):
            return q
    return cells, red


def face(kind, args):
    """the graph in the order of Lean's `Face.nb`, checked here to be geom.py's graph as multisets"""
    nbg, m = geom.build(kind, *args)
    cells, red = lean_face(kind, args)
    ix = {c: i for i, c in enumerate(cells)}
    nb = []
    for p in cells:
        o = geom.axis(p)
        l = []
        for off in LEAN_OFF[o]:
            if sum(off) == 0:
                q = red(tuple(p[i] + off[i] for i in range(3)))
                if q in ix:
                    l.append(ix[q])
        nb.append(l)
    assert [sorted(a) for a in nb] == [sorted(b) for b in nbg], "Lean mirror and geom.py disagree"
    return len(nb), nb, m


def tables(A, nb, m):
    Dc = [D1**m1 * D2**m2 for (m1, m2) in m]
    T = [[alive_num(m[i][0], m[i][1], j // 2, j % 2 == 1) for j in range(2 * (len(nb[i]) + 1))] for i in range(A)]
    return Dc, T


def alphas(A, nb, T, x):
    out = []
    for i in range(A):
        k = sum((x >> j) & 1 for j in nb[i])
        s = (x >> i) & 1
        out.append(T[i][2 * k + s])
    return out


def numerators(A, nb, Dc, T):
    """dense integer matrix N[x][y] (object array)"""
    n = 1 << A
    N = np.empty((n, n), dtype=object)
    ys = range(n)
    for x in range(n):
        al = alphas(A, nb, T, x)
        row = [1] * n
        for i in range(A):
            a, b = Dc[i] - al[i], al[i]
            for y in ys:
                row[y] *= b if (y >> i) & 1 else a
        N[x, :] = row
    return N


def perron(A, N, Dtot, iters=400, bits=200):
    n = 1 << A
    Qf = np.array(N[1:, 1:], dtype=float) / float(Dtot)
    w, vr = np.linalg.eig(Qf)
    j = int(np.argmax(w.real))
    r = np.abs(vr[:, j].real)
    r = r / r.max()
    # exact refinement: V <- N V, rescaled to `bits` bits, on the non-empty states (index 0 = empty, kept 0)
    V = [0] + [int(round(float(v) * 2**60)) for v in r]
    Nl = [list(N[x]) for x in range(n)]
    for _ in range(iters):
        W = [0] + [sum(a * b for a, b in zip(Nl[x], V)) for x in range(1, n)]
        mx = max(W)
        sh = mx.bit_length() - bits
        V = [w_ >> sh if sh > 0 else w_ << -sh for w_ in W]
    lam = float(Fraction(sum(a * b for a, b in zip(Nl[n - 1], V)), Dtot * V[n - 1])) if V[n - 1] else None
    return V, Nl, w[j].real, lam


def bounds(A, Nl, Dtot, Vup, Vlo):
    n = 1 << A
    up = max(Fraction(sum(a * b for a, b in zip(Nl[x], Vup)), Dtot * Vup[x]) for x in range(1, n))
    lo = min(Fraction(sum(a * b for a, b in zip(Nl[x], Vlo)), Dtot * Vlo[x]) for x in range(1, n) if Vlo[x] > 0)
    return up, lo


def tree(vals):
    if len(vals) == 1:
        return "(.leaf %d)" % vals[0]
    h = len(vals) // 2
    return "(.node %s %s)" % (tree(vals[:h]), tree(vals[h:]))


def dec_up(fr, digits):
    s = 10**digits
    q = -((-fr.numerator * s) // fr.denominator)
    return q, s


def dec_dn(fr, digits):
    s = 10**digits
    return (fr.numerator * s) // fr.denominator, s


def main():
    kind = sys.argv[1]
    args = [int(a) for a in sys.argv[2:]]
    name = kind.capitalize() + ''.join(str(a) for a in args)
    A, nb, m = face(kind, args)
    Dc, T = tables(A, nb, m)
    Dtot = 1
    for d in Dc:
        Dtot *= d
    N = numerators(A, nb, Dc, T)
    V, Nl, lam_float, lam_exact = perron(A, N, Dtot)
    n = 1 << A
    # die surely in one step: every alpha_i(x) = 0
    sure = [x != 0 and all(a == 0 for a in alphas(A, nb, T, x)) for x in range(n)]
    zeros = [x for x in range(1, n) if V[x] == 0]
    assert all(sure[x] for x in zeros), "a state with r = 0 that does not die surely: needs a finer upper vector"
    pos = [V[x] for x in range(1, n) if V[x] > 0]
    vmin = min(pos)
    Vup = [0] + [V[x] if V[x] > 0 else vmin for x in range(1, n)]
    Vlo = list(V)
    up, lo = bounds(A, Nl, Dtot, Vup, Vlo)
    digits = 22
    Lup, Mup = dec_up(up, digits)
    Llo, Mlo = dec_dn(lo, digits)
    print('# %s %s: A = %d, die-surely states %d, r = 0 states %d' % (kind, args, A, sum(sure), len(zeros)), file=sys.stderr)
    print('# lambda (float eig) %.16f; Collatz-Wielandt: %.20f <= lambda <= %.20f' % (lam_float, float(lo), float(up)), file=sys.stderr)
    print('# h = 1 - lambda in [%.17e, %.17e]; ln tau in [%.12f, %.12f]' % (
        1 - float(up), 1 - float(lo), -np.log(1 - float(lo)), -np.log(1 - float(up))), file=sys.stderr)
    cond = Fraction(max(Vup), vmin)
    print('# max V_up / min V_up = %.6g; V_lo(full) / max V_lo = %.6g' % (float(cond), V[n - 1] / max(V)), file=sys.stderr)
    out = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%sData.lean' % name)
    with open(out, 'w') as f:
        f.write('/-\nCertificate data for the face `%s %s` of the dice surrogate, written by\n'
                '`python3 research/blast/lean/dice_cert.py %s %s` (do not edit by hand).\n'
                'Checked in the kernel by `GumpMath/DiceCert.lean`; nothing here is trusted.\n-/\n'
                % (kind, ' '.join(map(str, args)), kind, ' '.join(map(str, args))))
        f.write('import GumpMath.DiceCert\n\nset_option maxRecDepth 100000\n\nnamespace Gump.Dice.%sData\nopen Gump.Dice\n\n' % name)
        f.write('/-- in-layer neighbour lists, as `geom.py` builds them -/\n')
        f.write('def G : List (List ℕ) := %s\n\n' % ('[' + ', '.join('[' + ', '.join(map(str, l)) + ']' for l in nb) + ']'))
        f.write('/-- coins (m1, m2) per cell -/\n')
        f.write('def C : List (ℕ × ℕ) := %s\n\n' % ('[' + ', '.join('(%d, %d)' % mm for mm in m) + ']'))
        f.write('/-- alive numerators, T[i][2k + s] -/\n')
        f.write('def T : List (List ℕ) := %s\n\n' % ('[' + ', '.join('[' + ', '.join(map(str, l)) + ']' for l in T) + ']'))
        f.write('/-- the tables at rho1 = %d/%d, rho2 = %d/%d -/\n' % (N1, D1, N2, D2))
        f.write('def data : Data := ⟨%d, %d, %d, %d, G, C, T⟩\n\n' % (N1, D1, N2, D2))
        f.write('/-- the upper vector (positive off the empty state) -/\n')
        f.write('def Vup : Tree := %s\n\n' % tree(Vup))
        f.write('/-- the lower vector -/\n')
        f.write('def Vlo : Tree := %s\n\n' % tree(Vlo))
        f.write('/-- lam_up = %d / %d -/\n' % (Lup, Mup))
        f.write('def Lup : ℕ := %d\ndef Mup : ℕ := %d\n' % (Lup, Mup))
        f.write('/-- mu_lo = %d / %d -/\n' % (Llo, Mlo))
        f.write('def Llo : ℕ := %d\ndef Mlo : ℕ := %d\n\n' % (Llo, Mlo))
        f.write('def vmin : ℕ := %d\ndef vmax : ℕ := %d\ndef wmax : ℕ := %d\ndef wfull : ℕ := %d\n\n' % (
            vmin, max(Vup), max(Vlo), Vlo[n - 1]))
        f.write('end Gump.Dice.%sData\n' % name)
    print('# wrote %s' % out, file=sys.stderr)


if __name__ == '__main__':
    main()
