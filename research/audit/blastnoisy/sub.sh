#!/bin/sh
# Replications of the pull request's sampler (binary built from its nz.c, unmodified unless BIN says otherwise).
#   sh research/audit/blastnoisy/sub.sh BIN R M SEED0 NRUNS LAM1 DELTA NSWEEP TAG [NREP=10] [KFLIP=15]
# Each run (seed SEED0 + i) has its own 512 lanes and makes NREP replications; the other parameters are the frozen ones
# (NBATCH 8, TPRE 32, TWIN 24, WBACK 12).  Output: research/scratch/audit_noisy/runs/<TAG>_s<seed>.txt
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/audit_noisy; mkdir -p $S/runs
BIN=$1; R=$2; M=$3; SEED0=$4; NRUNS=$5; LAM=$6; DELTA=$7; NSW=$8; TAG=$9; NREP=${10:-10}; KF=${11:-15}
i=0
while [ $i -lt $NRUNS ]; do
  seed=$((SEED0 + i))
  $S/$BIN $R sub $seed $NREP $LAM $DELTA 8 $NSW $KF 32 24 12 $M > $S/runs/${TAG}_s$seed.tmp && mv $S/runs/${TAG}_s$seed.tmp $S/runs/${TAG}_s$seed.txt
  i=$((i + 1))
done
