#!/usr/bin/env python3
"""PR 14 review: an independent, channel-resolved CPU measurement of slab faces and transverse firewalls, and an
emulation of fwslab.py's attribution rules on the same histories.

Stepper: research/peeling/rep.c (bit-sliced, checked against the engine by research/peeling/validate.py); graph:
research/peeling/geom.slab. Neither is PR 14's code. `validate` re-checks rep.c on the skewed slab itself against the
engine (the slab tiled 8x into a 12-torus; populations x 8, every generation).

    python3 research/audit/gpu_pr14/cpu_channels.py validate 3 6 8 3000
    taskset -c 3 python3 research/audit/gpu_pr14/cpu_channels.py run 3 6 8 400000 SEED W     # 64*W replicas, one life each
    python3 research/audit/gpu_pr14/cpu_channels.py analyze 3 6 8

Per replica (resolution 16 generations): the two face layers' death times, the first T3 firewall per transverse
diagonal (as research/peeling/slabs.py), the settle time (period dividing 840). Saved under
research/scratch/audit_gpu_pr14/. `analyze` prints
  (T) the channel-resolved truth: first event = earliest of face death / firewall formation; settled censored;
  (G) fwslab.py's rules applied to the same histories, launches of K = 2^18 from birth (the K the GPU runs reach):
      firewall-first lives end at the face death if it comes before the next launch boundary, else at that boundary;
      a life that settles after its firewall but before that end is censored as settled; the direction label is the
      lowest-numbered diagonal with a firewall at detection.
"""
import glob, math, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'peeling'))
import geom                                           # noqa: E402
from analyze import death_times, ring_firewall, INF   # noqa: E402
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr14')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
os.makedirs(OUT, exist_ok=True)


def validate(N1, N2, m, gens, Nt=12, p=0.4, seed=7):
    v = geom.slab(N1, m, N2)
    assert Nt % N1 == 0 and Nt % N2 == 0 and Nt >= m + 3
    rng = np.random.default_rng(seed)
    live = np.nonzero(rng.random(len(v.cells)) < p)[0]
    ci = os.path.join(OUT, 'ci.txt'); open(ci, 'w').write('\n'.join(map(str, live)))
    vb = os.path.join(OUT, 'vv.bin'); geom.build_rep(); v.write(vb)
    out = subprocess.run([geom.REP, vb, '1', '0.0', '1', str(gens), '16', '-i', ci, '-t'], capture_output=True, text=True).stdout
    mine = [int(l.split()[2]) for l in out.splitlines() if l.startswith('T')]
    # tile into the Nt-torus: translations a(N1,0,-N1) + b(0,N2,-N2) in cube coordinates
    pts = set()
    for c in live:
        p0 = np.array(v.cells[c])
        for a in range(Nt // N1):
            for b in range(Nt // N2):
                q = p0 + 2 * np.array([a * N1, b * N2, -a * N1 - b * N2])
                pts.add(tuple(int(x) % (2 * Nt) for x in q))
    cf = os.path.join(OUT, 'cells.txt'); open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    pl = os.path.join(OUT, 'pl.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(Nt), '--gens', str(gens), '--no-halt', '--poplog', pl],
                   check=True, capture_output=True)
    ref = [int(l.split()[1]) for l in open(pl)]
    k = Nt * Nt // (N1 * N2)
    assert len(pts) == k * len(live)
    # rep's trace line g is the population after g steps; the poplog's line 0 is the seed (see AUTOMATON.md section 4)
    if mine[0] == len(live):         # rep's trace starts with the seed
        mine = mine[1:]
    off = 1 if ref[0] == len(pts) else 0
    n = min(len(mine), len(ref) - off)
    ok = all(mine[i] * k == ref[i + off] for i in range(n))
    print(f'slab {N1}x{N2}x{m} vs engine torus {Nt} (x{k}): {n} generations, {"MATCH" if ok else "MISMATCH"}; '
          f'rep {mine[:4]}.. engine/{k} {[x // k for x in ref[off:off + 4]]}..; last {mine[n - 1]} {ref[n - 1 + off] // k}')
    # the graph itself, from AUTOMATON.md's doubled offsets
    def key(q):
        a = next(x for x in range(3) if q[x] % 2)
        cu = [(q[x] - (x == a)) // 2 for x in range(3)]
        return (cu[0] % N1, cu[1] % N2, sum(cu), a)
    idx = {key(c): i for i, c in enumerate(v.cells)}
    assert len(idx) == len(v.cells)
    v.canon = lambda q: idx.get(key(q)) if 0 <= key(q)[2] < m else None
    bad = 0
    for i, c in enumerate(v.cells):
        a = next(x for x in range(3) if c[x] % 2)
        b_, c_ = [x for x in range(3) if x != a]
        offs = []
        for sb in (2, -2):
            for sc in (2, -2):
                o = [0, 0, 0]; o[b_] = sb; o[c_] = sc; offs.append(o)
        for sa in (1, -1):
            for e in (b_, c_):
                for se in (1, -1):
                    o = [0, 0, 0]; o[a] = sa; o[e] = se; offs.append(o)
        want = sorted(x for x in (v.canon(tuple(c[t] + o[t] for t in range(3))) for o in offs) if x is not None)
        got = sorted(x for x in v.nb[i] if x >= 0)
        bad += want != got
    print(f'graph: {bad} cells whose neighbour list differs from the AUTOMATON offsets')
    return ok and bad == 0


def run(N1, N2, m, cap, seed, W):
    v = geom.slab(N1, m, N2)
    st, pop, la = v.run(W, 0.4, seed, cap, 16)
    ge = v.gen_end
    D = death_times(la, ge)
    keys = [k for k, _ in v.layers]
    face = np.minimum(D[:, keys.index((0, 1))], D[:, keys.index((0, 2 * m - 1))])
    fw = np.full((len(st), 3), INF)
    for d in (1, 2, 3):
        cols = [i for i, k in enumerate(keys) if k[0] == d]
        if len(cols) >= 3:
            fw[:, d - 1] = ring_firewall(D[:, cols], ring=True)
    f = os.path.join(OUT, f'ch_{N1}x{N2}x{m}_s{seed}.npz')
    np.savez(f, face=face, fw=fw, settle=st, gen_end=ge, cap=cap, seed=seed)
    print(f'{f}: {len(st)} replicas, gen_end {ge}, face<inf {np.isfinite(face).sum()}, fw<inf {np.isfinite(fw.min(1)).sum()}')


def analyze(N1, N2, m, K=1 << 18):
    fs = sorted(glob.glob(os.path.join(OUT, f'ch_{N1}x{N2}x{m}_s*.npz')))
    face, fw, st, ge = [], [], [], []
    for f in fs:
        z = np.load(f)
        face.append(z['face']); fw.append(z['fw']); st.append(z['settle']); ge.append(np.full(len(z['face']), int(z['gen_end'])))
    face, fw, st, ge = np.concatenate(face), np.concatenate(fw), np.concatenate(st), np.concatenate(ge)
    seeds = [int(np.load(f)['seed']) for f in fs]
    assert len(set(seeds)) == len(seeds)
    R = len(face)
    stop = np.where(st >= 0, st, ge).astype(float)
    fwm = fw.min(1)
    # (T) truth
    end = np.minimum.reduce([face, fwm, stop])
    kF = (face == end) & (face < fwm) & (face <= stop)       # face strictly first (ties -> firewall)
    kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
    E = end.sum(); F, Wn = int(kF.sum()), int(kW.sum())
    sh = Wn / (F + Wn)
    print(f'slab {N1}x{N2}x{m}: {len(fs)} runs, {R} replicas (one life each); censored/settled first {R - F - Wn}')
    print(f' (T) face {F}, firewall {Wn} ({sh:.2%} +- {math.sqrt(sh * (1 - sh) / (F + Wn)):.2%}); exposure {E:.4g}')
    print(f'     ln tau_face = {math.log(2 * E / F):.3f} +- {1 / math.sqrt(F):.3f};  ln tau_fw = {math.log(E / Wn):.3f} +- {1 / math.sqrt(Wn):.3f};'
          f'  first-event ln(2E/(F+W)) = {math.log(2 * E / (F + Wn)):.3f}')
    firstdir = np.argmin(fw, 1) + 1
    print(f'     firewall-first by the direction that formed first: {[int(((firstdir == d) & kW).sum()) for d in (1, 2, 3)]}')
    lag = (face - fwm)[kW]
    print(f'     generations firewall -> face death: median {np.median(lag):.4g}, mean {np.mean(lag[np.isfinite(lag)]):.4g}, '
          f'90% {np.quantile(lag, .9):.4g}, beyond the cap {int((~np.isfinite(lag)).sum())}; settled after the firewall, before the face: '
          f'{int(((stop < face) & kW).sum())}')
    # (G) fwslab.py's rules
    B = np.ceil(fwm / K) * K
    det = np.where(face <= B, face, B)                     # fw-first: detection time
    gW = kW & ~(stop < det)                                 # settled between firewall and detection -> censored as settled
    gS = kW & (stop < det)
    endG = np.where(kF, face, np.where(gW, det, np.where(gS, stop, end)))
    EG = endG.sum()
    lab = np.zeros(R, int)
    for d in (3, 2, 1):
        lab = np.where(fw[:, d - 1] <= det, d, lab)
    print(f' (G) face {F}, firewall {int(gW.sum())} (lost to settling: {int(gS.sum())}); exposure {EG:.4g} ({EG / E - 1:+.3%} vs truth)')
    print(f'     ln tau_face = {math.log(2 * EG / F):.3f};  ln tau_fw = {math.log(EG / gW.sum()):.3f};  '
          f'first-event = {math.log(2 * EG / (F + gW.sum())):.3f};  labels {[int(((lab == d) & gW).sum()) for d in (1, 2, 3)]}')


if __name__ == '__main__':
    c = sys.argv[1]; a = list(map(int, sys.argv[2:]))
    if c == 'validate':
        sys.exit(0 if validate(*a) else 1)
    elif c == 'run':
        run(*a)
    else:
        analyze(*a)
