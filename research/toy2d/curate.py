"""Copy the small, curated results from research/scratch/toy2d/law_*.json into research/toy2d/data/.
python3 research/toy2d/curate.py   (then figures.py)"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, '..', 'scratch', 'toy2d'); D = os.path.join(HERE, 'data')
os.makedirs(D, exist_ok=True)
jobs = [  # (scratch file, curated name, n edges, extra args)
    ('law_cross2_B34S234_W16_none_main.json', 'law_cross2_B34S234.json', 2, []),
    ('law_moore_B45S23467_W16_none_main.json', 'law_moore_B45S23467.json', 2, []),
    ('law_cross2_B34S234_W16_mx_sym.json', 'law_cross2_B34S234_mx.json', 2, []),
    ('law_cross2_B34S234_W16_my_sym.json', 'law_cross2_B34S234_my.json', 2, []),
    ('law_cross2_B34S234_W16_t2_sym.json', 'law_cross2_B34S234_t2.json', 2, []),
] + [('law_cross2_B34S234_box0_%s_sym.json' % s, 'law_cross2_B34S234_box_%s.json' % s, 4, []) for s in ('none', 'd4', 'c4', 'diag')]
for src, dst, ne, extra in jobs:
    p = os.path.join(SCR, src)
    if not os.path.exists(p):
        print('missing', src); continue
    out = subprocess.run([sys.executable, os.path.join(HERE, 'analyze.py'), p, '--ne', str(ne), '--json', os.path.join(D, dst)] + extra,
                         capture_output=True, text=True)
    print('==', dst); print(out.stdout[-3000:], out.stderr[-500:])
raw = json.load(open(os.path.join(SCR, 'law_cross2_B34S234_W16_none_main.json')))
json.dump({L: dict(age_exposure=r['age_exposure'], age_deaths=r['age_deaths']) for L, r in raw.items()},
          open(os.path.join(D, 'law_cross2_B34S234_raw_hazard.json'), 'w'))
