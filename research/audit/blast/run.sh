#!/bin/sh
# Everything behind research/audit/REVIEW-blast.md, from the repository root.  One core each; times on this machine.
# Bulk output: research/scratch/audit_blast (records of single deaths, about 0.4 GB).  Tables: research/audit/blast/data.
set -e
D=research/audit/blast; S=research/scratch/audit_blast
mkdir -p $S
for v in "slab 1 4 21" "hull 11" "slab 1 12 28" "slab 1 4 28"; do python3 $D/geom.py $v; done
# the stepper against reference/oracle.py, state for state, with a negative control (5 to 25 s each)
python3 $D/geom.py check slab 1 4 21 1200
python3 $D/geom.py check hull 11 1200
python3 $D/geom.py check slab 1 12 28 1000
python3 $D/geom.py check slab 1 4 28 1000
gcc -O3 -march=native -o $S/fd $D/fd.c
# fd VESSEL run SEED GENS PREFIX THR MAXD OSUB RSUB BURN U0     (8.5, 5, 5 minutes)
$S/fd $S/slab_1_4_21.bin run 11 45000000 $S/slab63_s11 45 60000 1024 1009 1000 32
$S/fd $S/slab_1_4_21.bin run 12 25000000 $S/slab63_s12 45 20000 1024 1009 1000 32
$S/fd $S/slab_1_4_21.bin run 13 25000000 $S/slab63_s13 45 2000 4096 1009 1000 32
$S/fd $S/hull_11.bin run 21 22000000 $S/hull63_s21 45 60000 1024 1009 1000 32
$S/fd $S/hull_11.bin run 22 12000000 $S/hull63_s22 45 20000 1024 1009 1000 32
$S/fd $S/hull_11.bin run 23 12000000 $S/hull63_s23 45 2000 4096 1009 1000 32
# 84 cells: the loop-12 tube and the wide torus (8.5 minutes each)
for s in 31 32; do $S/fd $S/slab_1_12_28.bin run $s 46000000 $S/tube84_s$s 59 4000 4096 1009 1000 43; done
for s in 41 42; do $S/fd $S/slab_1_4_28.bin run $s 46000000 $S/wide84_s$s 59 4000 4096 1009 1000 43; done
# tables (0.5 to 2 minutes each)
python3 $D/analyse.py slab_1_4_21 slab63_s11 slab63_s12 slab63_s13 --out $D/data/slab63.txt
python3 $D/analyse.py hull_11 hull63_s21 hull63_s22 hull63_s23 --out $D/data/hull63.txt
python3 $D/analyse.py slab_1_12_28 tube84_s31 tube84_s32 --out $D/data/tube84.txt
python3 $D/analyse.py slab_1_4_28 wide84_s41 wide84_s42 --out $D/data/wide84.txt
python3 $D/rimtest.py hull_11 hull63_s21 48 > $D/data/rimtest.txt
python3 $D/rimtest.py slab_1_4_21 slab63_s11 48 >> $D/data/rimtest.txt
python3 $D/dice.py > $D/data/dice.txt
