/-
**Both exits, proved at 9 cells**: the share of the quasi-stationary death flux of the face `(hull 3)` through the
bust (a fall of at least half the face, ⌈A/2⌉ cells, in one generation among the last 6 transitions; `qsd.c`
`halffall_share K=6`, `rigour/README.md` claim 4: 0.0170) lies in (0.017017, 0.017018): this face dies mostly by
the fade. Written by `python3 research/blast/lean/dice_exit.py`; every check is run by the kernel.
-/
import GumpMath.DiceHull3ExitData
import GumpMath.DiceHull3

set_option maxRecDepth 100000

namespace Gump.Dice
namespace Hull3ExitData
open Hull3Data

theorem base : Data.nbBase (hull 3).A N0 = true := by decide +kernel
theorem n1 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N1 N0) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem n2 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N2 N1) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem n3 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N3 N2) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem n4 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N4 N3) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem n5 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N5 N4) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem n6 : Data.allRows (data.nbRow (hull 3).A (hull 3).half N6 N5) (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem pois : Data.allRows (data.poisRow (hull 3).A (data.Dt (hull 3).A) 6 N6 Wp Wm S p ((Lup : ℚ) / Mup) eps om)
    (2 ^ (hull 3).A) = true := by
  decide +kernel
theorem w0 : Wp.get (hull 3).A 0 = 0 ∧ Wm.get (hull 3).A 0 = 0 := by decide +kernel

end Hull3ExitData
open Hull3Data Hull3ExitData

/-- **The bust share of the face `(hull 3)`** (K = 6): for every quasi-stationary law (μ, λ),
0.017017 < bustShare < 0.017018. -/
theorem hull3_bust (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
    0.017017 < (hull 3).bustShare ρ1 ρ2 6 μ lam ∧ (hull 3).bustShare ρ1 ρ2 6 μ lam < 0.017018 := by
  obtain ⟨l1, l2, -, -⟩ := hull3_tau μ lam hq
  rw [hρ1, hρ2] at hq
  have r0 : ∀ v : Fin (2 ^ (hull 3).A), (N0.get (hull 3).A v : ℚ) =
      (data.Dt (hull 3).A : ℚ) ^ 0 * (hull 3).noBust ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) 0 v :=
    data.nbBase_spec (hull 3).A N0 base _ _ (hull 3) rfl
  have r1 := data.nbRow_spec (hull 3) tab N1 N0 0 n1 r0
  have r2 := data.nbRow_spec (hull 3) tab N2 N1 1 n2 r1
  have r3 := data.nbRow_spec (hull 3) tab N3 N2 2 n3 r2
  have r4 := data.nbRow_spec (hull 3) tab N4 N3 3 n4 r3
  have r5 := data.nbRow_spec (hull 3) tab N5 N4 4 n5 r4
  have r6 := data.nbRow_spec (hull 3) tab N6 N5 5 n6 r5
  have hb := data.poisson_bound (hull 3) tab 6 N6 Wp Wm S (by norm_num [S]) p ((Lup : ℚ) / Mup) eps om pois w0
    r6 μ lam hq
  have hl' : |(((Lup : ℚ) / Mup : ℚ) : ℝ) - lam| ≤ (0.9165673655948901374 : ℝ) - 0.9165673655948901373 := by
    have h1 : (((Lup : ℚ) / Mup : ℚ) : ℝ) ≤ 0.9165673655948901374 := by norm_num [Lup, Mup]
    have h2 : (0.9165673655948901373 : ℝ) ≤ (((Lup : ℚ) / Mup : ℚ) : ℝ) := by norm_num [Lup, Mup]
    rw [abs_le]; constructor <;> linarith
  have hb' : |∑ x, μ x * ((hull 3).noBust ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) 6 x : ℝ) -
      (p : ℝ) * (1 - lam)| ≤ ((eps : ℝ) + ((0.9165673655948901374 : ℝ) - 0.9165673655948901373) * om) * (1 - lam) := by
    refine hb.trans (mul_le_mul_of_nonneg_right ?_ (by linarith))
    have : (0 : ℝ) ≤ (om : ℝ) := by norm_num [om]
    nlinarith
  have := share_interval _ lam p ((eps : ℝ) + ((0.9165673655948901374 : ℝ) - 0.9165673655948901373) * om) 0.9165673655948901373 0.9165673655948901374 6
    (by norm_num) l1 l2 (by linarith) (by norm_num [p, eps, om]) hb'
  rw [← hρ1, ← hρ2] at this
  unfold Face.bustShare
  constructor
  · refine lt_of_lt_of_le ?_ this.1
    norm_num [p, eps, om]
  · refine lt_of_le_of_lt this.2 ?_
    norm_num [p, eps, om]

end Gump.Dice
