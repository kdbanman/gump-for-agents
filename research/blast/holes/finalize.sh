#!/bin/sh
# Rebuild the committed tables from the raw counts (data/), then fill README.md's table markers.
#   sh finalize.sh            (uses data/slab12_s101.txt, data/hull29_s201.txt.gz, data/hull29_launch.txt.gz)
cd "$(dirname "$0")"
T=$(mktemp -d)
gunzip -c data/hull29_s201.txt.gz > $T/hull.txt
gunzip -c data/hull29_launch.txt.gz > $T/hull_launch.txt
python3 ana.py torus data/slab12_s101.txt > data/torus_table.txt
python3 ana.py torus data/slab12_launch.txt | sed -n '/how a patch empties/,$p' > data/torus_launch_table.txt
python3 ana.py hull $T/hull.txt --torus data/slab12_s101.txt > data/hull_table.txt
python3 ana.py hull $T/hull_launch.txt | sed -n '/^(F)/,$p' > data/hull_launch_table.txt
rm -rf $T
python3 fill_readme.py
