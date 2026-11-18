#!/usr/bin/env python3
"""upper.py (blast/model): the UPPER tail of the stationary face population (the over-full faces from which
agent `anatomy` saw wrapped faces bust), from the population histograms in data/ (short runs, 1.5e8 samples).

Per face: ln pi(P) at P/A = 0.70, 0.73, 0.77 (63 cells: 44, 46, 48.5), the Gaussian value there with the
stationary mean and variance, and the local slope. Then tube against wide at equal area in the upper tail.

    python3 research/blast/model/upper.py
"""
import glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qsd, frontgas as FG


def load(spec):
    best = None
    for d in (qsd.DAT, qsd.SCR):
        for pre in ('hist_s_', 'hist_', 'hist5_'):
            p = os.path.join(d, pre + spec + '.txt')
            if os.path.exists(p):
                for ln in open(p):
                    u = ln.split()
                    if u and u[0] == 'phist':
                        ph = [int(x) for x in u[1:]]
                        if best is None or sum(ph) > sum(best):
                            best = ph
    return best


def lnpi_at(ph, x):
    """ln pi interpolated linearly at real x"""
    tot = sum(ph[1:]); i = int(math.floor(x))
    if ph[i] < 30 or ph[i + 1] < 30:
        return None
    a, b = math.log(ph[i] / tot), math.log(ph[i + 1] / tot)
    return a + (b - a) * (x - i)


def lncum_at(ph, x):
    tot = sum(ph[1:]); c = sum(ph[int(math.ceil(x)):])
    return math.log(c / tot) if c >= 30 else None


specs = sorted({os.path.basename(f)[7:-4] for f in glob.glob(os.path.join(qsd.DAT, 'hist_s_gen_*_c1.txt')) +
                glob.glob(os.path.join(qsd.SCR, 'hist_s_gen_*_c1.txt'))},
               key=lambda s: (FG.prim_loops(*[int(x) for x in s.split('_')[1:4]])[0], 3 * int(s.split('_')[1]) * int(s.split('_')[3])))
print('face              A loop2   mean    var  | ln P(P >= 0.73 A): measured, Gaussian(mean, var), difference | per cell: measured, Gaussian')
T = {}
for s in specs:
    t = s.split('_'); h, k, d = int(t[1]), int(t[2]), int(t[3]); A = 3 * h * d
    ph = load(s); tot = sum(ph[1:])
    m = sum(n * c for n, c in enumerate(ph) if n) / tot; v = sum((n - m) ** 2 * c for n, c in enumerate(ph) if n) / tot
    x = 0.73 * A; lc = lncum_at(ph, x)
    z = (math.ceil(x) - 0.5 - m) / math.sqrt(v); g = math.log(0.5 * math.erfc(z / math.sqrt(2)))
    T[s] = (A, m, v, ph)
    if lc is None:
        print(f'{s:16s} {A:4d} {FG.prim_loops(h, k, d)[0]:3d} {m:7.3f} {v:6.2f} | (too few samples)   Gaussian {g:8.3f}')
        continue
    print(f'{s:16s} {A:4d} {FG.prim_loops(h, k, d)[0]:3d} {m:7.3f} {v:6.2f} | {lc:8.3f} {g:8.3f} {lc - g:+7.3f} | {lc / A:8.4f} {g / A:8.4f}')

print('\ntube against wide at equal area, upper tail: Delta_up = ln pi_tube(P) - ln pi_wide(P)')
for tb, wd, A, D in (('gen_1_5_22_c1', 'gen_1_4_22_c1', 66, 0.125), ('gen_1_12_28_c1', 'gen_1_4_28_c1', 84, 0.220),
                     ('gen_1_16_36_c1', 'gen_6_0_6_c1', 108, 0.381)):
    if tb not in T or wd not in T:
        continue
    a, b = T[tb][3], T[wd][3]
    out = []
    for fr in (0.60, 0.65, 0.70, 0.73, 0.77):
        la, lb = lnpi_at(a, fr * A), lnpi_at(b, fr * A)
        out.append(f'P/A {fr:.2f}: {la - lb:+.3f}' if la is not None and lb is not None else f'P/A {fr:.2f}: n/a')
    print(f'  A = {A} (lifetime discount of the tube D = {D:.3f}): ' + ';  '.join(out))
