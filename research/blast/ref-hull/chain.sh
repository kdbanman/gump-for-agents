#!/bin/sh
# chain.sh R K SEED0 OUT  -- K independent replications with the fixed parameters (see README)
R=$1; K=$2; S0=$3; OUT=$4
i=0
while [ $i -lt $K ]; do
  nice -n 10 ./rh run $R $((S0 + i)) 200000 60000 2 4 2 6 1 100000 >> $OUT
  i=$((i + 1))
done
