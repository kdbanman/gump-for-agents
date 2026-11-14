#!/bin/bash
# core A after batchD: deterministic segments at every small n, then the next torus (1,2),(0,b)
cd "$(dirname "$0")"
while pgrep -f batchD.sh > /dev/null; do sleep 5; done
for n in 5 6 7 8 9 10 11 12; do python3 run.py run seg_det_n$n det $((n+3)) 8 30 64 4 26112 3; done
for n in 14 15 16 18 19 20; do python3 run.py run seg_det_n$n det $((n+3)) 8 50 256 4 26112 3; done
for n in 22 23 24; do python3 run.py run seg_det_n$n det $((n+3)) 8 100 256 4 26112 3; done
python3 run.py run det_k2_b16 det 16 8 60 256 4 26112 0 2
python3 run.py run det_k2_b20 det 20 8 120 256 4 26112 0 2
python3 run.py run det_k2_b24 det 24 8 400 256 4 26112 0 2
python3 run.py run det_k2_b28 det 28 8 2400 256 4 26112 0 2
