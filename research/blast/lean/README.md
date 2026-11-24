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

`sh research/blast/lean/check.sh` (`--long` adds the 4,218-generation log, the differential test and the census;
`--mathlib` builds and checks the Mathlib package, after `cd research/blast/lean/mathlib && lake exe cache get` once:
Mathlib v4.36.0, 7 GB on disk). **Last run, 2026-11-24 by the integration, in the shared tree with most modules
built and nothing else building:** `--mathlib` from 15:48:40 UTC, 193 s wall (it rebuilt `DiceBound3` after a
comment edit, and the modules that import it); then `--long` from 15:53:16 UTC, 331 s (differential test 185 s,
census 70 s). Both end `lean: all checks passed`: 52 core modules and 73 Mathlib modules build; `STATEMENTS.md` is
current (205 rows); 187 `#print axioms` lines in the core package and 221 in the Mathlib package (220 with
`[propext, Classical.choice, Quot.sound]`, one with `[propext, Quot.sound]`), none beyond the standard three; the
2012 logs of sides 8 to 11 identical; three soups equal to the oracle for 60 generations; the differential test
passes with every mutant caught; 1,307 of 1,307 catalogue objects certified. From an empty `.lake` the core check
took 852 s at load 12 to 14 on 4 cores (`notes/tape.md`, 14:15 UTC, before the tape agent's third task); the Dice
exit modules peak near 7 GB and must be built one at a time.

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
| The neighbourhood is symmetric on cells (and not off them) | `nbrs_symm`, `nbrs_not_symm_off_cells` | `Gump/Symm.lean` |
| **The executable stepper is `step`, and n steps of it are `run`**, with no hypothesis on the pattern: no birth is missed | `step_support`, `stepFin_config`, `runFin_config` | `Gump/FiniteCorrect.lean` |
| The hull holds finitely many cells; **every finite seed is eventually periodic** (cycle within 2^N + 1); **no spaceships** | `mem_hullCells`, `eventually_periodic`, `finite_eventually_periodic`, `no_spaceship` | `Gump/Periodic.lean` |
| Speed limit: a light cone of max-norm radius 2n; attained in one generation | `light_cone`, `dead_ball`, `live_near_seed`, `speed_two_attained` | `Gump/Speed.lean` |
| The 48 lattice symmetries and the even translations commute with the dynamics; a seed's symmetry is preserved forever | `offsets_sym`, `step_act`, `run_act`, `symmetry_preserved` | `Gump/Equivariance.lean` |
| Axis-aligned half-spaces do not confine; two dead layers are not a firewall | `axis_halfspace_not_confining`, `two_layers_not_firewall` | `Gump/Sharpness.lean` |
| The six faces of a cube are a still life; a bit-parallel stepper is `step`; a kernel-checkable certificate that a cell list is an oscillator of exactly period P | `cube_still`, `Bits.bstep_spec`, `Bits.oscCert_spec`, `Bits.evCert_spec` | `Gump/Certify.lean`, `Gump/Bits.lean` |
| The oracle's even-H array-index torus is `step` on the periodic configuration | `Torus.lift_tstep`, `Torus.lift_trun` | `Gump/Torus.lean` |
| line-C (cap, N units of wire C, rake gun) has exact period 4 from generation 2N, for N = 2, 3, 12, 13 | `Signals.lineC_N_period_four` | `Gump/Signals.lean` (written by `signals_gen.py`) |
| All 1,307 objects of `research/atlas/catalogue.jsonl` are oscillators of exactly their listed period (kernel-checked by a script; the generated theorems are not in the library) | `python3 research/blast/lean/census_check.py research/scratch/blast/lean/census` | scratch |
| **T5** for gump on a finite vessel: the energy step, ΔE = D − Q, the energy's bounds, period ≤ 2 within 26N generations once overcrowding events stop, every oscillator of period ≥ 3 has them, the window budget | `energy_step`, `energy_identity`, `energy_bounds`, `period_two_of_no_O1`, `oscillator_period_two`, `hull_period_two_of_no_O1`, `budget` | `mathlib/GumpMath/Threshold.lean` |
| Upper and lower certificates for a killed finite Markov chain: Q ≥ 0 and Qv ≤ λv give Qᵗv ≤ λᵗv and survival ≤ c·λᵗ·v; Qv ≥ μv gives survival ≥ μᵗ·v/C (first step of line 3 of the climb) | `pow_mulVec_le`, `le_pow_mulVec`, `survival_le`, `survival_ge` | `mathlib/GumpMath/Certificate.lean` |

All **[proved, machine-checked]**; axioms: `propext`, `Classical.choice`, `Quot.sound` only (`Axioms.lean`).
T2 and T3 are proved here as two instances of one lemma (a dead sealed set stays dead), which is how T6 says they
should be read. T2 and T3 are stated for every integer level C, not only for lattice layers; no parity is needed.

### Added on 2026-11-24 (the last-day blast)

Every row is **[proved, machine-checked]** (kernel tier: `decide +kernel` for every base run and certificate, no
`native_decide` anywhere, axioms within the standard three; `AxiomsTape.lean` in the core, `mathlib/AxiomsDice.lean`,
`AxiomsChain.lean`, `AxiomsLink.lean`). The last column says whether a referee has read the statement against its
source and attacked it (reviews in `research/blast/ref-tape/`, `ref-dice/`, `ref-chain/`); the authors' accounts are
`notes/tape.md`, `notes/dice.md`, `notes/chain.md`, `notes/link.md`, and every row's difference from its source is in
`STATEMENTS.md`.

**The catalogue's "for every N" laws** (core Lean; objects are the catalogue's cell lists, `research/signals/`):

| statement | Lean name | file | refereed |
|---|---|---|---|
| **The tape theorem**: every word over {B, C} on the wire moves one unit per two generations, on the whole lattice (signals §10) | `tape_run`, `tape_local_run` | `Gump/Tape.lean`, `Gump/TapeBase.lean` | yes (`ref-tape`, first review: same; `tape_local_run` says more) |
| **The gun's line**: line-C of N ≥ 2 units returns after p > 0 from generation s iff s ≥ 2N and 4 ∣ p (period exactly 4, preperiod exactly 2N) (§21) | `Line.line_orbit`, `line_period_four` | `Gump/Line.lean` | yes (same as the row, more than the source) |
| **A clock of every length**: a named state of capL + N units of wire C + capR has exact period 4N + 2, every N ≥ 1 (§11) | `Clock.clockOf_period`, `clock_cycle`, `lit_clock_small`, `X0_lit` (`clock_every_length`, an existential, says less) | `Gump/Clock.lean` | yes (first review's D1, repaired; second review: `clockOf_period` names its object) |
| **The clock from a single cell**: the one added cell lights the clock of N units into an oscillator of exact period 4N + 2, every N; for N ≥ 6 it is on the cycle at generation N − 2 and at no earlier one | `Clock.lit_clock`, `lit_word`, `lit_enters`, `lit_first`, `lit_enters_at`, `lit_clock_exact` | `Gump/ClockLit.lean`, `ClockLitFirst.lean`, `ClockLitOdd.lean` | yes (third review, at 40520c7: no defect; oracle N = 6–30, entry exactly at N − 2, exact period 4N + 2) |
| **Nine rigid signals** on the rake train, at every place and every time (§30–35) | `Tape.Signals.signal_run`, `train_step`, `train_shift` | `Gump/TapeSignals.lean` | yes (same) |
| **The unzip law, sharp**: for every k ≥ 1 push 8's count read is the tape of its k pulses at every even generation from 2k + 6 on, and not at 2k + 4 (push 8 §5; REVIEW-signals-8 §3) | `Unzip.unzip_law_sharp`, `unzip_law`, `stretch_stands` | `Gump/UnzipProof.lean`, `Gump/Unzip.lean` | yes (same) |
| **The call law, whole**: REVIEW-signals-9 §3 (a) the store wire and the free line evolve as a disjoint union at every generation, and (b) the wire carries the k pulses from 2k + 34 on, every k ≥ 1 | `Call.call_law : CallLaw` (`call_law_a`, `call_law_b`, `line_rest`); a second bit box `Call.Box.bstep_spec` | `Gump/CallProof.lean`, `CallBox.lean`, `CallLine.lean`, `CallUnion.lean`, `CallUnionLocal.lean` | yes ((b) in the first review, (a) and the box in the second) |
| **The readers**: capL of the clock eats every word and keeps no trace (§15); the call line's left cap (`call9.json`, another cap) eats every word too | `Clock.reader_run`, `reader_step`; `Reader.reader9_run`, `reader_run_gen` | `Gump/ClockReader.lean`, `Gump/CallReader.lean` | yes (third review; the finite cell, the call crossing it and the gluing to `call_law`'s V_k are not covered, as the row says) |
| **The beam**: gun, N units of train and absorber have period exactly 4, every N ≥ 1 (§21) | `Beam.beam_period` | `Gump/LineBeam.lean` | yes (third review; oracle N = 1–20, 30) |
| **The divider**: period exactly 8 from generation 2N − 3, every N ≥ 8, and not periodic from 2N − 4 (§21b) | `Divider.divider_period` | `Gump/LineDivider.lean` | yes (third review; oracle N = 8–20, 24, 30; N = 3–7 obey the same law on the oracle, so N ≥ 8 is the proof's limit, not the automaton's) |

**The dice surrogate's lifetime** (`mathlib/`; `Face.P` in `GumpMath/DiceDef.lean` is the one-layer surrogate of
`research/blast/rigour/`, gump's rule on a face with each cell's cells beneath replaced by its own coins, as a killed
chain with rational entries; the first theorems in the repository about a lifetime):

| statement | Lean name | file | refereed |
|---|---|---|---|
| The definition is the source's surrogate | `Face.P`, `hull`, `torus`, `strip`, `patch` | `GumpMath/DiceDef.lean` | yes (`ref-dice`: all 1,310,720 entries of the five 9-cell kernels equal its own, built from the oracle) |
| **Five 9-cell faces** (hull triangle R = 3, tori (1,0),(0,3) and (1,1),(0,3), strip 1×3, patch 1×3): for every QSD, λ in a 19-digit interval and −ln(1 − λ) to ten digits (hull: (2.4837157463, 2.4837157464)); λ > 0 assumed on the tori | `hull3_lifetime`, `hull3_tau`, `torus103_tau`, `torus113_tau`, `strip13_tau`, `patch13_tau` | `GumpMath/DiceHull3.lean`, `DiceTorus103.lean`, `DiceTorus113.lean`, `DiceStrip13.lean`, `DicePatch13.lean` | yes (λ bracketed by the referee's own exact enclosure; `*_lifetime` pins the decay rate with loose constants, 1384 against a true 1.63) |
| **Both exits at 9 cells**: the share of the death flux whose last six transitions hold a fall of ⌈A/2⌉ cells is in (0.017017, 0.017018) on the hull triangle and (0.936852, 0.936853) on the torus (1,1),(0,3), at every generation, for every QSD | `hull3_bust`, `torus113_bust`, `flux_share`, `death_flux`, `hull3_bust_flux`, `torus113_bust_flux` | `GumpMath/DiceHull3Exit.lean`, `DiceTorus113Exit.lean`, `DiceFlux.lean` | yes (the flux step a theorem since `flux_share`; second review) |
| **Theorem 1 at every size**: ln τ < 2.5095·A on every face with all its coins and on every hull face; < 2.2165·A on every hull face; < 1.9228·A on every wrapped face | `lntau_le_all`; `lntau_le_hull`; `lntau_le_hull_all` (with `hull_type`, `hull_balanced`); `torus_regular`, `lntau_le_torus` | `GumpMath/DiceBound.lean`, `DiceHull.lean`, `DiceHullAll.lean`, `DiceBound3.lean`, `DiceTorusReg.lean`, `DiceBound2.lean` | yes (true with room: 1.9228 is 4.1 to 6.4 times ln τ/A on tori up to 12 cells) |
| τ is the mean lifetime: P_μ(T > t) = λ^t and E_μ T = 1/(1 − λ) for every QSD, on every face whose empty state is absorbing | `qsd_survival`, `qsd_mean`, `qsd_mean_all`, `hull3_mean`, `qsd_mean_hull` | `GumpMath/DiceMean.lean` | yes (the proof is `ref-dice`'s, `QsdSurvival.lean`; the module read by `ref-chain`, fourth review) |

**The chain theory** (`mathlib/GumpMath/Chain*.lean`, 16 modules: `rigour/THEOREMS.md` on an abstract finite killed
chain, with Perron–Frobenius built here because Mathlib has none):

| statement | Lean name | file | refereed |
|---|---|---|---|
| **Theorem 2, the tilt identity**: ln τ = ∫₀¹⟨E⟩_s ds = Σ_i c_i, the tilted mean decreasing, ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ = E_μ[E], for every QSD | `tilt_identity`, `neg_log_Z_one`, `IsQSD.lifetime_eq`, `price_mem` | `ChainTilt.lean` | yes |
| A dominant QSD on every finite killed chain (λ ≥ every QSD's, ≥ Q u u, the decay rate of the longest-lived start); Perron–Frobenius (Wielandt); one class ⇒ one QSD with λ > 0; equal prices along symmetries | `exists_qsd`, `tilt_identity_exists`; `exists_pos_eigenvector`, `left_eigen_unique`, `qsd_exists_unique`, `price_invariant` | `ChainExist.lean`, `ChainPerron.lean` | yes (first review's D2, the λ = 0 point mass, repaired by `IsDominantQSD`) |
| **Theorem 1**: ln τ ≤ 2.51·A on every face of the surrogate; ≤ 2.2412·A on the kagome layer over any finite torus | `upper_bound_coins`, `emax_main`, `kagome_sharp_bound` | `ChainCoins.lean`, `ChainSharp.lean` | yes |
| **Lemma 0 with its geometry on every wrapped face** (H,K),(0,D): one QSD with λ > 0, positive; one price per orientation, ln τ = HD(c_X + c_Y + c_Z); one price per cell on rotation-invariant tori | `kagome_lemma0`, `wrapped_lemma0`, `wrapped_one_price_HD`, `wrapped_rotation_HD`, `torus_card` | `ChainKagome.lean`, `ChainTorus.lean` | yes (D3, \|T\| = HD, repaired) |
| The rate from every start; Lemma R (routes); the seam identity (the modelling step a hypothesis) | `decay_bounds`, `lifetime_from_bounds_K`; `routes_first`, `routes_second`, `two_routes_step`; `seam_identity`, `seam_sharp` | `ChainRate.lean`, `ChainRoutes.lean`, `ChainSeam.lean` | yes |
| Theorem 3 from (SSM), as an implication; one price from pointwise (or almost-everywhere) convergence of the per-cell tilted energy, a jump along the tilt allowed; (SSM) forces a continuous limit; the price exists under gluing inequalities | `thm3a`–`thm3d`; `price_of_pointwise`, `price_of_ae`, `tilt_riemann_bounds`, `jump_refutes_SSM`; `price_exists_of_sub`, `price_interval` | `ChainSSM.lean`, `ChainTiltLimit.lean`, `ChainPrice.lean` | yes (D4: `price_of_ae` is the referee's, taken over) |

**The link: the chain theorems for `Face.P` itself** (`mathlib/GumpMath/Link*.lean`):

| statement | Lean name | file | refereed |
|---|---|---|---|
| **The five 9-cell faces, complete**: dominant QSD, the only one with λ > 0, positive; λ in the certified interval and ln τ (τ = E_μT) to ten digits; ln τ = Σ_i c_i with each cell's own death probability as its factor; equal prices within the classes of table automorphisms; two-sided decay at λ from every start that can survive | `hull3_full`, `torus103_full`, `torus113_full`, `strip13_full`, `patch13_full`; `hull3_complete` (adds survFrom = `Face.survival` and the dice bounds) | `LinkFaces.lean`, `LinkSurv.lean` | yes (second and third reviews; every price class as coarse as the numerics allow) |
| **The 12-cell torus (2,0),(0,2)**: unique dominant QSD, all twelve prices equal (ln τ = 12·c), ln τ < 1.9228·12; no λ interval | `torus202_full` | `LinkTorus202.lean` | yes |
| **Every wrapped face** (H,K),(0,D), H, D > 0, no hypothesis: all the clauses of the 9-cell theorems but the λ interval, ln τ = HD(c₀ + c₁ + c₂), one price per cell on rotation-invariant tori, ln τ < 1.9228·A | `torusNb_all`, `wrapped_full_all`, `wrapped_theorems_all`, `wrapped_area` | `LinkWrappedAll.lean`, `LinkWrappedArea.lean`, `LinkWrapped*.lean` | yes (third review: clean; checked on 208 tori and more) |
| **Every hull face** R, no hypothesis: dominant law, tilt identity with named factors, ln τ < 2.2165·A, survFrom = `Face.survival` | `cellsOK_hull`, `hull_theorems` | `LinkHull.lean` | yes (`ref-chain`, fourth review: clean; `hull R` has no cells for even R, so "every R" is every R with A > 0, i.e. odd R, as the rows say) |
| **Every hull face under `Lemma0F (hull R)`**: uniqueness, positivity, decay at λ, equal prices along every table automorphism; `Lemma0F` itself kernel-proved for R = 1, 3, …, 13 (3 to 84 cells), the triangle's rotation and reflection for R = 3, …, 13 | `hull_full_all`, `face_full_of`, `lemma0_of_cert`, `price_aut`, `hull_full_sym`; `hull1_lemma0` … `hull13_lemma0` | `LinkHull.lean`, `LinkFaceAut.lean`, `LinkHullCert.lean` | yes (fourth review: the certificates regenerate byte for byte from the referee's oracle-built tables; `autOK` rejects permutations that keep neighbours but not coins and the reverse; on hull 3 the prices are 0.0481050722 at the three corners and 0.3899000883 at the other six, as the classes claim) |

#### Added after the integration (2026-11-24)

| statement | Lean name | file | refereed |
|---|---|---|---|
| **Every hull face, no hypothesis**: `Lemma0F (hull R)` by a general proof for every R with A > 0, hence the dominant law unique among λ > 0, positive on every living state, decay at exactly λ, ln τ = Σ c_i, ln τ < 2.2165·A, survFrom = `Face.survival`, equal prices along every table automorphism | `hull_lemma0`, `hull_full_every` (`descent`, `enterT`, `walk_all`, `grow`, `step_TZ`, `step_U`, `aliveF_u`, `kc_le_four`, `stepN_mask`) | `LinkHullGen.lean` | no |
| **The triangle's six symmetries on every hull face**: the rotation and the reflection are table automorphisms for every R; equal prices along them | `aut_general`, `rot_aut`, `refl_aut`, `hull_prices_sym` | `LinkHullSym.lean` | no |

### What is not proved (as of 2026-11-24)

- **The price per cell.** The limit of ln τ/A is proved to exist only under hypotheses (gluing inequalities with
  defects, `price_exists_of_sub`; or pointwise convergence of the per-cell tilted energy, `price_of_pointwise`); no
  gluing inequality is known for the surrogate. **No lower bound** ln τ ≥ c·A (B2 of `THEOREMS.md`) for any infinite
  family; the upper bounds above are all there is, and they sit well above the truth.
- ~~Uniqueness on hull faces beyond R = 13~~ **proved after the integration**: `HullGen.hull_lemma0` gives `Lemma0F (hull R)`
  for every R with A > 0 by a general argument, so `hull_full_every` has no hypothesis, and `rot_aut`, `refl_aut` give the
  triangle's symmetries for every R (table "Added after the integration" above; refereed, `ref-chain` fifth review).
  Uniqueness on strips is not proved.
- **λ intervals beyond the five 9-cell faces.** The 12-cell certificate was generated (with the 48-element symmetry
  reduction, `DiceSym.lean`) but its build was killed at 12 GB in one declaration and ran over 25 minutes split; it is
  not committed. 15 and 18 cells need the transfer product of `qsd.c` with a correctness proof, not written.
- **The meetings of signals** (§31; REVIEW-signals-6 §3): they need a superposition lemma for two far-apart signals
  and outcome runs wider than the 64-box (the 128-box of `CallBox` or a moving window). Also not covered: the finite
  cell during a call, other seed places, "at no earlier generation" for the call law; that the nine signals are all
  of the train's rigid signals is not claimed.
- **That the surrogate is gump.** `Face.P` gives each cell private coins; gump over coins on its own cells beneath
  shares each coin between face cells. From the full R = 3 hull face the one-step laws differ by total variation
  0.33 (`ref-dice`, defect 5, measured exactly), and 12 of the 15 cells beneath that face lie on the hull's other
  faces. Every lifetime theorem here is about the surrogate.
- (SSM), the hypothesis of Theorem 3, is not proved (the chain agent's judgment, with reasons, is that it is false as
  stated: `notes/chain.md`). From 2026-11-18 and still open: T5 on tori; that 36 is the least two-layer sealed set;
  `gumpcheck`'s file parsing and printing.

**Is the Lean rule gump?** A proof in Lean is about Lean's definition of the rule. Two ties to the ground truth,
both run by `check.sh` [measured]:
- `gumpcheck cube` runs the Lean rule on the 2012 closed-cube seeds and prints the logs in `reference/golden/`
  line for line: sides 8, 9, 10, and side 11 through its 4,218 generations.
- `gumpcheck states` compares the Lean stepper with `reference/oracle.py` state for state: three soups, 60
  generations each, no mismatch; with one cell of one generation moved, it fails at that generation.
The stepper (`Gump/Finite.lean`) evaluates `Gump.step` itself, and **`stepFin_config` proves it equal to `step`**
(n steps equal to `run`), so what `gumpcheck` computes is the function the theorems are about; its file parsing
and printing are not proved. A wider differential test, `sh research/blast/lean/difftest.sh` (6 minutes) [measured]:
9,442 generations against the oracle with no mismatch, on every one of the 2^13 states of a cell and its twelve
neighbours for each orientation, 238 soups over nine densities, catalogued objects (a still life, two oscillators,
wire C, the rake gun), and the oracle's torus at seven sizes; 15 mutants of the rule (offsets, birth and survival
sets, parity tests) are each caught.

`STATEMENTS.md` (written by `statements.py`; 205 rows on 2026-11-24) puts each headline theorem's Lean statement,
verbatim, next to the sentence it is meant to be and says where the two differ in strength. `check.sh` fails if it is
stale (`python3 statements.py --check`: writes nothing, exits 1 on any difference; a referee had found it stale and
the check silent). Several proofs use `decide +kernel` (the kernel evaluates a decision procedure; no axiom is
added): `hex_check`, `cube_still`, an example in `Bits.lean`, the four `Signals` theorems, every census theorem, and
since 2026-11-24 every base run of the catalogue laws and every certificate of the Dice and Link modules. Nothing in
either package uses `native_decide`; there is no `*Native.lean` file.

**Refereed on 2026-11-24** (`research/blast/ref-lean/REVIEW.md`; the statements of 2026-11-18, not the proofs and
not the later files). No theorem broken: of the 50 rows, 36 say the same as their source, 7 say more and 7 say
less (three acknowledged; four T5 rows that did not say "no tori" and now do). Its own tests from the oracle
found no disagreement (55 checks), `collectAxioms` on all 1,782 core and 86 Mathlib constants found nothing
beyond the standard three, and a clean clone builds and passes. **What it did break was `check.sh`**: three of
its four comparisons with the oracle sat behind pipes and could not fail it, it did not run on a fresh clone,
and `gumpcheck states` passed on files that compared nothing. All three are repaired (the attacks are in
`research/blast/ref-lean/attack_gumpcheck.sh`).

Three more referees read the day's new files, each with its own code from `reference/oracle.py`:
- **`ref-tape`** (`research/blast/ref-tape/REVIEW.md`, three reviews, at 6be19d4, ba36f77, 40520c7). No theorem
  broken; the Lean objects are the catalogue's cell for cell; the laws hold on the oracle beyond the base cases, with
  their sharp boundaries; no axiom beyond the three in 3,556 constants. Defects and repairs: D1 `clock_every_length`
  is an existential that two short clocks side by side satisfy for N = 7 (repaired: `clockOf_period` names the
  object, the row says "less"); D2 `STATEMENTS.md` stale and `check.sh` blind to it (repaired: regenerated, and
  `statements.py --check` in `check.sh`); D3 three stale passages (repaired). The third review found one slip of
  prose: the odd-N base times of `lit_first` are 4, 8, 12, 16 in Lean's `Xb` convention (11, 15, 19, 23 counted
  from X0); corrected in the row and in `notes/tape.md`, still in the header comment of `Gump/ClockLitFirst.lean`.
  Not checked by it: the internal steps of the zone and base checks (`zonesLit_ok`, `smallOK_ok`, `oddCheck_ok`,
  `baseLitCheck_ok`, the readers' zone checks, the divider's `S`), the tape agent's scripts, sizes beyond N = 30
  and words beyond eight random words of 64 letters, `local_union`'s internal steps, k beyond 20 for the call law.
- **`ref-dice`** (`research/blast/ref-dice/REVIEW.md`, two reviews, at a65957b and 6f70d2d). Could not break the Dice
  modules: `Face.P` equals its own kernel on all 1,310,720 entries of the five 9-cell faces, its exact λ lie inside
  every certified interval, the checkers reject perturbed certificates. Defects and repairs: (1) the lemma cited for
  E_μT = 1/(1 − λ) did not exist (the referee proved it, `ref-dice/QsdSurvival.lean`; adopted as `DiceMean.lean`);
  (2) the bust share was the death flux's only through prose (now the theorem `flux_share`); (3) a reversed sentence
  in the notes (corrected); (4) the `hull3_lifetime` row overstated (it pins the decay rate, with constants 1384
  against a true 1.63; the row says so); (5) the surrogate is gump over *private* coins (said in the notes; total
  variation 0.33 from gump over shared coins); (6) `DiceSym` had no client in the Dice modules (said). Second review:
  no defect in the statements; two text slips (the `DiceBound3` header, the `torus113_bust_flux` row's 0.152, which
  is the hull's: on that torus from state 73 the share of all deaths is 0.934), corrected on 2026-11-24 by the
  integration. Not checked by it: no rebuild (the kernel checks are taken from the built oleans), no 12-cell or
  larger certificate, the agent's Python, `DiceMean.lean`.
- **`ref-chain`** (`research/blast/ref-chain/REVIEW.md`, three reviews, up to 55cf4a5). Proofs sound, hygiene clean,
  no number broke; the wrapped-face statements say what the source says, on a layer model confirmed against the
  oracle. Defects (first review) and repairs (f32bb82): D1 `bit_surrogate`'s local factorisation was existential, so
  "ln τ = Σ c_i" could hold with all prices but one zero (the factor is now named); D2 "some QSD" admitted the λ = 0
  point mass with ln τ = 0 (now `IsDominantQSD`); D3 |T| = HD unproved (`torus_card`); D4 `price_of_pointwise` asked
  convergence at the jump point itself (`price_of_ae`, the referee's, taken over); D5 the notes' list of the source's
  gaps overstated (corrected: none is a gap in the mathematics); D6 `lifetime_from_bounds` conditional on r < 1
  (`lifetime_from_bounds_K`); D7 rows (corrected; `kagome_sharp_bound` added). Second review: D1–D7 closed in the
  statements, the Link theorems say what their rows say about `Face.P` itself. Third review: clean; the generators
  rewrite the committed modules byte for byte. Not checked by it: the 19th digit of the λ intervals, a full kernel
  re-run of a reachability certificate (memory), `CellsOK` beyond 108 cells, tori above 12 cells for prices,
  `DiceMean.lean`. Fourth review (`LinkHull`, `LinkFaceAut`, `LinkHullCert` up to 5e8aa76, and `DiceMean`): clean.
  `Lemma0F` is true on every face checked and slightly stronger than uniqueness needs; false on a face where the law
  is not unique (`two_not_lemma0`). Not checked by it: prices on hull 5 (18 cells) and larger, `Lemma0F (hull R)` for
  R ≥ 15 (nobody claims it), `lntau_le_hull_all` (the dice referee's second review covers it), the rebuilt
  `LinkHullCert.olean` (it re-elaborated the source).

Not checked: the proofs are the kernel's. Every file of 2026-11-24 has been read by a referee. Nobody has checked these statements against the sources but their authors, the PI and the referees
named above. `set36` was found by a fresh SAT run; `ref-lean` compared it with `sealed.py minsat 2 7 36`'s set: the same up to the slab's
symmetries and even in-layer translations (`ref-lean/set36_compare.py`), not checked literally cell for cell.

## The climb

Each line is a goal at full size with a first move. Difficulty is a fact to be found out, not a reason to choose a
smaller goal; where a tool is missing from Lean's libraries, building it is part of the work.

1. **The rest of the structure theory.** Done on 2026-11-18: T6 in full, T5 on finite vessels, eventual periodicity,
   no spaceships, the speed limit, the symmetries, the stepper's correctness. Open: T5 on tori and the uncapped rule
   with its Goles–Olivos theorem; that 36 is the least two-layer sealed set; the torus clause of Theorem 3 on the
   torus itself; whether a set sealed in a thick slab can be bounded along a non-generic in-plane direction;
   `research/theory/thickness.md` §4 (thin slabs cannot sustain chaos: the percolation step).
2. **A certified census.** Still lifes, oscillators and sealed sets in bounded windows, found by SAT or search
   outside Lean and certified inside it (`decide`, `bv_decide` with its checked certificates). First move: the
   six faces of a cube are a still life; the 6-cell hexagon ring is sealed in one layer; the 36-cell set in two.
2b. **The catalogue's "for every N" laws as theorems** (proposed by the lead on pull request 39, with where each is
   stated most exactly; "a finite set of base runs plus an induction"). In the lead's order: (1) the tape theorem,
   `research/signals/README.md` §10; (2) a clock of every length, §11, `research/signals/prove_clock.py`; (3) the
   gun's line, period exactly 4 from generation 2N for every N ≥ 2, §21, `prove_line.py`, `prove_beam.py`; (4) nine
   rigid signals on the rake train, §30–35; (5) the unzip law, `research/signals/push8/README.md`,
   `prove_unzip8.py`, with `research/audit/REVIEW-signals-8.md` read first; (6) the call law,
   `research/audit/REVIEW-signals-9.md` §3, `research/audit/signals9/proof9.py`, which no referee has read: a
   formal proof would be its first. Objects are cell lists in `research/signals/objects/` and `push8/`, `push9/`.
   Foothold: `Signals.lineC_N_period_four` for N = 2, 3, 12, 13 and `Bits.oscCert_spec`; base runs of a few hundred
   cells are within the kernel's reach. Statements quantify over the whole lattice with finite support. If a base
   run is too long for the kernel, `native_decide` for base runs only, in a separate tier of the axioms table, each
   such run also in the differential test. First move: the tape theorem, then the gluing induction for (3).
   **Done on 2026-11-24, all six, in the kernel tier with no `native_decide`:** the tape theorem, the gun's line
   (preperiod exactly 2N), the clock of every length and from a single cell (exact period 4N + 2, entry exactly at
   N − 2), the nine signals, the unzip law in the review's sharp form (by a new argument, not the source's seam
   path), the call law whole (both parts, with a second bit box); and beyond the list the two readers, the beam and
   the divider. Open: the meetings of signals (§31: a superposition lemma for two far-apart signals, and outcome
   runs wider than the 64-box); the finite cell during a call; the divider for N = 3 … 7 (the oracle obeys the law
   there; the induction's base starts at 8).
3. **Finite vessels as Markov chains, with certified rates.** The dice surrogate and the noisy hull are finite
   chains with honest randomness. For a non-negative matrix Q and a positive vector v, Qv ≤ λv entrywise gives
   survival ≤ C·λᵗ, and Qv ≥ λv gives survival ≥ c·λᵗ: two inductions, no spectral theory. So a vector computed
   outside Lean certifies a two-sided bound on a death rate inside it, in exact rational arithmetic. First move: the 9-cell hull triangle of the
   one-layer dice surrogate, its rate in a proved interval set beside the exactly solved value (ln τ =
   2.4837157463, reproduced by the outside audit): the first theorem in the repository about a lifetime.
   **Done on 2026-11-24:** that theorem (`hull3_tau`, λ to 19 digits, ln τ in (2.4837157463, 2.4837157464)) and four
   more 9-cell faces. Next: 12 cells (the certificate exists; its symmetry check is the cost: check invariance under
   two or three generators rather than all 48 automorphisms), then the transfer product of `qsd.c` with its
   correctness proof for 15 and 18 cells, then the noisy hull.
4. **The blast's theorems** (`rigour/THEOREMS.md`): Lemma 0, Theorem 1 (ln τ ≤ 2.509·A), the tilt identity,
   Lemma R, the seam identity, and Theorem 3 with its hypothesis proved or refuted rather than assumed.
   **Done on 2026-11-24** on an abstract killed chain and then for `Face.P` itself: the tilt identity on every face;
   Theorem 1 at 2.51·A everywhere, 2.2165·A on every hull face, 2.2412·A and 1.9228·A on every wrapped face; Lemma 0
   with its geometry and one price per orientation on every wrapped face; on hull faces under `Lemma0F`,
   kernel-checked to R = 13; Lemma R; the seam identity (its modelling step a hypothesis); Theorem 3 as an
   implication, and a weaker hypothesis (pointwise convergence of the per-cell tilted energy) proved sufficient.
   Open: `Lemma0F (hull R)` for every R (the certificate's construction is uniform in R; its formalisation is the
   next move), Lemma 0 on strips, and (SSM) itself.
5. **Both exits as theorems.** That a wrapped face of the surrogate dies by the bust and a rimmed one by the fade
   is measured and exactly computed at small sizes. Prove it for all sizes: a lower bound on the bust's share on
   wrapped faces, an upper bound on rimmed ones.
   **Done on 2026-11-24 at 9 cells:** the bust carries 0.936852–0.936853 of the death flux on the torus (1,1),(0,3)
   and 0.017017–0.017018 on the hull triangle (`torus113_bust_flux`, `hull3_bust_flux`). All sizes: open.
6. **The price.** A proved interval for the cost per cell of a face's death, first for the surrogate (the limit
   exists by Theorem 2's local sum; pin it between certified bounds from finite strips), then for gump under
   noise at depth, then with the noise taken to zero.
   **State on 2026-11-24:** upper bounds only (Theorem 1's constants, all well above the truth); the limit exists
   under gluing inequalities with defects (`price_exists_of_sub`, `price_interval`) or under pointwise convergence of
   the tilted energy (`price_of_pointwise`), and no gluing inequality is known for the surrogate; the lower bound B2
   is open for every density. The surrogate of these theorems gives each cell private coins: it is not gump over
   shared coins (total variation 0.33 in one step from the full 9-cell hull face, `ref-dice`).
7. **The summit.** The face law for gump with its constant, and why a hull face and a wrapped face pay different
   prices at the sizes measured, as theorems.

## For a contributing agent

Pick a line above, or add one that is larger. State the theorem in Lean first, in the terms of `Gump/Basic.lean`,
and get the statement read by someone else before proving it. A result counts when `check.sh` passes: no
`sorry`, no `native_decide` unless the README says where and why, axioms printed in `Axioms.lean`. Say what was
not checked. If the libraries lack what the proof needs, write it.
