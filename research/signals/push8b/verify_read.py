#!/usr/bin/env python3
"""Verify a read of a stored unit from a second wire, with reference/oracle.py alone (numpy, json and the oracle;
nothing else of this repository is imported).

    python3 verify_read.py objects/NAME.json

The file gives, for each stored value (a `case`):
  store     either `cells` (the store at generation 0) or `start` + `flips` + `gens` (cells at generation 0, cells
            flipped at given generations, and the number of generations after which the store is taken: push 7's line
            and its write);
  reader    the cells of the second wire, put beside the store at that moment (generation 0 of the read);
  missing   cells of the reader that the store makes die (the crossing's standing state), possibly none;
  probe     cells flipped at generation `probe_gen` (the signal put on the reader);
  out       the exact difference, at generation `out_gen`, between the run with the probe and the run without;
  restored  the generation from which the two runs are identical.
Checks, each with oracle.step on an array torus (`box`; every live cell stays more than 4 sites inside it, checked, so
the torus is never felt and the statements hold in empty space):
  A  (line cases) the store alone is standing: its state repeats after 4 generations at the moment it is taken
  B  store + reader, no probe: at generation 16 the state is exactly (store alone) u (reader alone) minus `missing`,
     and X(t + 4) = X(t) for t = 16 .. probe_gen + 4: a standing object, the store in it cell for cell as it is alone
  C  with the probe: at EVERY generation up to `until` no cell of the store's tube (1 <= x+y+z <= 5, 1 <= x-y+z <= 5)
     differs from the run without the probe: the store is never touched
  D  at `out_gen` the difference between the two runs is exactly `out`
  E  from `restored` to `until` the two runs are identical, cell for cell: store and reader are exactly as they were
  F  the `out` of the cases differ pairwise: the fate of the signal tells the stored values apart
Prints PASS or FAIL per check and ALL PASS."""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402


def masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


class Box:
    def __init__(self, shape, offset):
        self.shape = tuple(shape); self.off = tuple(offset); self.m = masks(self.shape)
        idx = np.indices(self.shape)
        x, y, z = (idx[i] - self.off[i] for i in range(3))
        self.tube = (x + y + z >= 1) & (x + y + z <= 5) & (x - y + z >= 1) & (x - y + z <= 5)

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            i = tuple(c[k] + self.off[k] for k in range(3))
            assert all(4 < i[k] < self.shape[k] - 5 for k in range(3)), ('cell outside the box', c)
            assert self.m[0][i] or self.m[1][i] or self.m[2][i], ('not a cell', c)
            h[i] = 1
        assert int(h.sum()) == len(set(map(tuple, cells)))
        return h

    def step(self, h):
        n = oracle.step(h, self.m)
        # nothing may come within 4 sites of the seam
        assert not n[:5].any() and not n[-5:].any() and not n[:, :5].any() and not n[:, -5:].any() \
            and not n[:, :, :5].any() and not n[:, :, -5:].any(), 'the pattern reached the edge of the box'
        return n

    def cells(self, h):
        return sorted(tuple(int(v) - self.off[k] for k, v in enumerate(p)) for p in np.argwhere(h))


def main():
    ob = json.load(open(sys.argv[1]))
    ok = True; t0 = time.time()
    outs = {}
    print(f"{ob['name']}: {ob['note']}")
    for case in ob['cases']:
        lab = case['label']
        st = case['store']
        if 'cells' in st:
            store = [tuple(c) for c in st['cells']]
        else:
            bx = Box(st['box'], st['offset'])
            start = ob[st['start']] if isinstance(st['start'], str) else st['start']
            h = bx.arr([tuple(c) for c in start])
            flips = {f[0]: f[1] for f in st['flips']}
            for t in range(st['gens']):
                if t in flips:
                    for c in flips[t]:
                        i = tuple(c[k] + bx.off[k] for k in range(3)); h[i] ^= 1
                h = bx.step(h)
            h4 = h
            for _ in range(4):
                h4 = bx.step(h4)
            good = bool((h4 == h).all())
            print('PASS' if good else 'FAIL', f"A  [{lab}] the store alone, {st['gens']} generations after its start (write at generation {sorted(flips)}), repeats after 4 generations: standing ({int(h.sum())} cells)"); ok &= good
            store = bx.cells(h)
        B = Box(ob['box'], ob['offset'])
        reader = [tuple(c) for c in case['reader']]
        assert not set(store) & set(reader), 'store and reader overlap'
        hs, hr, y = B.arr(store), B.arr(reader), B.arr(store + reader)
        pg, og, rg, until = case['probe_gen'], case['out_gen'], case['restored'], case['until']
        good = True; x = None; touched = False; dout = None; same_from = None
        for t in range(until + 1):
            if t == 16:
                want = hs | hr
                for c in case['missing']:
                    i = tuple(c[k] + B.off[k] for k in range(3)); assert want[i] == 1; want[i] = 0
                gB = bool((y == want).all()); y16 = y.copy()
            if 16 < t <= pg + 4 and (t - 16) % 4 == 0:
                gB &= bool((y == y16).all())
            if t == pg:
                x = y.copy()
                for c in case['probe']:
                    i = tuple(c[k] + B.off[k] for k in range(3)); x[i] ^= 1
            if x is not None:
                d = x != y
                if (d & B.tube).any():
                    touched = True
                if t == og:
                    dout = B.cells(d)
                if t >= rg and d.any():
                    good = False
            if t < until:
                y = B.step(y); hs = B.step(hs) if t < 16 else hs; hr = B.step(hr) if t < 16 else hr
                if x is not None:
                    x = B.step(x)
        print('PASS' if gB else 'FAIL', f"B  [{lab}] store ({len(store)} cells) + reader ({len(reader)} cells), no probe: at generation 16 exactly (store alone) u (reader alone) minus {len(case['missing'])} cell(s), and of period 4 to generation {pg + 4}"); ok &= gB
        print('PASS' if not touched else 'FAIL', f"C  [{lab}] probe of {len(case['probe'])} cells at generation {pg}: no cell of the store's tube differs from the probe-free run at any generation {pg}..{until}"); ok &= not touched
        want = sorted(tuple(c) for c in case['out'])
        gD = dout == want
        print('PASS' if gD else 'FAIL', f"D  [{lab}] at generation {og} the two runs differ in exactly the {len(want)} given cells ({case['out_text']})"); ok &= gD
        print('PASS' if good else 'FAIL', f"E  [{lab}] from generation {rg} to {until} the run with the probe is identical to the run without it"); ok &= good
        outs[lab] = dout
    labs = list(outs)
    gF = all(outs[a] != outs[b] for i, a in enumerate(labs) for b in labs[i + 1:])
    print('PASS' if gF else 'FAIL', f"F  what is travelling differs between the stored values {labs}"); ok &= gF
    print(('ALL PASS' if ok else 'SOME FAIL') + f"  ({time.time() - t0:.0f} s)")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
