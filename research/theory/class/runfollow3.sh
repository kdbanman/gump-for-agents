#!/bin/sh
cd "$(dirname "$0")"
while pgrep -f run3d.sh > /dev/null || pgrep -f runfollow.sh > /dev/null || pgrep -f runfollow2.sh > /dev/null; do sleep 5; done
python3 follow.py hulls3d fcc:4:6:3,4,5,6,7:0.42 fcc:4:7:3,4,5,6:0.48 bcc8:3:5:3,4,5,6:0.5 bcc8:3:6:3,4,5:0.57 sc6:2:3:2,3,4,5:0.4 sc6:2:4:2,3,4,5:0.52 sc6:2:5:2,3,4:0.63 cross3d2:3:5:3,4,5,6:0.4 bond10:4:6:4,5,6,7:0.45 bond10:4:7:4,5,6:0.55
python3 follow.py more3d
