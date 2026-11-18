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
- **Difference:** Stronger: the band is C < s ≤ C + 6 for any integer C.

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
- **Difference:** Same, doubled.

### `period_two_of_no_O1` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem period_two_of_no_O1 (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (T : ℕ) (hO : ∀ t, T ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) : ∃ t₀, T ≤ t₀ ∧ t₀ ≤ T + 26 * V.card ∧ ∀ t, t₀ ≤ t → run c (t + 2) = run c t
```

- **Meant to be:** A, T5: an orbit with no such events from some time on has period ≤ 2 (reached within 26N + 1 further steps).
- **Difference:** Same, with the bound 26N.

### `oscillator_period_two` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem oscillator_period_two (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (μ P : ℕ) (hP : 0 < P) (hper : ∀ t, μ ≤ t → run c (t + P) = run c t) (hO : ∀ t, μ ≤ t → ∀ p, 6 ≤ count (run c (t + 1)) p → run c t p = false) : ∀ t, μ ≤ t → run c (t + 2) = run c t
```

- **Meant to be:** A, T5: every oscillator of period ≥ 3 has them.
- **Difference:** Contrapositive form: an eventually periodic orbit without overcrowding events has period dividing 2.

### `budget` (`mathlib/GumpMath/Threshold.lean`)

```lean
theorem budget (hc : ∀ p, c p = true → p.isCell = true) (hV : ∀ t p, run c t p = true → p ∈ V) (T K : ℕ) : (∑ t ∈ Finset.range K, (mism V c (T + t) : ℤ)) ≤ 20 * ∑ t ∈ Finset.range K, (o1 V c (T + t) : ℤ) + 26 * V.card
```

- **Meant to be:** `threshold.md`: M/(N·T) ≤ 20·O1/(N·T) + 26/T.
- **Difference:** Same, as a sum over any window. The uncapped rule U and the Goles–Olivos theorem for it are not formalised.

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
- **Difference:** Existence only, for every two-layer slab. The set is from a fresh SAT run and has not been compared with `sealed.py`'s. Minimality (36) is not in Lean.

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
