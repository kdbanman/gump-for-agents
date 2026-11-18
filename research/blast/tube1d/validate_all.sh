#!/bin/sh
# Deterministic limit of tube1d.c against reference/oracle.py, state for state, 1500 generations, three tori and two
# tubes, plus the negative control (one wrong neighbour must fail).  About 2 minutes.
#   sh validate_all.sh [EXE]
cd "$(dirname "$0")"
E=${1:-../../scratch/blast/tube1d/tube1d}
[ -x "$E" ] || { mkdir -p ../../scratch/blast/tube1d; gcc -O3 -march=native -o "$E" tube1d.c -lm; }
python3 validate.py $E 4 0 4 8 12 1 1500
python3 validate.py $E 1 4 21 8 21 2 1500
python3 validate.py $E 1 12 28 8 28 3 1500
python3 validate.py $E 1 17 32 8 32 4 1500
python3 validate.py $E 1 3 25 7 25 5 1500
python3 validate.py $E 4 0 4 8 12 1 1500 bad
python3 validate.py $E 1 12 28 8 28 3 1500 bad
