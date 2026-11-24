/-
**The first theorem in the repository about a lifetime**: the 9-cell hull triangle (R = 3) of the one-layer
dice surrogate at (ρ1, ρ2) = (0.44, 0.42), `rigour/README.md` claim 3, "triangle R=3: 2.4837157463".

`hull3_lifetime`: for every t, from the full face and from every state,
    0.72 · 0.9165673655948901373 ^ t ≤ P_full(T > t),     P_x(T > t) ≤ 1384 · 0.9165673655948901374 ^ t.
`hull3_tau`: every quasi-stationary law (μ, λ) has 0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374, so
h = 1 - λ = 0.08343263440510986(26..27) (dense.py: 8.3432634405110e-02, qsd.c: 8.3432634405108e-02) and
    2.4837157463 < ln τ = -ln(1 - λ) < 2.4837157464.
The certificate (two integer vectors on the 512 states) was found by `dice_cert.py hull 3`; the kernel checks
it row by row (`decide +kernel`, no other trust).
-/
import GumpMath.DiceHull3Data
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace Hull3Data

theorem tab : data.tabOK (hull 3) = true := by decide +kernel

theorem up : Data.allRows (data.rowUp (hull 3).A (data.Dt (hull 3).A) Lup Mup Vup) (2 ^ (hull 3).A) = true := by
  decide +kernel

theorem lo : Data.allRows (data.rowLo (hull 3).A (data.Dt (hull 3).A) Llo Mlo Vlo) (2 ^ (hull 3).A) = true := by
  decide +kernel

theorem vu : Data.vecOK Vup (hull 3).A vmin vmax = true := by decide +kernel
theorem vl : Data.vecOK Vlo (hull 3).A vmin wmax = true := by decide +kernel
theorem vl0 : Data.vecOK Vlo (hull 3).A 0 wmax = true := by decide +kernel
theorem vfull : Vlo.get (hull 3).A (hull 3).full = wfull := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]

end Hull3Data
open Hull3Data

/-- **The lifetime of the 9-cell hull triangle, for every t.** Survival from the full face is at least
0.72 · 0.9165673655948901373 ^ t, and from every state at most 1384 · 0.9165673655948901374 ^ t. -/
theorem hull3_lifetime (t : ℕ) :
    (0.72 : ℚ) * 0.9165673655948901373 ^ t ≤ (hull 3).survival ρ1 ρ2 t (hull 3).full ∧
    ∀ x, (hull 3).survival ρ1 ρ2 t x ≤ 1384 * 0.9165673655948901374 ^ t := by
  rw [hρ1, hρ2]
  obtain ⟨hl, hu⟩ := data.lifetime_of_cert (hull 3) Vup Vlo Lup Mup Llo Mlo vmin vmax wmax tab up lo vu vl0
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [wmax]) t
  constructor
  · refine le_trans ?_ (hl (hull 3).full)
    rw [Data.vec, vfull]
    gcongr
    · norm_num [wfull, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (hu x) ?_
    gcongr
    · norm_num [vmax, vmin]
    · norm_num [Lup, Mup]

end Gump.Dice

namespace Gump.Dice
open Hull3Data

/-- **ln τ of the 9-cell hull triangle.** For every quasi-stationary law (μ, λ) of the chain,
0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374, and τ = E_μ T = 1/(1 - λ) has
2.4837157463 < ln τ < 2.4837157464 (`rigour/README.md`: 2.4837157463). -/
theorem hull3_tau (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
    (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
    2.4837157463 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.4837157464 := by
  rw [hρ1, hρ2] at hq
  obtain ⟨h1, h2⟩ := data.qsd_bounds (hull 3) Vup Vlo Lup Mup Llo Mlo vmin vmax vmin wmax tab up lo vu vl
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [vmin]) μ lam hq
  have l1 : (0.9165673655948901373 : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ 0.9165673655948901374 := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ (by linarith) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    have hs : 0 ≤ expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    calc (1 - lam) * (expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15) ^ 3
        ≤ (1 - 0.9165673655948901373) * (expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15) ^ 3 := by
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ (by linarith) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - 0.9165673655948901374) * (expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15) ^ 3 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15) ^ 3 := by
          gcongr

end Gump.Dice
