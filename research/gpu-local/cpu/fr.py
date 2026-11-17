#!/usr/bin/env python3
"""CPU face-torus runner: build, vessel export, validation, runs and the summary (see README.md here).

  python -u research/gpu-local/cpu/fr.py build
  python -u research/gpu-local/cpu/fr.py step A KK B [m=8] [gens=2000]       # stepper vs engine, every generation
  python -u research/gpu-local/cpu/fr.py events A KK B GENS SEED [m=8]      # life by life vs numpy (128 lanes)
  python -u research/gpu-local/cpu/fr.py bench A KK B [m=8] [gens=20000]
  python -u research/gpu-local/cpu/fr.py run A KK B HOURS SEED0 [m=8] [threads=4] [chunk=15]
  python -u research/gpu-local/cpu/fr.py summary [A KK B [m=8]]             # all csv files if no torus given

Vessel: research/shape/tslab.py's tslab(a, kk, b, m) (cells, neighbour graph); faces t = 0 and t = m - 1; rings =
transverse diagonals with >= 3 layers, layer index (s - 1) / 2 with s = d.p mod P_d (tslab.periods), ring order s.
"""
import csv, glob, hashlib, math, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
import tslab  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'gpu-local-cpu')
DATA = os.path.join(ROOT, 'research', 'data', 'gpu_local_cpu')
EXE = os.path.join(SCR, 'fr.exe')
SRC = os.path.join(HERE, 'fr.c')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump.exe')
TDIAGS = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]
W = 4
LANES = 64 * W
os.makedirs(SCR, exist_ok=True)


def gcc():
    for p in glob.glob(os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'WinGet', 'Packages',
                                    'BrechtSanders.WinLibs*', 'mingw64', 'bin', 'gcc.exe')):
        return p
    return 'gcc'


def build():
    if not os.path.exists(EXE) or os.path.getmtime(EXE) < os.path.getmtime(SRC):
        g = gcc(); env = dict(os.environ); env['PATH'] = os.path.dirname(g) + os.pathsep + env['PATH']
        subprocess.check_call([g, '-O3', '-march=native', '-static', '-o', EXE + '.new.exe', SRC, '-lpthread'], env=env)
        os.replace(EXE + '.new.exe', EXE)
    return EXE


def code_id():
    return 'fr.c:' + hashlib.sha1(open(SRC, 'rb').read()).hexdigest()[:10]


class Slab:
    def __init__(self, a, kk, b, m=8):
        v = tslab.tslab(a, kk, b, m)
        self.a, self.kk, self.b, self.m = a, kk, b, m
        self.cells = np.array(v.cells, np.int64)
        self.n = len(self.cells)
        self.nb = v.nb.astype(np.int64)
        self.t = (self.cells.sum(1) - 1) // 2
        self.A = int((self.t == 0).sum()); assert self.A == 3 * a * b
        self.P = tslab.periods(a, kk, b)
        self.rings = []
        for dv, P in zip(TDIAGS, self.P):
            s = (self.cells @ np.array(dv)) % P
            assert sorted(set(s.tolist())) == list(range(1, P, 2))
            if P // 2 >= 3:
                self.rings.append(((s - 1) // 2).astype(np.int64))
        self.path = os.path.join(SCR, f'v_{a}_{kk}_{b}_m{m}.bin')

    def write(self):
        arr = [0x46524631, self.n, self.m, self.A, self.a, self.kk, self.b]
        buf = np.array(arr, '<i4').tobytes() + self.nb.astype('<i4').tobytes() + self.t.astype('<i4').tobytes()
        buf += np.array([len(self.rings)], '<i4').tobytes()
        for r in self.rings:
            buf += np.array([r.max() + 1], '<i4').tobytes() + r.astype('<i4').tobytes()
        open(self.path, 'wb').write(buf)
        return self.path


# ---------------- stepper vs engine ----------------
def engine_nt(a, kk, b, m):
    for Nt in range(m + 3, 400):
        if Nt % b == 0 and Nt % a == 0 and ((Nt // a) * kk) % b == 0:
            return Nt


def engine_sets(v, b0, gens):
    """tile a slab state into the engine's cubic Nt-torus (tslab.validate's construction), run the engine with
    --trace, reduce each generation to slab nodes; the engine state must stay lattice-periodic"""
    a, kk, b, m = v.a, v.kk, v.b, v.m
    Nt = engine_nt(a, kk, b, m)
    reps = {((x * a) % Nt, (x * kk + y * b) % Nt) for x in range(Nt // a) for y in range(Nt // b)}
    kcop = Nt * Nt // (a * b); assert len(reps) == kcop
    pts = set()
    for c in np.nonzero(b0)[0]:
        p0 = v.cells[c]
        for (x, y) in reps:
            q = p0 + 2 * np.array([x, y, -x - y])
            pts.add(tuple(int(z) % (2 * Nt) for z in q))
    assert len(pts) == kcop * int(b0.sum())
    tag = f'{os.getpid()}_{a}_{kk}_{b}_{m}'
    cf, tr = os.path.join(SCR, f'cells_{tag}.txt'), os.path.join(SCR, f'trace_{tag}.txt')
    open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(Nt), '--gens', str(gens), '--no-halt', '--trace', tr],
                   check=True, capture_output=True)
    key = {}
    cube = v.cells.copy(); ax = np.argmax(v.cells % 2, 1); cube[np.arange(v.n), ax] -= 1; cube //= 2
    for i in range(v.n):
        key[(int(cube[i, 0]), int(cube[i, 1]), int(v.t[i]), int(ax[i]))] = i
    sets = []
    with open(tr) as f:
        for line in f:
            parts = line.split()[1:]
            if len(sets) > gens:
                break
            q = np.array([list(map(int, s.split(','))) for s in parts], np.int64).reshape(-1, 3)
            if len(q):
                qa = np.argmax(q % 2, 1); qc = q.copy(); qc[np.arange(len(q)), qa] -= 1; qc //= 2
                tt = qc.sum(1) % Nt
                nodes = []
                for (i, j), t_, x in zip(qc[:, :2], tt, qa):
                    ii, jj = tslab.reduce_ij(int(i), int(j), a, kk, b)
                    nodes.append(key[(ii, jj, int(t_), int(x))])
                u = np.unique(nodes)
            else:
                u = np.zeros(0, np.int64)
            assert len(q) == kcop * len(u), 'engine state not lattice-periodic'
            sets.append(u)
    os.remove(cf); os.remove(tr)
    assert np.array_equal(sets[0], np.nonzero(b0)[0])
    return sets, Nt, kcop


def pack(bits):
    """(LANES, n) bool -> n*W u64 node-major"""
    by = np.packbits(bits.T, axis=1, bitorder='little')        # (n, LANES/8)
    return np.ascontiguousarray(by).view(np.uint64).reshape(-1)


def unpack(words, n):
    by = words.reshape(n, W).view(np.uint8)
    return np.unpackbits(by, axis=1, bitorder='little').T.astype(bool)   # (LANES, n)


def step_check(a, kk, b, m=8, gens=2000):
    exe = build(); v = Slab(a, kk, b, m); vp = v.write()
    rng = np.random.default_rng(1000 + a + 7 * kk + 31 * b + m)
    bits = rng.random((LANES, v.n)) < 0.4
    cases = []
    lanes_by_case = [[0, 63, 64], [100, 127, 128], [255, 200, 129]]
    for c in range(3):
        b0 = np.random.default_rng(77 + c).random(v.n) < 0.4
        sets, Nt, kcop = engine_sets(v, b0, gens + 1)
        cases.append((b0, sets))
        bits[lanes_by_case[c]] = b0
    init = os.path.join(SCR, f'init_{os.getpid()}.bin'); out = os.path.join(SCR, f'tr_{os.getpid()}.bin')

    def run(start):
        pack(start).tofile(init)
        subprocess.run([exe, 'trace', vp, init, out, str(gens)], check=True)
        st = np.fromfile(out, np.uint64).reshape(gens, v.n * W)
        return st
    st = run(bits)
    bad = 0; first = None
    for g in range(gens):
        lb = unpack(st[g], v.n)
        for c, (b0, sets) in enumerate(cases):
            for l in lanes_by_case[c]:
                if not np.array_equal(np.nonzero(lb[l])[0], sets[g + 1]):
                    bad += 1; first = g + 1 if first is None else first
    print(f'torus ({a},{kk}),(0,{b}) x{m} n={v.n}: fr.c trace vs engine torus {Nt} (x{kcop}), {gens} gens x 9 lanes '
          f'(3 engine soups): {"all equal" if bad == 0 else f"{bad} mismatches, first at generation {first}"}')
    ok = bad == 0
    # negative control 1: compare with the next generation
    bad1 = sum(not np.array_equal(np.nonzero(unpack(st[g], v.n)[0])[0], cases[0][1][g + 2]) for g in range(min(300, gens - 1)))
    # negative control 2: one node flipped in the start state of lane 0
    deep = int(np.argmax(np.minimum(v.t, m - 1 - v.t)))
    bits2 = bits.copy(); bits2[0, deep] ^= True
    st2 = run(bits2)
    bad2 = sum(not np.array_equal(np.nonzero(unpack(st2[g], v.n)[0])[0], cases[0][1][g + 1]) for g in range(min(300, gens)))
    print(f'  negative controls (must be > 0): next-generation comparison {bad1} of 300 differ; one node flipped {bad2} of 300 differ')
    os.remove(init); os.remove(out)
    ok = ok and bad1 > 0 and bad2 > 0
    print('STEP', 'OK' if ok else 'FAIL')
    return ok


# ---------------- events vs an independent numpy implementation ----------------
def events_check(a, kk, b, gens, seed, m=8, nl=128, face_every=1):
    """numpy steps lanes 0..nl-1 with a counting rule (not bit-sliced), tests the same definitions every generation
    (faces, firewalls on its own ring layers, period 1-2, the three snapshot levels), takes each new soup from fr.c's
    dump, and must end the same lives at the same generations with the same kinds. face_every > 1: negative control."""
    exe = build(); v = Slab(a, kk, b, m); vp = v.write()
    lv, sp = os.path.join(SCR, f'lives_{os.getpid()}.txt'), os.path.join(SCR, f'soups_{os.getpid()}.bin')
    if face_every == 1 or not os.path.exists(lv):
        print(subprocess.run([exe, 'events', vp, str(seed), str(gens), lv, sp], check=True, capture_output=True, text=True).stdout.strip())
    n = v.n
    rec = np.dtype([('g', '<i8'), ('lane', '<i4'), ('bits', 'u1', (n,))])
    soups = np.fromfile(sp, rec)
    C = [tuple(map(int, l.split())) for l in open(lv)]
    C = sorted(x for x in C if x[0] < nl)
    # own geometry from the cells
    nbm = np.where(v.nb < 0, n, v.nb)
    face0 = np.nonzero(v.t == 0)[0]; face1 = np.nonzero(v.t == m - 1)[0]
    rings = []
    for dv, P in zip(TDIAGS, v.P):
        L = P // 2
        if L >= 3:
            s = (v.cells @ np.array(dv)) % P
            rings.append([np.nonzero(s == 2 * l + 1)[0] for l in range(L)])
    it = {}
    for r in soups:
        if r['lane'] < nl:
            it.setdefault(int(r['lane']), []).append((int(r['g']), r['bits'].astype(bool)))
    ptr = {l: 1 for l in range(nl)}
    x = np.zeros((n + 1, nl), bool)
    for l in range(nl):
        assert it[l][0][0] == 0
        x[:n, l] = it[l][0][1]
    prev = x.copy()
    snaps = [x.copy() for _ in range(3)]
    birth = np.zeros(nl, np.int64)
    lives = []
    for g in range(1, gens + 1):
        cnt = x[nbm].sum(1, dtype=np.int16)                  # (n, 12, nl) -> (n, nl)
        new = np.zeros_like(x)
        new[:n] = (cnt == 4) | (cnt == 5) | (x[:n] & (cnt == 3))
        f0 = new[face0].any(0); f1 = new[face1].any(0)
        deadF = ~(f0 & f1) if g % face_every == 0 else np.zeros(nl, bool)
        fw = np.zeros(nl, bool)
        for lay in rings:
            dead = np.array([~new[idx].any(0) for idx in lay])
            L = len(lay)
            for l in range(L):
                fw |= dead[l] & dead[(l + 1) % L] & dead[(l + 2) % L]
        still = (new == prev).all(0)
        per = np.zeros(nl, bool)
        for s in snaps:
            per |= (new == s).all(0)
        prev = x; x = new
        end = np.nonzero(deadF | fw | still | per)[0]
        for l in end:
            kind = 4 if fw[l] else 1 if deadF[l] else 2 if still[l] else 3
            lives.append((int(l), int(birth[l]), g - int(birth[l]), kind))
            if ptr[l] >= len(it[l]):          # (control only) fr.c ended fewer lives on this lane
                bits = np.random.default_rng(g * 1000 + int(l)).random(n) < 0.4
            else:
                gg, bits = it[l][ptr[l]]; ptr[l] += 1
                if face_every == 1:
                    assert gg == g, f'fr.c reseeded lane {l} at {gg}, numpy ended it at {g}'
            x[:n, l] = bits; prev[:n, l] = bits
            for s in snaps:
                s[:n, l] = bits
            birth[l] = g
        for k, sh in enumerate((10, 14, 18)):
            if g % (1 << sh) == 0:
                snaps[k] = x.copy()
    for l in range(nl):
        lives.append((l, int(birth[l]), gens - int(birth[l]), 0))
    lives.sort()
    same = lives == C
    kinds = {k: sum(1 for c in C if c[3] == k) for k in range(5)}
    print(f'events ({a},{kk}),(0,{b}) x{m}, lanes 0..{nl - 1}, {gens} gens, face test every {face_every}: '
          f'fr.c {len(C)} lives (kinds {kinds}), numpy {len(lives)}: {"IDENTICAL" if same else "DIFFER"}')
    if not same:
        d = [i for i, (p, q) in enumerate(zip(lives, C)) if p != q][:3]
        for i in d:
            print('   numpy', lives[i], 'fr.c', C[i])
    return same


def bench(a, kk, b, m=8, gens=20000):
    exe = build(); v = Slab(a, kk, b, m); vp = v.write()
    print(subprocess.run([exe, 'bench', vp, '1', str(gens)], check=True, capture_output=True, text=True).stdout.strip())


def csv_path(a, kk, b, m):
    return os.path.join(DATA, f'fr_{a}_{kk}_{b}_m{m}.csv')


def run(a, kk, b, hours, seed0, m=8, threads=4, chunk=15.0):
    assert 1 <= threads <= 12 and chunk <= 20
    exe = build(); v = Slab(a, kk, b, m); vp = v.write()
    os.makedirs(DATA, exist_ok=True)
    path = csv_path(a, kk, b, m)
    if os.path.exists(path):
        used = {int(r['seed']) for r in csv.DictReader(open(path))}
        clash = used & set(range(seed0, seed0 + threads))
        assert not clash, f'seeds already used in {path}: {sorted(clash)[:5]}'
    cmd = ' '.join(['python', '-u', 'research/gpu-local/cpu/fr.py', 'run', str(a), str(kk), str(b), str(hours), str(seed0),
                    f'm={m}', f'threads={threads}', f'chunk={chunk}'])
    print(f'fr run ({a},{kk}),(0,{b}) x{m} n={v.n}: {threads} threads, seeds {seed0}..{seed0 + threads - 1}, {hours} h, '
          f'rows every {chunk} min -> {path}', flush=True)
    p = subprocess.Popen([exe, 'run', vp, str(seed0), str(threads), str(hours), str(chunk), path, code_id(), cmd])
    print(f'fr.exe pid {p.pid}', flush=True)
    p.wait()
    summary_file(path)


def summary_file(path):
    rows = list(csv.DictReader(open(path)))
    if not rows:
        return
    by = {}
    for r in rows:
        by.setdefault(int(r['seed']), []).append(r)
    E = sum(int(r['exposure']) for r in rows); F = sum(int(r['face']) for r in rows)
    Wn = sum(int(r['fw']) for r in rows); S = sum(int(r['settled']) for r in rows); Sc = sum(int(r['settled_cyc']) for r in rows)
    wall = sum(float(r['wall_s']) for r in rows)
    rate = F / E if E else 0
    chi2 = 0.0
    for s, rs in by.items():
        e = sum(int(r['exposure']) for r in rs); f = sum(int(r['face']) for r in rs)
        mu = rate * e
        chi2 += (f - mu) ** 2 / mu if mu > 0 else 0
    r0 = rows[0]
    lf = math.log(2 * E / F) if F else float('nan')
    print(f'torus ({r0["torus"]}) x{r0["m"]} A = {r0["A"]}: {len(rows)} rows, {len(by)} seeds, {wall / 3600:.2f} thread-hours, '
          f'exposure {E:.4g}, face {F}, firewall {Wn}, settled {S} (of which cycles > 2: {Sc})')
    print(f'  ln tau_face = {lf:.4f} +- {1 / math.sqrt(max(F, 1)):.4f};  chi2 across seeds {chi2:.1f} on {len(by) - 1}' +
          (f';  ln tau_fw = {math.log(E / Wn):.3f} +- {1 / math.sqrt(Wn):.3f}' if Wn else ''))


def summary(a=None, kk=None, b=None, m=8):
    paths = [csv_path(a, kk, b, m)] if a is not None else sorted(glob.glob(os.path.join(DATA, 'fr_*.csv')))
    for p in paths:
        summary_file(p)


if __name__ == '__main__':
    what = sys.argv[1]
    pos = [x for x in sys.argv[2:] if '=' not in x]
    opt = {k: float(v) if '.' in v else int(v) for k, v in (x.split('=') for x in sys.argv[2:] if '=' in x)}
    if what == 'build':
        print(build())
    elif what == 'step':
        sys.exit(0 if step_check(*map(int, pos[:3]), **opt) else 1)
    elif what == 'events':
        ok = events_check(*map(int, pos[:5]), **opt)
        if 'face_every' not in opt:
            ctl = events_check(*map(int, pos[:5]), face_every=2, **opt)
            print('negative control (face test every 2nd generation) must differ:', 'differs' if not ctl else 'IDENTICAL (FAIL)')
            ok = ok and not ctl
        print('EVENTS', 'OK' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    elif what == 'bench':
        bench(*map(int, pos[:3]), **opt)
    elif what == 'run':
        run(*map(int, pos[:3]), float(pos[3]), int(pos[4]), **opt)
    elif what == 'summary':
        summary(*map(int, pos[:3]), **opt) if pos else summary()
