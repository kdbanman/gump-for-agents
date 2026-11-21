/-
Consequences of T2 for finite patterns (`docs/AUTOMATON.md` section 3): the diagonal hull holds finitely
many cells, so every finite seed is eventually periodic, within 2^N + 1 generations where N is the
number of cells of the hull; and there are no spaceships: no finite nonempty pattern
reappears translated by a nonzero vector, at any generation.
-/
import Gump.Sealed

namespace Gump

/-- `run` composes. -/
theorem run_add (c : Config) (m : Nat) : ∀ n, run c (m + n) = run (run c m) n
  | 0 => rfl
  | n + 1 => by rw [← Nat.add_assoc, run, run, run_add c m n]

/-! ### A pigeonhole principle -/

/-- **Pigeonhole.** A sequence with values in a list of length k repeats among its first k + 1 terms. -/
theorem pigeonhole {α : Type} (f : Nat → α) (S : List α) (h : ∀ n, f n ∈ S) :
    ∃ i j, i < j ∧ j ≤ S.length ∧ f i = f j := by
  apply Classical.byContradiction
  intro hne
  have hnd : ((List.range (S.length + 1)).map f).Nodup := by
    rw [List.nodup_iff_pairwise_ne, List.pairwise_map]
    apply List.Pairwise.imp_of_mem _ List.pairwise_lt_range
    intro a b _ hb hab heq
    simp only [List.mem_range] at hb
    exact hne ⟨a, b, hab, by omega, heq⟩
  have := hnd.length_le_of_subset (fun x hx => by
    obtain ⟨n, _, rfl⟩ := List.mem_map.mp hx
    exact h n)
  simp at this
  omega

/-- All lists of booleans of length k. -/
def boolLists : Nat → List (List Bool)
  | 0 => [[]]
  | k + 1 => (boolLists k).map (false :: ·) ++ (boolLists k).map (true :: ·)

theorem length_boolLists : ∀ k, (boolLists k).length = 2 ^ k
  | 0 => rfl
  | k + 1 => by simp only [boolLists, List.length_append, List.length_map, length_boolLists k]; omega

theorem mem_boolLists : ∀ l : List Bool, l ∈ boolLists l.length
  | [] => by simp [boolLists]
  | b :: l => by
    cases b <;> simp [boolLists, mem_boolLists l]

/-! ### The hull holds finitely many cells -/

/-- The eight body diagonals. -/
def allDiags : List Diag :=
  [⟨true, true, true⟩, ⟨true, true, false⟩, ⟨true, false, true⟩, ⟨true, false, false⟩,
   ⟨false, true, true⟩, ⟨false, true, false⟩, ⟨false, false, true⟩, ⟨false, false, false⟩]

theorem mem_allDiags (d : Diag) : d ∈ allDiags := by
  obtain ⟨a, b, c⟩ := d; cases a <;> cases b <;> cases c <;> decide

/-- Every point with all three coordinates in [-R, R]. -/
def box (R : Nat) : List Pt :=
  (List.range (2 * R + 1)).flatMap fun (i : Nat) => (List.range (2 * R + 1)).flatMap fun (j : Nat) =>
    (List.range (2 * R + 1)).map fun (k : Nat) => (⟨(i : Int) - R, (j : Int) - R, (k : Int) - R⟩ : Pt)

theorem mem_box {R : Nat} {p : Pt} (hx : p.x.natAbs ≤ R) (hy : p.y.natAbs ≤ R) (hz : p.z.natAbs ≤ R) :
    p ∈ box R := by
  obtain ⟨x, y, z⟩ := p
  simp only at hx hy hz
  simp only [box, List.mem_flatMap, List.mem_map, List.mem_range, Pt.mk.injEq]
  exact ⟨(x + R).toNat, by omega, (y + R).toNat, by omega, (z + R).toNat, by omega, by omega, by omega,
    by omega⟩

/-- A radius that holds the region `d·p ≤ C d` for all eight diagonals. -/
def hullR (C : Diag → Int) : Nat := (allDiags.map fun d => (C d).toNat).foldr (· + ·) 0

/-- Whether a point lies in the region `d·p ≤ C d` for all eight diagonals. -/
def inHull (C : Diag → Int) (p : Pt) : Bool := allDiags.all fun d => decide (d.dot p ≤ C d)

/-- **The cells of a diagonal hull, as a finite list.** -/
def hullCells (C : Diag → Int) : List Pt := (box (hullR C)).filter fun p => p.isCell && inHull C p

theorem inHull_iff (C : Diag → Int) (p : Pt) : inHull C p = true ↔ ∀ d, d.dot p ≤ C d := by
  simp only [inHull, List.all_eq_true, decide_eq_true_eq]
  exact ⟨fun h d => h d (mem_allDiags d), fun h d _ => h d⟩

theorem le_foldr_add {l : List Nat} {a : Nat} (h : a ∈ l) : a ≤ l.foldr (· + ·) 0 := by
  induction l with
  | nil => simp at h
  | cons b l ih =>
    simp only [List.mem_cons] at h
    simp only [List.foldr_cons]
    rcases h with rfl | h
    · omega
    · have := ih h; omega

/-- The diagonal of a point's own signs. -/
def signDiag (p : Pt) : Diag := ⟨decide (0 ≤ p.x), decide (0 ≤ p.y), decide (0 ≤ p.z)⟩

/-- The L1 norm is the layer along the diagonal of the point's own signs. -/
theorem dot_signDiag (p : Pt) : (signDiag p).dot p = p.x.natAbs + p.y.natAbs + p.z.natAbs := by
  obtain ⟨x, y, z⟩ := p
  simp only [signDiag, Diag.dot, sg]
  by_cases hx : 0 ≤ x <;> by_cases hy : 0 ≤ y <;> by_cases hz : 0 ≤ z <;> simp [hx, hy, hz] <;> omega

theorem l1_le_hullR (C : Diag → Int) (p : Pt) (h : ∀ d, d.dot p ≤ C d) :
    p.x.natAbs + p.y.natAbs + p.z.natAbs ≤ hullR C := by
  have hd := h (signDiag p)
  rw [dot_signDiag] at hd
  have hm : (C (signDiag p)).toNat ≤ hullR C :=
    le_foldr_add (List.mem_map_of_mem (f := fun d => (C d).toNat) (mem_allDiags _))
  omega

/-- **The hull holds finitely many cells**: every cell of the region `d·p ≤ C d` is in `hullCells C`,
and conversely. -/
theorem mem_hullCells (C : Diag → Int) (p : Pt) :
    p ∈ hullCells C ↔ p.isCell = true ∧ ∀ d, d.dot p ≤ C d := by
  simp only [hullCells, List.mem_filter, Bool.and_eq_true, inHull_iff]
  constructor
  · exact fun h => h.2
  · intro h
    refine ⟨?_, h⟩
    have := l1_le_hullR C p h.2
    exact mem_box (by omega) (by omega) (by omega)

/-- The box lists each point once. -/
theorem box_nodup (R : Nat) : (box R).Nodup := by
  unfold box
  rw [List.nodup_iff_pairwise_ne, List.pairwise_flatMap]
  refine ⟨fun i _ => ?_, ?_⟩
  · rw [List.pairwise_flatMap]
    refine ⟨fun j _ => ?_, ?_⟩
    · rw [List.pairwise_map]
      refine List.Pairwise.imp ?_ List.pairwise_lt_range
      intro a b hab e
      simp only [Pt.mk.injEq] at e
      omega
    · refine List.Pairwise.imp ?_ List.pairwise_lt_range
      intro a b hab x hx y hy e
      simp only [List.mem_map, List.mem_range] at hx hy
      obtain ⟨k, _, rfl⟩ := hx
      obtain ⟨k', _, rfl⟩ := hy
      simp only [Pt.mk.injEq] at e
      omega
  · refine List.Pairwise.imp ?_ List.pairwise_lt_range
    intro a b hab x hx y hy e
    simp only [List.mem_flatMap, List.mem_map, List.mem_range] at hx hy
    obtain ⟨j, _, k, _, rfl⟩ := hx
    obtain ⟨j', _, k', _, rfl⟩ := hy
    simp only [Pt.mk.injEq] at e
    omega

/-- **The list of the hull's cells has no repetition**, so its length is the number of cells of the hull. -/
theorem hullCells_nodup (C : Diag → Int) : (hullCells C).Nodup :=
  List.Pairwise.filter _ (box_nodup _)

/-! ### Every finite seed is eventually periodic -/

/-- **Every pattern inside a diagonal hull is eventually periodic**, and enters its cycle within
2^N + 1 generations, N = `(hullCells C).length` the number of cells of the hull (`mem_hullCells`,
`hullCells_nodup`): there are μ and T > 0 with
μ + T ≤ 2^N + 1 and `run c (n + T) = run c n` for every n ≥ μ. -/
theorem eventually_periodic (c : Config) (C : Diag → Int) (h : ∀ p, c p = true → ∀ d, d.dot p ≤ C d) :
    ∃ μ T, 0 < T ∧ μ + T ≤ 2 ^ (hullCells C).length + 1 ∧ ∀ n, μ ≤ n → run c (n + T) = run c n := by
  have hlive : ∀ n p, run c (n + 1) p = true → p ∈ hullCells C := by
    intro n p hp
    rw [mem_hullCells]
    refine ⟨?_, hull C c h (n + 1) p hp⟩
    simp only [run, step, Bool.and_eq_true] at hp
    exact hp.1
  let f : Nat → List Bool := fun n => (hullCells C).map (run c (n + 1))
  have hf : ∀ n, f n ∈ boolLists (hullCells C).length := fun n => by
    have := mem_boolLists (f n)
    simpa [f] using this
  obtain ⟨i, j, hij, hj, heq⟩ := pigeonhole f _ hf
  rw [length_boolLists] at hj
  have hrun : run c (i + 1) = run c (j + 1) := by
    funext p
    by_cases hp : p ∈ hullCells C
    · exact List.map_inj_left.mp heq p hp
    · cases h1 : run c (i + 1) p <;> cases h2 : run c (j + 1) p
      · rfl
      · exact absurd (hlive j p h2) hp
      · exact absurd (hlive i p h1) hp
      · rfl
  refine ⟨i + 1, j - i, by omega, by omega, ?_⟩
  intro n hn
  have e1 : n + (j - i) = (j + 1) + (n - (i + 1)) := by omega
  have e2 : n = (i + 1) + (n - (i + 1)) := by omega
  rw [e1, run_add, ← hrun, ← run_add, ← e2]

/-- An upper bound for the layers of a finite list along every diagonal. -/
def listBound (L : List Pt) : Int := ((L.map fun p => p.x.natAbs + p.y.natAbs + p.z.natAbs).foldr (· + ·) 0 : Nat)

theorem dot_le_listBound {L : List Pt} {p : Pt} (hp : p ∈ L) (d : Diag) : d.dot p ≤ listBound L := by
  have hsum : ∀ (l : List Pt), p ∈ l →
      p.x.natAbs + p.y.natAbs + p.z.natAbs ≤ (l.map fun p => p.x.natAbs + p.y.natAbs + p.z.natAbs).foldr (· + ·) 0 := by
    intro l hl
    induction l with
    | nil => simp at hl
    | cons q l ih =>
      simp only [List.mem_cons] at hl
      simp only [List.map_cons, List.foldr_cons]
      rcases hl with rfl | hl
      · omega
      · have := ih hl; omega
  have := hsum L hp
  unfold listBound
  obtain ⟨sx, sy, sz⟩ := d
  cases sx <;> cases sy <;> cases sz <;> simp only [Diag.dot, sg] <;> simp <;> omega

/-- **Every finite seed is eventually periodic.** If every live point of `c` is in the finite list `L`,
there are μ and T > 0 with `run c (n + T) = run c n` for every n ≥ μ. -/
theorem finite_eventually_periodic (c : Config) (L : List Pt) (hL : ∀ p, c p = true → p ∈ L) :
    ∃ μ T, 0 < T ∧ ∀ n, μ ≤ n → run c (n + T) = run c n := by
  obtain ⟨μ, T, hT, _, h⟩ := eventually_periodic c (fun _ => listBound L)
    (fun p hp d => dot_le_listBound (hL p hp) d)
  exact ⟨μ, T, hT, h⟩

/-! ### No spaceships -/

theorem exists_max {l : List Pt} (f : Pt → Int) (hl : l ≠ []) : ∃ a ∈ l, ∀ b ∈ l, f b ≤ f a := by
  induction l with
  | nil => exact absurd rfl hl
  | cons q l ih =>
    by_cases hl' : l = []
    · subst hl'; exact ⟨q, by simp, by simp⟩
    · obtain ⟨a, ha, hmax⟩ := ih hl'
      by_cases hqa : f a ≤ f q
      · refine ⟨q, by simp, ?_⟩
        intro b hb
        simp only [List.mem_cons] at hb
        rcases hb with rfl | hb
        · exact Int.le_refl _
        · exact Int.le_trans (hmax b hb) hqa
      · refine ⟨a, by simp [ha], ?_⟩
        intro b hb
        simp only [List.mem_cons] at hb
        rcases hb with rfl | hb
        · omega
        · exact hmax b hb

/-- A finite nonempty pattern has a live point furthest along any diagonal. -/
theorem exists_extreme (c : Config) (L : List Pt) (hL : ∀ p, c p = true → p ∈ L) (hne : ∃ p, c p = true)
    (d : Diag) : ∃ a, c a = true ∧ ∀ b, c b = true → d.dot b ≤ d.dot a := by
  obtain ⟨p, hp⟩ := hne
  have hl : L.filter c ≠ [] := by
    intro h
    have : p ∈ L.filter c := List.mem_filter.mpr ⟨hL p hp, hp⟩
    simp [h] at this
  obtain ⟨a, ha, hmax⟩ := exists_max d.dot hl
  refine ⟨a, (List.mem_filter.mp ha).2, fun b hb => hmax b (List.mem_filter.mpr ⟨hL b hb, hb⟩)⟩

/-- **No spaceships.** If a finite nonempty pattern, at some generation T, contains its own translate by
v, then v = 0. (A spaceship of any period would be such a pattern; so would a pattern that only grows
in one direction.) -/
theorem no_spaceship (c : Config) (L : List Pt) (hL : ∀ p, c p = true → p ∈ L) (hne : ∃ p, c p = true)
    (T : Nat) (v : Pt) (h : ∀ p, c p = true → run c T (p + v) = true) : v = ⟨0, 0, 0⟩ := by
  have key : ∀ d : Diag, d.dot v ≤ 0 := by
    intro d
    obtain ⟨a, ha, hmax⟩ := exists_extreme c L hL hne d
    apply Classical.byContradiction
    intro hv
    have hdead : ∀ q, d.dot a < d.dot q → c q = false := by
      intro q hq
      cases hcq : c q with
      | false => rfl
      | true => have := hmax q hcq; omega
    have := confinement d (d.dot a) c hdead T (a + v) (by rw [Diag.dot_add]; omega)
    rw [h a ha] at this
    contradiction
  have h1 := key ⟨true, true, true⟩; have h2 := key ⟨false, false, false⟩
  have h3 := key ⟨true, false, false⟩; have h4 := key ⟨false, true, true⟩
  have h5 := key ⟨false, true, false⟩; have h6 := key ⟨true, false, true⟩
  obtain ⟨x, y, z⟩ := v
  simp only [Diag.dot, sg] at h1 h2 h3 h4 h5 h6
  simp only [Pt.mk.injEq]
  simp at h1 h2 h3 h4 h5 h6
  omega

end Gump
