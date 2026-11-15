#!/usr/bin/env python3
"""ana.py: ln tau_face = ln(2E/F) from tor.c's life records (E = sum of every life's age at its end, F = face deaths).

    python3 ana.py REC [REC ...]
Per file and pooled: lives by kind, ln(2E/F) +- 1/sqrt(F), ln tau_fw = ln(E/W); cycles (period = age - snapshot age:
the first return after the snapshot) and the exposure they carry past their snapshot (the alternative convention);
the face hazard in age bins relative to the pooled hazard; the hazard beyond 2 and 4 mean lives.
"""
import math, sys
import numpy as np
REC = np.dtype([('lane', '<i4'), ('kind', '<i4'), ('birth', '<i8'), ('age', '<i8'), ('snap', '<i8'), ('life', '<i8')])


def one(R):
    E = float(R['age'].sum()); F = int((R['kind'] == 1).sum()); W = int((R['kind'] == 4).sum())
    return E, F, W


def main(paths):
    allR = []
    for p in paths:
        R = np.fromfile(p, REC); allR.append(R)
        E, F, W = one(R)
        print(f'{p}: lives {len(R)} kinds(open, face, cycle, -, fw) {np.bincount(R["kind"], minlength=5).tolist()} '
              f'E {E:.6g}  ln(2E/F) = {math.log(2 * E / F):.5f} +- {1 / math.sqrt(F):.5f}')
    R = np.concatenate(allR)
    E, F, W = one(R)
    l = math.log(2 * E / F); e = 1 / math.sqrt(F)
    vals = [math.log(2 * one(x)[0] / one(x)[1]) for x in allR]; errs = [1 / math.sqrt(one(x)[1]) for x in allR]
    chi2 = sum(((v - l) / s) ** 2 for v, s in zip(vals, errs))
    print(f'POOLED: {len(paths)} runs, lives {len(R)}, E {E:.6g}, F {F}, W {W}: ln tau_face = ln(2E/F) = {l:.5f} +- {e:.5f}; '
          f'runs chi2 {chi2:.2f} on {len(paths) - 1}' + (f'; ln tau_fw = {math.log(E / W):.4f} +- {1 / math.sqrt(W):.4f}' if W else ''))
    cyc = R[R['kind'] == 2]
    if len(cyc):
        per = cyc['age'] - cyc['snap']
        u, c = np.unique(per, return_counts=True)
        extra = float(per.sum())
        print(f'  cycles: {len(cyc)} ({len(cyc) / F:.2e} per face death); periods {dict(zip(u.tolist(), c.tolist()))}; '
              f'max entry-bound (snapshot age) {cyc["snap"].max()}; exposure after the snapshot {extra:.3g} '
              f'({extra / E:.1e} of E: ln changes by {math.log(1 - extra / E):+.1e} if cut there)')
    h = F / E
    edges = np.array([0, 60, 200, 1000] + list(np.geomspace(3000, max(4000, R['age'].max()), 9).astype(np.int64)))
    edges = np.unique(edges)
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        ex = float(np.clip(np.minimum(R['age'], hi) - lo, 0, None).sum())
        fd = int(((R['kind'] == 1) & (R['age'] > lo) & (R['age'] <= hi)).sum())
        if ex > 0 and fd > 0:
            rows.append(f'({lo},{hi}] {fd / ex / h:.3f}+-{math.sqrt(fd) / ex / h:.3f}')
    print('  face hazard by age / pooled hazard: ' + '; '.join(rows))
    ml = 1 / h                                             # mean life to a face death = E/F = tau_face / 2
    for k in (2, 4):
        ex = float(np.clip(R['age'] - k * ml, 0, None).sum()); fd = int(((R['kind'] == 1) & (R['age'] > k * ml)).sum())
        if fd:
            print(f'  face hazard beyond {k} mean lives ({k * ml:.3g}): {fd / ex / h:.3f} +- {math.sqrt(fd) / ex / h:.3f} '
                  f'of the pooled ({fd} deaths)')


if __name__ == '__main__':
    main(sys.argv[1:])
