#!/bin/bash
# Pulse search with unknown uniform background (repeat 1 cube): table of SAT / UNSAT / TIMEOUT.
#   bash bounds.sh > ../scratch/signals/bounds.log        (hours on one core at the default 300 s per instance)
#   LIMIT=120 TUBES="33 34" bash bounds.sh             (TUBES: tubes as two digits each; LIMIT: seconds per instance)
# Each instance is run with two solvers (CaDiCaL 1.5.3 and Glucose 4) so that an UNSAT does not rest on one program.
cd "$(dirname "$0")"
for tb in ${TUBES:-22 23 33 34}; do
  tube="${tb:0:1} ${tb:1:1}"
  for ps in "1 1" "2 1" "3 1" "3 2" "4 1" "4 3" "5 1" "5 2" "5 3" "5 4" "6 1" "6 5"; do
    for solver in cadical153 glucose4; do
      out=$(timeout ${LIMIT:-300} python3 sat_pulse.py $tube 13 $ps --solver $solver --timeout 100000 2>&1 | head -1)
      [ -z "$out" ] && out="TIMEOUT tube $tube N=13 (p,s)=($ps) ${LIMIT:-300}s"
      echo "$solver: $out"
    done
  done
done
