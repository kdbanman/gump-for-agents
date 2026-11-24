/-
**`TorusNb H K D` for every H, D > 0** (`torusNb_all`), so `wrapped_full` holds on every wrapped face with no
hypothesis left (`wrapped_full_all`).

The proof reads the dice agent's definitions directly: cell i of `gridCells H D` is the cell of orientation i mod 3
at (⌊i/3⌋ div D, ⌊i/3⌋ mod D) (`grid_getElem?`), so that cell's index is 3(aD + b) + o (`idxOf_grid`); the
in-layer neighbours of the cell (o, a, b) are six cells (o', a + Δa, b + Δb) (`inlayer`, one list per
orientation, in the order of `Gump.offsets`), each reduced by `Tr` (`torus_red`); and that list of six is a
permutation of the kagome list `offs` (decided).
-/
import GumpMath.LinkWrappedCheck

set_option linter.unusedSectionVars false

namespace Gump.Link.Wrapped
open Gump Gump.Dice

/-! ### Cells of `gridCells` by index -/

theorem flatMap_getElem? {α : Type*} (g : ℕ → List α) (n : ℕ) (hg : ∀ a, (g a).length = n) :
    ∀ W i, i < W * n → ((List.range W).flatMap g)[i]? = (g (i / n))[i % n]? := by
  intro W
  induction W with
  | zero => intro i hi; simp at hi
  | succ W ih =>
    intro i hi
    have hlen : ((List.range W).flatMap g).length = W * n := by
      rw [List.length_flatMap]; simp [hg]
    rw [List.range_succ, List.flatMap_append, List.flatMap_singleton]
    by_cases h : i < W * n
    · rw [List.getElem?_append_left (by rw [hlen]; exact h), ih i h]
    · push Not at h
      rw [List.getElem?_append_right (by rw [hlen]; exact h), hlen]
      have hq : i / n = W := Nat.div_eq_of_lt_le h hi
      have hr : i % n = i - W * n := by
        have := Nat.div_add_mod i n
        rw [hq, mul_comm, add_comm] at this
        exact Nat.eq_sub_of_add_eq this
      rw [hq, hr]

theorem length_grid (H D : ℕ) : (gridCells H D).length = 3 * H * D := by
  unfold gridCells
  simp [List.length_flatMap]
  ring

theorem grid_getElem? (H D i : ℕ) (hD : 0 < D) (hi : i < 3 * H * D) :
    (gridCells H D)[i]? = some (abCell (i % 3) ((i / 3 / D : ℕ) : ℤ) ((i / 3 % D : ℕ) : ℤ)) := by
  unfold gridCells
  rw [flatMap_getElem? _ (3 * D) (fun a => by simp [List.length_flatMap]; ring) H i (by linarith)]
  have hj : i % (3 * D) < D * 3 := by rw [mul_comm D]; exact Nat.mod_lt _ (by positivity)
  rw [flatMap_getElem? _ 3 (fun b => by simp) D _ hj, List.getElem?_map,
    List.getElem?_range (Nat.mod_lt _ (by norm_num))]
  simp only [Option.map_some]
  rw [Nat.mod_mod_of_dvd _ (Dvd.intro D rfl), Nat.mod_mul_right_div_self, Nat.div_div_eq_div_mul]

theorem idxOf_grid (H D : ℕ) (hD : 0 < D) (o : ℕ) (ho : o < 3) (a b : ℕ) (ha : a < H) (hb : b < D) :
    (gridCells H D).idxOf? (abCell o (a : ℤ) (b : ℤ)) = some ((a * D + b) * 3 + o) := by
  have hn : (a * D + b) * 3 + o < 3 * H * D := by
    have : a * D + b < H * D := by
      calc a * D + b < a * D + D := by omega
        _ = (a + 1) * D := by ring
        _ ≤ H * D := Nat.mul_le_mul_right _ ha
    have h2 : (a * D + b) * 3 + o < H * D * 3 := by omega
    calc (a * D + b) * 3 + o < H * D * 3 := h2
      _ = 3 * H * D := by ring
  have hl : (a * D + b) * 3 + o < (gridCells H D).length := by rw [length_grid]; exact hn
  rw [idxOf?_nodup (gridCells_nodup H D) hl]
  have h := grid_getElem? H D _ hD hn
  rw [List.getElem?_eq_getElem hl, Option.some.injEq] at h
  rw [h]
  have h3 : ((a * D + b) * 3 + o) / 3 = a * D + b := by omega
  have hm3 : ((a * D + b) * 3 + o) % 3 = o := by omega
  have hdiv : (a * D + b) / D = a := by
    rw [mul_comm, Nat.mul_add_div hD, Nat.div_eq_of_lt hb, add_zero]
  have hmod : (a * D + b) % D = b := by
    rw [mul_comm, Nat.mul_add_mod, Nat.mod_eq_of_lt hb]
  rw [h3, hm3, hdiv, hmod]

/-! ### The in-layer neighbours of a cell -/

/-- The in-layer neighbours of the cell of orientation o, as (orientation, Δa, Δb), in the order of
`Gump.offsets`. -/
def DL : ℕ → List (ℕ × ℤ × ℤ)
  | 0 => [(0, -1, 1), (0, 1, -1), (1, 1, 0), (1, 0, 0), (2, 0, 1), (2, 0, 0)]
  | 1 => [(1, 0, 1), (1, 0, -1), (0, -1, 0), (0, 0, 0), (2, -1, 1), (2, 0, 0)]
  | _ => [(2, 1, 0), (2, -1, 0), (0, 0, -1), (0, 0, 0), (1, 1, -1), (1, 0, 0)]

theorem DL_perm (o : ℕ) : (DL o).Perm (offs o) := by
  match o with
  | 0 => decide
  | 1 => decide
  | n + 2 => show (DL 2).Perm (offs 2); decide

theorem DL_lt (o : ℕ) : ∀ w ∈ DL o, w.1 < 3 := by
  intro w hw
  match o with
  | 0 => simp only [DL, List.mem_cons, List.not_mem_nil, or_false] at hw; rcases hw with h|h|h|h|h|h <;> simp [h]
  | 1 => simp only [DL, List.mem_cons, List.not_mem_nil, or_false] at hw; rcases hw with h|h|h|h|h|h <;> simp [h]
  | n + 2 => simp only [DL, List.mem_cons, List.not_mem_nil, or_false] at hw; rcases hw with h|h|h|h|h|h <;> simp [h]

theorem inlayer (o : ℕ) (ho : o < 3) (a b : ℤ) :
    (nbrs (abCell o a b)).filterMap (fun q => if d111.dot q = d111.dot (abCell o a b) then some q else none) =
      (DL o).map (fun w => abCell w.1 (a + w.2.1) (b + w.2.2)) := by
  unfold nbrs
  rw [axis_abCell, List.filterMap_map]
  simp only [Function.comp, Diag.dot_add, add_eq_left]
  interval_cases o
  all_goals
    simp only [abCell, Pt.axis, offsets, DL, List.map_cons, List.map_nil]
    norm_num [Diag.dot, d111, sg, List.filterMap_cons]
    and_intros
    all_goals (apply Pt.ext' <;> simp <;> ring)

/-! ### The general bijection -/

theorem nb_eq (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (i : ℕ) (hi : i < 3 * H * D) :
    (torus H K D).nb i = (DL (i % 3)).map
      (fun v => idx H K D v.1 (((i / 3 / D : ℕ) : ℤ) + v.2.1) (((i / 3 % D : ℕ) : ℤ) + v.2.2)) := by
  have hc : (torus H K D).cell i = abCell (i % 3) ((i / 3 / D : ℕ) : ℤ) ((i / 3 % D : ℕ) : ℤ) := by
    unfold Face.cell
    rw [List.getD_eq_getElem?_getD]
    show ((gridCells H D)[i]?).getD _ = _
    rw [grid_getElem? H D i hD hi]; rfl
  have e : (torus H K D).nb i = (nbrs ((torus H K D).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((torus H K D).cell i) then (gridCells H D).idxOf? ((torus H K D).red q) else none :=
    rfl
  rw [e, hc]
  have hsplit : ∀ (l : List Pt) (c : Pt → Prop) [DecidablePred c] (g : Pt → Option ℕ),
      l.filterMap (fun q => if c q then g q else none) =
        (l.filterMap (fun q => if c q then some q else none)).filterMap g := by
    intro l c _ g
    rw [List.filterMap_filterMap]
    congr 1; funext q
    split_ifs <;> rfl
  rw [hsplit, inlayer _ (Nat.mod_lt _ (by norm_num)), List.filterMap_map]
  rw [← List.filterMap_eq_map]
  refine List.filterMap_congr (fun w hw => ?_)
  have hw3 := DL_lt _ w hw
  simp only [Function.comp]
  rw [torus_red, axisIdx_abCell _ hw3, coordA_abCell _ hw3, coordB_abCell _ hw3]
  have hH' : (0 : ℤ) < H := by exact_mod_cast hH
  have hD' : (0 : ℤ) < D := by exact_mod_cast hD
  set A0 := (((i / 3 / D : ℕ) : ℤ) + w.2.1)
  set B0 := (((i / 3 % D : ℕ) : ℤ) + w.2.2)
  have h0a : 0 ≤ (Tr H K D A0 B0).1 := Int.emod_nonneg _ hH'.ne'
  have h1a : (Tr H K D A0 B0).1 < H := Int.emod_lt_of_pos _ hH'
  have h0b : 0 ≤ (Tr H K D A0 B0).2 := Int.emod_nonneg _ hD'.ne'
  have h1b : (Tr H K D A0 B0).2 < D := Int.emod_lt_of_pos _ hD'
  obtain ⟨a0, ha0⟩ : ∃ n : ℕ, (n : ℤ) = (Tr H K D A0 B0).1 := ⟨_, Int.toNat_of_nonneg h0a⟩
  obtain ⟨b0, hb0⟩ : ∃ n : ℕ, (n : ℤ) = (Tr H K D A0 B0).2 := ⟨_, Int.toNat_of_nonneg h0b⟩
  rw [← ha0, ← hb0, idxOf_grid H D hD w.1 hw3 a0 b0 (by omega) (by omega)]
  unfold idx
  rw [← ha0, ← hb0]
  first
  | rfl
  | (congr 1; omega)

/-- **The general bijection**: on every wrapped face (H, D > 0) the dice agent's neighbour lists are those of
the kagome layer, up to order. -/
theorem torusNb_all (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) : TorusNb H K D := by
  refine ⟨length_grid H D, fun i hi => ?_⟩
  rw [nb_eq H K D hH hD i hi]
  unfold kIdx
  exact (DL_perm _).map _

end Gump.Link.Wrapped
