#!/bin/sh
# Follow-up to diag.sh (PI, 2026-11-18, for the review of pull request 39). CPU only, four cores, about an hour.
#   sh research/blast/noisy/diag2.sh
# (a) The sampler at 84 cells and eps = 1/16 with the odd sweeps on (WBACK 12) and off (WBACK 0), about 230
#     replications each, with ancestry lines: at 84 cells the chain will be known by brute force (the lead's rebuild),
#     so this says whether either form of the sampler is off. Output: scratch runs_diag/ (anc_R13_*, w0_R13_*).
# (b) A depth series at 63 cells by brute force: noise at depth >= DW under the watched face for DW = 1 .. 6
#     (>= 3 under the others, as always), at eps = 1/4 (M = B/4; B changes with the region). How far below a face is
#     its death decided? Output: scratch depth.txt, one BRUTE line per DW.
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; D=$S/runs_diag; mkdir -p $D
gcc -O3 -march=native -o $S/nz_anc $HERE/nz.c -lm
T0=$(date +%s)
one() { # R M SEED WBACK TAG
  case $1 in 11) LAM=18; NSW=38;; 13) LAM=28; NSW=50;; 15) LAM=38; NSW=65;; esac
  nice -n 10 $S/nz_anc $1 sub $3 10 $LAM 3 8 $NSW 15 32 24 $4 $2 > $D/$5_R$1_M$2_s$3.txt
}
loop() { # WBACK TAG SEED0 NMAX
  i=0; while [ $i -lt $4 ] && [ $(( $(date +%s) - T0 )) -lt 3000 ]; do one 13 64 $(($3 + i)) $1 $2; i=$((i + 1)); done
}
( loop 12 anc 13601 16 ) &
( loop 0 w0 13701 16 ) &
( i=0; while [ $i -lt 8 ] && [ $(( $(date +%s) - T0 )) -lt 3000 ]; do one 13 64 $((13651 + i)) 12 anc; one 13 64 $((13751 + i)) 0 w0; i=$((i + 1)); done ) &
( for dw in 6 5 4 3 2 1; do
    B=$($S/nz_anc 11 brute 1 2000 0 $dw 3 | sed 's/.* B \([0-9]*\) M .*/\1/')
    nice -n 10 $S/nz_anc 11 brute $((1200 + dw)) 12000000 $((B / 4)) $dw 3 >> $S/depth.txt
  done ) &
wait
echo "diag2 done after $(( ($(date +%s) - T0) / 60 )) minutes"
