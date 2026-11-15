#!/usr/bin/env python3
"""research/constant/eq_forecast.py (part C of research/constant/PREDICTIONS.md) re-run with the 4x4 anchor replaced
by this review's own measurement (t4.c: E = 2.9696e10, F = 2,907,478, ln tau_face = 9.9246 +- 0.0006) instead of
research/shape2/data/A48.csv's (4,0,4) row. Nothing in research/constant is changed; the loader is patched in memory.
    python3 research/audit/gpu_local_pr23/eq_forecast_patched.py"""
import os, runpy, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'constant'))
import load  # noqa: E402
_raw = load.periodic_raw


def patched(*a, **k):
    out = _raw(*a, **k)
    for r in out:
        if r['src'] == 'shape2/A48.csv:4 0 4':
            r['E'], r['F'], r['W'] = 2.9696e10, 2907478, 7454
            r['y'], r['se'] = load.pt(r['E'], r['F'], 2)
    return out


load.periodic_raw = patched
sys.argv = ['eq_forecast.py']
runpy.run_path(os.path.join(ROOT, 'research', 'constant', 'eq_forecast.py'), run_name='__main__')
