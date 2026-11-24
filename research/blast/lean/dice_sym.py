#!/usr/bin/env python3
"""Lifetime certificates for 12-cell faces of the dice surrogate, with the row checks run on orbit representatives.

Like dice_cert.py, but: the automorphisms of the face's tables (cell permutations preserving neighbour multisets and
coins) are enumerated; the certificate vectors are made exactly invariant (constant on orbits); the kernel checks
the rows (P v)(x) vs lambda v(x) only at one state per orbit, and `GumpMath/DiceSym.lean` (`rows_of_reps`) carries
them to every state (P(sx, sy) = P(x, y)). The eigenvector is a float one (numpy), so the bounds are ~1e-13 wide.

    python3 research/blast/lean/dice_sym.py torus 2 0 2     # -> GumpMath/DiceTorus202Data.lean, DiceTorus202.lean
"""
import sys, os
from fractions import Fraction
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dice_cert as dc  # noqa: E402


def automorphisms(nb, m):
    A = len(nb)
    res = []

    def ok_partial(s):
        for i, j in s.items():
            if m[i] != m[j] or len(nb[i]) != len(nb[j]):
                return False
            for a in nb[i]:
                if a in s and s[a] not in nb[j]:
                    return False
        return True

    def rec(s, used):
        if len(s) == A:
            if all(Counter(s[a] for a in nb[i]) == Counter(nb[s[i]]) for i in range(A)):
                res.append([s[i] for i in range(A)])
            return
        i = len(s)
        for j in range(A):
            if j in used:
                continue
            s[i] = j
            if ok_partial(s):
                rec(s, used | {j})
            del s[i]
    rec({}, frozenset())
    return res


def act(g, x):
    return sum(1 << g[i] for i in range(len(g)) if (x >> i) & 1)


def row_numerators(A, nb, Dc, T, x):
    al = dc.alphas(A, nb, T, x)
    n = 1 << A
    row = np.ones(n, dtype=object)
    ys = np.arange(n)
    for i in range(A):
        bit = (ys >> i) & 1
        row = row * np.where(bit == 1, al[i], Dc[i] - al[i]).astype(object)
    return row


def main():
    kind = sys.argv[1]
    args = [int(a) for a in sys.argv[2:]]
    name = kind.capitalize() + ''.join(str(a) for a in args)
    lname = kind + ''.join(str(a) for a in args)
    F = '(%s %s)' % (kind, ' '.join(map(str, args)))
    A, nb, m = dc.face(kind, args)
    Dc, T = dc.tables(A, nb, m)
    Dt = 1
    for d in Dc:
        Dt *= d
    n = 1 << A
    G = automorphisms(nb, m)
    # orbits
    rep = [-1] * n
    wit = [None] * n
    reps = []
    for x in range(n):
        if rep[x] >= 0:
            continue
        reps.append(x)
        for gi, g in enumerate(G):
            y = act(g, x)
            if rep[y] < 0:
                rep[y] = x
                wit[y] = gi
    print('# %s: A = %d, |Aut| = %d, %d orbits' % (F, A, len(G), len(reps)), file=sys.stderr)
    # float killed matrix and Perron vector (right)
    al = np.array([dc.alphas(A, nb, T, x) for x in range(n)], dtype=float)   # n x A
    Dcf = np.array(Dc, dtype=float)
    pa = al / Dcf
    ys = np.arange(n)
    Q = np.ones((n, n))
    for i in range(A):
        bit = ((ys >> i) & 1)[None, :]
        Q *= np.where(bit == 1, pa[:, i][:, None], 1 - pa[:, i][:, None])
    Qk = Q[1:, 1:]
    v = np.ones(n - 1)
    for _ in range(3000):
        w = Qk @ v
        lam = w.max() / v.max()
        v = w / w.max()
    r = np.concatenate([[0.0], v])
    # symmetrize: constant on orbits
    orb_mean = {}
    for x in range(n):
        orb_mean.setdefault(rep[x], []).append(r[x])
    rs = np.array([np.mean(orb_mean[rep[x]]) for x in range(n)])
    zeros = [x for x in range(1, n) if rs[x] < 1e-300]
    sure = [x for x in range(1, n) if all(a == 0 for a in dc.alphas(A, nb, T, x))]
    assert set(zeros) <= set(sure), 'r = 0 on a state that does not die surely'
    S = 2**64
    V = [0] + [int(round(rs[x] * S)) for x in range(1, n)]
    vmin = min(V[x] for x in range(1, n) if V[x] > 0)
    Vup = [0] + [V[x] if V[x] > 0 else 1 for x in range(1, n)]
    Vlo = list(V)
    Gs = [1 if x in zeros else 0 for x in range(n)]
    up, lo, kap = Fraction(0), None, Fraction(0)
    for x in reps:
        if x == 0:
            continue
        row = row_numerators(A, nb, Dc, T, x)
        nu = int(np.dot(row, np.array(Vup, dtype=object)))
        up = max(up, Fraction(nu, Dt * Vup[x]))
        if Vlo[x] > 0:
            nl = int(np.dot(row, np.array(Vlo, dtype=object)))
            f = Fraction(nl, Dt * Vlo[x])
            lo = f if lo is None else min(lo, f)
        if zeros:
            ng = int(np.dot(row, np.array(Gs, dtype=object)))
            kap = max(kap, Fraction(ng, Dt * Vup[x]))
    Lup, Mup = dc.dec_up(up, 22)
    Llo, Mlo = dc.dec_dn(lo, 22)
    lam_s = dc.dec_str(Fraction(Lup, Mup), 16, True)
    mu_s = dc.dec_str(Fraction(Llo, Mlo), 16, False)
    vmax = max(Vup)
    wmax = max(Vlo)
    Kg, Ng = (kap.numerator, kap.denominator) if kap > 0 else (0, 1)
    if zeros:
        Kconst = Fraction(vmax, vmin) + Fraction(Kg, Ng) * vmax / Fraction(Lup, Mup)
        x0 = sum(1 << i for i in range(A) if i % 3 == 0)
        x0doc = 'the %d cells of orientation x alive' % bin(x0).count('1')
    else:
        Kconst = Fraction(vmax, vmin)
        x0 = n - 1
        x0doc = 'the full face'
    wx = Vlo[x0]
    K_s = dc.const_up(Kconst)
    c_s = dc.const_dn(Fraction(wx, wmax))
    a_s, b_s, lnlo, lnhi = dc.lntau_bounds(mu_s, lam_s)
    print('# lambda (power iteration) %.16f; certified %s <= lambda <= %s' % (lam, mu_s, lam_s), file=sys.stderr)
    print('# ln tau in [%.13f, %.13f] (stated %s < ln tau < %s); K = %s, c = %s' % (lnlo, lnhi, a_s, b_s, K_s, c_s),
          file=sys.stderr)
    Rm = [1 if rep[x] == x else 0 for x in range(n)]
    Wr = [rep[x] for x in range(n)]
    Wg = [wit[x] for x in range(n)]
    out = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%sData.lean' % name)
    with open(out, 'w') as f:
        f.write('/-\nCertificate data for the face `%s` of the dice surrogate (rows checked on orbit representatives),\n'
                'written by `python3 research/blast/lean/dice_sym.py %s %s` (do not edit by hand). Nothing here is trusted.\n-/\n'
                % (F, kind, ' '.join(map(str, args))))
        f.write('import GumpMath.DiceSym\n\nset_option maxRecDepth 100000\n\nnamespace Gump.Dice.%sData\nopen Gump.Dice Gump.Dice.Data\n\n' % name)
        f.write('def G : List (List ℕ) := %s\n\n' % ('[' + ', '.join('[' + ', '.join(map(str, l)) + ']' for l in nb) + ']'))
        f.write('def C : List (ℕ × ℕ) := %s\n\n' % ('[' + ', '.join('(%d, %d)' % mm for mm in m) + ']'))
        f.write('def T : List (List ℕ) := %s\n\n' % ('[' + ', '.join('[' + ', '.join(map(str, l)) + ']' for l in T) + ']'))
        f.write('def data : Data := ⟨%d, %d, %d, %d, G, C, T⟩\n\n' % (dc.N1, dc.D1, dc.N2, dc.D2))
        f.write('/-- the %d automorphisms of the tables, with their actions on states -/\n' % len(G))
        f.write('def gens : List (List ℕ × Tree) := [%s]\n\n' % ', '.join(
            '([%s], Tree.build %d (act [%s]) 0)' % (', '.join(map(str, g)), A, ', '.join(map(str, g))) for g in G))
        f.write('def Vup : Tree := %s\n\n' % dc.tree(Vup))
        f.write('def Vlo : Tree := %s\n\n' % dc.tree(Vlo))
        f.write('def Gs : Tree := %s\n\n' % dc.tree(Gs))
        f.write('def Rm : Tree := %s\n\n' % dc.tree(Rm))
        f.write('def Wr : Tree := %s\n\n' % dc.tree(Wr))
        f.write('def Wg : Tree := %s\n\n' % dc.tree(Wg))
        f.write('def Kg : ℕ := %d\ndef Ng : ℕ := %d\n' % (Kg, Ng))
        f.write('def Lup : ℕ := %d\ndef Mup : ℕ := %d\ndef Llo : ℕ := %d\ndef Mlo : ℕ := %d\n' % (Lup, Mup, Llo, Mlo))
        f.write('def vmin : ℕ := %d\ndef vmax : ℕ := %d\ndef wmax : ℕ := %d\ndef wx : ℕ := %d\n\n' % (vmin, vmax, wmax, wx))
        f.write('end Gump.Dice.%sData\n' % name)
    print('# wrote %s' % out, file=sys.stderr)
    sub = dict(N=name, n=lname, F=F, A=A, lam=lam_s, mu=mu_s, K=K_s, c=c_s, a=a_s, b=b_s, x0=x0, x0doc=x0doc,
               ng=len(G), nreps=len(reps), readme=dc.README.get((kind, tuple(args)), 'see the table'),
               k=max(1, int(float(b_s)) + 1), h_lo=dc.dec_str(1 - Fraction(lam_s), 16, False),
               h_hi=dc.dec_str(1 - Fraction(mu_s), 16, True))
    sub['pk'] = ') ^ %d' % sub['k']
    thm = os.path.join(HERE, 'mathlib', 'GumpMath', 'Dice%s.lean' % name)
    with open(thm, 'w') as f:
        f.write(TEMPLATE % sub)
    print('# wrote %s' % thm, file=sys.stderr)


TEMPLATE = """/-
The lifetime of the %(A)d-cell face `%(F)s` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = %(readme)s). Written by `python3 research/blast/lean/dice_sym.py`; the row checks
run on the %(nreps)d orbit representatives of the %(ng)d table automorphisms (`GumpMath/DiceSym.lean`), every check in the kernel.
  `%(n)s_lifetime`: survival from x₀ (%(x0doc)s) and from every state, for every t;
  `%(n)s_tau`: %(mu)s ≤ λ ≤ %(lam)s for every quasi-stationary law (μ, λ) with λ > 0, so
  h = 1 - λ ∈ [%(h_lo)s, %(h_hi)s] and %(a)s < ln τ = -ln(1 - λ) < %(b)s.
-/
import GumpMath.Dice%(N)sData
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace %(N)sData
open Data

theorem tab : data.tabOK %(F)s = true := by decide +kernel
theorem syms : gens.all (fun g => data.symOK %(F)s.A g.1 g.2) = true := by decide +kernel
theorem invs : gens.all (fun g => invOK %(F)s.A g.2 Vup && invOK %(F)s.A g.2 Vlo && invOK %(F)s.A g.2 Gs) = true := by
  decide +kernel
theorem reps : repsOK %(F)s.A gens Wg Wr Rm = true := by decide +kernel
theorem up : marked %(F)s.A Rm (data.rowLe %(F)s.A (data.Dt %(F)s.A) Lup Mup Vup Vup) = true := by decide +kernel
theorem gs : marked %(F)s.A Rm (data.rowLe %(F)s.A (data.Dt %(F)s.A) Kg Ng Gs Vup) = true := by decide +kernel
theorem lo : marked %(F)s.A Rm (data.rowLo %(F)s.A (data.Dt %(F)s.A) Llo Mlo Vlo) = true := by decide +kernel
theorem v2 : Data.vecOK2 Vup Gs %(F)s.A vmin vmax = true := by decide +kernel
theorem vu1 : Data.vecOK Vup %(F)s.A 1 vmax = true := by decide +kernel
theorem vl0 : Data.vecOK Vlo %(F)s.A 0 wmax = true := by decide +kernel
theorem sure : data.sureOK Vlo %(F)s.A = true := by decide +kernel
theorem vx : Vlo.get %(F)s.A %(x0)d = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]

theorem hsym : ∀ g ∈ gens, data.symOK %(F)s.A g.1 g.2 = true := by
  have := syms; rw [List.all_eq_true] at this; exact this
theorem hinv : ∀ g ∈ gens, invOK %(F)s.A g.2 Vup = true ∧ invOK %(F)s.A g.2 Vlo = true ∧ invOK %(F)s.A g.2 Gs = true := by
  have := invs; rw [List.all_eq_true] at this
  intro g hg; have := this g hg; simp only [Bool.and_eq_true] at this; exact ⟨this.1.1, this.1.2, this.2⟩

theorem iup : ∀ x, (%(F)s.P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Vup %(F)s.A) x ≤ ((Lup : ℚ) / Mup) * vec Vup %(F)s.A x :=
  data.ineq_up_of_reps %(F)s tab gens Wg Wr Rm hsym Vup Vup (fun g hg => (hinv g hg).1)
  (fun g hg => (hinv g hg).1) reps Lup Mup (by norm_num [Mup]) up
theorem igs : ∀ x, (%(F)s.P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Gs %(F)s.A) x ≤ ((Kg : ℚ) / Ng) * vec Vup %(F)s.A x :=
  data.ineq_up_of_reps %(F)s tab gens Wg Wr Rm hsym Gs Vup (fun g hg => (hinv g hg).2.2)
  (fun g hg => (hinv g hg).1) reps Kg Ng (by norm_num [Ng]) gs
theorem ilo : ∀ x, ((Llo : ℚ) / Mlo) * vec Vlo %(F)s.A x ≤ (%(F)s.P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Vlo %(F)s.A) x :=
  data.ineq_lo_of_reps %(F)s tab gens Wg Wr Rm hsym Vlo (fun g hg => (hinv g hg).2.1) reps Llo Mlo
  (by norm_num [Mlo]) lo

end %(N)sData
open %(N)sData

/-- **The lifetime of the face `%(F)s`, for every t.** Survival from x₀ = %(x0)d (%(x0doc)s) is at least
%(c)s · %(mu)s ^ t; from every state, survival to t + 1 is at most %(K)s · %(lam)s ^ (t + 1). -/
theorem %(n)s_lifetime (t : ℕ) :
    (%(c)s : ℚ) * %(mu)s ^ t ≤ %(F)s.survival ρ1 ρ2 t ⟨%(x0)d, by decide⟩ ∧
    ∀ x, %(F)s.survival ρ1 ρ2 (t + 1) x ≤ %(K)s * %(lam)s ^ (t + 1) := by
  rw [hρ1, hρ2]
  constructor
  · refine le_trans ?_ (data.survival_lo_ineq %(F)s Vlo Llo Mlo wmax tab ilo vl0 (by norm_num [Mlo]) (by norm_num [wmax]) t _)
    rw [Data.vec, show ((⟨%(x0)d, by decide⟩ : Fin (2 ^ %(F)s.A)) : ℕ) = %(x0)d from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (data.survival_up_sure_ineq %(F)s Vup Gs Lup Mup Kg Ng vmin vmax tab iup igs v2 (by norm_num [Mup])
      (by norm_num [Ng]) (by norm_num [vmin]) (by norm_num [Lup]) t x) ?_
    gcongr
    · norm_num [vmax, vmin, Kg, Ng, Lup, Mup]
    · norm_num [Lup, Mup]

/-- **ln τ of the face `%(F)s`.** For every quasi-stationary law (μ, λ) with λ > 0,
%(mu)s ≤ λ ≤ %(lam)s and %(a)s < ln τ < %(b)s. -/
theorem %(n)s_tau (μ : Fin (2 ^ %(F)s.A) → ℝ) (lam : ℝ) (hq : IsQSD %(F)s ρ1 ρ2 μ lam) (hlam : 0 < lam) :
    (%(mu)s : ℝ) ≤ lam ∧ lam ≤ %(lam)s ∧
    %(a)s < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < %(b)s := by
  rw [hρ1, hρ2] at hq
  have h1 := data.qsd_lo_sure_ineq %(F)s Vlo Llo Mlo wmax tab ilo vl0 sure (by norm_num [Mlo]) μ lam hq hlam
  have h2 := data.qsd_up_ineq %(F)s Vup Lup Mup 1 vmax tab iup vu1 (by norm_num [Mup]) (by norm_num) μ lam hq
  have l1 : (%(mu)s : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ %(lam)s := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ %(k)d (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    calc (1 - lam) * (expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15%(pk)s
        ≤ (1 - %(mu)s) * (expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15%(pk)s := by
          have hs : 0 ≤ expSum (%(a)s / %(k)d) 15 + expErr (%(a)s / %(k)d) 15 := by
            simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
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


if __name__ == '__main__':
    main()
