#!/usr/bin/env python3
"""words8 (push 8): every word of up to K family units put into a standing background, and what it becomes.

    python3 words8.py [--K 3] [--mid ''] [--at left|right|in] [--g0 0] [--out F.json]

Background as in signals8 (capL + 7^50 + mid + 7^50 + capR).  An event replaces K consecutive units by a word over the
16 family units (hex digits; phase 0) at generation 0.  Without --mid the word sits in plain wire B; with --mid it
is placed so that its last unit is the unit before the stretch (--at left), its first unit the unit after the
stretch's edge (--at right), or straddling each boundary (--at in: every offset that overlaps the stretch).
Verdicts as signals8.  Printed: the count of each verdict, and for each mover the words that give it alone.
"""
import sys, os, json, itertools, argparse
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X, signals8 as S
from lab8 import tr


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--K', type=int, default=3); ap.add_argument('--mid', default='')
    ap.add_argument('--at', default='left'); ap.add_argument('--out'); ap.add_argument('--T', type=int, default=60)
    a = ap.parse_args()
    C = S.Census(a.mid, 50, 50, a.T)
    base = '7' * 50 + a.mid + '7' * 50
    w0 = 50; w1 = 50 + len(a.mid) - 1
    if not a.mid:
        offs = [50]
    elif a.at == 'left':
        offs = [w0 - a.K]
    elif a.at == 'right':
        offs = [w1 + 1]
    else:
        offs = list(range(w0 - a.K + 1, w1 + 1))
    rows = []
    for off in offs:
        for k in range(1, a.K + 1):
            for w in itertools.product('0123456789abcdef', repeat=k):
                w = ''.join(w)
                old = base[off:off + k]
                if w == old or (k > 1 and (w[0] == old[0] or w[-1] == old[-1])):
                    continue                      # shorter words cover it
                fl = X.hexword(old, 4 + off) ^ X.hexword(w, 4 + off)
                v, parts = C.event(fl, 0)
                rows.append(dict(word=w, off=off, verdict=v, parts=parts))
    def key(r):
        if r['verdict'] == 'move':
            return 'move: ' + ' + '.join(sorted(f"{n}({'>' if d > 0 else '<' if d < 0 else '.'})" for n, d, _ in r['parts']))
        if r['verdict'].startswith('stand'):
            return r['verdict'] + ' ' + r['parts'][0][0]
        return r['verdict']
    cnt = Counter(key(r) for r in rows); ex = defaultdict(list)
    for r in rows:
        ex[key(r)].append((r['word'], r['off']))
    print(f"background 7^50 {a.mid} 7^50, words at offsets {offs}: {len(rows)} events")
    for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print(f'  {v:5d}  {k}   e.g. {ex[k][:4]}')
    names = {v: dict(parity=k[0], cells=sorted(k[1])) for k, v in C.names.items()}
    for n in sorted(names, key=lambda s: int(s[1:])):
        print(f"  {n}: {len(names[n]['cells'])} cells {names[n]['cells'][:12]}{' ...' if len(names[n]['cells']) > 12 else ''}")
    if a.out:
        json.dump(dict(rows=rows, names=names), open(a.out, 'w'))


if __name__ == '__main__':
    main()
