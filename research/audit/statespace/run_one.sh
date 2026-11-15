#!/bin/bash
# research/audit/statespace/run_one.sh KIND ARGS...   enumerate one vessel with the audit's own code
# writes research/scratch/audit_ss/NAME.{bin,out,champ,sample}; checks the table sample against geom.py's step
set -e
D=/home/user/gump-for-agents/research/audit/statespace
S=/home/user/gump-for-agents/research/scratch/audit_ss
mkdir -p $S
[ -x $S/aenum ] || cc -O3 -march=native -fopenmp -o $S/aenum $D/aenum.c
NAME=$(echo "$@" | tr ' ' '_')
python3 $D/geom.py write "$@" $S/$NAME.bin
OMP_NUM_THREADS=${OMP_NUM_THREADS:-2} $S/aenum $S/$NAME.bin $S/$NAME.champ $S/$NAME.sample 3000 > $S/$NAME.out
python3 - "$@" <<EOF
import sys; sys.path.insert(0, '$D'); import geom
v = geom.V(sys.argv[1], sys.argv[2:])
bad = sum(1 for l in open('$S/$NAME.sample') if v.step(int(l.split()[0], 16)) != int(l.split()[1], 16))
print('table sample vs python step:', 'OK' if bad == 0 else f'{bad} MISMATCHES')
EOF
cat $S/$NAME.out | grep -v transient_hist
