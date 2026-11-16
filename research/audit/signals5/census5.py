"""B(i), B(ii) of REVIEW-signals-5: recount the ends of the rake train with an independent key, and check that known
ends are in the lists.  Stepper: st5.step (checked against the oracle by check_st5.py).

    python3 census5.py            (about 1 min)  writes ../../scratch/audit/signals5/ends.json

Key of an end: its orbit's minimal period p; D(t) = cells of the orbit at t (units KS - 20 .. its highest live unit) that
differ from the plain train, t = 0..p-1.  The symmetries of the train are (translate by k units, shift time by 2k); the key is the
least, over all k with the lowest unit of D'(0) in {0, 1}, of the tuple (D'(0), .., D'(p-1)), D'(t) = tau^k D(t - 2k).
"""
import json, os, sys
from st5 import step, train, unit, tr, mirror, in_tube, HERE, ROOT

P4 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p4')
P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals5')
LISTS = [os.path.join(P4, 'abs8_fb_31.json'), os.path.join(P4, 'abs4_fb_33.json'),
         os.path.join(P5, 'abs_fb_35.json'), os.path.join(P5, 'abs_fb_37.json')]


def orbit_D(cap, KS, T, far=-40):
    x = train(0, far, KS) | frozenset(cap)
    st = []
    for t in range(2 * T + 1):
        st.append(frozenset(c for c in x if unit(c) >= KS - 20)); x = step(x)
    assert st[T] == st[0] and st[2 * T] == st[0], 'not periodic'
    p = next(q for q in range(1, T + 1) if T % q == 0 and st[q] == st[0] and all(st[i + q] == st[i] for i in range(T)))
    # differences from the train on units up to the end's highest unit (train cells beyond the end do not count,
    # so that the key is covariant under translation)
    D = [st[t] ^ train(t, KS - 20, max(unit(c) for c in st[t]) + 1) for t in range(p)]
    return p, D


def key(p, D):
    best = None
    for k in range(-40, 41):
        Dp = [frozenset(tr(c, k) for c in D[(t - 2 * k) % p]) for t in range(p)]
        if not Dp[0] or min(unit(c) for c in Dp[0]) not in (0, 1):
            continue
        tup = tuple(tuple(sorted(s)) for s in Dp)
        best = tup if best is None or tup < best else best
    assert best is not None
    return (p, best)


def planes(cells):
    return max(c[0] + c[1] - c[2] for c in cells), max(c[0] - c[1] - c[2] for c in cells)


def main():
    ends = {}; entries = 0; per_list = {}
    for fn in LISTS + [os.path.join(P4, 'abs8_fb_33.json')]:
        d = json.load(open(fn)); ks = []
        for e in d['list']:
            cap = [tuple(c) for c in e['cap']]
            p, D = orbit_D(cap, d['KS'], d['T'])
            k = key(p, D); ks.append(k)
            if fn in LISTS:
                entries += 1
                ends.setdefault(k, dict(src=os.path.basename(fn), cap=cap, KS=d['KS'], p=p, C=d['C']))
        per_list[os.path.basename(fn)] = ks
        print(f'{os.path.basename(fn)}: {len(ks)} entries, {len(set(ks))} distinct keys, periods {sorted(set(k[0] for k in ks))}')
    print(f'{entries} entries in the four census lists, {len(ends)} distinct ends')
    s33_4, s33_8 = set(per_list['abs4_fb_33.json']), set(per_list['abs8_fb_33.json'])
    print('abs8_fb_33 (period dividing 8, C = 33) equals abs4_fb_33 as a set of ends:', s33_4 == s33_8)
    s31, s37 = set(per_list['abs8_fb_31.json']), set(per_list['abs_fb_37.json'])
    print('C = 31 absorber in the C = 37 list:', s31 <= s37, '; C = 33 ends all in C = 37:', s33_4 <= s37,
          '; C = 35 ends all in C = 37:', set(per_list['abs_fb_35.json']) <= s37)
    # capA of the line, mirrored to a +v end, in its absorbing cycle
    ln = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
    N = 12
    x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
        frozenset(tr(tuple(c), N) for c in ln['gun'])
    for _ in range(2 * N + 40):
        x = step(x)
    m = frozenset(mirror(c) for c in x)
    # find the train phase t and translation k with m equal to the train on a band beyond the mirrored gun
    lo_u = min(unit(c) for c in m) + 5
    found = None
    for t in range(4):
        for k in range(-3, 4):
            mm = frozenset(tr(c, k) for c in m)
            if frozenset(c for c in mm if lo_u + k <= unit(c) < lo_u + k + 6) == train(t, lo_u + k, lo_u + k + 6):
                found = (t, k, mm); break
        if found:
            break
    assert found, 'mirrored line stream is not the train'
    t, k, mm = found
    u = lo_u + k
    while frozenset(c for c in mm if unit(c) == u) == train(t, u, u + 1):
        u += 1
    KS = u - 2
    capall = frozenset(c for c in mm if unit(c) >= KS)
    # re-express at train phase 0: step forward to a generation t' = 0 mod 4 of the train
    y = train(t, KS - 60, KS) | capall
    tt = t
    while tt % 4:
        y = step(y); tt += 1
    capA_end = frozenset(c for c in y if unit(c) >= KS)
    p, D = orbit_D(sorted(capA_end), KS, 4)
    kA = key(p, D)
    allc = frozenset().union(*[frozenset(tr(c, 0) for c in s) for s in D])
    orbit_cells = set()
    z = train(0, KS - 40, KS) | capA_end
    for _ in range(4):
        orbit_cells |= {c for c in z if unit(c) >= KS - 2}; z = step(z)
    print(f'capA mirrored, in its absorbing cycle: period {p}; orbit inside the 3x3 tube: '
          f'{all(in_tube(c) for c in orbit_cells)}; planes (max x+y-z, max x-y-z) over the orbit: {planes({tr(c, 6 - KS) for c in orbit_cells})} (moved to KS = 6);'
          f' in the census: {kA in ends}')
    json.dump(dict(ends=[dict(v, key_period=k[0]) for k, v in ends.items()], capA=dict(cap=sorted(capA_end), KS=KS, in_census=kA in ends)),
              open(os.path.join(OUT, 'ends.json'), 'w'))


if __name__ == '__main__':
    main()
