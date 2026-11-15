#!/bin/bash
# Block 3 of PREDICTIONS.md, three lanes.
#   for L in 1 2 3; do nohup bash research/theory/symmetric/batch3.sh $L > research/scratch/symmetric/batch3_$L.log 2>&1 & done
cd "$(dirname "$0")/../../.."
R="python3 research/theory/symmetric/run.py run"
if [ "$1" = 1 ]; then
$R hex_8_0_c3v 200000 1
$R hex_9_0_c3v 400000 1
$R hex_10_0_c3v 1000000 1
$R hex_6_6_c3v 1000000 1
$R oct_7_c_c1 100000 1
$R oct_8_v_c1 100000 1
$R oct_13_c_c2v 1000000 1
$R hex_11_0_c3v 3000000 1
$R hex_12_0_c3v 6000000 1
fi
if [ "$1" = 2 ]; then
$R oct_13_c_csz 4000000 1
$R oct_14_v_c1 10000000 1
fi
if [ "$1" = 3 ]; then
$R oct_29_c_td 1000000 1
$R oct_30_v_td 1000000 1
$R oct_17_c_d2h 40000000 1
fi
echo BATCH3 LANE $1 DONE
