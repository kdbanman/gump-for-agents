# Lean statements against their sources

Written by `python3 research/blast/lean/statements.py`; the Lean statements are copied from the files by the
script. A = `docs/AUTOMATON.md` §3; Th = `research/theory/thickness.md` §2. Every theorem here is in `Axioms.lean`
and `check.sh` fails if any rests on more than `propext`, `Classical.choice`, `Quot.sound`.

## Definitions against the oracle

### `mem_offsets_iff` (`Gump/Spec.lean`)

```lean
theorem mem_offsets_iff (a : Axis) (o : Pt) : o ∈ offsets a ↔ (o.get a = 0 ∧ (o.get a.others.1).natAbs = 2 ∧ (o.get a.others.2).natAbs = 2) ∨ ((o.get a).natAbs = 1 ∧ (((o.get a.others.1).natAbs = 1 ∧ o.get a.others.2 = 0) ∨ (o.get a.others.1 = 0 ∧ (o.get a.others.2).natAbs = 1)))
```

- **Meant to be:** A §2 and `reference/oracle.py` `offsets`: the 4 coplanar faces at ±2e_b ± 2e_c and the 8 perpendicular faces at ±e_a ± e_b, ±e_a ± e_c.
- **Difference:** Same.

### `isCell_iff` (`Gump/Spec.lean`)

```lean
theorem isCell_iff (p : Pt) : p.isCell = true ↔ ∃ a : Axis, p.get a % 2 = 1 ∧ p.get a.others.1 % 2 = 0 ∧ p.get a.others.2 % 2 = 0
```

- **Meant to be:** A §1: exactly one odd coordinate; `oracle.py` `masks`.
- **Difference:** Same.

### `rule_iff` (`Gump/Spec.lean`)

```lean
theorem rule_iff (alive : Bool) (n : Nat) : rule alive n = true ↔ (alive = false ∧ (n = 4 ∨ n = 5)) ∨ (alive = true ∧ (n = 3 ∨ n = 4 ∨ n = 5))
```

- **Meant to be:** A §2: a dead cell becomes live iff n ∈ {4,5}; a live cell stays live iff n ∈ {3,4,5}.
- **Difference:** Same.

### `nbrs_isCell` (`Gump/Spec.lean`)

```lean
theorem nbrs_isCell (p : Pt) (h : p.isCell = true) : ∀ q ∈ nbrs p, q.isCell = true
```

- **Meant to be:** (implicit in A §2) neighbours of a face are faces.
- **Difference:** Same.

## T1 to T4 and the hull

### `layer_histogram` (`Gump/Layers.lean`)

```lean
theorem layer_histogram (a : Axis) (d : Diag) : [-4, -2, 0, 2, 4].map (fun v => ((offsets a).map d.dot).count v) = [1, 2, 6, 2, 1]
```

- **Meant to be:** A, T1: for every cell and every d, its 12 neighbours are distributed over layers as Δs = −4: 1, −2: 2, 0: 6, +2: 2, +4: 1.
- **Difference:** Same (a statement about the offsets, for each orientation and diagonal).

### `Sealed.run_dead` (`Gump/Sealed.lean`)

```lean
theorem Sealed.run_dead {S : Pt → Bool} (hS : Sealed S) {c : Config} (hc : DeadOn c S) : ∀ n, DeadOn (run c n) S
```

- **Meant to be:** A, T6: a dead sealed set stays dead whatever happens elsewhere.
- **Difference:** Same. `Sealed` is defined on all points of Z³, cells or not.

### `Sealed.union` (`Gump/Sealed.lean`)

```lean
theorem Sealed.union {S T : Pt → Bool} (hS : Sealed S) (hT : Sealed T) : Sealed (fun p => S p || T p)
```

- **Meant to be:** A, T6: unions of sealed sets are sealed.
- **Difference:** Same, for two sets.

### `confinement` (`Gump/Sealed.lean`)

```lean
theorem confinement (d : Diag) (C : Int) (c : Config) (h : ∀ p, C < d.dot p → c p = false) : ∀ n p, C < d.dot p → run c n p = false
```

- **Meant to be:** A, T2: if every cell with s > C is dead, that stays true forever.
- **Difference:** Stronger: C is any integer, not only a lattice level.

### `hull` (`Gump/Sealed.lean`)

```lean
theorem hull (C : Diag → Int) (c : Config) (h : ∀ p, c p = true → ∀ d, d.dot p ≤ C d) : ∀ n p, run c n p = true → ∀ d, d.dot p ≤ C d
```

- **Meant to be:** A, T2: any finite pattern stays forever inside its diagonal hull, and the hull can only shrink.
- **Difference:** Stated for any intersection of half-spaces d·p ≤ C d that contains the pattern; finiteness is not needed.

### `firewall` (`Gump/Sealed.lean`)

```lean
theorem firewall (d : Diag) (C : Int) (c : Config) (h : ∀ p, C < d.dot p → d.dot p ≤ C + 6 → c p = false) : ∀ n p, C < d.dot p → d.dot p ≤ C + 6 → run c n p = false
```

- **Meant to be:** A, T3: if three consecutive layers C+2, C+4, C+6 are all dead, they stay dead forever.
- **Difference:** Stronger in the band (C < s ≤ C + 6 for any integer C); it holds for every configuration of the lattice, infinite ones included. The source adds "applies to toroidal patterns too": that is not stated as a theorem; it follows for even H from this row applied to the periodic lift (`Torus.lift_trun`).

### `firewall_separates` (`Gump/Sealed.lean`)

```lean
theorem firewall_separates (d : Diag) (C : Int) (c c' : Config) (hc : DeadOn c (band d C)) (hc' : DeadOn c' (band d C)) (hag : ∀ p, d.dot p ≤ C → c p = c' p) : ∀ n p, d.dot p ≤ C → run c n p = run c' n p
```

- **Meant to be:** A, T3: the two sides never influence each other again.
- **Difference:** Stated for the side below the band; the other side is the same theorem for the opposite diagonal.

### `slab_closed` (`Gump/Sealed.lean`)

```lean
theorem slab_closed (d : Diag) (A B : Int) (c : Config) (h : ∀ p, c p = true → A ≤ d.dot p ∧ d.dot p ≤ B) : ∀ n p, run c n p = true → A ≤ d.dot p ∧ d.dot p ≤ B
```

- **Meant to be:** A, T4: a pattern contained in m consecutive layers stays in those layers.
- **Difference:** Same, for any integers A ≤ s ≤ B.

## The bridge: the stepper, symmetries, finite seeds

### `nbrs_symm` (`Gump/Symm.lean`)

```lean
theorem nbrs_symm {p q : Pt} (hp : p.isCell = true) (hq : q.isCell = true) : q ∈ nbrs p ↔ p ∈ nbrs q
```

- **Meant to be:** (used by T5 and by the stepper) the neighbourhood is symmetric.
- **Difference:** For cells; `nbrs_not_symm_off_cells` shows the hypothesis is needed.

### `stepFin_config` (`Gump/FiniteCorrect.lean`)

```lean
theorem stepFin_config (live : Pattern) : (stepFin live).config = step live.config
```

- **Meant to be:** (the tie to the running automaton) the executable stepper misses no birth.
- **Difference:** Equal to `step` as functions, with no hypothesis on the pattern.

### `runFin_config` (`Gump/FiniteCorrect.lean`)

```lean
theorem runFin_config (live : Pattern) : ∀ n, (runFin live n).config = run live.config n
```

- **Meant to be:** the same for n generations.
- **Difference:** Same.

### `symmetry_preserved` (`Gump/Equivariance.lean`)

```lean
theorem symmetry_preserved (g : Sym) {v : Pt} (hv : v.even) (c : Config) (h : ∀ p, c (g.act v p) = c p) : ∀ n p, run c n (g.act v p) = run c n p
```

- **Meant to be:** A §2: the dynamics is invariant under translations by cube steps × O_h; a seed's symmetry is preserved forever.
- **Difference:** Every one of the 48 × even translations commutes with the dynamics. That these are all the symmetries of the lattice is not proved.

### `finite_eventually_periodic` (`Gump/Periodic.lean`)

```lean
theorem finite_eventually_periodic (c : Config) (L : List Pt) (hL : ∀ p, c p = true → p ∈ L) : ∃ μ T, 0 < T ∧ ∀ n, μ ≤ n → run c (n + T) = run c n
```

- **Meant to be:** A, T2 consequences: every finite seed is eventually periodic.
- **Difference:** Same; `eventually_periodic` adds the bound μ + T ≤ 2^N + 1 with N the number of hull cells.

### `no_spaceship` (`Gump/Periodic.lean`)

```lean
theorem no_spaceship (c : Config) (L : List Pt) (hL : ∀ p, c p = true → p ∈ L) (hne : ∃ p, c p = true) (T : Nat) (v : Pt) (h : ∀ p, c p = true → run c T (p + v) = true) : v = ⟨0, 0, 0⟩
```

- **Meant to be:** A, T2 consequences: no spaceships.
- **Difference:** Stronger: a later generation need only contain a translate of the seed.

### `light_cone` (`Gump/Speed.lean`)

```lean
theorem light_cone {c c' : Config} {p : Pt} : ∀ n r, (∀ q, Near (r + 2 * n) p q → c q = c' q) → ∀ q, Near r p q → run c n q = run c' n q
```

- **Meant to be:** A, speed limit: information moves at most 2 doubled units per generation in max-norm.
- **Difference:** Same; `speed_two_attained` shows the bound is reached in one generation. Tightness beyond one generation is not proved.

### `axis_halfspace_not_confining` (`Gump/Sharpness.lean`)

```lean
theorem axis_halfspace_not_confining : ¬ ∀ c : Config, (∀ p : Pt, 0 < p.x → c p = false) → ∀ p : Pt, 0 < p.x → step c p = false
```

- **Meant to be:** A, T2: axis-aligned half-spaces do not confine.
- **Difference:** One half-space (x > 0), with a witness.

### `two_layers_not_firewall` (`Gump/Sharpness.lean`)

```lean
theorem two_layers_not_firewall : ¬ ∀ c : Config, (∀ p : Pt, -1 < (⟨true, true, true⟩ : Diag).dot p → (⟨true, true, true⟩ : Diag).dot p ≤ 3 → c p = false) → ∀ p : Pt, -1 < (⟨true, true, true⟩ : Diag).dot p → (⟨true, true, true⟩ : Diag).dot p ≤ 3 → step c p = false
```

- **Meant to be:** A, T3: two dead layers are not enough.
- **Difference:** One diagonal and one level, with a four-cell witness.

### `cube_still` (`Gump/Certify.lean`)

```lean
theorem cube_still : run (lcfg [⟨1, 0, 0⟩, ⟨-1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨0, -1, 0⟩, ⟨0, 0, 1⟩, ⟨0, 0, -1⟩]) 1 = lcfg [⟨1, 0, 0⟩, ⟨-1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨0, -1, 0⟩, ⟨0, 0, 1⟩, ⟨0, 0, -1⟩]
```

- **Meant to be:** A: the 6 faces of a single cube are a still life.
- **Difference:** "Smallest" is not proved.

### `lift_tstep` (`Gump/Torus.lean`)

```lean
theorem lift_tstep (H : Nat) (hH : 0 < H) (heven : H % 2 = 0) (h : TState) : lift H (tstep H h) = step (lift H h)
```

- **Meant to be:** A §4: for even H the array-index torus is a proper torus.
- **Difference:** The oracle's torus step, transcribed, equals `step` on the periodic lift. Even H only; the odd-H seam is not modelled.

### `oscCert_spec` (`Gump/Bits.lean`)

```lean
theorem oscCert_spec (L : List Pt) (P : Nat) (h : oscCert L P = true) : 0 < P ∧ run (lcfg L) P = lcfg L ∧ ∀ k, 0 < k → k < P → run (lcfg L) k ≠ lcfg L
```

- **Meant to be:** (census) a cell list is an oscillator of exactly period P.
- **Difference:** A certificate the kernel evaluates; used for line-C and for the 1,307 catalogue objects.

## T5: the threshold lemma (Mathlib package)

### `energy_identity` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem energy_identity (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (t : ℕ) : F V c (t + 1) - F V c t = drive V c t - diss V c t
```

- **Meant to be:** A, T5: for gump ΔE = D − Q exactly.
- **Difference:** F = 2E, so drive and dissipation are doubled. The vessel is a finite set holding every live point of a run on the infinite lattice; tori are not covered.

### `energy_bounds` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem energy_bounds (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (t : ℕ) : -12 * (V.card : ℤ) ≤ F V c t ∧ F V c t ≤ 14 * V.card
```

- **Meant to be:** `research/theory/threshold.md`: −6N ≤ E ≤ 7N.
- **Difference:** Doubled. Says less than the source in one respect, like every T5 row here: the vessel is a finite set holding the run on the infinite lattice (a hull, or any region dead outside for ever); A, T5 also covers tori, which are not formalised.

### `period_two_of_no_O1` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem period_two_of_no_O1 (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (T : ℕ) (hO : ∀ t, T ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) : ∃ t₀, T ≤ t₀ ∧ t₀ ≤ T + 26 * V.card ∧ ∀ t, t₀ ≤ t → run c (t + 2) = run c t
```

- **Meant to be:** A, T5: an orbit with no such events from some time on has period ≤ 2 (reached within 26N + 1 further steps).
- **Difference:** The bound is 26N. "No such events" is the source's own condition, no O1 event (no overcrowded cell that was alive one generation earlier), which is weaker than no overcrowding. No tori (see `energy_bounds`).

### `oscillator_period_two` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem oscillator_period_two (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (μ P : ℕ) (hP : 0 < P) (hper : ∀ t, μ ≤ t → run c (t + P) = run c t) (hO : ∀ t, μ ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) : ∀ t, μ ≤ t → run c (t + 2) = run c t
```

- **Meant to be:** A, T5: every oscillator of period ≥ 3 has them.
- **Difference:** Contrapositive form: an eventually periodic orbit with no O1 events has period dividing 2. No tori.

### `budget` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem budget (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (T K : ℕ) : (∑ t ∈ Finset.range K, (mism V c (T + t) : ℤ)) ≤ 20 * ∑ t ∈ Finset.range K, (o1 V c (T + t) : ℤ) + 26 * V.card
```

- **Meant to be:** `threshold.md`: M/(N·T) ≤ 20·O1/(N·T) + 26/T.
- **Difference:** As a sum over any window. No tori. The uncapped rule U and the Goles–Olivos theorem for it are not formalised.

## T6 in full: sealed sets

### `sealed_iff_run_dead` (`Gump/Thickness.lean`)

```lean
theorem sealed_iff_run_dead (W : Pt → Bool) (hW : ∀ p, W p = true → p.isCell = true) : Sealed W ↔ ∀ c : Config, DeadOn c W → ∀ n, DeadOn (run c n) W
```

- **Meant to be:** Th, Lemma 1 with its converse: W is sealed iff, dead, it stays dead whatever happens elsewhere.
- **Difference:** Same, for sets of cells (points that are not cells are never alive).

### `exists_birth` (`Gump/Thickness.lean`)

```lean
theorem exists_birth (W : Pt → Bool) (p : Pt) (hp : p.isCell = true) (hW : W p = true) (h4 : 4 ≤ (nbrs p).countP (fun q => !W q)) : ∃ c : Config, DeadOn c W ∧ step c p = true
```

- **Meant to be:** Th, Lemma 1, converse: if some c ∈ W has out(c, W) ≥ 4, there is a configuration with W dead whose successor has c alive.
- **Difference:** Same.

### `no_finite_sealed` (`Gump/Thickness.lean`)

```lean
theorem no_finite_sealed (L : List Pt) (hne : L ≠ []) : ¬ Sealed (fun p => L.contains p)
```

- **Meant to be:** A, T6 and Th, Theorem 3: in the full lattice no finite set is sealed.
- **Difference:** Stronger: any nonempty finite set of points, cells or not.

### `exists_six_outside` (`Gump/Thickness.lean`)

```lean
theorem exists_six_outside (S : Pt → Bool) (L : List Pt) (hL : ∀ p, S p = true → p ∈ L) (hne : ∃ p, S p = true) : ∃ p, S p = true ∧ 6 ≤ (nbrs p).countP (fun q => !S q)
```

- **Meant to be:** Th, proof of Theorem 3: 6 of the 12 neighbours of the maximiser are outside W.
- **Difference:** Same.

### `slab_not_sealed_of_finite` (`Gump/Thickness.lean`)

```lean
theorem slab_not_sealed_of_finite (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B) (S : Pt → Bool) (hSV : ∀ p, S p = true → slab d A B p = true) (L : List Pt) (hL : ∀ p, S p = true → p ∈ L) (hne : ∃ p, S p = true) : ¬ SealedIn (slab d A B) S
```

- **Meant to be:** A, T6 and Th, Theorem 3: in a slab of three or more layers no finite set is sealed.
- **Difference:** Same; "three layers" is the hypothesis that three odd levels s, s+2, s+4 lie in [A, B].

### `sealed_component_infinite` (`Gump/Thickness.lean`)

```lean
theorem sealed_component_infinite (W : Pt → Bool) (hW : Sealed W) (p : Pt) (hp : W p = true) : ¬ ∃ L : List Pt, ∀ q, Reach W p q → q ∈ L
```

- **Meant to be:** Th, Theorem 3 with Lemma 2: every component of a sealed set is infinite.
- **Difference:** Same (full lattice); `slab_component_infinite` is the slab version.

### `hull_component_touches` (`Gump/Thickness.lean`)

```lean
theorem hull_component_touches (C : Diag → Int) (W : Pt → Bool) (hW : SealedIn (hullV C) W) (hWV : ∀ p, W p = true → hullV C p = true) (p : Pt) (hp : W p = true) : ∃ q, Reach W p q ∧ 3 ≤ (nbrs q).countP (fun r => !hullV C r)
```

- **Meant to be:** A, T6 and Th, Theorem 3: in a diagonal-hull vessel every component of a sealed set is adjacent to the outside.
- **Difference:** Stronger: the cell found has at least three neighbours outside the vessel.

### `torus_slab_loop` (`Gump/ThickTorus.lean`)

```lean
theorem torus_slab_loop {α : Type} (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B) (W : Pt → Bool) (hW : SealedIn (slab d A B) W) (hWV : ∀ p, W p = true → slab d A B p = true) (cls : Pt → α) (F : List α) (hF : ∀ q, W q = true → cls q ∈ F) (p : Pt) (hp : W p = true) : ∃ q q', Reach W p q ∧ Reach W q q' ∧ q ≠ q' ∧ cls q = cls q'
```

- **Meant to be:** Th, Theorem 3: on a torus slab every component of a nonempty sealed set contains a non-contractible loop.
- **Difference:** Stated on the universal cover: two different points of one component with the same image under any map with finitely many values on W. That "sealed on the torus" equals "the lift is sealed in the infinite slab" is not proved here.

### `hexagon_sealed` (`Gump/ThickHex.lean`)

```lean
theorem hexagon_sealed (d : Diag) (c0 c1 c2 c3 c4 c5 : Pt) (hc : c0.isCell = true) (h1 : c1 ∈ kagNbrs d c0) (h2 : c2 ∈ kagNbrs d c1) (h3 : c3 ∈ kagNbrs d c2) (h4 : c4 ∈ kagNbrs d c3) (h5 : c5 ∈ kagNbrs d c4) (h0 : c0 ∈ kagNbrs d c5) (hnd : [c0, c1, c2, c3, c4, c5].Nodup) : SealedIn (slab d (d.dot c0) (d.dot c0)) (fun q => [c0, c1, c2, c3, c4, c5].contains q)
```

- **Meant to be:** A, T6 and Th, Theorem 4 (i): the 6 cells of a kagome hexagon ring form a sealed set (in one layer).
- **Difference:** Every closed kagome walk of six distinct cells, in every layer of every diagonal. That such walks are exactly the hexagon rings is a modelling choice.

### `layer_sealed_six` (`Gump/ThickSmall.lean`)

```lean
theorem layer_sealed_six (d : Diag) (s : Int) (L : List Pt) (hne : L ≠ []) (hV : ∀ p ∈ L, slab d s s p = true) (hS : SealedIn (slab d s s) (fun p => L.contains p)) : 6 ≤ L.length
```

- **Meant to be:** Th, Theorem 4 (i): no sealed set has fewer cells.
- **Difference:** Stronger than the source, where minimality was a SAT search in a patch: here every nonempty finite set sealed in a layer has at least 6 cells, for every layer and diagonal.

### `halfPlane_sealed` (`Gump/ThickSmall.lean`)

```lean
theorem halfPlane_sealed (d : Diag) (s : Int) (v : Pt) (C : Int) : SealedIn (slab d s s) (halfPlane d s v C)
```

- **Meant to be:** A, T6 and Th, Theorem 4 (ii): every half-plane of a layer is sealed.
- **Difference:** Same, for any integer direction.

### `layer_halfPlane_dead` (`Gump/ThickSmall.lean`)

```lean
theorem layer_halfPlane_dead (d : Diag) (s : Int) (v : Pt) (C : Int) (c : Config) (hout : ∀ p, slab d s s p = false → c p = false) (hc : ∀ p, slab d s s p = true → C < dotv v p → c p = false) : ∀ n p, slab d s s p = true → C < dotv v p → run c n p = false
```

- **Meant to be:** Th, Theorem 4 (ii): a one-layer pattern never leaves the convex hull of its live cells.
- **Difference:** Weaker in form: stated half-plane by half-plane. That the complement of a convex hull of lattice points is a union of integer half-planes is not formalised.

### `set36_all_sealed` (`Gump/ThickSmall.lean`)

```lean
theorem set36_all_sealed (d : Diag) (t : Pt) (ht : t.IsEven) : SealedIn (slab d (1 + d.dot t) (3 + d.dot t)) (fun q => set36.contains (d.refl (q + t.neg)))
```

- **Meant to be:** A, T6 and Th, Proposition 5: in two layers a 36-cell set is sealed.
- **Difference:** Existence only, for every two-layer slab. The set is from a fresh SAT run; the referee compared it with `sealed.py`'s and found it the same up to the slab's symmetries (`ref-lean/REVIEW.md`, `set36_compare.py`). Minimality (36) is not in Lean.

### `sealed_iff_nine` (`Gump/ThickCore.lean`)

```lean
theorem sealed_iff_nine (S : Pt → Bool) : Sealed S ↔ ∀ p, S p = true → 9 ≤ (nbrs p).countP S
```

- **Meant to be:** A, T6 remark: "at most 3 neighbours outside" is "at least 9 inside".
- **Difference:** Same.

### `core_nine` (`Gump/ThickCore.lean`)

```lean
theorem core_nine (D : Pt → Bool) : (∀ p, core D p = true → D p = true ∧ 9 ≤ (nbrs p).countP (core D)) ∧ (∀ S : Pt → Bool, (∀ p, S p = true → D p = true) → (∀ p, S p = true → 9 ≤ (nbrs p).countP S) → ∀ p, S p = true → core D p = true)
```

- **Meant to be:** A, T6 remark: the largest dead sealed set is the 9-core of the graph induced on the dead cells.
- **Difference:** Same; `core D` is the union of the sealed subsets of D.

### `core_iff_not_bp` (`Gump/ThickCore.lean`)

```lean
theorem core_iff_not_bp (D : Pt → Bool) (p : Pt) : core D p = true ↔ ¬ BPClosure (fun q => !D q) p
```

- **Meant to be:** A, T6 remark: it is the set never reached when the live cells are closed under bootstrap percolation with threshold 4.
- **Difference:** Same; the closure is defined as the least closed superset, not by rounds.

### `skeleton_mono` (`Gump/ThickCore.lean`)

```lean
theorem skeleton_mono (c : Config) (t : Nat) : ∀ k p, skeleton c t p = true → skeleton c (t + k) p = true
```

- **Meant to be:** A, T6: the largest dead sealed set K(t) only grows.
- **Difference:** Same; `slabSkeleton_mono` is the version inside a slab.

### `pocket_autonomous` (`Gump/ThickPocket.lean`)

```lean
theorem pocket_autonomous (K P : Pt → Bool) (hP : ClosedUpTo K P) (c c' : Config) (hc : ∀ n, DeadOn (run c n) K) (hc' : ∀ n, DeadOn (run c' n) K) (hag : ∀ p, P p = true → c p = c' p) : ∀ n p, P p = true → run c n p = run c' n p
```

- **Meant to be:** Th §4, reduction: the pockets a dead sealed set encloses evolve independently.
- **Difference:** Same.

### `finite_pocket_periodic` (`Gump/ThickPocket.lean`)

```lean
theorem finite_pocket_periodic (K : Pt → Bool) (hK : Sealed K) (c : Config) (t₀ : Nat) (hdead : DeadOn (run c t₀) K) (p : Pt) (hp : p.isCell = true) (hpK : K p = false) (L : List Pt) (hL : ∀ q, Reach (fun q => q.isCell && !K q) p q → q ∈ L) : ∃ μ T, 0 < T ∧ μ + T ≤ t₀ + 2 ^ L.length ∧ ∀ n, μ ≤ n → run c (n + T) p = run c n p
```

- **Meant to be:** Th §4, reduction: a finite pocket is eventually periodic.
- **Difference:** With the bound: transient plus period at most t₀ + 2^N.

### `beyond_sealed_iff` (`Gump/ThickHalf.lean`)

```lean
theorem beyond_sealed_iff (u w : Pt) (hw : dotv u w = 1) (C : Int) : Sealed (beyond u C) ↔ (u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs)
```

- **Meant to be:** (new; A, T2 says only that axis-aligned half-spaces do not confine) for a primitive integer direction, the far side of a plane is sealed iff the direction is a body diagonal.
- **Difference:** New. Primitivity is given by a witness w with u·w = 1; the reduction of a non-primitive direction is not proved.

### `sealed_unbounded` (`Gump/ThickHalf.lean`)

```lean
theorem sealed_unbounded (S : Pt → Bool) (hS : Sealed S) (hne : ∃ p, S p = true) (v : Pt) (hv : ∀ a, ∀ o ∈ offsets a, dotv v o ≠ 0) (M : Int) : ∃ p, S p = true ∧ M < dotv v p
```

- **Meant to be:** (new; sharpens Theorem 3) a nonempty sealed set is unbounded along every generic direction.
- **Difference:** New; `slab_sealed_unbounded` is the in-plane version in thick slabs.

## Theorem 2, the tilt identity, for a finite killed chain (rigour/THEOREMS.md; mathlib/GumpMath/Chain*.lean)

### `tilt_identity` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem tilt_identity {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) : log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧ log (K.lifetime μ) = ∑ i, L.price μ i ∧ Antitone (fun s => tiltMean μ L.energy s L.energy) ∧ tiltMean μ L.energy 1 L.energy ≤ log (K.lifetime μ) ∧ log (K.lifetime μ) ≤ tiltMean μ L.energy 0 L.energy ∧ tiltMean μ L.energy 0 L.energy = ∑ x, μ x * L.energy x
```

- **Meant to be:** THEOREMS.md, Theorem 2: for S(G) under (K), with μ_s ∝ μ e^{-sE}: ln τ = ∫₀¹⟨E⟩_s ds = Σ_i c_i, c_i = ∫₀¹⟨ε_i⟩_s ds; s ↦ ⟨E⟩_s is non-increasing, so ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀.
- **Difference:** Stronger in scope: any finite killed chain whose one-step death probability is a product of local factors in (0, 1] (that is (K) with the product kernel), and any quasi-stationary law μ (a probability row vector with μQ = λμ). τ is defined as Σ_t P_μ(T > t) with P_μ(T > t) = Σ_y (μQ^t)_y; the path space is not constructed. The surrogate enters by instantiation (tilt_identity_product).

### `neg_log_Z_one` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem neg_log_Z_one {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) : -log (Z μ E 1) = ∫ s in (0:ℝ)..1, tiltMean μ E s E
```

- **Meant to be:** the analytic core of Theorem 2 (the referee's reading (i)): -ln E_μ e^{-E} = ∫₀¹ ⟨E⟩_s ds for any probability vector and any real E.
- **Difference:** Same. Z(s) is a finite sum of exponentials: no eigenvalue perturbation theory is needed.

### `IsQSD.lifetime_eq` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem IsQSD.lifetime_eq {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (hh : 0 < K.hazard μ) : K.lifetime μ = 1 / K.hazard μ
```

- **Meant to be:** Lemma 0 / Theorem 2's proof: τ = E_μ T = 1/h with h = Σ μ d = 1 - λ.
- **Difference:** Same, with E_μ T := Σ_t P_μ(T > t); IsQSD.survival_eq gives P_μ(T > t) = λ^t.

### `IsQSD.last_living_law` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem IsQSD.last_living_law {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (hh : 0 < K.hazard μ) (x : σ) : ∑' t, (μ ᵥ* (K.Q ^ t)) x * K.death x = μ x * K.death x / K.hazard μ
```

- **Meant to be:** Theorem 2: μ₁(x) = μ(x) d(x)/h is the law of the last living state X_{T-1} under P_μ.
- **Difference:** Same, with P_μ(X_{T-1} = x) written as Σ_t P_μ(X_t = x) d(x).

### `price_mem` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem price_mem {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) (emax : ℝ) (hmax : ∀ i x, L.cost i x ≤ emax) (i : V) : 0 ≤ L.price μ i ∧ L.price μ i ≤ emax
```

- **Meant to be:** Theorem 2: c_i ∈ [0, ε_max].
- **Difference:** Same.

### `exists_qsd` (`mathlib/GumpMath/ChainExist.lean`)

```lean
theorem exists_qsd [Nonempty σ] (K : KilledChain σ) : ∃ μ lam, K.IsDominantQSD μ lam
```

- **Meant to be:** (used silently by Theorem 2 on hull faces and strips, where Lemma 0 is not proved) a quasi-stationary law exists.
- **Difference:** New, and the law is identified (IsDominantQSD, repair D2): every finite killed chain on a nonempty set has a quasi-stationary law whose λ is maximal among all quasi-stationary laws, at least Q u u for every state u, and the exponential decay rate of the longest-lived start (P_x(T > t) ≤ C_ε(λ+ε)^t for all x, ≥ λ^t for some x at each t). So the λ = 0 point mass on a surely-dying state is excluded wherever a state can persist. That λ is the spectral radius is not stated beyond this.

### `tilt_identity_exists` (`mathlib/GumpMath/ChainExist.lean`)

```lean
theorem tilt_identity_exists [Nonempty σ] {V : Type*} [Fintype V] (K : KilledChain σ) (L : K.LocalDeath V) : ∃ μ lam, K.IsDominantQSD μ lam ∧ Real.log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧ Real.log (K.lifetime μ) = ∑ i, L.price μ i ∧ Real.log (K.lifetime μ) ≤ ∑ x, μ x * L.energy x ∧ ∀ u, 1 / (1 - K.Q u u) ≤ K.lifetime μ
```

- **Meant to be:** Theorem 2 on every face, wrapped or rimmed.
- **Difference:** For the dominant law (IsDominantQSD); also ln τ ≤ E_μ[E] (Theorem 1) and τ ≥ 1/(1 − Q u u) for every u. Uniqueness is not claimed where Lemma 0 is not available (hull faces, strips).

### `tilt_identity_product` (`mathlib/GumpMath/ChainLemma0.lean`)

```lean
theorem tilt_identity_product [Nonempty V] : ∃ μ lam, G.toSubsetChain.killed.IsDominantQSD μ lam ∧ Real.log (G.toSubsetChain.killed.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ G.localDeath.energy s G.localDeath.energy ∧ Real.log (G.toSubsetChain.killed.lifetime μ) = ∑ i, G.localDeath.price μ i ∧ Real.log (G.toSubsetChain.killed.lifetime μ) ≤ ∑ x, μ x * G.localDeath.energy x ∧ ∀ u, 1 / (1 - G.toSubsetChain.killed.Q u u) ≤ G.toSubsetChain.killed.lifetime μ
```

- **Meant to be:** Theorem 2 for S(G): the surrogate's kernel is a product over cells with (K).
- **Difference:** For every product kernel P(x, y) = Π_i (a_i(x) if i ∈ y else 1 − a_i(x)) with 0 ≤ a_i < 1, for the dominant QSD, with the local factors the cells' own 1 − a_i (G.localDeath, named); also ln τ ≤ E_μ[E] and τ ≥ 1/(1 − Q u u). The surrogate's a_i (coins and B45/S345) is supplied by the instantiation; ChainCoins.lean has the one-cell law.

### `price_invariant` (`mathlib/GumpMath/ChainPerron.lean`)

```lean
theorem price_invariant {V : Type*} [Fintype V] {K : KilledChain σ} (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) (hlam : 0 < lam) (huniq : ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ) (g : σ ≃ σ) (hg : ∀ x y, K.Q (g x) (g y) = K.Q x y) (π : V ≃ V) (hc : ∀ i x, L.dc (π i) (g x) = L.dc i x) (i : V) : L.price μ (π i) = L.price μ i
```

- **Meant to be:** Theorem 2: on a wrapped face c_i depends only on the orientation of i; c_X = c_Y = c_Z on tori invariant under the rotation by 2π/3.
- **Difference:** For any permutation g of states preserving Q and π of cells carrying the local factors along, given that the quasi-stationary law with λ > 0 is unique. Discharged in Lean for the translations (kagome_one_price) and the rotation by 2π/3 (kagome_rotation).

### `kagome_one_price` (`mathlib/GumpMath/ChainKagome.lean`)

```lean
theorem kagome_one_price (hgen : AddSubgroup.closure ({e1, e2} : Set T) = ⊤) : ∃ μ lam, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ ν lam', (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ (o : Orient) (p q : T), (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, p) = (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, q)) ∧ Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = Fintype.card T * ∑ o : Orient, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: on a wrapped face c_i depends only on the orientation of i, so ln τ(Λ) = (A/3)(c_X + c_Y + c_Z).
- **Difference:** Same, for the surrogate on the kagome layer over every finite abelian group generated by e1, e2 (A = 3|T|), for the unique QSD with λ > 0; proved from Lemma 0 (kagome_lemma0) and the translations. The rotation clause is kagome_rotation.

### `kagome_rotation` (`mathlib/GumpMath/ChainKagome.lean`)

```lean
theorem kagome_rotation (hgen : AddSubgroup.closure ({e1, e2} : Set T) = ⊤) : ∃ μ lam, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ c c' : Cell T, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c = (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c') ∧ Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 3 * Fintype.card T * (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (Orient.X, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: c_X = c_Y = c_Z when Λ is invariant under the rotation by 2π/3 (equilateral tori): one price per cell.
- **Difference:** Same, with the invariance stated as an automorphism R of T with R e1 = -e2, R e2 = e1 - e2 (the rotation (x,y,z) ↦ (y,z,x) of the layer); then ln τ = 3|T|·c.

## Perron–Frobenius, built here (Mathlib has none)

### `exists_pos_eigenvector` (`mathlib/GumpMath/ChainPerron.lean`)

```lean
theorem exists_pos_eigenvector [Nonempty σ] {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j) (hirr : Irreducible A) : ∃ r : ℝ, 0 ≤ r ∧ ∃ v : σ → ℝ, (∀ i, 0 < v i) ∧ A *ᵥ v = r • v
```

- **Meant to be:** (the brief) a positive eigenvector of an irreducible non-negative matrix on a finite set.
- **Difference:** Same, with a non-negative eigenvalue (Wielandt's proof). That this eigenvalue is the spectral radius is not proved; left_eigenvalue_eq shows every probability row eigenvector has it.

### `left_eigen_unique` (`mathlib/GumpMath/ChainPerron.lean`)

```lean
theorem left_eigen_unique [Nonempty σ] {A : Matrix σ σ ℝ} (hA : ∀ i j, 0 ≤ A i j) (hirr : Irreducible A) {μ ν : σ → ℝ} {lam lam' : ℝ} (hμ : IsProb μ) (hν : IsProb ν) (he : μ ᵥ* A = lam • μ) (he' : ν ᵥ* A = lam' • ν) : lam = lam' ∧ μ = ν
```

- **Meant to be:** Darroch–Seneta's ingredient: the quasi-stationary law of an irreducible chain is unique.
- **Difference:** Same: two probability row eigenvectors of an irreducible non-negative matrix are equal and have the same eigenvalue.

### `qsd_exists_unique` (`mathlib/GumpMath/ChainPerron.lean`)

```lean
theorem qsd_exists_unique (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) (hin : ∀ y, ¬ p y → ∃ x, p x ∧ 0 < K.Q x y) (hu : ∃ u, p u ∧ 0 < K.Q u u) : ∃ μ lam, K.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam
```

- **Meant to be:** Lemma 0 ⇒ the quasi-stationary law μ is unique and charges every non-empty state.
- **Difference:** Uniqueness among laws with λ > 0. Lean's IsQSD is only the eigen-equation μQ = λμ, under which the point mass at a surely-dying state (the all-alive wrapped face) is a solution with λ = 0; under the standard definition of a QSD (P_μ(T > t) > 0 for all t, i.e. λ > 0) the source's statement is right as written.

### `decay_bounds` (`mathlib/GumpMath/ChainRate.lean`)

```lean
theorem decay_bounds (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] [Nonempty {x // p x}] (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) : ∃ r m M : ℝ, 0 ≤ r ∧ 0 < m ∧ m ≤ M ∧ (∀ ν lam, K.IsQSD ν lam → 0 < lam → lam = r) ∧ (∀ t x, p x → m / M * r ^ t ≤ K.survFrom t x) ∧ (∀ t x, K.survFrom (t + 1) x ≤ M / m * r ^ t)
```

- **Meant to be:** Lemma 0 / Darroch–Seneta: from the quasi-stationary law the death time is geometric with ratio λ; the source's τ is meant as the lifetime of a face.
- **Difference:** New: from every state x of the living class, (m/M)λ^t ≤ P_x(T > t) and P_x(T > t+1) ≤ (M/m)λ^t, m ≤ w ≤ M the Perron column vector, and every QSD with λ > 0 has this λ. So the decay rate from every start is λ.

### `lifetime_from_bounds` (`mathlib/GumpMath/ChainRate.lean`)

```lean
theorem lifetime_from_bounds (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] [Nonempty {x // p x}] (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) : ∃ r m M : ℝ, 0 ≤ r ∧ 0 < m ∧ m ≤ M ∧ (∀ ν lam, K.IsQSD ν lam → 0 < lam → lam = r) ∧ (r < 1 → ∀ x, p x → m / M / (1 - r) ≤ K.lifetimeFrom x ∧ K.lifetimeFrom x ≤ 1 + M / m / (1 - r))
```

- **Meant to be:** (the tie between τ = E_μ T and a lifetime measured from a fair start)
- **Difference:** New: conditional on r < 1 (an implication in the theorem): (m/M)/(1−λ) ≤ E_x T ≤ 1 + (M/m)/(1−λ) for x in the class; ln E_x T = ln τ up to ln(M/m) + O(1). The spread M/m is not bounded. lifetime_from_bounds_K proves r < 1 from (K).

### `lifetime_from_bounds_K` (`mathlib/GumpMath/ChainRate.lean`)

```lean
theorem lifetime_from_bounds_K (K : KilledChain σ) (p : σ → Prop) [DecidablePred p] [Nonempty {x // p x}] (hirr : Irreducible (K.block p)) (hout : ∀ y, ¬ p y → ∀ z, K.Q y z = 0) (hK : ∀ x, 0 < K.death x) : ∃ r m M : ℝ, 0 ≤ r ∧ r < 1 ∧ 0 < m ∧ m ≤ M ∧ (∀ ν lam, K.IsQSD ν lam → 0 < lam → lam = r) ∧ (∀ x, p x → m / M / (1 - r) ≤ K.lifetimeFrom x ∧ K.lifetimeFrom x ≤ 1 + M / m / (1 - r))
```

- **Meant to be:** (the tie between τ and a lifetime from a start, unconditional)
- **Difference:** As lifetime_from_bounds with λ < 1 proved from (K): every state dies with positive probability.

## Theorem 1, the upper bound, with its constant

### `upper_bound` (`mathlib/GumpMath/ChainTilt.lean`)

```lean
theorem upper_bound {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) (emax : ℝ) (hmax : ∀ i x, L.cost i x ≤ emax) : log (K.lifetime μ) ≤ ∑ x, μ x * L.energy x ∧ ∑ x, μ x * L.energy x ≤ emax * Fintype.card V
```

- **Meant to be:** THEOREMS.md, Theorem 1: ln τ ≤ E_μ[E] ≤ ε_max · A.
- **Difference:** Same, for any finite killed chain with local death factors and any quasi-stationary law.

### `threeCoins_death_ge` (`mathlib/GumpMath/ChainCoins.lean`)

```lean
theorem threeCoins_death_ge {ρ1 ρ2 : ℝ} (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) (alive : Bool) (k : ℕ) (hk : k ≤ 6) : atomMin ρ1 ρ2 ≤ death3 ρ1 ρ2 alive k
```

- **Meant to be:** Theorem 1: with three coins ε_max = -ln min(ρ1²ρ2, (1-ρ1)²(1-ρ2)): every death of a cell needs b = 0 or b = 3.
- **Difference:** Same, for every state of the cell and k ≤ 6 live in-layer neighbours.

### `twoCoins_death_ge` (`mathlib/GumpMath/ChainCoins.lean`)

```lean
theorem twoCoins_death_ge {ρ1 ρ2 : ℝ} (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) (alive : Bool) (k : ℕ) (hk : k ≤ 2) : atomMin ρ1 ρ2 ≤ death2 ρ1 alive k
```

- **Meant to be:** (K) on hull faces: the corners have coins (2,0) and two neighbours.
- **Difference:** The same bound holds for them (k ≤ 2).

### `upper_bound_coins` (`mathlib/GumpMath/ChainCoins.lean`)

```lean
theorem upper_bound_coins {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ} (hμ : K.IsQSD μ lam) {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) (hdc : ∀ i x, atomMin ρ1 ρ2 ≤ L.dc i x) : log (K.lifetime μ) ≤ -log (atomMin ρ1 ρ2) * Fintype.card V
```

- **Meant to be:** Theorem 1 with its constant, for every face.
- **Difference:** Hypothesis: every local factor is at least the smallest atom, which the two lemmas above give for the surrogate's cells.

### `emax_main` (`mathlib/GumpMath/ChainCoins.lean`)

```lean
theorem emax_main : -log (atomMin 0.44 0.42) ≤ 2.51
```

- **Meant to be:** Theorem 1: ε_max = 2.509 at (0.44, 0.42).
- **Difference:** Proved ε_max ≤ 2.51; the exact value −ln(0.44²·0.42) = 2.50946… exceeds the printed 2.509 (rounding). On wrapped faces kagome_sharp_bound gives ln τ ≤ 2.2412·A, hence ≤ 2.509·A there; on hull faces only 2.51·A is proved.

### `emax_fair` (`mathlib/GumpMath/ChainCoins.lean`)

```lean
theorem emax_fair : -log (atomMin 0.5 0.5) ≤ 2.08
```

- **Meant to be:** Theorem 1: ε_max = 2.079 at (½, ½).
- **Difference:** Proved ε_max ≤ 2.08 (the exact value is ln 8).

### `kagome_upper_bound` (`mathlib/GumpMath/ChainKagome.lean`)

```lean
theorem kagome_upper_bound {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) {μ : Living (Cell T) → ℝ} {lam : ℝ} (hμ : (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam) : Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) ≤ -Real.log (atomMin ρ1 ρ2) * (3 * Fintype.card T)
```

- **Meant to be:** THEOREMS.md, Theorem 1 on wrapped faces: ln τ ≤ 2.509·A.
- **Difference:** ln τ ≤ -ln min(ρ1²ρ2,(1-ρ1)²(1-ρ2))·A for every QSD of the surrogate on the kagome layer over T, A = 3|T|; with emax_main, ≤ 2.51·A at (0.44, 0.42).

### `kagome_sharp_bound` (`mathlib/GumpMath/ChainSharp.lean`)

```lean
theorem kagome_sharp_bound {μ : Living (Cell T) → ℝ} {lam : ℝ} (hμ : (kernel e1 e2 0.44 0.42 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam) : Real.log ((kernel e1 e2 0.44 0.42 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) ≤ 2.2412 * (3 * Fintype.card T)
```

- **Meant to be:** ref-chain/REVIEW.md D7 (the referee's paper proof): ln τ ≤ (2ε_max + ε₂)/3·A = 2.2411·A on wrapped faces.
- **Difference:** Same argument, for every QSD of the surrogate on the kagome layer over any finite T at (0.44, 0.42), proved as ≤ 2.2412·A (the constant is 2.241096). Ingredients: indeg (every cell is the neighbour of six slots), card_S_le (3|S| ≤ 2A), energy_le_sharp. Not for hull faces. The dice agent's Gump.Dice.lntau_le_regular (ln τ < 1.9228·A on its faces proved regular) is a separate theorem about Gump.Dice.Face.

## Lemma 0, one living class

### `kagome_lemma0` (`mathlib/GumpMath/ChainKagome.lean`)

```lean
theorem kagome_lemma0 (hgen : AddSubgroup.closure ({e1, e2} : Set T) = ⊤) : let C := (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain Irreducible (C.killed.block C.canLive) ∧ (∀ y, ¬ C.canLive y → ∀ z, C.killed.Q y z = 0) ∧ (∀ y : Living (Cell T), 0 < C.killed.Q ⟨uX, uX_nonempty⟩ y) ∧ (∃ μ lam, C.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', C.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
```

- **Meant to be:** THEOREMS.md, Lemma 0 (wrapped faces), geometry included: one living class, aperiodic at u = the X cells, the rest dies surely and is reachable from u; hence the QSD is unique and charges every non-empty state.
- **Difference:** For the surrogate with three coins per cell (0 < ρ1, ρ2 < 1) on the kagome layer over any finite abelian group T generated by e1, e2 (every wrapped face (H,K),(0,D) is T = ℤ²/⟨(H,K),(0,D)⟩), neighbours with multiplicity. The neighbour lists were checked against reference/oracle.py's offsets by a script (notes/chain.md), not in Lean; that this layer is the other agent's `torus` face is not proved. Uniqueness among λ > 0. Step (4) is proved by a different route (Y and Z detours) from the source's line growth.

### `one_class` (`mathlib/GumpMath/ChainInst.lean`)

```lean
theorem one_class (K : KilledChain σ) (u : σ) (hu : ∀ y, 0 < K.Q u y) (hreach : ∀ x, K.CanSurvive x → ∃ k, 0 < (K.Q ^ k) x u) : ∃ μ lam, K.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', K.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam
```

- **Meant to be:** THEOREMS.md, Lemma 0 and its consequence: one living class, so the quasi-stationary law is unique and charges every non-empty state.
- **Difference:** Abstract form, for any finite killed chain: if some living state u leads to every living state in one step (step (3): the X cells, every cell with k = 2) and every state that can survive one step leads to u (steps (1), (2), (4)), the law with λ > 0 is unique and positive. The two hypotheses are the geometric content, to be checked on each face.

### `lemma0` (`mathlib/GumpMath/ChainLemma0.lean`)

```lean
theorem lemma0 [Nonempty V] (hsing : ∀ i j : V, ReflTransGen C.Step {i} {j}) (u : Finset V) (hun : u.Nonempty) (hu : C.M u = univ) (hreach : ∃ i, ReflTransGen C.Step {i} u) : Irreducible (C.killed.block C.canLive) ∧ (∀ y, ¬ C.canLive y → ∀ z, C.killed.Q y z = 0) ∧ (∀ y : Living V, 0 < C.killed.Q ⟨u, hun⟩ y) ∧ C.canLive ⟨u, hun⟩
```

- **Meant to be:** THEOREMS.md, Lemma 0: on a wrapped face Q is irreducible and aperiodic on L, every state outside L dies surely, every state is reachable from L.
- **Difference:** The geometric steps of the proof are hypotheses: (2) singletons communicate, (3) a state u with M(u) = V, (4) u reachable from a singleton. Step (1) is the hypothesis of SubsetChain, proved for product kernels (ProductKernel.supp).

### `lemma0_qsd` (`mathlib/GumpMath/ChainLemma0.lean`)

```lean
theorem lemma0_qsd [Nonempty V] (hsing : ∀ i j : V, ReflTransGen C.Step {i} {j}) (u : Finset V) (hun : u.Nonempty) (hu : C.M u = univ) (hreach : ∃ i, ReflTransGen C.Step {i} u) : ∃ μ lam, C.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', C.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam
```

- **Meant to be:** Lemma 0: the quasi-stationary law is unique and charges every non-empty state.
- **Difference:** Among laws with λ > 0 (see qsd_exists_unique).

### `death_pos` (`mathlib/GumpMath/ChainLemma0.lean`)

```lean
theorem death_pos (a : Living V) : 0 < C.killed.death a
```

- **Meant to be:** (K) in the form used by Lemma 0's proof: from every state the face is empty one generation later with positive probability.
- **Difference:** Follows from step (1) (∅ ⊆ M(x)).

## Lemma R, routes

### `routes_first` (`mathlib/GumpMath/ChainRoutes.lean`)

```lean
theorem routes_first [Nonempty ι] (h c : ι → ℝ → ℝ) (A : ℝ) (hpos : ∀ r, 0 < h r A) (hd : ∀ r, HasDerivAt (h r) (-(c r A) * h r A) A) : HasDerivAt (fun B => -log (∑ r, h r B)) (meanPrice h c A) A
```

- **Meant to be:** Lemma R: d ln τ/dA = Σ_r p_r c_r.
- **Difference:** Same, for any finite partition into differentiable positive rates with h_r' = -c_r h_r.

### `routes_second` (`mathlib/GumpMath/ChainRoutes.lean`)

```lean
theorem routes_second [Nonempty ι] (h c c' : ι → ℝ → ℝ) (A : ℝ) (hpos : ∀ r, 0 < h r A) (hd : ∀ r, HasDerivAt (h r) (-(c r A) * h r A) A) (hc : ∀ r, HasDerivAt (c r) (c' r A) A) : HasDerivAt (meanPrice h c) (-(∑ r, share h r A * (c r A - meanPrice h c A) ^ 2) + ∑ r, share h r A * c' r A) A
```

- **Meant to be:** Lemma R: d² ln τ/dA² = -Var_p(c) + Σ_r p_r c_r'.
- **Difference:** Same, as the derivative of Σ p c.

### `log_odds` (`mathlib/GumpMath/ChainRoutes.lean`)

```lean
theorem log_odds (h1 h2 : ℝ → ℝ) (c1 c2 A : ℝ) (p1 : 0 < h1 A) (p2 : 0 < h2 A) (d1 : HasDerivAt h1 (-c1 * h1 A) A) (d2 : HasDerivAt h2 (-c2 * h2 A) A) : HasDerivAt (fun B => log (h1 B / h2 B)) (c2 - c1) A
```

- **Meant to be:** Lemma R: for two routes d ln(p₁/p₂)/dA = c₂ - c₁.
- **Difference:** Same.

### `routes_concave` (`mathlib/GumpMath/ChainRoutes.lean`)

```lean
theorem routes_concave [Nonempty ι] (a c : ι → ℝ) (ha : ∀ r, 0 < a r) : ConcaveOn ℝ Set.univ (fun B => -log (∑ r, a r * exp (-(c r * B))))
```

- **Meant to be:** Lemma R: two routes each exactly exponential in A give a concave ln τ.
- **Difference:** Any finite number of exponential routes.

### `two_routes_step` (`mathlib/GumpMath/ChainRoutes.lean`)

```lean
theorem two_routes_step (α β cb cs D : ℝ) (hα : 0 < α) (hβ : 0 < β) : -log (expRoute α cb (D + 1) + expRoute β cs (D + 1)) - (-log (expRoute α cb D + expRoute β cs D)) = cs - log (1 - expRoute α cb D / (expRoute α cb D + expRoute β cs D) * (1 - exp (-(cb - cs))))
```

- **Meant to be:** Lemma R's discrete form, as corrected by the referee (REVIEW.md A3): ln τ(D+1) - ln τ(D) = c_s - ln(1 - p(D)(1 - e^{-(c_b - c_s)})).
- **Difference:** Same; the source's c_s + p(c_b - c_s) is not this.

## The seam identity (blast/image)

### `seam_identity` (`mathlib/GumpMath/ChainSeam.lean`)

```lean
theorem seam_identity (hF : ∀ i j, 0 ≤ F i j) (M L' k : ℕ) (hk : 1 ≤ k) (hL : L' + 1 = k * (M + 1)) (a : B) (xs : Fin M → B) : PT F M a xs = (∑ ys : Fin L' → B, PC F M L' a xs a ys) * Matrix.trace (F ^ (M + 1 + (L' + 1))) / (Matrix.trace (F ^ (M + 1)) * (F ^ (L' + 1)) a a)
```

- **Meant to be:** image/README.md: a torus is its cover conditioned on the seam's whole history recurring one loop along, divided by how likely that is: P_T(s₀..s_{m-1}) = P_C(s₀..s_{m-1}, s_m = s₀)/[π(s₀) Z].
- **Difference:** The finite-K exact form, with (F^L)(s₀, s₀)/Tr F^N in place of π(s₀)·const, for F ≥ 0 and a cover a whole number of loops long. The factorisation of the history weight into a transfer matrix on bands two graph steps thick, and the cover having the same F, are the hypothesis (the ring weight), not derived from gump's rule. The referee measured that it also holds off multiples wherever (F^L)(a,a) > 0 (not formalised), and fails otherwise (2-cycle).

### `seam_identity_obs` (`mathlib/GumpMath/ChainSeam.lean`)

```lean
theorem seam_identity_obs (hF : ∀ i j, 0 ≤ F i j) (M L' k : ℕ) (hk : 1 ≤ k) (hL : L' + 1 = k * (M + 1)) (f : B → (Fin M → B) → ℝ) : ∑ a, ∑ xs, PT F M a xs * f a xs = ∑ a, ∑ xs, ∑ ys : Fin L' → B, PC F M L' a xs a ys * f a xs * (Matrix.trace (F ^ (M + 1 + (L' + 1))) / (Matrix.trace (F ^ (M + 1)) * (F ^ (L' + 1)) a a))
```

- **Meant to be:** (★): P_T(pattern on W) = P_C(pattern on W) · E_C[Q | pattern on W] / Z, for windows in the seam.
- **Difference:** For the mean of any observable of the torus's cut configuration.

### `seam_sharp` (`mathlib/GumpMath/ChainSeam.lean`)

```lean
theorem seam_sharp (M : ℕ) (h1 : Matrix.trace (F ^ (M + 1)) = 1) (h2 : Matrix.trace (F ^ (M + 1 + (M + 1))) = 1) (a : B) (xs : Fin M → B) : ∑ ys : Fin M → B, PC F M M a xs a ys = PT F M a xs * ∑ ys : Fin M → B, PT F M a ys
```

- **Meant to be:** REVIEW.md B, the sharp form for K = 2: P_C(seam = s₀, rest = s₁, image = s₀) = P_T(s₀, s₁) · P_T(seam = s₀).
- **Difference:** Under Tr F^m = Tr F^{2m} = 1 (the referee's Z = 1 for a deterministic rule from a normalised soup), which is assumed, not derived.

### `cover_marginal` (`mathlib/GumpMath/ChainSeam.lean`)

```lean
theorem cover_marginal (M L' : ℕ) (a : B) (xs : Fin M → B) : ∑ ys : Fin L' → B, coverW F M L' a xs a ys = torusW F M a xs * (F ^ (L' + 1)) a a
```

- **Meant to be:** image/README.md, "comparing the two products term by term".
- **Difference:** Same (Chapman–Kolmogorov, sum_pathF).

### `coverW_eq_ringL` (`mathlib/GumpMath/ChainSeam.lean`)

```lean
theorem coverW_eq_ringL (M L' : ℕ) (a : B) (xs : Fin M → B) (c : B) (ys : Fin L' → B) : coverW F M L' a xs c ys = ringL F (a :: (List.ofFn xs ++ c :: List.ofFn ys))
```

- **Meant to be:** (the modelling step) the cover's weight cut at the seam and its image is the product of F round the ring.
- **Difference:** Same.

## Theorem 3, conditional on (SSM)

### `thm3a` (`mathlib/GumpMath/ChainSSM.lean`)

```lean
theorem thm3a {F : ι → Face} {cinf K ξ K0 : ℝ} (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0) (g : ι) : |(F g).logTau - cinf * (F g).area| ≤ K * ∑ i, exp (-((F g).r i / ξ)) + K0
```

- **Meant to be:** THEOREMS.md, Theorem 3 (a): under (SSM), |ln τ(G) - c_∞ A| ≤ K Σ_i e^{-r_i/ξ}.
- **Difference:** With the referee's repair (an additive K₀), and from the integrated hypothesis IntSSM (|c_i(G) - c_∞| ≤ K e^{-r_i/ξ} + K₀/A), which is all the proof uses and which (SSM) implies (SSM.toIntSSM). r_i is any number attached to each cell.

### `SSM.toIntSSM` (`mathlib/GumpMath/ChainSSM.lean`)

```lean
theorem SSM.toIntSSM {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0) (hint : IntervalIntegrable einf MeasureTheory.volume 0 1) : IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0
```

- **Meant to be:** Theorem 3's hypothesis (SSM), uniform in s ∈ [0,1], with the referee's K₀/A.
- **Difference:** Needs e_∞ integrable; redundant for every family with arbitrarily small error terms (SSM.toIntSSM_of_small).

### `thm3b` (`mathlib/GumpMath/ChainSSM.lean`)

```lean
theorem thm3b {F : ι → Face} {cinf K ξ K0 ℓ : ℝ} (hK : 0 ≤ K) (hξ : 0 < ξ) (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0) (g : ι) (hr : ∀ i, (ℓ - 2) / 2 ≤ (F g).r i) : |(F g).logTau - cinf * (F g).area| ≤ K * (F g).area * exp (-((ℓ - 2) / (2 * ξ))) + K0
```

- **Meant to be:** Theorem 3 (b): wrapped faces with shortest loop ℓ: |ln τ - c_∞ A| ≤ K A e^{-(ℓ-2)/2ξ}.
- **Difference:** Plus K₀; the geometric fact r_i ≥ (ℓ - 2)/2 is the hypothesis.

### `thm3c` (`mathlib/GumpMath/ChainSSM.lean`)

```lean
theorem thm3c {F : ι → Face} {cinf K ξ K0 C R : ℝ} (hK : 0 ≤ K) (hξ : 0 < ξ) (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0) (g : ι) (d : (F g).V → ℕ) (hd : ∀ i, (F g).r i = d i) (hcount : ∀ r : ℕ, ((univ.filter (fun i => d i = r)).card : ℝ) ≤ C * R) (hCR : 0 ≤ C * R) : |(F g).logTau - cinf * (F g).area| ≤ K * (C * R / (1 - exp (-(1 / ξ)))) + K0
```

- **Meant to be:** Theorem 3 (c): polygons: |ln τ - c_∞ A| ≤ K Σ_r n_r e^{-r/ξ} ≤ K′·(rim length).
- **Difference:** Plus K₀; with integer distances and at most C·R cells at each distance as hypotheses, K′ = K C/(1 - e^{-1/ξ}).

### `thm3d` (`mathlib/GumpMath/ChainSSM.lean`)

```lean
theorem thm3d {F : ℕ → Face} {cinf K ξ K0 : ℝ} (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0) (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop) (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0)) : Tendsto (fun n => (F n).logTau / (F n).area) atTop (𝓝 cinf)
```

- **Meant to be:** Theorem 3 (d): along a sequence with rim/A → 0 and ℓ → ∞, ln τ / A → c_∞, the same number for rimmed and wrapped faces.
- **Difference:** Stated with A → ∞ and Σ_i e^{-r_i/ξ} = o(A) as the hypotheses.

### `tilt_riemann_bounds` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem tilt_riemann_bounds (G : Face) (n : ℕ) (hn : 0 < n) : (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k + 1 : ℕ) / n) G.L.energy ≤ G.logTau ∧ G.logTau ≤ (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy
```

- **Meant to be:** (new; THEOREMS.md Theorem 2's monotonicity, used quantitatively) ln τ from finitely many tilted means.
- **Difference:** New: (1/n)Σ_{k=1}^{n}⟨E⟩_{k/n} ≤ ln τ ≤ (1/n)Σ_{k=0}^{n-1}⟨E⟩_{k/n} on every face, a bracket of width ≤ ε_max A/n.

### `price_of_pointwise` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem price_of_pointwise (F : ℕ → Face) (emax : ℝ) (hA : ∀ n, 0 < (F n).area) (hmax : ∀ n i x, (F n).L.cost i x ≤ emax) (f : ℝ → ℝ) (hlim : ∀ s ∈ Set.Ioc (0:ℝ) 1, Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (f s))) : Tendsto (fun n => (F n).logTau / (F n).area) atTop (𝓝 (∫ s in (0:ℝ)..1, f s))
```

- **Meant to be:** (new; replaces (SSM) in Theorem 3 (d)) the price per cell from a bulk limit at each tilt.
- **Difference:** New and weaker than (SSM): if ⟨E⟩_{s,G_n}/A_n → f(s) for every s ∈ (0,1] (no rate, no uniformity in s, no locality; jumps of f allowed), then ln τ/A → ∫₀¹ f. Two families have one price when their pointwise limits agree. Its hypothesis asks convergence at the jump point too; price_of_ae (the referee's) needs only almost every s.

### `SSM.einf_continuousOn` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem SSM.einf_continuousOn {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0) (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) : ContinuousOn einf (Set.Icc 0 1)
```

- **Meant to be:** REVIEW.md A2.3 (the referee's argument): a jump of e_∞ makes (SSM) false, since every finite face's curve is continuous.
- **Difference:** Same, as a theorem: (SSM) on a family with arbitrarily small error terms forces e_∞ continuous on [0,1].

### `price_compare` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem price_compare (G G' : Face) (hA : 0 < G.area) (hA' : 0 < G'.area) (n : ℕ) (hn : 0 < n) (δ w : ℝ) (hδ : ∀ k ≤ n, |tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy / G.area - tiltMean G'.μ G'.L.energy ((k : ℕ) / n) G'.L.energy / G'.area| ≤ δ) (hw : (tiltMean G.μ G.L.energy 0 G.L.energy - tiltMean G.μ G.L.energy 1 G.L.energy) / G.area ≤ w) (hw' : (tiltMean G'.μ G'.L.energy 0 G'.L.energy - tiltMean G'.μ G'.L.energy 1 G'.L.energy) / G'.area ≤ w) : |G.logTau / G.area - G'.logTau / G'.area| ≤ δ + w / n
```

- **Meant to be:** (new; the finite form of price_of_pointwise) two faces with the same per-cell tilted energy at finitely many tilts have nearly the same price.
- **Difference:** New: if the per-cell curves differ by ≤ δ at s = k/n and each falls by ≤ w over [0,1], then |ln τ/A − ln τ′/A′| ≤ δ + w/n.

### `price_of_ae` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem price_of_ae (F : ℕ → Face) (emax : ℝ) (hA : ∀ n, 0 < (F n).area) (hmax : ∀ n i x, (F n).L.cost i x ≤ emax) (f : ℝ → ℝ) (hlim : ∀ᵐ s ∂volume, s ∈ Set.Ioc (0:ℝ) 1 → Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (f s))) : Tendsto (fun n => (F n).logTau / (F n).area) atTop (𝓝 (∫ s in (0:ℝ)..1, f s))
```

- **Meant to be:** (the referee's form of price_of_pointwise, taken over from ref-chain/RefChainVacuity.lean)
- **Difference:** ln τ/A → ∫₀¹f from convergence of ⟨E⟩_{s,G_n}/A_n for almost every s ∈ (0,1]: a first-order jump costs nothing even if the finite curves do not converge at the jump point.

### `SSM.toIntSSM_of_small` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem SSM.toIntSSM_of_small {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0) (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) : IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0
```

- **Meant to be:** (taken over from the referee) (SSM) gives IntSSM with no integrability hypothesis.
- **Difference:** For families with arbitrarily small error terms. (Lean also has it under the referee's name SSM.toIntSSM'.)

### `SSM.tilt_limit` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem SSM.tilt_limit {F : ℕ → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0) (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop) (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0)) (s : ℝ) (hs : s ∈ Set.Icc (0:ℝ) 1) : Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (einf s))
```

- **Meant to be:** (taken over from the referee, RefChainSSM.lean) under (SSM) the per-cell tilted energy converges to e_∞ at every tilt.
- **Difference:** Along families with A → ∞ and Σ_i e^{-r_i/ξ} = o(A).

### `jump_refutes_SSM` (`mathlib/GumpMath/ChainTiltLimit.lean`)

```lean
theorem jump_refutes_SSM {F : ℕ → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop) (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0)) (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) (f : ℝ → ℝ) (hf : ∀ s ∈ Set.Icc (0:ℝ) 1, Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (f s))) (hjump : ¬ ContinuousOn f (Set.Icc 0 1)) : ¬ SSM F einf K ξ K0
```

- **Meant to be:** REVIEW.md A2.3 in full (taken over from the referee): a jump of the limiting per-cell tilted energy refutes (SSM).
- **Difference:** For families with large faces and arbitrarily small error terms, whatever e_∞, K, K₀.

## The price per cell (conditional on gluing inequalities)

### `price_exists_of_sub` (`mathlib/GumpMath/ChainPrice.lean`)

```lean
theorem price_exists_of_sub (a : ℕ → ℝ) (C : ℝ) (ha : ∀ n, 0 ≤ a n) (hsub : ∀ m n, a (m + n) ≤ a m + a n + C) : ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧ ∀ n, n ≠ 0 → p ≤ (a n + C) / n
```

- **Meant to be:** (README climb, line 6) the price per cell exists.
- **Difference:** Conditional: under a(m+n) ≤ a(m) + a(n) + C with a ≥ 0 (Fekete); then p ≤ (a n + C)/n for every n. The inequality is not proved for the surrogate.

### `price_exists_of_super` (`mathlib/GumpMath/ChainPrice.lean`)

```lean
theorem price_exists_of_super (a : ℕ → ℝ) (C' M : ℝ) (hM : ∀ n, n ≠ 0 → a n ≤ M * n) (hsup : ∀ m n, a m + a n - C' ≤ a (m + n)) : ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧ ∀ n, n ≠ 0 → (a n - C') / n ≤ p
```

- **Meant to be:** the same from the other side.
- **Difference:** Conditional: under a(m+n) ≥ a(m) + a(n) - C′ and a n ≤ M n; then p ≥ (a n - C′)/n. The inequality is the lower bound B2 in another form and is not proved.

### `price_interval` (`mathlib/GumpMath/ChainPrice.lean`)

```lean
theorem price_interval (a : ℕ → ℝ) (C C' : ℝ) (ha : ∀ n, 0 ≤ a n) (hsub : ∀ m n, a (m + n) ≤ a m + a n + C) (hsup : ∀ m n, a m + a n - C' ≤ a (m + n)) : ∃ p, Tendsto (fun n => a n / n) atTop (𝓝 p) ∧ ∀ n, n ≠ 0 → (a n - C') / n ≤ p ∧ p ≤ (a n + C) / n
```

- **Meant to be:** (README climb, line 6) a proved interval for the price from certified finite faces.
- **Difference:** Conditional on both gluing inequalities: p ∈ [(a n - C′)/n, (a n + C)/n] for every n ≥ 1.

## The instantiation interface (for GumpMath/Dice*.lean)

### `isQSD_of` (`mathlib/GumpMath/ChainInst.lean`)

```lean
theorem isQSD_of (P : Matrix S S ℝ) (o : S) (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1) (μ : S → ℝ) (lam : ℝ) (h0 : μ o = 0) (hnn : ∀ x, 0 ≤ μ x) (htot : ∑ x, μ x = 1) (heig : ∀ y, y ≠ o → ∑ x, μ x * P x y = lam * μ y) : (ofStochastic P o hP hrow).IsQSD (fun x => μ x) lam
```

- **Meant to be:** (the shape of Gump.Dice.IsQSD) a law on all states vanishing at the empty face and a left eigenvector on the others is a quasi-stationary law of the killed chain.
- **Difference:** Same.

### `surrogate_theorems` (`mathlib/GumpMath/ChainInst.lean`)

```lean
theorem surrogate_theorems {V : Type*} [Fintype V] (P : Matrix S S ℝ) (o : S) (hne : ∃ x, x ≠ o) (hP : ∀ x y, 0 ≤ P x y) (hrow : ∀ x, ∑ y, P x y = 1) (a : V → S → ℝ) (ha0 : ∀ i x, 0 ≤ a i x) (ha1 : ∀ i x, a i x < 1) (hprod : ∀ x, x ≠ o → P x o = ∏ i, (1 - a i x)) {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) (hatom : ∀ i x, atomMin ρ1 ρ2 ≤ 1 - a i x) : ∃ μ lam, (ofStochastic P o hP hrow).IsDominantQSD μ lam ∧ Real.log ((ofStochastic P o hP hrow).lifetime μ) = ∑ i, (ofStochastic_local P o hP hrow a ha0 ha1 hprod).price μ i ∧ Real.log ((ofStochastic P o hP hrow).lifetime μ) ≤ -Real.log (atomMin ρ1 ρ2) * Fintype.card V ∧ ∀ u, 1 / (1 - (ofStochastic P o hP hrow).Q u u) ≤ (ofStochastic P o hP hrow).lifetime μ
```

- **Meant to be:** Theorems 1 and 2 for S(G), from the surrogate's kernel as a stochastic matrix with the empty face absorbing.
- **Difference:** Hypotheses: P ≥ 0, rows sum to 1, P(x, ∅) = Π_i (1 − a_i(x)) with 0 ≤ a_i < 1, and 1 − a_i ≥ min(ρ1²ρ2, (1−ρ1)²(1−ρ2)). The law is the dominant QSD and the local factors are named (ofStochastic_local … a); also τ ≥ 1/(1 − Q u u).

### `bitP_row` (`mathlib/GumpMath/ChainBits.lean`)

```lean
theorem bitP_row (x : Fin (2 ^ A)) : ∑ y, bitP A a x y = 1
```

- **Meant to be:** (needed by the instantiation) the surrogate's kernel on bit masks is stochastic: Σ_y Π_{i<A}(a_i or 1 - a_i) = 1.
- **Difference:** For every a: a sum over bit masks of a product over bits factorises (sum_bits).

### `one_sub_aliveProbR_three` (`mathlib/GumpMath/ChainBits.lean`)

```lean
theorem one_sub_aliveProbR_three (ρ1 ρ2 : ℝ) (k : ℕ) (s : Bool) : 1 - aliveProbR ρ1 ρ2 2 1 k s = death3 ρ1 ρ2 s k
```

- **Meant to be:** (the instantiation) 1 - aliveProb with coins (2,1) is the death probability of ChainCoins.
- **Difference:** Same, for every k and state; aliveProbR is Gump.Dice.aliveProb transcribed over ℝ (by reading, not by a Lean proof).

### `bit_surrogate` (`mathlib/GumpMath/ChainBits.lean`)

```lean
theorem bit_surrogate (A : ℕ) (hA : 0 < A) (ρ1 ρ2 : ℝ) (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) (m1 m2 : ℕ → ℕ) (k : ℕ → ℕ → ℕ) (hcell : ∀ (x : Fin (2 ^ A)) i, i < A → (m1 i = 2 ∧ m2 i = 1 ∧ k x i ≤ 6) ∨ (m1 i = 2 ∧ m2 i = 0 ∧ k x i ≤ 2)) : let a : ℕ → ℕ → ℝ := fun x i => aliveProbR ρ1 ρ2 (m1 i) (m2 i) (k x i) ((x : ℕ).testBit i) ∃ (hP : ∀ x y, 0 ≤ bitP A a x y) (μ : {x : Fin (2 ^ A) // x ≠ empty A} → ℝ) (lam : ℝ) (L : (ofStochastic (bitP A a) (empty A) hP bitP_row).LocalDeath (Fin A)), (ofStochastic (bitP A a) (empty A) hP bitP_row).IsDominantQSD μ lam ∧ (∀ (i : Fin A) (x : {x : Fin (2 ^ A) // x ≠ empty A}), L.dc i x = 1 - aliveProbR ρ1 ρ2 (m1 i) (m2 i) (k ((x : Fin (2 ^ A)) : ℕ) i) (((x : Fin (2 ^ A)) : ℕ).testBit i)) ∧ Real.log ((ofStochastic (bitP A a) (empty A) hP bitP_row).lifetime μ) = ∑ i, L.price μ i ∧ Real.log ((ofStochastic (bitP A a) (empty A) hP bitP_row).lifetime μ) ≤ -Real.log (atomMin ρ1 ρ2) * A ∧ ∀ u, 1 / (1 - (ofStochastic (bitP A a) (empty A) hP bitP_row).Q u u) ≤ (ofStochastic (bitP A a) (empty A) hP bitP_row).lifetime μ
```

- **Meant to be:** THEOREMS.md, Theorems 1 and 2 for S(G) on every face, in the bit-mask form of GumpMath/DiceDef.lean.
- **Difference:** Every face with A ≥ 1 cells whose cells have coins (2,1) and k ≤ 6, or (2,0) and k ≤ 2 (hull faces and strips included): the dominant QSD, the local factor of cell i named as 1 − aliveProbR(cell i) (repair D1: so ln τ = Σ_i c_i is about per-cell prices), ln τ ≤ ε_max·A, τ ≥ 1/(1 − Q u u). k is any function with those bounds, not tied to a neighbourhood; the face's m1, m2, k and the cast from ℚ are the remaining inputs.

### `bit_one_class` (`mathlib/GumpMath/ChainBits.lean`)

```lean
theorem bit_one_class (h0 : ∀ (x : Fin (2 ^ A)) i, i < A → 0 ≤ a x i) (h1 : ∀ (x : Fin (2 ^ A)) i, i < A → a x i < 1) (u : Fin (2 ^ A)) (hu0 : u ≠ empty A) (hu : ∀ i, i < A → 0 < a u i) (hreach : ∀ x, (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le)) bitP_row).CanSurvive x → ∃ k, 0 < ((ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le)) bitP_row).Q ^ k) x ⟨u, hu0⟩) : ∃ μ lam, (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le)) bitP_row).IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', (ofStochastic (bitP A a) (empty A) (bitP_nonneg h0 (fun x i hi => (h1 x i hi).le)) bitP_row).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam
```

- **Meant to be:** Lemma 0 on bit masks: the QSD is unique and charges every non-empty state.
- **Difference:** Hypotheses: a state u in which every cell can be alive next (on wrapped faces: one orientation, k = 2 everywhere), and every state that can survive reaches u (the geometric part, per face).

## Every wrapped face (H,K),(0,D) (rigour/geom.py `torus H K D`)

### `torus_finite` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem torus_finite (H K D : ℤ) (hH : 0 < H) (hD : 0 < D) : Finite (Torus H K D)
```

- **Meant to be:** (the setting) the translations of the wrapped face (H,K),(0,D) form a finite group.
- **Difference:** T = ℤ²/⟨(H,K),(0,D)⟩ in the basis E1, E2, for H, D > 0 (every class has a representative in [0,H)×[0,D)); torus_generated: generated by the images of (1,0) and (0,1).

### `wrapped_lemma0` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_lemma0 : let C := (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain Irreducible (C.killed.block C.canLive) ∧ (∀ y, ¬ C.canLive y → ∀ z, C.killed.Q y z = 0) ∧ (∀ y : Living (Cell (Torus H K D)), 0 < C.killed.Q ⟨uX, uX_nonempty⟩ y) ∧ (∃ μ lam, C.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ ∀ ν lam', C.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
```

- **Meant to be:** THEOREMS.md, Lemma 0, on every wrapped face.
- **Difference:** kagome_lemma0 on T = ℤ²/⟨(H,K),(0,D)⟩, for any Fintype and DecidableEq instances (one exists: torus_fintype).

### `wrapped_one_price` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_one_price : ∃ μ lam, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ (o : Orient) (p q : Torus H K D), (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, p) = (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, q)) ∧ Real.log ((kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = Fintype.card (Torus H K D) * ∑ o : Orient, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: one price per orientation on every wrapped face.
- **Difference:** Same, log τ = |T|·(c_X + c_Y + c_Z); |T| = HD is torus_card, and wrapped_one_price_HD states log τ = HD·(c_X + c_Y + c_Z).

### `wrapped_upper_bound` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_upper_bound {μ : Living (Cell (Torus H K D)) → ℝ} {lam : ℝ} (hμ : (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam) : Real.log ((kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) ≤ -Real.log (atomMin ρ1 ρ2) * (3 * Fintype.card (Torus H K D))
```

- **Meant to be:** THEOREMS.md, Theorem 1 on every wrapped face.
- **Difference:** ln τ ≤ ε_max·3|T| for every QSD.

### `wrapped_rotation` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_rotation (H K D : ℤ) [Fintype (Torus H K D)] [DecidableEq (Torus H K D)] (hl1 : (K, -H - K) ∈ lattice H K D) (hl2 : (D, -D) ∈ lattice H K D) {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) : ∃ μ lam, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ c c' : Cell (Torus H K D), (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c = (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c') ∧ Real.log ((kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 3 * Fintype.card (Torus H K D) * (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (Orient.X, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: c_X = c_Y = c_Z when Λ is invariant under the rotation by 2π/3.
- **Difference:** Invariance stated as (K, -H-K) ∈ Λ and (D, -D) ∈ Λ (the images of the two periods under (a,b) ↦ (b, -a-b)).

### `torus_2_0_2_one_price` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem torus_2_0_2_one_price [Fintype (Torus 2 0 2)] [DecidableEq (Torus 2 0 2)] {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) : ∃ μ lam, (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ c c' : Cell (Torus 2 0 2), (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c = (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c') ∧ Real.log ((kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 3 * Fintype.card (Torus 2 0 2) * (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (Orient.X, 0)
```

- **Meant to be:** (example) the 12-cell torus (2,0),(0,2) of rigour/data/exact.csv.
- **Difference:** Unique QSD and ln τ = 3|T|·c, one price per cell; torus_2_0_2_twelve states ln τ = 12·c. The number c is not computed in Lean.

### `torus_card` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem torus_card (H K D : ℤ) (hH : 0 < H) (hD : 0 < D) [Fintype (Torus H K D)] : (Fintype.card (Torus H K D) : ℤ) = H * D
```

- **Meant to be:** (rows wrapped_one_price, torus_2_0_2_one_price) |T| = HD.
- **Difference:** Same: |ℤ²/⟨(H,K),(0,D)⟩| = H·D for H, D > 0 (the representatives [0,H)×[0,D) are a bijection, torusRep_bijective).

### `wrapped_one_price_HD` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_one_price_HD : ∃ μ lam, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ ν lam', (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ (o : Orient) (p q : Torus H K D), (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, p) = (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, q)) ∧ Real.log ((kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = (H : ℝ) * D * ∑ o : Orient, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (o, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: ln τ(Λ) = (A/3)(c_X + c_Y + c_Z) on every wrapped face.
- **Difference:** Same, A = 3HD, for the unique QSD with λ > 0.

### `wrapped_rotation_HD` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem wrapped_rotation_HD (hl1 : (K, -H - K) ∈ lattice H K D) (hl2 : (D, -D) ∈ lattice H K D) : ∃ μ lam, (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ c c' : Cell (Torus H K D), (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c = (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c') ∧ Real.log ((kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 3 * (H : ℝ) * D * (kernel (te1 H K D) (te2 H K D) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (Orient.X, 0)
```

- **Meant to be:** THEOREMS.md, Theorem 2: on rotation-invariant tori one price per cell, ln τ = A·c.
- **Difference:** Same, ln τ = 3HD·c.

### `torus_2_0_2_twelve` (`mathlib/GumpMath/ChainTorus.lean`)

```lean
theorem torus_2_0_2_twelve [Fintype (Torus 2 0 2)] [DecidableEq (Torus 2 0 2)] {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) : ∃ μ lam, (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ 0 < lam ∧ (∀ c c' : Cell (Torus 2 0 2), (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c = (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ c') ∧ Real.log ((kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 12 * (kernel (te1 2 0 2) (te2 2 0 2) ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ (Orient.X, 0)
```

- **Meant to be:** (example) the 12-cell torus (2,0),(0,2): ln τ = 12·c.
- **Difference:** Same; c is not computed in Lean.

## The dice surrogate's lifetime: kernel-checked certificates (rigour/README.md, THEOREMS.md; mathlib/GumpMath/Dice*.lean)

### `hull3_lifetime` (`mathlib/GumpMath/DiceHull3.lean`)

```lean
theorem hull3_lifetime (t : ℕ) : (0.72 : ℚ) * 0.9165673655948901373 ^ t ≤ (hull 3).survival ρ1 ρ2 t (hull 3).full ∧ ∀ x, (hull 3).survival ρ1 ρ2 t x ≤ 1384 * 0.9165673655948901374 ^ t
```

- **Meant to be:** rigour/README.md claim 3: the 9-cell hull triangle R = 3 at (0.44, 0.42), ln τ = 2.4837157463 (h = 8.3432634405e-02, dense.py and qsd.c).
- **Difference:** Weaker than the README's number in one respect and different in kind: it pins the decay rate λ to 19 digits for every t, but its constants are loose (the true sup over t of P_x(T > t)/λ^t is about 1.63, against the stated 1384; ref-dice REVIEW.md). ln τ itself is hull3_tau. The chain is `Face.P` of DiceDef.lean (tied to dense.py by dice_tie.py and, exactly, by the referee's kernel).

### `hull3_tau` (`mathlib/GumpMath/DiceHull3.lean`)

```lean
theorem hull3_tau (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) : (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧ 2.4837157463 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.4837157464
```

- **Meant to be:** the same row: ln τ = 2.4837157463, τ := E_μ T = 1/h for the quasi-stationary law μ.
- **Difference:** For every quasi-stationary law (μ, λ) (IsQSD: a probability vector on the non-empty states with μQ = λμ), 0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374 and 2.4837157463 < -ln(1-λ) < 2.4837157464. Existence and uniqueness of μ (Lemma 0) are not proved here; the statement is vacuous if no QSD exists.

### `torus103_tau` (`mathlib/GumpMath/DiceTorus103.lean`)

```lean
theorem torus103_tau (μ : Fin (2 ^ (torus 1 0 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 0 3) ρ1 ρ2 μ lam) (hlam : 0 < lam) : (0.9664099275695942426 : ℝ) ≤ lam ∧ lam ≤ 0.9664099275695942427 ∧ 3.3935247190 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 3.3935247191
```

- **Meant to be:** README claim 3: wrapped face (1,0),(0,3), ln τ = 3.3935247191.
- **Difference:** 3.3935247190 < ln τ < 3.3935247191 for every QSD with λ > 0 (a QSD with λ = 0 exists here: the point mass on the full face, which dies surely).

### `torus113_tau` (`mathlib/GumpMath/DiceTorus113.lean`)

```lean
theorem torus113_tau (μ : Fin (2 ^ (torus 1 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 1 3) ρ1 ρ2 μ lam) (hlam : 0 < lam) : (0.9324323935928482210 : ℝ) ≤ lam ∧ lam ≤ 0.9324323935928482211 ∧ 2.6946266059 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.6946266060
```

- **Meant to be:** README claim 3: wrapped face (1,1),(0,3), ln τ = 2.6946266059.
- **Difference:** 2.6946266059 < ln τ < 2.6946266060, every QSD with λ > 0.

### `strip13_tau` (`mathlib/GumpMath/DiceStrip13.lean`)

```lean
theorem strip13_tau (μ : Fin (2 ^ (strip 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (strip 1 3) ρ1 ρ2 μ lam) : (0.9391216736592712685 : ℝ) ≤ lam ∧ lam ≤ 0.9391216736592712686 ∧ 2.7988780569 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.7988780570
```

- **Meant to be:** README claim 3: free strip 1×3, ln τ = 2.7988780569.
- **Difference:** 2.7988780569 < ln τ < 2.7988780570, every QSD.

### `patch13_tau` (`mathlib/GumpMath/DicePatch13.lean`)

```lean
theorem patch13_tau (μ : Fin (2 ^ (patch 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (patch 1 3) ρ1 ρ2 μ lam) : (0.8474738060566295030 : ℝ) ≤ lam ∧ lam ≤ 0.8474738060566295031 ∧ 1.8804189341 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 1.8804189342
```

- **Meant to be:** README claim 3: patch 1×3, ln τ = 1.8804189341.
- **Difference:** Bounds as stated in the theorem, every QSD.

### `torus113_lifetime` (`mathlib/GumpMath/DiceTorus113.lean`)

```lean
theorem torus113_lifetime (t : ℕ) : (0.71 : ℚ) * 0.9324323935928482210 ^ t ≤ (torus 1 1 3).survival ρ1 ρ2 t ⟨73, by decide⟩ ∧ ∀ x, (torus 1 1 3).survival ρ1 ρ2 (t + 1) x ≤ 9.86 * 0.9324323935928482211 ^ (t + 1)
```

- **Meant to be:** the survival form for the wrapped face (1,1),(0,3).
- **Difference:** Lower bound from the state with the cells of orientation x alive (the full face dies surely); the upper bound from t+1 on, for every state.

## Both exits at 9 cells (rigour/README.md claim 4; mathlib/GumpMath/DiceExit*.lean)

### `torus113_bust` (`mathlib/GumpMath/DiceTorus113Exit.lean`)

```lean
theorem torus113_bust (μ : Fin (2 ^ (torus 1 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 1 3) ρ1 ρ2 μ lam) (hlam : 0 < lam) : 0.936852 < (torus 1 1 3).bustShare ρ1 ρ2 6 μ lam ∧ (torus 1 1 3).bustShare ρ1 ρ2 6 μ lam < 0.936853
```

- **Meant to be:** README claim 4: wrapped (1,1),(0,3), bust share 0.9369 (qsd.c halffall_share K=6: a fall of ≥ ⌈A/2⌉ cells in one generation among the last 6 transitions).
- **Difference:** bustShare 6 μ λ ∈ (0.936852, 0.936853) for every QSD with λ > 0. bustShare is defined as 1 - μ·noBust 6 / (λ^5 (1-λ)); that this is the share of the death flux is the stationarity argument in DiceExit.lean's header, in prose, not formalised (it is now a theorem in path form: `flux_share`, `torus113_bust_flux`). The share is the stationary share of the death flux (deaths from the quasi-stationary law), not the share of all deaths from a fixed start (on this torus, from state 73, that share is 0.934, ref-dice second review).

### `hull3_bust` (`mathlib/GumpMath/DiceHull3Exit.lean`)

```lean
theorem hull3_bust (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) : 0.017017 < (hull 3).bustShare ρ1 ρ2 6 μ lam ∧ (hull 3).bustShare ρ1 ρ2 6 μ lam < 0.017018
```

- **Meant to be:** README claim 4: triangle R = 3, bust share 0.0170: a rimmed face dies by the fade.
- **Difference:** bustShare 6 ∈ (0.017017, 0.017018) for every QSD; same caveat. The share is the stationary share of the death flux (deaths from the quasi-stationary law), not the share of all deaths from a fixed start (from the full hull face it is about 0.152, ref-dice).

## Theorem 1 for every size (rigour/THEOREMS.md Theorem 1; mathlib/GumpMath/DiceBound.lean)

### `survival_le_all` (`mathlib/GumpMath/DiceBound.lean`)

```lean
theorem survival_le_all (F : Face) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) (hc : ∀ q, F.coin q = true) : ∀ (t : ℕ) (x : Fin (2 ^ F.A)), F.survival ρ1 ρ2 t x ≤ (1 - delta0 ρ1 ρ2 ^ F.A) ^ t
```

- **Meant to be:** THEOREMS.md Theorem 1 (B1): ln τ ≤ ε_max·A, ε_max = -ln min(ρ1²ρ2, (1-ρ1)²(1-ρ2)).
- **Difference:** Survival form, for every face whose points beneath all carry coins (every wrapped face and strip, every size) and all densities in [0,1]: P_x(T > t) ≤ (1 - δ₀^A)^t. The middle term E_μ[E] (Jensen) is not formalised; hull faces (corners with two coins) are not covered.

### `qsd_le_all` (`mathlib/GumpMath/DiceBound.lean`)

```lean
theorem qsd_le_all (F : Face) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) (hc : ∀ q, F.coin q = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) : lam ≤ 1 - ((delta0 ρ1 ρ2 ^ F.A : ℚ) : ℝ)
```

- **Meant to be:** the same, eigenvalue form.
- **Difference:** λ ≤ 1 - δ₀^A for every QSD.

### `lntau_le_all` (`mathlib/GumpMath/DiceBound.lean`)

```lean
theorem lntau_le_all (F : Face) (hc : ∀ q, F.coin q = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (hA : 0 < F.A) : -Real.log (1 - lam) < 2.5095 * F.A
```

- **Meant to be:** THEOREMS.md: ε_max = 2.509 at (0.44, 0.42).
- **Difference:** ln τ < 2.5095·A for every QSD of every such face.

### `lntau_le_regular` (`mathlib/GumpMath/DiceBound2.lean`)

```lean
theorem lntau_le_regular (F : Face) (hc : ∀ q, F.coin q = true) (hr : F.regular) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (hA : 0 < F.A) : -Real.log (1 - lam) < 1.9228 * F.A
```

- **Meant to be:** THEOREMS.md Theorem 1, sharpened (not in the source): a finite local inequality that bounds every wrapped face at once.
- **Difference:** For every face with all its coins that is regular (six neighbour slots per cell, each cell in six slots: every wrapped face; `regular` is checked here for the tori (1,0),(0,3), (1,1),(0,3), (2,0),(0,2) only, not proved for the general torus), ln τ < 1.9228·A for every QSD (δ₁ = 0.1462 from a weight 152/125 on every live-dead edge; the weights cancel).

## Second task, 2026-11-24 14:00–15:30 UTC: the exits as path statements; Theorem 1 on every hull face (mathlib/GumpMath/DiceFlux.lean, DiceHull.lean, DiceBound3.lean, DiceHullAll.lean)

### `flux_share` (`mathlib/GumpMath/DiceFlux.lean`)

```lean
theorem flux_share (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (h0 : 0 < lam) (h1 : lam < 1) (K : ℕ) (hK : 1 ≤ K) (m : ℕ) : (∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if (F.dies l && F.bustLast K l) = true then 1 else 0) x : ℝ)) / (∑ x, μ x * (F.pathE ρ1 ρ2 (m + K) (fun l => if F.dies l = true then 1 else 0) x : ℝ)) = F.bustShare ρ1 ρ2 K μ lam
```

- **Meant to be:** rigour/README.md claim 4 and qsd.c halffall_share: the share of the quasi-stationary death flux whose last K transitions contain a fall of at least half the face.
- **Difference:** Path form, every generation: for every QSD (μ, λ) with 0 < λ < 1, K ≥ 1, m ≥ 0, P_μ(T = m+K, bust in the last K) / P_μ(T = m+K) = bustShare K μ λ, with paths summed explicitly (pathE: every list of m+K states with the product of its transition probabilities). Replaces the prose step of DiceExit.lean. The sum over all generations is not formed (every generation has the same ratio). The share is the stationary share of the death flux (deaths from the quasi-stationary law), not the share of all deaths from a fixed start (from the full hull face it is about 0.152, ref-dice).

### `death_flux` (`mathlib/GumpMath/DiceFlux.lean`)

```lean
theorem death_flux (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (n : ℕ) : ∑ x, μ x * (F.pathE ρ1 ρ2 (n + 1) (fun l => if F.dies l = true then 1 else 0) x : ℝ) = lam ^ n * (1 - lam)
```

- **Meant to be:** From the QSD the death time is geometric: P_μ(T = n+1) = λ^n (1-λ).
- **Difference:** Same, on the explicit path sum.

### `hull3_bust_flux` (`mathlib/GumpMath/DiceFlux.lean`)

```lean
theorem hull3_bust_flux (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) (m : ℕ) : 0.017017 < (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if ((hull 3).dies l && (hull 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) / (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if (hull 3).dies l = true then 1 else 0) x : ℝ)) ∧ (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if ((hull 3).dies l && (hull 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) / (∑ x, μ x * ((hull 3).pathE ρ1 ρ2 (m + 6) (fun l => if (hull 3).dies l = true then 1 else 0) x : ℝ)) < 0.017018
```

- **Meant to be:** README claim 4: triangle R = 3, bust share 0.0170 (a rimmed face dies by the fade).
- **Difference:** For every QSD and every generation m+6, the path share is in (0.017017, 0.017018). The share is the stationary share of the death flux (deaths from the quasi-stationary law), not the share of all deaths from a fixed start (from the full hull face it is about 0.152, ref-dice).

### `torus113_bust_flux` (`mathlib/GumpMath/DiceFlux.lean`)

```lean
theorem torus113_bust_flux (μ : Fin (2 ^ (torus 1 1 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 1 1 3) ρ1 ρ2 μ lam) (hlam : 0 < lam) (m : ℕ) : 0.936852 < (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if ((torus 1 1 3).dies l && (torus 1 1 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) / (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if (torus 1 1 3).dies l = true then 1 else 0) x : ℝ)) ∧ (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if ((torus 1 1 3).dies l && (torus 1 1 3).bustLast 6 l) = true then 1 else 0) x : ℝ)) / (∑ x, μ x * ((torus 1 1 3).pathE ρ1 ρ2 (m + 6) (fun l => if (torus 1 1 3).dies l = true then 1 else 0) x : ℝ)) < 0.936853
```

- **Meant to be:** README claim 4: wrapped (1,1),(0,3), bust share 0.9369.
- **Difference:** For every QSD with λ > 0 and every generation m+6, in (0.936852, 0.936853). The share is the stationary share of the death flux (deaths from the quasi-stationary law), not the share of all deaths from a fixed start (on this torus the full face dies surely; from state 73 the share of all deaths is 0.934, ref-dice).

### `lntau_le_hull` (`mathlib/GumpMath/DiceHull.lean`)

```lean
theorem lntau_le_hull (R : ℕ) (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam) (hA : 0 < (hull R).A) : -Real.log (1 - lam) < 2.5095 * (hull R).A
```

- **Meant to be:** THEOREMS.md Theorem 1 (B1) on hull faces, whose corners have two coins.
- **Difference:** Every R: ln τ < 2.5095·A for every QSD of hull R (hull_cells: corners have coins (2,0) and degree ≤ 2, every other cell (2,1)); survival_le_hull for every state and t.

### `lntau_le_hull_all` (`mathlib/GumpMath/DiceHullAll.lean`)

```lean
theorem lntau_le_hull_all (R : ℕ) (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam) (hA : 0 < (hull R).A) : -Real.log (1 - lam) < 2.2165 * (hull R).A
```

- **Meant to be:** The weighted local inequality applied to hull faces (not in the source).
- **Difference:** Every R: ln τ < 2.2165·A for every QSD of hull R (weight 1341/1000 on live–dead slots; hull_balanced and hull_type: degrees 6/4/2 with coins (2,1)/(2,1)/(2,0), proved for every R; type_check by the kernel).

### `torus_regular` (`mathlib/GumpMath/DiceTorusReg.lean`)

```lean
theorem torus_regular (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) : (torus H K D).regular
```

- **Meant to be:** (needed for the weighted bound on wrapped faces) every wrapped face has six neighbour slots per cell and every cell is in six slots.
- **Difference:** Every torus H K D with H, D > 0 (Face.regular), from the reduction modulo the period lattice (Tr_shift, Tr_sub, Tr_id) and the symmetry red_symm.

### `lntau_le_torus` (`mathlib/GumpMath/DiceTorusReg.lean`)

```lean
theorem lntau_le_torus (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (μ : Fin (2 ^ (torus H K D).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus H K D) ρ1 ρ2 μ lam) (hA : 0 < (torus H K D).A) : -Real.log (1 - lam) < 1.9228 * (torus H K D).A
```

- **Meant to be:** The weighted local inequality on wrapped faces (not in the source).
- **Difference:** Every wrapped face (H, D > 0): ln τ < 1.9228·A for every QSD. Replaces the per-face checks of DiceRegular.lean.

### `qsd_mean` (`mathlib/GumpMath/DiceMean.lean`)

```lean
theorem qsd_mean (F : Face) (ρ1 ρ2 : ℚ) (h0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → F.P ρ1 ρ2 F.empty y = 0) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (hl0 : 0 ≤ lam) (hl1 : lam < 1) : ∑' t : ℕ, ∑ x, μ x * (F.survival ρ1 ρ2 t x : ℝ) = 1 / (1 - lam)
```

- **Meant to be:** rigour/README.md: τ := E_μ T = 1/h, h = 1 − λ, for the quasi-stationary law μ.
- **Difference:** Same, as Σ_t P_μ(T > t) = 1/(1 − λ) for every QSD with 0 ≤ λ < 1 on any face whose ∅ is absorbing (qsd_survival: P_μ(T > t) = λ^t). Proved by the referee ref-dice (QsdSurvival.lean, 003cb73), taken over in DiceMean.lean; qsd_mean_all, hull3_mean, qsd_mean_hull instantiate it.

## The link: Theorems 1 and 2 and Lemma 0 for the dice agent's Face.P (GumpMath/Link*.lean)

### `P_cast` (`mathlib/GumpMath/LinkBridge.lean`)

```lean
theorem P_cast (F : Face) (ρ1 ρ2 : ℚ) (x y : Fin (2 ^ F.A)) : ((F.P ρ1 ρ2 x y : ℚ) : ℝ) = bitP F.A (aR F ρ1 ρ2) x y
```

- **Meant to be:** (the chain notes' instantiation step (1)) Face.P over ℝ is the chain arm's bitP.
- **Difference:** Same, for every Gump.Dice.Face and all ρ1, ρ2 (aliveProb_cast: the dice agent's binomial sums cast to ℝ are aliveProbR).

### `toDice` (`mathlib/GumpMath/LinkBridge.lean`)

```lean
theorem toDice (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ} {lam : ℝ} (h : (chain F hd).IsQSD μ lam) : IsQSD F ρ1 ρ2 (extend F μ) lam
```

- **Meant to be:** (the bridge) the chain's quasi-stationary laws are the dice agent's Gump.Dice.IsQSD.
- **Difference:** Extension by 0 at the empty face; ofDice is the converse.

### `face_theorems` (`mathlib/GumpMath/LinkBridge.lean`)

```lean
theorem face_theorems (F : Face) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) (hA : 0 < F.A) : ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ (∀ i x, (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs hc).price μ i ∧ Real.log ((chain F hs.dens).lifetime μ) ≤ -Real.log (atomMin (ρ1 : ℝ) (ρ2 : ℝ)) * F.A ∧ ∀ u, 1 / (1 - (chain F hs.dens).Q u u) ≤ (chain F hs.dens).lifetime μ
```

- **Meant to be:** THEOREMS.md, Theorems 1 and 2, for Face.P itself: the dominant QSD, ln τ = Σ_i c_i with c_i the price of cell i's own death probability, ln τ ≤ ε_max·A.
- **Difference:** For every Face whose cells have coins (2,1), or (2,0) with at most two neighbours (CellsOK), at 0 < ρ1, ρ2 < 1; the chain is ofStochastic of (F.P : ℝ) at F.empty. face_theorems_allcoins: every face with all its coins.

### `aliveProbR_pos_iff` (`mathlib/GumpMath/LinkUnique.lean`)

```lean
theorem aliveProbR_pos_iff {ρ1 ρ2 : ℝ} (h0 : 0 < ρ1) (h1 : ρ1 < 1) (h2 : 0 < ρ2) (h3 : ρ2 < 1) (m1 m2 k : ℕ) (s : Bool) : 0 < aliveProbR ρ1 ρ2 m1 m2 k s ↔ canB m1 m2 k s = true
```

- **Meant to be:** (Lemma 0, step (1), for the coin law) a cell can be alive next iff some coin outcome puts k + heads in the window.
- **Difference:** For 0 < ρ1, ρ2 < 1, any coin counts.

### `face_class` (`mathlib/GumpMath/LinkUnique.lean`)

```lean
theorem face_class : ∃ hu' : u < 2 ^ F.A, (∀ y, 0 < (chain F hs.dens).Q ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩ y) ∧ ∀ x, (chain F hs.dens).CanSurvive x → ∃ k, 0 < ((chain F hs.dens).Q ^ k) x ⟨⟨u, hu'⟩, u_ne F c htab hc u nxt dist huOK hR hu'⟩
```

- **Meant to be:** THEOREMS.md, Lemma 0, face by face: u leads to every living state in one step and every state that can survive leads to u.
- **Difference:** From a certificate (u, nxt, dist) checked by the kernel against the dice agent's checked tables (uOK, reachOK).

### `face_lifetime` (`mathlib/GumpMath/LinkUnique.lean`)

```lean
theorem face_lifetime (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hcd : cellsD c F.A = true) (hA : 0 < F.A) (u : ℕ) (nxt dist : List ℕ) (huOK : uOK c F.A u = true) (hR : reachOK c F.A u nxt dist = true) (lo hi a b : ℝ) (hτ : ∀ μ lam, IsQSD F ρ1 ρ2 μ lam → 0 < lam → lo ≤ lam ∧ lam ≤ hi ∧ a < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < b) : ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ lo ≤ lam ∧ lam ≤ hi ∧ a < Real.log ((chain F hs.dens).lifetime μ) ∧ Real.log ((chain F hs.dens).lifetime μ) < b ∧ (∀ i x, (localDeath F hs (cellsOK_of_tab F c htab hcd)).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs (cellsOK_of_tab F c htab hcd)).price μ i ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain F hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain F hs.dens).survFrom t x) ∧ (∀ t x, (chain F hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** (the assembly) the lifetime theorem of a certified face.
- **Difference:** Given the tables, the reachability certificate and the dice agent's interval for λ for every QSD with λ > 0.

### `price_sym` (`mathlib/GumpMath/LinkSym.lean`)

```lean
theorem price_sym (htab : c.tabOK F = true) (hsym : c.symOK F.A σ I = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hρ1 : ρ1 = (c.n1 : ℚ) / c.d1) (hρ2 : ρ2 = (c.n2 : ℚ) / c.d2) (hc : CellsOK F) {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ} {lam : ℝ} (hμ : (chain F hs.dens).IsQSD μ lam) (hlam : 0 < lam) (huniq : ∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) (i : Fin F.A) : (localDeath F hs hc).price μ (cellPerm F c hsym i) = (localDeath F hs hc).price μ i
```

- **Meant to be:** THEOREMS.md, Theorem 2: equal prices for cells exchanged by a symmetry.
- **Difference:** For every permutation of the cells preserving the dice agent's tables (Data.symOK, DiceSym.lean), given uniqueness of the QSD with λ > 0.

### `hull3_full` (`mathlib/GumpMath/LinkFaces.lean`)

```lean
theorem hull3_full : ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧ 2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧ (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (hull 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) for the face (hull 3): its quasi-stationary law exists, is unique and charges every living state; ln τ = 2.4837157463…; ln τ is a sum of per-cell prices.
- **Difference:** One theorem about Gump.Dice.Face.P at (0.44, 0.42): the dominant QSD is unique among λ > 0 and positive on every living state; 0.9165673655948901373 ≤ λ ≤ 0.9165673655948901374 (the dice agent's certificate) and 2.4837157463 < ln τ < 2.4837157464; survival from every state that can survive is between (m/M)λ^t and (M/m)λ^(t−1); ln τ = Σ_i c_i with c_i the price of cell i's own death probability 1 − F.a x i; equal prices within the classes corners {0,3,8}, the other six cells. τ = E_μ T is defined through the killed chain's survival sums.

### `torus103_full` (`mathlib/GumpMath/LinkFaces.lean`)

```lean
theorem torus103_full : ∃ μ lam, (chain (torus 1 0 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 1 0 3) ρ1 ρ2 (extend (torus 1 0 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus 1 0 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.9664099275695942426 : ℝ) ≤ lam ∧ lam ≤ 0.9664099275695942427 ∧ 3.3935247190 < Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) < 3.3935247191 ∧ (∀ i x, L.dc i x = 1 - (((torus 1 0 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus 1 0 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (torus 1 0 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus 1 0 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus 1 0 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (torus 1 0 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) for the face (torus 1 0 3): its quasi-stationary law exists, is unique and charges every living state; ln τ = 3.3935247190…; ln τ is a sum of per-cell prices.
- **Difference:** One theorem about Gump.Dice.Face.P at (0.44, 0.42): the dominant QSD is unique among λ > 0 and positive on every living state; 0.9664099275695942426 ≤ λ ≤ 0.9664099275695942427 (the dice agent's certificate) and 3.3935247190 < ln τ < 3.3935247191; survival from every state that can survive is between (m/M)λ^t and (M/m)λ^(t−1); ln τ = Σ_i c_i with c_i the price of cell i's own death probability 1 − F.a x i; equal prices within the classes {0,1,3,4,6,7} and {2,5,8} (c_X = c_Y ≠ c_Z, as the referee measured). τ = E_μ T is defined through the killed chain's survival sums.

### `torus113_full` (`mathlib/GumpMath/LinkFaces.lean`)

```lean
theorem torus113_full : ∃ μ lam, (chain (torus 1 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 1 1 3) ρ1 ρ2 (extend (torus 1 1 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus 1 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.9324323935928482210 : ℝ) ≤ lam ∧ lam ≤ 0.9324323935928482211 ∧ 2.6946266059 < Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) < 2.6946266060 ∧ (∀ i x, L.dc i x = 1 - (((torus 1 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus 1 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (torus 1 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus 1 1 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus 1 1 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (torus 1 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) for the face (torus 1 1 3): its quasi-stationary law exists, is unique and charges every living state; ln τ = 2.6946266059…; ln τ is a sum of per-cell prices.
- **Difference:** One theorem about Gump.Dice.Face.P at (0.44, 0.42): the dominant QSD is unique among λ > 0 and positive on every living state; 0.9324323935928482210 ≤ λ ≤ 0.9324323935928482211 (the dice agent's certificate) and 2.6946266059 < ln τ < 2.6946266060; survival from every state that can survive is between (m/M)λ^t and (M/m)λ^(t−1); ln τ = Σ_i c_i with c_i the price of cell i's own death probability 1 − F.a x i; equal prices within the classes one class: all nine prices equal. τ = E_μ T is defined through the killed chain's survival sums.

### `strip13_full` (`mathlib/GumpMath/LinkFaces.lean`)

```lean
theorem strip13_full : ∃ μ lam, (chain (strip 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (strip 1 3) ρ1 ρ2 (extend (strip 1 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (strip 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.9391216736592712685 : ℝ) ≤ lam ∧ lam ≤ 0.9391216736592712686 ∧ 2.7988780569 < Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) < 2.7988780570 ∧ (∀ i x, L.dc i x = 1 - (((strip 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (strip 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (strip 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (strip 1 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (strip 1 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (strip 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) for the face (strip 1 3): its quasi-stationary law exists, is unique and charges every living state; ln τ = 2.7988780569…; ln τ is a sum of per-cell prices.
- **Difference:** One theorem about Gump.Dice.Face.P at (0.44, 0.42): the dominant QSD is unique among λ > 0 and positive on every living state; 0.9391216736592712685 ≤ λ ≤ 0.9391216736592712686 (the dice agent's certificate) and 2.7988780569 < ln τ < 2.7988780570; survival from every state that can survive is between (m/M)λ^t and (M/m)λ^(t−1); ln τ = Σ_i c_i with c_i the price of cell i's own death probability 1 − F.a x i; equal prices within the classes {0,2,3,5,6,8} and {1,4,7}. τ = E_μ T is defined through the killed chain's survival sums.

### `patch13_full` (`mathlib/GumpMath/LinkFaces.lean`)

```lean
theorem patch13_full : ∃ μ lam, (chain (patch 1 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (patch 1 3) ρ1 ρ2 (extend (patch 1 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (patch 1 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.8474738060566295030 : ℝ) ≤ lam ∧ lam ≤ 0.8474738060566295031 ∧ 1.8804189341 < Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) < 1.8804189342 ∧ (∀ i x, L.dc i x = 1 - (((patch 1 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (patch 1 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (patch 1 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (patch 1 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (patch 1 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (patch 1 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) for the face (patch 1 3): its quasi-stationary law exists, is unique and charges every living state; ln τ = 1.8804189341…; ln τ is a sum of per-cell prices.
- **Difference:** One theorem about Gump.Dice.Face.P at (0.44, 0.42): the dominant QSD is unique among λ > 0 and positive on every living state; 0.8474738060566295030 ≤ λ ≤ 0.8474738060566295031 (the dice agent's certificate) and 1.8804189341 < ln τ < 1.8804189342; survival from every state that can survive is between (m/M)λ^t and (M/m)λ^(t−1); ln τ = Σ_i c_i with c_i the price of cell i's own death probability 1 − F.a x i; equal prices within the classes {0,8}, {1,7}, {2,6}, {3,5}, {4}. τ = E_μ T is defined through the killed chain's survival sums.

### `face_unique` (`mathlib/GumpMath/LinkNoCert.lean`)

```lean
theorem face_unique (F : Face) (c : Data) (htab : c.tabOK F = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) (hA : 0 < F.A) (u : ℕ) (nx ds : ℕ → ℕ) (huOK : uOK c F.A u = true) (hR : reachOKF c F.A u nx ds = true) : ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs hc).price μ i ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain F hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain F hs.dens).survFrom t x) ∧ (∀ t x, (chain F hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** (the assembly without a certified λ) Lemma 0, the decay rate and the tilt identity for a face.
- **Difference:** As face_lifetime without the λ interval; the certificate is given as functions (trees for 12 cells).

### `torus202_full` (`mathlib/GumpMath/LinkTorus202.lean`)

```lean
theorem torus202_full : ∃ μ lam, (chain (torus 2 0 2) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus 2 0 2) ρ1 ρ2 (extend (torus 2 0 2) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus 2 0 2) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, L.dc i x = 1 - (((torus 2 0 2).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus 2 0 2) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (torus 2 0 2).A, L.price μ i = L.price μ j) ∧ Real.log ((chain (torus 2 0 2) sdens.dens).lifetime μ) = 12 * L.price μ ⟨0, hA⟩ ∧ Real.log ((chain (torus 2 0 2) sdens.dens).lifetime μ) < 1.9228 * 12 ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus 2 0 2) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus 2 0 2) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (torus 2 0 2) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorem 2: one price per cell on a rotation-invariant torus) for the 12-cell torus (2,0),(0,2).
- **Difference:** For Gump.Dice.Face.P at (0.44, 0.42): unique QSD among λ > 0, positive on every living state, all twelve prices equal, ln τ = 12·c, ln τ < 1.9228·12 (the dice agent's lntau_le_regular), the decay rate from every start. No certified interval for λ (the dice agent's 12-cell certificate was not built); the tables are mine, checked by Data.tabOK against Face.nb.

### `survFrom_cast` (`mathlib/GumpMath/LinkSurv.lean`)

```lean
theorem survFrom_cast (F : Face) {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (h : Absorbing F ρ1 ρ2) : ∀ t (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}), (chain F hd).survFrom t x = ((F.survival ρ1 ρ2 t x : ℚ) : ℝ)
```

- **Meant to be:** (the question whether the chain's decay clause and the dice agent's hull3_lifetime are about one object) the chain's P_x(T > t) is Face.survival.
- **Difference:** Equal as functions, cast ℚ → ℝ, for every face whose empty state is absorbing (Absorbing): every hull face (absorbing_hull, from the dice agent's hull_P_empty_row) and every face with all its coins (absorbing_of_coins, from P_empty_row); also Face.survival t ∅ = 0 there.

### `hull3_complete` (`mathlib/GumpMath/LinkSurv.lean`)

```lean
theorem hull3_complete : ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧ 2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧ Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧ (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧ (∀ i j : Fin (hull 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧ (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (hull 3) sdens.dens).survFrom t x = (((hull 3).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧ (∀ t, (hull 3).survival ρ1 ρ2 t (hull 3).empty = 0) ∧ (∀ t, (0.72 : ℝ) * 0.9165673655948901373 ^ t ≤ (chain (hull 3) sdens.dens).survFrom t full') ∧ (∀ t x, (chain (hull 3) sdens.dens).survFrom t x ≤ 1384 * (0.9165673655948901374 : ℝ) ^ t)
```

- **Meant to be:** rigour/README.md claim 3 for the face (hull 3), with the dice agent's explicit decay constants.
- **Difference:** Everything in hull3_full, and: survFrom = Face.survival; 0.72·λ₋^t ≤ P_full(T > t) and P_x(T > t) ≤ 1384·λ₊^t for every living x and every t (from hull3_lifetime), λ₋ = 0.9165673655948901373 ≤ λ ≤ λ₊ = …374 in the same theorem.

### `Q_eq` (`mathlib/GumpMath/LinkWrappedFull.lean`)

```lean
theorem Q_eq (x y : {x : Fin (2 ^ (torus H K D).A) // x ≠ (torus H K D).empty}) : (ker H K D hs).toSubsetChain.killed.Q (stateEquiv (torus H K D) (cellEquiv H K D hH hD hnb.1) x) (stateEquiv (torus H K D) (cellEquiv H K D hH hD hnb.1) y) = (chain (torus H K D) hs.dens).Q x y
```

- **Meant to be:** (the bijection, consequence) on a wrapped face Face.P is the chain arm's kagome kernel over Torus H K D.
- **Difference:** Entry by entry along the relabelling stateEquiv (live cells ↔ a subset of Orient × Torus H K D via cellEquiv, cell 3(aD+b)+o ↦ (o, (a,b))), at every 0 < ρ1, ρ2 < 1, under TorusNb H K D.

### `wrapped_full` (`mathlib/GumpMath/LinkWrappedFull.lean`)

```lean
theorem wrapped_full (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (hnb : TorusNb H K D) : ∃ μ lam, (chain (torus H K D) Hull3.sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus H K D) ρ1 ρ2 (extend (torus H K D) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus H K D) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (LT H K D Hull3.sdens).dc i x = 1 - (((torus H K D).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) = ∑ i, (LT H K D Hull3.sdens).price μ i ∧ (∀ i j : Fin (torus H K D).A, (i : ℕ) % 3 = (j : ℕ) % 3 → (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j) ∧ Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) < 1.9228 * (torus H K D).A ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus H K D) Hull3.sdens.dens).survFrom t x) ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom t x = (((torus H K D).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧ (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D → ∀ i j, (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j)
```

- **Meant to be:** Lemma 0, Theorems 1 and 2 on a wrapped face, for Face.P itself, under the hypothesis TorusNb.
- **Difference:** The hypothesis form (kept: wrapped_full_all supplies TorusNb). At (ρ1, ρ2) = (0.44, 0.42).

### `torusNb_all` (`mathlib/GumpMath/LinkWrappedAll.lean`)

```lean
theorem torusNb_all (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) : TorusNb H K D
```

- **Meant to be:** (the general bijection) the dice agent's torus H K D cell list is Orient × Torus H K D, Face.nb carried to Kagome.nbrs.
- **Difference:** For every H, D > 0 and every K: 3HD cells, and nb i is a permutation of kIdx i, whose image under phi is exactly Kagome.nbrs (phi i) (kIdx_map). Also kernel-checked (decide +kernel) on ten tori, torusNb_1_0_1 … torusNb_3_0_3, independently of the general proof.

### `wrapped_theorems_all` (`mathlib/GumpMath/LinkWrappedAll.lean`)

```lean
theorem wrapped_theorems_all (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) : ∃ μ lam, (chain (torus H K D) hs.dens).IsDominantQSD μ lam ∧ IsQSD (torus H K D) ρ1 ρ2 (extend (torus H K D) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus H K D) hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (LT H K D hs).dc i x = 1 - (((torus H K D).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus H K D) hs.dens).lifetime μ) = ∑ i, (LT H K D hs).price μ i ∧ (∀ i j : Fin (torus H K D).A, (i : ℕ) % 3 = (j : ℕ) % 3 → (LT H K D hs).price μ i = (LT H K D hs).price μ j) ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus H K D) hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus H K D) hs.dens).survFrom t x) ∧ (∀ t x, (chain (torus H K D) hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (torus H K D) hs.dens).survFrom t x = (((torus H K D).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧ (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D → ∀ i j, (LT H K D hs).price μ i = (LT H K D hs).price μ j)
```

- **Meant to be:** Lemma 0, Theorems 1 and 2 on every wrapped face, for Face.P itself, every strict density.
- **Difference:** For every H, D > 0, K, and 0 < ρ1, ρ2 < 1: a dominant QSD (also the dice agent's IsQSD), λ > 0, μ > 0 on every living state, unique among λ > 0; ln τ = Σ_i c_i (c_i the price of cell i's own death probability); c_i = c_j when i ≡ j mod 3 (one price per orientation); one price per cell when (K, −H−K), (D, −D) are periods; decay at exactly λ from every state that can survive (constants m/M, M/m); survFrom = Face.survival. No hypothesis.

### `wrapped_full_all` (`mathlib/GumpMath/LinkWrappedAll.lean`)

```lean
theorem wrapped_full_all (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) : ∃ μ lam, (chain (torus H K D) Hull3.sdens.dens).IsDominantQSD μ lam ∧ IsQSD (torus H K D) ρ1 ρ2 (extend (torus H K D) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (torus H K D) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (LT H K D Hull3.sdens).dc i x = 1 - (((torus H K D).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) = ∑ i, (LT H K D Hull3.sdens).price μ i ∧ (∀ i j : Fin (torus H K D).A, (i : ℕ) % 3 = (j : ℕ) % 3 → (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j) ∧ Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) < 1.9228 * (torus H K D).A ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (torus H K D) Hull3.sdens.dens).survFrom t x) ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom t x = (((torus H K D).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧ (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D → ∀ i j, (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j)
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) on every wrapped face, with the sharpened Theorem 1.
- **Difference:** wrapped_theorems_all at (ρ1, ρ2) = (0.44, 0.42), and ln τ < 1.9228·A (the dice agent's lntau_le_torus, every wrapped face). No hypothesis. Not stated: a value of λ on any torus beyond the certified ones.

### `wrapped_area` (`mathlib/GumpMath/LinkWrappedArea.lean`)

```lean
theorem wrapped_area (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (μ : {x : Fin (2 ^ (torus H K D).A) // x ≠ (torus H K D).empty} → ℝ) (lam : ℝ) (hμ : (chain (torus H K D) hs.dens).IsQSD μ lam) (hlam : 0 < lam) : Real.log ((chain (torus H K D) hs.dens).lifetime μ) = (H : ℝ) * D * ((LT H K D hs).price μ (c3 H K D hH hD 0 (by norm_num)) + (LT H K D hs).price μ (c3 H K D hH hD 1 (by norm_num)) + (LT H K D hs).price μ (c3 H K D hH hD 2 (by norm_num))) ∧ (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D → Real.log ((chain (torus H K D) hs.dens).lifetime μ) = (torus H K D).A * (LT H K D hs).price μ (c3 H K D hH hD 0 (by norm_num)))
```

- **Meant to be:** Theorem 2 on the wrapped faces in area form: ln τ = H·D·(c_X + c_Y + c_Z), and ln τ = A·c on a rotation-invariant torus.
- **Difference:** For Face.P on torus H K D, every H, D > 0, K, 0 < ρ1, ρ2 < 1, every QSD with λ > 0 (it is the unique one): c_o is the price of cell o < 3 (orientation o at the origin); the second form when (K, −H−K) and (D, −D) are periods, A = 3HD. No hypothesis.

### `cellsOK_hull` (`mathlib/GumpMath/LinkHull.lean`)

```lean
theorem cellsOK_hull (R : ℕ) : CellsOK (Gump.Dice.hull R)
```

- **Meant to be:** (the PI's fourth task, step 1) every hull face has its coins: (2,1), or (2,0) with at most two neighbours.
- **Difference:** For every R, from the dice agent's hull_type (the three cell types (6,2,1), (4,2,1), (2,2,0)). No hypothesis.

### `hull_theorems` (`mathlib/GumpMath/LinkHull.lean`)

```lean
theorem hull_theorems (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) : ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧ IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧ (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x = (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ))
```

- **Meant to be:** THEOREMS.md, Theorems 1 and 2, on every hull face for Face.P itself.
- **Difference:** For every R with A > 0, at (0.44, 0.42): the dominant QSD (also the dice agent's IsQSD), the tilt identity ln τ = Σ c_i with c_i the price of cell i's own death probability, ln τ < 2.2165·A (the dice agent's lntau_le_hull_all), survFrom = Face.survival. No hypothesis. hull_theorems_at: the same at every 0 < ρ1, ρ2 < 1 without the bound.

### `face_full_of` (`mathlib/GumpMath/LinkHull.lean`)

```lean
theorem face_full_of (hc : CellsOK F) (hA : 0 < F.A) (h0 : Lemma0F F) : ∃ μ lam, (chain F hs.dens).IsDominantQSD μ lam ∧ IsQSD F ρ1 ρ2 (extend F μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (localDeath F hs hc).dc i x = 1 - ((F.a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain F hs.dens).lifetime μ) = ∑ i, (localDeath F hs hc).price μ i ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain F hs.dens).CanSurvive x → m / M * lam ^ t ≤ (chain F hs.dens).survFrom t x) ∧ (∀ t x, (chain F hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

- **Meant to be:** THEOREMS.md, Lemma 0 and its consequences, from Lemma 0 stated combinatorially.
- **Difference:** For every face with CellsOK and A > 0 and every 0 < ρ1, ρ2 < 1: Lemma0F F (a living u from which every cell can be alive next, reached by possible transitions from every living state some cell of which can be alive next; density-free) gives uniqueness among λ > 0, μ > 0 on every living state, decay at exactly λ from every state that can survive.

### `hull_full_all` (`mathlib/GumpMath/LinkHull.lean`)

```lean
theorem hull_full_all (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) (h0 : Lemma0F (Gump.Dice.hull R)) : ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧ IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x) ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x = (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ))
```

- **Meant to be:** rigour/README.md claim 3 and THEOREMS.md (Lemma 0, Theorems 1, 2) on every hull face, under the single named hypothesis Lemma0F (hull R).
- **Difference:** At (0.44, 0.42), every R with A > 0: unique law among λ > 0, positive on every living state, ln τ = Σ c_i, ln τ < 2.2165·A, decay at exactly λ, survFrom = Face.survival. Lemma0F (hull R) is proved by the kernel for R = 1, 3, …, 13 (hull<R>_lemma0, LinkHullCert*.lean) and not for general R.

### `lemma0_of_cert` (`mathlib/GumpMath/LinkHull.lean`)

```lean
theorem lemma0_of_cert (u c0 : ℕ) (common : List ℕ) (walks : List (List ℕ)) (h : certOK F u c0 common walks = true) : Lemma0F F
```

- **Meant to be:** (the hypothesis from a certificate) Lemma0F from a polynomial-size certificate.
- **Difference:** certOK F u c0 common walks: every cell can be alive next from u, a path of possible transitions from {c0} to u, and from every {i} to {c0}; any face.

### `price_aut` (`mathlib/GumpMath/LinkFaceAut.lean`)

```lean
theorem price_aut {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F) {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ} {lam : ℝ} (hμ : (chain F hs.dens).IsQSD μ lam) (hlam : 0 < lam) (huniq : ∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) (i : Fin F.A) : (localDeath F hs hc).price μ (autPerm hπ i) = (localDeath F hs hc).price μ i
```

- **Meant to be:** THEOREMS.md, Theorem 2: equal prices for cells exchanged by a symmetry, for any automorphism of a face's tables.
- **Difference:** For every face with CellsOK, every π with autOK F π (π permutes the cells, carries each neighbour list to that of the image up to order, keeps m1 and m2; a Boolean), and the QSD unique among λ > 0: c_{π i} = c_i.

### `hull_full_sym` (`mathlib/GumpMath/LinkFaceAut.lean`)

```lean
theorem hull_full_sym (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) (h0 : Lemma0F (Gump.Dice.hull R)) : ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧ IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧ (∀ ν lam', (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧ (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧ Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧ (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).CanSurvive x → m / M * lam ^ t ≤ (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x) ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧ (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x = (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧ (∀ (π : List ℕ) (hπ : autOK (Gump.Dice.hull R) π = true) (i : Fin (Gump.Dice.hull R).A), (LH R Hull3.sdens).price μ (autPerm hπ i) = (LH R Hull3.sdens).price μ i)
```

- **Meant to be:** rigour/README.md claim 3 on every hull face with the prices equal along the triangle's symmetries, under Lemma0F (hull R).
- **Difference:** hull_full_all plus c_{π i} = c_i for every autOK automorphism π of hull R; the rotation (x,y,z) ↦ (y,z,x) and the reflection (x,y,z) ↦ (y,x,z) are kernel-checked automorphisms for R = 3, …, 13 (hull<R>_rot, hull<R>_refl), not for general R.

## The catalogue's "for every N" laws: the tape, the gun's line, the rake train's signals (tape files)

### `tape_run` (`Gump/Tape.lean`)

```lean
theorem tape_run (w : Int → Letter) (n : Nat) : run (tape w) (2 * n) = tape (fun u => w (u + n))
```

- **Meant to be:** `research/signals/README.md` §10, the tape: every pattern made of B units and C units moves towards −v at one unit per 2 generations; every infinite sequence over {B, C} is an exact solution moving at one unit per 2 generations (reviewed in `research/audit/REVIEW-signals-2.md` row 5; part A of `REVIEW-signals-9.md` §3 for wire B, the same letters `7`, `b`).
- **Difference:** Same, on the whole lattice, for every word w : ℤ → {B, C} (finite, one-sided and two-sided words alike). Stated at even generations; nothing is said about the odd ones (the source needs nothing there either).

### `tape_local_run` (`Gump/Tape.lean`)

```lean
theorem tape_local_run (w : Int → Letter) (a b : Int) : ∀ (n : Nat) (c : Config), (∀ q, a - 2 * n ≤ unitOf q → unitOf q ≤ b + 2 * n → c q = tape w q) → ∀ p, a ≤ unitOf p → unitOf p ≤ b → run c (2 * n) p = tape (fun u => w (u + n)) p
```

- **Meant to be:** The form the gluing arguments use (`REVIEW-signals-9.md` §3, W(k) 'by A both continue for ever'): what lies on a stretch of tape determines the stretch 2n generations later.
- **Difference:** Stronger than the source states: any configuration that is the tape of w on the units a − 2n .. b + 2n is, 2n generations later, the tape of the shifted word on a .. b, whatever lies outside.

### `line_orbit` (`Gump/Line.lean`)

```lean
theorem line_orbit (N : Nat) (hN : 2 ≤ N) (s p : Nat) (hp : 0 < p) : run (lineC N) (s + p) = run (lineC N) s ↔ 2 * N ≤ s ∧ p % 4 = 0
```

- **Meant to be:** §21: the line (capA + N units of bare wire C + the gun) has period exactly 4 from generation 2N on for every N ≥ 2; `verify_line.py` (D): and not from generation 2N − 1 (measured there for N = 2, 3, 12, 13, 30).
- **Difference:** Stronger: for every N ≥ 2 the state at s returns after p > 0 generations iff s ≥ 2N and 4 ∣ p, so the preperiod is exactly 2N for every N (the source proves period 4 from 2N by induction and measures the 2N − 1 clause). Object in the coordinates of `objects/line-C.json`; base runs S(4,1), N = 2, 3 by the kernel.

### `line_period_four` (`Gump/Line.lean`)

```lean
theorem line_period_four (N : Nat) (hN : 2 ≤ N) : run (lineC N) (2 * N + 4) = run (lineC N) (2 * N) ∧ (∀ k, 0 < k → k < 4 → run (lineC N) (2 * N + k) ≠ run (lineC N) (2 * N)) ∧ run (lineC N) (2 * N - 1 + 4) ≠ run (lineC N) (2 * N - 1)
```

- **Meant to be:** §21 in the form of `Gump.Signals.lineC_2_period_four`, `lineC_3_period_four`, `lineC_12_period_four`, `lineC_13_period_four` (N = 2, 3, 12, 13).
- **Difference:** Same as `line_orbit`, specialised: period 4 from 2N, no smaller, not from 2N − 1.

### `S_succ` (`Gump/Line.lean`)

```lean
theorem S_succ {N : Nat} {m : Int} (h : S N m) : S (N + 1) (m + 1) ∧ ∀ t, X (N + 1) t = glue m (L N t) (shiftC 1 (X N t))
```

- **Meant to be:** `research/signals/prove_line.py`'s induction S(N, m) → S(N+1, m+1): Y(t) = L_N(t) on units ≤ m and τX_N(t) on units > m is X_{N+1}.
- **Difference:** Same argument; the witness of 'not period 2' is carried at a unit > m and that of 'not from 2N − 1' at a unit ≤ m + 1, which the source does not need.

### `train_step` (`Gump/TapeSignals.lean`)

```lean
theorem train_step (t : Nat) : step (train t) = train (t + 1)
```

- **Meant to be:** §30, `echo6.check_train`: the plain rake train (rake5 on even units, rakef on odd at generation 0) is an orbit and moves one unit towards −v every 2 generations.
- **Difference:** Same, on the whole lattice (the train infinite along the wire); `train_shift` is the motion.

### `signal_run` (`Gump/TapeSignals.lean`)

```lean
theorem signal_run (K : Kind) (u : Int) (hu : u % 2 = K.par % 2) (n : Nat) : run (xorC (train 1) (lcfg (sig K u))) (2 * n) = xorC (train (1 + 2 * n)) (lcfg (sig K (u + K.dir * n)))
```

- **Meant to be:** §30 and `prove_echo.py` (E, U, H, K0), `REVIEW-signals-6.md` §2 and `research/audit/signals6/sig6.py` (K3, N1, N2, N3, N4): each of the nine signals rides the infinite train for ever, rigidly, one unit per 2 generations.
- **Difference:** Same, for every lowest unit of the kind's parity and every n: run (train 1 ⊕ sig K u) (2n) = train (1 + 2n) ⊕ sig K (u + dir·n). That these are all the train's signals is not claimed (nor by the source).

### `glue_run` (`Gump/TapeBase.lean`)

```lean
theorem glue_run (m : Int) (X Z : Nat → Config) (hX : ∀ t p, unitOf p ≤ m → step (X t) p = X (t + 1) p) (hZ : ∀ t p, m + 1 ≤ unitOf p → step (Z t) p = Z (t + 1) p) (hXZ : ∀ t p, m ≤ unitOf p → unitOf p ≤ m + 1 → X t p = Z t p) : ∀ t, run (glue m (X 0) (Z 0)) t = glue m (X t) (Z t)
```

- **Meant to be:** The gluing step of §11, §21, push 8 and `REVIEW-signals-9.md` §3: two orbits that agree on the units m, m + 1, one obeying the rule on units ≤ m and the other on units > m, glue to an orbit.
- **Difference:** Same, with a fixed seam; the moving seam is `glue_run_moving` (its own row).

### `orbit_classify` (`Gump/TapeBase.lean`)

```lean
theorem orbit_classify (c : Config) (μ : Nat) (hμ : 1 ≤ μ) (h4 : run c (μ + 4) = run c μ) (h2 : run c (μ + 2) ≠ run c μ) (ht : run c (μ + 3) ≠ run c (μ - 1)) : ∀ s p, 0 < p → (run c (s + p) = run c s ↔ μ ≤ s ∧ p % 4 = 0)
```

- **Meant to be:** (the meaning of 'period exactly 4 from generation μ, and not from μ − 1')
- **Difference:** A general lemma: the three facts X(μ+4) = X(μ), X(μ+2) ≠ X(μ), X(μ+3) ≠ X(μ−1) give: X(s+p) = X(s) iff s ≥ μ and 4 ∣ p.

### `clock_every_length` (`Gump/Clock.lean`)

```lean
theorem clock_every_length (N : Nat) (hN : 1 ≤ N) : ∃ c : Config, run c (4 * N + 2) = c ∧ (∀ k, 0 < k → k < 4 * N + 2 → run c k ≠ c) ∧ ∀ q, c q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧ -64 ≤ q.x + q.z ∧ q.x + q.z < 64
```

- **Meant to be:** §11: a clock of period exactly 4N + 2 exists for every N ≥ 1 (`prove_clock.py`; REVIEW-signals-2 row 1).
- **Difference:** **Less than the claim**: an existential that does not name the clock (referee ref-tape D1: the lit clocks of 1 and 2 units side by side satisfy it for N = 7). The theorem that names the object is `clockOf_period`. Kept unchanged.

### `clock_cycle` (`Gump/Clock.lean`)

```lean
theorem clock_cycle (j : Nat) : run (clockY j) (4 * (6 + j) + 2) = clockY j ∧ (∀ k, 0 < k → k < 4 * (6 + j) + 2 → run (clockY j) k ≠ clockY j) ∧ ∀ q, clockY j q = true → -4 ≤ unitOf q ∧ unitOf q ≤ (6 + j : Nat) + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧ -64 ≤ q.x + q.z ∧ q.x + q.z < 64
```

- **Meant to be:** §11's surgery: the base cycle (here the clock of 6 units, period 26) cut at unit m with j units inserted is an orbit of period exactly p + 4j.
- **Difference:** Same; the chart arithmetic (A), (B) is proved for every j, i, t by omega (the source enumerated j ≤ 40); base N0 = 6 instead of 8 or 12.

### `lit_clock_small` (`Gump/Clock.lean`)

```lean
theorem lit_clock_small (N : Nat) (h1 : 1 ≤ N) (h5 : N ≤ 5) : run (run (lcfg (litList N)) (N - 2)) (4 * N + 2) = run (lcfg (litList N)) (N - 2) ∧ ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) (N - 2)) k ≠ run (lcfg (litList N)) (N - 2)
```

- **Meant to be:** §11, `verify_clock.py`: the lit clock (one added cell) has period 4N + 2; REVIEW-signals-2: it enters its cycle after max(N − 2, 0) generations.
- **Difference:** N = 1 .. 5 only: from generation max(N − 2, 0) an oscillator of exact period 4N + 2 (that it is not periodic earlier is not claimed).

### `unzip_law_sharp` (`Gump/UnzipProof.lean`)

```lean
theorem unzip_law_sharp : UnzipLawSharp
```

- **Meant to be:** push 8 §5 and `prove_unzip8.py`: the count read leaves exactly k pulses two units apart for every k; REVIEW-signals-8 §3: final from generation 2k + 6, not at 2k + 4.
- **Difference:** Same, on the whole lattice with the infinite store wire, the stretch's first unit at 0. `UnzipLawSharp` is a definition in `Gump/Unzip.lean`: ∀ k ≥ 1, (∀ n ≥ k + 3, run (countRead k) (2n) = tape (pulses k (2 − n))) ∧ run (countRead k) (2(k + 2)) ≠ tape (pulses k (2 − (k + 2))). Proved by an induction on time (the front `f 9`), not by the source's seam argument.

### `unzip_law` (`Gump/UnzipProof.lean`)

```lean
theorem unzip_law : UnzipLaw
```

- **Meant to be:** push 8 §5 as the push states it: from generation 4k + 8 on.
- **Difference:** Same (`UnzipLaw` in `Gump/Unzip.lean`: ∀ k ≥ 1, ∀ n ≥ 2k + 4, run (countRead k) (2n) = tape (pulses k (2 − n))); a corollary of `unzip_law_sharp`.

### `stretch_stands` (`Gump/Unzip.lean`)

```lean
theorem stretch_stands (k : Nat) (hk : 1 ≤ k) : ∀ n : Nat, run (store k) (2 * n) = store k
```

- **Meant to be:** push 8 §6: the memory cell holding k stands (period 2); here its infinite-wire form, wire B with d^k f.
- **Difference:** For the infinite wire, every k ≥ 1; the finite cell with its two caps is not covered.

### `glue_run_moving` (`Gump/Unzip.lean`)

```lean
theorem glue_run_moving (m : Nat → Int) (A Z : Nat → Config) (hm : ∀ t, m (t + 1) ≤ m t + 1 ∧ m t ≤ m (t + 1) + 1) (hA : ∀ t p, unitOf p ≤ m t → step (A t) p = A (t + 1) p) (hZ : ∀ t p, m t < unitOf p → step (Z t) p = Z (t + 1) p) (hAZ : ∀ t p, m t - 1 ≤ unitOf p → unitOf p ≤ m t + 1 → A t p = Z t p) : ∀ t, run (glue (m 0) (A 0) (Z 0)) t = glue (m t) (A t) (Z t)
```

- **Meant to be:** push 8's and the call law's gluing step: a seam that moves at most one unit per generation, with agreement on three units.
- **Difference:** Same; proved, not used by the unzip proof here.

### `call_law_b` (`Gump/CallProof.lean`)

```lean
theorem call_law_b (k : Nat) (hk : 1 ≤ k) (n : Nat) (hn : k + 17 ≤ n) : V k (2 * n) = tape (pulses k (cross + 3 - ((n : Int) - 14)))
```

- **Meant to be:** `research/audit/REVIEW-signals-9.md` §3 (b) and P1 of its proof (`proof9.py` parts D, E): for every k ≥ 1, at every even t ≥ 2k + 34, V_k(t) (the store wire alone, e1 = (1,2,0) of the crossing unit made live at generation 29) is plain wire B carrying exactly k units b at units c + 3 − (t − 28)/2 + 2j, j < k.
- **Difference:** Same, on the whole lattice with the infinite store wire, c = 35 as in call9.json; the second conjunct of `Gump.Call.CallLaw`. Proved by the time induction of the unzip law (front `f b 9`), not by the review's seam path. Part (a) of the call law (X_k = V_k ⊔ Lf) is not proved.

### `clockOf_period` (`Gump/Clock.lean`)

```lean
theorem clockOf_period (N : Nat) (hN : 1 ≤ N) : run (clockOf N) (4 * N + 2) = clockOf N ∧ (∀ k, 0 < k → k < 4 * N + 2 → run (clockOf N) k ≠ clockOf N) ∧ ∀ q, clockOf N q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧ -64 ≤ q.x + q.z ∧ q.x + q.z < 64
```

- **Meant to be:** §11: a clock of period exactly 4N + 2 for every N ≥ 1, as a named object.
- **Difference:** `clockOf N` is the lit clock (capL + N units + capR + one cell) at generation max(N − 2, 0) for N ≤ 5, and the surgery's cycle `clockY (N − 6)` for N ≥ 6: exact period 4N + 2, support in units −4 .. N + 3. That `clockY j` is a state of the lit clock of 6 + j units is not proved (measured by the referee for j ≤ 6).

### `line_rest` (`Gump/CallLine.lean`)

```lean
theorem line_rest : LineRest
```

- **Meant to be:** `REVIEW-signals-9.md` §3 and `proof9.py` part B: the free call line (with the CALL) is at rest from generation 42.
- **Difference:** Same: `Lf (2n) = lcfg line` for n ≥ 21 (`LineRest`), by the kernel on the 128 × 128 × 16 box of `Gump/CallBox.lean`, whose stepper `Gump.Call.Box.bstep_spec` is proved equal to `Gump.step`.

### `call_law_a` (`Gump/CallUnionLocal.lean`)

```lean
theorem call_law_a (k : Nat) (hk : 1 ≤ k) : ∀ t, run (callStart k) t = fun p => V k t p || Lf t p
```

- **Meant to be:** `REVIEW-signals-9.md` §3 (a): X_k(t) = V_k(t) ⊔ Lf(t) at every generation, for every k ≥ 1.
- **Difference:** Same (disjointness in `V_Lf_disjoint`): supports by `confinement`/`hull`, the union law off the 44-cell interaction set by `step_or`, and at it by kernel checks at every generation (store, start, `VW` words, all 256 tape words for t ≥ 44).

### `call_law` (`Gump/CallUnionLocal.lean`)

```lean
theorem call_law : CallLaw
```

- **Meant to be:** `REVIEW-signals-9.md` §3, the whole call law: (a) and (b) for every k ≥ 1.
- **Difference:** Same: `CallLaw` (Gump/Call.lean) proved. The review's "what is left" (ii)–(iv) (the finite cell, other seed places, "at no earlier generation") are not covered.

### `X0_lit` (`Gump/Clock.lean`)

```lean
theorem X0_lit : run (lcfg (litList 6)) 41 = lcfg X0
```

- **Meant to be:** (referee ref-tape's observation) the surgery's base X0 is a state of the catalogue's lit clock.
- **Difference:** Same: the lit clock of six units at generation 41 is X0, so `clockY 0` is its state at generation 53 (`clockY_zero_lit`). For j ≥ 1 that `clockY j` is a state of the lit clock of 6 + j units is not proved.

### `lit_word` (`Gump/ClockLit.lean`)

```lean
theorem lit_word (N : Nat) (h6 : 6 ≤ N) : ∀ m, m ≤ mmax N → run (lcfg (litList N)) (2 * m) = ucfg (FL N m)
```

- **Meant to be:** (PI's brief, third task) the lit clock's transient as a word family for every N: from one cell the rake f runs from unit N/2 towards capR, shedding units of wire B (pulses p<) behind it.
- **Difference:** Same, for every N ≥ 6: at generation 2m (m ≤ mmax N = ⌈N/2⌉ − 1) the lit clock is `FL N m`: f at N/2 + m, wire B at N/2 − m + 2i (i < m), wire C elsewhere, caps untouched. Checked on the oracle for N = 6 .. 30 by `tape_lit.py`; proved by local double steps (tape windows, three zone families, `zonesLit_ok`) for N ≥ 16 and by whole-clock kernel steps (`smallOK_ok`) for 6 ≤ N ≤ 15.

### `lit_enters` (`Gump/ClockLit.lean`)

```lean
theorem lit_enters (N : Nat) (h6 : 6 ≤ N) : run (lcfg (litList N)) (2 * mmax N) = run (clockOf N) (2 * (N - 6) + 3)
```

- **Meant to be:** §11 and the owner's journal (2026-11-15, 10:30): one cell lights the clock of N units into the cycle `clockOf N`; matched at generation N − 2 with `clockY (N − 6)`.
- **Difference:** For even N: at generation N − 2 exactly (2 · mmax N = N − 2), the state of `clockOf N` at generation 2(N − 6) + 3, i.e. `Y_{N−6}` at surgery time 2(N − 6) + 8 (`FL_entry`). For odd N this theorem matches at N − 1 (2 · mmax N = N − 1); the match at N − 2 is `lit_odd_entry` (ClockLitOdd), and the whole claim with "at no earlier generation" is `lit_enters_at`.

### `lit_clock` (`Gump/ClockLit.lean`)

```lean
theorem lit_clock (N : Nat) (hN : 1 ≤ N) (g : Nat) (hg : litEntry N ≤ g) : (∃ s, run (lcfg (litList N)) g = run (clockOf N) s) ∧ run (run (lcfg (litList N)) g) (4 * N + 2) = run (lcfg (litList N)) g ∧ ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) g) k ≠ run (lcfg (litList N)) g
```

- **Meant to be:** §11, `verify_clock.py`: the clock lit by one cell is an oscillator of period exactly 4N + 2, for every N ≥ 1.
- **Difference:** Same, for every N ≥ 1: from generation `litEntry N` (max(N − 2, 0) for N ≤ 5; N − 2 for even, N − 1 for odd N ≥ 6) every state of the lit clock is a state of the cycle of `clockOf N` and has exact period 4N + 2. With `lit_enters` this makes the journal's 4N + 2 clock a theorem from a single cell.

### `beam_period` (`Gump/LineBeam.lean`)

```lean
theorem beam_period (N : Nat) (hN : 1 ≤ N) : run (beam N) 4 = beam N ∧ ∀ k, 0 < k → k < 4 → run (beam N) k ≠ beam N
```

- **Meant to be:** §21, `prove_beam.py`: the beam (the mirror-image gun, N units of rake train, the SAT absorber of C = 31; `objects/beam-5f.json`) has period exactly 4 for every N ≥ 1.
- **Difference:** Same, for every N ≥ 1 (period 4, and no smaller period). The object is given unit by unit (`beamU`, `Gump/LineBeamData.lean` from `tape_beam.py`, which checks that it reassembles to the catalogue's Object(N) for N = 1 .. 30). Proved by the source's induction N → N + 2 (`S_step`, the gluing by `glue_run`) from kernel bases S 8, S 9, and N = 1 .. 9 directly. Not covered: the cell count 33 + 5N, the hull, the stream's one-cell pulses (the hole).

### `reader_run` (`Gump/ClockReader.lean`)

```lean
theorem reader_run (w : Int → Letter) : ∀ n : Nat, run (readerC w) (2 * n) = readerC (fun u => w (u + n))
```

- **Meant to be:** §15, `prove_reader.py`: capL of the clock eats every word of the B/C tape and remembers nothing: at every even generation, for every word, the state is capL and the tape moved on, cell for cell.
- **Difference:** Same, for every word w (any function from units to {B, C}; its letters on the units ≥ 0 are on the tape): `readerC w` (capL on the units < 0, `tape w` on the units ≥ 0) is at generation 2n `readerC` of w moved n units. One double step (`reader_step`) is tape windows on the units ≥ 2 and one kernel check per word on the units 0 .. 3 (`readerOK_ok`, the source's 16 closed states). The source's `--U 4` variant and other caps in the census (`readers.py`) are not covered.

### `reader9_run` (`Gump/CallReader.lean`)

```lean
theorem reader9_run (w : Int → Letter) (n : Nat) : run (readerCall w) (2 * n) = readerCall (fun u => w (u + n))
```

- **Meant to be:** `REVIEW-signals-9.md` §3, what is left (ii): whether the third push's reader theorem covers the call line's left cap (`call9.json` `capL`; that the cap takes a train of any length is measured to k = 40).
- **Difference:** Covered, by a new theorem: call9's capL (18 cells, not the clock's capL) eats every word too: capL9 on the units < 4 and any word on the units ≥ 4 is at generation 2n capL9 and the word moved n units (`readerCall`). Proved by `reader_run_gen` (`ClockReader`'s proof written for any cap passing 16 zone checks), `cap9OK_ok`. This is the cap at the end of a bare store wire: the finite cell of the call law (the cap during the call, with the call line across the cell) is not covered.

### `lit_enters_exact` (`Gump/ClockLitFirst.lean`)

```lean
theorem lit_enters_exact (N : Nat) (h6 : 6 ≤ N) (he : N % 2 = 0) : (∃ s, run (lcfg (litList N)) (N - 2) = run (clockOf N) s) ∧ ∀ g, g < N - 2 → ∀ k, run (lcfg (litList N)) g ≠ run (clockOf N) k
```

- **Meant to be:** (PI's brief, third task) the lit clock enters the cycle of `clockOf N` at generation N − 2, "at no earlier generation" if true.
- **Difference:** For even N ≥ 6: on the cycle at generation N − 2 and at no earlier generation (`lit_first_even`: no state before N − 2 is any state of the cycle; the witness is the left end at generation N − 3, one kernel-checked cell per base time).

### `lit_first` (`Gump/ClockLitFirst.lean`)

```lean
theorem lit_first (N : Nat) (h6 : 6 ≤ N) (g : Nat) (hg : g < N - 2) (k : Nat) : run (lcfg (litList N)) g ≠ run (clockOf N) k
```

- **Meant to be:** (PI's brief, third task) "at no earlier generation": the lit clock of N units is on no state of the cycle of `clockOf N` before generation N − 2.
- **Difference:** Same, for every N ≥ 6: even N by the left end at N − 3 (`lit_first_even`), odd N by the right end at N − 3 (`lit_first_odd`: C, f, C, capR is the right end of no base state; the left end would not do, it is that of the base at times 4, 8, 12, 16 in Lean's `Xb` convention, i.e. generations 11, 15, 19, 23 counted from X0, `Xb_nat`; ref-tape third review). With `lit_enters_at` the entry is exactly N − 2 for every N ≥ 6.

### `lit_enters_at` (`Gump/ClockLitOdd.lean`)

```lean
theorem lit_enters_at (N : Nat) (h6 : 6 ≤ N) : (∃ s, run (lcfg (litList N)) (N - 2) = run (clockOf N) s) ∧ ∀ g, g < N - 2 → ∀ k, run (lcfg (litList N)) g ≠ run (clockOf N) k
```

- **Meant to be:** (PI's brief, third task) one cell lights the clock of N units into the cycle `clockOf N`, matched at generation N − 2 with `clockY (N − 6)`, at no earlier generation; the owner's journal (2026-11-15, 10:30) on the 4N + 2 clock as a theorem from a single cell.
- **Difference:** Same, for every N ≥ 6: the state at N − 2 is a state of the cycle (even N: `clockY (N − 6)` at generation 2(N − 6) + 3, `lit_enters`; odd N: at 2(N − 6) + 2, `lit_odd_entry`, three local one-generation kernel checks against base times 7, 9, 11), and no earlier state is (`lit_first`). `lit_clock_exact`: from N − 2 on, exact period 4N + 2. N ≤ 5: `lit_clock_small` (from max(N − 2, 0); minimality there not claimed).

### `divider_period` (`Gump/LineDivider.lean`)

```lean
theorem divider_period (N : Nat) (hN : 8 ≤ N) : run (divC N) (2 * N - 3 + 8) = run (divC N) (2 * N - 3) ∧ (∀ k, 0 < k → k < 8 → run (divC N) (2 * N - 3 + k) ≠ run (divC N) (2 * N - 3)) ∧ run (divC N) (2 * N - 4 + 8) ≠ run (divC N) (2 * N - 4)
```

- **Meant to be:** §21b, `prove_divider.py`: the divider (line-C(N) and the oscillator `osc` of `objects/divider-C8.json`) has period exactly 8 from generation 2N − 3 for every N ≥ 8.
- **Difference:** Same, for every N ≥ 8: the state at 2N − 3 returns after 8 generations and after no fewer, and the state at 2N − 4 does not return after 8 (so it is on no cycle: the preperiod is exactly 2N − 3). Proved by the source's (and `Line.lean`'s) induction N → N + 1 with the oscillator in the right chart (`S_succ`), from the kernel base S 14 3 (`baseCheck_ok`, 37 generations) and N = 8 .. 13 directly (`directOK_ok`). capA, the wire unit and the gun are asserted equal to line-C's by `tape_divider.py`, which also checks the periods on the oracle for N = 8 .. 16. N = 3 .. 7 (direct runs in the catalogue) are not covered.
