#!/bin/bash
# PR 18 review, follow-up (plan: REVIEW-gpu-pr18.md, "Follow-up 2026-11-14: the 4x5 point"): 16 chunks, seeds 921..936,
# each 512 replicas x 3e6 generations after a 2000-generation burn-in, lean program (rhombi 1x1 ... 4x5), 30 batches;
# every hit of 3x4, 4x4, 4x5 logged. A chunk is complete when its .tsv ends with the "#masked" line; the driver skips
# complete chunks, so it can be restarted after a stop (an incomplete chunk is rerun from scratch). Optional argument:
# the most chunks to run in this call (5 chunks ~ 103 min, under the 2-hour limit on background jobs).
D=/home/user/gump-for-agents/research/scratch/pr18
cd $D
[ -f prog_lean.bin ] || python3 /home/user/gump-for-agents/research/audit/gpu_pr18/geom18.py prog_lean.bin 0 lean
MAX=${1:-16}; k=0
for s in $(seq 921 936); do
  grep -q '^#masked' f2_s$s.tsv 2>/dev/null && continue
  [ $k -ge $MAX ] && exit 0; k=$((k+1))
  ./pc prog_lean.bin 8 0.4 $s 2000 3000000 30 f2_s$s.tsv -e 'rhombus 3x4' -e 'rhombus 4x4' -e 'rhombus 4x5' -E f2_s$s.ev 2> f2_s$s.log
done
echo ALLDONE
