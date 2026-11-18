#!/bin/sh
S=/home/user/gump-for-agents/research/scratch/blast/strips
r() { # vessel p1 p2 seed T0 maxd maxs
  nice -n 10 $S/strips2 life $1 $2 $3 $4 $5 $6 $7 1 > $S/runs/${1}_${2}_${3}_s$4.txt 2> $S/runs/${1}_${2}_${3}_s$4.err
}
r prism 7 7 707 1000 2600 1800
r prism 7 6 706 1000 12000 480
r prism 7 3 703 200 300000 30
r prism 7 5 705 1000 40000 120
r prism 9 3 903 400 100000 40
r prism 9 4 904 1000 30000 80
r prism 9 5 905 1000 5000 400
r prism 11 3 1103 1000 60000 60
r prism 11 4 1104 1000 6000 200
r slab 4 4 44 1000 60000 40
r slab 5 4 54 1000 30000 60
r slab 6 4 64 1000 6000 120
r slab 5 5 55 1000 5000 180
r slab 4 3 43 300 200000 30
r slab 5 3 53 500 100000 30
r slab 6 3 63 1000 60000 40
r slab 7 3 73 1000 40000 60
r slab 8 3 83 1000 20000 90
r tet 3 0 3 50 400000 15
r tet 4 0 4 50 400000 15
r tet 5 0 5 100 300000 20
r tet 6 0 6 150 300000 30
r tet 7 0 7 200 200000 40
r tet 8 0 8 300 100000 60
r tet 9 0 9 400 50000 90
echo done > $S/runs/queueB.done
