#!/usr/bin/env python3
"""How the thin face dies, from the review's own death profiles (tt.c -P): for each face death, the face's cells over
the 32 generations before it (the last is the empty one).

    python3 research/audit/thin/prof.py TAG b wall

Per lag k (generations before the empty generation): mean population; mean number of occupied sites; mean span of
the live region (ring: b minus the longest circular empty run; segment: first to last occupied site); mean number of
islands (runs of occupied sites separated by >= 2 empty sites); and, measured from the site of the last live cell(s)
(k = 1), the mean extent of the live region to its left and to its right (along the shortest way, within the
island that contains or is nearest the last site).
"""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tt  # noqa: E402


def decode(h, ncell):
    bits = []
    for ch in h:
        v = int(ch, 16)
        for t in range(4):
            bits.append((v >> t) & 1)
    return bits[:ncell]


def main(tag, b, wall):
    sites = list(range(wall, b))
    ncell = 3 * len(sites)
    files = sorted(glob.glob(os.path.join(tt.OUT, tag, 'p*.txt')))
    K = 31
    pop = np.zeros(K + 1); occ = np.zeros(K + 1); span = np.zeros(K + 1); isl = np.zeros(K + 1)
    left = np.zeros(K + 1); right = np.zeros(K + 1); nd = 0
    lastn = {}
    for fn in files:
        for line in open(fn):
            p = line.split()
            gens = p[2:]
            if len(gens) != 32 or set(gens[-1]) != {'0'}:
                continue                     # a line still being written
            nd += 1
            occs = []
            for k in range(1, K + 1):
                bits = decode(gens[-1 - k], ncell)
                o = [any(bits[3 * j:3 * j + 3]) for j in range(len(sites))]
                pop[k] += sum(bits); occs.append(o)
            o1 = occs[0]; idx1 = [j for j, x in enumerate(o1) if x]
            lastn[len(idx1)] = lastn.get(len(idx1), 0) + 1
            for k in range(1, K + 1):
                o = occs[k - 1]; S = len(o); occ[k] += sum(o)
                if wall == 0:
                    # longest circular empty run
                    if not any(o):
                        continue
                    run = best = 0
                    for x in o + o:
                        run = run + 1 if not x else 0; best = max(best, min(run, S))
                    span[k] += S - best
                    # islands: circular runs of occupied separated by >= 2 empties
                    s0 = next(j for j in range(S) if o[j] and not o[j - 1] or (o[j] and all(o)))
                    ni = 0; gap = 2
                    for t in range(S):
                        x = o[(s0 + t) % S]
                        if x:
                            if gap >= 2:
                                ni += 1
                            gap = 0
                        else:
                            gap += 1
                    isl[k] += ni
                    # extents from the centre c of the last live sites (k = 1), circular
                    c = idx1[len(idx1) // 2]
                    L = R = 0; g = 0
                    for t in range(1, S // 2 + 1):           # walk right until a gap of >= 2 empties
                        if o[(c + t) % S]:
                            R = t; g = 0
                        else:
                            g += 1
                            if g >= 2:
                                break
                    g = 0
                    for t in range(1, S // 2 + 1):
                        if o[(c - t) % S]:
                            L = t; g = 0
                        else:
                            g += 1
                            if g >= 2:
                                break
                    left[k] += L; right[k] += R
                else:
                    js = [j for j, x in enumerate(o) if x]
                    if not js:
                        continue
                    span[k] += js[-1] - js[0] + 1
                    ni = 1 + sum(1 for a, c2 in zip(js, js[1:]) if c2 - a >= 3)
                    isl[k] += ni
                    c = idx1[len(idx1) // 2]
                    left[k] += max(0, c - js[0]); right[k] += max(0, js[-1] - c)
    print(f'{tag}: b={b} wall={wall}, {nd} deaths; sites occupied one generation before death: '
          + ', '.join(f'{n}: {v / nd:.3f}' for n, v in sorted(lastn.items())[:5]))
    print(' k    pop  occ.sites  span  islands  left  right')
    for k in range(1, K + 1):
        print(f'{k:2d} {pop[k] / nd:6.2f} {occ[k] / nd:8.2f} {span[k] / nd:7.2f} {isl[k] / nd:6.2f} {left[k] / nd:6.2f} {right[k] / nd:6.2f}')
    ref = pop[K] / nd
    for k in range(1, K + 1):
        if pop[k] / nd >= ref / 2:
            k0 = k - 1; f = (ref / 2 - pop[k0] / nd) / (pop[k] / nd - pop[k0] / nd) if k0 else 0
            print(f'half of pop(k={K}) = {ref:.1f} reached at lag {k0 + f:.2f}')
            break


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
