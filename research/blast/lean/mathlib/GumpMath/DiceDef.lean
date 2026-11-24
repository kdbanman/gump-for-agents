/-
The one-layer dice surrogate of `research/blast/rigour/` (README.md "The surrogate", THEOREMS.md "The chain"),
as a killed finite Markov chain with rational transition probabilities, in the terms of `Gump/Basic.lean`.

A *face* is a finite list of cells of gump's lattice (`Gump.Pt`) lying in one layer d·p = const along a body
diagonal d (`Gump.Diag`, `Gump/Layers.lean`). Cell i of the face is `cells[i]`. A *state* is a number
x < 2 ^ A (A = number of cells): cell i is alive iff bit i of x is set (the indexing of `rigour/dense.py`).
The empty face is x = 0.

One generation, for each cell i at the point p independently:
* k = the number of live in-layer neighbours: the neighbours q ∈ `Gump.nbrs p` with d·q = d·p, each
  mapped by `red` to its representative (the identity on a free face; reduction modulo the period
  lattice on a wrapped face), counted with multiplicity, alive iff the representative is a live cell
  of the face (a representative that is not a cell of the face is dead: the free rim);
* coins: every neighbour q of p beneath the face (d·q = d·p - 2: density ρ1; d·q = d·p - 4: density ρ2)
  that exists (`coin q`) is replaced by an independent coin of that density (gump's cells beneath, made
  private); b = number of heads;
* the cell is alive next iff `Gump.rule (alive now) (k + b)` (B45/S345).
Neighbours above the face (d·q > d·p) are dead: on the hull faces of `geom.py` they lie outside the hull.

`P` is the transition matrix on the 2 ^ A states (a product over cells), `survival t x` the probability
that the face is still non-empty after t generations from x, i.e. P_x(T > t) with T the generation at
which the face is first empty (the empty face is absorbing, `P_zero`).
-/
import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Gump.Layers

namespace Gump.Dice
open Gump Finset Matrix

/-- A face of the dice surrogate. -/
structure Face where
  /-- the cells of the face, in order: cell i is `cells[i]` -/
  cells : List Pt
  /-- the body diagonal along which the face is one layer; beneath means a smaller d·q -/
  diag : Diag
  /-- the representative of a point of the face's layer -/
  red : Pt → Pt
  /-- which points beneath the face exist (carry a coin) -/
  coin : Pt → Bool

namespace Face
variable (F : Face)

/-- The number of cells. -/
def A : ℕ := F.cells.length

/-- The point of cell i. -/
def cell (i : ℕ) : Pt := F.cells.getD i ⟨0, 0, 0⟩

/-- The in-layer neighbours of cell i, as cell indices, with multiplicity; a neighbour whose
representative is not a cell of the face is left out (it is dead). -/
def nb (i : ℕ) : List ℕ :=
  (nbrs (F.cell i)).filterMap fun q =>
    if F.diag.dot q = F.diag.dot (F.cell i) then F.cells.idxOf? (F.red q) else none

/-- The number of coins one layer beneath cell i (cells of gump at d·q = d·p - 2 that exist). -/
def m1 (i : ℕ) : ℕ :=
  (nbrs (F.cell i)).countP fun q => decide (F.diag.dot q = F.diag.dot (F.cell i) - 2) && F.coin q

/-- The number of coins two layers beneath cell i (d·q = d·p - 4). -/
def m2 (i : ℕ) : ℕ :=
  (nbrs (F.cell i)).countP fun q => decide (F.diag.dot q = F.diag.dot (F.cell i) - 4) && F.coin q

/-- The number of live in-layer neighbours of cell i in state x. -/
def k (x i : ℕ) : ℕ := (F.nb i).countP fun j => x.testBit j

end Face

/-- The probability that m coins of density ρ show exactly j heads. -/
def bin (m : ℕ) (ρ : ℚ) (j : ℕ) : ℚ := (m.choose j : ℚ) * ρ ^ j * (1 - ρ) ^ (m - j)

/-- The probability that a cell is alive next generation, given its state s, its number k of live
in-layer neighbours and its coins (m1 of density ρ1, m2 of density ρ2): with j + l heads,
n = k + j + l and the cell is alive next iff `Gump.rule s n`. -/
def aliveProb (ρ1 ρ2 : ℚ) (m1 m2 k : ℕ) (s : Bool) : ℚ :=
  ∑ j ∈ range (m1 + 1), ∑ l ∈ range (m2 + 1),
    if rule s (k + j + l) then bin m1 ρ1 j * bin m2 ρ2 l else 0

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

/-- The probability that cell i is alive next generation, from state x. -/
def a (x i : ℕ) : ℚ := aliveProb ρ1 ρ2 (F.m1 i) (F.m2 i) (F.k x i) (x.testBit i)

/-- **The transition matrix** of the surrogate S(G): the cells update independently, so the
probability of x → y is the product over cells of a_i(x) (cell i alive in y) or 1 - a_i(x). -/
def P : Matrix (Fin (2 ^ F.A)) (Fin (2 ^ F.A)) ℚ :=
  fun x y => ∏ i ∈ range F.A, if (y : ℕ).testBit i then F.a ρ1 ρ2 x i else 1 - F.a ρ1 ρ2 x i

/-- The indicator of the non-empty states. -/
def live : Fin (2 ^ F.A) → ℚ := fun y => if (y : ℕ) = 0 then 0 else 1

/-- **Survival**: the probability that the face, started from x, is not empty after t generations,
P_x(T > t) = Σ_y (P ^ t)(x, y) · [y ≠ ∅]. -/
def survival (t : ℕ) (x : Fin (2 ^ F.A)) : ℚ := ((F.P ρ1 ρ2) ^ t *ᵥ F.live) x

/-- The full face: every cell alive. -/
def full : Fin (2 ^ F.A) := ⟨2 ^ F.A - 1, Nat.sub_lt (pow_pos (by norm_num) _) one_pos⟩

/-- The probability that the face is empty one generation after x. -/
def death (x : Fin (2 ^ F.A)) : ℚ := ∏ i ∈ range F.A, (1 - F.a ρ1 ρ2 x i)

end Face

/-! ### The faces of `research/blast/rigour/geom.py`, cell for cell in its order -/

/-- The diagonal (1,1,1). -/
def d111 : Diag := ⟨true, true, true⟩

/-- The cells of the rimmed triangular face x, y, z ≥ 0, x + y + z = R of the octahedral hull
|x| + |y| + |z| ≤ R (`geom.py hull R`), in the order x, then y. -/
def hullCells (R : ℕ) : List Pt :=
  ((List.range (R + 1)).flatMap fun (x : ℕ) => (List.range (R + 1 - x)).map fun (y : ℕ) =>
    (⟨(x : ℤ), (y : ℤ), ((R - x - y : ℕ) : ℤ)⟩ : Pt)).filter Pt.isCell

/-- The hull face of side R: a free face (no reduction), coins exactly at the points beneath that lie in
the hull (`geom.py`: "cells beneath outside the hull do not exist (no coin)"). -/
def hull (R : ℕ) : Face where
  cells := hullCells R
  diag := d111
  red := id
  coin := fun q => decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)

/-- Orientation index of a cell: 0, 1, 2 for normal axis x, y, z. -/
def axisIdx (p : Pt) : ℕ := match p.axis with | .X => 0 | .Y => 1 | .Z => 2

/-- `geom.py ab_cell` in the layer x + y + z = 1: the cell of orientation o at (a, b), i.e.
base_o + a (2,-2,0) + b (2,0,-2) with base = (1,0,0), (0,1,0), (0,0,1). -/
def abCell (o : ℕ) (a b : ℤ) : Pt :=
  match o with
  | 0 => ⟨1 + 2 * a + 2 * b, -2 * a, -2 * b⟩
  | 1 => ⟨2 * a + 2 * b, 1 - 2 * a, -2 * b⟩
  | _ => ⟨2 * a + 2 * b, -2 * a, 1 - 2 * b⟩

/-- `geom.py cell_ab`: the coordinates a, b of a cell of the layer x + y + z = 1. -/
def coordA (p : Pt) : ℤ := -((p.y - (if axisIdx p = 1 then 1 else 0)) / 2)
def coordB (p : Pt) : ℤ := -((p.z - (if axisIdx p = 2 then 1 else 0)) / 2)

/-- The cells (o, a, b), a < W, b < D, in `geom.py`'s order (a, then b, then o). -/
def gridCells (W D : ℕ) : List Pt :=
  (List.range W).flatMap fun (a : ℕ) => (List.range D).flatMap fun (b : ℕ) =>
    (List.range 3).map fun (o : ℕ) => abCell o a b

/-- The wrapped face with period lattice (H,K),(0,D) in the basis E1 = (2,-2,0), E2 = (2,0,-2)
(`geom.py torus H K D`; 3HD cells, every cell with its six in-layer neighbours and three coins). -/
def torus (H K D : ℕ) : Face where
  cells := gridCells H D
  diag := d111
  red := fun p => abCell (axisIdx p) (coordA p % H) ((coordB p - coordA p / H * K) % D)
  coin := fun _ => true

/-- The free strip W unit cells wide and D long, periodic along its length (`geom.py strip W D`):
every cell keeps its three coins; a neighbour across the rim is dead. -/
def strip (W D : ℕ) : Face where
  cells := gridCells W D
  diag := d111
  red := fun p => abCell (axisIdx p) (coordA p) (coordB p % D)
  coin := fun _ => true

/-- The patch W × D with a free rim all round (`geom.py patch W D`). -/
def patch (W D : ℕ) : Face where
  cells := gridCells W D
  diag := d111
  red := id
  coin := fun _ => true

/-- The densities of the coins in `rigour/`'s main runs: ρ1 = 0.44, ρ2 = 0.42. -/
def ρ1 : ℚ := 11 / 25
def ρ2 : ℚ := 21 / 50

end Gump.Dice
