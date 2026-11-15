#!/usr/bin/env bash
# Build the site and run every check on it.   bash site/check.sh [--no-app] [--quick]
#   --no-app   do not rebuild the web app; copy web/dist as it is (it must exist)
#   --quick    skip check-signals.js (about 35 s on one core; needs python3 + numpy)
# Needs python3 (standard library), node, and for the smoke test the pre-installed Playwright with its Chromium.
set -euo pipefail
cd "$(dirname "$0")/.."
build_args=(); quick=0
for a in "$@"; do
  case "$a" in
    --no-app) build_args+=(--no-app) ;;
    --quick) quick=1 ;;
    *) echo "unknown option $a" >&2; exit 2 ;;
  esac
done
step() { echo; echo "== $*"; }
step build;            python3 site/build.py "${build_args[@]}"
step stepper;          node site/checks/check-core.js
if [ "$quick" = 0 ]; then
  step signals;        node site/checks/check-signals.js | tail -n 1
fi
step parity;           python3 site/checks/check-parity.py
step links;            python3 site/checks/check-links.py
step smoke;            node site/checks/smoke.js
echo; echo "site/check.sh: all checks passed"
