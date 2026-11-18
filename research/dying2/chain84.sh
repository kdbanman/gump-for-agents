#!/bin/bash
# the two 84-cell faces, one thread, one after the other (research/dying2/README.md)
P=/c/Users/kdbanman/.venvs/gump-gpu/Scripts/python.exe
cd /c/Users/kdbanman/dev/gump-for-agents
$P -u research/dying2/dy.py run 1 12 28 2.0 84001 43.30 6 threads=1 nullsh=15 H=4096 R=512 maxdeath=2500 maxrec=30000 chunk=10
$P -u research/dying2/dy.py run 2 4 14 2.5 84101 43.48 6 threads=1 nullsh=15 H=4096 R=512 maxdeath=2500 maxrec=30000 chunk=10
