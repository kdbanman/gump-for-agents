#!/bin/sh
# Everything this directory claims, in one command (about 10 seconds; with --long about 80):
#   sh research/blast/lean/check.sh [--long]
# 1. the Lean development builds (every theorem is checked by Lean's kernel);
# 2. no `sorry`, and no theorem rests on anything but Lean's three standard axioms;
# 3. the Lean rule, run by the stepper built on `Gump.step`, prints the 2012 closed-cube logs in
#    reference/golden/ line for line (sides 8, 9, 10; side 11, 4,218 generations, with --long);
# 4. the same stepper equals reference/oracle.py state for state on three soups for 60 generations.
# Needs Lean 4 (elan; the toolchain is pinned in lean-toolchain), python3 and numpy.
set -e
LONG=no; [ "$1" = "--long" ] && LONG=yes
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$HERE/../../..; export PATH=$HOME/.elan/bin:$PATH
cd $HERE
lake build Gump gumpcheck 2>&1 | tail -1
if grep -n "sorry" Gump/*.lean Check.lean; then echo "FAIL: sorry"; exit 1; fi
lake env lean Axioms.lean > .lake/axioms.txt
if grep -v "depends on axioms: \[propext, Classical.choice, Quot.sound\]$" .lake/axioms.txt | grep -v "does not depend on any axioms$"; then echo "FAIL: an unexpected axiom"; exit 1; fi
echo "$(wc -l < .lake/axioms.txt) headline theorems: no sorry, no axiom beyond propext, Classical.choice, Quot.sound"
T=$(mktemp -d)
for t in "08 13 29 23" "09 17 35 71" "10 17 37 65" "11 19 41 4218"; do
  set -- $t
  if [ $1 = 11 ] && [ "$LONG" != yes ]; then continue; fi
  f=$(ls $ROOT/reference/golden/legacy_cube_side$1_*.txt)
  .lake/build/bin/gumpcheck cube $2 $3 $4 > $T/cube.txt
  if awk '{print $1, $2}' $f | cmp -s - $T/cube.txt; then echo "2012 log, closed cube of side $1: identical, $(wc -l < $f) lines"; else echo "FAIL: side $1 differs from the 2012 log"; exit 1; fi
done
for s in 1 2 3; do
  python3 oracle_states.py $T/soup.txt $s 60 $((4 + s)) 0.4
  .lake/build/bin/gumpcheck states $T/soup.txt | sed "s|$T/soup.txt|oracle, soup $s|"
done
rm -rf $T
echo "lean: all checks passed"
