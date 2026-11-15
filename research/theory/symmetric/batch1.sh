#!/bin/bash
# Block 1 of PREDICTIONS.md: run list (spec, generations per replica). Sequential, one core.
#   nohup bash research/theory/symmetric/batch1.sh > research/scratch/symmetric/batch1.log 2>&1 &
cd "$(dirname "$0")/../../.."
R="python3 research/theory/symmetric/run.py run"
# asymmetric partners (rect_4_2_c1 seed 1 was the speed test; seed 2 adds to it)
$R rect_3_2_c1 100000 1
$R rect_4_2_c1 400000 2
$R rect_5_2_c1 1000000 1
$R rect_3_3_c1 400000 1
# mirror only, Q = 2, 3, 4
for s in rect_6_2_cs rect_8_2_cs rect_4_3_cs rect_4_4_cs; do $R $s 400000 1; done
for s in rect_10_2_cs rect_6_3_cs; do $R $s 1000000 1; done
# threefold only
for s in hex_6_0_c3 hex_6_0_c3_o2 hex_6_0_c3_o4 hex_5_2_c3 hex_6_1_c3; do $R $s 200000 1; done
for s in hex_4_4_c3 hex_7_0_c3 hex_6_2_c3; do $R $s 600000 1; done
# vessels: asymmetric and D2h, both centrings
for s in oct_9_c_c1 oct_10_v_c1; do $R $s 100000 1; done
for s in oct_9_c_d2h oct_10_v_d2h oct_11_c_d2h oct_12_v_d2h; do $R $s 200000 1; done
for s in oct_13_c_d2h oct_14_v_d2h; do $R $s 1000000 1; done
for s in oct_11_c_c1 oct_12_v_c1; do $R $s 600000 1; done
# the long ones
$R rect_12_2_cs 3000000 1
$R rect_8_3_cs 3000000 1
$R rect_6_4_cs 3000000 1
$R hex_7_1_c3 2000000 1
$R hex_5_4_c3 3000000 1
$R hex_8_0_c3 4000000 1
$R oct_15_c_d2h 4000000 1
$R oct_16_v_d2h 4000000 1
$R rect_6_2_c1 6000000 1
$R rect_4_3_c1 6000000 1
$R rect_3_4_c1 6000000 1
echo BATCH1 DONE
