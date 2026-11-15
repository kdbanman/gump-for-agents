#!/bin/bash
# The SAT listener instances of README section 26, three at a time; one line of output each (plus any model).
# bash listen_batch.sh > ../scratch/signals/p5/listen_batch.txt
cd "$(dirname "$0")"
{
for C in 29 31 33 35 37 39 41; do echo "$C --S 40"; done
for C in 31 33 35 37; do for w in 0,1 0,2 0,1,2 0,2,4; do echo "$C --S 40 --word $w"; done; done
for C in 31 33 35 37 39; do echo "$C --S 40 --mult 2 --multB 2"; done
for C in 29 31 33 35; do echo "$C --S 40 --lo -1 --hi 7"; done
for C in 29 31 33; do echo "$C --S 40 --lo -1 --hi 7 --mult 2 --multB 2"; done
} | xargs -P 3 -I{} sh -c 'python3 sat_listen.py {} --minutes 25 2>&1 | grep -v "^building"'
