"""Lead's own check that the clock's left cap eats any word of B and C units (2026-11-15).

Uses only reference/oracle.py and three lists of cells from research/signals/objects/clock-C.json (capL, the C
unit, capR); a B unit is the C unit with (0,2,3) taken out and (1,0,4) put in (as in objects/tape-BC.json).
Object(word) = capL + unit(word[k]) moved by k*(2,0,-2) for k = 0..N-1 + capR moved by N*(2,0,-2), in empty space.
Claim under test (research/signals/README.md, section 17): the word moves one unit towards the left cap every 2
generations and the cap swallows it, keeping no trace: at generation 2t the state is exactly Object(word shifted
by t and padded with C), for every t up to N, and after that the bare capped wire for good.
    python3 research/audit/signals_reader_lead_check.py [N] [number of random words] [seed]
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

d = json.load(open('research/signals/objects/clock-C.json'))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
nwords = int(sys.argv[2]) if len(sys.argv) > 2 else 6
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
C = [tuple(c) for c in d['unit']]; B = [c for c in C if c != (0, 2, 3)] + [(1, 0, 4)]
assert (0, 2, 3) in C and len(B) == 5
capL = [tuple(c) for c in d['capL']]; capR = [tuple(c) for c in d['capR']]
def obj(word):
    cells = set(capL) | {tr(c, N) for c in capR}
    for k, w in enumerate(word): cells |= {tr(c, k) for c in (B if w == 'B' else C)}
    return cells
allc = obj('C' * N) | obj('B' * N)
lo = [min(c[i] for c in allc) for i in range(3)]; hi = [max(c[i] for c in allc) for i in range(3)]
H = max(hi[i] - lo[i] for i in range(3)) + 28; H += H % 2
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
off = [((H - (hi[i] - lo[i])) // 2 - lo[i]) // 2 * 2 for i in range(3)]
def arr(cs):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple(c[i] + off[i] for i in range(3)); assert valid[x], c
        h[x] = True
    return h
words = ['C' * (N - 1) + 'B', 'B' + 'C' * (N - 1), 'CB' * (N // 2), 'C' * 3 + 'B' * (N - 6) + 'C' * 3]
words += [''.join(rng.choice(['B', 'C'], N - 2)) + 'CC' for _ in range(nwords)]
ok = True
for w in words:
    w = w.ljust(N, 'C')
    st = arr(obj(w)); good = True; first_bad = None
    for g in range(1, 2 * N + 9):
        st = oracle.step(st, m)
        if g % 2 == 0:
            t = g // 2
            want = arr(obj((w[t:] + 'C' * t)[:N]))
            if not np.array_equal(st, want):
                good = False; first_bad = g; break
    ok &= good
    print(w, 'eaten letter by letter, the cap unchanged at every even generation' if good else f'DIFFERS at generation {first_bad}')
print('PASS' if ok else 'FAIL')
