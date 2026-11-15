#!/bin/bash
# bash research/wrap/validate_all.sh > research/wrap/data/validate.log 2>&1
cd "$(dirname "$0")/../.."
for L in "2 2 6" "1 3 13" "1 3 14" "1 3 15" "1 3 17" "1 4 18" "1 3 18" "1 3 19" "1 3 21" "1 8 21" "1 5 22" "1 3 22" \
         "1 4 22" "1 3 23" "1 4 23" "1 4 25" "1 8 20" "2 2 10"; do
  python3 research/wrap/validate.py $L 1500 || echo "VALIDATE FAIL $L"
done
python3 research/wrap/validate.py 1 3 17 300 --neg || echo "NEGATIVE CONTROL DID NOT FAIL"
echo VALIDATION DONE
