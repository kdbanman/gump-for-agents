#!/bin/sh
# lead's re-run of the blast audit: oracle anchor on two vessels, fresh seeds, the audit's own analysis
cd "$(dirname "$0")/../.."
D=research/audit/blast; S=research/scratch/audit_blast
set -e
python3 $D/geom.py slab 1 4 21 >/dev/null; python3 $D/geom.py hull 11 >/dev/null
python3 $D/geom.py check slab 1 4 21 1200 | tail -3
python3 $D/geom.py check hull 11 1200 | tail -3
[ -x $S/fd ] || gcc -O3 -march=native -o $S/fd $D/fd.c
( $S/fd $S/slab_1_4_21.bin run 91 6000000 $S/lead63_s91 45 2000 4096 1009 1000 32 > $S/lead63_s91.log 2>&1 ) &
( $S/fd $S/hull_11.bin run 92 6000000 $S/leadhull_s92 45 2000 4096 1009 1000 32 > $S/leadhull_s92.log 2>&1 ) &
wait
python3 $D/analyse.py slab_1_4_21 lead63_s91 --out $S/lead_slab63.txt > /dev/null 2>&1 || echo ANALYSE-SLAB-FAILED
python3 $D/analyse.py hull_11 leadhull_s92 --out $S/lead_hull63.txt > /dev/null 2>&1 || echo ANALYSE-HULL-FAILED
wc -l $S/lead_slab63.txt $S/lead_hull63.txt
echo DONE
