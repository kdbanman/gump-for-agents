#!/bin/sh
# resumable: each call tops up to the target wall time (seconds). Two chains, one core each.
cd "$(dirname "$0")/../.." || exit 1
case "$1" in
  a) for x in "7 300" "9 900" "11 2700" "13 4800"; do set -- $x; python3 research/fluct/qsd.py $1 $2 4; done ;;
  b) for x in "15 1500" "17 1500" "19 1800"; do set -- $x; python3 research/fluct/qsd.py $1 $2 2 lite; done ;;
esac
