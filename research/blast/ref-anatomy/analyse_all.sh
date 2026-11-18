#!/bin/sh
# every table of REVIEW.md from the outputs of run.sh
cd "$(dirname "$0")"
mkdir -p out data
for n in t63 tube60 h63 t48; do python3 analyse.py $n > /dev/null; done
( head -1 data/returnmap_t63.csv; for n in t63 tube60 h63 t48; do tail -n +2 data/returnmap_$n.csv; done ) > data/returnmap.csv
( head -1 data/autocorr_t63.csv; for n in t63 tube60 h63 t48; do tail -n +2 data/autocorr_$n.csv; done ) > data/autocorr.csv
rm -f data/returnmap_*.csv data/autocorr_*.csv
python3 island.py 120 > /dev/null
