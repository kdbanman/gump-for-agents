# Review of pull request 8 (research/gpu: GPU ensembles on Modal)

Adversarial review, 2026-11-13. Branch `claude/awesome-cray-boq9vz` at **be7b01d** (unchanged at fetch time).
Worktree used read-only; no GPU, no Modal. Scripts: `research/audit/gpu_pr8/` (some written by an earlier reviewer
that stopped before writing a verdict; each is re-read and its use stated below).

Status: in progress. Verdicts are written as they are reached.

## Files touched outside research/gpu/ and research/data/gpu_facelaw/

## Claim 2: asymmetric face law curves upward (A = 108, 135)

**Verdict: the numbers are confirmed as far as the committed data can confirm them; the headline framing ("0.39 nats,
13σ above the line this repo had extrapolated") is wrong as a measure of anything and must be restated.** What
survives: the local slope keeps rising past A = 84, and A = 108 sits 0.21 ± 0.04 nats above the straight line through
the *verified* CPU points A = 45–84. What does not: that this is a new upward bend, or a 13σ effect.

Ran:

    python3 research/audit/gpu_pr8/rederive.py PR8      # earlier reviewer's script; read and kept: own unpacking, own sums
    python3 research/audit/gpu_pr8/dupcheck.py PR8      # new: repeated death ages vs a chance estimate
    python3 research/audit/gpu_pr8/curvature.py         # new: fits to verified CPU and GPU points

(PR8 = the worktree at be7b01d.) Findings:

1. **The table re-derives exactly** from the committed JSON with independent code: ln τ_face = ln(8 · exposure /
   deaths) after T0 = 200 gives 13.635 (764,941), 18.141 (34,026), 23.376 ± 0.031 (1,059), 29.341 ± 0.250 (16, three
   runs). The stored aggregates agree with the stored per-bin hazards and, where raw lives are stored, with the raw
   lives (sum of all ages = replicas × generations to 1.5 × 10⁻³ or better).
2. **Definition is the repo's.** τ_face = 8 × (mean wait from age 200 to the first extinct face layer of 8) in the
   exact hull of an asymmetric p = 0.35 soup on |p|₁ ≤ R; lives ending before 200 are excluded with their exposure;
   lives open at the end are censored (exposure counted, no death); estimator exposure/deaths. Same as
   `research/fluct/` and `verify_face_law.py`. Calibration holds: A = 63 GPU 13.635 ± 0.001 vs CPU-verified
   13.633 ± 0.008; A = 84 GPU 18.141 ± 0.005 vs CPU 18.077 ± 0.054 (1.2σ). The result is independent of T0
   (60, 200, 1000, 10⁴ all give 23.376 at A = 108; 18.141–18.142 at A = 84).
3. **Start of clock / censoring.** Birth is the end of the launch at which the replica was reseeded; the death age
   is exact to the generation (launch start + in-launch generation − birth). Frozen time after a death is not
   counted. Correct.
4. **No sign of stuck (settled, never-dying) replicas inflating exposure.** These runs predate period-3+ detection,
   so "no settles recorded" is evidence only for period 1–2 (kind 2 was detected and is 0 in 800,000 lives). The
   evidence for period ≥ 3 is indirect but adequate: a stuck fraction f would make the hazard fall at old ages.
   R = 11 (ages to 15τ): hazard flat to 6–15τ (3,305 deaths vs 3,238 expected), f ≲ 10⁻⁵. R = 13: ages ≥ 3τ give
   626 deaths vs 655 expected (0.96 ± 0.04), f ≲ 0.4%. R = 15: deaths after age 1.8 × 10⁸ 211 vs 200 expected —
   flat. To inflate A = 108 by 0.39 nats a third of the replicas would have to be stuck; excluded.
5. **Error bars** are 1/√deaths in ln τ, right for an exponential wait with independent lives (each life a distinct
   soup; see claim 6). Not inflated by duplicates: repeated death ages within the R = 13 run are 37 pairs vs 34.6
   expected by chance (estimated from near-coincidences, `dupcheck.py`); the earlier reviewer's "~8.5" chance figure
   was a crude uniform-density estimate and is wrong.
6. **The 13σ is not a test of curvature.** The line 0.2077·A + 0.55 is the endpoint of a quasi-stationary
   distribution fit (fluct README correction 1), not a fit to lifetimes, and it already misses verified lifetimes:
   A = 45 by −0.08 nats (28σ, critic board E2) and A = 84 by +0.08. The σ quoted is the GPU point's alone. Measured
   against lifetimes:
   - local slopes, verified CPU then GPU: 0.2010 (30→45), 0.2119 (45→63), 0.2116 ± 0.0026 (63→84),
     0.2208 ± 0.0026 (84→108, CPU 84) or 0.2181 ± 0.0013 (GPU 84), 0.221 ± 0.009 (108→135). Rising — but it was
     already rising from A = 30 to 63, so the bend is not new beyond A = 84;
   - the straight line through verified A = 45, 63, 84 predicts 23.167 ± 0.028 at A = 108: GPU is +0.21 (≈5σ);
   - curved fits (a + bA + c√A or quadratic) through verified A = 45–84 predict 23.15 ± 0.16–0.19: GPU is +0.23
     (≈1.2σ), i.e. consistent with the curvature already present; through A = 30–84 they predict 23.59 / 23.93,
     *above* the GPU value (but no 3-parameter form fits A = 30–84 well: χ² 7.9 and 19.5 for 1 dof);
   - GPU points alone (63, 84, 108): quadratic coefficient 2.6σ; with A = 135 2.8σ. With CPU 45–84 + GPU 108:
     4.9σ in either curved form.
   **Dropping subsets:** without A = 135 nothing changes; without A = 30 the curvature is 4.9σ; with only GPU points it
   is 2.6σ. The curvature survives every cut; its size is model-dependent.
7. **The conjecture "0.208–0.209 per site extrapolations are lower bounds"** follows from rising local slopes
   (all ≥ 0.211 from A = 45 on), so it is plausible; note that the rim-free slab slope is 0.2088 ± 0.0009, so
   octahedral faces at A ≥ 45 cost *more* per site than slab faces, which the PR does not discuss. Free 3-parameter
   fits give asymptotic slopes 0.23–0.26 for a + bA + c√A, which shows the extrapolation is not determined by
   these data; the PR should not quote a single asymptotic number and does not.
8. **R = 17:** 16 deaths in three runs at ages ≤ 0.0015τ; it rests entirely on the hazard being flat over three
   more decades (the PR says so). The seed-3 run was kept from a batch whose three containers ran the same initial
   soups (permuted); keeping one of three is legitimate as long as the choice was not made by outcome — the PR
   keeps s3 because it predates nothing else; not checkable, and immaterial at ±0.25.

Not checked: the kernel's correctness at R = 15 and 17 on a GPU (see claim 1); an independent CPU measurement at
A = 108 (≈ 1 death per 6 minutes on one core; not enough in the time available to test a 0.2-nat effect).
An independent CPU measurement at A = 84 is below (filled in when the run ends).

## Claim 6: seed-collision bug found and fixed

## Claim 3: symmetric faces at A = 759, 828 against forecasts

## Claim 4: O_h vertex lineages R = 36, 38, 40 memoryless; tau(40) 21% above the file

## Claim 1: kernels bit-exact against the engine; settle detection

## Claim 5: qsd.py's settle flaw matters at R = 36

## General code review

## Fixes required before merge / things to note
