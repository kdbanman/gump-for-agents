#!/usr/bin/env python3
"""layers.py NAME: write scratch/NAME.layers (cells of the third and fourth layer beneath each face of a slab) for boom.c run."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
nm = sys.argv[1]; m = json.load(open(os.path.join(SCR, nm + '.json'))); cells = m['cells']
lay = lambda s: [i for i, p in enumerate(cells) if sum(p) == s]
out = []
for s3, s4 in ((5, 7), (11, 9)):       # face 0 is s = 1 (layers 3, 5, 7 beneath), face 1 is s = 15 (13, 11, 9)
    for l in (lay(s3), lay(s4)): out.append(' '.join(map(str, [len(l)] + l)))
open(os.path.join(SCR, nm + '.layers'), 'w').write('\n'.join(out) + '\n'); print(nm, [len(x.split()) - 1 for x in out])
