#!/usr/bin/env python3
"""Do the three pipelines' soups have the same early hazard? The face-death hazard in the first generations depends only
on the soup's distribution; the late (quasi-stationary) hazard does not depend on it at all.

  gpu     the GPU's soup_bit (research/gpu/kernel.cuh: mix64(mix64(mix64(seed) + r) + i) < p 2^64, i the node's
          position in kernel B's layout, gsim.shared_layout's perm), seeds as eqtorus.run draws them
          ((48002 << 32) + round), stepped by t4.c (-init);
  t4      t4.c's own hash, from the production records (lives of age <= 60);
  rep     research/peeling/rep.c's xoshiro soups AND its stepper, K = 1 (exact last-alive times), cap 64, through
          research/peeling/geom.Vessel.run on research/shape/tslab's 4x4 vessel (their code, only read).
    python3 research/audit/gpu_local_pr23/soups.py gpu ROUNDS      # 2560 soups per round
    python3 research/audit/gpu_local_pr23/soups.py rep JOBS        # 4096 soups per job, seeds 777000 + j
"""
import math, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_pr23')
sys.path.insert(0, HERE)
import geom4  # noqa: E402

C1, C2, C3 = np.uint64(0x9E3779B97F4A7C15), np.uint64(0xBF58476D1CE4E5B9), np.uint64(0x94D049BB133111EB)


def mix64(z):
    z = z + C1
    z = (z ^ (z >> np.uint64(30))) * C2
    z = (z ^ (z >> np.uint64(27))) * C3
    return z ^ (z >> np.uint64(31))


def gpu_soups(seed, R, p=0.4):
    pos = np.array(geom4.CELLS)
    a = np.argmax(pos % 2, axis=1)
    perm = np.lexsort((pos[:, 2], pos[:, 1], pos[:, 0], a))          # kernel-B position i holds node perm[i]
    thr = np.uint64(min(int(p * 2.0 ** 64), 2 ** 64 - 1))
    with np.errstate(over='ignore'):
        h = mix64(mix64(np.uint64(seed)) + np.arange(R, dtype=np.uint64))
        bits_pos = mix64(h[:, None] + np.arange(len(pos), dtype=np.uint64)[None, :]) < thr
    out = np.empty_like(bits_pos); out[:, perm] = bits_pos
    return out


def early(age, kind, lives, cut=60):
    d = int(((kind == 1) & (age <= cut)).sum())
    ex = np.minimum(age, cut).sum() + cut * (lives - len(age)) if lives > len(age) else np.minimum(age, cut).sum()
    return d, ex


if __name__ == '__main__':
    what, k = sys.argv[1], int(sys.argv[2])
    if what == 'gpu':
        g = os.path.join(SCR, 'g44.bin'); geom4.write(g)
        D = EX = L = 0
        for rnd in range(1, k + 1):
            s = gpu_soups((48002 << 32) + rnd, 2560)
            st = os.path.join(SCR, 'gpu_soups.u8'); s.astype(np.uint8).tofile(st)
            out = os.path.join(SCR, 'gpu_soups_ev.bin')
            subprocess.run([os.path.join(SCR, 't4'), g, '40', '0', '60', '-init', st, out], check=True, capture_output=True)
            r = np.fromfile(out, np.int64).reshape(-1, 4)
            ex = np.where(r[:, 1] > 0, r[:, 0], 60).sum()
            D += int((r[:, 1] == 1).sum()); EX += int(ex); L += len(s)
        print(f'gpu soups: {L} lives, face deaths by age 60: {D}, hazard {1e5 * D / EX:.2f} +- {1e5 * math.sqrt(D) / EX:.2f} '
              f'x1e-5, deaths per life {D / L:.5f}')
    elif what == 'rep':
        sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
        import tslab
        v = tslab.tslab(4, 0, 4)
        keys = [key for key, _ in v.layers]
        f0, f1 = keys.index((0, 1)), keys.index((0, 15))
        D = EX = L = 0
        for j in range(k):
            st, pop, la = v.run(64, 0.4, 777000 + j, 60, 1)
            ge = v.gen_end
            dt = []
            for c in (f0, f1):
                x = (la[:, c] + 1).astype(float); x[la[:, c] >= ge] = np.inf; dt.append(x)
            face = np.minimum(*dt)
            dead = np.isfinite(face) & (face <= 60)
            D += int(dead.sum()); EX += float(np.where(dead, face, 60).sum()); L += len(face)
        print(f'rep.c soups and stepper (K = 1): {L} lives, face deaths by age 60: {D}, hazard '
              f'{1e5 * D / EX:.2f} +- {1e5 * math.sqrt(D) / EX:.2f} x1e-5, deaths per life {D / L:.5f}')
