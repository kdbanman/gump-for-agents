#!/usr/bin/env python3
"""pool runs of one vessel (sum all counts).   python3 pool.py OUT IN1 IN2 ...   (names in research/scratch/blast/ref-boom/)"""
import sys, os
from collections import OrderedDict
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
acc = OrderedDict(); head = None
for name in sys.argv[2:]:
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A':
            head = l if head is None else head; continue
        if w[0] == 'E':
            key = ('E',); vals = [float(w[i]) for i in (1, 3, 5, 7, 9, 11)]
        elif w[0] in ('N', 'L', 'U'):
            key = (w[0], w[1]); vals = [float(w[2])]
        elif w[0] in ('D', 'C'):
            key = (w[0], w[1], w[2]); vals = list(map(float, w[3:]))
        elif w[0] == 'M':
            key = ('M',); vals = list(map(float, w[1:]))
        else:
            continue
        acc[key] = [a + b for a, b in zip(acc[key], vals)] if key in acc else vals
with open(os.path.join(S, sys.argv[1] + '.txt'), 'w') as f:
    f.write(head)
    order = {'E': 0, 'N': 1, 'L': 2, 'U': 3, 'D': 4, 'C': 5, 'M': 6}
    for key in sorted(acc, key=lambda k: (order[k[0]],) + tuple(int(x) for x in k[1:])):
        v = acc[key]
        if key[0] == 'E':
            f.write('E %d deaths %d old %d nper %d burnfail %d gens %d\n' % tuple(v))
        else:
            f.write(' '.join(key) + ' ' + ' '.join('%d' % x for x in v) + '\n')
