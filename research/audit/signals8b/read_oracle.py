#!/usr/bin/env python3
"""read_oracle.py: the read of push 8b rebuilt on reference/oracle.py from the initial cells in the push's JSON.

    python3 read_oracle.py NAME [--long]      NAME = read-echo-B-line | read-pair-C-line | cell-small | read-echo-B-small | read-pair-C-small

Taken from the JSON: the start cells and write flips of the store (or its cells), the reader's cells, the probe's cells
and its generation.  NOT taken: `out`, `restored`, `missing`, any expected answer.  Everything printed is measured here.
Per case:
  S   the store alone at the moment it is taken: smallest p with X(t+p) = X(t), p in 1, 2, 4, 8
  U   store + reader, no probe: the generations 0..8 at which the state is exactly (store alone) u (reader alone); the
      smallest period of the joint state at generation 16; (--long) the same test again 400 generations on
  T   with the probe: the number of generations at which a cell of the store's tube 1 <= x+y+z <= 5, 1 <= x-y+z <= 5
      differs from the unprobed run (the tube is that of the push's frame; for the reader see `far`)
  D   size of the difference at every 2nd generation after the probe
  R   first generation from which probed = unprobed (then for ever: same state, same rule)
  E   the difference 30 generations after the probe
"""
import sys, time
import numpy as np
import qa


def period(box, h):
    x = h
    for p in range(1, 9):
        x = box.step(x)
        if (x == h).all():
            return p
    return None


def main():
    name = sys.argv[1]; long_ = '--long' in sys.argv
    ob = qa.obj(name); t0 = time.time()
    summary = []
    for case in ob['cases']:
        st = case['store']
        if 'cells' in st:
            store = [tuple(c) for c in st['cells']]
            bx = qa.Box.around(store, 12)
            hs = bx.arr(store)
        else:
            start = [tuple(c) for c in (ob[st['start']] if isinstance(st['start'], str) else st['start'])]
            bx = qa.Box.around(start, 12)
            hs = bx.arr(start)
            flips = {f[0]: [tuple(c) for c in f[1]] for f in st['flips']}
            for t in range(st['gens']):
                if t in flips:
                    bx.flip(hs, flips[t])
                hs = bx.step(hs)
        ps = period(bx, hs)
        store = bx.cells(hs)
        reader = [tuple(c) for c in case['reader']]
        probe = [tuple(c) for c in case['probe']]
        pg = case['probe_gen']
        print(f"[{case['label']}]  S: store {len(store)} cells, period {ps}", flush=True)
        B = qa.Box.around(store + reader, 16)
        tube = np.zeros(B.shape, bool)
        idx = np.indices(B.shape)
        x, y, z = (idx[i] - B.off[i] for i in range(3))
        tube = (x + y + z >= 1) & (x + y + z <= 5) & (x - y + z >= 1) & (x - y + z <= 5)
        s, r, u = B.arr(store), B.arr(reader), B.arr(store + reader)
        pr = period(B, r)
        union_ok = []
        for t in range(9):
            union_ok.append(bool((u == (s | r)).all()))
            s, r, u = B.step(s), B.step(r), B.step(u)
        # now at generation 9
        for t in range(9, 16):
            u = B.step(u)
        pu = period(B, u)
        print(f"   U: reader {len(reader)} cells, period {pr}; joint = union at generations 0..8: {union_ok}; joint period at generation 16: {pu}", flush=True)
        if long_:
            v = u
            for t in range(400):
                v = B.step(v)
            print(f"   U: 400 generations later the joint state is the same: {bool((v == u).all())}", flush=True)
        for t in range(16, pg):
            u = B.step(u)
        xx = u.copy(); B.flip(xx, probe)
        touched = 0; sizes = []; first_same = None; echo = []
        T = 140
        for t in range(T + 1):
            d = xx != u
            n = int(d.sum())
            if (d & tube).any():
                touched += 1
            if t % 2 == 0:
                sizes.append(n)
            if n == 0 and first_same is None:
                first_same = t
            if n and first_same is not None:
                first_same = None
            if t == 30:
                echo = B.cells(d)
            if n == 0:
                break
            xx, u = B.step(xx), B.step(u)
        print(f"   T: generations (of {t + 1}) with a difference inside the store's tube: {touched}")
        print(f"   D: difference size every 2 generations after the probe: {sizes}")
        print(f"   R: identical from {first_same} generations after the probe")
        print(f"   E: 30 generations after the probe the runs differ in {len(echo)} cells: {echo}", flush=True)
        summary.append((case['label'], ps, pu, all(union_ok), touched, first_same, echo))
    print(f'({time.time() - t0:.0f} s)')


if __name__ == '__main__':
    main()
