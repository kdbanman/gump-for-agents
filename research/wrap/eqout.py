#!/usr/bin/env python3
"""The lead's check: fit without the 48- and 57-cell equilateral faces, forecast them.  python3 research/wrap/eqout.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fit as Fm, models as Mm  # noqa: E402
for mode, corr in (('lead', False), ('all', True)):
    pts = Fm.select(mode, corr, wrap=False)
    eq = [p for p in pts if p['A'] in (48, 57) and p['g'][0] == p['g'][1] == p['g'][2]]
    tr = [p for p in pts if p not in eq]
    for model in ('LAW', 'HAZ'):
        v, fe = Mm.forecast(model, tr, eq, Mm.START[model])
        print(f'{mode:4s} data, {model}: ' + '; '.join(f"A={p['A']} measured {p['y']:.4f} forecast {x:.4f} ± {e:.4f} "
              f"(diff {p['y'] - x:+.4f})" for p, x, e in zip(eq, v, fe)))
