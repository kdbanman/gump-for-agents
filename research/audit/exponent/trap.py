#!/usr/bin/env python3
"""Noise-immune debris in the driven-face models (review section 1.3).

For a model graph and a cube centre c (all-even doubled coordinates), put the cube's six faces alive and every other
dynamic cell dead, and check whether every dynamic cell's next state is forced (the same for every value of the
noise cells).  If so the state is a fixed point whatever the noise does: the face never dies.
  python3 trap.py            -> table over (R, w) for a cube at the vertex (R-1,0,0) and one in the face interior
"""
import graphs


def immune(g, cells_index, live):
    N, nb = g['N'], g['nb']
    st = [0] * (N + g['M'])
    for i in live:
        st[i] = 1
    for i in range(N):
        fixed = sum(st[j] for j in nb[i] if 0 <= j < N)
        nz = sum(1 for j in nb[i] if j >= N)
        outs = {int((fixed + k) in (4, 5) or (st[i] and fixed + k == 3)) for k in range(nz + 1)}
        if outs != {st[i]}:
            return False
    return True


def cube(c):
    out = []
    for a in range(3):
        for s in (1, -1):
            p = list(c); p[a] += s; out.append(tuple(p))
    return out


def main():
    for R, w in ((7, 3), (7, 4), (7, 5), (11, 3), (11, 4), (11, 5), (11, 6), (13, 4), (13, 5)):
        g = graphs.hull_model(R, w)
        ix = {p: i for i, p in enumerate(g['dyn'])}
        res = []
        k = (R + 1) // 3
        k += k % 2
        for name, c in (('vertex', (R - 1, 0, 0)), ('interior', (k, k, R - 1 - 2 * k))):
            cs = cube(c)
            if not all(p in ix for p in cs) or not any(sum(p) == R for p in cs):
                res.append('%s: n/a' % name); continue
            res.append('%s %s: %s' % (name, c, 'IMMUNE' if immune(g, ix, [ix[p] for p in cs]) else 'not immune'))
        print('hull model R=%d w=%d  ' % (R, w) + ';  '.join(res))
    for a, b, w in ((4, 4, 4), (4, 4, 5), (4, 4, 6)):
        g = graphs.slab_model(a, b, w)
        key = graphs.slab_canon(a, b)
        cells = graphs.slab_cells(a, b, [-(2 * j + 1) for j in range(w)])
        ix = {p: i for i, p in enumerate(cells)}
        c = (2, 2, -6)                      # a cube with faces in layers s = -1 and -3
        cs = [key(p) for p in cube(c)]
        ok = all(p in ix for p in cs) and immune(g, ix, [ix[p] for p in cs])
        print('slab model %dx%d w=%d  cube %s (layers %s): %s' % (a, b, w, c, sorted({sum(p) for p in cs}), 'IMMUNE' if ok else 'not immune'))


if __name__ == '__main__':
    main()
