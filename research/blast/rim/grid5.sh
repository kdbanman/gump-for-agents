#!/bin/bash
# neighbour test: 8-row faces beside 10-row faces (prism(8,10,L): faces 2,3 have 8 rows, depth 10); rim kinds swapped (par 1)
cd "$(dirname "$0")"
while pgrep -f "grid4.sh" > /dev/null; do sleep 1; done
./grid.sh 40 1 "8 10 4 0"
./grid.sh 120 1 "8 10 5 0"
./grid.sh 30 1 "8 8 4 1"
./grid.sh 60 1 "8 8 5 1"
