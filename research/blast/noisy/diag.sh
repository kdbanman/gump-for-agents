#!/bin/sh
# Two diagnostics asked for in the review of pull request 39 (PI, 2026-11-18). CPU only, three cores, under two hours.
#   sh research/blast/noisy/diag.sh
# Phase 1, ancestry: the frozen sampler with new seeds; nz.c now prints after each REP line a line
#   ANC rep : lambda:D/top ...   D = distinct initial chains among the chains at or below lambda, top = largest family's share.
# Phase 2, odd sweeps off (WBACK 0: every sweep proposes anywhere in the T generations), 108 cells, eps = 1/16.
# Output: research/scratch/blast/noisy/runs_diag/ (anc_*.txt and w0_*.txt). Runs are started only in the first 95 minutes.
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; D=$S/runs_diag; mkdir -p $D
gcc -O3 -march=native -o $S/nz_anc $HERE/nz.c -lm
T0=$(date +%s)
one() { # R M SEED WBACK TAG
  case $1 in 11) LAM=18; NSW=38;; 13) LAM=28; NSW=50;; 15) LAM=38; NSW=65;; esac
  nice -n 10 $S/nz_anc $1 sub $3 10 $LAM 3 8 $NSW 15 32 24 $4 $2 > $D/$5_R$1_M$2_s$3.txt
}
( one 15 128 15501 12 anc; one 15 128 15502 12 anc; one 15 128 15503 12 anc ) &
( one 15 64 15601 12 anc; one 15 64 15602 12 anc; one 15 64 15603 12 anc ) &
( one 11 16 11501 12 anc; one 11 4 11511 12 anc; one 13 64 13501 12 anc; one 15 32 15701 12 anc; one 15 32 15702 12 anc; one 15 32 15703 12 anc ) &
wait
echo "phase 1 done after $(( ($(date +%s) - T0) / 60 )) minutes"
for c in 0 1 2; do
  ( i=0; while [ $i -lt 14 ] && [ $(( $(date +%s) - T0 )) -lt 5700 ]; do one 15 128 $((15800 + 20 * c + i)) 0 w0; i=$((i + 1)); done ) &
done
wait
echo "phase 2 done after $(( ($(date +%s) - T0) / 60 )) minutes"
