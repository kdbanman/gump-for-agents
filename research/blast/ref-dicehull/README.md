# research/blast/ref-dicehull: referee of "Dice under the hull" (split-hull), 2026-11-18

The account is `REVIEW.md`. Reproduce (one core, about 20 minutes; bulk output in `research/scratch/blast/ref-dicehull/`):

    S=research/scratch/blast/ref-dicehull; H=research/blast/ref-dicehull; mkdir -p $S
    python3 $H/validate.py 1200                                  # rd.c against reference/oracle.py; builds $S/rd
    for R in 9 11 15 17; do for WD in 6 8 99; do python3 $H/geom.py $R $WD $S/g_${R}_$WD.bin; done; done
    $S/rd $S/g_11_6.bin run 12 20000000 200 32  > $S/bf_R11_WD6_d32_b200.txt   # chain; last argument 27 = coins 0.42; g_11_8 = 8 rule layers
    $S/rd $S/g_11_99.bin run8 32 2000000 200 32 > $S/gump_R11_b200.txt         # gump, anchors' protocol
    $S/rd $S/g_17_99.bin run 13 2000000 500 32  > $S/tail_R17_gump.txt         # living state; g_17_6 -> tail_R17_WD6.txt
    $S/rd $S/g_11_6.bin win 51 5000000 200 32 31.27 5.24 > $S/dur_R11_WD6.txt  # fatal-dip durations
    gcc -O3 -march=native -o $S/hd_anc $H/hd_anc.c -lm; python3 research/blast/split-hull/hullgeom.py 17 $S/hg_17.bin
    WD=6 NR=924 $S/hd_anc $S/hg_17.bin sub 880017 12 51 3 8 22 5 32 24 - 12 > $S/anc_R17_s880017.txt   # sampler + ancestry
    python3 $H/ana.py; python3 $H/pool.py; python3 $H/paths.py

File names and seeds of every run are in the scratch queue scripts as used: seeds 11 to 22 (`run`), 31, 32 (`run8`),
51 (`win`), 770017, 880017, 990017 (R = 17 sampler), 880013 (R = 13 sampler). `pool.py` also reads split-hull's
scratch files, which were still growing when the review was written (its tables are as of 05:46 UTC).
