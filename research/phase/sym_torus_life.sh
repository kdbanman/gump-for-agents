#!/bin/sh
# Lifetimes of symmetric whole-torus soups (no hull, no faces): sym.py makes the soup, the engine runs it.
# usage: sym_torus_life.sh GROUP N RUNS CAP OUT.jsonl   (GUMP env var = engine binary with snapshot support)
G=${GUMP:-$(dirname "$0")/../../engine/target/release/gump}
D=$(dirname "$0"); T=$(mktemp -d)
for r in $(seq 1 "$3"); do
  python3 "$D/sym.py" soup "$1" "$2" 0.35 "$r" "$T/s.gump" >/dev/null
  "$G" run --snapshot "$T/s.gump" --torus "$2" --gens "$4" --hash-window 65536 | tail -1 |
    python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(json.dumps({'group':'$1','N':$2,'rng':$r,'status':d['status'],'life':d['cycle_start'] if d['cycle_start'] is not None else d['gen'],'pop':d['pop']}))"
done >> "$5"
rm -rf "$T"
