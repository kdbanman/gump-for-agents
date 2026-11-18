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
