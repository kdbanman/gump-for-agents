#!/usr/bin/env python3
"""make8 (push 8): writes the JSON objects of this push.

    python3 make8.py            objects/line7-read.json, objects/cell8.json

objects/line7-read.json: push 7's 419-cell line (y0 of its record line-N80-gun4-end70-n1, copied), the writes (E and
n = 1..5 holes at generation 1, push 7's cells; the fifth hole by the same rule, 3 rakes further), and two reads made
at generation 882 by removing ONE cell: the count read (stator (0,1,2) of unit 40, the unit of wire B next to the
stretch) and the bit read (stator (0,1,4) of unit 70).  The cells a verifier should then see are written as
differences from the n = 1 line (pulses), from the definitions of the two pulses of wire B.
objects/cell8.json: the memory cell (see verify_cell8.py).
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wire8 as W, exp8 as X
from lab8 import tr

E = [[65, 2, -62], [66, 0, -63], [66, 0, -61]]
HOLE = lambda j: list(tr((1, 2, 2), 49 + 6 * j))


def line7():
    y0, f = W.push7_line(1)
    assert sorted(map(list, f[1])) == sorted(E + [HOLE(0)])
    for n in (2, 3, 4):
        assert sorted(map(list, W.push7_line(n)[1][1])) == sorted(E + [HOLE(j) for j in range(n)])
    d = dict(
        note="push 7's line (gun 4, 80 units of rake train, mirrored end 70; 419 cells at generation 0) and reads of what E and n holes "
             "write on it. Doubled coordinates (x, y, z); unit u = the cells with x in {2u, 2u+1}; the wire runs along (1,0,-1). "
             "writes[n]: cells flipped at generation 1 (E and n holes). At generation T0 the object is standing (period 4). "
             "count_read / bit_read: ONE cell removed at generation T0; probe[n] = the cells in which the state at probe_gen must "
             "differ from the n = 1 line (untouched after its write) at the same generation; at final_gen the whole state must "
             "equal that of the line named in final[n] (written and then left alone).",
        L=100, HY=16, y0=[list(c) for c in sorted(y0)],
        writes={str(n): [[1, E + [HOLE(j) for j in range(n)]]] for n in range(1, 6)},
        T0=882,
        count_read=dict(flip=list(tr((0, 1, 2), 40)), probe_gen=922,
                        probe={'1': [list(c) for c in X.pulseR(59)],
                               **{str(n): [list(c) for j in range(n) for c in X.pulseL(23 + 2 * j)] for n in (2, 3, 4)}},
                        final_gen=1103, final={str(n): 1 for n in (1, 2, 3, 4)}),
        bit_read=dict(flip=list(tr((0, 1, 4), 70)), probe_gen=942, probe={'1': [list(c) for c in X.pulseL(40)]},
                      final_gen=1082, final={'1': 1, '2': 3, '3': 4, '4': 5}))
    json.dump(d, open(os.path.join(HERE, 'objects', 'line7-read.json'), 'w'))
    print('wrote objects/line7-read.json')


if __name__ == '__main__':
    line7()
    if os.path.exists(os.path.join(HERE, 'cell8.py')):
        import cell8
        cell8.write()
