#!/usr/bin/env bash
# item 4: face12e B45/S345 (not gump).  O_h-symmetric boxes 4^3 .. 12^3; boxes of 7^3 to 3e7 (2 x 64 soups, ~45 min)
cd "$(dirname "$0")"
O=../../../scratch/class_followup; mkdir -p $O
python3 three_d.py symcheck 6 >> $O/face12e_sym.jsonl
for n in 4 5 6 7 8 9 10 11 12; do python3 three_d.py symbox 6 $n 2000000 1; done >> $O/face12e_sym.jsonl
for s in 11 12; do python3 three_d.py box face12e 6 7 30000000 $s 4096; done >> $O/face12e_box7.jsonl
