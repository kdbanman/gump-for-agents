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
