#!/usr/bin/env python3
"""Empty patches on a large living face (the lead's experiment, 2026-11-14).

Slab N x N x m (default 12 x 12 x 8, A = 432 cells per face), soups p = 0.4 as in fwslab.py, kernel B (gsim, shared
memory) stepped one generation per launch; after a burn-in, at every generation a second kernel tests, on both faces
(the outer layers t = 0 and t = m - 1), every translate of every patch shape for "all of the patch's face-layer cells
dead". Shapes (fixed in advance, PREDICTIONS.md): rhombi a x b unit cells (3ab cells; a unit cell = the 3 face-layer
cells of one cube (i, j)), strips 1 x b (b = N wraps the torus), hexagonal balls of radius 1..3 in the face layer's
in-layer neighbour graph (6 neighbours: the kagome 4 + the 2 coplanar diagonal ones). Translates: the N*N unit-cell
positions for rhombi and strips, every face-layer cell as centre for balls. Perimeter: in-layer neighbour pairs with
one cell in the patch and one out.

Counted per (patch item, word-column) on the GPU without atomics; per batch the host sums them. Replicas that freeze
(face death or settling, kernel events) are masked out from that generation on (hits and samples alike); a transverse
firewall (fwslab.firewalled, checked every `fw_every` generations) drops the replica from its detection on.
Also counted: "empty at t and at t + 1" (per item, the previous generation's empty mask is kept).

  modal run research/gpu/modal_app.py::patches ...        (see modal_app.py)
  python3 research/gpu/patches.py table research/data/gpu_patches/*.json   # tables and fits from the committed counts
"""
import json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RHOMBI = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5), (5, 6), (6, 6)]
BALLS = [1, 2, 3]

KERNEL = r'''
typedef unsigned int u32;
extern "C" __global__ void patch_count(const u32* __restrict__ GA, int NP, int WT, const int* __restrict__ cells,
    const int* __restrict__ off, int nitems, const u32* __restrict__ frz, const u32* __restrict__ drop,
    u32* prev, u32* hits, u32* hits2, u32* samples) {
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  if (idx >= nitems * WT) return;
  int item = idx / WT, w = idx % WT;
  u32 acc = 0;
  const u32* col = GA + (size_t)w * NP;
  for (int c = off[item]; c < off[item + 1]; c++) acc |= col[cells[c]];
  u32 mask = ~(frz[w] | drop[w]);
  u32 e = ~acc & mask;
  u32 p = prev[idx];
  prev[idx] = e;
  hits[idx] += __popc(e);
  hits2[idx] += __popc(e & p);
  samples[idx] += __popc(mask);
}
'''


def shapes(N):
    out = [dict(name=f'rhombus {a}x{b}', kind='rhombus', a=a, b=b) for a, b in RHOMBI]
    out += [dict(name=f'strip 1x{b}' + (' (wraps)' if b == N else ''), kind='strip', a=1, b=b) for b in range(1, N + 1)]
    out += [dict(name=f'ball r={r}', kind='ball', r=r) for r in BALLS]
    return out


def geometry(v):
    """per face, per shape: the list of translates, each a list of old node indices; and each shape's cells, perimeter"""
    N1, N2, m = v.N1, v.N2, v.m
    inlayer = [[j for j in v.nb[u] if j >= 0 and v.layer[j] == v.layer[u]] for u in range(v.n)]
    def perim(S):
        S = set(S)
        return sum(1 for u in S for j in inlayer[u] if j not in S)
    faces = []
    for t in (0, m - 1):
        cell = lambda i, j, a: v.key[(i % N1, j % N2, t, a)]
        layer_nodes = [u for u in range(v.n) if v.layer[u] == t]
        per_shape = []
        for sh in shapes(N1):
            items = []
            if sh['kind'] in ('rhombus', 'strip'):
                for i0 in range(N1):
                    for j0 in range(N2):
                        items.append(sorted({cell(i0 + x, j0 + y, a) for x in range(sh['a']) for y in range(sh['b']) for a in range(3)}))
            else:
                for c0 in layer_nodes:
                    seen, front = {c0}, [c0]
                    for _ in range(sh['r']):
                        front = [j for u in front for j in inlayer[u] if j not in seen]
                        seen |= set(front)
                    items.append(sorted(seen))
            per_shape.append(items)
        faces.append(per_shape)
    meta = []
    for k, sh in enumerate(shapes(N1)):
        it = faces[0][k]
        sizes = {len(x) for x in it}; per = {perim(x) for x in it}
        assert len(sizes) == 1 and len(per) == 1, (sh, sizes, per)   # every translate the same shape
        meta.append(dict(sh, cells=sizes.pop(), perimeter=per.pop(), translates=len(it)))
    return faces, meta


def brute(bits, faces):
    """per item (face, shape, translate order): number of replicas whose patch is all dead (bits: (R, n) bool, old order)"""
    out = []
    for per_shape in faces:
        for items in per_shape:
            for cells in items:
                out.append(int((~bits[:, cells].any(1)).sum()))
    return np.array(out, np.int64)


class Counter:
    def __init__(self, s, faces):
        import cupy as cp
        self.cp, self.s = cp, s
        inv = np.empty(s.n, np.int64); inv[s.perm] = np.arange(s.n)
        flat, off = [], [0]
        for per_shape in faces:
            for items in per_shape:
                for cells in items:
                    flat += [int(inv[c]) for c in cells]; off.append(len(flat))
        self.nitems = len(off) - 1
        self.cells, self.off = cp.asarray(np.array(flat, np.int32)), cp.asarray(np.array(off, np.int32))
        self.kern = cp.RawKernel(KERNEL, 'patch_count')
        z = lambda: cp.zeros(self.nitems * s.WT, cp.uint32)
        self.prev, self.hits, self.hits2, self.samples = z(), z(), z(), z()
        self.drop = cp.zeros(s.WT, cp.uint32)

    def reset(self, prev=True):
        for a in ((self.prev,) if prev else ()) + (self.hits, self.hits2, self.samples):
            a[...] = 0

    def count(self):
        s = self.s; tot = self.nitems * s.WT
        self.kern(((tot + 255) // 256,), (256,), (s.A, np.int32(s.n + 1), np.int32(s.WT), self.cells, self.off,
                                                 np.int32(self.nitems), s.frz, self.drop, self.prev, self.hits, self.hits2, self.samples))

    def totals(self):
        cp = self.cp
        f = lambda a: cp.asnumpy(a.reshape(self.nitems, self.s.WT).sum(1, dtype=cp.uint64)).astype(np.int64)
        return f(self.hits), f(self.hits2), f(self.samples)


def per_shape_sums(arr, faces):
    """item array -> per shape (summed over faces and translates)"""
    out = np.zeros(len(faces[0]), np.int64); i = 0
    for per_shape in faces:
        for k, items in enumerate(per_shape):
            out[k] += arr[i:i + len(items)].sum(); i += len(items)
    return out


def run(N=12, m=8, gens=2_000_000, seed=1, p=0.4, burn=2000, batches=32, fw_every=1 << 16, log=print):
    import cupy as cp
    import gsim, fwslab
    from vessels import SlabVessel
    v = SlabVessel(N, N, m)
    faces, meta = geometry(v)
    s = gsim.Sim(v, backend='gpu')
    rs = fwslab.rings(v)
    start_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    t0 = time.time()
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)
    reps, _, kk = s.step(burn)
    burn_events = [int(x) for x in kk]
    c = Counter(s, faces)
    c.reset()
    nb = max(1, gens // batches)
    B = dict(hits=[], hits2=[], samples=[])
    fw_dropped = 0
    g = 0
    while g < gens:
        for _ in range(min(nb, gens - g)):
            s._run((s.blocks,), (s.T,), (s.pk, s.fe, s.A, s.B, np.int32(1), np.int32(1), s.frz, s.ev_t, s.ev_k),
                   shared_mem=s.smem)
            c.count()
            g += 1
            if g % fw_every == 0:
                bits = s.get_all()
                fw, _ = fwslab.firewalled(bits, rs)
                if fw.any():
                    m32 = np.zeros(s.WT, np.uint32)
                    for r in np.nonzero(fw)[0]:
                        m32[r >> 5] |= np.uint32(1) << np.uint32(r & 31)
                    newly = int(np.unpackbits((m32 & ~cp.asnumpy(c.drop)).view(np.uint8)).sum())
                    fw_dropped += newly
                    c.drop |= cp.asarray(m32)
        h, h2, sm = c.totals()
        for k, a in (('hits', h), ('hits2', h2), ('samples', sm)):
            B[k].append(per_shape_sums(a, faces).tolist())
        c.reset(prev=False)
        log(json.dumps(dict(gen=g, elapsed=round(time.time() - t0), samples_6x6=B['samples'][-1][10], hits_6x6=B['hits'][-1][10])))
    frz = cp.asnumpy(s.frz)
    frozen = int(np.unpackbits(frz.view(np.uint8)).sum())
    kinds = cp.asnumpy(s.ev_k)[np.nonzero(np.unpackbits(frz.view(np.uint8), bitorder='little'))[0]].tolist()
    return dict(slab=[N, N, m], A=v.A, seed=seed, p=p, burn=burn, gens=g, replicas=s.R, start_utc=start_utc,
                wall_s=time.time() - t0, burn_events=burn_events, frozen_after_burn=frozen, frozen_kinds=kinds,
                firewall_dropped=fw_dropped, shapes=meta, batches=B)


def validate(N=12, m=8, snapshots=24, seed=7, p=0.4, burn=2000, spacing=97, log=print):
    """the GPU counter against a brute-force count from the definition, on `snapshots` states (all replicas)"""
    import cupy as cp
    import gsim
    from vessels import SlabVessel
    v = SlabVessel(N, N, m)
    faces, meta = geometry(v)
    s = gsim.Sim(v, backend='gpu')
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)
    s.step(burn)
    c = Counter(s, faces)
    ok, total_hits = True, 0
    for k in range(snapshots):
        s.step(spacing)
        c.reset()
        c.count()
        h, _, sm = c.totals()
        bits = s.get_all()
        frz = np.unpackbits(cp.asnumpy(s.frz).view(np.uint8), bitorder='little').astype(bool)
        want = brute(bits[~frz], faces)
        same = np.array_equal(h, want) and int(sm[0]) == int((~frz).sum())
        ok &= same; total_hits += int(want.sum())
        if not same:
            log(f'  snapshot {k}: MISMATCH in {int((h != want).sum())} of {len(want)} items')
    log(f'patch counter vs brute force: {snapshots} states x {s.R} replicas x {c.nitems} items, {total_hits} empty '
        f'patches: {"identical" if ok else "DIFFER"}')
    return ok


def table(paths):
    recs = [json.load(open(p)) for p in paths]
    seeds = [r['seed'] for r in recs]
    if len(set(seeds)) < len(seeds):
        raise SystemExit('two runs with the same seed')
    meta = recs[0]['shapes']
    H = np.sum([np.sum(r['batches']['hits'], 0) for r in recs], 0)
    H2 = np.sum([np.sum(r['batches']['hits2'], 0) for r in recs], 0)
    S = np.sum([np.sum(r['batches']['samples'], 0) for r in recs], 0)
    # batch-means error of ln P (batches of all runs pooled)
    bh = np.concatenate([np.array(r['batches']['hits']) for r in recs]); bs = np.concatenate([np.array(r['batches']['samples']) for r in recs])
    print(f'{len(recs)} runs, {sum(r["gens"] * r["replicas"] for r in recs):.3g} replica-generations after burn-in; '
          f'frozen after burn-in {sum(r["frozen_after_burn"] for r in recs)}, firewall-dropped {sum(r["firewall_dropped"] for r in recs)}')
    print(' shape                cells  perim  translates      samples          hits    ln P            persist P(t,t+1)/P(t)')
    rows = []
    for k, sh in enumerate(meta):
        P = H[k] / S[k] if S[k] else float('nan')
        fr = bh[:, k] / np.maximum(bs[:, k], 1)
        se = (fr.std(ddof=1) / math.sqrt(len(fr)) / P) if H[k] > 0 and P > 0 else float('nan')
        lp = math.log(P) if H[k] > 0 else float('nan')
        per = H2[k] / H[k] if H[k] else float('nan')
        print(f' {sh["name"]:20s} {sh["cells"]:5d} {sh["perimeter"]:6d} {sh["translates"]:10d} {S[k]:14d} {H[k]:12d}   '
              f'{lp:8.3f} +- {se:.3f}   {per:.3f}')
        rows.append(dict(sh, samples=int(S[k]), hits=int(H[k]), hits2=int(H2[k]), lnP=lp, se=se))
    rh = [r for r in rows if r['kind'] == 'rhombus' and r['cells'] >= 12 and r['hits'] >= 10]
    if len(rh) >= 4:
        y = np.array([r['lnP'] for r in rh]); w = 1 / np.array([max(r['se'], 1e-4) for r in rh]) ** 2
        X = np.c_[np.ones(len(rh)), -np.array([r['cells'] for r in rh], float), -np.array([r['perimeter'] for r in rh], float)]
        cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); chi2 = float((w * (y - X @ beta) ** 2).sum())
        print(f'\nfit, rhombi 2x2 and up with >= 10 hits ({len(rh)} shapes): ln P = {beta[0]:.3f} - c cells - sigma perimeter;'
              f' c = {beta[1]:.4f} +- {math.sqrt(cov[1, 1]):.4f}, sigma = {beta[2]:.4f} +- {math.sqrt(cov[2, 2]):.4f}, '
              f'chi2 = {chi2:.1f} for {len(rh) - 3} dof (batch-means errors)')
        inc = [(-(b['lnP'] - a['lnP']) / (b['cells'] - a['cells'])) for a, b in zip(rh[:-1], rh[1:])]
        print('incremental cost per cell along the rhombi:', ', '.join(f'{a["cells"]}->{b["cells"]}: {x:.4f}' for a, b, x in zip(rh[:-1], rh[1:], inc)))
    return rows


if __name__ == '__main__':
    if sys.argv[1] == 'table':
        table(sys.argv[2:])
