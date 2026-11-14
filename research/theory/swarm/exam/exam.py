"""Examiner's runner: drv16 (exam copy of research/theory/exponent/drv.c, PB = 16) on xp's graphs, chunked and
restartable, every chunk kept (batch means). Results in research/scratch/exam/runs_<tag>.json.

  python3 exam.py <job> [args]      jobs: v1 v2 v3 pe1 e1 e2 e3 se2 report
"""
import json, os, sys, time, zlib, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory', 'exponent'))
import xp
SCR = os.path.join(ROOT, 'research', 'scratch', 'exam')
os.makedirs(SCR, exist_ok=True)
BIN = os.path.join(SCR, 'drv16')


def build():
    src = os.path.join(HERE, 'drv16.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-DW=4', '-DPB=16', '-o', BIN, src, '-lm'])


def gfile(g):
    fn = os.path.join(SCR, 'g_%s.bin' % g['name'])
    xp.write_graph(g, fn)
    return fn


def nogap(g):
    g['lines'] = [(f & ~2, c) for f, c in g['lines']]
    return g


def notched(L):
    """toy_strip(16, L) with cells (row 0, col 0), (row 0, col 1) removed (dead for ever)."""
    g = nogap(xp.toy_strip(16, L))
    gone = {0, 1}                       # idx(y, x) = y * L + x
    keep = [i for i in range(g['N']) if i not in gone]
    new = {o: n for n, o in enumerate(keep)}
    nb = np.array([[new.get(j, -1) if j >= 0 else -1 for j in g['nb'][i]] for i in keep], int)
    lines = [(f, [new[c] for c in cl if c in new]) for f, cl in g['lines']]
    return dict(g, name='toy_notch_16x%d' % L, N=len(keep), nb=nb, lines=lines)


def run(key, g, rule, p, T0, deaths, maxsec, rho=None, nev=None, tag='main', chunk=20000):
    build()
    fn = os.path.join(SCR, 'runs_%s.json' % tag)
    db = json.load(open(fn)) if os.path.exists(fn) else {}
    nev = nev or g.get('nedge', 1)
    rec = db.get(key) or dict(chunks=[], nev=nev, graph=g['name'], N=g['N'], A=len(g['lines'][0][1]), p=p, T0=T0,
                              rho=rho, rule=list(rule))
    gf = gfile(g)
    out = os.path.join(SCR, 'tmp_%s_%s.txt' % (tag, key))
    t0 = time.time(); gens = rec.get('lastgens', chunk)
    while time.time() - t0 < maxsec:
        ev = np.sum([c['deaths_by_event'] for c in rec['chunks']], 0) if rec['chunks'] else [0]
        if sum(np.atleast_1d(ev)[:nev]) >= deaths:
            break
        seed = 7919 * len(rec['chunks']) + 104729 * (zlib.crc32(key.encode()) % 9973) + 31
        cmd = [BIN, 'qsd', gf, str(rule[0]), str(rule[1]), str(p), str(seed), str(T0), str(int(gens)), out]
        cmd.append(','.join('%.6f' % r for r in (rho if rho else [0.5]))); cmd.append('0')
        tc = time.time(); subprocess.run(cmd, check=True); dt = time.time() - tc
        d = xp.read_out(out)
        c = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in d.items()}
        c['secs'] = dt; c['seed'] = seed
        rec['chunks'].append(c)
        gens = int(min(max(gens * min(4.0, 60.0 / max(dt, 1e-3)), 2000), 2e8)); rec['lastgens'] = gens
        db = json.load(open(fn)) if os.path.exists(fn) else {}
        db[key] = rec
        json.dump(db, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
    s = summ(rec)
    print('%-22s chunks %d secs %.0f expo %.3g deaths %d other %d settles %d maxage %d  ln tau %.4f +- %.4f' %
          (key, len(rec['chunks']), s['secs'], s['expo'], s['deaths'], s['other'], s['settles'], s['maxage'], s['lntau'],
           s['err']), flush=True)
    return rec


def summ(rec, events=None):
    ch = rec['chunks']; nev = rec['nev']
    ev = np.sum([np.atleast_1d(c['deaths_by_event']) for c in ch], 0)
    events = events if events is not None else list(range(nev))
    d = int(sum(ev[e] for e in events)); expo = sum(c['exposure'] for c in ch)
    h = d / (len(events) * expo) if d else float('nan')
    hist = np.sum([np.atleast_1d(c['hist']) for c in ch], 0)
    tr = np.sum([np.atleast_1d(c['trans']) for c in ch], 0).reshape(32, 32)
    return dict(deaths=d, other=int(ev.sum() - sum(ev[:nev])), expo=expo, h=h, lntau=-np.log(h), err=1 / np.sqrt(d) if d else np.nan,
                settles=int(sum(c['settles'] for c in ch)), maxage=int(max(c.get('maxage', 0) for c in ch)),
                secs=sum(c['secs'] for c in ch), hist=hist, trans=tr, ev=ev)


def profile(rec, line=0, lags=(1, 2, 3, 4)):
    """mean count of profile line `line` (0 = the dying line) at the given lags, pooled over profile groups, with
    batch-means errors over chunks."""
    ch = rec['chunks']
    ng = sum(1 for k in ch[0] if k.startswith('profn'))
    n = np.array([sum(c['profn%d' % gq] for gq in range(ng)) for c in ch])
    S = np.array([sum(np.array(c['prof%d_%d' % (gq, line)]) for gq in range(ng)) for c in ch])  # chunks x 64
    tot = n.sum(); mean = S.sum(0) / tot
    out = []
    for j in lags:
        m = mean[j - 1]
        ok = n > 0
        # ratio estimator, batch means: var = sum (S_c - m n_c)^2 / (sum n)^2 * k/(k-1)
        k = ok.sum()
        var = ((S[ok, j - 1] - m * n[ok]) ** 2).sum() / tot ** 2 * k / max(k - 1, 1)
        out.append((j, m, np.sqrt(var), k))
    return tot, out


if __name__ == '__main__':
    job = sys.argv[1]
    TOY, GUMP = xp.TOY, xp.GUMP
    if job == 'v1':
        for L in (12, 16):
            run('v1_L%d' % L, nogap(xp.toy_model(1, L)), TOY, 0.4, 50, 4000, 120, rho=[0.472, 0.472], tag='valid')
    elif job == 'v2':
        run('v2_16x16', nogap(xp.toy_strip(16, 16)), TOY, 0.4, 300, 4000, 200, tag='valid')
    elif job == 'v3':
        run('v3_slab3x4m12', nogap(xp.gump_slab(3, 4, 12)), GUMP, 0.35, 300, 4000, 200, tag='valid')
    elif job == 'pe1':
        L = int(sys.argv[2]); tgt = {30: 1500, 34: 600, 38: 250}[L]; cap = {30: 15, 34: 25, 38: 50}[L] * 60
        run('pe1_L%d' % L, nogap(xp.toy_model(1, L)), TOY, 0.4, 50, tgt, cap, rho=[0.472, 0.472], tag='pe1')
    elif job == 'e1':
        for L in map(int, sys.argv[2].split(',')):
            run('e1_L%d' % L, notched(L), TOY, 0.4, 300, 600, 12 * 60, nev=1, tag='e1')
    elif job == 'e2':
        for L, tgt, cap in ((32, 400, 15), (36, 300, 25)):
            run('e2_L%d' % L, nogap(xp.toy_strip(16, L)), TOY, 0.4, 300, tgt, cap * 60, tag='e2')
    elif job == 'e3':
        run('e3_slab5x4m8', nogap(xp.gump_slab(5, 4, 8)), GUMP, 0.35, 300, 3000, 20 * 60, tag='e3')
    elif job == 'se2':
        for a, b in ((3, 4), (4, 4)):
            run('se2_gump_%dx%d' % (a, b), nogap(xp.gump_slab_model(a, b, 6)), GUMP, 0.35, 300, 4000, 600, rho=[0.5, 0.5], tag='se2')
        for L in (16, 20):
            run('se2_toy_L%d' % L, nogap(xp.toy_model(8, L)), TOY, 0.4, 300, 4000, 600, rho=[0.5, 0.5], tag='se2')
