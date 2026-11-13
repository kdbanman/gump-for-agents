# Board (critic)

_Kept by the critic. Last update: 2026-11-13, after the replies to path, source and counting, round 1 (the
round 1 report of probability is written and not yet read). Scripts named here are in `critic/lab/`; run them from that directory. "Checked" means I
re-derived or recomputed it; "read" means I compared the statement with its source and did nothing more.
Proofs and commands behind every "checked" are in `critic/journal.md`._

## Who is here

| who | directory | toolkit | state |
|---|---|---|---|
| probability | `swarm/probability/` | dice in place of chaos: particle systems, coupling, percolation, contours | round 1 written; reply pending |
| counting | `swarm/counting/` | the map with a trapdoor: exact counts, transfer matrices, escape rates, entropy | round 1 answered (`to-counting.md`) |
| path | `swarm/path/` | least unlikely route to empty: large deviations, effective dynamics, structure | round 1 answered (`to-path.md`) |
| source | `swarm/source/` | deterministic systems that are provable random sources; what the bulk would have to satisfy | round 1 answered (`to-source.md`) |
| librarian | `swarm/library/` | primary papers: `shelf.md` (one line per source), `notes/`, `requests.md` (append-only, anyone) | first pass finished: 59 sources, ten notes files |

Where lines could meet, which I watch: the probability of an empty edge under a product measure (a transfer
matrix about a dice model); quasi-stationary measures and escape rates; the face game with free cells beneath;
the dice model itself (probability fixes it, source drives it deterministically, counting counts its trapdoor);
**hypotheses on equal-time one-step kernels** (path's Theorem P and source's Lemma 3 are the same projection:
path holds certificates on the face population, source holds classes of drive kernels and deterministic relatives).

## Errors in the problem statement (and in the sources it lists)

None of these changes the problem. Each is a number or sentence a proof could lean on and should not.

- **E1. The 2D law is not a straight line with slope 0.416.** Refit of the seven committed points
  (`research/toy2d/data/law_cross2_B34S234.json`): the line 0.7295 + 0.4160·L has χ² = 28.9 on 5 degrees of
  freedom. Local slopes between successive sizes: 0.442, 0.407, 0.428, 0.400, 0.421, 0.382 (± 0.006–0.015).
  With a ln L term the coefficient of L is 0.374 ± 0.009; with a 1/L term, 0.395 ± 0.005; from L ≥ 20 alone,
  0.410 ± 0.003. **The 2D target is 0.36–0.42, not 0.416.** (PROBLEM.md now says so.)
- **E2. Gump: the slope does not fall.** Verified octahedral data are A = 30, 45, 63, 84 (ln τ = 6.804, 9.819,
  13.633, 18.077 ± 0.003, 0.003, 0.008, 0.054); local slopes 0.2010, 0.2119, 0.2116. A = 108, 135 (23.376 ± 0.031,
  29.34 ± 0.25; GPU ensembles) are now **reviewed** (`research/audit/REVIEW-gpu-pr8.md`: tables re-derived, kernel
  emulated exactly on a CPU, an independent CPU run at A = 84 gives 18.154 ± 0.025; no second implementation at
  those sizes; read, not checked by me). Local slopes there: 0.218 from the GPU's own A = 84 value, 0.221 from the
  verified one; then 0.221. The cost per cell is still rising at A = 135. The old fit 0.2077 + 0.55/A misses the
  A = 45 point by 28 standard errors. Rim-free (periodic slab) faces: 0.2088 ± 0.0009, A = 27–90.
- **E3. Octahedral faces of these sizes are mostly rim** (checked, `checks_round0.py`). A face of the hull of
  radius R = 2k − 1 has A = 3k(k+1)/2 cells: 3 corner cells with 4 neighbours inside the vessel, 6(k−1) rim
  cells with 7, and A − 6k + 3 interior cells with 9. Interior cells: 9 of 30, 18 of 45, 30 of 63, 45 of 84,
  63 of 108, 84 of 135.
- **E4. "Overcrowded-and-alive events" is loosely worded.** The event (O1 in `threshold.md`) is: n ≥ 6 at time t
  *and alive at time t − 1*. The face figures 0.073 and 0.035 come from one vessel (R = 9, 30 soups), where "face"
  means the outermost *live* layer and the 773 layer deaths include every later, smaller layer. The 0.035 is an
  average over the last 50 generations; it does not by itself show a 50-generation precursor.
- **E5. "Symmetric faces: slope ≈ γ/6" was imposed, not measured.** Free fits give 0.024–0.044 (fluct README §3).
  New, reviewed (GPU; CLAIMS GP2, grade B−, read): ln τ = 21.903 ± 0.031 and 24.175 ± 0.072 at A = 759, 828
  (cube-centred), 22.409 ± 0.040 at A = 759 (vertex-centred). Local slope 759 → 828: 0.0329 per cell, i.e. 0.197
  per independent cell (×6), against 0.163 from the A/7.7 law of A = 198–513: symmetric faces are cheaper per
  independent cell than asymmetric ones and the gap is closing with size. The death rate in those cube-centred
  runs falls with age.
- **E6. The 2D symmetry ratios 0.42 and 0.50 have different baselines** (0.1733/0.41 in strips; 0.171/0.343 in
  boxes). The symmetric slopes are equal; the asymmetric baselines differ.
- **E7. The lineage rows (slow variable; 1% double peels) were measured on O_h-symmetric states only.**
- **E8. In the 2D strips the edge wait is a competing hazard.** At depth 16 the strip is cut across by three dead
  columns far more often than it loses an edge (cuts + interior firewalls against edge deaths: 4,768 / 898 at
  L = 28; 22,252 / 676 at L = 32; 85,256 / 495 at L = 36), and a cut replica is reseeded. See E12.
- **E9. In 2D not every death is "the tail reaching one cell".** Share of edge deaths whose edge had ≥ 7 live
  cells one generation earlier: 22% at L = 12, 10% at L = 16, 5% at L = 20, 2% at L = 24, ≤ 1% from L = 28. A
  fully live row dies at once iff no cell has both cells beneath it dead. The one-row dice model has the same
  channel (30% at L = 8, 7% at L = 18, exact; lab L0b.4).
- **E10. False "[proved]" statement in `research/theory/exponent/theorems.md`, Lemma A (c):** "A gump face can
  always die in one generation given suitable layers beneath." Counterexample in the interior of a face: in the
  layer x + y + z = 13 let (4,4,5), (4,5,4), (5,4,4) and (3,4,6) be alive, their other face neighbours dead. (4,4,5)
  has three live face neighbours and dies only if all three cells beneath it are alive, among them (3,4,4);
  (4,5,4) has two and dies only if all three beneath it are dead, among them (3,4,4). The cube lemma (lemma
  exchange) gives the general form. Exhaustive: 180,615 of the 262,144 configurations of the R = 5 face and 187 of
  512 at R = 3 cannot be emptied in one generation; all of them can in two (lab L0b.3).
- **E11.** Closed: the starting points are now in PROBLEM.md; see the next section.
- **E12. The facts table leaves out the second way chaos dies, and with it the limit of the area law.** In a
  periodic slab three consecutive layers of another diagonal form a sealed band that wraps the torus (checked):
  for an N × N torus about 4.5·m·N cells (13N at m = 3, 36N at m = 8, 54N at m = 12) against 3N² for a face,
  so the band is the smaller sealed set once N > about 1.5·m. Measured (notebook 2026-11-12, `research/peeling/`;
  read, not re-measured): slabs with m = 3–6 die by such bands, ln τ_fw ≈ −1.4 + 0.54·N·m + 0.22·N (about 0.12
  per band cell); the first event switches from band to face at m ≈ N; elongated tori die by bands. So **"the
  lifetime is exponential in the area" is a statement about hulls, and about slabs only while the thickness is at
  least about the width**; at fixed thickness it must fail as A grows. The verified slab law (m = 8, A = 27–90) is
  inside the face regime. The 2D analogue is E8. Two prices per dead cell (0.21 in a face, 0.12 in a band) are a
  fact a theory of "cost per cell" has to produce.
- **E13. "An i.i.d. outside gives too large a constant" is true of the 2D rule only.** 2D, one row over dice:
  0.52–0.53 per cell (exact, lab L0b.4) against 0.36–0.42. Gump, one face layer over dice (the exponent study's
  sampled values, unchecked): ln τ = 5.88, 8.73, 12.46 at A = 30, 45, 63 against 6.80, 9.82, 13.63, i.e. about one
  nat *shorter*-lived with nearly the same slope (0.190, 0.207 against 0.201, 0.212); at depth 2 and 3 the slope is
  too large (0.236–0.242; 0.228), at depth 4–5 it agrees. The gap has no single sign.
- **E14. "Death takes a few generations and happens everywhere on the face at once" is two statements of
  different standing.** 2D: the last two generations go from about nine cells to two to none at L = 12–24, with
  a sag of ≤ 12% over the ten generations before (exponent study, sampled; unchecked): at 2 cells per generation
  nothing crosses those rows in that time. Gump: **the collapse is not of fixed length.** From the existing
  pre-death histories (lab L1.3): the lag at which the mean population of a dying face is half the living mean is
  3.2, 4.7, 5.9, 6.8 generations at A = 30, 45, 63, 84, and looking back from the death the mean population is one
  curve at every size until it saturates (1.6, 3.5, 6.4, 9.7, 13.6, 17.6 at lags 1…6). The farthest two cells of
  those faces are 5, 6, 7, 8 generations apart (`startpoints.py crossing`). "Ordinary until −16, then 10–12
  generations" (fluct README) describes the largest of these faces, not a size-independent plunge.

## The lead's starting points: what I checked

**probability.**
- "The cap breaks monotonicity; T5 says where": true. Gump = the monotone threshold rule except at cells with
  n ≥ 6 (2D: n ≥ 5). Two exact companions (lemma exchange, "capped against uncapped"): the uncapped rule bounds
  the capped one from above only; and no monotone map lies below the capped rule except ones that die in two
  generations. So **"the cap as a bounded perturbation of a monotone rule" is badly posed as a comparison on the
  whole state space**; it needs a named class of configurations, and the cap is not rare where it would be used
  (40% of bulk cells and 13.5% of the cells of the outermost live layer are overcrowded each generation).
- "The face layer over fresh random layers, where an empty face is absorbing by T2": true (a dead face cell sees
  at most 3 cells beneath; 2D: 2). This is the exponent study's one-row model; it is defined below as D2 / D3 and
  is now exact for the 2D rule (lab L0b.4). Not in the graveyard: item 6 is about an *unknown* outside, item 7
  about this model's constant. No lower bound e^{cL} is proved for it. Two structural facts: in D2 the cells
  update independently given the row, with two deterministic transitions ((dead, k = 0) stays dead; (live, k = 2)
  stays alive); in D3 the noise is shared inside each cube triple and independent between triples (cube lemma).

**counting.**
- "For an invertible relative the law reduces to counting the trapdoor": **void.** In a bijective relative
  nothing is absorbing: the second-order lift of gump is a bijection confined to the same hulls, "face empty now"
  has frequency exactly 2⁻ᴬ, and no state ever enters "face empty twice running" (counting's Lemma 2; checked).
- The bijection lemma is true **if a point that never falls counts as T = ∞** (checked: proof, and every
  permutation of ≤ 7 points). Over the points that do fall the bound is |X′|/(2|H|) − 1/2 with X′ the cycles that
  meet H. The union bound #{T ≤ t} ≤ (t + 1)|H| is stronger, bounds the law and not only the mean, and holds for
  any invariant measure of any map.
- "What replaces the uniform measure": in a finite vessel every invariant measure of gump or of the 2D rule
  gives the trapdoor measure zero (face death is irreversible; lemma exchange). An invariant measure is therefore
  not the replacement, in any finite vessel.
- "Countable exactly for small k": done for the 2D rule at k = 1, 2 (counting's Theorem 3; lab L3.1, L3.2): the
  from-soup probability that the edge is empty at generation k decays exactly like e^{−c_k L} with c₁ = 0.551535,
  c₂ = 0.467693. k = 3 needs 2³⁶ window states (not by a plain transfer matrix). Gump, k = 1: a condition cube by cube
  (cube lemma), so a two-dimensional count; exact on hull faces by enumeration, on strips by transfer matrix.
- "Too large a constant": see E13.

**path.**
- "A rare configuration, not a slow path; a few generations; everywhere at once": see E14. In gump the collapse
  lengthens with the face (half-way lag 3.2 → 6.8 generations from A = 30 to 84).
- "γ = cost per cell of the cheapest killing pattern, priced by the chaotic phase's own space-time measure": not
  yet a statement, because the measure is not defined. In a finite vessel no invariant measure carries chaos
  (lemma exchange). The candidates are a quasi-stationary law (exists for dice models; for the deterministic
  rule only as something sampled) or a limit of soup measures on an infinite face (exists along subsequences;
  uniqueness unknown; there the face never dies and what is priced is an empty window, the exponent study's
  E(ℓ)). The second choice needs its own bridge from windows to finite faces.
- "No dead patch smaller than a whole face is protected": true in hulls for R ≤ 10 (exact) and in slabs while
  N < 1.5·m; **false in wider slabs and in 2D strips** (E12, E8), where death does nucleate on the band.
- "…so death cannot nucleate and spread": **does not follow.** "Not sealed" says only that *some* outside revives
  a cell (thickness.md Lemma 1, converse). Nucleation is about the typical outside. What is measured on the side
  of the conclusion: gaps in a 2D edge close from their ends (toy2d §4.3), holes in a face heal from the rim.

**source.**
- "Bipermutive, uniform product start ⇒ one cell's states over time are i.i.d. uniform": true, and more is true
  (lemma exchange, "permutive sources"; checked by proof and enumeration): permutivity in one extreme variable e
  is enough, in any dimension, and the whole field {x_p(t)} is i.i.d. for any set of cells P with no two differing
  by a multiple of e. Two rows beneath an edge need e to reach two rows per generation. The primary statement is
  not on the shelf yet (requests item 5).
- "So a deterministic system can feed exact dice to a boundary": **only from an unbounded reservoir.** Each die
  uses up one fresh initial cell; N random bits give at most N bits of exact dice. A confined vessel cannot supply
  exact dice for e^{cA} generations, so aim (a) is a statement about a half-space, not about a relative that is
  confined as gump is.
- "Whether confinement and the firewall can be kept": inside a binary permutive source with a quiescent dead
  state, no (a lone live cell p makes p − e alive). The empty face over the source stays absorbing.
- "By T5 … freezes within 26N + 1 steps": true with "freezes" = "reaches period ≤ 2", and under the weaker
  hypothesis "no O1 event" (checked, journal §7). T5 locates where *energy* enters. A finite deterministic map
  creates no randomness anywhere: it loses 1.7–2.5 bits per generation in the smallest vessels (lab L0b.7).
- "The critic will point you to the dice model": D2 and D3 below, until the probability line fixes another.

## Definitions a proof must match

- **Gump.** Cells = doubled coordinates with exactly one odd entry; 12 neighbours (AUTOMATON §2); B45/S345 =
  "alive next iff n + x ≥ 4, except n ≥ 6 dies" (checked). **Vessel** = diagonal hull |d·(p − c)| ≤ R, c a cube
  centre (R odd) or a vertex (R even); the outside is dead for ever (T2). **Face** = the cells of the hull with
  d·(p − c) = R for one signed diagonal d (8 faces). A face **dies** at the first generation at which it has no
  live cell; it then stays empty. **Slab** a × b × m: m consecutive {111} layers modulo the translations
  (2a, 0, −2a), (0, 2b, −2b); two faces of 3ab cells (`startpoints.make_slab`).
- **2D rule.** Neighbours (±1,0), (±2,0), (0,±1), (0,±2); B34/S234 = "alive next iff n + x ≥ 3, except n ≥ 5
  dies" (checked). **Strip** W × L: W rows, L columns, periodic along the row; **edge** = row 0 or row W − 1 (the
  measured law has W = 16). **Box**: no wrap; four edges.
- **τ is a hazard, not a mean over initial states.** h = (face deaths) / (face-generations of exposure), counted
  over soup-started replicas older than T0 (200–300 generations) that have not settled into a cycle and, in
  strips, have not been cut; τ = 1/h. A mean of the death time over all initial states does not exist: in every
  small vessel enumerated a positive fraction of states never loses a face or edge (20.0% of the states of the
  3 × 6 strip, 24.7% of the 4 × 5 box, 22% of the R = 2 gump hull). A theorem has to say which τ it bounds, and in
  which vessel (E12).
- **Sealed** (in a vessel V): every cell of W has at most 3 (gump) or 2 (2D) neighbours in V \ W. Sufficient,
  not necessary, for a dead W to stay dead.
- **Dice models already in the repository** (names fixed here so that lines can point at one object).
  **D2(L, ρ)**: a ring of L cells follows the 2D rule; the two cells beneath each cell are i.i.d. Bernoulli(ρ),
  redrawn every generation; death = empty ring (absorbing). **D2(L, ρ; w)**: the same with w rows following the
  rule over two rows of dice; death = row 0 empty. **D3(face, ρ; w)**: the top w layers of a hull face or of a
  periodic face follow gump, the next two layers are dice. These are `toy_model`, `gump_model`,
  `gump_slab_model` of `research/theory/exponent/xp.py`. For a dice model τ = 1/(1 − λ), λ the Perron eigenvalue of
  the kernel on living states, is well defined (Darroch–Seneta).

## Facts table of PROBLEM.md: what I checked

| row | status |
|---|---|
| gump ln τ at A = 30…84 | read against fluct README and `fluct/data/qsd_summary.json`: reproduces. See E2 |
| GPU numbers at A = 108, 135 | reviewed elsewhere (read: `research/audit/REVIEW-gpu-pr8.md`); not recomputed by me. See E2 |
| straight tail, ratio 0.6–0.7, h ≈ 0.6·P(1), 62% from one cell | recomputed from `qsd_summary.json`: h/p₁ = 0.645, 0.613, 0.601, 0.594; p_k/p_{k+1} = 0.65–0.69 (k = 1), 0.47–0.56 (k = 2), 0.74–0.87 (k = 3), 0.60–0.70 (k = 4…7). The ratio at k ≥ 4 drifts down with size: "size-independent end-game" holds to about 10% |
| favoured 3-cell state is a kagome triangle | read (notebook 2026-11-13: 38% of three-cell faces, 1,263 face-generations, one vessel R = 9). It is the triple of the cube lemma: the three faces of one cube |
| 2D law, tail, h/p₁ 0.52 → 0.27 | recomputed from the data file: reproduces; see E1, E8, E9 |
| symmetric gump faces | read; see E5 (with the new points at A = 759, 828) |
| 2D symmetry ratios | read; local slopes recomputed from the committed files (lab L1.6, L3.7); see E6. The C4 slope is measured under heavy settling |
| overcrowding rates | read; see E4. Not re-measured |
| sealed sets: 6-ring, 36-cell set, none in ≥ 3 layers; face smallest in a hull | proof of Theorem 3 re-derived; 6-ring minimal by search; 36-cell set not checked; hulls exact to R = 10; see E12 for slabs |
| slow variable; 1% double peels | read; see E7 |
| plunge 10 generations; 2D flash | read; see E14 |

## Who is using which idea

| idea | who | state |
|---|---|---|
| the face as a system driven through b(c); rim lemma (holes heal only from the rim; recovery at speed ≤ 1) | path (L1) | proved, checked |
| a one-step inequality for a statistic of the face bounds the hazard, no Markov property (Theorem P) | path | proved, checked. As first stated (geometric φ) its hypothesis is false; with φ free it holds on the measured rows with a loss of 4.0 nats at every size (lab L1.2) |
| sealed sets = complements of bootstrap-closed sets; isoperimetry of sealed sets in hulls (aim A) | path (L3, L4) | L3, L4 proved, checked; A exact to R = 10 (lab), open in general; false in wide slabs (E12) |
| one exponent 0.345 for the 2D rule in every geometry, a ring carrying a power of L (G1) | path | guess from committed data; exam E1 filed. D2 on a segment is exact (lab L1.5): undecided |
| flash or front; the remnant | path (G2, exam E2) | gump: not a flash of fixed length (E14). 2D: open |
| finite-horizon exponents from soup: λ(T ≤ k) = tr(M_kᴸ)/2^{(2k+1)L}, c_k decreasing in k, c_∞ = lim c_k; conjecture C1: the measured exponent of each geometry is c_∞ | counting (Theorem 3, C1) | theorem proved, checked (c₁, c₂ exact); C1 a guess, in tension with three measured slopes |
| boundary conditions and symmetry at a fixed horizon: free ends ≥ ring, mirror ≥ half, C4 and diagonal = no symmetry | counting (Prop. 4) | proved, checked at k = 1 on small boxes; c⁰_k = c_k verified for k = 1, 2 (lab) |
| the second-order lift as an invertible relative | counting (Lemma 2) | proved, checked: its faces never die |
| collision entropy of the top three rows as a countable hypothesis (claim 15) | counting | inequality proved; hypothesis fails from generation 2 in every vessel that can be enumerated (lab L3.5) |
| a deterministic relative that is a dice model exactly: true rule in the top w layers over a deep-permutive bulk, feedback allowed (R_w(Q), "gump on parity") | source (Lemma 1) | proved, checked. Needs a half-infinite reservoir |
| the death law of a face depends on the bulk only through the equal-time conditional law κ_t of the two layers beneath given the w layers above; a class 𝒦 of such kernels on which the dice theorem holds (Aim B) | source (Lemma 3, C9) | Lemma 3 proved, checked; 𝒦 is a goal, nothing proved |
| entropy accounting: what a finite vessel cannot supply | source (Lemma 2) | proved; excludes conditioning on the whole past only (reply, item 2) |
| threshold lemma with weights decaying in space; a threshold bulk is not a source | source (Lemma 4, Cor. 4a, 4b) | proved, checked; constants poor (C_U ≈ 1.4×10⁶ per cell) |

## Graveyard: ideas already tried here and dropped, with the reason

1. **Extrapolating the tail to n = 0** from n/A ≥ 0.1 (quadratic: off by 0.5–0.8 nats; Gaussian: 2–7 nats). The
   tail is straight near zero and must be measured there. (fluct README §1.)
2. **n as the reaction coordinate; splitting along n.** n removes 16–18% of the uncertainty about die-or-recover.
   Forward-flux sampling gains nothing: clones differing by one cell have 55–95% correlated fates. (fluct §2.)
3. **"Exponentially decaying correlations ⇒ exponential-in-area wait"** (PROGRAM M2 as worded). Invalid: mix a
   measure with decaying correlations with weight e^{−√L} on the empty row; every covariance moves by ≤ 4e^{−√L}
   and P(empty) ≥ e^{−√L}. A ratio (ψ-type) mixing bound is what multiplies. (Checked.)
4. **Random map with killing** (PROGRAM E2): predicts an immortal basin of order τ²/2^N. In small vessels the
   basin is 5–94% of all states; most immortal cycles are debris of period ≤ 2.
5. **Energy arguments for freezing or for a critical drive rate.** One-layer oscillators of periods 3–12 balance
   drive and dissipation exactly; the threshold lemma is false on infinite configurations.
6. **Block construction for an edge driven by an unknown outside.** The exponent study reported it failing at the
   first step and gave two reasons. Only the second stands. The comparison theorem (Durrett, Ten lectures, Thms
   4.1–4.3; `library/notes/nonmonotone.md` §1; read in the note) assumes nothing about monotonicity: it needs a
   set H of block configurations and a good event of probability > 1 − 6^{−4(2M+1)²} that works **for every
   configuration outside the block**. That uniformity over the outside is the obstruction: an unknown outside
   contaminates two cells per side per generation. With dice beneath, the adversary is only the rest of the
   same row. Bramson–Ding–Durrett carry out a block construction for a non-monotone process (same note, §3).
   The comparison is along one direction: for a finite chain of m blocks it gives e^{cm}, a side, not an area.
7. **Shallow dice models as a formula for the constant.** 2D, one row: 0.52–0.53 (exact); three rows still 10%
   high; gump at depth 3 misses by 0.3–1.0 nats; depth 4–8 agrees (sampled, unchecked). See E13.
8. **The stabiliser rule for symmetry** (exponent ÷ order of the face's stabiliser): wrong as a complete account
   (four-fold rotation fixes no edge and lowers the slope by 20%).
9. **0.416 = 2 × 0.208.** See E1.
10. **0.2077 as gump's asymptote.** See E2.
11. **Cubes outlive their ensembles / lineage memory.** Post hoc; not a fact to explain.
12. **"The plunge lengthens with L in the 2D rule."** Reported false (two-generation flash; unchecked).
13. **"A gump face can die in one generation whatever its configuration."** False; see E10.
14. **A monotone process below the capped rule.** Any monotone map H ≤ G has H∘H = ∅ (checked). A comparison from
    below must leave the full state space.
15. **Exact dice from a confined deterministic source for the whole lifetime.** Entropy: N cells give at most N
    bits of dice; lifetimes are e^{cA}. Exact transfer needs a reservoir that deep (source Lemma 2 states it as
    Σ_t H(b_t | whole past) ≤ N). This excludes properties that condition on the whole past, not on a window.
16. **"No small sealed set ⇒ death cannot nucleate."** Not an implication (sealed = safe against every outside),
    and its premise fails in wide slabs and strips (E12).
17. **Reading a slope from exact data at L < 15 in the one-row dice model.** The step of ln τ per cell oscillates
    between 0.43 and 0.62 for L = 8–14 before settling near 0.52–0.53 (lab L0b.4).
18. **Theorem P with φ = r^{min(n,K)}** (path's hypothesis H as first stated). Rows n = 1, 2 do not contract for any
    r ≤ 0.9, in gump's measured table and in D2: from one cell the face dies with probability 0.37–0.41 (D2: 0.28)
    and does not drift up. The first three or four values of φ must be free (lab L1.1, L1.2).
19. **An exact quasi-stationary law, or an exactly geometric wait, for the deterministic rule in a finite vessel.**
    None exists (lemma exchange, "trapdoors" (v)). "Memoryless" there is an approximate statement about a window
    of times; exact statements need dice or an infinite system.
20. **An invertible relative with a lifetime law.** A bijection of a finite set has no absorbing set that is
    entered from outside; the face of the second-order lift never dies (counting Lemma 2). The uniform measure
    gives frequencies of "empty now", not lifetimes.

## Lemma exchange

Usable by all. "Checked" = by a critic; the journal has the proof or the command.

- **T2, T3 and 2D analogues** (checked by offsets): a dead cell beyond an empty outer layer sees ≤ 3 (gump) or
  ≤ 2 (2D); three dead layers or rows are permanent, two are not.
- **T5** (checked: identity re-derived): ΔE = D − Q; with no O1 event from some time on, period ≤ 2 within 26N + 1
  steps. Rests on Goles–Olivos only for its name; the proof in threshold.md §2 is self-contained. (Primary source
  not on the shelf: requests item 7.)
- **The cube lemma** (checked: proof by offsets; `startpoints.py triangles`). A face layer is the disjoint union
  of triples, each the three faces of one cube that lie in the layer (a kagome triangle of one of the two
  orientations, one cell of each normal axis; hull rims included). Beneath a triple lie the other three faces
  u_x, u_y, u_z of the same cube (one layer in) and three private cells v_x, v_y, v_z (two layers in), and the
  number of live cells beneath the face cell of axis a is **b_a = u_b + u_c + v_a**. Nothing is shared between
  cubes. Of the 64 triples (b_x, b_y, b_z) exactly 40 occur; (3, 0, ·) does not. The three corner cells of a
  hull face have only two cells beneath, both shared: they have no private cell.
- **Rim lemma** (path L1; checked): a dead face cell all of whose in-face neighbours are dead stays dead whatever
  lies beneath. So the live set of a face spreads at in-face speed ≤ 1 and a hole is refilled only from its rim.
- **Theorem P** (path; proof checked). For any process, any statistic Z of it, any 0 ≤ φ ≤ 1: if at every time of a
  window P(death next | Z) + E[φ(Z′); still observed | Z] ≤ a·φ(Z) + ε, with censoring rate ≤ s̄ and a + ε ≤ 1 − s̄,
  a < 1 − s̄, then the hazard is at most ε(1 − s̄)/(1 − s̄ − a) after a burn-in. No Markov property is used. Statement
  and proof: `path/journal.md` entry 3.
- **Sealed = complement of a bootstrap-closed set** (path L3; checked): the unsealed region V \ K(t) is the
  θ-neighbour bootstrap closure of the live set and never grows. **Top-layer rigidity** (path L4; checked): a cell
  in the top layer of a sealed set whose three upward neighbours are in the vessel has all its other neighbours in
  the set.
- **Capped against uncapped** (checked). Gᵗ(S) ⊆ Fᵗ(S) for the uncapped monotone rule F, also with shared dice.
  Any monotone H ≤ G satisfies H(S) ⊆ G(all alive) = the six vertex cells of a cube-centred hull, the four
  corners of a box, nothing in slabs, strips, tori, vertex-centred hulls; and H∘H = ∅.
- **Finite-horizon law for the 2D rule** (counting Theorem 3; proof checked; exact checks on strips). From the
  uniform soup, in a strip with ≥ 2k + 1 rows, P(edge empty at generation k) = tr(M_kᴸ)/2^{(2k+1)L} ≤ m_k e^{−c_k L},
  M_k a 0/1 matrix on windows of 4k columns of rows 0…2k; c_k is also the exact decay rate of empty windows of the
  infinite edge at generation k; 0 < c_{k+1} ≤ c_k < ln 2. **c₁ = 0.551535, c₂ = 0.467693** (density 0.472: 0.489963,
  0.4671). Box edge (free ends): the same count with closed walks at the all-dead window, and the same exponent
  for k = 1, 2 (its class is dominant). Statement and proof: `counting/journal.md` entries 4, 5. This is a law at
  fixed age as L grows; it is not the measured law (the bound is useful only while k ≲ √L).
- **Lone-cube guard** (counting, entry 4; argument read): the six faces of a cube whose top faces lie in a face
  layer, alone in a dead box of half-width 2k + 2, keep that face alive for k generations whatever is outside the
  box. Hence for a slab face P(dead by generation k) ≤ e^{−c⁻_k A} from soup, c⁻_k > 0 for each k.
- **Symmetry inside a light cone** (counting Prop. 4(e); read): under a G-symmetric soup, a set whose
  k-generation cone meets each G-orbit at most once has the same law as under the free soup.
- **Trapdoors** (checked). (i) Bijection, T = ∞ off the cycles meeting H: mean T ≥ |X|/(2|H|) − 1/2.
  (ii) Any map, any invariant μ: P_μ(T ≤ t) ≤ (t + 1)μ(H). (iii) Finite vessel, H_k = {face non-empty now, empty k
  generations later}: μ(H_k) = 0 for every invariant μ. (iv) Uniform start, any map:
  P(T ≤ t) ≤ Σ_{s ≤ t} |F⁻ˢ(H)|/|X|. (v) A map of a finite set with a hole has no conditionally invariant
  probability with 0 < λ < 1 (the librarian's remark in `notes/escape-rates.md` B1; checked: every point of the
  support has a preimage in the support, so the support contains a cycle, and around a cycle of length k
  μ(y) ≤ λ^k μ(y)).
- **Local threshold lemma** (source Lemma 4; proof checked; identity and inequality verified on every pair of
  states of the hull R = 2v and of the 2D box 3 × 4, and term by term over every local picture). With weights
  a_i = λ^{−d_i} (d any 1-Lipschitz function on the cell graph, 1 < λ² < 4/3; 2D: < 3/2) and S = Σ a_i² < ∞:
  m·Σ_{mismatches that are not O1} a_i² ≤ (12λ + 1 + θ′)S + c′·Σ_{O1 events} a_i², on finite or infinite vessels.
  **Corollary (settles threshold.md §6):** under the uncapped rule on the infinite lattice every cell has at most
  C_U mismatches, uniformly in the configuration, so every cell is eventually of period ≤ 2; a threshold bulk
  has entropy rate zero at any finite set of cells. Statement and proof: `source/journal.md` S5.
- **Starvation** (checked, two lines): in a face with at most three live cells no live face cell is overcrowded
  (k ≤ 2, b ≤ 3). So in a death from n ≤ 3 (94% of gump's measured deaths) every cell dies with n ≤ 2.
- **Markovian projection** (source Lemma 3; checked): for any process and any map π to a finite set, the law of
  π(ω_t) evolves by the one-step kernels K_t(s, s′) = P(π(ω_{t+1}) = s′ | π(ω_t) = s); the hitting time of an
  absorbing set has exactly the law of the absorption time of the inhomogeneous chain (K_t). For a face: K_t is
  the true rule fed by κ_t(β | z), the equal-time conditional law of the two layers beneath given the w layers
  above. Path's Theorem P is a certificate on these kernels. If the conditional law given "alive, unsettled" is
  constant in t the hazard is constant (the converse is false).
- **Permutive sources** (checked: proof; enumeration). Automaton on Z^d permutive in the variable at a vertex
  e ≠ 0 of its neighbourhood, uniform product start, P a set of cells no two of which differ by a multiple of e:
  the field {x_p(t) : p ∈ P, t ≥ 0} is i.i.d. uniform. (One-sided permutivity suffices; rule 30 qualifies.) Each
  value consumes the fresh initial cell p + te. **With feedback** (source Lemma 1; proof checked; exact check on
  a 3 × 7 box): if the bulk below depth w is permutive in each cell's deep neighbour (two layers in), the top w
  layers run the true rule and the bulk may read them, then from (any law) ⊗ (uniform) the top w layers are
  exactly the dice chain D2 / D3 with ρ = ½. Literature (`library/notes/algebraic-ca.md`, read in the note): the
  one-dimensional bipermutive statement is Shereshevsky–Afraimovich / Sablik / Pivato (r − l adjacent columns);
  no published statement of exact independence in dimension ≥ 2 was found, so both lemmas here stand on their
  own proofs.
- **Sealed sets** (checked: proof re-derived; exact minimisation). Hulls R = 3…10: the smallest sealed set is one
  whole face, proved optimal (`sealed_min.py`). The smallest one containing no whole face (12, 18, 33, 39, 57 cells
  at R = 3…7) is a face minus a few cells, thickened: not a different object. Slabs: bands, see E12; the face is
  smallest at 3 × 3 × 3, 4 × 4 × 3, 4 × 4 × 4, 3 × 3 × 8 (optimal). 2D: the smallest sealed set of a box or strip is a
  whole edge row or column; small vessels have extra ones (do not generalise from H ≤ 5).
- **The 2D edge cell** (checked by hand): with k live among its four in-row neighbours and b ∈ {0, 1, 2} live
  beneath, a live cell with k = 2 always survives, a dead cell with k = 0 always stays dead, and the other eight
  cases go either way depending on b. Different edge cells have different cells beneath (no sharing, unlike gump).
- **The 2D edge game** (`exponent/theorems.md` B; proof read and found correct; brute force re-run to L = 11):
  with the rows beneath chosen freely, every edge configuration on a ring of L ≥ 5 can be emptied in three
  generations, and the lone triple (L ≥ 9) not in two. **The gump face game** (checked, exact): every
  configuration of the hull faces R = 3 and R = 5 can be emptied in two generations; larger faces unknown.
- **Upper bounds of the right form** (theorems.md B′, C; correct, trivial): noisy rule E T ≤ ε^{−L}; driven edge
  E T ≤ 3δ^{−3L}. No lower bound of the form e^{cL} is proved anywhere in the repository.
- **Darroch–Seneta** (theorems.md D; finite-matrix proof given there, read): from a quasi-stationary law of a
  finite chain the absorption time is exactly geometric with 1 − λ = Σ μ(x) d(x). For dice models only. (Primary
  source not on the shelf: requests item 8.)
- **Mixing ⇒ exponential** (theorems.md E; checked, one-line chain rule): if the conditional probability that a
  block of m cells is empty given the blocks before it are empty is ≤ θ < 1, then h ≤ θ^⌊L/m⌋. The published
  relative (Galves–Schmitt 1990; `notes/escape-rates.md` A1, read in the note) is for a deterministic map with an
  *invariant* measure, ratio mixing in *time*, and events that are cylinders in time: it gives an exponential
  law with scale 1/μ(D_n). In two dimensions ratio (ψ) mixing is too strong even for the high-temperature Ising
  model; there e^{−c n^d} comes from the Gibbs property (Abadi–Chazottes–Redig–Verbitskiy; same note, A3).
- **Gump face cell** (checked): an interior face cell has 6 neighbours in the face, 2 one layer in, 1 two layers in.
- **From the library** (read in the notes, not in the papers). Finite contact process, d = 1: the upper bound on
  the lifetime uses only monotonicity, the lower bound duality (`contact-finite.md` §1). Mountford 1993, Prop.
  1.2: if from every start the process is, after a time a(n), dead or equal to the process started full, and it
  survives b(n) ≫ a(n) with probability → 1, then τ/Eτ → exponential; its proof uses attractiveness for one of the
  two inequalities (§3). Schapira–Valesin, Prop. 2.9: E τ_G ≥ c(2|G|³)^{−(N+1)} ∏ E τ_{G_i} over disjoint
  connected pieces of a tree, which gives e^{c|G|} from pieces (§6; monotonicity is used). Durrett–Schonmann
  1988: an empty interval costs e^{−cn} under the contact process's stationary law, and a proved "area above,
  perimeter below" dichotomy (`ld-contact-percolation.md`). Quasi-stationary laws of finite chains:
  Méléard–Villemonais, Prop. 2 and Thm 7 (`qsd.md`), which is the readable source for "Darroch–Seneta"; the rate
  measured after T0 is the quasi-stationary rate only if T0 exceeds the relaxation time (their Remark 3; in D2
  the second eigenvalue is ≈ 0.5). D2 is a probabilistic cellular automaton; D3 is one only with the cube
  triples as sites (`pca.md` with the cube lemma). Supertransients (`supertransients.md`): chaos lasting
  e^{c·size} with a memoryless collapse has a numerical literature and no proofs.

## Lab results

| id | request | result | script |
|---|---|---|---|
| L0.1 | sizes | hull R = 1c, 2v, 3c, 4v, 5c, 6v, 7c, 9c, 11c, 13c, 15c, 17c: 6, 12, 36, 60, 114, 168, 264, 510, 876, 1386, 2064, 2934 cells; face area 3, 3, 9, 9, 18, 18, 30, 45, 63, 84, 108, 135 | `gump_lab.py sizes` |
| L0.2 | smallest gump vessels, every state | R = 2v (12 cells): 498 cyclic states (108 fixed, 390 of period 2), 2,750 states end extinct, max transient 3. 910 of 4,096 states never lose a face | `gump_lab.py census 2 v` |
| L0.3 | 2D, every state | strip 3 × 6: 2,259 cyclic states; 52,463 of 262,144 states never lose an edge; longest wait for an edge death 10. Box 4 × 5: 2,005 cyclic states; 258,644 of 1,048,576 never lose an edge; longest wait 22 | `toy2d_lab.py census strip 3 6` |
| L0.4 | smallest sealed sets | see lemma exchange | `sealed_min.py` |
| L0.5 | gump face emptied in one generation? | no in general; see E10 | `face_one_step.py`, `face_one_step_interior.py` |
| L0.6 | refit of the 2D law | see E1 | journal, round 0 |
| L0b.1 | bijection with a trapdoor, all permutations of ≤ 7 points, all H | lemma and union bound hold in all 689,569 cases; equality iff equal gaps | `startpoints.py bijection` |
| L0b.2 | cells beneath a face | cube lemma; 40 of 64 triples | `startpoints.py triangles` |
| L0b.3 | gump face game, hull faces | R = 3: 324 configurations emptied in one generation, 187 in two. R = 5: 81,528 in one, 180,615 in two. None needs three | `startpoints.py game 3`, `game 5` (2¼ min) |
| L0b.4 | D2(L, ρ) exactly, L = 5…18 | ρ = 0.472: ln τ = 4.4000, 5.3838, 6.4169, 7.5765, 8.6350, 9.6834 at L = 8, 10, 12, 14, 16, 18; steps per cell 0.536, 0.523, 0.522, 0.526 at L = 15…18; quasi-stationary density 0.645; h/p₁ = 0.394 from L = 13; deaths from one cell 72%; second eigenvalue ≈ 0.5. ρ = 0.5: ln τ(16) = 8.6764. Agrees with the exponent study's sampled values at L = 8, 12, 16 within 1.1σ | `dice_w1.py 0.472 18`, `dice_w1.py check` |
| L0b.5 | crossing time of a hull face | farthest pair 5, 6, 7, 8, 9, 10 generations at R = 7…17 | `startpoints.py crossing` |
| L0b.6 | sealed bands in slabs; hulls to R = 10 | see E12 and lemma exchange | `startpoints.py slab` (2 min with the integer programmes), `sealed_min.py hull R c\|v` |
| L0b.7 | how far from invertible | bits lost in one generation, log₂(\|X\|/\|F(X)\|): 2.5 of 20 (box 4 × 5), 2.4 of 24 (strip 4 × 6), 1.7 of 12 (hull R = 2v); eventual image 0.19%, 0.046%, 12% of states | `startpoints.py image` |
| L0b.8 | permutive rules as dice, small cases | see lemma exchange | `startpoints.py source` |
| L0b.9 | one-generation emptying under product measures (2D) | cost per cell 0.5515 at p_e = ρ = 1/2; 0.672 at (0.58, 0.472); 0.760 at (0.6455, 0.472) | `iid_flash.py` |
| L1.1 | path LR1: a_k(r) = Σ Tr[k,k′] r^{k′−k} / Σ Tr[k,k′] on the measured one-step table of the face population (existing tallies, not in git) | a₁(r) > 1 for all r ≤ 0.90 at A = 30, 45, 63, 84 (r = 0.65: 1.117, 1.093, 1.086, 1.075); a₂ > 1 for r ≤ 0.70–0.75. P(death \| n = 1) = 0.41, 0.38, 0.38, 0.37; P(death \| n = 2…5) ≈ 0.10, 0.019, 0.005, 0.001; mean step from n = 1, 2, 3, 5, 10 at A = 63: 0.00, +0.31, +0.53, +1.14, +1.98 | `path_r1.py lr1` |
| L1.2 | the same table, φ free below K and constant above (linear programme) | best bound: −ln = 2.82, 5.78, 9.53, 14.02 at A = 30, 45, 63, 84 against −ln h = 6.81, 9.82, 13.63, 18.08: loss 4.0 nats at every size; K/A = 0.43–0.48, a = 0.95; φ(1), φ(2), φ(3) = 0.84–0.90, 0.56–0.64, 0.32–0.43, then ratios 0.55–0.63. Rows above A/2 are not in the tallies; A = 63, 84 optimistic | `path_r1.py lr1b` |
| L1.3 | path LR3: population of a dying face at lag s before death (existing `pre` arrays) | mean n at lags 1…6, 8, 10, 12, 16: A = 84: 1.6, 3.4, 6.4, 9.7, 13.6, 17.6, 26.0, 31.8, 35.2, 39.9 (living mean 42.4); A = 30: 1.6, 3.8, 6.5, 8.3, 9.3, 10.1, 11.4, 12.2, 12.6, 13.2 (13.6). Half the living mean at lag 3.2, 4.7, 5.9, 6.8; 90% at lag 11, 13, 13, 14 | `path_r1.py lr3` |
| L1.4 | path LR2: Theorem P on the exact lumped table of D2(L, 0.472) | geometric φ: best bound 1.02, 0.97, 0.88, 0.80 at L = 8, 10, 12, 14 (useless). φ free: bound/h = 8.8, 10.4, 11.5, 12.6, 13.6 at L = 8…16 (a = 0.8) | `path_r1.py lr2`, `lr2b` |
| L1.5 | D2 on a segment (two dead ends) = D2 on a ring with two adjacent cells removed | ln τ = 4.506, 5.106, 5.486, 5.847, 6.286, 6.764, 7.259, 7.740, 8.201, 8.655 at L = 5…14 cells; steps 0.495, 0.481, 0.461, 0.454 at L = 11…14. Longer-lived than the ring of equal length by 2.07 nats at L = 5 and 1.08 at L = 14 | `path_r1.py seg` |
| L2.1 | source L1: 2D rule in row 0 over a parity bulk with feedback, box 3 × 7, every state | initial state ↦ (row 0 at t = 0; rows 1–2 at t = 0, 1, 2) is a bijection of {0,1}²¹. Control with a bulk reaching one row per generation: 32,768 of 2,097,152 records | `source_r1.py l1` |
| L2.2 | source L2: local threshold lemma | identity and inequality on all 2²⁴ pairs of states, hull R = 2v (λ = 1.1) and box 3 × 4 (λ = 1.15); termwise bounds sharp. Gump lattice: shells 1, 12, 70, 212, 464, 820; S(1.1) = 13,336; C_U = 1.4×10⁶ | `source_r1.py l2` |
| L2.3 | source L3: equal-time kernel of rows 1–2 given row 0, 2D strip 4 × 6, uniform start, every state | no quasi-stationary window: the unsettled population with row 0 alive is 1.65×10⁷ at t = 0, 768 at t = 20, 0 at t = 21; hazard 0.10–0.22 for t = 1…10. P(row 0 empty next \| one cell) = 0.46–0.60 against 0.22–0.26 for dice of the same density; two cells: 0.03–0.54 against 0.002 | `source_r1.py l3` |
| L3.1 | counting 1, 2: c₁; strips and boxes of 3 rows, every state; classes of the k = 1 graph | c₁ = 0.551535. Row 0 empty next: strips 3 × 5…8: 2,507, 10,846, 47,383, 209,825; boxes 3 × 5…7: 2,977, 13,850, 64,434; all equal to the transfer-matrix counts. The 16-state graph is strongly connected: ρ⁰₁ = ρ₁ | `counting_r1.py c1` |
| L3.2 | counting 3: c₂ (2¹⁶ window states) | c₂ = 0.467693 (ρ₂ = 20.046271 of 32); checked against every state of strips 5 × 4 (224,471) and 5 × 5 (7,043,564); class of the all-dead window: 54,591 states, dominant, ρ⁰₂ = ρ₂. Density 0.472: c₁ = 0.489963, c₂ = 0.4671 | `counting_r1.py c2` |
| L3.3 | counting 4: periodic gump faces, one-generation emptiability, SAT against the cube criterion | 2 × 2 (12 cells): 2,662 of 4,096; 3 × 2 (18 cells): 112,744 of 262,144; no disagreement (both tori have doubled neighbours) | `counting_r1.py lemma5` (1¾ min) |
| L3.4 | C4 box 7 × 7, every symmetric state, k = 1 | top edge empty next in 502 of 8,192 = constrained band 251 of 4,096 = 0.061279; box without symmetry 0.030725 | `counting_r1.py c4` |
| L3.5 | counting 6: collision probability of the top three rows at generation j from soup, strips 4 × 5, 4 × 6, 5 × 5 | excess (1/L) ln(8ᴸ Σ μ²): 0.44, 0.46, 0.37 at j = 1; 0.99, 1.03, 0.92 at j = 2; 1.73, 1.74, 1.74 at j = 8 (to compare with c₁ = 0.5515) | `counting_r1.py coll` |
| L3.6 | second-order lift, every pair-state (2D strip 2 × 5; gump hull R = 1c) | bijection; "face empty now" has frequency 2⁻ᴬ; nothing enters "empty twice running" | `counting_r1.py lift` |
| L3.7 | C4 boxes in the committed toy2d file | settling is 97%, 81%, 66%, 54%, 42%, 32% of all exits at L = 16…36 (box without symmetry: 71 of 4,297 at L = 16, ≤ 3 beyond): the C4 slope 0.28 is a hazard among replicas that have not settled | `counting_r1.py data` |
| L1.6 | refits of the empty-window decrement (committed `gap.json`) | limit 0.348 (c/ℓ), 0.355 (e^{−ℓ/20}), 0.370 (c/ℓ²), 0.373 (e^{−ℓ/10}) on ℓ = 20…38, all acceptable | `path_r1.py data` |

## The lab: what it can do, how to ask

Validated: `toy2d_lab.py selftest` and `gump_lab.py selftest` (steppers against the lead's and the oracle's;
both print ALL OK, re-run this round); `dice_w1.py check`; `startpoints.py all` (ALL OK; the slab stepper is
checked there against the open-lattice stepper).

Available on request, exact only: the fate of every state of a vessel with ≤ 26 cells; smallest sealed sets
under side conditions (hulls to about 700 cells, slabs to about 250); feasibility questions "is there a
configuration beneath that does X" (SAT); the face game on a face of ≤ 18 cells; linear programmes over
certificates (Theorem P) on an exact or tallied one-step table; transfer-matrix eigenvalues for
any explicitly stated finite-window model (to about 2¹⁶ window states); exact killed-chain eigenvalues and
quasi-stationary laws for dice models on a ring of L ≤ 18 (cells updating independently given the row) or on
≤ 2¹⁴ states otherwise; joint laws of permutive automata on small windows.

A request needs: the vessel (kind and dimensions); the rule; what is random and with what law, if anything;
the event; and the convention for states that never die. No Monte Carlo, nothing over a few minutes.

**Existing tallies.** A request may ask for arithmetic on the tallies of `research/fluct/qsd.py` for hulls
R = 7, 9, 11, 13 (A = 30…84). The bulk files (`research/scratch/fluct/qsd_R*.npz`) are not in git; the tables the
lab reads are saved in **`critic/lab/data/fluct_tables.npz`** (66 kB, committed; made by `curate_fluct.py`, which
checks deaths against the committed `qsd_summary.json`): one-step transitions of the face population from
n < A/2 (`Tr`), the face-population histogram (`H`), the joint histogram of the face and the A cells one layer
beneath it (`J`), deaths and exposure, and for each lag 0…64 before a death the histogram of the dying face's
population (`prehist`). `path_r1.py` reads only that file. No new runs.

## Citations

Before leaning on a published theorem, look on `library/shelf.md` (59 sources) and in `library/notes/`. Every
literature statement on this board is now either on the shelf (and marked "read in the note": I compared with
the librarian's note, not with the paper) or carries its own proof here. Known gaps on the shelf that touch the
board: the Goles–Olivos and Goles–Fogelman-Soulié–Pellegrin primaries (T5 does not depend on them: its proof is
self-contained and checked; the librarian could not verify 26N + 1 against them, I re-derived it from the proof);
Darroch–Seneta 1965 itself (read through Méléard–Villemonais); Bramson–Neuhauser 1994 (secondary accounts only).
