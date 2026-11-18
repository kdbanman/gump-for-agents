#!/usr/bin/env python3
"""push 8b: list the reads in the output of survey2.py.

    python3 reads.py FILE.jsonl [FILE2.jsonl ...] [--all]

An outcome is *clean* if the store and the reader are restored cell for cell at the end ('restored').  For each
placement class (cls) and launch delay, the sequence of outcomes over the positions u is printed when two positions
have different clean outcomes (a non-destructive read between the two local environments), and, with --all, when any
two positions differ."""
import json, sys
from collections import defaultdict, Counter

LINE = {1: '', 2: 'pp f', 3: 'ppp f', 4: 'pppp f'}


def key(rec, d):
    if rec['static'] == 'burn':
        return 'BURN'
    o = rec['pulse'][d]
    c = o['check'] if isinstance(o['check'], str) else 'sig' + str(len(o['check']))
    if o['final'] == 'restored':
        return c
    f = o['final']
    return c + ('/STORE' if f['store'] else '/reader') + str(f['n'])


def main():
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    show_all = '--all' in sys.argv
    by = defaultdict(dict)
    for fn in files:
        for l in open(fn):
            r = json.loads(l)
            by[(r['reader'], r['n'], r['cls'], r['g'], r['phi'])][r['u']] = r
    tot = Counter(); nread = 0
    for k in sorted(by):
        rows = by[k]
        us = sorted(rows)
        for d in (0, 1):
            seq = [key(rows[u], d) for u in us]
            for s in seq:
                tot[s.split('/')[0] if '/' not in s else s.split('/')[0] + '/' + ('STORE' if 'STORE' in s else 'reader')] += 1
            clean = set(s for s in seq if '/' not in s and s != 'BURN')
            # distinguish different sigN contents
            det = []
            for u in us:
                r = rows[u]
                if r['static'] == 'burn':
                    det.append('BURN'); continue
                o = r['pulse'][d]
                det.append(json.dumps(o['check']) if o['final'] == 'restored' else None)
            cl = set(x for x in det if x not in (None, 'BURN'))
            if len(cl) >= 2 or (show_all and len(set(seq)) >= 2):
                nread += len(cl) >= 2
                r0 = rows[us[0]]
                t0 = r0['t']; t0 = [t0[0] - 2 * us[0], t0[1], t0[2] + 2 * us[0]]
                print(f"{k[0]} n={k[1]} cls {k[2]} g {k[3]} phi {k[4]} delay {2 * d} t(u=0) {t0} ur {r0['ur']} static {[rows[u]['static'][0] for u in us]}")
                print('    ' + '  '.join(f'{u}:{s}' for u, s in zip(us, seq)))
    print('outcomes (all positions, both delays):', dict(tot))
    print('placement classes with two different clean outcomes at different positions:', nread)


if __name__ == '__main__':
    main()
