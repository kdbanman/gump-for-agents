#!/bin/bash
# loop^2 9 tube lifetimes (after the density production); one core
export OMP_NUM_THREADS=1
cd "$(dirname "$0")/../.."
while pgrep -f wraplocal/prod.sh > /dev/null; do sleep 15; done
python3 research/wrap/validate.py 1 7 24 1500
python3 research/wrap/validate.py 1 8 27 1500
python3 research/wraplocal/tsjob.py job 1 7 24 22000000 309001
python3 research/wraplocal/tsjob.py job 1 8 27 100000000 309002
