#!/bin/sh
# second follow-up queue (resumable top-ups): s = after the side-16 top-up, a = after the large-R lite chain
cd "$(dirname "$0")/../.." || exit 1
Q="python3 research/fluct/qsd.py"
case "$1" in
  s) while pgrep -f "qsd.py snap" >/dev/null; do sleep 20; done
     $Q sym 41 c 3000 1 lite
     $Q sym 45 c 4200 1 lite ;;
  a) while pgrep -f "run_qsd.sh b" >/dev/null; do sleep 20; done
     $Q sym 43 c 4200 1 lite ;;
esac
