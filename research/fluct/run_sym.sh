#!/bin/sh
# resumable symmetric campaign (one core); each line tops up to its wall-time target
cd "$(dirname "$0")/../.." || exit 1
Q="python3 research/fluct/qsd.py"
$Q sym 37 c 600 1
$Q snap research/data/cube16_gen1025000000.gump v 3600 1 lite
$Q sym 39 c 1200 1 lite
$Q sym 33 c 400 1
$Q sym 35 c 500 1
$Q sym 42 v 1800 1 lite
$Q sym 36 v 900 1 lite
$Q sym 30 v 400 1
