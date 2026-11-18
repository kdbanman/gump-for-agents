#!/usr/bin/env python3
"""research/dying2: build dy.c, check it, run it (see README.md here).

  P -u research/dying2/dy.py build
  P -u research/dying2/dy.py step A KK B [m=8] [gens=2000]          # dy.c's stepper vs the engine, every generation
  P -u research/dying2/dy.py events A KK B GENS SEED PBAR KDUMP NULLSH H R [m=8]   # everything vs numpy, lanes 0..127
  P -u research/dying2/dy.py pbar A KK B [gens=300000]              # stationary P (one thread, lanes 0..255)
  P -u research/dying2/dy.py run A KK B HOURS SEED0 PBAR KDUMP [threads=1] [nullsh=16] [H=4096] [R=1024]
                                  [maxdeath=..] [maxrec=..] [chunk=10]

Vessel: research/shape/tslab.py's tslab(a, kk, b, m) through research/gpu-local/cpu/fr.py's Slab (imported, with its
scratch directory redirected here; nothing of fr.py's is built or written). Outputs under research/scratch/dying2/.
"""
import os, subprocess, sys, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu-local', 'cpu'))
import fr  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'dying2')
os.makedirs(SCR, exist_ok=True)
fr.SCR = SCR                       # Slab paths and engine_sets temp files go here, never to gpu-local-cpu
EXE = os.path.join(SCR, 'dy.exe')
SRC = os.path.join(HERE, 'dy.c')
W, LANES, T0 = 4, 256, 512


def build():
    if not os.path.exists(EXE) or os.path.getmtime(EXE) < os.path.getmtime(SRC):
        g = fr.gcc(); env = dict(os.environ); env['PATH'] = os.path.dirname(g) + os.pathsep + env['PATH']
        subprocess.check_call([g, '-O3', '-march=native', '-static', '-o', EXE + '.new.exe', SRC, '-lpthread'], env=env)
        os.replace(EXE + '.new.exe', EXE)
    return EXE


def slab(a, kk, b, m=8):
    v = fr.Slab(a, kk, b, m)
    v.write()
    return v


# ---------------- records ----------------
def read_records(path, A, with_bits=True):
    """yields dicts: type seed lane face birth g age a1 a2 a3 a4 L, and bits (L, 2, A) bool (face, beneath)"""
    nb8 = (A + 7) // 8
    raw = np.fromfile(path, np.uint8)
    out, pos, N = [], 0, len(raw)
    while pos + 96 <= N:
        h = raw[pos:pos + 96].view('<i8')
        L = int(h[11]); sz = 96 + L * 2 * nb8
        if pos + sz > N:
            break                                   # a record still being written
        r = dict(zip(['type', 'seed', 'lane', 'face', 'birth', 'g', 'age', 'a1', 'a2', 'a3', 'a4', 'L'], map(int, h)))
        if with_bits:
            by = raw[pos + 96:pos + sz].reshape(L, 2, nb8)
            r['bits'] = np.unpackbits(by, axis=2, bitorder='little')[:, :, :A].astype(bool)
        out.append(r); pos += sz
    return out


def parse_stats_line(line, A):
    t = line.split()
    keys = ['seed', 'chunk', 'utc', 'wall', 'gens', 'lanegens', 'face', 'fw', 's12', 'scyc', 'deaths_ok', 'dead_noexc',
            'expo', 'sumP', 'sumP2', 'ndd', 'nrd', 'nnull', 'rec_skipped', 'open']
    d = {}
    for k, x in zip(keys, t):
        d[k] = x if k == 'utc' else float(x) if k == 'wall' else int(x)
    i = t.index('H'); d['hist'] = np.array(list(map(int, t[i + 1:i + 2 + A])))
    j = t.index('E'); d['exc'] = np.array(list(map(int, t[j + 1:j + 1 + 3 * (A + 1)]))).reshape(A + 1, 3)
    return d


# ---------------- stepper vs engine (fr.py's step_check with dy.exe) ----------------
def step_check(a, kk, b, m=8, gens=2000):
    exe = build(); v = slab(a, kk, b, m); vp = v.path
    rng = np.random.default_rng(1000 + a + 7 * kk + 31 * b + m)
    bits = rng.random((LANES, v.n)) < 0.4
    cases = []
    lanes_by_case = [[0, 63, 64], [100, 127, 128], [255, 200, 129]]
    for c in range(3):
        b0 = np.random.default_rng(77 + c).random(v.n) < 0.4
        sets, Nt, kcop = fr.engine_sets(v, b0, gens + 1)
        cases.append((b0, sets))
        bits[lanes_by_case[c]] = b0
    init = os.path.join(SCR, f'init_{os.getpid()}.bin'); out = os.path.join(SCR, f'tr_{os.getpid()}.bin')

    def run(start):
        fr.pack(start).tofile(init)
        subprocess.run([exe, 'trace', vp, init, out, str(gens)], check=True)
        return np.fromfile(out, np.uint64).reshape(gens, v.n * W)
    st = run(bits)
    bad = 0
    for g in range(gens):
        lb = fr.unpack(st[g], v.n)
        for c, (b0, sets) in enumerate(cases):
            for l in lanes_by_case[c]:
                bad += not np.array_equal(np.nonzero(lb[l])[0], sets[g + 1])
    print(f'torus ({a},{kk}),(0,{b}) x{m} n={v.n}: dy.c trace vs engine torus {Nt} (x{kcop}), {gens} gens x 9 lanes: '
          f'{"all equal" if bad == 0 else f"{bad} mismatches"}')
    bad1 = sum(not np.array_equal(np.nonzero(fr.unpack(st[g], v.n)[0])[0], cases[0][1][g + 2]) for g in range(min(300, gens - 1)))
    deep = int(np.argmax(np.minimum(v.t, m - 1 - v.t)))
    bits2 = bits.copy(); bits2[0, deep] ^= True
    st2 = run(bits2)
    bad2 = sum(not np.array_equal(np.nonzero(fr.unpack(st2[g], v.n)[0])[0], cases[0][1][g + 1]) for g in range(min(300, gens)))
    print(f'  negative controls (must be > 0): next generation {bad1} of 300 differ; one node flipped {bad2} of 300 differ')
    os.remove(init); os.remove(out)
    ok = bad == 0 and bad1 > 0 and bad2 > 0
    print('STEP', 'OK' if ok else 'FAIL')
    return ok


# ---------------- everything vs numpy ----------------
def events_check(a, kk, b, gens, seed, pbar, kdump, nullsh, H, R, m=8, nl=128):
    """numpy steps lanes 0..nl-1 by the counting rule from dy.c's soups, applies fr.c's event definitions and dy.c's
    excursion / dump definitions itself, and must give the same lives, the same records (bit for bit) and the same
    tallies. The firewall / settled tests are fr.events_check's (copied)."""
    exe = build(); v = slab(a, kk, b, m); n, A = v.n, v.A
    od = os.path.join(SCR, f'ev_{a}_{kk}_{b}_{seed}'); os.makedirs(od, exist_ok=True)
    print(subprocess.run([exe, 'events', v.path, str(seed), str(gens), od, str(pbar), str(kdump), str(nullsh), str(H), str(R),
                          str(nl)], check=True, capture_output=True, text=True).stdout.strip())
    rec = np.dtype([('g', '<i8'), ('lane', '<i4'), ('bits', 'u1', (n,))])
    soups = np.fromfile(os.path.join(od, 'soups.bin'), rec)
    C = sorted(tuple(map(int, l.split())) for l in open(os.path.join(od, 'lives.txt')))
    C = [x for x in C if x[0] < nl]
    Crec = read_records(os.path.join(od, 'dump.bin'), A)
    Cst = parse_stats_line(open(os.path.join(od, 'stats.txt')).read(), A)
    nbm = np.where(v.nb < 0, n, v.nb)
    lay = [np.arange(0, A), np.arange(A, 2 * A), np.arange((m - 2) * A, (m - 1) * A), np.arange((m - 1) * A, m * A)]
    rings = []
    for dv, Pd in zip(fr.TDIAGS, v.P):
        L = Pd // 2
        if L >= 3:
            s = (v.cells @ np.array(dv)) % Pd
            rings.append([np.nonzero(s == 2 * l + 1)[0] for l in range(L)])
    it = {}
    for r in soups:
        if r['lane'] < nl:
            it.setdefault(int(r['lane']), []).append((int(r['g']), r['bits'].astype(bool)))
    ptr = {l: 1 for l in range(nl)}
    x = np.zeros((n + 1, nl), bool)
    for l in range(nl):
        x[:n, l] = it[l][0][1]
    prev = x.copy(); snaps = [x.copy() for _ in range(3)]
    birth = np.zeros(nl, np.int64)
    ring = np.zeros((H, 4, A, nl), bool)
    prevok = np.zeros((2, nl), bool); prevab = np.zeros((2, nl), bool); inexc = np.zeros((2, nl), bool)
    minp = np.zeros((2, nl), np.int64); gst = np.zeros((2, nl), np.int64); gmn = np.zeros((2, nl), np.int64)
    expo = sumP = sumP2 = 0; hist = np.zeros(A + 1, np.int64); exc = np.zeros((A + 1, 3), np.int64)
    deaths_ok = dead_noexc = 0
    lives, recs = [], []

    def mk(typ, l, f, g, L, a1, a2, a3):
        fl, bl = (0, 1) if f == 0 else (3, 2)
        bits = np.stack([ring[(gg % H), [fl, bl], :, l] for gg in range(g - L + 1, g + 1)])
        return (typ, l, f, g, int(birth[l]), g - int(birth[l]), int(a1), int(a2), int(a3), L, bits)
    for g in range(1, gens + 1):
        cnt = x[nbm].sum(1, dtype=np.int16)
        new = np.zeros_like(x)
        new[:n] = (cnt == 4) | (cnt == 5) | (x[:n] & (cnt == 3))
        f0 = new[lay[0]].any(0); f1 = new[lay[3]].any(0)
        deadF = ~(f0 & f1)
        fw = np.zeros(nl, bool)
        for ly in rings:
            dead = np.array([~new[idx].any(0) for idx in ly]); L = len(ly)
            for l in range(L):
                fw |= dead[l] & dead[(l + 1) % L] & dead[(l + 2) % L]
        still = (new == prev).all(0)
        per = np.zeros(nl, bool)
        for s in snaps:
            per |= (new == s).all(0)
        prev = x; x = new
        for q in range(4):
            ring[g % H, q] = x[lay[q]]
        P = np.stack([x[lay[0]].sum(0), x[lay[3]].sum(0)])
        age = g - birth; ok = age > T0
        for f in range(2):
            ab = P[f] >= pbar
            was = inexc[f].copy()
            lower = was & (P[f] < minp[f])
            gmn[f][lower] = g; minp[f][lower] = P[f][lower]
            recov = was & ab
            for l in np.nonzero(recov)[0]:
                mp = int(minp[f][l]); exc[mp, 0] += 1
                if mp <= kdump:
                    recs.append(mk(2, l, f, g, int(min(R, age[l] - T0)), gst[f][l], gmn[f][l], mp))
            inexc[f][recov] = False
            st = ~was & ok & prevok[f] & prevab[f] & ~ab
            inexc[f][st] = True; minp[f][st] = P[f][st]; gmn[f][st] = g; gst[f][st] = g
            prevab[f] = ab; prevok[f] = ok
            expo += int(ok.sum()); sumP += int(P[f][ok].sum()); sumP2 += int((P[f][ok] ** 2).sum())
            hist += np.bincount(P[f][ok], minlength=A + 1)
        if g % (1 << nullsh) == 0:
            nf = (g >> nullsh) & 1
            for l in np.nonzero(ok)[0]:
                recs.append(mk(3, l, nf, g, 1, P[nf][l], 0, 0))
        end = np.nonzero(deadF | fw | still | per)[0]
        dd = np.stack([~f0, ~f1])
        for l in end:
            kind = 4 if fw[l] else 1 if deadF[l] else 2 if still[l] else 3
            lives.append((int(l), int(birth[l]), g - int(birth[l]), kind))
            for f in range(2):
                if kind == 1 and dd[f][l]:
                    if age[l] > T0:
                        deaths_ok += 1
                        if inexc[f][l]:
                            exc[minp[f][l], 1] += 1
                        else:
                            dead_noexc += 1
                        recs.append(mk(1, l, f, g, int(min(H, age[l] - T0)), gst[f][l] if inexc[f][l] else -1,
                                       P[1 - f][l], int(dd[0][l] and dd[1][l])))
                elif inexc[f][l]:
                    exc[minp[f][l], 2] += 1
            gg, bits = it[l][ptr[l]]; ptr[l] += 1
            assert gg == g, f'dy.c reseeded lane {l} at {gg}, numpy ended it at {g}'
            x[:n, l] = bits; prev[:n, l] = bits
            for s in snaps:
                s[:n, l] = bits
            birth[l] = g; prevok[:, l] = False; inexc[:, l] = False
        for k, sh in enumerate((10, 14, 18)):
            if g % (1 << sh) == 0:
                snaps[k] = x.copy()
    for l in range(nl):
        lives.append((l, int(birth[l]), gens - int(birth[l]), 0))
    lives.sort()
    ok_lives = lives == C
    Ck = sorted(((r['type'], r['lane'], r['face'], r['g'], r['birth'], r['age'], r['a1'], r['a2'], r['a3'], r['L']), r['bits'])
                for r in Crec if r['lane'] < nl) if Crec else []
    Nk = sorted((t[:10], t[10]) for t in recs)
    ok_rec = len(Ck) == len(Nk) and all(c[0] == q[0] and np.array_equal(c[1], q[1]) for c, q in zip(Ck, Nk))
    ok_st = (Cst['expo'] == expo and Cst['sumP'] == sumP and Cst['sumP2'] == sumP2 and np.array_equal(Cst['hist'], hist)
             and np.array_equal(Cst['exc'], exc) and Cst['deaths_ok'] == deaths_ok and Cst['dead_noexc'] == dead_noexc)
    types = {t: sum(1 for r in Nk if r[0][0] == t) for t in (1, 2, 3)}
    print(f'events ({a},{kk}),(0,{b}) x{m}, lanes 0..{nl - 1}, {gens} gens: lives {len(C)} {"IDENTICAL" if ok_lives else "DIFFER"}; '
          f'records {len(Ck)} (numpy {len(Nk)}: deaths {types[1]}, recovered {types[2]}, null {types[3]}) '
          f'{"IDENTICAL" if ok_rec else "DIFFER"}; tallies (exposure {expo}, excursions {int(exc.sum())}, deaths at age > T0 '
          f'{deaths_ok}, not in an excursion {dead_noexc}) {"IDENTICAL" if ok_st else "DIFFER"}')
    if not ok_rec:
        for c, q in zip(Ck, Nk):
            if c[0] != q[0] or not np.array_equal(c[1], q[1]):
                print('  first difference: dy.c', c[0], 'numpy', q[0]); break
    ok = ok_lives and ok_rec and ok_st and types[1] > 0 and types[2] > 0 and types[3] > 0
    print('EVENTS', 'OK' if ok else 'FAIL')
    return ok


def pbar(a, kk, b, m=8, gens=300000):
    exe = build(); v = slab(a, kk, b, m)
    od = os.path.join(SCR, f'pbar_{a}_{kk}_{b}'); os.makedirs(od, exist_ok=True)
    print(subprocess.run([exe, 'events', v.path, '424242', str(gens), od, '1000', '-1', '62', '16', '16', '256'],
                         check=True, capture_output=True, text=True).stdout.strip())
    st = parse_stats_line(open(os.path.join(od, 'stats.txt')).read(), v.A)
    mu = st['sumP'] / st['expo']; sd = (st['sumP2'] / st['expo'] - mu * mu) ** 0.5
    print(f'({a},{kk}),(0,{b}) A={v.A}: Pbar = {mu:.3f}, sigma_P = {sd:.3f} over {st["expo"]} face-generations at age > {T0}')
    return mu, sd


def run(a, kk, b, hours, seed0, pb, kdump, threads=1, nullsh=16, H=4096, R=1024, maxdeath=1 << 40, maxrec=1 << 40,
        chunk=10.0, m=8):
    exe = build(); v = slab(a, kk, b, m)
    od = os.path.join(SCR, f'run_{a}_{kk}_{b}'); os.makedirs(od, exist_ok=True)
    for t in range(threads):
        assert not os.path.exists(os.path.join(od, f'stats_{seed0 + t}.txt')), f'seed {seed0 + t} already used in {od}'
    args = [exe, 'run', v.path, str(seed0), str(threads), str(hours), str(chunk), od, str(pb), str(kdump), str(nullsh),
            str(H), str(R), str(maxdeath), str(maxrec)]
    print('dy run', ' '.join(args[2:]), flush=True)
    p = subprocess.Popen(args)
    print(f'dy.exe pid {p.pid}', flush=True)
    p.wait()


if __name__ == '__main__':
    what = sys.argv[1]
    pos = [x for x in sys.argv[2:] if '=' not in x]
    opt = {k: float(v) if '.' in v else int(v) for k, v in (x.split('=') for x in sys.argv[2:] if '=' in x)}
    if what == 'build':
        print(build())
    elif what == 'step':
        sys.exit(0 if step_check(*map(int, pos[:3]), **opt) else 1)
    elif what == 'events':
        sys.exit(0 if events_check(*map(int, pos[:5]), float(pos[5]), *map(int, pos[6:10]), **opt) else 1)
    elif what == 'pbar':
        pbar(*map(int, pos[:3]), **opt)
    elif what == 'run':
        run(*map(int, pos[:3]), float(pos[3]), int(pos[4]), float(pos[5]), int(pos[6]), **opt)
