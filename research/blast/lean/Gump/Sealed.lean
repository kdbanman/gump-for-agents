/-
Sealed sets, and from them T2 (octahedral confinement), T3 (firewall) and T4 (closed sub-automata)
of `docs/AUTOMATON.md`, with the opening statement of T6: a dead sealed set stays dead whatever
happens elsewhere, and unions of sealed sets are sealed.

A set is sealed if each of its points has at most three neighbours outside it. Birth needs four.
-/
import Gump.Layers

namespace Gump

/-- A set of points, given by its indicator, is *sealed* if each of its points has at most three
neighbours outside it. -/
def Sealed (S : Pt → Bool) : Prop :=
  ∀ p, S p = true → (nbrs p).countP (fun q => !S q) ≤ 3

/-- The configuration is dead on the set. -/
def DeadOn (c : Config) (S : Pt → Bool) : Prop := ∀ p, S p = true → c p = false

/-- **A dead sealed set is dead one generation later, whatever happens elsewhere.** -/
theorem Sealed.step_dead {S : Pt → Bool} (hS : Sealed S) {c : Config} (hc : DeadOn c S) :
    DeadOn (step c) S := by
  intro p hp
  apply step_dead_of_count_le_three (hc p hp)
  refine Nat.le_trans ?_ (hS p hp)
  unfold count
  apply List.countP_mono_left
  intro q _ hq
  cases hSq : S q with
  | false => rfl
  | true => rw [hc q hSq] at hq; contradiction

/-- **A dead sealed set stays dead forever.** -/
theorem Sealed.run_dead {S : Pt → Bool} (hS : Sealed S) {c : Config} (hc : DeadOn c S) :
    ∀ n, DeadOn (run c n) S
  | 0 => hc
  | n + 1 => hS.step_dead (hS.run_dead hc n)

/-- Unions of sealed sets are sealed. -/
theorem Sealed.union {S T : Pt → Bool} (hS : Sealed S) (hT : Sealed T) :
    Sealed (fun p => S p || T p) := by
  intro p hp
  have key : ∀ (U : Pt → Bool), (nbrs p).countP (fun q => !U q) ≤ 3 →
      (∀ q, U q = true → (S q || T q) = true) →
      (nbrs p).countP (fun q => !(S q || T q)) ≤ 3 := by
    intro U hU hsub
    refine Nat.le_trans ?_ hU
    apply List.countP_mono_left
    intro q _ hq
    cases hUq : U q with
    | false => rfl
    | true => rw [hsub q hUq] at hq; contradiction
  cases hSp : S p with
  | true => exact key S (hS p hSp) (fun q h => by simp [h])
  | false =>
    have hTp : T p = true := by simpa [hSp] using hp
    exact key T (hT p hTp) (fun q h => by simp [h])

/-- The open half-space above layer C along a diagonal. -/
def above (d : Diag) (C : Int) : Pt → Bool := fun p => decide (C < d.dot p)

/-- A band of six layers along a diagonal: C < s ≤ C + 6 (three consecutive layers of the lattice). -/
def band (d : Diag) (C : Int) : Pt → Bool := fun p => decide (C < d.dot p ∧ d.dot p ≤ C + 6)

/-- Half-spaces across a body diagonal are sealed. -/
theorem above_sealed (d : Diag) (C : Int) : Sealed (above d C) := by
  intro p hp
  have hp' : C < d.dot p := by simpa [above] using hp
  unfold nbrs
  rw [List.countP_map]
  refine Nat.le_trans ?_ (below_le_three p.axis d)
  apply List.countP_mono_left
  intro o _ ho
  simp [above, Diag.dot_add] at ho
  simp only [decide_eq_true_eq]
  omega

/-- Bands of three consecutive layers across a body diagonal are sealed. -/
theorem band_sealed (d : Diag) (C : Int) : Sealed (band d C) := by
  intro p hp
  have hp' : C < d.dot p ∧ d.dot p ≤ C + 6 := by simpa [band] using hp
  unfold nbrs
  rw [List.countP_map]
  refine Nat.le_trans ?_ (outside_band_le_three p.axis d (d.dot p - C) (by omega) (by omega))
  apply List.countP_mono_left
  intro o _ ho
  simp [band, Diag.dot_add] at ho
  simp only [decide_eq_true_eq]
  omega

/-- **T2 (octahedral confinement).** If every point above layer C along a body diagonal is dead, that
stays true forever. -/
theorem confinement (d : Diag) (C : Int) (c : Config) (h : ∀ p, C < d.dot p → c p = false) :
    ∀ n p, C < d.dot p → run c n p = false := by
  intro n p hp
  have hdead : DeadOn c (above d C) := fun q hq => h q (by simpa [above] using hq)
  exact (above_sealed d C).run_dead hdead n p (by simpa [above] using hp)

/-- **T3 (firewall), first half.** If three consecutive layers along a body diagonal are dead, they
stay dead forever. -/
theorem firewall (d : Diag) (C : Int) (c : Config)
    (h : ∀ p, C < d.dot p → d.dot p ≤ C + 6 → c p = false) :
    ∀ n p, C < d.dot p → d.dot p ≤ C + 6 → run c n p = false := by
  intro n p h1 h2
  have hdead : DeadOn c (band d C) := fun q hq => by
    have := (by simpa [band] using hq : C < d.dot q ∧ d.dot q ≤ C + 6)
    exact h q this.1 this.2
  exact (band_sealed d C).run_dead hdead n p (by simp [band, h1, h2])

/-- **T4 (closed sub-automata).** A pattern contained in the layers A ≤ s ≤ B stays in them. -/
theorem slab_closed (d : Diag) (A B : Int) (c : Config)
    (h : ∀ p, c p = true → A ≤ d.dot p ∧ d.dot p ≤ B) :
    ∀ n p, run c n p = true → A ≤ d.dot p ∧ d.dot p ≤ B := by
  intro n p hp
  have up : ∀ q, B < d.dot q → c q = false := by
    intro q hq
    cases hc : c q with
    | false => rfl
    | true => have := (h q hc).2; omega
  have down : ∀ q, -A < d.neg.dot q → c q = false := by
    intro q hq
    rw [Diag.neg_dot] at hq
    cases hc : c q with
    | false => rfl
    | true => have := (h q hc).1; omega
  constructor
  · apply Classical.byContradiction
    intro hlt
    have := confinement d.neg (-A) c down n p (by rw [Diag.neg_dot]; omega)
    rw [this] at hp; contradiction
  · apply Classical.byContradiction
    intro hgt
    have := confinement d B c up n p (by omega)
    rw [this] at hp; contradiction

/-- **The diagonal hull.** A pattern that lies inside an intersection of half-spaces d·p ≤ C d, one for
each body diagonal (an octahedron, possibly truncated), stays inside it forever. With the tightest
C this is the pattern's diagonal hull; applied again from any later generation, the hull can only
shrink. -/
theorem hull (C : Diag → Int) (c : Config) (h : ∀ p, c p = true → ∀ d, d.dot p ≤ C d) :
    ∀ n p, run c n p = true → ∀ d, d.dot p ≤ C d := by
  intro n p hp d
  apply Classical.byContradiction
  intro hgt
  have hdead : ∀ q, C d < d.dot q → c q = false := by
    intro q hq
    cases hc : c q with
    | false => rfl
    | true => have := h q hc d; omega
  have := confinement d (C d) c hdead n p (by omega)
  rw [this] at hp; contradiction

/-- One generation does not carry anything across a dead band: two configurations that are dead on
the band and agree below it agree below it one generation later. -/
theorem step_agree_below (d : Diag) (C : Int) (c c' : Config)
    (hc : DeadOn c (band d C)) (hc' : DeadOn c' (band d C))
    (hag : ∀ p, d.dot p ≤ C → c p = c' p) :
    ∀ p, d.dot p ≤ C → step c p = step c' p := by
  intro p hp
  have hcount : count c p = count c' p := by
    unfold count nbrs
    rw [List.countP_map, List.countP_map]
    apply List.countP_congr
    intro o ho
    have h4 := dot_offset_le_four p.axis d o ho
    by_cases hq : d.dot (p + o) ≤ C
    · simp [Function.comp, hag (p + o) hq]
    · have hb : band d C (p + o) = true := by
        rw [Diag.dot_add] at hq
        simp [band, Diag.dot_add]; omega
      simp [Function.comp, hc (p + o) hb, hc' (p + o) hb]
  simp [step, hag p hp, hcount]

/-- **T3 (firewall), second half.** Across three dead consecutive layers the two sides never
influence each other again: two histories that start dead on the band and equal below it stay equal
below it forever. -/
theorem firewall_separates (d : Diag) (C : Int) (c c' : Config)
    (hc : DeadOn c (band d C)) (hc' : DeadOn c' (band d C))
    (hag : ∀ p, d.dot p ≤ C → c p = c' p) :
    ∀ n p, d.dot p ≤ C → run c n p = run c' n p
  | 0 => hag
  | n + 1 => step_agree_below d C (run c n) (run c' n)
      ((band_sealed d C).run_dead hc n) ((band_sealed d C).run_dead hc' n)
      (firewall_separates d C c c' hc hc' hag n)

end Gump
