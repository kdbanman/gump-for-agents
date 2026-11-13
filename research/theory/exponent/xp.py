"""xp: graph builders and run driver for drv.c (research/theory/exponent).

Vessels / models (all return a graph dict; `gfile` writes it once under research/scratch/exponent/):
  toy_strip(H, L)            the toy (cross2, B34/S234) in a strip of H rows, L columns periodic along the edge; rows
                             outside dead.  Events: 0 = top edge row empty, 1 = bottom edge row empty, then interior
                             firewalls (3 adjacent dead rows), then transverse cuts (3 adjacent dead columns).
  toy_model(w, L)            DRIVEN-EDGE MODEL: rows 0..w-1 follow the rule; rows w and w+1 are i.i.d. Bernoulli noise
                             redrawn every generation (noise classes 0 and 1).  Event 0 = edge row empty; then
                             firewalls inside the dynamic rows.
  toy_slave(H, L, w, d)      a full strip (the donor) plus a slave copy of w rows whose two rows "below" are read
                             from donor rows d and d+1 (one-way coupling: true statistics, no feedback).
  gump_model(R, w)           the same recipe for gump: the top w {111} layers of the octahedral hull |p|_1 <= R follow
                             B45/S345, the next two layers are noise.  Event 0 = the face layer empty.
  gump_hull(R)               the full hull (deterministic), 8 faces; events 0..7 = a face layer empty.
run(name, graph, ...)        accumulate qsd chunks until `deaths` events of kind `nev` or `maxsec`; JSON in scratch.
"""
import json, os, struct, subprocess, sys, time, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'exponent'))
os.makedirs(SCR, exist_ok=True)
TOY = (24, 28)      # B34/S234 as masks
GUMP = (48, 56)     # B45/S345
CROSS2 = [(1, 0), (-1, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2)]


def compile_bin(W=4, src='drv.c', name='drv', extra=()):
    out = os.path.join(SCR, name + ('' if W == 4 else '_w%d' % W))
    s = os.path.join(HERE, src)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(s):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-DW=%d' % W, *extra, '-o', out, s, '-lm'])
    return out


def write_graph(g, fn):
    nb = np.asarray(g['nb'], '<i4')
    with open(fn, 'wb') as f:
        f.write(struct.pack('<iii', g['N'], g['M'], nb.shape[1]))
        f.write(nb.tobytes())
        f.write(np.asarray(g.get('cls', np.zeros(g['M'])), '<i4').tobytes())
        f.write(struct.pack('<i', len(g['lines'])))
        for flag, cl in g['lines']:
            f.write(struct.pack('<ii', flag, len(cl))); f.write(np.asarray(cl, '<i4').tobytes())
        f.write(struct.pack('<i', len(g['events'])))
        for ev in g['events']:
            f.write(struct.pack('<i', len(ev))); f.write(np.asarray(ev, '<i4').tobytes())
        pr = g.get('profs', [])
        f.write(struct.pack('<i', len(pr)))
        for ev, ls in pr:
            f.write(struct.pack('<ii', ev, len(ls))); f.write(np.asarray(ls, '<i4').tobytes())


def gfile(g):
    fn = os.path.join(SCR, 'g_%s.bin' % g['name'])
    if not os.path.exists(fn):
        write_graph(g, fn)
    return fn


def toy_strip(H, L, offs=CROSS2, fw=3):
    idx = lambda y, x: y * L + (x % L)
    nb = np.full((H * L, len(offs)), -1, int)
    for y in range(H):
        for x in range(L):
            for k, (dx, dy) in enumerate(offs):
                if 0 <= y + dy < H:
                    nb[idx(y, x), k] = idx(y + dy, x + dx)
    lines = []
    for y in range(H):
        flag = 7 if y in (0, H - 1) else (4 if (y < 4 or y >= H - 4) else 0)
        lines.append((flag, [idx(y, x) for x in range(L)]))
    for x in range(L):
        lines.append((0, [idx(y, x) for y in range(H)]))
    events = [[0], [H - 1]] + [list(range(y, y + fw)) for y in range(1, H - fw)]
    events += [[H + (x + j) % L for j in range(fw)] for x in range(L)]
    profs = [(0, list(range(0, min(4, H)))), (1, list(range(H - 1, max(H - 5, -1), -1)))]
    return dict(name='toy_strip_%dx%d' % (H, L), N=H * L, M=0, nb=nb, lines=lines, events=events, profs=profs,
                nedge=2, shape=(H, L))


def toy_model(w, L, offs=CROSS2, fw=3):
    N, M = w * L, 2 * L
    def idx(y, x):
        return y * L + (x % L)          # rows w, w+1 are the noise cells N .. N+2L-1
    nb = np.full((N, len(offs)), -1, int)
    for y in range(w):
        for x in range(L):
            for k, (dx, dy) in enumerate(offs):
                if 0 <= y + dy < w + 2:
                    nb[idx(y, x), k] = idx(y + dy, x + dx)
    cls = [0] * L + [1] * L
    lines = [((7 if y == 0 else 4), [idx(y, x) for x in range(L)]) for y in range(w)]
    events = [[0]] + [list(range(y, y + fw)) for y in range(1, w - fw + 1)]
    profs = [(0, list(range(0, min(4, w))))]
    return dict(name='toy_model_w%d_L%d' % (w, L), N=N, M=M, nb=nb, cls=cls, lines=lines, events=events, profs=profs,
                nedge=1, shape=(w, L))


def toy_slave(H, L, w, d, offs=CROSS2, fw=3):
    g = toy_strip(H, L, offs, fw)
    N0 = H * L
    sid = lambda y, x: N0 + y * L + (x % L)
    did = lambda y, x: y * L + (x % L)
    nb = np.full((N0 + w * L, len(offs)), -1, int)
    nb[:N0] = g['nb']
    for y in range(w):
        for x in range(L):
            for k, (dx, dy) in enumerate(offs):
                yy = y + dy
                if 0 <= yy < w:
                    nb[sid(y, x), k] = sid(yy, x + dx)
                elif yy >= w:
                    nb[sid(y, x), k] = did(d + (yy - w), x + dx)
    nl0 = len(g['lines'])
    lines = [(0, c) for f, c in g['lines']] + [((7 if y == 0 else 4), [sid(y, x) for x in range(L)]) for y in range(w)]
    events = [[nl0]] + g['events'] + [[nl0 + y + j for j in range(fw)] for y in range(1, w - fw + 1)]
    profs = [(0, [nl0 + y for y in range(min(4, w))])]
    return dict(name='toy_slave_%dx%d_w%d_d%d' % (H, L, w, d), N=N0 + w * L, M=0, nb=nb, lines=lines, events=events,
                profs=profs, nedge=1, shape=(H, L))


# ---------------------------------------------------------------------------------------------------- gump
def gump_offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(tuple(v))
    for o in (b, c):
        for sa in (1, -1):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(tuple(v))
    return out


GOFF = [gump_offsets(a) for a in range(3)]


def hull_cells(R):
    r = range(-R, R + 1)
    return [(x, y, z) for x in r for y in r for z in r
            if (x % 2) + (y % 2) + (z % 2) == 1 and abs(x) + abs(y) + abs(z) <= R]


def gump_model(R, w, fw=3):
    cells = [p for p in hull_cells(R) if sum(p) >= R - 2 * (w + 1)]
    dyn = [p for p in cells if sum(p) >= R - 2 * (w - 1)]
    noi = [p for p in cells if sum(p) < R - 2 * (w - 1)]
    ix = {p: i for i, p in enumerate(dyn)}
    ix.update({p: len(dyn) + i for i, p in enumerate(noi)})
    nb = np.full((len(dyn), 12), -1, int)
    for i, p in enumerate(dyn):
        a = [c % 2 for c in p].index(1)
        for k, o in enumerate(GOFF[a]):
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            if q in ix:
                nb[i, k] = ix[q]
    cls = [0 if sum(p) == R - 2 * w else 1 for p in noi]
    lines = [((5 if y == 0 else 4), [ix[p] for p in dyn if sum(p) == R - 2 * y]) for y in range(w)]
    events = [[0]] + [list(range(y, y + fw)) for y in range(1, w - fw + 1)]
    profs = [(0, list(range(0, min(4, w))))]
    return dict(name='gump_model_R%d_w%d' % (R, w), N=len(dyn), M=len(noi), nb=nb, cls=cls, lines=lines,
                events=events, profs=profs, nedge=1, A=len(lines[0][1]))


def gump_hull(R):
    cells = hull_cells(R)
    ix = {p: i for i, p in enumerate(cells)}
    nb = np.full((len(cells), 12), -1, int)
    for i, p in enumerate(cells):
        a = [c % 2 for c in p].index(1)
        for k, o in enumerate(GOFF[a]):
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            if q in ix:
                nb[i, k] = ix[q]
    lines = []
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                lines.append((1, [ix[p] for p in cells if sx * p[0] + sy * p[1] + sz * p[2] == R]))
    events = [[i] for i in range(8)]
    return dict(name='gump_hull_R%d' % R, N=len(cells), M=0, nb=nb, lines=lines, events=events, nedge=8,
                A=len(lines[0][1]))


def slab_cells(a, b, layers):
    """cells of {111} layers s = x+y+z in `layers`, modulo the in-plane translations (2a,-2a,0), (0,2b,-2b):
    canonical representative (x mod 2a, y mod 2b, s).  3ab cells per layer (a kagome torus of a x b unit cells)."""
    out = []
    for s in layers:
        for x in range(2 * a):
            for y in range(2 * b):
                z = s - x - y
                if (x % 2) + (y % 2) + (z % 2) == 1:
                    out.append((x, y, s))
    return out


def _slab_nb(cells, a, b, dynamic):
    ix = {c: i for i, c in enumerate(cells)}
    nb = np.full((dynamic, 12), -1, int)
    for i, (x, y, s) in enumerate(cells[:dynamic]):
        p = (x, y, s - x - y)
        ax = [c % 2 for c in p].index(1)
        for k, o in enumerate(GOFF[ax]):
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            c = (q[0] % (2 * a), q[1] % (2 * b), sum(q))
            if c in ix:
                nb[i, k] = ix[c]
    return nb, ix


def gump_slab(a, b, m, fw=3):
    """Deterministic slab of m {111} layers, periodic in-plane (a x b kagome cells, 3ab cells per layer); both
    outer layers are faces.  Events: 0, 1 = a face layer empty; then interior firewalls (3 adjacent dead layers);
    then oblique firewalls (3 adjacent dead layers of one of the other three diagonals, which wrap the torus)."""
    layers = [-(2 * j + 1) for j in range(m)]           # s = -1, -3, ..., top face first
    cells = slab_cells(a, b, layers)
    nb, ix = _slab_nb(cells, a, b, len(cells))
    lines = [((5 if j in (0, m - 1) else (4 if (j < 4 or j >= m - 4) else 0)), [ix[c] for c in cells if c[2] == s])
             for j, s in enumerate(layers)]
    events = [[0], [m - 1]] + [list(range(y, y + fw)) for y in range(1, m - fw)]
    # oblique layers: s' = s - 2x (period 4a), s - 2y (period 4b), s - 2z = 2x + 2y - s (constant on the torus classes
    # only modulo gcd; use the class of (x + y) modulo 2*lcm-free: handled by brute force below)
    for name, f, per in (('x', lambda x, y, s: (s - 2 * x) % (4 * a), 4 * a), ('y', lambda x, y, s: (s - 2 * y) % (4 * b), 4 * b)):
        vals = sorted(set(f(*c) for c in cells))
        base = len(lines)
        for v in vals:
            lines.append((0, [ix[c] for c in cells if f(*c) == v]))
        nv = len(vals)
        events += [[base + (i + j) % nv for j in range(fw)] for i in range(nv)]
    if a == b:                                           # third oblique family is periodic only on square tori
        f = lambda x, y, s: (2 * x + 2 * y - s) % (4 * a)
        vals = sorted(set(f(*c) for c in cells)); base = len(lines)
        for v in vals:
            lines.append((0, [ix[c] for c in cells if f(*c) == v]))
        nv = len(vals)
        events += [[base + (i + j) % nv for j in range(fw)] for i in range(nv)]
    profs = [(0, list(range(0, min(4, m)))), (1, list(range(m - 1, max(m - 5, -1), -1)))]
    return dict(name='gump_slab_%dx%d_m%d' % (a, b, m), N=len(cells), M=0, nb=nb, lines=lines, events=events,
                profs=profs, nedge=2, A=3 * a * b)


def gump_slab_model(a, b, w, fw=3):
    """Driven-face model with a periodic face: top w layers follow the rule, the next two are noise."""
    layers = [-(2 * j + 1) for j in range(w + 2)]
    cells = slab_cells(a, b, layers)
    N = 3 * a * b * w
    nb, ix = _slab_nb(cells, a, b, N)
    cls = [0 if c[2] == layers[w] else 1 for c in cells[N:]]
    lines = [((5 if j == 0 else 4), [ix[c] for c in cells if c[2] == layers[j]]) for j in range(w)]
    events = [[0]] + [list(range(y, y + fw)) for y in range(1, w - fw + 1)]
    profs = [(0, list(range(0, min(4, w))))]
    return dict(name='gump_slabmodel_%dx%d_w%d' % (a, b, w), N=N, M=len(cells) - N, nb=nb, cls=cls, lines=lines,
                events=events, profs=profs, nedge=1, A=3 * a * b)


# ---------------------------------------------------------------------------------------------------- runs
def read_out(fn):
    d = {}
    for line in open(fn):
        k, *v = line.split()
        v = [float(t) for t in v]
        d[k] = v[0] if len(v) == 1 else np.array(v)
    return d


ACC = ['exposure', 'deaths', 'early', 'settles', 'settles_exposed', 'gapN']
VEC = ['deaths_by_event', 'age_exposure', 'age_deaths', 'hist', 'trans', 'gapE']


def qsd(g, rule, p, seed, T0, gens, out, rho=None, eps=0.0, W=4):
    exe = compile_bin(W)
    cmd = [exe, 'qsd', gfile(g), str(rule[0]), str(rule[1]), str(p), str(seed), str(T0), str(int(gens)), out]
    cmd.append(','.join('%.6f' % r for r in (rho if rho else [0.5])))
    cmd.append(repr(float(eps)))
    subprocess.run(cmd, check=True)
    return read_out(out)


def dbfile(tag):
    return os.path.join(SCR, 'runs_%s.json' % tag)


def run(key, g, rule=TOY, p=0.4, T0=300, deaths=400, maxsec=600, rho=None, eps=0.0, tag='main', chunk=2000, nev=None,
        W=4, quiet=False):
    """Accumulate chunks for record `key` in runs_<tag>.json until `deaths` events among the first `nev` events
    (default: the graph's nedge) or `maxsec` of wall time in this call."""
    fn = dbfile(tag)
    db = json.load(open(fn)) if os.path.exists(fn) else {}
    nev = nev or g.get('nedge', 1)
    rec = db.get(key) or dict(chunks=0, nedge=nev, graph=g['name'], rule=list(rule), p=p, T0=T0, rho=rho, eps=eps,
                              cells=g['N'], llen=len(g['lines'][0][1]), **{k: 0 for k in ACC}, **{k: [] for k in VEC},
                              ages=[], prof={})
    t0 = time.time(); gens = rec.get('lastgens', chunk)
    out = os.path.join(SCR, 'tmp_%s_%s.txt' % (tag, key))
    while time.time() - t0 < maxsec:
        ev = rec['deaths_by_event']
        if ev and sum(ev[:nev]) >= deaths:
            break
        tc = time.time()
        d = qsd(g, rule, p, 7919 * rec['chunks'] + 104729 * (zlib.crc32(key.encode()) % 9973) + 17, T0, gens, out, rho, eps, W)
        dt = time.time() - tc
        rec['chunks'] += 1
        for k in ACC:
            rec[k] += d[k]
        for k in VEC:
            v = list(np.atleast_1d(d[k])); rec[k] = [a + b for a, b in zip(rec[k] or [0] * len(v), v)]
        for k in d:
            if k.startswith('prof'):
                v = list(np.atleast_1d(d[k])); old = rec['prof'].get(k)
                rec['prof'][k] = [a + b for a, b in zip(old, v)] if old else v
        for line in open(out + '.deaths'):
            e, age = map(int, line.split())
            if e < nev and len(rec['ages']) < 20000:
                rec['ages'].append(age)
        gens = int(min(max(gens * min(4.0, 40.0 / max(dt, 1e-3)), 1000), 2e8)); rec['lastgens'] = gens
        db = json.load(open(fn)) if os.path.exists(fn) else {}
        db[key] = rec
        json.dump(db, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
    s = summary(rec)
    if not quiet:
        print('%-28s expo %.3g deaths %d other %d settles %d  tau = %.4g  ln tau = %.3f +- %.3f  p1 %.3g h/p1 %.3f' %
              (key, rec['exposure'], s['deaths'], s['other'], rec['settles'], s['tau'], s['lntau'], s['err'],
               s['p'][1] if len(s['p']) > 1 else float('nan'), s['h_over_p1']), flush=True)
    return rec


def summary(rec):
    nev = rec['nedge']; ev = rec['deaths_by_event'] or [0]
    d = sum(ev[:nev]); expo = rec['exposure']
    h = d / (nev * expo) if expo and d else float('nan')
    hist = np.array(rec['hist'] or [0.0]); tot = hist.sum()
    p = hist / tot if tot else hist
    return dict(deaths=int(d), other=int(sum(ev[nev:])), h=h, tau=1 / h if h == h else float('inf'),
                lntau=-np.log(h) if h == h else float('inf'), err=1 / np.sqrt(d) if d else float('nan'), p=p,
                h_over_p1=h / p[1] if len(p) > 1 and p[1] > 0 else float('nan'),
                mean=float((p * np.arange(len(p))).sum()), var=float((p * np.arange(len(p)) ** 2).sum() - (p * np.arange(len(p))).sum() ** 2))


def load(tag):
    fn = dbfile(tag)
    return json.load(open(fn)) if os.path.exists(fn) else {}


if __name__ == '__main__':
    print(compile_bin())
