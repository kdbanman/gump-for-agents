#!/bin/sh
# Second clean run, after clean_build.sh found that check.sh cannot start on a fresh clone (it redirects into
# .lake/build.log before anything has created .lake). The only change: `mkdir .lake` in the clone. Reuses the
# clone and the Mathlib cache that clean_build.sh downloaded into research/scratch/blast/ref-lean.
#   sh research/blast/ref-lean/clean_build2.sh   (log: research/scratch/blast/ref-lean/clean_build2.log)
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
B=$REPO/research/scratch/blast/ref-lean
export PATH=$HOME/.elan/bin:$PATH
export XDG_CACHE_HOME=$B/xdgcache MATHLIB_CACHE_DIR=$B/xdgcache/mathlib
stamp() { echo "== $(date -u +%H:%M:%S) $*"; }
t() { s=$(date +%s); "$@"; r=$?; echo "   exit $r, $(( $(date +%s) - s )) s"; return 0; }
cd $B/clone && git log -1 --format='%H' && git status --short | head
mkdir research/blast/lean/.lake
stamp "check.sh";            t taskset -c 0 sh research/blast/lean/check.sh
stamp "check.sh (again, built)"; t taskset -c 0 sh research/blast/lean/check.sh
stamp "check.sh --long";     t taskset -c 0 sh research/blast/lean/check.sh --long
stamp "check.sh --mathlib";  t taskset -c 0 sh research/blast/lean/check.sh --mathlib
stamp "done"
