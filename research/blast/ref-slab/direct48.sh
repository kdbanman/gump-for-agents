#!/bin/bash
# direct count through the sampler's own pipeline (LAM1 = 0: no levels, no sweeps), 40 short runs of 100 replications
# (short, so that immortal "stuck" lanes cannot accumulate in the persistent ensemble)
: > out/sub_48_directshort.txt
for s in $(seq 7501 7540); do WD=6 nice -n 10 ./ss_diag g_4_0_4.bin sub $s 100 0 3 8 0 4 32 24 - 12 | grep "^REP" >> out/sub_48_directshort.txt; done
