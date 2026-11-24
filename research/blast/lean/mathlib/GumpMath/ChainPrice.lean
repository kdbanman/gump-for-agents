/-
The price per cell (line 6 of `research/blast/lean/README.md`'s climb; target 4 of the chain brief):
what turns finite exact or certified lifetimes into a proved interval for lim log τ / A.

For a family of faces G_n built from n copies of one block (a tube or strip lengthened one unit at a time,
a torus of n periods), put a n = log τ(G_n).  Gluing inequalities with defects,
  (SUB)   a (m + n) ≤ a m + a n + C        (joining two pieces costs at most C in log τ),
  (SUPER) a (m + n) ≥ a m + a n - C'       (each piece reseeds the other: the lower bound B2 in another form),
give, by Fekete's lemma (Mathlib's `Subadditive.tendsto_lim`, applied to a + C and to C' - a):
  `price_exists_of_sub`    (SUB) alone and a ≥ 0: the price p = lim a n / n exists, and p ≤ (a n + C)/n
                           for every n ≥ 1;
  `price_exists_of_super`  (SUPER) alone and a n ≤ M n (Theorem 1 gives M = ε_max · block size):
                           the price exists and p ≥ (a n - C')/n for every n ≥ 1;
  `price_interval`         both: p ∈ [(a n - C')/n, (a n + C)/n] for every n ≥ 1, so one exactly solved
                           or certified face pins the price to within (C + C')/n.
Neither gluing inequality is proved for the surrogate (see `notes/chain.md`).
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace Gump.Chain.Price
open Filter Topology

theorem bddBelow_div (u : ℕ → ℝ) (c : ℝ) (h : ∀ n, n ≠ 0 → c ≤ u n / n) :
    BddBelow (Set.range fun n => u n / n) := by
  refine ⟨min c 0, ?_⟩
  rintro _ ⟨n, rfl⟩
  rcases eq_or_ne n 0 with hn | hn
  · subst hn; simp
  · exact (min_le_left _ _).trans (h n hn)

/-- **The price exists under (SUB)**, and every finite face bounds it above. -/
theorem price_exists_of_sub (a : ℕ → ℝ) (C : ℝ) (ha : ∀ n, 0 ≤ a n)
    (hsub : ∀ m n, a (m + n) ≤ a m + a n + C) :
    ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧ ∀ n, n ≠ 0 → p ≤ (a n + C) / n := by
  set u : ℕ → ℝ := fun n => a n + C
  have hu : Subadditive u := fun m n => by simp only [u]; linarith [hsub m n]
  have hb : BddBelow (Set.range fun n => u n / n) :=
    bddBelow_div u (-|C|) (fun n hn => by
      have hn' : (1 : ℝ) ≤ n := by exact_mod_cast Nat.one_le_iff_ne_zero.2 hn
      rw [le_div_iff₀ (by linarith)]
      simp only [u]
      have := ha n
      have : -|C| * n ≤ -|C| := by nlinarith [abs_nonneg C]
      linarith [neg_abs_le C])
  refine ⟨hu.lim, ?_, fun n hn => hu.lim_le_div hb hn⟩
  have h1 := hu.tendsto_lim hb
  have h2 : Tendsto (fun n : ℕ => C / (n : ℝ)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
  have h3 := h1.sub h2
  simp only [sub_zero] at h3
  refine h3.congr' ?_
  filter_upwards [eventually_ne_atTop 0] with n hn
  simp only [u]
  have : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.2 hn
  field_simp
  ring

/-- **The price exists under (SUPER)** with a linear upper bound, and every finite face bounds it below. -/
theorem price_exists_of_super (a : ℕ → ℝ) (C' M : ℝ) (hM : ∀ n, n ≠ 0 → a n ≤ M * n)
    (hsup : ∀ m n, a m + a n - C' ≤ a (m + n)) :
    ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧ ∀ n, n ≠ 0 → (a n - C') / n ≤ p := by
  set v : ℕ → ℝ := fun n => C' - a n
  have hv : Subadditive v := fun m n => by simp only [v]; linarith [hsup m n]
  have hb : BddBelow (Set.range fun n => v n / n) :=
    bddBelow_div v (-|C'| - M) (fun n hn => by
      have hn' : (1 : ℝ) ≤ n := by exact_mod_cast Nat.one_le_iff_ne_zero.2 hn
      rw [le_div_iff₀ (by linarith)]
      simp only [v]
      have := hM n hn
      have : -|C'| * n ≤ -|C'| := by nlinarith [abs_nonneg C']
      have : -|C'| ≤ C' := neg_abs_le C'
      nlinarith)
  refine ⟨-hv.lim, ?_, fun n hn => ?_⟩
  · have h1 := hv.tendsto_lim hb
    have h2 : Tendsto (fun n : ℕ => C' / (n : ℝ)) atTop (𝓝 0) :=
      tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
    have h3 := h2.sub h1
    simp only [zero_sub] at h3
    refine h3.congr' ?_
    filter_upwards [eventually_ne_atTop 0] with n hn
    simp only [v]
    have : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.2 hn
    field_simp
    ring
  · have := hv.lim_le_div hb hn
    simp only [v] at this
    have hn0 : (0 : ℝ) < n := by exact_mod_cast Nat.pos_of_ne_zero hn
    have e : (C' - a n) / n = -((a n - C') / n) := by ring
    rw [e] at this
    linarith

/-- **The price interval.**  Under (SUB) and (SUPER), the price exists and lies in
[(a n - C')/n, (a n + C)/n] for every n ≥ 1. -/
theorem price_interval (a : ℕ → ℝ) (C C' : ℝ) (ha : ∀ n, 0 ≤ a n)
    (hsub : ∀ m n, a (m + n) ≤ a m + a n + C) (hsup : ∀ m n, a m + a n - C' ≤ a (m + n)) :
    ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧
      ∀ n, n ≠ 0 → (a n - C') / n ≤ p ∧ p ≤ (a n + C) / n := by
  obtain ⟨p, hp, hle⟩ := price_exists_of_sub a C ha hsub
  have hM : ∀ n, n ≠ 0 → a n ≤ (a 1 + |C|) * n := by
    intro n hn
    induction n, Nat.one_le_iff_ne_zero.2 hn using Nat.le_induction with
    | base => simp
    | succ n hn1 ih =>
      have h1 := hsub n 1
      have h2 := ih (by omega)
      push_cast
      nlinarith [le_abs_self C]
  obtain ⟨p', hp', hge⟩ := price_exists_of_super a C' (a 1 + |C|) hM hsup
  have hpp : p = p' := tendsto_nhds_unique hp hp'
  subst hpp
  exact ⟨p, hp, fun n hn => ⟨hge n hn, hle n hn⟩⟩

end Gump.Chain.Price
