#!/usr/bin/env python3
"""Validate nzd.c (research/blast/density) before any row is trusted.

    python3 research/blast/density/validate.py [GENS=1200]

1. Oracle: with no noise the stepper is gump bit for bit (reference/oracle.py) on the hull at R = 11 and R = 9: three
   soups in lanes 0, 37, 511, every cell, every generation; the watched face's population, the "another face is
   empty" bit, the number of empty faces. Negative control: one neighbour swapped must fail.
2. The coins: with a different bias at each depth, from an all-dead and from an all-live state, the share of the
   cells of N at depth d set alive by one noise call is q p_d and the share set dead is q (1 - p_d), q = 1 - (1 - 1/B)^M;
   no cell outside N changes; the fair path (bias 1/2) and the comparison path (bias 1/2 forced) both give 1/2.
   The shuffled coin copies the current state of a random cell of the source layer: with the layer all alive (all
   dead) nothing changes; with only the layer's cells outside N alive, an N cell set alive is a copy.
   Negative control: a coin of bias 0.6 read as 0.5 must fail the test.
3. Same BRUTE line as research/blast/noisy/nz.c with every bias 1/2 (four settings); negative controls: the bias-1/2
   coin through the comparison path (NZD_GENERAL=1) and another seed must give different lines.
4. The excursion counts (REC line) recomputed here from a dump of every lane's watched population and other-face bit.
5. The layer groups: sizes against their definition here; the group "face" reproduces the watched population.
"""
import ctypes, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle

GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
S = os.path.join(ROOT, 'research', 'scratch', 'blast', 'density'); os.makedirs(S, exist_ok=True)
so = os.path.join(S, 'libnzd.so'); exe = os.path.join(S, 'nzd_val'); nzexe = os.path.join(S, 'nz_val')
subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-DLIB', '-o', so, os.path.join(HERE, 'nzd.c'), '-lm'])
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', exe, os.path.join(HERE, 'nzd.c'), '-lm'])
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', nzexe, os.path.join(ROOT, 'research', 'blast', 'noisy', 'nz.c'), '-lm'])
SIG = [np.array((1 - 2 * (f & 1), 1 - 2 * ((f >> 1) & 1), 1 - 2 * ((f >> 2) & 1))) for f in range(8)]
EXPECT = {9: 45, 11: 63, 13: 84, 15: 108}
ok_all = True
VP = ctypes.c_void_p


def report(name, err):
    global ok_all
    print(f'{name}: ' + ('OK' if err is None else 'FAILED: ' + err), flush=True)
    ok_all &= err is None


def report_neg(name, err):
    global ok_all
    print(f'{name} (negative control): ' + ('NOT DETECTED (bad)' if err is None else 'fails as it must: ' + err), flush=True)
    ok_all &= err is not None


def geometry(lib, R, DW=6, DO=3):
    n = lib.geom_init(R, DW, DO); A = lib.v_A()
    co = np.zeros((n, 3), np.int32); lib.v_coords(co.ctypes.data_as(VP))
    return n, A, co


def oracle_check(R, swap):
    lib = ctypes.CDLL(so)
    n, A, co = geometry(lib, R)
    H = 2 * (R + 3); c0 = H // 2
    m = oracle.masks(H); ix = tuple((co + c0).T)
    cc = np.indices((H, H, H)) - c0
    inside = (m[0] | m[1] | m[2]) & (np.abs(cc).sum(0) <= R)
    assert int(inside.sum()) == n and inside[ix].all() and A == EXPECT[R]
    faces = [np.where(co @ s == R)[0] for s in SIG]
    assert all(len(f) == A for f in faces) and (faces[0] == np.arange(A)).all()
    if swap:
        i = n // 2; lib.v_swap(i, 5, int((lib.v_nb(i, 5) + 7) % n))
    lanes = [0, 37, 511]; rng = np.random.default_rng(3000 + R)
    lib.v_clear(); xs = []
    for lane in lanes:
        x = (inside & (rng.random((H, H, H)) < 0.35)).astype(np.int8); xs.append(x)
        lib.v_set(lane, np.ascontiguousarray(x[ix].astype(np.uint8)).ctypes.data_as(VP))
    buf = np.zeros(n, np.uint8)
    for g in range(1, GENS + 1):
        lib.v_step()
        for k, lane in enumerate(lanes):
            xs[k] = oracle.step(xs[k], m)
            lib.v_get(lane, buf.ctypes.data_as(VP)); ref = xs[k][ix].astype(np.uint8)
            if not (buf == ref).all():
                return f'state differs at generation {g}, lane {lane} ({int((buf != ref).sum())} cells)'
            if xs[k].sum() != ref.sum():
                return f'oracle has live cells outside the hull at generation {g}'
            if lib.v_pop(lane) != int(ref[:A].sum()):
                return f'watched-face population differs at generation {g}'
            empt = [not ref[faces[f]].any() for f in range(8)]
            if lib.v_od(lane) != int(any(empt[1:])) or lib.v_ndead(lane) != sum(empt):
                return f'empty-face bookkeeping differs at generation {g}'
    return None


def coin_check(R, DW, M, biases, general=0, read_as=None, trials=60):
    """biases: dict depth -> p (or -1 for shuffle is handled elsewhere). read_as: what the test assumes (negative control)."""
    lib = ctypes.CDLL(so)
    lib.set_coin.argtypes = [ctypes.c_int, ctypes.c_double]
    n, A, co = geometry(lib, R, DW, 3)
    lib.set_general(general)
    for d, p in biases.items():
        lib.set_coin(d, p)
    nN = lib.v_nN(); B = lib.v_B(); Nc = np.zeros(nN, np.int32); lib.v_ncells(Nc.ctypes.data_as(VP))
    dep = (R - co @ SIG[0]) // 2
    q = 1 - (1 - 1 / B) ** M
    lib.v_seed(12345)
    inN = np.zeros(n, bool); inN[Nc] = True
    ones = np.zeros(n); zeros = np.zeros(n); buf = np.zeros(n, np.uint8)
    for start in (0, 1):
        for t in range(trials):
            lib.v_clear()
            st = np.full(n, start, np.uint8)
            for lane in range(512):
                lib.v_set(lane, st.ctypes.data_as(VP))
            lib.v_noise(M)
            for lane in range(0, 512, 7):
                lib.v_get(lane, buf.ctypes.data_as(VP))
                if (buf[~inN] != start).any():
                    return 'a cell outside N changed'
                if start == 0: ones += buf
                else: zeros += 1 - buf
    nl = len(range(0, 512, 7)) * trials
    for d in sorted(set(dep[Nc])):
        sel = inN & (dep == d); cells = sel.sum() * nl
        p = (read_as or biases).get(d, 0.5)
        fo, fz = ones[sel].sum() / cells, zeros[sel].sum() / cells
        for name, f, want in (('alive', fo, q * p), ('dead', fz, q * (1 - p))):
            sd = np.sqrt(want * (1 - want) / cells)
            if abs(f - want) > 5 * sd:
                return f'depth {d}: share set {name} {f:.5f}, expected {want:.5f} +- {sd:.5f}'
    return None


def shuffle_check(R, DW, M, core):
    lib = ctypes.CDLL(so)
    lib.set_coin.argtypes = [ctypes.c_int, ctypes.c_double]
    n, A, co = geometry(lib, R, DW, 3)
    lib.set_srccore(core)
    for d in range(1, 30):
        lib.set_coin(d, -1.0)
    nN = lib.v_nN(); Nc = np.zeros(nN, np.int32); lib.v_ncells(Nc.ctypes.data_as(VP))
    dep = (R - co @ SIG[0]) // 2; dmo = np.min([(R - co @ SIG[f]) // 2 for f in range(1, 8)], 0)
    inN = np.zeros(n, bool); inN[Nc] = True
    for d in sorted(set(dep[Nc])):
        d = int(d); ns = lib.v_nsrc(d); src = np.zeros(ns, np.int32); lib.v_srcs(d, src.ctypes.data_as(VP))
        want = np.where((dep == d) & ((dmo >= 3) if core else True))[0]
        if not (len(src) == len(want) and (np.sort(src) == want).all()):
            return f'shuffle source of depth {d} differs from its definition'
    lib.v_seed(777); buf = np.zeros(n, np.uint8)
    for fill in (0, 1):     # the whole hull alive (dead): a copy changes nothing
        st = np.full(n, fill, np.uint8); lib.v_clear()
        for lane in range(512): lib.v_set(lane, st.ctypes.data_as(VP))
        for t in range(20):
            lib.v_noise(M)
        for lane in range(0, 512, 5):
            lib.v_get(lane, buf.ctypes.data_as(VP))
            if (buf != fill).any():
                return f'all {"alive" if fill else "dead"}: a shuffled coin changed a cell'
    # only the source cells outside N alive: after one call, the share of N cells at depth d set alive is
    # q * (alive share of the source) to first order (earlier darts of the call change the source a little)
    st = np.zeros(n, np.uint8)
    st[~inN] = 1
    lib.v_clear()
    for lane in range(512): lib.v_set(lane, st.ctypes.data_as(VP))
    lib.v_noise(M)
    if not core:
        B = lib.v_B(); q = 1 - (1 - 1 / B) ** M; tot = {}
        for lane in range(512):
            lib.v_get(lane, buf.ctypes.data_as(VP))
            if (buf[~inN] != 1).any():
                return 'a cell outside N changed'
            for d in sorted(set(dep[Nc])):
                sel = inN & (dep == d); tot.setdefault(d, [0, 0]); tot[d][0] += buf[sel].sum(); tot[d][1] += sel.sum()
        for d, (k, c) in tot.items():
            f_src = ((dep == d) & ~inN).sum() / (dep == d).sum(); want = q * f_src; sd = np.sqrt(want * (1 - want) / c)
            if abs(k / c - want) > 5 * sd + 0.01:
                return f'depth {d}: share {k / c:.4f}, expected about {want:.4f}'
    return None


def cond_check(R, DW, M, trials=40):
    """conditioned coins: bias p_m by m = live face neighbours. Face all dead (m = 0) or all alive (m = 2 at depth 1,
    m = 1 at depth 2); N cells start dead (alive) and the share set alive (dead) is q p_m (q (1 - p_m))."""
    lib = ctypes.CDLL(so)
    lib.set_coin.argtypes = [ctypes.c_int, ctypes.c_double]; lib.set_ccoin.argtypes = [ctypes.c_int] + [ctypes.c_double] * 3
    n, A, co = geometry(lib, R, DW, 3)
    tab = {1: (0.1, 0.5, 0.8), 2: (0.3, 0.7, 0.5)}
    for d, t in tab.items(): lib.set_ccoin(d, *t)
    for d in range(3, 30): lib.set_coin(d, 0.25)
    nN = lib.v_nN(); B = lib.v_B(); Nc = np.zeros(nN, np.int32); lib.v_ncells(Nc.ctypes.data_as(VP))
    dep = (R - co @ SIG[0]) // 2; q = 1 - (1 - 1 / B) ** M
    inN = np.zeros(n, bool); inN[Nc] = True; buf = np.zeros(n, np.uint8); lib.v_seed(4321)
    for face in (0, 1):
        for start in (0, 1):
            acc = np.zeros(n); nl = 0
            for t in range(trials):
                st = np.full(n, start, np.uint8); st[:A] = face; lib.v_clear()
                for lane in range(512): lib.v_set(lane, st.ctypes.data_as(VP))
                lib.v_noise(M)
                for lane in range(0, 512, 7):
                    lib.v_get(lane, buf.ctypes.data_as(VP)); nl += 1
                    if (buf[~inN] != st[~inN]).any(): return 'a cell outside N changed'
                    acc += buf if start == 0 else 1 - buf
            for d in sorted(set(dep[Nc])):
                sel = inN & (dep == d); cells = sel.sum() * nl
                if d in tab:
                    p = tab[d][0] if face == 0 else tab[d][2 if d == 1 else 1]
                else:
                    p = 0.25
                want = q * (p if start == 0 else 1 - p); f = acc[sel].sum() / cells; sd = np.sqrt(want * (1 - want) / cells)
                if abs(f - want) > 5 * sd:
                    return f'face {face}, start {start}, depth {d}: share {f:.5f}, expected {want:.5f} +- {sd:.5f}'
    return None


def brute(exe_, R, seed, gens, M, DW, extra=None, env=None):
    cmd = [exe_, str(R), 'brute', str(seed), str(gens), str(M), str(DW), '3'] + ([extra] if extra else [])
    e = dict(os.environ); e.update(env or {})
    out = subprocess.run(cmd, capture_output=True, text=True, env=e, check=True).stdout
    return out


def first_line(out):
    return [l for l in out.splitlines() if l.startswith('BRUTE')][0]


def rec_check():
    path = os.path.join(S, 'val_dump.bin')
    gens = 30000
    out = brute(exe, 9, 31, gens, 16, 6, None, {'NZD_DUMP': path})
    rec = [l for l in out.splitlines() if l.startswith('REC')][0].split()
    H = int(rec[2]); got = {}
    for tok in rec[4:]:
        k, v = tok.split(':'); got[int(k)] = tuple(int(x) for x in v.split('/'))
    data = np.fromfile(path, np.uint8).reshape(-1, 2, 512)
    assert data.shape[0] == gens + 200
    NK = np.zeros(16, int); DK = np.zeros(16, int); CK = np.zeros(16, int)
    if ' settled 0 ' not in first_line(out):
        return 'a settled life in the validation run (not modelled here)'
    for l in range(512):
        age = 0; arm = [False] * 16; pend = [False] * 16
        for g in range(data.shape[0]):
            p = int(data[g, 0, l]); odl = int(data[g, 1, l]); age += 1
            counted = g >= 200 and age > 200
            if p >= H:
                pend = [False] * 16; arm = [True] * 16
            else:
                for k in range(16):
                    if arm[k] and p <= k:
                        arm[k] = False
                        if counted: pend[k] = True; NK[k] += 1
            if p == 0 or odl:
                for k in range(16):
                    if pend[k]:
                        if p == 0: DK[k] += 1
                        else: CK[k] += 1
                pend = [False] * 16; arm = [False] * 16; age = 0
    for k in range(16):
        if got[k] != (NK[k], DK[k], CK[k]):
            return f'k = {k}: nzd {got[k]}, here {(NK[k], DK[k], CK[k])}'
    os.remove(path)
    return None


def layer_check():
    out = brute(exe, 11, 5, 3000, 0, 1, None, {'NZD_LAYERS': '1'})
    lib = ctypes.CDLL(so); n, A, co = geometry(lib, 11, 1, 3); R = 11
    dep = (R - co @ SIG[0]) // 2; dmo = np.min([(R - co @ SIG[f]) // 2 for f in range(1, 8)], 0)
    sizes = {f'full{k}': int((dep == k).sum()) for k in range(1, 6)}
    sizes.update({f'core{k}': int(((dep == k) & (dmo >= 3)).sum()) for k in range(1, 6)})
    sizes['core6+'] = int(((dep >= 6) & (dmo >= 3)).sum()); sizes['face'] = A
    for l in out.splitlines():
        if l.startswith('LAYER'):
            t = l.split()
            if int(t[3]) != sizes[t[1]]:
                return f'group {t[1]} has {t[3]} cells, definition {sizes[t[1]]}'
        if l.startswith('BYPOP face'):
            for tok in l.split()[3:]:
                p, dens, cnt = tok.split(':')
                if float(cnt) > 0 and abs(float(dens) * A - int(p)) > 0.6e-4 * A:   # printed to 4 decimals
                    return f'face group at population {p} reads {float(dens) * A}'
    bias = [l for l in out.splitlines() if l.startswith('BIAS')][0]
    for k in range(1, 6):
        if f' {k}({sizes[f"core{k}"]}):' not in bias:
            return f'core{k} size differs from the replaced cells at depth {k}'
    return None


for R in (11, 9):
    report(f'1. oracle, R = {R}, {GENS} generations x 3 lanes, no noise', oracle_check(R, False))
    report_neg(f'1. oracle, R = {R}, one neighbour swapped', oracle_check(R, True))
report('2. coins by depth (R = 11, DW = 1, M = 256): 0.1, 0.9, 0.3, 0.42, rest 0.7', coin_check(11, 1, 256, {1: 0.1, 2: 0.9, 3: 0.3, 4: 0.42, 5: 0.7, 6: 0.7, 7: 0.7, 8: 0.7}))
report('2. fair path (every bias 1/2)', coin_check(11, 1, 256, {}))
report('2. bias 1/2 through the comparison path', coin_check(11, 2, 128, {d: 0.5 for d in range(1, 12)}, general=1))
report_neg('2. coins of bias 0.6 read as 0.5', coin_check(11, 1, 256, {d: 0.6 for d in range(1, 12)}, read_as={d: 0.5 for d in range(1, 12)}))
report('2. shuffled coin, source = the whole layer', shuffle_check(11, 1, 256, 0))
report('2. shuffled coin, source = the layer\'s core', shuffle_check(11, 1, 256, 1))
report('2. conditioned coins (bias by the number of live face neighbours), face all dead and all alive', cond_check(11, 1, 256))
cases = [(11, 1201, 20000, 256, 1), (11, 1202, 20000, 128, 2), (11, 1206, 20000, 64, 6), (9, 901, 30000, 16, 6), (11, 5, 20000, 0, 1)]
for R, seed, gens, M, DW in cases:
    a = first_line(brute(nzexe, R, seed, gens, M, DW)); b = first_line(brute(exe, R, seed, gens, M, DW))
    report(f'3. same BRUTE line as nz.c: R {R} seed {seed} gens {gens} M {M} DW {DW}', None if a == b else f'\n  nz : {a}\n  nzd: {b}')
a = first_line(brute(nzexe, 11, 1201, 20000, 256, 1))
b = first_line(brute(exe, 11, 1201, 20000, 256, 1, None, {'NZD_GENERAL': '1'}))
report_neg('3. bias 1/2 through the comparison path against nz.c', None if a == b else 'lines differ')
b = first_line(brute(exe, 11, 1200, 20000, 256, 1))
report_neg('3. another seed against nz.c', None if a == b else 'lines differ')
b = first_line(brute(exe, 11, 1201, 20000, 256, 1, '1:0.5,*:0.5'))
report('3. the list form with every bias 1/2', None if a == b else 'lines differ')
report('4. excursion counts recomputed from a dump (R = 9, M = 16, 30,000 generations)', rec_check())
report('5. layer groups and the face group', layer_check())
print('VALIDATION', 'PASSED' if ok_all else 'FAILED')
sys.exit(0 if ok_all else 1)
