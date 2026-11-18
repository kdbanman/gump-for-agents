#!/bin/bash
# Referee's tables: every number of REVIEW.md that comes from sampler replications or dying paths.
#   bash final.sh > data/final.txt
cd "$(dirname "$0")"
R=../../scratch/blast/ref-slab/out; D=../split-slab/data; F=../../scratch/blast/split-slab/subpaths_full
mkdir -p data; cp $R/sub_*.txt $R/brute_*.txt $R/diag2_*.txt data/ 2>/dev/null
echo "== brute force, own stepper (dice.c) =="; cat data/brute_*.txt | grep -v "^$"
echo; echo "== sampler replications pooled (pool.py) =="
python3 pool.py "48 cells, fresh seeds (ref-slab)" data/sub_48_s7*.txt
ls data/sub_48_direct.txt >/dev/null 2>&1 && python3 pool.py "48 cells, direct count through the sampler's own pipeline (LAM1 = 0: no levels, no sweeps)" data/sub_48_direct.txt
python3 pool.py "63 cells, split-slab's" $D/sub_1_4_21_s2.txt $D/sub_1_4_21_s4.txt
python3 pool.py "63 cells, fresh seeds" data/sub_63_s*.txt
python3 pool.py "63 cells, all" $D/sub_1_4_21_s2.txt $D/sub_1_4_21_s4.txt data/sub_63_s*.txt
python3 pool.py "84 tube, split-slab's" $D/sub_1_12_28_s2.txt $D/sub_1_12_28_s4.txt
python3 pool.py "120 tube, split-slab's (s2, s3)" $D/sub_1_18_40_s2.txt $D/sub_1_18_40_s3.txt
python3 pool.py "120 tube, fresh seeds" data/sub_120_s*.txt
python3 pool.py "120 tube, all" $D/sub_1_18_40_s2.txt $D/sub_1_18_40_s3.txt data/sub_120_s*.txt
ls data/sub_120big_s*.txt >/dev/null 2>&1 && python3 pool.py "120 tube, fourfold ensemble (NBATCH 32 = 16,384 chains), fresh seed" data/sub_120big_s*.txt
python3 pool.py "192 wide, split-slab's (s2, s3)" $D/sub_8_0_8_s2.txt $D/sub_8_0_8_s3.txt
ls $D/sub_8_0_8_s5.txt >/dev/null 2>&1 && python3 pool.py "192 wide, split-slab's later file s5 (not in the README under review)" $D/sub_8_0_8_s5.txt
python3 pool.py "192 wide, fresh seeds" data/sub_192w_s*.txt
python3 pool.py "192 wide, all (s2, s3, s5 if present, fresh)" $D/sub_8_0_8_s*.txt data/sub_192w_s*.txt
python3 pool.py "192 tube, split-slab's (s2, s3)" $D/sub_1_30_64_s2.txt $D/sub_1_30_64_s3.txt
ls data/sub_192t_s*.txt >/dev/null 2>&1 && python3 pool.py "192 tube, fresh seeds" data/sub_192t_s*.txt
ls data/sub_192t_s*.txt >/dev/null 2>&1 && python3 pool.py "192 tube, all (s2, s3, fresh)" $D/sub_1_30_64_s2.txt $D/sub_1_30_64_s3.txt data/sub_192t_s*.txt
python3 pool.py "144 tube, split-slab's" $D/sub_1_22_48_s2.txt
python3 pool.py "108 wide, split-slab's" $D/sub_6_0_6_s2.txt
python3 pool.py "108 tube, split-slab's" $D/sub_1_16_36_s2.txt $D/sub_1_16_36_s3.txt
python3 pool.py "96 tube, split-slab's" $D/sub_1_17_32_s2.txt $D/sub_1_17_32_s3.txt
echo; echo "== shares: natural deaths by brute force (shares.py brute) =="
for x in "48 bpaths_dice_48" "48 bpaths_gump_48" "63 bpaths_dice_63" "63 bpaths_gump_63" "60 bpaths_dice_60t" "60 bpaths_gump_60t" "84 bpaths_dice_84t"; do set -- $x; [ -e $R/$2.txt ] && python3 shares.py $1 brute $R/$2.txt; done
echo; echo "== shares: sampler paths (shares.py sub) =="
sub() { A=$1; shift; lab=$1; shift; echo -n "$lab: "; python3 shares.py $A sub "$@"; }
sub 48 "48 fresh" $R/paths_48_s7101.txt:$R/sub_48_s7101.txt
sub 63 "63 split-slab" $F/subpaths_1_4_21_s4.txt:$D/sub_1_4_21_s4.txt
a=""; for f in $R/paths_63_s*.txt; do s=${f/paths_/sub_}; a="$a $f:$s"; done; sub 63 "63 fresh" $a
sub 84 "84 tube split-slab" $F/subpaths_1_12_28_s4.txt:$D/sub_1_12_28_s4.txt
sub 108 "108 tube split-slab" $F/subpaths_1_16_36_s2.txt:$D/sub_1_16_36_s2.txt
sub 108 "108 wide split-slab" $F/subpaths_6_0_6_s2.txt:$D/sub_6_0_6_s2.txt
sub 120 "120 tube split-slab" $F/subpaths_1_18_40_s2.txt:$D/sub_1_18_40_s2.txt
a=""; for f in $R/paths_120_s*.txt; do s=${f/paths_/sub_}; a="$a $f:$s"; done; sub 120 "120 tube fresh" $a
sub 120 "120 tube all" $F/subpaths_1_18_40_s2.txt:$D/sub_1_18_40_s2.txt $a
[ -e $R/paths_120big_s7260.txt ] && sub 120 "120 tube fourfold ensemble" $R/paths_120big_s7260.txt:$R/sub_120big_s7260.txt
sub 144 "144 tube split-slab" $F/subpaths_1_22_48_s2.txt:$D/sub_1_22_48_s2.txt
sub 192 "192 tube split-slab" $F/subpaths_1_30_64_s2.txt:$D/sub_1_30_64_s2.txt $F/subpaths_1_30_64_s3.txt:$D/sub_1_30_64_s3.txt
a=""; for f in $R/paths_192t_s*.txt; do [ -e $f ] || continue; s=${f/paths_/sub_}; a="$a $f:$s"; done; [ -n "$a" ] && sub 192 "192 tube fresh" $a
[ -n "$a" ] && sub 192 "192 tube all" $F/subpaths_1_30_64_s2.txt:$D/sub_1_30_64_s2.txt $F/subpaths_1_30_64_s3.txt:$D/sub_1_30_64_s3.txt $a
sub 192 "192 wide split-slab" $F/subpaths_8_0_8_s2.txt:$D/sub_8_0_8_s2.txt $F/subpaths_8_0_8_s3.txt:$D/sub_8_0_8_s3.txt
a=""; for f in $R/paths_192w_s*.txt; do s=${f/paths_/sub_}; a="$a $f:$s"; done; sub 192 "192 wide fresh" $a
sub 192 "192 wide all" $F/subpaths_8_0_8_s2.txt:$D/sub_8_0_8_s2.txt $F/subpaths_8_0_8_s3.txt:$D/sub_8_0_8_s3.txt $a
