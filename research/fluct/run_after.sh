#!/bin/sh
# follow-up queue: waits for the given chain to finish, then runs its continuation (resumable top-ups)
cd "$(dirname "$0")/../.." || exit 1
Q="python3 research/fluct/qsd.py"
case "$1" in
  a) while pgrep -f "run_qsd.sh a" >/dev/null; do sleep 20; done
     research/fluct/run_qsd.sh b ;;
  s) while pgrep -f "run_sym.sh" >/dev/null; do sleep 20; done
     $Q snap research/data/cube16_gen1025000000.gump v 7200 1 lite
     $Q sym 45 c 5400 1 lite ;;
esac
