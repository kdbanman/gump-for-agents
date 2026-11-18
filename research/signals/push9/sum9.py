#!/usr/bin/env python3
"""sum9 (push 9): summary of wall9.py output files.

    python3 sum9.py G.jsonl [G2.jsonl ...] [--show CLASS]

Classes of a (placement, e):
  trigger      the stretch stands with the object (rest inert or unchanged) and both pulses release it
  trigger-1    the same for one of the two pulses only
  falls        the stretch does not stand beside the object and is released without a pulse (wall-sensitive)
  keeps        the stretch is still there after a pulse and something else has changed on the wire (letters kept)
  mess         everything else
Printed per class: the number of (placement, e), of distinct objects, and the distinct outcomes with counts.
"""
import sys, json, re
from collections import Counter, defaultdict


def expand(rle):
    out = []
    for m in re.finditer(r'(.)(?:\^(\d+))?', rle):
        ch, n = m.group(1), m.group(2)
        out.append(ch * (int(n) if n else 1))
    return ''.join(out)


def klass(res):
    rest = res.get('rest', '')
    if rest.startswith('RELEASE') or rest == 'ERASED':
        return 'falls', rest.split('  ')[-1] if rest != 'ERASED' else 'ERASED'
    if rest in ('inert', 'unchanged'):
        a, b = res.get('A', ''), res.get('B', '')
        ra, rb = a.startswith('RELEASE') or a == 'ERASED', b.startswith('RELEASE') or b == 'ERASED'
        w = lambda x: x.split('  ')[-1].split(' ')[-1] if x.startswith('RELEASE') else x[:60]
        if ra and rb:
            return 'trigger', (w(a), w(b))
        if ra or rb:
            return 'trigger-1', (w(a), w(b))
        for x in (a, b):
            if x.startswith('other') and 'obj=same' in x:
                s = expand(x.split(' ')[1])
                if 'd' in s and '?' not in s and '_' not in s and '8' not in s and s.count('b') + s.count('6') > 0 and len(set(s) - set('7b6fd')) == 0:
                    return 'keeps', (w(a), w(b))
    return 'mess', None


def main():
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = sys.argv[sys.argv.index('--show') + 1] if '--show' in sys.argv else None
    rows = []
    for f in files:
        for l in open(f):
            try:
                rows.append(json.loads(l))
            except Exception:
                pass
    by = defaultdict(list)
    for r in rows:
        k, w = klass(r['res'])
        by[k].append((r, w))
    for k in ('trigger', 'trigger-1', 'falls', 'keeps', 'mess'):
        v = by.get(k, [])
        print(f'{k}: {len(v)} (placement, e); {len(set(r["id"] for r, _ in v))} objects')
        if k == 'mess':
            continue
        c = Counter((str(w), r['R'][:40], r['L'][:40]) for r, w in v)
        for kk, n in c.most_common(40):
            print(f'   {n:5d}  out {kk[0]}   | plain wire: R {kk[1]}, L {kk[2]}')
        if show == k:
            for r, w in v:
                print('     ', r['id'], r['gi'], r['ph'], r['t'], 'e', r['e'], w)


if __name__ == '__main__':
    main()
