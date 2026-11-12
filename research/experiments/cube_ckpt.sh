#!/bin/sh
# Closed cube of side N, run to its end in checkpointed chunks so a killed process loses at most one chunk.
# Usage (from repo root): research/experiments/cube_ckpt.sh N [CHUNK_GENS]
# Re-running resumes from research/scratch/cubes/cubeN.ckpt.gump. Result: cubeN.summary.json, evN.jsonl.
n=$1; chunk=${2:-25000000}; D=research/scratch/cubes; G=engine/target/release/gump
mkdir -p $D; snap=$D/cube$n.ckpt.gump
[ -f $snap ] || : > $D/ev$n.jsonl
while :; do
  if [ -f $snap ]; then src="--snapshot $snap"; else src="--cube $n"; fi
  $G run $src --gens $chunk --snapshot-out $snap.tmp --events $D/ev$n.part.jsonl --every 64 --out /dev/null --hash-window 65536 | tail -1 > $D/cube$n.last.json || exit 1
  cat $D/ev$n.part.jsonl >> $D/ev$n.jsonl
  status=$(python3 -c "import json;print(json.load(open('$D/cube$n.last.json'))['status'])") || exit 1
  if [ "$status" != running ]; then cp $D/cube$n.last.json $D/cube$n.summary.json; break; fi
  mv $snap.tmp $snap
done
