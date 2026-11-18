/-
T5, the threshold lemma (`docs/AUTOMATON.md` section 3; `research/theory/threshold.md`), for gump itself
on a finite vessel: a finite set V of points that holds every live point at every generation (for a
finite seed, the cells of its diagonal hull, `Gump.hullCells`, by T2).

Notation (threshold.md section 1), with x(t) = `run c t` as 0/1 and h_p(t) = n_p(t) + x_p(t):
  F t = 2 E(t+1) = -2 Σ_p x_p(t+1) h_p(t) + 7 Σ_p (x_p(t+1) + x_p(t))      (doubled, to stay in ℤ)
Proved here:
  `energy_step`      F(t+1) - F(t) = -Σ_p (x_p(t+2) - x_p(t)) (2 h_p(t+1) - 7)            (★)
  `energy_identity`  F(t+1) - F(t) = drive t - diss t, exactly: the drive is Σ (2h - 7) over O1 events
                     (overcrowded at t+1, n ≥ 6, and live at t), the dissipation Σ |2h - 7| over the
                     mismatches x(t+2) ≠ x(t) at cells that are not overcrowded               (ΔE = D - Q)
  `energy_bounds`    -12 |V| ≤ F t ≤ 14 |V|                                   (-6N ≤ E ≤ 7N)
  `period_two_of_no_O1`  with no O1 event from T on, the orbit has period ≤ 2 from some t₀ ≤ T + 26 |V| on
  `oscillator_period_two`  an orbit periodic from μ with no O1 event from μ on has period ≤ 2 from μ on
                     (so every oscillator of period ≥ 3 has an O1 event)
The symmetry of the neighbourhood (`Gump.nbrs_symm`) is what makes x(t)ᵀ W x(t-1) symmetric in its two
arguments; it is the only place the geometry enters.
-/
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Gump.Symm
import Gump.Periodic

namespace Gump.Threshold
open Gump Finset

/-- A state as 0 or 1. -/
def ind (b : Bool) : ℤ := if b then 1 else 0

theorem ind_nonneg (b : Bool) : 0 ≤ ind b := by cases b <;> simp [ind]
theorem ind_le_one (b : Bool) : ind b ≤ 1 := by cases b <;> simp [ind]

theorem nbrs_nodup (p : Pt) : (nbrs p).Nodup := by
  apply (offsets_nodup p.axis).map
  intro o o' h
  obtain ⟨a, b, c⟩ := o
  obtain ⟨a', b', c'⟩ := o'
  simp only [Pt.mk.injEq]
  have h1 := congrArg Pt.x h; have h2 := congrArg Pt.y h; have h3 := congrArg Pt.z h
  simp only [Pt.add_x, Pt.add_y, Pt.add_z] at h1 h2 h3
  omega

theorem countP_eq_sum (l : List Pt) (f : Pt → Bool) : (l.countP f : ℤ) = (l.map fun q => ind (f q)).sum := by
  induction l with
  | nil => simp
  | cons q l ih =>
    rw [List.countP_cons, List.map_cons, List.sum_cons, ← ih]
    cases f q <;> simp [ind] <;> ring

theorem count_le (b : Config) (p : Pt) : count b p ≤ 12 := by
  unfold count
  have := List.countP_le_length (p := b) (l := nbrs p)
  rw [nbrs_length] at this
  exact this

variable (V : Finset Pt)

/-- The live-neighbour count as a sum over the vessel, for a configuration living in the vessel. -/
theorem count_eq_sum (b : Config) (hb : ∀ q, b q = true → q ∈ V) (p : Pt) :
    (count b p : ℤ) = ∑ q ∈ V, if q ∈ nbrs p then ind (b q) else 0 := by
  unfold count
  rw [countP_eq_sum, ← List.sum_toFinset _ (nbrs_nodup p)]
  have : ∀ q, (if q ∈ nbrs p then ind (b q) else 0) = if q ∈ (nbrs p).toFinset then ind (b q) else 0 := by
    intro q; simp
  simp only [this, Finset.sum_ite_mem]
  symm
  apply Finset.sum_subset Finset.inter_subset_right
  intro q _ hq
  have : b q = false := by
    cases hbq : b q with
    | false => rfl
    | true => exact absurd (Finset.mem_inter.mpr ⟨hb q hbq, by assumption⟩) hq
  simp [this, ind]

/-- Σ_{p ∈ V} [a p] h_b(p), with h_b = (live neighbours in b) + [b p]: the form x(t)ᵀ (A + I) x(t-1). -/
def pair (a b : Config) : ℤ := ∑ p ∈ V, ind (a p) * ((count b p : ℤ) + ind (b p))

/-- **The pairing is symmetric** for configurations living on cells of the vessel (by `nbrs_symm`). -/
theorem pair_comm (a b : Config) (ha : ∀ q, a q = true → q ∈ V ∧ q.isCell = true)
    (hb : ∀ q, b q = true → q ∈ V ∧ q.isCell = true) : pair V a b = pair V b a := by
  have key : ∀ (a b : Config), (∀ q, b q = true → q ∈ V) →
      pair V a b = ∑ p ∈ V, ∑ q ∈ V, ((if q ∈ nbrs p then ind (a p) * ind (b q) else 0) +
        if q = p then ind (a p) * ind (b q) else 0) := by
    intro a b hb'
    unfold pair
    apply Finset.sum_congr rfl
    intro p hp
    rw [count_eq_sum V b hb' p, Finset.sum_add_distrib, Finset.sum_ite_eq' V p, if_pos hp, mul_add,
      Finset.mul_sum]
    congr 1
    apply Finset.sum_congr rfl
    intro q _
    split <;> simp
  rw [key a b (fun q h => (hb q h).1), key b a (fun q h => (ha q h).1), Finset.sum_comm]
  apply Finset.sum_congr rfl; intro p _
  apply Finset.sum_congr rfl; intro q _
  -- the term for (p, q) on the left is the term for (q, p) on the right
  congr 1
  · by_cases hap : a q = true
    · by_cases hbq : b p = true
      · have hs := nbrs_symm (ha q hap).2 (hb p hbq).2
        by_cases h1 : p ∈ nbrs q
        · rw [if_pos h1, if_pos (hs.mp h1), mul_comm]
        · rw [if_neg h1, if_neg (fun h => h1 (hs.mpr h))]
      · simp at hbq; simp [hbq, ind]
    · simp at hap; simp [hap, ind]
  · by_cases h : p = q
    · subst h; simp [mul_comm]
    · rw [if_neg h, if_neg (Ne.symm h)]

theorem pair_nonneg (a b : Config) : 0 ≤ pair V a b := by
  unfold pair
  apply Finset.sum_nonneg
  intro p _
  exact mul_nonneg (ind_nonneg _) (add_nonneg (by positivity) (ind_nonneg _))

/-- The number of live points of a configuration in the vessel. -/
def pop (a : Config) : ℤ := ∑ p ∈ V, ind (a p)

theorem pop_le (a : Config) : pop V a ≤ V.card := by
  unfold pop
  calc ∑ p ∈ V, ind (a p) ≤ ∑ _p ∈ V, (1 : ℤ) := Finset.sum_le_sum (fun p _ => ind_le_one _)
    _ = V.card := by simp

theorem pop_nonneg (a : Config) : 0 ≤ pop V a := Finset.sum_nonneg (fun p _ => ind_nonneg _)

theorem pair_le (a b : Config) : pair V a b ≤ 13 * pop V a := by
  unfold pair pop
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro p _
  have h1 := count_le b p
  have h2 := ind_le_one (b p)
  have h3 := ind_nonneg (a p)
  have h4 : ((count b p : ℕ) : ℤ) + ind (b p) ≤ 13 := by omega
  nlinarith

/-! ### The energy of an orbit -/

variable (c : Config)

/-- x_p(t) as 0/1. -/
def xs (t : ℕ) (p : Pt) : ℤ := ind (run c t p)

/-- h_p(t) = n_p(t) + x_p(t). -/
def hs (t : ℕ) (p : Pt) : ℤ := (count (run c t) p : ℤ) + xs c t p

/-- F t = 2 E(t + 1) = -2 x(t+1)ᵀ (A + I) x(t) + 7 (|x(t+1)| + |x(t)|). -/
def F (t : ℕ) : ℤ := -2 * pair V (run c (t + 1)) (run c t) + 7 * (pop V (run c (t + 1)) + pop V (run c t))

/-- Live points of the orbit are cells, if the seed's are. -/
theorem run_isCell (hc : ∀ p, c p = true → p.isCell = true) : ∀ t p, run c t p = true → p.isCell = true
  | 0, p, h => hc p h
  | t + 1, p, h => by
    simp only [run, step, Bool.and_eq_true] at h
    exact h.1

variable {V c}

/-- **(★)** The energy step, exactly. -/
theorem energy_step (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V)
    (t : ℕ) :
    F V c (t + 1) - F V c t = -∑ p ∈ V, (xs c (t + 2) p - xs c t p) * (2 * hs c (t + 1) p - 7) := by
  have hcell := run_isCell c hc
  have hsym := pair_comm V (run c (t + 1)) (run c t) (fun q h => ⟨hV _ q h, hcell _ q h⟩)
    (fun q h => ⟨hV _ q h, hcell _ q h⟩)
  unfold F
  rw [hsym]
  simp only [pair, pop, xs, hs, Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib,
    ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro p _
  ring

/-- The drive: O1 events at t + 1 (overcrowded, n ≥ 6, and live two generations earlier), each
contributing 2h - 7 ≥ 5. -/
def drive (V : Finset Pt) (c : Config) (t : ℕ) : ℤ :=
  ∑ p ∈ V, if 6 ≤ count (run c (t + 1)) p ∧ run c t p = true then 2 * hs c (t + 1) p - 7 else 0

/-- The dissipation: mismatches x(t+2) ≠ x(t) at points that are not overcrowded, each contributing
|2h - 7| ≥ 1. -/
def diss (V : Finset Pt) (c : Config) (t : ℕ) : ℤ :=
  ∑ p ∈ V, if count (run c (t + 1)) p ≤ 5 ∧ run c (t + 2) p ≠ run c t p then |2 * hs c (t + 1) p - 7| else 0

/-- The per-cell identity behind ΔE = D - Q: gump agrees with the uncapped threshold rule "alive iff
h ≥ 4" except at overcrowded cells, where it says dead. -/
theorem cell_identity (hc : ∀ p, c p = true → p.isCell = true) (t : ℕ) (p : Pt) :
    -((xs c (t + 2) p - xs c t p) * (2 * hs c (t + 1) p - 7)) =
      (if 6 ≤ count (run c (t + 1)) p ∧ run c t p = true then 2 * hs c (t + 1) p - 7 else 0) -
      (if count (run c (t + 1)) p ≤ 5 ∧ run c (t + 2) p ≠ run c t p then |2 * hs c (t + 1) p - 7| else 0) := by
  have h2 : run c (t + 2) p = (p.isCell && rule (run c (t + 1) p) (count (run c (t + 1)) p)) := rfl
  simp only [xs, hs]
  rw [h2]
  generalize hn : count (run c (t + 1)) p = n
  cases hcell : p.isCell
  · have h0 : run c t p = false := by
      cases h : run c t p with
      | false => rfl
      | true => rw [run_isCell c hc t p h] at hcell; contradiction
    simp [h0, ind]
  · have hi0 := ind_nonneg (run c (t + 1) p)
    have hi1 := ind_le_one (run c (t + 1) p)
    by_cases hlo : n ≤ 2
    · have hneg : 2 * ((n : ℤ) + ind (run c (t + 1) p)) - 7 < 0 := by omega
      rw [abs_of_neg hneg]
      have hr : ∀ b, rule b n = false := by intro b; cases b <;> simp [rule] <;> omega
      cases h1 : run c (t + 1) p <;> cases h0 : run c t p <;> simp [hr, ind, h0, h1] <;> omega
    · by_cases hhi : 6 ≤ n
      · have hr : ∀ b, rule b n = false := by intro b; cases b <;> simp [rule] <;> omega
        cases h1 : run c (t + 1) p <;> cases h0 : run c t p <;>
          simp [hr, ind, h0, h1, hhi, show ¬ n ≤ 5 by omega] <;> ring
      · have : n = 3 ∨ n = 4 ∨ n = 5 := by omega
        rcases this with rfl | rfl | rfl <;>
          cases h1 : run c (t + 1) p <;> cases h0 : run c t p <;> simp [rule, ind, h0, h1] <;> norm_num

/-- **ΔE = D - Q, exactly** (doubled: F = 2E). -/
theorem energy_identity (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V)
    (t : ℕ) : F V c (t + 1) - F V c t = drive V c t - diss V c t := by
  rw [energy_step hc hV t, ← Finset.sum_neg_distrib, drive, diss, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl (fun p _ => cell_identity hc t p)

theorem drive_nonneg (t : ℕ) : 0 ≤ drive V c t := by
  apply Finset.sum_nonneg
  intro p _
  split
  · rename_i h
    have := ind_nonneg (run c (t + 1) p)
    simp only [hs, xs]
    omega
  · exact le_refl _

theorem diss_nonneg (t : ℕ) : 0 ≤ diss V c t := by
  apply Finset.sum_nonneg
  intro p _
  split
  · exact abs_nonneg _
  · exact le_refl _

/-- With no O1 event at t + 1, the drive is zero. -/
theorem drive_eq_zero (t : ℕ) (hO : ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) :
    drive V c t = 0 := by
  apply Finset.sum_eq_zero
  intro p _
  rw [if_neg]
  rintro ⟨h6, ht⟩
  rw [hO p h6] at ht
  contradiction

/-- With no O1 event at t + 1, a mismatch in the vessel dissipates at least 1 (in units of 2E). -/
theorem one_le_diss (t : ℕ) (hO : ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) (p : Pt)
    (hp : p ∈ V) (hm : run c (t + 2) p ≠ run c t p) : 1 ≤ diss V c t := by
  have h5 : count (run c (t + 1)) p ≤ 5 := by
    apply Classical.byContradiction
    intro h6
    have h0 := hO p (by omega)
    have h2 : run c (t + 2) p = false := by
      show (p.isCell && rule (run c (t + 1) p) (count (run c (t + 1)) p)) = false
      cases run c (t + 1) p <;> simp [rule] <;> omega
    rw [h0, h2] at hm
    exact hm rfl
  have hterm : (1 : ℤ) ≤ if count (run c (t + 1)) p ≤ 5 ∧ run c (t + 2) p ≠ run c t p then
      |2 * hs c (t + 1) p - 7| else 0 := by
    rw [if_pos ⟨h5, hm⟩]
    apply Int.one_le_abs
    simp only [hs]
    omega
  refine le_trans hterm ?_
  apply Finset.single_le_sum (f := fun p => if count (run c (t + 1)) p ≤ 5 ∧ run c (t + 2) p ≠ run c t p then
      |2 * hs c (t + 1) p - 7| else 0) _ hp
  intro q _
  split
  · exact abs_nonneg _
  · exact le_refl _

/-- **Bounds on the energy**: -12 |V| ≤ 2E ≤ 14 |V|. -/
theorem energy_bounds (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V)
    (t : ℕ) : -12 * (V.card : ℤ) ≤ F V c t ∧ F V c t ≤ 14 * V.card := by
  have hcell := run_isCell c hc
  have hsym := pair_comm V (run c (t + 1)) (run c t) (fun q h => ⟨hV _ q h, hcell _ q h⟩)
    (fun q h => ⟨hV _ q h, hcell _ q h⟩)
  have h1 := pair_le V (run c (t + 1)) (run c t)
  have h2 := pair_le V (run c t) (run c (t + 1))
  have h3 := pair_nonneg V (run c (t + 1)) (run c t)
  have h4 := pop_le V (run c (t + 1)); have h5 := pop_le V (run c t)
  have h6 := pop_nonneg V (run c (t + 1)); have h7 := pop_nonneg V (run c t)
  unfold F
  constructor <;> linarith

/-- **T5 (a) for gump.** If from generation T on no cell is overcrowded (n ≥ 6) at t + 1 while live at
t (no O1 event), the orbit has period at most 2 from some generation t₀ ≤ T + 26 |V| on. -/
theorem period_two_of_no_O1 (hc : ∀ p, c p = true → p.isCell = true)
    (hV : ∀ t p, run c t p = true → p ∈ V) (T : ℕ)
    (hO : ∀ t, T ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) :
    ∃ t₀, T ≤ t₀ ∧ t₀ ≤ T + 26 * V.card ∧ ∀ t, t₀ ≤ t → run c (t + 2) = run c t := by
  have key : ∃ t₀, T ≤ t₀ ∧ t₀ ≤ T + 26 * V.card ∧ run c (t₀ + 2) = run c t₀ := by
    apply Classical.byContradiction
    intro hne
    have hdrop : ∀ t, T ≤ t → t ≤ T + 26 * V.card → F V c (t + 1) ≤ F V c t - 1 := by
      intro t h1 h2
      have hneq : run c (t + 2) ≠ run c t := fun h => hne ⟨t, h1, h2, h⟩
      obtain ⟨p, hp⟩ : ∃ p, run c (t + 2) p ≠ run c t p := by
        apply Classical.byContradiction
        intro hall
        apply hneq
        funext p
        apply Classical.byContradiction
        intro hp
        exact hall ⟨p, hp⟩
      have hpV : p ∈ V := by
        cases h2p : run c (t + 2) p
        · rw [h2p] at hp
          exact hV t p (by cases h0 : run c t p <;> simp_all)
        · exact hV (t + 2) p h2p
      have := energy_identity hc hV t
      have hd := drive_eq_zero (V := V) t (hO t h1)
      have hq := one_le_diss (V := V) t (hO t h1) p hpV hp
      linarith
    have hind : ∀ k, k ≤ 26 * V.card + 1 → F V c (T + k) ≤ F V c T - k := by
      intro k
      induction k with
      | zero => intro _; simp
      | succ k ih =>
        intro hk
        have := hdrop (T + k) (by omega) (by omega)
        have := ih (by omega)
        rw [← Nat.add_assoc]
        push_cast
        linarith
    have hfin := hind (26 * V.card + 1) le_rfl
    have hb1 := (energy_bounds hc hV (T + (26 * V.card + 1))).1
    have hb2 := (energy_bounds hc hV T).2
    push_cast at hfin
    linarith
  obtain ⟨t₀, h1, h2, h3⟩ := key
  refine ⟨t₀, h1, h2, fun t ht => ?_⟩
  obtain ⟨m, rfl⟩ : ∃ m, t = t₀ + m := ⟨t - t₀, by omega⟩
  rw [show t₀ + m + 2 = (t₀ + 2) + m by omega, run_add, h3, ← run_add]

/-- **T5 (b′) for gump.** An orbit that is periodic from μ on, with no O1 event from μ on, has period at
most 2 from μ on. So every oscillator of period ≥ 3 has an O1 event in its cycle. -/
theorem oscillator_period_two (hc : ∀ p, c p = true → p.isCell = true)
    (hV : ∀ t p, run c t p = true → p ∈ V) (μ P : ℕ) (hP : 0 < P)
    (hper : ∀ t, μ ≤ t → run c (t + P) = run c t)
    (hO : ∀ t, μ ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) :
    ∀ t, μ ≤ t → run c (t + 2) = run c t := by
  obtain ⟨t₀, _, _, h⟩ := period_two_of_no_O1 hc hV μ hO
  have iter : ∀ k t, μ ≤ t → run c (t + k * P) = run c t := by
    intro k
    induction k with
    | zero => intro t _; simp
    | succ k ih =>
      intro t ht
      rw [show t + (k + 1) * P = (t + k * P) + P by ring, hper _ (by omega), ih t ht]
  intro t ht
  have hle : t₀ ≤ t + t₀ * P := by
    have : t₀ ≤ t₀ * P := Nat.le_mul_of_pos_right t₀ hP
    omega
  rw [← iter t₀ (t + 2) (by omega), show t + 2 + t₀ * P = (t + t₀ * P) + 2 by omega, h _ hle, iter t₀ t ht]

/-- **T5 for a finite seed, in its diagonal hull.** For a seed on cells inside the region d·p ≤ C d (all
eight diagonals), with no O1 event from T on, the orbit has period ≤ 2 from some t₀ ≤ T + 26 N on,
N the number of cells of the hull. -/
theorem hull_period_two_of_no_O1 (c : Config) (hc : ∀ p, c p = true → p.isCell = true) (C : Diag → Int)
    (h : ∀ p, c p = true → ∀ d, d.dot p ≤ C d) (T : ℕ)
    (hO : ∀ t, T ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) :
    ∃ t₀, T ≤ t₀ ∧ t₀ ≤ T + 26 * (hullCells C).toFinset.card ∧ ∀ t, t₀ ≤ t → run c (t + 2) = run c t := by
  apply period_two_of_no_O1 hc _ T hO
  intro t p hp
  rw [List.mem_toFinset, mem_hullCells]
  exact ⟨run_isCell c hc t p hp, hull C c h t p hp⟩

/-! ### The budget over a window (threshold.md section 3) -/

/-- The number of O1 events at t + 1 in the vessel. -/
def o1 (V : Finset Pt) (c : Config) (t : ℕ) : ℕ :=
  (V.filter fun p => 6 ≤ count (run c (t + 1)) p ∧ run c t p = true).card

/-- The number of mismatches x(t + 2) ≠ x(t) in the vessel. -/
def mism (V : Finset Pt) (c : Config) (t : ℕ) : ℕ := (V.filter fun p => run c (t + 2) p ≠ run c t p).card

theorem drive_le (t : ℕ) : drive V c t ≤ 19 * (o1 V c t : ℤ) := by
  unfold drive o1
  rw [Finset.card_filter]
  push_cast
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro p _
  split
  · have := count_le (run c (t + 1)) p
    have := ind_le_one (run c (t + 1) p)
    simp only [hs, xs]
    omega
  · simp

theorem mism_le (hc : ∀ p, c p = true → p.isCell = true) (t : ℕ) :
    (mism V c t : ℤ) ≤ diss V c t + o1 V c t := by
  unfold mism diss o1
  rw [Finset.card_filter, Finset.card_filter]
  push_cast
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro p _
  have hd0 : (0 : ℤ) ≤ if count (run c (t + 1)) p ≤ 5 ∧ run c (t + 2) p ≠ run c t p then
      |2 * hs c (t + 1) p - 7| else 0 := by split <;> simp
  have ho0 : (0 : ℤ) ≤ if 6 ≤ count (run c (t + 1)) p ∧ run c t p = true then 1 else 0 := by split <;> simp
  by_cases hm : run c (t + 2) p ≠ run c t p
  · rw [if_pos hm]
    by_cases h5 : count (run c (t + 1)) p ≤ 5
    · rw [if_pos ⟨h5, hm⟩]
      have : 1 ≤ |2 * hs c (t + 1) p - 7| := Int.one_le_abs (by simp only [hs]; omega)
      linarith
    · have h2 : run c (t + 2) p = false := by
        show (p.isCell && rule (run c (t + 1) p) (count (run c (t + 1)) p)) = false
        cases run c (t + 1) p <;> simp [rule] <;> omega
      have h0 : run c t p = true := by
        cases h : run c t p
        · rw [h2, h] at hm; exact absurd rfl hm
        · rfl
      rw [if_neg (fun h => h5 h.1),
        if_pos (⟨by omega, h0⟩ : 6 ≤ count (run c (t + 1)) p ∧ run c t p = true)]
      simp
  · rw [if_neg hm]
    linarith

/-- **The budget (threshold.md section 3).** Over any window of K generations from T, the number of
mismatches x(t + 2) ≠ x(t) is at most 20 times the number of O1 events plus 26 |V|: sustained activity
beyond period 2 needs overcrowding of cells that were live two generations earlier, at a rate of at
least one event per 20 mismatches. -/
theorem budget (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V)
    (T K : ℕ) :
    (∑ t ∈ Finset.range K, (mism V c (T + t) : ℤ)) ≤
      20 * ∑ t ∈ Finset.range K, (o1 V c (T + t) : ℤ) + 26 * V.card := by
  have hdiss : ∀ K, ∑ t ∈ Finset.range K, diss V c (T + t) =
      ∑ t ∈ Finset.range K, drive V c (T + t) - (F V c (T + K) - F V c T) := by
    intro K
    induction K with
    | zero => simp
    | succ K ih =>
      rw [Finset.sum_range_succ, Finset.sum_range_succ, ih]
      have := energy_identity hc hV (T + K)
      rw [show T + (K + 1) = T + K + 1 by omega]
      linarith
  have h1 : ∑ t ∈ Finset.range K, drive V c (T + t) ≤ 19 * ∑ t ∈ Finset.range K, (o1 V c (T + t) : ℤ) := by
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum (fun t _ => drive_le _)
  have h2 : ∑ t ∈ Finset.range K, (mism V c (T + t) : ℤ) ≤
      ∑ t ∈ Finset.range K, diss V c (T + t) + ∑ t ∈ Finset.range K, (o1 V c (T + t) : ℤ) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_le_sum (fun t _ => mism_le hc _)
  have hb1 := (energy_bounds hc hV (T + K)).1
  have hb2 := (energy_bounds hc hV T).2
  have := hdiss K
  linarith

end Gump.Threshold
