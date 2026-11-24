#!/bin/sh
# Third clean run (after clean_build2.sh): check.sh at HEAD builds every Gump.* module but not the root module
# `Gump` that Axioms.lean imports (and in mathlib/ not `GumpMath`, which mathlib/Axioms.lean imports), so on a fresh
# clone the axiom step fails, silently (lean's errors go to stdout, which is redirected into .lake/axioms.txt).
# Workaround here: build the two root modules by hand, then run check.sh, --long, --mathlib; then the 2026-11-18
# check.sh (commit 9ed370d; the Lean files are the same) once. One core, timed.
#   sh research/blast/ref-lean/clean_build3.sh   (log: research/scratch/blast/ref-lean/clean_build3.log)
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
B=$REPO/research/scratch/blast/ref-lean
export PATH=$HOME/.elan/bin:$PATH
export XDG_CACHE_HOME=$B/xdgcache MATHLIB_CACHE_DIR=$B/xdgcache/mathlib
stamp() { echo "== $(date -u +%H:%M:%S) $*"; }
t() { s=$(date +%s); "$@"; r=$?; echo "   exit $r, $(( $(date +%s) - s )) s"; return 0; }
cd $B/clone
stamp "lake build Gump (root module, by hand)"; ( cd research/blast/lean && t taskset -c 0 lake build Gump 2>&1 | tail -1 )
stamp "check.sh";            t taskset -c 0 sh research/blast/lean/check.sh
stamp "check.sh --long";     t taskset -c 0 sh research/blast/lean/check.sh --long
stamp "lake build GumpMath (root module, by hand)"; ( cd research/blast/lean/mathlib && t taskset -c 0 lake build GumpMath 2>&1 | tail -3 )
stamp "check.sh --mathlib";  t taskset -c 0 sh research/blast/lean/check.sh --mathlib
stamp "check.sh of 2026-11-18 (9ed370d)"; git checkout -q 9ed370d -- research/blast/lean/check.sh
t taskset -c 0 sh research/blast/lean/check.sh
t taskset -c 0 sh research/blast/lean/check.sh --mathlib
git checkout -q HEAD -- research/blast/lean/check.sh
stamp "done"
