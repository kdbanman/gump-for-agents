#!/bin/bash
# the rule on w layers over coins (one core)
cd "$(dirname "$0")"
for w in 1 2 3 4 5 6; do python3 run.py run mod_b16_w$w model 16 $w 60 256 4; done
for w in 1 2 3 4 5 6; do python3 run.py run mod_b24_w$w model 24 $w 150 256 4; done
python3 run.py run mod_b20_w5 model 20 5 90 256 4
python3 run.py run mod_b20_w5_r30 model 20 5 90 256 4 19661
python3 run.py run mod_b20_w5_r55 model 20 5 90 256 4 36045
