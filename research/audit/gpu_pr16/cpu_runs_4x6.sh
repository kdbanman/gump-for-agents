#!/bin/bash
# PR 16 review: a third batch of 4x6x8 (the GPU - CPU difference after cpu_runs_more.sh was 2.5 sigma); same settings.
cd "$(dirname "$0")/../../.."
( for s in $(seq 16126 16138); do taskset -c 0 python3 research/audit/gpu_pr14/cpu_channels.py run 4 6 8 2000000 $s 5; done ) &
( for s in $(seq 16139 16150); do taskset -c 1 python3 research/audit/gpu_pr14/cpu_channels.py run 4 6 8 2000000 $s 5; done ) &
wait
