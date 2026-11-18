#!/bin/bash
# Prism grid: bash research/blast/rim/grid.sh TB SEED "T1 T2 L PAR" ...   (TB seconds per point at about 3.5e7 node-steps/s)
cd "$(dirname "$0")/../../.."
TB=$1; SEED=$2; shift 2
for v in "$@"; do
  set -- $v; n=$(( 12 * $1 * $2 * $3 / 8 * 1 )); n=$(python3 -c "print(int(1.5*$1*$2*$3))")
  gens=$(python3 -c "print(int($TB*3.5e7/$n))")
  nice -n 10 python3 research/blast/rim/run.py prism $1 $2 $3 $4 $gens $SEED
done
