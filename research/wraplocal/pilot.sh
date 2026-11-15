#!/bin/bash
# pilot survey: 1024 replicas, 300 burn, 3000 measured generations per torus (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")/../.."
for t in "2 2 12" "1 10 24" "1 12 28" "1 3 24" "1 3 28" "1 5 24" "1 7 28" "1 5 28" "1 4 23" "1 4 24" "1 4 28" "1 4 25" "6 0 6" "1 7 24"; do
  python3 research/wraplocal/live.py run $t 16 300 3000 101
done
