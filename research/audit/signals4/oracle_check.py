#!/usr/bin/env python3
"""st.step against reference/oracle.py, cell for cell, on the objects REVIEW-signals-4 uses:
line N = 9, beam N = 9 and 10, divider N = 12 and 13, a divider with a hole, a beam with holes, the line with two
oscillators, and C8.24b beside the line.  Oracle on a torus with 30 doubled units of padding; compared every
generation for G generations.   python3 oracle_check.py"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
sys.path.insert(0, os.path.join(st.ROOT, 'reference'))
import oracle


def compare(name, cells, G):
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    H = span + 60; H += H % 2
    off = tuple(H // 4 * 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 4 * 2 for i in range(3))
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    m = oracle.masks(H); s = frozenset(cells)
    for t in range(G):
        h = oracle.step(h, m); s = st.step(s)
        o = frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in np.argwhere(h))
        if o != s:
            print('FAIL', name, 'generation', t + 1); return False
    print('PASS', name, f'{len(cells)} cells, {G} generations, H = {H}', flush=True); return True


if __name__ == '__main__':
    import objects4 as ob
    ok = True
    for name, cells, G in ob.controls():
        ok &= compare(name, cells, G)
    print('ALL PASS' if ok else 'SOME FAILED')
