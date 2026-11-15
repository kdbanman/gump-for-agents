"""Positive and negative controls for the study's two SAT encodings (imports research/signals/sat_turn.py and
sat_writer.py: testing them is the point).  Run from research/signals:
    python3 ../audit/signals3/sat_controls.py        (about 1 min)
sat_turn: clock-C's capR (first unit 10, the encoding's KS) is fixed as the cap.  Our own measurement
(turn_check.py) gives c_R = 0: rake at unit 9 at t = 0 (a = -18), mirror rake at units 4,5 at T needs
T + 8 + 18 = 40, i.e. T = 14 (class k = 0).  Expect SAT at T = 14, UNSAT at T = 12, 16, 18 (the cap is fixed,
so the turn is fixed).  Also a k = 2 cap of the 5 x 5 tube (first of k2caps_16_47.json) fixed: expect SAT at
T = 16 in the 5 x 5 tube.
sat_writer: capR fixed as the writer at unit 6: SAT with word C (it writes CCCC...), UNSAT with the word
free but non-constant (a known non-writer is not mistaken for a writer), at T = 2 and T = 4."""
import json, os, sys
sys.path.insert(0, os.getcwd())
import sat_turn, sat_writer, scat
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import r3
tr = r3.tr; unit = r3.unit


def fixcap(R, pb, Zt, cap, KS):
    capset = set(cap); missing = [c for c in capset if c not in R.index]
    for i in range(R.n):
        if R.units[i] >= KS:
            pb.fix(Zt[i], R.cells[i] in capset)
    return missing


capR10 = [tr(c, 10) for c in r3.capR0]
for T in (12, 14, 16, 18):
    R, pb, Z, X, ua, u0 = sat_turn.build(T, 47, 1, 5, 10, 2)
    miss = fixcap(R, pb, Z[0], capR10, 10)
    st, m = pb.solve('cadical153', 300)
    print(f'sat_turn, capR of clock-C fixed, C=47, T={T} (class {(T + 2 * ua + 4 + 2 * u0) % 4}): {st}; cap cells outside the region: {len(miss)}', flush=True)
k2 = json.load(open(os.path.join(r3.gs.ROOT, 'research', 'scratch', 'signals', 'k2caps_16_47.json')))[7]['cap']
for T in (14, 16):
    R, pb, Z, X, ua, u0 = sat_turn.build(T, 47, -1, 7, 10, 2)
    miss = fixcap(R, pb, Z[0], [tuple(c) for c in k2], 10)
    st, m = pb.solve('cadical153', 300)
    print(f'sat_turn, k2 cap #7 fixed, 5x5 tube, T={T} (class {(T + 2 * ua + 4 + 2 * u0) % 4}): {st}; outside: {len(miss)}', flush=True)
capR6 = [tr(c, 6) for c in r3.capR0]
for T, word in ((2, 'C'), (4, 'C'), (4, None), (6, None)):
    R, pb, X, W = sat_writer.build(T, 31, 1, 5, 6, word)
    miss = fixcap(R, pb, X[0], capR6, 6)
    st, m = pb.solve('cadical153', 300)
    print(f'sat_writer, capR of clock-C fixed at unit 6, C=31, T={T}, word {word or "free, non-constant"}: {st}; outside: {len(miss)}', flush=True)
