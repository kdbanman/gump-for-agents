#!/usr/bin/env python3
"""blast/holes: tables from the output of `holes run`.
   python3 ana.py torus SLABFILE...          f(a,b), mixed second differences, triangles, how patches empty
   python3 ana.py hull HULLFILE... [--torus SLABFILE...]   interior against torus, distance map, corner, rim strips,
                                                 triangles with 0, 1, 2 real rims, how patches empty by position
   Several files of the same vessel are pooled (their lane groups are all treated as independent runs).
Errors: delete-one-group jackknife over the independent groups of 32 lanes (8 per file)."""
import sys, math, json
import numpy as np

TRI = 9
def load(fns):
    T = {}; P = {}; meta = None; gens = 0; grp_off = 0; per = []
    for fn in fns:
        m = {}; rows = []; prow = []
        for line in open(fn):
            w = line.split()
            if not w: continue
            if w[0] == 'H' and w[1] == 'vessel':
                m = {w[i]: w[i + 1] for i in range(1, len(w) - 1, 2)}
            elif w[0] == 'H':
                m['facedensity'] = float(w[2]); m['emptyface'] = int(w[4])
            elif w[0] == 'T':
                rows.append((tuple(map(int, w[1:6])), int(w[6]), np.array(list(map(float, w[7:15])))))
            elif w[0] == 'P':
                prow.append(w)
        per.append((m, rows, prow))
    ng = 8 * len(per)
    gens = [int(m['gens']) for m, _, _ in per]
    for fi, (m, rows, prow) in enumerate(per):
        for key, stride, c in rows:
            if key not in T: T[key] = np.zeros(ng)
            # store as probability numerators normalised to "counts per generation of exposure" later: keep
            # counts*stride so that pooled files with equal weights per generation add correctly
            T[key][8 * fi:8 * fi + 8] = c * stride
        for w in prow:
            key = tuple(map(int, w[1:6]))
            d = P.setdefault(key, dict(n=0, old=0, re=0, bust=0, full=0, face=np.zeros(10), ben=np.zeros(10), fall=np.zeros(21)))
            n = int(w[w.index('n') + 1])
            d['n'] += n; d['old'] += int(w[w.index('old') + 1]); d['re'] += int(w[w.index('re') + 1])
            d['bust'] += int(w[w.index('bust') + 1]); d['full'] += int(w[w.index('full') + 1])
            i = w.index('face'); d['face'] += n * np.array(list(map(float, w[i + 1:i + 11])))
            i = w.index('ben'); d['ben'] += n * np.array(list(map(float, w[i + 1:i + 11])))
            i = w.index('fall'); d['fall'] += np.array(list(map(float, w[i + 1:i + 22])))
    meta = per[0][0]; meta['gens_each'] = gens; meta['ng'] = ng
    # exposure per group, in lane-generations: gens * 32 for the groups of each file
    meta['expo'] = np.repeat(np.array(gens, float) * 32, 8)
    meta['emptyface'] = sum(m['emptyface'] for m, _, _ in per)
    meta['facedensity'] = [m['facedensity'] for m, _, _ in per]
    return meta, T, P

class Q:
    """A quantity sum_i w_i * (-ln P_i), P_i = counts_i / (exposure * translates_i), with a jackknife error."""
    def __init__(self, terms):   # terms: list of (w, countvec, expovec*translates)
        self.terms = terms
    def __add__(self, o): return Q(self.terms + o.terms)
    def __sub__(self, o): return Q(self.terms + [(-w, c, e) for w, c, e in o.terms])
    def __rmul__(self, k): return Q([(k * w, c, e) for w, c, e in self.terms])
    def val(self):
        v = 0.0
        for w, c, e in self.terms:
            if c.sum() <= 0: return float('nan')
            v += -w * math.log(c.sum() / e.sum())
        return v
    def err(self):
        ng = len(self.terms[0][1]); qs = []
        for g in range(ng):
            v = 0.0
            for w, c, e in self.terms:
                cc = c.sum() - c[g]
                if cc <= 0: return float('inf')
                v += -w * math.log(cc / (e.sum() - e[g]))
            qs.append(v)
        qs = np.array(qs)
        return math.sqrt((ng - 1) / ng * ((qs - qs.mean()) ** 2).sum())
    def hits(self): return min(c.sum() for w, c, e in self.terms)
    def s(self, nd=4):
        v, e = self.val(), self.err()
        if math.isnan(v): return '      -      '
        if not math.isfinite(e): return f'{v:.{nd}f}(?)'
        return f'{v:.{nd}f}±{e:.{nd}f}'

def torus_tables(meta, T):
    n = int(meta['n']); expo = meta['expo']
    def f(cls, a, b):       # class 0 = P (grids 0, 2), 1 = Q (grids 1, 3); a x b and b x a pooled
        c = np.zeros(meta['ng']); ntr = 0
        # triangles: only the top face's grid has the hull face's orientation (the bottom grid, built by inversion,
        # holds the triangle turned by 180 degrees: cls 2 and 3 return that one)
        if b == TRI: keys = {(cls, a, TRI, 0, 0)}
        else: keys = {(g, x, y, 0, 0) for g in (cls % 2, cls % 2 + 2) for (x, y) in ((a, b), (b, a))}
        for k in keys:
            ntr += n * n
            if k in T: c = c + T[k]
        return Q([(1.0, c, expo * ntr)])
    return f

def M(f, a, b):  # mixed second difference at (a+1/2, b+1/2)
    return f(a + 1, b + 1) - f(a + 1, b) - f(a, b + 1) + f(a, b)

def extrap(f):
    """Where does the bulk cost per cell go? (1) strips: the cost of one more unit of length of a strip a wide,
       I_a(b) = f(a,b+1) - f(a,b), extrapolated in b by Shanks' rule on its last three good values; the price of
       the a-th row of a long strip is then [eps(a) - eps(a-1)]/3. (2) fits M/3 = c + U(a+1/2) + U(b+1/2)."""
    print('\nextrapolations of the bulk cost (class P) [model-dependent]')
    eps = {}
    for a in range(1, 5):
        I = []
        for b in range(1, 8):
            q = f(0, a, b + 1) - f(0, a, b)
            if math.isnan(q.val()) or not math.isfinite(q.err()) or q.err() > 0.03: break
            I.append((q.val(), q.err()))
        if len(I) < 3: continue
        x0, x1, x2 = I[-3][0], I[-2][0], I[-1][0]
        den = (x2 - x1) - (x1 - x0)
        sh = x2 - (x2 - x1) ** 2 / den if abs(den) > 1e-9 and 0 < (x2 - x1) / (x1 - x0) < 1 else float('nan')
        eps[a] = (x2, sh, len(I))
        print(f'  strip {a} wide: last increment (b={len(I)}->{len(I)+1}) {x2:.4f}±{I[-1][1]:.4f}; ratio of the last two steps {(x2-x1)/(x1-x0):.2f}; Shanks limit {sh:.4f}')
    for a in range(2, 5):
        if a in eps and a - 1 in eps:
            print(f'  price per cell of row {a} of a long strip: from last increments {(eps[a][0]-eps[a-1][0])/3:.4f}, from Shanks limits {(eps[a][1]-eps[a-1][1])/3:.4f}')
    pts = []
    for a in range(1, 5):
        for b in range(a, 8):
            q = (1 / 3) * M(lambda x, y: f(0, x, y), a, b)
            if math.isnan(q.val()) or not math.isfinite(q.err()) or q.err() > 0.012: continue
            pts.append((a + .5, b + .5, q.val(), q.err()))
    for amin in (1.5, 2.5):
        sel = [p for p in pts if p[0] >= amin]
        if len(sel) < 4: continue
        y = np.array([p[2] for p in sel]); e = np.array([max(p[3], 0.001) for p in sel])   # 0.001: a floor for model error
        for name, U in (('exp(-x/xi)', lambda x, t: np.exp(-x / t)), ('x^-p', lambda x, t: x ** (-t))):
            best = None
            for t in np.arange(0.3, 8.01, 0.05):
                X = np.stack([np.ones(len(sel)), np.array([U(p[0], t) + U(p[1], t) for p in sel])], 1)
                co, *_ = np.linalg.lstsq(X / e[:, None], y / e, rcond=None)
                chi = float((((X @ co) - y) / e) ** 2 @ np.ones(len(sel)))
                if best is None or chi < best[0]: best = (chi, t, co[0], co[1])
            ok = [None, None]
            for t in np.arange(0.3, 8.01, 0.05):
                X = np.stack([np.ones(len(sel)), np.array([U(p[0], t) + U(p[1], t) for p in sel])], 1)
                co, *_ = np.linalg.lstsq(X / e[:, None], y / e, rcond=None)
                chi = float((((X @ co) - y) / e) ** 2 @ np.ones(len(sel)))
                if chi < best[0] * (1 + 4.0 / max(1, len(sel) - 3)) + 0.0:
                    ok = [co[0] if ok[0] is None else min(ok[0], co[0]), co[0] if ok[1] is None else max(ok[1], co[0])]
            print(f'  fit M/3 = c + B[U(a+1/2) + U(b+1/2)], U = {name}, {len(sel)} values with a+1/2 >= {amin}: c = {best[2]:.4f} (range {ok[0]:.4f} .. {ok[1]:.4f}), parameter {best[1]:.2f}, B = {best[3]:.3f}, chi2 = {best[0]:.1f} on {len(sel)-3}')

def show_pre(P, sel, title):
    print(title)
    print('  shape  where          events  not-new  flicker  bust-share  over-full-share   patch density at lags 1..5 | layer beneath at lags 0..4')
    for name, keys in sel:
        d = None
        for k in keys:
            if k not in P: continue
            if d is None: d = {x: (v.copy() if hasattr(v, 'copy') else v) for x, v in P[k].items()}
            else:
                for x in d: d[x] = d[x] + P[k][x]
        if d is None or d['n'] == 0: continue
        nn = d['n']
        print(f"  {name:22s} {nn:8d} {d['old']:8d} {d['re']:7d}   {d['bust']/nn:.3f}±{math.sqrt(d['bust']*(nn-d['bust'])/nn**3):.3f}     {d['full']/nn:.3f}        "
              + ' '.join(f'{x/nn:.3f}' for x in d['face'][1:6]) + ' | ' + ' '.join(f'{x/nn:.3f}' for x in d['ben'][0:5]))

def main():
    args = sys.argv[1:]
    mode = args[0]; rest = args[1:]
    tor = []
    if '--torus' in rest:
        i = rest.index('--torus'); tor = rest[i + 1:]; rest = rest[:i]
    if mode == 'torus':
        meta, T, P = load(rest)
        f = torus_tables(meta, T)
        print(f"torus {meta['n']}x{meta['n']}x{meta['L']}: generations {meta['gens_each']}, lanes 256 each, face density {meta['facedensity']}, empty-face checks {meta['emptyface']}")
        print('\n-ln P(a x b rhombus empty), class P (outward triangles, the hull kind); a down, b across')
        for a in range(1, 7): print(f'  a={a} ' + ' '.join(f'{f(0, a, b).s():>15s}' for b in range(a, 9)))
        print('hits: ' + ' | '.join(' '.join(f'{int(f(0, a, b).hits())}' for b in range(a, 9)) for a in range(1, 7)))
        print('\nsame, class Q (inward triangles)')
        for a in range(1, 7): print(f'  a={a} ' + ' '.join(f'{f(1, a, b).s():>15s}' for b in range(a, 9)))
        print('\nboth classes averaged in P (as the GPU table did): 2x2 6.254, 2x3 8.793, 3x3 12.128, 3x4 15.3999/15.3979, 4x4 19.4233/19.4183, 4x5 23.364±0.034')
        for a, b in ((1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)):
            c = np.zeros(meta['ng'])
            for g in range(4):
                for k in {(g, a, b, 0, 0), (g, b, a, 0, 0)}:
                    if k in T: c = c + T[k]
            q = Q([(1.0, c, meta['expo'] * int(meta['n']) ** 2 * (4 if a == b else 8))])
            print(f'  {a}x{b} {q.s()}  hits {int(c.sum())}')
        for cls, nm in ((0, 'P'), (1, 'Q')):
            print(f'\nbulk cost per cell from mixed second differences, M(a+1/2, b+1/2)/3, class {nm}; a down, b across (b >= a)')
            for a in range(1, 6):
                print(f'  a={a}.5 ' + ' '.join(f"{((1/3) * M(lambda x, y: f(cls, x, y), a, b)).s():>15s}" for b in range(a, 8)))
        print('\ncost of one more unit of length, f(a, b+1) - f(a, b), per cell (divided by 3a), class P; a down, b across')
        for a in range(1, 6):
            print(f'  a={a} ' + ' '.join(f"{((1/(3*a)) * (f(0, a, b + 1) - f(0, a, b))).s():>15s}" for b in range(1, 8)))
        print('\ntriangles of side s (3s(s+1)/2 cells), -ln P')
        print('  (class P upright = the hull face\'s own shape | class P turned by 180 degrees | class Q upright | class Q turned)')
        for s in range(1, 8): print(f'  s={s} cells {3*s*(s+1)//2:3d}  {f(0, s, TRI).s():>15s} | {f(2, s, TRI).s():>15s} | {f(1, s, TRI).s():>15s} | {f(3, s, TRI).s():>15s}   hits {int(f(0, s, TRI).hits())}')
        print('second differences of the triangle cost in s (3 cells each), per cell, class P: ' +
              ' '.join(f"s={s}: {((1/3) * (f(0, s + 1, TRI) - 2.0 * f(0, s, TRI) + f(0, s - 1, TRI))).s()}" for s in range(2, 6)))
        extrap(f)
        both = lambda a, b: Q([(0.5, *f(0, a, b).terms[0][1:]), (0.5, *f(1, a, b).terms[0][1:])])
        print('\nan empty patch against a closed torus of the same shape: mean of the two classes of -ln P, less ln tau_face of the a x b torus (research/constant/out/points.txt)')
        for (a, b), lt in (((4, 4), 9.9251), ((3, 6), 11.0824), ((4, 5), 12.4865), ((2, 8), 9.4888)):
            q = both(a, b)
            print(f'  {a}x{b} perimeter {2*(a+b)}: -ln P {q.s(3)}  ln tau {lt:.4f}  difference {q.val()-lt:.3f}±{q.err():.3f}')
        show_pre(P, [(f'{a}x{a} torus', [(0, a, a, 0, 0), (2, a, a, 0, 0)]) for a in (2, 3, 4)], '\nhow a patch empties (class P)')
        return
    meta, T, P = load(rest)
    R = int(meta['R']); k = (R + 1) // 2; expo = meta['expo']; ng = meta['ng']
    print(f"hull R={R} (side k={k}, {3*k*(k+1)//2} cells a face): generations {meta['gens_each']}, face density {meta['facedensity']}, empty-face checks {meta['emptyface']}")
    def dist(a, b, I, J):
        if b == TRI: return (I, J, k - a - I - J)
        return (I, J, k + 1 - I - J - a - b)
    def pool(a, b, cond):
        """Pool the rhombus a x b over positions (I0, J0) with cond(dI, dJ, dM) true; the mirror image b x a at
           (J0, I0) is pooled with cond evaluated on the mirrored distances (dJ, dI, dM)."""
        c = np.zeros(ng); ntr = 0
        for I in range(k):
            for J in range(k):
                d = dist(a, b, I, J)
                if d[2] < 0: continue
                if cond(*d):
                    ntr += 24
                    if (0, a, b, I, J) in T: c = c + T[(0, a, b, I, J)]
        if b != TRI and a != b:
            for I in range(k):
                for J in range(k):
                    d = dist(b, a, I, J)
                    if d[2] < 0: continue
                    if cond(d[1], d[0], d[2]):
                        ntr += 24
                        if (0, b, a, I, J) in T: c = c + T[(0, b, a, I, J)]
        if ntr == 0: return None
        return Q([(1.0, c, expo * ntr)])
    ft = None
    if tor:
        mt, Tt, Pt = load(tor); ft = torus_tables(mt, Tt)
    shapes = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (4, 3), (4, 4)]
    print('\n(A) interior against torus: every unit cell >= m rows from every rim; f = -ln P; the difference hull - torus (class P)')
    for m in (4, 3, 2):
        print(f'  margin {m}:')
        for a, b in shapes:
            if a > b: continue
            q = pool(a, b, lambda dI, dJ, dM: min(dI, dJ, dM) >= m)
            if q is None or math.isnan(q.val()): continue
            line = f'    {a}x{b}  hull {q.s():>15s} hits {int(q.hits()):10d}'
            if ft:
                t = ft(0, a, b); d = q.val() - t.val(); e = math.hypot(q.err(), t.err())
                line += f'   torus {t.s():>15s}   hull-torus {d:+.4f}±{e:.4f}'
            print(line)
    print('\n(B) the same rhombus against its distance d from one rim (rim J=0; the side of a units lies along the rim;')
    print('    its other unit cells >= 3 rows from the other two rims); columns d = 0, 1, 2, 3, 4, 5; last: torus')
    for a, b in shapes:
        cells = []
        for d in range(6):
            q = pool_exact(T, k, expo, ng, a, b, d)
            cells.append(q.s(3) if q is not None else '     -     ')
        print(f'  {a} along x {b} deep: ' + ' '.join(f'{c:>13s}' for c in cells) + (f'   | {ft(0, a, b).s(3)}' if ft else ''))
    print('\n(C) corner rhombi (I0 = J0 = 0, two sides on rims) and their cost less the torus value')
    for a, b in [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)]:
        q = pool(a, b, lambda dI, dJ, dM: dI == 0 and dJ == 0)
        if q is None: continue
        line = f'  {a}x{b}  corner {q.s():>15s} hits {int(q.hits()):9d}'
        if ft:
            t = ft(0, a, b); line += f'   torus {t.s():>15s}  corner-torus {q.val()-t.val():+.3f}±{math.hypot(q.err(), t.err()):.3f}'
        print(line)
    for marg in (3, 2):
        print(f'\n(D) rim strips: w rows against a rim, l units along it, ends >= {marg} rows from the other rims; g(w, l) = -ln P; w down, l across')
        g = lambda w, l: strip(T, k, expo, ng, w, l, marg)
        for w in range(1, 6): print(f'  w={w} ' + ' '.join(f'{(g(w, l).s(3) if g(w, l) is not None else "-"):>13s}' for l in range(1, 9)))
        print('  hits: ' + ' | '.join(' '.join(f'{int(g(w, l).hits()) if g(w, l) is not None else 0}' for l in range(1, 9)) for w in range(1, 6)))
        print('  cost per cell of row w+1 from the mixed second difference [g(w+1,l+1) - g(w+1,l) - g(w,l+1) + g(w,l)]/3; w down, l across')
        for w in range(1, 5):
            cells = []
            for l in range(1, 8):
                qs = [g(w + 1, l + 1), g(w + 1, l), g(w, l + 1), g(w, l)]
                cells.append(((1 / 3) * (qs[0] - qs[1] - qs[2] + qs[3])).s() if all(q is not None for q in qs) else '-')
            print(f'  w={w}.5 ' + ' '.join(f'{c:>15s}' for c in cells))
        if ft:
            print('  the same for the torus (class P): M(w+1/2, l+1/2)/3')
            for w in range(1, 5):
                print(f'  w={w}.5 ' + ' '.join(f"{((1/3) * M(lambda x, y: ft(0, x, y), w, l)).s():>15s}" for l in range(1, 8)))
            print('  rim strips less torus, in the cost per cell from the mixed second difference')
            for w in range(1, 5):
                cells = []
                for l in range(1, 8):
                    qs = [g(w + 1, l + 1), g(w + 1, l), g(w, l + 1), g(w, l)]
                    if not all(q is not None for q in qs): cells.append('-'); continue
                    qr = (1 / 3) * (qs[0] - qs[1] - qs[2] + qs[3]); qt = (1 / 3) * M(lambda x, y: ft(0, x, y), w, l)
                    e = math.hypot(qr.err(), qt.err())
                    cells.append(f'{qr.val()-qt.val():+.4f}±{e:.4f}' if math.isfinite(e) and not math.isnan(qr.val() - qt.val()) else '-')
                print(f'  w={w}.5 ' + ' '.join(f'{c:>15s}' for c in cells))
            print('  rim strip less the same rhombus in the torus, g(w,l) - f(w,l); w down, l across')
            for w in range(1, 6):
                cells = []
                for l in range(1, 9):
                    q = g(w, l)
                    if q is None or math.isnan(q.val()) or math.isnan(ft(0, w, l).val()): cells.append('-'); continue
                    cells.append(f'{q.val()-ft(0, w, l).val():+.3f}±{math.hypot(q.err(), ft(0, w, l).err()):.3f}')
                print(f'  w={w} ' + ' '.join(f'{c:>13s}' for c in cells))
        print('  cost per cell of one more unit of length, [g(w, l+1) - g(w, l)]/(3w); w down, l across')
        for w in range(1, 6):
            cells = []
            for l in range(1, 8):
                q1, q0 = g(w, l + 1), g(w, l)
                cells.append(((1 / (3 * w)) * (q1 - q0)).s() if q1 is not None and q0 is not None else '-')
            print(f'  w={w} ' + ' '.join(f'{c:>15s}' for c in cells))
        print('  cost per cell of one more row, [g(w+1, l) - g(w, l)]/(3l); w -> w+1 down, l across')
        for w in range(0, 5):
            cells = []
            for l in range(1, 9):
                q1, q0 = g(w + 1, l), (g(w, l) if w > 0 else None)
                if w == 0: cells.append(((1 / (3 * l)) * q1).s() if q1 is not None else '-')
                else: cells.append(((1 / (3 * l)) * (q1 - q0)).s() if q1 is not None and q0 is not None else '-')
            print(f'  {w}->{w+1} ' + ' '.join(f'{c:>15s}' for c in cells))
    print('\n(E) triangles of side s (a hull face of side s as a hole): two real rims (corner), one (on a rim, >= 3 from the others; >= 2 in brackets), none (>= 3 from all), torus')
    tri = {}
    for s in range(1, 9):
        qc = pool(s, TRI, lambda dI, dJ, dM: dI == 0 and dJ == 0)
        qr = pool(s, TRI, lambda dI, dJ, dM: dJ == 0 and dI >= 3 and dM >= 3)
        qr2 = pool(s, TRI, lambda dI, dJ, dM: dJ == 0 and dI >= 2 and dM >= 2)
        qi = pool(s, TRI, lambda dI, dJ, dM: min(dI, dJ, dM) >= 3)
        qi2 = pool(s, TRI, lambda dI, dJ, dM: min(dI, dJ, dM) >= 2)
        tri[s] = (qc, qr, qi, qr2, qi2)
        fmt = lambda q: (q.s(3) + f' [{int(q.hits())}]') if q is not None and not math.isnan(q.val()) else '-'
        print(f'  s={s} cells {3*s*(s+1)//2:3d}: corner {fmt(qc):>24s}  rim {fmt(qr):>24s} ({fmt(qr2)})  interior {fmt(qi):>22s} ({fmt(qi2)})' + (f'  torus {ft(0, s, TRI).s(3)}' if ft else ''))
    json.dump({str(s): [(q.val(), q.err()) if q is not None else None for q in v] for s, v in tri.items()}, open('/dev/null', 'w'))
    anchors = {4: 6.804, 5: 9.819, 6: 13.633, 7: 18.141, 8: 23.3392}
    print('  edge-to-rim conversions: rim - corner, interior - rim (torus for the interior if given), and 2*corner - rim against ln tau')
    for s in range(1, 8):
        qc, qr, qi, qr2, qi2 = tri[s]
        if qc is None or qr2 is None or math.isnan(qc.val()) or math.isnan(qr2.val()): continue
        qR = qr if (qr is not None and not math.isnan(qr.val()) and qr.hits() > 50) else qr2
        lam1 = qR - qc
        line = f'  s={s}: rim-corner {lam1.s(3)}'
        if ft and not math.isnan(ft(0, s, TRI).val()):
            t = ft(0, s, TRI); line += f'  torus-rim {t.val()-qR.val():.3f}±{math.hypot(t.err(), qR.err()):.3f}'
        F = 2.0 * qc - qR
        line += f'   2*corner-rim {F.s(3)}'
        if s in anchors: line += f'   ln tau {anchors[s]:.3f}  difference {F.val()-anchors[s]:.3f}'
        print(line)
    print('  second differences in s, per cell (divided by 3): corner | rim (margin 2) | ln tau of hull faces: k=5 0.2663, k=6 0.2313, k=7 0.2300')
    for s in range(2, 7):
        out = []
        for idx in (0, 3):
            qs = [tri[s + 1][idx], tri[s][idx], tri[s - 1][idx]]
            out.append(((1 / 3) * (qs[0] - 2.0 * qs[1] + qs[2])).s() if all(q is not None and not math.isnan(q.val()) for q in qs) else '-')
        print(f'  s={s}: {out[0]:>16s} | {out[1]:>16s}')
    sel = []
    for a in (2, 3, 4):
        sel.append((f'{a}x{a} corner', [(0, a, a, 0, 0)]))
        sel.append((f'{a}x{a} on a rim', [(0, a, a, I, 0) for I in range(3, k) if k + 1 - I - 2 * a >= 3] + [(0, a, a, 0, J) for J in range(3, k) if k + 1 - J - 2 * a >= 3]))
        sel.append((f'{a}x{a} one row in', [(0, a, a, I, 1) for I in range(3, k) if k - I - 2 * a >= 3] + [(0, a, a, 1, J) for J in range(3, k) if k - J - 2 * a >= 3]))
        sel.append((f'{a}x{a} interior(>=3)', [(0, a, a, I, J) for I in range(3, k) for J in range(3, k) if k + 1 - I - J - 2 * a >= 3]))
        sel.append((f'{a}x{a} interior(>=2)', [(0, a, a, I, J) for I in range(2, k) for J in range(2, k) if k + 1 - I - J - 2 * a >= 2]))
    show_pre(P, sel, '\n(F) how a patch empties, by position')

def pool_exact(T, k, expo, ng, a, b, d):
    """a units along the rim J=0, b deep, at distance d: entries (a, b, I0, J0=d) with I0 >= 3, dM >= 3, pooled with
       the mirror (b, a, I0=d, J0)."""
    c = np.zeros(ng); ntr = 0
    for I in range(3, k):
        dM = k + 1 - I - d - a - b
        if dM < 3: continue
        ntr += 24
        if (0, a, b, I, d) in T: c = c + T[(0, a, b, I, d)]
        ntr += 24
        if (0, b, a, d, I) in T: c = c + T[(0, b, a, d, I)]
    if ntr == 0: return None
    return Q([(1.0, c, expo * ntr)])

_sc = {}
def strip(T, k, expo, ng, w, l, marg):
    key = (w, l, marg, id(T))
    if key in _sc: return _sc[key]
    c = np.zeros(ng); ntr = 0
    for I in range(marg, k):
        dM = k + 1 - I - 0 - l - w
        if dM < marg: continue
        ntr += 48
        if (0, l, w, I, 0) in T: c = c + T[(0, l, w, I, 0)]
        if (0, w, l, 0, I) in T: c = c + T[(0, w, l, 0, I)]
    q = Q([(1.0, c, expo * ntr)]) if ntr else None
    _sc[key] = q
    return q

if __name__ == '__main__':
    main()
