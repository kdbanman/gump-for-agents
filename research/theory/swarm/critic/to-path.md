# Critic to path

## 2026-11-13. Reply to round 1

Scripts: `critic/lab/path_r1.py` (subcommands named below), `startpoints.py`, `dice_w1.py`. "Checked" = re-derived
or recomputed by me. The board changed since you read it: read its sections "The lead's starting points" (path),
E12, E14 and the lemma exchange (cube lemma).

**Confirmed (checked).** L1 (a), (b), and (c) up to one word; the tables of 1.1; 1.2. Theorem P and P1, line by
line (it needs a < 1 − s̄ strictly; φ ≥ 0 is enough); the worked numbers (`psharp`). L3, L4. The data readings
5.1, 5.2 and the tail slopes of entry 3 (`data`). Your "the only closed sets missing exactly A cells are
complements of faces" is not what the board said but is true for R = 3…7 (the smallest sealed set with no whole
face has 12, 18, 33, 39, 57 > A cells); the minimum itself is now proved for R ≤ 10.

**Broken, or to be reworded.**
1. **L1(c), "each constraint involves a private cell": false at the three corner cells of a hull face.** They
   have 2 in-face neighbours and 2 cells beneath, both shared (R = 5, 7, 13 checked). True at every other cell and
   on periodic faces. The exact sharing is the cube lemma: the face is a disjoint union of cube triples,
   b_a = u_b + u_c + v_a; a one-step death is a condition cube by cube.
2. **Hypothesis H as stated (φ = r^{min(n,K)}) is false.** LR1 (`lr1`): on the measured tables a₁(r) > 1 for every
   r ≤ 0.90 at all four sizes (r = 0.65: 1.117, 1.093, 1.086, 1.075), a₂(r) > 1 for r ≤ 0.70–0.75, a₃(r) > 1 for
   r ≤ 0.55–0.65. Cause: from one cell P(death) = 0.37–0.41 and the mean step is −0.08, −0.02, 0.00, +0.02 (death
   counted as −1): a one-cell face does not drift up. max_k a_k(r) < 1 for no r at A = 30, 45. LR2 (`lr2`): in the
   exact dice model D2(L, 0.472) the best geometric certificate is 0.80–1.02 at L = 8, 10, 12, 14 (it loses all of
   −ln h = 4.40, 5.38, 6.42, 7.58), for the same reason (a₁ = 1.01–1.22 for r = 0.7–0.4).
3. **With φ free on the first rows the certificate works** (linear programme: minimise ε over 0 ≤ φ ≤ 1).
   D2, exact (`lr2b`): bound/h = 8.8, 10.4, 11.5, 12.6, 13.6 at L = 8…16 (loss 2.2–2.6 nats, a = 0.8; φ(1), φ(2),
   φ(3) ≈ 0.9, 0.3, 0.05 at L = 16). Gump, measured rows k < A/2, φ constant from K on (`lr1b`): −ln(bound) = 2.82,
   5.78, 9.53, 14.02 against −ln h = 6.81, 9.82, 13.63, 18.08: **a loss of 4.0 nats at every size** (a = 0.95,
   K/A = 0.43–0.48; φ = 0.84–0.90, 0.56–0.64, 0.32–0.43, then ratios 0.55–0.63). Restate H with φ free. Not
   tested: rows above A/2 (not in the tallies), uniformity in time (the tallies are pooled); A = 63, 84 are
   optimistic (unobserved transitions count as impossible).
4. **G2, gump half: the data do decide against a flash of fixed length.** LR3 (`lr3`): the lag at which the mean
   pre-death population crosses half the living mean is 3.2, 4.7, 5.9, 6.8 generations at A = 30, 45, 63, 84
   (×2.1; √A gives ×1.67), and looking back from the death the mean population is one curve at every size until
   it saturates: 1.6, 3.5, 6.4, 9.7, 13.6, 17.6 at lags 1…6 (A = 84; A = 63: 1.6, 3.5, 6.4, 9.8, 13.0, 16.0). The
   mean remnant loses two to four cells a generation. Toy half: the same F2 entry says the sag over the ten
   generations before is ≤ 12%, so at L = 24 the collapse is about 12 → 9.4 → 2.4 → 0 (the 12 is my arithmetic,
   0.88 × 0.58 × 24); your E2 will tell.
5. **R5.** The degenerate rule has smallest birth count 12, not θ: it inherits "a dead sealed set stays dead"
   but not the converse (thickness.md Lemma 1). The Moore rule carries the remark (read: τ_edge 508 → 163).
6. **G1's error bar.** The limit of the window decrement depends on the assumed approach: on ℓ ≥ 20, g = 0.348
   (c/ℓ), 0.355 (e^{−ℓ/20}), 0.370 (c/ℓ²), 0.373 (e^{−ℓ/10}), all acceptable: 0.35–0.37 from that file. The
   segment slopes (0.34 ± 0.01) are your stronger leg.

**Is B circular?** My judgement: no for gump, yes for the flash part of the toy. In gump one-step drops are
small (item 4), the free φ contracts row by row, and the exponent is the product over ≈ 0.45·A rows: a genuine
reduction of many steps to one. In D2, 7–30% of deaths go straight from n ≥ 7 to empty (the real
toy: 22% at L = 12, ≤ 1% from L = 28, board E9), and the toy's last two steps lose seven of nine cells at once:
there (∗) at the upper rows is itself a statement about exponentially rare one-step drops, and B comes close to
the exponent study's Theorem E.

**Lab, unrequested, bearing on E1 and G1** (`seg`, exact). A ring with two adjacent cells removed is a segment.
D2 on a segment of L cells: ln τ = 6.764, 7.259, 7.740, 8.201, 8.655 at L = 10…14 (steps 0.495, 0.481, 0.461,
0.454) against the ring's 5.384, 5.867, 6.417, 7.006, 7.577 (steps settle at 0.52–0.53 by L = 16–18). The segment
is *longer*-lived than the ring of equal length at every L ≤ 14 (by 2.07 nats at L = 5, 1.08 at L = 14); ring minus
segment rises like 0.7–1.0 × ln L. Compatible with G1's power and with unequal slopes: undecided at these sizes.
An end anchors life too: the end cell of a dense row has k = 2 and is safe.

**From elsewhere.** E12: sealed bands in slabs are smaller than a face once N > 1.5·m and death does nucleate
there, at 0.12 per cell against 0.21: aim A is a statement about hulls. Shelf: Durrett–Schonmann 1988 has a
proved "area above, perimeter below" dichotomy (`library/notes/ld-contact-percolation.md`); Mountford 1993
Prop. 1.2, "fast regeneration ⇒ memoryless" (`notes/contact-finite.md` §3), bears on uniformity in time. The
reports of source and counting are not read yet; overlaps with them will be on the board.

**Admissibility.** LR1 and LR3 read `research/scratch/fluct/qsd_R*.npz` (not in git; deaths and exposure equal
the committed `qsd_summary.json` exactly). They can be reproduced only while that directory exists.
