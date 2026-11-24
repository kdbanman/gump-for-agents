/-
The lifetime of the 9-cell face `(hull 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = 2.4837157463). Written by `python3 research/blast/lean/dice_cert.py hull 3`
with its certificate `GumpMath/DiceHull3Data.lean`; every check is run by the kernel (`decide +kernel`).
  `hull3_lifetime`: survival from x₀ (the full face) and from every state, for every t;
  `hull3_tau`: 0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374 for every quasi-stationary law (μ, λ), so
  h = 1 - λ ∈ [0.0834326344051098626, 0.0834326344051098627] and 2.4837157463 < ln τ = -ln(1 - λ) < 2.4837157464.
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

theorem vl0 : Data.vecOK Vlo (hull 3).A 0 wmax = true := by decide +kernel
theorem vx : Vlo.get (hull 3).A 511 = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]
theorem vu : Data.vecOK Vup (hull 3).A vmin vmax = true := by decide +kernel
theorem vl : Data.vecOK Vlo (hull 3).A vmin wmax = true := by decide +kernel

end Hull3Data
open Hull3Data

/-- **The lifetime of the face `(hull 3)`, for every t.** Survival from the full face is at least
0.72 · 0.9165673655948901373 ^ t, and from every state at most 1384 · 0.9165673655948901374 ^ t. -/
theorem hull3_lifetime (t : ℕ) :
    (0.72 : ℚ) * 0.9165673655948901373 ^ t ≤ (hull 3).survival ρ1 ρ2 t (hull 3).full ∧
    ∀ x, (hull 3).survival ρ1 ρ2 t x ≤ 1384 * 0.9165673655948901374 ^ t := by
  rw [hρ1, hρ2]
  obtain ⟨hl, hu⟩ := data.lifetime_of_cert (hull 3) Vup Vlo Lup Mup Llo Mlo vmin vmax wmax tab up lo vu vl0
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [wmax]) t
  constructor
  · refine le_trans ?_ (hl (hull 3).full)
    rw [Data.vec, show (((hull 3).full : Fin _) : ℕ) = 511 from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (hu x) ?_
    gcongr
    · norm_num [vmax, vmin]
    · norm_num [Lup, Mup]

/-- **ln τ of the face `(hull 3)`.** For every quasi-stationary law (μ, λ),
0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374 and τ = E_μ T = 1/(1 - λ) has 2.4837157463 < ln τ < 2.4837157464. -/
theorem hull3_tau (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
    (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
    2.4837157463 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.4837157464 := by
  rw [hρ1, hρ2] at hq
  obtain ⟨h1, h2⟩ := data.qsd_bounds (hull 3) Vup Vlo Lup Mup Llo Mlo vmin vmax vmin wmax tab up lo vu vl
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [vmin]) μ lam hq
  have l1 : (0.9165673655948901373 : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ 0.9165673655948901374 := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ 3 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    have hs : 0 ≤ expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    calc (1 - lam) * (expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15) ^ 3
        ≤ (1 - 0.9165673655948901373) * (expSum (2.4837157463 / 3) 15 + expErr (2.4837157463 / 3) 15) ^ 3 := by
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ 3 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - 0.9165673655948901374) * (expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15) ^ 3 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (2.4837157464 / 3) 15 - expErr (2.4837157464 / 3) 15) ^ 3 := by
          gcongr

end Gump.Dice
