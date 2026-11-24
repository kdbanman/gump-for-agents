#!/bin/sh
# Everything this directory claims, in one command (about two minutes from nothing on one core; seconds once built):
#   sh research/blast/lean/check.sh [--long] [--mathlib]
# --long adds the side-11 log (4,218 generations), the differential test against the oracle (difftest.sh --quick,
# about 3 minutes) and the kernel-checked census of the atlas catalogue (census_check.py, about a minute).
# --mathlib builds the Mathlib package (needs `cd mathlib && lake exe cache get` once, network, 7 GB) and checks
# its axioms: T5 and the certificate lemmas.
# 1. the Lean development builds (every theorem is checked by Lean's kernel);
# 2. no `sorry`, and no theorem rests on anything but Lean's three standard axioms;
# 3. the Lean rule, run by the stepper built on `Gump.step`, prints the 2012 closed-cube logs in
#    reference/golden/ line for line (sides 8, 9, 10; side 11, 4,218 generations, with --long);
# 4. the same stepper equals reference/oracle.py state for state on three soups for 60 generations.
# Needs Lean 4 (elan; the toolchain is pinned in lean-toolchain), python3 and numpy.
set -e
LONG=no; MATH=no
for a in "$@"; do [ "$a" = "--long" ] && LONG=yes; [ "$a" = "--mathlib" ] && MATH=yes; done
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$HERE/../../..; export PATH=$HOME/.elan/bin:$PATH
cd $HERE
# STATEMENTS.md must be what statements.py writes from the sources and the statements_*.json rows (a stale copy once
# went unnoticed); --check writes nothing and exits non-zero on any difference
python3 statements.py --check || { echo "FAIL: STATEMENTS.md is stale"; exit 1; }
# every module in Gump/ is built, whether or not Gump.lean imports it
MODS=$(ls Gump/*.lean | sed 's|Gump/\(.*\)\.lean|Gump.\1|')
mkdir -p .lake
lake build Gump $MODS gumpcheck > .lake/build.log 2>&1 || { tail -20 .lake/build.log; echo "FAIL: build"; exit 1; }
tail -1 .lake/build.log
if grep -n "declaration uses 'sorry'" .lake/build.log; then echo "FAIL: sorry"; exit 1; fi
if grep -n "sorry" Gump/*.lean Check.lean; then echo "FAIL: sorry"; exit 1; fi
# native_decide (the compiler trusted as a prover) only in files named *Native.lean, for long base runs, and their
# theorems only in Axioms*Native.lean: a separate tier, counted apart below (in Lean 4.36 such a theorem shows an
# auxiliary axiom of its own in `#print axioms`, which the first tier's filter rejects).
if grep -n "native_decide" $(ls Gump/*.lean | grep -v "Native\.lean$"); then echo "FAIL: native_decide outside *Native.lean"; exit 1; fi
: > .lake/axioms.txt
for f in $(ls Axioms*.lean | grep -v "Native\.lean$"); do lake env lean $f >> .lake/axioms.txt || { echo "FAIL: $f does not run"; exit 1; }; done
if [ ! -s .lake/axioms.txt ]; then echo "FAIL: no axioms were printed"; exit 1; fi
if grep -v "depends on axioms: \[propext, Classical.choice, Quot.sound\]$" .lake/axioms.txt | grep -v "does not depend on any axioms$" | grep -v "depends on axioms: \[propext\]$" | grep -v "depends on axioms: \[propext, Quot.sound\]$" | grep -v "depends on axioms: \[Classical.choice, Quot.sound\]$" | grep -v "depends on axioms: \[propext, Classical.choice\]$" | grep -v "depends on axioms: \[Quot.sound\]$" | grep -v "depends on axioms: \[Classical.choice\]$"; then echo "FAIL: an unexpected axiom"; exit 1; fi
echo "$(wc -l < .lake/axioms.txt) headline theorems: no sorry, no axiom beyond propext, Classical.choice, Quot.sound"
if ls Axioms*Native.lean > /dev/null 2>&1; then
  : > .lake/axioms_native.txt
  for f in Axioms*Native.lean; do lake env lean $f >> .lake/axioms_native.txt || { echo "FAIL: $f does not run"; exit 1; }; done
  if grep -n "sorryAx" .lake/axioms_native.txt; then echo "FAIL: sorry in the native tier"; exit 1; fi
  echo "$(wc -l < .lake/axioms_native.txt) theorems in the second tier (base runs by native_decide: these trust the compiler, Lean.ofReduceBool)"
fi
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
  # no pipe on the checker: its exit status is the verdict, and its line must say 60 generations and 0 mismatches
  .lake/build/bin/gumpcheck states $T/soup.txt > $T/out.txt || { cat $T/out.txt; echo "FAIL: the Lean stepper and the oracle differ on soup $s"; exit 1; }
  grep -q ": 60 generations compared with the oracle state for state, 0 mismatches" $T/out.txt || { cat $T/out.txt; echo "FAIL: soup $s was not compared in full"; exit 1; }
  sed "s|$T/soup.txt|oracle, soup $s|" $T/out.txt
done
rm -rf $T
if [ "$LONG" = yes ]; then
  sh difftest.sh --quick > .lake/difftest.log 2>&1 || { tail -20 .lake/difftest.log; echo "FAIL: the differential test"; exit 1; }
  tail -3 .lake/difftest.log
  python3 census_check.py $ROOT/research/scratch/blast/lean/census > .lake/census.log 2>&1 || { tail -20 .lake/census.log; echo "FAIL: the census"; exit 1; }
  tail -2 .lake/census.log
fi
if [ "$MATH" = yes ]; then
  ( cd mathlib && MM=$(ls GumpMath/*.lean | sed 's|GumpMath/\(.*\)\.lean|GumpMath.\1|')
    mkdir -p .lake
    lake build GumpMath $MM > .lake/build.log 2>&1 || { tail -20 .lake/build.log; echo "FAIL: mathlib build"; exit 1; }
    if grep -n "declaration uses 'sorry'" .lake/build.log; then echo "FAIL: sorry (mathlib)"; exit 1; fi
    if grep -n "sorry\|native_decide" GumpMath/*.lean; then echo "FAIL: sorry or native_decide (mathlib)"; exit 1; fi
    : > .lake/axioms.txt; for f in $(ls Axioms*.lean | grep -v "Native\.lean$"); do lake env lean $f >> .lake/axioms.txt || { echo "FAIL: mathlib/$f does not run"; exit 1; }; done
    if [ ! -s .lake/axioms.txt ]; then echo "FAIL: no axioms were printed (mathlib)"; exit 1; fi
    if grep -v "depends on axioms: \[propext, Classical.choice, Quot.sound\]$" .lake/axioms.txt | grep -v "does not depend on any axioms$" | grep -v "depends on axioms: \[propext\]$" | grep -v "depends on axioms: \[propext, Quot.sound\]$"; then echo "FAIL: an unexpected axiom (mathlib)"; exit 1; fi
    echo "mathlib package: $(wc -l < .lake/axioms.txt) theorems, no sorry, no axiom beyond the standard three" )
fi
echo "lean: all checks passed"
