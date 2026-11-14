#!/bin/bash
# PR 16 review: more seeds of the A = 72 pair, after cpu_runs.sh (same settings).
cd "$(dirname "$0")/../../.."
( for s in $(seq 16012 16040); do taskset -c 0 python3 research/audit/gpu_pr14/cpu_channels.py run 3 8 8 500000 $s 10; done ) &
( for s in $(seq 16107 16125); do taskset -c 1 python3 research/audit/gpu_pr14/cpu_channels.py run 4 6 8 2000000 $s 5; done ) &
wait
