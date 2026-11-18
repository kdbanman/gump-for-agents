# Gump in Lean

Started 18:07 UTC, 2026-11-18, on the owner's word ("go ahead and install lean, and start work in its direction").
Lean 4.36.0, pinned in `lean-toolchain`. This directory is the core development and needs nothing but Lean;
`mathlib/` is a second package that adds Mathlib for the theorems that want sums, matrices and measures.

## The aim

**Every theorem of this project checked by Lean's kernel, and the measured laws turned into theorems and checked
too.** The summit is the open problem itself: a machine-checked law for how long a face of gump's hull lives, with
its constant, for gump and not only for a surrogate. Today nobody has a paper proof of that law. That is a fact
about today. It is not the size of the goal, and nothing below is written to shrink it.

Lean is used here in two ways. It is a judge: a statement counts as proved when `check.sh` passes with no
`sorry` and no axiom beyond Lean's standard three. And it is an instrument: exhaustive finite facts, exact
rational linear algebra and certificate checking are computations Lean can certify, so a bound found by a
program outside Lean becomes a theorem once Lean has checked its certificate.

## What is checked now

`sh research/blast/lean/check.sh` (about 10 seconds; `--long` adds the 4,218-generation log). The Mathlib package:
`cd research/blast/lean/mathlib && lake exe cache get && lake build` (Mathlib v4.36.0; the cache is 7 GB on disk).

| statement (`docs/AUTOMATON.md`) | Lean name | file |
|---|---|---|
| The lattice, the twelve neighbours, B45/S345, one generation, n generations | `Pt`, `offsets`, `rule`, `step`, `run` | `Gump/Basic.lean` |
| The definitions restated in the oracle's terms: an offset is a neighbour iff it is ±2 on both other axes and 0 on the normal one, or ±1 on the normal axis and ±1 on exactly one other; a cell has exactly its axis coordinate odd; born with 4 or 5, stays with 3, 4 or 5; neighbours of cells are cells; the twelve offsets are distinct | `mem_offsets_iff`, `isCell_iff`, `axis_odd`, `rule_iff`, `nbrs_isCell`, `offsets_nodup` | `Gump/Spec.lean` |
| **T1**, layer histogram: 1, 2, 6, 2, 1 neighbours at Δs = −4, −2, 0, +2, +4, for every orientation and diagonal | `layer_histogram` | `Gump/Layers.lean` |
| A dead sealed set stays dead whatever happens elsewhere (opening of **T6**) | `Sealed.step_dead`, `Sealed.run_dead` | `Gump/Sealed.lean` |
| Unions of sealed sets are sealed (**T6**) | `Sealed.union` | `Gump/Sealed.lean` |
| Half-spaces across a body diagonal are sealed; bands of three layers are sealed | `above_sealed`, `band_sealed` | `Gump/Sealed.lean` |
| **T2**, octahedral confinement | `confinement` | `Gump/Sealed.lean` |
| A pattern stays inside its diagonal hull forever | `hull` | `Gump/Sealed.lean` |
| **T3**, firewall: three dead layers stay dead | `firewall` | `Gump/Sealed.lean` |
| **T3**, second half: the two sides never influence each other again | `firewall_separates` | `Gump/Sealed.lean` |
| **T4**, a pattern in the layers A ≤ s ≤ B stays in them | `slab_closed` | `Gump/Sealed.lean` |

| **T6 / Theorem 3**, no finite sealed set in the full lattice (any nonempty finite set of points) | `no_finite_sealed`, `not_sealed_of_finite`, `exists_six_outside` | `Gump/Thickness.lean` |
| **Theorem 3**, no finite set sealed in a slab of three or more layers | `slab_not_sealed_of_finite`, `layers_not_sealed_of_finite` | `Gump/Thickness.lean` |
| **Lemma 1**, both halves: a set of cells is sealed iff, dead, it stays dead whatever happens elsewhere (lattice, any vessel, slabs) | `exists_birth`, `sealed_iff_run_dead`, `sealedIn_iff_step_dead`, `sealedIn_slab_iff_run_dead` | `Gump/Thickness.lean` |
| **Theorem 3**, components: infinite in the lattice and in thick slabs; in a hull vessel each touches the outside | `sealed_component_infinite`, `slab_component_infinite`, `hull_component_touches`, `finite_closed_touches` | `Gump/Thickness.lean` |
| **Theorem 3**, torus clause, on the universal cover | `torus_slab_loop`, `torus_loop` | `Gump/ThickTorus.lean` |
| **Theorem 4 (i)**: every hexagon ring is sealed in its layer; no nonempty sealed set of five or fewer cells in any layer (the source had this by SAT in a patch; here it is proved for every layer) | `hexagon_sealed`; `layer_sealed_six`, `layer_no_sealed_le_five` | `Gump/ThickHex.lean`, `Gump/ThickSmall.lean` |
| **Theorem 4 (ii)**: half-planes of a layer are sealed; false in two layers | `halfPlane_sealed`, `layer_halfPlane_dead`, `two_layer_halfPlane_not_sealed` | `Gump/ThickSmall.lean` |
| **Proposition 5**, existence: a 36-cell set sealed in every two-layer slab | `set36_sealed`, `set36_all_sealed`, `two_layers_finite_sealed` | `Gump/ThickSmall.lean` |
| **T6, remark**: the largest sealed subset is the 9-core and the complement of the threshold-4 bootstrap closure; K(t) only grows | `sealed_iff_nine`, `core_nine`, `core_iff_not_bp`, `skeleton_mono`, `slabSkeleton_mono` | `Gump/ThickCore.lean` |
| Pockets of a dead sealed set evolve independently; a finite pocket is eventually periodic within t₀ + 2^N | `pocket_autonomous`, `finite_pocket_periodic`, `slab_finite_pocket_periodic` | `Gump/ThickPocket.lean` |
| **New**: for a primitive integer direction, the far side of a plane is sealed iff the direction is a body diagonal | `beyond_sealed_iff`, `axis_halfspace_not_sealed` | `Gump/ThickHalf.lean` |
| **New**: a nonempty sealed set is unbounded along every generic direction (lattice; in-plane in thick slabs) | `sealed_unbounded`, `slab_sealed_unbounded` | `Gump/ThickHalf.lean`, `Gump/ThickGeneric.lean` |
| Upper and lower certificates for a killed finite Markov chain: Q ≥ 0 and Qv ≤ λv give Qᵗv ≤ λᵗv and survival ≤ c·λᵗ·v; Qv ≥ μv gives survival ≥ μᵗ·v/C (first step of line 3 of the climb) | `pow_mulVec_le`, `le_pow_mulVec`, `survival_le`, `survival_ge` | `mathlib/GumpMath/Certificate.lean` |

All **[proved, machine-checked]**; axioms: `propext`, `Classical.choice`, `Quot.sound` only (`Axioms.lean`).
T2 and T3 are proved here as two instances of one lemma (a dead sealed set stays dead), which is how T6 says they
should be read. T2 and T3 are stated for every integer level C, not only for lattice layers; no parity is needed.

**Is the Lean rule gump?** A proof in Lean is about Lean's definition of the rule. Two ties to the ground truth,
both run by `check.sh` [measured]:
- `gumpcheck cube` runs the Lean rule on the 2012 closed-cube seeds and prints the logs in `reference/golden/`
  line for line: sides 8, 9, 10, and side 11 through its 4,218 generations.
- `gumpcheck states` compares the Lean stepper with `reference/oracle.py` state for state: three soups, 60
  generations each, no mismatch; with one cell of one generation moved, it fails at that generation.
The stepper (`Gump/Finite.lean`) evaluates `Gump.step` itself, the function the theorems are about, at every
live cell and every neighbour of one. Not yet proved in Lean: that no other cell can be born (it cannot: a dead
cell with no live neighbour stays dead, and the neighbourhood is symmetric).

`STATEMENTS.md` (written by `statements.py`) puts each headline theorem's Lean statement, verbatim, next to the
sentence it is meant to be and says where the two differ in strength. One proof, `hex_check` in `ThickHex.lean`,
uses `decide +kernel` (the kernel evaluates the check; no axiom is added); nothing uses `native_decide`.

Not checked: nothing here is refereed by a second agent; the statements were read against their sources by their
authors and by the PI only. `set36` was found by a fresh SAT run and not compared with `sealed.py`'s set.

## The climb

Each line is a goal at full size with a first move. Difficulty is a fact to be found out, not a reason to choose a
smaller goal; where a tool is missing from Lean's libraries, building it is part of the work.

1. **The rest of the structure theory.** T6 in full (no finite sealed set in three or more layers; the 9-core);
   T5 (the energy, ΔE = D − Q, period ≤ 2 without overcrowding); eventual periodicity of every finite seed; the
   speed limit; the symmetric neighbourhood and "neighbours of cells are cells"; the stepper's correctness.
   First move: T6's extremal-cell argument, in `Gump/Thickness.lean`.
2. **A certified census.** Still lifes, oscillators and sealed sets in bounded windows, found by SAT or search
   outside Lean and certified inside it (`decide`, `bv_decide` with its checked certificates). First move: the
   six faces of a cube are a still life; the 6-cell hexagon ring is sealed in one layer; the 36-cell set in two.
3. **Finite vessels as Markov chains, with certified rates.** The dice surrogate and the noisy hull are finite
   chains with honest randomness. For a non-negative matrix Q and a positive vector v, Qv ≤ λv entrywise gives
   survival ≤ C·λᵗ, and Qv ≥ λv gives survival ≥ c·λᵗ: two inductions, no spectral theory. So a vector computed
   outside Lean certifies a two-sided bound on a death rate inside it, in exact rational arithmetic. First move:
   the one-layer dice surrogate on the smallest wrapped and rimmed faces, with its rate in a proved interval.
4. **The blast's theorems** (`rigour/THEOREMS.md`): Lemma 0, Theorem 1 (ln τ ≤ 2.509·A), the tilt identity,
   Lemma R, the seam identity, and Theorem 3 with its hypothesis proved or refuted rather than assumed.
5. **Both exits as theorems.** That a wrapped face of the surrogate dies by the bust and a rimmed one by the fade
   is measured and exactly computed at small sizes. Prove it for all sizes: a lower bound on the bust's share on
   wrapped faces, an upper bound on rimmed ones.
6. **The price.** A proved interval for the cost per cell of a face's death, first for the surrogate (the limit
   exists by Theorem 2's local sum; pin it between certified bounds from finite strips), then for gump under
   noise at depth, then with the noise taken to zero.
7. **The summit.** The face law for gump with its constant, and why a hull face and a wrapped face pay different
   prices at the sizes measured, as theorems.

## For a contributing agent

Pick a line above, or add one that is larger. State the theorem in Lean first, in the terms of `Gump/Basic.lean`,
and get the statement read by someone else before proving it. A result counts when `check.sh` passes: no
`sorry`, no `native_decide` unless the README says where and why, axioms printed in `Axioms.lean`. Say what was
not checked. If the libraries lack what the proof needs, write it.
