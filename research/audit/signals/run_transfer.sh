#!/bin/bash
# The transfer-graph table (one core, memory-capped).  Output: research/scratch/audit_signals/transfer_<tube>.txt
cd "$(dirname "$0")"
ulimit -v 6000000
for tb in ${TUBES:-22 23}; do
  out=../../scratch/audit_signals/transfer_$tb.txt; : > $out
  for ps in "1 1" "2 1" "3 1" "3 2" "4 1" "4 3" "5 1" "5 2" "5 3" "5 4" "6 1" "6 5"; do
    nice -n 10 timeout ${LIMIT:-1800} python3 transfer.py ${tb:0:1} ${tb:1:1} $ps 2>&1 | grep -E "RESULT|UNDEC|PULSE|oracle|rror" >> $out \
      || echo "tube $tb ($ps): no RESULT (timeout or memory)" >> $out
  done
done
