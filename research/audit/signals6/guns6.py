"""D of REVIEW-signals-6: the 68 guns of research/scratch/signals/p6/guns_5f_37.json, deduplicated (translation and
time shift), and each run against the up-moving signals E, U, N1 with st6.Batch (3x3 tube, planes C <= 37).

    python3 guns6.py            (~1 min)

Each gun (its cells 'cap' of units >= KS = 6) is set at the end of the train T.train(phi + t) on units < KS, phi
found by search (the orbit must be periodic with period dividing 4 and leave units < KS as the train).  Key: the
orbit translated so that its lowest unit differing from the train is 0, re-indexed so that generation t has train
phase t; the four states on units >= -1.  The signal is put at train phase 1 at unit -30 or -31 (its parity) and the
run is compared with the undisturbed run for G = 160 generations (exact: the piece is units -300..14):
  healed    equal on the whole state at some t <= G, and still equal at G;
  returned  at G the units >= -12 equal the undisturbed run and the difference is a set of rigid known signals;
  dead      otherwise.
"""
import json, os, time
from collections import Counter, defaultdict
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import kinds6, sig6

KS, C = 6, 37
UA = -300
FN = os.path.join(st6.ROOT, 'research', 'scratch', 'signals', 'p6', 'guns_5f_37.json')


def phase_of(cap):
    for phi in range(4):
        x = T.train(phi, -60, KS) | cap
        st = [x]
        for t in range(12):
            x = st6.step(x); st.append(x)
        if all(units(st[t], -40, KS) == units(T.train(phi + t, -60, KS), -40, KS) for t in range(12)) and \
           all(units(st[t + 4], -40, 99) == units(st[t], -40, 99) for t in range(8)):
            return phi, st
    return None, None


def key(st, phi):
    # aligned orbit O(t), t = 0..3, train phase t: O(t) = st[(t - phi) % 4 + 4] (st index s has phase phi + s)
    O = [st[((t - phi) % 4) + 4] for t in range(4)]
    m = min(unit_of(c) for t in range(4) for c in units(O[t], -40, 99) ^ units(T.train(t, -40, 99), -40, 99))
    # translate by -m: phase shifts by +2m; re-index t' = t + 2m
    O2 = [None] * 4
    for t in range(4):
        O2[(t + 2 * m) % 4] = trs(units(O[t], m - 1, 99), -m)
    return tuple(tuple(sorted(s)) for s in O2), m


def main():
    t0 = time.time()
    d = json.load(open(FN))
    assert d['pattern'] == '5f' and d['KS'] == KS and d['C'] == C
    caps = [frozenset(tuple(c) for c in e['cap']) for e in d['list']]
    keys = []; phis = []
    for cap in caps:
        phi, st = phase_of(cap)
        assert phi is not None
        k, m = key(st, phi)
        keys.append(k); phis.append(phi)
    groups = defaultdict(list)
    for i, k in enumerate(keys):
        groups[k].append(i)
    print(f'{len(caps)} entries, {len(groups)} distinct guns up to translation and time shift; '
          f'classes of more than one: {[g for g in groups.values() if len(g) > 1]}')
    cells = [c for u in range(UA, 16) for c in kinds6.tube3(u) if c[0] + c[1] - c[2] <= C and c[0] - c[1] - c[2] <= C]
    B = st6.Batch(cells)
    G = 160
    res = {}
    for kind, u in (('E', -30), ('U', -31), ('N1', -30)):
        S = np.zeros((2 * len(caps), B.n + 1), np.uint8)
        start = []
        for i, cap in enumerate(caps):
            x = T.train(phis[i], UA, KS) | cap
            S[2 * i] = B.vec(x)
            start.append((1 - phis[i]) % 4)          # generation at which the train has phase 1
        eqt = [None] * len(caps)
        for t in range(G + 1):
            for i in range(len(caps)):
                if t == start[i]:
                    assert units(B.set_of(S[2 * i]), -60, -20) == T.train(1, -60, -20)
                    S[2 * i + 1] = S[2 * i] ^ B.vec(sig6.sig(kind, u))
                elif t < start[i]:
                    S[2 * i + 1] = S[2 * i]
            if t > 4:
                eq = (S[0::2] == S[1::2]).all(axis=1)
                for i in np.nonzero(eq)[0]:
                    eqt[i] = eqt[i] if eqt[i] is not None else t
            if t < G:
                S = B.step(S)
        out = []
        for i in range(len(caps)):
            dd = B.set_of(S[2 * i] ^ S[2 * i + 1])
            assert all(unit_of(c) > UA + G + 1 for c in dd)
            if not dd:
                out.append(('healed', eqt[i]))
            elif not units(dd, -12, 99):
                out.append(('returned?', len(dd)))
            else:
                out.append(('dead', len(units(dd, -12, 99))))
        res[kind] = out
        print(f'{kind}: {Counter(o[0] for o in out)}; healed entries: {[i for i, o in enumerate(out) if o[0] == "healed"]}; '
              f'distinct guns healed: {len(set(keys[i] for i, o in enumerate(out) if o[0] == "healed"))}; '
              f'returned?: {[(i, o) for i, o in enumerate(out) if o[0] == "returned?"]}  ({time.time() - t0:.0f} s)', flush=True)
    # consistency: entries with the same key behave the same
    for kind in res:
        for g in groups.values():
            assert len(set(res[kind][i][0] for i in g)) == 1, (kind, g)
    sizes = {i: len(caps[i]) for i in range(len(caps))}
    json.dump(dict(groups=list(groups.values()), res=res, phis=phis), open(os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals6', 'guns6.json'), 'w'))


if __name__ == '__main__':
    main()
