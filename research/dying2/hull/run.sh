#!/bin/bash
# Production runs of hd.c (research/dying2/hull/README.md). Bulk output in research/scratch/dying2-hull/.
#   bash research/dying2/hull/run.sh 11 0.1667 1100      # R, hours, seed0  (3 threads: seeds seed0..seed0+2)
#   bash research/dying2/hull/run.sh 13 1.6667 1300
set -e
R=$1; H=$2; S=$3
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
SCR=$ROOT/research/scratch/dying2-hull
GCC=$(ls -d "$LOCALAPPDATA"/Microsoft/WinGet/Packages/BrechtSanders.WinLibs*/mingw64/bin 2>/dev/null | head -1)
[ -n "$GCC" ] && export PATH="$GCC:$PATH"
cd "$SCR"
[ hdx.exe -nt "$ROOT/research/dying2/hull/hd.c" ] || gcc -O3 -march=native -static -Wall -o hdx.exe "$ROOT/research/dying2/hull/hd.c" -lpthread
if [ "$R" = 11 ]; then U=32; K=12; else U=43; K=17; fi
#        vessel     seed0 thr hours prefix     U  KDUMP CAPREC MAXDEATHS NULLEV NULLCAP HD   SD   HR   SR
./hdx.exe run hv_$R.bin $S 3 $H run_${R}_s$S $U $K 300 1500 9973 30000 4096 1024 1024 256
echo "done R=$R seeds $S.. $(date -u)"
