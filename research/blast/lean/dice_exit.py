#!/usr/bin/env python3
"""Certificates for the two exits (bust and fade) of a small face of the dice surrogate, checked in Lean.

The bust, as rigour/qsd.c defines it ("halffall_share"): a death whose last K transitions (the death itself
included) contain a fall of at least half = ceil(A/2) cells in one generation. With
    N_0(v) = [v = empty],   N_k(u) = [u != empty] sum_v P(u, v) [pop u - pop v < half] N_{k-1}(v),
N_K(x) = P_x(T = K and no fall >= half in the K transitions), and for a quasi-stationary law (mu, lambda) the
bust share is  1 - mu.N_K / (lambda^(K-1) h),  h = 1 - lambda = mu.d  (d(x) = P(x, empty)).

This script computes D^k N_k exactly (integers; D the common denominator of P), and a Poisson certificate:
p (a rational near q = mu.N_K / mu.d), w (an integer vector over a scale S) with
    res = N_K - p d - (lam' w - P w),   |res| <= eps d,   |w| <= omega d   entrywise,
so that for every quasi-stationary law with lambda in [mu_lo, lam_up], |q - p| <= eps + (lam_up - mu_lo) omega
(mu.(P w) = lambda mu.w).  It writes GumpMath/Dice<Name>ExitData.lean.

    python3 research/blast/lean/dice_exit.py torus 1 1 3 [K=6]
"""
import sys, os
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dice_cert as dc  # noqa: E402


def main():
    kind = sys.argv[1]
    args = [int(a) for a in sys.argv[2:5] if a.isdigit()] if kind == 'torus' else [int(a) for a in sys.argv[2:3]] if kind == 'hull' else [int(a) for a in sys.argv[2:4]]
    rest = sys.argv[2 + len(args):]
    K = int(rest[0]) if rest else 6
    name = kind.capitalize() + ''.join(str(a) for a in args)
    A, nb, m = dc.face(kind, args)
    Dc, T = dc.tables(A, nb, m)
    Dt = 1
    for d in Dc:
        Dt *= d
    Nm = dc.numerators(A, nb, Dc, T)
    n = 1 << A
    half = (A + 1) // 2
    pop = [bin(x).count('1') for x in range(n)]
    Nl = [list(Nm[x]) for x in range(n)]
    # exact N_k scaled by Dt^k
    Nt = [[1 if v == 0 else 0 for v in range(n)]]
    for k in range(1, K + 1):
        prev = Nt[-1]
        cur = [0] * n
        for u in range(1, n):
            row = Nl[u]
            cur[u] = sum(row[v] * prev[v] for v in range(n) if pop[u] - pop[v] < half)
        Nt.append(cur)
    # float quantities
    Q = np.array(Nm[1:, 1:], dtype=float) / float(Dt)
    w_, vl = np.linalg.eig(Q.T)
    j = int(np.argmax(w_.real))
    lam = w_[j].real
    mu = np.abs(vl[:, j].real); mu /= mu.sum()
    dvec = np.array([float(Fraction(Nl[x][0], Dt)) for x in range(1, n)])
    NK = np.array([float(Fraction(Nt[K][x], Dt**K)) for x in range(1, n)])
    h = float(mu @ dvec)
    q = float(mu @ NK) / h
    share = 1 - q / lam**(K - 1)
    print('# %s %s K=%d: lambda %.15f, h %.15e (1-lambda %.15e), q = mu.N_K/mu.d %.12f, bust share %.10f' % (
        kind, args, K, lam, h, 1 - lam, q, share), file=sys.stderr)
    # Poisson: (lam I - Q) w = N_K - q d, with mu.w = 0 (least squares on the augmented system)
    rhs = NK - q * dvec
    M = np.vstack([lam * np.eye(n - 1) - Q, mu[None, :]])
    b = np.concatenate([rhs, [0.0]])
    w, *_ = np.linalg.lstsq(M, b, rcond=None)
    S = 2**64
    W = [0] + [int(round(x * S)) for x in w]
    # exact residual with p = q rounded, lam' = the certified upper bound of dice_cert (recomputed here)
    pfr = Fraction(q).limit_denominator(10**18)
    # certified lambda bounds: rerun the eigen-certificate
    V, _, _, _ = dc.perron(A, Nm, Dt)
    zeros = [x for x in range(1, n) if V[x] == 0]
    Vup = [0] + [V[x] if V[x] > 0 else 1 for x in range(1, n)]
    up, lo = dc.bounds(A, Nl, Dt, Vup, V)
    Lup, Mup = dc.dec_up(up, 22)
    Llo, Mlo = dc.dec_dn(lo, 22)
    lamq = Fraction(Lup, Mup)
    eps = Fraction(0)
    om = Fraction(0)
    for x in range(1, n):
        PW = Fraction(sum(Nl[x][y] * W[y] for y in range(n)), Dt * S)
        dx = Fraction(Nl[x][0], Dt)
        res = Fraction(Nt[K][x], Dt**K) - pfr * dx - (lamq * Fraction(W[x], S) - PW)
        eps = max(eps, abs(res) / dx)
        om = max(om, abs(Fraction(W[x], S)) / dx)
    gap = Fraction(Lup, Mup) - Fraction(Llo, Mlo)
    eta = eps + gap * om
    print('# p = %.15f, eps = %.3e, omega = %.3e, lambda gap %.1e: |q - p| <= %.3e' % (
        float(pfr), float(eps), float(om), float(gap), float(eta)), file=sys.stderr)
    # the decimals stated for lambda by dice_cert (same rounding)
    lam_s = dc.dec_str(Fraction(Lup, Mup), 19, True)
    mu_s = dc.dec_str(Fraction(Llo, Mlo), 19, False)
    epsq = dc_up_short(eps)
    omq = dc_up_short(om)
    eta = epsq + (Fraction(lam_s) - Fraction(mu_s)) * omq
    slo = 1 - (pfr + eta) / Fraction(mu_s)**(K - 1)
    shi = 1 - (pfr - eta) / Fraction(lam_s)**(K - 1)
    print('# bust share in [%.12f, %.12f]' % (float(slo), float(shi)), file=sys.stderr)
    a_s = dc.dec_str(slo, 6, False)
    b_s = dc.dec_str(shi, 6, True)
    if Fraction(a_s) == slo:
        a_s = dc.dec_str(slo - Fraction(1, 10**6), 6, False)
    if Fraction(b_s) == shi:
        b_s = dc.dec_str(shi + Fraction(1, 10**6), 6, True)
    Wp = [max(x, 0) for x in W]
    Wm = [max(-x, 0) for x in W]
    out = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%sExitData.lean' % name)
    with open(out, 'w') as f:
        f.write('/-\nExit certificate data for the face `%s %s`, K = %d, written by\n'
                '`python3 research/blast/lean/dice_exit.py %s %s %d` (do not edit by hand).\n'
                'Checked in the kernel by `GumpMath/Dice%sExit.lean`; nothing here is trusted.\n-/\n'
                % (kind, ' '.join(map(str, args)), K, kind, ' '.join(map(str, args)), K, name))
        f.write('import GumpMath.Dice%sData\nimport GumpMath.DiceExit\n\nset_option maxRecDepth 100000\n\n'
                'namespace Gump.Dice.%sExitData\nopen Gump.Dice\n\n' % (name, name))
        for k in range(K + 1):
            f.write('/-- D^%d noBust %d -/\ndef N%d : Tree := %s\n\n' % (k, k, k, dc.tree(Nt[k])))
        f.write('def Wp : Tree := %s\n\ndef Wm : Tree := %s\n\n' % (dc.tree(Wp), dc.tree(Wm)))
        f.write('def S : ℕ := %d\n' % S)
        f.write('def p : ℚ := %d / %d\n' % (pfr.numerator, pfr.denominator))
        f.write('def eps : ℚ := %d / %d\n' % (epsq.numerator, epsq.denominator))
        f.write('def om : ℚ := %d / %d\n\n' % (omq.numerator, omq.denominator))
        f.write('end Gump.Dice.%sExitData\n' % name)
    print('# wrote %s' % out, file=sys.stderr)
    F = '(%s %s)' % (kind, ' '.join(map(str, args)))
    lname = kind + ''.join(str(a) for a in args)
    steps = ''.join('theorem n%d : Data.allRows (data.nbRow %s.A %s.half N%d N%d) (2 ^ %s.A) = true := by\n  decide +kernel\n'
                    % (k, F, F, k, k - 1, F) for k in range(1, K + 1))
    reps = ''.join('  have r%d := data.nbRow_spec %s tab N%d N%d %d n%d r%d\n' % (k, F, k, k - 1, k - 1, k, k - 1)
                   for k in range(1, K + 1))
    has_sure = len(zeros) > 0
    thm = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%sExit.lean' % name)
    sub = dict(N=name, n=lname, F=F, K=K, a=a_s, b=b_s, lam=lam_s, mu=mu_s, steps=steps, reps=reps,
               share=README_SHARE.get((kind, tuple(args)), '-'),
               lamhyp=' (hlam : 0 < lam)' if has_sure else '', lamarg=' hlam' if has_sure else '',
               exit='bust' if Fraction(a_s) > Fraction(1, 2) else 'fade',
               lampos=' with λ > 0' if has_sure else '')
    with open(thm, 'w') as f:
        f.write(EXIT_TEMPLATE % sub)
    print('# wrote %s' % thm, file=sys.stderr)


README_SHARE = {('torus', (1, 1, 3)): '0.9369', ('hull', (3,)): '0.0170'}


def dc_up_short(x):
    """a rational >= x with a short decimal form (2 significant digits)"""
    if x == 0:
        return Fraction(0)
    e = 0
    while Fraction(10)**e * x < 10:
        e += 1
    while Fraction(10)**e * x >= 100:
        e -= 1
    q = Fraction(10)**e * x
    return Fraction(-((-q.numerator) // q.denominator)) / Fraction(10)**e


EXIT_TEMPLATE = """/-
**Both exits, proved at 9 cells**: the share of the quasi-stationary death flux of the face `%(F)s` through the
bust (a fall of at least half the face, ⌈A/2⌉ cells, in one generation among the last %(K)d transitions; `qsd.c`
`halffall_share K=%(K)d`, `rigour/README.md` claim 4: %(share)s) lies in (%(a)s, %(b)s): this face dies mostly by
the %(exit)s. Written by `python3 research/blast/lean/dice_exit.py`; every check is run by the kernel.
-/
import GumpMath.Dice%(N)sExitData
import GumpMath.Dice%(N)s

set_option maxRecDepth 100000

namespace Gump.Dice
namespace %(N)sExitData
open %(N)sData

theorem base : Data.nbBase %(F)s.A N0 = true := by decide +kernel
%(steps)stheorem pois : Data.allRows (data.poisRow %(F)s.A (data.Dt %(F)s.A) %(K)d N%(K)d Wp Wm S p ((Lup : ℚ) / Mup) eps om)
    (2 ^ %(F)s.A) = true := by
  decide +kernel
theorem w0 : Wp.get %(F)s.A 0 = 0 ∧ Wm.get %(F)s.A 0 = 0 := by decide +kernel

end %(N)sExitData
open %(N)sData %(N)sExitData

/-- **The bust share of the face `%(F)s`** (K = %(K)d): for every quasi-stationary law (μ, λ)%(lampos)s,
%(a)s < bustShare < %(b)s. -/
theorem %(n)s_bust (μ : Fin (2 ^ %(F)s.A) → ℝ) (lam : ℝ) (hq : IsQSD %(F)s ρ1 ρ2 μ lam)%(lamhyp)s :
    %(a)s < %(F)s.bustShare ρ1 ρ2 %(K)d μ lam ∧ %(F)s.bustShare ρ1 ρ2 %(K)d μ lam < %(b)s := by
  obtain ⟨l1, l2, -, -⟩ := %(n)s_tau μ lam hq%(lamarg)s
  rw [hρ1, hρ2] at hq
  have r0 : ∀ v : Fin (2 ^ %(F)s.A), (N0.get %(F)s.A v : ℚ) =
      (data.Dt %(F)s.A : ℚ) ^ 0 * %(F)s.noBust ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) 0 v :=
    data.nbBase_spec %(F)s.A N0 base _ _ %(F)s rfl
%(reps)s  have hb := data.poisson_bound %(F)s tab %(K)d N%(K)d Wp Wm S (by norm_num [S]) p ((Lup : ℚ) / Mup) eps om pois w0
    r%(K)d μ lam hq
  have hl' : |(((Lup : ℚ) / Mup : ℚ) : ℝ) - lam| ≤ (%(lam)s : ℝ) - %(mu)s := by
    have h1 : (((Lup : ℚ) / Mup : ℚ) : ℝ) ≤ %(lam)s := by norm_num [Lup, Mup]
    have h2 : (%(mu)s : ℝ) ≤ (((Lup : ℚ) / Mup : ℚ) : ℝ) := by norm_num [Lup, Mup]
    rw [abs_le]; constructor <;> linarith
  have hb' : |∑ x, μ x * (%(F)s.noBust ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) %(K)d x : ℝ) -
      (p : ℝ) * (1 - lam)| ≤ ((eps : ℝ) + ((%(lam)s : ℝ) - %(mu)s) * om) * (1 - lam) := by
    refine hb.trans (mul_le_mul_of_nonneg_right ?_ (by linarith))
    have : (0 : ℝ) ≤ (om : ℝ) := by norm_num [om]
    nlinarith
  have := share_interval _ lam p ((eps : ℝ) + ((%(lam)s : ℝ) - %(mu)s) * om) %(mu)s %(lam)s %(K)d
    (by norm_num) l1 l2 (by linarith) (by norm_num [p, eps, om]) hb'
  rw [← hρ1, ← hρ2] at this
  unfold Face.bustShare
  constructor
  · refine lt_of_lt_of_le ?_ this.1
    norm_num [p, eps, om]
  · refine lt_of_le_of_lt this.2 ?_
    norm_num [p, eps, om]

end Gump.Dice
"""


if __name__ == '__main__':
    main()
