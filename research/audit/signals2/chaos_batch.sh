#!/bin/bash
# runs of chaos_check.py for the review (about 15 min on one core)
cd "$(dirname "$0")"
for args in "C all 0.4 12 100 2000" "B all 0.4 12 100 3000" "C outside 0.4 12 50 4000" "B outside 0.4 12 50 5000" \
            "C all 0.2 12 50 6000" "C all 0.6 12 50 7000" "C all 0.1 12 50 7500" "C all 0.4 4 50 8000" "C all 0.4 24 50 9000" \
            "C all 0.4 1 50 9500" "B all 0.2 12 50 10000" "B all 0.1 12 50 10500" "B all 0.4 4 50 11000" "B all 0.4 1 50 11500"; do
  python3 chaos_check.py $args
done
