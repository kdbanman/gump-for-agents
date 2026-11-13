#!/bin/sh
# Second batch: structured side-12 lineages (fresh file) and the perturbation test at side 13.
cd "$(dirname "$0")/../.."
mv research/scratch/lineage/plateaus_struct12.csv research/scratch/lineage/plateaus_struct12_partial.csv.bak 2>/dev/null
python3 research/lineage/run_lineages.py struct 12 600 3
python3 research/lineage/run_lineages.py struct 14 300 3 4e7 84
python3 research/lineage/perturb.py 13 20000 150 4 3
