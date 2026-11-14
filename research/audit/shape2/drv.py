#!/usr/bin/env python3
"""Driver for the review of research/shape2/: reuses research/audit/shape/ts.c + ts.py (independent of
research/shape2 and research/shape), with output redirected to research/scratch/audit_shape2/.

    python3 research/audit/shape2/drv.py validate a k b GENS N
    python3 research/audit/shape2/drv.py run a k b W GENS SEED [CAP]
    python3 research/audit/shape2/drv.py stats a k b [CAP]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import ts  # noqa
ts.OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_shape2')
ts.BIN = os.path.join(ts.OUT, 'ts')
os.makedirs(ts.OUT, exist_ok=True)

if __name__ == '__main__':
    c = sys.argv[1]; args = list(map(int, sys.argv[2:]))
    L = tuple(args[:3])
    if c == 'validate':
        sys.exit(0 if ts.validate(L, args[3], args[4]) else 1)
    elif c == 'run':
        ts.run(L, args[3], args[4], args[5], *(args[6:7] or [500000]))
    else:
        ts.stats(L, *(args[3:4] or [500000]))
