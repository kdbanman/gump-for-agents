"""Lead's own check of the echo found by the review of the fifth signals push (2026-11-15).

Claim (research/audit/REVIEW-signals-5.md section 3 (iii)): the line (gun, wire, receiving cap capA) with a
catalogue oscillator standing beside capA answers a one-cell hole in the stream with a signal sent back: after the
hole has reached the end, the whole state differs from the undisturbed run in exactly three cells, which move
rigidly one unit towards the gun every two generations, through the oncoming rakes; the end, the oscillator and
every rake are as in the undisturbed run.  The gun dies when the signal arrives.

Here: reference/oracle.py only, and the initial cells of research/audit/signals5/end_echo.json (line, oscillator,
the generation tg at which the hole cell is removed).  None of the reviewer's code.  For each record:
  1  the hole cell is alive at generation tg of the undisturbed run;
  2  D(t) = gapped XOR undisturbed, over the whole torus: the generations at which D has exactly three cells, and
     whether D(t + 2) is D(t) moved one unit (2, 0, -2) for all of them (a rigid signal moving towards +x, the gun);
  3  while the signal travels, nothing else differs (that is what |D| = 3 says), so capA, the oscillator and every
     rake are as undisturbed;
  4  afterwards: the number of cells in which the two runs differ at the end of the run (the gun's fate).

    python3 research/audit/signals_echo_lead_check.py        (about 20 s)
"""
import json, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import oracle

H = 96
OFF = (32, 48, 64)
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
recs = json.load(open(os.path.join(HERE, 'signals5', 'end_echo.json')))


def arr(cs):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple((c[i] + OFF[i]) % H for i in range(3))
        assert valid[x], c
        h[x] = True
    return h


def cells(a):
    return sorted(tuple(int(v[i]) - OFF[i] for i in range(3)) for v in np.argwhere(a))


shift = lambda a: np.roll(np.roll(a, 2, axis=0), -2, axis=2)       # one unit towards +x
ok = True
for r in recs:
    line, osc = [tuple(c) for c in r['line']], [tuple(c) for c in r['oscillator']]
    xs = [c[0] for c in line + osc]; zs = [c[2] for c in line + osc]
    assert max(xs) - min(xs) < H - 30 and max(zs) - min(zs) < H - 30
    p = arr(set(line) | set(osc))
    for _ in range(r['tg']):
        p = oracle.step(p, m)
    hx = tuple((r['hole'][i] + OFF[i]) % H for i in range(3))
    alive = bool(p[hx])
    g = p.copy(); g[hx] = False
    D = []
    for t in range(1, 81):
        p = oracle.step(p, m); g = oracle.step(g, m)
        D.append(p ^ g)
    n = [int(d.sum()) for d in D]
    three = [t for t in range(1, 81) if n[t - 1] == 3]
    run = [t for t in three if t + 2 in three]
    rigid = bool(run) and all(np.array_equal(D[t + 1], shift(D[t - 1])) for t in run)
    first = cells(D[three[0] - 1]) if three else None
    echo = r['osc'] in ('C18.23a', 'C20.33c')          # the fifth record is the review's "wall", kept for comparison
    good = alive and ((len(three) >= 12 and rigid) if echo else not rigid)
    ok &= good
    print(f"{r['osc']} gap {r['gap_k']}: hole cell alive at generation {r['tg']}: {alive}")
    print(f"  cells differing, generations 1..80 after the hole: {n}")
    if three:
        print(f"  exactly three cells differ at generations {three[0]}..{three[-1]} ({len(three)} generations); "
              f"first: {first}; rigid, one unit towards the gun per two generations: {rigid}")
    print(f"  cells differing at generation 80: {n[-1]}   {('OK' if echo else 'OK (the wall: a front, the difference grows steadily, no compact signal)') if good else 'NOT AS CLAIMED'}")
print('PASS' if ok else 'FAIL')
