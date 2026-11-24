/-
**ln τ is linear in the area on every wrapped face, for `Face.P` itself** (`wrapped_area`): for the unique
quasi-stationary law with λ > 0 of `torus H K D` (H, D > 0, every K, every 0 < ρ1, ρ2 < 1),
ln τ = H·D·(c₀ + c₁ + c₂), with c_o the price of cell o (the three orientations at the origin), and on a
rotation-invariant torus ln τ = A·c₀ (A = 3HD). From the chain arm's `wrapped_one_price_HD` and
`wrapped_rotation_HD` on the kagome layer, carried along `Q_eq` with `torusNb_all`.
-/
import GumpMath.LinkWrappedAll

set_option linter.unusedSectionVars false

namespace Gump.Link.Wrapped
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Chain.Kagome Gump.Link Finset

/-- Cell o < 3 of the wrapped face: orientation o at the origin. -/
def c3 (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (o : ℕ) (ho : o < 3) : Fin (torus H K D).A :=
  ⟨o, by
    rw [(torusNb_all H K D hH hD).1]
    have : 1 ≤ H * D := Nat.one_le_iff_ne_zero.2 (Nat.mul_ne_zero hH.ne' hD.ne')
    calc o < 3 := ho
      _ ≤ 3 * (H * D) := by omega
      _ = 3 * H * D := by ring⟩

theorem sum_orient {M : Type*} [AddCommMonoid M] (g : Orient → M) :
    ∑ o : Orient, g o = g .X + g .Y + g .Z := by
  rw [show (univ : Finset Orient) = {Orient.X, Orient.Y, Orient.Z} from rfl,
    Finset.sum_insert (by decide), Finset.sum_insert (by decide), Finset.sum_singleton, add_assoc]

/-- **ln τ = H·D·(c₀ + c₁ + c₂) on every wrapped face, and ln τ = A·c₀ on a rotation-invariant one**, for the
unique quasi-stationary law of `Face.P` with λ > 0 (it exists: `wrapped_theorems_all`). -/
theorem wrapped_area (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)
    (μ : {x : Fin (2 ^ (torus H K D).A) // x ≠ (torus H K D).empty} → ℝ) (lam : ℝ)
    (hμ : (chain (torus H K D) hs.dens).IsQSD μ lam) (hlam : 0 < lam) :
    Real.log ((chain (torus H K D) hs.dens).lifetime μ) =
        (H : ℝ) * D * ((LT H K D hs).price μ (c3 H K D hH hD 0 (by norm_num)) +
          (LT H K D hs).price μ (c3 H K D hH hD 1 (by norm_num)) +
          (LT H K D hs).price μ (c3 H K D hH hD 2 (by norm_num))) ∧
      (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D →
        Real.log ((chain (torus H K D) hs.dens).lifetime μ) =
          (torus H K D).A * (LT H K D hs).price μ (c3 H K D hH hD 0 (by norm_num))) := by
  classical
  have hHz : (0 : ℤ) < H := by exact_mod_cast hH
  have hDz : (0 : ℤ) < D := by exact_mod_cast hD
  let _ : Fintype (Torus (H : ℤ) K D) := (torus_fintype (H : ℤ) K D hHz hDz).some
  have hnb := torusNb_all H K D hH hD
  set f := cellEquiv H K D hH hD hnb.1 with hf
  set eL := stateEquiv (torus H K D) f with heL
  have hQ := Q_eq H K D hH hD hnb hs
  have hc := dc_eq H K D hH hD hnb hs
  have hK := transport_qsd' eL hQ hμ
  -- the face price of cell i is the kernel price of its cell
  have hprice : ∀ i, (LT H K D hs).price μ i =
      (ker H K D hs).localDeath.price (fun x => μ (eL.symm x)) (f i) := by
    intro i
    have := transport_price eL hQ (LT H K D hs) (ker H K D hs).localDeath f (fun i x => hc i x)
      (fun x => μ (eL.symm x)) i
    simpa using this
  have hcell : ∀ (o : ℕ) (ho : o < 3), f (c3 H K D hH hD o ho) = (orientOf o, 0) := by
    intro o ho
    rw [hf, cellEquiv_apply]
    show phi H K D o = _
    unfold phi
    have h1 : o % 3 = o := Nat.mod_eq_of_lt ho
    have h2 : o / 3 = 0 := Nat.div_eq_of_lt ho
    rw [h1, h2, Nat.zero_div, Nat.zero_mod, Nat.cast_zero]
    rfl
  -- ln τ on the face is ln τ of the kernel at the transported law (both are -log(1 - λ))
  have hlogeq : Real.log ((chain (torus H K D) hs.dens).lifetime μ) =
      Real.log ((ker H K D hs).toSubsetChain.killed.lifetime (fun x => μ (eL.symm x))) := by
    rw [log_lifetime_eq (LT H K D hs) hμ, log_lifetime_eq (ker H K D hs).localDeath hK]
  constructor
  · obtain ⟨μ2, lam2, hq2, hlam2, huniq2, -, hlog2⟩ :=
      wrapped_one_price_HD (H : ℤ) K D hHz hDz hs.r0 hs.r1 hs.r2 hs.r3
    obtain ⟨he, -⟩ := huniq2 _ _ hK hlam
    rw [hlogeq, he, hlog2, sum_orient, hprice, hprice, hprice, hcell, hcell, hcell, he]
    rfl
  · intro hl1 hl2
    obtain ⟨μ3, lam3, hq3, hlam3, hall, hlog3⟩ :=
      wrapped_rotation_HD (H : ℤ) K D hHz hDz hs.r0 hs.r1 hs.r2 hs.r3 hl1 hl2
    obtain ⟨μ2, lam2, hq2, hlam2, huniq2, -, -⟩ :=
      wrapped_one_price_HD (H : ℤ) K D hHz hDz hs.r0 hs.r1 hs.r2 hs.r3
    obtain ⟨he, -⟩ := huniq2 _ _ hK hlam
    obtain ⟨he3, -⟩ := huniq2 _ _ hq3 hlam3
    rw [hlogeq, he, ← he3, hlog3, hprice, hcell, he, ← he3, hnb.1]
    push_cast
    rfl

end Gump.Link.Wrapped
