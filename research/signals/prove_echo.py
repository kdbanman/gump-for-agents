#!/usr/bin/env python3
"""The echo (and the three other signals of the plain rake train that one flipped cell makes) ride the train for ever: an exact
two-generation computation on the infinite lattice (sg.step_set; checked against the oracle by check_stepper.py).

For each signal kind K with difference set sig(K, u) at train phase 1:
    S(0) = train(1) XOR sig(K, 0)  on units -A..A,  stepped twice;
    on units -A+3 .. A-3 (where a finite piece is exact: one unit per generation) S(2) must equal
    train(3) XOR sig(K, 0) moved by DIR[K] units (and train(3) = train(1) moved by -1 unit).
Since train(3) moved by +1 is train(1) (echo6.check_train), S(2) moved by -DIR... is again of the form
train(1) XOR sig(K, u'), so by induction S(2j) = train(2j+1) XOR sig(K, DIR*j) for every j >= 0 on the infinite
train: each signal rides the train for ever, rigidly, one unit per 2 generations.  Also prints the odd-phase cells.

    python3 prove_echo.py        (1 s)
"""
import echo6 as E

E.check_train()
A = 30
ok = True
for K in ('E', 'H', 'K0', 'U'):
    u = E.SIG1[K][0]
    S0 = E.train(1, -A, A) ^ E.sig(K, u)
    S1 = E.run(S0, 1); S2 = E.run(S1, 1)
    want = E.units(E.train(3, -A, A) ^ E.trs(E.sig(K, u), E.DIR[K]), -A + 3, A - 3)
    good = E.units(S2, -A + 3, A - 3) == want
    d1 = E.units(S1, -A + 3, A - 3) ^ E.train(2, -A + 3, A - 3)
    u1 = min(E.unit_of(c) for c in d1)
    print(f"{K}: phase 1 lowest unit {u}: {sorted(E.SIG1[K][1])}; phase 2 (one generation on): lowest unit {u1}: "
          f"{sorted(E.tr(c, -u1) for c in d1)}; two generations on: moved {E.DIR[K]:+d} unit: {good}")
    ok &= good
print('PASS' if ok else 'FAIL')
