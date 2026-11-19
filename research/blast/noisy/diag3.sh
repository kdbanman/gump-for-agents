#!/bin/sh
# More of diag2.sh's part (a): the sampler at 84 cells and eps = 1/16, odd sweeps on (WBACK 12) and off (WBACK 0),
# alternating on four cores for about 105 minutes (about 600 replications each), with ancestry lines.
#   sh research/blast/noisy/diag3.sh
# Why: on reads above off at 84 cells (+0.027 +- 0.028) and at 108 (+0.092 +- 0.050). With these rows the difference
# at 84 cells is known to about 0.014, where one replication's law has no long tail to hide behind.
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; D=$S/runs_diag; mkdir -p $D
[ -x $S/nz_anc ] || gcc -O3 -march=native -o $S/nz_anc $HERE/nz.c -lm
T0=$(date +%s)
for c in 0 1 2 3; do
  ( i=0; while [ $i -lt 20 ] && [ $(( $(date +%s) - T0 )) -lt 6100 ]; do
      nice -n 10 $S/nz_anc 13 sub $((13800 + 40 * c + i)) 10 28 3 8 50 15 32 24 12 64 > $D/anc_R13_M64_s$((13800 + 40 * c + i)).txt
      nice -n 10 $S/nz_anc 13 sub $((14000 + 40 * c + i)) 10 28 3 8 50 15 32 24 0 64 > $D/w0_R13_M64_s$((14000 + 40 * c + i)).txt
      i=$((i + 1)); done ) &
done
wait
echo "diag3 done after $(( ($(date +%s) - T0) / 60 )) minutes"
