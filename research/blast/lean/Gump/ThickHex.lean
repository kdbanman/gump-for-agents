/-
Theorem 4 (i) of `research/theory/thickness.md` for **every** hexagon ring: every closed walk of six distinct
cells along kagome bonds (in-layer neighbours of different orientation) is sealed in its layer, for every layer
of every diagonal.

The proof moves the walk by an even translation and a reflection so that it starts at a unit vector of the
layer `x + y + z = 1`, and then checks every such walk (at most 4·3⁴ = 324 non-backtracking walks from each of
the three unit vectors) by `decide +kernel`: the kernel evaluates the check, no compiled code is trusted.

Core Lean only: no Mathlib.
-/
import Gump.ThickSmall

namespace Gump

/-- The kagome neighbours of a cell in its layer along `d`: neighbours in the same layer with another
orientation (the four kagome bonds; the other two in-layer neighbours sit across hexagons). -/
def kagNbrs (d : Diag) (p : Pt) : List Pt :=
  (nbrs p).filter (fun q => d.dot q == d.dot p && !(q.axis == p.axis))

/-- **The finite check**: from each unit vector of the layer `x + y + z = 1`, every closed non-backtracking
walk of six distinct cells along kagome bonds is sealed in the layer. (`decide +kernel`: 3 starting cells, at
most 324 walks each, each walk's six cells checked against their twelve neighbours.) -/
theorem hex_check : ∀ a : Axis, ∀ c1 ∈ kagNbrs d111 a.unit, ∀ c2 ∈ (kagNbrs d111 c1).filter (· != a.unit),
    ∀ c3 ∈ (kagNbrs d111 c2).filter (· != c1), ∀ c4 ∈ (kagNbrs d111 c3).filter (· != c2),
    ∀ c5 ∈ (kagNbrs d111 c4).filter (· != c3), a.unit ∈ kagNbrs d111 c5 →
    [a.unit, c1, c2, c3, c4, c5].Nodup →
    ∀ p ∈ [a.unit, c1, c2, c3, c4, c5],
      (nbrs p).countP (fun q => slab d111 1 1 q && ![a.unit, c1, c2, c3, c4, c5].contains q) ≤ 3 := by
  intro a; cases a <;> decide +kernel

theorem mem_nbrs_translate (p q t : Pt) (ht : t.IsEven) : q + t ∈ nbrs (p + t) ↔ q ∈ nbrs p := by
  rw [nbrs_add_even p t ht, List.mem_map]
  constructor
  · rintro ⟨r, hr, he⟩
    have : r = q := by
      have hx := congrArg Pt.x he; have hy := congrArg Pt.y he; have hz := congrArg Pt.z he
      simp only [Pt.add_x, Pt.add_y, Pt.add_z] at hx hy hz
      exact Pt.ext' (by omega) (by omega) (by omega)
    exact this ▸ hr
  · intro h; exact ⟨q, h, rfl⟩

theorem kagNbrs_translate (d : Diag) (p q t : Pt) (ht : t.IsEven) :
    q + t ∈ kagNbrs d (p + t) ↔ q ∈ kagNbrs d p := by
  simp only [kagNbrs, List.mem_filter, mem_nbrs_translate p q t ht, Diag.dot_add,
    axis_add_even p t ht, axis_add_even q t ht, Bool.and_eq_true, beq_iff_eq]
  constructor
  · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by omega, h3⟩
  · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by omega, h3⟩

theorem Diag.refl_inj (d : Diag) {p q : Pt} (h : d.refl p = d.refl q) : p = q := by
  rw [← Diag.refl_refl d p, h, Diag.refl_refl]

theorem mem_nbrs_refl (d : Diag) (p q : Pt) : d.refl q ∈ nbrs (d.refl p) ↔ q ∈ nbrs p := by
  rw [List.Perm.mem_iff (nbrs_refl_perm d p), List.mem_map]
  constructor
  · rintro ⟨r, hr, he⟩; exact (Diag.refl_inj d he) ▸ hr
  · intro h; exact ⟨q, h, rfl⟩

theorem kagNbrs_refl (d : Diag) (p q : Pt) : d.refl q ∈ kagNbrs d (d.refl p) ↔ q ∈ kagNbrs d111 p := by
  simp only [kagNbrs, List.mem_filter, mem_nbrs_refl, Diag.dot_refl, refl_axis]

theorem refl_mod_two (d : Diag) (p : Pt) :
    (d.refl p).x % 2 = p.x % 2 ∧ (d.refl p).y % 2 = p.y % 2 ∧ (d.refl p).z % 2 = p.z % 2 := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> simp only [Diag.refl, sg] <;> simp <;> omega

/-- **Theorem 4 (i), existence, for every hexagon ring.** Six distinct cells `c0, …, c5`, each a kagome
neighbour (along `d`) of the one before and `c0` of `c5`, form a set sealed in their layer `d·p = d·c0`. -/
theorem hexagon_sealed (d : Diag) (c0 c1 c2 c3 c4 c5 : Pt) (hc : c0.isCell = true)
    (h1 : c1 ∈ kagNbrs d c0) (h2 : c2 ∈ kagNbrs d c1) (h3 : c3 ∈ kagNbrs d c2) (h4 : c4 ∈ kagNbrs d c3)
    (h5 : c5 ∈ kagNbrs d c4) (h0 : c0 ∈ kagNbrs d c5) (hnd : [c0, c1, c2, c3, c4, c5].Nodup) :
    SealedIn (slab d (d.dot c0) (d.dot c0)) (fun q => [c0, c1, c2, c3, c4, c5].contains q) := by
  obtain ⟨u, hu⟩ : ∃ u, u = c0.axis.unit := ⟨_, rfl⟩
  obtain ⟨t, htdef⟩ : ∃ t : Pt, t = c0 + (d.refl u).neg := ⟨_, rfl⟩
  have ht : t.IsEven := by
    obtain ⟨e1, e2, e3⟩ := cell_mod_two hc
    obtain ⟨r1, r2, r3⟩ := refl_mod_two d u
    rw [← hu] at e1 e2 e3
    subst htdef
    simp only [Pt.IsEven, Pt.add_x, Pt.add_y, Pt.add_z, Pt.neg]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  have hct : c0 + t.neg = d.refl u := by
    subst htdef; apply Pt.ext' <;> simp [Pt.neg] <;> omega
  obtain ⟨f, hfdef⟩ : ∃ f : Pt → Pt, f = fun q => d.refl (q + t.neg) := ⟨_, rfl⟩
  have hf0 : f c0 = u := by rw [hfdef]; simp only [hct, Diag.refl_refl]
  have hfinj : ∀ p q, f p = f q → p = q := by
    intro p q h
    rw [hfdef] at h
    have h' := Diag.refl_inj d h
    calc p = p + t.neg + t := (add_neg_add' p t).symm
      _ = q + t.neg + t := by rw [h']
      _ = q := add_neg_add' q t
  have hbond : ∀ p q, q ∈ kagNbrs d p → f q ∈ kagNbrs d111 (f p) := by
    intro p q h
    rw [hfdef, ← kagNbrs_refl d, Diag.refl_refl, Diag.refl_refl,
      kagNbrs_translate d p q t.neg (neg_isEven t ht)]
    exact h
  have hne : ∀ p q, p ≠ q → (f p != f q) = true := by
    intro p q h
    simp only [bne_iff_ne, ne_eq]
    exact fun he => h (hfinj p q he)
  simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false, not_or] at hnd
  obtain ⟨⟨n01, n02, n03, n04, n05⟩, ⟨n12, n13, n14, n15⟩, ⟨n23, n24, n25⟩, ⟨n34, n35⟩, n45, -⟩ := hnd
  have hchk := hex_check c0.axis
  rw [← hu] at hchk
  have b1 := hbond c0 c1 h1
  have b0 := hbond c5 c0 h0
  have nb2 := hne c2 c0 (Ne.symm n02)
  rw [hf0] at b1 b0 nb2
  have hcheck := hchk (f c1) b1
    (f c2) (List.mem_filter.2 ⟨hbond c1 c2 h2, nb2⟩)
    (f c3) (List.mem_filter.2 ⟨hbond c2 c3 h3, hne c3 c1 (Ne.symm n13)⟩)
    (f c4) (List.mem_filter.2 ⟨hbond c3 c4 h4, hne c4 c2 (Ne.symm n24)⟩)
    (f c5) (List.mem_filter.2 ⟨hbond c4 c5 h5, hne c5 c3 (Ne.symm n35)⟩)
    b0
    (by
      rw [← hf0]
      simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false, not_or]
      refine ⟨⟨?_, ?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩, ⟨?_, ?_⟩, ?_, by simp⟩ <;>
        intro he <;> first
          | exact n01 (hfinj _ _ he) | exact n02 (hfinj _ _ he) | exact n03 (hfinj _ _ he)
          | exact n04 (hfinj _ _ he) | exact n05 (hfinj _ _ he) | exact n12 (hfinj _ _ he)
          | exact n13 (hfinj _ _ he) | exact n14 (hfinj _ _ he) | exact n15 (hfinj _ _ he)
          | exact n23 (hfinj _ _ he) | exact n24 (hfinj _ _ he) | exact n25 (hfinj _ _ he)
          | exact n34 (hfinj _ _ he) | exact n35 (hfinj _ _ he) | exact n45 (hfinj _ _ he))
  rw [← hf0] at hcheck
  -- the image is sealed in the layer `x + y + z = 1`
  have hS' : SealedIn (slab d111 1 1) (fun q => [f c0, f c1, f c2, f c3, f c4, f c5].contains q) := by
    intro p hp
    exact hcheck p (by simpa using hp)
  -- carry it back: reflect, then translate
  have hS := (hS'.refl_slab d).translate_slab t ht
  have hlev : 1 + d.dot t = d.dot c0 := by
    have e : c0 = t + d.refl u := by subst htdef; apply Pt.ext' <;> simp [Pt.neg] <;> omega
    have : d.dot c0 = d.dot t + d.dot (d.refl u) := by rw [← Diag.dot_add, ← e]
    rw [this, Diag.dot_refl]
    have : d111.dot u = 1 := by rw [hu]; cases c0.axis <;> decide
    omega
  rw [hlev] at hS
  have hmem : ∀ q, [f c0, f c1, f c2, f c3, f c4, f c5].contains (d.refl (q + t.neg)) =
      [c0, c1, c2, c3, c4, c5].contains q := by
    intro q
    have hfq : d.refl (q + t.neg) = f q := by rw [hfdef]
    rw [hfq]
    apply Bool.eq_iff_iff.2
    simp only [List.contains_iff_mem, List.mem_cons, List.not_mem_nil, or_false]
    constructor
    · intro h
      rcases h with h | h | h | h | h | h <;>
        first
          | exact Or.inl (hfinj _ _ h) | exact Or.inr (Or.inl (hfinj _ _ h))
          | exact Or.inr (Or.inr (Or.inl (hfinj _ _ h)))
          | exact Or.inr (Or.inr (Or.inr (Or.inl (hfinj _ _ h))))
          | exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hfinj _ _ h)))))
          | exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (hfinj _ _ h)))))
    · intro h
      rcases h with rfl | rfl | rfl | rfl | rfl | rfl <;> simp
  intro q hq
  have := hS q (by simp only [hmem]; exact hq)
  refine Nat.le_trans (Nat.le_of_eq ?_) this
  apply List.countP_congr
  intro r _
  simp only [hmem]

/-- The hypotheses of `hexagon_sealed` are met (they are not vacuous): `hexRing` is such a walk. -/
theorem hexRing_walk :
    (⟨1, 0, 0⟩ : Pt).isCell = true ∧ (⟨2, -1, 0⟩ : Pt) ∈ kagNbrs d111 ⟨1, 0, 0⟩ ∧
    (⟨2, -2, 1⟩ : Pt) ∈ kagNbrs d111 ⟨2, -1, 0⟩ ∧ (⟨1, -2, 2⟩ : Pt) ∈ kagNbrs d111 ⟨2, -2, 1⟩ ∧
    (⟨0, -1, 2⟩ : Pt) ∈ kagNbrs d111 ⟨1, -2, 2⟩ ∧ (⟨0, 0, 1⟩ : Pt) ∈ kagNbrs d111 ⟨0, -1, 2⟩ ∧
    (⟨1, 0, 0⟩ : Pt) ∈ kagNbrs d111 ⟨0, 0, 1⟩ ∧ hexRing.Nodup := by
  decide

end Gump
