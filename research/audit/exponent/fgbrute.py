#!/usr/bin/env python3
"""Independent brute force of the exact functional graphs of exponent.md section 6.2 (fg.c).

For a small vessel of the toy (B34/S234 on the cross (+-1,0), (+-2,0), (0,+-1), (0,+-2)), computes the successor of
every one of the 2^N states with numpy (cell by cell from the definition), then by plain array iteration: the
death time T of every state (T = 0 if some edge is empty), the immortal basin, the immortal cycles by period, and
all cycles.  Compares with the filed fg.c output research/scratch/exponent/fg_<kind>_<H>x<L>.txt.
Shares no code with research/theory/exponent/fg.c.

  python3 fgbrute.py strip 3 6  [box 4 4 ...]
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILED = os.path.join(HERE, '..', '..', 'scratch', 'exponent')


def successor(kind, H, L):
    N = H * L
    X = np.arange(1 << N, dtype=np.uint32)
    bit = lambda y, x: ((X >> np.uint32(y * L + x)) & np.uint32(1)).astype(np.uint8)
    B = {(y, x): bit(y, x) for y in range(H) for x in range(L)}
    out = np.zeros(1 << N, np.uint32)
    for y in range(H):
        for x in range(L):
            n = np.zeros(1 << N, np.uint8)
            for dy, dx in ((0, 1), (0, -1), (0, 2), (0, -2), (1, 0), (-1, 0), (2, 0), (-2, 0)):
                yy, xx = y + dy, x + dx
                if not 0 <= yy < H:
                    continue
                if kind == 'strip':
                    xx %= L
                elif not 0 <= xx < L:
                    continue
                n += B[(yy, xx)]
            s = B[(y, x)]
            alive = ((n == 3) | (n == 4) | ((s == 1) & (n == 2)))
            out |= alive.astype(np.uint32) << np.uint32(y * L + x)
    return out


def edges(kind, H, L):
    top = sum(1 << x for x in range(L)); bot = sum(1 << ((H - 1) * L + x) for x in range(L))
    e = [top, bot]
    if kind == 'box':
        e += [sum(1 << (y * L) for y in range(H)), sum(1 << (y * L + L - 1) for y in range(H))]
    return e


def analyse(kind, H, L):
    N = H * L
    F = successor(kind, H, L)
    X = np.arange(1 << N, dtype=np.uint32)
    alive = np.ones(1 << N, bool)
    for e in edges(kind, H, L):
        alive &= (X & np.uint32(e)) != 0
    INF = np.iinfo(np.int32).max
    T = np.where(alive, INF, 0).astype(np.int64)
    for _ in range(1 << 16):
        Tn = np.where(alive, np.minimum(T[F] + 1, INF), 0)
        if np.array_equal(Tn, T):
            break
        T = Tn
    # cyclic states: iterate the image until it stops shrinking
    cyc = np.ones(1 << N, bool)
    while True:
        img = np.zeros(1 << N, bool); img[F[cyc]] = True
        img &= cyc
        if img.sum() == cyc.sum():
            break
        cyc = img
    idx = np.nonzero(cyc)[0]
    per = np.zeros(len(idx), np.int64); z = F[idx].copy(); k = 1
    todo = np.ones(len(idx), bool)
    while todo.any():
        hit = todo & (z == idx); per[hit] = k; todo &= ~hit
        z = F[z]; k += 1
    imm = T[idx] >= INF
    hist = np.bincount(T[T < INF])
    res = dict(immortal_basin=int((T >= INF).sum()), immortal_cyclic_states=int(imm.sum()),
               cyclic_states=len(idx), death_hist=[int(v) for v in hist],
               immortal_by_period={int(p): int((per[imm] == p).sum() // p) for p in np.unique(per[imm])},
               cycles_by_period={int(p): int((per == p).sum() // p) for p in np.unique(per)})
    return res


def filed(kind, H, L):
    d = {}
    for line in open(os.path.join(FILED, 'fg_%s_%dx%d.txt' % (kind, H, L))):
        k, *v = line.split(); d[k] = v
    return dict(immortal_basin=int(d['immortal_basin'][0]), immortal_cyclic_states=int(d['immortal_cyclic_states'][0]),
                cyclic_states=int(d['cyclic_states'][0]), death_hist=[int(v) for v in d['death_hist']],
                immortal_by_period={int(t.split(':')[0]): int(t.split(':')[1]) for t in d['immortal_by_period'] if not t.startswith('big')},
                cycles_by_period={int(t.split(':')[0]): int(t.split(':')[1]) for t in d['cycles_by_period'] if not t.startswith('big')})


if __name__ == '__main__':
    a = sys.argv[1:]
    allok = True
    for i in range(0, len(a), 3):
        kind, H, L = a[i], int(a[i + 1]), int(a[i + 2])
        mine, theirs = analyse(kind, H, L), filed(kind, H, L)
        ok = mine == theirs
        allok &= ok
        print('%s %dx%d (N=%d): %s  basin %d, immortal cyclic states %d, cyclic states %d, max death time %d' %
              (kind, H, L, H * L, 'IDENTICAL to fg.c' if ok else 'DIFFERENT', mine['immortal_basin'],
               mine['immortal_cyclic_states'], mine['cyclic_states'], len(mine['death_hist']) - 1))
        if not ok:
            for k in mine:
                if mine[k] != theirs[k]:
                    print('   %s: mine %s\n   %s  fg.c %s' % (k, str(mine[k])[:300], ' ' * len(k), str(theirs[k])[:300]))
    print('ALL IDENTICAL' if allok else 'MISMATCH')
