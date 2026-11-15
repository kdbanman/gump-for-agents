#!/usr/bin/env python3
"""Lift zombie_1_4_12_p16.txt to the cubic 12-torus (12 copies) and let the Rust engine report its period.
    python3 research/audit/shape3/zombie_check.py"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geom, validate as v  # noqa
L = (1, 4, 12); cells, *_ = geom.build(L); idx = {c: i for i, c in enumerate(cells)}
live = [idx[tuple(map(int, l.split()))] for l in open(os.path.join(HERE, 'zombie_1_4_12_p16.txt')) if not l.startswith('#')]
cf = os.path.join(v.OUT, 'zombie_lift.txt')
open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in v.lift(cells, live, L, 12)))
j = json.loads(subprocess.run([v.ENGINE, 'run', '--cells', cf, '--torus', '12', '--gens', '5000'], capture_output=True, text=True).stdout.splitlines()[-1])
print(f'slab cells {len(live)}, lifted {len(live) * 12}: engine status {j["status"]}, period {j["period"]}, cycle start {j["cycle_start"]}')
