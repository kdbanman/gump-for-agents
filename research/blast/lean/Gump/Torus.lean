/-
The oracle's array-index torus (`reference/oracle.py`, `step`, for even H), transcribed, and the theorem
that it is the infinite-lattice step of the periodic configuration.

oracle.py: the state is an H×H×H array h; for each axis a, cnt = Σ over offsets(a) of np.roll(h, -o), i.e.
cnt[i] = Σ_o h[(i + o) mod H]; the new state is 1 exactly at the cells of axis a (mask a) where h = 0 and
cnt ∈ {4, 5}, or h = 1 and cnt ∈ {3, 4, 5}; every other entry is 0. `tstep` below is that, entry by entry.
`lift_tstep`: for even H > 0, reading the array periodically, `tstep` is `Gump.step`. (For odd H the parity
of a coordinate is not preserved across the seam and the statement is false; `docs/AUTOMATON.md` section 4.)
-/
import Gump.Equivariance

namespace Gump.Torus
open Gump

/-- An array state: the entry at (i, j, k), used for 0 ≤ i, j, k < H. -/
abbrev TState := Nat → Nat → Nat → Bool

/-- np.roll's index arithmetic: (i + d) mod H. -/
def wrap (H : Nat) (i : Nat) (d : Int) : Nat := (((i : Int) + d) % (H : Int)).toNat

/-- The point of the array entry (i, j, k). -/
def at3 (i j k : Nat) : Pt := ⟨i, j, k⟩

/-- **oracle.py `step` on the array-index torus**: entry (i, j, k) is alive next iff it is a cell (`masks`)
and B45/S345 holds for its count over the offsets of its axis, read with wrap-around. -/
def tstep (H : Nat) (h : TState) : TState := fun i j k =>
  (at3 i j k).isCell &&
    rule (h i j k) ((offsets (at3 i j k).axis).countP fun o => h (wrap H i o.x) (wrap H j o.y) (wrap H k o.z))

/-- n generations on the torus. -/
def trun (H : Nat) (h : TState) : Nat → TState
  | 0 => h
  | n + 1 => tstep H (trun H h n)

/-- The periodic configuration of an array state: p is read at (p mod H). -/
def lift (H : Nat) (h : TState) : Config := fun p =>
  h (p.x % (H : Int)).toNat (p.y % (H : Int)).toNat (p.z % (H : Int)).toNat

theorem toNat_emod (a : Int) {H : Nat} (hH : 0 < H) : (((a % (H : Int)).toNat : Nat) : Int) = a % (H : Int) :=
  Int.toNat_of_nonneg (Int.emod_nonneg a (by omega))

/-- **The torus is gump on the periodic configuration.** For even H > 0, reading the array periodically,
one generation of the oracle's array-index torus is one generation of `Gump.step`. -/
theorem lift_tstep (H : Nat) (hH : 0 < H) (heven : H % 2 = 0) (h : TState) :
    lift H (tstep H h) = step (lift H h) := by
  funext p
  have h2 : (2 : Int) ∣ (H : Int) := by omega
  -- the array entry of p and its parities
  have ex := toNat_emod p.x hH
  have ey := toNat_emod p.y hH
  have ez := toNat_emod p.z hH
  have px : ((p.x % (H : Int)).toNat : Int) % 2 = p.x % 2 := by rw [ex, Int.emod_emod_of_dvd _ h2]
  have py : ((p.y % (H : Int)).toNat : Int) % 2 = p.y % 2 := by rw [ey, Int.emod_emod_of_dvd _ h2]
  have pz : ((p.z % (H : Int)).toNat : Int) % 2 = p.z % 2 := by rw [ez, Int.emod_emod_of_dvd _ h2]
  have hcell : (at3 (p.x % (H : Int)).toNat (p.y % (H : Int)).toNat (p.z % (H : Int)).toNat).isCell = p.isCell := by
    apply Bool.eq_iff_iff.mpr
    rw [isCell_iff_sum, isCell_iff_sum]
    simp only [at3]
    omega
  have hax : (at3 (p.x % (H : Int)).toNat (p.y % (H : Int)).toNat (p.z % (H : Int)).toNat).axis = p.axis :=
    axis_congr px py pz
  simp only [lift, tstep, step, count, nbrs, hcell, hax]
  congr 2
  rw [List.countP_map]
  apply List.countP_congr
  intro o _
  simp only [Function.comp, wrap, lift, Pt.add_x, Pt.add_y, Pt.add_z, ex, ey, ez, Int.emod_add_emod]

/-- **n generations of the torus are n generations of gump on the periodic configuration.** -/
theorem lift_trun (H : Nat) (hH : 0 < H) (heven : H % 2 = 0) (h : TState) :
    ∀ n, lift H (trun H h n) = run (lift H h) n
  | 0 => rfl
  | n + 1 => by rw [trun, lift_tstep H hH heven, lift_trun H hH heven h n]; rfl

end Gump.Torus
