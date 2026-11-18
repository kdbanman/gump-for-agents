#!/usr/bin/env python3
"""place_report.py: tallies of place.py's survey, to set beside the push's sections 2 and 3.

    python3 place_report.py B|C [FILE...]"""
import json, os, sys
from collections import Counter
import qa


def main():
    kind = sys.argv[1]
    files = sys.argv[2:] or [os.path.join(qa.SCR, f'place_{kind}_0of1.jsonl')]
    recs = [json.loads(l) for fn in files for l in open(fn)]
    print(f'reader {kind}: {len(recs)} placements')
    st = Counter((r['stand']['B'], r['stand']['Bp']) for r in recs)
    print('  stand beside (B, Bp):', dict(sorted(st.items())))
    both = [r for r in recs if r['one']]
    print(f'  standing beside both: {len(both)}')
    free = {'B': [(1, 0, 0), (2, 2, 1)], 'C': [(1, 0, 2), (3, 0, 2)]}[kind]      # the right-going pulse at unit 0, own frame

    def fate(out, ok):
        if not ok:
            return 'not restored'
        if not out:
            return 'gone'
        us = sorted({c[0] >> 1 for c in map(tuple, out)})
        cells = sorted(tuple(c) for c in out)
        u0 = min(c[0] >> 1 for c in cells)
        base = sorted((c[0] - 2 * u0, c[1], c[2] + 2 * u0) for c in cells)
        return 'pass' if base == sorted(free) and u0 > 0 else f'other({len(cells)})'
    one = Counter()
    for r in both:
        fB = fate(*r['one']['L']['B']); fP = fate(*r['one']['L']['Bp'])
        clean = 'not restored' not in (fB, fP)
        one[('clean' if clean else 'unclean', (fB if clean else '-'), (fP if clean else '-'))] += 1
    print('  one pulse from the left end, (beside B, beside Bp):')
    for k, v in sorted(one.items()):
        print('     ', k, v)
    diff = sum(1 for r in both for side in 'LR' if r['one'][side]['B'][1] and r['one'][side]['Bp'][1] and r['one'][side]['B'][0] != r['one'][side]['Bp'][0])
    print(f'  one pulse, either end: restored beside both and a different travelling signal: {diff}')
    reads = [(r, k) for r in both for k, v in r['pairs'].items() if v['read']]
    pl = sorted({(r['g'], r['phase']) for r, k in reads})
    print(f'  pair reads: {len(reads)} (placement, end, spacing) in {len({(r["g"], r["phase"], tuple(r["t"])) for r, k in reads})} placements')
    by = {}
    for r, k in reads:
        by.setdefault((r['g'], r['phase'], tuple(r['t']), r['ur']), []).append((k, tuple(r['pairs'][k]['n'])))
    for key in sorted(by, key=lambda x: (x[1], x[0])):
        print('     g=%d phase=%d t=%s ur=%d:' % key, ' '.join(f'{k}:{n[0]}/{n[1]}' for k, n in sorted(by[key])))


if __name__ == '__main__':
    main()
