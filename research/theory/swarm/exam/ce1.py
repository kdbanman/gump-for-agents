"""C-E1 (counting, revised): gump hulls with soups symmetric under the mirror (x, y, z) -> (y, x, z), and the V6
validation. Engine: exam/t2dx.c (t2d.c + a 262144 snapshot), graphs from research/theory/exponent/xp.gump_hull.

  python3 ce1.py v6            t2dx vs t2d bit-identical on a short run; asymmetric R = 7 hull vs fluct's 6.804
  python3 ce1.py run R SECS    mirror-symmetric hull R (restartable; tops up by SECS of wall time)
  python3 ce1.py report
"""
import json, os, struct, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory', 'exponent'))
import xp
SCR = os.path.join(ROOT, 'research', 'scratch', 'exam')
EXE = os.path.join(SCR, 't2dx')
B, S = 48, 56                                        # B45/S345
FIXED = [0, 1, 6, 7]                                 # gump_hull face order (sx, sy, sz) loops: sx == sy


def graph(R, sym):
    g = xp.gump_hull(R)
    cells = xp.hull_cells(R); ix = {p: i for i, p in enumerate(cells)}
    orb = -np.ones(len(cells), np.int32); n = 0
    for i, p in enumerate(cells):
        if orb[i] >= 0: continue
        imgs = {p, (p[1], p[0], p[2])} if sym else {p}
        for q in imgs: orb[ix[q]] = n
        n += 1
    fn = os.path.join(SCR, 'g_t2d_hull_R%d_%s.bin' % (R, 'mxy' if sym else 'none'))
    with open(fn, 'wb') as f:
        nb = np.asarray(g['nb'], '<i4')
        f.write(struct.pack('<ii', len(cells), nb.shape[1])); f.write(nb.tobytes()); f.write(orb.astype('<i4').tobytes())
        f.write(struct.pack('<ii', n, len(g['lines'])))
        for flag, cl in g['lines']:
            f.write(struct.pack('<ii', flag, len(cl))); f.write(np.asarray(cl, '<i4').tobytes())
        f.write(struct.pack('<i', len(g['events'])))
        for ev in g['events']:
            f.write(struct.pack('<i', len(ev))); f.write(np.asarray(ev, '<i4').tobytes())
    return fn, n, len(cells)


def read(fn):
    d = {}
    for line in open(fn):
        k, *v = line.split(); d[k] = [float(t) for t in v]
    return d


def run(key, R, sym, secs, T0=200, p=0.35, tag='ce1'):
    fn = os.path.join(SCR, 'runs_%s.json' % tag)
    db = json.load(open(fn)) if os.path.exists(fn) else {}
    rec = db.get(key) or dict(chunks=[], R=R, sym=sym)
    gf, _, N = graph(R, sym)
    gens = rec.get('lastgens', 5000); t0 = time.time()
    out = os.path.join(SCR, 'tmp_%s.txt' % key)
    while time.time() - t0 < secs:
        seed = 1000003 * R + 7919 * len(rec['chunks']) + (17 if sym else 5)
        tc = time.time()
        subprocess.run([EXE, 'qsd', gf, str(B), str(S), str(p), str(seed), str(T0), str(int(gens)), out], check=True)
        dt = time.time() - tc
        d = read(out); d['secs'] = dt; rec['chunks'].append(d)
        gens = int(min(max(gens * min(4.0, 120.0 / max(dt, 1e-3)), 2000), 1e8)); rec['lastgens'] = gens
        db = json.load(open(fn)) if os.path.exists(fn) else {}
        db[key] = rec; json.dump(db, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
    return summ(rec)


def summ(rec):
    ch = rec['chunks']
    ev = np.sum([c['deaths_by_event'] for c in ch], 0); expo = sum(c['exposure'][0] for c in ch)
    fx = ev[FIXED].sum(); al = ev.sum()
    return dict(expo=expo, ev=ev, fixed=int(fx), all=int(al), lnfix=np.log(4 * expo / fx) if fx else np.inf,
                lnall=np.log(8 * expo / al) if al else np.inf, err=1 / np.sqrt(fx) if fx else np.nan,
                settles=int(sum(c['settles'][0] for c in ch)), maxage=int(max(c['maxage'][0] for c in ch)),
                secs=sum(c['secs'] for c in ch))


if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'v6':
        subprocess.check_call(['gcc', '-O3', '-march=native', '-DW=4', '-o', os.path.join(SCR, 't2d_orig'),
                               os.path.join(ROOT, 'research', 'toy2d', 't2d.c'), '-lm'])
        gf, _, _ = graph(7, False)
        outs = []
        for exe in (os.path.join(SCR, 't2d_orig'), EXE):
            o = os.path.join(SCR, 'v6_%s.txt' % os.path.basename(exe))
            subprocess.run([exe, 'qsd', gf, str(B), str(S), '0.35', '11', '200', '30000', o], check=True)
            outs.append([l for l in open(o) if not l.startswith('maxage')])
        print('t2dx vs t2d on R = 7, 30000 generations:', 'IDENTICAL' if outs[0] == outs[1] else 'DIFFERENT')
        s = run('v6_R7_none', 7, False, 60, tag='valid')
        print('asymmetric R = 7: ln tau_face = %.4f +- %.4f (%d deaths; fluct 6.804 +- 0.003)' % (s['lnall'], 1 / np.sqrt(s['all']), s['all']))
    elif job == 'run':
        R, secs = int(sys.argv[2]), float(sys.argv[3])
        s = run('mxy_R%d' % R, R, True, secs)
        print('R=%d expo %.3g fixed-face deaths %d of %d first deaths; ln tau_fix %.4f +- %.4f; settles %d maxage %d secs %.0f'
              % (R, s['expo'], s['fixed'], s['all'], s['lnfix'], s['err'], s['settles'], s['maxage'], s['secs']))
    elif job == 'report':
        db = json.load(open(os.path.join(SCR, 'runs_ce1.json')))
        for k, r in sorted(db.items()):
            s = summ(r)
            print(k, 'A', {13: 84, 15: 108, 17: 135}[r['R']], 'ln tau_fix %.4f +- %.4f' % (s['lnfix'], s['err']), 'fixed', s['fixed'],
                  'all', s['all'], 'by face', s['ev'].astype(int).tolist(), 'settles', s['settles'], 'maxage', s['maxage'], 'secs %.0f' % s['secs'])
