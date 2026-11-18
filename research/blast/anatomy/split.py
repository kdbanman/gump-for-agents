#!/usr/bin/env python3
"""Crude split of a wrapped face's death rate: (falls of >= half the face per generation in the living face) x
(share of such falls that are fatal). Reads out/RUN_crash.json and the .sum files.   python3 split.py"""
import json, os, numpy as np, deaths as D
for run in ('t48', 'tube54', 'tube60', 't63', 't75'):
    c = json.load(open(os.path.join(D.HERE, 'out', run + '_crash.json'))); s = D.read_sum(run)
    ev = c['share_fall_half_ctl'] * c['deaths']; rate = c['share_fall_half_ctl'] / 10
    fatal = c['share_fall_half'] * np.exp(-s['lntau']) / rate
    print(f'{run}: A = {int(s["na"])}; {ev:.0f} falls of >= half the face in {c["deaths"]} living windows of 10 generations: ln(rate per generation) = {np.log(rate):.2f} '
          f'+- {1 / np.sqrt(max(ev, 1)):.2f}; ln(share of them fatal) = {np.log(fatal):.2f}; ln tau = {s["lntau"]:.3f}')
