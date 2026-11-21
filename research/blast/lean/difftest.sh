#!/bin/sh
# Differential test of the Lean stepper against reference/oracle.py, state for state (see difftest.py):
#   sh research/blast/lean/difftest.sh [--quick]
# every neighbourhood state of every axis (3 x 2^13), a few hundred soups of many shapes, sizes and densities,
# catalogued and signal objects as seeds, the even-H torus (Gump.Torus.tstep, via TorusCheck.lean),
# the coverage of (axis, alive, neighbour count), and 15 mutants of the oracle's rule as negative controls.
# Bulk files go to research/scratch/blast/lean/difftest/ (ignored by git). Needs Lean (elan), python3, numpy.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$HERE/../../..; export PATH=$HOME/.elan/bin:$PATH
cd $HERE
lake build gumpcheck 2>&1 | tail -1
OUT=$ROOT/research/scratch/blast/lean/difftest
mkdir -p $OUT
python3 difftest.py $HERE/.lake/build/bin/gumpcheck $OUT "$@"
