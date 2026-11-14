#!/bin/bash
# core A after batchD: is the 8-layer slab thick enough (m = 12)?; deterministic segments at every small n; the next torus (1,2),(0,b)
cd "$(dirname "$0")"
while pgrep -f batchD.sh > /dev/null; do sleep 5; done
python3 run.py run det12_b16 det 16 12 60 256 4
python3 run.py run seg_det12_n13 det 16 12 60 256 4 26112 3
python3 run.py run seg_det12_n21 det 24 12 150 256 4 26112 3
python3 run.py run seg_m6_n13 model 16 6 60 256 4 26112 3
python3 run.py run seg_m8_n13 model 16 8 60 256 4 26112 3
for n in 5 6 7 8 9 10 11 12; do python3 run.py run seg_det_n$n det $((n+3)) 8 30 64 4 26112 3; done
for n in 14 15 16 18 19 20; do python3 run.py run seg_det_n$n det $((n+3)) 8 50 256 4 26112 3; done
for n in 22 23 24; do python3 run.py run seg_det_n$n det $((n+3)) 8 100 256 4 26112 3; done
python3 run.py run det_k2_b16 det 16 8 60 256 4 26112 0 2
python3 run.py run det_k2_b20 det 20 8 120 256 4 26112 0 2
python3 run.py run det_k2_b24 det 24 8 400 256 4 26112 0 2
python3 run.py run det_k2_b28 det 28 8 2400 256 4 26112 0 2
