/-
The symmetries of the lattice are symmetries of the dynamics (`docs/AUTOMATON.md` section 2): for every
element g of the octahedral group O_h (48 signed permutations of the coordinates) and every translation
by cube steps (an even vector v in doubled coordinates), the map G p = g p + v commutes with `step` and
`run`. Hence a seed's symmetry is preserved forever.

The proof: G preserves cells; for a cell p, the neighbours of G p are G applied to the neighbours of p,
up to order. The second fact is a finite check over the 48 elements and 3 axes (`decide`).
-/
import Gump.Symm
import Gump.Layers

namespace Gump

/-- The six permutations of the coordinates. -/
inductive Perm3 where
  | id | swapXY | swapXZ | swapYZ | cyc | cyc2
deriving DecidableEq, Repr

def Perm3.apply : Perm3 → Pt → Pt
  | .id, p => p
  | .swapXY, ⟨x, y, z⟩ => ⟨y, x, z⟩
  | .swapXZ, ⟨x, y, z⟩ => ⟨z, y, x⟩
  | .swapYZ, ⟨x, y, z⟩ => ⟨x, z, y⟩
  | .cyc, ⟨x, y, z⟩ => ⟨y, z, x⟩
  | .cyc2, ⟨x, y, z⟩ => ⟨z, x, y⟩

/-- An element of the octahedral group O_h: permute the coordinates, then change their signs
(`true` keeps the sign). 6 × 8 = 48 elements. -/
structure Sym where
  perm : Perm3
  sx : Bool
  sy : Bool
  sz : Bool
deriving DecidableEq, Repr

def Sym.apply (g : Sym) (p : Pt) : Pt :=
  ⟨sg g.sx (g.perm.apply p).x, sg g.sy (g.perm.apply p).y, sg g.sz (g.perm.apply p).z⟩

/-- The lattice symmetry p ↦ g p + v. -/
def Sym.act (g : Sym) (v : Pt) (p : Pt) : Pt := g.apply p + v

/-- A translation by cube steps: all three doubled coordinates even. -/
def Pt.even (v : Pt) : Prop := v.x % 2 = 0 ∧ v.y % 2 = 0 ∧ v.z % 2 = 0

theorem Pt.mk_add (a b c a' b' c' : Int) : (⟨a, b, c⟩ : Pt) + ⟨a', b', c'⟩ = ⟨a + a', b + b', c + c'⟩ := rfl

theorem Sym.apply_add (g : Sym) (p q : Pt) : g.apply (p + q) = g.apply p + g.apply q := by
  obtain ⟨π, sx, sy, sz⟩ := g
  obtain ⟨x, y, z⟩ := p
  obtain ⟨x', y', z'⟩ := q
  rw [Pt.mk_add]
  cases π <;> simp only [Sym.apply, Perm3.apply, Pt.mk_add, sg_add]

theorem sg_emod_two (b : Bool) (n : Int) : sg b n % 2 = n % 2 := by
  cases b <;> simp only [sg, Bool.false_eq_true, ↓reduceIte] <;> omega

/-- A point is a cell iff its three coordinates mod 2 sum to 1. -/
theorem isCell_iff_sum (p : Pt) : p.isCell = true ↔ p.x % 2 + p.y % 2 + p.z % 2 = 1 := by
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq]
  omega

/-- The coordinates of g p mod 2 are a permutation of those of p. -/
theorem Sym.apply_mod_two (g : Sym) (p q : Pt) (hx : p.x % 2 = q.x % 2) (hy : p.y % 2 = q.y % 2)
    (hz : p.z % 2 = q.z % 2) :
    (g.apply p).x % 2 = (g.apply q).x % 2 ∧ (g.apply p).y % 2 = (g.apply q).y % 2 ∧
      (g.apply p).z % 2 = (g.apply q).z % 2 := by
  obtain ⟨π, sx, sy, sz⟩ := g
  obtain ⟨x, y, z⟩ := p
  obtain ⟨x', y', z'⟩ := q
  simp only at hx hy hz
  cases π <;> simp only [Sym.apply, Perm3.apply, sg_emod_two] <;> omega

/-- Lattice symmetries map cells to cells and other points to other points. -/
theorem isCell_act (g : Sym) {v : Pt} (hv : v.even) (p : Pt) : (g.act v p).isCell = p.isCell := by
  apply Bool.eq_iff_iff.mpr
  rw [isCell_iff_sum, isCell_iff_sum]
  obtain ⟨hvx, hvy, hvz⟩ := hv
  have e1 : (g.act v p).x % 2 = (g.apply p).x % 2 := by simp only [Sym.act, Pt.add_x]; omega
  have e2 : (g.act v p).y % 2 = (g.apply p).y % 2 := by simp only [Sym.act, Pt.add_y]; omega
  have e3 : (g.act v p).z % 2 = (g.apply p).z % 2 := by simp only [Sym.act, Pt.add_z]; omega
  rw [e1, e2, e3]
  obtain ⟨π, sx, sy, sz⟩ := g
  obtain ⟨x, y, z⟩ := p
  simp only [Sym.apply, sg_emod_two]
  cases π <;> simp only [Perm3.apply] <;> omega

/-- The axis of the image of a cell. -/
theorem axis_act (g : Sym) {v : Pt} (hv : v.even) {p : Pt} (hp : p.isCell = true) :
    (g.act v p).axis = (g.apply p.axis.unit).axis := by
  obtain ⟨h1, h2, h3⟩ := cell_mod_two hp
  obtain ⟨k1, k2, k3⟩ := g.apply_mod_two p p.axis.unit h1 h2 h3
  obtain ⟨hvx, hvy, hvz⟩ := hv
  apply axis_congr <;> simp only [Sym.act, Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

/-- **The finite check.** For each of the 48 elements g and each axis a, the offsets of the axis of
g e_a are the images under g of the offsets of a, up to order. -/
theorem offsets_sym (g : Sym) (a : Axis) :
    (offsets (g.apply a.unit).axis).Perm ((offsets a).map g.apply) := by
  obtain ⟨π, sx, sy, sz⟩ := g
  cases π <;> cases sx <;> cases sy <;> cases sz <;> cases a <;> decide

/-- The live-neighbour count is carried along by a lattice symmetry. -/
theorem count_act (g : Sym) {v : Pt} (hv : v.even) (c : Config) {p : Pt} (hp : p.isCell = true) :
    count c (g.act v p) = count (fun q => c (g.act v q)) p := by
  unfold count nbrs
  rw [List.countP_map, List.countP_map, axis_act g hv hp, (offsets_sym g p.axis).countP_eq,
    List.countP_map]
  apply List.countP_congr
  intro o _
  simp only [Function.comp, Sym.act, Sym.apply_add]
  have : g.apply p + v + g.apply o = g.apply p + g.apply o + v := by
    apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  rw [this]

/-- **One generation commutes with every lattice symmetry.** -/
theorem step_act (g : Sym) {v : Pt} (hv : v.even) (c : Config) :
    step (fun q => c (g.act v q)) = fun p => step (c) (g.act v p) := by
  funext p
  simp only [step]
  rw [isCell_act g hv p]
  cases hp : p.isCell
  · rfl
  · rw [count_act g hv c hp]

/-- **n generations commute with every lattice symmetry.** -/
theorem run_act (g : Sym) {v : Pt} (hv : v.even) (c : Config) :
    ∀ n, run (fun q => c (g.act v q)) n = fun p => run c n (g.act v p)
  | 0 => rfl
  | n + 1 => by
    rw [run, run_act g hv c n, step_act g hv]
    rfl

/-- **A seed's symmetry is preserved forever.** If the seed is invariant under a lattice symmetry, so is
every later generation. -/
theorem symmetry_preserved (g : Sym) {v : Pt} (hv : v.even) (c : Config)
    (h : ∀ p, c (g.act v p) = c p) : ∀ n p, run c n (g.act v p) = run c n p := by
  intro n p
  have hc : (fun q => c (g.act v q)) = c := funext h
  have := congrFun (run_act g hv c n) p
  rw [hc] at this
  exact this.symm

/-- The 48 elements are distinct maps (so the group acting is all of O_h, not a quotient). -/
theorem sym_faithful (g h : Sym) (e : g.apply ⟨1, 2, 3⟩ = h.apply ⟨1, 2, 3⟩) : g = h := by
  obtain ⟨π, sx, sy, sz⟩ := g
  obtain ⟨π', sx', sy', sz'⟩ := h
  revert e
  cases π <;> cases π' <;> cases sx <;> cases sy <;> cases sz <;> cases sx' <;> cases sy' <;> cases sz' <;>
    decide

end Gump
