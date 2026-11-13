#!/bin/sh
cd "$(dirname "$0")"
while pgrep -f run2d.sh > /dev/null || pgrep -f run3d.sh > /dev/null; do sleep 5; done
python3 follow.py stage4
python3 follow.py weak
python3 follow.py gump3
python3 follow.py hulls2d
