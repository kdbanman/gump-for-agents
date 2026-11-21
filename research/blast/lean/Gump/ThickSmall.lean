/-
The small cases of `research/theory/thickness.md` section 2: what *is* sealed in one and two layers.

* Theorem 4 (i): the 6-cell hexagon ring is sealed in one layer, and **no nonempty set of at most 5 cells is
  sealed in one layer** (proved here for every layer, every diagonal and every finite set; the paper's
  minimality was a SAT search inside a patch).
* Theorem 4 (ii): every half-plane of a layer is sealed; hence a one-layer pattern never enters a half-plane
  that holds none of its live cells (its convex hull does not grow).
* Proposition 5, existence: a 36-cell set is sealed in the two-layer slab, so the hypothesis "three layers" of
  Theorem 3 (`slab_not_sealed_of_finite`) cannot be dropped, and the parity trap `A = 0, B = 4` is real.

Core Lean only: no Mathlib.
-/
import Gump.Thickness
import Gump.Symm

namespace Gump

/-- The diagonal `(1, 1, 1)`. -/
def d111 : Diag := ⟨true, true, true⟩

/-! ## Generalities: an integer dot product, negation of offsets, counting -/

/-- The integer dot product. -/
def dotv (v p : Pt) : Int := v.x * p.x + v.y * p.y + v.z * p.z

theorem dotv_add (v p q : Pt) : dotv v (p + q) = dotv v p + dotv v q := by
  simp only [dotv, Pt.add_x, Pt.add_y, Pt.add_z, Int.mul_add]; omega

theorem dotv_neg (v o : Pt) : dotv v o.neg = - dotv v o := by
  simp only [dotv, Pt.neg, Int.mul_neg]; omega

theorem Diag.dot_neg (d : Diag) (o : Pt) : d.dot o.neg = - d.dot o := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> simp [Diag.dot, sg, Pt.neg] <;> omega

/-- The offsets are centrally symmetric. -/
theorem offsets_neg_perm (a : Axis) : ((offsets a).map Pt.neg).Perm (offsets a) := by
  cases a <;> decide

theorem countP_add_le (l : List Pt) (P Q R : Pt → Bool)
    (hP : ∀ x ∈ l, P x = true → R x = true) (hQ : ∀ x ∈ l, Q x = true → R x = true)
    (hPQ : ∀ x ∈ l, P x = true → Q x = true → False) :
    l.countP P + l.countP Q ≤ l.countP R := by
  induction l with
  | nil => simp
  | cons a l ih =>
    have ih' := ih (fun x hx => hP x (List.mem_cons_of_mem _ hx)) (fun x hx => hQ x (List.mem_cons_of_mem _ hx))
      (fun x hx => hPQ x (List.mem_cons_of_mem _ hx))
    have h1 := hP a (by simp)
    have h2 := hQ a (by simp)
    have h3 := hPQ a (by simp)
    simp only [List.countP_cons]
    cases hpa : P a <;> cases hqa : Q a <;> cases hra : R a <;> simp_all <;> omega

/-- A list without repetitions whose elements all lie in another list is no longer than it. -/
theorem length_le_of_subset : ∀ (l₁ l₂ : List Pt), l₁.Nodup → (∀ x ∈ l₁, x ∈ l₂) → l₁.length ≤ l₂.length
  | [], _, _, _ => by simp
  | a :: t, l₂, hnd, hsub => by
    rw [List.nodup_cons] at hnd
    have ha : a ∈ l₂ := hsub a (by simp)
    have ih := length_le_of_subset t (l₂.erase a) hnd.2 (fun x hx => by
      have hxa : x ≠ a := fun h => hnd.1 (h ▸ hx)
      exact (List.mem_erase_of_ne hxa).2 (hsub x (List.mem_cons_of_mem _ hx)))
    rw [List.length_erase_of_mem ha] at ih
    have : 0 < l₂.length := List.length_pos_of_mem ha
    simp only [List.length_cons]; omega

/-- For a cell in the layer `s`, its neighbours in the layer are the six at `Δs = 0`. -/
theorem layer_nbr_iff (d : Diag) (s : Int) (p : Pt) (hp : slab d s s p = true) (o : Pt)
    (ho : o ∈ offsets p.axis) : slab d s s (p + o) = decide (d.dot o = 0) := by
  simp only [slab, Bool.and_eq_true, decide_eq_true_eq] at hp
  have hq : (p + o).isCell = true := nbrs_isCell p hp.1 (p + o) (List.mem_map.2 ⟨o, ho, rfl⟩)
  simp only [slab, hq, Diag.dot_add, Bool.true_and]
  apply Bool.eq_iff_iff.2
  simp only [decide_eq_true_eq]; omega

theorem in_layer_count (a : Axis) (d : Diag) : (offsets a).countP (fun o => decide (d.dot o = 0)) = 6 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-! ## Theorem 4 (ii): half-planes of a layer are sealed -/

/-- At most three of the six in-layer offsets point backward along any integer vector: they come in pairs
`±o`. -/
theorem in_layer_back_le_three (a : Axis) (d : Diag) (v : Pt) :
    (offsets a).countP (fun o => decide (d.dot o = 0 ∧ dotv v o < 0)) ≤ 3 := by
  have hperm := List.Perm.countP_eq (fun o => decide (d.dot o = 0 ∧ dotv v o < 0)) (offsets_neg_perm a)
  rw [List.countP_map] at hperm
  have := countP_add_le (offsets a) (fun o => decide (d.dot o = 0 ∧ dotv v o < 0))
    ((fun o => decide (d.dot o = 0 ∧ dotv v o < 0)) ∘ Pt.neg) (fun o => decide (d.dot o = 0))
    (by intro x _ h; simp only [decide_eq_true_eq] at h ⊢; exact h.1)
    (by intro x _ h; simp only [Function.comp, decide_eq_true_eq, Diag.dot_neg, dotv_neg] at h ⊢; omega)
    (by intro x _ h1 h2; simp only [Function.comp, decide_eq_true_eq, Diag.dot_neg, dotv_neg] at h1 h2; omega)
  rw [in_layer_count, ← hperm] at this
  omega

/-- The open half-plane `C < v·p` of the layer `s` along `d`, for any integer vector `v`. -/
def halfPlane (d : Diag) (s : Int) (v : Pt) (C : Int) : Pt → Bool :=
  fun p => slab d s s p && decide (C < dotv v p)

/-- **Theorem 4 (ii).** Every half-plane of a layer is sealed in the layer. -/
theorem halfPlane_sealed (d : Diag) (s : Int) (v : Pt) (C : Int) :
    SealedIn (slab d s s) (halfPlane d s v C) := by
  intro p hp
  have hp' := hp
  simp only [halfPlane, Bool.and_eq_true, decide_eq_true_eq] at hp'
  obtain ⟨hpV, hC⟩ := hp'
  refine Nat.le_trans ?_ (in_layer_back_le_three p.axis d v)
  unfold nbrs
  rw [List.countP_map]
  apply List.countP_mono_left
  intro o ho h
  simp only [Function.comp, halfPlane, layer_nbr_iff d s p hpV o ho, Bool.and_eq_true,
    decide_eq_true_eq, Bool.not_eq_true', Bool.and_eq_false_imp, dotv_add] at h
  simp only [decide_eq_true_eq]
  refine ⟨h.1, ?_⟩
  have := h.2 h.1
  simp only [decide_eq_false_iff_not] at this
  omega

/-- **Convex confinement in one layer.** If every live cell lies in the layer `s` and the half-plane
`C < v·p` of the layer holds no live cell, it never holds one. (A one-layer pattern never leaves the convex
hull of its live cells, read half-plane by half-plane.) -/
theorem layer_halfPlane_dead (d : Diag) (s : Int) (v : Pt) (C : Int) (c : Config)
    (hout : ∀ p, slab d s s p = false → c p = false)
    (hc : ∀ p, slab d s s p = true → C < dotv v p → c p = false) :
    ∀ n p, slab d s s p = true → C < dotv v p → run c n p = false := by
  have hW : ∀ p, halfPlane d s v C p = true → p.isCell = true := by
    intro p hp
    simp only [halfPlane, slab, Bool.and_eq_true] at hp; exact hp.1.1
  have := (sealedIn_slab_iff_run_dead d s s (halfPlane d s v C) hW).1 (halfPlane_sealed d s v C) c
    (fun p hp => hout p (by simpa using hp))
    (fun p hp => by
      simp only [halfPlane, Bool.and_eq_true, decide_eq_true_eq] at hp; exact hc p hp.1 hp.2)
  intro n p h1 h2
  exact this n p (by simp [halfPlane, h1, h2])

/-! ## Theorem 4 (i): the hexagon ring, and nothing smaller -/

/-- A kagome hexagon ring of the layer `s = 1` along `(1, 1, 1)`, in cyclic order. -/
def hexRing : List Pt := [⟨1, 0, 0⟩, ⟨2, -1, 0⟩, ⟨2, -2, 1⟩, ⟨1, -2, 2⟩, ⟨0, -1, 2⟩, ⟨0, 0, 1⟩]

/-- It is a ring: consecutive cells are neighbours (kagome bonds, of different orientations), and each cell is
also a neighbour of the opposite one (across the hexagon). -/
theorem hexRing_ring :
    (List.range 6).all (fun i =>
      (nbrs (hexRing.getD i ⟨0, 0, 0⟩)).contains (hexRing.getD ((i + 1) % 6) ⟨0, 0, 0⟩) &&
      (nbrs (hexRing.getD i ⟨0, 0, 0⟩)).contains (hexRing.getD ((i + 3) % 6) ⟨0, 0, 0⟩)) = true := by
  decide

/-- **Theorem 4 (i), existence.** The hexagon ring is sealed in its layer. -/
theorem hexRing_sealed : SealedIn (slab d111 1 1) (fun p => hexRing.contains p) := by
  have h : ∀ p ∈ hexRing, (nbrs p).countP (fun q => slab d111 1 1 q && !hexRing.contains q) ≤ 3 := by
    decide
  intro p hp
  exact h p (by simpa using hp)

/-- The in-layer offsets that point backward along the in-plane functional `d.perp`. -/
def backs (a : Axis) (d : Diag) : List Pt :=
  (offsets a).filter (fun o => d.dot o == 0 && decide (d.perp o < 0))

theorem backs_length (a : Axis) (d : Diag) : (backs a d).length = 3 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

theorem backs_nodup (a : Axis) (d : Diag) : (backs a d).Nodup := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- If a backward in-layer offset is left out, four in-layer offsets are forward or that one. -/
theorem back_forced (a : Axis) (d : Diag) : ∀ o ∈ backs a d,
    4 ≤ (offsets a).countP (fun o' => d.dot o' == 0 && (decide (0 < d.perp o') || o' == o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- One of the three backward neighbours of a cell (the one across a hexagon) is a neighbour of neither of
the other two, nor of itself. (The other two can be neighbours of each other: that depends on the functional.) -/
theorem backs_apart (a : Axis) (d : Diag) : ∃ o1 ∈ backs a d, ∀ o ∈ backs a d,
    ∀ o'' ∈ offsets (a.unit + o1).axis, o1 + o'' ≠ o := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- The axis of `p + o` for a cell `p` is the axis of `e_a + o`. -/
theorem axis_add_cell (p o : Pt) (hp : p.isCell = true) : (p + o).axis = (p.axis.unit + o).axis := by
  obtain ⟨h1, h2, h3⟩ := cell_mod_two hp
  apply axis_congr <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

/-- **Theorem 4 (i), minimality.** In one layer (any layer, any diagonal), every nonempty sealed set has at
least six cells (as a list, repetitions allowed, it has length at least six). *Proof.* The cell `p` furthest along the in-plane functional has its three forward in-layer
neighbours outside the set, so its three backward ones `b₁, b₂, b₃` are inside; they are pairwise not
neighbours, so the three or more neighbours of `b₁` inside the set are new cells: six in all. -/
theorem layer_sealed_six (d : Diag) (s : Int) (L : List Pt) (hne : L ≠ [])
    (hV : ∀ p ∈ L, slab d s s p = true) (hS : SealedIn (slab d s s) (fun p => L.contains p)) :
    6 ≤ L.length := by
  obtain ⟨p, hpL, hmax⟩ := exists_max_set (fun p => L.contains p) L (fun p h => by simpa using h)
    (by obtain ⟨p, hp⟩ := List.exists_mem_of_ne_nil L hne; exact ⟨p, by simpa using hp⟩) d.perp
  have hpL' : p ∈ L := by simpa using hpL
  have hpV := hV p hpL'
  have hpcell : p.isCell = true := by simp only [slab, Bool.and_eq_true] at hpV; exact hpV.1
  -- the backward neighbours are in the set
  have hback : ∀ o ∈ backs p.axis d, p + o ∈ L := by
    intro o ho
    apply Classical.byContradiction
    intro hno
    have h4 := back_forced p.axis d o ho
    have h3 := hS p hpL
    dsimp only at h3
    have : (offsets p.axis).countP (fun o' => d.dot o' == 0 && (decide (0 < d.perp o') || o' == o)) ≤
        (nbrs p).countP (fun q => slab d s s q && !L.contains q) := by
      unfold nbrs
      rw [List.countP_map]
      apply List.countP_mono_left
      intro o' ho' h
      simp only [Function.comp, layer_nbr_iff d s p hpV o' ho', Bool.and_eq_true, decide_eq_true_eq,
        beq_iff_eq, Bool.or_eq_true, Bool.not_eq_true'] at h ⊢
      refine ⟨h.1, ?_⟩
      rcases h.2 with h2 | rfl
      · cases hq : L.contains (p + o') with
        | false => rfl
        | true =>
          have := hmax _ hq
          rw [Diag.perp_add] at this; omega
      · simpa using hno
    omega
  -- the backward neighbour across a hexagon, and its neighbours in the set
  obtain ⟨o1, ho1, hapart⟩ := backs_apart p.axis d
  have hb1 : p + o1 ∈ L := hback o1 ho1
  have hb1V := hV _ hb1
  let N1 := (nbrs (p + o1)).filter (fun q => L.contains q)
  have hN1 : 3 ≤ N1.length := by
    have h3 := hS _ (by simpa using hb1)
    dsimp only at h3
    have h6 : (nbrs (p + o1)).countP (fun q => slab d s s q) = 6 := by
      rw [← in_layer_count (p + o1).axis d]
      unfold nbrs
      rw [List.countP_map]
      apply List.countP_congr
      intro o ho
      simp only [Function.comp, layer_nbr_iff d s (p + o1) hb1V o ho]
    have := countP_le_add (nbrs (p + o1)) (fun q => slab d s s q) (fun q => L.contains q)
      (fun q => slab d s s q && !L.contains q)
      (by intro q _ h; cases hq : L.contains q <;> simp_all)
    simp only [N1, ← List.countP_eq_length_filter]
    omega
  -- `backs` shifted to `p`, then `N1`: six distinct cells of `L`
  have hcell1 : (p + o1).isCell = true := by simp only [slab, Bool.and_eq_true] at hb1V; exact hb1V.1
  have hax : (p + o1).axis = (p.axis.unit + o1).axis := axis_add_cell p o1 hpcell
  have hnd6 : ((backs p.axis d).map (p + ·) ++ N1).Nodup := by
    rw [List.nodup_append]
    refine ⟨?_, ?_, ?_⟩
    · unfold List.Nodup
      rw [List.pairwise_map]
      refine (backs_nodup p.axis d).imp ?_
      intro a b hab heq; apply hab
      have hx := congrArg Pt.x heq; have hy := congrArg Pt.y heq; have hz := congrArg Pt.z heq
      simp only [Pt.add_x, Pt.add_y, Pt.add_z] at hx hy hz
      exact Pt.ext' (by omega) (by omega) (by omega)
    · exact (nbrs_nodup _).sublist List.filter_sublist
    · intro x hx y hy hxy
      subst hxy
      obtain ⟨o, ho, rfl⟩ := List.mem_map.1 hx
      have hy' := (List.mem_filter.1 hy).1
      simp only [nbrs, List.mem_map] at hy'
      obtain ⟨o'', ho'', heq⟩ := hy'
      rw [hax] at ho''
      apply hapart o ho o'' ho''
      have hx := congrArg Pt.x heq; have hy := congrArg Pt.y heq; have hz := congrArg Pt.z heq
      simp only [Pt.add_x, Pt.add_y, Pt.add_z] at hx hy hz
      exact Pt.ext' (by simp; omega) (by simp; omega) (by simp; omega)
  have hsub : ∀ x ∈ (backs p.axis d).map (p + ·) ++ N1, x ∈ L := by
    intro x hx
    rcases List.mem_append.1 hx with hx | hx
    · obtain ⟨o, ho, rfl⟩ := List.mem_map.1 hx; exact hback o ho
    · simpa using (List.mem_filter.1 hx).2
  have := length_le_of_subset _ L hnd6 hsub
  simp only [List.length_append, List.length_map, backs_length] at this
  omega

/-- **Theorem 4 (i), minimality, as a non-existence.** No nonempty set of at most five cells is sealed in a
layer. -/
theorem layer_no_sealed_le_five (d : Diag) (s : Int) (L : List Pt) (hne : L ≠ [])
    (hV : ∀ p ∈ L, slab d s s p = true) (h5 : L.length ≤ 5) :
    ¬ SealedIn (slab d s s) (fun p => L.contains p) := by
  intro hS
  have := layer_sealed_six d s L hne hV hS
  omega

/-! ## Proposition 5, existence: a finite sealed set in two layers -/

/-- A 36-cell set of the two-layer slab `1 ≤ s ≤ 3` along `(1, 1, 1)`: 18 cells in the layer `s = 1`, then 18
in the layer `s = 3`. Found by a SAT search (CaDiCaL, smallest sealed set through `(1, 0, 0)` within the box
`[-8, 8]³`; the same size as the set printed by `research/theory/sealed.py minsat 2 7 36`, not checked to be the
same set). -/
def set36 : List Pt :=
  [⟨-3, 0, 4⟩, ⟨-3, 2, 2⟩, ⟨-2, -1, 4⟩, ⟨-2, 0, 3⟩, ⟨-2, 1, 2⟩, ⟨-2, 2, 1⟩, ⟨-1, -2, 4⟩, ⟨-1, 2, 0⟩,
   ⟨0, -3, 4⟩, ⟨0, -2, 3⟩, ⟨0, 1, 0⟩, ⟨0, 2, -1⟩, ⟨1, -2, 2⟩, ⟨1, 0, 0⟩, ⟨2, -3, 2⟩, ⟨2, -2, 1⟩,
   ⟨2, -1, 0⟩, ⟨2, 0, -1⟩,
   ⟨-2, 0, 5⟩, ⟨-2, 1, 4⟩, ⟨-2, 2, 3⟩, ⟨-2, 3, 2⟩, ⟨-1, 0, 4⟩, ⟨-1, 2, 2⟩, ⟨0, -2, 5⟩, ⟨0, -1, 4⟩,
   ⟨0, 2, 1⟩, ⟨0, 3, 0⟩, ⟨1, -2, 4⟩, ⟨1, 2, 0⟩, ⟨2, -2, 3⟩, ⟨2, -1, 2⟩, ⟨2, 0, 1⟩, ⟨2, 1, 0⟩,
   ⟨3, -2, 2⟩, ⟨3, 0, 0⟩]

/-- 36 distinct cells, 18 in each of the two layers. -/
theorem set36_shape :
    set36.length = 36 ∧ set36.Nodup ∧ (∀ p ∈ set36, slab d111 1 3 p = true) ∧
      (set36.filter (fun p => d111.dot p == 1)).length = 18 := by
  decide

/-- **Proposition 5, existence.** The 36-cell set is sealed in the two-layer slab. -/
theorem set36_sealed : SealedIn (slab d111 1 3) (fun p => set36.contains p) := by
  have h : ∀ p ∈ set36, (nbrs p).countP (fun q => slab d111 1 3 q && !set36.contains q) ≤ 3 := by
    decide
  intro p hp
  exact h p (by simpa using hp)

/-- The parity trap: the slab `0 ≤ s ≤ 4` holds the same cells as `1 ≤ s ≤ 3` (two layers), since cells have
odd `s`. -/
theorem slab_parity (d : Diag) (k : Int) (p : Pt) : slab d (2 * k) (2 * k + 4) p = slab d (2 * k + 1) (2 * k + 3) p := by
  cases hc : p.isCell with
  | false => simp [slab, hc]
  | true =>
    have := dot_odd d p hc
    simp only [slab, hc, Bool.true_and]
    apply Bool.eq_iff_iff.2
    simp only [decide_eq_true_eq]; omega

/-- **Three layers are needed in Theorem 3.** In the slab `0 ≤ s ≤ 4` (two layers: `B - A = 4` is not enough,
the levels must hold three odd numbers) there is a nonempty finite sealed set. -/
theorem two_layers_finite_sealed :
    ∃ L : List Pt, L ≠ [] ∧ (∀ p ∈ L, slab d111 0 4 p = true) ∧
      SealedIn (slab d111 0 4) (fun p => L.contains p) := by
  have h04 : ∀ p, slab d111 0 4 p = slab d111 1 3 p := fun p => slab_parity d111 0 p
  refine ⟨set36, by decide, fun p hp => by rw [h04]; exact set36_shape.2.2.1 p hp, ?_⟩
  intro p hp
  simp only [h04]
  exact set36_sealed p hp

/-! ## Every hexagon ring, every 36-cell set: translations and reflections -/

/-- A vector with even coordinates (a translation of the lattice of cubes). -/
def Pt.IsEven (t : Pt) : Prop := t.x % 2 = 0 ∧ t.y % 2 = 0 ∧ t.z % 2 = 0

theorem isCell_add_even (p t : Pt) (ht : t.IsEven) : (p + t).isCell = p.isCell := by
  obtain ⟨hx, hy, hz⟩ := ht
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.isCell, Pt.add_x, Pt.add_y, Pt.add_z]
  have e1 : (x + t.x) % 2 = x % 2 := by omega
  have e2 : (y + t.y) % 2 = y % 2 := by omega
  have e3 : (z + t.z) % 2 = z % 2 := by omega
  rw [e1, e2, e3]

theorem axis_add_even (p t : Pt) (ht : t.IsEven) : (p + t).axis = p.axis := by
  obtain ⟨hx, hy, hz⟩ := ht
  apply axis_congr <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

/-- Translations by even vectors carry neighbours to neighbours. -/
theorem nbrs_add_even (p t : Pt) (ht : t.IsEven) : nbrs (p + t) = (nbrs p).map (· + t) := by
  simp only [nbrs, axis_add_even p t ht, List.map_map]
  apply List.map_congr_left
  intro o _
  apply Pt.ext' <;> simp only [Function.comp, Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

theorem neg_isEven (t : Pt) (ht : t.IsEven) : t.neg.IsEven := by
  obtain ⟨hx, hy, hz⟩ := ht
  simp only [Pt.IsEven, Pt.neg]; omega

theorem add_neg_cancel' (p t : Pt) : p + t + t.neg = p := by
  apply Pt.ext' <;> simp [Pt.neg] <;> omega

theorem add_neg_add' (q t : Pt) : q + t.neg + t = q := by
  apply Pt.ext' <;> simp [Pt.neg] <;> omega

/-- **Sealed sets translate.** If `W` is sealed in `V`, its translate by an even vector `t` is sealed in the
translate of `V`. -/
theorem SealedIn.translate {V W : Pt → Bool} (hS : SealedIn V W) (t : Pt) (ht : t.IsEven) :
    SealedIn (fun q => V (q + t.neg)) (fun q => W (q + t.neg)) := by
  intro q hq
  have hp := hS _ hq
  have e : q = q + t.neg + t := (add_neg_add' q t).symm
  rw [e, nbrs_add_even _ t ht, List.countP_map]
  refine Nat.le_trans (Nat.le_of_eq ?_) hp
  apply List.countP_congr
  intro r _
  simp only [Function.comp, add_neg_cancel']

/-- The translate of a slab by an even vector is a slab. -/
theorem slab_translate (d : Diag) (A B : Int) (t : Pt) (ht : t.IsEven) (q : Pt) :
    slab d A B (q + t.neg) = slab d (A + d.dot t) (B + d.dot t) q := by
  have hc : (q + t.neg).isCell = q.isCell := isCell_add_even q t.neg (neg_isEven t ht)
  simp only [slab, hc, Diag.dot_add, Diag.dot_neg]
  cases q.isCell
  · rfl
  · simp only [Bool.true_and]
    apply Bool.eq_iff_iff.2
    simp only [decide_eq_true_eq]; omega

/-- A sealed set of a slab, translated by an even vector, is sealed in the translated slab. -/
theorem SealedIn.translate_slab {d : Diag} {A B : Int} {W : Pt → Bool} (hS : SealedIn (slab d A B) W)
    (t : Pt) (ht : t.IsEven) :
    SealedIn (slab d (A + d.dot t) (B + d.dot t)) (fun q => W (q + t.neg)) := by
  have := hS.translate t ht
  intro q hq
  have h := this q hq
  simp only [slab_translate d A B t ht] at h
  exact h

/-- The reflection that carries the diagonal `(1, 1, 1)` to `d`. -/
def Diag.refl (d : Diag) (p : Pt) : Pt := ⟨sg d.sx p.x, sg d.sy p.y, sg d.sz p.z⟩

theorem sg_sg (b : Bool) (n : Int) : sg b (sg b n) = n := by cases b <;> simp [sg]

theorem Diag.refl_refl (d : Diag) (p : Pt) : d.refl (d.refl p) = p := by
  simp [Diag.refl, sg_sg]

theorem Diag.refl_add (d : Diag) (p q : Pt) : d.refl (p + q) = d.refl p + d.refl q := by
  apply Pt.ext' <;> simp [Diag.refl, sg_add]

theorem Diag.dot_refl (d : Diag) (p : Pt) : d.dot (d.refl p) = d111.dot p := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> simp [Diag.dot, Diag.refl, sg, d111]

theorem refl_isCell (d : Diag) (p : Pt) : (d.refl p).isCell = p.isCell := by
  obtain ⟨a, b, c⟩ := d
  obtain ⟨x, y, z⟩ := p
  cases a <;> cases b <;> cases c <;> simp only [Diag.refl, sg, Pt.isCell] <;> simp

theorem refl_axis (d : Diag) (p : Pt) : (d.refl p).axis = p.axis := by
  obtain ⟨a, b, c⟩ := d
  apply axis_congr <;> cases a <;> cases b <;> cases c <;> simp only [Diag.refl, sg] <;> simp <;> omega

/-- The offsets are invariant under each reflection (as lists up to order). -/
theorem offsets_refl_perm (d : Diag) (a : Axis) : ((offsets a).map d.refl).Perm (offsets a) := by
  obtain ⟨x, y, z⟩ := d
  cases a <;> cases x <;> cases y <;> cases z <;> decide

/-- Reflections carry neighbours to neighbours. -/
theorem nbrs_refl_perm (d : Diag) (p : Pt) : (nbrs (d.refl p)).Perm ((nbrs p).map d.refl) := by
  have e : (nbrs p).map d.refl = ((offsets p.axis).map d.refl).map (d.refl p + ·) := by
    simp only [nbrs, List.map_map]
    apply List.map_congr_left
    intro o _
    simp [Function.comp, Diag.refl_add]
  rw [e, nbrs, refl_axis]
  exact ((offsets_refl_perm d p.axis).map _).symm

theorem slab_refl (d : Diag) (A B : Int) (p : Pt) : slab d A B (d.refl p) = slab d111 A B p := by
  simp [slab, refl_isCell, Diag.dot_refl]

/-- **Sealed sets reflect.** A set sealed in a slab along `(1, 1, 1)`, reflected, is sealed in the slab along
`d` with the same levels. -/
theorem SealedIn.refl_slab {A B : Int} {W : Pt → Bool} (hS : SealedIn (slab d111 A B) W) (d : Diag) :
    SealedIn (slab d A B) (fun q => W (d.refl q)) := by
  intro q hq
  have hp := hS _ hq
  have e : q = d.refl (d.refl q) := (Diag.refl_refl d q).symm
  rw [e, List.Perm.countP_eq _ (nbrs_refl_perm d _), List.countP_map]
  refine Nat.le_trans (Nat.le_of_eq ?_) hp
  apply List.countP_congr
  intro r _
  simp only [Function.comp, slab_refl, Diag.refl_refl]

/-- **Theorem 4 (i), existence, for every layer of every diagonal.** For every diagonal `d` and every even
translation `t`, the reflected and translated hexagon ring is sealed in its layer `d·p = 1 + d·t`. (All
hexagon rings of all layers are of this form: the hexagons of a kagome layer form one orbit of the layer's
translations, and even translations move a layer by every even amount. That sentence is not checked here;
`hexagon_sealed` in `Gump/ThickHex.lean` proves the statement for every closed kagome walk of six cells
directly.) -/
theorem hexRing_all_sealed (d : Diag) (t : Pt) (ht : t.IsEven) :
    SealedIn (slab d (1 + d.dot t) (1 + d.dot t)) (fun q => hexRing.contains (d.refl (q + t.neg))) :=
  (hexRing_sealed.refl_slab d).translate_slab t ht

/-- **Proposition 5, existence, for every two-layer slab.** Every pair of consecutive layers along every
diagonal holds a 36-cell sealed set (the reflected and translated `set36`). -/
theorem set36_all_sealed (d : Diag) (t : Pt) (ht : t.IsEven) :
    SealedIn (slab d (1 + d.dot t) (3 + d.dot t)) (fun q => set36.contains (d.refl (q + t.neg))) :=
  (set36_sealed.refl_slab d).translate_slab t ht

/-- **Theorem 4 (ii) fails in two layers**: a half-plane of the two-layer slab need not be sealed (the
bottom-layer cell `(1, 0, 0)` has four neighbours in the slab behind the line `v·p = v·(1,0,0)`,
`v = (-2, 1, 1)`). -/
theorem two_layer_halfPlane_not_sealed :
    ¬ SealedIn (slab d111 1 3) (fun p => slab d111 1 3 p && decide (-3 < dotv ⟨-2, 1, 1⟩ p)) := by
  intro h
  have := h ⟨1, 0, 0⟩ (by decide)
  revert this
  decide

/-- **The faces of a slab are sealed** (the dead sets that the measurements of thickness.md §2 find as the
smallest on small torus slabs of three layers): the cells of a slab with `d·p ≤ C` are sealed in the slab, for
every `C`. -/
theorem slab_lower_sealed (d : Diag) (A B C : Int) : SealedIn (slab d A B) (slab d A C) := by
  intro p hp
  simp only [slab, Bool.and_eq_true, decide_eq_true_eq] at hp
  refine Nat.le_trans ?_ (below_le_three p.axis d.neg)
  unfold nbrs
  rw [List.countP_map]
  apply List.countP_mono_left
  intro o _ h
  simp only [Function.comp, slab, Bool.and_eq_true, Bool.not_eq_true', Bool.and_eq_false_imp,
    decide_eq_true_eq, decide_eq_false_iff_not, Diag.dot_add] at h
  simp only [decide_eq_true_eq, Diag.neg_dot]
  have := h.2 h.1.1
  omega

end Gump
