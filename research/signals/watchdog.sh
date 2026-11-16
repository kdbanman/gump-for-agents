#!/bin/bash
# pysat's interrupt does not fire on these instances (README section 23): kill from outside.
# sat_listen.py instances older than 25 min and sat_gun.py ones older than 20 min; a CUT line is written for each.
OUT=$1
while true; do
  ps -eo pid=,etimes=,args= | grep -E "python3 sat_(listen|gun)\.py" | grep -v grep | while read pid et rest; do
    lim=1500; case "$rest" in *sat_gun*) lim=1200;; esac
    if [ "$et" -gt "$lim" ]; then kill $pid; echo "CUT     (killed from outside after ${et}s) $rest" >> "$OUT"; fi
  done
  sleep 30
done
