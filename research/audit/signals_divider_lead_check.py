"""Lead's own check of the fourth push's divider (2026-11-15).  Uses only reference/oracle.py and the cell lists
capA, unit, gun, osc of research/signals/objects/divider-C8.json.

Object(N) = capA + N units of bare wire C + gun and osc moved by N units, alone in empty space; the line is the same
without osc.  Claims (research/signals/README.md sections 21, 21b): the line is a free-standing oscillator of
period 4 (a gun, a wire, a cap that swallows the rakes); with the period-8 oscillator beside the wire every second
rake is removed, the wire beyond carries one rake per 8 generations, the whole object has period exactly 8, and the
oscillator is never changed.

Checked here, cell for cell:
  1  osc alone has period exactly 8, and stays in the layers x + y + z >= 7 (the wire's tube is <= 5);
  2  in Object(N), at every generation, every cell of osc alone is alive, and the only other cell ever alive in
     those layers is one cell beside the oscillator, alive at generations 8, 16, 24, ... and dead one generation
     later (so "never changed" holds for the oscillator's own cells; the push's wording does not mention this cell);
  3  the line (no osc) is periodic with period exactly 4 from some generation on; Object(N) with period exactly 8;
  4  late in the run, along the wire between the cap and the oscillator: the line's pattern repeats every 2 units;
     the divider's repeats every 4 units and not every 2;
  5  read unit by unit (stators present, sites (1,0,0), (1,0,2), (1,0,4), (0,2,3) as bits 0..3) at the last even
     generation, that stretch of the line is 5f5f..., of the divider 5f9f5f9f... (wire C itself is b).

    python3 research/audit/signals_divider_lead_check.py [N]        (default N = 24; about a minute)
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
ob = json.load(open('research/signals/objects/divider-C8.json'))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
capA, unit, gun, osc = ([tuple(c) for c in ob[k]] for k in ('capA', 'unit', 'gun', 'osc'))
bare = {tr(c, k) for c in unit for k in range(-6, N + 6)}           # wire C, for comparison only
line = set(capA) | {tr(c, k) for c in unit for k in range(N)} | {tr(c, N) for c in gun}
oscN = {tr(c, N) for c in osc}
H = 128
OFF = (24, 56, 2 * N + 44)
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
idx = np.indices((H, H, H))
X = idx[0] - OFF[0]
S = (idx[0] - OFF[0]) + (idx[1] - OFF[1]) + (idx[2] - OFF[2])
outer = S >= 7


def arr(cs):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple(c[i] + OFF[i] for i in range(3))
        assert all(8 <= v < H - 8 for v in x) and valid[x], (c, x)
        h[x] = True
    return h


def shift(a, k):
    return np.roll(np.roll(a, 2 * k, axis=0), -2 * k, axis=2)


def history(h, T):
    out = [h]
    for _ in range(T):
        h = oracle.step(h, m); out.append(h)
    return out


def period_from(hist, p):
    """smallest t0 with hist[t] == hist[t + p] for all t >= t0 in the run (None if not even at the end)"""
    t0 = None
    for t in range(len(hist) - p - 1, -1, -1):
        if np.array_equal(hist[t], hist[t + p]):
            t0 = t
        else:
            break
    return t0


T = 2 * N + 96
ok = True
ho = history(arr(oscN), T)
r = np.array_equal(ho[0], ho[8]) and not np.array_equal(ho[0], ho[4]) and all(not (h & ~outer).any() for h in ho)
ok &= r; print(f'N = {N}, {T} generations on the oracle\n1  osc alone: period exactly 8, always in x + y + z >= 7: {r}')
hd = history(arr(line | oscN), T)
allthere = all(not (ho[t] & ~hd[t]).any() for t in range(T + 1))
extra = {}
for t in range(T + 1):
    for c in np.argwhere(hd[t] & outer & ~ho[t]):
        extra.setdefault(tuple(int(v) for v in c - np.array(OFF)), []).append(t)
r = allthere and len(extra) <= 1 and all(ts == list(range(8, T + 1, 8)) for ts in extra.values())
ok &= r; print(f'2  every cell of the free oscillator alive at every generation: {allthere}; other cells ever alive in the outer '
               f'layers: {[(c, "generations 8, 16, ..., %d" % ts[-1]) for c, ts in extra.items()]}: {r}')
hl = history(arr(line), T)
tl4, td8, td4 = period_from(hl, 4), period_from(hd, 8), period_from(hd, 4)
tl2 = period_from(hl, 2)
r = tl4 is not None and tl4 < T - 40 and tl2 is None and td8 is not None and td8 < T - 40 and td4 is None
ok &= r; print(f'3  line: period 4 from generation {tl4} (period 2: {tl2}); divider: period 8 from generation {td8} (period 4: {td4}): {r}')
a, b = 3, N - 8                                   # units between the cap and the oscillator (osc is at units N-4..N-2)
win = lambda lo, hi: (X >= 2 * lo) & (X < 2 * hi) & ~outer
rep = lambda h, p: np.array_equal(shift(h, -p) & win(a, b - p), h & win(a, b - p))
r = all(rep(hl[t], 2) for t in range(T - 8, T + 1)) and all(rep(hd[t], 4) and not rep(hd[t], 2) for t in range(T - 8, T + 1))
ok &= r; print(f'4  units {a}..{b - 1}, last 9 generations: line repeats every 2 units; divider every 4 and not every 2: {r}')
SITES, ST = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)], {(0, 1, 2), (0, 1, 4)}


def word(h, lo, hi):
    w = ''
    for u in range(lo, hi):
        cs = {tuple(int(v) for v in c - np.array(OFF)) for c in np.argwhere(h & (X >= 2 * u) & (X < 2 * u + 2) & ~outer)}
        cs = {(c[0] - 2 * u, c[1], c[2] + 2 * u) for c in cs}
        w += '%x' % sum(1 << i for i in range(4) if SITES[i] in cs) if ST <= cs and not (cs - ST - set(SITES)) else '?'
    return w


t = T - (T % 2)
wl, wd = word(hl[t], a, b), word(hd[t], a, b)
r = set(wl[0::2] + '|' + wl[1::2]) == set('5f|') and wl[0] != wl[1] and all(wd[i] == wd[i + 4] for i in range(len(wd) - 4)) \
    and sorted(wd[:4]) == ['5', '9', 'f', 'f']
ok &= r; print(f'5  generation {t}, units {a}..{b - 1}: line {wl}, divider {wd}: {r}')
print('PASS' if ok else 'FAIL')
