#!/usr/bin/env python3
"""Claim a, the vessel and the stepper: PR 12's SlabVessel and its unchanged kernel B on slab graphs, on a CPU.

  taskset -c 3 python3 research/audit/gpu_pr12/slab_kernel_check.py PR12_WORKTREE

1 graph:   SlabVessel(N1, N2, 8) against an adjacency built here from docs/AUTOMATON.md's 12 offsets with an explicit
           skewed-torus wrap (periods (N1,0,-N1), (0,N2,-N2) in cubes) and dead outside layers t = 0..m-1; face
           groups = layers t = 0 and t = m-1 of 3 N1 N2 cells. Production sizes 6x6x8, 6x7x8 and 11x11x8.
2 engine:  kernel B (PR 8's ucontext emulation, research/audit/gpu_pr8/shared_shim_uc.cpp) on SlabVessel(11, 11, 8),
           state compared with `gump run --torus 11 --slab-layers 8 --diag 0 --trace` every generation (own mapping).
3 fl.c:    kernel B in the production shape of the committed runs (6x6x8: J = 2, T = 448; 6x7x8: J = 2, T = 512) against
           fl.c on the same graph: full state after launches of 1/7/250/1000, and kind-1 generations vs fl.c's run_until.
Exit 1 on any failure.
"""
import ctypes, math, os, subprocess, sys
import numpy as np

PR = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SHIM = os.path.join(ROOT, 'research', 'audit', 'gpu_pr8', 'shared_shim_uc.cpp')
sys.path.insert(0, os.path.join(PR, 'research', 'gpu'))
import gsim                                       # noqa: E402  the PR's host code
from vessels import SlabVessel                    # noqa: E402
fl = gsim.fl
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump'); fl.GUMP = GUMP
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr12'); os.makedirs(SCR, exist_ok=True)
ok_all = True


def report(name, ok):
    global ok_all
    ok_all &= bool(ok)
    print(f'{"OK  " if ok else "FAIL"} {name}', flush=True)


# ---------- 1: independent slab graph
def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for o in (b, c):
        for sa in (1, -1):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(v)
    return out


def my_slab(N1, N2, m):
    """cells keyed by (cube i mod N1, cube j mod N2, layer t = i+j+k, axis); reduction by the two periods"""
    def key(p):
        a = [x % 2 for x in p].index(1)
        c = [(p[x] - (1 if x == a else 0)) // 2 for x in range(3)]
        t = sum(c)
        if not 0 <= t < m:
            return None
        return (c[0] % N1, c[1] % N2, t, a)       # (i,j,k) ~ (i+N1, j, k-N1) ~ (i, j+N2, k-N2): t fixed, i, j mod N
    cells = {}
    for t in range(m):
        for i in range(N1):
            for j in range(N2):
                for a in range(3):
                    p = [2 * i, 2 * j, 2 * (t - i - j)]; p[a] += 1
                    cells[(i, j, t, a)] = tuple(p)
    adj = {}
    for kk, p in cells.items():
        adj[kk] = sorted([key([p[x] + v[x] for x in range(3)]) or ('out',) for v in offsets(kk[3])], key=str)
    return cells, adj


for N1, N2 in ((6, 6), (6, 7), (11, 11)):
    v = SlabVessel(N1, N2, 8)
    cells, adj = my_slab(N1, N2, 8)
    kof = {tuple(map(int, c)): None for c in v.cells}
    # map PR node -> my key through the PR's cell coordinates
    def kk(p):
        p = list(map(int, p)); a = [x % 2 for x in p].index(1)
        c = [(p[x] - (1 if x == a else 0)) // 2 for x in range(3)]
        return (c[0] % N1, c[1] % N2, sum(c), a)
    keys = [kk(p) for p in v.cells]
    good = len(set(keys)) == v.n == len(cells) == 3 * N1 * N2 * 8
    for i in range(v.n):
        mine = adj[keys[i]]
        theirs = sorted([keys[j] if j >= 0 else ('out',) for j in v.nb[i]], key=str)
        good &= mine == theirs
    lay = np.array([k[2] for k in keys])
    f0, f1 = set(v.groups[0][0].tolist()), set(v.groups[1][0].tolist())
    good &= f0 == set(np.nonzero(lay == 0)[0].tolist()) and f1 == set(np.nonzero(lay == 7)[0].tolist())
    good &= v.A == 3 * N1 * N2 and v.face_groups == [0, 1]
    good &= all(len(set(v.nb[i][v.nb[i] >= 0])) == (v.nb[i] >= 0).sum() for i in range(v.n))   # no doubled neighbour
    nout = (v.nb < 0).sum(1)
    report(f'graph SlabVessel({N1},{N2},8): n={v.n}, every neighbour list = independent build; faces = layers 0, 7 '
           f'({v.A} cells each); dead-outside neighbours per cell by layer {[int(nout[lay == t].max()) for t in range(8)]}', good)


# ---------- kernel B on the CPU (class as in research/audit/gpu_pr8/shared_cpu_check.py, production defaults)
class SharedCPU:
    def __init__(self, v, WB=2, J=None, blocks=1, pw=128):
        n = v.n; self.v, self.n = v, n
        J = J or max(2 * math.ceil(n / 1024), 1)
        L = gsim.shared_layout(v, J, True)
        self.perm, self.T, self.WB, self.J, self.blocks = L['perm'], L['T'], WB, J, blocks
        self.NP = n + 1; self.WT = blocks * WB; self.R = 32 * self.WT
        src = open(os.path.join(PR, 'research/gpu/kernel_shared.cuh')).read()
        decl = 'extern __shared__ u32 sm[];'; assert src.count(decl) == 1
        tag = f'slab_n{n}_wb{WB}_t{L["T"]}_j{J}_q{L["Q"]}_nf{L["nf"]}_pw{pw}'
        d = os.path.join(SCR, 'build_' + tag); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'kernel_shared_sub.cuh'), 'w').write(src.replace(decl, 'u32 *sm = g_sm;'))
        so = os.path.join(d, 'k.so')
        defs = [f'-DK_N={n}', f'-DK_NP={n + 1}', f'-DK_WB={WB}', f'-DK_T={L["T"]}', f'-DK_J={J}', f'-DK_Q={L["Q"]}',
                f'-DK_NF={L["nf"]}', '-DK_MINB=1', f'-DK_PW={pw}', '-DK_KEEP=0']
        subprocess.check_call(['g++', '-O2', '-std=c++11', '-w', '-shared', '-fPIC', '-o', so, SHIM, '-I', d,
                               '-I', os.path.join(PR, 'research/gpu')] + defs)
        self.lib = ctypes.CDLL(so)
        self.pk = np.ascontiguousarray(L['pk'], np.uint32); self.fe = np.ascontiguousarray(L['fe'], np.uint32)
        self.A = np.zeros(self.WT * self.NP, np.uint32); self.B = np.zeros_like(self.A)
        self.frz = np.zeros(self.WT, np.uint32)
        self.ev_t = np.zeros(self.R, np.uint32); self.ev_k = np.zeros(self.R, np.uint8)

    def set_all(self, bits):
        bits = bits[:, self.perm]
        cols = np.ascontiguousarray(np.packbits(bits.T, axis=1, bitorder='little')).view(np.uint32)
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
        bad = self.lib.run(self.blocks, P(self.pk), P(self.fe), P(self.A), P(self.B), gens, int(freeze), P(self.frz), P(self.ev_t), P(self.ev_k))
        assert bad == 0
        newly = self.frz & ~before
        reps = np.nonzero(np.unpackbits(newly.view(np.uint8), bitorder='little'))[0]
        return reps, self.ev_t[reps].astype(np.int64), self.ev_k[reps].astype(np.int64)


# ---------- 2: against the engine's torus slab, every generation
N, m, T = 11, 8, 600
v = SlabVessel(N, N, m)
tr = os.path.join(SCR, f'slab_trace_{os.getpid()}.txt')
subprocess.run([GUMP, 'run', '--soup', '0.4', '--torus', str(N), '--slab-layers', str(m), '--diag', '0', '--rng', '77',
                '--gens', str(T), '--no-halt', '--trace', tr], capture_output=True, check=True)
lines = open(tr).read().splitlines(); os.remove(tr)
def eng_cells(line):
    return [tuple(map(int, q.split(','))) for q in line.split()[1:]]
c0 = eng_cells(lines[0])
lay0 = sorted({(sum((x - (x % 2 == 1)) // 2 for x in p)) % N for p in c0})
off = next(o for o in range(N) if set(lay0) <= {(o + k) % N for k in range(m)})
def to_key(p):
    a = [x % 2 for x in p].index(1)
    c = [(p[x] - (1 if x == a else 0)) // 2 for x in range(3)]
    t = (sum(c) - off) % N
    # engine cube (i,j,k) on the N^3 torus; slab key: i, j mod N and the layer: the slab's in-plane lattice is the
    # zero-sum sublattice of N Z^3, so (i mod N, j mod N, t) identifies the cube
    return (c[0] % N, c[1] % N, t, a)
pkey = {}
for idx, p in enumerate(v.cells):
    p = list(map(int, p)); a = [x % 2 for x in p].index(1)
    c = [(p[x] - (1 if x == a else 0)) // 2 for x in range(3)]
    pkey[(c[0] % N, c[1] % N, sum(c), a)] = idx
def state(line):
    b = np.zeros(v.n, bool); b[[pkey[to_key(p)] for p in eng_cells(line)]] = True; return b
s = SharedCPU(v, WB=2, J=None, blocks=1)
rng = np.random.default_rng(5)
bits = rng.random((s.R, v.n)) < 0.4
lanes = [0, 17, 31, 32, 63]
bits[lanes] = state(lines[0])
s.set_all(bits)
bad = 0
for t in range(1, T + 1):
    s.step(1, freeze=False)
    want = state(lines[t]); got = s.get_all()
    bad += sum(int(not np.array_equal(got[l], want)) for l in lanes)
report(f'kernel B (J={s.J}, T={s.T}) on SlabVessel(11,11,8) = engine --torus 11 --slab-layers 8 --diag 0, every generation, '
       f'{T} gens x {len(lanes)} lanes ({bad} mismatches; engine live cells at start {len(c0)})', bad == 0)
# negative control: one generation late must mismatch
s.set_all(bits); s.step(1, freeze=False)
late = s.get_all()[0]
report('negative control: kernel state after 1 gen != engine state after 2 gens', not np.array_equal(late, state(lines[2])))

# ---------- 3: production shapes against fl.c, stepping and face-death generations
for N1, N2, Tw in ((6, 6, 448), (6, 7, 512)):
    v = SlabVessel(N1, N2, 8)
    s = SharedCPU(v, WB=2, J=2, blocks=1)
    assert s.T == Tw, (s.T, Tw)
    f = fl.Sim(v, W=s.R // 64)
    b0 = np.random.default_rng(N1 * 10 + N2).random((s.R, v.n)) < 0.4
    s.set_all(b0); f.set_all(b0); good = True
    for L in (1, 7, 250, 1000):
        s.step(L, freeze=False); f.run(L, record=False); good &= np.array_equal(s.get_all(), f.get_all())
    report(f'kernel B production shape {N1}x{N2}x8 (J=2, T={s.T}) = fl.c after launches 1/7/250/1000', good)
    # sparse soups so faces die within the test: kind-1 generation equal to fl.c run_until
    b1 = np.random.default_rng(N1 * 7 + N2).random((s.R, v.n)) < 0.18
    s.set_all(b1); f.set_all(b1)
    TT = 400
    sg, sm, _ = f.run_until(TT, np.zeros(s.R, np.int32), np.full(s.R, 1 << 30, np.int32))
    got = np.full(s.R, -1); kind = np.zeros(s.R, int); done = 0
    while done < TT:
        reps, tt, kk = s.step(100); got[reps] = tt + done; kind[reps] = kk; done += 100
    born = (sm == 0) & (sg == 0)
    fd = (sm == 0) & ~born; mine = (kind == 1) & ~born
    agree = np.array_equal(fd, mine) and np.array_equal(sg[fd], got[mine])
    report(f'kind-1 (outer layer extinct) generations {N1}x{N2}x8 p=0.18: {int(fd.sum())} face deaths, equal to fl.c', agree and fd.sum() > 5)
sys.exit(0 if ok_all else 1)
