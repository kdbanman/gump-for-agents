#!/bin/sh
# The runs of research/audit/REVIEW-blast-noisy.md, in the order of the review.  One core each unless said; times are
# for one core of this machine (Xeon 2.1 GHz, AVX-512) with two other processes running.
#   sh research/audit/blastnoisy/run.sh check | brute | sampler | tables
# PR = the pull request's research/blast/noisy (default: the read-only worktree the review used).
cd "$(dirname "$0")/../../.." || exit 1
A=research/audit/blastnoisy; S=research/scratch/audit_noisy; PR=${PR:-research/scratch/blast-wt/research/blast/noisy}
mkdir -p $S/brute $S/young $S/runs
nb() { R=$1; shift; $S/nb $S/hull_$R.bin run "$@"; }
case "$1" in
check)   # 3 minutes: builds the hull files and nb; nb = oracle with the noise off; darts = slow reference; dart law
  python3 $A/validate.py ;;
brute)   # nb R SEED GENS M MODE [BURN REPORT MAXAGE]; the last RES line of each file is the result
  for M in 0 4 16 64; do nb 9 $((900 + M)) 2500000 $M F > $S/brute/b9_M${M}_F_s$((900 + M)).txt; done    # 15 to 60 s each
  nb 9 964 1500000 64 L > $S/brute/b9_M64_L_s964.txt                    # 3 minutes (the literal darts)
  nb 9 904 2500000 4 L > $S/brute/b9_M4_L_s904.txt                      # 40 s
  nb 11 1100 20000000 0 F > $S/brute/b11_M0_F_s1100.txt                 # 3 minutes
  nb 11 1116 20000000 16 F > $S/brute/b11_M16_F_s1116.txt               # 5 minutes
  nb 11 1117 20000000 16 F > $S/brute/b11_M16_F_s1117.txt               # 5 minutes
  nb 11 1164 20000000 64 F > $S/brute/b11_M64_F_s1164.txt               # 10 minutes
  nb 11 1356 10000000 256 F > $S/brute/b11_M256_F_s1356.txt             # 13 minutes
  nb 11 1190 20000000 0 F 200 2000000 6000 > $S/young/y11_M0_s1190.txt  # 4 minutes: hulls replaced at age 6,000
  nb 11 21 22000000 0 F 999 2000000 0 0.4 > $S/fdcheck_hull63_s21.txt    # 3 minutes: fd.c's run of seed 21, count for count
  nb 13 1300 45000000 0 F > $S/brute/b13_M0_s1300.txt                   # 10 minutes: the control at 84 cells
  nb 13 1304 45000000 0 F > $S/brute/b13_M0_s1304.txt                   # 10 minutes
  nb 13 1301 110000000 256 F > $S/brute/b13_M256_s1301.txt              # 106 minutes: 84 cells, eps 1/4
  nb 13 1390 64000000 0 F 200 4000000 6000 > $S/young/y13_M0_s1390.txt  # 17 minutes: 84 cells, hulls replaced at age 6,000
  ;;
sampler) # the pull request's sampler: nz_author = its nz.c unmodified; nz_anc = the same with the ancestry columns
  gcc -O3 -march=native -o $S/nz_author $PR/nz.c -lm
  python3 $A/patch_anc.py $PR/nz.c $S/nz_anc.c && gcc -O3 -march=native -o $S/nz_anc $S/nz_anc.c -lm
  $S/nz_author 11 sub 71000 2 18 3 8 38 15 32 24 12 16 > $S/t_first.txt
  $S/nz_anc 11 sub 71000 2 18 3 8 38 15 32 24 12 16 | sed 's/ anc_ens.*//' | diff - $S/t_first.txt && echo "nz_anc = nz, number for number"
  # sub.sh BIN R M SEED0 NRUNS LAM1 DELTA NSWEEP TAG [NREP]
  sh $A/sub.sh nz_author 11 16 71100 25 18 3 38 a11_M16_D3_S38          # 12 minutes: frozen, 63 cells, eps 1/16
  sh $A/sub.sh nz_author 11 64 71400 25 18 3 38 a11_M64_D3_S38          # 22 minutes: frozen, 63 cells, eps 1/4
  sh $A/sub.sh nz_anc 9 4 79100 20 10 3 27 c9_M4_D3_S27                 # 3 minutes: 45 cells, eps 1/16
  sh $A/sub.sh nz_anc 9 16 79200 20 10 3 27 c9_M16_D3_S27               # 3 minutes: 45 cells, eps 1/4
  sh $A/sub.sh nz_anc 11 16 72100 15 18 6 38 c11_M16_D6_S38             # 4 minutes: DELTA 6
  sh $A/sub.sh nz_anc 11 16 72200 15 18 3 19 c11_M16_D3_S19             # 4 minutes: NSWEEP halved
  sh $A/sub.sh nz_anc 11 16 72300 4 18 1 38 c11_M16_D1_S38              # 6 minutes: DELTA 1
  sh $A/sub.sh nz_anc 11 16 72310 6 18 1 38 c11_M16_D1_S38              # 9 minutes
  sh $A/sub.sh nz_anc 11 16 72400 5 18 3 76 c11_M16_D3_S76              # 5 minutes: NSWEEP doubled
  sh $A/sub.sh nz_anc 11 16 72500 2 18 3 38 c11_M16_D3_S38              # 1 minute: frozen, with ancestry
  sh $A/sub.sh nz_anc 15 128 81500 1 38 3 65 c15_M128_D3_S65 6          # 2 minutes: ancestry at 108 cells, eps 1/16
  sh $A/sub.sh nz_anc 15 32 81600 1 38 3 65 c15_M32_D3_S65 6            # 2 minutes: ancestry at 108 cells, eps 1/64
  sh $A/sub.sh nz_anc 13 64 81300 1 28 3 50 c13_M64_D3_S50 10           # 2 minutes: ancestry at 84 cells, eps 1/16
  sh $A/sub.sh nz_anc 13 256 83400 8 28 3 50 c13_M256_D3_S50 5          # 23 minutes: 84 cells, eps 1/4, against the brute force
  sh $A/sub.sh nz_anc 15 512 85400 9 38 3 65 c15_M512_D3_S65 2          # 38 minutes: 108 cells, eps 1/4
  sh $A/sub.sh nz_anc 15 512 85600 1 38 3 65 c15_M512_D3_S65 2          # 4 minutes
  ;;
tables)
  python3 $A/brute.py
  python3 $A/summary.py
  python3 $A/ages.py $S/young/y11_M0_s1190.txt
  python3 $A/ages.py $S/young/y13_M0_s1390.txt
  python3 $A/ages.py $S/brute/b11_M0_F_s1100.txt
  python3 $A/rows.py "$S/runs/c9_*.txt"
  python3 $A/rows.py "$S/runs/a11_*.txt" "$S/runs/c11_*.txt"
  python3 $A/rows.py "$S/runs/c13_*.txt" "$S/runs/c15_*.txt"
  python3 $A/rows.py "$PR/data/runs/sub_R1[13]_*.txt"                   # the pull request's own 63- and 84-cell rows (head b80248c: PR=research/scratch/blast-wt2/research/blast/noisy)
  python3 $A/c108.py $PR/data/runs
  python3 $A/tail108.py $PR/data/runs $A/data/runs
  ;;
*) echo "usage: sh research/audit/blastnoisy/run.sh check | brute | sampler | tables" ;;
esac
