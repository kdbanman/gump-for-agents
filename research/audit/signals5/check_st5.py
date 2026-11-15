"""Check st5's steppers against reference/oracle.py on the cases REVIEW-signals-5 uses them for.

    python3 check_st5.py [n_ends]      (default 8; about 3 min)

(1) The train formula st5.train is an orbit: a finite piece (units -40..40) stepped by the oracle equals the
    formula on units -20..20 for 8 generations.
(2) st5.step (sparse) equals the oracle cell for cell on a finite train + end + event, every generation.
(3) st5.Tube (batch, refilled boundary U0 = -30) equals the oracle on all units >= -20, every generation to 140
    (the finite piece starts at unit -100; its far end does not reach unit -20 by then), for n ends from the census
    (half from those that heal, half from those that die), each with three events: the hole of word [0], a removal
    of a subset of a unit at an odd generation, and a one-cell addition.
"""
import json, os, random, sys
import numpy as np
from st5 import *

P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
n_ends = int(sys.argv[1]) if len(sys.argv) > 1 else 8

# (1)
x = train(0, -40, 41)
for t, s in oracle_run(x, 8):
    assert frozenset(c for c in s if -20 <= unit(c) <= 20) == train(t, -20, 21), ('train formula', t)
print('(1) train formula = oracle on units -20..20, generations 0..8: OK')

vec = []
for part in (0, 1):
    d = json.load(open(os.path.join(P5, f'census_vec_{part}.json')))
    for v in d['vectors']:
        vec.append((d['ends'][v['end']], v['outcomes'][0]))
rng = random.Random(5)
heal = [e for e, o in vec if o == 'healed']; dead = [e for e, o in vec if o == 'dead']
sample = rng.sample(heal, n_ends // 2) + rng.sample(dead, n_ends - n_ends // 2)
TB = Tube(-30, 39); G = 140; bad = 0; nb_hit = 0; ncmp = 0
for j, e in enumerate(sample):
    KS = e['KS']; cap = frozenset(tuple(c) for c in e['cap'])
    events = [(0, frozenset([tr((1, 0, 4), 4)]), frozenset()),                     # word [0] at generation 0
              (1, frozenset([tr((0, 0, 5), -6), tr((0, 1, 2), -6)]), frozenset()),   # removal at generation 1
              (1, frozenset(), frozenset([tr((0, 2, 3), -5)]))]                      # addition at generation 1
    for (g0, rem, add) in events:
        x0 = train(0, -100, KS) | cap
        if g0:
            x0 = step(x0)
        assert rem <= x0 and not (add & x0)
        x0 = (x0 - rem) | add
        S = np.array([TB.vec(c for c in x0 if unit(c) >= -31)])
        sp = x0
        for t, s in oracle_run(x0, G):
            w = frozenset(c for c in s if unit(c) >= -20)
            mine = frozenset(c for c in TB.cells_of(S[0]) if unit(c) >= -20)
            if j < 2:
                assert frozenset(c for c in sp if unit(c) >= -20) == w, ('sparse', j, t)
                sp = step(sp)
            if not TB.boundary_plain(S, g0 + t)[0]:
                nb_hit += 1; break                          # the disturbance reached the refilled boundary: stop
            if mine != w:
                bad += 1; print('MISMATCH', j, g0, t); break
            ncmp += 1
            S = TB.step(S, g0 + t)
    print(f'  end {j} ({len(cap)} cells, {"heals" if j < n_ends // 2 else "dies"} on word [0]): 3 events x {G} generations', flush=True)
print(f'(2) sparse st5.step = oracle (2 ends x 3 events x {G} generations, whole state on units >= -20): OK')
print(f'(3) st5.Tube = oracle on units >= -20: {"OK" if not bad else str(bad) + " MISMATCHES"} ({n_ends} ends x 3 events, {ncmp} generations compared; {nb_hit} runs stopped early because the disturbance reached unit -30)')
