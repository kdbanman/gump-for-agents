#!/bin/sh
# verdict 1, the largest hull face (second core, from 09:00 UTC): model R = 13, w = 4, five 20-minute pieces
cd "$(dirname "$0")"
for s in 1 2 3 4 5; do QS_SETTLE=1 python3 run.py model 13 4 1200 200 40$s; done
