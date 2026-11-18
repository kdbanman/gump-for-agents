#!/bin/bash
# wide symmetric prisms (all four faces equivalent, w rows, depth w) at short lengths: the marginal price of a row
cd "$(dirname "$0")"
while pgrep -f "grid.sh 25 1" > /dev/null; do sleep 2; done
./grid.sh 12 1 "8 8 3 0" "6 6 3 0"
./grid.sh 30 1 "10 10 3 0" "6 6 6 0"
./grid.sh 60 1 "12 12 3 0" "10 10 4 0"
./grid.sh 100 1 "14 14 3 0"
./grid.sh 150 1 "12 12 4 0" "8 8 6 0" "16 16 3 0"
