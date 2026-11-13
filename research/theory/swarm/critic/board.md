# Board (critic)

_Kept by the critic. Last update: 2026-11-13, round 0 (before any solver report). Scripts named here are in
`critic/lab/`; run them from that directory. "Checked" means I re-derived or recomputed it; "read" means I
compared the statement with its source and did nothing more._

## Errors in the problem statement (and in the sources it lists)

None of these changes the problem. Each is a number or sentence a proof could lean on and should not.

- **E1. The 2D law is not a straight line with slope 0.416.** Refit of the seven committed points
  (`research/toy2d/data/law_cross2_B34S234.json`): the line 0.7295 + 0.4160·L has χ² = 28.9 on 5 degrees of
  freedom. Local slopes between successive sizes: 0.442, 0.407, 0.428, 0.400, 0.421, 0.382 (± 0.006–0.015).
  With a ln L term the coefficient of L is 0.374 ± 0.009; with a 1/L term, 0.395 ± 0.005; from L ≥ 20 alone,
  0.410 ± 0.003. The exponent study (unchecked) now gives 0.36–0.41 for the asymptote. **The 2D target is
  0.36–0.42, not 0.416**; "a formula that gives 0.416" (PROBLEM.md, what would count) may aim at the wrong number.
- **E2. Gump: "A = 30…135 measured" overstates what is verified, and the slope does not fall.** Verified
  octahedral data are A = 30, 45, 63, 84 (ln τ = 6.804, 9.819, 13.633, 18.077 ± 0.003, 0.003, 0.008, 0.054);
  A = 108, 135 are the unverified GPU numbers. The local slopes of the verified points are 0.2010, 0.2119,
  0.2116: level or rising. The first row of the facts table (−ln h/A = 0.2268 … 0.2152) falls only because the
  intercept is positive. The old fit 0.2077 + 0.55/A misses the A = 45 point by 0.08 nats, 28 standard errors,
  so its "± 0.0014" is not an error bar on anything. Rim-free (periodic slab) faces: 0.2088 ± 0.0009, A = 27–90.
- **E3. Octahedral faces of these sizes are mostly rim** (checked, `checks_round0.py`). A face of the hull of
  radius R = 2k − 1 has A = 3k(k+1)/2 cells: 3 corner cells with 4 neighbours inside the vessel, 6(k−1) rim
  cells with 7, and A − 6k + 3 interior cells with 9. Interior cells: 9 of 30, 18 of 45, 30 of 63, 45 of 84,
  63 of 108, 84 of 135. "Area, not perimeter" (question 1) cannot be read off octahedral data alone; the slab
  faces are the clean case.
- **E4. "Overcrowded-and-alive events" is loosely worded.** The event (O1 in `threshold.md`) is: n ≥ 6 at time t
  *and alive at time t − 1*. The face figures 0.073 and 0.035 come from one vessel (R = 9, A = 45, 30 soups),
  where "face" means the outermost *live* layer.
- **E5. "Symmetric faces: slope ≈ γ/6" was imposed, not measured.** The fit form a + (0.209/6)·A − 0.196·√A fixes
  the slope; free fits give 0.024–0.044 (fluct README §3).
- **E6. The 2D symmetry ratios 0.42 and 0.50 have different baselines.** 0.42 = 0.1733/0.41 in periodic strips
  16 deep; 0.50 = 0.171/0.343 in L × L boxes (first-death times). The symmetric slopes are equal (0.173, 0.171);
  it is the asymmetric baselines that differ (0.416 strip, 0.343 box).
- **E7. The lineage rows (slow variable; 1% double peels) were measured on O_h-symmetric states only**
  (hull radius 31–38). For asymmetric faces "memoryless" rests on CV ≈ 1 and a hazard flat in age (slabs; fluct).
- **E8. In the 2D strips the edge wait is a competing hazard, tested for memorylessness only at short ages when
  L ≥ 28.** At depth 16 the strip is cut across by three dead columns far more often than it loses an edge
  (cuts + interior firewalls against edge deaths: 4,768 / 898 at L = 28; 22,252 / 676 at L = 32;
  85,256 / 495 at L = 36), and a cut replica is reseeded. At L = 36 a replica lives about 1.7×10⁴ generations
  before it is cut; τ_edge is 5.8×10⁶.
- **E9. In 2D not every death is "the tail reaching one cell".** From the same data file (`frm`): the share of
  edge deaths whose edge had ≥ 7 live cells one generation earlier is 22% at L = 12, 10% at L = 16, 5% at
  L = 20, 2% at L = 24, ≤ 1% from L = 28. Mechanism (checked): in a fully live row every cell has four live
  in-row neighbours and survives only if both cells beneath it are dead.
- **E10. A false "[proved]" statement in `research/theory/exponent/theorems.md`, Lemma A, consequence (c):**
  "A gump face can always die in one generation given suitable layers beneath." The per-cell half is true (no
  face cell is safe). The statement about the face is false, because neighbouring face cells share the cells
  beneath them. Exhaustive (`face_one_step.py`): on the 18-cell face of the R = 5 hull, 180,615 of the 262,144
  configurations cannot be emptied in one generation whatever lies beneath; on the 9-cell face of R = 3, 187 of
  512. Smallest counterexample, checked by hand: live cells (0,0,5), (0,1,4), (0,2,3), (1,0,4). Cell (0,0,5) has
  two live face neighbours and dies only if both cells beneath it are dead; (0,1,4) has three and dies only if
  all three beneath it are alive; they share the cell (−1,0,4). What is true on those two faces: every
  configuration with ≤ 3 live cells can be emptied in one generation; on the R = 3 face every configuration can
  be emptied in two (`face_game.py`).
- **E11.** I did not find the lead's "starting thoughts" in the repository, so I have not checked them.

## Definitions a proof must match

- **Gump.** Cells = doubled coordinates with exactly one odd entry; 12 neighbours (AUTOMATON §2); B45/S345 =
  "alive next iff n + x ≥ 4, except n ≥ 6 dies" (checked). **Vessel** = diagonal hull |d·(p − c)| ≤ R, c a cube
  centre (R odd) or a vertex (R even); the outside is dead for ever (T2). **Face** = the cells of the hull with
  d·(p − c) = R for one signed diagonal d (8 faces). A face **dies** at the first generation at which it has no
  live cell; it then stays empty. Slab faces: the two outer layers of m consecutive {111} layers on a torus.
- **2D rule.** Neighbours (±1,0), (±2,0), (0,±1), (0,±2); B34/S234 = "alive next iff n + x ≥ 3, except n ≥ 5
  dies" (checked). **Strip** W × L: W rows, L columns, periodic along the row; **edge** = row 0 or row W − 1 (a
  ring of L cells; the measured law has W = 16). **Box**: no wrap; four edges.
- **τ is a hazard, not a mean over initial states.** h = (face deaths) / (face-generations of exposure), counted
  over soup-started replicas older than T0 (200–300 generations) that have not settled into a cycle and, in
  strips, have not been cut; τ = 1/h. A mean of the death time over all initial states does not exist: in every
  small vessel I enumerated a positive fraction of states never loses a face or edge (they settle into debris
  that touches every edge): 20.0% of the states of the 3 × 6 strip, 24.7% of the 4 × 5 box, 22% of the R = 2
  gump hull. A theorem has to say which τ it bounds.
- **Sealed** (in a vessel V): every cell of W has at most 3 (gump) or 2 (2D) neighbours in V \ W. Sufficient,
  not necessary, for a dead W to stay dead.

## Facts table of PROBLEM.md: what I checked

| row | status |
|---|---|
| gump −ln h/A at A = 30…84 | read against fluct README and `fluct/data/qsd_summary.json`: reproduces. See E2 for how to read it |
| GPU numbers at A = 108, 135 | not checked (under review elsewhere). Local slopes implied: 0.2146, 0.2181, 0.2209 |
| straight tail, ratio 0.6–0.66, h ≈ 0.6·P(1), 62% from one cell | recomputed from `qsd_summary.json`: h/p₁ = 0.645, 0.613, 0.601, 0.594; p_k/p_{k+1} = 0.65–0.69 (k = 1), 0.47–0.56 (k = 2), 0.74–0.87 (k = 3), 0.60–0.70 (k = 4…7). The ratio at k ≥ 4 drifts down with size (k = 4: 0.659 → 0.610 from A = 30 to 84): "size-independent end-game" holds to about 10% |
| 2D law, tail, h/p₁ 0.52 → 0.27 | recomputed from the data file: reproduces; see E1, E8, E9 |
| symmetric gump faces | read; see E5 |
| 2D symmetry ratios | read; see E6 |
| overcrowding rates | read; see E4. Not re-measured |
| sealed sets: 6-ring, 36-cell set, none in ≥ 3 layers | proof of Theorem 3 re-derived; identity e + 2(a + b) = 4d checked for all orientations; 6-ring minimal by search; 36-cell set not checked |
| slow variable; 1% double peels | read; see E7 |
| octahedral 1.7–1.9× tougher than slab | read (CLAIMS F6: 1.66, 1.66, 1.93). The exponent study reports equal *slopes* for the two |

## The three lines

No reports yet. Toolkits as assigned: **probability** (dice in place of chaos: particle systems, coupling,
percolation, contours); **counting** (the map with a trapdoor: exact counts, transfer matrices, escape rates,
entropy, solvable relatives); **path** (least unlikely route to empty: large deviations, effective dynamics of
the face, structure). Places where two lines could meet, which I will watch: the probability of an empty edge
under a product measure (a transfer-matrix computation about a dice model); quasi-stationary measures and
escape rates; the edge game with free rows beneath.

## Who is using which idea

(empty)

## Graveyard: ideas already tried here and dropped, with the reason

1. **Extrapolating the tail to n = 0** from n/A ≥ 0.1 (quadratic: off by 0.5–0.8 nats; Gaussian: 2–7 nats). The
   tail is straight near zero and must be measured there. (fluct README §1.)
2. **n as the reaction coordinate; splitting along n.** n removes 16–18% of the uncertainty about die-or-recover.
   Forward-flux sampling gains nothing: clones differing by one cell have 55–95% correlated fates, because the
   plunge (≈ 10 generations) is faster than a perturbation spreads. The rare event is a rare configuration, not
   a slow path. (fluct README §2.)
3. **"Exponentially decaying correlations ⇒ exponential-in-area wait"** (PROGRAM M2 as worded). The implication
   is invalid: mix a measure with decaying correlations with weight e^{−√L} on the empty row; every covariance
   moves by ≤ 4e^{−√L} and P(empty) ≥ e^{−√L}. A ratio (ψ-type) mixing bound is what multiplies.
   (`exponent/theorems.md` E, remark 1; I checked the counterexample.)
4. **Random map with killing** (PROGRAM E2): predicts an immortal basin of order τ²/2^N. In small vessels the
   basin is 5–94% of all states; most immortal cycles are debris of period ≤ 2. (Exponent F1; my census agrees on
   the cases I ran: 3 × 6 strip 20.0%, 1,859 immortal cyclic states of which 1,679 have period ≤ 2.)
5. **Energy arguments for freezing or for a critical drive rate.** One-layer oscillators of periods 3–12 balance
   drive and dissipation exactly; no local unconditional lower bound on dissipation exists. The threshold lemma
   is false on infinite configurations. (threshold.md §6, thickness.md.)
6. **Block construction and comparison with oriented percolation for the driven edge** (the contact-process
   route). Reported to fail at the first step: the rule is not monotone, and an unknown outside contaminates two
   cells per side per generation, the speed at which anything spreads. (`exponent/theorems.md`, "What is not
   proved". Their argument; I have not tried to break it.)
7. **Shallow dice models.** One row of the rule over i.i.d. Bernoulli(bulk density) rows has the right form and
   the wrong constant (slope 0.53 against ≈ 0.41). Three rows: still 10% high; gump at depth 3 misses by 0.3–1.0
   nats. Depth 4–8 agrees. (Exponent F4, F5, F8; unchecked.) Mean field puts the edge density at 0.68 against a measured 0.5–0.6.
8. **The stabiliser rule for symmetry** (exponent ÷ order of the face's stabiliser): right for symmetries that
   fix an edge; wrong as a complete account (four-fold rotation fixes no edge and lowers the slope by 20%).
9. **0.416 = 2 × 0.208.** See E1. Do not build on it.
10. **0.2077 as gump's asymptote.** See E2.
11. **Cubes outlive their ensembles / lineage memory.** Post hoc (P ≈ 0.18 without side 16); no memory found at
    R ≤ 38. Not a fact to explain.
12. **"The plunge lengthens with L in the 2D rule."** Reported false: a two-generation flash at every size
    (exponent F2; unchecked).
13. **"A gump face can die in one generation whatever its configuration."** False; see E10.

## Lemma exchange

From the repository, usable by all three. "Checked" = by me, this round.

- **T2, T3 and 2D analogues** (checked by offsets): a dead cell beyond an empty outer layer sees ≤ 3 (gump) or
  ≤ 2 (2D); three dead layers or rows are permanent, two are not.
- **Sealed sets** (checked: proof re-derived; exact minimisation). In the hulls R = 3, 4, 5, 6, 7 the smallest
  sealed set is one whole face (9, 9, 18, 18, 30 cells), and the smallest sealed set containing no whole face has
  12, 18, 33, 39, 57 cells (`sealed_min.py hull R c|v`, integer programme, proved optimal). 2D: the smallest sealed
  set of a box or strip is a whole edge row or column; with whole rows and columns forbidden the smallest are
  large bent bands joining the sides (33 cells in the 8 × 8 box, 42 in 9 × 10, 44 in the 8 × 9 strip).
  Small vessels have extra sealed sets (rows {1, 3} of a 5-row box; the middle row of a 3-row strip; alternate
  whole columns on an even ring): do not generalise from H ≤ 5.
- **The 2D edge cell** (checked by hand): with k live cells among its four in-row neighbours and b ∈ {0, 1, 2}
  live among the two beneath, a live cell with k = 2 always survives, a dead cell with k = 0 always stays dead,
  and the other eight cases go either way depending on b. Different edge cells have different cells beneath.
- **The 2D edge game** (`exponent/theorems.md` B; proof read and found correct; their brute force re-run to
  L = 11): with the rows beneath chosen freely, every edge configuration on a ring of L ≥ 5 can be emptied in
  three generations, and the lone triple (L ≥ 9) not in two.
- **Upper bounds of the right form** (theorems.md B′, C; correct, trivial): noisy rule E T ≤ ε^{−L}; driven edge
  E T ≤ 3δ^{−3L}. No lower bound of the form e^{cL} is proved anywhere in the repository.
- **Darroch–Seneta** (theorems.md D; standard): started from a quasi-stationary law of a finite chain the
  absorption time is exactly geometric with 1 − λ = Σ μ(x) d(x). It applies to a dice model, not to the
  deterministic rule.
- **Mixing ⇒ exponential** (theorems.md E; checked, one-line chain rule): if the conditional probability that a
  block of m cells is empty given the blocks before it are empty is ≤ θ < 1, then h ≤ θ^⌊L/m⌋.
- **Gump face cell** (checked): an interior face cell has 6 neighbours in the face, 2 one layer in, 1 two layers
  in; each cell one layer in lies beneath exactly two face cells.

## Lab results

| id | request | result | script |
|---|---|---|---|
| L0.1 | sizes | hull R = 1c, 2v, 3c, 4v, 5c, 6v, 7c, 9c, 11c, 13c, 15c, 17c: 6, 12, 36, 60, 114, 168, 264, 510, 876, 1386, 2064, 2934 cells; face area 3, 3, 9, 9, 18, 18, 30, 45, 63, 84, 108, 135 | `gump_lab.py sizes` |
| L0.2 | smallest gump vessels, every state | R = 1c (6 cells): 2 cyclic states. R = 2v (12 cells, the vertex star): 498 cyclic states (108 fixed, 390 of period 2), 2,750 states end extinct, max transient 3: agrees with CLAIMS T10. 910 of 4,096 states never lose a face | `gump_lab.py census 2 v` |
| L0.3 | 2D, every state | strip 3 × 6: 2,259 cyclic states (369 / 1,710 / 180 of period 1 / 2 / 4); 52,463 of 262,144 states never lose an edge; longest wait for an edge death 10. Box 4 × 5: 2,005 cyclic states (periods 1, 2, 3, 4); 258,644 of 1,048,576 never lose an edge; longest wait 22 | `toy2d_lab.py census strip 3 6` |
| L0.4 | smallest sealed sets | see lemma exchange | `sealed_min.py` |
| L0.5 | gump face emptied in one generation? | no in general; see E10 | `face_one_step.py 3`, `5` |
| L0.6 | refit of the 2D law | see E1 | inline, journal |

## The lab: what it can do, how to ask

Validated this round: `toy2d_lab.py selftest` (my stepper against the lead's `toy2d_check.py` step function on
strips; boxes through the strip-with-three-dead-columns embedding; the full map of every state against both;
censuses against the exponent agent's independent `fg_summary.json`) and `gump_lab.py selftest` (against
`check_threshold.py`'s stepper and `reference/oracle.py`; T1; face areas). Both print ALL OK.

Available on request, exact only: the fate of every state of a vessel with ≤ 26 cells (death times, immortal
basin, cycles); smallest sealed sets under side conditions; feasibility questions of the kind "is there a
configuration beneath that does X" (SAT); transfer-matrix eigenvalues for any explicitly stated finite-window
model; exact killed-chain eigenvalues for dice models on ≤ 2^20 states.

A request needs: the vessel (kind and dimensions); the rule; what is random and with what law, if anything;
the event; and the convention for states that never die. No Monte Carlo, nothing over a few minutes.
