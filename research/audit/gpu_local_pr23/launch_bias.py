#!/usr/bin/env python3
"""Upper bound, from the committed per-life data, on the exposure that research/gpu/fwslab.py's launch grid leaves in
ln tau_face: a firewall found at a launch boundary (kind 4 ending exactly at a boundary) was formed at some time in
that launch, so it carries at most (boundary - previous boundary) of unrecognised exposure; a kind-3 life (period
3..128, recognised at generation P of the next launch) at most one launch + 128. Boundaries = the set of birth
generations and the run's end (every reseed happens at a boundary; a boundary without a reseed is not seen, which
only makes the bound larger). Runs without raw lives are listed as such.
    python3 research/audit/gpu_local_pr23/launch_bias.py research/data/gpu_facelaw
"""
import base64, glob, json, math, os, sys, zlib
import numpy as np


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'gpu'))
import facelaw  # noqa: E402  (only its unpack)
by = {}
for p in sorted(glob.glob(os.path.join(sys.argv[1], 'fwslab*.json'))):
    r = json.load(open(p))
    key = 'x'.join(map(str, r['slab']))
    b = by.setdefault(key, dict(E=0, F=0, ex4=0, ex3=0, n4b=0, n4=0, noraw=0, ml=set()))
    b['E'] += r['exposure']; b['F'] += r['face']; b['ml'].add(r.get('max_launch'))
    if 'raw' not in r:
        b['noraw'] += 1; continue
    a, k, bi, _ = facelaw.unpack(r['raw'])
    end = bi + a
    B = np.unique(np.concatenate([bi, [r['gens']]]))
    atb = np.isin(end, B)
    prev = B[np.maximum(np.searchsorted(B, end, 'left') - 1, 0)]
    m4 = (k == 4) & atb
    b['n4'] += int((k == 4).sum()); b['n4b'] += int(m4.sum())
    b['ex4'] += int((end - prev)[m4].sum())
    m3 = k == 3
    b['ex3'] += int(((end - prev) + 128)[m3].sum())
for key, b in by.items():
    frac = (b['ex4'] + b['ex3']) / b['E']
    print(f"{key:7s} max_launch {sorted(x for x in b['ml'] if x) or 'unrecorded'}: firewalls {b['n4']}, found at a boundary "
          f"{b['n4b']}; bound on unrecognised exposure {frac:.2e} of E (fw {b['ex4'] / b['E']:.2e}, kind 3 "
          f"{b['ex3'] / b['E']:.2e}) -> ln tau_face high by at most {frac:.4f} (stat. error {1 / math.sqrt(max(b['F'], 1)):.4f})"
          + (f"; {b['noraw']} run(s) without raw lives" if b['noraw'] else ''))
