#!/bin/sh
# Tallies of the one-step map; one core, about 12 minutes in all. Output: research/scratch/blast/ref-map/*.tal
S=../../scratch/blast/ref-map
mkdir -p $S
gcc -O3 -march=native -o $S/gs gs.c
python3 build_vessel.py hull 9 $S/h9.graph; python3 build_vessel.py hull 11 $S/h11.graph
python3 build_vessel.py hull 13 $S/h13.graph; python3 build_vessel.py slab 4 21 $S/t63.graph
nice -n 10 $S/gs $S/h9.graph  2026111901  7000000 300 $S/h9.tal
nice -n 10 $S/gs $S/h11.graph 2026111902 16000000 300 $S/h11.tal
nice -n 10 $S/gs $S/h13.graph 2026111903  6000000 300 $S/h13.tal
nice -n 10 $S/gs $S/t63.graph 2026111904 12000000 300 $S/t63.tal 33 25
date -u > $S/run.done
# added 04:59 UTC: a fourth hull size (30 cells) and a second, longer run at 84 cells (merged with the first: h13.tal+h13b.tal)
nice -n 10 $S/gs $S/h7.graph 2026111905 4000000 300 $S/h7.tal
nice -n 10 $S/gs $S/h13.graph 2026111906 12000000 300 $S/h13b.tal
# added 05:10 UTC: the last 24 generations of every dying face (GS_DUMP), for dying.py; fresh seeds, short runs
GS_DUMP=$S/h9.dying  nice -n 10 $S/gs $S/h9.graph  2026111911   600000 300 $S/h9_d.tal
GS_DUMP=$S/t63.dying nice -n 10 $S/gs $S/t63.graph 2026111912  7000000 300 $S/t63_d.tal 33 25
GS_DUMP=$S/h11.dying nice -n 10 $S/gs $S/h11.graph 2026111913  4000000 300 $S/h11_d.tal
GS_DUMP=$S/h7.dying  nice -n 10 $S/gs $S/h7.graph  2026111914   300000 300 $S/h7_d.tal
GS_DUMP=$S/h13.dying nice -n 10 $S/gs $S/h13.graph 2026111915 12000000 300 $S/h13_d.tal
