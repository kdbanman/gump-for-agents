#!/bin/sh
# nuchain.sh OUTDIR : plain-running dip rates, 8 independent seeds per radius (lamA = ceil(P-bar))
O=$1
run() { R=$1; G=$2; LA=$3; for s in 1 2 3 4 5 6 7 8; do nice -n 10 ./rh nu $R $s $G $LA >> $O/nu$R.txt; done; }
run 17 200000 70
run 15 200000 56
run 13 150000 43
run 11 150000 32
run 9 150000 22
echo done > $O/nu.done
run 19 100000 86
echo done > $O/nu19.done
