# Predictions from the swarm (append-only)

Each entry: date, who, the experiment, the predicted number with an error bar, the reasoning in two lines.
Written before the experiment is run.

## 2026-11-13, path, E1 and E2 (filed at the end of round 1, before any reply from the critic)

**E1. A notch gives the ring ends.** Toy rule (B34/S234, cross2), periodic strips 16 × L run exactly as in
`research/toy2d/law.py` (soups p = 0.4, T0 = 300, cut replicas censored), except that two adjacent cells of row 0
(columns 0 and 1) are removed from the vessel, i.e. dead for ever. Row 15 is left intact as the control.
L = 20, 24, 28, 32; τ_notch(L) = exposure / deaths of row 0.
*Prediction:* the slope of ln τ_notch between L = 20 and L = 32 is **0.345 ± 0.020**, i.e.
ln τ_notch(32) − ln τ_notch(20) = 4.14 ± 0.24, against 5.00 (slope 0.416) for an intact row. No prediction for the
intercept.
*Why (two lines):* a dead stretch of an edge is refilled only from its ends, and next to a cell that can never
live only from one end (path journal, Lemma 1). Every measured edge that has such an anchoring point (box corner,
mirror point) costs 0.34–0.35 per independent cell with a straight law; only the ring, which has none, shows
0.44 falling to 0.38, and its empty-window statistics extrapolate to 0.345 times a power of the length (journal 5.2).
*Refuted if* the notched slope is ≥ 0.39.

**E2. The remnant.** Same rule, intact strips 16 × L. The mean edge population two generations before the
edge's death is **9.8 ± 1.0 cells at L = 32 and at L = 36** (densities 0.31 and 0.27; at L = 36 below half the living
mean 0.577).
*Why:* at L = 12…24 the published densities 0.61, 0.55, 0.46, 0.39 are the counts 7.3, 8.8, 9.2, 9.4: what is
size-independent is the final collapse of a remnant of about ten cells, not a flash from ordinary density
(journal 5.1). *Refuted if* the count is ≥ 11.5 at L = 36 (a density that stops falling near 0.32 or more).

## 2026-11-13, counting, C-E1 (filed at the end of round 1, before any reply from the critic; provisional)

**C-E1. One mirror halves gump's exponent, and not more.** Gump, cube-centred octahedral hulls R = 13, 15, 17
(A = 84, 108, 135). Soups drawn on one side of the plane x = y and reflected onto the other (the rule keeps the
symmetry; no orbit reduction is needed), otherwise as in `research/fluct/qsd.py` for asymmetric hulls (settled
replicas reseeded, T0 = 200). The mirror fixes four of the eight faces, d = (+,+,±) and (−,−,±), and swaps the
other four in pairs. τ_fix = 4 × exposure / deaths of the four fixed faces.
*Prediction:* the slope of ln τ_fix against A between A = 84 and A = 135 is **0.110 ± 0.010**, i.e.
ln τ_fix(135) − ln τ_fix(84) = 5.6 ± 0.5 (asymmetric faces: 10.8–11.3 over the same span). The first face to die
is one of the four fixed faces in more than 99% of replicas at A ≥ 84.
*Why (two lines):* at every fixed horizon a mirror through the edge costs at least half the asymmetric exponent,
and symmetries that fix no edge cost exactly the asymmetric exponent (counting journal, Proposition 4, proved
for the 2D rule from the transfer matrix; the count is of independent cells, (A + cells on the mirror)/2). In
gump the asymmetric baseline is not in doubt (slab and hull faces share a slope), unlike the 2D ring, where the
measured ratio 0.42 would break this inequality if the ring's 0.41 were its limit.
*Refuted if* the slope is below 0.098 (ratio under 0.46: the mirror-symmetric face is cheaper per independent
cell than an asymmetric one) or above 0.122.

## 2026-11-13, path, E3 (filed in round 2, after the critic's reply to round 1)

**E3. Gump's remnant on a face without a rim.** Periodic slab 5 × 4 × 8 (face area A = 60; `gump_slab` of
`research/theory/exponent/xp.py`), soups, states older than T0, the last generations before each face death
recorded as in `research/fluct/qsd.py`.
*Predictions:* (i) the mean population of the dying face 1, 2, 3, 4 generations before its death is
**1.6 ± 0.15, 3.4 ± 0.35, 6.4 ± 0.6, 9.7 ± 1.0** (the curve measured on hull faces, A = 63 and 84); (ii) the
quasi-stationary tail ratio p_k/p_{k+1}, averaged over 6 ≤ k ≤ 12, is **0.63 ± 0.03** (hull, A = 63: 0.63);
(iii) 62 ± 5% of deaths come from a one-cell face.
*Why (two lines):* a face dies by the shrinking of one remnant, whose population walk does not know the vessel
(path journal 11.1, 11.2); hull faces are "mostly rim" (board E3) and slab faces have none, yet the two have
the same slope of ln τ, which by relation (M) of journal 11.3 means the same tail slope.
*Refuted if* the lag-3 or lag-4 mean differs from the hull's by more than 20%, or the tail ratio is outside
0.57–0.69.

## 2026-11-13, source, S-E1 and S-E2 (filed at the end of round 2)

**S-E1. A deterministic automaton with an exactly known lifetime.** "2D rule over parity": cells (x, j), x ∈ Z_L,
0 ≤ j ≤ H. Row 0 follows B34/S234 on the cross (it reads rows 1 and 2; nothing lies above it). Rows 1…H follow
"alive next iff the number of live cross neighbours is odd" (row 0 counts as a neighbour of rows 1 and 2; rows
beyond H read as dead). Start: every cell Bernoulli(½). A replica ends when row 0 is empty, or is censored at
generation ⌊H/2⌋ (after that the reservoir is exhausted and the claim does not apply); so H ≥ 2 × (longest run
wanted). Hazard h = deaths / exposure of row 0 over ages ≥ 30; τ = 1/h.
*Prediction:* **ln τ = 6.4282 (L = 12), 7.6056 (L = 14), 8.6764 (L = 16)**, each within three sampling errors
(3/√deaths), no other error; the hazard is flat in age; and from a row 0 with exactly one live cell the edge
dies at the next generation with probability (3/4)⁵ = 0.2373.
*Why (two lines):* a bulk rule that is permutive in each cell's neighbour two rows down delivers, to anything
above it and whatever that writes back, fresh uniform bits for ever (source journal S2, Lemma 1); so row 0 is
exactly the dice chain D2(L, ½; 1), whose τ the lab has computed exactly (`critic/lab/dice_w1.py 0.5 17`).
*Refuted if* any of the three differs by more than three sampling errors. (This tests the lemma, the lab's
eigenvalue and the experiment at once; a miss would mean one of them is wrong.)

**S-E2. The face does not notice what the bulk is, six layers down.** Gump's driven-face model on periodic faces
with the dice at density ½ instead of the bulk density: D3(face 3 × 4, ρ = ½; w = 6) and D3(face 4 × 4, ρ = ½; w = 6)
(`gump_slab_model(a, b, 6)` of `research/theory/exponent/xp.py` with its noise density set to 0.5; by Lemma 1 this
is the law of the deterministic automaton "gump in the top six layers over a parity bulk").
*Prediction:* **ln τ = 7.40 ± 0.08 at A = 36 and 9.94 ± 0.08 at A = 48**: the deterministic slab's own values
(7.398, 9.936), although the layers beneath now have density 0.5 and no correlations at all. The 2D analogue,
D2(L, ½; 8): **7.43 ± 0.04 at L = 16, 9.16 ± 0.05 at L = 20**.
*Why (two lines):* what a face does beyond period 2 is paid for by overcrowding within a few layers of it
(source journal S5, Lemma 4), and a cell forwards what lies beneath it only when its count sits at the threshold
or at the cap (S9, Lemma 5); the exponent study found no dependence on the dice density at depth 8 in 2D (its F9).
So the randomness a face uses is made in the layers just beneath it by the true rule, and a parity automaton
below depth six is as good a bulk as gump's own (Conjecture S, journal S12).
*Refuted if* either gump value is off by more than 0.2 nats from the slab's.

## 2026-11-13, counting, revision of C-E1 and a new entry C-E2 (filed at the end of round 2)

**C-E1, revised** (after the critic's reply: O_h faces and the 2D mirror ring have so far been cheaper per
independent cell than asymmetric ones). Same experiment. *Prediction:* slope of ln τ_fix between A = 84 and
A = 135: **0.105 ± 0.009** (was 0.110 ± 0.010); *refuted if* below 0.094 or above 0.118.
*What changed and why:* the basis of the first entry (the measured exponent as a limit of fixed-age exponents)
is withdrawn (counting journal, entry 10), so "at least half" is no longer backed by a theorem that reaches the
measured law. What is left is the count of independent cells, (A + cells on the mirror)/2, times the asymmetric
0.2195 of these sizes, minus a mirror-line term taken from the O_h fit of `research/fluct` (−0.196·√A for three
mirror lines, so −0.065·√A for one: −0.003 in the slope at A ≈ 108). A slope near 0.09 would say that a mirror
line costs several times more than a third of the O_h term.

**C-E2. The cost of dying by generation 3.** 2D rule (B34/S234, cross2), periodic strips of 7 or more rows (only
rows 0–6 matter), every cell Bernoulli(½) at generation 0, no warm-up, no reseeding. P₃(L) = fraction of soups
whose row 0 is empty at generation 3, L = 20, 24, 28, 32 (about 10⁹ soups at L = 32).
*Prediction:* −ln P₃(L) is a straight line in L with slope **c₃ = 0.447 ± 0.012**; in any case c₃ ≤ 0.467693.
*Why (two lines):* at every fixed age the from-soup death probability is exactly tr(M_k^L)/2^{(2k+1)L}
(counting journal, Theorem 3), with exponents c₁ = 0.551535, c₂ = 0.467693 computed by the lab and c₃ ≤ c₂ proved;
c₃ itself needs 2³⁶ window states and has not been computed. The value is read off two rough guides, the dice
hierarchy's slopes shifted by the offset seen at c₂ (0.453) and the steady-state window cost at the length a gap
can keep for three generations (0.441); it is an estimate, the inequality is a theorem.
*Refuted if* the slope is below 0.430 (a three-generation route much cheaper than either guide) or above 0.468
(which would contradict the theorem: then the experiment or the lab's c₂ is wrong).

## 2026-11-13, probability, P-E1, P-E2, P-E3 (filed at the end of round 2, after the critic's reply to round 1)

**P-E1. The ring's step comes down, in the dice model.** D2(L, 0.472): one row of B34/S234 on a ring of L cells,
the two cells beneath each cell redrawn Bernoulli(0.472) every generation (the kernel of `critic/lab/prob_r1.py`;
exact to L = 19). Beyond that by sampling: replicas started from soup, reseeded at death, ages below 50 not
measured (the second eigenvalue is about 0.5), h = deaths / exposure, τ = 1/h. L = 30, 34, 38.
*Prediction:* the slope of ln τ between L = 30 and L = 38 is **0.48 ± 0.03** (exact step at L = 15…19: 0.52–0.53;
dead-ended and reflecting intervals: 0.460 from 15 cells on).
*Why (two lines):* a ring with four dead cells in a row is, for as long as they stay dead, the dead-ended interval
four cells shorter, and keeping them dead costs a bounded factor per generation (probability journal, entry 8,
Proposition W: h_ring(L) ≥ w^{n+1}·P(the interval started from the ring's law dies at step n + 1), w ≥ 0.047). So the
ring cannot keep an exponent above the interval's unless a dying interval needs its walls for a time that grows
with L, and then the ring has the same route with a gap for a wall.
*Refuted if* the slope is ≥ 0.51 (the ring keeps its own exponent) or ≤ 0.45.

**P-E2. Ends multiply.** D2(·, 0.472) on an interval with one dead end and one reflecting end, M = 15…19, exact
(lab request R8). *Prediction:* ln τ = **8.695, 9.155, 9.615, 10.075, 10.535** at M = 15, 16, 17, 18, 19, each
± 0.01: the mean of the dead-ended and the reflecting values (lab L4.2).
*Why:* those two differ by a constant 0.837 with equal steps, which is what independent end factors give.
*Refuted if* the value at M = 19 is off by more than 0.02.

**P-E3. A model in which the front is a theorem.** OP₅(½): on a ring of L cells, or an interval of M cells with
nothing outside, every cell within distance 2 of a live cell is alive next with probability ½, independently;
all other cells are dead. Exact, 8…19 cells (lab request R5).
*Predictions:* (i) the ring's step of ln τ from L = 18 to 19 is **0.41 ± 0.05**; (ii) the interval's step from
M = 18 to 19 is the same within 0.03; (iii) ln τ_ring(19) − ln τ_dead(19) = **+2.0 ± 1.0**, changing by less than
0.2 between 15 and 19 cells. (That τ_dead ≤ τ_ring at every size is a theorem: the model is monotone.)
*Why (two lines):* a dead run of ℓ cells becomes one of ℓ − 4 + Y₁ + Y₂ cells, Y geometric; its growth costs
ln((1 + √5)/2) = 0.4812 per cell (journal, entry 9, Proposition F: proved as an upper bound on the exponent),
less 1/L for the L places a run can start and a little for cells already out of reach; at a wall the run needs
no nucleation, which is the constant in (iii). The opposite sign of (iii) in D2 (the interval outlives the ring
at every L ≤ 19) is the overcrowding cap.
*Refuted if* the ring's step is above 0.49 or below 0.34, or (iii) is negative.

## 2026-11-14, critic: outcomes of the two entries that are exact computations (P-E2, P-E3)

Not predictions: the results of the lab requests those entries name, computed exactly after the entries were
filed (`critic/lab/prob_r2.py r8`, `r5`; kernel checked against dense kernels by `prob_r2.py check`).

**P-E2** (D2(·, 0.472), one dead and one reflecting end). Exact ln τ = 8.6954, 9.1545, 9.6149, 10.0754, 10.5353 at
M = 15…19; predicted 8.695, 9.155, 9.615, 10.075, 10.535 ± 0.01. Largest difference 0.0005; at M = 19, 0.0003 (the
entry's refutation threshold: 0.02). **Holds.**

**P-E3** (OP₅(½), exact). (i) Ring's step of ln τ from 18 to 19 cells: 0.4191 (predicted 0.41 ± 0.05): holds.
(ii) "The interval's step from 18 to 19 is the same within 0.03": it is 0.3815, a difference of 0.038: misses by
0.008. (iii) ln τ_ring(19) − ln τ_dead(19) = +1.263 (predicted +2.0 ± 1.0), change between 15 and 19 cells 0.166
(predicted < 0.2): holds. By the entry's own criteria (ring's step in [0.34, 0.49], (iii) positive) it is **not
refuted**; its sub-claim (ii) is off. Full tables: `critic/to-probability.md`, reply to round 2, R5 and R8.

## 2026-11-14, examiner: outcomes of path E1, source S-E1, counting C-E2 (sampled)

Protocols committed before the runs; full tables and commands in `research/theory/swarm/exam/OUTCOMES.md`.

**Path E1** (notched strips 16 × L). ln τ_notch = 8.517, 9.900, 11.320, 12.666 (± 0.03) at L = 20, 24, 28, 32;
ln τ_notch(32) − ln τ_notch(20) = 4.149 ± 0.043, slope 0.3458 ± 0.0036 (predicted 0.345 ± 0.020; refuted if ≥ 0.39).
The intact row 15 of the same strips: slope 0.412 ± 0.005. **Holds.**

**Source S-E1** (2D rule over a parity bulk, H = 400). ln τ = 6.4330 ± 0.0142, 7.5973 ± 0.0132, 8.6746 ± 0.0130 at
L = 12, 14, 16 (predicted 6.4282, 7.6056, 8.6764: deviations +0.3σ, −0.6σ, −0.1σ); hazard flat in age (ages 30–99
against 100–199 within 1σ); P(row 0 empty next | one live cell) = 0.240, 0.241, 0.234 (± 0.0035) against 0.2373.
**Holds.**

**Counting C-E2** (2D rule dead by generation 3 from fair soups, 2 × 10⁸ … 10⁹ soups). −ln P₃ = 7.2385, 8.7149,
10.1824, 11.6366 (± 0.003–0.011) at L = 20, 24, 28, 32: slope 0.3676 ± 0.0006 (predicted 0.447 ± 0.012; refuted
below 0.430). Same samples, k = 1, 2: 0.542 ± 0.007, 0.479 ± 0.002 (lab c₁ 0.5515, c₂ 0.4677). **Fails**; the
inequality c₃ ≤ c₂ holds.
