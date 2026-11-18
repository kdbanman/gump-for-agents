#!/usr/bin/env python3
"""near.py (audit of push 8b, q.c): does the echo reader sense a wall or an edge at a distance?

    python3 near.py

Store: a capped wire B of 56 units with a stretch d^k f (wall at unit w, edge at w + k).  Readers B13 and B8 with the
crossing at unit 0.  For every w in -12..12 and k = 1..5: does the reader stand, and is the response to the reading
pair EXACTLY (cell for cell, generation for generation, in the reader's frame) the response beside plain wire B or
beside a long stretch?  A response that differed from both would be a read of the wall's distance.
Printed per reader and k: one character per w:  X the reader does not stand;  B / P the whole history of the
difference (probed xor unprobed, every generation until it vanishes) equals that beside plain B / beside the middle
of a long stretch;  ? it equals neither (listed below the table)."""
import qa, rd
from qa import pk, up, run, xor, union, same

OWN = rd.capped(-14, 14)


def word(w, k, ua=-28, ub=28):
    s = ['7'] * (ub - ua)
    if k:
        for u in range(w, w + k):
            s[u - ua] = 'd'
        s[w + k - ua] = 'f'
    return ''.join(s)


def history(J, P, ur, T=300):
    r = rd.lock(J, {0: pk(P(rd.pR(ur - 9) + rd.pR(ur - 10)))}, T)
    if r['first'] is None or r['tube']:
        return None
    return tuple(tuple(r['diffs'][t].tolist()) for t in range(r['first']))


if __name__ == '__main__':
    for name, mk, ur in (('B13', rd.B13, -1), ('B8', rd.B8, 0)):
        P = mk(0)
        ref = {}
        for lab, wd in (('B', word(0, 0)), ('P', word(-20, 40))):
            v, J, R = rd.install(pk(rd.capped(-28, 28, wd)), P, OWN)
            ref[lab] = history(J, P, ur)
            print(f'{name}: beside {"plain wire B" if lab == "B" else "the middle of a stretch of 40"}: install {v}, response lasts {len(ref[lab])} generations')
        odd = []
        for k in range(1, 6):
            row = ''
            for w in range(-12, 13):
                v, J, R = rd.install(pk(rd.capped(-28, 28, word(w, k))), P, OWN, settle=160)
                if J is None or v == 'store':
                    row += 'X'; continue
                h = history(J, P, ur)
                if h is None:
                    row += '!'; odd.append((k, w, 'not restored or the store touched'))
                elif h == ref['B']:
                    row += 'B'
                elif h == ref['P']:
                    row += 'P'
                else:
                    row += '?'; odd.append((k, w, f'response lasts {len(h)} generations'))
            print(f'  k={k}  w=-12..12:  {row}')
        for o in odd:
            print('   ', o)
