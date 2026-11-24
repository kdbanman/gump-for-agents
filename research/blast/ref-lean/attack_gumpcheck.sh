#!/bin/sh
# Referee's attacks on the executable tie (REVIEW.md, section 5): gumpcheck's parsing and set comparison, and the
# way check.sh uses gumpcheck, difftest and the census. Runs on the clean clone made by clean_build.sh; edits nothing
# outside research/scratch/blast/ref-lean.
#   sh research/blast/ref-lean/attack_gumpcheck.sh      (about two minutes)
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
B=$REPO/research/scratch/blast/ref-lean
L=$B/clone/research/blast/lean
G=$L/.lake/build/bin/gumpcheck
W=$B/attack; rm -rf $W; mkdir -p $W
export PATH=$HOME/.elan/bin:$PATH
run() { label=$1; shift; out=$("$@" 2>&1); rc=$?; echo "[$label] exit $rc: $(echo "$out" | tail -1)"; }

python3 $L/oracle_states.py $W/good.txt 1 60 5 0.4
run "a right file (oracle soup 1, 60 generations)" $G states $W/good.txt
# 1. one cell of generation 30 moved: caught by gumpcheck itself
awk 'BEGIN{g=-1} /^G/{g=$2; n=0; print; next} {n++; if (g==30 && n==1) {print $1+2, $2, $3} else print}' $W/good.txt > $W/moved.txt
run "one cell of generation 30 moved" $G states $W/moved.txt
# 2. files that are wrong but pass
: > $W/empty.txt
run "an empty file" $G states $W/empty.txt
awk '/^G 1 /{exit} {print}' $W/good.txt > $W/onlyseed.txt
run "only generation 0" $G states $W/onlyseed.txt
awk '/^G 11 /{exit} {print}' $W/good.txt > $W/truncated.txt
run "truncated after generation 10 (of 60)" $G states $W/truncated.txt
sed 's/^\([0-9-]*\) \([0-9-]*\) \([0-9-]*\)$/\1,\2,\3/' $W/good.txt > $W/commas.txt
run "every cell line written x,y,z (none parses)" $G states $W/commas.txt
awk '/^G/{print "G 0 999"; next} {print}' $W/good.txt > $W/headers.txt
run "every header says G 0 999" $G states $W/headers.txt
awk 'BEGIN{g=-1} /^G/{g=$2; print; next} {print} g==20 && !done {print "7 7 7 7"; print "1 1 1"; done=1}' $W/good.txt > $W/junk.txt
run "generation 20 also lists '7 7 7 7' and the non-cell '1 1 1'" $G states $W/junk.txt
# 3. a right file in another dress
sed 's/$/\r/' $W/good.txt > $W/crlf.txt
run "the right file with CRLF line endings" $G states $W/crlf.txt
sed 's/ /\t/g' $W/good.txt > $W/tabs.txt
run "the right file with tabs between coordinates" $G states $W/tabs.txt

# 4. check.sh's verdict does not depend on gumpcheck states, difftest or the census: a python3 shim that corrupts
#    each soup written by oracle_states.py (one cell of generation 30 moved), and makes difftest.py and
#    census_check.py report failure and exit 1. Everything else is the real python3.
mkdir -p $W/shim
REAL=$(command -v python3)
cat > $W/shim/python3 <<EOF
#!/bin/sh
case "\$1" in
  *oracle_states.py) $REAL "\$@" || exit \$?
     awk 'BEGIN{g=-1} /^G/{g=\$2; n=0; print; next} {n++; if (g==30 && n==1) {print \$1+2, \$2, \$3} else print}' "\$2" > "\$2.x" && mv "\$2.x" "\$2" ;;
  *difftest.py) echo "difftest: FAIL (shim)"; exit 1 ;;
  *census_check.py) echo "census: 0 of 1307 (shim)"; exit 1 ;;
  *) exec $REAL "\$@" ;;
esac
EOF
chmod +x $W/shim/python3
echo "--- check.sh --long with the shim (state comparison corrupted; difftest and census fail):"
( cd $B/clone && PATH=$W/shim:$PATH sh research/blast/lean/check.sh --long; echo "check.sh exit status: $?" ) 2>&1 | grep -v "^  " | tail -12
