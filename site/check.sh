#!/usr/bin/env bash
# Build the site and run every check on it.   bash site/check.sh [--no-app] [--quick] [--artifact]
#   --no-app    do not rebuild the web app; copy web/dist as it is (it must exist)
#   --quick     skip check-signals.js (about 35 s on one core; needs python3 + numpy)
#   --artifact  build and check the private artifact copy, site/dist-artifact/, instead of site/dist/: stepper, parity,
#               links, the page contract on every page, and the smoke test over http and file:// with no fetch allowed
# Needs python3 (standard library), node, and for the smoke test the pre-installed Playwright with its Chromium.
set -euo pipefail
cd "$(dirname "$0")/.."
build_args=(); quick=0; art=0
for a in "$@"; do
  case "$a" in
    --no-app) build_args+=(--no-app) ;;
    --quick) quick=1 ;;
    --artifact) art=1; build_args+=(--artifact) ;;
    *) echo "unknown option $a" >&2; exit 2 ;;
  esac
done
step() { echo; echo "== $*"; }
step build;            python3 site/build.py "${build_args[@]}"
step stepper;          node site/checks/check-core.js
if [ "$quick" = 0 ]; then
  step signals;        node site/checks/check-signals.js | tail -n 1
fi
if [ "$art" = 1 ]; then
  step parity;         python3 site/checks/check-parity.py --dist site/dist-artifact
  step links;          python3 site/checks/check-links.py --artifact
  step contract;       python3 site/checks/check-contract.py site/dist-artifact
  step smoke;          node site/checks/smoke.js --artifact
  echo; echo "site/check.sh --artifact: all checks passed ($(python3 -c 'import json;print(len(json.load(open("site/dist-artifact/FILES.json"))))') supporting files in FILES.json)"
else
  step parity;         python3 site/checks/check-parity.py
  step links;          python3 site/checks/check-links.py
  step contract;       python3 site/checks/check-contract.py site/dist
  step smoke;          node site/checks/smoke.js
  echo; echo "site/check.sh: all checks passed"
fi
