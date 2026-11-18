#!/usr/bin/env python3
"""Rebuild section 6's results in README.md from data/ (between the markers).   python3 fill.py"""
import glob, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-slab', 'subpaths_full'))
t = subprocess.run([sys.executable, os.path.join(HERE, 'table_sub.py')], capture_output=True, text=True).stdout
pooled = t.split('Pooled over seeds')[1].split('\n', 1)[1].strip()
ps = []
for f in sorted(glob.glob(os.path.join(SCR, 'subpaths_*_s*.txt')), key=lambda f: [int(x) for x in re.findall(r'\d+', os.path.basename(f))][:3]):
    H, K, D = [int(x) for x in re.findall(r'\d+', os.path.basename(f))][:3]
    o = subprocess.run([sys.executable, os.path.join(HERE, 'subpaths.py'), f, str(3 * H * D)], capture_output=True, text=True).stdout
    ps.append(o.replace(SCR + '/', '').strip())
open(os.path.join(HERE, 'data', 'subpaths_stats.txt'), 'w').write('\n'.join(ps) + '\n')
body = '**Results** (`python3 table_sub.py`; every replication of version 2, pooled over seeds):\n\n' + pooled + '\n'
p = os.path.join(HERE, 'README.md'); s = open(p).read()
a, b = '<!-- SUB-RESULTS-BEGIN -->', '<!-- SUB-RESULTS-END -->'
if a not in s:
    s = s.replace('RESULTS-SUB-TABLE', a + '\n' + b)
s = s.split(a)[0] + a + '\n' + body + b + s.split(b)[1]
open(p, 'w').write(s)
print(body); print('\n'.join(ps))
