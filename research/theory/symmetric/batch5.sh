#!/bin/bash
# Block 5 of PREDICTIONS.md, three lanes.
#   for L in 1 2 3; do nohup bash research/theory/symmetric/batch5.sh $L > research/scratch/symmetric/batch5_$L.log 2>&1 & done
cd "$(dirname "$0")/../../.."
R="python3 research/theory/symmetric/run.py run"
if [ "$1" = 1 ]; then
$R oct_35_c_oh 20000000 1
$R oct_37_c_oh 30000000 1
fi
if [ "$1" = 2 ]; then
$R oct_37_c_td 26000000 1
fi
if [ "$1" = 3 ]; then
$R oct_37_c_td 26000000 2
fi
echo BATCH5 LANE $1 DONE
