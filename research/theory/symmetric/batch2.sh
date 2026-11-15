#!/bin/bash
# Block 2 of PREDICTIONS.md. Sequential, one core.
#   nohup bash research/theory/symmetric/batch2.sh > research/scratch/symmetric/batch2.log 2>&1 &
cd "$(dirname "$0")/../../.."
R="python3 research/theory/symmetric/run.py run"
# D2h again with the ladder snapshots (seed 2; the seed-1 files of block 1 are moved aside by the caller)
for s in oct_9_c_d2h oct_10_v_d2h; do $R $s 200000 2; done
for s in oct_11_c_d2h oct_12_v_d2h; do $R $s 400000 2; done
for s in oct_13_c_d2h oct_14_v_d2h; do $R $s 1000000 2; done
# rim ladder and the other groups of order two, A = 63
for s in oct_11_c_c2v oct_12_v_c2v; do $R $s 200000 1; done
for s in oct_11_c_csz oct_12_v_csz; do $R $s 400000 1; done
for s in oct_11_c_ci oct_11_c_c2e; do $R $s 2000000 1; done
# O_h and T_d, both centrings
for r in "23_c" "24_v" "25_c" "26_v" "27_c" "28_v"; do $R oct_${r}_oh 200000 1; done
for r in "29_c" "30_v"; do $R oct_${r}_oh 400000 1; done
for r in "31_c" "32_v"; do $R oct_${r}_oh 1000000 1; done
for r in "19_c" "20_v" "21_c" "22_v" "23_c" "24_v"; do $R oct_${r}_td 200000 1; done
for r in "25_c" "26_v" "27_c" "28_v"; do $R oct_${r}_td 1000000 1; done
# T and T_h
for r in "15_c" "16_v" "17_c" "18_v"; do $R oct_${r}_t 200000 1; done
for r in "19_c" "20_v"; do $R oct_${r}_t 1000000 1; done
for r in "19_c" "20_v" "21_c" "22_v" "23_c" "24_v"; do $R oct_${r}_th 400000 1; done
# long ones
$R oct_21_c_t 2000000 1
$R oct_33_c_oh 4000000 1
$R oct_34_v_oh 4000000 1
$R oct_31_c_td 4000000 1
$R oct_32_v_td 4000000 1
$R oct_33_c_td 6000000 1
echo BATCH2 DONE
