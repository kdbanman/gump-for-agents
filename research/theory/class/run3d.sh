#!/bin/sh
# 3D test set: caps b+1 .. K_f+2 of every family (torus 10^3 periods, then {sealed-plane} slabs 8 layers deep)
cd "$(dirname "$0")"
while pgrep -f run2d.sh > /dev/null; do sleep 5; done
python3 scan.py fcc      --areas 25,49,81 --sec 10 --cmax 11
python3 scan.py bcc8     --areas 25,49,81 --sec 10 --cmax 8
python3 scan.py sc6      --areas 25,49,81 --sec 10 --cmax 7
python3 scan.py cross3d2 --areas 25,49,81 --sec 10 --cmax 12
python3 scan.py bond10   --areas 27,48,75 --sec 10 --cmax 9
python3 scan.py face8    --areas 27,48,75 --sec 10 --cmax 8
python3 scan.py bcc14    --areas 25,49,81 --sec 10 --cmax 12
python3 scan.py sc18     --areas 25,49,81 --sec 10 --cmax 15
python3 scan.py face18   --areas 27,48,75 --sec 10 --cmax 15
python3 scan.py sc26     --areas 25,49,81 --sec 10 --cmax 19
