#!/bin/sh
cd "$(dirname "$0")"
while pgrep -f run2d.sh > /dev/null || pgrep -f run3d.sh > /dev/null || pgrep -f runfollow.sh > /dev/null; do sleep 5; done
python3 follow.py vn
