#!/bin/bash
# symmetric prisms (T, T, L, 0): four equivalent faces of T rows over depth T, neighbours of the same width
cd "$(dirname "$0")"
./grid.sh 8 1 "6 6 4 0" "6 6 5 0" "8 8 3 0"
./grid.sh 15 1 "6 6 6 0" "10 10 3 0" "7 7 4 0"
./grid.sh 30 1 "6 6 7 0" "12 12 3 0" "7 7 5 0" "9 9 4 0"
./grid.sh 60 1 "10 10 4 0" "14 14 3 0"
./grid.sh 100 1 "8 8 6 0" "6 6 8 0" "12 12 4 0" "7 7 6 0"
