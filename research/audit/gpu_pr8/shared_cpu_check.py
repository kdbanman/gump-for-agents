#!/usr/bin/env python3
"""Run PR 8's production kernel (research/gpu/kernel_shared.cuh) on the CPU and check it against fl.c and the engine.

  taskset -c 3 python3 research/audit/gpu_pr8/shared_cpu_check.py PR8_WORKTREE [--skip-fl]

The kernel source is compiled unchanged apart from replacing its `extern __shared__` declaration by a pointer, inside
shared_shim.cpp (POSIX threads for the block, barriers for __syncthreads and for warp shuffles). The host-side layout
(node order, packed neighbour table, face-entry table) comes from the PR's own gsim.shared_layout, as in production.
Checks:
  1 stepping: every replica's full state equal to fl.c's after every launch (launch lengths 1, 7, 250, 1000), freeze off
  2 events:   kind-1 (face extinct) generation equal to fl.c's run_until for every replica, launches of 100 / 1000
  3 settling: R = 7 soups that the engine runs to a cycle (period p, cycle_start c); faces off; kind 2 at c + 2 for
              p <= 2, kind 3 at L + p (L = first launch start >= c) for 2 < p <= 128
  4 engine:   one asymmetric soup (R = 11) and one O_h vertex soup (R = 24) from `gump run`, compared with the engine's
              state after 3000 generations in 4 lanes
Exit status 1 on any failure.

Run pinned to one core (taskset -c N): the block is emulated with K_T threads.
"""
import ctypes, json, math, os, subprocess, sys
import numpy as np

PR = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PR, 'research', 'gpu'))
import gsim                       # noqa: E402  (the PR's host code; imports the PR's copy of fl)
fl = gsim.fl
SKIP12 = '--skip-fl' in sys.argv
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr8')
os.makedirs(SCR, exist_ok=True)
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
fl.GUMP = GUMP                    # the PR checkout has no engine build; use this tree's


class SharedCPU:
    def __init__(self, v, WB=2, J=None, blocks=2, faces=True, pw=128):
        n = v.n; self.v, self.n = v, n
        J = J or max(2 * math.ceil(n / 1024), 1)
        L = gsim.shared_layout(v, J, faces)
        self.perm, self.T, self.WB, self.J, self.blocks = L['perm'], L['T'], WB, J, blocks
        self.NP = n + 1; self.WT = blocks * WB; self.R = 32 * self.WT
        src = open(os.path.join(PR, 'research/gpu/kernel_shared.cuh')).read()
        decl = 'extern __shared__ u32 sm[];'
        assert src.count(decl) == 1
        tag = f'n{n}_wb{WB}_t{L["T"]}_j{J}_q{L["Q"]}_nf{L["nf"]}_pw{pw}'
        d = os.path.join(SCR, 'build_' + tag); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'kernel_shared_sub.cuh'), 'w').write(src.replace(decl, 'u32 *sm = g_sm;'))
        so = os.path.join(d, 'k.so')
        defs = [f'-DK_N={n}', f'-DK_NP={n + 1}', f'-DK_WB={WB}', f'-DK_T={L["T"]}', f'-DK_J={J}', f'-DK_Q={L["Q"]}',
                f'-DK_NF={L["nf"]}', '-DK_MINB=1', f'-DK_PW={pw}', '-DK_KEEP=0']
        subprocess.check_call(['g++', '-O1', '-std=c++11', '-w', '-shared', '-fPIC', '-pthread', '-o', so,
                               os.path.join(HERE, 'shared_shim.cpp'), '-I', d, '-I', os.path.join(PR, 'research/gpu')] + defs)
        self.lib = ctypes.CDLL(so)
        self.pk = np.ascontiguousarray(L['pk'], np.uint32); self.fe = np.ascontiguousarray(L['fe'], np.uint32)
        self.A = np.zeros(self.WT * self.NP, np.uint32); self.B = np.zeros_like(self.A)
        self.frz = np.zeros(self.WT, np.uint32)
        self.ev_t = np.zeros(self.R, np.uint32); self.ev_k = np.zeros(self.R, np.uint8)

    def set_all(self, bits):
        bits = bits[:, self.perm]
        cols = np.ascontiguousarray(np.packbits(bits.T, axis=1, bitorder='little')).view(np.uint32)   # (n, WT)
        st = np.zeros((self.WT, self.NP), np.uint32); st[:, :self.n] = cols.T
        self.A[:] = st.reshape(-1); self.B[:] = st.reshape(-1); self.frz[:] = 0

    def get_all(self):
        st = self.A.reshape(self.WT, self.NP)[:, :self.n].T
        bits = np.unpackbits(np.ascontiguousarray(st).view(np.uint8), axis=1, bitorder='little').T.astype(bool)
        out = np.empty_like(bits); out[:, self.perm] = bits
        return out

    def step(self, gens, freeze=True):
        before = self.frz.copy()
        P = lambda a: a.ctypes.data_as(ctypes.c_void_p)
        self.lib.run(self.blocks, P(self.pk), P(self.fe), P(self.A), P(self.B), gens, int(freeze), P(self.frz), P(self.ev_t), P(self.ev_k))
        newly = self.frz & ~before
        reps = np.nonzero(np.unpackbits(newly.view(np.uint8), bitorder='little'))[0]
        return reps, self.ev_t[reps].astype(np.int64), self.ev_k[reps].astype(np.int64)


ok_all = True


def report(name, ok):
    global ok_all
    ok_all &= bool(ok)
    print(f'{"OK  " if ok else "FAIL"} {name}', flush=True)


def soups(v, R, nrep, seed, p=0.35):
    rng = np.random.default_rng(seed)
    sd = np.abs(v.cells - v.c).sum(1) <= R
    return (rng.random((nrep, v.n)) < p) & sd


# 1 + 2: against fl.c (asymmetric R = 7 with 2 warps per block, R = 9 with the production J)
for R, J, WB, blocks in (() if SKIP12 else ((7, None, 2, 1), (9, 'x', 2, 2), (7, 'x', 1, 2))):   # None = production J
    v = fl.Vessel(fl.octa_hull(R), 'c', False)
    s = SharedCPU(v, WB=WB, J=(math.ceil(v.n / 64) if J == 'x' else None), blocks=blocks)
    b0 = soups(v, R, s.R, 100 + R)
    f = fl.Sim(v, W=s.R // 64)
    s.set_all(b0); f.set_all(b0)
    good = True; done = 0
    for L in (1, 7, 250, 1000, 1, 250):
        s.step(L, freeze=False); f.run(L, record=False); done += L
        good &= np.array_equal(s.get_all(), f.get_all())
    report(f'stepping vs fl.c, R={R} nodes={v.n} T={s.T} J={s.J} WB={WB} replicas={s.R}, {done} gens in launches 1/7/250/1000', good)
    for K in (100, 1000):
        s.set_all(b0); f.set_all(b0)
        sg, sm, _ = f.run_until(3000, np.zeros(s.R, np.int32), np.full(s.R, 1 << 30, np.int32))
        got = np.full(s.R, -1); kind = np.zeros(s.R, int); done = 0
        while done < 3000:
            reps, tt, kk = s.step(K); got[reps] = tt + done; kind[reps] = kk; done += K
        born_dead = (sm == 0) & (sg == 0)
        fd = (sm == 0) & ~born_dead; mine = (kind == 1) & ~born_dead
        agree = np.array_equal(fd, mine) and np.array_equal(sg[fd], got[mine]) and np.all(got[born_dead] == 1)
        st_fl = (sm == -2)
        # fl.c's settle stop counts generations stepped; kernel kind 2 at the generation whose state equals two back
        print(f'     events R={R} launches of {K}: face deaths fl.c {fd.sum()} kernel {mine.sum()}; fl.c settled {st_fl.sum()}, '
              f'kernel kind 2 {(kind == 2).sum()}, kind 3 {(kind == 3).sum()}')
        report(f'face-death generations vs fl.c, R={R}, launches of {K}', agree)

# 3: settling against the engine's cycle detection (R = 7 soups, faces off)
cases = []
for rng_i in range(1, 400):
    out = subprocess.run([GUMP, 'run', '--soup', '0.35', '--radius', '7', '--rng', str(rng_i), '--gens', '200000'],
                         capture_output=True, text=True, check=True).stdout
    sm_ = json.loads(out.strip().splitlines()[-1])
    if sm_['status'] != 'extinct' and sm_['period'] is not None:
        cases.append((rng_i, sm_['period'], sm_['cycle_start']))
    if len(cases) >= 60:
        break
per = [c[1] for c in cases]
print(f'     settling cases: {len(cases)} soups, periods {sorted(set(per))}, cycle_start max {max(c[2] for c in cases)}')
v = fl.Vessel(fl.octa_hull(7), 'c', False)
s = SharedCPU(v, WB=2, J=math.ceil(v.n / 64), blocks=1, faces=False)
lanes = np.arange(len(cases)) * (s.R // len(cases))
bits = np.zeros((s.R, v.n), bool)
for lane, (rng_i, p, c) in zip(lanes, cases):
    cells, _ = fl.gump_cells(['--soup', '0.35', '--radius', '7', '--rng', str(rng_i)], 0, 'a')
    bits[lane] = fl.bits_from_cells(v, cells)
s.set_all(bits)
K = 1000; G = max(c[2] for c in cases) + 2 * K + 140; ev = {}; g = 0
while g < G:
    reps, tt, kk = s.step(K)
    for r, t, k in zip(reps, tt, kk):
        ev[int(r)] = (g + int(t), int(k))
    g += K
bad = []
for lane, (rng_i, p, c) in zip(lanes, cases):
    want = (c + 2, 2) if p <= 2 else ((-(-c // K) * K + p, 3) if p <= 128 else None)
    if ev.get(int(lane)) != want:
        bad.append((rng_i, p, c, want, ev.get(int(lane))))
report(f'settle events vs engine cycle detection ({len(cases)} soups, launches of {K}); wrong: {bad[:5]}', not bad)

# 4: engine, 3000 generations
for args, centre, sym in ((['--soup', '0.35', '--radius', '11', '--rng', '5'], 'c', False),
                          (['--soup', '0.35', '--radius', '24', '--sym', 'oh', '--rng', '4', '--center', '1,1,1'], 'v', True)):
    c0, s0 = fl.gump_cells(args, 0, 'e0')
    cT, _ = fl.gump_cells(args, 3000, 'eT')
    hull = s0['hull_final']
    v = fl.Vessel(hull, centre, sym)
    s = SharedCPU(v, WB=2, J=math.ceil(v.n / 64), blocks=1)
    rng = np.random.default_rng(7)
    bits = rng.random((s.R, v.n)) < 0.35
    lanes = [0, 31, 32, 63]
    bits[lanes] = fl.bits_from_cells(v, c0)
    s.set_all(bits)
    for L in (1000, 999, 1, 1000):
        s.step(L, freeze=False)
    out = s.get_all(); want = set(map(tuple, cT))
    res = [set(map(tuple, fl.cells_from_bits(v, out[r]))) == want for r in lanes]
    report(f'engine state after 3000 gens: {" ".join(args)} (nodes {v.n}, T {s.T}): lanes {res}', all(res))

print('ALL OK' if ok_all else 'FAILURES')
sys.exit(0 if ok_all else 1)
