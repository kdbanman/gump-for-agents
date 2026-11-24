/-
The lifetime of the 9-cell face `(strip 1 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = 2.7988780569). Written by `python3 research/blast/lean/dice_cert.py strip 1 3`
with its certificate `GumpMath/DiceStrip13Data.lean`; every check is run by the kernel (`decide +kernel`).
  `strip13_lifetime`: survival from x₀ (the full face) and from every state, for every t;
  `strip13_tau`: 0.9391216736592712685 ≤ λ ≤ 0.9391216736592712686 for every quasi-stationary law (μ, λ), so
  h = 1 - λ ∈ [0.0608783263407287314, 0.0608783263407287315] and 2.7988780569 < ln τ = -ln(1 - λ) < 2.7988780570.
-/
import GumpMath.DiceStrip13Data
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace Strip13Data

theorem tab : data.tabOK (strip 1 3) = true := by decide +kernel

theorem up : Data.allRows (data.rowUp (strip 1 3).A (data.Dt (strip 1 3).A) Lup Mup Vup) (2 ^ (strip 1 3).A) = true := by
  decide +kernel

theorem lo : Data.allRows (data.rowLo (strip 1 3).A (data.Dt (strip 1 3).A) Llo Mlo Vlo) (2 ^ (strip 1 3).A) = true := by
  decide +kernel

theorem vl0 : Data.vecOK Vlo (strip 1 3).A 0 wmax = true := by decide +kernel
theorem vx : Vlo.get (strip 1 3).A 511 = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]
theorem vu : Data.vecOK Vup (strip 1 3).A vmin vmax = true := by decide +kernel
theorem vl : Data.vecOK Vlo (strip 1 3).A vmin wmax = true := by decide +kernel

end Strip13Data
open Strip13Data

/-- **The lifetime of the face `(strip 1 3)`, for every t.** Survival from the full face is at least
0.97 · 0.9391216736592712685 ^ t, and from every state at most 512 · 0.9391216736592712686 ^ t. -/
theorem strip13_lifetime (t : ℕ) :
    (0.97 : ℚ) * 0.9391216736592712685 ^ t ≤ (strip 1 3).survival ρ1 ρ2 t (strip 1 3).full ∧
    ∀ x, (strip 1 3).survival ρ1 ρ2 t x ≤ 512 * 0.9391216736592712686 ^ t := by
  rw [hρ1, hρ2]
  obtain ⟨hl, hu⟩ := data.lifetime_of_cert (strip 1 3) Vup Vlo Lup Mup Llo Mlo vmin vmax wmax tab up lo vu vl0
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [wmax]) t
  constructor
  · refine le_trans ?_ (hl (strip 1 3).full)
    rw [Data.vec, show (((strip 1 3).full : Fin _) : ℕ) = 511 from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (hu x) ?_
    gcongr
    · norm_num [vmax, vmin]
    · norm_num [Lup, Mup]

/-- **ln τ of the face `(strip 1 3)`.** For every quasi-stationary law (μ, λ),
0.9391216736592712685 ≤ λ ≤ 0.9391216736592712686 and τ = E_μ T = 1/(1 - λ) has 2.7988780569 < ln τ < 2.7988780570. -/
theorem strip13_tau (μ : Fin (2 ^ (strip 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (strip 1 3) ρ1 ρ2 μ lam) :
    (0.9391216736592712685 : ℝ) ≤ lam ∧ lam ≤ 0.9391216736592712686 ∧
    2.7988780569 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.7988780570 := by
  rw [hρ1, hρ2] at hq
  obtain ⟨h1, h2⟩ := data.qsd_bounds (strip 1 3) Vup Vlo Lup Mup Llo Mlo vmin vmax vmin wmax tab up lo vu vl
    (by norm_num [Mup]) (by norm_num [Mlo]) (by norm_num [vmin]) (by norm_num [vmin]) μ lam hq
  have l1 : (0.9391216736592712685 : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ 0.9391216736592712686 := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ 3 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    have hs : 0 ≤ expSum (2.7988780569 / 3) 15 + expErr (2.7988780569 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    calc (1 - lam) * (expSum (2.7988780569 / 3) 15 + expErr (2.7988780569 / 3) 15) ^ 3
        ≤ (1 - 0.9391216736592712685) * (expSum (2.7988780569 / 3) 15 + expErr (2.7988780569 / 3) 15) ^ 3 := by
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (2.7988780570 / 3) 15 - expErr (2.7988780570 / 3) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ 3 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - 0.9391216736592712686) * (expSum (2.7988780570 / 3) 15 - expErr (2.7988780570 / 3) 15) ^ 3 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (2.7988780570 / 3) 15 - expErr (2.7988780570 / 3) 15) ^ 3 := by
          gcongr

end Gump.Dice
