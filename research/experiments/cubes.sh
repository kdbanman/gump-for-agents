#!/bin/sh
# Closed cubes beyond the original's series: lifetime + peel schedule. Usage: cubes.sh N [N...]
# Writes research/scratch/cubes/cubeN.summary.json and evN.jsonl (layer deaths, resolution 64 gens).
G=engine/target/release/gump; D=research/scratch/cubes; mkdir -p $D
for n in "$@"; do
  $G run --cube $n --events $D/ev$n.jsonl --every 64 --out /dev/null --hash-window 65536 | tail -1 > $D/cube$n.summary.json
done
