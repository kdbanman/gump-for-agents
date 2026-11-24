/-
**The triangle's symmetries on every hull face** (`rot_aut`, `refl_aut`): the rotation (x,y,z) ↦ (y,z,x) and the
reflection (x,y,z) ↦ (y,x,z), acting on the cells of `hull R` by `idxOf`, are automorphisms of the tables
(`autOK`) for every R. Hence on every hull face the prices are equal along the six symmetries of the triangle
(`hull_prices_sym`), with no hypothesis.

The general step (`aut_general`): a map of points that is additive, keeps d·p, the hull and the corners, is
injective and carries each cell's twelve offsets to those of its image (up to order) is an automorphism.
-/
import GumpMath.LinkHullGen

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace Gump.Link.HullGen
open Gump Gump.Dice Gump.Link Finset

variable (R : ℕ)

/-- The action of a map of points on the cells of `hull R`. -/
def gList (g : Pt → Pt) : List ℕ :=
  (List.range (Gump.Dice.hull R).A).map fun i => (Gump.Dice.hullCells R).idxOf (g ((Gump.Dice.hull R).cell i))

theorem idx_lt (q : Pt) (hq : q ∈ Gump.Dice.hullCells R) : (Gump.Dice.hullCells R).idxOf q < (Gump.Dice.hull R).A :=
  List.idxOf_lt_length_of_mem hq

theorem cell_idx (q : Pt) (hq : q ∈ Gump.Dice.hullCells R) :
    (Gump.Dice.hull R).cell ((Gump.Dice.hullCells R).idxOf q) = q := by
  rw [Face.hull_cell_eq R _ (idx_lt R q hq)]
  exact List.getElem_idxOf (idx_lt R q hq)

theorem idxOf?_mem (q : Pt) (hq : q ∈ Gump.Dice.hullCells R) :
    (Gump.Dice.hullCells R).idxOf? q = some ((Gump.Dice.hullCells R).idxOf q) :=
  (idxOf?_nodup (Gump.Dice.hullCells_nodup R) (idx_lt R q hq)).2 (List.getElem_idxOf (idx_lt R q hq))

theorem idxOf?_not (q : Pt) (hq : q ∉ Gump.Dice.hullCells R) : (Gump.Dice.hullCells R).idxOf? q = none := by
  rw [List.idxOf?_eq_none_iff]; exact hq

theorem gList_getD (g : Pt → Pt) (i : ℕ) (hi : i < (Gump.Dice.hull R).A) :
    (gList R g).getD i 0 = (Gump.Dice.hullCells R).idxOf (g ((Gump.Dice.hull R).cell i)) := by
  unfold gList
  rw [List.getD_eq_getElem _ _ (by simp [hi]), List.getElem_map, List.getElem_range]

/-- **A map of points with the hull's symmetries is an automorphism of the tables.** -/
theorem aut_general (g : Pt → Pt) (hadd : ∀ p q, g (p + q) = g p + g q)
    (hdot : ∀ p, d111.dot (g p) = d111.dot p)
    (hmem : ∀ p, g p ∈ Gump.Dice.hullCells R ↔ p ∈ Gump.Dice.hullCells R)
    (hcor : ∀ p, corner (g p) ↔ corner p) (hinj : Function.Injective g)
    (hoff : ∀ p ∈ Gump.Dice.hullCells R, (offsets (g p).axis).Perm ((offsets p.axis).map g)) :
    autOK (Gump.Dice.hull R) (gList R g) = true := by
  have hlen : (gList R g).length = (Gump.Dice.hull R).A := by simp [gList]
  have hlt : ∀ i < (Gump.Dice.hull R).A, (gList R g).getD i 0 < (Gump.Dice.hull R).A := fun i hi => by
    rw [gList_getD R g i hi]
    exact idx_lt R _ ((hmem _).2 (Face.hull_cell_mem R i hi))
  have hnd : (gList R g).Nodup := by
    unfold gList
    refine (List.nodup_range).map_on fun i hi j hj e => ?_
    rw [List.mem_range] at hi hj
    have hci := (hmem _).2 (Face.hull_cell_mem R i hi)
    have hcj := (hmem _).2 (Face.hull_cell_mem R j hj)
    have := congrArg (Gump.Dice.hull R).cell e
    rw [cell_idx R _ hci, cell_idx R _ hcj] at this
    exact cell_inj R hi hj (hinj this)
  have hperm : ∀ i < (Gump.Dice.hull R).A,
      (((Gump.Dice.hull R).nb i).map ((gList R g).getD · 0)).Perm
        ((Gump.Dice.hull R).nb ((gList R g).getD i 0)) := by
    intro i hi
    set p := (Gump.Dice.hull R).cell i with hpdef
    have hp : p ∈ Gump.Dice.hullCells R := Face.hull_cell_mem R i hi
    have hgp : g p ∈ Gump.Dice.hullCells R := (hmem p).2 hp
    rw [gList_getD R g i hi]
    have e1 : (Gump.Dice.hull R).nb i = (nbrs p).filterMap fun q =>
        if d111.dot q = d111.dot p then (Gump.Dice.hullCells R).idxOf? q else none := rfl
    have e2 : (Gump.Dice.hull R).nb ((Gump.Dice.hullCells R).idxOf (g p)) = (nbrs (g p)).filterMap fun q =>
        if d111.dot q = d111.dot (g p) then (Gump.Dice.hullCells R).idxOf? q else none := by
      show (nbrs ((Gump.Dice.hull R).cell _)).filterMap _ = _
      rw [cell_idx R _ hgp]
      rfl
    rw [e1, e2, List.map_filterMap]
    have key : ((nbrs p).filterMap fun q => Option.map ((gList R g).getD · 0)
        (if d111.dot q = d111.dot p then (Gump.Dice.hullCells R).idxOf? q else none)) =
        ((nbrs p).map g).filterMap fun q =>
          if d111.dot q = d111.dot (g p) then (Gump.Dice.hullCells R).idxOf? q else none := by
      rw [List.filterMap_map]
      refine List.filterMap_congr fun q _ => ?_
      simp only [Function.comp, hdot]
      by_cases hd : d111.dot q = d111.dot p
      · rw [if_pos hd, if_pos hd]
        by_cases hq : q ∈ Gump.Dice.hullCells R
        · rw [idxOf?_mem R q hq, idxOf?_mem R (g q) ((hmem q).2 hq), Option.map_some,
            gList_getD R g _ (idx_lt R q hq), cell_idx R q hq]
        · rw [idxOf?_not R q hq, idxOf?_not R (g q) (fun h => hq ((hmem q).1 h)), Option.map_none]
      · rw [if_neg hd, if_neg hd, Option.map_none]
    rw [key]
    refine List.Perm.filterMap _ ?_
    have : (nbrs p).map g = ((offsets p.axis).map g).map (g p + ·) := by
      unfold nbrs; rw [List.map_map, List.map_map]
      exact List.map_congr_left fun v _ => hadd p v
    rw [this]
    exact ((hoff p hp).map (g p + ·)).symm
  have hm : ∀ i < (Gump.Dice.hull R).A,
      (Gump.Dice.hull R).m1 ((gList R g).getD i 0) = (Gump.Dice.hull R).m1 i ∧
      (Gump.Dice.hull R).m2 ((gList R g).getD i 0) = (Gump.Dice.hull R).m2 i := by
    intro i hi
    have hgp := (hmem _).2 (Face.hull_cell_mem R i hi)
    have hj := hlt i hi
    refine ⟨by rw [(Gump.Dice.hull_cells R _ hj).1, (Gump.Dice.hull_cells R i hi).1], ?_⟩
    rw [m2_eq R _ hj, m2_eq R i hi, gList_getD R g i hi, cell_idx R _ hgp]
    by_cases hc : corner ((Gump.Dice.hull R).cell i)
    · rw [if_pos ((hcor _).2 hc), if_pos hc]
    · rw [if_neg (fun h => hc ((hcor _).1 h)), if_neg hc]
  unfold autOK
  simp only [Bool.and_eq_true, beq_iff_eq, List.all_eq_true, List.mem_range, decide_eq_true_eq]
  exact ⟨⟨⟨hlen, hlt⟩, hnd⟩, fun i hi => ⟨⟨List.isPerm_iff.2 (hperm i hi), (hm i hi).1⟩, (hm i hi).2⟩⟩

/-- The rotation of the triangle. -/
def rot (p : Pt) : Pt := ⟨p.y, p.z, p.x⟩
/-- The reflection of the triangle. -/
def refl (p : Pt) : Pt := ⟨p.y, p.x, p.z⟩

theorem rot_aut : autOK (Gump.Dice.hull R) (gList R rot) = true := by
  refine aut_general R rot (fun p q => rfl) (fun p => ?_) (fun p => ?_) (fun p => ?_) (fun p q h => ?_)
    (fun p hp => ?_)
  · simp only [rot, Diag.dot, d111, sg, ite_true]; ring
  · obtain ⟨x, y, z⟩ := p; simp only [rot, mem_hull_iff]; omega
  · obtain ⟨x, y, z⟩ := p; simp only [rot, corner]; omega
  · obtain ⟨a, b, c⟩ := p; obtain ⟨d, e, f⟩ := q; simp only [rot, Pt.mk.injEq] at h ⊢; omega
  · obtain ⟨x, y, z⟩ := p
    rw [mem_hull_iff] at hp
    obtain ⟨-, -, -, -, hpar⟩ := hp
    rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
    · rw [show rot ⟨x, y, z⟩ = ⟨y, z, x⟩ from rfl, axis_Z _ _ _ hy hz, axis_X _ _ _ hx]; decide
    · rw [show rot ⟨x, y, z⟩ = ⟨y, z, x⟩ from rfl, axis_X _ _ _ hy, axis_Y _ _ _ hx hy]; decide
    · rw [show rot ⟨x, y, z⟩ = ⟨y, z, x⟩ from rfl, axis_Y _ _ _ hy hz, axis_Z _ _ _ hx hy]; decide

theorem refl_aut : autOK (Gump.Dice.hull R) (gList R refl) = true := by
  refine aut_general R refl (fun p q => rfl) (fun p => ?_) (fun p => ?_) (fun p => ?_) (fun p q h => ?_)
    (fun p hp => ?_)
  · simp only [refl, Diag.dot, d111, sg, ite_true]; ring
  · obtain ⟨x, y, z⟩ := p; simp only [refl, mem_hull_iff]; omega
  · obtain ⟨x, y, z⟩ := p; simp only [refl, corner]; omega
  · obtain ⟨a, b, c⟩ := p; obtain ⟨d, e, f⟩ := q; simp only [refl, Pt.mk.injEq] at h ⊢; omega
  · obtain ⟨x, y, z⟩ := p
    rw [mem_hull_iff] at hp
    obtain ⟨-, -, -, -, hpar⟩ := hp
    rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
    · rw [show refl ⟨x, y, z⟩ = ⟨y, x, z⟩ from rfl, axis_Y _ _ _ hy hx, axis_X _ _ _ hx]; decide
    · rw [show refl ⟨x, y, z⟩ = ⟨y, x, z⟩ from rfl, axis_X _ _ _ hy, axis_Y _ _ _ hx hy]; decide
    · rw [show refl ⟨x, y, z⟩ = ⟨y, x, z⟩ from rfl, axis_Z _ _ _ hy hx, axis_Z _ _ _ hx hy]; decide

end Gump.Link.HullGen

namespace Gump.Link
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Finset

theorem autPerm_gList (R : ℕ) (g : Pt → Pt) (hπ : autOK (Gump.Dice.hull R) (HullGen.gList R g) = true)
    (hmem : ∀ p, g p ∈ Gump.Dice.hullCells R ↔ p ∈ Gump.Dice.hullCells R)
    (i j : Fin (Gump.Dice.hull R).A) (h : (Gump.Dice.hull R).cell j = g ((Gump.Dice.hull R).cell i)) :
    autPerm hπ i = j := by
  apply Fin.ext
  rw [autPerm_val, HullGen.gList_getD R g i i.2]
  have hgp := (hmem _).2 (Face.hull_cell_mem R i i.2)
  apply HullGen.cell_inj R (HullGen.idx_lt R _ hgp) j.2
  rw [HullGen.cell_idx R _ hgp, h]

/-- **Equal prices along the triangle's six symmetries, on every hull face** (every R with A > 0, no
hypothesis): for the quasi-stationary law of `Face.P` with λ > 0 (unique, `hull_full_every`), c_j = c_i whenever
cell j is the rotation (x,y,z) ↦ (y,z,x) or the reflection (x,y,z) ↦ (y,x,z) of cell i; these generate the six. -/
theorem hull_prices_sym (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A)
    (μ : {x : Fin (2 ^ (Gump.Dice.hull R).A) // x ≠ (Gump.Dice.hull R).empty} → ℝ) (lam : ℝ)
    (hμ : (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD μ lam) (hlam : 0 < lam)
    (i j : Fin (Gump.Dice.hull R).A)
    (h : (Gump.Dice.hull R).cell j = HullGen.rot ((Gump.Dice.hull R).cell i) ∨
      (Gump.Dice.hull R).cell j = HullGen.refl ((Gump.Dice.hull R).cell i)) :
    (LH R Hull3.sdens).price μ j = (LH R Hull3.sdens).price μ i := by
  obtain ⟨μ0, lam0, -, -, -, -, huniq, -⟩ := hull_full_every R hA
  obtain ⟨e1, e2⟩ := huniq μ lam hμ hlam
  have huniq' : ∀ ν lam', (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' →
      ν = μ ∧ lam' = lam := fun ν l h1 h2 => by
    obtain ⟨a, b⟩ := huniq ν l h1 h2; exact ⟨a.trans e1.symm, b.trans e2.symm⟩
  rcases h with h | h
  · have hmem : ∀ p, HullGen.rot p ∈ Gump.Dice.hullCells R ↔ p ∈ Gump.Dice.hullCells R := fun p => by
      obtain ⟨x, y, z⟩ := p; simp only [HullGen.rot, HullGen.mem_hull_iff]; omega
    rw [← autPerm_gList R _ (HullGen.rot_aut R) hmem i j h]
    exact price_aut (HullGen.rot_aut R) Hull3.sdens (cellsOK_hull R) hμ hlam huniq' i
  · have hmem : ∀ p, HullGen.refl p ∈ Gump.Dice.hullCells R ↔ p ∈ Gump.Dice.hullCells R := fun p => by
      obtain ⟨x, y, z⟩ := p; simp only [HullGen.refl, HullGen.mem_hull_iff]; omega
    rw [← autPerm_gList R _ (HullGen.refl_aut R) hmem i j h]
    exact price_aut (HullGen.refl_aut R) Hull3.sdens (cellsOK_hull R) hμ hlam huniq' i

end Gump.Link
