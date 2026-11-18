#!/usr/bin/env python3
"""Does where the survivors sit decide whether a thin hull face dies? q(k | class) at the first passage of an
excursion to exactly k live cells.

  python -u research/dying2/hull/condq.py R PREFIX [PREFIX ...]

Sample: every dumped death (single face) whose final excursion first reaches P <= k at exactly P = k, and every
dumped recovered dip (minimum m, 1 <= m <= k) that first reaches P <= k at exactly P = k with the face state stored
at that generation. Weights restore the full population of excursions: a recovered dip of minimum m counts
rec[m] / dumped[m] (hist files), a death counts (dead excursions) / (dumped deaths). q(k | class) = weighted
deaths / (weighted deaths + weighted recoveries). Classes of the k survivors: number in the rim row (row 0); number
within 1.5 cube units of a corner; mean pair distance (cube units) below / above the pooled median.
Errors: binomial on the effective counts (sum w)^2 / sum w^2.
"""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as an  # noqa: E402


def main(R, prefixes, ks=(2, 3, 4, 6, 9)):
    g = an.geom(R); fp = g['face_pos']; nfn = g['nfn']
    rec = np.zeros(128); dead = 0; dumped = np.zeros(128)
    for p in prefixes:
        for f in glob.glob(os.path.join(an.SCR, p + '_t*.hist')):
            L = open(f).read().split('\n')
            a = np.array([list(map(int, l.split())) for l in L[2:] if l.strip()])
            rec += a[:, 2]; dead += a[:, 3].sum(); dumped += a[:, 5]
    recs = []
    for p in prefixes:
        for f in sorted(glob.glob(os.path.join(an.SCR, p + '_t*.dump'))):
            recs += [r for r in an.read_dumps(f, g) if r['type'] in (1, 2)]
    deaths = [r for r in recs if r['type'] == 1 and bin(r['a']).count('1') == 1]
    recov = [r for r in recs if r['type'] == 2]
    wd = dead / len(deaths)
    row0 = g['row'][0]; dc0 = g['dcorner'][0]; xyz0 = g['xyz'][fp[0]]
    U = None
    for f in glob.glob(os.path.join(an.SCR, prefixes[0] + '_t0.hist')):
        hd = open(f).readline().split(); U = int(dict(zip(hd[0::2], hd[1::2]))['U'])

    def canon(r, f, js):
        s = an.bits(r['st'][js], nfn); c = np.zeros(len(fp[0]), bool); c[g['canon'][f]] = s[fp[f]]; return c

    def feats(c):
        q = xyz0[c]
        d = np.sqrt(((q[:, None] - q[None]) ** 2).sum(-1))
        sp = d[np.triu_indices(len(q), 1)].mean() if len(q) > 1 else 0.0
        return int((row0[c] == 0).sum()), int((dc0[c] < 1.5).sum()), sp

    print(f'R = {R}: dead excursions {dead}, dumped deaths {len(deaths)} (weight {wd:.2f}), recovered dumps {len(recov)}; U = {U}')
    out = []
    for k in ks:
        items = []          # (dies, weight, rim, corner, spread)
        for r in deaths:
            f = [b for b in range(8) if (r['a'] >> b) & 1][0]
            pp = r['pops'][:, f].astype(int); nH = len(pp); age = r['gen'] - r['birth']; lo = max(0, nH - age)
            w = np.nonzero(pp[lo:] >= U)[0]
            if not len(w):
                continue
            s0 = lo + w[-1] + 1; j = s0 + int(np.argmax(pp[s0:] <= k))
            js = j - (nH - len(r['st']))
            if pp[j] != k or js < 0:
                continue
            items.append((1, wd) + feats(canon(r, f, js)))
        nd = len(items)
        for r in recov:
            m = r['b']
            if m > k or dumped[m] == 0:
                continue
            f = r['a']; pp = r['pops'][:, f].astype(int); nH = len(pp); s0 = nH - 1 - r['c']
            if s0 < 0:
                continue
            j = s0 + int(np.argmax(pp[s0:] <= k)); js = j - (nH - len(r['st']))
            if pp[j] != k or js < 0:
                continue
            items.append((0, rec[m] / dumped[m]) + feats(canon(r, f, js)))
        it = np.array(items, float)
        D, Wt = it[:, 0], it[:, 1]
        med = np.median(it[:, 4])

        def q(mask):
            w1 = (Wt * D * mask).sum(); w0 = (Wt * (1 - D) * mask).sum(); wt = w1 + w0
            neff = (Wt * mask).sum() ** 2 / max((Wt ** 2 * mask).sum(), 1e-12)
            qq = w1 / wt if wt > 0 else math.nan
            return qq, math.sqrt(qq * (1 - qq) / neff) if neff > 0 else math.nan, int(mask.sum())
        qa = q(np.ones(len(it)))
        line = [f'  k = {k}: {nd} deaths, {len(it) - nd} recoveries at first passage P = k; q(all) = {qa[0]:.3f} +- {qa[1]:.3f}']
        rows = [('all', '', *qa)]
        for nm, col, bins in (('rim-row survivors', 2, None), ('survivors within 1.5 of a corner', 3, None)):
            vals = it[:, col]
            for v in range(0, k + 1):
                mk = vals == v
                if mk.sum() < 30:
                    continue
                qq = q(mk.astype(float))
                rows.append((nm, v, *qq))
                line.append(f'      {nm} = {v}: q {qq[0]:.3f} +- {qq[1]:.3f} (n {qq[2]}; share {(Wt * mk).sum() / Wt.sum():.3f})')
        for nm, mk in (('spread below median', it[:, 4] < med), ('spread above median', it[:, 4] >= med)):
            qq = q(mk.astype(float)); rows.append((nm, f'{med:.2f}', *qq))
            line.append(f'      {nm} ({med:.2f}): q {qq[0]:.3f} +- {qq[1]:.3f} (n {qq[2]})')
        print('\n'.join(line))
        out += [(k,) + r_ for r_ in rows]
    with open(os.path.join(an.DATA, f'R{R}_condq.csv'), 'w') as fh:
        fh.write('k,class,value,q,q_se,n\n')
        for o in out:
            fh.write(f'{o[0]},{o[1]},{o[2]},{o[3]:.5g},{o[4]:.5g},{o[5]}\n')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2:])
