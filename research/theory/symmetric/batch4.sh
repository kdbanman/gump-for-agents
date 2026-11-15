#!/bin/bash
# Block 4 of PREDICTIONS.md.   nohup bash research/theory/symmetric/batch4.sh > research/scratch/symmetric/batch4.log 2>&1 &
cd "$(dirname "$0")/../../.."
R="python3 research/theory/symmetric/run.py run"
$R oct_19_c_o 400000 1
$R oct_20_v_o 400000 1
$R oct_21_c_o 400000 1
$R oct_13_c_c2e 4000000 1
$R oct_35_c_td 20000000 1
echo BATCH4 DONE
