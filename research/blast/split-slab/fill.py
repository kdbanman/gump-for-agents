#!/usr/bin/env python3
"""Rebuild section 6's results in README.md from data/ (between the markers).   python3 fill.py"""
import glob, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-slab', 'subpaths_full'))
t = subprocess.run([sys.executable, os.path.join(HERE, 'table_sub.py')], capture_output=True, text=True).stdout
pooled = t.split('Pooled over seeds')[1].split('\n', 1)[1].strip()
ps = []; rows = []; groups = {}
for f in sorted(glob.glob(os.path.join(SCR, 'subpaths_*_s*.txt'))):
    groups.setdefault(tuple(int(x) for x in re.findall(r'\d+', os.path.basename(f))[:3]), []).append(f)
for (H, K, D), fs in sorted(groups.items(), key=lambda kv: (3 * kv[0][0] * kv[0][2], -kv[0][0])):
    o = subprocess.run([sys.executable, os.path.join(HERE, 'subpaths.py'), *fs, str(3 * H * D)], capture_output=True, text=True).stdout
    o = o.replace(SCR + '/', '')
    ps.append('\n'.join(l for l in o.strip().split('\n') if not l.startswith('ROW')))
    rows += [f'  | ({H},{K}),(0,{D}) ' + l[4:] for l in o.split('\n') if l.startswith('ROW')]
ptab = ('  | torus | cells | replications | fall >= A/2 | fall >= 0.4 A | largest fall | it starts from | and leaves | generations from it to the death |\n'
        '  |---|---:|---:|---|---|---|---|---|---|\n' + '\n'.join(rows))
open(os.path.join(HERE, 'data', 'subpaths_stats.txt'), 'w').write('\n'.join(ps) + '\n')
body = '**Results** (`python3 table_sub.py`; every replication of version 2, pooled over seeds):\n\n' + pooled + '\n'
p = os.path.join(HERE, 'README.md'); s = open(p).read()
a, b = '<!-- SUB-RESULTS-BEGIN -->', '<!-- SUB-RESULTS-END -->'
if a not in s:
    s = s.replace('RESULTS-SUB-TABLE', a + '\n' + b)
s = s.split(a)[0] + a + '\n' + body + b + s.split(b)[1]
pa, pb = '<!-- PATHTABLE-BEGIN -->', '<!-- PATHTABLE-END -->'
if pa not in s:
    s = s.replace('PATHTABLE', pa + '\n' + pb)
s = s.split(pa)[0] + pa + '\n' + ptab + '\n' + pb + s.split(pb)[1]
open(p, 'w').write(s)
print(body); print('\n'.join(ps))
