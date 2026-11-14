#!/bin/bash
# segments (a wall of 3 sites), then windows on the b = 64 ring (one core); starts when batchB is done
cd "$(dirname "$0")"
while pgrep -f batchB.sh > /dev/null; do sleep 5; done
python3 run.py run seg_det_n13 det 16 8 60 256 4 26112 3
python3 run.py run seg_det_n21 det 24 8 150 256 4 26112 3
python3 run.py run seg_det_n29 det 32 8 500 256 4 26112 3
for n in 5 6 7 8 10 12; do python3 run.py run seg_m1_n$n model $((n+3)) 1 40 64 4 26112 3; done
for n in 16 20 24; do python3 run.py run seg_m1_n$n model $((n+3)) 1 120 256 4 26112 3; done
python3 run.py run win_det_b64 det 64 8 1800 256 2
python3 run.py run seg_det_n37 det 40 8 1800 256 4 26112 3
