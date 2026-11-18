#!/usr/bin/env python3
"""latch_check (REVIEW-signals-8): the push's search for a pulse-triggered read (latch8.py --k 3 --pairs --words 3),
its 48 standing states rebuilt from their recorded events with st8 and each sent the pulse again.

    python3 latch_check.py F.json [--orc 6]

F.json = the file written by `python3 latch8.py --k 3 --pairs --words 3 --out F.json` (run from the push's
directory).  For each row the first recorded event is replayed: capL + 7^40 ddd f 7^40 + push 7's right cap; the
event at generation g0; 200 generations; a right-going pulse laid 20 and 21 units before the wall; 140 more.  The
letters of the wire are compared with the row's; --orc: that many rows are also run on the oracle (whole state
against st8 at the end).  Then every outcome is classed here: is there any in which no d is left and the whole
state is the plain line with a rigid train?
"""
import sys, re, json, time
import a8
from a8 import tr

T0 = time.time()


def hexrle(s):
    """the push's run-length form (exp8.hexrle): runs of three or more as x^n"""
    out = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i] + ('^%d' % (j - i) if j - i > 2 else s[i] * (j - i - 1))); i = j
    return ''.join(out)


def parse(tag, w0):
    if tag.startswith('word '):
        w = tag[5:]
        return 0, a8.word_cells('7' * len(w), w0 - len(w)) ^ a8.word_cells(w, w0 - len(w))
    g0 = int(tag[-1])
    tups = [tuple(int(v) for v in m.split(',')) for m in re.findall(r'\(([^)]*)\)', tag)]
    if tag.startswith('1cell'):
        u = int(re.match(r'1cell u(-?\d+)', tag).group(1))
        return g0, {tr(tups[0], w0 + u)}
    return g0, {tr(c, w0) for c in tups}


def replay(tag, d, sim):
    word = '7' * 40 + 'dddf' + '7' * 40; N = len(word); w0 = 44
    S = (a8.Orc if sim == 'orc' else a8.Box)(-6, N + 16)
    h = S.arr(a8.cell_state(word, a8.CAPR7))
    g0, fl = parse(tag, w0)
    h = S.run(h, g0); S.flip(h, sorted(fl)); h = S.run(h, 200 - g0)
    struct = a8.letters_of(S.cells(h), w0 - 8, w0 + 8)
    S.flip(h, [tr((1, 0, 0), w0 - d), tr((0, 2, 3), w0 - d + 1)]); h = S.run(h, 140)
    c = S.cells(h)
    return struct, a8.letters_of(c, 4, 4 + N), c


def main():
    rows = json.load(open(sys.argv[1]))
    norc = int(sys.argv[sys.argv.index('--orc') + 1]) if '--orc' in sys.argv else 6
    same = 0; rel = []; n = 0; orc_ok = 0; orc_n = 0
    for i, r in enumerate(rows):
        for j, d in enumerate((20, 21)):
            struct, w, c = replay(r['tags'][0], d, 'box')
            n += 1
            same += (struct == r['letters'] and hexrle(w) == r['outs'][j][0])
            if 'd' not in w and '?' not in w and '_' not in w and c == a8.cell_state(w, a8.CAPR7) and w.strip('7'):
                rel.append((r['letters'], a8.rle(w.strip('7'))))
            if i % max(1, len(rows) // norc) == 0 and j == 0 and orc_n < norc:
                s2, w2, c2 = replay(r['tags'][0], d, 'orc'); orc_n += 1; orc_ok += (c2 == c)
    print(('PASS ' if same == n else 'FAIL ') + f'{len(rows)} rows, both distances: structure letters and outcome letters equal to the push\'s in {same} of {n} (st8)  [{time.time() - T0:.0f} s]')
    print(('PASS ' if orc_ok == orc_n else 'FAIL ') + f'{orc_n} rows on the oracle: whole state at the end equal to st8 in {orc_ok}  [{time.time() - T0:.0f} s]')
    print(('PASS ' if not rel else 'NOTE ') + f'outcomes that are exactly the plain line with a train and no d left: {rel}')


if __name__ == '__main__':
    main()
