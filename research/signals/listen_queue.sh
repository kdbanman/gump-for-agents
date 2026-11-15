#!/bin/bash
# A worker for the queue of sat_listen.py instances (one argument line per instance in QUEUE; output appended to OUT).
# Start up to three:  bash listen_queue.sh QUEUE OUT &
cd "$(dirname "$0")"
Q=$1; OUT=$2
while true; do
  line=$(flock "$Q.lock" sh -c "head -n1 '$Q'; sed -i 1d '$Q'")
  [ -z "$line" ] && break
  python3 sat_listen.py $line --minutes 25 2>&1 | grep -v "^building" >> "$OUT"
done
