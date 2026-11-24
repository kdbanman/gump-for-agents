/-
The lifetime of the 9-cell face `(torus 1 0 3)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = 3.3935247191). Written by `python3 research/blast/lean/dice_cert.py torus 1 0 3`
with its certificate `GumpMath/DiceTorus103Data.lean`; every check is run by the kernel (`decide +kernel`).
  `torus103_lifetime`: survival from x₀ (the 3 cells of orientation x alive) and from every state, for every t;
  `torus103_tau`: 0.9664099275695942426 ≤ λ ≤ 0.9664099275695942427 for every quasi-stationary law (μ, λ) with λ > 0, so
  h = 1 - λ ∈ [0.0335900724304057573, 0.0335900724304057574] and 3.3935247190 < ln τ = -ln(1 - λ) < 3.3935247191.
-/
import GumpMath.DiceTorus103Data
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace Torus103Data

theorem tab : data.tabOK (torus 1 0 3) = true := by decide +kernel

theorem up : Data.allRows (data.rowUp (torus 1 0 3).A (data.Dt (torus 1 0 3).A) Lup Mup Vup) (2 ^ (torus 1 0 3).A) = true := by
  decide +kernel

theorem lo : Data.allRows (data.rowLo (torus 1 0 3).A (data.Dt (torus 1 0 3).A) Llo Mlo Vlo) (2 ^ (torus 1 0 3).A) = true := by
  decide +kernel

theorem vl0 : Data.vecOK Vlo (torus 1 0 3).A 0 wmax = true := by decide +kernel
theorem vx : Vlo.get (torus 1 0 3).A 73 = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]
theorem gs : Data.allRows (data.rowLe (torus 1 0 3).A (data.Dt (torus 1 0 3).A) Kg Ng Gs Vup) (2 ^ (torus 1 0 3).A) = true := by
  decide +kernel
theorem v2 : Data.vecOK2 Vup Gs (torus 1 0 3).A vmin vmax = true := by decide +kernel
theorem vu1 : Data.vecOK Vup (torus 1 0 3).A 1 vmax = true := by decide +kernel
theorem sure : data.sureOK Vlo (torus 1 0 3).A = true := by decide +kernel

end Torus103Data
open Torus103Data

/-- **The lifetime of the face `(torus 1 0 3)`, for every t.** Survival from x₀ = 73 (the 3 cells of orientation x alive) is at least
0.96 · 0.9664099275695942426 ^ t; from every state, survival to t + 1 is at most 3.07 · 0.9664099275695942427 ^ (t + 1).
(The full face dies surely in one generation: every cell has k = 6, or is overcrowded.) -/
theorem torus103_lifetime (t : ℕ) :
    (0.96 : ℚ) * 0.9664099275695942426 ^ t ≤ (torus 1 0 3).survival ρ1 ρ2 t ⟨73, by decide⟩ ∧
    ∀ x, (torus 1 0 3).survival ρ1 ρ2 (t + 1) x ≤ 3.07 * 0.9664099275695942427 ^ (t + 1) := by
  rw [hρ1, hρ2]
  constructor
  · refine le_trans ?_ (data.survival_lo (torus 1 0 3) Vlo Llo Mlo wmax tab lo vl0 (by norm_num [Mlo]) (by norm_num [wmax]) t _)
    rw [Data.vec, show ((⟨73, by decide⟩ : Fin (2 ^ (torus 1 0 3).A)) : ℕ) = 73 from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (data.survival_up_sure (torus 1 0 3) Vup Gs Lup Mup Kg Ng vmin vmax tab up gs v2 (by norm_num [Mup])
      (by norm_num [Ng]) (by norm_num [vmin]) (by norm_num [Lup]) t x) ?_
    gcongr
    · norm_num [vmax, vmin, Kg, Ng, Lup, Mup]
    · norm_num [Lup, Mup]

/-- **ln τ of the face `(torus 1 0 3)`.** For every quasi-stationary law (μ, λ) with λ > 0,
0.9664099275695942426 ≤ λ ≤ 0.9664099275695942427 and τ = E_μ T = 1/(1 - λ) has 3.3935247190 < ln τ < 3.3935247191. -/
theorem torus103_tau (μ : Fin (2 ^ (torus 1 0 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 0 3) ρ1 ρ2 μ lam) (hlam : 0 < lam) :
    (0.9664099275695942426 : ℝ) ≤ lam ∧ lam ≤ 0.9664099275695942427 ∧
    3.3935247190 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 3.3935247191 := by
  rw [hρ1, hρ2] at hq
  have h1 := data.qsd_lo_sure (torus 1 0 3) Vlo Llo Mlo wmax tab lo vl0 sure (by norm_num [Mlo]) μ lam hq hlam
  have h2 := data.qsd_up (torus 1 0 3) Vup Lup Mup 1 vmax tab up vu1 (by norm_num [Mup]) (by norm_num) μ lam hq
  have l1 : (0.9664099275695942426 : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ 0.9664099275695942427 := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ 4 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    have hs : 0 ≤ expSum (3.3935247190 / 4) 15 + expErr (3.3935247190 / 4) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    calc (1 - lam) * (expSum (3.3935247190 / 4) 15 + expErr (3.3935247190 / 4) 15) ^ 4
        ≤ (1 - 0.9664099275695942426) * (expSum (3.3935247190 / 4) 15 + expErr (3.3935247190 / 4) 15) ^ 4 := by
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (3.3935247191 / 4) 15 - expErr (3.3935247191 / 4) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ 4 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - 0.9664099275695942427) * (expSum (3.3935247191 / 4) 15 - expErr (3.3935247191 / 4) 15) ^ 4 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (3.3935247191 / 4) 15 - expErr (3.3935247191 / 4) 15) ^ 4 := by
          gcongr

end Gump.Dice
