#!/bin/bash
# Round 3 of the review of research/dying: run plan, fixed before any production run (pilot: r3_pilot.sh, used only
# for the thresholds; r3_val.py ALL OK first). Usage: bash r3_plan.sh 1 & bash r3_plan.sh 2 & wait   (two cores, ~25 min)
# r3_ex (= ex2 + 7-bit counts + deep-excursion dumps), 256 lanes, soup 0.4, events every generation, Brent settled
# test, T0 = 512, fresh seeds 9411-9417. PBAR thresholds: the study's (21.67, 31.29, 42.49, 55.14, csz 28.83,
# slab 32.57), which give the same integer thresholds as this review's pilot (21.60, 31.25, 42.45, 55.19, 28.90,
# 32.58); R = 17 (A = 135, not in the study) uses the pilot's 69.49. Deep-excursion dumps at M3 = 9 (c1) and 8
# (csz), the study's. Samples of the face union every SAMPK generations for stationary occupancy and the thinned
# controls.
#
# Analysis fixed now (r3_ana.py):
#  1-2. nu(p) by the study's definition (min P < p.PBAR, per face, per generation of exposure) at p = 0.05..0.95;
#       also nu(<= k) per integer k and an interpolated nu at exact levels (linear in ln nu between integers), to
#       separate the size effect from integer quantisation. -ln nu(0.5)/A, ln nu(0.9), [ln nu(0.9) - ln nu(p)]/A.
#  3.   Tail slope per live cell over 0.10-0.45: unweighted (lead) and count-weighted (registered); local slopes by
#       window of k.
#  4.   K(A) = c.A - ln tau - ln nu(0.9) for trial c; ln tau own (A = 45, 63, 84) and the GPU's (45-135); H_A(k) =
#       ln nu(<= k) + ln tau against k (where the shortfall sits); extrapolation of the per-site curve at p >= 0.2 in
#       1/A and then to p = 0, with the spread over fit choices as the error.
#  5.   T2 profile as the study defines it, its thinned control, a uniform rho-weighted random-points control, and two
#       alignment-free versions: split-half (centroid from a random half, occupancy counted on the other half) and
#       the pair correlation of live cells against the same for thinned stationary faces.
#  6.   T3 corrected centroid, its control, and a centroid-free statistic (survivors in the third of cells nearest
#       the tied edge over the rho expectation, against the same for thinned faces).
#  7.   T4 as defined, its random baseline, and a rule-aware baseline (empty cells with at least one live in-face
#       neighbour at t, the minimum the rule allows for a face cell, which has 3 neighbours outside the face).
#  8.   Slab: ln tau_face = ln(E/D), nu(p), the same statistics; firewall families of the lattice (r3_geo.py info).
D=/home/user/gump-for-agents/research/scratch/audit_dying/r3; cd $D
x() { # name seed gens pbar m3 sampk
  b=x_$1; ./r3_ex g_$1.txt run $2 0.4 $3 $b.lives /dev/null $b.smp $6 /dev/null 0 1 512 $4 $b.x $5 $b.dx > $b.json; }
if [ "$1" = 1 ]; then
  x v11c_c1 9411 4000000 31.29 9 1024; x v9c_c1 9412 1000000 21.67 -1 100000000; x v13c_c1 9413 8000000 42.49 -1 100000000
elif [ "$1" = 2 ]; then
  x v15c_c1 9414 6000000 55.14 -1 100000000; x v11c_csz 9415 1600000 28.83 8 512; x slab21 9416 4000000 32.57 9 1024
  x v17c_c1 9417 1500000 69.49 -1 100000000
fi
