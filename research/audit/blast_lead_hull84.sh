#!/bin/sh
# Lead's run, 2026-11-18: death records on the 84-cell hull face (radius 13) with the audit's stepper (research/audit/blast/fd.c),
# to count the share of deaths that hold a one-generation fall of half the face.  Forecast frozen in the notebook entry
# of 2026-11-18 ("how a face dies, audited from outside") before the run.  Two cores, about 30 minutes.
cd "$(dirname "$0")/../.."
D=research/audit/blast; S=research/scratch/audit_blast
set -e
mkdir -p $S
python3 $D/geom.py hull 13 >/dev/null
[ -x $S/fd ] || gcc -O3 -march=native -o $S/fd $D/fd.c
for s in 93 94; do ( $S/fd $S/hull_13.bin run $s 45000000 $S/leadhull84_s$s 59 6000 4096 1009 1000 43 > $S/leadhull84_s$s.log 2>&1 ) & done
wait
python3 $D/analyse.py hull_13 leadhull84_s93 leadhull84_s94 --out $S/lead_hull84.txt > /dev/null
grep -n -E 'ln tau_face|>= 0.[345] A:|generations from the launch|population at the launch: mean|falls of >= 0.5 A' $S/lead_hull84.txt
