#!/bin/sh
cd "$(dirname "$0")"
while pgrep -f runfollow.sh > /dev/null || pgrep -f runfollow2.sh > /dev/null || pgrep -f runfollow3.sh > /dev/null; do sleep 5; done
python3 follow.py hulls3d cross3:4:7:6,8,10,12:0.45 cross3:4:8:5,6,7,8,9:0.5 cross4:5:9:8,10,12:0.44 cross4:5:10:6,8,10:0.48 fcc:4:8:3,4,5:0.52 fcc:4:9:3,4,5:0.57 cross3d2:3:6:3,4,5:0.45 bcc14:5:8:3,4,5:0.45 sc18:6:10:3,4,5,6:0.44
