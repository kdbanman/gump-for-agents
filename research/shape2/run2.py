#!/usr/bin/env python3
"""Thin wrapper around research/shape/tslab.py (stepper research/peeling/rep.c on the twisted slab graph) that writes
to research/scratch/shape2/ instead of research/scratch/shape/.

    python3 research/shape2/run2.py run a k b CAP SEED W      # 64*W lives, one life each; output ch_a_k_b_sSEED.npz
    python3 research/shape2/run2.py validate a k b GENS N      # population vs engine, every generation (tslab.validate)
    python3 research/shape2/run2.py check a k b                # transverse layer periods (tslab.check)
    python3 research/shape2/run2.py stats a k b                # first-event statistics (tslab.stats)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'shape'))
import tslab  # noqa: E402
tslab.OUT = os.path.join(HERE, '..', 'scratch', 'shape2')
os.makedirs(tslab.OUT, exist_ok=True)

if __name__ == '__main__':
    c = sys.argv[1]; args = list(map(int, sys.argv[2:]))
    if c == 'run':
        tslab.run(*args)
    elif c == 'validate':
        sys.exit(0 if tslab.validate(*args) else 1)
    elif c == 'check':
        sys.exit(0 if tslab.check(*args) else 1)
    else:
        tslab.analyze(*args)
