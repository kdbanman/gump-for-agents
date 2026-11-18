#!/bin/sh
# Replications of the frozen sampler on the noisy chain; one core; needs no attention.
#   sh research/blast/noisy/run_sub.sh R M SEED0 NRUNS [NREP=10]
# NRUNS runs one after another with seeds SEED0, SEED0+1, ...; each run has its own 512 stationary lanes and makes
# NREP replications. eps = M / B (B = 256, 1024, 2048, 4096, 8192 for R = 11, 13, 15, 17, 19).
# Output: research/scratch/blast/noisy/runs/sub_R<R>_M<M>_s<SEED>.txt (complete REP lines are usable at any time).
# Analyse with: python3 research/blast/noisy/ana.py   and   python3 research/blast/noisy/fit.py
# Frozen parameters (PREDICTIONS.md block 2): LAM1 = round(P-bar - 2.5 sigma_P), DELTA 3, NBATCH 8,
# NSWEEP = round(0.6 A), KFLIP 15, TPRE 32, TWIN 24, WBACK 12; N = depth >= 6 under the watched face, >= 3 under the others.
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; mkdir -p $S/runs
[ -x $S/nz ] || gcc -O3 -march=native -o $S/nz $HERE/nz.c -lm
R=$1; M=$2; SEED0=$3; NRUNS=$4; NREP=${5:-10}
case $R in 9) LAM=10; NSW=27;; 11) LAM=18; NSW=38;; 13) LAM=28; NSW=50;; 15) LAM=38; NSW=65;; 17) LAM=51; NSW=81;; 19) LAM=65; NSW=99;; *) echo "no frozen parameters for R = $R"; exit 2;; esac
i=0
while [ $i -lt $NRUNS ]; do
  seed=$((SEED0 + i))
  nice -n 10 $S/nz $R sub $seed $NREP $LAM 3 8 $NSW 15 32 24 12 $M > $S/runs/sub_R${R}_M${M}_s$seed.txt
  i=$((i + 1))
done
