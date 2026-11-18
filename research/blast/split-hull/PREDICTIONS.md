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

## Block 3: 04:11 UTC. A forecast of the 135-, 165- and 198-cell faces from brute-force dip rates (not a measurement)

Known: the first brute-force tables (`levels.py`, exposures 3 to 12 x 10^7 hull-generations per size) and the four
anchors. Found in them: -ln q(0.6) = ln tau + ln nu(0.6 P-bar) is 5.611, 8.668, 12.242, 16.330 at 45, 63, 84, 108
cells, a straight line in the area to +0.003, -0.003, -0.002, +0.002 (slope 0.1701 per cell; a term in the edge k,
if fitted, is -0.03 against the lifetime's -0.34). The same holds at 0.5 and 0.4 within their errors; at 0.7 and
above a rim term appears. So I conjecture **ln tau = a + 0.1701 A - ln nu(0.6 P-bar)**, and nu(0.6 P-bar) can be
measured by plain running at any size: -8.304 +- 0.008 (135 cells), -9.764 +- 0.022 (165), -11.34 +- 0.06 (198).

| face | forecast of ln tau_face | error (anchors' errors through the line, nu's error, choice of fit) | competing values |
|---|---|---|---|
| R = 17, 135 cells | **29.23** | +- 0.025 | 29.230 (second difference repeats), 29.205, 29.163 |
| R = 19, 165 cells | **35.80** | +- 0.045 | 35.81 if it repeats |
| R = 21, 198 cells | **43.00** | +- 0.08 | |

- P(the 135-cell face, once measured to +- 0.03, is nearer 29.230 than 29.163) = 85% (was 62% in block 1).
- P(the line through -ln q(0.6) misses the measured 135-cell value by more than 0.05) = 15%.
- Second differences of ln tau implied: 0.693 (k = 8), 0.68 +- 0.03 (k = 9), 0.63 +- 0.10 (k = 10). P(the k = 10
  value, after the longer runs now started, is below 0.66) = 55%: the dip rate's own second difference looks
  smaller at the largest size (-0.177, -0.177, -0.183, -0.166 +- 0.025, -0.11 +- 0.06), which I do not trust yet.
- Longer runs at R = 17, 19, 21 are started now; they will move nu(0.6) within the errors above (P = 80% each).

## Scores of block 2 (04:17 UTC)

- "The line through -ln q(0.9) has all residuals within 0.02" (45%): **no.** The first tables stop at
  floor(0.9 P-bar), so the nearest level I can interpolate is 0.85: residuals +0.026, -0.030, -0.012, +0.016
  (weighted chi2 44 on 2). The dying study's "to within 0.01" does not survive threshold-free rates here.
- "The straight-line forecast from the shallow level for 135 cells is below 29.20" (65%): yes (29.105 at 0.85), but
  that fit is not a line, so the number means nothing.
- "Forecasts from the four levels agree within 0.05" (35%): **no**: 29.105, 29.122, 29.178, 29.223 at p = 0.85, 0.8,
  0.7, 0.6. What I had not foreseen: the fits separate cleanly into lines (p <= 0.6: chi2 0.4, 1.7, 0.1 on 2) and
  non-lines (p >= 0.7: chi2 9, 32, 44), and the lines agree with each other. **The choice of p <= 0.6 was made after
  seeing this**, by the quality of the fit; block 3 is the forecast that follows from it.
- "ln nu at the shallow level keeps falling through 165 and 198 cells" (85%): yes (-3.063, -3.264, -3.490 at 0.85).
- Donor swap at R = 11: within 2 errors of 13.633 (50%): yes, emptily (13.534 +- 0.117, 6 replications); scatter
  below the flip sampler's 0.15 (40%): **no** (0.24).

## Block 3, addendum (04:17 UTC): values after the first longer runs at R = 19 and 21, same law, nothing refitted

- nu(0.6 P-bar) moved within its error at R = 19 (-9.764 +- 0.022 to -9.749 +- 0.007) and at R = 21 (-11.337 +- 0.059
  to -11.387 +- 0.018). The law's values are now 29.223 +- 0.016 (135 cells; its longer run is still going),
  35.772 +- 0.021 (165), 43.024 +- 0.032 (198). "The second difference repeats at 0.691" gives 29.230, 35.812, 43.085;
  "the wrapped price takes over" gives 29.163, 35.613, 42.689.
- The hint of a smaller second difference of ln nu at the largest size (block 3: P = 55% for below 0.66) went away
  with more data: -0.177, -0.177, -0.183 +- 0.017, -0.151 +- 0.022, -0.192 +- 0.027 centred on R = 11 ... 19.
- Outside the fit, one size down: the 30-cell face (R = 7; my brute force 6.8345 +- 0.0024 under this protocol, 6.804
  on file) lies 0.22 ABOVE the line of -ln q(0.6). The line is a statement about 45 cells and more.
- New, for whoever has a torus stepper [conjectured]: if what happens below 0.6 P-bar (density about 0.28 to 0.30)
  does not know about the rim, a wrapped face should have the same q there as a rimmed face of equal area, and the
  whole gap between hull and torus (0.474, 0.594, 0.779 at 63, 84, 108 cells) should be the logarithm of the ratio
  of their dip rates to that density. P(the gap at 63 cells is explained to within 0.1 by the dip rates) = 40%.
- Correction to the last item, 04:19 UTC, no new data: I wrote 40% before recalling `research/dying` round 3's slab.
  Its 63-cell torus has a cheaper tail than the hull face (0.427 against 0.499 per live cell lost) and a dearer
  shallow part, which already says that q below half population is larger on the torus (by roughly e^1). So I
  now put "the hull/torus gap is all in the dip rates" at 10%. What my tables show is narrower: among hull faces
  of 45 to 108 cells, q below 0.6 P-bar has no term that grows with the edge. The rim can still change q by a
  fixed factor (the last cells sit on the rim line, agent anatomy), and the torus can have another slope.

## Block 3, final values (04:36 UTC; all runs in, law unchanged, nothing refitted by hand)

ln tau_face from "-ln q(0.6) is a straight line" (weighted fit -2.049 + 0.17014 A over the four anchors, chi2 1.1 on 2)
and the measured nu(0.6 P-bar) = -8.302 +- 0.003, -9.754 +- 0.005, -11.368 +- 0.011:
**29.223 +- 0.014 (135 cells), 35.779 +- 0.020 (165), 43.007 +- 0.027 (198).** From fixed-density levels (0.28 A):
29.218 +- 0.012, 35.781 +- 0.021, 43.02 +- 0.05. Every nu moved within its first error (forecast of 80% each: held).
P(the 135-cell face, measured to +- 0.03, lies within 0.05 of 29.223) = 75%. The way I expect to be wrong if I am:
low, through one-generation busts taking a growing share of deaths (README, "The bust route").

## Block 4: 04:50 UTC. Dice under the hull (subset simulation on a hull dice chain), frozen before any run at R >= 11

Known: at R = 9 only, the hull dice chain (true rule on depth 0..5 beneath the watched face, fair coins on depth 6
and 7, everything inside the true hull boundary) gives 9.837 +- 0.018 by brute force (gump: 9.819) and 9.84 +- 0.07
from four replications of split-slab's subset sampler adapted to it (`hd.c`).
Parameters, by split-slab's frozen recipe with my measured P-bar and sigma_P, fixed now for all sizes:
LAM1 = round(P-bar - 2.5 sigma_P) = 10, 18, 28, 38, 51 for R = 9, 11, 13, 15, 17; DELTA 3; NBATCH 8 (4,096 chains);
NSWEEP = round(A / 6) = 8, 10, 14, 18, 22; KFLIP 5 (split-slab's 4 scaled by ND / 2A = 1.2 to 1.33); TPRE 32;
TWIN 24; WBACK 12. No tuning on R = 13 or 15.

- P(the sampler lands within two of its own errors of the anchors at BOTH R = 13 and R = 15) = 55%.
- P(the chain itself, by brute force at R = 11, is within 0.04 of 13.633) = 75%.
- If both calibrations pass, the forecast for the sampler's R = 17 value is the one already frozen:
  **29.223 +- 0.014** (block 3); P(the sampler's value, with its own error e, lies within 2 sqrt(e^2 + 0.03^2) of
  it) = 70%. I expect e near 0.10 with the replications I can afford, which will not separate 29.230 from 29.163
  by itself (0.067 apart): P(e <= 0.035) = 10%.

## Scores of block 4 (05:25 UTC)

- "Within two errors at both R = 13 and R = 15" (55%): **yes**: +0.093 +- 0.065 and +0.079 +- 0.074 (48 replications each).
- "The chain by brute force at R = 11 within 0.04 of 13.633" (75%): **no**: 13.70 +- 0.06 (275 deaths; +0.07, inside
  its own error, outside my 0.04).
- "The sampler's R = 17 value within 2 sqrt(e^2 + 0.03^2) of 29.223" (70%): the chain gives 29.453 +- 0.042 (120
  replications). Raw: +0.230 against an allowance of 0.103: **no**. With the blind sizes' offset removed
  (29.367 +- 0.065): +0.144 against 0.143: **no, by a hair**. I had not said which; both miss.
- "e <= 0.035" (10%): no (0.042). "e near 0.10": it came out better, 0.042.
- So the forecast of block 3 (29.223 +- 0.014) is 1.4 to 2.2 errors below what the dice chain says, depending on
  how the chain's offset is read. If the chain is right and its offset is 0.09, the second difference of ln tau at
  k = 8 is 0.83 +- 0.07, larger than 0.69, not smaller.

## After block 4 (05:45 UTC): what more replications did to the dice chain's numbers (no forecast was frozen for these)

- R = 13: 48 replications gave +0.093 +- 0.065 above gump, 234 give +0.051 +- 0.026. R = 15: 48 gave +0.079 +- 0.074,
  184 give +0.008 +- 0.086: the error grew, because one replication in the second seed carried 11% of the summed
  rate. I had quoted the 48-replication errors as if the rates were well behaved; they are heavy-tailed at 108 cells.
- R = 17: 125 replications, 29.445 +- 0.041 on the chain, no large replication yet (largest share 3%). Less the pooled
  blind offset (+0.047 +- 0.025): 29.398 +- 0.048. Against block 3's 29.223 +- 0.014 that is +0.175, 3.5 quoted errors.
  I do not trust the quoted error downward (see README) and read 29.40 +0.06/-0.15.
- Brute force of the chain at R = 11, redone with 1,097 deaths: 13.639 +- 0.030 (gump 13.633): the earlier 13.70 +- 0.06
  was a fluctuation; block 4's "within 0.04" would have held.
