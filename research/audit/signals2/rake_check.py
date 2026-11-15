"""The rake of wire C on the oracle (README section 10), beyond the study's cases.

    python3 rake_check.py

R1  rake alone for 40 rounds of 2 generations on a ring of 100 units: at generation 2m the state is exactly the
    wire + the rake cell at u0+m + a p< at u0+m-2, .., u0-m (the study checked m <= 10).
R2  rake against a p< started sep units ahead, sep = 3..22: claim: even sep -> eaten (state = rake alone),
    odd -> the rake stops (no rake; every 2 generations the whole state moves one unit towards -v).
R3  the mirror rake (the image of the rake, one generation on, under (x,y,z) -> (z-4, y, x+4)) against a p>
    (the study: sg only), and R4 rake against mirror rake: kymographs and the same two tests.
"""
import numpy as np
import gs, wirec as W
ok = True
R = W.Ring(100); u0 = 20
o = R.run(R.with_rake(u0), 80)
good = True
for mm in range(1, 41):
    e = R.with_rake(u0 + mm)
    for k in range(1, mm + 1):
        e = R.with_pl(u0 + mm - 2 * k, e)
    good &= o[2 * mm] == e
print('PASS' if good else 'FAIL', 'R1 rake alone, m = 1..40: wire + rake at u0+m + p< at u0+m-2, .., u0-m, exactly'); ok &= good
R = W.Ring(64); u0 = 10; T = 2 * 22 + 6
alone = R.run(R.with_rake(u0), T + 2)
res = []
for sep in range(3, 23):
    o = R.run(R.with_pl(u0 + sep, R.with_rake(u0)), T + 2)
    eaten = o[T] == alone[T]
    rigid = o[T + 2] == R.shift(o[T], -1)
    res.append((sep, 'eaten' if eaten else 'stops' if rigid else 'other'))
pred = all(r == ('eaten' if s % 2 == 0 else 'stops') for s, r in res)
print('PASS' if pred else 'FAIL', 'R2 rake vs p<, sep 3..22:', ' '.join(f'{s}:{r}' for s, r in res)); ok &= pred
# R3 mirror rake: X(1) of the rake, mirrored
R = W.Ring(64)
x1 = R.run(R.with_rake(30), 1, every=1)[1]
mr = R.key(W.MIRROR(c) for c in x1)
o = R.run(mr, 12)
print('    mirror rake alone, every 2 generations:')
for t in range(0, 13, 2):
    print('     ', R.hexrow(o[t]))
# its unit: find where it sits; test against p> started sep units behind (to its -v side)
row0 = R.hexrow(mr); um = [i for i, ch in enumerate(row0) if ch != 'b']
print('    mirror rake occupies units', um)
alone = R.run(mr, 60)
res = []
for sep in range(3, 21):
    o = R.run(R.with_pr(um[0] - sep, mr), 60)
    eaten = o[56] == alone[56]
    rigid = o[58] == R.shift(o[56], 1)
    res.append((sep, 'eaten' if eaten else 'stops' if rigid else 'other'))
print('    R3 mirror rake vs p> started sep units on its -v side:', ' '.join(f'{s}:{r}' for s, r in res))
# R4 rake vs mirror rake
R = W.Ring(80)
for sep in (10, 11, 12, 13):
    S = R.with_rake(10)
    x1 = R.run(R.with_rake(10 + sep), 1, every=1)[1]
    m2 = R.key(W.MIRROR(c) for c in x1)
    # the mirror of a rake at unit a sits at unit ~ (-a) + const; translate it to start sep units right of the rake
    r0 = R.hexrow(m2); pos = [i for i, ch in enumerate(r0) if ch != 'b'][0]
    m2 = R.shift(m2, 10 + sep - pos)
    S = frozenset((S - R.bg) | (m2 - R.bg) | (R.bg & S & m2))
    o = R.run(S, 50)
    print(f'    R4 rake at 10, mirror rake at {10 + sep}:')
    for t in range(0, 51, 4):
        print('      ', R.hexrow(o[t]))
print('ALL PASS' if ok else 'SOME FAILED')
