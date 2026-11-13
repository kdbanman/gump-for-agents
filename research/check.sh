#!/usr/bin/env bash
# Standing checks: re-verify the cheap, exact anchors of this project. One line per check; exit 1 on any failure.
# A few minutes on one core (most of it is building the engine and its tests).
#
#   research/check.sh            # from the repo root (or anywhere: it cd's there)
#   research/check.sh --long     # also: side-11 oracle vs golden log (~50 s) and the side-14/15 cube lifetimes (~5 min)
#   LEGACY_DIR=/home/user/kdbanman/gump/dev/cubic_init_results research/check.sh   # also the side-12/13 legacy logs
#
# What is covered and why: research/AUDIT-2026-11-13.md, section "Standing checks". Add a line here whenever a
# claim becomes an exact, fast anchor (a theorem check, a bit-exactness check, a number re-derived from committed data).
set -u
cd "$(dirname "$0")/.."
LONG=0; [ "${1:-}" = "--long" ] && LONG=1
G=engine/target/release/gump
FAILED=0; NCHECK=0
T0=$(date +%s)

# run NAME CMD... : pass iff the command exits 0
run() {
  local name=$1; shift
  local out s=$(date +%s)
  out=$("$@" 2>&1); local rc=$?
  NCHECK=$((NCHECK + 1))
  if [ $rc -eq 0 ]; then printf 'PASS  %-34s %4ss\n' "$name" $(( $(date +%s) - s ))
  else printf 'FAIL  %-34s %4ss  (exit %s)\n' "$name" $(( $(date +%s) - s )) $rc; FAILED=$((FAILED + 1)); echo "$out" | tail -15 | sed 's/^/      | /'; fi
}
# grepok NAME PATTERN-THAT-MUST-APPEAR PATTERN-THAT-MUST-NOT CMD... : for scripts that print results but always exit 0
grepok() {
  local name=$1 must=$2 mustnot=$3; shift 3
  local out s=$(date +%s)
  out=$("$@" 2>&1); local rc=$?
  NCHECK=$((NCHECK + 1))
  if [ $rc -eq 0 ] && echo "$out" | grep -Eq -- "$must" && { [ -z "$mustnot" ] || ! echo "$out" | grep -Eq -- "$mustnot"; }; then
    printf 'PASS  %-34s %4ss\n' "$name" $(( $(date +%s) - s ))
  else printf 'FAIL  %-34s %4ss\n' "$name" $(( $(date +%s) - s )); FAILED=$((FAILED + 1)); echo "$out" | tail -15 | sed 's/^/      | /'; fi
}

# --- engine: build and its own tests (fast vs scalar kernel, T2/T3 properties, snapshots, catalogue) ---
run  "engine build"                  bash -c "cd engine && cargo build --release -q"
run  "engine cargo test (27 tests)"  bash -c "cd engine && cargo test --release -q -- --test-threads=1"
# --- correctness anchors: original's logs, numpy oracle ---
run  "engine vs golden logs 8-11"    python3 engine/scripts/check_golden.py
run  "engine vs oracle (5 rules)"    python3 engine/scripts/check_oracle.py
run  "engine ensemble == per-gen"    python3 engine/scripts/check_ensemble.py
run  "engine layer deaths == events" python3 engine/scripts/check_deaths.py
for f in reference/golden/legacy_cube_side0{8,9}_H*.txt reference/golden/legacy_cube_side10_H*.txt; do
  H=$(echo "$f" | sed 's/.*_H\([0-9]*\)\.txt/\1/')
  grepok "oracle vs $(basename "$f" .txt | sed 's/legacy_cube_//')" "mismatches vs log: 0;" "" \
         python3 reference/oracle.py legacy-cube "$H" --compare "$f"
done
if [ "${LEGACY_DIR:-}" != "" ] && [ -f "$LEGACY_DIR/population26.txt" ]; then
  run "engine vs legacy logs 12, 13"  python3 engine/scripts/check_golden.py "$LEGACY_DIR/population24.txt" 65 "$LEGACY_DIR/population26.txt" 70
fi
# --- theorems and exact small facts ---
grepok "T1-T4 brute force (reference)" "T1 layer histogram.*True" "False|breached at gen: None" python3 reference/check_theory.py
run  "independent rule + T1-T4 (audit)" python3 research/audit/independent.py
run  "clockwork twists (audit)"      python3 research/audit/clockwork_check.py
grepok "threshold lemma checks (S5)"  "period>=3', 'overcrowded'\) 329" "period>=3', 'never|>2 or no convergence" \
       python3 research/theory/check_threshold.py
grepok "energy identity selftest"     "^selftest ok" "FAIL|Traceback|AssertionError" python3 research/theory/energy.py selftest
# --- other steppers in the repo, bit-exact against the engine ---
grepok "fluct orbit stepper (fl.c)"   "^ALL OK" "" python3 research/fluct/validate.py
grepok "peeling replica stepper (rep.c)" "octa15.* match " "MISMATCH" python3 research/peeling/validate.py
grepok "phase numpy stepper (gl.py)"  "^ALL OK" "MISMATCH" python3 research/phase/check_numpy.py
# --- numbers re-derived from committed data ---
run  "headline numbers from data (audit)" python3 research/audit/data_claims.py
# --- exact engine facts that the storyline quotes (side 11 and 13 peel schedules) ---
peel() {  # peel N "last_alive of the outer layers (axis 0, s>0, hull)\ncycle_start final_pop"
  local tmp; tmp=$(mktemp -d)
  $G run --cube "$1" --events "$tmp/ev.jsonl" --every 1 --out /dev/null > "$tmp/sum.json" || return 1
  local got; got=$(python3 -c "
import json,sys
ev=[json.loads(l) for l in open('$tmp/ev.jsonl')]
print(' '.join(str(e['last_alive']) for e in sorted(ev,key=lambda e:-e['s']) if e['axis']==0 and e['s']>0 and e['cause']=='hull' and e['last_alive']>4))
s=json.loads(open('$tmp/sum.json').read().splitlines()[-1]); print(s['cycle_start'], s['pop'])")
  rm -rf "$tmp"
  [ "$got" = "$2" ] || { echo "got: $got"; echo "want: $2"; return 1; }
}
run  "side-11 peels 3289/3476/3795"   peel 11 "$(printf '3289 3476 3795\n4218 36')"
run  "side-13 peels, end 169049"      peel 13 "$(printf '130191 145841 156784 166634 168161\n169049 108')"
if [ $LONG -eq 1 ]; then
  grepok "oracle vs side11_H60 (long)" "mismatches vs log: 0;" "" \
         python3 reference/oracle.py legacy-cube 60 --compare reference/golden/legacy_cube_side11_H60.txt
  cube_end() { $G run --cube "$1" --every 64 --out /dev/null --hash-window 65536 | tail -1 | grep -q "\"gen\":$2,.*\"pop\":$3,"; }
  run "side-14 ends 4460298, p2 528"   cube_end 14 4460298 528
  run "side-15 ends 37367092, extinct" cube_end 15 37367092 0
fi

echo "check.sh: $((NCHECK - FAILED))/$NCHECK passed in $(( $(date +%s) - T0 ))s"
[ $FAILED -eq 0 ]
