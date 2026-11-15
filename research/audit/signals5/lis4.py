"""C of REVIEW-signals-5: the four runs that gapstream.py labelled 'LISTENER?' (gapstream_end.jsonl), on the oracle
alone.  python3 lis4.py   (about 5 min)

Each run from its generation 0 (line N = 12 at generation 2N + 8 of its own run, + the oscillator S) with
reference/oracle.py on an even box torus with 16 cells of padding (checked: no live cell comes within 4 of the box
edge), plain and with the hole removed at generation tg.  Reported:
the generation from which the plain run's wire units 2..11 hold no live cell in the line's tube; final period and
population of both runs; whether the oscillator is a phase of its free orbit at the end in both; whether the two
final cycles are equal up to a time shift; and whether any wire cell (line tube, units 2..11) is live in either
final cycle (a gun with rakes on the wire would need some)."""
import json, os
from st5 import step, unit, tr, oracle_run, ROOT

P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
ln = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
N = 12
x0 = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ln['gun'])
tube = lambda c: 1 <= c[0] + c[1] + c[2] <= 7 and 1 <= c[0] - c[1] + c[2] <= 7
recs = [json.loads(l) for l in open(os.path.join(P5, 'gapstream_end.jsonl'))]
recs = [r for r in recs if r['verdict'] == 'LISTENER?' and r['gap_gun']]
print(len(recs), 'records')
G = 1000; PAD = 16
for r in recs:
    S = frozenset(tuple(c) for c in r['cells'])
    orb = [S]
    for _ in range(r['P'] - 1):
        orb.append(step(orb[-1]))
    sup = frozenset().union(*orb)
    start = x0 | S                      # the oscillator is placed at generation 2N + 8 of the line
    out = {}
    for name in ('plain', 'gap'):
        hist = []; empty_from = None
        it = None
        # generation 0 of the record = line at 2N+8 with S; the line part is stepped by the oracle too
        pre = x0
        for t, s in oracle_run(x0, 2 * N + 8, pad=PAD):
            pre = s
        cur = pre | S
        for t, s in oracle_run(cur, r['tg'], pad=PAD):
            cur = s
        if name == 'gap':
            assert tuple(r['hole']) in cur
            cur = cur - {tuple(r['hole'])}
        bb = [(min(c[i] for c in cur) - PAD + 4, max(c[i] for c in cur) + PAD - 4) for i in range(3)]
        for t, s in oracle_run(cur, G, pad=PAD):
            assert all(bb[i][0] <= c[i] <= bb[i][1] for c in s for i in range(3)), 'near the box edge'
            if t >= G - 200:
                hist.append(s)
            w = [c for c in s if tube(c) and 2 <= unit(c) <= 11]
            if w:
                empty_from = None
            elif empty_from is None:
                empty_from = t + r['tg']
        last = hist[-1]
        per = next(p for p in range(1, 101) if hist[-1 - p] == last)
        cyc = hist[-per:]
        osc_ok = all(any((s & sup) == o for o in orb) for s in cyc)
        wire = any(c for s in cyc for c in s if tube(c) and 2 <= unit(c) <= 11)
        out[name] = (per, len(last), osc_ok, wire, empty_from, cyc)
    same = any(out['plain'][5][0] == s for s in out['gap'][5])
    print(f"{r['osc']} gap {r['gap_k']} at generation {r['tg']}:")
    for name in ('plain', 'gap'):
        per, pop, ok, wire, ef, _ = out[name]
        print(f'   {name:5s}: final period {per}, population {pop}, oscillator a free-orbit phase: {ok}, '
              f'live wire cells on units 2..11 in the final cycle: {wire}, wire units 2..11 empty from generation {ef}')
    print(f'   final cycles equal up to a time shift: {same}')


# Added: is the gapped run's final cycle the working line (line-C N = 12 in its own period-4 cycle) with the
# oscillator beside it?  Oracle only.
*_, (t_, L0) = oracle_run(x0, 2 * N + 40, pad=PAD)
Lc = [s for t, s in oracle_run(L0, 3, pad=PAD)]
for r in recs:
    S = frozenset(tuple(c) for c in r['cells'])
    orb = [S]
    for _ in range(r['P'] - 1):
        orb.append(step(orb[-1]))
    sup = frozenset().union(*orb)
    *_, (t_, pre) = oracle_run(x0, 2 * N + 8, pad=PAD)
    *_, (t_, cur) = oracle_run(pre | S, r['tg'], pad=PAD)
    cur = cur - {tuple(r['hole'])}
    *_, (t_, fin) = oracle_run(cur, G, pad=PAD)
    cyc = [s for t, s in oracle_run(fin, 20, pad=PAD)]
    ok = all(any(frozenset(c for c in s if c not in sup) == frozenset(c for c in l if c not in sup) for l in Lc) and
             any((s & sup) == o for o in orb) for s in cyc)
    print(f"{r['osc']} gap {r['gap_k']}: gapped run's final cycle = the working line (period-4 cycle of line-C N = 12, "
          f"outside the oscillator's support) + the oscillator in its free orbit, at every generation of 20: {ok}")
