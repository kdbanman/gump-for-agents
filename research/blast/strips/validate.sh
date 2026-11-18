#!/bin/sh
# sh validate.sh > validate_log.txt   (about a minute)
S=${S:-/home/user/gump-for-agents/research/scratch/blast/strips}; D=$(dirname "$0")
for v in "oct 9 0" "prism 7 5" "prism 9 3" "prism 11 4" "prism 5 6" "slab 4 3" "slab 5 4" "tet 5 0" "tet 6 0" "tet 7 0"; do
  n=$(echo $v | tr ' ' '_')
  $S/strips val $v 31 1000 0 $S/val_$n.txt && python3 $D/validate.py $S/val_$n.txt
  $S/strips val $v 31 1000 1 $S/neg_$n.txt && python3 $D/validate.py $S/neg_$n.txt expect-fail
  rm -f $S/val_$n.txt $S/neg_$n.txt
done
