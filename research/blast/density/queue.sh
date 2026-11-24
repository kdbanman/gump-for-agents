#!/bin/sh
# A worker (one core): takes the first line of the queue file (under a lock), runs it, repeats until the queue is
# empty. Lines: "TAG R SEED GENS M DW BIAS [VAR=VALUE ...]". Several workers may share a queue; lines may be added or
# reordered while they run.
#   sh research/blast/density/queue.sh QUEUEFILE
HERE=$(cd "$(dirname "$0")" && pwd); Q=$1
while :; do
  line=$(flock "$Q.lock" sh -c "head -n 1 '$Q'; sed -i 1d '$Q'")
  [ -z "$line" ] && { [ -s "$Q" ] && continue; exit 0; }
  set -- $line; tag=$1; R=$2; seed=$3; gens=$4; M=$5; dw=$6; bias=$7; shift 7
  case "$tag" in '#'*) continue;; esac
  env "$@" sh $HERE/row.sh $tag $R $seed $gens $M $dw $bias
done
