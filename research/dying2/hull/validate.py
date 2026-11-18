#!/usr/bin/env python3
"""hd.c's production step against the Rust engine, every generation, on the hull vessel; and hd.c's face counter
against numpy on every lane and generation. With two negative controls.

  python -u research/dying2/hull/validate.py R GENS SEED     # e.g. 11 2000 7; prints VALIDATE OK / FAILED

1. `hd trace`: 256 lanes of fresh 0.35 soups (hd.c's own soup code), GENS generations, every state written.
2. Lanes 0, 63, 64, 130, 255: the initial cell set to `gump run --cells F --gens GENS --no-halt --trace` (open
   space: the hull is exact by AUTOMATON.md T2); the cell set must be equal at every generation 1..GENS.
3. The face counts written by hd.c (the bit-sliced counter of production) must equal numpy's popcount of each of the
   8 face groups, every lane, every generation.
Negative controls (must FAIL): (a) hd's state at t against the engine's at t + 1; (b) the engine started from lane
0's soup with one node of the face layer flipped, against hd's lane 0.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying2-hull')
EXE = os.path.join(SCR, 'hd.exe')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump.exe')
W, LANES, NF = 4, 256, 8


def unpack(words, n):
    """n*W u64 node-major -> (LANES, n) bool"""
    b = np.unpackbits(words.reshape(n, W).view(np.uint8), axis=1, bitorder='little')   # (n, 256)
    return b.T.astype(bool)


def engine_trace(cells, gens, tag):
    cf, tr = os.path.join(SCR, f'vcells_{tag}.txt'), os.path.join(SCR, f'vtrace_{tag}.txt')
    open(cf, 'w').write('\n'.join(' '.join(map(str, p)) for p in cells) + '\n')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--gens', str(gens), '--no-halt', '--trace', tr], check=True, capture_output=True)
    out = []
    with open(tr) as f:
        for line in f:
            parts = line.split()[1:]
            out.append({tuple(map(int, s.split(','))) for s in parts})
    os.remove(cf); os.remove(tr)
    return out


def main(R, gens, seed):
    g = np.load(os.path.join(SCR, f'hv_{R}.npz'))
    cells, fn, face_pos = g['cells'], g['fn'], g['face_pos']
    n = len(cells)
    out = os.path.join(SCR, f'vtrace_hd_{R}.bin')
    subprocess.run([EXE, 'trace', os.path.join(SCR, f'hv_{R}.bin'), str(seed), out, str(gens)], check=True)
    raw = np.fromfile(out, np.uint8)
    sw = n * W * 8
    states = [unpack(raw[i * sw:(i + 1) * sw].view(np.uint64), n) for i in range(gens + 1)]
    cnt = raw[(gens + 1) * sw:].reshape(gens, NF, LANES)
    os.remove(out)
    ok = True
    # 3. counts
    bad = 0
    for t in range(gens):
        st = states[t + 1][:, fn]                                   # (LANES, nfn)
        want = np.stack([st[:, face_pos[f]].sum(1) for f in range(NF)])
        bad += int((want != cnt[t]).sum())
    print(f'face counter: {gens} gens x 256 lanes x 8 faces: {"all equal" if bad == 0 else f"{bad} MISMATCHES"}', flush=True)
    ok &= bad == 0
    # 2. engine
    for lane in (0, 63, 64, 130, 255):
        c0 = cells[states[0][lane]]
        eng = engine_trace(c0, gens, f'{R}_{lane}')
        assert eng[0] == set(map(tuple, c0))
        mism = [t for t in range(1, gens + 1) if set(map(tuple, cells[states[t][lane]])) != eng[t]]
        pops = [len(eng[t]) for t in (0, gens // 2, gens)]
        print(f'lane {lane:3d}: engine every generation 1..{gens}: {"all equal" if not mism else f"{len(mism)} MISMATCHES, first {mism[0]}"} '
              f'(population {pops})', flush=True)
        ok &= not mism
        if lane == 0:
            shift = sum(set(map(tuple, cells[states[t][lane]])) != eng[t + 1] for t in range(1, gens))
            print(f'  negative control (a), against the engine one generation later: {shift} of {gens - 1} generations differ', flush=True)
            ok &= shift > 0
            fl = states[0][lane].copy(); fl[fn[len(fn) // 2]] ^= True
            engf = engine_trace(cells[fl], gens, f'{R}_flip')
            dif = sum(set(map(tuple, cells[states[t][lane]])) != engf[t] for t in range(1, gens + 1))
            print(f'  negative control (b), engine from a state with one face node flipped: {dif} of {gens} generations differ', flush=True)
            ok &= dif > 0
    print('VALIDATE OK' if ok else 'VALIDATE FAILED', f'R = {R}, gens {gens}, seed {seed}')
    return ok


if __name__ == '__main__':
    sys.exit(0 if main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) else 1)
