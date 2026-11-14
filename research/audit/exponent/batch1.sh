#!/bin/sh
# verdict 1, first pass (one core): hull truth and hull models, own seeds
cd "$(dirname "$0")"
python3 run.py hull 7 20 200 201
python3 run.py hull 11 150 200 202
python3 run.py hull 11 150 2000 203
for w in 3 4 5; do python3 run.py model 7 $w 20 200 21$w; done
for w in 3 4 5 6 8; do python3 run.py model 11 $w 120 200 22$w; done
python3 run.py model 9 5 30 200 235
python3 run.py model 9 6 30 200 236
python3 run.py model 9 8 30 200 238
