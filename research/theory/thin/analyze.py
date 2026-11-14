#!/usr/bin/env python3
"""Tables from the chunk files of run.py.

    python3 analyze.py life TAG...           # ln tau per tag, local slopes between successive tags
    python3 analyze.py win TAG [lmax]        # empty-window probability E(l), cost k(l) = -ln E(l+1)/E(l), jackknife errors
    python3 analyze.py qsd TAG               # face population in the living state, deaths by population one generation before
    python3 analyze.py static WINTAG LIFETAG...   # ln tau(b) + ln E(b - s) for shifts s (E from WINTAG)

E(l): probability that l given consecutive sites of a living face are empty (site s = {Z_s, Y_s, X_{s+1}}),
from the histogram of maximal empty runs: E(l) = sum_r N_r (r - l + 1)^+ / (samples x b).
Errors: jackknife over chunks (each chunk an independent seed), so time and space correlations are included.
"""
import glob, math, os, sys
import numpy as np
import run as R


def chunks(tag):
    return [R.parse(f) for f in sorted(glob.glob(os.path.join(R.OUT, tag, 'c*.txt')))]


def E_of(hrun, nsamp, b, lmax):
    r = np.arange(len(hrun))
    return np.array([(hrun * np.clip(r - l + 1, 0, None)).sum() / (nsamp * b) for l in range(lmax + 1)])


def jack(cs, f):
    """f(list of chunks) -> vector; returns value on all chunks and jackknife error"""
    full = f(cs); n = len(cs)
    if n < 2:
        return full, np.full_like(full, np.nan)
    # group into at most 40 blocks
    nb = min(n, 40); blocks = [cs[i::nb] for i in range(nb)]
    vals = np.array([f([c for j, bl in enumerate(blocks) if j != i for c in bl]) for i in range(nb)])
    with np.errstate(invalid='ignore'):
        err = np.sqrt((nb - 1) / nb * ((vals - vals.mean(0)) ** 2).sum(0))
    return full, err


def win(tag, lmax=None, quiet=False):
    cs = chunks(tag); b = int(cs[0]['head']['b']); lmax = lmax or b - 1

    def lnE(cc):
        h = sum(c['hrun'] for c in cc); n = sum(c['tot']['nsamp'] for c in cc)
        with np.errstate(divide='ignore'):
            return np.log(E_of(h, n, b, lmax))

    def kap(cc):
        e = lnE(cc); return e[:-1] - e[1:]
    le, ee = jack(cs, lnE); k, ke = jack(cs, kap)
    nsamp = sum(c['tot']['nsamp'] for c in cs); hr = sum(c['hrun'] for c in cs)
    if not quiet:
        print(f'{tag}: b = {b}, {nsamp:.3g} face samples, {len(cs)} chunks')
        print('  l   ln E(l)      +-      k(l) = -ln E(l+1)/E(l)   +-     runs >= l')
        for l in range(1, lmax):
            if not np.isfinite(le[l + 1]):
                break
            print(f'{l:3d} {le[l]:9.4f} {ee[l]:8.4f}   {k[l]:8.4f} {ke[l]:8.4f}   {int(hr[l:].sum())}')
    return le, ee, k, ke


def qsd(tag):
    cs = chunks(tag); b = int(cs[0]['head']['b'])
    hp = sum(c['hpop'] for c in cs); dp = sum(c['dpop'] for c in cs); hm = sum(c['hmax'] for c in cs)
    n = np.arange(len(hp)); tot = hp.sum()
    mean = (hp * n).sum() / tot; var = (hp * n * n).sum() / tot - mean ** 2
    print(f'{tag}: b = {b}, A = {3 * b}; face population in the living state: mean {mean:.3f} ({mean / (3 * b):.4f} per cell), variance {var:.3f}')
    print('  deaths by face population one generation before (share):', ' '.join(f'{k}:{dp[k] / dp.sum():.3f}' for k in range(1, 13)))
    print('  P(n = k), k = 1..12:', ' '.join(f'{hp[k] / tot:.2e}' for k in range(1, 13)))
    print('  P(longest empty run of sites >= m), m = b-8..b-1:', ' '.join(f'{m}:{hm[m:].sum() / hm.sum():.2e}' for m in range(b - 8, b)))
    pre = sum(c['pre'] for c in cs); npre = sum(c['tot']['npre'] for c in cs)
    if npre:
        print('  mean face population 1..12 generations before death:', ' '.join(f'{x / npre:.2f}' for x in pre[:12]))


def life(tags):
    rows = []
    for pat in tags:
        for d in sorted(glob.glob(os.path.join(R.OUT, pat))):
            acc = R.load(os.path.basename(d))
            if acc is None:
                continue
            lt, er, F = R.lntau(acc); rows.append((int(acc['head']['b']), os.path.basename(d), lt, er, F))
    rows.sort()
    prev = None
    for b, tag, lt, er, F in rows:
        s = ''
        if prev and prev[0] != b:
            sl = (lt - prev[2]) / (b - prev[0]); se = math.hypot(er, prev[3]) / (b - prev[0])
            s = f'   slope from b = {prev[0]}: {sl:.4f} +- {se:.4f} per site = {sl / 3:.4f} +- {se / 3:.4f} per cell'
        print(f'{tag:24s} b = {b:2d} A = {3 * b:3d} ln tau = {lt:8.4f} +- {er:.4f} ({F} deaths){s}')
        prev = (b, tag, lt, er, F)
    return rows


def static(wintag, lifetags):
    le, ee, k, ke = win(wintag, quiet=True)
    rows = life(lifetags)
    print(f'ln tau(b) + ln E(b - s), E from {wintag}:')
    print('   b   ' + ' '.join(f's={s:<6d}' for s in range(0, 9)))
    for b, tag, lt, er, F in rows:
        print(f'  {b:2d}  ' + ' '.join(f'{lt + le[b - s]:8.3f}' if b - s < len(le) and np.isfinite(le[b - s]) else '    -   ' for s in range(0, 9)))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'life':
        life(sys.argv[2:])
    elif cmd == 'win':
        win(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == 'qsd':
        for t in sys.argv[2:]:
            qsd(t)
    elif cmd == 'static':
        static(sys.argv[2], sys.argv[3:])
