#!/usr/bin/env python3
"""Driver for ring.c (thin torus, packed rings).

    python3 run.py validate                       # ring.c against the reference stepper (= oracle) and the engine
    python3 run.py run TAG det|model b m_or_w SECONDS [T0] [GS] [rho16] [WALL]   # chunks until SECONDS; resumable
    python3 run.py stats TAG...                   # ln tau per tag from the chunk files (prefix match with *)

Chunk files: research/scratch/thin/<TAG>/c<k>.txt (one per chunk, seed = hash of tag and k). A run can be killed
at any time: finished chunks are kept, the unfinished one is lost.
"""
import glob, hashlib, math, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'thin')
BIN = os.path.join(OUT, 'ring')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
sys.path.insert(0, HERE)
import thin  # noqa: E402

P0 = 26214          # soup density 0.4 (x 65536)
RHO = 26112         # coin density 102/256 = 0.3984 (x 65536): the thin torus's bulk density (layers 2-5: 0.397)


def build():
    os.makedirs(OUT, exist_ok=True)
    src = [os.path.join(HERE, f) for f in ('ring.c', 'nbr.h')]
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < max(map(os.path.getmtime, src)):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', BIN + '.new', src[0]])
        os.replace(BIN + '.new', BIN)


def ring(mode, b, mw, seed, gens, T0, out, cap=0, gs=0, rho=RHO, p0=P0, extra=(), notch=0):
    subprocess.check_call([BIN, mode, str(b), str(mw), str(rho), str(p0), str(seed), str(gens), str(T0), str(cap),
                           str(gs), out, *extra, *(('-n', str(notch)) if notch else ())])


def parse(path):
    d = {}
    with open(path) as f:
        lines = f.read().splitlines()
    h = lines[0].split(); d['head'] = dict(zip(h[0::2], h[1::2]))
    t = lines[1].split()[1:]; d['tot'] = {k: float(v) for k, v in zip(t[0::2], t[1::2])}
    for line in lines[2:]:
        p = line.split(); d[p[0]] = np.array(p[1:], float)
    return d


def read_dump(path, b, nt):
    """dump -> array [gens + 1, lanes, nt * 3 * b] of 0/1"""
    rows = {}
    for line in open(path):
        p = line.split(); g, l = int(p[0]), int(p[1])
        words = [int(x, 16) for x in p[3:]]
        bits = np.array([(w >> c) & 1 for w in words for c in range(b)], np.int8)
        rows[(g, l)] = bits
    G = max(g for g, _ in rows) + 1; NLn = max(l for _, l in rows) + 1
    return np.array([[rows[(g, l)] for l in range(NLn)] for g in range(G)])


def validate_dump(mode, b, mw, gens, seed=5, notch=0):
    """Every lane, every generation: the dumped next state is the reference stepper's image of the dumped state,
    except where a life ended; ends (deaths, ages) are recomputed and compared with ring's own tallies."""
    nt = mw + 2 if mode == 'model' else mw
    dp = os.path.join(OUT, f'dump_{os.getpid()}.txt'); out = os.path.join(OUT, f'vout_{os.getpid()}.txt')
    ring(mode, b, mw, seed, gens, 0, out, extra=('-d', dp), notch=notch)
    D = read_dump(dp, b, nt); r = parse(out)
    nb = thin.graph(b, nt)
    nd = mw * 3 * b
    faces = [np.arange(3 * b)] + ([np.arange((mw - 1) * 3 * b, mw * 3 * b)] if mode == 'det' else [])
    wall = np.zeros(nd, bool)                       # face cells held dead: sites 0..notch-1 = {Z_s, Y_s, X_{s+1}}
    for f in faces:
        for s_ in range(notch):
            wall[f[0] + 2 * b + s_] = wall[f[0] + b + s_] = wall[f[0] + (s_ + 1) % b] = True
    assert not D[:, :, :nd][:, :, wall].any(), 'a wall cell is alive in the dump'
    bad = 0; deaths = 0; expo = 0; born = np.zeros(D.shape[1], int); other = 0; steps = 0
    for g in range(gens):
        for l in range(D.shape[1]):
            nxt = thin.step_ref(D[g, l], nb)[:nd]
            nxt[wall] = 0
            nde = sum(int(nxt[f].sum() == 0) for f in faces)
            got = D[g + 1, l][:nd]
            steps += 1
            if nde:
                deaths += nde; expo += g + 1 - born[l]; born[l] = g + 1
            elif not (got == nxt).all():
                if (g + 1) % 840 == 0:
                    other += 1; expo += g + 1 - born[l]; born[l] = g + 1   # snapshot event (not re-derived here)
                else:
                    bad += 1
    expo += int((gens - born).sum())
    ok = bad == 0 and deaths == int(r['tot']['alldeaths']) and (other > 0 or expo == int(r['expo'].sum()))
    msg = (f'validate_dump {mode} b={b} layers={mw} wall={notch}: {steps} lane-steps, {bad} wrong, deaths {deaths} '
           f'(ring: {int(r["tot"]["alldeaths"])}), exposure {expo} (ring: {int(r["expo"].sum())}), snapshot ends {other}')
    if mode == 'model':
        nz = D[:gens, :, nd:].astype(float)                  # coins
        dens = nz.mean(); n = nz.size
        z = (dens - RHO / 65536) / math.sqrt(dens * (1 - dens) / n)
        ac = np.mean((nz[1:] - dens) * (nz[:-1] - dens)) / (dens * (1 - dens))      # lag 1 in time
        sp = np.mean((nz[:, :, 1:] - dens) * (nz[:, :, :-1] - dens)) / (dens * (1 - dens))   # adjacent cells
        ln = np.mean((nz[:, 1:] - dens) * (nz[:, :-1] - dens)) / (dens * (1 - dens))  # adjacent lanes
        msg += (f'; coins: density {dens:.5f} (want {RHO / 65536:.5f}, z = {z:+.2f}), correlation in time {ac:+.5f}, '
                f'between cells {sp:+.5f}, between lanes {ln:+.5f} (1/sqrt(n) = {1 / math.sqrt(n):.5f})')
        ok = ok and abs(z) < 4 and max(abs(ac), abs(sp), abs(ln)) < 5 / math.sqrt(n)
    for f in (dp, out):
        os.remove(f)
    print(msg, 'OK' if ok else 'FAIL')
    return ok


def validate_engine(b, m, gens, seed=3):
    """Lane 0 from a listed soup against the engine on the cubic b-torus (b copies), population every generation."""
    rng = np.random.default_rng(seed)
    n = m * 3 * b
    live = np.nonzero(rng.random(n) < 0.4)[0]
    ini = os.path.join(OUT, f'ini_{os.getpid()}.txt'); open(ini, 'w').write('\n'.join(map(str, live)))
    dp = os.path.join(OUT, f'dump_{os.getpid()}.txt'); out = os.path.join(OUT, f'vout_{os.getpid()}.txt')
    ring('det', b, m, seed, gens, 0, out, extra=('-i', ini, '-d', dp))
    mine = []
    for line in open(dp):
        p = line.split()
        if p[1] == '0':
            mine.append(sum(bin(int(x, 16)).count('1') for x in p[3:]))
    pts = set()
    for i in live:
        t, o, c = i // (3 * b), (i // b) % 3, i % b
        p0 = thin.doubled(t, o, c)
        for s in range(b):
            pts.add(((p0[0] + 2 * s) % (2 * b), (p0[1] + 2 * s) % (2 * b), (p0[2] - 4 * s) % (2 * b)))
    assert len(pts) == b * len(live)
    cf = os.path.join(OUT, f'cells_{os.getpid()}.txt'); open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    pl = os.path.join(OUT, f'pl_{os.getpid()}.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(b), '--gens', str(gens), '--no-halt', '--poplog', pl],
                   check=True, capture_output=True)
    ref = {int(l.split()[0]): int(l.split()[1]) for l in open(pl)}
    # compare until lane 0's first reseed (a face death): the engine has no reseeding
    nmatch = 0
    for g, v in enumerate(mine):
        if g in ref and ref[g] == v * b:
            nmatch += 1
        else:
            break
    for f in (ini, dp, out, cf, pl):
        os.remove(f)
    ok = nmatch >= min(gens, 200)
    print(f'validate_engine b={b} m={m}: populations equal to the engine (x{b} copies) for the first {nmatch} generations '
          f'of {gens} (a mismatch after a face death is the reseeding); {len(set(mine[:nmatch]))} distinct', 'OK' if ok else 'FAIL')
    return ok, nmatch


def chunk_seed(tag, k):
    return int(hashlib.sha256(f'{tag}:{k}'.encode()).hexdigest()[:12], 16)


def run(tag, mode, b, mw, seconds, T0=256, gs=0, rho=RHO, gens=None, notch=0):
    build()
    d = os.path.join(OUT, tag); os.makedirs(d, exist_ok=True)
    t0 = time.time(); k = len(glob.glob(os.path.join(d, 'c*.txt')))
    # chunk length: about 60 s
    if gens is None:
        tt = time.time(); ring(mode, b, mw, 1, 20000, T0, os.path.join(OUT, f'probe_{os.getpid()}.txt'), gs=gs, rho=rho, notch=notch)
        os.remove(os.path.join(OUT, f'probe_{os.getpid()}.txt'))
        gens = max(20000, int(20000 * 60 / max(time.time() - tt, 1e-3)))
    while time.time() - t0 < seconds:
        tmp = os.path.join(d, f'tmp_{os.getpid()}')
        ring(mode, b, mw, chunk_seed(tag, k), gens, T0, tmp, gs=gs, rho=rho, notch=notch)
        os.replace(tmp, os.path.join(d, f'c{k}.txt')); k += 1
    print(f'{tag}: {k} chunks', flush=True)


def load(tag):
    fs = sorted(glob.glob(os.path.join(OUT, tag, 'c*.txt')))
    if not fs:
        return None
    acc = None
    for f in fs:
        r = parse(f)
        if acc is None:
            acc = r; acc['n'] = 1; continue
        for k, v in r.items():
            if k == 'head':
                assert all(v[q] == acc['head'][q] for q in ('mode', 'b', 'layers', 'T0', 'rho16')) \
                    and v.get('notch', '0') == acc['head'].get('notch', '0')
            elif k == 'tot':
                for kk in v:
                    acc['tot'][kk] += v[kk]
            elif k in acc and len(acc[k]) == len(v):
                acc[k] = acc[k] + v
            elif k not in acc:
                acc[k] = v
        acc['n'] += 1
    return acc


def lntau(acc):
    """per-face ln tau = ln(nface * exposure / deaths), error 1/sqrt(deaths)"""
    nface = 2 if acc['head']['mode'] == 'det' else 1
    F, E = acc['tot']['deaths'], acc['tot']['expo']
    if F == 0:
        return float('nan'), float('nan'), 0
    return math.log(nface * E / F), 1 / math.sqrt(F), int(F)


def stats(tags):
    for pat in tags:
        for d in sorted(glob.glob(os.path.join(OUT, pat))):
            tag = os.path.basename(d); acc = load(tag)
            if acc is None:
                continue
            lt, er, F = lntau(acc); h = acc['head']; t = acc['tot']
            # hazard in three age classes of the binned record (ages >= T0)
            T0 = int(h['T0']); ex, de = acc['expo'], acc['deaths']
            ks = [k for k in range(len(ex)) if (1 << k) - 1 >= T0 and ex[k] > 0]
            thirds = ''
            if ks:
                cum = np.cumsum(ex[ks]); cuts = np.searchsorted(cum, [cum[-1] / 3, 2 * cum[-1] / 3])
                parts = [ks[:cuts[0] + 1], ks[cuts[0] + 1:cuts[1] + 1], ks[cuts[1] + 1:]]
                nf = 2 if h['mode'] == 'det' else 1
                thirds = ' '.join(f'{math.log(nf * ex[p].sum() / de[p].sum()):.3f}' if p and de[p].sum() > 0 else '-' for p in parts)
            print(f'{tag:28s} {h["mode"]:5s} b={h["b"]:>2s} A={3 * int(h["b"]):3d} layers={h["layers"]} chunks={acc["n"]:4d} '
                  f'deaths={F:8d} ln tau = {lt:.4f} +- {er:.4f}  settled={int(t["settled"])} interior={int(t["interior"])} '
                  f'both={int(t["both"])}  by age: {thirds}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'validate':
        build()
        ok = True
        ok &= thin.oracle_check(16, 8, 300)
        ok &= thin.oracle_check(12, 5, 200)
        for (mode, b, mw, g) in [('det', 16, 8, 400), ('det', 5, 8, 300), ('det', 64, 8, 150), ('det', 7, 3, 1000),
                                 ('model', 16, 5, 300), ('model', 6, 1, 2000), ('model', 64, 2, 150), ('model', 9, 3, 1000)]:
            ok &= validate_dump(mode, b, mw, g)
        for (mode, b, mw, g, nn) in [('det', 12, 8, 600, 3), ('det', 64, 8, 100, 5), ('model', 9, 1, 2000, 3), ('model', 20, 5, 300, 4)]:
            ok &= validate_dump(mode, b, mw, g, notch=nn)
        for (b, m, g) in [(16, 8, 3000), (24, 8, 3000), (40, 8, 1500)]:
            ok &= validate_engine(b, m, g)[0]
        print('ALL OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)
    elif cmd == 'run':
        tag, mode, b, mw, seconds = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
        T0 = int(sys.argv[7]) if len(sys.argv) > 7 else 256
        gs = int(sys.argv[8]) if len(sys.argv) > 8 else 0
        rho = int(sys.argv[9]) if len(sys.argv) > 9 else RHO
        notch = int(sys.argv[10]) if len(sys.argv) > 10 else 0
        run(tag, mode, b, mw, seconds, T0, gs, rho, notch=notch)
    elif cmd == 'stats':
        stats(sys.argv[2:] or ['*'])
