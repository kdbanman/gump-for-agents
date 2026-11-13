#!/usr/bin/env python3
"""Lineage statistics (memorylessness of single lineages) recomputed from a run's raw lives, with any window.

  python3 research/gpu/lineage.py research/data/gpu_facelaw/symvR40_s103_A10G.json 5     # the 5-tau numbers for R = 40

Complete-life sample: lives born at least T0 + L*tau before the end of the run (L = 2nd argument, default 10), so
each either died (residence = age - T0) or is known to outlive L*tau; settled lives (kinds 2, 3) and lives that ended
before T0 are excluded. Runs store raw lives only when they have at most 60,000 (facelaw.run, raw_cap).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelaw

r = json.load(open(sys.argv[1]))
L = float(sys.argv[2]) if len(sys.argv) > 2 else 10
if 'raw' not in r:
    raise SystemExit('no raw lives stored in this run (more than raw_cap lives); its lineage block was computed on the GPU host')
a, k, b = facelaw.unpack(r['raw'])
st = facelaw.lineage_stats(a, k, b, r['gens'], 1000 if r.get('sym') else 200, L_mult=L)
print(json.dumps({x: y for x, y in st.items() if x != 'hazard_by_age'}))
print('hazard x tau by age/tau:', ', '.join(f"[{h['lo_tau']:.2g},{h['hi_tau']:.2g}) {h['rate_x_tau']:.3f} ({h['deaths']})"
                                       for h in st['hazard_by_age'] if h['rate_x_tau'] is not None))
