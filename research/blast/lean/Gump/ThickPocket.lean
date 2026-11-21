/-
The reduction of `research/theory/thickness.md` section 4: once a sealed set is dead, the cells outside it fall
into *pockets* (components of the complement) that evolve independently, and a cell whose pocket is finite is
eventually periodic, with transient plus period at most `t₀ + 2^N` (`N` the size of a list holding the pocket).

"No activity crosses between pockets" is `pocket_autonomous`; the periodicity is `pocket_periodic` and its two
readings, in the full lattice (`finite_pocket_periodic`) and in a slab (`slab_finite_pocket_periodic`).

What section 4 says is still missing (that from a random start the pockets are a.s. finite at some fixed time
in one and two layers) is a probabilistic statement and is not attempted here.

Core Lean only: no Mathlib.
-/
import Gump.ThickCore
import Gump.Periodic

namespace Gump

/-- `P` is closed up to `K`: every neighbour of a point of `P` is in `P` or in `K`. -/
def ClosedUpTo (K P : Pt → Bool) : Prop := ∀ p, P p = true → ∀ q ∈ nbrs p, P q = true ∨ K q = true

/-- One generation on `P` depends only on the configuration on `P`, if `K` is dead. -/
theorem pocket_step (K P : Pt → Bool) (hP : ClosedUpTo K P) (c c' : Config) (hc : DeadOn c K)
    (hc' : DeadOn c' K) (hag : ∀ p, P p = true → c p = c' p) : ∀ p, P p = true → step c p = step c' p := by
  intro p hp
  have hcount : count c p = count c' p := by
    unfold count
    apply List.countP_congr
    intro q hq
    rcases hP p hp q hq with h | h
    · rw [hag q h]
    · rw [hc q h, hc' q h]
  simp [step, hag p hp, hcount]

/-- **No activity crosses into a pocket.** If `K` stays dead in two histories and they agree on `P` (closed up
to `K`) at time 0, they agree on `P` forever. -/
theorem pocket_autonomous (K P : Pt → Bool) (hP : ClosedUpTo K P) (c c' : Config)
    (hc : ∀ n, DeadOn (run c n) K) (hc' : ∀ n, DeadOn (run c' n) K)
    (hag : ∀ p, P p = true → c p = c' p) : ∀ n p, P p = true → run c n p = run c' n p
  | 0 => hag
  | n + 1 => pocket_step K P hP (run c n) (run c' n) (hc n) (hc' n) (pocket_autonomous K P hP c c' hc hc' hag n)

/-- **A finite pocket is eventually periodic.** If `K` is dead at every time from `t₀` on and `P` (closed up
to `K`) lies in a list `L`, the history on `P` is eventually periodic, with transient plus period at most
`t₀ + 2^|L|`. -/
theorem pocket_periodic (K P : Pt → Bool) (hP : ClosedUpTo K P) (c : Config) (t₀ : Nat)
    (hK : ∀ n, DeadOn (run c (t₀ + n)) K) (L : List Pt) (hL : ∀ p, P p = true → p ∈ L) :
    ∃ μ T, 0 < T ∧ μ + T ≤ t₀ + 2 ^ L.length ∧
      ∀ n, μ ≤ n → ∀ p, P p = true → run c (n + T) p = run c n p := by
  let f : Nat → List Bool := fun n => L.map (run c (t₀ + n))
  have hf : ∀ n, f n ∈ boolLists L.length := fun n => by
    have := mem_boolLists (f n)
    simpa [f] using this
  obtain ⟨i, j, hij, hj, heq⟩ := pigeonhole f _ hf
  rw [length_boolLists] at hj
  have hagree : ∀ p, P p = true → run c (t₀ + i) p = run c (t₀ + j) p :=
    fun p hp => List.map_inj_left.mp heq p (hL p hp)
  have hlater : ∀ k p, P p = true → run c (t₀ + i + k) p = run c (t₀ + j + k) p := by
    intro k p hp
    rw [run_add c (t₀ + i), run_add c (t₀ + j)]
    refine pocket_autonomous K P hP _ _ ?_ ?_ hagree k p hp
    · intro n; rw [← run_add, Nat.add_assoc]; exact hK (i + n)
    · intro n; rw [← run_add, Nat.add_assoc]; exact hK (j + n)
  refine ⟨t₀ + i, j - i, by omega, by omega, ?_⟩
  intro n hn p hp
  have e1 : n + (j - i) = t₀ + j + (n - (t₀ + i)) := by omega
  have e2 : n = t₀ + i + (n - (t₀ + i)) := by omega
  rw [e1, ← hlater _ p hp, ← e2]

/-- The component of a cell in the cells outside `K` (its pocket) is closed up to `K`. -/
theorem comp_closedUpTo (K : Pt → Bool) (p : Pt) :
    ClosedUpTo K (comp (fun q => q.isCell && !K q) p) := by
  intro q hq r hr
  cases hK : K r with
  | true => right; rfl
  | false =>
    left
    have hqc : q.isCell = true := by
      have := comp_sub _ p q hq
      simp only [Bool.and_eq_true] at this; exact this.1
    have hrc : r.isCell = true := nbrs_isCell q hqc r hr
    exact comp_closed _ p q r hq hr (by simp [hrc, hK])

/-- **Section 4's reduction, full lattice.** Let `K` be sealed and dead at time `t₀`. A cell outside `K` whose
pocket (its component among the cells outside `K`) lies in a list `L` is eventually periodic, with transient
plus period at most `t₀ + 2^|L|`. (With `K = K(t₀)`, the skeleton: if every component of `U(t₀)` is finite,
every cell is eventually periodic.) -/
theorem finite_pocket_periodic (K : Pt → Bool) (hK : Sealed K) (c : Config) (t₀ : Nat)
    (hdead : DeadOn (run c t₀) K) (p : Pt) (hp : p.isCell = true) (hpK : K p = false) (L : List Pt)
    (hL : ∀ q, Reach (fun q => q.isCell && !K q) p q → q ∈ L) :
    ∃ μ T, 0 < T ∧ μ + T ≤ t₀ + 2 ^ L.length ∧ ∀ n, μ ≤ n → run c (n + T) p = run c n p := by
  obtain ⟨μ, T, hT, hb, hper⟩ := pocket_periodic K (comp (fun q => q.isCell && !K q) p)
    (comp_closedUpTo K p) c t₀ (fun n => by rw [run_add]; exact hK.run_dead hdead n) L
    (fun q hq => hL q (comp_eq_true.1 hq))
  exact ⟨μ, T, hT, hb, fun n hn => hper n hn p (comp_eq_true.2 (Reach.refl (by simp [hp, hpK])))⟩

/-- **Section 4's reduction, in a slab.** In the slab `A ≤ d·p ≤ B`, start dead outside the slab, and let `K`
be sealed in the slab and dead at time `t₀`. A cell of the slab outside `K` whose pocket (its component among
the slab's cells outside `K`) lies in a list `L` is eventually periodic, with transient plus period at most
`t₀ + 2^|L|`. -/
theorem slab_finite_pocket_periodic (d : Diag) (A B : Int) (K : Pt → Bool) (hK : SealedIn (slab d A B) K)
    (c : Config) (hout : DeadOn c (fun q => !slab d A B q)) (t₀ : Nat) (hdead : DeadOn (run c t₀) K)
    (p : Pt) (hp : slab d A B p = true) (hpK : K p = false) (L : List Pt)
    (hL : ∀ q, Reach (fun q => slab d A B q && !K q) p q → q ∈ L) :
    ∃ μ T, 0 < T ∧ μ + T ≤ t₀ + 2 ^ L.length ∧ ∀ n, μ ≤ n → run c (n + T) p = run c n p := by
  let Z : Pt → Bool := fun q => K q || !slab d A B q
  let P := comp (fun q => slab d A B q && !K q) p
  have hP : ClosedUpTo Z P := by
    intro q hq r _
    cases hZ : Z r with
    | true => right; rfl
    | false =>
      left
      simp only [Z, Bool.or_eq_false_iff, Bool.not_eq_false'] at hZ
      exact comp_closed _ p q r hq (by assumption) (by simp [hZ.1, hZ.2])
  have hZdead : ∀ n, DeadOn (run c (t₀ + n)) Z := by
    have hout' := run_dead_outside_slab d A B c hout
    have hKdead : ∀ n, DeadOn (run c (t₀ + n)) K := by
      intro n
      induction n with
      | zero => exact hdead
      | succ n ih => exact hK.step_dead (hout' (t₀ + n)) ih
    intro n q hq
    simp only [Z, Bool.or_eq_true, Bool.not_eq_true'] at hq
    rcases hq with h | h
    · exact hKdead n q h
    · exact hout' (t₀ + n) q (by simp [h])
  obtain ⟨μ, T, hT, hb, hper⟩ := pocket_periodic Z P hP c t₀ hZdead L
    (fun q hq => hL q (comp_eq_true.1 hq))
  exact ⟨μ, T, hT, hb, fun n hn => hper n hn p (comp_eq_true.2 (Reach.refl (by simp [hp, hpK])))⟩

end Gump
