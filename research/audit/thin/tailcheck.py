#!/usr/bin/env python3
"""Do lives that stopped dying hide in the thin line's lifetime tags? (review of research/theory/thin/)
Reads the line's raw chunk files research/scratch/thin/TAG/c*.txt (their age-binned exposure and deaths, ages >= T0)
and the review's own (research/scratch/audit_thin/TAG/s*.txt). For a flat hazard h = F/E, the deaths expected in the
old-age tail (ages >= X lane-lives) are h * E_tail; a life stuck without dying adds exposure there and no deaths.
Prints, per tag, the observed and expected deaths in the tails beyond 4 and 8 mean lane-lives, and the largest age bin
with exposure in units of the mean lane-life.

    python3 research/audit/thin/tailcheck.py [TAGPATTERN]
"""
import glob, math, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))


def load_line(d):
    E = None; F = None; T0 = None; nf = 2
    for fn in glob.glob(os.path.join(d, 'c*.txt')):
        ls = open(fn).read().split('\n')
        h = ls[0].split(); kv = {h[i]: h[i + 1] for i in range(0, len(h) - 1, 2)}
        T0 = int(kv['T0']); nf = 2 if kv['mode'] == 'det' else 1
        e = [float(x) for x in next(l for l in ls if l.startswith('expo ')).split()[1:]]
        f = [float(x) for x in next(l for l in ls if l.startswith('deaths ')).split()[1:]]
        E = e if E is None else [x + y for x, y in zip(E, e)]
        F = f if F is None else [x + y for x, y in zip(F, f)]
    return E, F, T0, nf


def load_own(d):
    E = None; F = None
    for fn in glob.glob(os.path.join(d, 's*.txt')):
        ls = open(fn).read().split('\n')
        h = ls[0].split(); kv = {h[i]: h[i + 1] for i in range(0, len(h) - 1, 2)}
        e = [float(x) for x in ls[1].split()[1:]]; f = [float(x) for x in ls[2].split()[1:]]
        E = e if E is None else [x + y for x, y in zip(E, e)]
        F = f if F is None else [x + y for x, y in zip(F, f)]
    return E, F, int(kv['T0']), int(kv['faces'])


def check(name, E, F, T0, nf):
    k0 = T0.bit_length() - 1
    Et, Ft = sum(E[k0:]), sum(F[k0:])
    if not Ft:
        return
    h = Ft / Et; life = 1 / h * 1.0      # mean lane-life (any face) in generations
    out = []
    for X in (4, 8):
        j = next((j for j in range(len(E)) if (1 << j) >= X * life), len(E))
        Ex, Fx = sum(E[j:]), sum(F[j:])
        out.append(f'ages >= {1 << j} ({(1 << j) / life:.1f} lives): obs {Fx:.0f} exp {h * Ex:.1f}')
    jmax = max((j for j in range(len(E)) if E[j] > 0), default=0)
    print(f'{name:22s} deaths {Ft:8.0f} ln tau {math.log(nf * Et / Ft):.4f} | ' + ' | '.join(out) +
          f' | oldest bin [2^{jmax}, 2^{jmax + 1}) = {(1 << jmax) / life:.1f} lives')


if __name__ == '__main__':
    pat = sys.argv[1] if len(sys.argv) > 1 else '*'
    for d in sorted(glob.glob(os.path.join(ROOT, 'research', 'scratch', 'thin', pat))):
        if os.path.isdir(d) and glob.glob(os.path.join(d, 'c*.txt')):
            try:
                check('line ' + os.path.basename(d), *load_line(d))
            except StopIteration:
                pass
    for d in sorted(glob.glob(os.path.join(ROOT, 'research', 'scratch', 'audit_thin', pat))):
        if os.path.isdir(d) and glob.glob(os.path.join(d, 's*.txt')):
            check('own  ' + os.path.basename(d), *load_own(d))
