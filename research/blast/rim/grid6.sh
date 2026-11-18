#!/bin/bash
# runs with the death ring (-r): the last 13 generations of every face death, for bust.py; they also add lives
cd "$(dirname "$0")/../../.."
S=research/scratch/blast/rim
while pgrep -f "grid.sh 140 1" > /dev/null; do sleep 1; done
r() { # T1 T2 L par TB seed
  n=$(python3 -c "print(int(1.5*$1*$2*$3))"); gens=$(python3 -c "print(int($5*3.5e7/$n))")
  nice -n 10 python3 research/blast/rim/run.py prism $1 $2 $3 $4 $gens $6 8 -r $S/ring_$1_$2_$3_$4.txt 12000
}
r 8 8 4 0 10 2
r 8 8 5 0 80 2
r 10 10 4 0 50 2
r 12 12 3 0 20 2
r 14 14 3 0 60 1
nice -n 10 python3 research/blast/rim/run.py hull 9 800000 2 8 -r $S/ring_hull_9.txt 12000
r 10 10 5 0 250 2
r 9 9 5 0 90 1
r 8 10 4 0 30 1
