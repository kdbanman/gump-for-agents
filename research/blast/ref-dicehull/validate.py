#!/usr/bin/env python3
"""Validate rd.c against reference/oracle.py, state for state.

    python3 research/blast/ref-dicehull/validate.py [GENS=1200]

1. Full hull, no coins (geom WD = 99), R = 9 and 11, 4 soups each: every generation of rd.c equals the oracle's
   (the oracle runs free on a torus of side 2R + 6; outside the hull it must stay dead by T2, also checked).
2. The dice chain (WD = 6, coins fair and coins 27/64; WD = 8): every generation's rule cells equal one oracle step
   applied to the previous dumped state (rule cells + that generation's coins; nothing deeper), and the coins have
   the stated density.
3. Negative control: the same with one neighbour of one cell swapped must fail.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle
S = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'ref-dicehull'); os.makedirs(S, exist_ok=True)
GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
EXE = os.path.join(S, 'rd')
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', EXE, os.path.join(HERE, 'rd.c'), '-lm'])


def load(R, WD, swap):
    g = os.path.join(S, f'val_{R}_{WD}_{swap}.bin')
    out = subprocess.check_output([sys.executable, os.path.join(HERE, 'geom.py'), str(R), str(WD), g] + (['1'] if swap else [])).split()
    n, A, NRULE = int(out[4]), int(out[1]), int(out[2])
    raw = np.fromfile(g, np.int32); xyz = raw[3 + 12 * NRULE:].reshape(n, 3)
    return g, n, A, NRULE, xyz


def run(R, WD, swap, dpm, seed):
    g, n, A, NRULE, xyz = load(R, WD, swap)
    rng = np.random.default_rng(seed)
    init = (rng.random((4, n)) < 0.5).astype(np.uint8)
    fi, fo = os.path.join(S, 'val_init.bin'), os.path.join(S, 'val_out.bin')
    init.tofile(fi)
    subprocess.check_call([EXE, g, 'val', fi, str(GENS), fo, str(seed), str(dpm)])
    st = np.fromfile(fo, np.uint8).reshape(GENS, 4, n)
    H = 2 * R + 6; c = H // 2; m = oracle.masks(H)
    ix = (xyz[:, 0] + c, xyz[:, 1] + c, xyz[:, 2] + c)
    first_bad = None; changed = 0; outside_born = 0
    for lane in range(4):
        h = np.zeros((H, H, H), np.int8); h[ix] = init[lane]
        for t in range(GENS):
            if WD < 99:                       # one oracle step from the previous dumped state (coins included)
                h = np.zeros((H, H, H), np.int8); h[ix] = init[lane] if t == 0 else st[t - 1, lane]
            h = oracle.step(h, m)
            want = h[ix][:NRULE]
            if WD >= 99:
                outside_born += int(h.sum() - want.sum())
            if not np.array_equal(want, st[t, lane, :NRULE]):
                if first_bad is None or t < first_bad:
                    first_bad = t + 1
                break
            if t and not np.array_equal(st[t, lane, :NRULE], st[t - 1, lane, :NRULE]):
                changed += 1
    dens = st[:, :, NRULE:].mean() if NRULE < n else float('nan')
    return first_bad, changed, outside_born, dens, n, A, NRULE, st[-1, :, :A].sum(1)


ok = True
for R in (9, 11):
    fb, ch, ob, _, n, A, NRULE, pf = run(R, 99, 0, 32, 1000 + R)
    print(f'full hull R={R}: n={n} A={A}; {GENS} generations x 4 soups: first mismatch {fb}; lane-generations with a changing state {ch}; '
          f'cells born outside the hull in the oracle {ob}; face populations at the end {pf.tolist()}')
    ok &= fb is None and ob == 0
    fb, *_ = run(R, 99, 1, 32, 1000 + R)
    print(f'   negative control (one neighbour swapped): first mismatch at generation {fb}')
    ok &= fb is not None
for R, WD, dpm in ((9, 6, 32), (11, 6, 32), (11, 6, 27), (11, 8, 32), (9, 8, 27)):
    fb, ch, _, dens, n, A, NRULE, pf = run(R, WD, 0, dpm, 2000 + R + WD + dpm)
    print(f'dice chain R={R} WD={WD} dpm={dpm}/64: n={n} A={A} rule cells {NRULE} dice cells {n - NRULE}; first mismatch {fb}; '
          f'changing lane-generations {ch}; density of the coins {dens:.4f} (want {dpm / 64:.4f}); face populations at the end {pf.tolist()}')
    ok &= fb is None and abs(dens - dpm / 64) < 0.004
    fb, *_ = run(R, WD, 1, dpm, 2000 + R + WD + dpm)
    print(f'   negative control: first mismatch at generation {fb}')
    ok &= fb is not None
print('VALIDATION PASSED' if ok else 'VALIDATION FAILED')
