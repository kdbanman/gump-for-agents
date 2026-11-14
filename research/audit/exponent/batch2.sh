#!/bin/sh
# verdict 1, periodic faces (one core): deterministic 12-layer slabs and the driven-face models; then the toy windows
cd "$(dirname "$0")"
python3 run.py slab 3 3 25 300 301
python3 run.py slab 3 4 40 300 302
python3 run.py slab 4 5 150 300 303
python3 run.py slab 5 5 660 300 304
for w in 3 4 5 6; do QS_SETTLE=1 python3 run.py slabmodel 3 3 $w 20 300 31$w; done
for w in 3 4 5 6; do QS_SETTLE=1 python3 run.py slabmodel 4 5 $w 100 300 32$w; done
QS_SETTLE=1 python3 run.py slabmodel 4 4 4 40 300 334
QS_SETTLE=1 python3 run.py slabmodel 5 5 5 600 300 335
QS_SETTLE=1 python3 run.py slabmodel 5 5 6 600 300 336
../../scratch/audit_exponent/toygap run 777 600 2000000 > ../../scratch/audit_exponent/toygap_777.txt
