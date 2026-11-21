/-
The speed limit of `docs/AUTOMATON.md` section 3: information moves at most 2 doubled units per
generation in max-norm (one cube per generation).

Stated as a light cone: the state at p after n generations is determined by the initial state on the
max-norm ball of radius 2n about p. The bound is attained in one generation (`speed_two_attained`).
-/
import Gump.Basic

namespace Gump

/-- q lies within max-norm distance r of p (doubled units). -/
def Near (r : Nat) (p q : Pt) : Prop :=
  (q.x - p.x).natAbs ≤ r ∧ (q.y - p.y).natAbs ≤ r ∧ (q.z - p.z).natAbs ≤ r

theorem offsets_small : ∀ a : Axis, ∀ o ∈ offsets a, o.x.natAbs ≤ 2 ∧ o.y.natAbs ≤ 2 ∧ o.z.natAbs ≤ 2 := by
  intro a; cases a <;> decide

/-- Every neighbour is within max-norm distance 2. -/
theorem nbrs_near (p : Pt) : ∀ q ∈ nbrs p, Near 2 p q := by
  intro q hq
  simp only [nbrs, List.mem_map] at hq
  obtain ⟨o, ho, rfl⟩ := hq
  have := offsets_small _ o ho
  simp only [Near, Pt.add_x, Pt.add_y, Pt.add_z]
  omega

/-- One generation at p reads only the configuration within max-norm distance 2 of p. -/
theorem step_local {c c' : Config} {p : Pt} (h : ∀ q, Near 2 p q → c q = c' q) :
    step c p = step c' p := by
  have hc : count c p = count c' p := by
    unfold count
    apply List.countP_congr
    intro q hq
    rw [h q (nbrs_near p q hq)]
  have hp : c p = c' p := h p (by simp [Near])
  simp [step, hc, hp]

/-- **Speed limit (light cone).** If two configurations agree within max-norm distance r + 2n of p, then
after n generations they agree within distance r of p. With r = 0: the state at p after n generations
is a function of the initial state on the ball of radius 2n about p. -/
theorem light_cone {c c' : Config} {p : Pt} :
    ∀ n r, (∀ q, Near (r + 2 * n) p q → c q = c' q) → ∀ q, Near r p q → run c n q = run c' n q
  | 0, r, h => fun q hq => h q (by simpa using hq)
  | n + 1, r, h => by
    intro q hq
    apply step_local
    intro q' hq'
    refine light_cone (p := p) n (r + 2) (fun q'' hq'' => h q'' ?_) q' ?_
    · have e : r + 2 + 2 * n = r + 2 * (n + 1) := by omega
      rw [e] at hq''
      exact hq''
    · unfold Near at *
      omega

/-- The empty configuration stays empty. -/
theorem run_empty : ∀ n, run (fun _ => false) n = fun _ => false
  | 0 => rfl
  | n + 1 => by
    funext p
    rw [run, run_empty n]
    simp [step, rule, count]

/-- **Nothing comes from further than 2n.** If a configuration is dead on the max-norm ball of radius 2n
about p, then p is dead after n generations. Equivalently, a point live at generation n lies within
max-norm distance 2n of a point live at generation 0. -/
theorem dead_ball {c : Config} {p : Pt} (n : Nat) (h : ∀ q, Near (2 * n) p q → c q = false) :
    run c n p = false := by
  have := light_cone (c := c) (c' := fun _ => false) (p := p) n 0
    (fun q hq => by rw [h q (by simpa using hq)]) p (by simp [Near])
  rw [this, run_empty]

/-- The support moves at most 2n in n generations. -/
theorem live_near_seed {c : Config} {p : Pt} (n : Nat) (h : run c n p = true) :
    ∃ q, Near (2 * n) p q ∧ c q = true := by
  apply Classical.byContradiction
  intro hne
  have := dead_ball (c := c) (p := p) n (fun q hq => by
    cases hcq : c q with
    | false => rfl
    | true => exact absurd ⟨q, hq, hcq⟩ hne)
  rw [this] at h
  contradiction

/-- **The bound 2 is attained in one generation.** The cell (1, 0, 0) is born when its four coplanar
corner neighbours (1, ±2, ±2) are alive, and not when (1, 2, 2), at max-norm distance 2, is removed. -/
theorem speed_two_attained :
    step (fun q => decide (q ∈ [⟨1, 2, 2⟩, ⟨1, 2, -2⟩, ⟨1, -2, 2⟩, ⟨1, -2, -2⟩])) ⟨1, 0, 0⟩ = true ∧
    step (fun q => decide (q ∈ [⟨1, 2, -2⟩, ⟨1, -2, 2⟩, ⟨1, -2, -2⟩])) ⟨1, 0, 0⟩ = false := by
  decide

end Gump
