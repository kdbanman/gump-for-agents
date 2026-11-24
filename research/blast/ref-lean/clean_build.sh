#!/bin/sh
# Referee's clean-machine run of the Lean checks (research/blast/ref-lean/REVIEW.md, section "clean build").
#   sh research/blast/ref-lean/clean_build.sh COMMIT
# Clones the local repository into research/scratch/blast/ref-lean/clone (nothing from the authors' .lake),
# checks out COMMIT, and runs check.sh, check.sh --long, the Mathlib cache download into a fresh cache directory,
# and check.sh --mathlib, each on one core (taskset -c 0), timed. Log: research/scratch/blast/ref-lean/clean_build.log
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
B=$REPO/research/scratch/blast/ref-lean
C=${1:-HEAD}
export PATH=$HOME/.elan/bin:$PATH
export XDG_CACHE_HOME=$B/xdgcache          # a fresh Mathlib cache: nothing downloaded earlier is reused
export MATHLIB_CACHE_DIR=$B/xdgcache/mathlib
mkdir -p $B $XDG_CACHE_HOME
stamp() { echo "== $(date -u +%H:%M:%S) $*"; }
t() { s=$(date +%s); "$@"; r=$?; echo "   exit $r, $(( $(date +%s) - s )) s"; return 0; }
cd $B && rm -rf clone && git clone -q $REPO clone && cd clone && git checkout -q $C && git log -1 --format='%H %s'
ls research/blast/lean/.lake 2>/dev/null && echo "UNEXPECTED: .lake present in clone"
stamp "check.sh";            t taskset -c 0 sh research/blast/lean/check.sh
stamp "check.sh --long";     t taskset -c 0 sh research/blast/lean/check.sh --long
stamp "lake exe cache get";  ( cd research/blast/lean/mathlib && t taskset -c 0 lake exe cache get )
stamp "check.sh --mathlib";  t taskset -c 0 sh research/blast/lean/check.sh --mathlib
stamp "done"
