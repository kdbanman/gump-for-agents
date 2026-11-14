#!/bin/bash
# PR 18 review CPU ensemble: 2 runs x 512 replicas x 3e6 generations after a 2000-generation burn-in
cd /home/user/gump-for-agents/research/scratch/pr18
for s in 901 902; do ./pc prog_o0.bin 8 0.4 $s 2000 3000000 40 run_s$s.tsv 2> run_s$s.log; done
