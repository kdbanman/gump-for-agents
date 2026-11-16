"""D of REVIEW-signals-6: mutation tests on the push's own instance (research/signals/sat_gun_echo.py, unchanged,
imported and run with sys.argv; CaDiCaL 1.5.3 as the push), models re-stepped with st6.

    python3 pushsat6.py U37      the push's U instance at C = 37 (SAT expected); the model's A re-stepped with st6:
                                 a period-4 gun that absorbs U (whole state equal to the undisturbed run)
(A 'blank signal' plant was tried and cannot be built: sat_gun_echo.histories needs a non-empty signal.)
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SIG = os.path.normpath(os.path.join(HERE, '..', '..', 'signals'))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'scratch', 'audit', 'signals6'))
mode = sys.argv[1]
sys.path.insert(0, SIG)
os.chdir(SIG)
import echo6
import sat_gun_echo
fn = os.path.join(OUT, f'pushsat_{mode}.json')
C = mode[-2:]
kind = 'U' if mode.startswith('U') else 'E'
sys.argv = ['sat_gun_echo.py', C, '--kind', kind, '--out', fn]
t0 = time.time()
sat_gun_echo.main()
print(f'push instance done in {time.time() - t0:.0f} s')
sys.path.insert(0, HERE)
os.chdir(HERE)
if os.path.exists(fn) and mode.startswith('U'):
    import st6, trains6 as T, guns6, sig6, kinds6
    from st6 import units
    d = json.load(open(fn))
    cap = frozenset(tuple(c) for c in d['A'])
    phi, st = guns6.phase_of(cap)
    print('model A: period-4 gun at the end of the train (st6):', phi is not None)
    x = T.train(phi, -300, 6) | cap
    t = 0
    while (phi + t) % 4 != 1:
        x = st6.step(x); t += 1
    y = x ^ sig6.sig('U', -31)
    eq = None
    for g in range(160):
        x = st6.step(x); y = st6.step(y)
        if eq is None and x == y:
            eq = g + 1
    print(f'model A hit by U (st6, U at unit -31): equal to the undisturbed run from generation {eq} on; equal at 160: {x == y}')
