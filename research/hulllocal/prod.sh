#!/bin/sh
# Production runs of research/hulllocal (3 cores). Output: research/scratch/hulllocal/*.npz
P="python3 research/hulllocal/hl.py run"
$P hull15 32 32 1000 4000 1
$P hull13 32 32 1000 4000 2
$P slab_6_0_6_8 32 32 1000 4000 3
$P slab_2_4_14_8 32 32 1000 4000 4
$P slab_1_18_49_8 32 32 1000 4000 5
$P hull15 16 32 4000 4000 6          # burn-in control
for m in 12 16 24; do
  $P slab_6_0_6_$m 32 32 1000 4000 1$m
  $P slab_2_4_14_$m 32 32 1000 4000 2$m
done
$P hull11 32 32 1000 4000 7
$P hull17 32 32 1000 4000 8
