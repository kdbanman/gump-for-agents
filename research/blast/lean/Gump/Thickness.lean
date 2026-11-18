/-
Theorem 3 of `research/theory/thickness.md` (T6 of `docs/AUTOMATON.md`): no finite sealed set in the full
lattice or in a slab of three or more {111} layers; and the converse half of Lemma 1, so that sealed sets
are exactly the sets that stay dead whatever happens elsewhere.

The paper proof takes the cell of the set furthest along a generic direction. Here the direction is an
integer vector, generic for the 36 offsets (no offset is orthogonal to it), and every fact about the offsets
is checked by `decide`.

Core Lean only: no Mathlib.
-/
import Gump.Sealed
import Gump.Spec

namespace Gump

/-! ## Sealed relative to a vessel -/

/-- `S` is *sealed in the vessel* `V` (cells outside `V` are dead forever): each point of `S` has at most
three neighbours in `V` outside `S`. With `V` everything, this is `Sealed`. -/
def SealedIn (V S : Pt → Bool) : Prop :=
  ∀ p, S p = true → (nbrs p).countP (fun q => V q && !S q) ≤ 3

theorem sealedIn_univ_iff (S : Pt → Bool) : SealedIn (fun _ => true) S ↔ Sealed S := by
  simp [SealedIn, Sealed]

/-- The slab of the cells whose layer along `d` lies between `A` and `B`. Cells have odd `d.dot p`, so its
layers are the odd levels in `[A, B]`. -/
def slab (d : Diag) (A B : Int) : Pt → Bool :=
  fun p => p.isCell && decide (A ≤ d.dot p ∧ d.dot p ≤ B)

/-- Unions of sets sealed in a vessel are sealed in it. -/
theorem SealedIn.union {V S T : Pt → Bool} (hS : SealedIn V S) (hT : SealedIn V T) :
    SealedIn V (fun p => S p || T p) := by
  intro p hp
  have key : ∀ (U : Pt → Bool), (nbrs p).countP (fun q => V q && !U q) ≤ 3 →
      (∀ q, U q = true → (S q || T q) = true) →
      (nbrs p).countP (fun q => V q && !(S q || T q)) ≤ 3 := by
    intro U hU hsub
    refine Nat.le_trans ?_ hU
    apply List.countP_mono_left
    intro q _ hq
    cases hUq : U q with
    | false => simp_all
    | true => rw [hsub q hUq] at hq; simp at hq
  cases hSp : S p with
  | true => exact key S (hS p hSp) (fun q h => by simp [h])
  | false =>
    have hTp : T p = true := by simpa [hSp] using hp
    exact key T (hT p hTp) (fun q h => by simp [h])

/-- A dead set sealed in a vessel is dead one generation later, if everything outside the vessel is dead. -/
theorem SealedIn.step_dead {V S : Pt → Bool} (hS : SealedIn V S) {c : Config}
    (hout : DeadOn c (fun p => !V p)) (hc : DeadOn c S) : DeadOn (step c) S := by
  intro p hp
  apply step_dead_of_count_le_three (hc p hp)
  refine Nat.le_trans ?_ (hS p hp)
  unfold count
  apply List.countP_mono_left
  intro q _ hq
  cases hVq : V q with
  | false => rw [hout q (by simp [hVq])] at hq; contradiction
  | true =>
    cases hSq : S q with
    | false => rfl
    | true => rw [hc q hSq] at hq; contradiction

/-! ## Facts about the offsets, all by `decide` -/

/-- Every cell has odd layer along every diagonal. -/
theorem dot_odd (d : Diag) (p : Pt) (h : p.isCell = true) : d.dot p % 2 = 1 := by
  obtain ⟨x, y, z⟩ := p
  obtain ⟨sx, sy, sz⟩ := d
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq] at h
  cases sx <;> cases sy <;> cases sz <;> simp only [Diag.dot, sg] <;> simp <;> omega

/-- A generic functional for the 36 offsets: `x + 3y + 9z`. -/
def gen (p : Pt) : Int := p.x + 3 * p.y + 9 * p.z

theorem gen_add (p q : Pt) : gen (p + q) = gen p + gen q := by
  simp only [gen, Pt.add_x, Pt.add_y, Pt.add_z]; omega

/-- Exactly six of the twelve offsets point forward along `gen` (and none is orthogonal to it). -/
theorem gen_pos_count (a : Axis) : (offsets a).countP (fun o => decide (0 < gen o)) = 6 := by
  cases a <;> decide

/-- An in-plane functional for the diagonal `d`: `v = (s_x, 2 s_y, -3 s_z)`, so `v · d = 1 + 2 - 3 = 0`. -/
def Diag.perp (d : Diag) (p : Pt) : Int := sg d.sx p.x + 2 * sg d.sy p.y - 3 * sg d.sz p.z

theorem Diag.perp_add (d : Diag) (p q : Pt) : d.perp (p + q) = d.perp p + d.perp q := by
  simp only [Diag.perp, Pt.add_x, Pt.add_y, Pt.add_z, sg_add]; omega

/-- The in-plane functional is generic: no offset is orthogonal to it. -/
theorem perp_ne_zero (a : Axis) (d : Diag) : ∀ o ∈ offsets a, d.perp o ≠ 0 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- The identity behind Theorem 3: for the two offsets `a ≠ b` at `Δs = +2` and the one `e` at `Δs = +4`,
`e + 2(a + b) = 4d`, for every orientation and diagonal. (The proof below does not use it: `decide` counts
directly. It is the reason the counts `bottom_count` and `top_count` hold for every generic in-plane `v`.) -/
theorem up_identity (ax : Axis) (d : Diag) :
    ∀ e ∈ offsets ax, ∀ a ∈ offsets ax, ∀ b ∈ offsets ax, d.dot e = 4 → d.dot a = 2 → d.dot b = 2 → a ≠ b →
      e + a + a + b + b = ⟨4 * sg d.sx 1, 4 * sg d.sy 1, 4 * sg d.sz 1⟩ := by
  have h : ∀ e ∈ (offsets ax).filter (fun o => d.dot o == 4),
      ∀ a ∈ (offsets ax).filter (fun o => d.dot o == 2), ∀ b ∈ (offsets ax).filter (fun o => d.dot o == 2),
      a ≠ b → e + a + a + b + b = ⟨4 * sg d.sx 1, 4 * sg d.sy 1, 4 * sg d.sz 1⟩ := by
    obtain ⟨sx, sy, sz⟩ := d
    cases ax <;> cases sx <;> cases sy <;> cases sz <;> decide
  intro e he a ha b hb h4 h2a h2b hab
  exact h e (List.mem_filter.2 ⟨he, by simp [h4]⟩) a (List.mem_filter.2 ⟨ha, by simp [h2a]⟩)
    b (List.mem_filter.2 ⟨hb, by simp [h2b]⟩) hab

/-- A cell in a bottom layer (the layers `0, +2, +4` above it in the slab): at least four of its in-slab
neighbours lie forward along the in-plane functional. -/
theorem bottom_count (a : Axis) (d : Diag) :
    4 ≤ (offsets a).countP (fun o => decide (0 ≤ d.dot o ∧ 0 < d.perp o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- A cell in a top layer (the layers `0, -2, -4` in the slab). -/
theorem top_count (a : Axis) (d : Diag) :
    4 ≤ (offsets a).countP (fun o => decide (d.dot o ≤ 0 ∧ 0 < d.perp o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- A cell in an interior layer (the layers `-2, 0, +2` in the slab): at least five. -/
theorem interior_count (a : Axis) (d : Diag) :
    5 ≤ (offsets a).countP (fun o => decide (-2 ≤ d.dot o ∧ d.dot o ≤ 2 ∧ 0 < d.perp o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-! ## Maximisers -/

/-- A nonempty list has an element maximising any integer function. -/
theorem exists_max (L : List Pt) (hne : L ≠ []) (f : Pt → Int) : ∃ p ∈ L, ∀ q ∈ L, f q ≤ f p := by
  induction L with
  | nil => exact absurd rfl hne
  | cons a l ih =>
    cases l with
    | nil => exact ⟨a, by simp, fun q hq => by simp at hq; rw [hq]; exact Int.le_refl _⟩
    | cons b l' =>
      obtain ⟨p, hp, hmax⟩ := ih (by simp)
      by_cases h : f a ≤ f p
      · refine ⟨p, List.mem_cons_of_mem _ hp, ?_⟩
        intro q hq
        rcases List.mem_cons.1 hq with rfl | hq
        · exact h
        · exact hmax q hq
      · refine ⟨a, by simp, ?_⟩
        intro q hq
        rcases List.mem_cons.1 hq with rfl | hq
        · exact Int.le_refl _
        · have := hmax q hq; omega

/-- A nonempty set contained in a list has a point maximising any integer function over the set. -/
theorem exists_max_set (S : Pt → Bool) (L : List Pt) (hL : ∀ p, S p = true → p ∈ L)
    (hne : ∃ p, S p = true) (f : Pt → Int) :
    ∃ p, S p = true ∧ ∀ q, S q = true → f q ≤ f p := by
  obtain ⟨p0, hp0⟩ := hne
  have hne' : L.filter S ≠ [] := by
    intro h
    have : p0 ∈ L.filter S := List.mem_filter.2 ⟨hL p0 hp0, hp0⟩
    rw [h] at this; simp at this
  obtain ⟨p, hp, hmax⟩ := exists_max (L.filter S) hne' f
  refine ⟨p, (List.mem_filter.1 hp).2, fun q hq => hmax q (List.mem_filter.2 ⟨hL q hq, hq⟩)⟩

/-! ## Theorem 3 in the full lattice -/

/-- **The extremal cell.** In a finite nonempty set, the point furthest along `gen` has at least six of its
twelve neighbours outside the set. -/
theorem exists_six_outside (S : Pt → Bool) (L : List Pt) (hL : ∀ p, S p = true → p ∈ L)
    (hne : ∃ p, S p = true) :
    ∃ p, S p = true ∧ 6 ≤ (nbrs p).countP (fun q => !S q) := by
  obtain ⟨p, hp, hmax⟩ := exists_max_set S L hL hne gen
  refine ⟨p, hp, ?_⟩
  rw [← gen_pos_count p.axis]
  unfold nbrs
  rw [List.countP_map]
  apply List.countP_mono_left
  intro o _ ho
  simp only [decide_eq_true_eq] at ho
  simp only [Function.comp]
  cases hq : S (p + o) with
  | false => rfl
  | true =>
    have := hmax _ hq
    rw [gen_add] at this; omega

/-- **Theorem 3, full lattice.** No nonempty finite set of points is sealed. (Every point, cell or not, has
its twelve neighbours, so the hypothesis that the points are cells is not needed.) -/
theorem not_sealed_of_finite (S : Pt → Bool) (L : List Pt) (hL : ∀ p, S p = true → p ∈ L)
    (hne : ∃ p, S p = true) : ¬ Sealed S := by
  intro hS
  obtain ⟨p, hp, h6⟩ := exists_six_outside S L hL hne
  have := hS p hp
  omega

/-- **Theorem 3, full lattice**, in the shape of a list of cells. -/
theorem no_finite_sealed (L : List Pt) (hne : L ≠ []) : ¬ Sealed (fun p => L.contains p) := by
  apply not_sealed_of_finite _ L (fun p h => by simpa using h)
  obtain ⟨p, hp⟩ := List.exists_mem_of_ne_nil L hne
  exact ⟨p, by simpa using hp⟩

/-! ## Theorem 3 in a slab of three or more layers -/

/-- **Theorem 3, slab.** Let the slab `A ≤ d·p ≤ B` hold at least three layers (three odd levels `s, s+2,
s+4` in `[A, B]`). Then no nonempty finite set of cells of the slab is sealed in the slab: the cell furthest
along an in-plane generic direction has at least four neighbours in the slab outside the set. -/
theorem slab_exists_four_outside (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B)
    (S : Pt → Bool) (hSV : ∀ p, S p = true → slab d A B p = true)
    (L : List Pt) (hL : ∀ p, S p = true → p ∈ L) (hne : ∃ p, S p = true) :
    ∃ p, S p = true ∧ 4 ≤ (nbrs p).countP (fun q => slab d A B q && !S q) := by
  obtain ⟨p, hp, hmax⟩ := exists_max_set S L hL hne d.perp
  refine ⟨p, hp, ?_⟩
  have hpV := hSV p hp
  simp only [slab, Bool.and_eq_true, decide_eq_true_eq] at hpV
  obtain ⟨hcell, hA, hB⟩ := hpV
  have hodd := dot_odd d p hcell
  obtain ⟨s, hs, hAs, hsB⟩ := h3
  -- every forward neighbour inside the slab is in the slab and outside `S`
  have key : ∀ (W : Pt → Bool),
      (∀ o ∈ offsets p.axis, W o = true → A ≤ d.dot p + d.dot o ∧ d.dot p + d.dot o ≤ B) →
      (offsets p.axis).countP (fun o => W o && decide (0 < d.perp o)) ≤
        (nbrs p).countP (fun q => slab d A B q && !S q) := by
    intro W hW
    unfold nbrs
    rw [List.countP_map]
    apply List.countP_mono_left
    intro o ho hWo
    simp only [Bool.and_eq_true, decide_eq_true_eq] at hWo
    simp only [Function.comp, Bool.and_eq_true]
    have hq : (p + o).isCell = true := nbrs_isCell p hcell (p + o) (List.mem_map.2 ⟨o, ho, rfl⟩)
    have hl := hW o ho hWo.1
    refine ⟨?_, ?_⟩
    · simp only [slab, hq, Diag.dot_add, Bool.true_and, decide_eq_true_eq]; exact hl
    · cases hS : S (p + o) with
      | false => rfl
      | true =>
        have := hmax _ hS
        rw [Diag.perp_add] at this; have := hWo.2; omega
  by_cases hbot : d.dot p - 2 < A
  · -- bottom layer: the layers +2 and +4 are in the slab
    have hup : d.dot p + 4 ≤ B := by omega
    refine Nat.le_trans ?_ (key (fun o => decide (0 ≤ d.dot o)) ?_)
    · refine Nat.le_trans (bottom_count p.axis d) (Nat.le_of_eq ?_)
      apply List.countP_congr; intro o _; simp
    · intro o hmem ho
      simp only [decide_eq_true_eq] at ho
      have := dot_offset_le_four p.axis d o hmem
      omega
  · by_cases htop : B < d.dot p + 2
    · -- top layer
      have hdown : A ≤ d.dot p - 4 := by omega
      refine Nat.le_trans ?_ (key (fun o => decide (d.dot o ≤ 0)) ?_)
      · refine Nat.le_trans (top_count p.axis d) (Nat.le_of_eq ?_)
        apply List.countP_congr; intro o _; simp
      · intro o hmem ho
        simp only [decide_eq_true_eq] at ho
        have := dot_offset_ge_neg_four p.axis d o hmem
        omega
    · -- interior layer
      refine Nat.le_trans ?_ (key (fun o => decide (-2 ≤ d.dot o ∧ d.dot o ≤ 2)) ?_)
      · refine Nat.le_trans (Nat.le_trans (by decide : 4 ≤ 5) (interior_count p.axis d)) (Nat.le_of_eq ?_)
        apply List.countP_congr; intro o _; simp [and_assoc]
      · intro o _ ho
        simp only [decide_eq_true_eq] at ho
        omega

/-- **Theorem 3, slab of at least three layers.** No nonempty finite set of cells of the slab is sealed in
the slab. -/
theorem slab_not_sealed_of_finite (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B)
    (S : Pt → Bool) (hSV : ∀ p, S p = true → slab d A B p = true)
    (L : List Pt) (hL : ∀ p, S p = true → p ∈ L) (hne : ∃ p, S p = true) :
    ¬ SealedIn (slab d A B) S := by
  intro hS
  obtain ⟨p, hp, h4⟩ := slab_exists_four_outside d A B h3 S hSV L hL hne
  have := hS p hp
  omega

end Gump
