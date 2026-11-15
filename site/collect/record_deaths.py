#!/usr/bin/env python3
"""Record a few real face deaths for the overview's plate "How a face dies, watched".   python3 site/collect/record_deaths.py

What it does (about a minute, one core):
  1. writes the orbit graphs of the dying-face study's vessels oct_11_c_c1 (no symmetry: the free face) and
     oct_11_c_d2h (three mirrors: every edge of a face tied to its mirror image) with the study's own geometry
     (research/theory/symmetric/geom.py, through research/dying/load.py);
  2. compiles the study's stepper research/dying/sd.c (unchanged) into research/scratch/overview/deaths/ and runs it
     with fresh seeds (soup 0.4, checks every 4 generations, lives older than 512 generations, the first K deaths of
     each run dumped with the 128 generations before the check: not chosen, simply the first ones);
  3. for each dumped death finds the dying face and the generation of death exactly as research/dying/load.py does
     (the face is empty at lag 0 and was not empty one generation earlier), and keeps the face's 63 cells in the
     study's canonical frame for the last T generations (lag T-1 .. 0; lag 0 is the first empty generation);
  4. checks every recorded life against reference/oracle.py: the whole vessel (all cells of the full system, the
     orbit state expanded) is put in a padded box at the oldest recorded generation and stepped by the oracle, and
     at every generation the oracle's state must equal the recorded one, cell for cell, and nothing may live outside
     the vessel;
  5. writes site/collect/sources/deaths.json: the canonical cells, the tied edges, and per life the packed frames
     (base64, T x 63 bits, cell i of frame t in bit (t*63+i) of a little-endian bit string) with where it came from.
"""
import base64, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'dying'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import load                      # the study's geometry and canonical frame (read only)
import geom                      # research/theory/symmetric/geom.py, put on the path by load
import oracle                    # the numpy ground truth

SCR = os.path.join(ROOT, 'research', 'scratch', 'overview', 'deaths')
T = 80                           # frames kept per life
HIST = 128                       # generations dumped per death (>= T + CHK)
K = 4                            # deaths per group
RUNS = {'c1': (20261115, 8000), 'd2h': (20261116, 4000)}   # fresh seeds (the study used 1 and 2), generations


def run(group, seed, gens):
    q, canon, fidx, reps, face_orbit = load.geometry(group)
    g = os.path.join(SCR, f'graph_{group}.txt'); geom.write_graph(q, g)
    pre = os.path.join(SCR, f'{group}_s{seed}')
    cmd = [os.path.join(SCR, 'sd'), g, 'run', str(seed), '0.4', str(gens), '4', pre + '_lives.bin', pre + '_dump.bin',
           pre + '_null.bin', str(K), str(HIST), '512']
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    nb = (q.n + 7) // 8; rec = 20 + HIST * nb
    raw = np.fromfile(pre + '_dump.bin', dtype=np.uint8).reshape(-1, rec)
    hdr = raw[:, :20].copy().view(np.int32)
    hist = np.unpackbits(raw[:, 20:].reshape(len(raw), HIST, nb), axis=2, bitorder='little')[:, :, :q.n].astype(bool)
    assert len(hdr) == K, (group, len(hdr), out.stderr)
    nodes = [np.unique(q.orb[fidx[s]]) for s in reps]
    lives = []
    for d in range(K):
        h = hist[d]                                                      # h[j] = state j generations before the check
        empty = np.array([[not h[j][nd].any() for nd in nodes] for j in range(HIST)])
        anyempty = empty.any(1)
        assert anyempty[0], 'no empty face at the check'
        jd = int(np.argmin(anyempty)) - 1                                # last j with a face empty, contiguous from 0
        assert 0 <= jd < 4 and not empty[jd + 1].any()
        orbs = np.nonzero(empty[jd])[0]
        assert len(orbs) == 1, 'two faces died together; not recorded'
        s = reps[orbs[0]]
        fr = h[jd:jd + T][::-1][:, q.orb[fidx[s]]]                       # frame t = lag T-1-t; canonical cell order
        assert not fr[-1].any() and fr[-2].any()
        check_oracle(q, h, jd)
        bits = np.packbits(fr.reshape(-1), bitorder='little').tobytes()
        lives.append({'frames': base64.b64encode(bits).decode(), 'seed': seed, 'replica': int(hdr[d, 1]),
                      'age': int(hdr[d, 2]) * 4 - jd, 'death_gen': int(hdr[d, 4]) - jd, 'face': list(map(int, s))})
        print(f'{group} life {d}: replica {hdr[d,1]}, dies at age {lives[-1]["age"]} (run generation {lives[-1]["death_gen"]}), '
              f'face {s}, population {T - 1} generations before: {int(fr[0].sum())}; oracle agrees on {T - 1} steps', flush=True)
    return q, canon, lives


def check_oracle(q, h, jd):
    """Step the full vessel with the oracle from the oldest kept generation to the death, comparing every generation."""
    f = q.f; PAD = 14; HB = 2 * PAD + 2                                  # even shift keeps parity; HB even: a proper torus
    m = oracle.masks(HB); idx = tuple((f.cells + PAD).T)
    assert f.cells.min() + PAD >= 2 and f.cells.max() + PAD <= HB - 3
    def box(state):
        b = np.zeros((HB, HB, HB), np.int8); b[idx] = state[q.orb]; return b
    j0 = jd + T - 1
    b = box(h[j0])
    for j in range(j0 - 1, jd - 1, -1):
        b = oracle.step(b, m)
        want = box(h[j])
        assert (b == want).all(), f'oracle differs {j0 - j} generations in'


def main():
    os.makedirs(SCR, exist_ok=True)
    subprocess.run(['gcc', '-O3', '-march=native', '-o', os.path.join(SCR, 'sd'), os.path.join(ROOT, 'research', 'dying', 'sd.c')], check=True)
    out = {'how': 'python3 site/collect/record_deaths.py (research/dying/sd.c, fresh seeds; every frame checked against reference/oracle.py)',
           'T': T, 'groups': {}}
    for group, (seed, gens) in RUNS.items():
        q, canon, lives = run(group, seed, gens)
        out['canon'] = canon.tolist()                                    # the same 63 cells, same order, for both groups
        out['groups'][group] = {'tied': list(load.TIED[group]), 'graph': f'oct_11_c_{group}', 'orbit_nodes': int(q.n), 'lives': lives}
    p = os.path.join(HERE, 'sources', 'deaths.json')
    with open(p, 'w') as fh:
        json.dump(out, fh, separators=(',', ':'))
    print('wrote', p, os.path.getsize(p), 'bytes')


if __name__ == '__main__':
    main()
