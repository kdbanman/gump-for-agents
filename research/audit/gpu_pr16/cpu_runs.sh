#!/bin/bash
# PR 16 review: channel-resolved CPU runs of the A = 72 pair (rep.c stepper via research/audit/gpu_pr14/cpu_channels.py).
# Output: research/scratch/audit_gpu_pr14/ch_<slab>_s<seed>.npz; analyze with
#   python3 research/audit/gpu_pr14/cpu_channels.py analyze 3 8 8 2048 ; ... analyze 4 6 8 65536
cd "$(dirname "$0")/../../.."
python3 research/audit/gpu_pr14/cpu_channels.py validate 3 8 8 2000 24 || exit 1
python3 research/audit/gpu_pr14/cpu_channels.py validate 4 6 8 2000 12 || exit 1
( for s in $(seq 16001 16011); do taskset -c 0 python3 research/audit/gpu_pr14/cpu_channels.py run 3 8 8 500000 $s 10; done ) &
( for s in $(seq 16101 16106); do taskset -c 1 python3 research/audit/gpu_pr14/cpu_channels.py run 4 6 8 2000000 $s 5; done ) &
wait
