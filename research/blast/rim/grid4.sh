#!/bin/bash
# the decisive symmetric points: width 8 -> 10 -> 12 at L = 4, 5 and length 5 -> 6 at width 8
cd "$(dirname "$0")"
while pgrep -f "grid.sh 30 1" > /dev/null; do sleep 1; done
./grid.sh 50 1 "10 10 4 0"
./grid.sh 300 1 "10 10 5 0"
./grid.sh 140 1 "8 8 6 0" "12 12 4 0"
./grid.sh 60 1 "14 14 3 0"
