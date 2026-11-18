#!/usr/bin/env python3
"""verify_read8 (push 8): the reads of push 7's standing line, on reference/oracle.py alone (numpy, json).

    python3 verify_read8.py [objects/line7-read.json]

The oracle runs on the box torus 2L x HY x 2L (L = 100 units; the wire along (1,0,-1) closes into a ring; the object
is finite with dead margins, so by T2 the run is that of the infinite lattice).  Masks by oracle.masks' formula.
A_n: the line y0 with writes[n] flipped in at generation 1 (E and n holes), then left alone.  Checks:
  A  A_n(T0 + 4) == A_n(T0) for n = 1..5 (standing, period dividing 4) and the five states at T0 differ pairwise
  B  count read: A_n with ONE cell removed at T0 (count_read.flip), n = 1..4:
       at probe_gen the whole state == A_1 at that generation xor probe[n] (for n >= 2: n units of wire C in the wire
       B, i.e. n left-going pulses two units apart; for n = 1: one right-going pulse)
       at final_gen the whole state == A_1 at that generation (the stretch is gone, the pulses swallowed)
  C  bit read: A_n with ONE cell removed at T0 (bit_read.flip), n = 1..4:
       n = 1: at probe_gen the state == A_1 xor one left-going pulse, 30 units from where it was made (it crosses the
              place where the stretch would be); at final_gen == A_1 (swallowed by the left cap)
       n >= 2: at final_gen the state == A_{n+1} at that generation: the pulse is absorbed and the object is the one
              that one more hole would have written
Prints PASS or FAIL per check and ALL PASS.
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402


def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'objects', 'line7-read.json')
    d = json.load(open(fn))
    shape = (2 * d['L'], d['HY'], 2 * d['L'])
    par = np.indices(shape) % 2
    m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]
    valid = m[0] | m[1] | m[2]

    def idx(c):
        i = tuple(c[k] % shape[k] for k in range(3)); assert valid[i], c
        return i

    def arr(cells):
        h = np.zeros(shape, np.int8)
        for c in cells:
            h[idx(c)] = 1
        return h

    def xor(h, cells):
        h = h.copy()
        for c in cells:
            h[idx(c)] ^= 1
        return h

    def run(h, n):
        for _ in range(n):
            h = oracle.step(h, m)
        return h

    T0 = d['T0']; cr = d['count_read']; br = d['bit_read']
    gens = sorted({cr['probe_gen'], cr['final_gen'], br['probe_gen'], br['final_gen'], T0 + 4})
    ok_all = True; t0 = time.time()

    def report(ok, text):
        nonlocal ok_all
        ok_all &= bool(ok)
        print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - t0:.0f} s]', flush=True)

    def follow(h, t):
        """states of h (at generation t) at each generation of `gens`"""
        out = {}
        for g in gens:
            h = run(h, g - t); t = g; out[g] = h
        return out

    A0 = {}; A = {}
    for n in range(1, 6):
        h = arr(d['y0'])
        for g, cells in d['writes'][str(n)]:
            h = run(h, g); h = xor(h, cells)                    # one write generation per n
        A0[n] = run(h, T0 - d['writes'][str(n)][0][0])
        A[n] = follow(A0[n], T0)
        report(np.array_equal(A[n][T0 + 4], A0[n]), f'A  n = {n}: the written line is standing at generation {T0} (period dividing 4), {int(A0[n].sum())} cells')
    report(all(not np.array_equal(A0[i], A0[j]) for i in A0 for j in A0 if i < j), 'A  the five standing objects differ pairwise')
    for n in range(1, 5):
        B = follow(xor(A0[n], [cr['flip']]), T0)
        want = xor(A[1][cr['probe_gen']], cr['probe'][str(n)])
        what = 'one right-going pulse' if n == 1 else f'{n} left-going pulses (units of wire C), two units apart'
        report(np.array_equal(B[cr['probe_gen']], want), f"B  count read, n = {n}: one cell removed at {T0}; at {cr['probe_gen']} the state is the n = 1 line with {what}")
        f = cr['final'][str(n)]
        report(np.array_equal(B[cr['final_gen']], A[f][cr['final_gen']]), f"B  count read, n = {n}: at {cr['final_gen']} the whole state is the n = {f} line (plain wire B between the caps)")
    for n in range(1, 5):
        C = follow(xor(A0[n], [br['flip']]), T0)
        if str(n) in br['probe']:
            want = xor(A[1][br['probe_gen']], br['probe'][str(n)])
            report(np.array_equal(C[br['probe_gen']], want), f"C  bit read, n = {n}: one cell removed at {T0}; at {br['probe_gen']} the pulse has crossed 30 units of the line")
        f = br['final'][str(n)]
        txt = 'the pulse was swallowed by the left cap, nothing is left' if f == n else f'the pulse was absorbed: the object is the one {f} holes write'
        report(np.array_equal(C[br['final_gen']], A[f][br['final_gen']]), f"C  bit read, n = {n}: at {br['final_gen']} the whole state is the n = {f} line ({txt})")
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
