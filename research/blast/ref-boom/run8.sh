#!/bin/sh
# wide faces of 126-192 cells (binary rbw = final rb.c: MAXN 2048, 8 count planes, RB_STOP = wall-clock stop). Four cores.
# started 06:42 UTC; every job stops at 06:59:20 UTC (RB_STOP=1794985160), the 126-cell job at 06:47 (then a long 48-cell run for the kill law)
S=../../scratch/blast/ref-boom
(RB_STOP=1794985160 nice -n 5 ./rbw ahead 8 0 8 401 1e9 $S/a192.txt) &
(RB_STOP=1794985160 nice -n 5 ./rbw ahead 4 4 12 402 1e9 $S/a144.txt) &
(RB_STOP=1794985160 nice -n 5 ./rbw ahead 1 4 21 403 1e9 $S/a63L.txt) &
(RB_STOP=1794984441 nice -n 5 ./rbw ahead 6 0 7 404 1e9 $S/a126.txt; RB_STOP=1794985160 nice -n 5 ./rbw ahead 4 0 4 405 1e9 $S/a48L.txt) &
(for v in "6 0 7" "4 4 12" "8 0 8"; do RB=rbw HB=64 nice -n 5 python3 val.py $v 200 2>&1 | tail -3; done; RB=rbw HB=64 nice -n 5 python3 val.py 8 0 8 200 neg 2>&1 | tail -2) > $S/vallog.txt 2>&1 &
wait
