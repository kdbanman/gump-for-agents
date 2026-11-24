# Referee report: the Lean formalisation of 2026-11-18 (`research/blast/lean/`)

*Referee: an agent with no part in the work, 2026-11-24. Brief: break the statements, the definitions, the trust
base and the tie to `reference/oracle.py`. Examined: commit `2cfee2e` (its `research/blast/lean/` is `6cc1a68`; the
Lean files there are byte-identical to `9ed370d` of 2026-11-18, only `check.sh` and `statements.py` changed on
11-24). Files named `Dice*`, `Tape*`, `Line*`, `Clock*`, `Chain*` were not reviewed (one oracle test of `Line.lean`'s headline is in §8). Everything here is reproducible from
the scripts in this directory; bulk output is under `research/scratch/blast/ref-lean/`.*

**Verdict in one paragraph.** I found no theorem whose Lean statement is false to its source or quietly weaker
than its row says, apart from the torus restriction of the T5 rows, which four rows of `STATEMENTS.md` do not
mention. Every definition I examined is the document's, on cells. The kernel-checked library rests on
`propext`, `Classical.choice` and `Quot.sound` only: I audited all 1,782 constants of the core library and all
86 constants of the Mathlib package, not only the 74 + 12 listed. The defects are in the plumbing that ties the
proofs to the ground truth. `check.sh` does not start on a fresh clone. Its verdict ignores three of its four
oracle checks. `gumpcheck states` passes empty or unparsable files.

## 1. Defects, worst first

| # | defect | reproduction |
|---|---|---|
| D1 | **`check.sh` reports success whatever the oracle comparison, the differential test and the census say.** Each is a pipeline: `gumpcheck states … \| sed …`, `sh difftest.sh --quick \| tail -3`, `python3 census_check.py … \| tail -2`. A POSIX `sh` pipeline returns the status of its *last* command, so `set -e` never sees a failure. With every soup corrupted (one cell of generation 30 moved), and difftest and census both exiting 1, `check.sh --long` prints the `MISMATCH` lines, then `lean: all checks passed`, and exits 0. The README's "two ties to the ground truth, both run by `check.sh`" and "a result counts when `check.sh` passes" therefore rest, for the verdict, on the 2012 population logs alone (that comparison is inside an `if … cmp`, so it is enforced). | `sh research/blast/ref-lean/attack_gumpcheck.sh`, part 4. It uses a `python3` shim on `PATH`; no file is edited. |
| D2 | **`check.sh` cannot run on a fresh clone.** (a) Line 21 redirects into `.lake/build.log` before anything has created `.lake`, so it fails at once with "Directory nonexistent" and exit 1. The 11-18 version has the same line. (b) After `mkdir .lake`, today's version (`6cc1a68`) builds every `Gump.*` module but not the root module `Gump`, which `Axioms.lean` imports. The axiom step then fails *silently*, with exit 1 and no message, because lean prints its errors to stdout and stdout is redirected into `.lake/axioms.txt`. By reading, the same applies in `mathlib/` to `GumpMath`, which `mathlib/Axioms.lean` imports and `lake build $MM` does not build (not run: I built `GumpMath` by hand before the `--mathlib` step). The authors' workspace passes only because it still holds `Gump.olean` and `GumpMath.olean` from 2026-11-18 19:34. | `research/scratch/blast/ref-lean/clean_build.log`, `clean_build2.log` (scripts `clean_build.sh`, `clean_build2.sh`). Workaround: `mkdir .lake; lake build Gump` (and `lake build GumpMath`), see `clean_build3.sh`. |
| D3 | **`gumpcheck states` passes files that compare nothing.** Each of these exits 0: an empty file; a file holding only generation 0; a file truncated after 10 of 60 generations; a file whose every cell line is unparsable (`x,y,z` or tab-separated), which compares 60 empty generations. Lines that do not parse are dropped silently. The `G g n` header's generation number and count are never checked. Only the printed counts ("0 generations", "seed 0 cells") show it, and by D1 nothing reads them. It does catch a moved cell, an added non-cell, and CRLF line endings, which it parses correctly. | `attack_gumpcheck.sh`, parts 1–3. |
| D4 | **The statement table understates one restriction.** AUTOMATON T5 and threshold.md §1 set T5 in "a finite vessel (a torus, or a region whose outside is dead forever)". The Lean covers only finite sets of the infinite lattice that hold every live point. `energy_identity`'s row says so. The rows for `energy_bounds`, `period_two_of_no_O1`, `oscillator_period_two` and `budget` say "Same" although they have the same restriction. Likewise T3's "applies to … toroidal patterns too" is not stated; for even H it follows from `Torus.lift_trun`, but no theorem says it. | Compare `STATEMENTS.md` §T5 with `docs/AUTOMATON.md` line 98. |
| D5 | Small inaccuracies in the prose. (i) `oscillator_period_two`'s row says "without overcrowding events"; the Lean hypothesis is the weaker "no O1 event" (overcrowded *and* live two generations before), so the theorem is stronger than the row says. (ii) README: "One proof, `hex_check`, uses `decide +kernel`". So do `cube_still`, an example in `Bits.lean`, the four `Signals` theorems and every census theorem. (iii) `STATEMENTS.md`: "Every theorem here is in `Axioms.lean`". `exists_six_outside` is not; my full audit (§5) covers it. (iv) `check.sh` and the `Axioms.lean` header name `Lean.ofReduceBool` as the trace of `native_decide`. In Lean 4.36, `#print axioms` shows an auxiliary axiom `<name>._native.native_decide.ax_…` instead (control in `AllAxioms.lean`). The whitelist in `check.sh` still rejects it, so this is a stale comment only. (v) Timings: "about 10 seconds" for `check.sh`. From nothing, on one core, the build alone takes 124 s. | by reading; (iv): `lake env lean research/blast/ref-lean/AllAxioms.lean` |

Suggested fix for D1–D3 (not applied, since `research/blast/lean/` is not mine to edit):
- Run each check into a file and test its exit status: `gumpcheck states $T/soup.txt > $T/o || { cat $T/o; exit 1; }`, and the same for `difftest.sh` and `census_check.py`. `/bin/sh` here is dash, which rejects `set -o pipefail`, checked.
- `mkdir -p .lake` before the first redirect, and add `Gump` and `gumpcheck` to the build line (`GumpMath` in `mathlib/`).
- In `Check.lean`: reject lines that do not parse; require each header's g to be the previous g + 1 and n to equal the number of points read; require at least one comparison. `check.sh` should also require "60 generations compared".

## 2. The statements, row by row

Verdicts: **same** 36, **says more** 7 (the Lean is stronger than the sentence, and true), **says less** 7 (of
which 3 are acknowledged in their row), **cannot tell** 0. "Tested" names a check in `falsify.py` (§4). A row
I could not break is "not broken by these tests". It is not "correct".

| row | verdict | notes, tests |
|---|---|---|
| `mem_offsets_iff` | same | Basic.lean's offsets equal `oracle.offsets` as sets for each axis. The characterisation agrees with them on [-3,3]³ (tested). |
| `isCell_iff` | same | `Pt.isCell` equals the oracle's mask on all of [-7,7]³ (tested). |
| `rule_iff` | same | by reading. The difftest's local part feeds all 2¹³ neighbourhoods per axis (§6). |
| `nbrs_isCell` | same | 1,176 cells of [-7,7]³ (tested). |
| `layer_histogram` | same | 3 axes × 8 diagonals (tested). |
| `Sealed.run_dead` | same | for sets of cells. On a set containing non-cells, `Sealed` uses Lean's arbitrary neighbour list of a non-cell (`nbrs_not_symm_off_cells`). That is harmless: the theorem is still true and nothing in the documents concerns such sets. |
| `Sealed.union` | same | binary. Arbitrary unions are `core_sealed`. |
| `confinement` | says more | any integer C. The hypothesis asks every *point* above C to be dead, not only cells; for the oracle's states, which live on cells, that is the same. Hull test: 930 generations, 11,279 live cell-generations (oracle). |
| `hull` | says more | any intersection of the 8 half-spaces containing the pattern (tested by the oracle). |
| `firewall` | says more | any integer C (tested: 40 soups × 25 generations). The torus clause of T3 is not stated (D4). |
| `firewall_separates` | same | the other side follows from the opposite diagonal (checked by reading: the same band). |
| `slab_closed` | same | |
| `nbrs_symm` | same | all cell pairs within max-norm 2 in [-7,7]³ (tested). |
| `stepFin_config` | same | the proof covers all patterns. The executable is tied to the oracle by difftest (§6). |
| `runFin_config` | same | |
| `symmetry_preserved` | same | the 48 × even translations. Whether that is the whole group is not claimed by the Lean. |
| `finite_eventually_periodic` | same | `eventually_periodic`'s bound μ + T ≤ 2^N + 1 is the pigeonhole on N hull cells: correct and astronomically loose. |
| `no_spaceship` | says more | a later generation need only *contain* a nonzero translate. Not broken: 28 random seeds, 40 generations each (oracle). |
| `light_cone` | same | 2 per generation is a bound in max-norm (every offset has max-norm 2). In L1 a difference front moved 4 in one generation (tested), so the norm in the sentence matters. A max-norm spread of exactly 2n was seen up to n = 3 in 277 generations. Tightness for all n is not tested. |
| `axis_halfspace_not_confining` | same | |
| `two_layers_not_firewall` | same | the oracle refills two dead layers in one generation in 35 of 40 soups (tested). |
| `cube_still` | same | |
| `lift_tstep` | same | even H. Transcribed `tstep` = `oracle.step` entry by entry for H = 2..10, odd H included, also with non-cell bits set. `lift_tstep` holds for every even H ≤ 10 and fails for every odd one, as the file's header says (tested). |
| `oscCert_spec` | same | the census and line-C rest on it (§6). |
| `energy_identity` | says less | no tori (acknowledged). F, drive and diss transcribed literally: the identity holds at all 1,920 steps of 24 hull runs, 12,339 live cell-generations (tested). |
| `energy_bounds` | says less | no tori, which the row does not say (D4). Bounds hold at every step (tested). |
| `period_two_of_no_O1` | says less | no tori, not said (D4). Otherwise slightly sharper than the sentence: no O1 event from T+1 on gives t₀ ≤ T + 26N. In 11 runs with O1 events, period ≤ 2 came at most 6 generations after the last event (tested). |
| `oscillator_period_two` | says less | no tori, not said (D4). The hypothesis is weaker than the row's paraphrase (D5 i). 40 catalogue oscillators of period ≥ 3 all have O1 events, and over a period drive = dissipation (tested). |
| `budget` | says less | no tori, not said (D4). Holds on 480 random windows (tested). |
| `sealed_iff_run_dead` | same | |
| `exists_birth` | same | |
| `no_finite_sealed` | same | the "cells or not" extension concerns Lean's arbitrary non-cell neighbourhoods. It is true, but has no meaning in the document. |
| `exists_six_outside` | same | not in `Axioms.lean` (D5 iii). Standard axioms by my audit. |
| `slab_not_sealed_of_finite` | same | `h3` is exactly "three odd levels s, s+2, s+4 in [A, B]". |
| `sealed_component_infinite` | same | |
| `hull_component_touches` | says more | three neighbours outside, not one. |
| `torus_slab_loop` | says less | acknowledged. On the universal cover; its content is `slab_component_infinite` plus the pigeonhole on a finite colouring. That a set sealed on the torus lifts to a set sealed in the slab is not proved. |
| `hexagon_sealed` | same | the "modelling choice" holds. For a start cell of each axis in 4 layers of 3 diagonals, the closed kagome walks of six distinct cells number exactly two (the two hexagons at a kagome vertex). All 72 are sealed, and they are exactly the minimal sealed sets the complete search finds (tested). |
| `layer_sealed_six` | says more | every layer, every diagonal. Lists may repeat, which costs nothing, since the duplicate-free list of any finite set is one of them. Complete search to 7 cells through each start cell found no sealed set below 6 (tested). |
| `halfPlane_sealed` | same | 300 random (v, C), 17,620 cells (tested). |
| `layer_halfPlane_dead` | says less | acknowledged: half-plane by half-plane, and the convex-hull reading is not formalised. The convex-hull reading itself holds by the oracle on 120 one-layer soups (tested). |
| `set36_all_sealed` | same | as the row's sentence, which is existence. Minimality is not in Lean (acknowledged). I did the comparison the README lists as not done. `set36` is sealed by `sealed.py`'s own `is_sealed(W, 2)`. Each layer's 18 cells form one closed kagome walk (a Hamiltonian kagome cycle; the induced graph has 6 chords, i.e. six whole triangles). And `set36` is **the same set**, up to the slab's symmetries, as the one `python3 research/theory/sealed.py minsat 2 7 36` prints. That run (100 s, with pysat in a private venv; output in `minsat_2_7_36.txt`) also reproduces the source's patch minimality: none with 35 cells. Command: `set36_compare.py minsat_2_7_36.txt`. |
| `sealed_iff_nine` | same | |
| `core_nine` | same | the 9-core of the graph induced on D. |
| `core_iff_not_bp` | same | the closure is defined as the least closed superset. |
| `skeleton_mono` | same | full lattice. `slabSkeleton_mono` is the slab version (no torus). |
| `pocket_autonomous` | says more | K need only stay dead in both histories, not be sealed. |
| `finite_pocket_periodic` | same | |
| `beyond_sealed_iff` | same | as the new claim. Tested on all 29,410 primitive (u, C) with \|u_i\| ≤ 6 and C ∈ [-8, 8]: sealed iff \|u_x\| = \|u_y\| = \|u_z\|, with no disagreement. All 7,922 non-primitive pairs agree too (not claimed). `beyond` holds cells only, so no non-cell artefact enters. |
| `sealed_unbounded` | same | as the new claim. The hypothesis can be met: v = (1, 3, 9). `slab_sealed_unbounded`'s too: `Diag.perp` = (1, 2, −3) for (1,1,1) is in-plane and orthogonal to none of the 36 offsets (checked by hand). |

Hypotheses that might not be satisfiable: I checked by reading that each one in the 50 rows can be met. Several are
met by named witnesses in the library: `hexRing_walk`, `two_layers_finite_sealed`, the hull for `hV`, v = (1,3,9),
`Diag.perp`. The only vacuous instances are degenerate parameters, for instance an even s in `layer_sealed_six`
(no layer there). The ∃-statements have non-degenerate witnesses: `T > 0`, `q ≠ q'`, `L ≠ []`.

## 3. The definitions

| definition | verdict |
|---|---|
| `Pt`, `Pt.isCell` | ℤ³; `isCell` = exactly one odd coordinate, equal to `oracle.masks` (Lean's `%` is `Int.emod`, which agrees with Python's `%` for divisor 2). |
| `Pt.axis` | the odd coordinate on cells. On non-cells an arbitrary choice, used only when `Sealed`, `SealedIn` or `BPClosed` are applied to sets that contain non-cells. |
| `offsets`, `nbrs` | equal to `oracle.offsets(a)` as sets. `nbrs p = p + offsets(axis p)`, which is the oracle's `np.roll(h, −o)` convention (cnt[p] = h[p + o]; tested). |
| `rule`, `step`, `run` | B45/S345; `step` kills non-cells, as the oracle never writes them. Since neighbours of cells are cells, a live non-cell at generation 0 influences nothing. |
| `Sealed`, `SealedIn` | "at most 3 neighbours (in the vessel) outside", equal to `sealed.py`'s `is_sealed` on cell sets. |
| `slab`, `hullV`, `halfPlane`, `beyond`, `band`, `above` | cells, except `band` and `above`, which are all points; the extra points are harmless as above. |
| `core`, `skeleton`, `slabSkeleton` | the union of the sealed subsets, i.e. K(t) = the core of the dead cells. Full lattice or infinite slab; not tori. |
| `F`, `drive`, `diss`, `o1`, `mism` | F t = 2E(t+1) of threshold.md §1 with ordered pairs. Transcribed and checked: identity, bounds, symmetry of the pairing (§4). |
| `Torus.tstep`, `lift` | `tstep` is the oracle's step entry by entry for every H tested (2..10, odd included); `lift` reads the array mod H. |
| `oscCert`, `evCert`, `isOsc` | not trusted as definitions: their `_spec` theorems state the property in terms of `run` and `lcfg`. |

## 4. Falsification by computation: `falsify.py`

`python3 research/blast/ref-lean/falsify.py` (34 s on one core; 55 PASS lines; log in
`research/scratch/blast/ref-lean/falsify_all.log`): 0 FAIL lines. Written from `oracle.py` (offsets, masks, step on
padded even-H arrays), with Lean definitions transcribed literally where they might differ (`lean_isCell`,
`lean_axis`, `lean_nbrs`, `T5`, the `tstep` loop). The tests are `nbrs`, `layer`, `set36`, `beyond`, `t5`, `spaceship`
(with light cone), `torus` and `hull` (with firewall). Each is named in §2. A bug of my own on the first run is
worth recording, because it shows how such tests go vacuous. The array shift was odd, so every pattern died at
once and every dynamic test passed on empty runs. The tests now print live cell-generation counts.
`signals_tie.py` checks Gump/Signals.lean. For N = 2, 3, 12, 13, each Lean list minus its stated even translation
is exactly the object that `line-C.json`'s `note` describes. The oracle finds generation 2N + 4 equal to 2N and
2N + k different for k = 1, 2, 3. PASS.

## 5. The trust base

- grep of every Lean file, `Check.lean`, `TorusCheck.lean`, the lakefiles and both Axioms files for `axiom`,
  `sorry`, `native_decide`, `unsafe`, `implemented_by`, `extern`, `opaque`, `partial`, `set_option`, `admit`,
  `macro`/`elab`/`syntax`, custom `Decidable` instances. Nothing, apart from the expected:
  - `noncomputable` on `core`, `coreIn`, `skeleton`, `slabSkeleton` and `comp`, which are classical indicators
    used in statements and never evaluated;
  - `decide +kernel` in `hex_check`, `cube_still`, a `Bits` example and the four `Signals` theorems. The kernel
    evaluates these with its built-in Nat arithmetic; no axiom is added.
- **Every constant, not only the listed ones**: `AllAxioms.lean` walks the environment and applies
  `Lean.collectAxioms` (what `#print axioms` prints) to every constant whose module has root `Gump`. It found
  1,424 theorems, 325 definitions and 33 other constants. Axiom sets seen: {}, {propext}, {propext, Quot.sound},
  {propext, Classical.choice, Quot.sound}. No constant goes beyond those three, and no `axiom` or `opaque` is
  declared. `AllAxiomsMath.lean` does the same in the Mathlib package: 75 theorems and 11 definitions of
  `GumpMath`, none beyond the three. Controls in the same file: a `sorry` shows as `sorryAx`, a `native_decide` as
  `refereeCtlNative._native.native_decide.ax_1_1`.
  Command: `cd <built copy>/research/blast/lean && lake env lean research/blast/ref-lean/AllAxioms.lean`; for
  `mathlib/`, use `AllAxiomsMath.lean`.

## 6. Clean machine and the executable tie

Fresh `git clone` of the local repository at `2cfee2e`, nothing from the authors' `.lake`, the toolchain from
`lean-toolchain` (elan's v4.36.0), a fresh Mathlib cache directory, one core (`taskset -c 0`):

| step | result | time |
|---|---|---|
| `check.sh` as committed | **fails**: `.lake/build.log: Directory nonexistent` (D2a) | 0 s |
| after `mkdir .lake`: `check.sh` | build OK (53 jobs), then **fails silently** at `Axioms.lean`: `Gump.olean` does not exist (D2b) | 124 s |
| after `lake build Gump` by hand: `check.sh` | passes: 74 headline theorems, logs of sides 8, 9, 10 identical, 3 soups × 60 generations | 7 s |
| `check.sh --long` | passes: side 11 (4,219 lines), difftest `--quick` PASS (160 s), census 1,307 / 1,307 with its 5 negative controls rejected (82 s) | 316 s |
| `cd mathlib && lake exe cache get` | 9,117 files, network | 140 s |
| `lake build GumpMath` by hand (D2b), then `check.sh --mathlib` | passes: 12 theorems, standard axioms | 9 s + 8 s |
| the 11-18 `check.sh` (`9ed370d`), plain and `--mathlib` | pass once `.lake` exists (it builds the root `Gump`) | 5 s, 9 s |

So the clean machine passes everything once the two script defects are worked around. That holds for `--long`
and its differential test and census too, and nothing from the authors' build directories is needed.

**difftest.** Full run (`difftest.py` without `--quick`, 353 s on one core, exit 0): 9,442 generations, 0 mismatches. The figures are
the README's: 3 × 8,192 neighbourhood states, 238 soups, 6 objects, and the torus at H = 2, 4, 6, 8, 12, 16, 24
plus wire W00. Coverage is 78/78 (axis, state, count) triples, and the 15 mutants are all caught. By reading,
`local_seed` does give every centre exactly the stated 13-bit neighbourhood: copies are 6 apart and the
neighbours lie within 2, so no copy reaches another's centre. The torus part covers even H only. Odd H is
covered by my `torus` test, where `tstep` matches the oracle. `check.sh --long` runs only `--quick` (H = 4, 8, 16),
and by D1 its result does not reach the verdict. Log: `research/scratch/blast/ref-lean/difftest_full.log`.

**census.** The generated theorem is exactly `oscCert_spec`'s conclusion for the catalogue's phase-0 cells.
`census_check.py` treats a chunk as failed if lean exits non-zero or prints "error". Its exit status is lost
by D1, so I ran it standalone in the clean clone: 1,307 of 1,307, all five negative controls rejected, exit 0, 78 s
(`research/scratch/blast/ref-lean/census.log`).

## 7. Not checked

- The proofs themselves: the kernel checked them, and I read proofs only where a statement's meaning depended
  on them.
- That `set36` is literally identical to `sealed.py`'s set. I compared canonical forms under the 12 point
  symmetries of the slab and its even in-layer translations, and they agree.
- Minimality of 36 beyond the patch of radius 7. As the source says, that is not claimed.
- Odd-H seam behaviour beyond H ≤ 9. The tightness of the light cone beyond n = 3. Non-primitive directions
  beyond |u_i| ≤ 6. One-layer convex confinement beyond 120 small soups.
- The files written today (`Dice*`, `Tape*`, `Line*`, `Clock*`, `Chain*`, and the untracked files of the working
  tree). `check.sh`'s `MODS` glob builds whatever `Gump/*.lean` holds, so any in-flux file there also enters
  `check.sh`. Commits after `2cfee2e` (`4c65854`, `530940e`, …) are outside this review.

## 8. Outside the brief: `Line.lean`'s headline, by the oracle

`Gump/Line.lean` was committed at 11:33 today (`530940e`) and I did not review it. Its headline is
`line_orbit (N) (hN : 2 ≤ N) (s p) (hp : 0 < p) : run (lineC N) (s + p) = run (lineC N) s ↔ 2 * N ≤ s ∧ p % 4 = 0`.
I tested the informal reading with the oracle: line-C(N) built from `line-C.json` as its `note` says, every
s ≤ 2N + 8 and 1 ≤ p ≤ 12, for N = 2..14, 20 and 25. It holds in every case
(`python3 research/blast/ref-lean/line_orbit_oracle.py 14`, 12 s; log `research/scratch/blast/ref-lean/line_orbit.log`).
I did not check that the Lean `lineList N` is that object.
