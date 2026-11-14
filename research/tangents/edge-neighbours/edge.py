#!/usr/bin/env python3
"""Quick look at the rule the owner meant to write in 2012: B45/S345 where the four coplanar neighbours
are the edge-sharing ones ("edge") instead of the corner-touching ones the code actually reads ("corner" = gump).

  python3 edge.py check        the stepper against reference/oracle.py and a golden log (corner), and against the oracle with swapped offsets (edge)
  python3 edge.py torus        bulk behaviour on a torus, both neighbourhoods
  python3 edge.py confine      does a soup ever leave its box (edge) / its octahedron (corner)?
  python3 edge.py boxes        lifetimes of soups shut in boxes of k x k x k cubes (edge)
  python3 edge.py trace K SEED one run: population and the box of live cells over time
Run from the repository root (check needs reference/)."""
import sys, numpy as np

def offsets(axis, kind):
    a = axis; b, c = [i for i in range(3) if i != a]; offs = []
    if kind == "corner":
        for sb in (2, -2):
            for sc in (2, -2):
                o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(o)
    else:
        for t in (b, c):
            for s in (2, -2):
                o = [0, 0, 0]; o[t] = s; offs.append(o)
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(o)
    return np.array(offs)

class World:
    """Torus of H^3 doubled sites (H even); cells are the sites with exactly one odd coordinate."""
    def __init__(self, H, kind):
        self.H = H
        g = np.indices((H, H, H)).reshape(3, -1).T
        par = g % 2
        keep = par.sum(1) == 1
        self.xyz = g[keep]; self.axis = par[keep].argmax(1); self.M = len(self.xyz)
        lut = -np.ones(H ** 3, np.int64); flat = (self.xyz[:, 0] * H + self.xyz[:, 1]) * H + self.xyz[:, 2]; lut[flat] = np.arange(self.M)
        self.nb = np.zeros((self.M, 12), np.int64)
        for a in range(3):
            m = self.axis == a; q = (self.xyz[m][:, None, :] + offsets(a, kind)[None]) % H
            self.nb[m] = lut[(q[..., 0] * H + q[..., 1]) * H + q[..., 2]]
        assert (self.nb >= 0).all()
    def step(self, s):                      # s: (runs, M) uint8
        n = s[:, self.nb].sum(2, dtype=np.uint8)
        return (((n + s) >= 4) & (n < 6)).astype(np.uint8)
    def box(self, lo, hi):                  # cells with every coordinate in [lo, hi]
        return ((self.xyz >= lo) & (self.xyz <= hi)).all(1)

def check():
    sys.path.insert(0, "reference"); import oracle
    H = 40; lo, hi = oracle.legacy_seed_span(H)
    ref = [int(l.split()[1]) for l in open("reference/golden/legacy_cube_side08_H40.txt") if l.strip()]
    w = World(H, "corner"); s = w.box(lo, hi).astype(np.uint8)[None]
    bad = 0
    for g in range(1, len(ref)):
        s = w.step(s); bad += int(s.sum()) != ref[g]
    print("corner stepper vs golden side-8 log: mismatches", bad)
    for kind in ("corner", "edge"):
        H = 24; w = World(H, kind); rng = np.random.default_rng(7); s = (rng.random((1, w.M)) < 0.4).astype(np.uint8)
        oracle.offsets = (lambda a, k=kind: [tuple(o) for o in offsets(a, k)])
        m = oracle.masks(H); h = np.zeros((H, H, H), np.int8); h[w.xyz[:, 0], w.xyz[:, 1], w.xyz[:, 2]] = s[0]
        bad = 0
        for g in range(60):
            s = w.step(s); h = oracle.step(h, m); bad += not np.array_equal(h[w.xyz[:, 0], w.xyz[:, 1], w.xyz[:, 2]], s[0])
        print(kind, "stepper vs oracle.step with the same offsets, random torus state, 60 generations: mismatches", bad)

def torus():
    for kind in ("corner", "edge"):
        w = World(32, kind); rng = np.random.default_rng(1)
        for p in (0.15, 0.3, 0.5, 0.7):
            s = (rng.random((4, w.M)) < p).astype(np.uint8); out = []
            for g in range(1, 2001):
                t = w.step(s)
                if g in (10, 100, 500, 1000, 2000): out.append((g, round(float(t.mean()), 4), round(float((t != s).mean()), 4)))
                s = t
            n = s[:, w.nb].sum(2); over = float(((n >= 6)).mean())
            print(f"{kind:6s} torus 16^3 cubes, start density {p}: (generation, density, share changing) {out}  overcrowded {over:.3f}")

def confine():
    rng = np.random.default_rng(3)
    for kind in ("edge", "corner"):
        H = 56; c = 28; w = World(H, kind); half = 7
        inbox = w.box(c - half, c + half)
        s = ((rng.random((16, w.M)) < 0.4) & inbox).astype(np.uint8)
        d = np.abs(w.xyz - c); l1 = d.sum(1); linf = d.max(1)
        l10 = int(l1[s.any(0)].max())
        for g in range(400): s = w.step(s)
        ever = s.any(0)
        print(f"{kind:6s}: 16 soups in a box of half-width {half} (odd planes), 400 generations: largest |coordinate| now {int(linf[ever].max())}; "
              f"L1 radius at start {l10}, now {int(l1[ever].max())}; live {s.sum(1).min()}..{s.sum(1).max()}")

def run_boxes(k, runs, cap, kind="edge", seed=0, p=0.4):
    """Soups in a closed box of k^3 cubes. Returns the generation by which each run was first seen back at a
    snapshot taken at most 256 generations earlier (so periodic with period <= 256), i.e. the lifetime to within 256."""
    H = 2 * k + 8; H += H % 2; lo = 3; hi = lo + 2 * k            # odd planes lo..hi, three empty layers of padding all round
    w = World(H, kind); inbox = w.box(lo, hi); rng = np.random.default_rng(seed)
    s = ((rng.random((runs, w.M)) < p) & inbox).astype(np.uint8)
    life = np.full(runs, -1); alive = np.ones(runs, bool); snap = s.copy(); snap_t = 0; idx = np.arange(runs)
    escaped = False
    for g in range(1, cap + 1):
        s = w.step(s)
        if g % 256 == 0:
            escaped |= bool((s & ~inbox).any())
        same = (s == snap).all(1)
        if same.any():
            life[idx[same]] = snap_t; keep = ~same
            s = s[keep]; snap = snap[keep]; idx = idx[keep]
            if len(idx) == 0: break
        if g % 256 == 0: snap = s.copy(); snap_t = g
    return life, int(inbox.sum()), escaped

def boxes():
    for kind in ("edge",):
        for k, runs, cap in ((2, 64, 20000), (3, 64, 20000), (4, 64, 40000), (5, 48, 60000), (6, 32, 60000), (7, 24, 40000)):
            life, cells, esc = run_boxes(k, runs, cap, kind)
            done = life[life >= 0]; cens = int((life < 0).sum())
            med = "over cap" if cens > runs // 2 else int(np.sort(np.where(life < 0, cap * 10, life))[runs // 2])
            print(f"{kind} box {k}^3 cubes ({cells} cells), {runs} soups, cap {cap}: median lifetime {med}; finished {len(done)}, still running {cens}; "
                  f"quartiles of finished {np.percentile(done, [25, 50, 75]).astype(int).tolist() if len(done) else '-'}; left the box: {esc}", flush=True)

def trace(k, seed, cap=200000):
    H = 2 * k + 8; lo = 3; hi = lo + 2 * k
    w = World(H, "edge"); inbox = w.box(lo, hi); rng = np.random.default_rng(seed)
    s = ((rng.random((1, w.M)) < 0.4) & inbox).astype(np.uint8)
    last = None; snap = s.copy(); pops = []
    for g in range(1, cap + 1):
        s = w.step(s); live = w.xyz[s[0] > 0]
        ext = tuple(live.min(0).tolist() + live.max(0).tolist()) if len(live) else None
        if ext != last: print(g, "population", int(s.sum()), "live box (min xyz, max xyz)", ext, flush=True); last = ext
        pops.append(int(s.sum()))
        if (s == snap).all(): print("periodic by generation", g, "population", int(s.sum())); break
        if g % 256 == 0: snap = s.copy()
    q = np.array(pops); n = len(q) // 10 or 1
    print("mean population in tenths of the run:", [int(q[i * n:(i + 1) * n].mean()) for i in range(10)])

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "trace": trace(int(sys.argv[2]), int(sys.argv[3]))
    else: {"check": check, "torus": torus, "confine": confine, "boxes": boxes}[cmd]()
