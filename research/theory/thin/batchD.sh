#!/bin/bash
# core A after det_b36: exact 7-site segment, finer deterministic segments, the depth ladder on segments
cd "$(dirname "$0")"
while pgrep -f "run.py run det_b36" > /dev/null; do sleep 5; done
python3 sweep.py seg 7
python3 run.py run seg_det_n17 det 20 8 90 256 4 26112 3
python3 run.py run seg_det_n25 det 28 8 240 256 4 26112 3
for w in 1 2 3 4 5; do python3 run.py run seg_m${w}_n13 model 16 $w 60 256 4 26112 3; done
for w in 1 2 3 4 5; do python3 run.py run seg_m${w}_n21 model 24 $w 150 256 4 26112 3; done
python3 run.py run seg_det_n33 det 36 8 900 256 4 26112 3
