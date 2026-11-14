#!/bin/bash
# Every run behind README.md, as it was made (one core each; SECONDS is wall-clock on a loaded machine, about
# 4-8 million ring-generations per second for 8 lanes). Resumable: a call adds chunks to research/scratch/thin/TAG.
# Not meant to be run as a whole (about four core-hours); run the lines you want to check.
#   python3 run.py run TAG det|model b m_or_w SECONDS T0 GS [coin density/65536] [wall sites] [twist k]
cd "$(dirname "$0")"
R="python3 run.py run"

# deterministic rings, 8 layers
$R det_b16 det 16 8 60 256 4;  $R det_b20 det 20 8 60 256 4;  $R det_b24 det 24 8 120 256 4
$R det_b28 det 28 8 180 256 4; $R det_b32 det 32 8 400 256 4; $R det_b36 det 36 8 800 256 4
# the rule on w layers over coins: rings
for w in 1 2 3 4 5 6; do $R mod_b16_w$w model 16 $w 60 256 4; done
for w in 1 2 3 4 5 6; do $R mod_b24_w$w model 24 $w 150 256 4; done
$R mod_b20_w5 model 20 5 90 256 4; $R mod_b20_w5_r30 model 20 5 90 256 4 19661; $R mod_b20_w5_r55 model 20 5 90 256 4 36045
# deterministic segments (wall of 3 sites): n = b - 3
$R seg_det_n13 det 16 8 60 256 4 26112 3;  $R seg_det_n17 det 20 8 90 256 4 26112 3
$R seg_det_n21 det 24 8 150 256 4 26112 3; $R seg_det_n25 det 28 8 240 256 4 26112 3
$R seg_det_n29 det 32 8 500 256 4 26112 3; $R seg_det_n33 det 36 8 900 256 4 26112 3
$R seg_det_n37 det 40 8 1500 256 4 26112 3; $R seg_det_n45 det 48 8 1800 256 4 26112 3
for n in 5 6 7 8 9 10 11 12; do $R seg_det_n$n det $((n+3)) 8 30 64 4 26112 3; done
for n in 14 15 16 18 19 20; do $R seg_det_n$n det $((n+3)) 8 50 256 4 26112 3; done
for n in 22 23 24; do $R seg_det_n$n det $((n+3)) 8 100 256 4 26112 3; done
# one layer over coins on segments (to compare with sweep.py and to see where its law straightens)
for n in 5 6 7 8 10 12; do $R seg_m1_n$n model $((n+3)) 1 40 64 4 26112 3; done
for n in 16 20 24; do $R seg_m1_n$n model $((n+3)) 1 120 256 4 26112 3; done
# depth ladders on segments
for w in 1 2 3 4 5; do $R seg_m${w}_n13 model 16 $w 60 256 4 26112 3; done
for w in 1 2 3 4 5; do $R seg_m${w}_n21 model 24 $w 150 256 4 26112 3; done
$R seg_m6_n13 model 16 6 60 256 4 26112 3; $R seg_m8_n13 model 16 8 60 256 4 26112 3
# twelve layers instead of eight
$R det12_b16 det 16 12 60 256 4; $R seg_det12_n13 det 16 12 60 256 4 26112 3; $R seg_det12_n21 det 24 12 150 256 4 26112 3
# windows on a long ring; the front's distance from a wall in a long segment (face sampled every 2 generations)
$R win_det_b64 det 64 8 1200 256 2
$R seg_det_n61 det 64 8 1500 256 2 26112 3
# the next torus, (1,2),(0,b), shortest loop squared 7
$R det_k2_b16 det 16 8 60 256 4 26112 0 2;  $R det_k2_b20 det 20 8 120 256 4 26112 0 2
$R det_k2_b24 det 24 8 400 256 4 26112 0 2; $R det_k2_b28 det 28 8 2400 256 4 26112 0 2
# exact: one layer over coins
python3 exact1.py 5; python3 sweep.py ring 5; for n in 2 3 4 5 6 7; do python3 sweep.py seg $n; done
