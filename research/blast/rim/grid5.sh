#!/bin/bash
# second seeds for the mixed second difference at L 4 -> 5; odd widths 7 -> 9 at L = 5; the neighbour test:
# 8-row faces beside 10-row faces (prism(8,10,L): faces 2,3 have 8 rows over depth 10)
cd "$(dirname "$0")"
while pgrep -f "grid4.sh" > /dev/null; do sleep 1; done
./grid.sh 80 2 "8 8 5 0"
./grid.sh 100 1 "9 9 5 0"
./grid.sh 250 2 "10 10 5 0"
./grid.sh 40 1 "8 10 4 0"
./grid.sh 100 1 "8 10 5 0"
