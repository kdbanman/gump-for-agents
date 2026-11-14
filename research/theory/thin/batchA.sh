#!/bin/bash
# deterministic rings, m = 8 (one core). Resumable: each call adds chunks.
cd "$(dirname "$0")"
python3 run.py run det_b16 det 16 8 60 256 4
python3 run.py run det_b20 det 20 8 60 256 4
python3 run.py run det_b24 det 24 8 120 256 4
python3 run.py run det_b28 det 28 8 180 256 4
python3 run.py run det_b32 det 32 8 400 256 4
python3 run.py run det_b36 det 36 8 800 256 4
python3 run.py run det_b40 det 40 8 2000 256 4
