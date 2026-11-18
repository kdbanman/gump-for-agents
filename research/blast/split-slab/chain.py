#!/usr/bin/env python3
"""Is the tube's discount the entropy of crash timing?  (README section 10; the PI's test of 05:05 UTC.)

    python3 chain.py            # tubes of 144 and 192 cells, the wide tori of 108 and 192 cells; markdown tables

Chain picture (the PI's): the crash generations s_i of the sections of a dying tube form a chain with transfer matrix
M = I + u (J - I) on W timings; lam1 = 1 + (W - 1) u, lam2 = 1 - u. In the dying ensemble of a long chain
P(neighbours equal) = 1 / lam1 whatever W, so   discount per cell = -ln P1 / (cells per section),
P(s_0 = s_k) = 1/W + (1 - 1/W) (lam2 / lam1)^k, and the correlation length of timing is a / ln(lam1 / lam2).
On a ring of N sections (the tube is periodic) P(s_0 = s_k) = W d_k d_{N-k} / (lam1^N + (W - 1) lam2^N),
d_k = lam2^k + (lam1^k - lam2^k) / W; u is solved from the measured P1 with that formula.

Data: G/cells/cells_H_K_D_s5.txt (sections.py's definitions of ring, crash generation and half-fall). A section is a
block of r = 2 l rings (l lattice units, 12 l cells). Every offset of the cut (0..r-1 rings) is used and averaged.
When r does not divide the number of rings the last, incomplete block is dropped and only pairs inside the run
of complete blocks are used. Per replication first; mean +- standard error over replications.
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sections  # noqa
C = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-slab', 'cells'))


def rings(H, K, D):
    A = 3 * H * D; n = H * D
    q, vx, vy = sections.shortest(H, K, D)
    ii = np.array([(c // 3) // D for c in range(A)]); jj = np.array([(c // 3) % D for c in range(A)])
    t = (vx * jj - vy * ii) % n
    vals = sorted(set(t.tolist())); rank = {v: r for r, v in enumerate(vals)}
    return np.array([rank[x] for x in t]), len(vals), ii, jj


def load(fn):
    units = {}
    for line in open(fn):
        if line[0] != 'C':
            continue
        a, b = line.split('|'); t = a.split(); gens = b.split()
        if len(gens) < 16:
            continue
        units.setdefault(int(t[1]), []).append(np.array([[ch == '1' for ch in g] for g in gens[:16]], dtype=np.int16))
    return units


def ring_pk(u, W, N, k):
    l1, l2 = 1 + (W - 1) * u, 1 - u
    d = lambda j: l2 ** j + (l1 ** j - l2 ** j) / W
    return W * d(k) * d(N - k) / (l1 ** N + (W - 1) * l2 ** N)


def solve_u(P1, W, N):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ring_pk(mid, W, N, 1) > P1 else (lo, mid)
    return (lo + hi) / 2


def last_above(pop, m, theta):
    """threshold-free-of-selection timing: generations before the death at which the section last held >= theta m cells (17 = not in the record)"""
    for g in range(len(pop)):
        if pop[g] >= theta * m:
            return g + 1
    return len(pop) + 1


def tube(H, K, D, fn, lengths=(1, 2, 3, 4), thr=0.5, theta=None):
    ring, R, ii, jj = rings(H, K, D); A = 3 * H * D
    units = load(fn)
    out = []
    for l in lengths:
        r = 2 * l; N = R // r; circ = (R % r == 0); kmax = N // 2 if circ else N - 1
        per = {}          # per replication: sums
        for u_, Xs in units.items():
            acc = {}
            for X in Xs:
                ringpop = np.stack([X[:, ring == x].sum(1) for x in range(R)], 1).astype(float)     # 16 x R
                for o in range(r):
                    idx = [(o + b * r + np.arange(r)) % R for b in range(N)]
                    ks = []; hf = []
                    for b in range(N):
                        if theta is None:
                            k, bf, af = sections.crash(ringpop[:, idx[b]].sum(1), 6 * r)
                            ks.append(k); hf.append(bf - af >= thr)
                        else:
                            ks.append(last_above(ringpop[:, idx[b]].sum(1), 6 * r, theta)); hf.append(True)
                    for sep in range(1, kmax + 1):
                        pairs = [(b, (b + sep) % N) for b in range(N)] if circ else [(b, b + sep) for b in range(N - sep)]
                        for b, c in pairs:
                            e = float(ks[b] == ks[c])
                            a = acc.setdefault(sep, [0, 0, 0, 0]); a[0] += e; a[1] += 1
                            if hf[b] and hf[c]:
                                a[2] += e; a[3] += 1
                    a = acc.setdefault('hf', [0, 0]); a[0] += sum(hf); a[1] += N
            for key, a in acc.items():
                per.setdefault(key, []).append(a)
        res = {'l': l, 'N': N, 'circ': circ, 'cells': 12 * l, 'units': len(units)}
        hfa = np.array(per['hf'], float); res['hf'] = float((hfa[:, 0] / hfa[:, 1]).mean())
        for sep in range(1, kmax + 1):
            a = np.array(per[sep], float)
            pa = a[:, 0] / a[:, 1]; ok = a[:, 3] > 0; pb = a[ok, 2] / a[ok, 3]
            res[('all', sep)] = (float(pa.mean()), float(pa.std(ddof=1) / math.sqrt(len(pa))))
            res[('both', sep)] = (float(pb.mean()), float(pb.std(ddof=1) / math.sqrt(len(pb))))
        out.append(res)
    return out, R, A


def report_tube(H, K, D):
    fn = os.path.join(C, f'cells_{H}_{K}_{D}_s5.txt')
    out, R, A = tube(H, K, D, fn)
    print(f'\n**Tube ({H},{K}),(0,{D}), {A} cells, {R / 2:.0f} lattice units long, {out[0]["units"]} replications.**\n')
    for which, lab in (('both', 'both sections with a half-fall'), ('all', 'all sections')):
        print(f'Neighbouring sections, {lab}:\n')
        print('| section | cells | sections on the tube | share of sections with a half-fall | P1 = P(neighbours crash in the same generation) | discount per cell = -ln P1 / cells | ring-corrected ln lam1 / cells (W = 3) | P2 measured | P2 chain (W = 3) | P3 measured | P3 chain | P4 measured | P4 chain | xi of the chain (units) | W from the far plateau |')
        print('|---|---:|---:|---:|---|---|---:|---|---:|---|---:|---|---:|---:|---:|')
        for r in out:
            P1, e1 = r[(which, 1)]; N = r['N']; cells = r['cells']
            disc = -math.log(P1) / cells; de = e1 / P1 / cells
            Nring = N if r['circ'] else 10 ** 6
            u = solve_u(P1, 3, min(Nring, 400)) if P1 < 1 else 0.0
            l1, l2 = 1 + 2 * u, 1 - u
            xi = r['l'] / math.log(l1 / l2) if u > 0 else float('inf')
            row = [f'{r["l"]} unit' + ('s' if r['l'] > 1 else ''), str(cells), f'{N}' + ('' if r['circ'] else ' (+ remainder)'), f'{r["hf"]:.2f}', f'{P1:.3f} ± {e1:.3f}', f'{disc:.4f} ± {de:.4f}', f'{math.log(l1) / cells:.4f}']
            far = None
            for sep in (2, 3, 4):
                if (which, sep) in r:
                    pm, pe = r[(which, sep)]
                    pc = ring_pk(u, 3, N, sep) if r['circ'] else (1 / 3 + (2 / 3) * (l2 / l1) ** sep)
                    row += [f'{pm:.3f} ± {pe:.3f}', f'{pc:.3f}']; far = (pm, sep)
                else:
                    row += ['', '']
            # the farthest separation available: plateau 1/W if the chain has decorrelated
            seps = [k for k in range(1, 20) if (which, k) in r]
            pfar = r[(which, seps[-1])][0]
            row += [f'{xi:.1f}', f'{1 / pfar:.1f} (P = {pfar:.2f} at {seps[-1] * r["l"]} units)']
            print('| ' + ' | '.join(row) + ' |')
        print()
    return out


def report_wide(H, D):
    fn = os.path.join(C, f'cells_{H}_0_{D}_s5.txt'); A = 3 * H * D
    units = load(fn)
    ii = np.array([(c // 3) // D for c in range(A)]); jj = np.array([(c // 3) % D for c in range(A)])
    per = []
    for u_, Xs in units.items():
        acc = np.zeros(8)
        for X in Xs:
            for oi in range(H // 2):
                for oj in range(D // 2):
                    qi = (((ii - oi) % H) * 2) // H; qj = (((jj - oj) % D) * 2) // D; lab = qi * 2 + qj
                    ks = []; hf = []
                    for s in range(4):
                        k, bf, af = sections.crash(X[:, lab == s].sum(1).astype(float), A // 4); ks.append(k); hf.append(bf - af >= 0.5)
                    for (b, c), kind in (((0, 1), 0), ((2, 3), 0), ((0, 2), 0), ((1, 3), 0), ((0, 3), 4), ((1, 2), 4)):
                        e = float(ks[b] == ks[c]); acc[kind] += e; acc[kind + 1] += 1
                        if hf[b] and hf[c]:
                            acc[kind + 2] += e; acc[kind + 3] += 1
        per.append(acc)
    a = np.array(per)
    f = lambda x, y: (float((a[:, x] / a[:, y]).mean()), float((a[:, x] / a[:, y]).std(ddof=1) / math.sqrt(len(a))))
    cells = A // 4
    print(f'| ({H},0),(0,{D}) | {A} | {cells} | {len(a)} | ' + ' | '.join(f'{p:.3f} ± {e:.3f}' for p, e in (f(2, 3), f(0, 1), f(6, 7), f(4, 5))) +
          f' | {-math.log(f(2, 3)[0]) / cells:.4f} ± {f(2, 3)[1] / f(2, 3)[0] / cells:.4f} | {-math.log(f(0, 1)[0]) / cells:.4f} ± {f(0, 1)[1] / f(0, 1)[0] / cells:.4f} |')


def sensitivity():
    print('\n**Sensitivity of P1 to what counts as a crashed section (192-cell tube; both sections with a fall of at least thr of their cells).**\n')
    print('| thr | ' + ' | '.join(f'{l} units: share of sections, P1, -ln P1 / cells' for l in (2, 3, 4)) + ' |')
    print('|---:|---|---|---|')
    for thr in (0.3, 0.4, 0.5, 0.6):
        out, R, A = tube(1, 30, 64, os.path.join(C, 'cells_1_30_64_s5.txt'), lengths=(2, 3, 4), thr=thr)
        cellsrow = []
        for r in out:
            P1, e1 = r[('both', 1)]
            cellsrow.append(f'{r["hf"]:.2f}, {P1:.3f} ± {e1:.3f}, {-math.log(P1) / r["cells"]:.4f} ± {e1 / P1 / r["cells"]:.4f}')
        print(f'| {thr} | ' + ' | '.join(cellsrow) + ' |')


def emptying():
    print('\n**A crash time defined for every section, without selection: the number of generations before the death at which the section last held at least theta of its cells.** P_k = share of pairs of sections k apart with the same time; chain = ring formula with u from P1.\n')
    print('| tube | theta | section | N | P1 | -ln P1 / cells | ring-corrected ln lam1 / cells (W = 3) | P2 | P3 | P4 | chain W = 3: P2, P3, P4 | chain W = 5: P2, P3, P4 |')
    print('|---|---:|---|---:|---|---|---:|---|---|---|---|---|')
    for L in ((1, 22, 48), (1, 30, 64)):
        for theta in (0.3, 0.35, 0.4):
            out, R, A = tube(*L, os.path.join(C, 'cells_%d_%d_%d_s5.txt' % L), theta=theta)
            for r in out:
                P1, e1 = r[('all', 1)]; N = r['N']; cells = r['cells']
                g = lambda k: (f'{r[("all", k)][0]:.3f} ± {r[("all", k)][1]:.3f}' if ('all', k) in r else '')
                pred = {}
                for W in (3, 5):
                    u = solve_u(P1, W, N) if r['circ'] else (1 / P1 - 1) / (W - 1)
                    l1, l2 = 1 + (W - 1) * u, 1 - u
                    pred[W] = (math.log(l1) / cells, ', '.join((f'{ring_pk(u, W, N, k):.3f}' if r['circ'] else f'{1 / W + (1 - 1 / W) * (l2 / l1) ** k:.3f}') for k in (2, 3, 4) if ('all', k) in r))
                print(f'| {A} cells | {theta} | {r["l"]} u | {N} | {P1:.3f} ± {e1:.3f} | {-math.log(P1) / cells:.4f} ± {e1 / P1 / cells:.4f} | {pred[3][0]:.4f} | {g(2)} | {g(3)} | {g(4)} | {pred[3][1]} | {pred[5][1]} |')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sens':
        sensitivity(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'empty':
        emptying(); sys.exit(0)
    for L in ((1, 22, 48), (1, 30, 64)):
        report_tube(*L)
    print('\n**Wide tori cut into four quarters (every offset of the two cuts averaged): neighbouring quarters share an edge, diagonal ones a corner.**\n')
    print('| torus | cells | cells per quarter | replications | P(same generation), neighbours, both with a half-fall | neighbours, all | diagonal, both | diagonal, all | -ln P1 / cells (both) | (all) |')
    print('|---|---:|---:|---:|---|---|---|---|---|---|')
    for H, D in ((6, 6), (8, 8)):
        report_wide(H, D)
