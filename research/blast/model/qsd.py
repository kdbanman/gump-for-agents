#!/usr/bin/env python3
"""qsd.py (blast/model): the quasi-stationary distribution of a face's population from ex3's HIST files, the tail
slope of ln pi(n), the dip table (nu, q), and the tangent construction checked against the measured lifetime.

    python3 research/blast/model/qsd.py SPEC [SPEC ...]         # table per face
    python3 research/blast/model/qsd.py --summary SPEC ...      # one line per face
HIST files: research/scratch/blast/model/hist_SPEC.txt (made by queue1.sh; ex3 from research/dying/ex3.c).
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'model'))
DAT = os.path.join(HERE, 'data')


def load(spec):
    p = os.path.join(DAT, f'hist_{spec}.txt')
    if not os.path.exists(p):
        p = os.path.join(SCR, f'hist_{spec}.txt')
    d = {'exc': []}
    for ln in open(p):
        t = ln.split()
        if not t:
            continue
        if t[0] == 'phist':
            d['ph'] = [int(x) for x in t[1:]]
        elif t[0] == 'exc':
            d['exc'].append([int(x) for x in t[1:]])
        else:
            d[t[0]] = float(t[1])
    return d


def area(spec):
    t = spec.split('_')
    if t[0] == 'gen':
        return 3 * int(t[1]) * int(t[3])
    R = int(t[1]); k = (R + 1) // 2 - 0   # hull face of radius R (cube-centred): k = (R+1)/2 ... A = 3k(k+1)/2 with k = (R-3)/2+... fixed below
    return {7: 30, 9: 45, 11: 63, 13: 84, 15: 108, 17: 135}[R]


def stats(spec):
    d = load(spec); A = area(spec); ph = d['ph']; E = d['expo']; F = d['fdeaths']
    tot = sum(ph[1:])
    m = sum(n * c for n, c in enumerate(ph) if n) / tot
    v = sum((n - m) ** 2 * c for n, c in enumerate(ph) if n) / tot
    lp = [math.log(c / tot) if c > 0 else None for c in ph]
    # dips: exc rows are [minP, recovered, dead, censored]
    rec = {r[0]: r[1] for r in d['exc']}; dead = sum(r[2] for r in d['exc'])
    cum = 0; q = {}; nu = {}
    for n in range(1, len(ph)):
        cum += rec.get(n, 0)
        if cum + dead > 0:
            q[n] = dead / (cum + dead); nu[n] = (cum + dead) / E
    return dict(spec=spec, A=A, E=E, F=F, lntau=math.log(E / F) if F else float('nan'), se=1 / math.sqrt(F) if F else float('nan'),
                mean=m, var=v, rho=m / A, s2=v / A, lp=lp, ph=ph, q=q, nu=nu, tot=tot, dead=dead)


def slope(lp, ph, a, b):
    """weighted least-squares slope of ln pi(n) over a <= n <= b (weights = counts)"""
    xs = [n for n in range(a, b + 1) if lp[n] is not None and ph[n] >= 20]
    if len(xs) < 3:
        return float('nan'), float('nan')
    w = [ph[n] for n in xs]; W = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / W; my = sum(wi * lp[x] for wi, x in zip(w, xs)) / W
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs)); sxy = sum(wi * (x - mx) * (lp[x] - my) for wi, x in zip(w, xs))
    return sxy / sxx, 1 / math.sqrt(sxx)


def uslope(lp, ph, a, b):
    xs = [n for n in range(a, b + 1) if lp[n] is not None and ph[n] >= 20]
    if len(xs) < 3:
        return float('nan')
    mx = sum(xs) / len(xs); my = sum(lp[x] for x in xs) / len(xs)
    return sum((x - mx) * (lp[x] - my) for x in xs) / sum((x - mx) ** 2 for x in xs)


if __name__ == '__main__':
    args = sys.argv[1:]; summary = '--summary' in args; specs = [a for a in args if not a.startswith('--')]
    if summary:
        print('spec A lntau se mean rho var s2 | lam[2-6] lam[4-10] lam[6-0.3P] lam[0.15-0.45P] | n_t  x_t | tangentA*(lam rho - lam^2 s2/2) ; -ln pi(1) ; F/pi(1)')
    for s in specs:
        try:
            st = stats(s)
        except FileNotFoundError:
            continue
        lp, ph, m, v, A = st['lp'], st['ph'], st['mean'], st['var'], st['A']
        if summary:
            l1 = uslope(lp, ph, 2, 6); l2 = uslope(lp, ph, 4, 10); l3 = uslope(lp, ph, 6, int(0.3 * m))
            l4 = uslope(lp, ph, int(round(0.15 * m)), int(round(0.45 * m)))
            lam = l4
            nt = m - lam * v
            print(f"{s} {A} {st['lntau']:.4f} {st['se']:.4f} {m:.3f} {st['rho']:.4f} {v:.3f} {st['s2']:.4f} | {l1:.3f} {l2:.3f} {l3:.3f} {l4:.3f} | "
                  f"{nt:.1f} {nt / A:.3f} | {A * (lam * st['rho'] - lam * lam * st['s2'] / 2):.3f} ; "
                  f"{-lp[1] if lp[1] is not None else float('nan'):.3f} ; {st['F'] / ph[1] if ph[1] else float('nan'):.3f}")
            continue
        print(f"# {s}: A {A}, exposure {st['E']:.4g}, face deaths {st['F']:.0f}, ln tau {st['lntau']:.4f} +- {st['se']:.4f}, "
              f"mean {m:.3f} (rho {st['rho']:.4f}), var {v:.3f} (s2 {st['s2']:.4f})")
        print('# n  count  ln pi(n)  local slope ln pi(n+1)/pi(n)  gaussian slope  q(n)  ln nu(n)')
        for n in range(1, int(m) + 3):
            if ph[n] == 0:
                continue
            ls = lp[n + 1] - lp[n] if lp[n + 1] is not None else float('nan')
            print(f"{n:3d} {ph[n]:12d} {lp[n]:9.4f} {ls:7.3f} {(m - n - 0.5) / v:7.3f} {st['q'].get(n, float('nan')):9.5f} "
                  f"{math.log(st['nu'][n]) if n in st['nu'] else float('nan'):9.4f}")
