# Forecasts of agent split-hull (blast of 2026-11-18), frozen before the data

## Block 1: 03:50 UTC, before any run at R = 13, 15 or 17 (the sampler has only been run at R = 9 and 11)

Known to me: the anchors of `BRIEF-COMMON.md`, the three candidate values for the 135-cell face (29.230, 29.205,
29.163), and my sampler's behaviour at R = 9 and 11 only (scatter of single replications about 0.4 in ln τ at
R = 11 with 3 × 10⁵ trials per stage; mean within 0.2 of the anchor).

About the sampler (the thing most likely to fail tonight):

- P(the sampler, parameters frozen on R = 9 and 11, lands within 2 of its own standard errors of the anchor at
  R = 13 AND at R = 15) = 45%. I expect its error to grow fast with size: the dip from 0.9 P̄ to an empty face takes
  about 10 generations at R = 11, a deep flip needs several generations to change the face, so most of the
  selection acts on clones that are still identical.
- P(I reach ± 0.03 at R = 17 by 05:00 UTC) = 10%. P(± 0.10) = 30%. P(no usable number, error above 0.3) = 45%.
- If the R = 13 and 15 estimates miss, P(the miss is upward in ln τ, the estimator starved of lucky lineages) = 75%.

About gump (R = 17, 135 cells), held weakly since I have no information the PI lacks:

- ln τ_face(R = 17) = 29.21 ± 0.04. P(nearer 29.230 than 29.163) = 62%. P(nearer 29.163) = 38%.
  Reasoning: two equal second differences (0.691, 0.692) are weak evidence for a third; the one before them was
  0.799, so the sequence 0.799, 0.694, 0.690 is still falling, and a prefactor reading (29.205) sits between.
- ln τ_face(R = 19, 165 cells): 35.74 ± 0.10 (constant second difference gives 35.81; wrapped price with
  A^(−1.5): about 35.70). P(above 35.75) = 50%.
- Duration of the reactive path (generations from the crossing of 0.9 P̄ to the empty face) grows by less than 40%
  from R = 11 to R = 17: P = 65% (a flash, not a sweep). At R = 9 and 11 my sampler gave about 9 and 10.

## Block 2: 04:05 UTC, before any brute-force table of dip rates at R >= 11 has been produced (`levels.py` unrun)

Known: block 1; that my frozen sampler is biased at R = 11 (-0.173 +- 0.044) and starved at R = 13; the dying
study's statement (its round 3, review) that ln tau + ln nu(0.9) = 0.2125 A - 2.07 "to within 0.01 nats" over
45 to 108 cells, with threshold-free ln nu(0.9) = -2.34, -2.38, -2.40, -2.48, -2.53 at 45 ... 135 cells. I have
seen my own brute-force table at R = 9 only. The plan: measure nu(p) by plain running at R = 9 ... 21, form
-ln q(p) = ln tau(anchor) + ln nu(p) at 45 ... 108 cells, fit it, and forecast the larger faces from their nu(p).

- P(the straight line a + cA through -ln q(0.9) at the four anchors has all residuals within 0.02) = 45%. (With the
  dying study's rounded nu values I get residuals up to 0.06 by hand, so I doubt the "0.01".)
- P(the straight-line forecast from p = 0.9 for the 135-cell face is below 29.20) = 65%; my hand value is 29.15.
- P(the straight-line forecasts for 135 cells from p = 0.9, 0.8, 0.7, 0.6 agree within 0.05) = 35%. If they do not,
  the decomposition does not decide between 29.163 and 29.230 and I will say so.
- P(threshold-free ln nu(0.9) keeps falling with size through 165 and 198 cells, each below the last) = 85%.
- Donor swap (the deep half of each clone replaced by an independent hull's, two generations back) at R = 11,
  10 replications: P(within 2 standard errors of 13.633) = 50%; P(its scatter per replication is below the flip
  sampler's 0.15) = 40%.

## Scores of block 1 (04:05 UTC)

- "Within 2 errors of the anchor at R = 13 and 15" (45%): R = 13 gave 17.92 +- 0.37 (3 replications; within, but
  only because the error is huge); R = 15 not run. Not a pass in any useful sense. What I did not foresee: the
  sampler is already biased at R = 11.
- "Reach +- 0.03 at R = 17" (10%), "+- 0.10" (30%), "no usable number" (45%): **no usable number.**
- "A miss would be upward" (75%): **wrong.** The clear miss (R = 11) is downward: the flips help the face die.
- The gump forecasts (R = 17, R = 19, path duration) are not scored: no measurement.
