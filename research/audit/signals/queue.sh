#!/bin/bash
# The review's remaining runs, one after another on one core.  Outputs in research/scratch/audit_signals/.
cd "$(dirname "$0")"; O=../../scratch/audit_signals
ulimit -v 6000000
nice -n 10 python3 sat_probe.py > $O/sat_probe.txt 2>&1
nice -n 10 python3 flips_B.py > $O/flipsB.txt 2>&1
nice -n 10 python3 l2_gap.py > $O/l2_gap.txt 2>&1
nice -n 10 python3 fronts_check.py W00 W05 W18 --oracle > $O/fronts.txt 2>&1
nice -n 10 timeout 1800 python3 transfer.py 3 3 2 1 --wire pulse-B > $O/transfer_33_B.txt 2>&1
nice -n 10 timeout 1800 python3 transfer.py 3 3 2 1 --wire pulse-S > $O/transfer_33_S.txt 2>&1
nice -n 10 timeout 1800 python3 transfer.py 3 3 2 1 --still > $O/transfer_33_still.txt 2>&1
TUBES="23" LIMIT=900 ./run_transfer.sh
echo QUEUE DONE >> $O/fronts.txt
