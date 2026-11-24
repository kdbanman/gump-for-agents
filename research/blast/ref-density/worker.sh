#!/bin/sh
# A worker: takes the first line of the queue file (under flock), runs it, repeats until the file is empty.
#   sh research/blast/ref-density/worker.sh QUEUEFILE       (lines are shell commands run from the repository root)
Q=$1
while :; do
  CMD=$(flock "$Q.lock" sh -c 'head -n 1 "$1"; tail -n +2 "$1" > "$1.tmp"; mv "$1.tmp" "$1"' _ "$Q")
  [ -z "$CMD" ] && exit 0
  echo "$(date -u +%H:%M:%S) start $CMD"
  sh -c "$CMD"
  echo "$(date -u +%H:%M:%S) done"
done
