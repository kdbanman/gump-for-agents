#!/bin/sh
# Symmetric soups for the 2D gump (cross2 B34/S234); forecasts in PREDICTIONS.md (F1-F5).
# Strips W = 16 (periodic in x); boxes L x L. Output: research/scratch/toy2d/law_*.json; analyse with analyze.py.
cd "$(dirname "$0")"
R=B34/S234
# F1: mirror x -> -x (perpendicular to the edges): slope forecast I/2
python3 law.py $R cross2 16 16,24,32,40,48,56 --sym mx --deaths 400 --maxsec 600 --tag sym
# F3: mirror y -> -y (swaps the two edges): first-death wait x2, slope unchanged
python3 law.py $R cross2 16 16,20,24 --sym my --deaths 400 --maxsec 300 --tag sym
# F2: translation by L/2 at L = 32 must reproduce the asymmetric strip at L = 16 exactly
python3 law.py $R cross2 16 32 --sym t2 --deaths 2000 --maxsec 300 --tag sym
# F4/F5: square boxes, no symmetry / D4 / C4 / diagonal mirror
for s in none d4 c4 diag; do
  python3 law.py $R cross2 0 12,16,20,24,28 --vessel box --sym $s --deaths 400 --maxsec 300 --tag sym
done
