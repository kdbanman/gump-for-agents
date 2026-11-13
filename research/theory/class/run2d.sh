#!/bin/sh
# 2D test set: every cap of every family (bulk torus, then periodic strips 16 deep at three edge lengths)
cd "$(dirname "$0")"
for l in cross3 cross4 star2 tristar2 tristar3 tri18 vn tri6 kagome6 tri12 hex12 moore_r2 hex9 hex3 kagome4 kagome8; do
  python3 scan.py $l --sizes 12,20,28 --sec 10
done
