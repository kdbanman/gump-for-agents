/-
**Every wrapped face**, for `Face.P` itself, under one named hypothesis on the dice agent's neighbour lists.

`TorusNb H K D`: the face `torus H K D` has 3HD cells and the neighbour list of cell i = 3(aD + b) + o is,
up to order, that of the kagome layer: orientation o, position (a, b), e1 along a, e2 along b (`kIdx`).
It is a finite statement about the dice agent's definitions alone; `torusNb_of` proves it from a Boolean check,
which the kernel evaluates (`decide +kernel`) for the tori listed at the end.

Under it, the cells are `Orient × Torus H K D` (`cellEquiv`), the states are the subsets (`stateEquiv`), and
`Face.P` *is* the kagome kernel of `ChainKagome.lean` (`Q_eq`), entry by entry. The chain arm's theorems on the
wrapped kagome layer (`wrapped_lemma0`, `wrapped_one_price_HD`, `wrapped_rotation_HD`, `decay_bounds`) then
transport along the relabelling (`transport_*`), and `wrapped_full` states, for `Face.P` on `torus H K D`:
a unique quasi-stationary law with λ > 0, positive on every living state; one price per orientation; ln τ the
sum of the prices; ln τ < 1.9228·A (`lntau_le_torus`); decay at exactly λ from every state that can survive;
and one price per cell on rotation-invariant tori.
-/
import GumpMath.LinkSurv
import GumpMath.ChainTorus
import GumpMath.DiceTorusReg

set_option linter.unusedSectionVars false

namespace Gump.Link.Wrapped
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Chain.Kagome Gump.Link Finset

/-! ### The hypothesis -/

/-- The six kagome neighbours of a cell of orientation o, as (orientation, Δa, Δb) (`ChainKagome.nbrs`). -/
def offs : ℕ → List (ℕ × ℤ × ℤ)
  | 0 => [(0, -1, 1), (0, 1, -1), (1, 0, 0), (1, 1, 0), (2, 0, 0), (2, 0, 1)]
  | 1 => [(1, 0, 1), (1, 0, -1), (0, 0, 0), (0, -1, 0), (2, 0, 0), (2, -1, 1)]
  | _ => [(2, 1, 0), (2, -1, 0), (0, 0, 0), (0, 0, -1), (1, 0, 0), (1, 1, -1)]

/-- The index of the cell of orientation o at (a, b), reduced to the fundamental domain by the dice agent's `Tr`. -/
def idx (H K D : ℕ) (o : ℕ) (a b : ℤ) : ℕ :=
  (((Tr H K D a b).1 * D + (Tr H K D a b).2) * 3 + o).toNat

/-- The kagome neighbour indices of cell i = 3(aD + b) + o. -/
def kIdx (H K D i : ℕ) : List ℕ :=
  (offs (i % 3)).map fun v => idx H K D v.1 (((i / 3 / D : ℕ) : ℤ) + v.2.1) (((i / 3 % D : ℕ) : ℤ) + v.2.2)

/-- **The hypothesis of the general theorem**: the wrapped face `torus H K D` has 3HD cells, and its
neighbour lists are, up to order, those of the kagome layer. -/
def TorusNb (H K D : ℕ) : Prop :=
  (torus H K D).A = 3 * H * D ∧ ∀ i < 3 * H * D, ((torus H K D).nb i).Perm (kIdx H K D i)

/-- The same, as a Boolean the kernel can evaluate. -/
def torusNbB (H K D : ℕ) : Bool :=
  (torus H K D).A == 3 * H * D &&
    (List.range (3 * H * D)).all fun i => ((torus H K D).nb i).isPerm (kIdx H K D i)

theorem torusNb_of {H K D : ℕ} (h : torusNbB H K D = true) : TorusNb H K D := by
  simp only [torusNbB, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, List.mem_range] at h
  exact ⟨h.1, fun i hi => List.isPerm_iff.1 (h.2 i hi)⟩

/-! ### The cells -/

section Cells
variable (H K D : ℕ)

def orientOf : ℕ → Orient
  | 0 => .X
  | 1 => .Y
  | _ => .Z

/-- Cell i = 3(aD + b) + o of the dice agent's list, as a cell of the kagome layer. -/
def phi (i : ℕ) : Cell (Torus (H : ℤ) K D) :=
  (orientOf (i % 3), QuotientAddGroup.mk (((i / 3 / D : ℕ) : ℤ), ((i / 3 % D : ℕ) : ℤ)))

theorem mk_off (a b da db : ℤ) :
    (QuotientAddGroup.mk (a + da, b + db) : Torus (H : ℤ) K D) =
      QuotientAddGroup.mk (a, b) + da • te1 H K D + db • te2 H K D := by
  unfold te1 te2
  rw [← QuotientAddGroup.mk_zsmul, ← QuotientAddGroup.mk_zsmul, ← QuotientAddGroup.mk_add,
    ← QuotientAddGroup.mk_add]
  congr 1
  ext <;> simp

theorem phi_idx (hH : 0 < H) (hD : 0 < D) (o : ℕ) (ho : o < 3) (a b : ℤ) :
    phi H K D (idx H K D o a b) = (orientOf o, QuotientAddGroup.mk (a, b)) := by
  have hH' : (0 : ℤ) < H := by exact_mod_cast hH
  have hD' : (0 : ℤ) < D := by exact_mod_cast hD
  have h0a : 0 ≤ (Tr H K D a b).1 := Int.emod_nonneg _ hH'.ne'
  have h1a : (Tr H K D a b).1 < H := Int.emod_lt_of_pos _ hH'
  have h0b : 0 ≤ (Tr H K D a b).2 := Int.emod_nonneg _ hD'.ne'
  have h1b : (Tr H K D a b).2 < D := Int.emod_lt_of_pos _ hD'
  obtain ⟨a0, ha0⟩ : ∃ n : ℕ, (n : ℤ) = (Tr H K D a b).1 := ⟨_, Int.toNat_of_nonneg h0a⟩
  obtain ⟨b0, hb0⟩ : ∃ n : ℕ, (n : ℤ) = (Tr H K D a b).2 := ⟨_, Int.toNat_of_nonneg h0b⟩
  have hb0D : b0 < D := by omega
  have hidx : idx H K D o a b = (a0 * D + b0) * 3 + o := by
    unfold idx; rw [← ha0, ← hb0]; omega
  have h3 : ((a0 * D + b0) * 3 + o) / 3 = a0 * D + b0 := by omega
  have hm3 : ((a0 * D + b0) * 3 + o) % 3 = o := by omega
  have hdiv : (a0 * D + b0) / D = a0 := by
    rw [mul_comm, Nat.mul_add_div hD, Nat.div_eq_of_lt hb0D, add_zero]
  have hmod : (a0 * D + b0) % D = b0 := by
    rw [mul_comm, Nat.mul_add_mod, Nat.mod_eq_of_lt hb0D]
  unfold phi
  rw [hidx, h3, hm3, hdiv, hmod]
  congr 1
  apply QuotientAddGroup.eq.2
  obtain ⟨s, t, hst⟩ := Tr_sub H K D a b
  rw [← ha0, ← hb0] at hst
  refine AddSubgroup.mem_closure_pair.2 ⟨s, t, ?_⟩
  rw [hst]
  ext <;> simp <;> ring

theorem offs_lt (o : ℕ) : ∀ v ∈ offs o, v.1 < 3 := by
  intro v hv
  match o with
  | 0 => simp only [offs, List.mem_cons, List.not_mem_nil, or_false] at hv; rcases hv with h|h|h|h|h|h <;> simp [h]
  | 1 => simp only [offs, List.mem_cons, List.not_mem_nil, or_false] at hv; rcases hv with h|h|h|h|h|h <;> simp [h]
  | n + 2 => simp only [offs, List.mem_cons, List.not_mem_nil, or_false] at hv; rcases hv with h|h|h|h|h|h <;> simp [h]

/-- **The kagome neighbours of cell i are the cells `kIdx i`**, for every H, K, D (H, D > 0). -/
theorem kIdx_map (hH : 0 < H) (hD : 0 < D) (i : ℕ) :
    (kIdx H K D i).map (phi H K D) = Kagome.nbrs (te1 H K D) (te2 H K D) (phi H K D i) := by
  unfold kIdx
  rw [List.map_map]
  rw [List.map_congr_left (fun v hv => by
    show phi H K D (idx H K D v.1 _ _) = _
    rw [phi_idx H K D hH hD v.1 (offs_lt _ v hv)])]
  obtain h | h | h : i % 3 = 0 ∨ i % 3 = 1 ∨ i % 3 = 2 := by omega
  all_goals
    simp only [phi, h, offs, orientOf, List.map_cons, List.map_nil, Kagome.nbrs, mk_off, List.cons.injEq,
      Prod.mk.injEq, true_and, and_true]
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> module

theorem phi_inj (hD : 0 < D) {i j : ℕ} (hi : i < 3 * H * D) (hj : j < 3 * H * D) (h : phi H K D i = phi H K D j) :
    i = j := by
  have hH : 0 < H := by
    rcases Nat.eq_zero_or_pos H with h0 | h0
    · subst h0; simp at hi
    · exact h0
  unfold phi at h
  rw [Prod.mk.injEq] at h
  obtain ⟨ho, hp⟩ := h
  have hm : i % 3 = j % 3 := by
    have hi3 : i % 3 < 3 := Nat.mod_lt _ (by norm_num)
    have hj3 : j % 3 < 3 := Nat.mod_lt _ (by norm_num)
    interval_cases (i % 3) <;> interval_cases (j % 3) <;> first | rfl | (simp [orientOf] at ho)
  have hiH : i / 3 / D < H := by
    rw [Nat.div_div_eq_div_mul, Nat.div_lt_iff_lt_mul (by positivity)]; linarith
  have hjH : j / 3 / D < H := by
    rw [Nat.div_div_eq_div_mul, Nat.div_lt_iff_lt_mul (by positivity)]; linarith
  have hHn : ((H : ℤ)).toNat = H := Int.toNat_natCast H
  have hDn : ((D : ℤ)).toNat = D := Int.toNat_natCast D
  have hinj := (torusRep_bijective (H : ℤ) K D (by exact_mod_cast hH) (by exact_mod_cast hD)).1
  have := @hinj (⟨i / 3 / D, by rw [hHn]; exact hiH⟩, ⟨i / 3 % D, by rw [hDn]; exact Nat.mod_lt _ hD⟩)
    (⟨j / 3 / D, by rw [hHn]; exact hjH⟩, ⟨j / 3 % D, by rw [hDn]; exact Nat.mod_lt _ hD⟩) hp
  simp only [Prod.mk.injEq, Fin.mk.injEq] at this
  have e1 := Nat.div_add_mod (i / 3) D
  have e2 := Nat.div_add_mod (j / 3) D
  rw [this.1, this.2] at e1
  omega

variable [Fintype (Torus (H : ℤ) K D)] [DecidableEq (Torus (H : ℤ) K D)]

theorem card_cell (hH : 0 < H) (hD : 0 < D) : Fintype.card (Cell (Torus (H : ℤ) K D)) = 3 * H * D := by
  have h := torus_card (H : ℤ) K D (by exact_mod_cast hH) (by exact_mod_cast hD)
  rw [Fintype.card_prod, card_orient]
  have : Fintype.card (Torus (H : ℤ) K D) = H * D := by exact_mod_cast h
  rw [this]; ring

/-- **The cells of the wrapped face are the cells of the kagome layer.** -/
noncomputable def cellEquiv (hH : 0 < H) (hD : 0 < D) (hA : (torus H K D).A = 3 * H * D) :
    Fin (torus H K D).A ≃ Cell (Torus (H : ℤ) K D) :=
  Equiv.ofBijective (fun i => phi H K D i)
    ((Fintype.bijective_iff_injective_and_card _).2
      ⟨fun i j h => Fin.ext (phi_inj H K D hD (hA ▸ i.2) (hA ▸ j.2) h),
        by rw [Fintype.card_fin, card_cell H K D hH hD, hA]⟩)

theorem cellEquiv_apply (hH : 0 < H) (hD : 0 < D) (hA : (torus H K D).A = 3 * H * D) (i : Fin (torus H K D).A) :
    cellEquiv H K D hH hD hA i = phi H K D i := rfl

end Cells

/-! ### The states -/

section States
variable (F : Face) {V : Type*} [Fintype V] [DecidableEq V] (f : Fin F.A ≃ V)

/-- A state of the face as the set of its live cells. -/
def E (x : Fin (2 ^ F.A)) : Finset V := univ.filter (fun c => (x : ℕ).testBit (f.symm c))

theorem mem_E (x : Fin (2 ^ F.A)) (i : Fin F.A) : f i ∈ E F f x ↔ (x : ℕ).testBit i = true := by
  simp [E]

theorem high_bits (x : Fin (2 ^ F.A)) (j : ℕ) (hj : F.A ≤ j) : (x : ℕ).testBit j = false :=
  Nat.testBit_lt_two_pow (lt_of_lt_of_le x.isLt (Nat.pow_le_pow_right (by norm_num) hj))

theorem E_inj : Function.Injective (E F f) := by
  intro x y h
  apply Fin.ext
  apply Nat.eq_of_testBit_eq
  intro j
  by_cases hj : j < F.A
  · have := congrArg (fun s => f ⟨j, hj⟩ ∈ s) h
    simp only [mem_E, eq_iff_iff] at this
    cases hx : (x : ℕ).testBit j <;> cases hy : (y : ℕ).testBit j <;> simp_all
  · rw [high_bits F x j (by omega), high_bits F y j (by omega)]

theorem E_bij : Function.Bijective (E F f) :=
  (Fintype.bijective_iff_injective_and_card _).2 ⟨E_inj F f, by
    rw [Fintype.card_fin, Fintype.card_finset, ← Fintype.card_congr f, Fintype.card_fin]⟩

theorem E_empty_iff (x : Fin (2 ^ F.A)) : (E F f x).Nonempty ↔ x ≠ F.empty := by
  rw [ne_eq, empty_iff, Finset.nonempty_iff_ne_empty, ne_eq, not_iff_not]
  constructor
  · intro h
    apply Nat.eq_of_testBit_eq
    intro j
    rw [Nat.zero_testBit]
    by_cases hj : j < F.A
    · have : f ⟨j, hj⟩ ∉ E F f x := by rw [h]; exact Finset.notMem_empty _
      rw [mem_E] at this
      simpa using this
    · exact high_bits F x j (by omega)
  · intro h
    apply Finset.eq_empty_of_forall_notMem
    intro c hc
    have := (mem_E F f x (f.symm c)).1 (by simpa using hc)
    rw [h, Nat.zero_testBit] at this
    exact Bool.false_ne_true this

/-- **The living states of the face are the non-empty sets of cells.** -/
noncomputable def stateEquiv : {x : Fin (2 ^ F.A) // x ≠ F.empty} ≃ Living V :=
  Equiv.subtypeEquiv (Equiv.ofBijective (E F f) (E_bij F f)) (fun x => (E_empty_iff F f x).symm)

theorem stateEquiv_val (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}) : (stateEquiv F f x).1 = E F f x := rfl

end States

/-! ### Relabelling a killed chain -/

section Transport
variable {σ σ' : Type*} [Fintype σ] [DecidableEq σ] [Fintype σ'] [DecidableEq σ']
variable {K : KilledChain σ} {K' : KilledChain σ'} (e : σ ≃ σ') (hQ : ∀ x y, K'.Q (e x) (e y) = K.Q x y)
include hQ

theorem transport_qsd {ν : σ' → ℝ} {lam : ℝ} (h : K'.IsQSD ν lam) : K.IsQSD (fun x => ν (e x)) lam := by
  refine ⟨fun x => h.nonneg _, ?_, fun y => ?_⟩
  · rw [Equiv.sum_comp e ν]; exact h.total
  · have := h.eigen (e y)
    rw [← Equiv.sum_comp e] at this
    simpa [hQ] using this

theorem transport_qsd' {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) : K'.IsQSD (fun x => μ (e.symm x)) lam := by
  refine transport_qsd e.symm (fun x y => ?_) h
  rw [← hQ, Equiv.apply_symm_apply, Equiv.apply_symm_apply]

theorem transport_survFrom (t : ℕ) (x : σ) : K.survFrom t x = K'.survFrom t (e x) := by
  induction t generalizing x with
  | zero => rw [survFrom_zero, survFrom_zero]
  | succ t ih =>
    rw [survFrom_succ', survFrom_succ', ← Equiv.sum_comp e]
    exact sum_congr rfl (fun y _ => by rw [hQ, ih])

theorem transport_canSurvive (x : σ) : K.CanSurvive x ↔ K'.CanSurvive (e x) := by
  constructor
  · rintro ⟨y, hy⟩; exact ⟨e y, by rw [hQ]; exact hy⟩
  · rintro ⟨y, hy⟩; exact ⟨e.symm y, by rw [← hQ, Equiv.apply_symm_apply]; exact hy⟩

theorem transport_price {V V' : Type*} [Fintype V] [Fintype V'] (L : K.LocalDeath V) (L' : K'.LocalDeath V')
    (g : V ≃ V') (hc : ∀ i x, L'.dc (g i) (e x) = L.dc i x) (ν : σ' → ℝ) (i : V) :
    L.price (fun x => ν (e x)) i = L'.price ν (g i) := by
  have hE : ∀ x, L'.energy (e x) = L.energy x := fun x => by
    simp only [KilledChain.LocalDeath.energy, KilledChain.LocalDeath.cost]
    rw [← Equiv.sum_comp g]
    simp [hc]
  have hcost : ∀ x, L'.cost (g i) (e x) = L.cost i x := fun x => by simp [KilledChain.LocalDeath.cost, hc]
  simp only [KilledChain.LocalDeath.price]
  congr 1; funext s
  simp only [tiltMean, Z, tw]
  rw [← Equiv.sum_comp e (fun x => ν x * Real.exp (-(s * L'.energy x)) * L'.cost (g i) x),
    ← Equiv.sum_comp e (fun x => ν x * Real.exp (-(s * L'.energy x)))]
  simp only [hE, hcost]

end Transport

end Gump.Link.Wrapped
