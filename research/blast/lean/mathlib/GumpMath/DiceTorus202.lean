/-
The lifetime of the 12-cell face `(torus 2 0 2)` of the one-layer dice surrogate at (ρ1, ρ2) = (0.44, 0.42)
(`rigour/README.md` claim 3: ln τ = see the table). Written by `python3 research/blast/lean/dice_sym.py`; the row checks
run on the 144 orbit representatives of the 48 table automorphisms (`GumpMath/DiceSym.lean`), every check in the kernel.
  `torus202_lifetime`: survival from x₀ (the 4 cells of orientation x alive) and from every state, for every t;
  `torus202_tau`: 0.9813486469939093 ≤ λ ≤ 0.9813486469939113 for every quasi-stationary law (μ, λ) with λ > 0, so
  h = 1 - λ ∈ [0.0186513530060887, 0.0186513530060907] and 3.9818365882 < ln τ = -ln(1 - λ) < 3.9818365883.
-/
import GumpMath.DiceTorus202Data
import GumpMath.DiceLife
import GumpMath.DiceReal

set_option maxRecDepth 100000

namespace Gump.Dice
namespace Torus202Data
open Data

theorem tab : data.tabOK (torus 2 0 2) = true := by decide +kernel
theorem sym0 : data.symOK (torus 2 0 2).A g0.1 g0.2 = true := by decide +kernel
theorem inv0 : invOK (torus 2 0 2).A g0.2 Vup = true ∧ invOK (torus 2 0 2).A g0.2 Vlo = true ∧ invOK (torus 2 0 2).A g0.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym1 : data.symOK (torus 2 0 2).A g1.1 g1.2 = true := by decide +kernel
theorem inv1 : invOK (torus 2 0 2).A g1.2 Vup = true ∧ invOK (torus 2 0 2).A g1.2 Vlo = true ∧ invOK (torus 2 0 2).A g1.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym2 : data.symOK (torus 2 0 2).A g2.1 g2.2 = true := by decide +kernel
theorem inv2 : invOK (torus 2 0 2).A g2.2 Vup = true ∧ invOK (torus 2 0 2).A g2.2 Vlo = true ∧ invOK (torus 2 0 2).A g2.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym3 : data.symOK (torus 2 0 2).A g3.1 g3.2 = true := by decide +kernel
theorem inv3 : invOK (torus 2 0 2).A g3.2 Vup = true ∧ invOK (torus 2 0 2).A g3.2 Vlo = true ∧ invOK (torus 2 0 2).A g3.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym4 : data.symOK (torus 2 0 2).A g4.1 g4.2 = true := by decide +kernel
theorem inv4 : invOK (torus 2 0 2).A g4.2 Vup = true ∧ invOK (torus 2 0 2).A g4.2 Vlo = true ∧ invOK (torus 2 0 2).A g4.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym5 : data.symOK (torus 2 0 2).A g5.1 g5.2 = true := by decide +kernel
theorem inv5 : invOK (torus 2 0 2).A g5.2 Vup = true ∧ invOK (torus 2 0 2).A g5.2 Vlo = true ∧ invOK (torus 2 0 2).A g5.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym6 : data.symOK (torus 2 0 2).A g6.1 g6.2 = true := by decide +kernel
theorem inv6 : invOK (torus 2 0 2).A g6.2 Vup = true ∧ invOK (torus 2 0 2).A g6.2 Vlo = true ∧ invOK (torus 2 0 2).A g6.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym7 : data.symOK (torus 2 0 2).A g7.1 g7.2 = true := by decide +kernel
theorem inv7 : invOK (torus 2 0 2).A g7.2 Vup = true ∧ invOK (torus 2 0 2).A g7.2 Vlo = true ∧ invOK (torus 2 0 2).A g7.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym8 : data.symOK (torus 2 0 2).A g8.1 g8.2 = true := by decide +kernel
theorem inv8 : invOK (torus 2 0 2).A g8.2 Vup = true ∧ invOK (torus 2 0 2).A g8.2 Vlo = true ∧ invOK (torus 2 0 2).A g8.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym9 : data.symOK (torus 2 0 2).A g9.1 g9.2 = true := by decide +kernel
theorem inv9 : invOK (torus 2 0 2).A g9.2 Vup = true ∧ invOK (torus 2 0 2).A g9.2 Vlo = true ∧ invOK (torus 2 0 2).A g9.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym10 : data.symOK (torus 2 0 2).A g10.1 g10.2 = true := by decide +kernel
theorem inv10 : invOK (torus 2 0 2).A g10.2 Vup = true ∧ invOK (torus 2 0 2).A g10.2 Vlo = true ∧ invOK (torus 2 0 2).A g10.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym11 : data.symOK (torus 2 0 2).A g11.1 g11.2 = true := by decide +kernel
theorem inv11 : invOK (torus 2 0 2).A g11.2 Vup = true ∧ invOK (torus 2 0 2).A g11.2 Vlo = true ∧ invOK (torus 2 0 2).A g11.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym12 : data.symOK (torus 2 0 2).A g12.1 g12.2 = true := by decide +kernel
theorem inv12 : invOK (torus 2 0 2).A g12.2 Vup = true ∧ invOK (torus 2 0 2).A g12.2 Vlo = true ∧ invOK (torus 2 0 2).A g12.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym13 : data.symOK (torus 2 0 2).A g13.1 g13.2 = true := by decide +kernel
theorem inv13 : invOK (torus 2 0 2).A g13.2 Vup = true ∧ invOK (torus 2 0 2).A g13.2 Vlo = true ∧ invOK (torus 2 0 2).A g13.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym14 : data.symOK (torus 2 0 2).A g14.1 g14.2 = true := by decide +kernel
theorem inv14 : invOK (torus 2 0 2).A g14.2 Vup = true ∧ invOK (torus 2 0 2).A g14.2 Vlo = true ∧ invOK (torus 2 0 2).A g14.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym15 : data.symOK (torus 2 0 2).A g15.1 g15.2 = true := by decide +kernel
theorem inv15 : invOK (torus 2 0 2).A g15.2 Vup = true ∧ invOK (torus 2 0 2).A g15.2 Vlo = true ∧ invOK (torus 2 0 2).A g15.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym16 : data.symOK (torus 2 0 2).A g16.1 g16.2 = true := by decide +kernel
theorem inv16 : invOK (torus 2 0 2).A g16.2 Vup = true ∧ invOK (torus 2 0 2).A g16.2 Vlo = true ∧ invOK (torus 2 0 2).A g16.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym17 : data.symOK (torus 2 0 2).A g17.1 g17.2 = true := by decide +kernel
theorem inv17 : invOK (torus 2 0 2).A g17.2 Vup = true ∧ invOK (torus 2 0 2).A g17.2 Vlo = true ∧ invOK (torus 2 0 2).A g17.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym18 : data.symOK (torus 2 0 2).A g18.1 g18.2 = true := by decide +kernel
theorem inv18 : invOK (torus 2 0 2).A g18.2 Vup = true ∧ invOK (torus 2 0 2).A g18.2 Vlo = true ∧ invOK (torus 2 0 2).A g18.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym19 : data.symOK (torus 2 0 2).A g19.1 g19.2 = true := by decide +kernel
theorem inv19 : invOK (torus 2 0 2).A g19.2 Vup = true ∧ invOK (torus 2 0 2).A g19.2 Vlo = true ∧ invOK (torus 2 0 2).A g19.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym20 : data.symOK (torus 2 0 2).A g20.1 g20.2 = true := by decide +kernel
theorem inv20 : invOK (torus 2 0 2).A g20.2 Vup = true ∧ invOK (torus 2 0 2).A g20.2 Vlo = true ∧ invOK (torus 2 0 2).A g20.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym21 : data.symOK (torus 2 0 2).A g21.1 g21.2 = true := by decide +kernel
theorem inv21 : invOK (torus 2 0 2).A g21.2 Vup = true ∧ invOK (torus 2 0 2).A g21.2 Vlo = true ∧ invOK (torus 2 0 2).A g21.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym22 : data.symOK (torus 2 0 2).A g22.1 g22.2 = true := by decide +kernel
theorem inv22 : invOK (torus 2 0 2).A g22.2 Vup = true ∧ invOK (torus 2 0 2).A g22.2 Vlo = true ∧ invOK (torus 2 0 2).A g22.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym23 : data.symOK (torus 2 0 2).A g23.1 g23.2 = true := by decide +kernel
theorem inv23 : invOK (torus 2 0 2).A g23.2 Vup = true ∧ invOK (torus 2 0 2).A g23.2 Vlo = true ∧ invOK (torus 2 0 2).A g23.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym24 : data.symOK (torus 2 0 2).A g24.1 g24.2 = true := by decide +kernel
theorem inv24 : invOK (torus 2 0 2).A g24.2 Vup = true ∧ invOK (torus 2 0 2).A g24.2 Vlo = true ∧ invOK (torus 2 0 2).A g24.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym25 : data.symOK (torus 2 0 2).A g25.1 g25.2 = true := by decide +kernel
theorem inv25 : invOK (torus 2 0 2).A g25.2 Vup = true ∧ invOK (torus 2 0 2).A g25.2 Vlo = true ∧ invOK (torus 2 0 2).A g25.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym26 : data.symOK (torus 2 0 2).A g26.1 g26.2 = true := by decide +kernel
theorem inv26 : invOK (torus 2 0 2).A g26.2 Vup = true ∧ invOK (torus 2 0 2).A g26.2 Vlo = true ∧ invOK (torus 2 0 2).A g26.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym27 : data.symOK (torus 2 0 2).A g27.1 g27.2 = true := by decide +kernel
theorem inv27 : invOK (torus 2 0 2).A g27.2 Vup = true ∧ invOK (torus 2 0 2).A g27.2 Vlo = true ∧ invOK (torus 2 0 2).A g27.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym28 : data.symOK (torus 2 0 2).A g28.1 g28.2 = true := by decide +kernel
theorem inv28 : invOK (torus 2 0 2).A g28.2 Vup = true ∧ invOK (torus 2 0 2).A g28.2 Vlo = true ∧ invOK (torus 2 0 2).A g28.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym29 : data.symOK (torus 2 0 2).A g29.1 g29.2 = true := by decide +kernel
theorem inv29 : invOK (torus 2 0 2).A g29.2 Vup = true ∧ invOK (torus 2 0 2).A g29.2 Vlo = true ∧ invOK (torus 2 0 2).A g29.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym30 : data.symOK (torus 2 0 2).A g30.1 g30.2 = true := by decide +kernel
theorem inv30 : invOK (torus 2 0 2).A g30.2 Vup = true ∧ invOK (torus 2 0 2).A g30.2 Vlo = true ∧ invOK (torus 2 0 2).A g30.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym31 : data.symOK (torus 2 0 2).A g31.1 g31.2 = true := by decide +kernel
theorem inv31 : invOK (torus 2 0 2).A g31.2 Vup = true ∧ invOK (torus 2 0 2).A g31.2 Vlo = true ∧ invOK (torus 2 0 2).A g31.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym32 : data.symOK (torus 2 0 2).A g32.1 g32.2 = true := by decide +kernel
theorem inv32 : invOK (torus 2 0 2).A g32.2 Vup = true ∧ invOK (torus 2 0 2).A g32.2 Vlo = true ∧ invOK (torus 2 0 2).A g32.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym33 : data.symOK (torus 2 0 2).A g33.1 g33.2 = true := by decide +kernel
theorem inv33 : invOK (torus 2 0 2).A g33.2 Vup = true ∧ invOK (torus 2 0 2).A g33.2 Vlo = true ∧ invOK (torus 2 0 2).A g33.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym34 : data.symOK (torus 2 0 2).A g34.1 g34.2 = true := by decide +kernel
theorem inv34 : invOK (torus 2 0 2).A g34.2 Vup = true ∧ invOK (torus 2 0 2).A g34.2 Vlo = true ∧ invOK (torus 2 0 2).A g34.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym35 : data.symOK (torus 2 0 2).A g35.1 g35.2 = true := by decide +kernel
theorem inv35 : invOK (torus 2 0 2).A g35.2 Vup = true ∧ invOK (torus 2 0 2).A g35.2 Vlo = true ∧ invOK (torus 2 0 2).A g35.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym36 : data.symOK (torus 2 0 2).A g36.1 g36.2 = true := by decide +kernel
theorem inv36 : invOK (torus 2 0 2).A g36.2 Vup = true ∧ invOK (torus 2 0 2).A g36.2 Vlo = true ∧ invOK (torus 2 0 2).A g36.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym37 : data.symOK (torus 2 0 2).A g37.1 g37.2 = true := by decide +kernel
theorem inv37 : invOK (torus 2 0 2).A g37.2 Vup = true ∧ invOK (torus 2 0 2).A g37.2 Vlo = true ∧ invOK (torus 2 0 2).A g37.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym38 : data.symOK (torus 2 0 2).A g38.1 g38.2 = true := by decide +kernel
theorem inv38 : invOK (torus 2 0 2).A g38.2 Vup = true ∧ invOK (torus 2 0 2).A g38.2 Vlo = true ∧ invOK (torus 2 0 2).A g38.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym39 : data.symOK (torus 2 0 2).A g39.1 g39.2 = true := by decide +kernel
theorem inv39 : invOK (torus 2 0 2).A g39.2 Vup = true ∧ invOK (torus 2 0 2).A g39.2 Vlo = true ∧ invOK (torus 2 0 2).A g39.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym40 : data.symOK (torus 2 0 2).A g40.1 g40.2 = true := by decide +kernel
theorem inv40 : invOK (torus 2 0 2).A g40.2 Vup = true ∧ invOK (torus 2 0 2).A g40.2 Vlo = true ∧ invOK (torus 2 0 2).A g40.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym41 : data.symOK (torus 2 0 2).A g41.1 g41.2 = true := by decide +kernel
theorem inv41 : invOK (torus 2 0 2).A g41.2 Vup = true ∧ invOK (torus 2 0 2).A g41.2 Vlo = true ∧ invOK (torus 2 0 2).A g41.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym42 : data.symOK (torus 2 0 2).A g42.1 g42.2 = true := by decide +kernel
theorem inv42 : invOK (torus 2 0 2).A g42.2 Vup = true ∧ invOK (torus 2 0 2).A g42.2 Vlo = true ∧ invOK (torus 2 0 2).A g42.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym43 : data.symOK (torus 2 0 2).A g43.1 g43.2 = true := by decide +kernel
theorem inv43 : invOK (torus 2 0 2).A g43.2 Vup = true ∧ invOK (torus 2 0 2).A g43.2 Vlo = true ∧ invOK (torus 2 0 2).A g43.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym44 : data.symOK (torus 2 0 2).A g44.1 g44.2 = true := by decide +kernel
theorem inv44 : invOK (torus 2 0 2).A g44.2 Vup = true ∧ invOK (torus 2 0 2).A g44.2 Vlo = true ∧ invOK (torus 2 0 2).A g44.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym45 : data.symOK (torus 2 0 2).A g45.1 g45.2 = true := by decide +kernel
theorem inv45 : invOK (torus 2 0 2).A g45.2 Vup = true ∧ invOK (torus 2 0 2).A g45.2 Vlo = true ∧ invOK (torus 2 0 2).A g45.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym46 : data.symOK (torus 2 0 2).A g46.1 g46.2 = true := by decide +kernel
theorem inv46 : invOK (torus 2 0 2).A g46.2 Vup = true ∧ invOK (torus 2 0 2).A g46.2 Vlo = true ∧ invOK (torus 2 0 2).A g46.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem sym47 : data.symOK (torus 2 0 2).A g47.1 g47.2 = true := by decide +kernel
theorem inv47 : invOK (torus 2 0 2).A g47.2 Vup = true ∧ invOK (torus 2 0 2).A g47.2 Vlo = true ∧ invOK (torus 2 0 2).A g47.2 Gs = true :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
theorem reps : repsOK (torus 2 0 2).A gens Wg Wr Rm = true := by decide +kernel
theorem up : marked (torus 2 0 2).A Rm (data.rowLe (torus 2 0 2).A (data.Dt (torus 2 0 2).A) Lup Mup Vup Vup) = true := by decide +kernel
theorem gs : marked (torus 2 0 2).A Rm (data.rowLe (torus 2 0 2).A (data.Dt (torus 2 0 2).A) Kg Ng Gs Vup) = true := by decide +kernel
theorem lo : marked (torus 2 0 2).A Rm (data.rowLo (torus 2 0 2).A (data.Dt (torus 2 0 2).A) Llo Mlo Vlo) = true := by decide +kernel
theorem v2 : Data.vecOK2 Vup Gs (torus 2 0 2).A vmin vmax = true := by decide +kernel
theorem vu1 : Data.vecOK Vup (torus 2 0 2).A 1 vmax = true := by decide +kernel
theorem vl0 : Data.vecOK Vlo (torus 2 0 2).A 0 wmax = true := by decide +kernel
theorem sure : data.sureOK Vlo (torus 2 0 2).A = true := by decide +kernel
theorem vx : Vlo.get (torus 2 0 2).A 585 = wx := by decide +kernel

theorem hρ1 : ρ1 = ((data.n1 : ℚ) / data.d1) := by norm_num [ρ1, data]
theorem hρ2 : ρ2 = ((data.n2 : ℚ) / data.d2) := by norm_num [ρ2, data]

theorem hsym : ∀ g ∈ gens, data.symOK (torus 2 0 2).A g.1 g.2 = true := by
  simp only [gens, List.forall_mem_cons, List.forall_mem_nil, and_true]
  exact ⟨sym0, sym1, sym2, sym3, sym4, sym5, sym6, sym7, sym8, sym9, sym10, sym11, sym12, sym13, sym14, sym15, sym16, sym17, sym18, sym19, sym20, sym21, sym22, sym23, sym24, sym25, sym26, sym27, sym28, sym29, sym30, sym31, sym32, sym33, sym34, sym35, sym36, sym37, sym38, sym39, sym40, sym41, sym42, sym43, sym44, sym45, sym46, sym47⟩
theorem hinv : ∀ g ∈ gens, invOK (torus 2 0 2).A g.2 Vup = true ∧ invOK (torus 2 0 2).A g.2 Vlo = true ∧ invOK (torus 2 0 2).A g.2 Gs = true := by
  simp only [gens, List.forall_mem_cons, List.forall_mem_nil, and_true]
  exact ⟨inv0, inv1, inv2, inv3, inv4, inv5, inv6, inv7, inv8, inv9, inv10, inv11, inv12, inv13, inv14, inv15, inv16, inv17, inv18, inv19, inv20, inv21, inv22, inv23, inv24, inv25, inv26, inv27, inv28, inv29, inv30, inv31, inv32, inv33, inv34, inv35, inv36, inv37, inv38, inv39, inv40, inv41, inv42, inv43, inv44, inv45, inv46, inv47⟩

theorem iup : ∀ x, ((torus 2 0 2).P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Vup (torus 2 0 2).A) x ≤ ((Lup : ℚ) / Mup) * vec Vup (torus 2 0 2).A x :=
  data.ineq_up_of_reps (torus 2 0 2) tab gens Wg Wr Rm hsym Vup Vup (fun g hg => (hinv g hg).1)
  (fun g hg => (hinv g hg).1) reps Lup Mup (by norm_num [Mup]) up
theorem igs : ∀ x, ((torus 2 0 2).P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Gs (torus 2 0 2).A) x ≤ ((Kg : ℚ) / Ng) * vec Vup (torus 2 0 2).A x :=
  data.ineq_up_of_reps (torus 2 0 2) tab gens Wg Wr Rm hsym Gs Vup (fun g hg => (hinv g hg).2.2)
  (fun g hg => (hinv g hg).1) reps Kg Ng (by norm_num [Ng]) gs
theorem ilo : ∀ x, ((Llo : ℚ) / Mlo) * vec Vlo (torus 2 0 2).A x ≤ ((torus 2 0 2).P ((data.n1 : ℚ) / data.d1) ((data.n2 : ℚ) / data.d2) *ᵥ vec Vlo (torus 2 0 2).A) x :=
  data.ineq_lo_of_reps (torus 2 0 2) tab gens Wg Wr Rm hsym Vlo (fun g hg => (hinv g hg).2.1) reps Llo Mlo
  (by norm_num [Mlo]) lo

end Torus202Data
open Torus202Data

/-- **The lifetime of the face `(torus 2 0 2)`, for every t.** Survival from x₀ = 585 (the 4 cells of orientation x alive) is at least
0.97 · 0.9813486469939093 ^ t; from every state, survival to t + 1 is at most 4.46 · 0.9813486469939113 ^ (t + 1). -/
theorem torus202_lifetime (t : ℕ) :
    (0.97 : ℚ) * 0.9813486469939093 ^ t ≤ (torus 2 0 2).survival ρ1 ρ2 t ⟨585, by decide⟩ ∧
    ∀ x, (torus 2 0 2).survival ρ1 ρ2 (t + 1) x ≤ 4.46 * 0.9813486469939113 ^ (t + 1) := by
  rw [hρ1, hρ2]
  constructor
  · refine le_trans ?_ (data.survival_lo_ineq (torus 2 0 2) Vlo Llo Mlo wmax tab ilo vl0 (by norm_num [Mlo]) (by norm_num [wmax]) t _)
    rw [Data.vec, show ((⟨585, by decide⟩ : Fin (2 ^ (torus 2 0 2).A)) : ℕ) = 585 from rfl, vx]
    gcongr
    · norm_num [wx, wmax]
    · norm_num [Llo, Mlo]
  · intro x
    refine le_trans (data.survival_up_sure_ineq (torus 2 0 2) Vup Gs Lup Mup Kg Ng vmin vmax tab iup igs v2 (by norm_num [Mup])
      (by norm_num [Ng]) (by norm_num [vmin]) (by norm_num [Lup]) t x) ?_
    gcongr
    · norm_num [vmax, vmin, Kg, Ng, Lup, Mup]
    · norm_num [Lup, Mup]

/-- **ln τ of the face `(torus 2 0 2)`.** For every quasi-stationary law (μ, λ) with λ > 0,
0.9813486469939093 ≤ λ ≤ 0.9813486469939113 and 3.9818365882 < ln τ < 3.9818365883. -/
theorem torus202_tau (μ : Fin (2 ^ (torus 2 0 2).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 2 0 2) ρ1 ρ2 μ lam) (hlam : 0 < lam) :
    (0.9813486469939093 : ℝ) ≤ lam ∧ lam ≤ 0.9813486469939113 ∧
    3.9818365882 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 3.9818365883 := by
  rw [hρ1, hρ2] at hq
  have h1 := data.qsd_lo_sure_ineq (torus 2 0 2) Vlo Llo Mlo wmax tab ilo vl0 sure (by norm_num [Mlo]) μ lam hq hlam
  have h2 := data.qsd_up_ineq (torus 2 0 2) Vup Lup Mup 1 vmax tab iup vu1 (by norm_num [Mup]) (by norm_num) μ lam hq
  have l1 : (0.9813486469939093 : ℝ) ≤ lam := le_trans (by norm_num [Llo, Mlo]) h1
  have l2 : lam ≤ 0.9813486469939113 := le_trans h2 (by norm_num [Lup, Mup])
  refine ⟨l1, l2, ?_, ?_⟩
  · refine lt_neg_log (1 - lam) _ 4 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_
    calc (1 - lam) * (expSum (3.9818365882 / 4) 15 + expErr (3.9818365882 / 4) 15) ^ 4
        ≤ (1 - 0.9813486469939093) * (expSum (3.9818365882 / 4) 15 + expErr (3.9818365882 / 4) 15) ^ 4 := by
          have hs : 0 ≤ expSum (3.9818365882 / 4) 15 + expErr (3.9818365882 / 4) 15 := by
            simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
          gcongr
      _ < 1 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  · have hs : 0 ≤ expSum (3.9818365883 / 4) 15 - expErr (3.9818365883 / 4) 15 := by
      simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    refine neg_log_lt (1 - lam) _ 4 (by linarith) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) hs ?_
    calc (1 : ℝ) < (1 - 0.9813486469939113) * (expSum (3.9818365883 / 4) 15 - expErr (3.9818365883 / 4) 15) ^ 4 := by
          simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
      _ ≤ (1 - lam) * (expSum (3.9818365883 / 4) 15 - expErr (3.9818365883 / 4) 15) ^ 4 := by
          gcongr

end Gump.Dice
