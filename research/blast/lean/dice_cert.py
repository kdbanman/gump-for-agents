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


README = {('hull', (3,)): '2.4837157463', ('torus', (1, 0, 3)): '3.3935247191', ('torus', (1, 1, 3)): '2.6946266059',
          ('strip', (1, 3)): '2.7988780569', ('patch', (1, 3)): '1.8804189341'}


def dec_str(fr, digits, up):
    q, s = (dec_up if up else dec_dn)(fr, digits)
    t = str(q).rjust(digits + 1, '0')
    return t[:-digits] + '.' + t[-digits:]


def const_up(fr):
    """a short decimal >= fr"""
    if fr >= 10:
        return str(-((-fr.numerator) // fr.denominator))
    return dec_str(fr, 2, True)


def const_dn(fr):
    """a short decimal <= fr (fr > 0)"""
    for d in range(2, 12):
        st = dec_str(fr, d, False)
        if Fraction(st) > 0:
            return st
    raise ValueError(fr)


def lntau_bounds(mu_s, lam_s):
    from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
    getcontext().prec = 50
    lo = -(1 - Decimal(mu_s)).ln()
    hi = -(1 - Decimal(lam_s)).ln()
    q = Decimal('1e-10')
    a = lo.quantize(q, rounding=ROUND_FLOOR)
    b = hi.quantize(q, rounding=ROUND_CEILING)
    if lo - a < Decimal('1e-12'):
        a -= q
    if b - hi < Decimal('1e-12'):
        b += q
    return str(a), str(b), lo, hi


def main():
    kind = sys.argv[1]
    args = [int(a) for a in sys.argv[2:]]
    name = kind.capitalize() + ''.join(str(a) for a in args)
    lname = kind + ''.join(str(a) for a in args)
    F = '(%s %s)' % (kind, ' '.join(map(str, args)))
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
    has_sure = len(zeros) > 0
    Vup = [0] + [V[x] if V[x] > 0 else 1 for x in range(1, n)]
    Gs = [1 if (x in zeros) else 0 for x in range(n)]
    Vlo = list(V)
    up, lo = bounds(A, Nl, Dtot, Vup, Vlo)
    digits = 22
    Lup, Mup = dec_up(up, digits)
    Llo, Mlo = dec_dn(lo, digits)
    lam_s = dec_str(Fraction(Lup, Mup), 19, True)
    mu_s = dec_str(Fraction(Llo, Mlo), 19, False)
    vmax = max(Vup)
    wmax = max(Vlo)
    if has_sure:
        # kappa >= max_y (P 1_D)(y) / V(y)
        kap = max(Fraction(sum(Nl[y][z] for z in zeros), Dtot * Vup[y]) for y in range(1, n))
        Kg, Ng = (kap.numerator, kap.denominator) if kap > 0 else (0, 1)
        Kconst = Fraction(vmax, vmin) + Fraction(Kg, Ng) * vmax / Fraction(Lup, Mup)
        x0 = sum(1 << i for i in range(A) if i % 3 == 0)      # the cells of orientation x
        x0doc = 'the %d cells of orientation x alive' % bin(x0).count('1')
    else:
        Kg, Ng = 0, 1
        Kconst = Fraction(vmax, vmin)
        x0 = n - 1
        x0doc = 'the full face'
    wx = Vlo[x0]
    assert wx > 0
    K_s = const_up(Kconst)
    c_s = const_dn(Fraction(wx, wmax))
    a_s, b_s, lnlo, lnhi = lntau_bounds(mu_s, lam_s)
    print('# %s %s: A = %d, die-surely states %d, r = 0 states %d' % (kind, args, A, sum(sure), len(zeros)), file=sys.stderr)
    print('# lambda (float eig) %.16f; certified %s <= lambda <= %s' % (lam_float, mu_s, lam_s), file=sys.stderr)
    print('# ln tau in [%.15f, %.15f] (stated: %s < ln tau < %s; README %s)' % (
        lnlo, lnhi, a_s, b_s, README.get((kind, tuple(args)), '-')), file=sys.stderr)
    print('# K = %s, c(x0 = %d) = %s' % (K_s, x0, c_s), file=sys.stderr)
    out = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%sData.lean' % name)
    with open(out, 'w') as f:
        f.write('/-\nCertificate data for the face `%s %s` of the dice surrogate, written by\n'
                '`python3 research/blast/lean/dice_cert.py %s %s` (do not edit by hand).\n'
                'Checked in the kernel by `GumpMath/Dice%s.lean`; nothing here is trusted.\n-/\n'
                % (kind, ' '.join(map(str, args)), kind, ' '.join(map(str, args)), name))
        f.write('import GumpMath.DiceCert\n\nset_option maxRecDepth 100000\n\nnamespace Gump.Dice.%sData\nopen Gump.Dice\n\n' % name)
        f.write('/-- in-layer neighbour lists, in the order of `Face.nb` -/\n')
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
        if has_sure:
            f.write('/-- the indicator of the states that die surely -/\n')
            f.write('def Gs : Tree := %s\n\n' % tree(Gs))
            f.write('def Kg : ℕ := %d\ndef Ng : ℕ := %d\n\n' % (Kg, Ng))
        f.write('/-- lam_up = %d / %d -/\n' % (Lup, Mup))
        f.write('def Lup : ℕ := %d\ndef Mup : ℕ := %d\n' % (Lup, Mup))
        f.write('/-- mu_lo = %d / %d -/\n' % (Llo, Mlo))
        f.write('def Llo : ℕ := %d\ndef Mlo : ℕ := %d\n\n' % (Llo, Mlo))
        f.write('def vmin : ℕ := %d\ndef vmax : ℕ := %d\ndef wmax : ℕ := %d\ndef wx : ℕ := %d\n\n' % (
            vmin, vmax, wmax, wx))
        f.write('end Gump.Dice.%sData\n' % name)
    print('# wrote %s' % out, file=sys.stderr)
    thm = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%s.lean' % name)
    sub = dict(N=name, n=lname, F=F, kind=kind, args=' '.join(map(str, args)), A=A, lam=lam_s, mu=mu_s, K=K_s,
               c=c_s, a=a_s, b=b_s, x0=x0, x0doc=x0doc, readme=README.get((kind, tuple(args)), 'not tabulated'),
               h_lo=dec_str(1 - Fraction(lam_s), 19, False), h_hi=dec_str(1 - Fraction(mu_s), 19, True),
               k=max(1, int(float(b_s)) + 1), pk=') ^ %d' % max(1, int(float(b_s)) + 1))
    with open(thm, 'w') as f:
        f.write((TEMPLATE_SURE if has_sure else TEMPLATE) % sub)
    print('# wrote %s' % thm, file=sys.stderr)


HEAD = """/-
The lifetime of the %(A)d-cell face `%(F)s` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = %(readme)s). Written by `python3 research/blast/lean/dice_cert.py %(kind)s %(args)s`
with its certificate `GumpMath/Dice%(N)sData.lean`; every check is run by the kernel (`decide +kernel`).
  `%(n)s_lifetime`: survival from x₀ (%(x0doc)s) and from every state, for every t;
  `%(n)s_tau`: %(mu)s ≤ λ ≤ %(lam)s for every quasi-stationary law (μ, λ)%(lampos)s, so
  h = 1 - λ ∈ [%(h_lo)s, %(h_hi)s] and %(a)s < ln τ = -ln(1 - λ) < %(b)s.
-/
import GumpMath.Dice%(N)sData
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace %(N)sData

theorem tab : data.tabOK %(F)s = true := by decide +kernel

theorem up : Data.allRows (data.rowUp %(F)s.A (data.Dt %(F)s.A) Lup Mup Vup) (2 ^ %(F)s.A) = true := by
  decide +kernel

theorem lo : Data.allRows (data.rowLo %(F)s.A (data.Dt %(F)s.A) Llo Mlo Vlo) (2 ^ %(F)s.A) = true := by
  decide +kernel

theorem vl0 : Data.vecOK Vlo %(F)s.A 0 wmax = true := by decide +kernel
theorem vx : Vlo.get %(F)s.A %(x0)d = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]
"""

TAU = """
/-- **ln τ of the face `%(F)s`.** For every quasi-stationary law (μ, λ)%(lampos)s,
%(mu)s ≤ λ ≤ %(lam)s and τ = E_μ T = 1/(1 - λ) has %(a)s < ln τ < %(b)s. -/
theorem %(n)s_tau (μ : Fin (2 ^ %(F)s.A) → ℝ) (lam : ℝ) (hq : IsQSD %(F)s ρ1 ρ2 μ lam)%(lamhyp)s :
    (%(mu)s : ℝ) ≤ lam ∧ lam ≤ %(lam)s ∧
    %(a)s < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < %(b)s := by
  rw [hρ1, hρ2] at hq
%(qsd)s
  have l1 : (%(mu)s : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ %(lam)s := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ %(k)d (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    have hs : 0 ≤ expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    calc (1 - lam) * (expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15%(pk)s
        ≤ (1 - %(mu)s) * (expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15%(pk)s := by
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (%(b)s / %(k)d) 15 - expErr (%(b)s / %(k)d) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ %(k)d (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - %(lam)s) * (expSum (%(b)s / %(k)d) 15 - expErr (%(b)s / %(k)d) 15%(pk)s := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (%(b)s / %(k)d) 15 - expErr (%(b)s / %(k)d) 15%(pk)s := by
          gcongr

end Gump.Dice
"""

TEMPLATE = (HEAD + """theorem vu : Data.vecOK Vup %(F)s.A vmin vmax = true := by decide +kernel
theorem vl : Data.vecOK Vlo %(F)s.A vmin wmax = true := by decide +kernel

end %(N)sData
open %(N)sData

/-- **The lifetime of the face `%(F)s`, for every t.** Survival from the full face is at least
%(c)s · %(mu)s ^ t, and from every state at most %(K)s · %(lam)s ^ t. -/
theorem %(n)s_lifetime (t : ℕ) :
    (%(c)s : ℚ) * %(mu)s ^ t ≤ %(F)s.survival ρ1 ρ2 t %(F)s.full ∧
    ∀ x, %(F)s.survival ρ1 ρ2 t x ≤ %(K)s * %(lam)s ^ t := by
  rw [hρ1, hρ2]
  obtain ⟨hl, hu⟩ := data.lifetime_of_cert %(F)s Vup Vlo Lup Mup Llo Mlo vmin vmax wmax tab up lo vu vl0
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [wmax]) t
  constructor
  · refine le_trans ?_ (hl %(F)s.full)
    rw [Data.vec, show ((%(F)s.full : Fin _) : ℕ) = %(x0)d from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (hu x) ?_
    gcongr
    · norm_num [vmax, vmin]
    · norm_num [Lup, Mup]
""" + TAU.replace('%(qsd)s', """  obtain ⟨h1, h2⟩ := data.qsd_bounds %(F)s Vup Vlo Lup Mup Llo Mlo vmin vmax vmin wmax tab up lo vu vl
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [vmin]) μ lam hq""")).replace(
    '%(lampos)s', '').replace('%(lamhyp)s', '')

TEMPLATE_SURE = (HEAD + """theorem gs : Data.allRows (data.rowLe %(F)s.A (data.Dt %(F)s.A) Kg Ng Gs Vup) (2 ^ %(F)s.A) = true := by
  decide +kernel
theorem v2 : Data.vecOK2 Vup Gs %(F)s.A vmin vmax = true := by decide +kernel
theorem vu1 : Data.vecOK Vup %(F)s.A 1 vmax = true := by decide +kernel
theorem sure : data.sureOK Vlo %(F)s.A = true := by decide +kernel

end %(N)sData
open %(N)sData

/-- **The lifetime of the face `%(F)s`, for every t.** Survival from x₀ = %(x0)d (%(x0doc)s) is at least
%(c)s · %(mu)s ^ t; from every state, survival to t + 1 is at most %(K)s · %(lam)s ^ (t + 1).
(The full face dies surely in one generation: every cell has k = 6, or is overcrowded.) -/
theorem %(n)s_lifetime (t : ℕ) :
    (%(c)s : ℚ) * %(mu)s ^ t ≤ %(F)s.survival ρ1 ρ2 t ⟨%(x0)d, by decide⟩ ∧
    ∀ x, %(F)s.survival ρ1 ρ2 (t + 1) x ≤ %(K)s * %(lam)s ^ (t + 1) := by
  rw [hρ1, hρ2]
  constructor
  · refine le_trans ?_ (data.survival_lo %(F)s Vlo Llo Mlo wmax tab lo vl0 (by norm_num [Mlo]) (by norm_num [wmax]) t _)
    rw [Data.vec, show ((⟨%(x0)d, by decide⟩ : Fin (2 ^ %(F)s.A)) : ℕ) = %(x0)d from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (data.survival_up_sure %(F)s Vup Gs Lup Mup Kg Ng vmin vmax tab up gs v2 (by norm_num [Mup])
      (by norm_num [Ng]) (by norm_num [vmin]) (by norm_num [Lup]) t x) ?_
    gcongr
    · norm_num [vmax, vmin, Kg, Ng, Lup, Mup]
    · norm_num [Lup, Mup]
""" + TAU.replace('%(qsd)s', """  have h1 := data.qsd_lo_sure %(F)s Vlo Llo Mlo wmax tab lo vl0 sure (by norm_num [Mlo]) μ lam hq hlam
  have h2 := data.qsd_up %(F)s Vup Lup Mup 1 vmax tab up vu1 (by norm_num [Mup]) (by norm_num) μ lam hq""")).replace(
    '%(lampos)s', ' with λ > 0').replace('%(lamhyp)s', ' (hlam : 0 < lam)')


if __name__ == '__main__':
    main()
