#!/bin/bash
# production: per torus two seeds x 2048 replicas (8 blocks of 512), 500 burn-in, 4000 measured generations; one core
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")/../.."
for t in "$@"; do
  for s in 201 202; do
    python3 research/wraplocal/live.py run $t 32 500 4000 $s
  done
done
