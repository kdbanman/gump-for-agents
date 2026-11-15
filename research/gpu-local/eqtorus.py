#!/usr/bin/env python3
"""Equilateral (and any) face tori on this card: 8-layer slabs on the in-plane lattice (a, kk), (0, b) of
research/shape/tslab.py, for research/constant/PREDICTIONS.md part C.

  python -u research/gpu-local/eqtorus.py check A KK B [GENS]        # tslab check + GPU vs engine every generation
  python -u research/gpu-local/eqtorus.py run A KK B MINUTES SEED     # one run (guard on); json + a csv row
  python -u research/gpu-local/eqtorus.py summary A KK B              # pooled ln tau_face, ln tau_fw over the csv rows

Vessel: TwistedSlab = tslab.tslab's cells and neighbour graph, in the shape gsim.Sim expects (as vessels.SlabVessel,
which is the case kk = 0). Faces: the outer layers t = 0 and t = m - 1, A = 3ab each.

Engine comparison: a random soup on the torus is tiled into the engine's cubic Nt-torus (Nt Z^2 inside the lattice,
Nt >= m + 3, the construction of tslab.validate), `gump run --torus Nt --trace` gives every generation's cells, each
engine cell is reduced to its torus node, and the engine state must be lattice-periodic (cells = copies x nodes). The
GPU's lanes, stepped one generation at a time, must hold exactly that node set at every generation. Negative controls:
the same comparison against the next generation, and from the start state with one node flipped, must fail.

Run: as research/gpu/fwslab.py (first event of a life: face death kind 1, transverse firewall kind 4, both resolved
the same way), plus the cycle guard (kind 5, censored, thresholds GUARD * 2^j). Estimators from generation 0:
ln tau_face = ln(2 E / face), ln tau_fw = ln(E / fw), E = total exposure (all lives, all kinds, to their end).
"""
import csv, json, math, os, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
import tslab  # noqa: E402
import gsim, check, facelaw, fwslab, guard as guard_mod  # noqa: E402
from gsim import fl  # noqa: E402

M = 8
DATA = os.path.join(ROOT, 'research', 'data', 'gpu_local_eqtorus')
SCR = os.path.join(ROOT, 'research', 'scratch', 'gpu-local')
os.makedirs(SCR, exist_ok=True)


class TwistedSlab:
    def __init__(self, a, kk, b, m=M):
        g = tslab.tslab(a, kk, b, m)
        self.a, self.kk, self.b, self.m = a, kk, b, m
        self.cells = np.array(g.cells, np.int64)
        self.n = len(self.cells)
        self.nb = g.nb.astype(np.int32)
        self.sym, self.c, self.rep, self.hull = False, np.zeros(3, np.int64), None, None
        t = (self.cells.sum(1) - 1) // 2
        self.layer = t
        self.A = int((t == 0).sum())
        assert self.A == 3 * a * b
        faces = [np.nonzero(t == 0)[0], np.nonzero(t == m - 1)[0]]
        subs = [np.nonzero(t == 1)[0], np.nonzero(t == m - 2)[0]]
        self.groups = [(f.astype(np.int32), np.ones(len(f), np.int32)) for f in faces + subs]
        self.face_groups, self.sub_groups = [0, 1], [2, 3]
        self.orbit_of, self.osize = np.arange(self.n), np.ones(self.n, int)
        self.P = tslab.periods(a, kk, b)
        cube = self._cube(self.cells)
        ax = np.argmax(self.cells % 2, 1)
        self.key = {(int(c[0]), int(c[1]), int(tt), int(x)): i for i, (c, tt, x) in enumerate(zip(cube, t, ax))}

    @staticmethod
    def _cube(p):
        a = np.argmax(p % 2, 1)
        c = p.copy(); c[np.arange(len(p)), a] -= 1
        return c // 2

    def node_depth(self):
        return np.minimum(self.layer, self.m - 1 - self.layer)

    def nodes_from_engine(self, q, Nt):
        """engine cells (doubled coordinates on the Nt-torus; the slab occupies layers 0..m-1 of t = i + j + k mod Nt)"""
        q = np.asarray(q, np.int64).reshape(-1, 3)
        ax = np.argmax(q % 2, 1)
        c = self._cube(q)
        t = c.sum(1) % Nt
        out = []
        for (i, j), tt, x in zip(c[:, :2], t, ax):
            ii, jj = tslab.reduce_ij(int(i), int(j), self.a, self.kk, self.b)
            out.append(self.key[(ii, jj, int(tt), int(x))])
        return np.array(out, np.int64)


def rings(v):
    """the transverse diagonals with their layer incidence; moduli from tslab.periods (fwslab.rings for kk != 0)"""
    out = []
    for d, (dv, P) in enumerate(zip(fwslab.TDIAGS, v.P)):
        s = (v.cells @ np.array(dv)) % P
        vals = sorted(set(s.tolist()))
        assert vals == list(range(1, P, 2)), (d, vals)
        inc = np.zeros((v.n, len(vals)), np.float32)
        inc[np.arange(v.n), [vals.index(x) for x in s]] = 1
        out.append(dict(d=d + 1, layers=len(vals), inc=inc, cut=int(3 * inc.sum(0).min()) if len(vals) >= 3 else None))
    return out


def engine_nt(a, kk, b, m=M):
    for Nt in range(m + 3, 400):
        if Nt % b == 0 and Nt % a == 0 and ((Nt // a) * kk) % b == 0:
            return Nt
    raise ValueError


def engine_case(v, gens, seed=7, p=0.4):
    """random soup on the torus, tiled into the engine's Nt-torus; returns (start bits, per-generation node sets)"""
    a, kk, b, m = v.a, v.kk, v.b, v.m
    Nt = engine_nt(a, kk, b, m)
    rng = np.random.default_rng(seed)
    b0 = rng.random(v.n) < p
    reps = {((x * a) % Nt, (x * kk + y * b) % Nt) for x in range(Nt // a) for y in range(Nt // b)}
    kcop = Nt * Nt // (a * b)
    assert len(reps) == kcop
    pts = set()
    for cidx in np.nonzero(b0)[0]:
        p0 = v.cells[cidx]
        for (x, y) in reps:
            q = p0 + 2 * np.array([x, y, -x - y])
            pts.add(tuple(int(z) % (2 * Nt) for z in q))
    assert len(pts) == kcop * int(b0.sum())
    tag = f'{os.getpid()}_{a}_{kk}_{b}'
    cf, tr = os.path.join(SCR, f'cells_{tag}.txt'), os.path.join(SCR, f'trace_{tag}.txt')
    open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    subprocess.run([fl.GUMP, 'run', '--cells', cf, '--torus', str(Nt), '--gens', str(gens), '--no-halt', '--trace', tr],
                   check=True, capture_output=True)
    lines = open(tr).read().splitlines()
    os.remove(cf); os.remove(tr)
    cells = lambda line: np.array([list(map(int, q.split(','))) for q in line.split()[1:]], np.int64).reshape(-1, 3)
    sets = []
    for line in lines[:gens + 1]:
        q = cells(line)
        nodes = v.nodes_from_engine(q, Nt) if len(q) else np.zeros(0, np.int64)
        u = np.unique(nodes)
        assert len(q) == kcop * len(u), 'engine state not lattice-periodic'
        sets.append(u)
    start = np.zeros(v.n, bool); start[sets[0]] = True
    assert np.array_equal(start, b0)
    return b0, sets[1:], Nt, kcop


def check_engine(a, kk, b, gens=2000, m=M, control=None, **kw):
    v = TwistedSlab(a, kk, b, m)
    b0, sets, Nt, kcop = engine_case(v, gens + 1)
    s = gsim.Sim(v, backend='gpu', **kw)
    rng = np.random.default_rng(9)
    bits = rng.random((s.R, v.n)) < 0.4
    lanes = sorted({0, 31, 32, s.R // 2 + 5, s.R - 1})
    x0 = b0.copy()
    if control == 'flip':
        x0[int(np.argmax(v.node_depth()))] ^= True
    bits[lanes] = x0
    s.set_all(bits)
    bad, first = 0, None
    for t in range(gens):
        s.step(1, freeze=False)
        want = sets[t + 1] if control == 'shift' else sets[t]
        for lb in s.get_lanes(lanes):
            if not np.array_equal(np.nonzero(lb)[0], want):
                bad += 1; first = t + 1 if first is None else first
    tagc = f' [control {control}]' if control else ''
    print(f'torus ({a},{kk}),(0,{b}) x{m}{tagc}: GPU [{s.kernel} WB={s.WB} J={s.J}] vs engine torus {Nt} (x{kcop}), '
          f'{gens} gens x {len(lanes)} lanes: {"all equal" if bad == 0 else f"{bad} mismatches, first at generation {first}"}',
          flush=True)
    return bad == 0


def run(a, kk, b, wall_s, seed, p=0.4, m=M, guard=16, launch_s=1.0, max_launch=1 << 18, log=print):
    import cupy as cp
    v = TwistedSlab(a, kk, b, m)
    rs = rings(v)
    can_fw = any(r['layers'] >= 3 for r in rs)
    s = gsim.Sim(v, backend='gpu', keep=True)
    gd = guard_mod.CycleGuard(s, first=guard) if guard else None
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)
    birth = np.zeros(s.R, np.int64)
    ages, kinds, births, dirs, snaps = [], [], [], [], []
    G, rnd, K = 0, 1, min(1024, max_launch)
    start_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    t0 = time.time(); last = t0
    while time.time() - t0 < wall_s:
        t = time.time()
        reps, tt, kk_ = s.step(K)
        cp.cuda.Device().synchronize()
        dt = time.time() - t
        if can_fw:
            fw, which = fwslab.firewalled(s.get_all(), rs)
        else:                                # every transverse diagonal has 2 layers: no firewall can form
            fw, which = np.zeros(s.R, bool), np.zeros(s.R, np.int64)
        ended = []
        if len(reps):
            k2 = np.where((kk_ == 1) & fw[reps], 4, kk_)
            ages.append(G + tt - birth[reps]); kinds.append(k2); births.append(birth[reps].copy())
            dirs.append(np.where(k2 == 4, which[reps], 0)); ended.append(reps)
        frozen = np.zeros(s.R, bool); frozen[reps] = True
        G += K
        alive_fw = np.nonzero(fw & ~frozen)[0]
        if len(alive_fw):
            ages.append(G - birth[alive_fw]); kinds.append(np.full(len(alive_fw), 4)); births.append(birth[alive_fw].copy())
            dirs.append(which[alive_fw]); ended.append(alive_fw)
        if gd is not None:                   # a firewalled replica ends as kind 4 first; the guard sees the rest
            g_reps, g_snap = gd.boundary(G, birth)
            g_reps = np.setdiff1d(g_reps, alive_fw)
            if len(g_reps):
                ages.append(G - birth[g_reps]); kinds.append(np.full(len(g_reps), guard_mod.KIND)); births.append(birth[g_reps].copy())
                dirs.append(np.zeros(len(g_reps), np.int64)); ended.append(g_reps)
                snaps.append(np.stack([g_reps, G - birth[g_reps], gd.snap_age[g_reps]]))
        if ended:
            e = np.unique(np.concatenate(ended))
            s.reseed(e, seed=(seed << 32) + rnd, p=p); rnd += 1
            birth[e] = G
            if gd is not None:
                gd.reset(e)
        if dt < launch_s / 2 and K < max_launch:
            K *= 2
        if time.time() - last > 300:
            k = np.concatenate(kinds) if kinds else np.zeros(0)
            log(json.dumps(dict(torus=[a, kk, b], gen=G, face=int((k == 1).sum()), fw=int((k == 4).sum()),
                                guard=int((k == 5).sum()), elapsed=round(time.time() - t0))))
            last = time.time()
    ages.append(G - birth); kinds.append(np.zeros(s.R, np.int64)); births.append(birth.copy()); dirs.append(np.zeros(s.R, np.int64))
    A_, K_, B_, D_ = (np.concatenate(x).astype(np.int64) for x in (ages, kinds, births, dirs))
    cnt = {k: int((K_ == k).sum()) for k in range(6)}
    out = dict(torus=[a, kk, b], m=m, A=v.A, cuts={r['d']: r['cut'] for r in rs}, seed=seed, p=p, gens=G, replicas=s.R,
               start_utc=start_utc, wall_s=round(time.time() - t0, 1), max_launch=max_launch, nodes=v.n,
               config=dict(WB=s.WB, J=s.J, T=s.T, blocks=s.blocks), exposure=int(A_.sum()),
               face=cnt[1], fw=cnt[4], settled12=cnt[2], settled3pw=cnt[3], guard=cnt[5], open=cnt[0],
               exposure_guard=int(A_[K_ == 5].sum()), guard_first=guard, guard_thresholds=f'{guard} * 2^j' if guard else None,
               fw_by_direction={int(d): int(((K_ == 4) & (D_ == d)).sum()) for d in (1, 2, 3)})
    out['guard_lives'] = facelaw.pack(np.concatenate(snaps, axis=1) if snaps else np.zeros((3, 0), np.int64))
    if len(A_) <= 150000:
        out['raw'] = facelaw.pack(np.stack([A_, K_, B_, D_]))
    return out


CSV_FIELDS = ['torus', 'A', 'seed', 'start_utc', 'wall_s', 'gens', 'replicas', 'exposure', 'face', 'fw', 'settled12',
              'settled3pw', 'guard', 'open', 'exposure_guard', 'guard_thresholds', 'max_launch', 'code_commit', 'cmd']


def git_head():
    try:
        return subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        return 'unknown'


def summary(a, kk, b):
    path = os.path.join(DATA, f'eqtorus_{a}_{kk}_{b}.csv')
    rows = list(csv.DictReader(open(path)))
    seeds = [r['seed'] for r in rows]
    assert len(set(seeds)) == len(seeds), 'two runs with the same seed'
    E = sum(int(r['exposure']) for r in rows); F = sum(int(r['face']) for r in rows); W = sum(int(r['fw']) for r in rows)
    g5 = sum(int(r['guard']) for r in rows); e5 = sum(int(r['exposure_guard']) for r in rows)
    lf = math.log(2 * E / F) if F else float('nan')
    print(f'torus ({a},{kk}),(0,{b}) A = {rows[0]["A"]}: {len(rows)} runs, exposure {E:.4g}, face deaths {F}, firewalls {W}, '
          f'guard {g5} (their exposure {e5 / max(E, 1):.2e} of the total)')
    print(f'  ln tau_face = {lf:.4f} +- {1 / math.sqrt(max(F, 1)):.4f}' +
          (f';  ln tau_fw = {math.log(E / W):.3f} +- {1 / math.sqrt(W):.3f}' if W else ''))


if __name__ == '__main__':
    cmd = ' '.join(['python', '-u', 'research/gpu-local/eqtorus.py'] + sys.argv[1:])
    what = sys.argv[1]
    a, kk, b = map(int, sys.argv[2:5])
    if what == 'check':
        gens = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
        ok = tslab.check(a, kk, b)
        v = TwistedSlab(a, kk, b)
        print('cuts:', {r['d']: r['cut'] for r in rings(v)}, 'nodes', v.n)
        ok &= check_engine(a, kk, b, gens)
        ok &= check_engine(a, kk, b, gens, kernel='shared', J=3, WB=1, blocks=6)
        ok &= not check_engine(a, kk, b, 300, control='shift')
        ok &= not check_engine(a, kk, b, 300, control='flip')
        print('ALL OK' if ok else 'FAILURES')
        sys.exit(0 if ok else 1)
    elif what == 'run':
        minutes, seed = float(sys.argv[5]), int(sys.argv[6])
        out = run(a, kk, b, minutes * 60, seed)
        out['code_commit'] = git_head(); out['cmd'] = cmd
        os.makedirs(DATA, exist_ok=True)
        jp = os.path.join(SCR, f'eqtorus_{a}_{kk}_{b}_s{seed}.json')
        json.dump(out, open(jp, 'w'))
        path = os.path.join(DATA, f'eqtorus_{a}_{kk}_{b}.csv')
        new = not os.path.exists(path)
        with open(path, 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
            if new:
                w.writeheader()
            w.writerow(dict(out, torus=f'{a},{kk},{b}'))
        print(json.dumps({k: out[k] for k in CSV_FIELDS if k in out and k != 'cmd'}))
    elif what == 'summary':
        summary(a, kk, b)
