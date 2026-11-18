#!/bin/sh
# wchain.sh OUTDIR : plain-running dip rates on slab tori; pilot for P-bar, lamA = ceil(P-bar), then 8 seeds
O=$1
run() { H=$1; K=$2; D=$3; G=$4
  A=$((3 * H * D))
  PB=$(./sl nu $H $K $D 999 6000 $((A / 2 + 1)) | awk '{for(i=1;i<=NF;i++){if($i=="sumP")s=$(i+1); if($i=="nP")n=$(i+1)}; printf "%d", int(s/n)+1}')
  for s in 1 2 3 4 5 6 7 8; do nice -n 10 ./sl nu $H $K $D $s $G $PB >> $O/w_${H}_${K}_${D}.txt; done
  echo "$H $K $D lamA $PB" >> $O/w.progress
}
run 4 0 4 400000
run 1 7 19 400000
run 1 4 21 400000
run 6 0 6 300000
run 1 4 28 300000
run 1 12 28 300000
run 1 16 36 300000
run 1 9 25 300000
run 1 17 32 300000
echo done > $O/w.done
