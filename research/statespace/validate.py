#!/usr/bin/env python3
"""Check enum.c's step against reference/oracle.py on a vessel, generation by generation.

  validate.py ENUM KIND ARGS... [--states K] [--gens T] [--extra HEX,HEX,...]

K random states (uniform over the vessel's 2^N states, fixed rng 12345) plus the --extra states (champions) are
iterated T generations by `ENUM FILE --iterate T` and, independently, by oracle.step on the lifted state in the
oracle's array torus (vessels.embed). At every generation every copy of every vessel cell must agree with the
enumerator, and every valid oracle cell that is not a copy of a vessel cell must be dead (so no other cell is ever
alive). Prints OK or the first mismatch and exits 1.
"""
import os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import vessels as V
import oracle


def main():
    enum, kind = sys.argv[1], sys.argv[2]
    na = {'hull': 8, 'slab': 4, 'torus': 6}[kind]
    args = sys.argv[3:3 + na]; rest = sys.argv[3 + na:]
    K, T, extra = 40, 40, []
    for i, a in enumerate(rest):
        if a == '--states': K = int(rest[i + 1])
        if a == '--gens': T = int(rest[i + 1])
        if a == '--extra': extra = [int(x, 16) for x in rest[i + 1].split(',') if x]
    v = V.make(kind, args)
    rng = np.random.default_rng(12345)
    states = [int(x) for x in rng.integers(0, 1 << v.n, K, dtype=np.int64)] + extra
    with tempfile.NamedTemporaryFile(suffix='.nb', delete=False) as tf:
        fn = tf.name
    v.write(fn)
    out = subprocess.run([enum, fn, '--iterate', str(T)], input='\n'.join('%x' % s for s in states) + '\n',
                         capture_output=True, text=True, check=True).stdout.split('\n')
    os.unlink(fn)
    H, place, others = V.embed(v)
    m = oracle.masks(H)
    place_idx = [tuple(np.array(pl).T) for pl in place]
    oth = tuple(np.array(others).T) if others else None
    for si, line in enumerate(out[:len(states)]):
        traj = [int(x, 16) for x in line.split()]
        h = np.zeros((H, H, H), np.int8)
        for i in range(v.n):
            if traj[0] >> i & 1:
                h[place_idx[i]] = 1
        for g in range(1, T + 1):
            h = oracle.step(h, m)
            for i in range(v.n):
                vals = h[place_idx[i]]
                want = traj[g] >> i & 1
                if not (vals == want).all():
                    print(f'MISMATCH {v.name()} state {traj[0]:x} gen {g} cell {i}: enum {want}, oracle {vals.tolist()}')
                    sys.exit(1)
            if oth is not None and h[oth].any():
                print(f'LEAK {v.name()} state {traj[0]:x} gen {g}: a cell outside the vessel is alive')
                sys.exit(1)
    print(f'OK {v.name()} N={v.n} H={H} copies/cell={len(place[0])} states={len(states)} gens={T}')


if __name__ == '__main__':
    main()
