#!/bin/sh
# The main batch (about 2.5 hours on 3 cores). Output: research/scratch/lineage/plateaus_*.csv
cd "$(dirname "$0")/../.."
P="python3 research/lineage/run_lineages.py"
$P struct 13 800 3
$P soup 33 800 3
$P struct 12 600 3
$P soup 32 600 3
$P struct 14 300 3
$P soup 36 300 3
