#!/bin/bash
# core B (replaces the tail of batchC): the front's distance from a wall in a long segment, then the 37-site segment
cd "$(dirname "$0")"
python3 run.py run seg_det_n61 det 64 8 1500 256 2 26112 3
python3 run.py run seg_det_n37 det 40 8 1500 256 4 26112 3
python3 run.py run seg_det_n13 det 16 8 60 256 4 26112 3
python3 run.py run seg_det_n45 det 48 8 1800 256 4 26112 3
