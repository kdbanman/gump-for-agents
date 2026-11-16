"""Lead's own check of the fifth signals push's census of ends (2026-11-15).

Claim (research/signals/README.md section 27): of 741 ends of the rake train, 599 heal every word of gaps exactly
and 142 are destroyed by every word; nothing else happens.  The push stepped with its own windowed stepper, with
the train refilled 100 units back, and called a run healed when a window of 40 units in front of the end equals
the plain run's.

Here: a sample of ends (fixed seed), each put at the end of a FINITE train of L units alone on a torus, stepped by
reference/oracle.py only.  From the push come only the initial conditions: the end's cells (its `cap`), the
train's cells at generation 0 (sat_gun.train_cells) and which cell is the hole.  Per end and word, two runs, with
and without the hole:

  healed   the two WHOLE states (every cell of the torus, not a window) are equal at some generation g <= G, while
           the plain run's end still stands (its units >= KS - 6 repeat with the end's period at g: the train's
           far tail has not arrived).  Whole-state equality also rules out an echo sent back up the stream.
  dead     the two states differ at every generation <= G, and at generation G the holed run differs from the
           plain run in the train at least 12 units in front of the end, while the plain run's end still stands.

    python3 research/audit/signals_ends_lead_check.py [PER_CLASS] [SEED]     (default 6 + 6 ends, seed 1; ~100 s)
    python3 research/audit/signals_ends_lead_check.py all [i/n]              (every end; part i of n; ~100 core-min)
    EVENT=k0 python3 research/audit/signals_ends_lead_check.py all [i/n]     (the review's second signal, K0, in place
                                          of the holes: prints the table of the push's hole outcome against K0's)
"""
import json, sys, random, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
sys.path.insert(0, os.path.join(HERE, '..', 'signals'))
import oracle
os.chdir(os.path.join(HERE, '..', 'signals'))
import sat_gun as G                      # geometry of the initial state only: train(), train_cells()

ALL = len(sys.argv) > 1 and sys.argv[1] == 'all'
PER = int(sys.argv[1]) if len(sys.argv) > 1 and not ALL else 6
SEED = int(sys.argv[2]) if len(sys.argv) > 2 and not ALL else 1
PI, PN = map(int, sys.argv[2].split('/')) if ALL and len(sys.argv) > 2 else (0, 1)
P5 = os.path.join(HERE, '..', 'scratch', 'signals', 'p5')
unit = lambda c: c[0] >> 1
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
pat, _ = G.train([0xf, 0xb], True, 1)
WORDS = [[0], [0, 1, 2], [0, 2, 4, 6, 8]]
K0 = os.environ.get('EVENT') == 'k0'      # the review's second signal: wire cell (0,1,4) of unit -10 removed at generation 0
if K0:
    WORDS = ['K0']
L, GMAX, H = (int(v) for v in os.environ.get('LGH', '44,64,128').split(','))   # train length, generations, torus
ONLY = os.environ.get('ONLY')            # 'part:index' of one end, with EVENT/LGH, for a longer look at it
m = oracle.masks(H); valid = m[0] | m[1] | m[2]

ends = []
for part in (0, 1):
    d = json.load(open(os.path.join(P5, f'census_vec_{part}.json')))
    assert d['words'][0] == [0] and d['words'][5] == [0, 1, 2] and d['words'][7] == [0, 2, 4, 6, 8]
    for v in d['vectors']:
        e = d['ends'][v['end']]
        ends.append((part, v['end'], e, v['outcomes']))
heal = [x for x in ends if set(x[3]) == {'healed'}]
dead = [x for x in ends if set(x[3]) == {'dead'}]
print(f'{len(ends)} ends on file: {len(heal)} healed on every word, {len(dead)} dead on every word, '
      f'{len(ends) - len(heal) - len(dead)} other')
rng = random.Random(SEED)
sample = (heal + dead)[PI::PN] if ALL else rng.sample(heal, PER) + rng.sample(dead, PER)
if ONLY:
    sample = [x for x in ends if f'{x[0]}:{x[1]}' == ONLY]


def arr(cs, off):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple((c[i] + off[i]) % H for i in range(3))
        assert valid[x], (c, x)
        h[x] = True
    return h


ok = True; table = {}
for part, idx, e, outs in sample:
    KS, T = e['KS'], e['T']
    cap = frozenset(tuple(c) for c in e['cap'])
    train = G.train_cells(pat, 0, KS - L, KS, 1)
    xs = [c[0] for c in cap | train]
    assert max(xs) - min(xs) < H - 24, 'object too long for the torus'
    off = (16 - min(xs) + (min(xs) % 2), 64, 64)            # even offsets keep the cell classes
    rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in train), reverse=True)
    endzone = np.zeros((H, H, H), dtype=bool); endzone[2 * (KS - 6) + off[0]:2 * (KS + 30) + off[0]] = True
    far = np.zeros((H, H, H), dtype=bool); far[2 * (KS - 30) + off[0]:2 * (KS - 12) + off[0]] = True
    plain = [arr(cap | train, off)]
    for _ in range(GMAX):
        plain.append(oracle.step(plain[-1], m))
    stands = lambda g: np.array_equal(plain[max(g, T)][endzone], plain[max(g, T) - T][endzone])   # at max(g, T): equality at g lasts
    want = 'healed' if set(outs) == {'healed'} else 'dead'
    for wd in WORDS:
        holes = {tr((0, 1, 4), KS - 16)} if K0 else {tr((1, 0, 4), rakes[i]) for i in wd}
        assert holes <= train
        x = arr((cap | train) - holes, off)
        got, when = None, None
        for g in range(1, GMAX + 1):
            x = oracle.step(x, m)
            if np.array_equal(x, plain[g]):
                got, when = ('healed' if stands(g) else 'equal after the tail arrived'), g
                break
        if got is None:
            reach = bool((x ^ plain[GMAX])[far].any())
            got = 'dead' if (reach and stands(GMAX)) else f'differs at {GMAX} (far zone differs: {reach}, end stands: {stands(GMAX)})'
        good = got == want
        if K0:
            good = got in ('healed', 'dead'); table[(want, got)] = table.get((want, got), 0) + 1
        ok &= good
        print(f'  end {part}:{idx} ({e["src"]}, {e["cells"]} cells, period {T}) word {wd}: push {want}; oracle {got}'
              + (f' at generation {when}' if when else '') + ('' if good else '   <-- DISAGREES'), flush=True)
print(f'{len(sample)} ends x {len(WORDS)} words checked')
if K0:
    print('(push: every hole, oracle: K0) ->', sorted(table.items()), ' (PASS here means only: no third outcome)')
print('PASS' if ok else 'FAIL')
