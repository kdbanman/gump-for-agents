#!/bin/sh
# the fall's measured law: fd2 with its box on the peak of the route (2 minutes)
cd "$(dirname "$0")"
S=../../scratch/blast/ref-anatomy
nice -n 10 ./fd2 $S/geom_t48.txt map 2026111821 25  35 32 $S/map_t48peak.txt
nice -n 10 ./fd2 $S/geom_t63.txt map 2026111822 100 46 42 $S/map_t63peak.txt
