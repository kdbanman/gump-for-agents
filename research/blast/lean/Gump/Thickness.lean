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

/-- **Theorem 3, slab of `m ≥ 3` layers**, with the layers named: the slab of the `m` consecutive layers
`2k+1, 2k+3, …, 2k+2m-1` along `d`. -/
theorem layers_not_sealed_of_finite (d : Diag) (k : Int) (m : Nat) (hm : 3 ≤ m)
    (S : Pt → Bool) (hSV : ∀ p, S p = true → slab d (2 * k + 1) (2 * k + 2 * m - 1) p = true)
    (L : List Pt) (hL : ∀ p, S p = true → p ∈ L) (hne : ∃ p, S p = true) :
    ¬ SealedIn (slab d (2 * k + 1) (2 * k + 2 * m - 1)) S :=
  slab_not_sealed_of_finite d _ _ ⟨2 * k + 1, by omega, by omega, by omega⟩ S hSV L hL hne

/-! ## Lemma 1, converse: sealed sets are exactly the sets that stay dead whatever happens elsewhere -/

/-- The twelve neighbours of a point are distinct. -/
theorem nbrs_nodup (p : Pt) : (nbrs p).Nodup := by
  unfold nbrs List.Nodup
  rw [List.pairwise_map]
  refine (offsets_nodup p.axis).imp ?_
  intro a b hab heq
  apply hab
  have hx := congrArg Pt.x heq
  have hy := congrArg Pt.y heq
  have hz := congrArg Pt.z heq
  simp only [Pt.add_x, Pt.add_y, Pt.add_z] at hx hy hz
  obtain ⟨ax, ay, az⟩ := a
  obtain ⟨bx, by', bz⟩ := b
  simp only [Pt.mk.injEq] at *
  omega

/-- In a list without repetitions, at least `k` elements satisfying `P` give a subset of `P` meeting the list
in exactly `k` elements. -/
theorem exists_sub_count (l : List Pt) (hl : l.Nodup) (P : Pt → Bool) (k : Nat) (hk : k ≤ l.countP P) :
    ∃ T : Pt → Bool, (∀ q, T q = true → P q = true) ∧ l.countP T = k := by
  induction l generalizing k with
  | nil =>
    simp at hk; subst hk
    exact ⟨fun _ => false, by simp, by simp⟩
  | cons a l ih =>
    rw [List.nodup_cons] at hl
    obtain ⟨ha, hl⟩ := hl
    cases hPa : P a with
    | true =>
      rw [List.countP_cons_of_pos hPa] at hk
      cases k with
      | zero => exact ⟨fun _ => false, by simp, by simp⟩
      | succ k =>
        obtain ⟨T, hT, hc⟩ := ih hl k (by omega)
        refine ⟨fun q => q == a || T q, ?_, ?_⟩
        · intro q hq
          cases hqa : (q == a)
          · simp only [hqa, Bool.false_or] at hq; exact hT q hq
          · simp only [beq_iff_eq] at hqa; subst hqa; exact hPa
        · rw [List.countP_cons_of_pos (by simp), ← hc]
          congr 1
          apply List.countP_congr
          intro q hq
          have : q ≠ a := fun h => ha (h ▸ hq)
          simp [this]
    | false =>
      rw [List.countP_cons_of_neg (by simp [hPa])] at hk
      obtain ⟨T, hT, hc⟩ := ih hl k hk
      refine ⟨T, hT, ?_⟩
      have hTa : T a = false := by
        cases h : T a with
        | false => rfl
        | true => have := hT a h; rw [hPa] at this; contradiction
      rw [List.countP_cons_of_neg (by simp [hTa]), hc]

/-- **Lemma 1, converse, in a vessel.** If a cell `p` of `W` has at least four neighbours in the vessel `V`
outside `W`, some configuration that is dead outside `V` and dead on `W` has `p` alive one generation later
(exactly four of those neighbours alive, everything else dead). -/
theorem exists_birth_in (V W : Pt → Bool) (p : Pt) (hp : p.isCell = true) (hW : W p = true)
    (h4 : 4 ≤ (nbrs p).countP (fun q => V q && !W q)) :
    ∃ c : Config, DeadOn c (fun q => !V q) ∧ DeadOn c W ∧ step c p = true := by
  obtain ⟨T, hT, hc⟩ := exists_sub_count (nbrs p) (nbrs_nodup p) _ 4 h4
  have hdeadW : DeadOn T W := by
    intro q hq
    cases h : T q with
    | false => rfl
    | true => have := hT q h; simp [hq] at this
  refine ⟨T, ?_, hdeadW, ?_⟩
  · intro q hq
    cases h : T q with
    | false => rfl
    | true => have := hT q h; simp only [Bool.not_eq_true'] at hq; simp [hq] at this
  · simp [step, hp, hdeadW p hW, count, hc, rule]

/-- **Lemma 1, converse.** If a cell `p` of `W` has at least four neighbours outside `W`, some configuration
dead on `W` has `p` alive one generation later. -/
theorem exists_birth (W : Pt → Bool) (p : Pt) (hp : p.isCell = true) (hW : W p = true)
    (h4 : 4 ≤ (nbrs p).countP (fun q => !W q)) :
    ∃ c : Config, DeadOn c W ∧ step c p = true := by
  obtain ⟨c, _, h1, h2⟩ := exists_birth_in (fun _ => true) W p hp hW (by simpa using h4)
  exact ⟨c, h1, h2⟩

/-- **Lemma 1, both halves.** A set of cells is sealed iff, dead, it is dead one generation later whatever
the configuration elsewhere. -/
theorem sealed_iff_step_dead (W : Pt → Bool) (hW : ∀ p, W p = true → p.isCell = true) :
    Sealed W ↔ ∀ c : Config, DeadOn c W → DeadOn (step c) W := by
  constructor
  · intro hS c hc; exact hS.step_dead hc
  · intro h p hp
    apply Classical.byContradiction
    intro hlt
    obtain ⟨c, hc, hstep⟩ := exists_birth W p (hW p hp) hp (by omega)
    rw [h c hc p hp] at hstep; contradiction

/-- **Sealed sets are exactly the sets that stay dead whatever happens elsewhere.** A set of cells is sealed
iff every configuration dead on it stays dead on it forever. -/
theorem sealed_iff_run_dead (W : Pt → Bool) (hW : ∀ p, W p = true → p.isCell = true) :
    Sealed W ↔ ∀ c : Config, DeadOn c W → ∀ n, DeadOn (run c n) W := by
  constructor
  · intro hS c hc; exact hS.run_dead hc
  · intro h
    exact (sealed_iff_step_dead W hW).2 (fun c hc => h c hc 1)

/-- **Lemma 1, both halves, in a vessel.** A set of cells is sealed in `V` iff, dead, it is dead one
generation later whatever the configuration in `V` (everything outside `V` dead). -/
theorem sealedIn_iff_step_dead (V W : Pt → Bool) (hW : ∀ p, W p = true → p.isCell = true) :
    SealedIn V W ↔ ∀ c : Config, DeadOn c (fun q => !V q) → DeadOn c W → DeadOn (step c) W := by
  constructor
  · intro hS c hout hc; exact hS.step_dead hout hc
  · intro h p hp
    apply Classical.byContradiction
    intro hlt
    obtain ⟨c, hout, hc, hstep⟩ := exists_birth_in V W p (hW p hp) hp (by omega)
    rw [h c hout hc p hp] at hstep; contradiction

/-- In a slab, a configuration dead outside the slab stays dead outside it (T4). -/
theorem run_dead_outside_slab (d : Diag) (A B : Int) (c : Config)
    (hout : DeadOn c (fun q => !slab d A B q)) : ∀ n, DeadOn (run c n) (fun q => !slab d A B q) := by
  have hin : ∀ p, c p = true → A ≤ d.dot p ∧ d.dot p ≤ B := by
    intro p hp
    cases h : slab d A B p with
    | false => rw [hout p (by simp [h])] at hp; contradiction
    | true => simp only [slab, Bool.and_eq_true, decide_eq_true_eq] at h; exact h.2
  intro n p hp
  cases hr : run c n p with
  | false => rfl
  | true =>
    exfalso
    have hl := slab_closed d A B c hin n p hr
    have hcell : p.isCell = true := by
      cases n with
      | zero =>
        simp only [run] at hr
        cases h : slab d A B p with
        | false => rw [hout p (by simp [h])] at hr; contradiction
        | true => simp only [slab, Bool.and_eq_true] at h; exact h.1
      | succ n =>
        simp only [run, step, Bool.and_eq_true] at hr; exact hr.1
    simp [slab, hcell, hl.1, hl.2] at hp

/-- **Lemma 1 in a slab, forever.** A set of cells is sealed in a slab iff every configuration dead outside
the slab and dead on the set stays dead on the set forever. -/
theorem sealedIn_slab_iff_run_dead (d : Diag) (A B : Int) (W : Pt → Bool)
    (hW : ∀ p, W p = true → p.isCell = true) :
    SealedIn (slab d A B) W ↔
      ∀ c : Config, DeadOn c (fun q => !slab d A B q) → DeadOn c W → ∀ n, DeadOn (run c n) W := by
  constructor
  · intro hS c hout hc n
    induction n with
    | zero => exact hc
    | succ n ih => exact hS.step_dead (run_dead_outside_slab d A B c hout n) ih
  · intro h
    exact (sealedIn_iff_step_dead _ W hW).2 (fun c hout hc => h c hout hc 1)

/-! ## Components, and the last clause of Theorem 3 -/

/-- `U` is a union of neighbour-components of `W`: a neighbour in `W` of a point of `U` is in `U`. -/
def NbrClosed (W U : Pt → Bool) : Prop :=
  ∀ p q, U p = true → q ∈ nbrs p → W q = true → U q = true

/-- Reachability inside `W` through neighbours: `Reach W p q` says `q` is in the component of `p` in `W`. -/
inductive Reach (W : Pt → Bool) (p : Pt) : Pt → Prop
  | refl : W p = true → Reach W p p
  | tail {q r : Pt} : Reach W p q → r ∈ nbrs q → W r = true → Reach W p r

theorem Reach.mem {W : Pt → Bool} {p q : Pt} (h : Reach W p q) : W q = true := by
  induction h with
  | refl h => exact h
  | tail _ _ hr => exact hr

/-- The neighbour-component of `p` in `W`, as an indicator. -/
noncomputable def comp (W : Pt → Bool) (p : Pt) : Pt → Bool :=
  fun q => @decide (Reach W p q) (Classical.propDecidable _)

theorem comp_eq_true {W : Pt → Bool} {p q : Pt} : comp W p q = true ↔ Reach W p q := by
  simp [comp]

theorem comp_closed (W : Pt → Bool) (p : Pt) : NbrClosed W (comp W p) := by
  intro q r hq hr hW
  rw [comp_eq_true] at hq ⊢
  exact Reach.tail hq hr hW

theorem comp_sub (W : Pt → Bool) (p : Pt) : ∀ q, comp W p q = true → W q = true :=
  fun _ h => (comp_eq_true.1 h).mem

/-- Neighbour-closed parts of a set sealed in a vessel are sealed in it (Lemma 2: components of sealed sets
are sealed). -/
theorem SealedIn.of_closed {V W U : Pt → Bool} (hW : SealedIn V W) (hUW : ∀ p, U p = true → W p = true)
    (hcl : NbrClosed W U) : SealedIn V U := by
  intro p hp
  refine Nat.le_trans ?_ (hW p (hUW p hp))
  apply List.countP_mono_left
  intro q hq h
  simp only [Bool.and_eq_true, Bool.not_eq_true'] at h ⊢
  refine ⟨h.1, ?_⟩
  cases hWq : W q with
  | false => rfl
  | true => rw [hcl p q hp hq hWq] at h; exact absurd h.2 (by simp)

theorem countP_le_add (l : List Pt) (P Q R : Pt → Bool)
    (h : ∀ x ∈ l, P x = true → Q x = true ∨ R x = true) :
    l.countP P ≤ l.countP Q + l.countP R := by
  induction l with
  | nil => simp
  | cons a l ih =>
    have ih' := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    have ha := h a (by simp)
    simp only [List.countP_cons]
    cases hP : P a <;> cases hQ : Q a <;> cases hR : R a <;> simp_all <;> omega

/-- **In any vessel, a finite nonempty union of components of a sealed set reaches the vessel's wall**: its
cell furthest along `gen` has at least three of its neighbours outside the vessel. -/
theorem finite_closed_touches (V W U : Pt → Bool) (hW : SealedIn V W) (hUW : ∀ p, U p = true → W p = true)
    (hcl : NbrClosed W U) (L : List Pt) (hL : ∀ p, U p = true → p ∈ L) (hne : ∃ p, U p = true) :
    ∃ p, U p = true ∧ 3 ≤ (nbrs p).countP (fun q => !V q) := by
  obtain ⟨p, hp, hmax⟩ := exists_max_set U L hL hne gen
  refine ⟨p, hp, ?_⟩
  have hU := hW.of_closed hUW hcl p hp
  have h6 : 6 ≤ (nbrs p).countP (fun q => decide (gen p < gen q)) := by
    rw [← gen_pos_count p.axis]
    unfold nbrs
    rw [List.countP_map]
    apply Nat.le_of_eq
    apply List.countP_congr
    intro o _
    simp only [Function.comp, gen_add, decide_eq_true_eq]
    omega
  have := countP_le_add (nbrs p) (fun q => decide (gen p < gen q)) (fun q => V q && !U q) (fun q => !V q)
    (by
      intro q _ hq
      simp only [decide_eq_true_eq] at hq
      cases hVq : V q with
      | false => right; rfl
      | true =>
        left
        cases hUq : U q with
        | false => rfl
        | true => have := hmax q hUq; omega)
  omega

/-- The eight body diagonals. -/
def Diag.all : List Diag :=
  [⟨true, true, true⟩, ⟨true, true, false⟩, ⟨true, false, true⟩, ⟨true, false, false⟩,
   ⟨false, true, true⟩, ⟨false, true, false⟩, ⟨false, false, true⟩, ⟨false, false, false⟩]

theorem Diag.mem_all (d : Diag) : d ∈ Diag.all := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> decide

/-- A diagonal-hull vessel: the cells with `d·p ≤ C d` for each of the eight body diagonals (an octahedron,
possibly truncated). -/
def hullV (C : Diag → Int) : Pt → Bool :=
  fun p => p.isCell && Diag.all.all (fun d => decide (d.dot p ≤ C d))

theorem hullV_iff (C : Diag → Int) (p : Pt) :
    hullV C p = true ↔ p.isCell = true ∧ ∀ d, d.dot p ≤ C d := by
  simp only [hullV, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq]
  exact ⟨fun ⟨h1, h2⟩ => ⟨h1, fun d => h2 d (Diag.mem_all d)⟩, fun ⟨h1, h2⟩ => ⟨h1, fun d _ => h2 d⟩⟩

/-- The integers in `[-M, M]`. -/
def ints (M : Nat) : List Int := (List.range (2 * M + 1)).map (fun (i : Nat) => (i : Int) - (M : Int))

theorem mem_ints (M : Nat) (x : Int) (h1 : -(M : Int) ≤ x) (h2 : x ≤ M) : x ∈ ints M := by
  simp only [ints, List.mem_map, List.mem_range]
  exact ⟨(x + M).toNat, by omega, by omega⟩

/-- The points of the box `[-M, M]³`. -/
def box (M : Nat) : List Pt :=
  (ints M).flatMap (fun x => (ints M).flatMap (fun y => (ints M).map (fun z => ⟨x, y, z⟩)))

theorem mem_box (M : Nat) (p : Pt) (hx : -(M : Int) ≤ p.x ∧ p.x ≤ M) (hy : -(M : Int) ≤ p.y ∧ p.y ≤ M)
    (hz : -(M : Int) ≤ p.z ∧ p.z ≤ M) : p ∈ box M := by
  simp only [box, List.mem_flatMap, List.mem_map]
  exact ⟨p.x, mem_ints M _ hx.1 hx.2, p.y, mem_ints M _ hy.1 hy.2, p.z, mem_ints M _ hz.1 hz.2, rfl⟩

theorem natAbs_le_sum (C : Diag → Int) (l : List Diag) (d : Diag) (hd : d ∈ l) :
    (C d).natAbs ≤ (l.map (fun e => (C e).natAbs)).sum := by
  induction l with
  | nil => simp at hd
  | cons a l ih =>
    simp only [List.map_cons, List.sum_cons]
    rcases List.mem_cons.1 hd with rfl | h
    · omega
    · have := ih h; omega

/-- A diagonal-hull vessel is finite: it lies in a box. -/
theorem hullV_finite (C : Diag → Int) :
    ∀ p, hullV C p = true → p ∈ box ((Diag.all.map (fun e => (C e).natAbs)).sum) := by
  intro p hp
  obtain ⟨_, hd⟩ := (hullV_iff C p).1 hp
  let d : Diag := ⟨decide (0 ≤ p.x), decide (0 ≤ p.y), decide (0 ≤ p.z)⟩
  have h1 := hd d
  have h2 := natAbs_le_sum C Diag.all d (Diag.mem_all d)
  have hdot : d.dot p = p.x.natAbs + p.y.natAbs + p.z.natAbs := by
    simp only [d, Diag.dot, sg]
    split <;> split <;> split <;> simp_all <;> omega
  apply mem_box <;> omega

/-- **Theorem 3, last clause.** In a diagonal-hull vessel every component of a sealed set has a cell adjacent
to the vessel's outside; indeed a cell with at least three neighbours outside. -/
theorem hull_component_touches (C : Diag → Int) (W : Pt → Bool) (hW : SealedIn (hullV C) W)
    (hWV : ∀ p, W p = true → hullV C p = true) (p : Pt) (hp : W p = true) :
    ∃ q, Reach W p q ∧ 3 ≤ (nbrs q).countP (fun r => !hullV C r) := by
  obtain ⟨q, hq, h3⟩ := finite_closed_touches (hullV C) W (comp W p) hW (comp_sub W p) (comp_closed W p)
    (box ((Diag.all.map (fun e => (C e).natAbs)).sum))
    (fun q hq => hullV_finite C q (hWV q (comp_sub W p q hq))) ⟨p, comp_eq_true.2 (Reach.refl hp)⟩
  exact ⟨q, comp_eq_true.1 hq, h3⟩

/-- **Theorem 3, components, full lattice.** Every component of a sealed set is infinite. -/
theorem sealed_component_infinite (W : Pt → Bool) (hW : Sealed W) (p : Pt) (hp : W p = true) :
    ¬ ∃ L : List Pt, ∀ q, Reach W p q → q ∈ L := by
  rintro ⟨L, hL⟩
  have hW' : SealedIn (fun _ => true) W := (sealedIn_univ_iff W).2 hW
  have := (sealedIn_univ_iff _).1 (hW'.of_closed (comp_sub W p) (comp_closed W p))
  exact not_sealed_of_finite (comp W p) L (fun q hq => hL q (comp_eq_true.1 hq))
    ⟨p, comp_eq_true.2 (Reach.refl hp)⟩ this

/-- **Theorem 3, components, slab of at least three layers.** Every component of a set sealed in the slab is
infinite. -/
theorem slab_component_infinite (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B)
    (W : Pt → Bool) (hW : SealedIn (slab d A B) W) (hWV : ∀ p, W p = true → slab d A B p = true)
    (p : Pt) (hp : W p = true) :
    ¬ ∃ L : List Pt, ∀ q, Reach W p q → q ∈ L := by
  rintro ⟨L, hL⟩
  exact slab_not_sealed_of_finite d A B h3 (comp W p) (fun q hq => hWV q (comp_sub W p q hq)) L
    (fun q hq => hL q (comp_eq_true.1 hq)) ⟨p, comp_eq_true.2 (Reach.refl hp)⟩
    (hW.of_closed (comp_sub W p) (comp_closed W p))

end Gump
